# Granite 3.3 8B Formal Run - Independent Audit

**Decision: PASS - eligible for bounded two-backbone sensitivity analysis.**

## Integrity boundary

- Granite input: `paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\granite_formal\granite33_8b_q4km_seed20260805_clean1`.
- Qwen input: audited canonical rows only, SHA-256 `df7ef2bb6990fda50d1e0ba69a1bdcaeab08ffc47c01423afe750044333f027f`.
- The contaminated Qwen run directory was not read.
- Checks passed: 35/35. Exactly 720 keys, 720 unique server generation tasks, no resume, zero provider/parse/scoring errors or retries, all SQL read-only, and 720/720 direct SQLite execution/shape verdicts reproduced.
- Granite model file bytes/SHA, local manifest, official revision/license identity, prompt set, configuration, data and code hashes match the freeze.

## Granite recomputed cells

| Cell | Execution | Shape |
|---|---:|---:|
| F00_Full_NoShape | 77/180 = 0.4278 | 82/180 = 0.4556 |
| F01_Full_WithShape | 100/180 = 0.5556 | 158/180 = 0.8778 |
| F10_Compact_NoShape | 74/180 = 0.4111 | 79/180 = 0.4389 |
| F11_Compact_WithShape | 108/180 = 0.6000 | 166/180 = 0.9222 |

## Granite factorial effects

20,000 paired bootstrap draws over the same 70 normalized gold-SQL template clusters.

| Metric | Effect | Estimate | 95% CI |
|---|---|---:|---|
| correct_int | context_compact_main | +0.0139 | [-0.0574, +0.0801] |
| correct_int | shape_hint_main | +0.1583 | [-0.0200, +0.3665] |
| correct_int | interaction | +0.0611 | [-0.0524, +0.2000] |
| shape_int | context_compact_main | +0.0139 | [-0.0549, +0.0867] |
| shape_int | shape_hint_main | +0.4528 | [+0.2710, +0.6399] |
| shape_int | interaction | +0.0611 | [-0.0741, +0.1980] |

Exact McNemar tests and Holm-adjusted p-values for the eight Granite factorial edges are in `granite_registered_contrasts.csv`.

## Paired Granite-minus-Qwen cell sensitivity

The two backbones are not pooled as independent samples; every contrast is paired by the same 180 questions and template clusters.

| Cell | Metric | Qwen | Granite | Difference | 95% CI | Holm p |
|---|---|---:|---:|---:|---|---:|
| F00_Full_NoShape | correct_int | 0.4222 | 0.4278 | +0.0056 | [-0.0316, +0.0470] | 1 |
| F00_Full_NoShape | shape_int | 0.5000 | 0.4556 | -0.0444 | [-0.2222, +0.1421] | 1 |
| F01_Full_WithShape | correct_int | 0.7167 | 0.5556 | -0.1611 | [-0.2975, -0.0484] | 3.89888e-05 |
| F01_Full_WithShape | shape_int | 0.9667 | 0.8778 | -0.0889 | [-0.2249, +0.0125] | 0.0108072 |
| F10_Compact_NoShape | correct_int | 0.4333 | 0.4111 | -0.0222 | [-0.0800, +0.0239] | 1 |
| F10_Compact_NoShape | shape_int | 0.4389 | 0.4389 | +0.0000 | [-0.0804, +0.0885] | 1 |
| F11_Compact_WithShape | correct_int | 0.6000 | 0.6000 | +0.0000 | [-0.1019, +0.1095] | 1 |
| F11_Compact_WithShape | shape_int | 0.9611 | 0.9222 | -0.0389 | [-0.0909, +0.0055] | 0.710815 |

## Backbone-by-factor sensitivity

| Metric | Backbone interaction | Qwen effect | Granite effect | Granite-Qwen | 95% CI |
|---|---|---:|---:|---:|---|
| correct_int | backbone_x_context_compact_main | -0.0528 | +0.0139 | +0.0667 | [-0.0375, +0.1801] |
| correct_int | backbone_x_shape_hint_main | +0.2306 | +0.1583 | -0.0722 | [-0.1230, -0.0272] |
| correct_int | backbone_x_interaction | -0.1278 | +0.0611 | +0.1889 | [+0.0067, +0.4310] |
| shape_int | backbone_x_context_compact_main | -0.0333 | +0.0139 | +0.0472 | [-0.0376, +0.1351] |
| shape_int | backbone_x_shape_hint_main | +0.4944 | +0.4528 | -0.0417 | [-0.1811, +0.1049] |
| shape_int | backbone_x_interaction | +0.0556 | +0.0611 | +0.0056 | [-0.1836, +0.1743] |

## Bounded replication statement

- Execution shape-hint main effect direction replicated: Qwen +0.2306, Granite +0.1583 (both positive).
- Answer-shape main effect direction replicated: Qwen +0.4944, Granite +0.4528 (both positive).
- This is evidence from two quantized instruction backbones on one synthetic database, not general model-family robustness.

Canonical JSON/CSV files and recomputed rows are stored in this directory.
