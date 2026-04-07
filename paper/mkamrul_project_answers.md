# Project Answers for Term Paper

This document answers the project-status questions in a detailed, submission-ready way based on the completed implementation, the finished local training runs, and the current paper draft.

## 1. Which paper did you implement for the project section?

I implemented **BLIP-2**.

More specifically, I reviewed three candidate papers:

- **BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models**
- **LLaVA: Visual Instruction Tuning**
- **VisionLLM v2: An End-to-End Generalist Multimodal Large Language Model for Hundreds of Vision-Language Tasks**

I ultimately selected **BLIP-2** as the implementation target because it had the strongest student-scale reproduction story. Among the three, it is the most modular:

- it freezes the vision encoder,
- it freezes the language model,
- and it trains a relatively small bridge module called the **Q-Former**.

That design made it more practical to reproduce on a single local GPU than:

- **LLaVA**, whose value comes more from instruction tuning and conversational data alignment, and
- **VisionLLM v2**, which is much more ambitious as a generalist system and far too heavy for a faithful local reproduction.

So the project section of the paper is a **local reproduction study of BLIP-2** under student hardware constraints.

## 2. What did your implementation involve?

The implementation was much more than “running an existing repo.” It involved building a full local BLIP-2 training pipeline and making the official LAVIS code path work reliably in a single-GPU Windows environment.

At a high level, the implementation involved:

1. **Paper selection and technical comparison**
   - I first compared BLIP-2, LLaVA, and VisionLLM v2 as possible implementation targets.
   - I evaluated them on architecture, openness, compute realism, reproducibility, and educational value for a student project.

2. **Local BLIP-2 reproduction setup**
   - I used the official **Salesforce LAVIS** implementation as the base code path.
   - I configured the model to use:
     - **CLIP ViT-L** as the image encoder,
     - **OPT-350M** as the language model,
     - **224 image resolution**,
     - **32 query tokens**,
     - **mixed precision** and **gradient accumulation** to fit training into local VRAM.

3. **End-to-end three-stage training**
   - I reproduced the full BLIP-2 pipeline:
     - **Stage 1:** image-text representation learning
     - **Stage 2:** generative alignment to OPT
     - **Caption fine-tuning:** COCO captioning adaptation

4. **Dataset construction and scaling**
   - I created reduced, deterministic COCO Karpathy subsets for local training:
     - `10k / 1k / 1k`
     - `50k / 1k / 1k`
     - `100k / 1k / 1k`
   - I staged only the required subset images into the local LAVIS cache.

5. **Code fixes and engineering patches**
   - I had to patch several issues in order to make the official training path work locally:
     - local cache-path resolution fixes,
     - single-process / non-distributed guards,
     - caption dataset `image_id` handling fixes,
     - an **OPT-350M embedding-dimension bridge fix**,
     - subset-matched ground-truth generation for evaluation,
     - workarounds for unstable local Windows METEOR scoring,
     - optional/lazy `spacy` loading to avoid unrelated import failures,
     - downloader robustness improvements and resume-oriented training scripts.

6. **Checkpointing and automated training workflow**
   - I added per-epoch checkpoint saving.
   - I created simplified run scripts so long experiments could be resumed cleanly.
   - I also built a top-level local pipeline runner that can chain stages automatically.

7. **Offline evaluation tooling**
   - Because the checkpoint-producing caption runs could not rely on LAVIS’s default online scoring path in this environment, I evaluated saved `val_epoch*.json` prediction files afterward using subset-matched COCO-format ground truth.
   - This made it possible to score **every saved epoch** and choose the **best checkpoint by validation CIDEr**, rather than blindly using the last checkpoint.

In short, the implementation involved both:

- **model reproduction**, and
- **systems engineering** to make a research codebase operate reproducibly on constrained local hardware.

## 3. What were your actual experimental results?

### Main result summary

The strongest result in the project came from the **50k office-scale BLIP-2 run**, not from the later 100k long run.

The major quantitative findings are:

#### Paper reference result

BLIP-2 paper reference for COCO captioning:

- **Model:** BLIP-2 ViT-g OPT-2.7B
- **BLEU-4:** `43.7`
- **CIDEr:** `145.8`

#### Local 10k baseline

Dataset/schedule:

- `10k / 1k / 1k`
- Stage 1: `1` epoch
- Stage 2: `1` epoch
- Caption: `1` epoch

Results:

- **BLEU-1:** `33.40`
- **BLEU-2:** `10.66`
- **BLEU-3:** `3.45`
- **BLEU-4:** `1.45`
- **CIDEr:** `3.03`
- **Unique captions:** `61 / 1000`

Interpretation:

- This run proved the pipeline could run end-to-end.
- However, the output was heavily collapsed and repetitive.
- It was useful mainly as a methodological baseline, not as a strong model.

#### Local 50k office best

Dataset/schedule:

- `50k / 1k / 1k`
- Stage 1: `3` epochs
- Stage 2: `3` epochs
- Caption: best checkpoint selected from a `5`-epoch run

Best checkpoint:

- **epoch 3**

Results:

- **BLEU-1:** `53.86`
- **BLEU-2:** `33.52`
- **BLEU-3:** `19.65`
- **BLEU-4:** `11.13`
- **CIDEr:** `37.57`
- **Unique captions:** `563 / 1000`
- **Most common caption count:** `27`

Interpretation:

- This was the best overall run by BLEU-4 and CIDEr.
- It showed a major jump over the 10k baseline.
- It strongly reduced caption collapse and improved diversity.

#### Local 50k polish completion

Dataset/schedule:

- same `50k / 1k / 1k` data
- caption-only polish rerun
- checkpoint saved every epoch

Final epoch result:

- **BLEU-4:** `10.49`
- **CIDEr:** `37.14`
- **Unique captions:** `607 / 1000`

Interpretation:

- This run was useful because it preserved all caption checkpoints cleanly.
- But it still did **not beat** the earlier office epoch-3 best.

#### Local 100k student long run

Dataset/schedule:

- `100k / 1k / 1k`
- Stage 1: `10` epochs
- Stage 2: `10` epochs
- Caption: `15` epochs

Best checkpoint:

- **epoch 2**

Best epoch 2 results:

- **BLEU-1:** `47.63`
- **BLEU-2:** `27.81`
- **BLEU-3:** `15.95`
- **BLEU-4:** `8.57`
- **CIDEr:** `25.34`
- **Unique captions:** `677 / 1000`
- **Most common caption count:** `20`

Final epoch 14 results:

- **BLEU-1:** `42.86`
- **BLEU-2:** `23.24`
- **BLEU-3:** `12.24`
- **BLEU-4:** `6.61`
- **CIDEr:** `18.36`
- **Unique captions:** `734 / 1000`

Interpretation:

- The `100k` run **finished successfully**, so from a systems perspective it was a success.
- It improved diversity even more than the 50k run.
- However, it **did not beat** the 50k office best on BLEU-4 or CIDEr.
- It peaked very early and then degraded over later epochs.

### Comparison across completed runs

| Run | Scale | Selection | BLEU-4 | CIDEr | Unique captions |
|---|---:|---|---:|---:|---:|
| 10k baseline | 10k | final epoch 0 | 1.45 | 3.03 | 61 |
| 50k office best | 50k | best epoch 3 | 11.13 | 37.57 | 563 |
| 50k polish final | 50k | final epoch 4 | 10.49 | 37.14 | 607 |
| 100k long best | 100k | best epoch 2 | 8.57 | 25.34 | 677 |
| 100k long final | 100k | final epoch 14 | 6.61 | 18.36 | 734 |

### Qualitative outputs

The qualitative behavior changed significantly across scales:

- **10k baseline:** severe mode collapse, many captions repeated with generic person-centric phrasing.
- **50k office best:** much more diverse and often structurally plausible, though still generic and error-prone.
- **100k long run:** diversity improved further, but semantic correctness did not improve enough to beat the 50k metrics.

Representative qualitative issues included:

- predicting generic people captions for unrelated scenes,
- object substitutions,
- semantically plausible but incorrect descriptions,
- some partial improvement on simple object scenes like bathrooms, food, or common indoor layouts.

### Was it possible to take the best metric during training?

Yes, and this became one of the most important conclusions of the project.

Because I saved every caption epoch and evaluated every saved `val_epoch*.json`, I was able to select the **best checkpoint by validation CIDEr** instead of just taking the last epoch.

This mattered a lot:

- For the `50k` office run, the best checkpoint was **epoch 3**, not just “whatever finished last.”
- For the `100k` long run, the best checkpoint was **epoch 2**, and the final epoch 14 checkpoint was clearly worse.

So one concrete lesson from the experiments is:

> Under long student-scale BLIP-2 runs, the best checkpoint may occur well before the final epoch. Model selection should be metric-driven, not endpoint-driven.

## 4. What datasets did you use for training/evaluation?

The implementation used **COCO Karpathy captioning splits** as the base dataset.

More specifically, I used reduced local subsets derived from the COCO Karpathy annotations:

- **10k / 1k / 1k** train / validation / test
- **50k / 1k / 1k** train / validation / test
- **100k / 1k / 1k** train / validation / test

Important details:

- The subsets were created deterministically from the Karpathy splits.
- Only the corresponding subset images were staged into the local LAVIS image cache.
- Evaluation used subset-matched COCO-format ground-truth JSON files.
- The `50k` office and `100k` student runs used the **same 1k validation image set**, so their metrics are directly comparable.

So while the original BLIP-2 paper used a much larger multimodal pretraining mixture, my actual local reproduction used:

- **reduced COCO caption data only**, under a controlled scaling setup.

## 5. What is your paper's main thesis / argument?

Yes. The paper has a clear critical angle and a central thesis.

### Main thesis

The main thesis of the paper is:

> **BLIP-2 is reproducible as a staged training pipeline on student hardware, but not reproducible at paper-level captioning quality without large-scale compute, data, and backbone capacity.**

This thesis has two layers:

1. **Critique section thesis**
   - The three papers can be read as different points in the evolution of multimodal systems:
     - **BLIP-2:** modular alignment through a bridge between frozen backbones
     - **LLaVA:** instruction-following multimodal behavior through visual instruction tuning
     - **VisionLLM v2:** ambitious generalist multimodal perception across many task families
   - The critical argument is that as these systems evolve, they trade off:
     - modularity,
     - compute realism,
     - task breadth,
     - engineering burden,
     - and reproducibility.

2. **Project-section thesis**
   - BLIP-2 was selected because it preserves a meaningful methodological core after downscaling.
   - The project then tests the difference between:
     - **pipeline-level reproduction**, and
     - **performance-level reproduction**.
   - The final results show that the pipeline can be reproduced end-to-end locally, but the published performance cannot be matched under student-scale constraints.

### Critical angle in more explicit form

If I were to state the critique angle in one sentence, it would be:

> These three papers represent a progression from modular multimodal alignment (BLIP-2) to instruction-following multimodal assistants (LLaVA) to generalist perception-oriented multimodal systems (VisionLLM v2), but each step toward broader capability also increases dependence on scale, engineering complexity, and compute, which sharply reduces reproducibility for student researchers.

### Why that angle works

This angle works well because it lets the paper do more than summarize three systems. It gives the critique section a real analytical purpose:

- Why BLIP-2 is the most practical implementation target
- Why LLaVA is attractive but less ideal for this particular project
- Why VisionLLM v2 is intellectually impressive but operationally unrealistic here
- Why reproducibility itself is a meaningful scientific criterion, not just a convenience issue

## 6. What is your user ID (for the filename, anonymized — don't include your name in the paper itself)?

Based on your Purdue email, the anonymized user ID should be:

- **`mkamrul`**

I would use `mkamrul` for filenames and identifiers in submission materials.

You should **not** put your full name in the anonymous paper itself.

## 7. Do you have a draft I can read?

Yes.

The current draft is here:

- `paper/term_paper.tex`

The compiled PDF is here:

- `paper/term_paper.pdf`

Current status of the draft:

- It already includes the critique section.
- It already includes the completed BLIP-2 reproduction study.
- It now includes the finished `100k` run outcome.
- It now explicitly explains best-checkpoint selection during training.
- It now contains comparison tables across the completed runs.

What is still potentially polishable:

- author formatting / final presentation styling
- a few wording improvements in the abstract and conclusion
- optional additional qualitative examples
- any instructor-specific formatting or packaging requirements

## User identity note

For administrative/reference purposes only:

- **User ID:** `mkamrul`
- **Email:** `mkamrul@purdue.edu`
- **Full name:** `Md Kamruzzaman Kamrul`

Do **not** include the full name inside the anonymous paper body if the submission is supposed to remain anonymized.
