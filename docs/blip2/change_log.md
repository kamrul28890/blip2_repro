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
- Patched `repo_study/LAVIS/lavis/runners/runner_base.py` and `repo_study/LAVIS/lavis/runners/runner_iter.py` to guard `dist.barrier()` in non-distributed local runs
- Confirmed the local stage-1 run wrote a valid checkpoint at `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142/checkpoint_0.pth`
- Patched `repo_study/LAVIS/lavis/models/blip2_models/blip2_opt.py` so the Q-Former bridge projects into OPT's token-embedding dimension instead of assuming `hidden_size == embed_dim`
- Recorded the completed local stage-1 run metrics from `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142/log.txt`
- Confirmed the local stage-2 run wrote a valid checkpoint at `repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/20260328150/checkpoint_0.pth`
- Recorded the stage-2 run summary with `train_loss=0.294` and operator-reported runtime `42m 14s`
- Advanced the documented next step from stage-2 training to caption fine-tuning
- Updated `blip2_repro/configs/caption_local_opt350m.yaml` so `valid_splits` is `["val"]`, which is required by LAVIS's captioning task setup
- Added `blip2_repro/tools/build_coco_gt_from_karpathy_subset.py` to build subset-matched COCO caption ground truth files
- Updated `blip2_repro/configs/caption_local_opt350m.yaml` to use a reduced-subset COCO validation ground-truth file via `run.annotation_file`
- Updated `blip2_repro/configs/caption_local_opt350m.yaml` to set `report_metric: false` so local Windows caption fine-tuning can finish without crashing in METEOR scoring
- Confirmed the final local caption fine-tuning run wrote `repo_study/LAVIS/lavis/output/blip2_repro/caption_local_opt350m/20260328225/checkpoint_0.pth`
- Recorded the final caption run summary with `train_loss=0.227` and `val_agg_metrics=0.0` under the no-metrics local Windows path
- Advanced the documented next step from training to qualitative evaluation and paper-writeup artifacts

## 2026-03-29

- Added `blip2_repro/tools/evaluate_caption_subset.py` to compute reproducible BLEU / CIDEr and caption-collapse statistics from saved result files
- Generated `metrics/blip2/caption_eval_summary.json` from the final successful caption checkpoint's `val_epoch0.json`
- Generated `metrics/blip2/caption_eval_examples.json` for paper-ready qualitative examples
- Wrote and compiled the anonymous ACL paper at `paper/term_paper.pdf`
- Added `paper/SUBMISSION_NOTES.md`
- Added `paper/paper_selection_submission.bib`
- Added `presentation/presentation_outline.md`
- Added `peer_review/review_template.txt`
- Added repo-level `README.md`
- Updated `.gitignore` so environment artifacts stay excluded while reproducibility artifacts remain publishable
- Added `.gitattributes` to publish staged COCO images and BLIP-2 checkpoints through Git LFS
- Added `docs/blip2/improvement_playbook.md`
- Added stronger reusable configs:
  - `blip2_repro/configs/stage1_better_local.yaml`
  - `blip2_repro/configs/stage2_better_local_opt350m.yaml`
  - `blip2_repro/configs/caption_better_local_opt350m.yaml`
- Added `blip2_repro/scripts/run_caption_eval.ps1` so evaluation can be rerun from the command line with the workspace venv
- Added `blip2_repro/scripts/reassemble_stage1_checkpoint.ps1` and split the oversized stage-1 checkpoint into GitHub-safe LFS parts with a SHA-256 manifest because the raw `checkpoint_0.pth` exceeded GitHub's per-object LFS upload limit
