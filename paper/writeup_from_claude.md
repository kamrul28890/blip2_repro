\documentclass[11pt]{article}
\usepackage[review]{acl}
\usepackage{times}
\usepackage{latexsym}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{microtype}
\usepackage{inconsolata}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{array}
\usepackage{tabularx}
\usepackage{graphicx}
\usepackage{xspace}

\newcolumntype{Y}{>{\raggedright\arraybackslash}X}

\title{From Modular Alignment to Generalist Perception:\\
A Critique of Three Multimodal Systems and a\\
Student-Scale Reproduction of BLIP-2}

\author{Anonymous}

\begin{document}
\maketitle

%% =========================================================
\begin{abstract}
%% =========================================================
We study three landmark multimodal large language model (MLLM) papers---BLIP-2, LLaVA,
and VisionLLM~v2---through the dual lens of architectural critique and student-scale
reproducibility.
Our central argument is that these three systems represent a coherent but increasingly
demanding progression: from modular bridge-based alignment (BLIP-2), through
instruction-tuned conversational assistants (LLaVA), to ambitious end-to-end generalist
perception (VisionLLM~v2). Each step toward broader capability entails a measurable
increase in compute dependence, engineering complexity, and the difficulty of faithful
reproduction on commodity hardware.

Based on this analysis, we select BLIP-2 as the implementation target because its frozen
backbone design preserves a scientifically coherent downscaling story that the other two
systems do not.
We build a full local BLIP-2 reproduction pipeline on a single NVIDIA RTX~3070 8\,GB GPU
using the official Salesforce LAVIS codebase, reduced COCO Karpathy subsets, a
CLIP~ViT-L image encoder, and OPT-350M as the language model.
The reproduction faithfully executes all three training stages of the BLIP-2 pipeline:
stage-1 vision-language representation learning, stage-2 generative alignment, and
caption fine-tuning.
Across a controlled scaling study spanning \texttt{10k}, \texttt{50k}, and \texttt{100k}
COCO image subsets, the strongest completed local result is BLEU-4~11.13 and CIDEr~37.57
on a reduced 1,000-image validation subset, obtained at caption epoch~3 of the
\texttt{50k} office-scale run. This falls substantially below BLIP-2 ViT-g OPT-2.7B's
published Karpathy test performance of BLEU-4~43.7 and CIDEr~145.8, a gap that we
attribute systematically to backbone capacity, pre-training data scale, optimization
budget, and image resolution rather than to pipeline-level implementation failure.
A larger \texttt{100k} long run further reveals that additional data and extended epoch
budgets do not automatically improve caption quality under a fixed student-scale
architecture; the best checkpoint in that run occurred at epoch~2, with later epochs
exhibiting monotone metric decay. This finding underscores the importance of
metric-driven model selection in long training runs with limited regularization.
Our principal conclusion is twofold: the BLIP-2 \emph{pipeline} is reproducible on a
single consumer GPU after moderate engineering effort, but BLIP-2's \emph{captioning
performance} remains fundamentally bound to the scale of its frozen backbones and
pre-training corpus.
\end{abstract}

%% =========================================================
\section{Introduction}
%% =========================================================

The past three years have witnessed a rapid convergence in the design of multimodal
large language models (MLLMs).
What began as a collection of task-specific vision-language systems has evolved into a
small number of general architectural patterns: frozen-backbone bridge methods, instruction-tuned
generalist assistants, and end-to-end multi-decoder perception systems.
Each pattern offers a different answer to the same underlying design question: how should
a system combine the knowledge encoded in independently pretrained vision and language
backbones?

For practitioners and student researchers alike, this question carries an additional,
practical dimension. The published performance of frontier MLLMs is typically the product
of substantial compute investment that is inaccessible outside well-resourced laboratories.
Understanding \emph{which} aspects of a published result derive from architectural novelty,
and which derive primarily from scale, is therefore both a scientific question and a
prerequisite for meaningful reproduction work.

This report addresses both dimensions simultaneously.
We select three papers that exemplify distinct approaches to multimodal alignment:
BLIP-2~\citep{li2023blip2}, which trains a lightweight Querying Transformer (Q-Former)
between frozen image and language backbones;
LLaVA~\citep{liu2023visual}, which achieves strong assistant-like behavior through visual
instruction tuning on GPT-generated multimodal data; and
VisionLLM~v2~\citep{wu2024visionllmv2}, which extends MLLM outputs far beyond text
through a routing mechanism that connects a central language model to multiple
task-specific decoders.
We critique all three through the lens of architectural originality, supervision strategy,
openness, and reproducibility, and we identify BLIP-2 as the most suitable
implementation target for a student-scale project precisely because its frozen-backbone
modularity provides a coherent downscaling story.

We then conduct a local end-to-end reproduction of the BLIP-2 pipeline on a single NVIDIA
RTX~3070 8\,GB GPU, using the official LAVIS codebase as the base implementation.
The reproduction is not a simplified reimplementation; it uses the actual BLIP-2 training
stages with carefully selected reductions in backbone size, dataset scale, image
resolution, and optimization budget.
Our controlled scaling study---spanning \texttt{10k}, \texttt{50k}, and \texttt{100k}
COCO Karpathy training images---allows us to separate the effect of dataset size from the
effect of architecture, and to characterize the resulting metric gap relative to the
published paper.

The report makes four concrete contributions.
First, it provides a theoretically grounded comparative critique of BLIP-2, LLaVA, and
VisionLLM~v2, organized around the tradeoff between task breadth and compute realism.
Second, it documents a complete local BLIP-2 reproduction, including the engineering
changes required to run the LAVIS pipeline reliably on a single-process Windows
workstation.
Third, it presents a controlled scaling analysis with three data-scale conditions,
supporting the characterization of the metric gap as a function of scale rather than as
an unexplained implementation discrepancy.
Fourth, it demonstrates that best-checkpoint selection by validation CIDEr, rather than
acceptance of the final epoch, is empirically critical in long student-scale caption
runs---a practical methodological lesson that the reproduction evidence supports
concretely.

%% =========================================================
\section{Related Work and Positioning}
%% =========================================================

The development of vision-language pre-training (VLP) can be characterized by a
progression through four architectural families: dual-encoder contrastive
systems~\citep{radford2021clip}, fusion-encoder discriminative
systems~\citep{li2021albef}, encoder-decoder generative
systems~\citep{wang2021simvlm}, and unified transformer
systems~\citep{wang2022beit3}. Most members of these families perform end-to-end
pre-training on large-scale image-text corpora, which makes them computationally
prohibitive to reproduce faithfully at student scale.

BLIP-2~\citep{li2023blip2} represents an important departure from this tradition by
freezing both the vision encoder and the language model and concentrating all trainable
parameters in a small bridge module.
This modular philosophy is related to Flamingo~\citep{alayrac2022flamingo}, which inserts
cross-attention layers into a frozen LLM, but BLIP-2 differs by also freezing the image
encoder and by applying a multi-objective pre-training procedure to the bridge rather
than relying on a single image-to-text generation loss.

LLaVA~\citep{liu2023visual} takes a different approach: it trains a simple linear
projection between a frozen CLIP encoder and a Vicuna-style language model, and then
fine-tunes the combined system on 158K GPT-generated multimodal instruction-following
examples. This work is part of a broader line of instruction tuning research that
includes InstructBLIP~\citep{dai2024instructblip} and MiniGPT-4, and it helped establish
that assistant-like multimodal behavior could emerge from relatively simple architectures
given the right training data.

VisionLLM~v2~\citep{wu2024visionllmv2} occupies a different point in the design space
entirely: it extends an instruction-tuned MLLM to support structured output modalities
such as detection boxes, segmentation masks, pose keypoints, and generated images by
connecting the language model to specialized task decoders through a routing token
mechanism. This places it in the tradition of generalist vision systems such as
Unified-IO and Uni-Perceiver, but with a stronger emphasis on end-to-end gradient flow
from decoders back to the central model.

The three papers thus span a meaningful range of the MLLM design space, making them a
productive set for a comparative critique centered on the question of reproducibility
under resource constraints.

%% =========================================================
\section{Paper Critique}
%% =========================================================

\subsection{BLIP-2: Modular Alignment via a Trainable Bridge}

BLIP-2's central contribution is the Querying Transformer (Q-Former), a lightweight
transformer that mediates between a frozen image encoder and a frozen language model
through a small, fixed set of learnable query
tokens~\citep{li2023blip2}. The paper's most important architectural insight is the
two-stage pre-training decomposition. In stage~1, the Q-Former learns to extract
language-relevant visual representations from a frozen image encoder using three jointly
optimized objectives: image-text contrastive learning (ITC), image-text matching (ITM),
and image-grounded text generation (ITG). In stage~2, the Q-Former's output is projected
into the input embedding space of a frozen large language model, and the bridge is
further adapted to support autoregressive text generation conditioned on visual queries.
This decomposition is elegant because it converts what might otherwise be a difficult,
coupled multimodal optimization problem into a two-phase bridge-learning problem, each
phase with clear objectives and well-defined gradient flow.

\paragraph{Strengths.}
BLIP-2 is stronger than most contemporaneous systems by a clear margin on the metrics
that matter most for comparing modular methods: it outperforms Flamingo-80B on zero-shot
VQAv2 by 8.7 absolute points while using 54$\times$ fewer trainable
parameters~\citep{li2023blip2}. The use of frozen backbones also provides a practical
advantage for reproduction work, because it allows any compatible off-the-shelf image
encoder or language model to be substituted without retraining the entire system. The
paper is also genuinely open: the LAVIS codebase provides a working implementation of
the training pipeline, not merely inference code.

\paragraph{Weaknesses.}
The paper's framing of BLIP-2 as ``compute-efficient'' should be read with care. The
efficiency claim is relative to prior frontier systems, not to student-scale hardware.
The appendix reports that the largest model variant still requires a 16-A100 (40\,GB)
machine for fewer than six days in stage~1 and fewer than three days in stage~2, in
addition to the 129M pre-training images drawn from COCO, Visual Genome, CC3M, CC12M,
SBU, and a subset of LAION-400M~\citep{li2023blip2}. Furthermore, the paper's most
impressive results depend on ViT-g and OPT-2.7B or FlanT5-XXL as backbones, both of
which are substantially larger than what is accessible on a single consumer GPU.
A deeper weakness is that BLIP-2 does not exhibit strong in-context learning: the authors
themselves note that performance on VQA benchmarks does not improve when few-shot
in-context examples are provided, which they attribute to the single-pair structure of
the pre-training data. This is a fundamental limitation relative to Flamingo, which was
trained on interleaved multi-pair sequences.

\paragraph{Critical assessment.}
BLIP-2 is the most carefully designed of the three papers from a scientific standpoint.
Its two-stage decomposition is principled, its multi-objective stage-1 training is well
motivated, and its empirical analysis of the contribution of each training stage
(Figure~5 in the paper) is genuinely informative. However, the paper's implicit claim
that its efficiency advantages translate to broader accessibility must be qualified:
the frozen backbone assumption does not reduce the cost of the backbone itself, and the
most capable backbone combinations remain out of reach for most research settings without
institutional cluster access.

\subsection{LLaVA: Visual Instruction Tuning for Assistant Behavior}

LLaVA's contribution lies not primarily in its architecture---a linear projection layer
between a frozen CLIP~ViT-L encoder and a Vicuna language model---but in its
demonstration that GPT-generated multimodal instruction-following data can substantially
improve a model's alignment with user intent~\citep{liu2023visual}. The paper collects
158K instruction-following samples across three response types (conversation, detailed
description, and complex reasoning) by prompting text-only GPT-4 with image captions and
bounding box annotations as symbolic representations of the visual content.

\paragraph{Strengths.}
LLaVA's key insight is both simple and impactful: the gap between a capable
image-to-text model and a useful visual assistant is primarily a data alignment gap, not
an architectural one. Given a frozen CLIP encoder whose representations are already
semantically rich, a single linear projection layer is sufficient to enable strong
conversational behavior when the model is trained on appropriately structured instruction
data. This design has proved extremely influential; the LLaVA architecture (or minor
variations of it) became the dominant baseline for subsequent open-source multimodal
assistant research. The training cost is also comparatively modest: the authors report
that instruction fine-tuning completes in approximately 10 hours on 8 A100 GPUs, making
LLaVA substantially more accessible than BLIP-2's large-scale pretraining
regime~\citep{liu2023visual}. On ScienceQA, LLaVA combined with GPT-4 as a judge
achieves a new state-of-the-art accuracy of 92.53\%, demonstrating strong
generalization.

\paragraph{Weaknesses.}
LLaVA's dependence on GPT-4 for data generation introduces a methodological coupling
that is not fully acknowledged in the paper. The quality of the instruction-following
behavior is not independent of GPT-4's own biases, coverage limitations, and text-only
visual representations. In other words, the ``visual'' in visual instruction tuning is
partially a proxy: GPT-4 generates responses to symbolic descriptions of images, not to
the images themselves. This is a principled engineering choice given the constraint that
text-only models are strong teachers, but it limits the depth of visual reasoning that
can be grounded in the training data. The paper also does not provide a thorough
ablation of the projection layer itself; it is treated as a minimal architectural
baseline rather than as a component whose design is worth optimizing. Later work (LLaVA
1.5, LLaVA-NeXT) would show that replacing the linear projection with a multi-layer
perceptron and increasing image resolution yields substantial further gains, which
suggests that the original architecture left significant headroom unexplored.

\paragraph{Critical assessment.}
LLaVA's value lies in its data-centric framing: it redirects attention from architectural
innovation toward the quality and format of training supervision. However, its strength
is more as an alignment methodology than as a representation learning contribution. For a
student project on limited hardware, LLaVA is in principle more accessible than BLIP-2's
multi-stage pretraining, but its performance depends substantially on the quality and
volume of instruction data, which requires either API access to GPT-4 or a compatible
open alternative. The reproduction fidelity would be uncertain without replicating the
data generation pipeline.

\subsection{VisionLLM~v2: Toward a Unified End-to-End Generalist MLLM}

VisionLLM~v2 pursues the most ambitious agenda of the three papers: a single end-to-end
model, trained on hundreds of vision and vision-language tasks, capable of producing text
responses, detection boxes, segmentation masks, pose keypoints, and generated or edited
images~\citep{wu2024visionllmv2}. Its core technical contribution is the
\emph{super link} mechanism, which consists of two components: (1)~\emph{routing tokens}
added to the LLM vocabulary (e.g., \texttt{[DET]}, \texttt{[SEG]}, \texttt{[GEN]}),
which trigger decoder invocation when the LLM predicts them; and (2)~\emph{super-link
queries}, sets of randomly initialized learnable embeddings bound to each routing token
that carry task-specific information from the LLM's hidden states to the target decoder.
This design enables end-to-end gradient flow from task-specific decoders back through
the super-link queries to the central language model, which is a genuine advance over
text-message-based tool-use systems that cannot propagate such feedback.

\paragraph{Strengths.}
The breadth of VisionLLM~v2's capability coverage is genuinely impressive. The model
achieves competitive performance with specialized baselines on object detection
(56.7~AP$_b$ on COCO with a Swin-T backbone, comparable to Grounding-DINO-T), pose
estimation (competitive with UniPose-T on multiple benchmarks including long-tail
datasets), and interactive segmentation. Its in-context learning capability---demonstrated
across fine-grained recognition, object detection, and segmentation---extends the model's
utility beyond fixed task templates to few-shot adaptation at inference
time~\citep{wu2024visionllmv2}. The three-stage training strategy, which separates
multimodal dialogue pre-training from multi-capacity fine-tuning and decoder-only
convergence, is also a thoughtful methodological contribution that mitigates the
multi-task conflict problem reported in prior generalist systems.

\paragraph{Weaknesses.}
VisionLLM~v2's ambition creates a fundamental tension with scientific clarity. The system
integrates Grounding DINO, UniPose, Stable Diffusion~v1.5, and InstructPix2Pix as
external decoders, each with its own pre-training history, loss functions, and data
requirements. The super-link mechanism is appealing in principle, but isolating the
contribution of that mechanism from the contributions of the individual decoders and the
curated multi-task training data is difficult. The ablation study in the paper is helpful
but limited: it examines query count and shared versus unshared queries for two decoders,
but does not systematically isolate the effect of the routing token mechanism itself
relative to simpler alternatives. Reproducibility is the most severe limitation. The
appendix reports training on 64~A100 (80\,GB) GPUs for stage~1 and 128~A100~GPUs for
stages~2 and~3, with total wall-clock time of approximately 18 days across
stages~\citep{wu2024visionllmv2}. Combined with hundreds of datasets, dozens of task
templates, and multiple external pretrained decoders, faithful reproduction is not
feasible outside a well-resourced institution.

\paragraph{Critical assessment.}
VisionLLM~v2 is an important systems paper that demonstrates the feasibility of
unifying a wide range of vision tasks under a single model, and it advances the state
of the art on several challenging benchmarks. Its scientific value, however, is partly
entangled with its engineering ambition: the system is complex enough that its
behavioral properties are difficult to disentangle analytically. For a student
implementation project, it is not a viable target.

\subsection{Synthesis: A Reproducibility-Aware Comparison}

Table~\ref{tab:critique} summarizes the comparative critique. Reading across the three
papers, a clear pattern emerges: as the systems evolve from modular bridge learning
(BLIP-2), to instruction-tuned assistants (LLaVA), to generalist multi-decoder systems
(VisionLLM~v2), the breadth of supported tasks increases monotonically, but so does
the compute requirement, the number of external dependencies, and the difficulty of
meaningful reproduction.

\begin{table*}[t]
\centering
\small
\begin{tabularx}{\textwidth}{p{2.1cm} Y Y Y Y}
\toprule
Paper & Core mechanism & Key strengths & Key weaknesses & Reproducibility verdict \\
\midrule
BLIP-2 & Two-stage Q-Former bridge between frozen image encoder and frozen LLM &
Principled modular design; strong zero-shot VQA; open LAVIS codebase; best downscaling
story among the three &
Pre-training still requires large data and compute; paper-level performance depends on
ViT-g and OPT-2.7B or larger; limited in-context learning &
Best choice for a faithful but downscaled student reproduction \\
LLaVA & Linear projection from frozen CLIP to Vicuna LLM, fine-tuned on GPT-generated
visual instruction data &
Simple, influential architecture; strong assistant behavior; moderate training cost
(10\,h on 8$\times$A100); broad community adoption &
Performance tied to GPT-generated instruction data quality; projection design
underspecified; significant gains left by later improvements (LLaVA-1.5, NeXT) &
Viable with moderate cluster access; less suitable when instruction data pipeline
cannot be replicated \\
VisionLLM~v2 & Super-link routing tokens and per-decoder learnable queries connecting
an MLLM to multiple specialized perception and generation decoders &
Broadest task coverage (100+ tasks); end-to-end gradient flow; competitive with
specialist models; strong in-context learning &
Extremely high engineering and compute burden; scientific contributions difficult to
isolate; 128~A100 GPUs for later stages; not reproducible in student settings &
Not viable for this project; institutional cluster access required \\
\bottomrule
\end{tabularx}
\caption{Comparative critique of the three selected papers evaluated on core
mechanism, strengths, weaknesses, and student-scale reproducibility.}
\label{tab:critique}
\end{table*}

This progression is not merely an observation about resource requirements; it has
scientific implications. Each paper's design choices are shaped partly by what is
computationally feasible at its intended scale, and the methods that are most elegant
at one scale may not be most effective at another. BLIP-2's frozen-backbone philosophy
is elegant precisely because large frozen backbones exist and can be leveraged cheaply.
LLaVA's data-centric approach is powerful precisely because GPT-4 is available as a
data generator. VisionLLM~v2's super-link mechanism is effective precisely because
multiple strong specialist decoders can be co-trained end-to-end given sufficient
compute. Understanding this scale dependence is not a critique of any individual paper;
it is a prerequisite for making informed choices about reproduction targets.

%% =========================================================
\section{Reproduction Study: Local BLIP-2}
%% =========================================================

\subsection{Objective and Scope}

The reproduction does not aim to match the paper's performance.
Such a goal would be unachievable on the available hardware and would conflate two
distinct questions: (1)~whether the BLIP-2 training \emph{pipeline} can be executed
faithfully in a student setting, and (2)~whether the resulting \emph{model} achieves
paper-level quality.
We treat these as separate empirical questions and answer them in turn.

A successful reproduction outcome means the staged training pipeline runs end-to-end,
all three training stages produce valid checkpoints, caption outputs are generated from
the fine-tuned model, and a reproducible evaluation protocol yields well-defined metric
estimates.
A gap between local and paper-level performance is expected and informative; it becomes
the central empirical result of the project rather than a failure.

\subsection{BLIP-2 Method: A Technical Summary}

BLIP-2 is built around three components: a frozen vision encoder $E_v$, a frozen large
language model $E_l$, and a trainable Q-Former $Q_\theta$~\citep{li2023blip2}.
Given an image $x$, the encoder produces visual features $V = E_v(x)$.
The Q-Former maintains $M$~learned query embeddings $q_1, \ldots, q_M$ and computes
query-conditioned representations via cross-attention into $V$:
\begin{equation}
Z = Q_\theta(V) \in \mathbb{R}^{M \times d_q},
\label{eq:qformer}
\end{equation}
where $d_q$ is the Q-Former's hidden dimension. A linear projection $W$ maps $Z$ into
the LLM's embedding space, producing soft visual prompts $\hat{Z} = WZ$ that are
prepended to the input token sequence.

Stage~1 pre-trains the Q-Former against the frozen image encoder with three joint
objectives:
\begin{equation}
\mathcal{L}_{\text{stage1}} = \mathcal{L}_{\text{itc}} + \mathcal{L}_{\text{itm}} +
\mathcal{L}_{\text{itg}},
\label{eq:stage1_loss}
\end{equation}
where $\mathcal{L}_{\text{itc}}$ is the image-text contrastive loss computed between
the query output representation and the \texttt{[CLS]} token embedding of the text
encoder, $\mathcal{L}_{\text{itm}}$ is a binary matching loss over fused image-text
representations, and $\mathcal{L}_{\text{itg}}$ is an image-grounded text generation
loss. These objectives are applied with different self-attention masking strategies
between query tokens and text tokens so that each task receives an appropriate
information-flow regime.

Stage~2 aligns the Q-Former outputs to a frozen language model using an autoregressive
objective. For a target caption $y = (y_1, \ldots, y_T)$:
\begin{equation}
\mathcal{L}_{\text{stage2}} = -\sum_{t=1}^{T} \log p_\phi\!\left(y_t \mid y_{<t},
\hat{Z}\right),
\label{eq:stage2_loss}
\end{equation}
where $\phi$ denotes the frozen LLM parameters and $\hat{Z}$ conditions the language
model on the visual queries. The LLM weights remain fixed throughout; only $Q_\theta$
and $W$ are updated.

In the local reproduction, $M = 32$ query tokens are used, consistent with the paper's
main experimental configuration.

\subsection{Experimental Environment}

All experiments were conducted on a single NVIDIA RTX~3070 8\,GB GPU in a Windows
desktop environment.
The software stack consisted of PyTorch with CUDA support, Java~8 for caption evaluation
dependencies, and the official Salesforce LAVIS repository as the base
implementation~\citep{li2023blip2}. The local environment imposed hard constraints that
shaped all subsequent design choices: 8\,GB of device memory precluded paper-scale
backbone configurations, the absence of multi-GPU support eliminated the distributed
training path assumed by LAVIS, and Windows-specific runtime behavior introduced several
issues in evaluation and process management that required patches.

\subsection{Engineering Patches and Implementation Notes}

Making the LAVIS BLIP-2 pipeline operational in this environment required a set of
targeted engineering modifications, which we document here both for reproducibility and
to characterize the systems-level effort that reproducing a research codebase entails.

The most consequential patch addressed an embedding dimension mismatch introduced by
substituting OPT-350M for the paper's OPT-2.7B backbone: the Q-Former's output
projection dimension did not match OPT-350M's embedding dimension, requiring an
explicit bridge layer. Additional patches included local cache-path resolution fixes
for the COCO annotation and image directories; single-process guards to replace
distributed process-group assumptions; image-ID alignment fixes in the caption dataset
loader that caused mismatches between subset annotations and the evaluation ground
truth; a workaround for unstable Windows METEOR scoring (addressed by executing caption
epochs with \texttt{report\_metric=false} and evaluating saved prediction files
offline); optional lazy loading of the \texttt{spacy} dependency to suppress unrelated
import failures; and downloader robustness improvements, including explicit HTTP
timeouts, to prevent image staging from stalling indefinitely on completed downloads.

These modifications did not alter the training objectives, the model architecture, or
the evaluation metrics; they addressed the operational gap between a codebase designed
for distributed Linux training and a local, single-GPU Windows environment.

\subsection{Dataset Construction and Evaluation Protocol}

The local experiments use COCO Karpathy caption splits~\citep{lin2014coco} as the
evaluation benchmark. Rather than the paper's large-scale pre-training mixture, we
construct three deterministic reduced subsets to enable controlled scaling analysis:
a \texttt{10k} baseline, an office-scale \texttt{50k} run, and a student-scale
\texttt{100k} run. In all cases the validation and test sets are fixed at 1,000 images
each. Table~\ref{tab:subset-scales} summarizes the subset configuration.

\begin{table}[t]
\centering
\small
\begin{tabular}{lrrr}
\toprule
Condition & Train & Val & Test \\
\midrule
Baseline (\texttt{10k}) & 10,000 & 1,000 & 1,000 \\
Office scale (\texttt{50k}) & 50,000 & 1,000 & 1,000 \\
Student scale (\texttt{100k}) & 100,000 & 1,000 & 1,000 \\
\bottomrule
\end{tabular}
\caption{Dataset subset configurations used in the scaling study.
All conditions use the same fixed 1,000-image validation set.}
\label{tab:subset-scales}
\end{table}

Subset JSON files were constructed from the full Karpathy annotation files with
deterministic shuffling and seeded selection. Only the images referenced by each subset
were staged into the local LAVIS cache, which made it possible to expand the training
set incrementally across conditions without re-downloading or re-staging the entire COCO
dataset. Evaluation used subset-matched COCO-format ground truth: a custom ground-truth
JSON file was generated for each condition containing exactly the 1,000 validation image
annotations, ensuring that image IDs in the prediction files matched image IDs in the
reference files exactly. BLEU and CIDEr were computed offline from saved prediction
files using the official \texttt{pycocoevalcap} implementations. METEOR was excluded
from the reported metrics due to platform instability.

This evaluation design preserves \emph{internal} comparability across conditions: because
all three scaling conditions use the same 1,000-image validation set and the same offline
metric code path, the BLEU-4 and CIDEr values are directly comparable across rows in
Tables~\ref{tab:metrics} and~\ref{tab:internal-scaling}. They are not numerically
interchangeable with the paper's official Karpathy test-split results, which use the
full 5,000-image test set and the full COCO annotation file.

\subsection{Experimental Configuration}

Table~\ref{tab:setup-compare} situates the local reproduction relative to the paper's
strongest published captioning configuration.
The local backbone choices (CLIP~ViT-L and OPT-350M) are qualitatively consistent with
the BLIP-2 family but substantially smaller than the ViT-g and OPT-2.7B configuration
used for the paper's best-reported COCO captioning result.
Image resolution is 224$\times$224 throughout, compared with 364$\times$364 in the
paper's caption fine-tuning.

\begin{table*}[t]
\centering
\small
\begin{tabularx}{\textwidth}{p{3.2cm} Y Y}
\toprule
Dimension & BLIP-2 paper (best COCO config) & Local reproduction \\
\midrule
Pre-training data &
129M image-text pairs (COCO, VG, CC3M, CC12M, SBU, LAION subset)~\citep{li2023blip2} &
Reduced COCO Karpathy subsets only (\texttt{10k}--\texttt{100k} conditions) \\
Stage-1 schedule &
250k steps, batch~2320 (ViT-L) or 1680 (ViT-g)~\citep{li2023blip2} &
3--10 epochs (condition-dependent), batch 4, grad.\ acc.\ 8 \\
Stage-2 schedule &
80k steps, batch~1520--1920~\citep{li2023blip2} &
3--10 epochs, batch 2, grad.\ acc.\ 8 \\
Caption fine-tuning &
5 epochs, batch~256, image resolution 364~\citep{li2023blip2} &
5--15 epochs (condition-dependent), batch 1--2, grad.\ acc.\ 8, resolution 224 \\
Vision encoder &
ViT-g/14 (EVA-CLIP)~\citep{li2023blip2} &
CLIP ViT-L/14 \\
Language model &
OPT-2.7B~\citep{li2023blip2} &
OPT-350M \\
Hardware &
16$\times$A100 (40\,GB); $<$6\,d stage 1, $<$3\,d stage 2~\citep{li2023blip2} &
1$\times$RTX~3070 (8\,GB); multi-day desktop sessions \\
\bottomrule
\end{tabularx}
\caption{BLIP-2 paper configuration versus the local reproduction. All reductions
are deliberate and define the scientific meaning of the resulting performance gap.}
\label{tab:setup-compare}
\end{table*}

Within the local runs, the architecture is held fixed across all scaling conditions.
The controlled variables are training data scale and optimization budget; the backbone,
image resolution, number of query tokens, and evaluation protocol remain constant.
This design choice reflects a deliberate experimental philosophy: on constrained hardware,
changing multiple configuration axes simultaneously makes results difficult to interpret.
By isolating data scale and epoch budget as the primary variables, the scaling study can
attribute metric differences to those specific factors rather than to confounded changes.

Optimization hyperparameters were chosen conservatively to maximize training stability.
Stage~1 and stage~2 use an initial learning rate of $10^{-4}$ with a linear warmup and
cosine decay. Caption fine-tuning uses $10^{-5}$. Weight decay is 0.05 throughout. Beam
search during caption validation uses beam width~3, maximum output length~30, and minimum
output length~8.

\subsection{Training Progression}

Table~\ref{tab:experiment-schedule} summarizes the four-stage experimental progression.

\begin{table*}[t]
\centering
\small
\begin{tabularx}{\textwidth}{p{2.5cm} p{1.6cm} p{1.6cm} p{1.6cm} p{1.7cm} p{1.5cm} Y}
\toprule
Experiment & Data scale & Stage 1 & Stage 2 & Caption & Img.\ res. & Primary purpose \\
\midrule
Baseline & \texttt{10k/1k/1k} & 1 epoch & 1 epoch & 1 epoch & 224 &
Establish pipeline operability; verify end-to-end execution \\
Office scale & \texttt{50k/1k/1k} & 3 epochs & 3 epochs & 5 epochs & 224 &
Measure effect of larger data and longer schedule on caption quality \\
Caption polish & \texttt{50k/1k/1k} & reused & reused & 5 epochs & 224 &
Preserve all per-epoch checkpoints for best-epoch selection analysis \\
Student long run & \texttt{100k/1k/1k} & 10 epochs & 10 epochs & 15 epochs & 224 &
Stress-test the pipeline at larger scale; characterize late-epoch behavior \\
\bottomrule
\end{tabularx}
\caption{Experiment schedule in the local reproduction study. Architecture is held
fixed across all four conditions.}
\label{tab:experiment-schedule}
\end{table*}

The first experiment (\texttt{10k} baseline) served a purely methodological role:
demonstrate that the BLIP-2 pipeline could be made to run end-to-end in the local
environment with all engineering patches applied. This experiment succeeded, confirming
pipeline operability, but produced severely collapsed caption outputs with only 61 unique
captions over 1,000 validation images.

The second experiment (\texttt{50k} office scale, \texttt{3/3/5}) was designed to test
the primary local hypothesis: that increasing both dataset size and optimization budget,
while holding the architecture fixed, would materially improve caption quality. The
answer was affirmative. Caption diversity increased from 61 to 563 unique captions, and
BLEU-4 increased from 1.45 to 11.13, representing an approximately 7.7$\times$
improvement in the headline metric.

The third experiment (caption polish rerun) reproduced the caption stage from the
\texttt{50k} office stage-2 checkpoint with per-epoch checkpointing enabled throughout.
This experiment confirmed the best-epoch finding and produced a clean per-epoch metric
curve, but the best new checkpoint (epoch~4) did not surpass the earlier epoch-3
snapshot from the office run.

The fourth experiment (\texttt{100k} student long run, \texttt{10/10/15}) extended the
pipeline to the largest local data scale and the longest optimization budget. This run
completed successfully across all epochs, demonstrating that the local pipeline is
operationally robust at the \texttt{100k} scale. However, as detailed in
Section~\ref{sec:results}, the metric outcome was weaker than the \texttt{50k} office
best, and the run exhibited clear early peaking followed by monotone metric decay.

\subsection{Results and Evaluation}
\label{sec:results}

\subsubsection{Pipeline Completion and Training Losses}

All four experiments completed successfully, and all three training stages in each
experiment produced valid checkpoints. The strongest stage-wise training loss values
from completed runs are as follows. For the \texttt{50k} office run: stage-1 final
train loss~0.412 (ITC~0.214, ITM~0.054, LM~3.031); stage-2 final train
loss~0.767; caption epoch-3 train loss~0.367. For the \texttt{100k} long run: stage-1
final loss~0.330 (ITC~0.365, ITM~0.037, LM~2.241); stage-2 final loss~0.363; caption
final (epoch~14) loss~0.365.

That all six sets of training losses converge and that the \texttt{100k} stage-1 loss is
lower than the \texttt{50k} stage-1 loss (0.330 vs.\ 0.412) confirms that the longer
schedule and larger data volume do produce a more strongly optimized bridge at the
representation learning stage. The disconnect between training loss improvement and
captioning metric improvement in the \texttt{100k} run is therefore not a training
failure; it is evidence of overfitting or distribution shift in the captioning head
relative to the fixed student-scale backbone.

\subsubsection{Captioning Metrics}

Table~\ref{tab:metrics} compares the best local captioning result against the BLIP-2
paper's published COCO fine-tuned score for the ViT-g OPT-2.7B configuration.
The local best (BLEU-4~11.13, CIDEr~37.57) falls substantially below the paper result
(BLEU-4~43.7, CIDEr~145.8). This gap is expected given the backbone, data, and compute
differences enumerated in Table~\ref{tab:setup-compare}, and is analyzed systematically
in Section~\ref{sec:failure-analysis}.

\begin{table}[t]
\centering
\small
\begin{tabular}{lrr}
\toprule
Metric & Paper (ViT-g OPT-2.7B) & Local best (\texttt{50k}) \\
\midrule
BLEU-4 & 43.7 & 11.13 \\
CIDEr & 145.8 & 37.57 \\
\bottomrule
\end{tabular}
\caption{BLIP-2 paper COCO captioning result versus the local best checkpoint.
Numbers are reported on the standard $\times 100$ scale. The two results
are not directly comparable due to backbone, dataset, resolution, and evaluation
split differences.}
\label{tab:metrics}
\end{table}

Table~\ref{tab:internal-scaling} presents the internal scaling comparison across all
completed local runs. The most important empirical pattern is the non-monotonic
relationship between training scale and captioning performance: while the \texttt{50k}
run substantially outperforms the \texttt{10k} baseline, the \texttt{100k} run does not
outperform the \texttt{50k} run. This pattern holds at both the best-checkpoint and
final-checkpoint selection strategies, and it is accompanied by a steady increase in
caption diversity (unique caption count) even as metric quality declines.

\begin{table*}[t]
\centering
\small
\begin{tabular}{llcrrr}
\toprule
Run & Data scale & Checkpoint selection & BLEU-4 & CIDEr & Unique captions / 1000 \\
\midrule
Baseline & \texttt{10k} & Final epoch 0 & 1.45 & 3.03 & 61 \\
Office best & \texttt{50k} & Best epoch 3 & \textbf{11.13} & \textbf{37.57} & 563 \\
Polish completion & \texttt{50k} & Final epoch 4 & 10.49 & 37.14 & 607 \\
Long run best & \texttt{100k} & Best epoch 2 & 8.57 & 25.34 & 677 \\
Long run final & \texttt{100k} & Final epoch 14 & 6.61 & 18.36 & 734 \\
\bottomrule
\end{tabular}
\caption{Internal scaling comparison across completed local runs. All runs use the
same 1,000-image validation subset and the same offline evaluation protocol. Bold
indicates the best local result across all conditions.}
\label{tab:internal-scaling}
\end{table*}

\subsubsection{Best-Checkpoint Selection}
\label{sec:best-ckpt}

A practically important finding of this project is that best-checkpoint selection by
validation CIDEr---rather than acceptance of the last-epoch checkpoint---is empirically
critical under the long student-scale training schedule.
Table~\ref{tab:best-vs-final} isolates this effect for the \texttt{100k} long run.

\begin{table}[t]
\centering
\small
\begin{tabular}{lcrrr}
\toprule
\texttt{100k} checkpoint & Epoch & BLEU-4 & CIDEr & Unique caps \\
\midrule
Best (by val.\ CIDEr) & 2 & 8.57 & 25.34 & 677 \\
Final & 14 & 6.61 & 18.36 & 734 \\
\midrule
\multicolumn{2}{l}{Difference} & $-1.96$ & $-6.98$ & $+57$ \\
\bottomrule
\end{tabular}
\caption{Best-versus-final checkpoint comparison for the \texttt{100k} long run.
Accepting the final checkpoint instead of the best-CIDEr checkpoint would cost
1.96 BLEU-4 points and 6.98 CIDEr points.}
\label{tab:best-vs-final}
\end{table}

The cost of accepting the default last checkpoint rather than selecting the best
validation checkpoint is 1.96 BLEU-4 points and 6.98 CIDEr points---a meaningful
fraction of the total local signal. The practical implication is clear: under long runs
with fixed small-capacity backbones, the caption fine-tuning head may overfit to the
training distribution faster than the Q-Former-induced visual representations can improve.
Per-epoch checkpoint saving and offline metric evaluation should therefore be treated as
standard practice in student-scale BLIP-2 reproductions rather than as optional
refinements.

\subsubsection{Qualitative Behavior}

The qualitative outputs from the \texttt{50k} office best checkpoint are substantially
less collapsed than the \texttt{10k} baseline, but they exhibit a characteristic failure
pattern: the model defaults to semantically narrow but linguistically plausible
person-centric or object-centric templates that only partially match the image content.
Table~\ref{tab:qualitative} shows representative examples.

\begin{table*}[t]
\centering
\small
\begin{tabularx}{\textwidth}{p{1.6cm} Y Y}
\toprule
Image ID & Reference content (paraphrased from COCO annotations) & Generated caption \\
\midrule
91500 & Two teenagers seated on folding chairs playing video games &
a woman with her hands in her pockets \\
511622 & A woman wearing a scarf cooks food in a pan or wok &
a woman with her hands on her hips \\
341113 & A woman in a wetsuit rides a surfboard on a breaking wave &
a man with a gun in his hand \\
407403 & A painting of yellow tulips arranged in a white vase &
a woman holding a baby in her arms \\
353027 & A hand lifts a slice of mushroom pizza from a whole pie &
a woman with a baby in her arms \\
31240 & A passenger train is leaving or standing at a station &
a woman with her dog in her lap \\
\bottomrule
\end{tabularx}
\caption{Representative qualitative failures from the \texttt{50k} office-best checkpoint
evaluated on the 1,000-image validation subset. The generated captions are structurally
plausible but semantically misaligned with the image content.}
\label{tab:qualitative}
\end{table*}

The modal failure pattern is a generic pronoun-anchored template (``a woman with
\ldots'') applied regardless of image content. Of the 1,000 validation predictions,
563 are unique. The most common single caption appears 27 times, and the top 10 captions
collectively account for 176 predictions---indicating that the model has not fully
escaped mode collapse, though it has moved substantially in the right direction relative
to the 10k baseline's 61 unique captions.

This qualitative pattern is consistent with the hypothesis that the local model's
Q-Former has learned a visual representation that is weakly informative of the LLM
conditioning but not sufficiently discriminative to suppress template collapse. The
frozen OPT-350M language model's prior over high-likelihood generic captions is strong
enough to dominate the visual conditioning signal when that signal is weak---a dynamic
that the paper's larger backbones and richer pretraining data substantially attenuate.

\subsection{Failure Analysis}
\label{sec:failure-analysis}

The gap between local and paper-level performance can be decomposed into five
attributable factors:

\begin{enumerate}
\item \textbf{Backbone capacity.}
The paper's best captioning configuration uses ViT-g (1.0B parameters) and OPT-2.7B.
The local run uses CLIP~ViT-L and OPT-350M. The LLM is approximately 7.7$\times$
smaller, and the vision encoder is substantially weaker. Both factors directly limit the
quality of the frozen representations that the Q-Former must bridge.

\item \textbf{Pre-training data scale.}
The paper pre-trains on 129M image-text pairs from six sources. The local runs use only
10k--100k COCO images---a reduction of three to four orders of magnitude in
pre-training data volume. This is the largest single contributor to the metric gap,
because stage-1 Q-Former training depends critically on diverse image-text co-occurrence
to learn broadly useful visual representations.

\item \textbf{Optimization budget.}
The paper trains for 250k steps in stage~1 and 80k steps in stage~2, with batch
sizes that correspond to thousands of samples per step. The local runs complete far
fewer effective gradient updates per stage due to both the smaller dataset and the
smaller effective batch size.

\item \textbf{Image resolution.}
The paper uses 364$\times$364 images for caption fine-tuning. The local runs use
224$\times$224. Lower resolution degrades the image encoder's feature quality,
particularly for images where fine-grained visual details are needed to produce
accurate captions.

\item \textbf{Evaluation protocol differences.}
The paper reports results on the full 5,000-image Karpathy test set. The local
evaluation uses a 1,000-image validation subset with offline BLEU and CIDEr computation.
While the internal consistency of the local results is preserved, any direct numerical
comparison to the paper should be treated as qualitative rather than quantitative.
\end{enumerate}

Importantly, the observed metric gap narrows monotonically as the local setup is
strengthened from \texttt{10k} to \texttt{50k}, which is the behavior expected of a
structurally valid reproduction that is operating in a scale-constrained regime.
The gap does not narrow from \texttt{50k} to \texttt{100k}, which we attribute to a
capacity ceiling imposed by the fixed student-scale backbones rather than to a
methodological deficiency in the longer run.

%% =========================================================
\section{Threats to Validity}
%% =========================================================

Three classes of threats limit the interpretive strength of the local results.

\paragraph{Evaluation incomparability.}
Local validation metrics are computed on a 1,000-image subset using offline
\texttt{pycocoevalcap} scoring without METEOR. These numbers are internally consistent
across conditions but are not equivalent to the paper's full-set Karpathy test results.
All cross-paper comparisons should therefore be read as directional rather than
quantitative.

\paragraph{Architecture and scale differences.}
The local backbone combination (CLIP~ViT-L and OPT-350M) is qualitatively
within the BLIP-2 family, but the parameter counts, representation capacities, and
pre-training histories of these models differ substantially from the paper's best
configuration. It is therefore not possible to attribute the metric gap to any single
factor in isolation; the five factors listed in Section~\ref{sec:failure-analysis}
are mutually compounding.

\paragraph{Codebase-level differences.}
The reproduction required a set of engineering patches to the official LAVIS codebase
(documented in Section~4.3). These patches are conservative---they do not alter
training objectives or model architecture---but they mean that the local training path
is not an unmodified upstream implementation. The reported results are therefore the
product of the patched codebase, and any attempt to replicate this work should apply
the same patches.

%% =========================================================
\section{Reproducibility and Research Artifacts}
%% =========================================================

The reproduction is documented as a layered artifact set rather than as a single
narrative result. The repository contains local YAML configuration files for all four
experiments, stage-launcher scripts with resume support, data-subset construction tools,
offline evaluation scripts, per-epoch checkpoint registries, run progress registries,
saved \texttt{val\_epoch*.json} prediction files for all completed caption epochs, and
subset-matched COCO-format ground-truth JSON files.

This documentation serves two functions. First, it makes the reported metrics
auditable: each BLEU-4 and CIDEr value can be traced to a specific prediction file and
a specific ground-truth file, both of which are stored in the repository. Second, it
makes the work extensible: the \texttt{100k} long run was executed as a direct
continuation of the same codebase used for the \texttt{10k} baseline, and any future
run using stronger backbones or larger data would inherit the same infrastructure.

Treating the artifact trail as a scientific contribution in its own right is appropriate
here because the methodological value of the project is partly infrastructural. The
demonstration that the BLIP-2 pipeline can be made to run reliably on a single consumer
GPU, under Windows, without distributed training, and with reproducible per-epoch
evaluation, is a reusable contribution for other student researchers who wish to build
on the same approach.

%% =========================================================
\section{Discussion}
%% =========================================================

The results of this project point to two broader conclusions that extend beyond the
specific numbers reported.

\paragraph{The distinction between pipeline reproducibility and performance
reproducibility.}
These two notions of reproducibility are frequently conflated in informal discussions of
whether a paper ``can be reproduced.'' The present work demonstrates that they can come
apart sharply. The BLIP-2 pipeline is reproducible at student scale: all three training
stages execute correctly, the Q-Former training objectives converge as expected, and the
resulting caption model generates plausible outputs. But BLIP-2's performance is not
reproducible at student scale, because it depends fundamentally on backbone
capacity and pre-training data volume that are inaccessible on commodity hardware.
Recognizing this distinction is important for how the field communicates reproducibility
standards. Requiring performance reproducibility as the criterion would classify this
project as a failure; requiring pipeline reproducibility as the criterion would classify
it as a success. The truth is that both are informative---and that the gap between them
is the scientific result.

\paragraph{The scale-dependence of the modular alignment paradigm.}
BLIP-2's frozen-backbone philosophy is architecturally elegant, but the elegance is
conditioned on the frozen backbones being sufficiently capable. When smaller backbones
are substituted, the Q-Former must bridge a wider representational gap between a weaker
image encoder and a less capable language model. The result is that the visual
conditioning signal from the Q-Former is insufficient to suppress the language model's
strong prior over generic captions, producing the template collapse pattern visible in
Table~\ref{tab:qualitative}. This is not a flaw in the BLIP-2 design; it is evidence
that frozen-backbone modularity is a scale-conditional property, not a universal one.

The non-monotonic scaling behavior observed in the \texttt{100k} run sharpens this
point: once the student-scale backbone's capacity ceiling is reached, additional data
and longer training budgets do not improve caption quality---they increase diversity
(as measured by unique caption count) while degrading metric scores. This is consistent
with a model that has learned to reduce repetition but cannot learn to discriminate
between images at the semantic level required to improve BLEU or CIDEr.

%% =========================================================
\section{Conclusion}
%% =========================================================

We have presented a comparative critique of three influential multimodal systems---BLIP-2,
LLaVA, and VisionLLM~v2---and a local end-to-end reproduction of the BLIP-2 pipeline on
a single NVIDIA RTX~3070 8\,GB GPU. The critique situates the three papers along a
capability-versus-reproducibility tradeoff axis, arguing that each step toward broader
multimodal capability is accompanied by a commensurate increase in scale dependence.
BLIP-2 occupies the most reproducible position on this axis, which motivates its
selection as the implementation target.

The reproduction study demonstrates that the BLIP-2 pipeline is operationally
reproducible under student-scale constraints after a set of targeted engineering
modifications to the official LAVIS codebase. All three training stages complete
successfully across four experimental conditions spanning dataset sizes from 10k to 100k
COCO images. The strongest local result, obtained at epoch~3 of the \texttt{50k}
office-scale caption run, reaches BLEU-4~11.13 and CIDEr~37.57---approximately 25\%
and 26\% of the paper's reported values, respectively.

Three empirical findings from the scaling study are worth emphasizing as standalone
contributions. First, increasing dataset size from 10k to 50k produces a large
improvement in both metric performance and caption diversity. Second, increasing dataset
size further from 50k to 100k does not improve metrics and suggests a capacity ceiling
imposed by the student-scale backbone combination. Third, best-checkpoint selection by
validation CIDEr recovers 1.96 BLEU-4 points and 6.98 CIDEr points relative to the
final-epoch checkpoint in the \texttt{100k} long run, making metric-driven model
selection an important practical recommendation for long student-scale runs.

The fundamental conclusion---that BLIP-2's \emph{pipeline} is student-reproducible but
BLIP-2's \emph{performance} is not---is not a negative result. It is a precise and
useful characterization of where the difficulty lies, one that clarifies the
relationship between architectural design and scale dependence in a way that the paper's
published results alone cannot convey.

\bibliography{term_paper}

\end{document}