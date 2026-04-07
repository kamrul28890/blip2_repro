#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
LAVIS_ROOT="${LAVIS_ROOT:-$REPO_ROOT/repo_study/LAVIS}"
PYTHON_BIN="${PYTHON_BIN:-python}"
CONFIG_PATH="${CONFIG_PATH:-$REPO_ROOT/blip2_repro/configs/stage2_student_100k_opt350m.yaml}"
ANN_ROOT="${ANN_ROOT:-$LAVIS_ROOT/cache/coco/annotations}"
IMAGES_ROOT="${IMAGES_ROOT:-$LAVIS_ROOT/cache/coco/images}"
TRAIN_ANN="${TRAIN_ANN:-$ANN_ROOT/coco_karpathy_train_student_100k.json}"
VAL_ANN="${VAL_ANN:-$ANN_ROOT/coco_karpathy_val_student_1k.json}"
TEST_ANN="${TEST_ANN:-$ANN_ROOT/coco_karpathy_test_student_1k.json}"
RESUME_CKPT="${RESUME_CKPT:-}"

: "${STAGE1_CKPT:?Set STAGE1_CKPT to a stage-1 checkpoint path before running this script.}"

OPTIONS=(
  "model.pretrained=$STAGE1_CKPT"
  "datasets.coco_caption.build_info.annotations.train.url=$TRAIN_ANN"
  "datasets.coco_caption.build_info.annotations.train.storage=$TRAIN_ANN"
  "datasets.coco_caption.build_info.annotations.val.url=$VAL_ANN"
  "datasets.coco_caption.build_info.annotations.val.storage=$VAL_ANN"
  "datasets.coco_caption.build_info.annotations.test.url=$TEST_ANN"
  "datasets.coco_caption.build_info.annotations.test.storage=$TEST_ANN"
  "datasets.coco_caption.build_info.images.storage=$IMAGES_ROOT"
)

if [[ -n "$RESUME_CKPT" ]]; then
  OPTIONS+=("run.resume_ckpt_path=$RESUME_CKPT")
fi

cd "$LAVIS_ROOT"
"$PYTHON_BIN" train.py --cfg-path "$CONFIG_PATH" --options "${OPTIONS[@]}"
