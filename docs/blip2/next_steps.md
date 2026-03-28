# Next Steps

## Immediate

1. Run a longer logged stage-1 local session so epoch `0` can finish and emit a checkpoint.
2. Monitor the newest stage-3 log while that run is active.
3. If the 3070 run does not produce a checkpoint in a reasonable window, move the exact current repo state to an A100 machine before changing configs again.

Recommended command:

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
$config = (Resolve-Path '.\blip2_repro\configs\stage1_local.yaml').Path
.\scripts\run_logged_step.ps1 `
  -Stage stage3 `
  -Step stage1_local_long_run `
  -WorkingDirectory .\repo_study\LAVIS `
  -Command ('"{0}" train.py --cfg-path "{1}"' -f $python, $config)
```

To watch the latest log:

```powershell
$latest = Get-ChildItem .\logs\blip2\stage3 -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $latest.FullName -Wait
```

## After Stage-1 Checkpoint Exists

1. Register the checkpoint path in `metrics/blip2/checkpoint_registry.jsonl`.
2. Launch stage 2 with the same workspace venv.

Recommended command:

```powershell
.\blip2_repro\scripts\run_stage2_local.ps1 -Stage1Checkpoint "<absolute-path-to-stage1-checkpoint>"
```

## If You Switch To A100

1. Reuse the current workspace, configs, and LAVIS patches first.
2. Re-run the same stage-1 logged command before making new dependency or config changes.
3. Only reduce local constraints like batch size after you see the A100 behavior.

## Fallback Policy

If the primary environment path fails because `fairscale` or `import lavis` is blocked after the planned install sequence, recreate the venv and retry with:

- `torch==2.2.2`
- `torchvision==0.17.2`
- `torchaudio==2.2.2`
- `--index-url https://download.pytorch.org/whl/cu121`
