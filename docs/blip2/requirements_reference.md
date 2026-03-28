# Requirements Reference

## Source of Truth

- Upstream requirements: `repo_study/LAVIS/requirements.txt`
- Effective local requirements: `docs/blip2/requirements_effective.txt`
- Editable package install target: `repo_study/LAVIS`

## Effective Install Policy

The workspace uses the project venv only:

- Interpreter: `D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\.venv\Scripts\python.exe`
- Do not use system Python, a Conda environment, or any user-home `.venv`

## Effective Changes Relative to Upstream

The following lines are intentionally removed from the effective requirements file because PyTorch is installed first from the official CUDA wheel index:

- `torch>=1.10.0`
- `torchvision`
- `torchaudio`

The following compatibility substitutions are required on this Windows + Python 3.10 environment:

- Upstream: `open3d==0.13.0`
- Effective: `open3d==0.19.0`
- Added: `numpy<2`
- Upstream: `moviepy`
- Effective: `moviepy==1.0.3`
- Upstream: `peft`
- Effective: `peft==0.5.0`
- Added: `huggingface-hub==0.19.4`

The following package remained unchanged initially and then received a Windows-specific companion package after runtime validation failed:

- Keep `python-magic`
- Add `python-magic-bin==0.4.14`

## Planned Install Order

1. Upgrade pip, wheel, and setuptools in the workspace venv
2. Install `torch==2.4.1`, `torchvision==0.19.1`, and `torchaudio==2.4.1` from the official `cu121` index
3. Install `docs/blip2/requirements_effective.txt`
4. Install editable LAVIS with `--no-deps`

## Verified Compatibility Notes

- The effective requirements install resolves on this machine after the listed substitutions
- `open3d==0.13.0` does not resolve for this Python/Windows combination
- `opencv-python-headless==4.5.5.64` needs `numpy<2` on this machine
- `moviepy==1.0.3` is required because newer `moviepy` releases break the `moviepy.editor` import path used by LAVIS
- `peft==0.5.0` is required to stay compatible with `transformers==4.33.2`
- `huggingface-hub==0.19.4` is required so `diffusers<=0.16.0` can still import `cached_download`
- `python-magic-bin==0.4.14` resolves the missing `libmagic` runtime on Windows
- Java is required later by `pycocoevalcap` for caption metrics
