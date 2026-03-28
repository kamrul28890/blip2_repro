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

- Validated locally, but not checkpoint-complete yet
- Evidence:
  - latest smoke run uses the intended reduced dataset
  - latest smoke run loads `10000` train, `1000` val, and `1000` test records
  - latest smoke run enters `Start training epoch 0`
  - no checkpoint exists yet because the longest run was cut off by the external command timeout
- Acceptance criteria for the first runnable milestone:
  - met

## Stage 4: BLIP-2 Stage-2 Training

Prerequisite:

- A valid stage-1 checkpoint exists and is registered

Status:

- Blocked on stage-1 checkpoint

## Stage 5: Caption Fine-Tuning

Prerequisite:

- A valid stage-2 checkpoint exists and is registered

Status:

- Blocked on stage-2 checkpoint
