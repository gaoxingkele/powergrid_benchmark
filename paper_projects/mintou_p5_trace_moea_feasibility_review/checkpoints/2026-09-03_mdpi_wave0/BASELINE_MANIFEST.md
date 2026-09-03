# P1 Wave 0 Baseline Manifest

**Status:** `BASELINE_FROZEN / SCIENTIFIC_REVALIDATION_PENDING`  
**Frozen at:** 2026-09-03, Asia/Shanghai  
**Target journal:** Energies  
**Locked title:** `Investment Effectiveness Optimization Strategy based on Hybrid Multi-objective Evolution`  
**Authors:** Yubin Lin (first and corresponding), Jiyu Li, Xiaofei Ruan, Xiaoyu Huang, Dishan Yang  

## Locked identity and authority

- The title above is exact, including capitalization, hyphenation, and the word
  `based`; no alternate TRACE-MOEA title is authorized for the canonical
  manuscript or Energies submission source.
- The confirmed author order is exactly Yubin Lin, Jiyu Li, Xiaofei Ruan,
  Xiaoyu Huang, Dishan Yang. This stage neither adds/removes an author nor
  assigns CRediT roles, affiliations, funding, or approval on an author's behalf.
- `manuscript/MANUSCRIPT.md` is the canonical narrative source and
  `manuscript/journal_submission/paper.tex` is the canonical Energies submission
  source. If identity or claim strength differs elsewhere, these files must be
  reconciled to this manifest and `CLAIM_EVIDENCE_REGISTER.md`; the conflicting
  file does not acquire authority by being newer or rendered.

## Canonical, legacy, and read-only roots

| Root class | Repository-relative root | Authority and mutation rule |
|---|---|---|
| Canonical project root | `paper_projects/mintou_p5_trace_moea_feasibility_review/` | The only writable reconstruction-v2 project. Stage artifacts, manuscript revisions, and future registered evidence belong here. |
| Canonical future experiment root | `paper_projects/mintou_p5_trace_moea_feasibility_review/experiments/p5_s4_energies_investment_validation_v1/` | Reserved for the approved validation pipeline. At this stage it is a `NO_RESULTS` scaffold and supplies no outcome evidence. |
| Legacy ARA evidence root | `papers/mintou/mintou_p5_trace_moea_feasibility_review/` | Historical source, configuration, run, table, and logic evidence. Read-only: cite with scope, but do not overwrite, relabel, or silently promote it. |
| Shared implementation root | `src/powergrid_benchmark/` | Repository-level implementation used by the legacy runs. Read-only in this isolated stage; inspecting it does not authorize cross-project edits or convert code behavior into outcome evidence. |
| Read-only predecessor root | `paper_projects/mintou_p5_trace_moea_feasibility_review/experiments/p5_s3_matched_sensitivity/` | Preserved matched-output, normalization, sensitivity, failure, and reproduction record. Read-only: new work must not alter or replace any file under this root. |
| Legacy presentation root | `paper_projects/mintou_p5_trace_moea_feasibility_review/manuscript/submission_preview/` | Superseded preview only. Read-only and non-authoritative for title, authorship, scientific wording, or release status. |

The Wave-0 checkpoint files record the boundary between these roots. They do
not turn a legacy proxy result into new validation, and the canonical future
experiment root becomes evidentiary only after later protocol, pilot, formal-run,
and statistical gates are satisfied.

## Repository state

- Repository branch: `main`
- Repository HEAD: `5f74050b8bd5631e2f14fb1519ea18ed48bf1cfa`
- Baseline definition: the current working tree, not a clean checkout of HEAD.
- Relevant pre-existing modified files: `manuscript/MANUSCRIPT.md`; `manuscript/journal_submission/paper.tex`.
- The modified files are treated as author-owned current content. This checkpoint does not revert or overwrite them.
- Pre-checkpoint project inventory: 224 files; 13,633,181 bytes.
- Pre-checkpoint tree fingerprint (SHA-256 over sorted relative paths and file hashes, measured before this checkpoint directory was added): `7debe7a1d83b7f67d254eae0257aeeda562cdd3743339fb25f63b7456511714a`.

## Critical-file hashes

| Path | Bytes | SHA-256 |
|---|---:|---|
| `README.md` | 2,697 | `76bb559e023c53d37f708045e689a2d6e9197fcc79f5012da9f01a197bb01d50` |
| `manuscript/MANUSCRIPT.md` | 99,765 | `0bd5861ed5fa7d39a419286312d245a0f18815195f92ec2597f8ca85499ba346` |
| `manuscript/journal_submission/paper.tex` | 102,087 | `c454a3ff9b2a11cb912e410caf94b775a08a90e5c40851c747d5b2aae0ac9529` |
| `manuscript/journal_submission/paper.pdf` | 636,814 | `6ea5daac7b158ca2ee2547f958f2f6afdb05b73008abd2aff801866fa4da0ad4` |
| `JOURNAL_REVIEW.md` | 19,324 | `ac5c8a6ce1b2958b8b98bff7d3d83a8a44316e65375cd66de5677681587a893f` |
| `ROUND2_REVIEW.md` | 34,881 | `43f3a9f3e01003a7d5ef5009cb5716036f0adb42711d1bbb7d2a5c8b44773e80` |
| `experiments/p5_s3_matched_sensitivity/config.json` | 6,614 | `5ba5979683b3e4d46dfad86c8d2a360acf7435c924f774ddcec168162744888a` |
| `experiments/p5_s3_matched_sensitivity/run_experiments.py` | 44,883 | `48ae653cd94b810e8e424d85f21557fb56bbac5b03e73d41c37099a2f67b18b0` |

## Material inventory

- Main prose: Markdown and Energies-family LaTeX.
- Compiled baseline PDF: present.
- Existing experiment namespace: `experiments/p5_s3_matched_sensitivity`.
- Project support areas: `.paper_harness`, `logic`, and manuscript review files.
- Current bibliography inventory: 33 `\bibitem` entries; item-level audit pending.
- New experiment outputs must use a new namespace and must not overwrite `p5_s3_matched_sensitivity`.

## Freeze interpretation

This manifest proves which files constituted the working baseline. It does not certify the scientific claims, citations, figures, or PDF as submission-ready. Any later statement must be traced through `CLAIM_EVIDENCE_REGISTER.md` and the new experiment results.
