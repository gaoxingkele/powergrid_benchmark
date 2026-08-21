---
title: "Optimization of Grid-Connected and Off-Grid Hybrid Energy Systems for a Greenhouse Facility"
authors:
  - Nuri Caglayan
year: 2025
venue: Energies
doi: "10.3390/en18174712"
ara_version: "1.0"
domain: ["energy systems", "renewable energy", "agricultural engineering", "techno-economic optimization"]
keywords: ["hybrid energy systems", "renewable energy", "greenhouse energy management", "LCOE", "environmental sustainability", "economic feasibility", "HOMER Pro"]
claims_summary: "This study evaluates grid-connected and off-grid hybrid energy system configurations for a greenhouse facility in Turkiye, identifying G/PV as most cost-effective grid-connected (NPC $282,492, LCOE $0.0401/kWh, 54.94% CO2 reduction) and Gen/PV/B as most viable off-grid (NPC $1.19M, LCOE $0.342/kWh, 64.58% CO2 reduction) configuration, with sensitivity analysis revealing that inflation above 10% critically undermines economic feasibility."
abstract: "This study evaluates the technical, economic, and environmental feasibility of grid-connected and off-grid hybrid energy systems designed to meet the energy demands of a greenhouse facility. Various system configurations were developed based on combinations of solar, wind, diesel, and battery storage technologies. The analysis considers a daily electricity consumption of 369.52 kWh and a peak load of 52.59 kW for the greenhouse complex. Among the grid-connected systems, the grid/PV configuration was identified as the most optimal, offering the lowest Net Present Cost (NPC) of USD 282,492, the lowest Levelized Cost of Energy (LCOE) at USD 0.0401/kWh, and a reasonable emissions reduction of 54.94%. For off-grid scenarios, the generator/PV/battery configuration was the most cost-effective option, with a total cost of USD 1.19 million and an LCOE of USD 0.342/kWh. Environmentally, this system showed a strong performance, achieving a 64.58% reduction in CO2 emissions; in contrast, fully renewable systems such as PV/wind/battery and wind/battery configurations succeeded in reaching zero-emission targets but were economically unfeasible due to their very high investment costs and limited practical applicability. Sensitivity analyses revealed that economic factors such as inflation and energy prices have a critical effect on the payback time and the Internal Rate of Return (IRR)."
ownership_status: external_published_paper_not_project_original
local_pdf: "D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p5_hybrid_moea_feasibility_review/p5_hybrid_moea_feasibility_review__04__optimization_of_grid_connected_and_off_grid_hybrid_energy__4c312a5bb7.pdf"
---

# Layer Index

## Layer 0: Problem Framing
- [logic/problem.md](logic/problem.md) — Problem statement: optimal hybrid energy system configuration for a greenhouse facility under grid-connected and off-grid scenarios
- [logic/claims.md](logic/claims.md) — 10 claims spanning economic, environmental, and sensitivity dimensions
- [logic/concepts.md](logic/concepts.md) — Key technical and economic concepts (NPC, LCOE, HOMER Pro, etc.)
- [logic/experiments.md](logic/experiments.md) — Simulation experiments conducted via HOMER Pro
- [logic/related_work.md](logic/related_work.md) — Positioned relative to prior hybrid energy optimization studies

## Layer 1: Solution Space
- [logic/solution/constraints.md](logic/solution/constraints.md) — Design constraints (load profile, component specs, economic parameters, site conditions)

## Layer 2: Environment
- [src/environment.md](src/environment.md) — Software environment (HOMER Pro 3.14.2), data sources (NASA POWER), economic parameters

## Layer 3: Epistemic Trace
- [trace/exploration_tree.yaml](trace/exploration_tree.yaml) — Exploration tree tracking the reasoning process

## Layer 4: Evidence
- [evidence/README.md](evidence/README.md) — Evidence inventory
- [evidence/figures/](evidence/figures/) — Figure PNGs and descriptors (Figures 1-16)
- [evidence/tables/](evidence/tables/) — Table PNGs and descriptors (Tables 1-10)
