# Related Work / Citation Footprint

## Core References Cited in the Paper

### Dynamic Reconfiguration Methods

1. **Pan et al. (2022)** - "Dynamic reconfiguration of distribution network based on dynamic optimal period division and multi-group flight slime mould algorithm." *Electric Power Systems Research*, 208, 107925. [Ref 6]
   - Multi-period DR using MFSMA; decomposition approach based on load curve categories
   - Compared in Table 1 (decomposition DR)

2. **Cao et al. (2022)** - "Distribution Network Dynamic Reconfiguration Based on Improved Fuzzy C-Means Clustering with Time Series Analysis." *IEEJ Trans. Electrical and Electronic Engineering*, 17, 174-182. [Ref 7]
   - Decomposition DR using FCMC + PSO; time interval optimization

3. **Zhan et al. (2020)** - "Switch opening and exchange method for stochastic distribution network reconfiguration." *IEEE Trans. Smart Grid*, 11, 2995-3007. [Ref 8]
   - Heuristic SOE method for multi-hour stochastic reconfiguration
   - Tested on multiple systems including 33-, 119-, 84-, 136-, and 417-bus

4. **Azizivahed et al. (2018)** - "Multi-objective dynamic distribution feeder reconfiguration in automated distribution systems." *Energy*, 147, 896-914. [Ref 9]
   - Multi-objective complete DR using GWO+PSO; ENS, power loss, operation cost

5. **Dorostkar-Ghamsari et al. (2015)** - "Value of distribution network reconfiguration in presence of renewable energy resources." *IEEE Trans. Power Systems*, 31, 1879-1888. [Ref 10]
   - Hourly DR with solar and wind; solved via GAMS/MOSEK
   - Key comparison reference for IEEE 33-bus results

6. **Jafari et al. (2020)** - Hybrid EMA and WGA for DR [Ref 11]
   - Multi-objective: power loss, SAIFI, SAIDI, AENS

7. **Reference [12]** - Deep learning algorithm for DR [Ref 12]
   - Switching and power loss minimization

8. **Popovic and Kovacki (2022)** - "Multi-period reconfiguration planning considering distribution network automation." *Int. J. Electrical Power and Energy Systems*, 139, 107967. [Ref 17]
   - Backward dynamic programming for automated networks

### Risk-Based and Stochastic DR

9. **Popovic and Knezevic (2022)** - "Dynamic reconfiguration of distribution networks considering hosting capacity: A risk-based approach." *IEEE Trans. Power Systems*, 38, 3440-3450. [Ref 18]
   - Risk-based DR under load and generation uncertainty

10. **Santos et al. (2022)** - "Dynamic distribution system reconfiguration considering distributed renewable energy sources and energy storage systems." *IEEE Systems Journal*, 16, 3723-3733. [Ref 19]
    - DR + renewable + storage coordination via stochastic MILP

11. **Qiao et al. (2025)** - "Active and reactive power coordination optimization for active distribution network considering mobile energy storage system and dynamic network reconfiguration." *Electric Power Systems Research*, 238, 111080. [Ref 20]
    - MISOCP model for DR with mobile storage

### Graph-Based and RL Methods

12. **Zhan et al. (2024)** - "A Novel Graph Reinforcement Learning-Based Approach for Dynamic Reconfiguration of Active Distribution Networks with Integrated Renewable Energy." *Energies*, 17, 6311. [Ref 22]
    - Graph RL for DR

13. **Home-Ortiz et al. (2022)** - "Increasing RES hosting capacity in distribution networks through closed-loop reconfiguration and Volt/VAr control." *IEEE Trans. Industry Applications*, 58, 4424-4435. [Ref 21]
    - MISOCP for DR with reactive power compensation

### Other DR References

14. **Mukhopadhyay and Das (2020)** - "Multi-objective dynamic and static reconfiguration with optimized allocation of PV-DG and battery energy storage system." *Renewable and Sustainable Energy Reviews*, 124, 109777. [Ref 15]
15. **Peng et al. (2018)** - "Molecular evolution based dynamic reconfiguration of distribution networks with DGs considering three-phase balance and switching times." *IEEE Trans. Industrial Informatics*, 15, 1866-1876. [Ref 16]
16. **Lotfi and Shojaei (2023)** - "A dynamic model for multi-objective feeder reconfiguration in distribution network considering demand response program." *Energy Systems*, 14, 1051-1080. [Ref 23]
17. **Tu and Fan (2023)** - "IMODBO for optimal dynamic reconfiguration in active distribution networks." *Processes*, 11, 1827. [Ref 24]

### Uncertainty and Probabilistic Modeling

18. **Kayal and Chanda (2015)** - "Optimal mix of solar and wind distributed generations considering performance improvement of electrical distribution network." *Renewable Energy*, 75, 173-186. [Ref 25]
    - Source for DG probabilistic modeling parameters
19. **Khatod et al. (2012)** - "Evolutionary programming based optimal placement of renewable distributed generators." *IEEE Trans. Power Systems*, 28, 683-695. [Ref 26]
20. **Nikkhah and Rabiee (2019)** - "Multi-objective stochastic model for joint optimal allocation of DG units and network reconfiguration." *Renewable Energy*, 132, 471-485. [Ref 27]

### Foundational

21. **Ehsan and Yang (2019)** - "State-of-the-art techniques for modelling of uncertainties in active distribution network planning: A review." *Applied Energy*, 239, 1509-1523. [Ref 1]
22. **Golshannavaz et al. (2014)** - "Smart distribution grid: Optimal day-ahead scheduling with reconfigurable topology." *IEEE Trans. Smart Grid*, 5, 2402-2411. [Ref 2]
23. **Amini et al. (2024)** - "Passive Islanding Detection of Inverter-Based Resources in a Noisy Environment." *Energies*, 17, 4405. [Ref 3]

### COA Algorithm

24. **Dehghani et al. (2023)** - "Coati Optimization Algorithm." Reference [33]
    - Original COA paper; source for algorithm details

### Static Reconfiguration and Other Optimization

25. **Alqahtani et al. (2023)** - "Investigation and Minimization of Power Loss in Radial Distribution Network Using Gray Wolf Optimization." *Energies*, 16, 4571. [Ref 4]
26. **Amini et al. (2024)** - "Substation Cyberattack Detection and Mitigation in a High-Noise Environment." *IEEE ISGT*, Washington DC. [Ref 5]

### TPC 83-Bus Specific

27. **Bahmanifirouzi et al. (2012)** - "A new hybrid HBMO-SFLA algorithm for multi-objective distribution feeder reconfiguration problem considering distributed generator units." *Iranian J. Sci. Technol. Trans. Electr. Eng.*, 36, 51. [Ref 41]
28. **Lotfi (2022)** - "Multi-objective network reconfiguration and allocation of capacitor units in radial distribution system using an enhanced artificial bee colony optimization." *Electric Power Components and Systems*, 49, 1130-1142. [Ref 42]
29. **Su et al. (2005)** - "Distribution network reconfiguration for loss reduction by ant colony search algorithm." *Electric Power Systems Research*, 75, 190-199. [Ref 43]
30. **Niknam et al. (2012)** - "A new tribe modified shuffled frog leaping algorithm for multi-objective distribution feeder reconfiguration considering distributed generator units." *European Trans. Electrical Power*, 22, 308-333. [Ref 44]

## Position in the Literature

This paper contributes to the dynamic reconfiguration literature by:
1. **Extending uncertainty integration**: Unlike [6,9,11-16,20-22] that ignore or simplify uncertainty, this paper uses full scenario-based modeling for load, wind, and PV.
2. **Applying COA to DR**: First application of the Coati Optimization Algorithm to distribution network reconfiguration.
3. **Comprehensive cost objective**: Most papers consider fewer cost components. This work includes Closs, CVD, CSW, Cupn, CPV, and CWind in a unified framework.
4. **Dual validation**: Validates on both IEEE 33-bus (academic benchmark) and TPC 83-bus (real utility system).
5. **Reliability assessment**: Unlike most DR studies [10,14,22,24], this paper evaluates EENS to quantify reliability impact.
