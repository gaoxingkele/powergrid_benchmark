# Table 3 - Table of weighting factors for each criterion

**Source**: Table 3, §2.2 (p. 7)
**Caption**: "Table of weighting factors for each criterion."
**Screenshot**: table3.png (rendered from PDF page 7)
**Extraction type**: raw_table

| Criterion | Substation Load Level | Influence of Substation on Low-Voltage Level Grid | Substation Power Supply Coverage | Spatial Influence of the Substation | Load Density |
|---|---|---|---|---|---|
| Weighting factor | 0.385 | 0.043 | 0.120 | 0.226 | 0.226 |

**Notes**: Weights derived by column-sum normalization + row averaging of Table 2. Ranking: load level (0.385) > spatial influence = load density (0.226) > power supply coverage (0.120) > low-voltage-grid influence / 10 kV line count (0.043). Consistency ratio CR = 0.00726 < 0.1 threshold (stated in §2.2 text, not in the table). These are the w_ij used in Eq. 6. Supports C01.
