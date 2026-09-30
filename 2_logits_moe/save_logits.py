"""Run one expert once and save aligned logits for offline MoE evaluation."""

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import average_precision_score, precision_score, roc_auc_score
from torch.utils.data import DataLoader, Dataset, SequentialSampler
from tqdm import tqdm


# ---------------------------------------------------------------------------
# Model/data interface: edit these paths for the expert whose logits are saved.
# The corresponding command-line options can override them.
# ---------------------------------------------------------------------------
LLM_PATH = "Qwen/Qwen3-1.7B"
CHECKPOINT_PATH = Path("/path/to/checkpoint")
DATA_FILE = Path(
    Path(__file__).resolve().parent.parent / "1_fine_tuning" / "mock_data_10.jsonl"
)


SCHEMA_VERSION = 1
MAX_LEN = 2000
PROJECT_DIR = Path(__file__).resolve().parent.parent / "1_fine_tuning"


def label_to_one_hot(label):
    return [0, 1] if label == "1" else [1, 0]


def read_data(file_path):
    sentences = []
    labels = []
    fingerprint = hashlib.sha256()

    with file_path.open("r", encoding="utf-8") as reader:
        for line_number, line in enumerate(reader, start=1):
            sample = json.loads(line)
            if "icds" not in sample or "label" not in sample:
                raise KeyError(
                    f"{file_path}:{line_number} must contain 'icds' and 'label'."
                )
            sentence = sample["icds"]
            label = sample["label"]
            sentences.append(sentence)
            labels.append(label_to_one_hot(label))
            canonical_sample = json.dumps(
                {"icds": sentence, "label": label},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            fingerprint.update(canonical_sample.encode("utf-8"))
            fingerprint.update(b"\n")

    if not sentences:
        raise ValueError(f"No samples found in {file_path}.")
    return sentences, labels, fingerprint.hexdigest()


class TokenizedDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        return {
            "input_ids": self.encodings["input_ids"][index],
            "attention_mask": self.encodings["attention_mask"][index],
            "label": self.labels[index],
            "sample_index": index,
        }


def make_dataloader(data_file, tokenizer, batch_size):
    sentences, labels, data_fingerprint = read_data(data_file)
    encodings = tokenizer(
        sentences,
        padding=False,
        truncation=True,
        max_length=MAX_LEN,
    )
    dataset = TokenizedDataset(
        encodings,
        torch.tensor(labels, dtype=torch.float32),
    )

    def collate_batch(features):
        token_features = [
            {
                "input_ids": feature["input_ids"],
                "attention_mask": feature["attention_mask"],
            }
            for feature in features
        ]
        batch = tokenizer.pad(
            token_features,
            padding=True,
            pad_to_multiple_of=8,
            return_tensors="pt",
        )
        labels_tensor = torch.stack([feature["label"] for feature in features])
        sample_indices = torch.tensor(
            [feature["sample_index"] for feature in features],
            dtype=torch.long,
        )
        return batch["input_ids"], batch["attention_mask"], labels_tensor, sample_indices

    dataloader = DataLoader(
        dataset,
        sampler=SequentialSampler(dataset),
        batch_size=batch_size,
        collate_fn=collate_batch,
    )
    return dataloader, data_fingerprint


def positive_probabilities(logits):
    return torch.softmax(logits.float(), dim=1)[:, 1].cpu().numpy()


def calculate_metrics(logits, labels):
    labels_np = labels.cpu().numpy()
    predictions_np = logits.argmax(dim=1).cpu().numpy()
    scores_np = positive_probabilities(logits)

    metrics = {
        "precision": precision_score(
            labels_np,
            predictions_np,
            zero_division=0,
        ),
        "auprc": average_precision_score(labels_np, scores_np),
        "auroc": roc_auc_score(labels_np, scores_np),
    }

    order = np.argsort(-scores_np, kind="stable")
    sorted_labels = labels_np[order]
    total_positive = labels_np.sum()
    for percentage in (0.01, 0.02, 0.05, 0.10):
        k = math.ceil(len(sorted_labels) * percentage)
        true_positive = sorted_labels[:k].sum()
        metrics[f"top_{int(percentage * 100)}pct_ppv"] = (
            true_positive / k if k else 0.0
        )
        metrics[f"top_{int(percentage * 100)}pct_recall"] = (
            true_positive / total_positive if total_positive else 0.0
        )
    return metrics


def print_metrics(title, logits, labels):
    metrics = calculate_metrics(logits, labels)
    print(f"\n===== {title} =====")
    print("precision (PPV)", metrics["precision"])
    print("AUPRC", metrics["auprc"])
    print("AUROC", metrics["auroc"])
    for percentage in (1, 2, 5, 10):
        print(
            f"Top {percentage}% PPV",
            metrics[f"top_{percentage}pct_ppv"],
            "recall",
            metrics[f"top_{percentage}pct_recall"],
        )


def load_aligned_experts(file_paths):
    """Load three expert files and strictly verify sample/label alignment."""
    if len(file_paths) != 3:
        raise ValueError(f"Exactly 3 expert files are required, got {len(file_paths)}.")

    payloads = []
    required_keys = {
        "schema_version",
        "logits",
        "labels",
        "sample_indices",
        "data_fingerprint",
    }
    for file_path in file_paths:
        if not file_path.is_file():
            raise FileNotFoundError(f"Saved logits file not found: {file_path}")
        payload = torch.load(file_path, map_location="cpu", weights_only=True)
        missing = required_keys.difference(payload)
        if missing:
            raise KeyError(f"{file_path} is missing keys: {sorted(missing)}")
        if payload["schema_version"] != SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported schema in {file_path}: {payload['schema_version']}"
            )

        logits = payload["logits"]
        labels = payload["labels"].long()
        indices = payload["sample_indices"].long()
        if logits.ndim != 2 or logits.shape[1] != 2:
            raise ValueError(f"{file_path}: logits must have shape [N, 2].")
        if labels.ndim != 1 or indices.ndim != 1:
            raise ValueError(f"{file_path}: labels and sample_indices must be 1-D.")
        if logits.shape[0] != labels.numel() or labels.numel() != indices.numel():
            raise ValueError(f"{file_path}: logits, labels and indices have different N.")
        if not torch.isfinite(logits.float()).all():
            raise ValueError(f"{file_path}: logits contain NaN or Inf.")

        payload["logits"] = logits.float()
        payload["labels"] = labels
        payload["sample_indices"] = indices
        payloads.append(payload)

    reference = payloads[0]
    for expert_number, payload in enumerate(payloads[1:], start=2):
        if payload["data_fingerprint"] != reference["data_fingerprint"]:
            raise ValueError(
                f"Expert {expert_number} was evaluated on different data/content."
            )
        if not torch.equal(payload["sample_indices"], reference["sample_indices"]):
            raise ValueError(f"Expert {expert_number} sample order does not match expert 1.")
        if not torch.equal(payload["labels"], reference["labels"]):
            raise ValueError(f"Expert {expert_number} labels do not match expert 1.")

    expert_logits = torch.stack(
        [payload["logits"] for payload in payloads],
        dim=1,
    )
    return expert_logits, reference["labels"], reference["sample_indices"]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--llm-path",
        default=LLM_PATH,
        help="Base LLM name or local path (default: LLM_PATH at file top).",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=CHECKPOINT_PATH,
        help="LoRA checkpoint path (default: CHECKPOINT_PATH at file top).",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_FILE,
        help="Input JSONL path (default: DATA_FILE at file top).",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=1)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.batch_size <= 0:
        raise ValueError("--batch-size must be positive.")
    if not args.checkpoint.is_dir():
        raise FileNotFoundError(f"Checkpoint directory not found: {args.checkpoint}")
    if not args.data_file.is_file():
        raise FileNotFoundError(f"Data file not found: {args.data_file}")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for model inference.")

    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))
    from model import LLamaModel
    from transformers import AutoTokenizer

    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    tokenizer = AutoTokenizer.from_pretrained(args.llm_path)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    dataloader, data_fingerprint = make_dataloader(
        args.data_file,
        tokenizer,
        args.batch_size,
    )
    model = LLamaModel(
        2,
        adapter_path=str(args.checkpoint),
        model_id=args.llm_path,
    )
    model.eval()

    all_logits = []
    all_labels = []
    all_indices = []
    for input_ids, attention_mask, labels, sample_indices in tqdm(dataloader):
        labels = labels.cuda(non_blocking=True)
        with torch.inference_mode():
            logits, _ = model(
                input_ids=input_ids.cuda(non_blocking=True),
                attention_mask=attention_mask.cuda(non_blocking=True),
                labels=labels,
            )
        all_logits.append(logits.detach().cpu())
        all_labels.append(labels.argmax(dim=1).cpu())
        all_indices.append(sample_indices)

    logits = torch.cat(all_logits, dim=0)
    labels = torch.cat(all_labels, dim=0).long()
    sample_indices = torch.cat(all_indices, dim=0).long()
    expected_indices = torch.arange(labels.numel(), dtype=torch.long)
    if not torch.equal(sample_indices, expected_indices):
        raise RuntimeError("Unexpected sample order while saving logits.")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "logits": logits,
        "labels": labels,
        "sample_indices": sample_indices,
        "data_fingerprint": data_fingerprint,
        "data_file": str(args.data_file.resolve()),
        "checkpoint": str(args.checkpoint.resolve()),
        "llm_path": args.llm_path,
        "tokenizer": args.llm_path,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, args.output)
    print(f"Saved {labels.numel()} samples to {args.output}")
    print_metrics("Single expert", logits, labels)


if __name__ == "__main__":
    main()
