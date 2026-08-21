# Page-Scale Visual QA

Reviewed at the generated A4 preview scale on 2026-08-05.

- **PASS — direct-count legibility:** `179/180`, `155/180`, and `115/116`
  remain readable at approximately 7.1-inch content width.
- **PASS — interval semantics:** the cell figure has no error-bar glyphs and
  carries both a high-contrast `POINT ESTIMATES ONLY` banner and a footnote
  explaining that v2 cell intervals are composition-sensitivity intervals.
- **PASS — token audit:** both backbones are distinguished by color, marker or
  hatch, legend, and direct numeric labels; color is not the sole encoding.
- **PASS — axis/caption safety:** axes, units, panel labels, and offline-audit
  wording remain visible in `qa/page_scale_preview.pdf` and `.png`.
- **PASS — export consistency:** SVG/PDF/PNG are generated from the same
  plotting objects; PNG exports are at least 450 dpi and over 4000 px wide.

No component-experiment output was available or used. These are strictly
presentation-layer redraws of the frozen v2 CSV sources recorded in
`release_manifest.json`.
