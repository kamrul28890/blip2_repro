# BLIP-2 Experiment Ledger

This file is the report-safe record of the main BLIP-2 captioning comparisons in this workspace. Keep it updated whenever a new evaluation summary is produced.

## Paper Reference

- Paper model: `BLIP-2 ViT-g OPT2.7B`
- Paper evaluation: COCO Karpathy captioning table, paper-style `x100` metric scale
- BLEU-4: `43.7`
- CIDEr: `145.8`
- Source: `paper/term_paper.tex`

## Local 10k Baseline

- Dataset split: `10k / 1k / 1k`
- Schedule: stage 1 `1` epoch, stage 2 `1` epoch, caption `1` epoch
- Stage 1 train loss: `0.326`
- Stage 2 train loss: `0.294`
- Caption train loss: `0.227`
- BLEU-1: `33.40`
- BLEU-2: `10.66`
- BLEU-3: `3.45`
- BLEU-4: `1.45`
- CIDEr: `3.03`
- Unique captions: `61 / 1000`
- Most common caption count: `251`
- Summary artifact: `metrics/blip2/caption_eval_summary.json`
- Caption examples artifact: `metrics/blip2/caption_eval_examples.json`
- Run registry source: `metrics/blip2/run_registry.jsonl`

## Local 50k Office Best

- Dataset split: `50k / 1k / 1k`
- Schedule: stage 1 `3` epochs, stage 2 `3` epochs, caption best checkpoint selected from a `5` epoch run
- Stage 1 losses by epoch: `0.525 -> 0.454 -> 0.412`
- Stage 2 losses by epoch: `0.473 -> 0.802 -> 0.767`
- Best caption snapshot: `val_epoch3.json`
- BLEU-1: `53.86`
- BLEU-2: `33.52`
- BLEU-3: `19.65`
- BLEU-4: `11.13`
- CIDEr: `37.57`
- Unique captions: `563 / 1000`
- Most common caption count: `27`
- Summary artifact: `metrics/blip2/caption_eval_summary_office_epoch3.json`
- Caption examples artifact: `metrics/blip2/caption_eval_examples_office_epoch3.json`

## Local 50k Polish Completion

- Dataset split: `50k / 1k / 1k`
- Schedule: caption-only polish rerun, `5` epochs, checkpoint saved every epoch
- Final saved epoch: `epoch4`
- BLEU-4: `10.49`
- CIDEr: `37.14`
- Best conclusion: the earlier office `epoch3` snapshot remains the best validation result
- Summary artifact: `metrics/blip2/caption_eval_summary_office_polish_epoch4.json`
- Run log: `repo_study/LAVIS/lavis/output/blip2_repro/caption_office_50k_opt350m_polish/20260401094/log.txt`

## Next Planned Student-Scale Run

- Dataset split target: `100k / 1k / 1k`
- Recommended hardware target: Scholar `J` first, `H` fallback
- Planned schedule: stage 1 `5` epochs, stage 2 `5` epochs, caption `8` epochs
- Image size: `224`
- Language model: `facebook/opt-350m`
- Checkpoint policy: save every epoch and resume as needed
- Configs:
  - `blip2_repro/configs/stage1_student_100k.yaml`
  - `blip2_repro/configs/stage2_student_100k_opt350m.yaml`
  - `blip2_repro/configs/caption_student_100k_opt350m.yaml`
- Prep and run scripts:
  - `blip2_repro/scripts/prepare_student_100k_run.ps1`
  - `blip2_repro/scripts/run_stage1_student_100k.ps1`
  - `blip2_repro/scripts/run_stage2_student_100k.ps1`
  - `blip2_repro/scripts/run_caption_student_100k.ps1`
  - `blip2_repro/scripts/scholar/submit_stage1_student_100k.sbatch`
  - `blip2_repro/scripts/scholar/submit_stage2_student_100k.sbatch`
  - `blip2_repro/scripts/scholar/submit_caption_student_100k.sbatch`

## Desktop Long-Run Variant

- Dataset split target: `100k / 1k / 1k`
- Intended machine: local desktop
- Planned schedule: stage 1 `10` epochs, stage 2 `10` epochs, caption `15` epochs
- Configs:
  - `blip2_repro/configs/stage1_student_100k_long.yaml`
  - `blip2_repro/configs/stage2_student_100k_opt350m_long.yaml`
  - `blip2_repro/configs/caption_student_100k_opt350m_long.yaml`
- Simple launch scripts:
  - `blip2_repro/scripts/run_stage1_student_100k_long.ps1`
  - `blip2_repro/scripts/run_stage2_student_100k_long.ps1`
  - `blip2_repro/scripts/run_caption_student_100k_long.ps1`
