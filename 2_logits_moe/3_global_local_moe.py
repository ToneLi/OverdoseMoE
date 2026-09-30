"""Method 3: global-quality/local-entropy fusion of saved logits."""

import argparse
from pathlib import Path

import torch
import torch.nn.functional as F
from sklearn.metrics import average_precision_score

from save_logits import load_aligned_experts, positive_probabilities, print_metrics


EPSILON = 1e-12


def entropy_from_logits(logits):
    probabilities = F.softmax(logits, dim=-1)
    return -(probabilities * torch.log(probabilities + EPSILON)).sum(dim=-1)


def route_logits(expert_logits, global_quality, alpha, beta):
    entropies = entropy_from_logits(expert_logits)

    entropy_weights = F.softmax(-entropies, dim=1)
    entropy_logits = (entropy_weights.unsqueeze(-1) * expert_logits).sum(dim=1)

    routing_scores = alpha * global_quality.unsqueeze(0) - beta * entropies
    adaptive_weights = F.softmax(routing_scores, dim=1)
    adaptive_logits = (adaptive_weights.unsqueeze(-1) * expert_logits).sum(dim=1)
    return entropy_logits, adaptive_logits, entropy_weights, adaptive_weights


def validation_quality(expert_logits, labels):
    labels_np = labels.numpy()
    quality = []
    for expert_index in range(expert_logits.shape[1]):
        scores = positive_probabilities(expert_logits[:, expert_index, :])
        quality.append(average_precision_score(labels_np, scores))
    return torch.tensor(quality, dtype=torch.float32)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation-logits", type=Path, nargs=3, required=True)
    parser.add_argument("--test-logits", type=Path, nargs=3, required=True)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=1.0)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.alpha < 0 or args.beta < 0:
        raise ValueError("--alpha and --beta must be non-negative.")

    validation_logits, validation_labels, _ = load_aligned_experts(
        args.validation_logits
    )
    test_logits, test_labels, _ = load_aligned_experts(args.test_logits)
    global_quality = validation_quality(validation_logits, validation_labels)
    print("validation expert AUPRC", global_quality.tolist())

    (
        entropy_logits,
        adaptive_logits,
        entropy_weights,
        adaptive_weights,
    ) = route_logits(test_logits, global_quality, args.alpha, args.beta)

    print("mean expert weights", entropy_weights.mean(dim=0).tolist())
    print_metrics("Method 3 baseline: entropy-only MoE", entropy_logits, test_labels)

    print("mean expert weights", adaptive_weights.mean(dim=0).tolist())
    print_metrics(
        "Method 3: global-local adaptive MoE",
        adaptive_logits,
        test_labels,
    )


if __name__ == "__main__":
    main()
