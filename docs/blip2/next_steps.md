# Next Steps

## Immediate

1. Publish the repo with Git LFS so the staged COCO images and final checkpoints travel with the documentation.
2. Keep `paper/term_paper.pdf` as the canonical anonymous report and rename it to your userid-based filename only at submission time.
3. Use `paper/SUBMISSION_NOTES.md` as the handoff index for the paper, metrics, presentation outline, and review template.

Key publishable artifacts:

```powershell
D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\paper\term_paper.pdf
D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\metrics\blip2\caption_eval_summary.json
D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\metrics\blip2\caption_eval_examples.json
D:\Purdue\Courses\04. Spring 2026 ECE 59500-073 LEC\Term Paper\repo_study\LAVIS\lavis\output\blip2_repro\caption_local_opt350m\20260328225\checkpoint_0.pth
```

## Best Improvement Path On The Same Machine

1. Re-run the pipeline with the stronger configs:
   - `blip2_repro/configs/stage1_better_local.yaml`
   - `blip2_repro/configs/stage2_better_local_opt350m.yaml`
   - `blip2_repro/configs/caption_better_local_opt350m.yaml`
2. Recompute metrics with `blip2_repro/scripts/run_caption_eval.ps1`.
3. Compare the new `metrics/blip2/caption_eval_summary.json` against the baseline.

## If You Switch To Better Compute

1. Reuse the same repo, scripts, docs, and patches first.
2. Increase dataset size before changing the model family.
3. Scale `max_epoch`, `batch_size_train`, `accum_grad_iters`, and `image_size` through config changes rather than rewriting the workflow.
4. Use `docs/blip2/improvement_playbook.md` as the scaling guide.

## Fallback Policy

If the primary environment path fails because `fairscale` or `import lavis` is blocked after the planned install sequence, recreate the venv and retry with:

- `torch==2.2.2`
- `torchvision==0.17.2`
- `torchaudio==2.2.2`
- `--index-url https://download.pytorch.org/whl/cu121`
