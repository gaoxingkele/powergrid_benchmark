# Table 9: Result of IEEE 123-Node Power Distribution Network

- **Source**: Page 20, Section 5.4
- **Screenshot**: `table9.png`
- **Claims supported**: C01, C02, C03
- **Data**:

| Case | Total Cost (10^4 CNY) | MEG Nodes | Simulation Time |
|------|----------------------|-----------|-----------------|
| 1 | 13,104 | / | 30 min |
| 2 | 14,884 | / | 40 min |
| 3 | 14,482 | / | 1.2 h |
| 4 | 13,531 | 32, 112 | 4.3 h |
| 5 | 13,701 | 32, 112 | 10.1 h |

- **Key insight**: The same cost trends observed on the IEEE 33-bus system are replicated on the larger IEEE 123-bus system: Case 2 cost > Case 1 (DDU modeling increases cost because hardened lines can still fail); cost decreases from Case 2 to Case 4 as more resilience measures are added; Case 5 cost slightly exceeds Case 4 (DRO premium). Simulation times increase significantly with model complexity: Case 5 at 10.1 hours is over 20x longer than Case 1 at 30 minutes, reflecting the combinatorial complexity of the full DRO-DDU formulation on a larger system.
