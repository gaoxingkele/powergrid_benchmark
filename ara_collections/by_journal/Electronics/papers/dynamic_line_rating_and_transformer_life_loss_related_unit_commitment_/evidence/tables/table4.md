# Table 4: Comparison of transformer life loss costs based on different temperature multipliers

**Source**: Table 4, §5 (Case Study), page 15 (top of page)
**Caption**: "Comparison of transformer life loss costs based on different temperature multipliers."
**Screenshot**: table4.png
**Extraction type**: raw_table

Life-loss costs in 10^4 CNY. λ = temperature scaling factor applied to all regional 24 h temperature
curves.

| Temperature Multiplier (λ) | Life Loss Cost (Con-Model) | Life Loss Cost (TL-TF Model) | Cost Reduction |
|-----|-------|-------|-------|
| 0.9 | 0.082 | 0.030 | 63.4% |
| 1.0 | 0.130 | 0.040 | 69.2% |
| 1.1 | 0.189 | 0.051 | 73.0% |
| 1.2 | 0.285 | 0.680 | 76.1% |

**Transcription note / data anomaly**: values are copied verbatim. The λ = 1.2 TL-TF entry is printed
as **0.680**, which is internally inconsistent with its own "76.1%" cost-reduction column: a 76.1%
reduction from the Con-Model value 0.285 implies a TL-TF cost of ≈0.068, not 0.680 (and 0.680 would
exceed the conventional cost, contradicting the surrounding text that "the TL-TF model consistently
achieves lower life loss costs"). This is treated as a likely typographic error in the source
(0.680 vs 0.068); recorded as-printed and flagged. Trend across λ: life-loss cost rises with λ in
both models and the cost-reduction ratio increases monotonically (63.4% → 76.1%).
