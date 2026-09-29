# Network search and calibration report

Date: 2026-09-10

## Outcome

- The pre-existing C2GES registry contained NERC reports only.
- Six previously unregistered official ENTSO-E reports were downloaded with `aria2c`, hashed, and converted to non-verbatim PDF-layout statistics.
- Two AEMO reports were found on AEMO's official incident-report listing, but both aria2c and the permitted single-stream fallback received HTTP 403. They were not used in the profile.
- All eight located series are now marked ineligible for the future E1 confirmatory external test because their existence or content has been inspected.

## Profiled official reports

1. ENTSO-E final report on the 4 November 2006 disturbance.
2. ENTSO-E January 2017 cold-spell report.
3. ENTSO-E Continental Europe separation report for 8 January 2021.
4. ENTSO-E Rogowiec substation incident report for 17 May 2021.
5. ENTSO-E Iberia separation report for 24 July 2021.
6. ENTSO-E final report on the 28 April 2025 Iberian blackout.

The local sample spans 36--472 pages. Automated extraction yielded coarse layout-block counts only. These counts are useful for stress-test sizing but are not validated extraction units and must not be described as ground truth.

## Rights and evidence boundary

- Official public access was verified; redistribution authorization was not.
- Source PDFs remain in the ignored private cache.
- Public artifacts contain URLs, hashes, counts, and distribution summaries, not report text.
- This is seen calibration evidence, not an untouched test set.
- The search does not satisfy E1 because all accessed reports are now seen.

## Synthetic use

DeepSeek received fictional prompts and no source-report text. Its outputs were expanded locally to match the observed report/page/layout-count profile. Synthetic records are permitted only for software stress tests, schema tests, failure injection, and dry-run ablations. They are prohibited as evidence of external validity or real-world effectiveness.
