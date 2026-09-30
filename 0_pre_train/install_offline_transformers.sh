#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"

"${PYTHON_BIN}" -m pip install \
  --no-index \
  --find-links "${SCRIPT_DIR}/bao_transformers" \
  -r "${SCRIPT_DIR}/bao_transformers/requirements-transformers.txt"
