# Framework Figure Visual QA

Status: **PASS** (protocol/method structure only; no unfrozen result values).

## Rendering and inspection procedure

- Generated every figure from its JSON source configuration with the shared deterministic renderer.
- Exported editable SVG, vector PDF and 450-dpi PNG.
- Inspected all six PNGs at original resolution after rendering.
- Checked the outer eight-pixel raster boundary for non-white content, node geometry against the canvas, SVG live text, PDF headers, PNG resolution, manifest hashes and source/config hashes.
- Used the Okabe--Ito palette plus redundant shape, hatch and line-style encodings so meaning does not depend on hue alone.

## Before/after corrections

| Figure | Earlier defect | Corrective layout | Final status |
|---|---|---|---|
| `ma_f01_pipeline` | End nodes approached the crop; repair loop and label were crowded. | Pulled endpoints inward, separated the loop, enlarged the repair node, shortened it to `Repair pass`, and reduced hatch density. | PASS |
| `ma_f02_factorial_external_flow` | Eligibility arrows and audit area competed with labels. | Rebuilt as source, eligibility/pairing, 2-by-2 cells, and result-record columns with short labels. | PASS |
| `ma_f03_human_review_sealed_gate` | Long decision text was cramped. | Split criteria, adjudication and the short `All gates pass?` decision into separate nodes. | PASS |
| `c2_f01_three_protocols` | Input/output nodes approached the crop. | Moved endpoints inward and aligned three paired protocol lanes. | PASS |
| `c2_f02_oof_document_split` | Document-group diamond overflowed; folds, labels and audit overlapped. | Rebuilt as three swimlanes; separated document keying, title normalization/group assignment, splits, OOF, final fit and audit. A final geometry check confirms the three left-side nodes are disjoint. | PASS |
| `c2_f03_evidence_audit_bootstrap` | Input and audit content approached the crop. | Rebuilt as evidence, strict-gate and paired-inference columns; shortened the decision and inset the E4 node. | PASS |

Captions and evidence-source pointers are recorded beside each figure in the generated `captions.md`; cryptographic hashes and export properties are recorded in each `artifact_manifest.json`.
