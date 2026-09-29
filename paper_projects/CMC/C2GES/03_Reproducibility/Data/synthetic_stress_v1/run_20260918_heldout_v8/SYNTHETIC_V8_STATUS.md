# Held-out synthetic v8 — 2026-09-18

- Evidence class: fictional stress fixtures only
- Confirmatory claims allowed: false
- Human/expert annotation: none
- Codex critic: not run for this version (deterministic gates only)

## Dataset

- 8 reports, 4 series, unused themes relative to network-calibrated v6
- Seed 20260918
- Deterministic distribution gates: PASS (duplicate rate 0.0011)
- Factorial: 208/208 cells PASS

## Factorial means (ROUGE-L F1)

| Condition | 110 words | 260 words |
|---|---:|---:|
| Full (AB-5) | 0.3886 | 0.3481 |
| No-path (AB-6) | 0.3750 | 0.3269 |
| G-T | 0.3750 | 0.3269 |
| G-U | 0.3002 | 0.2346 |

Full-minus-no-path series-equal means: +0.0136 (110), +0.0212 (260); Holm-adjusted exact values 1.0.

## Interpretation

References are extractive reconstructions of the same typed role chain used to build the fixtures. A positive mean on this set diagnoses endpoint alignment on fictional gold, not unseen real-report validity, construct validity, or operational benefit.
