# TACT Three-Axis Coordinate Check

A three-axis coordinate classification method for localizing errors, failures, and anomalies of AI systems (large models / agents).

**L-axis** (at which layer it fails) · **M-axis** (how it fails) · **P-axis** (which facet is broken)

> **Criterion blueprint declaration**: the criteria and coordinates in this repository have not yet been independently verified by human annotators; they are a "criterion-carrying classification hypothesis", and correctness is to be confirmed item by item by community **ratify** (submitting real cases + structural validation). Users citing a coordinate should verify it themselves and must not treat it as a verified fact.

## Repository structure

```
├── LICENSE                          # CC BY 4.0 open-source license
├── tact-three-axis-check/           # main criterion engine
│   ├── SKILL.md                     # gate-passing flow and criteria (entry; read this first)
│   ├── references/                  # coordinate base coordinate_data.json + calibration set calibration_cases.json
│   ├── guard/                       # controlled-file integrity-check scripts (lock/unlock/watch/verify)
│   └── docs/                        # full history summary and analysis of the kappa consistency test
└── tact-ecosystem-interface/        # ecosystem-interface asset pack
    └── references/                  # crosswalks / EU AI Act obligations / meta-tags / Agentic coverage gap
```

## Quick start

1. Start from `tact-three-axis-check/SKILL.md` and do an L/M/P localization of the error phenomenon per the gate-passing flow.
2. Coordinate definitions are governed by `tact-three-axis-check/references/coordinate_data.json` (TACT v2.7.8, 117 child coordinates).
3. For industry-framework mappings / EU obligations / Agentic coverage-gap checks, use `tact-ecosystem-interface/`.

## Calibration and consistency

- Calibration baseline: `calibration_cases.json` (28 cases); run calibration mode to compute the three-axis hit rate as a diagnostic signal, **not a pass/fail gate**.
- Consistency history: `docs/TACT-kappa-full-history-analysis.md` (5 domestic models, 12 synthetic, Fleiss κ, final L κ 0.945 / hit 98.2%).
- Note: the kappa verification currently relies on model self-assessment; **independent human verification is left to spontaneous community ratify after open-sourcing**.

## Contributing

Real cases (de-identified) are welcome to help ratify coordinates; key solicitations:
- Agentic application incidents / anomaly records (reinforcing ASI05 / ASI07 coverage)
- Spontaneous boundary-crossing (M9 pending ratify) cases; accumulating **2 mutually unrelated real cases** triggers review

See the CONTRIBUTING.md in each subdirectory for details.

## License and contact

- License: Creative Commons Attribution 4.0 (CC BY 4.0), attribution **KLameng**. See `LICENSE`.
- Maintainer: **KLameng** · Contact email: **911712412@qq.com** (feedback / case submission / collaboration)

---

*Copyright (c) 2026 KLameng <911712412@qq.com> · Released under CC BY 4.0.*
