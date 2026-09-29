# C²GES exploratory external experiment report

**Date:** 2026-09-10  
**Evidence class:** exploratory only  
**Confirmatory claims allowed:** no  
**Final dataset version:** v3  
**Dataset SHA-256:** `6C70BBB7924F587B2306E0BF1EF772081AA6C0C8E6F5C37C0A525697BB1E3C47`

## Scope and claim boundary

Eight official reports were fixed in the inventory. Seven PDFs were acquired
from ENTSO-E, NERC, and Transpower; the fixed NESO item returned HTTP 403 and
was retained as a documented acquisition failure rather than replaced. Source
metadata or snippets had been seen before freezing, and the reference summaries
were extracted automatically from official summary sections without human
adjudication. These results therefore cannot satisfy prospective E1 or E2 and
must not be described as an unseen, preregistered, or human-validated test.

## Self-correction history

- v0 exposed five malformed selected units in a 30-item two-model audit.
- v1 split obvious heading/body and caption/body blocks.
- v2 required complete body sentences and removed normalized duplicates.
- v3 used PDF line/font boundaries throughout each block, excluded raw table
  units from the main experiment, and removed unit-led cross-page fragments.
- No v3 layout rule was changed after viewing v3 ROUGE results.

The final v3 corpus contains seven reports and seven report series, with 58 to
1408 candidates per report. It records excluded table-unit counts rather than
silently treating table rows as ordinary sentences. All 112 system-comparison
rows and all 182 factorial rows completed without failure. All methods used the
same candidates and complete-ranking 110/260-word budget function.

## Exploratory E1 results

| Budget | Highest mean ROUGE-L | C²GES no-path | C²GES full | Mean words, all methods |
|---:|---|---:|---:|---:|
| 110 | TextRank: 0.16897 | 0.16683 | 0.15884 | 107.14–109.00 |
| 260 | C²GES no-path: 0.18435 | 0.18435 | 0.17717 | 257.43–259.00 |

C²GES no-path minus Semantic-MMR was +0.00784 at 110 words and +0.00929
at 260 words. C²GES no-path minus TextRank was −0.00214 and +0.00478,
respectively. C²GES no-path minus PacSum-MiniLM was +0.00070 and +0.00563.
Every cluster-bootstrap interval crossed zero and all six Holm-adjusted exact
values equalled 1.0. The exploratory data therefore do not establish a
length-controlled system advantage.

## Exploratory E3 results

Full minus no-path was −0.00799 at 110 words (95% series-cluster interval
[−0.01949, 0.00149]) and −0.00718 at 260 words ([−0.01828, 0.00147]); the
two Holm-adjusted exact values were 0.5625. Typed minus untyped graph effects
were +0.00139 and −0.00544, with intervals crossing zero. Reservation, path,
and interaction effects in the 2×2 experiment did not survive their predefined
Holm family. These results support no-path as the simpler provisional default
and do not validate typed edges or path deletion as performance sources.

## Automated quality audit

DeepSeek and Codex independently labeled 29 AB-6 selected units from all seven
series. This was a machine-only error-discovery pilot, not human annotation.
Unit-validity agreement was 93.1% (Cohen's κ=0.633); neither model marked a v3
unit as malformed. Role agreement was 75.9% (κ=0.698), while agreement of the
lexical heuristic with DeepSeek and Codex was only 48.3% and 65.5%. Thus the
layout repair passed the machine prescreen, but lexical role validity remains
unestablished and still requires qualified independent human annotators.

## Manuscript decisions

1. Report this experiment only as post-access exploratory evidence.
2. Do not claim C²GES superiority over TextRank, Semantic-MMR, or PacSum.
3. Use no-path as the provisional default because Full showed no stable benefit.
4. Describe typed roles and edges as heuristic textual proxies.
5. Do not count LLM agreement as E2 or as an ethics-approved human study.
6. Formal submission readiness still requires a newly acquired, genuinely
   unseen series-level test, two qualified independent human annotators, and an
   institutional ethics approval or exemption determination where applicable.

## Reproducible artifacts

- `BUILD_MANIFEST_v3.json` and `layout_candidate_audit_v3.csv`
- `e1_system_comparison_exploratory_v3/`
- `e3_factorial_exploratory_v3/`
- `AUTOMATED_ANNOTATION_AGREEMENT_v3.json`
- `AUTOMATED_ANNOTATION_SAMPLING_MANIFEST_v3.csv`
- `AUTOMATED_ANNOTATION_DISAGREEMENTS_v3.csv`
- private source PDFs, derived text, and raw model responses under ignored
  directories; these are not redistribution artifacts.
