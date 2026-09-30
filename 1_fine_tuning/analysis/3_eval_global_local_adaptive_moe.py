"""Patient-specific entropy routing and global-local adaptive MoE fusion."""

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

# Global expert quality measured on the validation set (use validation AUPRC).
validation_auprc_1 = 0.2185
validation_auprc_2 = 0.1792
validation_auprc_3 = 0.2068

# Routing hyperparameters. Tune these only on the validation set.
ALPHA = 1.0  # Global validation-quality contribution
BETA = 1.0   # Patient-specific entropy contribution
EPSILON = 1e-12


def entropy_from_logits(logits):
    """Return one predictive entropy value per patient."""
    probabilities = F.softmax(logits, dim=-1)
    return -(probabilities * torch.log(probabilities + EPSILON)).sum(dim=-1)


def route_logits(expert_logits, global_quality, alpha, beta):
    """Create entropy-only and global-local patient-specific mixtures."""
    # expert_logits: [batch, expert, class]
    entropies = torch.stack(
        [entropy_from_logits(expert_logits[:, i, :]) for i in range(3)],
        dim=1,
    )

    # Baseline 3: w_i(x) = softmax(-H_i(x)).
    entropy_weights = F.softmax(-entropies, dim=1)
    entropy_logits = (entropy_weights.unsqueeze(-1) * expert_logits).sum(dim=1)

    # Proposed method: w_i(x) = softmax(alpha*Q_i - beta*H_i(x)).
    routing_scores = alpha * global_quality.unsqueeze(0) - beta * entropies
    adaptive_weights = F.softmax(routing_scores, dim=1)
    adaptive_logits = (adaptive_weights.unsqueeze(-1) * expert_logits).sum(dim=1)

    return entropy_logits, adaptive_logits, entropy_weights, adaptive_weights


def print_results(method_name, logits, gold, routing_weights):
    predictions = logits.argmax(dim=1)
    positive_probabilities = F.softmax(logits, dim=1)[:, 1]

    gold_np = gold.numpy()
    predictions_np = predictions.numpy()
    probabilities_np = positive_probabilities.numpy()

    print(f"\n===== {method_name} =====")
    print("mean expert weights", routing_weights.mean(dim=0).tolist())
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


def evaluate_dynamic_moe(models, dataloader, global_quality, alpha, beta):
    if len(models) != 3 or global_quality.numel() != 3:
        raise ValueError("Dynamic MoE requires exactly 3 models and 3 quality scores.")
    if not torch.isfinite(global_quality).all():
        raise ValueError("All validation AUPRC values must be finite.")
    if ((global_quality < 0) | (global_quality > 1)).any():
        raise ValueError("Validation AUPRC values must be between 0 and 1.")
    if alpha < 0 or beta < 0:
        raise ValueError("ALPHA and BETA must be non-negative.")

    for model in models:
        model.eval()

    all_entropy_logits = []
    all_adaptive_logits = []
    all_entropy_weights = []
    all_adaptive_weights = []
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

        # Shape: [batch_size, 3 experts, CLASSES]
        expert_logits = torch.stack(batch_logits, dim=1)
        (
            entropy_logits,
            adaptive_logits,
            entropy_weights,
            adaptive_weights,
        ) = route_logits(expert_logits, global_quality, alpha, beta)

        all_entropy_logits.append(entropy_logits)
        all_adaptive_logits.append(adaptive_logits)
        all_entropy_weights.append(entropy_weights)
        all_adaptive_weights.append(adaptive_weights)
        all_labels.append(labels.argmax(dim=1).cpu())

    gold = torch.cat(all_labels, dim=0)
    entropy_logits = torch.cat(all_entropy_logits, dim=0)
    adaptive_logits = torch.cat(all_adaptive_logits, dim=0)
    entropy_weights = torch.cat(all_entropy_weights, dim=0)
    adaptive_weights = torch.cat(all_adaptive_weights, dim=0)

    print_results(
        "Entropy-weighted MoE (baseline 3)",
        entropy_logits,
        gold,
        entropy_weights,
    )
    print_results(
        "Global-local adaptive fusion (proposed)",
        adaptive_logits,
        gold,
        adaptive_weights,
    )


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
    global_quality = torch.tensor(
        [validation_auprc_1, validation_auprc_2, validation_auprc_3],
        dtype=torch.float32,
    )
    evaluate_dynamic_moe(models, dataloader, global_quality, ALPHA, BETA)


if __name__ == "__main__":
    main()
