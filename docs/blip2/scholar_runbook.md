# Scholar Runbook

This runbook captures the intended student-scale BLIP-2 training path for Purdue Scholar.

## Recommended Hardware

- First choice: Scholar `J`
- Fallback: Scholar `H`
- Avoid `H-MIG` and `I-MIG` for training because the `6 GB` MIG slices are too small for this workflow

## Why The Workflow Is Resume-First

- Scholar GPU work should be submitted through Slurm, not run on a front-end host
- The GPU queue is short enough that long BLIP-2 stages should be treated as resumable jobs
- The `student_100k` configs save checkpoints every epoch so each stage can be resumed safely

## Planned Training Recipe

- Dataset: `100k / 1k / 1k`
- Vision encoder: `CLIP-L`
- Language model: `facebook/opt-350m`
- Image size: `224`
- Stage 1: `5` epochs
- Stage 2: `5` epochs
- Caption fine-tuning: `8` epochs
- Selection rule: choose the best caption checkpoint by `CIDEr`, not by the last epoch

## Local Preparation

Use PowerShell on the local workstation to stage the dataset:

```powershell
.\blip2_repro\scripts\prepare_student_100k_run.ps1
```

This creates:

- `repo_study/LAVIS/cache/coco/annotations/coco_karpathy_train_student_100k.json`
- `repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_student_1k.json`
- `repo_study/LAVIS/cache/coco/annotations/coco_karpathy_test_student_1k.json`
- `repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_student_1k_gt.json`

## Scholar Launch Files

- Stage 1 launcher: `blip2_repro/scripts/scholar/run_stage1_student_100k.sh`
- Stage 2 launcher: `blip2_repro/scripts/scholar/run_stage2_student_100k.sh`
- Caption launcher: `blip2_repro/scripts/scholar/run_caption_student_100k.sh`
- Eval launcher: `blip2_repro/scripts/scholar/run_caption_eval_student_100k.sh`
- Stage 1 submit script: `blip2_repro/scripts/scholar/submit_stage1_student_100k.sbatch`
- Stage 2 submit script: `blip2_repro/scripts/scholar/submit_stage2_student_100k.sbatch`
- Caption submit script: `blip2_repro/scripts/scholar/submit_caption_student_100k.sbatch`

## Submission Pattern

Stage 1:

```bash
VENV_PATH=/path/to/venv sbatch blip2_repro/scripts/scholar/submit_stage1_student_100k.sbatch
```

Stage 2:

```bash
VENV_PATH=/path/to/venv \
STAGE1_CKPT=/path/to/checkpoint_4.pth \
sbatch blip2_repro/scripts/scholar/submit_stage2_student_100k.sbatch
```

Caption:

```bash
VENV_PATH=/path/to/venv \
STAGE2_CKPT=/path/to/checkpoint_4.pth \
sbatch blip2_repro/scripts/scholar/submit_caption_student_100k.sbatch
```

## Resume Pattern

When a stage hits queue limits, resubmit it with `RESUME_CKPT` pointed at the latest saved checkpoint from the same output directory.

Examples:

```bash
VENV_PATH=/path/to/venv \
RESUME_CKPT=/path/to/checkpoint_2.pth \
sbatch blip2_repro/scripts/scholar/submit_stage1_student_100k.sbatch
```

```bash
VENV_PATH=/path/to/venv \
STAGE2_CKPT=/path/to/checkpoint_4.pth \
RESUME_CKPT=/path/to/checkpoint_5.pth \
sbatch blip2_repro/scripts/scholar/submit_caption_student_100k.sbatch
```

## Evaluation

After caption fine-tuning, evaluate a saved `val_epoch*.json` file:

```bash
source /path/to/venv/bin/activate
PREDICTION_FILE=/path/to/val_epoch6.json \
bash blip2_repro/scripts/scholar/run_caption_eval_student_100k.sh
```

The outputs go to:

- `metrics/blip2/caption_eval_summary_student_100k.json`
- `metrics/blip2/caption_eval_examples_student_100k.json`
