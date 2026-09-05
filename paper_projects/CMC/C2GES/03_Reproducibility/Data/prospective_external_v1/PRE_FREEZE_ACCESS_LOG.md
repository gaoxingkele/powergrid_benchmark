# C2GES prospective-v1 pre-freeze access log

Date recorded: 2026-09-06  
Protocol state: `DRAFT_NOT_FROZEN`  
Formal external test accessed: `false`

## Why this log exists

During source-discovery work, the web search interface returned content-bearing
snippets for several official reports and expanded one WECC PDF into searchable
text. Under the prospective protocol, any such candidate is conservatively treated
as seen before freeze. It is therefore excluded from the confirmatory external
test pool. This preserves the one-attempt external-test boundary instead of
silently treating exposed material as unseen.

## Exposed candidates and disposition

| Candidate | Official locator | Exposure | Confirmatory disposition |
|---|---|---|---|
| May 2024 Geomagnetic Disturbance Event Review | `https://www.nerc.com/globalassets/programs/rapa/gmd/reference-documents/may-2024-gmd-event-review.pdf` | title/search-result content snippet | exclude; development or qualitative context only |
| Incident Review: Voltage-Sensitive Crypto Load Reductions | `https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_considering_voltage-sensitive_crypto_load_reductions.pdf` | title/search-result content snippet | exclude; development or qualitative context only |
| Incident Review: Load-Pocket Shoulder Season Challenges | `https://www.nerc.com/globalassets/our-work/reports/event-reports/incident-review-load-pocket-shoulder-season-challenges.pdf` | title/search-result content snippet | exclude; development or qualitative context only |
| Incident Review: Preparing the Grid for Wind Energy Droughts and Down-Ramps | `https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_low_wind_event.pdf` | title and quoted secondary snippet | exclude; development or qualitative context only |
| Incident Review: Considering Simultaneous Voltage-Sensitive Load Reductions | `https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf` | title/search-result content snippet | exclude; development or qualitative context only |
| Inverter-Based Resource Disturbances in the Western Interconnection | `https://www.wecc.org/sites/default/files/documents/progress_report/2025/Inverter-Based%20Resource%20Disturbances%20in%20the%20Western%20Interconnection%2011.5.2025.pdf` | PDF text expanded, including executive summary and event descriptions | exclude from every confirmatory split |

The NERC and FERC index pages used to discover report titles are not experimental
documents and are retained only as source directories. The January 2025 Arctic
events report is already present in the historical development corpus and was
never eligible for the new external test.

## Required recovery action

A clean inventory must be assembled from official metadata without exposing
report body text or outcome-bearing snippets to the analysis team. Before any
candidate body is opened, the inventory must contain stable locators, proposed
series identifiers, access/rights records, download hashes, and a signed exclusion
of every item above. Only then may `EXTERNAL_PROTOCOL_FREEZE.json` become
`FROZEN` and `execution_allowed=true`.
