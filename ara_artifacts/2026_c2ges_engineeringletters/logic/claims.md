# Claims

## C01: C2GES Primary Evidence F1

- Statement: Full C2GES reaches evidence F1 0.2983 at K=3 on the imported 40-document candidate benchmark.
- Status: Imported from source package; not locally rerun.
- Scope: Agent-verified candidate labels, not expert gold.
- Falsification: A rerun on the same artifact and protocol produces materially different K=3 evidence F1.
- Proof: `paper_projects/2026_c2ges_engineeringletters/source/REVISION_NOTE.md`; `paper_projects/2026_c2ges_engineeringletters/source/supplement/bm25_k_sensitivity/summary.json`

## C02: Small Role-Selective Graph Gain

- Statement: The graph signal is a small role-selective auxiliary gain, with full minus no-graph evidence F1 +0.0060, 95% CI [0.0014, 0.0119], p=0.0254.
- Status: Imported from source package; not locally rerun.
- Scope: Role-selective graph gate revision only.
- Falsification: The same paired comparison does not reproduce a positive graph delta.
- Proof: `paper_projects/2026_c2ges_engineeringletters/source/REVISION_NOTE.md`

## C03: Claim Boundary

- Statement: The manuscript should not claim broad graph inference, causal discovery, or power-system counterfactual simulation.
- Status: Active revision rule.
- Scope: Current paper revision.
- Falsification: Revised manuscript introduces broad causal/graph/counterfactual claims unsupported by the imported evidence.
- Proof: `paper_projects/2026_c2ges_engineeringletters/review_requirements/revision_backlog.md`
