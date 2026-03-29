# BLIP-2 Workspace Index

This folder tracks the BLIP-2 local reproduction environment, installation work, failures, fixes, data staging, and execution progress for the term paper workspace.

## Current Status

- Interpreter policy: use `D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\Scripts\python.exe` only
- LAVIS source root: `repo_study/LAVIS`
- Local BLIP-2 configs: `blip2_repro/configs`
- Stage 0: complete
- Stage 1: complete
- Stage 2: complete
- Stage 3: complete with a local stage-1 checkpoint
- Stage 4: complete with a local stage-2 checkpoint
- Stage 5: complete with a local caption checkpoint

## Verified Outcomes

- Java 8 JRE is installed at `C:\Program Files\Eclipse Adoptium\jre-8.0.482.8-hotspot\bin\java.exe`
- PyTorch `2.4.1+cu121` is installed and CUDA is available on the local `NVIDIA GeForce RTX 3070`
- `import lavis, decord, fairscale, pycocotools, open3d` succeeds in the workspace venv
- Reduced COCO annotation counts are correct: `train=10000`, `val=1000`, `test=1000`
- Reduced COCO images are staged under `repo_study/LAVIS/cache/coco/images`
- The sample image `val2014/COCO_val2014_000000293244.jpg` exists and loads successfully
- The previously missing image `val2014/COCO_val2014_000000091349.jpg` was recovered by manual retry after an HTTP `503`
- A valid stage-1 checkpoint exists at `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142/checkpoint_0.pth`
- The stage-1 run logged `train_loss=0.326`, `train_loss_itc=0.343`, `train_loss_itm=0.360`, and `train_loss_lm=4.518`
- A valid stage-2 checkpoint exists at `repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/20260328150/checkpoint_0.pth`
- The stage-2 run logged `train_loss=0.294`
- The local stage-2 run completed in `42m 14s` on the RTX 3070, based on the operator-reported terminal timing
- A valid caption fine-tuning checkpoint exists at `repo_study/LAVIS/lavis/output/blip2_repro/caption_local_opt350m/20260328225/checkpoint_0.pth`
- The successful caption run logged `train_loss=0.227`
- The successful caption run wrote `result/val_epoch0.json` for qualitative inspection on the reduced validation subset

## Local Compatibility Patches

- `docs/blip2/requirements_effective.txt` carries Windows-compatible dependency pins for this workspace
- `blip2_repro/configs/*.yaml` now use absolute local annotation and image paths so they do not resolve through LAVIS's default `/export/home/.cache/lavis`
- `blip2_repro/scripts/*.ps1` stage runners now call the workspace venv interpreter directly
- `scripts/run_logged_step.ps1` refreshes `PATH` from machine/user environment variables before running commands
- `scripts/download_coco_subset_images.py` uses `http://images.cocodataset.org/` and now retries transient download failures
- `repo_study/LAVIS/lavis/models/base_model.py` was patched so `all_gather_with_grad()` safely returns the local tensor when distributed training is not initialized
- `repo_study/LAVIS/lavis/models/blip2_models/blip2_qformer.py` was patched for single-process rank handling and to avoid treating caption-dataset `image_id` lists as retrieval tensors
- `repo_study/LAVIS/lavis/models/blip2_models/blip2_opt.py` was patched so the Q-Former bridge projects into OPT's actual token-embedding dimension, which is required for `facebook/opt-350m`
- `repo_study/LAVIS/lavis/runners/runner_base.py` and `repo_study/LAVIS/lavis/runners/runner_iter.py` were patched to guard `dist.barrier()` in non-distributed local runs

## Latest Verified Artifacts

- First path-resolution failure: `logs/blip2/stage3/20260328_043847_stage1_local_smoke.log`
- Reduced-dataset path fix validated: `logs/blip2/stage3/20260328_044157_stage1_local_smoke_paths_fixed.log`
- Single-GPU distributed fix validation: `logs/blip2/stage3/20260328_044327_stage1_local_smoke_single_gpu_patch.log`
- Latest stage-1 smoke that continued running until external timeout: `logs/blip2/stage3/20260328_044436_stage1_local_smoke_non_dist_and_caption_fix.log`
- Stage-1 checkpoint run output: `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142/`
- Stage-2 checkpoint run output: `repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/20260328150/`
- Stage-5 caption checkpoint run output: `repo_study/LAVIS/lavis/output/blip2_repro/caption_local_opt350m/20260328225/`

## Stage Map

- Stage 0: scaffold docs, logs, metrics, and helper scripts
- Stage 1: install Python dependencies, Java, editable LAVIS, and verify imports/CUDA
- Stage 2: stage COCO images and validate sample paths
- Stage 3: run BLIP-2 stage-1 smoke test and capture outputs
- Stage 4: run BLIP-2 stage-2 training after a valid stage-1 checkpoint exists
- Stage 5: run caption fine-tuning after a valid stage-2 checkpoint exists

## Key Files

- `requirements_reference.md`
- `install_progress.md`
- `failures_and_fixes.md`
- `data_layout.md`
- `experiment_stages.md`
- `change_log.md`
- `next_steps.md`
- `requirements_effective.txt`

## Metrics and Logs

- Raw logs: `logs/blip2/`
- Machine-readable metrics: `metrics/blip2/`
- Logged command runner: `scripts/run_logged_step.ps1`
- High-level run attempts: `metrics/blip2/run_registry.jsonl`
- Milestone registry: `metrics/blip2/progress_registry.jsonl`
- Environment snapshot: `metrics/blip2/env_snapshot.json`

## What To Do Next

1. Use the repo-level `README.md` and `paper/SUBMISSION_NOTES.md` as the publish / handoff entry points.
2. After cloning with Git LFS, run `blip2_repro/scripts/reassemble_stage1_checkpoint.ps1` if you need the stage-1 checkpoint file restored from its split publish-safe artifact form.
3. If you want a stronger local model, move to the `*_better_local.yaml` configs and the guidance in `docs/blip2/improvement_playbook.md`.
4. If you want a stronger hardware run, reuse the same scripts and patches instead of rebuilding the workflow from scratch.
