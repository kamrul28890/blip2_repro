# Term Paper Blueprint

This file is the working blueprint for expanding `paper/term_paper.tex` into a more thesis-style technical report while keeping the existing ACL structure.

Use this as the writing guide for drafting sections now and updating only the result-dependent parts after the current `100k` run finishes.

## Core Thesis

The paper should argue one main point clearly and repeatedly:

`BLIP-2 is reproducible as a staged training pipeline on student hardware, but not reproducible at paper-level captioning quality without large-scale compute, data, and backbone capacity.`

That thesis should appear in:

- the abstract
- the end of the introduction
- the results discussion
- the conclusion

## Tone and Writing Standard

Write this paper as if it were halfway between:

- an ACL-style reproduction report
- a systems-heavy thesis chapter

That means:

- define the method precisely
- explain implementation details at the level of real engineering decisions
- justify every deviation from the original paper
- distinguish clearly between reproduction of the pipeline and reproduction of the reported performance
- report limitations honestly

## Section-by-Section Writing Plan

## 1. Abstract

### Goal

Provide a full project summary in one paragraph:

- what papers were reviewed
- why BLIP-2 was chosen
- what was reproduced
- how the reproduction was scaled down
- what succeeded
- what failed to match the paper

### Draft Content To Include Now

- compare BLIP-2, LLaVA, and VisionLLM v2
- state that BLIP-2 was selected because its modular bridge-learning design survives downscaling
- state that the local system uses LAVIS, CLIP-L, OPT-350M, and reduced COCO Karpathy subsets
- state that all three training stages completed locally
- state that the best current completed result is the office `50k / 1k / 1k` run

### Update Later

- add the final `100k` result if it beats the `50k` result

### Evidence Sources

- `paper/term_paper.tex`
- `docs/blip2/experiment_ledger.md`
- `metrics/blip2/report_metrics_snapshot.json`

## 2. Introduction

### Goal

Frame the problem and establish why this reproduction is worth doing.

### Paragraph Plan

Paragraph 1:

- explain the rise of vision-language models
- explain that modern multimodal systems combine large pretrained vision and language backbones
- note that paper-level performance often depends on compute that is inaccessible to students

Paragraph 2:

- explain the assignment structure: critique three papers and implement one
- introduce BLIP-2, LLaVA, and VisionLLM v2 as the candidate set

Paragraph 3:

- state why BLIP-2 is the best choice
- emphasize modularity, frozen backbones, and bridge-only learning

Paragraph 4:

- state the paper's central thesis explicitly
- define the difference between `pipeline-level reproduction` and `performance-level reproduction`

### Key Technical Points

- BLIP-2 is not easy in an absolute sense
- it is simply the most downscalable of the three
- the reproduction is scientifically useful because it exposes which parts of the original result are scale-sensitive

## 3. Paper Critique

This section already exists, but it should be expanded and made more technical.

### 3.1 BLIP-2

Add explicit discussion of:

- frozen image encoder
- Q-Former as bottleneck
- frozen LLM
- stage-1 objectives
- stage-2 generative alignment
- why the modularity matters for reproducibility

Add one paragraph clarifying that "compute-efficient" in the paper is only relative to prior multimodal models, not actually cheap.

### 3.2 LLaVA

Add explicit discussion of:

- visual instruction tuning
- dependence on synthetic GPT data
- stronger conversational alignment but weaker architectural modularity for a reproduction study

### 3.3 VisionLLM v2

Add explicit discussion of:

- generalist objective
- decoder-heavy architecture
- systems complexity as a reproducibility barrier

### 3.4 Comparison and Paper Choice

Strengthen this subsection by making the choice criteria explicit:

- conceptual clarity
- public implementation availability
- compute realism
- ablation value under downscaling
- engineering tractability

## 4. Project Section

Rename this section in the actual paper to something more thesis-like if you want stronger presentation.

Recommended replacement:

- `Reproduction Study`

Then expand it into the following subsections.

## 4.1 Objective and Scope

### Goal

Define exactly what this project tries to reproduce.

### Write Now

- not a full-scale replication of the paper's training regime
- yes: reproduce the staged BLIP-2 training pipeline
- yes: obtain valid stage checkpoints
- yes: produce caption outputs and evaluate them reproducibly
- no: match paper-scale training data or compute
- no: claim direct metric parity with the published result

### Key Phrase To Use

`The target of reproduction was methodological fidelity under aggressive scaling constraints, not paper-scale replication.`

## 4.2 BLIP-2 Method Overview

This section should be added as a new subsection before the experimental setup.

### Goal

Explain BLIP-2 technically enough that the reader understands what each training stage is doing.

### Subsection Plan

#### Vision encoder

- frozen CLIP-style image encoder
- outputs visual embeddings

#### Q-Former

- small trainable transformer
- uses learned query tokens
- extracts language-relevant visual information

#### Frozen language model

- receives projected Q-Former outputs
- remains frozen while the bridge is trained

#### Stage 1

- image-text representation learning
- explain the three losses:
  - image-text contrastive loss
  - image-text matching loss
  - language modeling loss

#### Stage 2

- align visual query outputs to the frozen LLM for generation
- explain why this stage is needed after representation pretraining

#### Caption fine-tuning

- task-specific adaptation on COCO captions
- explain how this differs from stage 2

### Helpful Repo Evidence

- `repo_study/LAVIS/lavis/models/blip2_models/blip2_qformer.py`
- `repo_study/LAVIS/lavis/models/blip2_models/blip2_opt.py`

## 4.3 Experimental Environment

### Goal

Make the compute and software environment explicit.

### Content To Include

- hardware: RTX 3070 8GB
- operating system: Windows desktop environment
- Python version used in the workspace
- PyTorch and CUDA environment
- editable LAVIS installation
- Java dependency for caption metrics
- local file layout for annotations, images, outputs, and metrics

### Important Argument

The environment was not just incidental context. It materially shaped:

- training feasibility
- evaluation feasibility
- required patches

### Evidence Sources

- `README.md`
- `docs/blip2/README.md`
- `docs/blip2/requirements_reference.md`
- `docs/blip2/failures_and_fixes.md`

## 4.4 Dataset Construction and Evaluation Protocol

### Goal

Describe how the local datasets differ from the paper and how evaluation was made reproducible.

### Paragraph Plan

Paragraph 1:

- introduce COCO Karpathy splits
- explain why COCO captioning is used

Paragraph 2:

- describe the `10k / 1k / 1k` baseline subset
- describe the `50k / 1k / 1k` office subset
- describe the `100k / 1k / 1k` student-scale long run

Paragraph 3:

- explain subset generation and deterministic shuffling
- explain image staging policy

Paragraph 4:

- explain why default evaluation was not enough
- subset-matched ground truth had to be generated
- BLEU and CIDEr were computed offline from saved predictions

### Tables To Add

Add a table listing:

- split name
- train rows
- val rows
- test rows
- unique images
- intended purpose

### Evidence Sources

- `docs/blip2/data_layout.md`
- `blip2_repro/tools/make_json_subset.py`
- `blip2_repro/tools/build_coco_gt_from_karpathy_subset.py`
- `blip2_repro/tools/evaluate_caption_subset.py`

## 4.5 Experimental Setup

This section exists, but should become more explicit and comparison-driven.

### Goal

Show exactly how the local setup differs from the paper.

### Keep

- paper vs local comparison table

### Expand With

- separate rows for `10k`, `50k`, and `100k`
- note the long-run desktop plan of `10 / 10 / 15`
- explicitly distinguish:
  - paper backbones
  - local backbones
  - paper data scale
  - local data scale
  - paper training budget
  - local training budget

### Evidence Sources

- `docs/blip2/experiment_ledger.md`
- `metrics/blip2/report_metrics_snapshot.json`

## 4.6 Implementation Details

This should become one of the longest and strongest sections.

### Goal

Show that the project involved real technical reasoning, not just launching stock configs.

### Suggested Subsections

#### Data path resolution

- LAVIS cache assumptions
- why local paths had to be overridden

#### Single-process / non-distributed fixes

- collective ops in a single-GPU setting
- barrier guards
- rank assumptions

#### Caption dataset handling fix

- why `image_id` handling was wrong for the local captioning path

#### OPT-350M bridge compatibility fix

- why the bridge dimension had to match the actual token-embedding dimension
- why this mattered for smaller OPT variants

#### Evaluation tooling

- subset-matched ground truth generation
- offline BLEU/CIDEr computation
- disabling unstable METEOR path during checkpoint-producing runs

#### Checkpointing and resume strategy

- save every epoch
- resume behavior
- long-run automation

#### Dataset downloader behavior

- downloader progress and the lack of request timeout
- stale worker hang after image staging completed
- why this mattered for the `100k` run setup

### Evidence Sources

- `docs/blip2/failures_and_fixes.md`
- `blip2_repro/scripts/*.ps1`
- `blip2_repro/scripts/run_student_100k_long_pipeline.ps1`
- `repo_study/LAVIS/lavis/models/blip2_models/blip2_opt.py`
- `repo_study/LAVIS/lavis/models/img2prompt_models/img2prompt_vqa.py`

## 4.7 Training Procedure

### Goal

Describe each training campaign as an experiment, not as a casual note.

### Recommended Structure

#### 10k baseline

- `1 / 1 / 1`
- objective: get the full pipeline running end to end
- outcome: severe caption collapse

#### 50k office run

- `3 / 3 / 5`
- objective: improve quality through larger subset and longer training
- outcome: large gain in BLEU/CIDEr and caption diversity

#### 50k polish run

- caption-only rerun with per-epoch checkpoint saving
- objective: finish a clean caption schedule and preserve all epochs
- outcome: completed cleanly but did not beat the earlier epoch-3 snapshot

#### 100k desktop long run

- `10 / 10 / 15`
- objective: push the best student-scale result further
- note that this section can be written now, with final metrics filled in later

### Suggested Table

Add an experiment table with columns:

- experiment name
- split size
- stage 1 epochs
- stage 2 epochs
- caption epochs
- batch size
- accumulation
- image size
- checkpoint policy
- status

## 4.8 Results and Evaluation

This section should be reorganized into staged subsections.

### 4.8.1 10k Baseline Results

Write now using:

- BLEU-4 `1.45`
- CIDEr `3.03`
- unique captions `61`
- severe mode collapse examples

### 4.8.2 50k Office Results

Write now using:

- stage-1 losses: `0.525 -> 0.454 -> 0.412`
- stage-2 losses: `0.473 -> 0.802 -> 0.767`
- best caption result at epoch 3
- BLEU-4 `11.13`
- CIDEr `37.57`
- unique captions `563`

### 4.8.3 50k Polish Results

Write now using:

- completed caption rerun through epoch 4
- BLEU-4 `10.49`
- CIDEr `37.14`
- why best-epoch selection matters

### 4.8.4 100k Results

Create this subsection now, but mark the metric table as pending while training is running.

Suggested placeholder wording:

`At the time of writing, the long-run 100k desktop experiment is in progress. The final comparison table will be updated once stage 2, caption fine-tuning, and per-epoch evaluation complete.`

### Tables To Include

1. Paper vs local metrics
2. Baseline vs office vs polish vs 100k comparison
3. Diversity statistics across runs

## 4.9 Qualitative Analysis

### Goal

Interpret caption behavior, not just scores.

### Paragraph Plan

Paragraph 1:

- describe collapse in the `10k` run

Paragraph 2:

- describe how `50k` improves diversity and visual grounding somewhat

Paragraph 3:

- describe remaining failure modes:
  - generic person-centric captions
  - object hallucination
  - failure to capture scene-specific details
  - template repetition

Paragraph 4:

- update later with `100k` examples if the run improves quality

### Evidence Sources

- `metrics/blip2/caption_eval_examples.json`
- `metrics/blip2/caption_eval_examples_office_epoch3.json`
- `metrics/blip2/caption_eval_examples_office_polish_epoch4.json`

## 4.10 Failure Analysis

Expand this into a more formal analytical section.

### Subsections To Add

#### Scale mismatch

- paper-scale data and steps versus local subsets

#### Backbone mismatch

- ViT-g / OPT-2.7B versus CLIP-L / OPT-350M

#### Optimization-budget mismatch

- fewer epochs and fewer effective updates in early runs

#### Evaluation mismatch

- local validation subset versus paper test split

#### Environment friction

- Windows-specific evaluation and dependency issues

#### Engineering overhead

- the cost of making the official code path work in the constrained setup

### Key Argument

The paper-performance gap should be explained primarily by scale and architecture differences, not framed as a mysterious failure of the reproduction.

## 5. Threats to Validity

Add this as a new top-level section before the conclusion.

### What To Include

- subset metrics are not directly comparable to the paper's full COCO test numbers
- validation subset is not the same as Karpathy test split
- code patches may alter behavior from stock LAVIS
- local hardware and software stack differ materially from the original training regime
- some comparisons are between completed local runs and an in-progress `100k` run

This section will make the paper feel much stronger and more credible.

## 6. Reproducibility and Artifacts

Add this as another top-level section before the conclusion.

### Goal

Summarize what an external reader would need to rerun the work.

### Include

- configs
- scripts
- logs
- metrics
- run registry
- checkpoint registry
- qualitative examples

### Key Sources

- `README.md`
- `docs/blip2/README.md`
- `docs/blip2/experiment_ledger.md`
- `metrics/blip2/run_registry.jsonl`
- `metrics/blip2/checkpoint_registry.jsonl`

## 7. Conclusion

### Goal

Restate the contribution without overselling.

### Paragraph Plan

Paragraph 1:

- BLIP-2 was the correct implementation target among the three papers

Paragraph 2:

- the local project successfully reproduced the staged training pipeline

Paragraph 3:

- the local system did not achieve paper-level captioning quality

Paragraph 4:

- the most important research lesson is that modular reproducibility does not imply performance reproducibility

### Update Later

- add one sentence summarizing whether the `100k` run further narrowed the gap

## Immediate Editing Plan For `term_paper.tex`

The next edit pass should:

1. keep the existing abstract, introduction, critique, results, and conclusion as the base
2. insert a new method-focused subsection after `Objective and Scope`
3. split the current implementation and results material into more granular subsections
4. add new top-level sections:
   - `Threats to Validity`
   - `Reproducibility and Artifacts`
5. leave placeholders only in the `100k` result paragraphs and one sentence in the abstract/conclusion

## Tables To Prepare

These tables should exist in the final paper:

1. paper critique comparison table
2. paper-vs-local setup table
3. experiment schedule table across `10k`, `50k`, polish, and `100k`
4. metric comparison table across runs
5. caption diversity table across runs
6. qualitative examples table

## Figures To Consider

If space allows, add:

- a BLIP-2 training pipeline diagram
- a simplified local reproduction workflow diagram
- a timeline / run lineage figure showing `10k -> 50k -> 100k`

## Final Sections That Depend On The Current Run

Only these parts should wait for the current `100k` run:

- the final sentence of the abstract
- the `100k` subsection in results
- one paragraph in qualitative analysis
- one sentence in the conclusion

Everything else can be drafted immediately.
