# Table 4: Ablation Study of Model Components

- **Source**: Table 4, Section 4.2.4
- **Caption**: "Ablation study of model components, relative to the full Case 3 model."
- **Screenshot**: table4.png
- **Extraction type**: raw_table

| Configuration | ∆Total Cost | ∆Wind Curtailment | Note |
|--------------|-------------|-------------------|------|
| Full model (Case 3) | reference | reference | all mechanisms active |
| Without LCOE degradation | −0.42% | ≈0 pts | storage at cycle limit; affects cost accounting only |
| Without P2G | +0.61% | +14.5 pts | surplus wind no longer absorbed |
| Without gas-network constraints | ≈0% | ≈0 pts | gas network not binding in this case |
| Wind penetration −30% | +9.17% | ≈0 pts | more thermal and gas needed; no surplus to curtail |
