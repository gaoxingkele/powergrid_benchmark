# Framework visual QA

**Review mode:** manual inspection of `qa/page_scale_preview.png` at original resolution after placement of all three figures at approximate MDPI single-column text width. Vector PDF/SVG and raster exports were generated from the same source.

## Decision

**PASS after one remediation cycle.** The first preview showed clipped/overlapping long labels. The generator was revised to use four-stage pipelines, shorter labels, explicit line breaks, and larger effective text. The regenerated preview has no clipped node label, no line crossing through text, and legible internal wording at page scale.

| Figure | Scientific-content check | Page-scale check | Decision |
|---|---|---|---|
| `ma_r1_f01_executed_pipeline` | one generation, parse/read-only validation/execution, terminal ledger; explicitly says no ranking/repair | labels and bottom boundary legible | PASS |
| `ma_r1_f02_factorial_design` | four cells; bundled context package; two backbones each one 180×4 run; 1440 total | cell labels and backbone counts legible | PASS |
| `ma_r1_f03_external_evidence_gate` | visible candidates cannot become sealed; separates human-reviewed unsealed and new confirmatory evidence | gates and evidence labels legible | PASS |

## Accessibility and export checks

- Information is encoded by position and text, not color alone.
- Dark outlines and high-contrast text remain understandable in grayscale.
- No decorative hatch or low-contrast background is used.
- SVG retains editable text; PDF uses TrueType text; PNG is exported at 450 dpi.
- The phrase “models × repetitions” is absent. The actual design is “Qwen-7B: one 180×4 run; Granite-8B: one 180×4 run.”
- No executed repair loop is drawn. A red boundary statement explicitly prevents misreading the old pilot as part of the canonical pipeline.

The page-scale preview is an authoring aid, not a claim that MDPI production rendering has been checked; the final assembled manuscript must be rebuilt and inspected again after insertion.

