Add one focused ablation table for the 100k failure question.
Include rows like:
50k with longer schedule
100k with shorter schedule
100k with lower stage-2 LR
100k with early-stop by CIDEr
This directly answers “data scale vs optimization mismatch.”
Add two small figures:
CIDEr and BLEU-4 vs caption epoch for 50k and 100k.
Stage-1 and stage-2 train loss trajectories.
Even simple line charts would make the degradation argument much stronger.
Add a reproducibility appendix subsection:
Exact command used for each reported metric file.
Path normalization note for moving artifacts across machines.
One “minimum rerun recipe” for a reviewer.
Strengthen threats-to-validity with explicit severity labels:
Split mismatch: high
Validation-based model selection: medium
Windows metric-path fragility: medium
Single-seed estimates: high
Tighten claims in abstract and conclusion:
Keep the central thesis.
Replace hard causal language with evidence-calibrated wording where ablations are missing.