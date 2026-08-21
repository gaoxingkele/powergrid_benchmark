# CMC Alias Workspace

This directory keeps the historical alias **CMC** for the two manuscripts, while
their current intended venue is **MDPI Applied Sciences (Basel)**.

The alias does not mean that the current files already comply with Applied
Sciences.  CMC/TSP source files are retained as the migration baseline and must
be converted to the MDPI template before submission.

## Papers

- `C2GES/` — *Causal-Role-Aware Extractive Evidence Selection for Power Grid
  Reliability Reports*
- `MA-SQLGrid/` — *MA-SQLGrid: A Multi-Stage Context-Grounding Framework for
  Text-to-SQL over Power Grid Maintenance Databases*

## Common layout

1. `00_Status_and_Index/` — actual target, alias and conversion checklist.
2. `01_Current_Manuscript/` — latest PDF, Word, LaTeX ZIP and supplement.
3. `02_CMC_Alias_LaTeX_Source/` — unpacked historical CMC/TSP source.
4. `03_Applied_Sciences_Template/` — local MDPI ACS template snapshot.
5. `04_Code_Data_Archive/` — complete code/data submission archives.
6. `05_CMC_Submission_and_Review_History/` — old cover letters, audits and reviews.

## Safety rule

Do not submit `02_CMC_Alias_LaTeX_Source/paper_cmc.tex` directly to MDPI.  It
uses `tsp.cls`, Vancouver references and CMC-specific declarations.  Create the
Applied Sciences version from the MDPI template in directory `03` and preserve
the CMC version as provenance.

The bundled MDPI template is the local snapshot dated 2026-06-23.  Re-check the
current Applied Sciences author instructions before final submission.
