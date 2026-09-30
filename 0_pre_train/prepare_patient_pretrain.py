#!/usr/bin/env python3
"""Create demo patient timelines and convert them for LLaMA-Factory pretraining."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


DEMO_TRAIN = [
    {
        "patienrID": (
            "P0001 <visit> Time: 0 months I10 | Essential hypertension; "
            "E11.9 | Type 2 diabetes mellitus without complications. "
            "<visit> Time: 6 months I10 | Essential hypertension; "
            "E11.9 | Type 2 diabetes mellitus without complications; "
            "metformin 500 mg twice daily."
        )
    },
    {
        "patienrID": (
            "P0002 <visit> Time: 0 months J45.909 | Unspecified asthma, uncomplicated; "
            "albuterol inhaler as needed. <visit> Time: 4 months J45.901 | "
            "Unspecified asthma with acute exacerbation; short course of prednisone."
        )
    },
    {
        "patienrID": (
            "P0003 <visit> Time: 0 months E78.5 | Hyperlipidemia, unspecified; "
            "atorvastatin 20 mg daily. <visit> Time: 12 months E78.5 | "
            "Hyperlipidemia, stable on current therapy."
        )
    },
    {
        "patienrID": (
            "P0004 <visit> Time: 0 months K21.9 | Gastro-esophageal reflux disease "
            "without esophagitis; omeprazole 20 mg daily. <visit> Time: 3 months "
            "K21.9 | Symptoms improved; continue lifestyle modification."
        )
    },
    {
        "patienrID": (
            "P0005 <visit> Time: 0 months M17.11 | Unilateral primary osteoarthritis, "
            "right knee; physical therapy recommended. <visit> Time: 5 months M17.11 | "
            "Persistent knee pain; topical diclofenac started."
        )
    },
    {
        "patienrID": (
            "P0006 <visit> Time: 0 months F32.A | Depression, unspecified; "
            "sertraline 25 mg daily. <visit> Time: 2 months F32.A | Mood improved; "
            "sertraline increased to 50 mg daily."
        )
    },
]

DEMO_DEV = [
    {
        "patienrID": (
            "P1001 <visit> Time: 0 months I10 | Essential hypertension; "
            "lisinopril 10 mg daily. <visit> Time: 3 months I10 | Blood pressure "
            "controlled; continue lisinopril."
        )
    },
    {
        "patienrID": (
            "P1002 <visit> Time: 0 months E03.9 | Hypothyroidism, unspecified; "
            "levothyroxine 50 mcg daily. <visit> Time: 6 months E03.9 | TSH within "
            "target range; continue current dose."
        )
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert patient JSON/JSONL/TXT into LLaMA-Factory pretrain JSONL."
    )
    parser.add_argument(
        "--train-file",
        type=Path,
        help="Optional real train file. If omitted, virtual demo records are used.",
    )
    parser.add_argument(
        "--dev-file",
        type=Path,
        help="Optional real dev file. If omitted, virtual demo records are used.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "data",
        help="Output directory (default: ./data next to this script).",
    )
    return parser.parse_args()


def read_records(path: Path) -> list[Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")

    if path.suffix.lower() == ".jsonl":
        records: list[Any] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON at {path}:{line_number}: {exc}") from exc
        return records

    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            return payload["data"]
        return [payload]

    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def extract_text(record: Any) -> str:
    if isinstance(record, str):
        text = record.strip()
    elif isinstance(record, dict):
        # "patienrID" intentionally supports the spelling in the source example.
        candidate_keys = (
            "text",
            "patienrID",
            "patientID",
            "patient_id",
            "timeline",
            "visit",
            "record",
            "content",
        )
        text = ""
        for key in candidate_keys:
            value = record.get(key)
            if isinstance(value, str) and value.strip():
                text = value.strip()
                break
        if not text:
            raise ValueError(
                "Object has no usable text field. Expected one of: "
                + ", ".join(candidate_keys)
            )
    else:
        raise ValueError(f"Unsupported record type: {type(record).__name__}")

    if not text:
        raise ValueError("Encountered an empty patient record")
    return text


def convert(records: Iterable[Any], split: str) -> list[dict[str, str]]:
    converted: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        try:
            converted.append({"text": extract_text(record)})
        except ValueError as exc:
            raise ValueError(f"Invalid {split} record #{index}: {exc}") from exc
    if not converted:
        raise ValueError(f"The {split} split is empty")
    return converted


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    if (args.train_file is None) != (args.dev_file is None):
        raise SystemExit("Provide both --train-file and --dev-file, or neither for demo data.")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    using_demo = args.train_file is None
    train_source = DEMO_TRAIN if using_demo else read_records(args.train_file)
    dev_source = DEMO_DEV if using_demo else read_records(args.dev_file)

    if using_demo:
        write_jsonl(output_dir / "demo_raw_train.jsonl", train_source)
        write_jsonl(output_dir / "demo_raw_dev.jsonl", dev_source)

    train_records = convert(train_source, "train")
    dev_records = convert(dev_source, "dev")
    write_jsonl(output_dir / "patient_pretrain_train.jsonl", train_records)
    write_jsonl(output_dir / "patient_pretrain_dev.jsonl", dev_records)

    dataset_info = {
        "patient_pretrain_train": {
            "file_name": "patient_pretrain_train.jsonl",
            "columns": {"prompt": "text"},
        },
        "patient_pretrain_dev": {
            "file_name": "patient_pretrain_dev.jsonl",
            "columns": {"prompt": "text"},
        },
    }
    with (output_dir / "dataset_info.json").open("w", encoding="utf-8") as handle:
        json.dump(dataset_info, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    source_description = "virtual demo data" if using_demo else "user input files"
    print(f"Prepared {len(train_records)} train and {len(dev_records)} dev records from {source_description}.")
    print(f"LLaMA-Factory dataset directory: {output_dir}")


if __name__ == "__main__":
    main()
