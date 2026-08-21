# Related Work Dependency Graph

## RW1: Rezaei BWM (Original Method)

**Type:** imports

**Delta:** Provides the foundational Best-Worst Method with fewer comparisons (2n-3) than AHP. The current paper extends this to Bayesian BWM for group decision-making.

**Reference:** Rezaei, J. Best-worst multi-criteria decision-making method: Some properties and a linear model. Omega 2016, 64, 126-130.

**Source ref:** [34]

---

## RW2: Mohammadi and Rezaei Bayesian BWM

**Type:** imports

**Delta:** Introduces the Bayesian extension of BWM enabling probabilistic group decision-making, which this paper uses as its primary weighting method in Stage 1.

**Reference:** Mohammadi, M.; Rezaei, J. Bayesian best-worst method: A probabilistic group decision making model. Omega 2020, 96, 102075.

**Source ref:** [55]

---

## RW3: Hwang and Yoon TOPSIS

**Type:** imports

**Delta:** Provides the TOPSIS ranking method used to compute comprehensive risk and benefit scores for each project in Stage 1.

**Reference:** Hwang, C.; Yoon, K. Multiple Attribute Decision Making: Methods and Applications. 1981.

**Source ref:** [58]

---

## RW4: Mirrashid and Naderpour ILA

**Type:** imports

**Delta:** Provides the ILA metaheuristic optimization algorithm with claimed superiority over 19 other algorithms. Used as the solver in Stage 2.

**Reference:** Mirrashid, M.; Naderpour, H. Incomprehensible but Intelligible-in-time logics: Theory and optimization algorithm. Knowl.-Based Syst. 2023, 264, 110305.

**Source ref:** [59]

---

## RW5: Wu et al. BWM Portfolio Selection

**Type:** baseline

**Delta:** Wu et al. proposed a BWM-based model for investment portfolio selection, but without group decision-making. The current paper uses Bayesian BWM for this purpose and shows it produces less extreme weights.

**Reference:** Wu, Q.; Liu, X.; Qin, J.; Zhou, L.; Mardani, A.; Deveci, M. An integrated multi-criteria decision-making and multi-objective optimization model for socially responsible portfolio selection. Technol. Forecast. Soc. Change 2022, 184, 121977.

**Source ref:** [62]

---

## RW6: Li and Shi GA Portfolio Optimization

**Type:** baseline

**Delta:** GA applied to financial portfolio problems, used as benchmark optimization algorithm for comparison with ILA in Section 5.1.3.

**Reference:** Li, H.; Shi, N. Application of Genetic Optimization Algorithm in Financial Portfolio Problem. Comput. Intell. Neurosci. 2022, 2022, 5246309.

**Source ref:** [63]

---

## RW7: Wang et al. Risk Minimization Approach

**Type:** baseline

**Delta:** Represents the single-objective risk minimization approach used as comparison scenario 1a.

**Reference:** Wang, Z.; Zheng, J.; Li, H. The Risk Evaluation Model of Mining Project Investment Based on Fuzzy Comprehensive Method. Appl. Mech. Mater. 2013, 295-298, 2928-2934.

**Source ref:** [60]

---

## RW8: Yang et al. Benefit Maximization Approach

**Type:** baseline

**Delta:** Represents the single-objective benefit maximization approach used as comparison scenario 1b.

**Reference:** Yang, J.; Xiang, Y.; Wang, Z.; Dai, J.; Wang, Y. Optimal Investment Decision of Distribution Network With Investment Ability and Project Correlation Constraints. Front. Energy Res. 2021, 9, 728834.

**Source ref:** [61]

---

## RW9: Gao et al. Multi-Objective PGI Optimization

**Type:** extends

**Delta:** Existing multi-objective PGI optimization using quantum genetic algorithm. Extended by adding Bayesian BWM evaluation and ILA solver.

**Reference:** Gao, L.; Zhao, Z.; Li, C. An Investment Decision-Making Approach for Power Grid Projects: A Multi-Objective Optimization Model. Energies 2022, 15, 1112.

**Source ref:** [8]

---

## RW10: Sha et al. Investment Demand Balance

**Type:** extends

**Delta:** Investment demand-capacity balance optimization, extended to include risk-benefit collaborative tradeoff.

**Reference:** Sha, Y.; Ma, Q.; Xu, C.; Tan, X.; Yan, J.; Zhang, Y. Research on the balance optimization of investment demand and investment capability of power grid enterprises. Energy Rep. 2023, 9, 943-950.

**Source ref:** [7]

---

## RW11: Serrano-Gomez Policy Risk

**Type:** bounds

**Delta:** Provides policy risk context for photovoltaic projects, used to support the policy risk indicator selection.

**Reference:** Serrano-Gomez, L.; Munoz-Hernandez, J. Risk Influence Analysis Assessing the Profitability of Large Photovoltaic Plant Construction Projects. Sustainability 2020, 12, 9127.

**Source ref:** [40]

---

## RW12: Zhao et al. Carbon Neutrality

**Type:** bounds

**Delta:** Provides carbon neutrality context for low-carbon constraints in PGI.

**Reference:** Zhao, Y.; Su, Q.; Li, B.; Zhang, Y.; Wang, X.; Zhao, H.; Guo, S. Have those countries declaring "zero carbon" or "carbon neutral" climate goals achieved carbon emissions-economic growth decoupling? J. Clean. Prod. 2022, 363, 132450.

**Source ref:** [53]

---

## Additional Contextual References

| Ref | Citation | Role |
|-----|----------|------|
| [1] | Hu, C. et al. Econ. Res. 2022 | Investment-consumption-export context |
| [2] | Davidov, S.; Pantos, M. Energy 2017 | Risk impact on PGI performance |
| [3] | Niu, D. et al. Sustainability 2018 | TOPSIS sustainability evaluation extended |
| [13] | Wang, Y. et al. Energy 2021 | Regional power supply context |
| [14] | Wang, Y. et al. Energy 2020 | Investment cap constraint |
| [15] | Saldarriaga-Loaiza, J. et al. Sustainability 2022 | VaR/CVaR financial hazard |
| [19] | Xue, Q. et al. Front. Energy Res. 2021 | Multi-objective risk-benefit |
| [20]-[28] | Various | MCDM power industry studies |
| [36] | Yuan, Z. et al. High Volt. 2023 | TOPSIS application reference |
| [40] | Serrano-Gomez, L. et al. Sustainability 2020 | Policy risk |
| [41] | Xie, Y. et al. Energy 2017 | Energy policy adjustment |
| [47] | Wang, Y. et al. Pol. J. Environ. Stud. 2017 | Geological risk |
| [48] | Mohagheghi, S. Int. J. Disaster Risk Reduct. 2014 | Natural disaster risk |
