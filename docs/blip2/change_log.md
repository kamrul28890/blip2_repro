# Change Log

## 2026-03-28

- Created `docs/blip2/`, `logs/blip2/`, and `metrics/blip2/`
- Added `scripts/run_logged_step.ps1`
- Updated `scripts/run_logged_step.ps1` to refresh `PATH` and execute the wrapped command through `cmd.exe`
- Added `scripts/download_coco_subset_images.py`
- Updated `scripts/download_coco_subset_images.py` to use HTTP COCO URLs and retry transient download failures
- Added `docs/blip2/requirements_effective.txt`
- Added the initial BLIP-2 environment and execution documentation set
- Established the interpreter policy to use the workspace venv only
- Recorded the required `open3d` compatibility substitution for this environment
- Added Windows/runtime compatibility pins for `numpy`, `moviepy`, `peft`, `huggingface-hub`, and `python-magic-bin`
- Installed Temurin 8 JRE
- Installed PyTorch `2.4.1+cu121`, `torchvision 0.19.1`, and `torchaudio 2.4.1`
- Installed effective requirements and editable LAVIS
- Staged all reduced-subset COCO images under `repo_study/LAVIS/cache/coco/images`
- Updated `blip2_repro/scripts/prepare_coco_subsets.ps1` to use the workspace venv interpreter
- Updated `blip2_repro/scripts/run_stage1_local.ps1` to use the workspace venv interpreter
- Updated `blip2_repro/scripts/run_stage2_local.ps1` to use the workspace venv interpreter
- Updated `blip2_repro/scripts/run_caption_local.ps1` to use the workspace venv interpreter
- Updated `blip2_repro/configs/stage1_local.yaml` to use absolute local annotation and image paths
- Updated `blip2_repro/configs/stage2_local_opt350m.yaml` to use absolute local annotation and image paths
- Updated `blip2_repro/configs/caption_local_opt350m.yaml` to use absolute local annotation and image paths
- Patched `repo_study/LAVIS/lavis/models/base_model.py` for non-distributed single-GPU gathering
- Patched `repo_study/LAVIS/lavis/models/blip2_models/blip2_qformer.py` for single-process rank handling
- Patched `repo_study/LAVIS/lavis/models/blip2_models/blip2_qformer.py` to skip retrieval-only `image_id` logic for caption-dataset lists
- Logged four stage-1 smoke attempts and resolved each blocker in sequence until the run entered training on the intended reduced dataset
