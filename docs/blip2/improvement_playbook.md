# BLIP-2 Improvement Playbook

This file explains the current best path for improving caption quality beyond the original `10k` baseline.

## Where We Started

The first fully successful local pipeline used a `10k / 1k / 1k` split and a `1 / 1 / 1` schedule:

- BLEU-4: `1.45`
- CIDEr: `3.03`
- only `61` unique captions across `1000` validation images

That result is preserved in:

- `metrics/blip2/caption_eval_summary.json`
- `metrics/blip2/report_metrics_snapshot.json`
- `docs/blip2/experiment_ledger.md`

## What Already Helped

The strongest improvement so far came from scaling both optimization and data:

- moving from `10k` train rows to `50k`
- moving from `1 / 1 / 1` epochs to `3 / 3 / 5`
- keeping the architecture fixed at `CLIP-L + OPT-350M + image_size 224`

That pushed the best validation snapshot to:

- BLEU-4: `11.13`
- CIDEr: `37.57`
- `563` unique captions across `1000` predictions

The best saved evaluation remains:

- `metrics/blip2/caption_eval_summary_office_epoch3.json`

## Highest-ROI Next Moves

### 1. Increase data before increasing model size

The next recommended experiment is the new student-scale `100k / 1k / 1k` run:

- `blip2_repro/configs/stage1_student_100k.yaml`
- `blip2_repro/configs/stage2_student_100k_opt350m.yaml`
- `blip2_repro/configs/caption_student_100k_opt350m.yaml`

This is a better bet than spending the same compute on `50k` with many more epochs.

### 2. Keep the successful architecture stable

For the next run, keep:

- `vit_model: clip_L`
- `opt_model: facebook/opt-350m`
- `image_size: 224`

Changing multiple major variables at once makes the comparison harder to trust in the report.

### 3. Save and resume every stage

The new configs save checkpoints every epoch. This matters because:

- your best `50k` result was not the final saved epoch
- Scholar GPU jobs should be treated as resumable
- the best checkpoint should be chosen by `CIDEr`, not by "latest"

The shared local stage scripts now also accept `ResumeCheckpoint`.

### 4. Add epochs carefully, not blindly

Recommended schedule for the next run:

- stage 1: `5` epochs
- stage 2: `5` epochs
- caption fine-tuning: `8` epochs

Going straight to `10` caption epochs on the same `50k` split is less attractive than moving to `100k`.

### 5. Keep image size modest until the stronger run is stable

Stay at `224` for the first `100k` attempt.

Only after a clean `100k` run would I test:

- `280`
- `320`

## Scholar-Specific Guidance

Use:

- `docs/blip2/scholar_runbook.md`

That runbook covers:

- preferred Scholar node choice
- resume-first Slurm usage
- the new `student_100k` launch scripts

## Recommended Next Experiment

If you want the best student-scale reproduction path now, run this progression:

1. `blip2_repro/scripts/prepare_student_100k_run.ps1`
2. `blip2_repro/configs/stage1_student_100k.yaml`
3. `blip2_repro/configs/stage2_student_100k_opt350m.yaml`
4. `blip2_repro/configs/caption_student_100k_opt350m.yaml`
5. evaluate every saved `val_epoch*.json`
6. record the best checkpoint in `docs/blip2/experiment_ledger.md`
