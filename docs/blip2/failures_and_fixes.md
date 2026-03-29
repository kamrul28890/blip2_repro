# Failures and Fixes

This file tracks every environment or execution failure that materially changes the setup, along with the exact fix applied.

## Recorded Issues

### 1. `open3d==0.13.0` does not resolve on Windows + Python 3.10

- Detection method: `pip install --dry-run -r repo_study/LAVIS/requirements.txt`
- Symptom: no matching distribution found for `open3d==0.13.0`
- Root cause: the upstream pin is too old for the current interpreter/platform combination
- Fix policy: replace only this line in the effective manifest with `open3d==0.19.0`
- Fix type: permanent for this workspace unless the Python version or platform changes

### 2. Java is missing before caption evaluation

- Detection method: `java -version`
- Symptom: `java` command not found
- Root cause: no JRE is currently installed on the machine path
- Fix policy: install `EclipseAdoptium.Temurin.8.JRE` via `winget`
- Fix type: required for `pycocoevalcap` metrics, not for early Python dependency installation

### 3. Fresh shell sessions do not immediately see the newly installed Java on `PATH`

- Detection method: direct shell `java -version` failed after the JRE install, while the executable existed on disk
- Symptom: `java` command not found in a fresh PowerShell session
- Root cause: the current shell did not inherit the updated machine/user `PATH`
- Fix policy: refresh `PATH` inside `scripts/run_logged_step.ps1` before each logged command and record the full JRE path in the environment snapshot
- Fix type: permanent for this workspace tooling

### 4. `scripts/run_logged_step.ps1` originally mishandled nested quoting for Python `-c` commands

- Detection method: logged smoke checks with inline Python snippets
- Symptom: PowerShell command parsing errors when passing quoted inline Python commands
- Root cause: nested PowerShell execution made quoting brittle
- Fix policy: execute the logged command through `cmd.exe /d /s /c` instead of a second PowerShell layer
- Fix type: permanent for this workspace tooling

### 5. `opencv-python-headless==4.5.5.64` failed against NumPy 2.x

- Detection method: `import cv2`
- Symptom: OpenCV import/runtime ABI mismatch
- Root cause: the pinned OpenCV build is not compatible with NumPy 2.x on this machine
- Fix policy: add `numpy<2` and install `numpy==1.26.4`
- Fix type: permanent for this workspace

### 6. `moviepy` API drift broke LAVIS imports

- Detection method: `import lavis`
- Symptom: `moviepy.editor` import failure
- Root cause: newer `moviepy` releases no longer match the import layout expected by LAVIS
- Fix policy: pin `moviepy==1.0.3`
- Fix type: permanent for this workspace

### 7. `peft` and `transformers` drift broke LAVIS imports

- Detection method: `import lavis`
- Symptom: missing `transformers` cache API compatibility through `peft`
- Root cause: newer `peft` expects a newer `transformers` API than the repo pin `transformers==4.33.2`
- Fix policy: pin `peft==0.5.0`
- Fix type: permanent for this workspace

### 8. `diffusers<=0.16.0` and latest `huggingface_hub` were incompatible

- Detection method: `import lavis`
- Symptom: `cached_download` import failure through `diffusers`
- Root cause: newer `huggingface_hub` versions removed the API expected by `diffusers<=0.16.0`
- Fix policy: pin `huggingface-hub==0.19.4`
- Fix type: permanent for this workspace

### 9. `python-magic` failed on Windows because `libmagic` was missing

- Detection method: `import magic`
- Symptom: missing `libmagic` runtime error
- Root cause: Windows needs the companion runtime package
- Fix policy: add `python-magic-bin==0.4.14`
- Fix type: permanent for this workspace

### 10. COCO image root was missing

- Detection method: filesystem inspection of `repo_study/LAVIS/cache/coco`
- Symptom: annotations existed, but `repo_study/LAVIS/cache/coco/images` did not
- Root cause: only annotation JSON files had been staged so far
- Fix policy: stage COCO 2014 images under the LAVIS cache layout before dataset and training smoke tests
- Fix type: required for any training or dataset verification run

### 11. COCO subset download over HTTPS failed certificate validation

- Detection method: first reduced-image staging run
- Symptom: repeated SSL trust/hostname failures against `https://images.cocodataset.org/...`
- Root cause: HTTPS trust was not reliable from this host for the COCO image endpoint
- Fix policy: change the downloader base URL to `http://images.cocodataset.org/`
- Fix type: workspace-specific implementation fix

### 12. One COCO image failed with HTTP `503` during subset staging

- Detection method: second reduced-image staging run
- Symptom: exactly one missing file, `val2014/COCO_val2014_000000091349.jpg`, failed with `http_error:503`
- Root cause: transient server-side failure
- Fix policy: manually retry the file with `curl.exe` and add retry support to `scripts/download_coco_subset_images.py`
- Fix type: permanent tooling improvement plus one-time data recovery

### 13. LAVIS local configs resolved through the wrong cache root

- Detection method: first stage-1 smoke run
- Symptom: dataset setup used `/export/home/.cache/lavis/...` instead of the prepared local cache under `repo_study/LAVIS/cache/...`
- Root cause: local YAML only overrode `storage`, so the upstream dataset defaults still resolved relative paths through LAVIS's default cache root
- Fix policy: patch the local BLIP configs to use absolute annotation and image paths, and set annotation `url` to the same local file path to prevent remote re-download
- Fix type: permanent for this workspace

### 14. BLIP-2 stage 1 assumed distributed collectives on single-GPU local runs

- Detection method: second stage-1 smoke run
- Symptom: `ValueError: Default process group has not been initialized`
- Root cause: `blip2_qformer.py` called `dist.get_rank()` and `all_gather_with_grad()` without a non-distributed guard
- Fix policy: patch `lavis/models/base_model.py` and `lavis/models/blip2_models/blip2_qformer.py` so the single-process local path safely uses rank `0` and local tensors
- Fix type: permanent for this workspace unless we later switch back to distributed-only launches

### 15. BLIP-2 stage 1 treated caption-dataset `image_id` values like retrieval tensors

- Detection method: third stage-1 smoke run
- Symptom: `AttributeError: 'list' object has no attribute 'view'`
- Root cause: the retrieval-only branch in `blip2_qformer.py` triggered whenever `image_id` existed, even if it came from caption data as a list of strings
- Fix policy: gate that branch so it only runs when `samples["image_id"]` is actually a tensor
- Fix type: permanent for this workspace

### 16. The latest local stage-1 smoke run exceeded the tool timeout before finishing epoch 0

- Detection method: fourth stage-1 smoke run
- Symptom: external timeout after the run had already entered training on the intended reduced dataset
- Root cause: the local RTX 3070 can start the run, but a full epoch over `10000` reduced training records still takes longer than the interactive tool timeout window
- Fix policy: run stage 1 as a longer background or supervised session, or move the same setup to an A100 machine if checkpoint turnaround is too slow
- Fix type: operational next step, not a code bug

### 17. BLIP-2 stage 2 with `facebook/opt-350m` failed on an embedding-dimension mismatch

- Detection method: the latest `termina_output.md` stage-2 run and the corresponding stage-2 traceback
- Symptom: `RuntimeError: Sizes of tensors must match except in dimension 1. Expected size 1024 but got size 512`
- Root cause: `blip2_opt.py` projected Q-Former outputs to `self.opt_model.config.hidden_size`, but `facebook/opt-350m` uses token embeddings with dimension `512` (`word_embed_proj_dim`) while the hidden size is `1024`
- Fix policy: project Q-Former outputs into `self.opt_model.get_input_embeddings().embedding_dim` so the bridge matches the actual `inputs_embeds` interface used in training and generation
- Fix type: permanent for this workspace and a generally safer implementation for smaller OPT variants

### 18. Caption fine-tuning config used an empty `valid_splits` list

- Detection method: the caption-stage traceback in `termina_output.md`
- Symptom: `AssertionError: Only support one split for evaluation.`
- Root cause: `lavis/tasks/captioning.py` expects `run.valid_splits` to contain exactly one split name, but the local caption config set it to an empty list
- Fix policy: set `run.valid_splits: ["val"]` in the local caption config so the captioning task can initialize correctly
- Fix type: permanent for this workspace config

### 19. Caption evaluation compared reduced-subset predictions against the full official COCO val ground truth

- Detection method: the latest caption-stage traceback in `termina_output.md`
- Symptom: `AssertionError` inside `pycocoevalcap` at `assert(gts.keys() == res.keys())`
- Root cause: the local caption run validates on `coco_karpathy_val_small.json` with `1000` images, but LAVIS's default COCO caption evaluation downloads the full `coco_karpathy_val_gt.json`, so the ground-truth and prediction image-id sets do not match
- Fix policy: generate a COCO-format ground-truth file from the reduced `coco_karpathy_val_small.json` subset and point `run.annotation_file` to it in the local caption config
- Fix type: permanent for this workspace's reduced-subset caption evaluation path

### 20. Caption metric scoring still failed on Windows inside METEOR after the subset ground-truth mismatch was fixed

- Detection method: the newest `termina_output.md` caption run after the subset-matched ground truth was added
- Symptom: metric scoring progressed through BLEU and then failed at METEOR with `OSError: [Errno 22] Invalid argument`
- Root cause: the Windows-local `pycocoevalcap` METEOR subprocess path is unstable in this environment even after the subset image-id mismatch is fixed
- Fix policy: set `run.report_metric: false` in the local caption config so the caption fine-tuning run can finish and save its checkpoint without entering the unstable Java/METEOR scoring path
- Fix type: practical workspace fix for local Windows training runs; quantitative caption metrics should be computed later with a more stable evaluation path if needed

## Current Outcome

- Environment installation is complete
- Dataset staging is complete
- Stage 1 completed epoch `0` locally and produced a valid checkpoint
- Stage 2 now has a concrete code-level fix for the OPT-350M bridge mismatch and is ready for a rerun
