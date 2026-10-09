# TACT Application Case: Three-Axis Localization and Repair of Variant-Classification Discrepancies

> Case nature: a real application demonstration of the TACT three-axis coordinate method (L-axis = at which layer it fails / M-axis = how it fails / P-axis = which facet is broken) in a genetic-variant ACMG/AMP classification scenario.
> Note: this case is a technical post-mortem. The variants involved are all test variants that can be retrieved from public databases (ClinVar / PubMed); they are **not any individual's clinical data**; the classification conclusions are for reference only and do not constitute a clinical diagnosis.

---

## 1. Background and goal

Use a "rule-driven, process-frozen, data-traceable" single-variant classification skill suite to run ACMG/AMP automatic classification on **42 test variants**, and after comparing against manual classification, **30 discrepancy points** arose. Each evidence code was then verified against real data sources one by one, and the TACT three-axis coordinate method was used to make a "mechanism-level" localization of the failures of this classification system.

Hard constraints of the skill-suite design:

1. **Rule source locked**: the operating steps of every evidence code must follow the original text of the *Guideline Interpretation* and the *Variant-Interpretation Query Paths*; no adaptation or extrapolation is allowed;
2. **Each evidence code is an independent skill**: PVS1, PM2, PM3, PP4, etc., each has its own skill file; paired ones are merged;
3. **Scheduler-mandated flow**: classification must go through "① delimit the usable evidence codes by variant type → ② invoke the sub-skills one by one to judge → ③ finish with mutual-exclusion resolution + final class"; no step may be skipped before output;
4. **Output ironclad rule**: every classification must give three points — evidence code + usage level, supporting data + classification rule, and the actual query path (database/PMID); write "not found" if not found.

Goal: verify whether this skill suite can turn ACMG classification from "AI's craft based on experience" into "AI's assembly line".

## 2. Verification method

Each discrepancy point is **evidenced separately, without reusing any example data inside the skill**:

| Data source | Use |
|---|---|
| ClinVar (eutils / page) | variant ID, clinical significance, review star level, submitter count |
| PubMed eutils | verify trans / homozygous / compound-heterozygous and phasing status abstract by abstract |
| GeneBe api-public (basic annotation only) | REVEL / AlphaMissense / population frequency |
| Ensembl VEP | NMD position, exon number |

Judgment convention: **confirmed** = the evidence code holds and our side indeed missed/misused it; **doubtful** = insufficient evidence, to be decided; **refuted** = that evidence code does not hold (with which side noted).

## 3. Verification conclusions (30 discrepancy points)

### 3.1 Distribution of judgments

| Judgment | Count |
|---|---|
| Answer right / our side wrong | ~17 |
| Partially confirmed / partially refuted | ~5 |
| Doubtful, to be decided | ~5 |
| Answer code refuted or strength over-graded | ~6 |

### 3.2 Key signals clustered by evidence code

1. **PM3 (trans scoring) — the answer most often holds; our biggest gap.** Involves 15+ discrepancies; our side either missed detection (insufficient depth in trans-case retrieval) or was conservative in strength (sufficient evidence yet assigned a lower tier). This is the first source of "missed codes".
2. **PP4 (phenotype specificity) — the code our side over-used most, 9 misuses.** Concentrated in genetically heterogeneous diseases where "phenotype-similar" was taken as "phenotype-specific"; the most typical one pushed LP wrongly to P because of 1 extra PP4 point.
3. **PM5 (same-residue amino acid) — the answer systematically over-graded strength.** Several places gave "Strong" although the same-site evidence lacked "2 definitive P"; our side's non-use of PM5 actually withstood scrutiny.
4. **PP3 (REVEL computational prediction) — the answer's data retrieval is generally correct; our side missed it in several places.** Several places had REVEL scores clearly falling into a tier, yet the whole PP3 was missing or downgraded because of "not found".
5. **PVS1 (LOF/splicing) — both sides have their own right and wrong.** The answer side wrongly graded some "reduced-penetrance-type" in-frame splicing as NMD-LOF at full tier; our side wrongly downgraded some nonsense variants with expected NMD, and also mis-hung some RNA-empirical LOF under PS3 (mutually exclusive with PVS1).
6. **PS3 / PS4 / PS2 (functional / frequency / de novo) — the answer is basically reliable, with an occasional code lacking empirical support; our side wrongly treated enzyme-activity associations in a carrier cohort as that variant's functional experiment.**

### 3.3 Variants needing classification correction (de-identified: public variant names kept, case details removed)

| Direction | Variant (public HGVS / ClinVar) |
|---|---|
| Our side needs up-grading | OCA2, F7, HEXB, SMPD1, ETFDH, GALC, SLC22A5, one each (VUS → LP/P range) |
| Our side needs down-grading | PKHD1, one (P → LP, PP4 refuted) |
| Answer side needs down-grading | CFTR, NSDHL, CCDC88C (evidence code refuted or classification over-aggressive) |

> Attachment: gene-variant naming-alignment corrections found during verification (F7, GALC, SLC12A3, SMPD1, etc., have alternate transcript numbering / propeptide-number offset); see the verification record in the same directory under `docs/` of the repo.

## 4. TACT three-axis localization

The verification report answers "who is right and who is wrong"; TACT answers the more fundamental question: **why does the system fail systematically on certain codes?**

### 4.1 Not a single-point fault, but a stacking of three kinds of failure

| TACT coordinate | Meaning | Corresponding failure category |
|---|---|---|
| **L1 · Internal to Model** | deleting external input, the AI errs in applying the criterion within a single turn | PP4 misuse, PM3 strength conservative, PS3 misuse, PVS1 tier, classification orientation |
| **L2 · Input/Output Interface** | the same variant "does not match symbolically" across different naming systems | gene/variant naming-alignment mismatch (alternate transcript numbering, propeptide-number offset) |
| **L3 · Reasoning-Collaboration Chain** | retrieval→classification linkage missing evidence | PM3 case missed, REVEL missed, ClinVar mis-read |

### 4.2 Failure modes (M-axis) and broken facets (P-axis)

- **M-axis**: the core is the stacking of **M1 insufficient information (missing evidence) ＋ M3 reasoning failure (criterion application)**; with M2 information corruption (naming-mapping error) also involved.
- **P-axis**: the broken facet falls on **P1 factual distortion** (the classification conclusion does not match the true pathogenicity classification).

### 4.3 Failure class → coordinate mapping

| Failure class | L | M | P |
|---|---|---|---|
| Retrieval/data-fetching (trans-case missed, REVEL missed, ClinVar mis-read) | L3 | M1 | P1 |
| Gene/variant naming alignment | L2 | M2 | P1-1 |
| Judgment scale (PP4 misuse, PM3 strength, PS3 misuse, PVS1 tier, weaker-stand-in-for-stronger) | L1 | M3 | P1 |
| Classification orientation (total score/threshold) | L1 | M3 | P1 |

### 4.4 Counter-check trail (why not a different coordinate)

- **Why is missed detection not M2 information corruption?** — missed detection is "did not fetch", not "fetched something wrong"; in essence it is insufficient **information (M1)**; naming-mapping error is **corruption (M2)**.
- **Why is judgment scale not M5 goal drift?** — the criterion is not driven by being "downgraded/traded off" (no goal driving it); it is a wrong inference scale when applying the criterion, fitting M3 better.
- **Why not M6 external adversarial action / M9 spontaneous collaboration?** — no attacker, no autonomous privilege escalation, no multi-agent spontaneous collaboration; it is a mechanism-face failure of the classification system itself; all excluded.
- **Why does P fall on P1 rather than P8/P7?** — what is broken is the accuracy of the classification conclusion (factual facet); no safety/fairness is involved.

This set of exclusions prevents the most dangerous misattribution: **misjudging a fixable process problem as "the data/environment is not good enough", and thereby giving up the fix.**

## 5. Executable repair checklist (by TACT priority)

| Failure class | Coordinate | Corresponding skill adjustment |
|---|---|---|
| Trans-case missed | L3/M1 | add "four-segment exhaustive retrieval" to trans retrieval: multiple keyword groups + allele search + per-abstract scoring + PMID re-check |
| REVEL missed | L3/M1 | add a fallback channel for computational-prediction retrieval; a miss must not silently discard it |
| ClinVar mis-read | L3/M1 | read submitter-level detail (star level, commentary); down-weight low-star and note it |
| Naming alignment | L2/M2 | add a "variant identity normalization" pre-step in the scheduler: MANE + variant ID + rsID; use synonym groups for retrieval |
| PP4 misuse | L1/M3 | add a "specificity counter-proof check": multi-gene heterogeneous → not usable; large gene with many benign variants → not usable; single-gene specific → usable |
| PM3 strength conservative | L1/M3 | add a "grade-high-over-grade-low" re-check node + scale-calibration precedent |
| PS3 misuse | L1/M3 | add an "evidence-nature verification": whether it targets this specific variant, whether there are positive/negative controls |
| PVS1 tier | L1/M3 | add NMD exon-rank re-check; non-canonical ±1/2 in splice regions must not be directly PVS1 |
| Classification orientation | L1/M3 | add a dual-convention re-check at the finishing layer + threshold-boundary annotation |

**Repair chain: 30 discrepancies → 3 mechanism clusters → 9 skill adjustments.** The adjustments do not change the usage standard, threshold, level, or mutual-exclusion rules of any evidence code; they only add process steps.

## 6. Conclusion

1. **The bottleneck of AI doing ACMG classification is not rules, but the process of "feeding evidence" and "applying criteria"** — consistent with the conclusions of the verification report and the TACT localization;
2. **Manual classification is not the gold standard** — the answer side also had evidence codes refuted, so "aligning to manual" should not be the ultimate goal; "aligning to true pathogenicity" is;
3. **TACT's value was validated by this real test**: it converged scattered discrepancies into "3 mechanism clusters + 9 executable adjustments", and used exclusion to stop misattribution.

**An open question left for peers**: if the classification system should "align to true pathogenicity" rather than "align to manual", who should define the gold standard? A possible direction is the **ClinGen VCEP expert-review mechanism + functional / segregation / frequency triangulation of evidence** — this is also the direction this skill suite will align to in the future.

## 7. De-identification and disclaimer

- This document has removed all identifiable information that could point to an individual, family, population, region, or institution;
- What is retained is only public scientific facts: gene names, HGVS variant names, ClinVar / PubMed citations;
- The classification and localization conclusions in the text are a technical post-mortem, **for reference only, and do not constitute a clinical diagnosis or medical advice**.

---

*Methods involved: single-variant classification skill suite · TACT three-axis coordinate method (coordinate_data v2.7.8, calibration set v1.2.0). Verification data sources: ClinVar, PubMed, GeneBe (basic annotation), Ensembl VEP.*
