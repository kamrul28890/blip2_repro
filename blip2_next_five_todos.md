# BLIP-2 Next Five To-Do's

This file summarizes what the latest run in `termina_output.md` proved, what failed, and what to do next.

## Current Situation

- Stage 1 training itself worked.
- The run completed epoch `0`.
- A valid checkpoint was saved at:

```text
D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\stage1_local\20260328142\checkpoint_0.pth
```

- The crash happened after checkpoint save, not during model training.
- The failure was caused by an unguarded `dist.barrier()` in `lavis/runners/runner_base.py` while running in non-distributed local mode.
- That runner bug has now been patched locally.

## 1. Keep The Existing Stage-1 Checkpoint

Do not retrain stage 1 just to recover the checkpoint. You already have it.

What to verify:

```powershell
Get-Item "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\stage1_local\20260328142\checkpoint_0.pth"
```

Why:

- The checkpoint is about 2.2 GB and was written successfully.
- The previous crash happened after saving it.
- Repeating stage 1 is optional now, not required.

## 2. Register The Checkpoint In Your Notes And Metrics

Record the exact path and what it represents.

Recommended fields:

- stage: `stage1`
- epoch: `0`
- source log: `termina_output.md`
- output directory: `repo_study/LAVIS/lavis/output/blip2_repro/stage1_local/20260328142`
- checkpoint path: the full absolute path above

Why:

- This avoids losing track of which checkpoint belongs to which run.
- You will need the exact path again for stage 2.

## 3. Decide Whether To Re-Run Stage 1 For A Clean Exit

You now have two valid paths:

Path A:
- Skip rerunning stage 1 and go straight to stage 2 using the saved checkpoint.

Path B:
- Re-run stage 1 once after the runner patch, only if you want a clean no-crash completion log.

If you choose Path B, use:

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
$config = (Resolve-Path '.\blip2_repro\configs\stage1_local.yaml').Path
.\scripts\run_logged_step.ps1 `
  -Stage stage3 `
  -Step stage1_local_post_barrier_fix `
  -WorkingDirectory .\repo_study\LAVIS `
  -Command ('"{0}" train.py --cfg-path "{1}"' -f $python, $config)
```

Why:

- The only reason to rerun is cleaner bookkeeping.
- It is not needed to unlock stage 2.

## 4. Start Stage 2 With The Saved Stage-1 Checkpoint

This is the real next technical step.

Run:

```powershell
.\blip2_repro\scripts\run_stage2_local.ps1 -Stage1Checkpoint "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\stage1_local\20260328142\checkpoint_0.pth"
```

What to watch for:

- GPU out-of-memory on the 3070
- OPT-350M download/load issues
- any new single-GPU distributed assumptions in stage 2

Why:

- Stage 1 already did its job: produce the bridge checkpoint.
- Stage 2 is the next assignment-relevant milestone.

## 5. If Stage 2 Fails Locally, Move The Exact Same Setup To A100

Do not redesign the workflow yet. First try the same patched repo and same checkpoint on stronger hardware.

Take with you:

- `blip2_repro/configs/`
- `blip2_repro/scripts/`
- `docs/blip2/`
- `metrics/blip2/`
- patched files under `repo_study/LAVIS/lavis/`
- the stage-1 checkpoint

Why:

- Your local stage 1 result already shows the setup is basically correct.
- The next likely blocker is compute, not project structure.
- Moving the same state to A100 gives the cleanest comparison and least extra debugging.

## Recommended Immediate Command

If you want the shortest path forward, do this next:

```powershell
.\blip2_repro\scripts\run_stage2_local.ps1 -Stage1Checkpoint "D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\stage1_local\20260328142\checkpoint_0.pth"
```
