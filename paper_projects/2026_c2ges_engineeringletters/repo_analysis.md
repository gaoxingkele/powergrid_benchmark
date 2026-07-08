# Repository Analysis

## Repository

This is an uploaded Paper Refine workspace, not an external GitHub repository.
The original zip contained an embedded `.git`; it was intentionally excluded from the benchmark-managed copy.

## License

Not specified in provided sources.

## Environment

- Python experiment wrapper: `source/code/main.py`
- Requirements file: `source/code/requirements.txt`
- Current requirement file lists only `numpy`; the wrapper also imports `rouge_score` and dynamically imports validation scripts expected outside this submitted package.
- Local `pdflatex` was not found in the current Windows environment.

## Data Dependencies

The experiment wrapper expects a workspace containing:

- `verification_pilot/agent_audit_40doc`
- `three-pack/config.yaml`
- `verification_pilot/scripts/run_baselines.py`
- `verification_pilot/scripts/run_c2ges.py`

These paths are referenced by `source/code/main.py` but are not present in the uploaded source package.

## Entrypoints

- Manuscript: `source/paper.tex`
- Experiment wrapper: `python source/code/main.py`
- Planned smoke command: `python source/code/main.py --limit-docs 1 --bootstrap-samples 10 --out-dir debug/c2ges_smoke_run`

## Reusable Components

- Manuscript source and figures.
- Final PDF.
- Supplement summary for BM25/K sensitivity.
- Revision and optimization notes.

## Integration Notes

The project is currently best treated as a manuscript-refinement package with partial experiment code. Reproducing the full experiment requires restoring the omitted validation workspace or adapting paths to the benchmark scaffold.

## Reproducibility Risks

- Missing dependency installation.
- Missing local validation workspace.
- No local LaTeX toolchain detected.
- Label provenance is agent-verified candidate labels, not expert gold.
