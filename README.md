# BLIP-2 Reproduction Workspace

This repository contains the full term-paper workspace for a local BLIP-2 reproduction study, along with the three papers that were read, the official repos that were inspected, the full documentation trail of what was attempted, the failures and fixes that were needed on Windows, the generated paper, and the final checkpoints / reduced COCO data used in the successful run.

The main project result is a complete three-stage BLIP-2 pipeline reproduction on a single RTX 3070 8GB GPU:

- stage 1 representation learning,
- stage 2 generative alignment with `facebook/opt-350m`,
- caption fine-tuning,
- offline evaluation and paper-ready reporting.

## What Is Included

- term-paper instructions: `NLP_Term_Paper_Instruction.pdf`
- the three selected papers: `Papers/`
- vendor repos studied during paper selection:
  - `repo_study/LAVIS`
  - `repo_study/LLaVA`
  - `repo_study/VisionLLM`
- BLIP-2 reproduction configs and runners: `blip2_repro/`
- install / failure / progress documentation: `docs/blip2/`
- raw logs: `logs/blip2/`
- machine-readable metrics and registries: `metrics/blip2/`
- compiled anonymous ACL paper: `paper/term_paper.pdf`
- final local checkpoints and result files:
  - `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/.../checkpoint_0.pth`
  - `repo_study/LAVIS/lavis/output/blip2_repro/stage2_local_opt350m/.../checkpoint_0.pth`
  - `repo_study/LAVIS/lavis/output/blip2_repro/caption_local_opt350m/.../checkpoint_0.pth`
- reduced COCO annotations and staged images under `repo_study/LAVIS/cache/coco/`

## Final Outcome

The local reproduction completed successfully and produced all three checkpoints. The best office-scale caption result is still below the BLIP-2 paper, but it is much stronger than the earlier reduced local baseline.

Final local evaluation summary:

- BLEU-1: `53.86`
- BLEU-2: `33.52`
- BLEU-3: `19.65`
- BLEU-4: `11.13`
- CIDEr: `37.57`
- unique captions across 1000 predictions: `563`

The exact evaluation artifact is:

- `metrics/blip2/caption_eval_summary_office_epoch3.json`

Representative qualitative failures are stored in:

- `metrics/blip2/caption_eval_examples_office_epoch3.json`

## Important Clone Note

This repo uses Git LFS for the staged COCO images and BLIP-2 checkpoint artifacts.

After cloning:

```powershell
git lfs install
git lfs pull
```

Without `git lfs pull`, the large model and image artifacts will only appear as pointer files.

One artifact is packaged slightly differently because GitHub LFS rejected the raw stage-1 checkpoint as a single object:

- `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142/checkpoint_0.pth` is stored as split LFS parts plus a SHA-256 manifest
- reconstruct it with `.\blip2_repro\scripts\reassemble_stage1_checkpoint.ps1`
- the script restores the original filename and verifies the expected hash

## Quick Start

### 1. Create a Python environment

Use Python `3.10.x`. The original successful run used Python `3.10.11`.

### 2. Install dependencies

The exact Windows-compatible dependency history is documented in:

- `docs/blip2/requirements_reference.md`
- `docs/blip2/requirements_effective.txt`
- `docs/blip2/install_progress.md`

The short version is:

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
python -m pip install -r docs/blip2/requirements_effective.txt
python -m pip install --no-deps -e repo_study/LAVIS
```

### 3. Install Java

Caption metrics on this workspace used Java 8:

```powershell
winget install --id EclipseAdoptium.Temurin.8.JRE -e
```

### 4. Verify the environment

Use the environment smoke tests listed in:

- `docs/blip2/experiment_stages.md`

## Reproducing The Runs

The staged local configs are under:

- `blip2_repro/configs/stage1_local.yaml`
- `blip2_repro/configs/stage2_local_opt350m.yaml`
- `blip2_repro/configs/caption_local_opt350m.yaml`

The stronger presets are under:

- `blip2_repro/configs/stage1_better_local.yaml`
- `blip2_repro/configs/stage2_better_local_opt350m.yaml`
- `blip2_repro/configs/caption_better_local_opt350m.yaml`

The stage runners are:

- `blip2_repro/scripts/run_stage1_local.ps1`
- `blip2_repro/scripts/run_stage2_local.ps1`
- `blip2_repro/scripts/run_caption_local.ps1`
- `blip2_repro/scripts/run_caption_eval.ps1`
- `blip2_repro/scripts/reassemble_stage1_checkpoint.ps1`

Examples:

```powershell
.\blip2_repro\scripts\run_stage1_local.ps1
.\blip2_repro\scripts\run_stage2_local.ps1 -Stage1Checkpoint ".\repo_study\LAVIS\lavis\output\blip2_repro\stage1_local\20260328142\checkpoint_0.pth"
.\blip2_repro\scripts\run_caption_local.ps1 -Stage2Checkpoint ".\repo_study\LAVIS\lavis\output\blip2_repro\stage2_local_opt350m\20260328150\checkpoint_0.pth"
.\blip2_repro\scripts\run_caption_eval.ps1 -PredictionFile ".\repo_study\LAVIS\lavis\output\blip2_repro\caption_local_opt350m\20260328225\result\val_epoch0.json"
```

## If You Have Better Compute

This workspace is already structured so someone with stronger hardware can reuse it with only small config changes.

The main knobs are:

- `max_epoch`
- `accum_grad_iters`
- `image_size`
- `batch_size_train`
- dataset annotation files
- `opt_model`

The detailed playbook is here:

- `docs/blip2/improvement_playbook.md`

If you have a stronger GPU or multiple GPUs, the easiest path is:

1. keep the same scripts,
2. point them at the stronger config files or your own edited configs,
3. replace the checkpoint arguments with your paths,
4. increase dataset size and epochs,
5. optionally swap `opt-350m` for a larger LM if your hardware allows it.

## Documentation Index

- workspace status: `docs/blip2/README.md`
- install history: `docs/blip2/install_progress.md`
- dependency notes: `docs/blip2/requirements_reference.md`
- failures and fixes: `docs/blip2/failures_and_fixes.md`
- data layout: `docs/blip2/data_layout.md`
- stage map: `docs/blip2/experiment_stages.md`
- change log: `docs/blip2/change_log.md`
- next steps: `docs/blip2/next_steps.md`
- improvement guide: `docs/blip2/improvement_playbook.md`

## Paper And Submission Assets

- final paper PDF: `paper/term_paper.pdf`
- LaTeX source: `paper/term_paper.tex`
- paper build / submission notes: `paper/SUBMISSION_NOTES.md`
- paper-selection `.bib` draft: `paper/paper_selection_submission.bib`
- presentation outline: `presentation/presentation_outline.md`
- peer-review template: `peer_review/review_template.txt`

## Notes On The Included Artifacts

- `.venv/` is intentionally excluded
- nested vendor `.git` directories are intentionally excluded
- staged images and checkpoints are included through Git LFS
- the stage-1 checkpoint is included as Git LFS split parts because the raw file exceeded GitHub's per-object upload limit
- the repo includes logs and metrics because they are part of the reproducibility story

## Summary

This repo is both:

- an archival record of what was done for the term paper, and
- a reusable BLIP-2 reproduction scaffold that another student can rerun locally or scale up on stronger hardware.
