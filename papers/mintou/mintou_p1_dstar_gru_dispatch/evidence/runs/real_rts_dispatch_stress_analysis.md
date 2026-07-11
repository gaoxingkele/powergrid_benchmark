# RTS-GMLC Dispatch Stress-Subset Analysis - DSTAR-GRU

Status: pressure-condition analysis over high renewable, high topology-risk, and feasibility-stress subsets. Lower composite score is better.

## all

- Proposed score: `0.73965420`
- Best baseline: `Renewable-First ED` with `0.74024403`
- Best ablation: `Ablation-NoTopology` with `0.74228760`
- Relative gain over best baseline: `0.08%`
- Relative gain over best ablation: `0.36%`

## high_renewable

- Proposed score: `0.28523862`
- Best baseline: `Renewable-First ED` with `0.28729632`
- Best ablation: `Ablation-NoTopology` with `0.29403700`
- Relative gain over best baseline: `0.72%`
- Relative gain over best ablation: `3.08%`

## high_topology

- Proposed score: `0.88435443`
- Best baseline: `Renewable-First ED` with `0.88435443`
- Best ablation: `Ablation-NoSiamese` with `0.88435443`
- Relative gain over best baseline: `0.00%`
- Relative gain over best ablation: `0.00%`

## ramp_stress

- Proposed score: `0.85392410`
- Best baseline: `Renewable-First ED` with `0.85392410`
- Best ablation: `Ablation-NoTopology` with `0.85414063`
- Relative gain over best baseline: `0.00%`
- Relative gain over best ablation: `0.03%`

## renewable_ramp_stress

- Proposed score: `0.35976128`
- Best baseline: `Renewable-First ED` with `0.35976128`
- Best ablation: `Ablation-NoTopology` with `0.36084696`
- Relative gain over best baseline: `0.00%`
- Relative gain over best ablation: `0.30%`

## Boundary

Stress-subset evidence is a dispatch-feasibility proxy, not AC-OPF or UC proof. It is useful for showing where the retrieval/topology components matter most under public RTS-GMLC scenarios.
