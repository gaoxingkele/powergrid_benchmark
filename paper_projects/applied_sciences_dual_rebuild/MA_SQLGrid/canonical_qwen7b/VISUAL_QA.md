# Visual QA

**Scope:** Qwen2.5-Coder-7B-Instruct Q4_K_M; GridDB only; single model/database; Granite pending.

Automated rendering checks pass for six SVG/PDF/450-dpi PNG figure families. All plots use explicit labels plus redundant markers or hatches. Forest plots show zero references; the heatmap prints cell values.

Manual review also **passes**. All six figures were placed at full text width on six A4 pages in `qa/page_scale_preview.pdf` and inspected from a 110-dpi page rendering. Figures 1 and 5 were regenerated after title/legend overlap was found. Figure 3 was simplified after label overlap. Figure 6 was regenerated because an initial “lowest accuracy” rule was dominated by singleton families; the final plot includes all 12 family clusters with at least three questions and prints each family size.

Placement guidance: keep every figure at full text width. Figures 2, 4, and 6 contain long labels and must not be reduced to a narrow single column.
