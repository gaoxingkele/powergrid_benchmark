# Related Work

This paper's literature landscape (25 references) is organised into five thematic clusters.

## Typed dependency graph

### Cluster A: CCGT unit-commitment models by component representation [8–13]
- Papers that model CCGTs as individual gas and steam turbine components with coupling constraints.
- **Relationship**: The paper builds on this cluster's component approach, adding novel constraints (minimum gas hours, load distribution) not present in any of these works.
- **Cited in**: §1.2 (Literature Review).
- References: [8] Lu & Shahidehpour (2004), [9] Diez-Ledezma et al. (2006), [10] Hwan Kim & Edgar (2009), [11] Daneshi & Srivastava (2012), [12] Ashouri et al. (2013), [13] Bruno et al. (2015).

### Cluster B: CCGT unit-commitment models by configuration/mode [2, 14–22]
- Papers that represent CCGTs via discrete operating modes (e.g., 2 × 1, 1 × 1) rather than individual units.
- **Relationship**: The paper positions itself as a hybrid of Cluster A and Cluster B — using component representation with configuration-style coupling constraints, motivated by gaps in both clusters.
- **Cited in**: §1.2; used as comparator in the case studies (§3) via the heuristic.
- Key references: [2] Arroyo & Conejo (2002, "modeling of CCGTs in UC problems"), [14] Ergin et al. (2009), [18] Morales-Espana et al. (2017).

### Cluster C: Startup and thermal-state modelling [1, 3–7]
- Papers on thermal-state-dependent startup ramps, equipment damage from incorrect startup sequencing, and steam-turbine thermal stress.
- **Relationship**: The paper draws on this cluster to justify the hot/warm/cold startup ramps (Table 2) and the blade-erosion evidence (Figure 1). The constraint that gas-turbine operating hours gate steam-turbine startup extends this cluster's concerns.
- **Cited in**: §1.1, §1.2.
- References: [1, 3] CCGT operational standards, [4–7] equipment damage / thermal stress studies.

### Cluster D: Colombian market rules [25] and ancillary regulation [23, 24]
- Documents describing the Colombian electricity market, deviation penalty rules, and reserve requirements.
- **Relationship**: Provides the economic quantification framework for the penalty analysis (C06).
- **Cited in**: §3.1, §3.2.
- Key reference: [25] CREG Colombian market deviation settlement rule.

### Cluster E: General UC and MIP methodology [26–28]
- Foundational texts on mixed-integer programming for unit commitment.
- **Relationship**: Standard methodological background.
- **Cited in**: §2 (formulation) and as model-class reference.
- Note: References beyond 25 are not individually enumerated in this paper; the total is 28.

## Known links to other papers in this ARA journal collection
- Not yet established; this is the first CCGT-dedicated SEUC paper in the collection.
