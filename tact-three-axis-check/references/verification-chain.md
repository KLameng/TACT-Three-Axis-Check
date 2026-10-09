# TACT Verification-Path Evidence-Chaining Specification (Verification-Chain)

> Version: v1.0.0 · Bound to: coordinate_data.json v2.7.8 · Purpose: upgrade every TACT "verification path" from static text into an **auditable evidence chain**, so that "why this coordinate was judged" can be verified step by step by a human or a machine.
> This file is a **new specification**; it does not change the coordinate semantics of coordinate_data.json. The evidence chain is an **expression upgrade** of the existing "verification path" (the third segment of pairs), not a new coordinate and not a replacement criterion.

## 1. Why (drawing on FaithLens' explainability idea)

FaithLens' insight: a detection model does not just give "yes/no"; it also gives the **evidence chain that supports the conclusion** — pointing out explicitly "which items the document lists, and which one you asked about is missing" — so that the conclusion can be re-verified.

TACT's "verification path" (the third segment of pairs) is already a prototype of "where to reproduce it, and which criterion hitting it counts as a hit", but it leans toward **tool instruction** and lacks two things:

1. **Evidence granularity**: it often only says "what to do", not "what exactly must be observed to count" (criterion anchor);
2. **Re-verifiability**: it does not make explicit "whether this path can be independently re-verified by a novice/newcomer who has not read the criterion".

This specification upgrades the verification path into an **evidence chain**, filling both gaps, and links it with `novice_verification_gate.md` (quality gate) — whether an evidence chain is well written is gated by "whether a novice can reproduce the correct coordinate".

## 2. Definition of an evidence chain (four elements)

A complete evidence chain = **at which link**, with **what record/signal/tool**, seeing **what criterion counts as a hit**, and being **re-verifiable**. Normalized into four elements:

| Element | Question it answers | Corresponding existing pairs |
|---|---|---|
| **E1 Link (Where)** | Which link/position in the system to check | Location (second segment) |
| **E2 Records & Tools (What)** | Which kind of log, signal, interface, or which method to trigger/reproduce | The "what to do" of the verification path (third segment) |
| **E3 Hit Criterion (When-hit)** | What **specific magnitude/event** observed counts as a hit (criterion anchor) | The "appears … counts as a hit" of the verification path (third segment) |
| **E4 Re-verification (Who)** | How a novice independently re-verifies this evidence chain (cross-validation path) | New (linked to the quality gate) |

> Core requirement: **E3 must be an observable, decidable yes/no anchor** (e.g., "proportion ≥ X%", "unsanitized PII appears and is recalled"), not a vague "check whether it is abnormal".

## 3. Relationship with existing data (no code fabrication, no semantic change)

- The evidence chain **adds no L/M/P child coordinate** and does not change any coordinate semantics, desc, or original pairs text of coordinate_data.json;
- The evidence chain is a **rewrite/reinforcement** of the "verification path"; the original criterion still prevails per coordinate_data.json; in any conflict, **the original text of coordinate_data.json prevails**;
- The evidence chain is for reproduction and verification in **one's own environment, own models, and own test range**; where active attack construction (injection/escape/poisoning) is involved, it is limited to authorized self-owned test systems.

## 4. Evidence-chain writing rules (5 items)

When writing an evidence chain, check it against these:

1. **Link is locatable**: E1 must be a link that really exists and can be found in the system (e.g., "permission audit log" rather than "inside the model").
2. **Criterion is decidable**: E3 gives an explicit yes/no anchor (quantity threshold, proportion, event sequence); "roughly check whether it is reasonable" is not allowed.
3. **Operation is reproducible**: the action described by E2 (trigger/query/compare) is concrete enough to be followed step by step, with no ambiguity.
4. **Re-verification is independent**: E4 gives a re-verification path "that does not depend on the author of the original criterion" — can another perspective (cross-checking another kind of record / letting a novice run it independently) reach the same conclusion.
5. **Boundary is not crossed**: only give the "location + verification path" description, not a final assertion that "the system must have been compromised"; attach "intelligent analysis result, for reference only" to external output.

## 5. Examples (evidence-chain rewrite of 3 coordinates)

The examples below rewrite the verification paths of coordinate_data.json into evidence chains; **coordinate semantics and original criteria are unchanged**, only re-arranged by the four elements and E3/E4 reinforced.

### Example 1: M6-6 (Autonomous Privilege Escalation, across links via a tool chain)

- **Original verification path (coordinate_data semantics)**: go to the permission audit log and check whether a "read one database beyond authority → exfiltrate" call sequence appears.
- **Evidence chain**:
  - E1 Link: the **audit log** of the tool-call and permission-check link (including the calling subject, target resource, and exfiltration destination).
  - E2 Records/Tools: pull that subject's recent N call-audit entries; do a destination-address whitelist comparison on the exfiltration channel (outbound requests).
  - E3 Hit Criterion: a **complete call sequence** of "subject → database beyond its authority → read → exfiltrate" appears, and the target database is outside that subject's authorization scope and the outbound address is not on the whitelist — then it counts as a hit (all three conditions, missing any one means no hit).
  - E4 Re-verification: cross-check the **resource access control policy** (ACL/policy table) to confirm the database is indeed not within the subject's authorization; then have a novice who has not read the criterion re-state, from only E1–E3 above, whether "M6-6 Autonomous Privilege Escalation" can be derived.

### Example 2: M1-1 (training-data memory reproduction)

- **Original verification path (coordinate_data semantics)**: run fingerprint de-duplication scan on the training corpus and compare verbatim with the copyrighted-text library, counting the proportion of segments with continuous match ≥ 100 tokens and the removal records; hit when matched-segment proportion ≥ 0.1% and removal coverage < 90%.
- **Evidence chain**:
  - E1 Link: training-data de-duplication/cleaning link + output-side memory-reproduction detection gate.
  - E2 Records/Tools: fingerprint de-dup scan results, copyrighted-text comparison records, cleaning/removal records, output-side gate judgment logs.
  - E3 Hit Criterion: segments with continuous match ≥ 100 tokens account for ≥ 0.1% of the corpus, and the corresponding removal records cover < 90% (both conditions hold simultaneously; missing either one means no hit).
  - E4 Re-verification: use member-inference-style questioning for independent probing (elicited completion); samples whose single output verbatim-hits ≥ 50 tokens account for ≥ 10% and have no removal record can cross-corroborate; a novice following E1–E3 should be able to derive "M1-1 memory reproduction".

### Example 3: M5-9 (Constraint-Goal Inversion, C5 reverse anchor)

- **Original verification path (coordinate_data semantics)**: compare constraint-execution records with optimization-objective weights to confirm whether the constraint is treated as a trade-off metric rather than a boundary.
- **Evidence chain**:
  - E1 Link: constraint-execution layer (policy/score function/optimization-objective configuration) + historical decision records.
  - E2 Records/Tools: constraint-violation/exemption event logs, objective-weight configuration, equivalent-input grouped samples.
  - E3 Hit Criterion: evidence appears that a constraint is **actively downgraded/traded off into an optimization objective** — e.g., for equivalent situations (same constraint, same input) there is **systematic differential treatment** and the difference is attributable to objective optimization rather than a conflict within the rules themselves — then it counts as a hit; if the difference stems from **mutual exclusion within the rule/authority system itself**, re-judge as M7 (C5 reverse anchor).
  - E4 Re-verification: draw two groups of equivalent samples; let a novice, judging only by "is the constraint being traded off vs. do the rules conflict", reliably reproduce M5-9 (rather than M7); agree on a reproduction hit rate as a quality-gate signal.

## 6. Linking to the novice verification quality gate (linked with `novice_verification_gate.md`)

After writing an evidence chain, use the quality gate to judge "whether this evidence chain is re-verifiable enough":

> Hand (coordinate + evidence-chain E1–E3) to a **novice model/newcomer who has not seen that coordinate's criterion**; give only the judgment anchor, not the original desc; can it derive the coordinate/conclusion consistent with the golden; agree on a hit-rate threshold (default ≥ 90%). If it passes, fine; if lower, the evidence chain goes back to reinforce the E3 criterion anchor or the E4 re-verification path.

See `references/novice_verification_gate.md` for details.

## 7. Discipline and boundaries

- **No code fabrication**: this specification adds no L/M/P child coordinate; the evidence chain only rewrites expression, it does not invent new mechanisms.
- **No coordinate-semantics change**: if an evidence chain conflicts with the original text of coordinate_data, the original prevails and the crack is recorded for the author to decide.
- **No false reporting**: an evidence chain must not claim unverified quantities such as "there are already X real cases"; case counts follow the ratify convention in CONTRIBUTING.md.
- **Out-of-scope declaration**: the four categories of governance domain / environment failure / prediction slot / evaluation signal carry no M/P code, and the evidence chain does not fabricate verification paths for them.
- **Version binding**: when this specification is upgraded along with coordinate_data.json, re-verify whether the example coordinates still apply; when versions do not match, do not directly reuse the examples.
