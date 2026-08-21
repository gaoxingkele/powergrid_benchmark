# Claims

## Primary Claims

| Claim ID | Statement | Evidence Location | Epistemic Status |
|----------|-----------|-------------------|------------------|
| C1 | The proposed bi-level HESS planning model simultaneously optimizes storage siting/sizing and power dynamic allocation, integrating investment costs, flexibility penalties, voltage stability, and line losses. | Sections 2.1.2-2.1.4, Equations (7)-(23) | Verified — mathematically formalized with explicit equations |
| C2 | PSO-VMD adaptively determines the optimal VMD decomposition parameters (mode number K, penalty factor alpha), eliminating subjectivity in frequency-based power allocation. | Section 2.1.1, Algorithm 1, Equations (1)-(6) | Verified — algorithmic procedure defined |
| C3 | The median spectrum threshold in VMD-PSO enables precise separation of high-frequency (Li-ion) and low-frequency (flow battery) components. | Section 2.1.1, Step 4, Equation (6) | Verified — clear threshold definition |
| C4 | IWAA with Refraction Opposition-based Learning enhances global search capability and prevents premature convergence in the exploration phase. | Section 3.2.1, Equation (51) | Verified — mathematical formulation provided |
| C5 | Dynamic crowding distance (sequential removal method) maintains superior Pareto solution diversity compared to conventional single-pass selection. | Section 3.2.2, Equation (52) | Verified — algorithm described |
| C6 | Multi-node coordinated HESS deployment (Scheme 5) outperforms single-node hybrid configuration (Scheme 4) across total cost, voltage fluctuations, line losses, and penalty costs. | Section 4, Table 2 | Verified — quantitative comparison (4.1% total cost reduction) |
| C7 | IWAA achieves superior solution quality, mean value, and stability compared to COOT, PSO, DE, and standard WAA for the HESS bi-level planning problem. | Section 4, Table 3 | Verified — 13.3% better penalty cost best solution than WAA; 10.5% better total cost than DE |
| C8 | The VMD-PSO decomposition achieves near-perfect reconstruction (max error 1.14e-13, RMSE 4.74e-15), confirming accurate power allocation. | Section 4, page 20 | Verified — numerical error metrics reported |
| C9 | Higher flexibility penalty coefficients lead to reduced optimal storage capacity; penalty coefficient in range 0.2-0.3 lambda_0 provides balanced trade-off for operators prioritizing stability. | Section 4, Table 4 | Verified — sensitivity analysis with five penalty levels |

## Claim Classification

### Novelty Claims
- **C1**: New formulation (bi-level HESS planning with multi-objective lower level)
- **C2**: New method (PSO optimization of VMD parameters for HESS power allocation)
- **C4**: New method (IWAA with refraction opposition-based learning)
- **C5**: New method (dynamic crowding distance with sequential removal)

### Performance Claims
- **C6**: Quantitative superiority over baseline schemes
- **C7**: Quantitative superiority over competing algorithms
- **C8**: Technical accuracy of decomposition method

### Domain/Context Claims
- **C3**: Effectiveness of median frequency threshold
- **C9**: Practical guidance for penalty coefficient selection

## Verification Status

| Claim | Verification Method | Result | Confidence |
|-------|-------------------|--------|------------|
| C1 | Model analysis | Model is well-specified mathematically | High |
| C2 | Algorithm analysis | PSO optimization of K and alpha is clearly described | High |
| C3 | Technical review | Median frequency split is a reasonable approach | Medium |
| C4 | Algorithm analysis | Refraction opposition learning is mathematically defined | High |
| C5 | Algorithm analysis | Sequential removal is well-described | High |
| C6 | Table 2 data | Direct numerical comparison supports claim | Very High |
| C7 | Table 3 data | Direct numerical comparison supports claim | Very High |
| C8 | Reported metrics | Extremely low error values support claim | Very High |
| C9 | Table 4 data | Clear monotonic trend supports claim | High |
