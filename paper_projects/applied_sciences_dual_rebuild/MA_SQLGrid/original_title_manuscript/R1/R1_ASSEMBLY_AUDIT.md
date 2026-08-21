# MA-SQLGrid Original-Title R1 Assembly Audit

Assembly completed: 2026-08-08, Asia/Shanghai  
Target: MDPI *Applied Sciences* article template  
Final title: **MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases**

## Outcome

The original-title R1 manuscript was assembled as an independent MDPI LaTeX
project in this directory. The prior narrow-title manuscript remains unchanged
at `MA_SQLGrid/manuscript_applsci/paper_applsci.tex`.

Final artifacts:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `paper_applsci.tex` | 39,445 | `B68685E184F0E5F3DC9698A5E27908AA1640F0FDA4A9B0CEBCFD79E8BB5E909D` |
| `references_verified.bib` | 15,883 | `155EB9325FF0C0D9C4A0F2A54B750C0FCBC21873B2807B51156F7988ACBDADDE` |
| `build/paper_applsci.pdf` | 482,867 | `0B9AB819053D462C5E41D1F365EC9CABD34D80146110DAB30220E1F3031D743F` |
| `build/r1_build_output.txt` | 122,490 | `F5E123512993561C61D243798C143FBC54E903704721A5F053CFCDAEB5496ABE` |

The final PDF contains **13 A4 pages**.

## Inputs and Reused Assets

| Evidence/source asset | SHA-256 | Assembly use |
|---|---|---|
| Original-title MA-SQLGrid DOCX | `CF220D2DE32A45CBF653E9B6502DDEA88867E5F7B8C7608FA79D816AD9765A52` | Title, five-role architectural intention, authors and affiliations; unsupported results excluded |
| Prior narrow-title Applied Sciences TeX | `F0CA2BA1E43599EE6B442B10071C9ACD0D39948B4801861D07B4BA824B8C83C8` | MDPI metadata, audited inherited result language, back matter and verified citation set |
| `ROUND1_SECTION_DRAFT.md` | `B6483C3C1E891A0B3E2E723F0518D54A2FF8AC5F7D17D00F565741D7F1F495D4` | R1 section and claim structure |
| `original_title_rebuild/ASSET_MAP.md` | `A6A8FA82227C419B7FC3AF10D58020D0F00F5B9D7E7C15F87D90011AB72ED44E` | Inherited/New/Diagnostic evidence separation |
| `original_title_rebuild/ma_sqlgrid_agents.py` | `E29E8EE3A08344388E1AFED10B798329F4D1FCB2B8CEB980A8D3D3A48FC90757` | Five specialist roles, blackboard, validation, critic and deterministic adjudication contracts |
| Retrospective diagnostic manifest | `EA32B502D1EC5E5EB2678A0491D4D3B5C0D5CEEFC4D503BD1DCB1B6CF2522AD8` | Hash-locked 180/173/172/7/1/0 coverage counts and accuracy prohibition |

The original DOCX's Spider, WikiSQL, large-corpus, agent-ablation, and claimed
counterfactual-gain numbers were not transferred. No new bibliography entry was
created; all 13 cited keys occur in the copied verified BibTeX file.

## Figures and Tables

The framework source is the implemented native SVG, with the visually reviewed
PNG derivative used by pdfLaTeX because the build does not invoke an SVG shell
converter.

| Figure asset | SHA-256 | Status |
|---|---|---|
| `figures/fig_ma_sqlgrid_implemented_coordination_r1.svg` | `E331940138A31904BEF7BD23FC7BA3C5EA554872AFAC5F5C9E9865676B39F0E0` | Lineage-bound SVG source |
| `figures/fig_ma_sqlgrid_implemented_coordination_r1_qa3.png` | `46CC87635C2563EEB22282124DE47225385B8254CB2BC0F75F674599253E5DE2` | Included framework rendering |
| `figures/results/fig01_v2_cells.pdf` | `1BDBB4F83C56C12E1184501355355E33BB65CBC409061B40C06F3592A636CEC4` | Inherited cell point estimates |
| `figures/results/figure_01_primary_effects.pdf` | `417EC304F12B48E4EBD2B6A258EDA6507054D057F487D6A55E7C65E5A028A3D1` | Inherited component effects |
| `figures/results/fig04_semantic_reliability.pdf` | `318108E69345F12E99D57CC9728883CDB2F2BCABC8E5D47AABEE87E8BA0183E7` | Inherited multi-state effects |

The GridDB cell table and retrospective replay coverage table were converted
from Markdown to native LaTeX `booktabs` tables. The final log contains no table
overflow warning. Render inspection covered the title/abstract page, framework
page, both table pages, all three result-figure pages, back matter, and references.
No clipping, overlap, or unreadable caption was observed.

## Evidence Boundary

- The 1440-prediction GridDB factorial experiment remains an inherited
  single-generation experiment, not a multi-agent run.
- The 700-call component study, 25,920-row state study, and 5000-call BIRD
  protocol retain their original denominators and method identities.
- The retrospective replay is explicitly named **retrospective offline
  coordination diagnostic**. It reports candidate coverage only and no selected
  accuracy, execution gain, rescue rate, or multi-agent superiority.
- Gold SQL and results remain outside the sealed coordination boundary.
- The prospective result placeholders from the Markdown draft were removed from
  Results. A budget-matched four-condition experiment is described only as
  future work, with no unexecuted result claimed.
- The implemented system is described as five specialist roles plus a separate
  deterministic controller, not six independent LLM agents or free-form debate.
- RTS-GMLC, SimBench, and NERC assets remain machine-adjudicated silver data,
  not expert gold.

## Build and Verification

Environment:

- MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)
- MiKTeX-BibTeX 4.2 (MiKTeX 25.12)
- Python 3.12.10

Executed from the R1 directory:

```powershell
& .\build.ps1
```

The script executes:

```text
python scripts/verify_manuscript.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex
bibtex build/paper_applsci
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build paper_applsci.tex
```

Final gates:

- Structural/evidence verifier: `PASS`
- Citation keys found in verified BibTeX: 13/13
- Included figures present: 4/4
- Native `booktabs` result tables: 2/2
- Undefined citations: 0
- Undefined cross-references: 0
- Fatal LaTeX errors: 0
- Overfull/underfull boxes in final log: 0
- PDF pages: 13
- PDF SHA-256: `0B9AB819053D462C5E41D1F365EC9CABD34D80146110DAB30220E1F3031D743F`

MiKTeX emitted its environment-level advisory that updates have not been
checked. All native compilation commands returned success; the advisory did not
alter the manuscript or create a LaTeX warning/fatal gate failure.
