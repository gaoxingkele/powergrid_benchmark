# Table 4 - Alignment of physical and economic optimization tools

**Source**: Table 4, Section 3.5 in the review. The table spans pages 16–17: its caption and the header/first row ("Primary Function") appear at the bottom of page 16, and the "Battery Modelling" and "Optimization Goal" rows continue at the top of page 17.
**Caption**: "Alignment of physical and economic optimization tools."
**Screenshot**: table4.png (rendered from page 17, showing the continuation rows; caption + first row are on the preceding page 16)
**Extraction type**: raw_table

| Feature | (PVsyst and Helioscope) | Macro-Scale Tool (HOMER Pro 3.18.4) | Integration Advantage |
| --- | --- | --- | --- |
| Primary Function | Physical modelling (e.g., shading, string layout). | Economic dispatch modelling focused on energy balancing and cost optimization. | Ensures that economic models are based on realistic energy yield rather than theoretically installed capacity. |
| Battery Modelling | Electrochemical cell degradation analysis. | System autonomy and replacement forecasting. | PVsyst provides effective battery capacity degradation over time, which allows HOMER to schedule realistic replacement costs. |
| Optimization Goal | Maximize physical energy yield. | Minimize Net Present Cost (NPC). | Links physical yield directly to economic savings. |

**Note on the paper's own numbering**: The paper labels TWO different tables as "Table 4" — this alignment table (§3.5) and, in §4.1, the sentence "Table 4 provides a comparative quantitative synthesis of recent artificial intelligence-driven forecasting models," which actually refers to the forecasting table captioned "Table 5" (see table5.md). This ARA files the object by its printed caption ("Table 4. Alignment of physical and economic optimization tools").

**Supports claims**: C01, C08
