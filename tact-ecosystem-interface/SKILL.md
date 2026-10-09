---
name: tact-ecosystem-interface
description: TACT three-axis coordinate method's ecosystem-interface asset pack: crosswalks (TACT↔OWASP/NIST/ATLAS/EU AI Act/OWASP Agentic 2026 bidirectional mappings), EU AI Act obligation mappings, and a meta-tag grading layer. Use when you need to translate a TACT coordinate into an industry-framework entry, look up EU legal obligation clauses, or add severity/detectability/mirror and other meta-tags to a coordinate. The coordinate system is governed by tact-three-axis-check (117 coordinates).
cross_skill_refs:
  - references/coordinate_data.json
---

# TACT Ecosystem Interface (tact-ecosystem-interface)

## Positioning

This skill is not an independent classification engine; it is the **external interface asset pack** of tact-three-axis-check (the gate-passing engine). Coordinate codes (e.g., M2-2, M6-6) are governed by tact-three-axis-check's `references/coordinate_data.json` — note that this file is located in the **sibling skill directory `tact-three-axis-check/references/coordinate_data.json`**, not under this skill's own `references`; the criteria and gate-passing flow also live in the main skill, and this skill does not duplicate them.

## Asset list

| File | Content | When to read |
|---|---|---|
| `references/crosswalk_four_frameworks.json` | TACT↔five-framework bidirectional mapping (OWASP LLM / NIST / EU AI Act / ATLAS / OWASP Agentic 2026; forward 48 items + reverse 32 items) | when a coordinate is hit and you need an industry name/framework reference |
| `references/eu_ai_act_obligations.json` | coordinate→EU AI Act obligation clause + landing action (forward 14 items + reverse self-check + compliance checklist) | for EU high-risk scenarios / compliance self-check |
| `references/tact_meta_tags.json` | 7-dimension meta-tags (severity / detectability / attack surface / mirror / status / semantic domain / evidence strength) | when you need to grade, rank, cross-check mirrors, or annotate a coordinate |
| `references/agentic_coverage_gap.md` | OWASP Agentic 2026 coverage-gap checklist (coverage status + M9 pending-ratify gap + community-collaboration entry) | for Agent-app risk mapping / gap check / community case solicitation |

## Usage flow (after passing the gates)

1. **Look up a crosswalk**: hit a coordinate → use the crosswalk forward table to find an industry entry (industry→coordinate) or the reverse table to find a framework reference (coordinate→industry name). Before external citation, check that entry's `status` field: `verified` may be cited, `hypothesis` must be labeled "pending verification". **Coordinate not found → label "no mapping yet", do not force a correspondence**.
2. **Look up obligations**: for EU deployment or medical high-risk scenarios → read `eu_ai_act_obligations.json`: coordinate→clause→landing action; a coordinate hit with `severity=S1` automatically enters the Art. 73 serious-incident reporting flow (see the meta-tags).
3. **Fill in meta-tags**: `tact_meta_tags.json` is split into 5 zones — `schema` (7-dimension definitions) / `mirrors` (18 mirror pairs) / `status_annotations` (prediction slots and prediction families) / `domain_symbol` (symbol-domain 8 coordinates) / `examples` (only 10 high-frequency coordinates fully annotated, **not exhaustive**). When adding meta-tags to an un-annotated coordinate, fill it per the schema's 7 dimensions; when evidence is insufficient, use `evidence_strength=E0/E1` and mark "pending verification", and do not overstate case counts. **If that coordinate has no complete tags → label "meta-tag pending", do not default to a missing value**.

## Discipline (guardrails)

- **Version binding**: the three tables are bound to TACT v2.7.8 and the framework versions (OWASP Top 10 for LLM 2025 / NIST AI 600-1 / EU AI Act 2024/1689 / ATLAS 2026 / OWASP Agentic Applications 2026). After a master-data upgrade, the mappings must be re-verified before reuse; when versions do not match, do not directly cite the mappings.
- **Data structure**: in `crosswalk_four_frameworks.json`, `forward` is a dict grouped by framework (OWASP/NIST/EU_AI_ACT/ATLAS/AGENTIC), and `reverse` is a flat list; the two shapes within the same file are an existing design, so handle each by its shape and do not assume homogeneity.
- **Verification status**: each mapping carries a `status` field: `verified` = supported by cases (citable); `hypothesis` = pending-verification hypothesis (must be labeled "pending verification" when cited); `verified_refused` = correctly refused by the governance domain (e.g., EU05/EU08/AT07 — that entry has no TACT coordinate; declare "governance domain" when citing, and do not treat it as a coordinate hit). Neither hypothesis nor verified_refused is treated as a verified fact.
- **Example-level annotation**: `tact_meta_tags.json` fully annotates only 10 high-frequency coordinates; the other coordinates' meta-tags are `null` pending. Before use, first check whether that coordinate has complete meta-tags; do not assume full coverage.
- **No new coordinates**: this skill only provides interfaces and annotations; it adds no L/M/P child coordinate. Coordinate addition/removal follows the evolution rule of tact-three-axis-check (two mutually unrelated real cases + structural validation).
- **Mapping is not a conclusion**: a crosswalk mapping is a "criterion-carrying translation hypothesis" and an obligation mapping is a "trigger clue" — a coordinate hit does not equal a legal obligation violation; judge against the performance baseline and the clause original text.
