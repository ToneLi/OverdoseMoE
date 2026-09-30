"""Method 2: prior-anchored entropy-adaptive fusion of saved logits."""

import argparse
import math
from pathlib import Path

import torch
import torch.nn.functional as F
from sklearn.metrics import average_precision_score

from save_logits import load_aligned_experts, positive_probabilities, print_metrics


EPSILON = 1e-12


def entropy_weights(expert_logits, beta):
    probabilities = F.softmax(expert_logits, dim=-1)
    entropies = -(probabilities * torch.log(probabilities + EPSILON)).sum(dim=-1)
    return F.softmax(-beta * entropies, dim=1)


def fuse_logits(expert_logits, prior_weights, lambda_value, beta):
    prior = torch.tensor(prior_weights, dtype=expert_logits.dtype).unsqueeze(0)
    adaptive = entropy_weights(expert_logits, beta)
    weights = (1.0 - lambda_value) * prior + lambda_value * adaptive
    return (weights.unsqueeze(-1) * expert_logits).sum(dim=1), weights


def select_lambda(validation_logits, validation_labels, prior, candidates, beta):
    labels_np = validation_labels.numpy()
    results = []
    print("\n===== Method 2 validation selection =====")
    for lambda_value in candidates:
        logits, _ = fuse_logits(validation_logits, prior, lambda_value, beta)
        auprc = average_precision_score(labels_np, positive_probabilities(logits))
        results.append((auprc, lambda_value))
        print(f"LAMBDA={lambda_value:.4g} validation AUPRC={auprc:.8f}")
    best_auprc, best_lambda = max(results, key=lambda item: (item[0], -item[1]))
    print("selected LAMBDA", best_lambda)
    print("selected validation AUPRC", best_auprc)
    return best_lambda


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation-logits", type=Path, nargs=3, required=True)
    parser.add_argument("--test-logits", type=Path, nargs=3, required=True)
    parser.add_argument(
        "--prior-weights",
        type=float,
        nargs=3,
        default=(0.30, 0.50, 0.20),
    )
    parser.add_argument(
        "--lambda-candidates",
        type=float,
        nargs="+",
        default=(0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30),
    )
    parser.add_argument("--entropy-beta", type=float, default=1.0)
    return parser.parse_args()


def main():
    args = parse_args()
    if any(weight < 0 for weight in args.prior_weights):
        raise ValueError("Prior weights must be non-negative.")
    if not math.isclose(sum(args.prior_weights), 1.0, abs_tol=1e-6):
        raise ValueError("Prior weights must sum to 1.")
    if args.entropy_beta < 0:
        raise ValueError("--entropy-beta must be non-negative.")
    if 0.0 not in args.lambda_candidates:
        raise ValueError("--lambda-candidates must include 0.0.")
    if any(value < 0 or value > 1 for value in args.lambda_candidates):
        raise ValueError("Every LAMBDA candidate must be between 0 and 1.")

    validation_logits, validation_labels, _ = load_aligned_experts(
        args.validation_logits
    )
    test_logits, test_labels, _ = load_aligned_experts(args.test_logits)
    best_lambda = select_lambda(
        validation_logits,
        validation_labels,
        args.prior_weights,
        args.lambda_candidates,
        args.entropy_beta,
    )

    baseline_logits, baseline_weights = fuse_logits(
        test_logits,
        args.prior_weights,
        0.0,
        args.entropy_beta,
    )
    print("mean expert weights", baseline_weights.mean(dim=0).tolist())
    print_metrics("Method 2: fixed prior baseline", baseline_logits, test_labels)

    selected_logits, selected_weights = fuse_logits(
        test_logits,
        args.prior_weights,
        best_lambda,
        args.entropy_beta,
    )
    print("mean expert weights", selected_weights.mean(dim=0).tolist())
    print_metrics(
        f"Method 2: adaptive weighted MoE (LAMBDA={best_lambda})",
        selected_logits,
        test_labels,
    )


if __name__ == "__main__":
    main()
