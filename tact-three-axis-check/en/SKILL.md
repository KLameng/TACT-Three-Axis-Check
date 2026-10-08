---
name: tact-three-axis-check
description: Locate failures, errors, and anomalies of AI systems as a unique coordinate in a closed coordinate space using the TACT three-axis coordinate taxonomy (L-axis = which layer it happened in / M-axis = how it went wrong / P-axis = which facet was broken). Use when the user describes a concrete problem, malfunction, anomalous output, or incident of an AI/LLM/agent system and wants to classify its error type, locate its L/M/P three-axis coordinate, and obtain a verification path. Execute the "Three-Step Matching Method": on the L-axis judge by the specific problem (single- or multi-select); on the M/P axes pass through the gates in order (parent coordinate first, then child coordinates; ask "is it" at every coordinate; strictly counter-check once regardless of the answer; finish the full path before deciding); finally output a structured conclusion containing the three-axis coordinate names, hit meaning, possible manifestations, occurrence location, and verification path. Trigger words: locate coordinate, what kind of error is this, TACT, three-axis, L-axis M-axis P-axis, error classification, failure-mode locating, look up a coordinate, verification path.
---

# TACT Three-Axis Coordinate Check

Locate the error phenomenon of an AI system as a unique coordinate in a closed coordinate space (L 4 layers × M 9 families × P 8 levels = 288 cells) and provide an executable verification path.

## Three things to remember about the coordinate system

The three axes are three facets of the same mechanism; each remembers one thing, and the axes do not overlap:

- **L-axis (where)**: the link in the system where the error occurs. L1 inside the model / L2 input-output interface / L3 reasoning-collaboration chain / L4 system environment.
- **M-axis (how)**: the form in which the error occurs. M1 insufficient information / M2 information corruption / M3 reasoning failure / M4 output corruption / M5 goal drift (excluding adversarial evasion) / M6 external adversarial action (including the agent's own adversarial behavior and regulatory evasion) / M7 rule-role-authority system mismatch / M8 system emergence / M9 spontaneous collaboration (parent coordinate admitted; opts empty; coordinate content pending ratification by real cases).
- **P-axis (what)**: which facet of consistency is broken. P1 factual distortion / P2 logical break / P3 completeness loss / P4 consistency breakdown / P5 compliance overstep / P6 goal deviation / P7 fairness imbalance / P8 safety threat.

A **parent coordinate** = a mechanism family; the same parent coordinate can contain multiple named subtypes (different concrete manifestations of the same mechanism family). When deciding a coordinate, ask "**is it essentially this layer**", not "does it merely touch it" — almost every error touches several layers; answering "yes" because it merely touches one will cause it to be wrongly stopped at an earlier layer.

### Hard-split criteria between parent coordinates (the M-axis internally mixes different dimensions; split first before passing the gates)

The 9 M-axis families mix three dimensions: form (M1-M5), source (M6/M9), system (M8), and rule system (M7). Between adjacent easily-confused families there is a veto-level criterion; hitting it redirects the judgment and does not allow stopping at the earlier family merely on "touch":

- **M5 (goal drift) vs M6 (external adversarial action)**: three checks; hitting any one goes to M6, and only if none hit does it go to M5——
  1. **Attack surface**: the event is actively manufactured by an external attacker (injection, poisoning, credential exploitation, supply-chain attack, etc.);
  2. **Privilege-overreach surface**: the behavior involves unauthorized acquisition/access/control/transmission of external resources, systems, or credentials (autonomous privilege escalation, escape, capability extraction, unauthorized data exfiltration);
  3. **Deception surface**: the behavior involves adversarial deception (inducing humans into high-risk decisions, exploiting detection/monitoring blind spots, forging state to deceive).
  **Pure autonomous deviation** not involving any of the above (irrelevant answers, goal drift, sycophancy, miscalibrated self-assessment, context drift, constraints downgraded by trade-off) → M5.
- **M6 (external adversarial action) vs M8 (system emergence)**: criterion = **whether an adversarial subject exists**. If there is an attacker or the agent's own adversarial behavior → M6; if there is no subject at all and the error emerges from combination/emergence → M8.
- **M5 (goal drift) vs M8 (system emergence)**: criterion = **single-entity deviation vs multi-component emergence**. The direction of a single system/model's behavior deviating from design intent → M5; multiple individually-correct parts combining to emerge an error → M8.
- **M7 (rule-system mismatch) vs M5 (goal drift)**: criterion = **the source of the conflict/mismatch**. The rule, duty, or authority system itself conflicts or mismatches (mutual exclusion, no ownership, unauthorized assumption) → M7; no conflict in the system, but the behavior direction is replaced/deviated (including constraint-goal inversion M5-9) → M5. **C5 reverse anchor (v1.1.1, fixes kappa v9 misjudgment by Yuanbao/Doubao)**: the model **actively downgrades/trade-offs a constraint into an optimization objective** (sacrificing the constraint for conversion rate, etc.) → M5-9; the **rule/duty/authority system itself** is mutually exclusive, has no ownership, or is assumed without authorization → M7. The distinction: C5 is **choosing not to comply at the execution layer** (the system is fine; the behavior direction deviates), M7 is **the system itself conflicting** (running into contradictory rules); "honoring old customers while misleading new ones" → M5-9.
- **M6 vs M9 (spontaneous collaboration)**: criterion = **the nature of the behavior**. Multi-agent collaboration breaking an access boundary or producing an adversarial action → M6 (M6-6); no adversarial action, only collaboration exceeding expectations that emerges from shared-resource utilization → M9. **When M9 is hit, output the fixed wording: 『Parent coordinate M9 spontaneous collaboration; child coordinate pending ratification by a real case; no child code assigned for now』**, and locate on the L-axis only; do not fabricate a child code, and do not treat the absence of a child code as failure.

### Gate-passing quick reference (split-sentence overview; details in each coordinate's desc)

- User-induced rule-bypass without malice: M6-11 (treat evasive behavior on the adversarial surface; do not redirect because "the user is not an attacker").
- Memory/summary writes: a write driven by an external attacker or malicious injection → M6-4; autonomous write without an attacker (including external non-malicious inducement) → M5-8.
- Group disparity: **first ask which layer the disparity is in** — the constraint-execution layer (whether constraints/boundaries are honored fluctuates with the group; equivalent situations treated differently) → M5-9; the decision-result layer (scores/recommendations/advice results systematically worse) → M2-5. Counter-example to prevent misjudgment: "honoring old customers while misleading new ones" looks like algorithmic discrimination but is a constraint-execution-layer disparity → M5-9; "a recommender gives one group systematically worse results" is the decision-result layer → M2-5.
- Privilege overreach: passively assuming an overreach task, permission check failing → M7-3; autonomous probing breakthrough without an external overreach command / without an external attack command (a legitimate user command does not change the autonomous-breakthrough essence) → M6-6.
- Data exfiltration: the agent transmits/writes data externally without authorization → M6-6 (the privilege-overreach surface includes "transmission"); a human user or tool actively uploading, or default product behavior → governance domain, occupies no M/P code.
- Self-interested deception combined with decision inducement: prioritize M6-5 by consequence surface.
- Data/retrieval errors: poisoning intent or an attacker exists → M6-7/M6-8; data or retrieval errors without intent → the M2 family.
- Injection and memory: the instruction is executed immediately → M6-3; the instruction/malicious content is written into memory or a summary and subsequently referenced persistently → M6-4; when both hold simultaneously, list both under the Three-Step Matching Method (immediate execution → M6-3; persistent reference → M6-4) rather than forcing a single code.
- Deception target: inducing/manipulating human decisions → M6-5; evading a monitoring/rule system → M6-11; mixed scenarios are decided by the final manipulated object.
- Constraint downgrade: the constraint trade-off serves a non-self-interested task/business goal → M5-9; self-interest-driven (exploiting reward loopholes for one's own benefit) → M5-5.
- Prohibition violation: the prohibition is directly ignored (no evasion) → M5-2; violating via variants, blind spots, splitting, etc. → M6-11.
- Inflated self-assessment: internal-confidence/self-assessment signals misalign with accuracy → M2-3; externally taking on tasks, overclaiming capability, faking benchmark results → M2-4.
- Constraint forgetting: a conclusion over-generalized after being stripped of context → M5-6; early information/constraints lost and forgotten in a long conversation → M8-3.
- Format violation: output/interface contract violations (format, schema, fields) → M4-3/P5-6; behavior/task-constraint violations (prohibitions, normative actions) → M5-2/P5-5.

### Cross-axis split statement

The same event can be hit independently on the M-axis and the P-axis (each of the three axes records one facet; this does not constitute double counting). Typical example: a self-written persistent instruction — M-axis passes **M5-8** (how it went wrong = goal silently replaced), P-axis passes **P6-4[5]** (what is broken = goal deviation); the two axes are independent and do not replace each other; constraint-goal inversion — M-axis passes **M5-9** (mechanism = constraint downgraded into an optimization objective), P-axis passes **P7-4** (broken = fairness-imbalance facet).
Inter-axis division statement: the L-axis asks "which layer", the M-axis asks "how it went wrong"; the semantic overlap of M8 and L3 is a division of labor, not duplication — an error that no single link makes but appears only when connected → L-axis L3, M-axis M8; "contradictory-sentence" output — logical conflict prioritizes P2-4, fact-checking errors go through P1-8, inconsistency with its own history goes through P4-9; environment-transfer mismatch prioritizes M1-3/P3-6 (mechanism facet), while an environment fault itself (network/quota/isolation boundary) goes through L4.

## Data file (must read before execution)

`references/coordinate_data.json` is the sole data base of this skill (v2.7.8, 117 refined coordinates / 580 "manifestation-location-verification-path" entries), structured:

- `L[]`: the 4 L-axis layers, each containing `code/name/criterion` (criterion is the operational criterion for judging "whether it belongs to this layer").
- `M_groups[]` / `P_groups[]`: 9 M-axis **parent coordinates** (M1-M9, of which M9 is admitted with opts empty and content pending ratification) and 8 P-axis **parent coordinates**, each containing `code/name/criterion` and `opts[]` (the **child coordinates** under that parent coordinate).
- Each child coordinate: `code` (e.g., M3-1), `name` (mechanism name), `desc` (one-sentence mechanism description), `pairs[]` (each entry a triple; count varies by coordinate):
  1. **Manifestation**: what the error looks like as a phenomenon;
  2. **Location**: which position/link of the system the error occurs in;
  3. **Verification path** (third segment): which link to go to, what operation to use for diff/reproduction, and which criterion appearing indicates a hit.

Whenever coordinate meaning, criterion, manifestation, location, or verification path is needed, always read this file; do not fabricate coordinate names or verification methods from memory.

## Three-Step Matching Method (core execution flow, strictly in order)

### Step 0: Pre-exclusion gate (exclude the "no-code" cases first, then enter L/M/P)

Before starting the Three-Step Matching Method, check the four types of **no M/P code** cases in order; hitting any one → **first pass the "over-exclusion guardrail", then take the corresponding exit** (only after the guardrail confirms exclusion should you stop entering the L/M/P gates); only if none hits do you enter Step 1. Judge each by its "subject/essence" anchor. **Mixed scenarios are not wholly excluded**: when, beyond the excluded part, a genuine model/system error component still exists, do not exclude it entirely; continue passing the gates to process the remaining part (mark the excluded part separately).

| No. | Case | Discrimination anchor (ask first) | Exit |
|---|---|---|---|
| E1 | **Governance domain** | Is the **subject of the error a human** — a human using AI as a tool to commit crimes/attacks (deepfake fraud, face-swap payment theft, etc.)? Note: adversarial/malicious acts **autonomously initiated by the agent** are not in this column; continue passing the gates | Governance domain, occupies no M/P code |
| E2 | **Environment/infrastructure failure (out-of-scope declaration)** | Is **the environment broken** (network/quota/isolation boundary/config defect/AppSec vulnerability/organizational governance), or is it the system failing to adapt to the environment (the latter is the M1-3/P3-6 mechanism facet, continue passing the gates)? And did the model itself not err? | Describe on L4 only, occupies no M/P code |
| E3 | **Prediction slot** | Is the mechanism supported by **only 1 real case** and on the prediction-slot list (sensor deception/input-medium replacement, safety emergency shutdown/circuit-breaker failure)? | Mark as prediction slot, describe at the L layer of the mechanism, occupy no formal M/P code, fabricate no code |
| E4 | **Evaluation risk signal** | Is it only a **tendency/signal** that has not yet constituted an occurred error event (rising deception, alignment regression, overreach tendency)? If it constitutes an actual error behavior, pass the gates | Describe on L1 only, occupies no M/P code |

**Over-exclusion guardrail (read before excluding):** the exclusion gate is a **split guide, not a final verdict** — after hitting any E, pass the following guardrail before deciding the exit. The core rule: **default-to-inclusion when in doubt** — if you are unsure whether to exclude, do not exclude; let it in and pass the gates, and let the Three-Step Matching Method (rather than the pre-gate) decide; if a genuine system error component is later found, revoke the exclusion and continue passing the gates.

- **G1 Structural · exclusion is revocable**: exclusion does not exempt review. After hitting any E, counter-check once: "Does a mixed scenario / an environment masking a system error / an autonomous agent component exist?" If any holds, do not release it; pass the gates on that component.
- **G2 (E1 governance domain) dual-subject split**: a human as a pure tool (deepfake fraud, face-swap payment theft, no autonomous error by the AI) → exclude; **human inducement + autonomous execution by the agent** of rule-bypassing/malicious acts → pass the gates (quick reference: user-induced rule-bypass → M6-11, autonomous privilege escalation → M6-6), do not wholly exclude because "a human participated".
- **G3 (E2 environment layer) ask first whether the system has an error component**: before excluding, confirm "whether the model/system itself also has erroneous behavior"; if so, it cannot be wholly attributed to L4; pass the gates on that component (e.g., an isolation-boundary fault simultaneously exposing autonomous privilege escalation and exfiltration → pass M6-6).
- **G4 (E4 evaluation signal) tendency vs behavior criterion**: has an **observable violation/error output** been produced? Yes → pass the gates; only tendency/signal → exclude (L1 only).
- **G5 (E3 prediction slot) list-drift protection**: the list is governed by the latest text of "Boundaries and Discipline"; once a mechanism is graduated (two mutually unrelated real cases appear) → no longer exclude, pass the gates normally; "sensor deception/input-medium replacement (prediction slot)" vs "feature perturbation M6-10 (formal code)" are split by "changing the input source vs changing the sample representation".

Rule definitions are governed by the "Boundaries and Discipline" section; this section is the operationalized entry; if after walking through every item you still cannot decide whether to exclude, return to "Boundaries and Discipline" to check the original text.

### Step 1: L-axis selection — judge by the specific problem, single- or multi-select

Read the criterion of each `L[]` one by one and, combined with the user's **specific problem**, judge which layer it erred in:

- If the phenomenon clearly occurs in only one link → single-select one L;
- If the phenomenon spans multiple links (e.g., committed within a single turn yet amplified again at the interface) → multi-select; complete the subsequent M/P gate-passing for each hit L separately.

#### L-axis operational criteria (added v1.0.3, based on kappa round-4 L-axis 63.3% convergence)

First ask the **overall-problem** layer: is this error "one the model can commit within a single turn on its own (not relying on cross-turn/external information)", "one that requires reading out cross-turn/external information", "one that occurs at the inbound/outbound boundary handoff", or "the environment itself broke"? Then use the table criteria to land the layer:

| L layer | Deciding question | Anchor |
|---|---|---|
| L1 inside the model | If all external input, cross-turn memory, collaboration units, and environmental factors are deleted, would a single standalone generation by the model still commit the error? | single-turn, no external dependency, appears within one generation |
| L2 input-output interface | Does the error occur at the **boundary handoff** where data enters / results leave the system (the two sides' symbols/fields/rules/conventions fail to match)? | inbound/outbound boundary, format/symbol/convention mismatch |
| L3 reasoning-collaboration chain | Does the error require **reading out cross-turn/external information** (RAG, memory, toolchain, long conversation, outdated documents) to participate in the current decision, or does it occur in inter-link transfer/handoff? | cross-turn/external readout, multi-link combination, each link individually correct |
| L4 system environment | Does the error originate from the runtime environment itself (network, quota, isolation boundary) rather than model behavior? | environment broken, model did not err |

**Key-boundary quick reference (either criterion suffices to land the layer)**:
- **L1 vs L3**: does it require reading out cross-turn/external information to participate in the current decision? Yes → L3; no → L1.
- **L1 vs L2**: an error the single generation can commit internally (not involving inbound/outbound boundary handoff) → L1; an error at the inbound/outbound boundary handoff (format/symbol/convention) → L2.
- **L2 vs L3**: an error in a single-turn inbound/outbound interface handoff → L2; in cross-turn/cross-link transfer and combination → L3.
- **L3 vs L4**: the fault source is within the model/reasoning-chain's repairable range → L3; in infrastructure and logically unrelated to model reasoning → L4.

**L-axis source-determination general rule (added v1.1.1, based on kappa v9 C6 reverse-constraint false-hit fix)**:

Before landing the layer, first ask the **error source**: is this error "spontaneously produced by the model itself within a single turn", or "driven by adversarial external input / cross-turn information"?

- The error source is **internally spontaneous to the model** (no external command/injection/cross-turn readout; the model's single-turn decision produces it) → prioritize L1;
- **Errors driven by adversarial external input such as prompt injection** (malicious instructions overriding the system prompt, embedded instructions taken as real and executed) → the "single-turn spontaneous" exemption does **not** apply — the source is at the input boundary rather than inside the model; by the sharp criterion judge **L2** (the error is triggered at the boundary handoff where data enters the system);
- Requires **reading out cross-turn/external information** to participate in the current decision (RAG, memory, toolchain, long conversation, outdated documents) → L3;
- An environmental fault causing the model to fail, with the model not erring → L4.

**Autonomous privilege-escalation special anchor (C2, v1.1.1, anti-overfitting version)**:
- The privilege-escalation **decision** is spontaneously produced inside the model (no external command/attacker) → **L1 is mandatory**;
- If the escalation **necessarily depends on cross-link/toolchain to complete**, and that link itself errs or mismatches (e.g., a link accepts the overreach command as a normal task) → **append L3**;
- If the escalation completes within a single turn (the model directly outputs the overreach result, no cross-link dependency) → **do not append L3**;
- **Never choose L4 because of "environment-left keys/credentials"** (the model actively exploits them; the environment did not make it fail; L4 holds only when an environmental fault makes the model fail).

> Note: the L golden of C1/C2/C3/C7 (poisoning, overreach, inducement, evasion) has been aligned by the v1.1.1 operational criteria — C1→L3 (cross-link readout), C2→L1 (the overreach decision is inside the model), C3→L1 (single-turn spontaneous speech), C7→L1 (single-turn spontaneous evasion), consistent with the v9 five-annotator convergence.

### Step 2: M- and P-axes — pass through the gates one by one with the Three-Step Matching Method

The M-axis and the P-axis each **independently** run the following flow (fixed order: M first, then P; parent-coordinate queue order M1→M9 / P1→P8, no skipping):

1. **Walk the parent coordinates first, then the child coordinates.** Go group by group through the parent-coordinate gate along M1→M2→…→M9 (P1→P2→…→P8); only after the parent-coordinate gate judges "yes" do you enter that group's `opts[]`, then walk the child-coordinate gates from the first child coordinate onward. Only a "no" allows you to move to the next.
2. **Ask "is it" before every coordinate.** Whichever coordinate you reach (parent or child), ask once against its criterion / desc / pairs manifestation "is this essentially this layer/entry"; each layer has only "yes/no" two options.
3. **Counter-check: regardless of whether the answer is "yes" or "no", strictly counter-check once to see whether the conclusion can be overturned.**
   - Answer "yes" → counter-check: "Is there a veto-level hard counter-example proving it is essentially not this entry?" (keep it only if it cannot be killed)
   - Answer "no" → counter-check: "Is its mechanism actually landed here? Was it misjudged as no because only the surface consequence was seen, not the mechanism?"
   - Supportive evidence is cheap (every error has touch evidence); what to look for is a **mechanism-level hard counter-example**, not fault-finding.
4. **Walk the full path before deciding; do not lock early.** Even if an earlier coordinate looks like a hit, you must finish asking the whole axis to prevent missing a more essential coordinate later; finally retain all hit coordinates that pass the counter-check and cannot be killed (one axis can hit multiple child coordinates; list them separately, do not force them into one).

### Step 3: Combine Steps 1 and 2 to give the overall conclusion

Combine the hit L and M, P into a complete coordinate (e.g., L2/M3/P1) and draft it in the output format below.

## Output-conclusion format (all five items required)

The conclusion must contain:

1. **Three-axis coordinate names**: the complete coordinate (e.g., L2/M3/P5) + the three parent-coordinate names (e.g., "input-output interface · reasoning failure · compliance overstep");
2. **The hit L-axis coordinate(s)**: the L coordinate number and name, and why this layer (cite the criterion); for multi-select L, explain each;
3. **All finally-hit child coordinates**, each giving four things:
   - **Meaning**: child-coordinate code + mechanism name + desc;
   - **Possible manifestations**: the 1~3 "manifestation" excerpts from that code's pairs most aligned with the user's phenomenon (may be multiple);
   - **Occurrence location**: the corresponding "location" (second segment of pairs);
   - **Verification path**: the corresponding third-segment "verification path", given verbatim as the operational criterion, unmodified and not self-created;
4. **Counter-check trail**: briefly state the points overturned by the counter-check or nearly misjudged at the parent/child-coordinate gates, and why the final coordinate was landed there (reflecting coordinate uniqueness);
5. If the whole axis is walked and still cannot be decided, do not force it: state that the existing 117 refined coordinates cannot accommodate it, and give the judgment on whether a new layer should be added according to "whether it is an independent unique mechanism and whether two mutually unrelated errors belong to the same mechanism", leaving the decision to the user; do not fabricate codes on your own.

## Boundaries and discipline

- Only do location and verification-path description; do not give final assertions such as "the system definitely has this vulnerability / has already been breached"; when the output faces the user, append "AI analysis result, for reference only".
- Verification paths are for reproduction/verification on **one's own environment, one's own model, one's own range**; when actively constructing attacks (injection, escape, poisoning) is involved, note that this is limited to an authorized self-owned test system and must not be launched against any third-party real system.
- Same-name child coordinates are not the same entry: go by code and its parent coordinate (e.g., M3-1 and P1-3 have similar mechanisms but different coordinate facets).
- Data is governed by `references/coordinate_data.json`; after a hit, use the pairs verbatim as the basis; fabrication of manifestations or verification steps from training memory is forbidden.
- **Out-of-scope declaration**: incidents in which "the system itself did not err" — config defects, infrastructure failures, traditional software/AppSec vulnerabilities, organizational governance (authorization scope, platform policy, copyright-licensing disputes) — are outside the classification scope; TACT is an error taxonomy, not an incident taxonomy; such phenomena are only described at the L4 environment layer, with no new M/P coordinates. A legitimate service used as an unlawful channel (channel-purpose hijacking) is a combined manifestation of "credential compromise + governance defect", decomposed into M4-2 credential leakage and a governance statement, with no standalone coordinate. Human attackers using AI tools to commit crimes/attacks (deepfake fraud, face-swap payment theft, etc.) belong to the governance domain and occupy no M/P code.
- **M6-10 boundary sealing**: textual-domain adversarial suffixes (GCG-type, co-occurring "representation-layer perturbation" and "semantic-layer injection") are all attributed to M6-3 prompt injection; M6-10 feature perturbation governs only multimodal/physical-domain perturbation (pixels, features, physical stickers, audio); the two coordinates are split by "semantic layer vs representation layer" and do not overlap.
- **Prediction slot**: mechanisms with only 1 real case (currently e.g., sensor deception/input-medium replacement, safety emergency shutdown/circuit-breaker failure) remain in prediction-slot status, occupying no formal child-coordinate number; they graduate after two mutually unrelated real cases appear per the evolution rule, with no self-fabricated codes.
- **Evaluation risk signal**: tendencies exposed by the model in evaluation (e.g., rising deception, alignment regression, overreach tendency) that have not constituted an occurred error event are only described at the L1 layer, occupying no M/P code; only after they constitute an actual error behavior do they pass the Three-Step Matching Method gates.
- **Mirror and symmetry**: each of the three axes records one facet; the same mechanism being double-listed on the M/P axes is a design feature (M judges how it went wrong, P judges what is broken), not a duplicate coordinate. Main mirror comparisons: M6-1≙P8-8 supply chain, M6-2≙P8-9 credential leakage, M6-3≙P6-4 prompt injection, M6-5≙P8-5 human-agent trust exploitation, M6-6≙P8-4 sandbox escape (approximate, not an exact same-name mirror; the P facet goes by phenomenon: escaping the sandbox → P8-4, permission-expanded assumption → P5-2, neither fits → leave blank pending verification), M6-11≙P8-7 regulatory evasion, M5-9≙P7-4 constraint-goal inversion, M5-8≙P6-4[5] self-written persistent instruction, M4-2≙P8-3 credential leakage, M4-3≙P5-6 contract violation. When deciding a coordinate, first ask "is it essentially this layer" (parent-coordinate criterion); mirror pairs do not preempt each other: a hit on the M-axis and a hit on the P-axis for the same event are retained independently. **New coordinates do not force a mirror to be added** — only when a real case proves that the P-side (or M-side) manifestation of that mechanism independently holds is it added; do not fabricate mirror entries "for symmetric aesthetics".

## Calibration set — this section is purely additive and does not modify any existing rule above

`references/calibration_cases.json` (v1.1.1, 21 cases, bound to coordinate_data.json v2.7.8) is the **calibration baseline** of this skill, with two purposes, both optional and not gating:

1. **Calibration mode**: run the gate-passing flow with this file, compare against the golden, and compute the three-axis hit rate; where misclassification clusters is the convergence point for SKILL.md/data wording. **Hit rate is a diagnostic signal, not a pass/fail; a low hit rate does not block skill use.**
2. **Regression mode**: rerun after every revision or coordinate_data upgrade to guard against silent drift.

Usage discipline (see `usage_rules` inside the file; read before execution):

- **Zero code fabrication**: this file contains no code that is not in coordinate_data.json; every golden code has been individually verified to exist.
- **synthetic is not empirical evidence**: cases with `status=synthetic` are discrimination samples constructed per well-known failure/attack patterns, testing only discrimination consistency; they are not treated as real incidents, not used for external citation, and not used as coordinate-ratify evidence.
- **Golden can be overturned**: when a conflicting new real case appears, revise that entry and record it; do not freeze it.
- **Cracks fixed at the author's discretion (v1.0.1)**: the M6-6 mirror name was corrected to P8-4 sandbox escape and marked approximate; the M6-3/M6-4 co-occurrence criterion was unified to dual-listing. If an executor later finds a discrepancy between a SKILL.md statement and the data, defer to the data and record it for the author's decision; do not unilaterally modify SKILL.md or coordinate_data.json.
- **v1.0.2 (execution-flow optimization)**: added "Step 0 Pre-exclusion gate" — four no-code cases (governance domain / environment layer (out-of-scope) / prediction slot / evaluation signal) are excluded first, then the L/M/P gates are entered; the quick-reference "group disparity" entry gained the M5-9/M2-5 reverse-comparison anchor (constraint-execution layer vs decision-result layer).
- **Maintenance record (2026-09-29, SKILL.md flow fix; coordinate_data.json and calibration_cases.json unchanged)**: fixed the M9 routing dead-end — appended the fixed landing wording at the end of the "Hard-split criteria · M6 vs M9" branch (when M9 is hit, output 『parent coordinate M9 spontaneous collaboration, child coordinate pending ratification by a real case, no child code assigned for now』, locating on the L-axis only), so the five-item output is self-consistent even when M9 is hit.
- **Maintenance record (2026-10-01, v1.0.3, kappa round-4 convergence)**: ①Step 1 L-axis selection added "L-axis operational criteria" (deciding question + key-boundary quick reference L1vsL3/L1vsL2/L2vsL3/L3vsL4), improving L-axis consistency and terminology (converging the common short board of the round-4 L-axis hit rate 63.3%); ②C2(CAL-02) P facet changed from blank to P5-2 (overreach access to out-of-permission data, permission self-expanded), P8-4 marked approximate-mirror pending empirical verification; calibration_cases.json's golden/expected_discipline/changelog updated in sync. This revision changed only SKILL.md execution guidance and calibration CAL-02, **not coordinate_data.json**.
- **Maintenance record (2026-10-01, v1.1.1, kappa v9 three-point landing + L golden alignment)**: ①added "L-axis source-determination general rule" — errors driven by adversarial external input such as prompt injection do not get the "single-turn spontaneous" exemption and are judged L2 by the sharp criterion (fixing C6 reverse-constraint false-hit: Doubao misjudged L1 in v9); ②M7 vs M5 gained the C5 reverse anchor — constraint actively downgraded/trade-offed → M5-9, system itself mutually exclusive → M7 (fixing the v9 Yuanbao/Doubao C5 misjudgment of M7, M κ recovered); ③added "autonomous privilege-escalation special anchor (anti-overfitting version)" — L1 mandatory, L4 must be excluded, L3 conditionally appended (C2 golden aligned, guarding against overfitting and mis-selection); ④calibration L golden fully aligned with v9 validation — CAL-02 L→L1, CAL-03 L→L1, CAL-10 L→L1, CAL-01 L→L3, CAL-14 L→L3 (eliminating self-contradictory golden among same-source cases). This revision changed only SKILL.md criteria guidance and calibration golden, **not coordinate_data.json**.
- **Kappa test record (v1.1.1 supplement, open-source statement section)**: the full history of L/M/P three-axis inter-model consistency κ (per-round prompts/results/theoretical basis, environment-κ vs real-scenario difference analysis, verification-scope statement) is in `docs/TACT-kappa全历程汇总与分析.md`. The test **used only different LLMs as annotators, with no human verification**; the "discrimination correctness" of κ awaits spontaneous ratification by the community's real cases after open-sourcing (flow in `CONTRIBUTING.md`), to be supplemented later. Positioning and known boundaries are in the root `README.md`.
