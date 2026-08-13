# Claim Scope Matrix

Use this matrix before manuscript drafting to keep every claim within the evidence boundary.

| Paper | Algorithm | Supported Scope | Boundary | Next Validation |
| --- | --- | --- | --- | --- |
| mintou_p1 | DSTAR-GRU | RTS-GMLC fixed/rolling dispatch proxy and high-renewable stress subset support DSTAR-GRU narrowly. | Not AC-OPF or unit-commitment proof; topology-control validation remains pending. | Add DC-OPF/UC or Grid2Op validation. |
| mintou_p2 | CSA-LoadNet | OPSD supports a narrow day-ahead cross-series aggregation claim; SimBench and Ausgrid expose short-horizon and cross-dataset limits. | Do not claim 1h superiority; claims should focus on day-ahead/24h behavior. | Add stronger neural short-horizon baselines only if 1h claims are needed. |
| mintou_p3 | CARS-MODE | Repeated SimBench planning runs support CARS-MODE narrowly; an AC back-check confirms feasibility but changes the physical ranking. | AC feasibility is checked on selected solutions, but the benchmark is still limited to one network family and the surrogate and AC rankings differ. | Add independent network families and pre-registered AC-first evaluation if a general planning-superiority claim is required. |
| mintou_p4 | SHIELD-MOEA | Four SimBench MV networks, six stress scenarios, repeated runs, and AC back-checks support a bounded SHIELD-MOEA resilience claim. | Evidence remains composition-level across four public MV networks and six scenarios; it is not an enterprise deployment or universal optimizer ranking. | Add independent utilities/network families and calibrated field consequence models before making deployment claims. |
| mintou_p5 | TRACE-MOEA | RTS-GMLC + SimBench + NERC-report-cache project-review proxy supports TRACE-MOEA. | Benchmark-derived review proxy lacks expert-labeled approval outcomes and calibrated costs. | Add expert-labeled feasibility-review outcomes and cost calibration. |
| mintou_p6 | BiLo-NSGA | Budget-constrained project-review proxy supports BiLo-NSGA and bidirectional local search. | Benchmark-derived project-review proxy lacks expert labels and enterprise validation. | Add expert-labeled review outcomes, dependency labels, and calibrated budget cases. |
