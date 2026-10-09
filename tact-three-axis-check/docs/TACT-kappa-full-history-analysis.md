# TACT Three-Axis Coordinate Taxonomy · Full History and Analysis of the Kappa Test

> Binding: coordinate_data.json v2.7.8 (117 coordinates) · calibration_cases.json v1.1.1 (21 cases)
> Test object: inter-model agreement κ across the L/M/P three axes (Fleiss κ, multiple annotators)
> Data convention: every value is given as a "with-empty-code / non-empty-code" pair (with-empty = counting the empty code as one category; non-empty-code = counting only κ among the non-empty-code categories); hit rate = the proportion agreeing with golden
> This document will be merged into the kappa-test section of the toolkit; the current test **uses only different LLMs as annotators, with no human-annotator testing; human annotation will be added later**.

---

## Part 0: Test Methodology Overview

| Item | Description |
|---|---|
| Annotators | 5 independent domestic LLMs: **Doubao / Yuanbao / DeepSeek / MiniMax M3 / iFlytek Spark** |
| Early comparison | Once used cocodot to relay overseas models (Claude Haiku, etc.) for a domestic-vs-overseas comparison, then dropped it when the quota ran out; the overseas comparison was unsustainable, so the annotation mainline converged on domestic models |
| Removed annotators | Kimi (dropped this round); workbuddy (a per-case replica of Kimi/iFlytek/MiniMax, confirming it reuses domestic-model backends underneath and is not independent) |
| Test cases | 12 synthetic judgment cases (C1–C12), whose phenomena correspond to the core split branches among the 21 calibration-set cases |
| Metrics | Fleiss κ (multi-annotator agreement) + hit rate (compared against golden) |
| Mechanism | Each round: give blind-annotation prompts → 5 independent annotations → compute κ/hit → cluster the disagreement points → locate the criterion cracks → fix criteria / fix golden → re-test in the next round |

**Validation discipline**: κ and the hit rate are **diagnostic signals**, not pass/fail. When modifying criteria, adhere to "first set the proposal → red-team attack → compromise and finalize → independent verification confirms a real improvement → only then land into the package"; throughout, the coordinate semantics in coordinate_data.json are not changed (only the SKILL.md criterion guidance and the calibration golden are changed).

---

## Part 1: Development History Summary Table (the whole journey at a glance)

| Round/Version | What changed this round | Rationale (why adjusted this way) | L κ (with-empty/non-empty) | L hit | M κ (with-empty/non-empty) | P κ (with-empty/non-empty) |
|---|---|---|---|---|---|---|
| R1 Round 1 | None (coarse prompt, parent coordinate + child coordinates) | Baseline: rough coordinate definitions, no sharp criterion | 0.555 / — | — | 0.758 / — | 0.658 / — |
| R2 Round 2 | **Fixed the P axis**: made the three-gate criteria explicit | P improvement comes from criterion explicitness, not objectivity (annotated conclusion) | 0.623 / — | — | 0.786 / — | **0.946 / —** |
| R3 Child-coordinate level | **Prompt refined to child coordinates** | Give all child codes to see whether agreement rises | 0.637 / — | — | **0.907 / —** | 0.717 / — |
| R4 Round 5 | — | After child-coordinate refinement, the fluctuations converged | 0.647–0.697 | — | 0.750–0.867 | 0.805–0.867 |
| v6 | **Fixed the M axis**: M5/M7/M8 hard-split + population-difference anchors | M mechanism-layer terminology + clear split criteria | 0.654 / 0.598 | 50.9% | **1.000 / 1.000** | 0.898 / 0.851 |
| v7 | **Changed L golden** (changed C1/C2/C8/C3/C7) | Try fixing golden to rescue L | 0.598 (κ unchanged) | 50.9→83.6% | 1.000 / 1.000 | 0.898 / 0.851 |
| v8 | **First version of the L sharp criterion** (sharp trio + insufficient-information discipline) | L's shortboard is criterion-boundary clarity, not golden | 0.664 / 0.608 | 81.8% | 1.000 / 1.000 | 0.887 / 0.834 |
| **v9** | **Sharp criterion + reverse constraint + 4 L anchors** | Added the "single-round spontaneous" reverse constraint to prevent over-exclusion | **0.953 / 0.945** | **98.2%** | 0.927 / 0.861 | 0.896 / 0.845 |
| v1.1.1 landed | Source-determination general rule + autonomous-privilege anti-overfitting anchor + C5 M anchor + full L-golden alignment (CAL-01/02/03/10/14) | κ has reached a plateau; switch to anti-overfitting landing | — | — | — | — |

**One-sentence throughline**: coarse prompt (all three axes low) → criterion explicitness (P meets target) → child-coordinate refinement (M rises) → M criterion patch (M full marks, exposing L as the only shortboard) → tried fixing golden to rescue L (failed, puncturing the truth that "L's problem lies in the criterion boundary, not golden") → sharp criterion (L hit 50.9→81.8, but Yuanbao outlier) → reverse constraint + anchors (L converges to 98.2%, surpassing MAST 0.88) → three-point anti-overfitting landing.

---

## Part 2: Round-by-Round Details (self-contained per round)

### R1 · Round 1 (baseline, coarse prompt)

**Prompt**: coarse-grained. Directly gave the L/M/P three-axis parent-coordinate + child-coordinate definitions, with no sharp criterion, no reverse constraint, and no operationalized anchors. Models landed a coordinate by superficial "term match".

**Results**: L 0.555 / M 0.758 / P 0.658.

**Analysis**: All three axes sit near or below the passing line. The root cause is that the coordinate definitions are "descriptive" rather than "operational" — models land coordinates by surface term matching, and each model drifts widely on the landing-layer judgment for the same case. M is slightly above L/P because the mechanism layer (where the problem lies) is relatively structurally defined.

**What to fix this round**: the P axis is the weakest and the easiest to operationalize, so fix P first.

---

### R2 · Round 2 (fix the P axis: make the three-gate criteria explicit)

**Prompt**: building on R1, made the P axis's "three gate questions" criteria explicit (which facet's consistency is broken, gate-by-gate counter-check, stop on superficial term match), and added operationalized splitting for easily-confused P codes (P1 Factual Distortion vs P4 Consistency Breakdown, etc.).

**Results**: L 0.623 / M 0.786 / **P 0.946**.

**Analysis**: P rose sharply (0.658→0.946), M rose slightly, L still low. Key conclusion: **P's gain came from "criterion explicitness", not "criterion objectivity"** — give operationalized criteria and the models become consistent; without them, the models drift on superficial term match. This established the methodology for all subsequent rounds: **the lever for raising agreement is criterion clarity, not changing golden, not swapping in better coordinate definitions.**

---

### R3 · Round 3 (prompt refined to child-coordinate level)

**Prompt**: upgraded the prompt from "parent + child coordinates" to **child-coordinate-level granularity** — giving, at the exact granularity of information the toolkit can actually extract at runtime, each child coordinate's manifestation / positioning / verification path verbatim, simulating the information supply the toolkit provides in real runs.

**Results**: M 0.907 / P 0.717 / L 0.637.

**Analysis**: M surged to 0.907 (mechanism-layer terminology advantage + refined description), but P fell back (0.946→0.717), L still lingered low. The reason for P's drop: after giving all child codes, **multi-select ambiguity increased** — models dual-list codes for "which facet is broken". This shows: **the finer the information, the higher agreement is not guaranteed; giving all child codes instead amplified the "multi-select boundary" disagreement.**

---

### R4 · Round 5

**Results**: L 0.647–0.697 / M 0.750–0.867 / P 0.805–0.867 (range values, multiple samples).

**Analysis**: the values fluctuated and converged on top of R3, but the overall picture was unchanged — M stable, P middle, L the shortboard. By now it was clear: **the L axis is the only systematic shortboard, and it is not a matter of prompt length or model capability, but of the criterion boundary itself not being clear enough.**

---

### v6 · M criterion patch (M full marks)

**What changed**: added hard-split criteria to the M axis — the dimensional distinction among M5 vs M7 vs M8 (single-entity deviation / rule-system mismatch / multi-component emergence), and added "population-difference" reverse anchors (constraint-execution layer → M5-9 Constraint-Goal Inversion; decision-outcome layer → M2-5 Algorithmic Discrimination).

**Rationale**: the M axis's 9 families mix three dimensions (form M1-M5, source M6/M9, system M8, rule system M7); without veto-level criteria between adjacent easily-confused families, models stop at the earlier layer on superficial match. Adding split criteria turns "is it essentially this layer" into a decidable operational question.

**Results (5 models)**: M with-empty/non-empty = **1.000 / 1.000**, hit 100% (all five converged on M5-9 for C5); P 0.898 / 0.851; L 0.654 / 0.598, **hit only 50.9%**.

**Analysis**: M full marks proves **mechanism-layer criterion clarity works** (the M-axis definitions are terminology-oriented with a clear process division, so stable criteria can be derived theoretically — its natural advantage). P is good. But **L is the only hard shortboard (hit 50.9%)** — the L axis's 4 layers drift badly across models.

---

### v7 · L golden revision (trial and error, puncturing the truth)

**What changed**: only changed the L-axis golden (moved C3/C7→L1, C1/C2/C8→L3, kept C6/C12 at L2), **reused v6's 5-model outputs, only swapped the golden and recomputed**.

**Rationale**: at the time we suspected L was poor because the golden was mis-specified, and wanted to rescue the hit rate by correcting the "standard answer".

**Results**: L hit rate 50.9% → 83.6%, but **κ did not budge: 0.598**.

**Analysis (key turning point)**: hit rate up, κ unchanged — **this punctured a truth: L's shortboard is not at all that the golden is mis-specified, but that criterion-boundary clarity is insufficient**. For the same case, each model judges a different layer (e.g., C6 is 3 models L2 + 2 models L1, C7 is 3 models L1 + 2 models L3, C12 is 3 models L2 + 2 models L1); it is not that "the standard answer is wrong", but that "the models do not know which criterion to use". Changing golden chases the result, not the root cause. **This established the subsequent direction: L must be fixed at the criterion layer; fixing it at the golden layer is ineffective.**

---

### v8 · First version of the L sharp criterion

**What changed**: added the "sharp-criterion trio" to the L axis — ① strip away every external factor; would the model still make the error in a single standalone generation (judge L1); ② does the error occur at the boundary-crossing convention mismatch between in and out (judge L2); ③ does the decision require reading cross-round / external information (judge L3). Also added the "insufficient-information discipline" — if you cannot point it out, do not force it in.

**Rationale**: the sharp criterion turns "which layer" from a "term description" into a "counterfactual test" (would it still err after removing external factors), making L's judgment operational.

**Results (5 models)**: L with-empty 0.664 / non-empty 0.608, hit 81.8%; M full marks; P 0.887 / 0.834.

**Analysis**: L hit went from 50.9% → 81.8%, the sharp-criterion direction is right. But **Yuanbao was a severe outlier (L hit only 54.5%)** — it treated the sharp criterion as "literally looking for intersections/environments": on C3 it took "output to the user" as a boundary intersection → L2, on C2 it judged L4 because of an "environmentally leftover key", on C12 it judged L1. **Root cause: the sharp criterion lacked a "reverse constraint"** — there was no explicit statement of "which errors, even if occurring in a single round, do not count as L1" (e.g., errors driven by external instructions, environmental prerequisites that should not count).

---

### v9 · Sharp criterion + reverse constraint + 4 L anchors (L converges)

**What changed**:
1. **Reverse-constraint general rule**: before landing a layer, first ask "is this error produced spontaneously by the model in a single round, or driven by adversarial external input / cross-round information" — single-round spontaneous → L1, external instruction/injection-driven → L2, cross-round read-out → L3;
2. **4 L anchors fixed**: C2 autonomous privilege escalation → L1, C12 input medium → L2, C8 long conversation → L3, C1 retrieval poisoning → L3;
3. M/P child codes cut to a **common set** (avoiding the ambiguity of giving all child codes).

**Rationale**: v8's Yuanbao outlier proved the sharp criterion needs a "reverse constraint" backstop — you cannot infer L1 from "single-round reproducible" alone; you must prevent "external input / environmental prerequisite" from being misjudged as L1/L4. Anchors, meanwhile, give definite exits for high-frequency boundary cases, lowering the freedom of model judgment.

**Results (5 models: Doubao/Yuanbao/DeepSeek/MiniMax M3/iFlytek)**:
- **L with-empty 0.953 / non-empty 0.945, hit 98.2%** (Yuanbao 100%, DeepSeek 100%, MiniMax 100%, iFlytek 100%, Doubao 90.9% — Doubao deviated toward L1 only on C6);
- M 0.927 / 0.861 (pulled down by the C5 M7 disagreement);
- P 0.896 / 0.845.

**Analysis**: the reverse constraint + anchors direction was entirely correct — Yuanbao recovered from v8's 54.5% to 100%, proving its v8 issue was a missing reverse constraint, not a capability problem. **L non-empty κ=0.945, hit 98.2%, surpassing the industry benchmark MAST's 0.88.** But v9 also exposed three residual disagreements (which became the landing plan):

**Three residuals of v9**:
1. **C6 reverse-constraint over-exclusion**: Doubao judged prompt injection as L1 (the other 4 as L2) — it treated "external-instruction-driven" as also "single-round spontaneous"; the reverse constraint lacked a precise exclusion clause.
2. **C5 M split**: DS/MiniMax/iFlytek judged M5-9 Constraint-Goal Inversion, Yuanbao judged M7-3 Unauthorized Task Assumption, Doubao judged M7-1 Rule Mutual Exclusion — the boundary between M5 (constraint actively downgraded) vs M7 (the system itself conflicts) is still blurry, pulling M κ from v6's 1.0 down to 0.861.
3. **C2 golden changed to L1**: all 5 judged L1 (autonomous-privilege decisions occur inside the model), golden changed from L3 to L1; along the way we found C8's dual-golden contradiction (calibration L1 vs validation L3; v9's five all chose L3), and aligned it together.

---

### v1.1.1 · Landing (three anti-overfitting finalizations + full L-golden alignment)

Landed following "first set the proposal → red-team attack → compromise → prevent overfitting":

| Point | Landed content (SKILL.md criterion / calibration golden) | Anti-overfitting rationale |
|---|---|---|
| C6 | New "L-axis source-determination general rule": errors driven by adversarial external input such as prompt injection **are not eligible for the single-round-spontaneous exemption and are judged L2** | Fixes Doubao's misjudgment; does not over-exclude C3/C7/C5 (their source is inside the model, unaffected) |
| C5 | M7 vs M5 adds a "C5 reverse anchor (counter-anchor)": constraint actively downgraded as a trade-off → M5-9 Constraint-Goal Inversion; the system itself mutually exclusive → M7 | Fixes Yuanbao/Doubao misjudging M7, M κ recovers |
| C2 | New "autonomous-privilege anti-overfitting anchor": L1 mandatory, L4 mandatory-excluded, **L3 conditionally appended** (only appended when it relies on cross-stage elements and those elements themselves are at fault); CAL-02 golden L→L1 | Anti-overfitting: the anchor is landed as a "criterion", not a "conclusion", leaving a counterfactual exit |
| C8 | CAL-14 golden L→L3 (aligned to v9's five) | Along the way fixes the dual-golden contradiction |
| Untouched | coordinate_data.json (coordinate semantics unchanged) | Criterion clarity does not touch coordinates |

**Post-landing anti-overfitting note**: the C2 anchor deliberately **does not land as "autonomous privilege escalation is always L1"**, but as L1 mandatory + L3 conditionally appended + L4 hard-excluded — because the anchor was built for 12 synthetic cases; if landed as a conclusion, real-world variants (where the privilege-escalation action genuinely crosses stages) would be misjudged; landed as a criterion, real variants can be adjudicated by the criterion itself, preventing overfitting.

**Full L-golden alignment (v1.1.1, eliminating self-contradiction among same-source cases)**: following CAL-02's change to L1, CAL-03(C3)/CAL-10(C7) were also aligned to L1 (single-round spontaneous decisions), CAL-01(C1) aligned to L3 (cross-stage read-out), CAL-14(C8) aligned to L3 — these five are essentially either "single-round spontaneous decision" or "cross-stage read-out"; v9's five all converged, and if calibration changed only C2 and not C3/C7, it would create golden contradictions among same-type cases. **coordinate_data.json was not touched throughout.**

---

## Part 3: Multi-Round Comparison: κ Evolution Table

| Axis | R1 | R2 | v6 | v7 | v8 | **v9** |
|---|---|---|---|---|---|---|
| L (with-empty/non-empty) | 0.555 | 0.623 | 0.654/0.598 | 0.598 | 0.664/0.608 | **0.953/0.945** |
| L hit | — | — | 50.9% | 83.6% (hit) | 81.8% | **98.2%** |
| M (with-empty/non-empty) | 0.758 | 0.786 | 1.000/1.000 | 1.000/1.000 | 1.000/1.000 | 0.927/0.861 |
| P (with-empty/non-empty) | 0.658 | 0.946 | 0.898/0.851 | 0.898/0.851 | 0.887/0.834 | 0.896/0.845 |

**Patterns that can be read out**:
1. **The M axis reached full marks earliest and is the most stable** — the mechanism layer (where the problem lies) has terminology-oriented definitions and a clear process division, can be derived theoretically, and structurally has a natural advantage over the other two axes. M dropping from 1.0 to 0.861 is the C5 M5/M7 boundary problem, already fixed at landing.
2. **The P axis stabilized at 0.85-0.9 after criterion explicitness** — P's gain proves "criterion explicitness" is the only lever; the P-axis coordinate set is accumulated rather than structurally advantaged, so stabilizing in this range is already good.
3. **The L axis is the last shortboard conquered** — from 0.555 all the way to 0.945, relying not on changing golden (v7 proved it ineffective) but on the three-layer combination of sharp criterion + reverse constraint + anchors. **Every step of L's rise from 0.5 to 0.945 validated the methodology that "criterion clarity > changing the answer".**

---

## Part 4: The Divergence Between Test-Environment κ and Real-World Performance (key analysis)

The user asked us to focus on analyzing: **the κ in the environment looks good — will real-world scenarios look equally good? Is there numerical inflation introduced by the golden?** The honest conclusion follows.

### 1. What κ measures vs. what real-world scenarios need — they differ

- **κ measures**: the degree to which multiple annotators **land on the same code** for the same batch of cases (agreement); it **does not measure whether the landing is correct** (correctness is handled by the hit rate/golden).
- **What real-world scenarios need**: the user's **correct placement + generalizability** on real incidents (different variants all land on the code they should land on).

**High environment κ ≠ correct real-world discrimination.** What we measured is "model-as-annotator agreement", not "real-user (human/agent) agreement". The 12 synthetic cases made the 5 models agree, but **whether they agreed on "right" or "wrong" (relative to the true mechanism) cannot be distinguished inside the environment.**

### 2. The "numerical inflation" risk introduced by the golden (named honestly)

- **Changing golden itself inflates the hit rate**: v7 is the lesson — only changing the golden raised the hit rate to 83.6%, but κ did not change, proving that changing golden is "cobbling the answer together" without raising agreement. **So the hit rate may be inflated, but κ is inflation-resistant** (κ looks only at inter-model agreement and does not depend on whether golden is right).
- **Agreement built from anchors/criteria may be hollow**: v9's 4 L anchors were **built for the 12 cases**; all 5 judging L1/L3 consistently does not mean it is mechanism-absolutely correct — **if the 5 models share similar training biases, they may be collectively wrong**. This is the ceiling of the synthetic methodology, and why, at landing, we made anchors into "criteria + a left counterfactual exit" rather than "conclusions".
- **The hit rate may be inflated, but κ is real**: taken together, **the κ values are credible (they measure agreement itself), but "agreement being correct" has not yet been validated by real cases** — i.e., "the models agree" is validated, but "agreed and correct" awaits real cases.

### 3. Limitations of the environment sample

- **12 synthetic cases cannot represent the distribution of real incidents**: real-incident variants are infinite (C2's privilege escalation may not be an API key, C4's expired document may not be RAG); anchors cannot cover all variants.
- **Judgment cases are not probability samples**: synthetic cases are judgment samples constructed from recognized failure/attack patterns; they test only discrimination agreement, are not empirical, and cannot be used to ratify coordinates.
- **Model shared-bias risk**: the 5 domestic models may have overlapping underlying training data; the possibility of collective misjudgment cannot be ruled out.

### 4. But κ still has real, irreplaceable value

- **Criterion clarity is a lever that genuinely stabilizes real use**: the sharp criteria, reverse constraint, and source-determination added in v9/landing make it **easier for users to judge correctly** on easily-confused boundaries in real scenarios — this is a real, effective, non-inflated benefit.
- **κ is a necessary precondition for agreement**: first make the annotators agree (high κ), then let the agreed result be validated correct by real cases (ratify) — this is the right path. High κ is a "necessary condition", not a "sufficient condition".
- **The ultimate validation of real-world scenarios rests with the community**: per the established route, the κ test has reached a plateau; continuing to iterate on synthetic cases is overfitting; **what should really be done is, after landing, keep regression mode to prevent drift, and hand correctness validation over to the community, where real cases organically ratify after open-sourcing** (this fits the principle of "not doing validation that requires human annotators").

### 5. Three concrete differences between real-world scenarios and the test environment

| Dimension | Test environment | Real-world scenario |
|---|---|---|
| Sample | 12 synthetic cases, covering the defined split branches | Infinite variants; anchors may overfit |
| Annotators | 5 domestic LLMs (may share biases) | Humans / multiple agents, whose judgment basis may be closer to engineering reality |
| Judgment reference | golden (defined synthetically) | Whether the real incident truly belongs to that mechanism (needs ratify) |
| Source of inflation | Hit rate may be inflated by golden revision | κ agreement is real, but correctness is unvalidated |

**Conclusion**: **the environment's κ is "agreement validated, correctness pending"** — it proves the criteria are clear enough for independent annotators to converge, but "converging correctly" must be adjudicated by real cases. This is exactly why we hand validation to the community, and why we anti-overfit at landing (land anchors as criteria, annotate the source of validation, keep regression mode).

---

## Part 5: Validation Scope Statement (keep this section when shipping into the toolkit)

- **The current test uses only different LLMs as annotators** (Doubao/Yuanbao/DeepSeek/MiniMax M3/iFlytek Spark, 5 independent domestic), computing Fleiss κ and the hit rate across the L/M/P three axes.
- **No human-annotator test has yet been conducted**; the "discrimination-correctness" layer of κ (relative to the true mechanism) has not yet been independently validated by humans or real cases.
- **Will be added later**: after open-sourcing, the community will organically submit real cases and perform ratify and kappa re-testing; the toolkit already has built-in "regression mode" (re-running the calibration set on every revision to prevent silent drift), at which point the community can reuse the same batch of calibration cases to check.
- All synthetic cases in this document are for discrimination-agreement testing only, **are not considered real-incident records, and must not be cited externally or used as evidence for coordinate ratify**.

---

## Appendix: Key Methodological Takeaways from the Development History

1. **Criterion explicitness > changing golden > swapping coordinate definitions**: R2 (P meets target) and v7 (L changing golden is ineffective) double-validated this ordering. There is only one reliable path to raising agreement — make the criteria into "decidable operational questions".
2. **Sharp criteria must be paired with a reverse constraint**: v8's Yuanbao outlier proved that if a sharp criterion gives only the positive direction ("single-round reproducible → L1") without the reverse ("external-input-driven / environmental prerequisites don't count"), it will over-exclude boundaries. The reverse constraint is the backstop of the sharp criterion.
3. **Land anchors as criteria, not as conclusions**: anchors built for synthetic cases carry overfitting risk; they must leave a "counterfactual exit" (e.g., C2's L3 conditional append), annotate the source of validation, and await ratify by real cases.
4. **Accept the inherent differences across the three axes**: the M axis (mechanism layer) is terminology-heavy and theoretically derivable, easiest to reach high agreement; the P axis (broken facet) relies on accumulation and has no structural advantage — stabilizing at 0.85+ is already good; the L axis (which layer) has criterion boundaries that most need operationalization and was the last shortboard conquered.
5. **"Cannot point it out" is not the same as "it must be some layer"**: when information is insufficient, you must go through clarification / multi-select / pending-review; never treat insufficient information as a basis for landing a layer — this is the fixed discipline of the sharp criterion, already hardened into the toolkit at landing.

> This document is the complete process and analysis-methodology record of the TACT toolkit's kappa test, and will be merged into the corresponding place in the toolkit. The test uses only LLM annotators, with no human-annotator testing; the community will organically supplement it later.
