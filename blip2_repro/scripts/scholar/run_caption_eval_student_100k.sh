#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
ANN_ROOT="${ANN_ROOT:-$REPO_ROOT/repo_study/LAVIS/cache/coco/annotations}"
GROUND_TRUTH_FILE="${GROUND_TRUTH_FILE:-$ANN_ROOT/coco_karpathy_val_student_1k_gt.json}"
OUTPUT_PATH="${OUTPUT_PATH:-$REPO_ROOT/metrics/blip2/caption_eval_summary_student_100k.json}"
EXAMPLES_OUTPUT_PATH="${EXAMPLES_OUTPUT_PATH:-$REPO_ROOT/metrics/blip2/caption_eval_examples_student_100k.json}"

: "${PREDICTION_FILE:?Set PREDICTION_FILE to the saved val_epoch*.json file before running this script.}"

"$PYTHON_BIN" \
  "$REPO_ROOT/blip2_repro/tools/evaluate_caption_subset.py" \
  --gt "$GROUND_TRUTH_FILE" \
  --pred "$PREDICTION_FILE" \
  --output "$OUTPUT_PATH" \
  --examples-output "$EXAMPLES_OUTPUT_PATH"
