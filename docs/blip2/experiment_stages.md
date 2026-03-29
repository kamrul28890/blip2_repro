# Experiment Stages

## Stage 0: Workspace Bootstrap

Completion criteria:

- Root docs, logs, and metrics folders exist
- `scripts/run_logged_step.ps1` exists and works
- Initial docs are present
- Baseline environment snapshot is recorded

Status:

- Complete

## Stage 1: Environment Installation

Completion criteria:

- Java 8 JRE is installed and `java -version` works
- Pinned PyTorch CUDA wheels are installed in the workspace venv
- Effective LAVIS requirements are installed
- Editable LAVIS is installed with `--no-deps`
- `import lavis, decord, fairscale, pycocotools, open3d` succeeds
- `torch.cuda.is_available()` is `True`

Status:

- Complete
- Evidence:
  - workspace interpreter verified
  - `torch==2.4.1+cu121`
  - CUDA available on `NVIDIA GeForce RTX 3070`
  - JRE installed and validated by full path
  - import smoke succeeded after compatibility pins

## Stage 2: Dataset Readiness

Completion criteria:

- COCO images are staged under `repo_study/LAVIS/cache/coco/images`
- Reduced JSON counts are re-verified
- Sample image path exists
- A one-image PIL load check succeeds

Status:

- Complete
- Evidence:
  - reduced counts `10000/1000/1000`
  - staged image counts `7066 + 4605 = 11671`
  - sample image exists and loads
  - manual retry recovered the one transiently missing `503` image

## Stage 3: BLIP-2 Stage-1 Smoke Test

Completion criteria:

- `python train.py --cfg-path blip2_repro/configs/stage1_local.yaml` reaches model and dataset initialization without dependency or path errors
- Logs are stored under `logs/blip2/stage3`
- The run is registered in `metrics/blip2/run_registry.jsonl`
- Any checkpoint path produced is registered in `metrics/blip2/checkpoint_registry.jsonl`

Status:

- Complete
- Evidence:
  - the local run produced `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142/checkpoint_0.pth`
  - the stage-1 output log recorded `train_loss=0.326`
  - the stage-1 checkpoint was validated by loading it with PyTorch
- Acceptance criteria for the first runnable milestone:
  - met

## Stage 4: BLIP-2 Stage-2 Training

Prerequisite:

- A valid stage-1 checkpoint exists and is registered

Status:

- Complete
- Evidence:
  - the local run produced `repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/20260328150/checkpoint_0.pth`
  - the stage-2 output log recorded `train_loss=0.294`
  - the operator-reported total training time was `42m 14s`

## Stage 5: Caption Fine-Tuning

Prerequisite:

- A valid stage-2 checkpoint exists and is registered

Status:

- Complete
- Evidence:
  - the local run produced `repo_study/LAVIS/lavis/output/blip2_repro/caption_local_opt350m/20260328225/checkpoint_0.pth`
  - the caption output log recorded `train_loss=0.227`
  - the run wrote `result/val_epoch0.json` on the reduced validation subset
  - local Windows metric scoring was intentionally disabled for the final successful checkpoint run because METEOR remained unstable in this environment
