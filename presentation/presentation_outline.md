# Presentation Outline

## Slide 1: Title

- Critique of BLIP-2, LLaVA, and VisionLLM v2
- Local BLIP-2 reproduction on a single RTX 3070

## Slide 2: Assignment Scope

- Read and critique three recent papers
- Implement one non-trivial paper
- Evaluate and compare with the paper

## Slide 3: The Three Papers

- BLIP-2: frozen image encoder plus frozen LLM with Q-Former bridge
- LLaVA: visual instruction tuning for assistant-style behavior
- VisionLLM v2: end-to-end multimodal generalist with multiple decoders

## Slide 4: Critique Summary

- BLIP-2: best downscaling story, still paper-scale expensive
- LLaVA: simple and relevant, but still wants moderate multi-GPU compute
- VisionLLM v2: strongest scope, weakest reproducibility for a class project

## Slide 5: Why BLIP-2 Was Chosen

- Core idea survives aggressive downscaling
- Official LAVIS codebase exists
- Modular frozen-backbone design is reproducible under limited compute

## Slide 6: Local Experimental Setup

- Hardware: 1x RTX 3070 8GB
- Vision encoder: CLIP ViT-L
- Language model: OPT-350M
- Data: reduced COCO Karpathy split, `10k/1k/1k`
- Training: 3 epochs for stage 1, 3 epochs for stage 2, and 5 epochs for caption fine-tuning on the office 50k split

## Slide 7: Engineering Work

- Fixed local data path resolution
- Patched single-GPU non-distributed issues
- Fixed OPT embedding-dimension bridge mismatch
- Built subset-matched COCO ground truth for evaluation
- Disabled unstable Windows METEOR path for final checkpoint generation

## Slide 8: Quantitative Results

- Stage 1 office train loss: `0.412`
- Stage 2 office train loss: `0.767`
- Best caption fine-tuning train loss: `0.367`
- Local BLEU-4: `11.13` vs paper `43.7`
- Local CIDEr: `37.57` vs paper `145.8`

## Slide 9: Qualitative Results

- `563` unique captions across `1000` predictions
- Most common caption appears `27` times
- Show 3 to 5 failure examples from `metrics/blip2/caption_eval_examples_office_epoch3.json`

## Slide 10: Conclusion

- Pipeline-level reproduction succeeded
- Performance parity did not
- Main causes: smaller backbones, tiny dataset, one-epoch schedule, Windows evaluation friction
- BLIP-2 was still the right paper choice for this assignment
