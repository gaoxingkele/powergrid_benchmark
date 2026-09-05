# C²GES Figure–Table Audit

**Audit date:** 2026-09-06  
**Manuscript:** `01_Manuscript/LaTeX/paper_applsci.tex`  
**Scope:** six figures, nine tables, captions, in-text references, source lineage, manuscript copies, and final PDF rendering  
**Verdict:** **PASS for the protocol-ready snapshot; prospective result figures/tables remain intentionally absent**

## 1. Mechanical findings

- LaTeX preflight found 6 figures, 9 tables, 17 resolved cross-references, 35 resolved citation keys, and no missing graphics.
- The complete registry `03_Reproducibility/Figures/FIGURE_LINEAGE.json` uses schema `c2ges-figure-lineage-v3` and covers all 6 manuscript figures.
- Twenty-nine registered input/script/output hashes were recomputed: 29 matched, 0 were missing, and 0 mismatched.
- Each of the 6 PDF figures under `01_Manuscript/LaTeX/figures/` is byte-identical to its counterpart under `03_Reproducibility/Figures/`.
- The rebuilt manuscript contains 24 A4 pages. Figure 6 was visually checked on page 20: titles, axes, point intervals, counts, and caption are legible with no clipping or overlap.
- The build log contains no overfull boxes, undefined citations, or undefined references. Underfull boxes arise chiefly from narrow table columns and are not visible overflow defects.

## 2. Figure evidence audit

| Figure | Function | Evidence source | Audit result |
|---|---|---|---|
| 1 | Method schematic | Implemented scoring and selection definition | PASS; explicitly captioned as a deterministic framework, not empirical evidence |
| 2 | Corpus flow | Rights-safe report metadata | PASS; counts are source-bound and the caption states the retained corpus scope |
| 3 | Aggregate ROUGE-L | Frozen config plus aggregate metric JSON | PASS; caption labels equal-unit, unequal-word, descriptive evidence |
| 4 | Output length | `output_length_summary.csv` | PASS; generator checks all 4 conditions × 2 budgets and 15 reports per cell |
| 5 | Paired differences | Anonymous report-level difference CSV | PASS; all 90 values and six sign-count panels are rights-safe and traceable |
| 6 | Component diagnosis | Independent post-run audit plus development calibration decision | PASS after repair; all plotted values are machine-read and validated rather than hard-coded |

The Figure 6 repair is material: the generator now rejects a non-PASS audit, any nonzero contrast-recalculation discrepancy, a calibration record that accessed the test input, an invalid count range, a missing K=5/K=10 strict-removal contrast, or a nonzero nominal winner mislabeled as zero weight. The source audit remains explicitly historical, descriptive, and non-confirmatory.

## 3. Table audit

The nine tables are consistent with the manuscript's evidence hierarchy:

- positioning, role-transition, synthetic-example, and tuning-opportunity tables describe scope or method and do not masquerade as results;
- the historical main-result, series-cluster, output-length, matched-word, and registered-contrast tables identify their estimand, budget, sample size, uncertainty convention, and exploratory/descriptive status where applicable;
- bold and underline conventions in the historical main table are defined as observed extrema, not inferential conclusions;
- no table reports E1, E2, or confirmatory E3 outcomes, because those studies have not been executed.

## 4. Remaining gates

This audit does **not** authorize submission-final claims. Tables S5–S10 and the prospective forest, interaction, and human-validity figures may be added only after E1/E2/E3 produce frozen outputs. Until then, the present tables and figures correctly document a protocol-ready historical snapshot rather than a completed prospective study.

## 5. Severity classification

- **Blocking figure/table defects:** 0 in the current snapshot.
- **Recommended follow-up:** regenerate the complete lineage registry after any figure or source change; rerun page-level visual QA after E1/E2/E3 backfill.
- **Nonblocking layout note:** narrow descriptive tables generate underfull-box warnings; no content is clipped or outside the printable area.
