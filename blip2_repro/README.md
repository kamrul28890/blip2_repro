# BLIP-2 Reproduction Starter

This folder scopes BLIP-2 down to a course-project-sized reproduction path:

- Stage 1: train the Q-Former bridge from scratch with a frozen vision encoder.
- Stage 2: align the bridge to a much smaller frozen language model (`facebook/opt-350m`) instead of OPT-2.7B.
- Caption fine-tuning: run a small COCO caption experiment from the stage-2 checkpoint.

The design goal is simple: keep the BLIP-2 training stages and model wiring intact, but reduce data, image size, batch size, and LLM size enough to make an honest first attempt on a single RTX 3070 8 GB card.

## Scope

This is not a paper-scale reproduction. It is a faithful reduced reproduction of the BLIP-2 method:

- frozen vision encoder
- trainable Q-Former / bridge
- frozen language model in stage 2
- staged training
- COCO-based evaluation path

## Folder Layout

- `configs/`: local-first LAVIS configs
- `scripts/`: PowerShell entry points
- `tools/`: helper utilities such as subset creation

## Expected Data Layout

The configs assume COCO data lives under the LAVIS cache tree:

```text
repo_study/LAVIS/cache/coco/
  annotations/
    coco_karpathy_train.json
    coco_karpathy_val.json
    coco_karpathy_test.json
    coco_karpathy_train_small.json
    coco_karpathy_val_small.json
    coco_karpathy_test_small.json
  images/
    ...
```

Important:

- LAVIS resolves relative dataset paths under its own `cache/` directory.
- The `*_small.json` files are not official. Create them with `scripts/prepare_coco_subsets.ps1`.
- The image root should match what the Karpathy JSON uses in the `image` field.

## First Run

1. Download the Karpathy annotation files into the LAVIS cache.

```powershell
.\blip2_repro\scripts\download_coco_karpathy_annotations.ps1
```

2. Prepare the reduced annotation files.

```powershell
.\blip2_repro\scripts\prepare_coco_subsets.ps1
```

3. Run stage 1 from scratch.

```powershell
.\blip2_repro\scripts\run_stage1_local.ps1
```

4. Pick the newest stage-1 checkpoint from:

```text
repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/<job_id>/
```

5. Run stage 2 with that checkpoint.

```powershell
.\blip2_repro\scripts\run_stage2_local.ps1 -Stage1Checkpoint "D:\path\to\checkpoint_0.pth"
```

6. Run caption fine-tuning from the stage-2 checkpoint.

```powershell
.\blip2_repro\scripts\run_caption_local.ps1 -Stage2Checkpoint "D:\path\to\checkpoint_0.pth"
```

## Suggested Local Sizes

The subset script defaults are intentionally small:

- train: 10,000 samples
- val: 1,000 samples
- test: 1,000 samples

That is enough for a real smoke test and enough signal to validate the full training path.

## What To Change On A100

If the local path works and you move to an A100 node, these are the first switches to flip:

- increase `batch_size_train`
- reduce `accum_grad_iters`
- raise `image_size` for caption fine-tuning from `224` toward `364`
- swap `facebook/opt-350m` to a larger frozen LLM such as `facebook/opt-1.3b` or the official `facebook/opt-2.7b`
- add Visual Genome back into stage 1 and stage 2

## Switch Criteria

Move to A100 if any of these happen even after lowering batch size to `1` and keeping AMP on:

- stage 2 still runs out of memory with `facebook/opt-350m`
- training throughput is so low that one epoch on the small subset is impractical
- Windows or local dependency friction in LAVIS starts costing more time than the experiment itself

## Notes

- The configs keep `distributed: false` for local runs.
- The caption config disables validation and test evaluation by default to keep the first pass focused on training-path verification.
- The stage handoff is done by overriding `model.pretrained` with the previous stage checkpoint.
