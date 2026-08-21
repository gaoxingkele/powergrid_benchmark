# MA-SQLGrid Applied Sciences Round-3 Assembly Report

## Status

Round-3 pre-review manuscript integration is complete within the isolated
`manuscript_applsci` directory. The superseded CMC manuscript and all upstream
canonical evidence are unchanged.

## Frozen manuscript snapshot

- Title: *MA-SQLGrid: A Controlled Factorial Study of Context Grounding for
  Text-to-SQL over a Power-Grid Maintenance Database*
- PDF: `build/paper_applsci.pdf`
- TeX SHA-256: `2724D78D2D2CDBD74E06783094FE07795E326BF2042803A606EB3EE2CDED0EC3`
- PDF SHA-256: `CF67243F9D6C100BDA76C3965E6513D2801741A1A5BF773C990FCCD23C8AF96F`
- PDF bytes: 664,506
- Author metadata: migrated from the paired CMC manuscript under explicit user authorization; see `../../AUTHOR_METADATA_MIGRATION_2026-08-06.md`.
- Pages: 25
- PDF-extracted token-like words, including references/front matter: 12,688
- Primary sections: 6
- Subsections/subsubsections: 31
- Numbered equation/align environments: 8
- Figures: 9 (3 framework, 3 factorial/audit, 2 prospective component, 1 multi-state reliability)
- Tables: 9
- Verified bibliography entries: 31
- Cited bibliography keys: 23

## Integrated canonical evidence

### Factorial and inference hierarchy

- v2: 1,440 aligned rows, corrected common-target endpoint, 720/720 direct
  SQLite verdict reproduction for each backbone.
- v3: 18 upstream files fail-closed against a hand-frozen input contract; 70
  normalized-SQL dependence-proxy groups (58 singletons, maximum 19), 39-group
  composition sensitivity, and frozen target counts 61/31/57/31.
- Primary execution family: exactly nine factorial/modifier tests, 100,000 group
  sign flips each, Holm 0/9.
- Secondary adherence family: only Qwen and Granite hint main effects pass; they
  are manipulation checks because the intervention supplies the scored target.
- Bootstrap limits are labeled composition-sensitivity intervals rather than
  population confidence intervals.

### Prospective component experiments

- Formal calls: 350 per backbone; 700 total; 170 E1-eligible questions in 61
  groups and 180 E2 V1 questions.
- E1 Qwen: +0.1059, interval [+0.0282, +0.2013], Holm p=0.0310 (positive for
  this snapshot only).
- E1 Granite: 0.0000; not promoted.
- E2 Qwen/Granite: +0.0389/+0.0556; neither promoted.
- Cross-backbone modifiers are not promoted; no replication claim is made.
- Independent component audit: 700 scored rows and 1,627 parsed candidates
  re-executed against frozen SQLite with zero flag mismatches; component release
  tests 6/6 pass.
- E4 reports input-token deltas of +50.3 (Qwen) and +61.8 (Granite). Latency is
  diagnostic only because the efficiency attestation is absent.

### Retrospective multi-state reliability

- Stage A contains 15 semantic states and three physical insertion-order
  diagnostics; all 1,440 archived predictions were executed on all 18 states.
- Two blinded technical reviewers held all 114 order-sensitive questions. The
  claim-promoting automatic subset contains 66 order-insensitive questions in
  12 normalized-SQL clusters.
- Exact denominators are 25,920 atomic rows, 7,920 primary semantic rows, 528
  primary predictions, and 16,416 held diagnostic rows.
- T0 reproduces canonical v2 for 1,440/1,440 predictions. Suite rates range from
  0.6212 to 0.8182; all nine Holm-adjusted factorial values equal 1.0000.
- Two independent pre-score and two independent post-score audits pass. One
  post-score audit independently executes 29,160 read-only SQL statements.
- This is a retrospective automated gold-SQL agreement stress test, not a human
  semantic audit or a population-accuracy estimate.

### Public/external boundary

- BIRD's protocol-pinned SQLite 3.40.1 gold-query preflight is 500/500 and the
  39-item technical freeze/audit is complete. Explicit human launch approval is
  absent; no model calls or model results exist.
- RTS-GMLC and SimBench candidates remain automatic, development-visible, and
  unadjudicated. No external accuracy, semantic validation, or operational
  generalization is claimed.

## Build and QA

- Manuscript evidence verifier: PASS (v2 26 files, v3 15 files, prospective
  analysis 4 files, component canonical manifest/copies, semantic release and
  dual post-score gates, 9 figures, 23 cited keys).
- LaTeX/BibTeX compilation: PASS.
- Undefined references/citations: 0.
- Overfull boxes: 0.
- Hyperref PDF-string warnings: 2, both caused by math notation in MDPI metadata;
  visible PDF content is unaffected.
- BibTeX warnings: 0.
- Underfull boxes: 4, limited to prose containing long model repository/hash
  strings and one prompt example; no clipping was observed.
- Multi-state result pages 15--17 were manually inspected. Both new tables and
  the forest plot are readable and unclipped; all p-value labels remain legible
  at full-page scale.
- Full PDF text was scanned for stale 499/500/SQLite-3.49 language, duplicated
  `the the`, promoted factorial-execution language, E2 efficacy, replication,
  controlled-latency, and external/human-semantic-validation claims; none was
  found.

## Human pre-submission blockers

1. Author names, affiliations, and correspondence are resolved from the paired
   CMC manuscript under explicit user authorization. Author-approved CRediT
   roles and any journal-requested non-corresponding-author e-mails remain open.
2. Funding, conflicts, acknowledgments, ethics/consent confirmation, and final
   generative-AI-use declaration.
3. Qualified human review/adjudication and a genuinely sealed follow-up set for
   any external-accuracy claim.
4. GridDB redistribution permission and source-specific license review.
5. License-reviewed public artifact deposit and permanent DOI/URL.
