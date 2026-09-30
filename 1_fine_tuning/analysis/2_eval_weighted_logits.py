"""Prior-anchored adaptive Weighted MoE with validation-set safety selection."""

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
from tqdm import tqdm
from transformers import AutoTokenizer

from model import LLamaModel
from eval_average_loits import compute_ece_from_logits, make_dataloader


CLASSES = 2
BATCH_SIZE = 1

# Use a separate validation set to select LAMBDA. Never tune it on TEST_FILE.
VALIDATION_FILE = Path("/path/to/validation.jsonl")
TEST_FILE = Path(
    "/mnt/data_218/home1/Cool_Chen/OOD_data_OUD_corhot/"
    "data_by_junhui_right/811_test_ood.jsonl"
)

# Fill in the three base model IDs and LoRA checkpoint directories here.
model_id_1 = "/path/to/base_model_1"
model_id_2 = "/path/to/base_model_2"
model_id_3 = "/path/to/base_model_3"

checkpoint_path_1 = Path("/path/to/checkpoint_1")
checkpoint_path_2 = Path("/path/to/checkpoint_2")
checkpoint_path_3 = Path("/path/to/checkpoint_3")

# The best fixed weights found for Method 2 on the validation set.
PRIOR_WEIGHTS = [0.30, 0.50, 0.20]

# LAMBDA=0 exactly reproduces Method 2, so it is always a candidate.
LAMBDA_CANDIDATES = [0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30]
ENTROPY_BETA = 1.0
EPSILON = 1e-12


def validate_configuration():
    if len(PRIOR_WEIGHTS) != 3:
        raise ValueError("PRIOR_WEIGHTS must contain exactly 3 values.")
    if any(weight < 0 for weight in PRIOR_WEIGHTS):
        raise ValueError("PRIOR_WEIGHTS must be non-negative.")
    if not math.isclose(sum(PRIOR_WEIGHTS), 1.0, rel_tol=0.0, abs_tol=1e-6):
        raise ValueError("PRIOR_WEIGHTS must sum to 1.")
    if 0.0 not in LAMBDA_CANDIDATES:
        raise ValueError("LAMBDA_CANDIDATES must include 0.0 as the safety baseline.")
    if any(value < 0 or value > 1 for value in LAMBDA_CANDIDATES):
        raise ValueError("Every LAMBDA candidate must be between 0 and 1.")
    if ENTROPY_BETA < 0:
        raise ValueError("ENTROPY_BETA must be non-negative.")


def collect_expert_logits(models, dataloader):
    """Run all experts and return [sample, expert, class] logits on CPU."""
    for model in models:
        model.eval()

    all_expert_logits = []
    all_labels = []

    for model_inputs, labels in tqdm(dataloader):
        labels = labels.cuda(non_blocking=True)
        batch_logits = []

        with torch.inference_mode():
            for model, inputs in zip(models, model_inputs):
                logits, _ = model(
                    input_ids=inputs["input_ids"].cuda(non_blocking=True),
                    attention_mask=inputs["attention_mask"].cuda(non_blocking=True),
                    labels=labels,
                )
                batch_logits.append(logits.float().cpu())

        all_expert_logits.append(torch.stack(batch_logits, dim=1))
        all_labels.append(labels.argmax(dim=1).cpu())

    return torch.cat(all_expert_logits, dim=0), torch.cat(all_labels, dim=0)


def entropy_weights(expert_logits):
    """Compute patient-specific expert weights from predictive entropy."""
    probabilities = F.softmax(expert_logits, dim=-1)
    entropies = -(
        probabilities * torch.log(probabilities + EPSILON)
    ).sum(dim=-1)
    return F.softmax(-ENTROPY_BETA * entropies, dim=1)


def fuse_logits(expert_logits, prior_weights, lambda_value):
    """Interpolate between fixed Method 2 weights and adaptive weights."""
    prior = torch.tensor(prior_weights, dtype=expert_logits.dtype).unsqueeze(0)
    adaptive = entropy_weights(expert_logits)
    weights = (1.0 - lambda_value) * prior + lambda_value * adaptive
    final_logits = (weights.unsqueeze(-1) * expert_logits).sum(dim=1)
    return final_logits, weights


def auprc_from_logits(logits, labels):
    positive_probabilities = F.softmax(logits, dim=1)[:, 1].numpy()
    return average_precision_score(labels.numpy(), positive_probabilities)


def select_lambda(validation_logits, validation_labels):
    """Select only on validation AUPRC; ties prefer the safer smaller LAMBDA."""
    results = []
    print("\n===== Validation LAMBDA selection =====")
    for lambda_value in LAMBDA_CANDIDATES:
        logits, _ = fuse_logits(
            validation_logits,
            PRIOR_WEIGHTS,
            lambda_value,
        )
        score = auprc_from_logits(logits, validation_labels)
        results.append((score, lambda_value))
        print(f"LAMBDA={lambda_value:.2f}, validation AUPRC={score:.6f}")

    best_score, best_lambda = max(results, key=lambda item: (item[0], -item[1]))
    baseline_score = next(score for score, value in results if value == 0.0)
    print("selected LAMBDA", best_lambda)
    print("baseline validation AUPRC", baseline_score)
    print("selected validation AUPRC", best_score)
    return best_lambda


def print_results(method_name, logits, gold, weights):
    predictions = logits.argmax(dim=1)
    positive_probabilities = F.softmax(logits, dim=1)[:, 1]

    gold_np = gold.numpy()
    predictions_np = predictions.numpy()
    probabilities_np = positive_probabilities.numpy()

    print(f"\n===== {method_name} =====")
    print("mean expert weights", weights.mean(dim=0).tolist())
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

    print("ECE:", compute_ece_from_logits(logits, gold, n_bins=10))


def main():
    validate_configuration()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required to evaluate these three models.")

    required_files = [VALIDATION_FILE, TEST_FILE]
    for data_file in required_files:
        if not data_file.is_file():
            raise FileNotFoundError(f"Data file not found: {data_file}")

    checkpoint_paths = [checkpoint_path_1, checkpoint_path_2, checkpoint_path_3]
    for checkpoint_path in checkpoint_paths:
        if not checkpoint_path.is_dir():
            raise FileNotFoundError(f"Checkpoint directory not found: {checkpoint_path}")

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

    validation_dataloader = make_dataloader(
        VALIDATION_FILE,
        tokenizers,
        BATCH_SIZE,
    )
    test_dataloader = make_dataloader(TEST_FILE, tokenizers, BATCH_SIZE)

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

    print("Collecting validation logits...")
    validation_logits, validation_labels = collect_expert_logits(
        models,
        validation_dataloader,
    )
    best_lambda = select_lambda(validation_logits, validation_labels)

    print("\nCollecting test logits...")
    test_logits, test_labels = collect_expert_logits(models, test_dataloader)

    # Always report the untouched Method 2 baseline.
    baseline_logits, baseline_weights = fuse_logits(
        test_logits,
        PRIOR_WEIGHTS,
        lambda_value=0.0,
    )
    print_results(
        "Original Method 2 (safety baseline)",
        baseline_logits,
        test_labels,
        baseline_weights,
    )

    improved_logits, improved_weights = fuse_logits(
        test_logits,
        PRIOR_WEIGHTS,
        lambda_value=best_lambda,
    )
    print_results(
        f"Prior-anchored adaptive Weighted MoE (LAMBDA={best_lambda})",
        improved_logits,
        test_labels,
        improved_weights,
    )


if __name__ == "__main__":
    main()
