# TACT Novice Verification Quality Gate (Novice Verification Gate)

> Version: v1.0.0 · Bound to: coordinate_data.json v2.7.8 · Linked with: `verification-chain.md` (evidence chain)
> Purpose: to set an **automatic, human-annotation-free** quality gate on "whether a verification path/evidence chain is re-verifiable enough" — drawing on FaithLens' idea of using a novice-level model to judge "whether the explanation lets a newcomer reach the correct conclusion".
> This file is a **mechanism specification**, new; it does not change the coordinate semantics of coordinate_data.json and introduces no verification that requires human annotators.

## 1. Why (drawing on FaithLens' novice judgment)

FaithLens' key design: after the generative model outputs an **explainable evidence chain**, a **novice-level model** (Llama-3.1-8B-Instruct) reproduces the conclusion using only the explanation — if the novice can reach the correct prediction from the explanation, the explanation quality is adequate; otherwise the explanation is insufficient. This is "using a newcomer to test explanation quality" and requires no human annotation at all.

TACT's corresponding pain point: no matter how detailed the verification path (third segment of pairs) is written, it is hard to judge "whether it is enough for someone who has not read the criterion to reproduce the correct coordinate". Measuring this by the novice reproduction rate is the most direct, and automatable (model self-assessment) way — consistent with the project's boundary of "doing only the automation parts that do not depend on human annotation".

## 2. Quality-gate definition

**Quality gate**: hand (coordinate + evidence chain E1–E3) to a **novice agent that has not seen that coordinate's criterion**, give only the judgment anchor, not the original desc, and see whether it can derive the coordinate/conclusion consistent with the golden. **Pass when the novice reproduction hit rate ≥ threshold**; otherwise the evidence chain goes back for reinforcement.

- **Object**: the verification path of any coordinate in `coordinate_data.json` (or the evidence chain in `verification-chain.md`);
- **Criterion**: compare the coordinate reproduced by the novice from the evidence chain with the golden (calibration_cases.json);
- **Default threshold recommendation**: **≥ 90%** (on the same order as FaithLens' explainability assessment standard; a project may raise it per scenario, and it is not recommended to go below 85%).

## 3. Quality-gate protocol (one-shot judgment)

1. **Select samples**: take a set of verification paths/evidence chains for a coordinate + the corresponding discrimination cases (preferably from `calibration_cases.json`; synthetic may also be used here, since only consistency is tested, not empirical validity).
2. **Construct novice input**: give only "phenomenon description + evidence-chain E1–E3 (where to check / what to check / hit criterion)" and "the candidate-code list of the L/M/P axis that coordinate belongs to"; **do not** give the coordinate's desc/pairs original text, and do not give the golden.
3. **Run the novice agent**: use a model that has not touched that criterion in this task (any LLM or a local small model will do) to run it independently and output the coordinate code it judges as hit.
4. **Compare and score**: for each sample, if the novice output's coordinate code is consistent with the golden, score 1 (an M/P dual listing counts as "hit means consistent"; an axis left empty in the golden is skipped).
5. **Judge**: hit rate = consistent samples / decidable samples. ≥ threshold → PASS; otherwise → locate the failed samples, go back to reinforce the E3 criterion anchor or the E4 re-verification path, and re-run.

## 4. Linking with the evidence chain

- E3 (hit-criterion anchor) of `verification-chain.md` is the core input for the novice judgment — the more decidable the anchor ("proportion ≥ X%", "a certain event sequence appears"), the easier the novice reproduces;
- when the quality gate FAILs, diagnose by the four evidence-chain elements: **E1 not locatable / E2 not reproducible / E3 criterion vague** → reinforce the corresponding element and re-run until PASS;
- after the quality gate passes, that evidence chain can be used as a later ratify candidate's "re-verifiable path" (but synthetic is still not used for ratify; only real cases are — see CONTRIBUTING.md).

## 5. Script skeleton (landable automation, for implementation reference)

The pseudocode below describes a minimal runnable quality gate; for implementation, plug in any OpenAI-compatible LLM interface; it does not depend on human annotation.

```
For the target coordinate in coordinate_data.json:
  take the third-segment verification path of each of its pairs → assemble as evidence_chain
  take the cases referencing that coordinate in calibration_cases.json (synthetic is fine) as the sample set
  For each sample:
    input = "Phenomenon: {phenomenon}\nCandidate codes: {all codes of this axis}\nJudge the hit code using only the following evidence chain:\n{evidence_chain}"
    output = novice_llm(input)   # any model that has not seen the criterion
    score += (normalize(novice_output) == golden code of that axis) ? 1 : 0
  hit_rate = score / len(samples)
  if hit_rate >= 0.90: PASS; else: list failed samples, prompt to reinforce E3/E4, re-run
```

> Note: the novice model can reuse any local/online LLM; the quality gate is **model self-assessment**, with no human annotator, consistent with the project's "validation left to community/automation" boundary.

## 6. Applicable scenarios

1. **Calibration-set maintenance**: after adding/revising synthetic cases, use the quality gate to confirm the verification path corresponding to their golden is "re-verifiable enough", to prevent discrimination ambiguity;
2. **SKILL.md wording convergence**: when a coordinate's hit rate stays low, use the quality gate to locate whether it is "evidence chain not re-verifiable" or "SKILL guidance problem";
3. **Gate before ratify**: before a real case enters ratify, first confirm the evidence chain of its corresponding coordinate can be reproduced by a novice (only real cases can be ratified; synthetic is not used for ratify).

## 7. Discipline and boundaries

- **No code fabrication**: the quality gate only judges evidence-chain quality; it adds/modifies no coordinate code;
- **No dependence on human annotation**: the whole process is model self-assessment/automation, with no human verifier; κ/independent back-testing is left to the community (CONTRIBUTING.md);
- **No coordinate-semantics change**: the quality gate does not rewrite coordinate_data criteria; in conflict with the original text, the original prevails;
- **Threshold is a recommendation, not mandatory**: default ≥ 90%, may be raised per project scenario; a low hit rate does not block skill use (same convention as the calibration set; it is a diagnostic signal, not a gate).
