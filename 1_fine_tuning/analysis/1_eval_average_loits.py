"""Uniform MoE baseline: average the logits from three LoRA models."""

import json
import math
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    jaccard_score,
    precision_score,
    roc_auc_score,
)
from torch.utils.data import DataLoader, Dataset, SequentialSampler
from tqdm import tqdm
from transformers import AutoTokenizer

from model import LLamaModel


MAX_LEN = 2000
CLASSES = 2
TEST_FILE = Path(
    "/mnt/data_218/home1/Cool_Chen/OOD_data_OUD_corhot/"
    "data_by_junhui_right/811_test_ood.jsonl"
)
BATCH_SIZE = 1

# Fill in the three base model IDs and LoRA checkpoint directories here.
model_id_1 = "/path/to/base_model_1"
model_id_2 = "/path/to/base_model_2"
model_id_3 = "/path/to/base_model_3"

checkpoint_path_1 = Path("/path/to/checkpoint_1")
checkpoint_path_2 = Path("/path/to/checkpoint_2")
checkpoint_path_3 = Path("/path/to/checkpoint_3")


def label_to_one_hot(label):
    return [0, 1] if label == "1" else [1, 0]


def get_data(file_path):
    sentences = []
    labels = []
    with file_path.open("r", encoding="utf-8") as reader:
        for line in reader:
            sample = json.loads(line)
            sentences.append(sample["icd"])
            labels.append(label_to_one_hot(sample["label"]))
    return sentences, labels


class TextDataset(Dataset):
    def __init__(self, sentences, labels):
        self.sentences = sentences
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return {
            "sentence": self.sentences[index],
            "labels": self.labels[index],
        }


def make_dataloader(test_file, tokenizers, batch_size):
    sentences, labels = get_data(test_file)
    dataset = TextDataset(sentences, torch.tensor(labels, dtype=torch.float32))

    def collate_batch(features):
        batch_labels = torch.stack([feature["labels"] for feature in features])
        batch_sentences = [feature["sentence"] for feature in features]
        model_inputs = [
            tokenizer(
                batch_sentences,
                padding=True,
                truncation=True,
                max_length=MAX_LEN,
                pad_to_multiple_of=8,
                return_tensors="pt",
            )
            for tokenizer in tokenizers
        ]
        return model_inputs, batch_labels

    return DataLoader(
        dataset,
        sampler=SequentialSampler(dataset),
        batch_size=batch_size,
        collate_fn=collate_batch,
    )


def compute_ece_from_logits(logits, labels, n_bins=10):
    probabilities = F.softmax(logits.float(), dim=1)
    confidences, predictions = probabilities.max(dim=1)
    correct = predictions.eq(labels).float()
    ece = torch.tensor(0.0)
    boundaries = torch.linspace(0, 1, n_bins + 1)

    for index in range(n_bins):
        lower = boundaries[index]
        upper = boundaries[index + 1]
        if index == n_bins - 1:
            in_bin = (confidences >= lower) & (confidences <= upper)
        else:
            in_bin = (confidences >= lower) & (confidences < upper)

        proportion = in_bin.float().mean()
        if proportion.item() > 0:
            accuracy = correct[in_bin].mean()
            confidence = confidences[in_bin].mean()
            ece += proportion * torch.abs(accuracy - confidence)

    return ece.item()


def evaluate_uniform_moe(models, dataloader):
    """Average three models' raw logits, then evaluate the final prediction."""
    if len(models) != 3:
        raise ValueError(f"Uniform MoE requires exactly 3 models, got {len(models)}")

    for model in models:
        model.eval()

    all_logits = []
    all_labels = []

    for model_inputs, labels in tqdm(dataloader):
        labels = labels.cuda(non_blocking=True)

        model_logits = []
        with torch.inference_mode():
            for model, inputs in zip(models, model_inputs):
                logits, _ = model(
                    input_ids=inputs["input_ids"].cuda(non_blocking=True),
                    attention_mask=inputs["attention_mask"].cuda(non_blocking=True),
                    labels=labels,
                )
                model_logits.append(logits.float().cpu())

        # Uniform MoE / Logit Averaging:
        # final_logits = (logits_1 + logits_2 + logits_3) / 3
        final_logits = torch.stack(model_logits, dim=0).mean(dim=0)
        all_logits.append(final_logits)
        all_labels.append(labels.argmax(dim=1).cpu())

    final_logits = torch.cat(all_logits, dim=0)
    gold = torch.cat(all_labels, dim=0)
    predictions = final_logits.argmax(dim=1)
    positive_probabilities = F.softmax(final_logits, dim=1)[:, 1]

    gold_np = gold.numpy()
    predictions_np = predictions.numpy()
    probabilities_np = positive_probabilities.numpy()

    print("precision", precision_score(gold_np, predictions_np, zero_division=0))
    print("F1", f1_score(gold_np, predictions_np, zero_division=0))
    print("jaccard", jaccard_score(gold_np, predictions_np, zero_division=0))
    print("auprc", average_precision_score(gold_np, probabilities_np))
    print("auroc", roc_auc_score(gold_np, probabilities_np))

    order = np.argsort(-probabilities_np)
    sorted_gold = gold_np[order]
    total_positive = gold_np.sum()
    for percentage in (0.01, 0.02, 0.05, 0.10):
        k = math.ceil(len(sorted_gold) * percentage)
        true_positive = sorted_gold[:k].sum()
        ppv = true_positive / k if k > 0 else 0
        recall = true_positive / total_positive if total_positive > 0 else 0
        print(percentage, "--the PPV is", ppv, "the recall is", recall)

    print("ECE:", compute_ece_from_logits(final_logits, gold, n_bins=10))


def main():
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required to evaluate these three models.")

    checkpoint_paths = [checkpoint_path_1, checkpoint_path_2, checkpoint_path_3]
    for checkpoint_path in checkpoint_paths:
        if not checkpoint_path.is_dir():
            raise FileNotFoundError(f"Checkpoint directory not found: {checkpoint_path}")
    if not TEST_FILE.is_file():
        raise FileNotFoundError(f"Test file not found: {TEST_FILE}")

    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    tokenizers = [
        AutoTokenizer.from_pretrained(model_id_1),
        AutoTokenizer.from_pretrained(model_id_2),
        AutoTokenizer.from_pretrained(model_id_3),
    ]
    for tokenizer in tokenizers:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
    dataloader = make_dataloader(TEST_FILE, tokenizers, BATCH_SIZE)

    model_1 = LLamaModel(
        CLASSES,
        adapter_path=str(checkpoint_path_1),
        model_id=model_id_1,
    )
    model_2 = LLamaModel(
        CLASSES,
        adapter_path=str(checkpoint_path_2),
        model_id=model_id_2,
    )
    model_3 = LLamaModel(
        CLASSES,
        adapter_path=str(checkpoint_path_3),
        model_id=model_id_3,
    )

    models = [model_1, model_2, model_3]
    evaluate_uniform_moe(models, dataloader)


if __name__ == "__main__":
    main()
