#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# ======================== User configuration ========================
MODEL_NAME_OR_PATH="${MODEL_NAME_OR_PATH:-Qwen/Qwen3-1.7B}"
GPU_IDS="${GPU_IDS:-0,1,2,3}"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/outputs/qwen3_1_7b_patient_lora_demo}"
TRAIN_FILE="${TRAIN_FILE:-${SCRIPT_DIR}/data/patient_pretrain_train.jsonl}"
DEV_FILE="${DEV_FILE:-${SCRIPT_DIR}/data/patient_pretrain_dev.jsonl}"
DISABLE_VERSION_CHECK="${DISABLE_VERSION_CHECK:-1}"
# ====================================================================

CONDA_ENV_NAME="${CONDA_ENV_NAME:-qwen3}"
LLAMAFACTORY_ROOT="${LLAMAFACTORY_ROOT:-${SCRIPT_DIR}/LLaMA-Factory}"

GPU_IDS="${GPU_IDS//[[:space:]]/}"
if [[ ! "${GPU_IDS}" =~ ^[0-9]+(,[0-9]+)*$ ]]; then
  echo "ERROR: GPU_IDS must be comma-separated GPU indexes, for example 3 or 0,1,2,3." >&2
  exit 1
fi
IFS=',' read -r -a GPU_LIST <<< "${GPU_IDS}"
GPU_COUNT="${#GPU_LIST[@]}"
export CUDA_VISIBLE_DEVICES="${GPU_IDS}"
export DISABLE_VERSION_CHECK

# LLaMA-Factory will launch one torchrun worker per visible GPU.
if (( GPU_COUNT > 1 )); then
  export FORCE_TORCHRUN="${FORCE_TORCHRUN:-1}"
fi

# Use PYTHON_BIN when explicitly supplied. Otherwise activate the named conda
# environment, making this directory portable across machines.
if [[ -z "${PYTHON_BIN:-}" ]]; then
  if [[ "${CONDA_DEFAULT_ENV:-}" != "${CONDA_ENV_NAME}" ]]; then
    if ! command -v conda >/dev/null 2>&1; then
      echo "ERROR: conda is unavailable. Activate qwen3 or set PYTHON_BIN." >&2
      exit 1
    fi
    CONDA_BASE="$(conda info --base)"
    PS1="${PS1:-}"
    # shellcheck disable=SC1091
    source "${CONDA_BASE}/etc/profile.d/conda.sh"
    conda activate "${CONDA_ENV_NAME}"
  fi
  PYTHON_BIN="$(command -v python)"
fi

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "ERROR: Python executable not found: ${PYTHON_BIN}" >&2
  exit 1
fi

cd "${SCRIPT_DIR}"

echo "Model: ${MODEL_NAME_OR_PATH}"
echo "GPU selection: physical GPU(s) ${CUDA_VISIBLE_DEVICES} (${GPU_COUNT} process(es))"
echo "Output directory: ${OUTPUT_DIR}"
echo "Train data: ${TRAIN_FILE}"
echo "Dev data: ${DEV_FILE}"
echo "LLaMA-Factory dependency version check disabled: ${DISABLE_VERSION_CHECK}"
echo "[1/2] Converting patient train/dev data..."
"${PYTHON_BIN}" prepare_patient_pretrain.py \
  --train-file "${TRAIN_FILE}" \
  --dev-file "${DEV_FILE}" \
  --output-dir "${SCRIPT_DIR}/data"

if [[ "${1:-}" == "--prepare-only" ]]; then
  echo "Data preparation completed (--prepare-only)."
  exit 0
fi

# Prefer an installed CLI, but allow running the bundled source tree directly.
if [[ -n "${LLAMAFACTORY_CLI:-}" ]]; then
  LLAMAFACTORY_COMMAND=("${LLAMAFACTORY_CLI}")
elif command -v llamafactory-cli >/dev/null 2>&1; then
  LLAMAFACTORY_COMMAND=("$(command -v llamafactory-cli)")
elif [[ -f "${LLAMAFACTORY_ROOT}/src/llamafactory/cli.py" ]]; then
  export PYTHONPATH="${LLAMAFACTORY_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}"
  LLAMAFACTORY_COMMAND=("${PYTHON_BIN}" -m llamafactory.cli)
else
  echo "ERROR: LLaMA-Factory was not found; no package installation was attempted." >&2
  echo "Either copy LLaMA-Factory beside this script or set one of:" >&2
  echo "  LLAMAFACTORY_ROOT=/path/to/LLaMA-Factory" >&2
  echo "  LLAMAFACTORY_CLI=/path/to/llamafactory-cli" >&2
  exit 2
fi

if [[ "${1:-}" == "--check-only" ]]; then
  "${PYTHON_BIN}" -c "import accelerate, datasets, omegaconf, peft, torch, transformers, trl, llamafactory; print('LLaMA-Factory and runtime dependencies: OK')"
  echo "Environment and data checks completed (--check-only)."
  exit 0
fi

TRAIN_OVERRIDES=(
  "model_name_or_path=${MODEL_NAME_OR_PATH}"
  "output_dir=${OUTPUT_DIR}"
)

echo "[2/2] Starting the 2-step Qwen3-1.7B LoRA pretraining smoke test on ${GPU_COUNT} GPU(s)..."
"${LLAMAFACTORY_COMMAND[@]}" train qwen3_lora_pretrain_demo.yaml "${TRAIN_OVERRIDES[@]}"
