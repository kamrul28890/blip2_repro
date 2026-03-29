# Submission Notes

This folder contains the completed anonymous ACL-style term paper and its build artifacts.

## Main Deliverable

- Final PDF: `paper/term_paper.pdf`
- LaTeX source: `paper/term_paper.tex`
- Bibliography used by the paper: `paper/term_paper.bib`

## Metric Sources Used In The Paper

- Final caption predictions:
  `repo_study/LAVIS/lavis/output/blip2_repro/caption_local_opt350m/20260328225/result/val_epoch0.json`
- Subset-matched COCO ground truth:
  `repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_small_gt.json`
- Reproducible evaluation summary:
  `metrics/blip2/caption_eval_summary.json`
- Qualitative examples used in the report:
  `metrics/blip2/caption_eval_examples.json`

## Final Numbers Reported

- Stage 1 train loss: `0.326`
- Stage 2 train loss: `0.294`
- Caption fine-tuning train loss: `0.227`
- BLEU-1: `33.40`
- BLEU-2: `10.66`
- BLEU-3: `3.45`
- BLEU-4: `1.45`
- CIDEr: `3.03`
- Unique captions in 1000 predictions: `61`

## What Still Needs A Manual Rename

The assignment wants a final PDF named `your_userid.pdf`. Rename `term_paper.pdf` at submission time once you decide the exact userid-based filename.

## Related Assignment Prep Files

- Paper-selection bibliography draft: `paper/paper_selection_submission.bib`
- Presentation outline: `presentation/presentation_outline.md`
- Peer-review template: `peer_review/review_template.txt`
