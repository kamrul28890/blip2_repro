# Install Progress

This log records install and verification work in chronological order. Raw command output is stored under `logs/blip2/`, while the machine-readable record for each command is appended to `metrics/blip2/install_attempts.jsonl`.

## Timeline

| Timestamp | Step | Status | Notes |
| --- | --- | --- | --- |
| 2026-03-28 | Bootstrap scaffold | Complete | Created docs, logs, metrics roots and the logged PowerShell runner |
| 2026-03-28 | Requirements analysis | Complete | Confirmed workspace venv path, annotation files, reduced subset counts, missing COCO images, and missing Java |
| 2026-03-28 | Effective manifest | Complete | Materialized `requirements_effective.txt` and then updated it with all Windows/runtime compatibility fixes actually needed on this machine |
| 2026-03-28 | Packaging tools | Complete | Upgraded `pip`, `setuptools`, and `wheel` in the workspace venv |
| 2026-03-28 | Java install | Complete | Installed Temurin 8 JRE; validated with the full executable path because fresh shell sessions still needed a `PATH` refresh |
| 2026-03-28 | PyTorch CUDA stack | Complete | Installed `torch==2.4.1`, `torchvision==0.19.1`, `torchaudio==2.4.1` from the official `cu121` index |
| 2026-03-28 | Effective requirements | Complete | Installed effective requirements after compatibility pinning for `open3d`, `numpy`, `moviepy`, `peft`, `huggingface-hub`, and `python-magic-bin` |
| 2026-03-28 | Editable LAVIS install | Complete | Installed `repo_study/LAVIS` with `--no-deps` |
| 2026-03-28 | Environment smoke tests | Complete | Verified interpreter, `pip list`, CUDA, imports, `nvidia-smi`, and `python-magic` |
| 2026-03-28 | COCO subset image staging | Complete | Staged all `11671` unique reduced-subset images after one manual retry for an HTTP `503` |
| 2026-03-28 | Stage-1 smoke attempt 1 | Failed | Used wrong effective cache root, downloaded/expected data under `/export/home/.cache/lavis`, and missed the prepared local image cache |
| 2026-03-28 | Stage-1 smoke attempt 2 | Failed | Reached the correct reduced dataset, then hit `dist.get_rank()` with no initialized process group |
| 2026-03-28 | Stage-1 smoke attempt 3 | Failed | Reached the first training step, then hit a caption-dataset `image_id` vs retrieval-tensor mismatch |
| 2026-03-28 | Stage-1 smoke attempt 4 | Timed out externally | After the local config and single-GPU patches, the run loaded the intended `10000/1000/1000` dataset and kept training until the command timeout stopped it |

## Notes

- Raw command output is stored under `logs/blip2/`
- Machine-readable command history is stored in `metrics/blip2/install_attempts.jsonl`
- The latest successful stage-1 launch log is `logs/blip2/stage3/20260328_044436_stage1_local_smoke_non_dist_and_caption_fix.log`
- No stage-1 checkpoint exists yet because the longest local run was stopped by timeout before epoch completion

## Installed Versions

- Python: `3.10.11`
- pip: `26.0.1`
- PyTorch: `2.4.1+cu121`
- GPU: `NVIDIA GeForce RTX 3070`
- Java: `OpenJDK 1.8.0_482 (Temurin)`
