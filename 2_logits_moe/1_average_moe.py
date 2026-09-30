"""Method 1: uniformly average three saved expert-logit files."""

import argparse
from pathlib import Path

from save_logits import load_aligned_experts, print_metrics


# Edit these three saved-logit paths before running Method 1.
EXPERT1_LOGITS = Path("/path/to/expert1_test.pt")
EXPERT2_LOGITS = Path("/path/to/expert2_test.pt")
EXPERT3_LOGITS = Path("/path/to/expert3_test.pt")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--test-logits",
        type=Path,
        nargs=3,
        default=(EXPERT1_LOGITS, EXPERT2_LOGITS, EXPERT3_LOGITS),
        metavar=("EXPERT1", "EXPERT2", "EXPERT3"),
        help="Override the three expert paths configured at the file top.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    expert_logits, labels, _ = load_aligned_experts(args.test_logits)
    fused_logits = expert_logits.mean(dim=1)
    print_metrics("Method 1: uniform logit averaging", fused_logits, labels)


if __name__ == "__main__":
    main()
