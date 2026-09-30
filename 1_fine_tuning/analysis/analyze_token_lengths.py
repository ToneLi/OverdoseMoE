import argparse
import json
from pathlib import Path

from transformers import AutoTokenizer

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import MODEL_ID


SCRIPT_DIR = Path(__file__).resolve().parent

# ======================== Data path configuration ========================
# Match the demo splits in train.py; replace these paths for your own datasets.
TRAIN_FILE = "../mock_data_10.jsonl"
TEST_FILE = "../mock_data_10.jsonl"
# ============================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Measure token lengths of the icd field in training and test datasets."
    )
    parser.add_argument(
        "--train-file",
        default=TRAIN_FILE,
        help="Training JSONL; relative paths are resolved from the script directory.",
    )
    parser.add_argument(
        "--test-file",
        default=TEST_FILE,
        help="Test JSONL; relative paths are resolved from the script directory.",
    )
    parser.add_argument("--text-field", default="icd", help="Text field name.")
    parser.add_argument("--batch-size", type=int, default=512, help="Tokenization batch size.")
    parser.add_argument(
        "--max-length",
        type=int,
        default=2000,
        help="Maximum length used by train.py, for counting truncated records.",
    )
    return parser.parse_args()


def resolve_path(file_name):
    path = Path(file_name).expanduser()
    return path if path.is_absolute() else SCRIPT_DIR / path


def read_texts(path, text_field):
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                text = record[text_field]
            except (json.JSONDecodeError, KeyError) as error:
                raise ValueError(f"{path}:{line_number} Invalid data format: {error}") from error
            yield str(text)


def update_stats(stats, lengths, max_length):
    for length in lengths:
        stats["count"] += 1
        stats["total"] += length
        stats["minimum"] = length if stats["minimum"] is None else min(stats["minimum"], length)
        stats["maximum"] = length if stats["maximum"] is None else max(stats["maximum"], length)
        stats["truncated"] += int(length > max_length)


def analyze_file(path, tokenizer, text_field, batch_size, max_length):
    stats = {
        "count": 0,
        "total": 0,
        "minimum": None,
        "maximum": None,
        "truncated": 0,
    }
    batch = []

    def tokenize_batch(texts):
        encoded = tokenizer(
            texts,
            padding=False,
            truncation=False,
            add_special_tokens=True,
            return_attention_mask=False,
        )
        update_stats(stats, [len(ids) for ids in encoded["input_ids"]], max_length)

    for text in read_texts(path, text_field):
        batch.append(text)
        if len(batch) >= batch_size:
            tokenize_batch(batch)
            batch.clear()

    if batch:
        tokenize_batch(batch)

    if stats["count"] == 0:
        raise ValueError(f"Dataset is empty: {path}")
    return stats


def print_stats(name, path, stats, max_length):
    truncated_percent = stats["truncated"] / stats["count"] * 100
    print(f"\n{name}: {path}")
    print(f"Samples: {stats['count']}")
    print(f"Mean token length: {stats['total'] / stats['count']:.2f}")
    print(f"Minimum token length: {stats['minimum']}")
    print(f"Maximum token length: {stats['maximum']}")
    print(
        f"Exceeding {max_length}, truncated during training: "
        f"{stats['truncated']} ({truncated_percent:.2f}%)"
    )


def main():
    args = parse_args()
    if args.batch_size <= 0 or args.max_length <= 0:
        raise ValueError("batch-size and max-length must be positive.")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    datasets = (
        ("Training set", resolve_path(args.train_file)),
        ("Test set", resolve_path(args.test_file)),
    )

    print(f"Tokenizer: {MODEL_ID}")
    for name, path in datasets:
        stats = analyze_file(
            path,
            tokenizer,
            args.text_field,
            args.batch_size,
            args.max_length,
        )
        print_stats(name, path, stats, args.max_length)


if __name__ == "__main__":
    main()
