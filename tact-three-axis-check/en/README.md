# TACT Three-Axis Coordinate Check (tact-three-axis-check)

Locates failures, errors, and anomalous phenomena of AI systems to a unique coordinate within a closed coordinate space (L 4 layers × M 9 families × P 8 tiers = 288 cells, 117 fine-grained child coordinates), and provides an executable verification path. It follows the "Three-Step Matching Method": the L-axis may be single- or multi-selected based on the problem; the M/P axes pass through the gates in sequence, and the method outputs a structured conclusion containing the three-axis coordinate names, hit meaning, possible manifestations, occurrence location, and verification path.

## Positioning (please read this section first)

**This toolkit is a "criterion blueprint + calibration baseline", not a finished taxonomy that has been "verified as reliable".**

Its value lies in converging the judgment of "which category of error an AI failure belongs to" from "loose terminology matching" into a **decidable operational question** (sharp criterion (decisive) + reverse constraint + anti-overfitting anchor). This set of criteria has been refined through 9 rounds of inter-model consistency testing, but **the "discriminative correctness" of the criteria still awaits validation by real cases**.

### Four open-source statements (must be followed when citing this toolkit externally)

1. **Positioning**: a criterion blueprint + calibration baseline, **not "verified as reliable"**. Before citing this toolkit as the basis for a conclusion, you must first state its validation status.
2. **Validation scope**: the inter-model consistency κ test across the L/M/P axes **uses only different large models as annotators (5 independent domestic models)**, **with no human review**; the κ's "discriminative correctness" (relative to real mechanisms) has not yet been independently verified by humans or real cases, **awaiting spontaneous community ratify after open-sourcing**. The full testing history and discrepancy analysis are in [`docs/TACT-kappa全历程汇总与分析.md`](docs/TACT-kappa全历程汇总与分析.md).
3. **synthetic is not empirical evidence**: the 21 samples in `references/calibration_cases.json` **are all synthetic criterion samples**, for consistency discrimination testing only; **they are not regarded as real incident records, must not be cited externally, and must not be used as evidence for coordinate ratify**.
4. **Coverage status (meta-tags / cross-map mapping)**: only **10/117** coordinates have complete meta-tag annotations; the rest are `null`, pending completion. Most cross-map mappings are in `hypothesis` (pending verification) status (only `verified` may be cited; citations of `hypothesis` must be labeled "pending verification"). Before use, check the annotation status of the target coordinate/mapping first; **do not assume everything is fully annotated**.

## Quick Start

1. Read the "Three-Step Matching Method" in `SKILL.md` (including Step 0 the Pre-Exclusion Gate, L-axis source determination, and M/P gate evaluation).
2. Coordinate meanings, criteria, manifestations, locations, and verification paths are all governed by `references/coordinate_data.json` (do not fabricate codes from memory).
3. After landing a coordinate, if you need industry/framework references, EU obligations, or meta-tags, use the sibling skill `tact-ecosystem-interface`.

## Toolkit Structure

| Path | Contents | Notes |
|---|---|---|
| `SKILL.md` | Criterion guidance and execution flow (v1.1.1) | Core file |
| `references/coordinate_data.json` | Coordinate base (v2.7.8, 117 child coordinates) | **Never modified**; coordinate semantics do not change with criterion revisions |
| `references/calibration_cases.json` | Calibration baseline (v1.1.1, 21 entries) | Used for calibration / regression mode |
| `docs/TACT-kappa全历程汇总与分析.md` | Full history and analysis method of the kappa test | Includes an honest statement of validation scope |
| `guard/` | Version lock and integrity protection (MANIFEST + verify/lock/unlock/watch) | Prevents controlled files from being externally rolled back / tampered with |
| `CONTRIBUTING.md` | Entry point for community ratify / real-case submission / kappa re-test | Path for correctness validation |

## Version

- coordinate_data.json **v2.7.8** (coordinate base, never modified)
- calibration_cases.json **v1.1.1** (calibration baseline, bound to v2.7.8)
- SKILL.md **v1.1.1** (criterion guidance)

Version maintenance discipline: **only modify the SKILL.md criterion guidance and the calibration golden; do not change the coordinate semantics in coordinate_data.json**; after a revision, follow the version lock process in `guard/` (see `guard/README.md` for details).

## Community Participation

For correctness validation, coordinate ratify, meta-tag completion, and cross-map verification—see [`CONTRIBUTING.md`](CONTRIBUTING.md).
