#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

GPU_IDS="${GPU_IDS:-3}"
MODEL_NAME_OR_PATH="${MODEL_NAME_OR_PATH:-Qwen/Qwen3-1.7B}"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/outputs/qwen3_1_7b_patient_lora_demo}"

export CUDA_VISIBLE_DEVICES="${GPU_IDS}"

LLAMAFACTORY_ROOT="${SCRIPT_DIR}/LLaMA-Factory"

export PYTHONPATH="${LLAMAFACTORY_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}"

echo "GPU: ${CUDA_VISIBLE_DEVICES}"
echo "Model: ${MODEL_NAME_OR_PATH}"
echo "Output: ${OUTPUT_DIR}"

cd "${SCRIPT_DIR}"

python -m llamafactory.cli train \
  qwen3_lora_pretrain_demo.yaml \
  "model_name_or_path=${MODEL_NAME_OR_PATH}" \
  "output_dir=${OUTPUT_DIR}"