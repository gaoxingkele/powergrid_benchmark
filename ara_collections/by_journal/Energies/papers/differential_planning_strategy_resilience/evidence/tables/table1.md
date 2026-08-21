# Table 1: Planning Scheme for Each Case

- **Source**: Page 14, Section 5.2
- **Screenshot**: `table1.png`
- **Claims supported**: C01, C02
- **Data**:

A matrix indicating which planning features are enabled (checkmark) or disabled (x) for each of the five cases:

| Feature | Case 1 | Case 2 | Case 3 | Case 4 | Case 5 |
|---------|--------|--------|--------|--------|--------|
| DDU | x | check | check | check | check |
| Multi-Level Line Reinforcement | check | check | check | check | check |
| Reconstruction (Reconfiguration) | x | x | check | check | check |
| Demand Response | x | x | x | check | check |
| Electric Vehicle | x | x | x | check | check |
| MEG | x | x | x | check | check |
| Distributed Samples (DRO) | x | x | x | x | check |

- **Key insight**: Cases incrementally add resilience measures, enabling isolation of each measure's contribution. Case 1 is the simplest baseline (no DDU, no flexible resources). Case 5 is the full proposed model with DDU, multi-level hardening, reconfiguration, DR, EV, MEG, and DRO.
