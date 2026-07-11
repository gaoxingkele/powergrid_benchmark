# Claim Scope Matrix

Use this matrix before manuscript drafting to keep every claim within the evidence boundary.

| Paper | Algorithm | Supported Scope | Boundary | Next Validation |
| --- | --- | --- | --- | --- |
| mintou_p1 | DSTAR-GRU | RTS-GMLC fixed/rolling dispatch proxy and high-renewable stress subset support DSTAR-GRU narrowly. | Not AC-OPF or unit-commitment proof; topology-control validation remains pending. | Add DC-OPF/UC or Grid2Op validation. |
| mintou_p2 | HyG-LoadFormer | OPSD and SimBench rolling evidence support day-ahead/24h hierarchical load forecasting. | Do not claim 1h superiority; claims should focus on day-ahead/24h behavior. | Add stronger neural short-horizon baselines only if 1h claims are needed. |
| mintou_p3 | CARS-MODE | SimBench DER/storage stress proxy supports CARS-MODE narrowly after preserving weak revisions. | Not AC/pandapower feasible planning proof; proxy hypervolume gain is narrow. | Add pandapower/AC load-flow and repeated DER-hosting scenario variance. |
| mintou_p4 | SHIELD-MOEA | SimBench resilience-planning proxy supports SHIELD-MOEA against baseline and ablation. | Scenario proxy lacks full AC/pandapower feasibility and scenario variance. | Add AC/pandapower feasibility and repeated scenario variance. |
| mintou_p5 | TRACE-MOEA | RTS-GMLC + SimBench + NERC-report-cache project-review proxy supports TRACE-MOEA. | Benchmark-derived review proxy lacks expert-labeled approval outcomes and calibrated costs. | Add expert-labeled feasibility-review outcomes and cost calibration. |
| mintou_p6 | BiLo-NSGA | Budget-constrained project-review proxy supports BiLo-NSGA and bidirectional local search. | Benchmark-derived project-review proxy lacks expert labels and enterprise validation. | Add expert-labeled review outcomes, dependency labels, and calibrated budget cases. |
