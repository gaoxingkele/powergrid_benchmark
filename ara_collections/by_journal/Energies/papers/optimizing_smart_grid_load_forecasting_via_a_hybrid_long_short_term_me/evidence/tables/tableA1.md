# Table A1: Sample Entries from Elia Grid Load Dataset

- **Source**: Appendix A (p.15)
- **Caption**: "Sample entries from Elia Grid Load dataset."
- **Screenshot**: tableA1.png
- **Extraction type**: raw_table

## Table data

Sample rows from the dataset, showing datetime-stamped load readings at 15-min resolution:

| Datetime (CET/CEST) | Datetime (UTC) | Elia Grid Load [MW] |
|---------------------|----------------|---------------------|
| 1/1/2022 00:00 | 12/31/2021 23:00 | 7229.321 |
| 1/1/2022 00:15 | 12/31/2021 23:15 | 7141.165 |
| 1/1/2022 00:30 | 12/31/2021 23:30 | 7066.856 |
| 1/1/2022 00:45 | 12/31/2021 23:45 | 6956.022 |
| 1/1/2022 01:00 | 1/1/2022 00:00 | 6906.256 |

The dataset contains timestamped 15-min load values for the period 1 January 2022 through 14 December 2022. It includes both CET (Central European Time) and UTC timestamps.

**Note**: The 15-min timestamps visible in Appendix A confirm the dataset resolution is 15-min intervals (00:00, 00:15, 00:30, 00:45, ...), which contradicts a statement in Section 3.5 that refers to "hourly energy load data from Elia" (documented as an internal inconsistency in constraints.md).
