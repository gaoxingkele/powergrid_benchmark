# MA-SQLGrid Round-2 Figure Assets

This directory contains presentation-only redraws requested during Round 2.
It does not modify the manuscript or `canonical_v2_reanalysis`, and it adds no
component-experiment results.

- `ma_r2_f01_v2_cells_point_estimates`: direct point estimates with percentage
  labels. The banner and footnote explicitly state that cell-level error bars
  are omitted. The very wide v2 cell intervals measure sensitivity to the
  observed template-cluster composition and should not be read as conventional
  independent-sample uncertainty. Cluster-aware inference belongs to the
  registered contrast table/effect plot.
- `ma_r2_f02_context_audit_direct_counts`: offline selector coverage with
  `179/180` all-table, `155/180` all-column, and `115/116` multi-table join-path
  labels, alongside mean model-token inputs for all four cells and both
  tokenizer families.

Regenerate and verify from the project root:

```powershell
python paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/round2_figure_assets/generate_round2_figures.py
python paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/round2_figure_assets/test_round2_figures.py
```

`release_manifest.json` records frozen input hashes, derived counts, output
hashes, and PNG dimensions/DPI. `qa/page_scale_preview.*` places both figures
at approximately 7.1-inch content width on an A4 page for legibility review.
