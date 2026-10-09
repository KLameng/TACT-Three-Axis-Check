# Contributing Guide: Community ratify and Real-Case Back-Fill

Correctness validation of this toolkit follows the route of "completed spontaneously by the community after open-sourcing" (no centralized validation requiring human annotators). The core mechanism is **ratify**: gradually validating/revising coordinates and criteria using real incident cases. This document explains how to submit real cases, how ratify is decided, and how data is back-filled.

## 1. Submitting Real Cases (how to submit)

Any actually occurred AI system failure/error/anomaly may be submitted as a candidate case. **A real case = non-synthetic, traceable record of phenomena from actual running/measured environments.**

### Submission process
1. Submit via an Issue using the template below; if sensitive/private content is involved, be sure to de-identify it—**describe only the phenomenon, with no real data**.
2. Maintainers/the community first perform a **preliminary determination**: run through the Three-Step Matching Method to judge whether it is a mechanism classifiable by this toolkit.
3. Once the threshold is met, it enters the ratify process.

### Submission template (Issue)
```markdown
## Real Case
- **Phenomenon**: what happened (objective description, no real data/credentials)
- **Environment**: system type (single model / agent / RAG / multi-agent), trigger conditions
- **Observation**: actual model/system output vs expectation
- **Reproducible**: yes/no, reproduction steps (if any)
- **Self-assigned coordinates** (optional): L/M/P self-assessment + rationale
- **Confidentiality statement**: de-identified, no real data
```

## 2. How ratify is decided (core rules)

### Coordinate ratify (graduate to formal status)
- **Prediction slot → formal code**: when **two mutually independent real cases** both fall under this mechanism, the graduation threshold is met (per the "evolution rule").
- **M9 Spontaneous Collaboration**: the parent coordinate has been admitted; its child coordinates await ratify by real cases; they graduate to formal status on the same threshold of two mutually independent real cases.
- **Conditions against ratify**: synthetic cases, different variants of the same incident (not counted as "mutually independent"), and model annotations suspected of sharing training bias.

### golden revision
- When a real case conflicts with the existing golden, the real case prevails: **revise the golden and record a changelog entry**; do not freeze.
- After revision, re-run the calibration set (regression mode) to confirm no silent drift has been introduced.

### Meta-tag / cross-map back-fill
- When real cases accumulate to `E1` (1 case), it may be marked `evidence_strength=E1`; `E2` (2 cases) / `E3` (≥3 cases) are upgraded step by step. **Do not overstate the case count.**
- Meta-tags are completed along the 7 dimensions of `schema`; when no cases exist, use `E0/E1` and mark as "pending verification".
- Of the cross-map mappings, only `verified` (case-supported) may be cited; citations of `hypothesis` must be labeled "pending verification".

## 3. kappa re-test (how to re-measure agreement)

After each revision / data version upgrade, run the calibration set to recompute the L/M/P three-axis κ and hit rate, and compare against the baseline (see the evolution table in `docs/TACT-kappa-full-history-analysis.md`):

- **Regression mode**: confirm that the changes introduced no silent drift (consistent with or better than the baseline).
- **New annotators**: the community may self-select models/humans to run the same calibration set and submit κ results; after accumulating multiple samples, the current 5 large-model annotators may be replaced/expanded.

## 4. Back-fill boundaries (what not to do)

- **Do not fabricate codes**: coordinate additions/deletions follow only the evolution rule of "two mutually independent real cases + structural validation"; do not add child coordinates on your own.
- **Do not touch the coordinate semantics of coordinate_data.json**: criterion revisions go through SKILL.md; coordinate semantics remain stable.
- **synthetic is not used for ratify**: the calibration set measures only discrimination agreement; it is not regarded as a real incident and is not used as evidence for coordinate ratify.

## 5. Version lock discipline

Before modifying the toolkit, read `guard/README.md` first and follow the standard process: `guard/unlock.sh` → edit → update `guard/MANIFEST.json` → `git commit` → `guard/lock.sh` → `guard/verify.sh`. When controlled files (SKILL.md / calibration_cases.json / coordinate_data.json) are externally rolled back, restore them with `git restore` + `verify.sh` and raise an alert.
