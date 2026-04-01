# Submission Notes

This folder contains the completed anonymous ACL-style term paper and its build artifacts.

## Main Deliverable

- Final PDF: `paper/term_paper.pdf`
- LaTeX source: `paper/term_paper.tex`
- Bibliography used by the paper: `paper/term_paper.bib`

## Metric Sources Used In The Paper

- Best local caption predictions:
  `repo_study/LAVIS/lavis/output/blip2_repro/caption_office_50k_opt350m/20260331152/result/val_epoch3.json`
- Subset-matched COCO ground truth:
  `repo_study/LAVIS/cache/coco/annotations/coco_karpathy_val_office_1k_gt.json`
- Reproducible evaluation summary for the best office snapshot:
  `metrics/blip2/caption_eval_summary_office_epoch3.json`
- Completed caption polish rerun summary:
  `metrics/blip2/caption_eval_summary_office_polish_epoch4.json`
- Qualitative examples used in the report:
  `metrics/blip2/caption_eval_examples_office_epoch3.json`

## Final Numbers Reported

- Stage 1 office train loss: `0.412`
- Stage 2 office train loss: `0.767`
- Best caption fine-tuning train loss used for comparison: `0.367`
- BLEU-1: `53.86`
- BLEU-2: `33.52`
- BLEU-3: `19.65`
- BLEU-4: `11.13`
- CIDEr: `37.57`
- Unique captions in 1000 predictions: `563`
- Caption polish rerun completed through epoch 4, but epoch 3 remained the best metric snapshot

## What Still Needs A Manual Rename

The assignment wants a final PDF named `your_userid.pdf`. Rename `term_paper.pdf` at submission time once you decide the exact userid-based filename.

## Related Assignment Prep Files

- Paper-selection bibliography draft: `paper/paper_selection_submission.bib`
- Presentation outline: `presentation/presentation_outline.md`
- Peer-review template: `peer_review/review_template.txt`
