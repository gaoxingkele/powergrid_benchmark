# Current-Version Boundary

## Canonical release

The only current manuscript sources in this directory are:

- `C2GES/paper_applsci.tex` and the PDF built from it;
- `MA_SQLGrid/paper_applsci.tex` and the PDF built from it.

The canonical release date is 2026-08-09. The 2026-08-11 audit rebinds the release to its actual final-compression page and figure counts. `CURRENT_RELEASE_MANIFEST.json` is the machine-readable authority.

## Superseded material

`_archive_pre_current_audit/` contains recoverable but non-current artifacts, including intermediate page checks, page-count reports, four-figure lineage files, unused architecture outputs, and two workspace-bound analysis scripts. These files are retained for provenance only and must not be used to describe, audit, or package the current PDFs.

The 2026-08-08 manuscripts and their 20-page/four-figure MA-SQLGrid Visual QA remain under the earlier `MA_SQLGrid/original_title_manuscript` and delivery directories outside this release root. They are historical versions, not alternative current sources.

## Reproduction entry points

- Dual framework figures: `python figure_sources/generate_dual_panel_frameworks.py`
- C2GES Figures 1--4: `python C2GES/scripts/generate_figures.py`
- C2GES Figures 5--6: `python C2GES/figures/generate_p60_additions.py`
- MA-SQLGrid Figures 2--6: `python MA_SQLGrid/figures/rebuild_publication_figures.py`
- Current lineage and release hashes: `python scripts/build_current_lineage.py`
- Current PDF page renders: `python scripts/audit_current_release.py`

All scripts resolve inputs from `__file__`; their behavior must not depend on the shell's current working directory.
