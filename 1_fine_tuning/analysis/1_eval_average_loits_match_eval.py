"""Average three models' logits and use exactly the same metrics as eval.py."""

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

from model import LLamaModel, MODEL_ID


MAX_LEN = 2000
CLASSES = 2
TEST_FILE = Path(
    "/mnt/data_218/home1/Cool_Chen/OOD_data_OUD_corhot/"
    "data_by_junhui_right/811_test_ood.jsonl"
)
BATCH_SIZE = 1

# This comparison script defaults to the exact checkpoint used by eval.py.
# LLamaModel reads the base-model ID from its adapter_config.json, also exactly
# as eval.py does. Change these paths only after this equivalence check passes.
EVAL_CHECKPOINT = Path(__file__).resolve().parent / "checkpoints"
checkpoint_path_1 = EVAL_CHECKPOINT
checkpoint_path_2 = EVAL_CHECKPOINT
checkpoint_path_3 = EVAL_CHECKPOINT


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
    """Same ECE implementation used by eval.py."""
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


def evaluate_uniform_moe(models, dataloader, match_single_model=False):
    """Average logits, or reproduce eval.py exactly for one repeated checkpoint.

    When all three checkpoint paths are the same, averaging three equal BF16
    tensors after converting them to FP32 is unnecessary and can change ties or
    calibration by a small amount.  In that case we still run all three models
    and verify every batch, but retain model 1's original logits exactly as
    eval.py does.
    """
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
                # Keep the original dtype. eval.py retains the model's BF16
                # logits; converting to FP32 before averaging is a different
                # numerical evaluation path.
                model_logits.append(logits.detach().cpu())

        if match_single_model:
            reference_logits = model_logits[0]
            for model_index, logits in enumerate(model_logits[1:], start=2):
                if not torch.equal(reference_logits, logits):
                    max_difference = (
                        reference_logits.float() - logits.float()
                    ).abs().max().item()
                    raise RuntimeError(
                        "The checkpoint paths are identical, but model 1 and "
                        f"model {model_index} produced different logits "
                        f"(max abs diff: {max_difference:.8g})."
                    )

            # This is deliberately not mean(stack(...)). It preserves exactly
            # the tensor that eval.py receives, including its original dtype.
            final_logits = reference_logits
        else:
            final_logits = torch.stack(
                [logits.float() for logits in model_logits], dim=0
            ).mean(dim=0)
        all_logits.append(final_logits)
        all_labels.append(labels.argmax(dim=1).cpu())

    final_logits = torch.cat(all_logits, dim=0)
    gold = torch.cat(all_labels, dim=0)
    predictions = final_logits.argmax(dim=1)

    # Important: eval.py uses outputs[:, 1], not softmax(outputs)[:, 1], for
    # AUPRC, AUROC and Top-K ranking. Keeping the raw positive-class logit here
    # makes the two evaluation scripts directly comparable.
    positive_scores = final_logits[:, 1]

    gold_np = gold.numpy()
    predictions_np = predictions.numpy()
    # eval.py builds Pro with outputs[0][1].cpu().item(). Doing the same here
    # also supports BF16 CPU tensors and preserves the exact ranking values.
    scores_np = np.asarray([score.item() for score in positive_scores])

    print("precision", precision_score(gold_np, predictions_np))
    print("F1", f1_score(gold_np, predictions_np))
    print("jaccard", jaccard_score(gold_np, predictions_np))
    print("auprc", average_precision_score(gold_np, scores_np))
    print("auroc", roc_auc_score(gold_np, scores_np))

    order = np.argsort(-scores_np)
    sorted_gold = gold_np[order]
    total_positive = gold_np.sum()
    for percentage in (0.01, 0.02, 0.05, 0.10):
        k = math.ceil(len(sorted_gold) * percentage)
        true_positive = sorted_gold[:k].sum()
        ppv = true_positive / k if k > 0 else 0
        recall = true_positive / total_positive if total_positive > 0 else 0
        print(
            percentage,
            "--the PPV is ",
            ppv,
            "the recall is",
            recall,
        )

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

    # eval.py tokenizes with MODEL_ID. These three experts belong to the same
    # Qwen3-1.7B project, so use that exact tokenizer for all of them.
    tokenizers = [AutoTokenizer.from_pretrained(MODEL_ID) for _ in range(3)]
    for tokenizer in tokenizers:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
    dataloader = make_dataloader(TEST_FILE, tokenizers, BATCH_SIZE)

    model_1 = LLamaModel(
        CLASSES,
        adapter_path=str(checkpoint_path_1),
    )
    model_2 = LLamaModel(
        CLASSES,
        adapter_path=str(checkpoint_path_2),
    )
    model_3 = LLamaModel(
        CLASSES,
        adapter_path=str(checkpoint_path_3),
    )

    resolved_checkpoint_paths = [path.resolve() for path in checkpoint_paths]
    match_single_model = len(set(resolved_checkpoint_paths)) == 1
    if match_single_model:
        print(
            "All three checkpoint paths are identical. Verifying per-sample "
            "logits and using model 1 logits unchanged to match eval.py."
        )

    evaluate_uniform_moe(
        [model_1, model_2, model_3],
        dataloader,
        match_single_model=match_single_model,
    )


if __name__ == "__main__":
    main()
