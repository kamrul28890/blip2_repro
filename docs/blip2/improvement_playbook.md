# BLIP-2 Improvement Playbook

This file explains how to improve the local BLIP-2 reproduction beyond the baseline run that produced severe caption collapse.

## Baseline Problem

The successful baseline run completed all stages, but the final caption model collapsed badly:

- BLEU-4: `1.45`
- CIDEr: `3.03`
- only `61` unique captions across `1000` validation images

The most important reason is that the current setup is extremely undertrained:

- `10k` train samples only
- `1` epoch in stage 1
- `1` epoch in stage 2
- `1` epoch in caption fine-tuning
- `accum_grad_iters: 16`, which further reduces the number of optimizer steps per epoch

## Highest-ROI Fixes

### 1. Increase optimization steps

The fastest local improvement path is to keep the same data but train longer:

- stage 1: `3` epochs
- stage 2: `3` epochs
- caption fine-tuning: `5` epochs

This is exactly why the stronger presets exist:

- `blip2_repro/configs/stage1_better_local.yaml`
- `blip2_repro/configs/stage2_better_local_opt350m.yaml`
- `blip2_repro/configs/caption_better_local_opt350m.yaml`

### 2. Reduce gradient accumulation

The baseline used `accum_grad_iters: 16`. On a tiny dataset, this means too few optimizer updates.

The better-local configs reduce this to `8`, which keeps memory manageable while increasing update frequency.

### 3. Increase data before increasing model size

Moving from `10k` train samples to `30k`, `50k`, or the full Karpathy train split will usually help more than trying a larger language model on the same tiny subset.

Recommended order:

1. `10k` with stronger epochs
2. `30k` with stronger epochs
3. `50k` or full Karpathy train
4. only then consider larger backbones or image sizes

### 4. Keep image size modest at first

Stay at `224` until the model trains more stably.

After that, test:

- `280`
- `320`
- `364` only if memory allows

Higher image size is not the first fix for the current failure mode.

### 5. Do not expect decoding tweaks to rescue this model

Changing:

- `num_beams`
- prompt wording
- `max_len`

may help a little, but it will not fix mode collapse caused by undertraining.

## Rough Local Time Estimates

These estimates are based on the observed timings from the successful baseline run on the RTX 3070:

- stage 1 baseline: `18m 31s`
- stage 2 baseline: `42m 14s`
- caption baseline: about `27m 34s`

Approximate totals:

- `10k`, stronger `3/3/5` schedule: about `5 to 6 hours`
- `30k`, stronger `3/3/5` schedule: about `16 hours`
- `50k`, stronger `3/3/5` schedule: about `27 hours`

These are rough planning numbers, not guarantees.

## If You Have Better Compute

If you move this repo to a stronger machine:

- keep the same scripts,
- point the scripts at the stronger config files,
- enlarge the dataset,
- raise `image_size`,
- optionally test a larger OPT checkpoint,
- optionally enable multi-GPU distributed runs after validating that your environment handles them cleanly.

## Recommended Next Experiment

If you want the best improvement per hour spent, run this progression:

1. `stage1_better_local.yaml`
2. `stage2_better_local_opt350m.yaml`
3. `caption_better_local_opt350m.yaml`
4. evaluate with `run_caption_eval.ps1`

If that helps, repeat the same schedule on a larger subset.
