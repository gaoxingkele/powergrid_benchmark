# Mintou Portfolio Status

Status date: 2026-07-11

## Engineering Coverage

| Paper | Algorithm | Target | Main Exp. | Ablations | Baselines | Smoke Runs | Public Benchmark | Current Signal |
|---|---|---|---:|---:|---:|---:|---|---|
| `mintou_p1` | `DSTAR-GRU` | IEEE Access | 7 | 6 | 8 | 525 | RTS-GMLC dispatch v3 + rolling/stress: narrow positive; OPF/UC needed | `narrow_promising_public_signal` |
| `mintou_p2` | `HyG-LoadFormer` | Electronics | 8 | 7 | 9 | 680 | OPSD v4 + SimBench v3 + rolling splits: 24h strong; 1h limitation | `day_ahead_promising_public_signal` |
| `mintou_p3` | `CARS-MODE` | Energies | 7 | 8 | 6 | 525 | SimBench DER/storage stress v5: narrow positive proxy; AC power-flow needed | `narrow_promising_public_signal` |
| `mintou_p4` | `SHIELD-MOEA` | Energies | 8 | 7 | 5 | 520 | SimBench resilience v2: promising hypervolume proxy | `promising_public_signal` |
| `mintou_p5` | `TRACE-MOEA` | IEEE Access | 7 | 8 | 6 | 525 | RTS-GMLC + SimBench + NERC-report-cache review v4: promising proxy signal | `promising_public_signal` |
| `mintou_p6` | `BiLo-NSGA` | Applied Sciences | 8 | 9 | 6 | 640 | RTS-GMLC + SimBench + NERC-report-cache review v3: promising proxy signal | `promising_public_signal` |

## Boundary

Synthetic smoke outputs validate code paths, ARA evidence wiring, method naming, baseline coverage, ablation coverage, and result-analysis generation. They must not be used as final manuscript performance claims.

P1 now has an RTS-GMLC benchmark-derived dispatch experiment with fixed, rolling, and stress-subset evidence. After preserving v1 weak and v2 marginal evidence, DSTAR-GRU gains 0.08% over the strongest baseline on the fixed split, 0.07% on rolling windows, and 0.72% on the high-renewable stress subset. OPF/UC validation is still required.

P2 now has OPSD and SimBench public-data benchmarks plus rolling temporal split evidence. OPSD 24h/day-ahead forecasting has a strong fixed and rolling signal; SimBench 24h has fixed and rolling normalized-MAE value. The 1h task remains a recorded limitation and should not be used as the main manuscript claim.

P3 now has a SimBench DER/storage stress planning experiment. After preserving v1/v2/v3 weak evidence and a v4 near-miss, CARS-MODE beats the strongest baseline NSGA-II by 0.46% and the strongest ablation FixedDE by 0.19% on the proxy hypervolume. This is a narrow positive signal; AC/pandapower feasibility remains required before strong manuscript claims.

P4 now has a SimBench benchmark-derived resilience planning experiment where SHIELD-MOEA beats the strongest baseline and ablation on the hypervolume proxy; full AC/pandapower validation remains required.

P5 now has an RTS-GMLC + SimBench + NERC-report-cache derived project-review experiment. TRACE-MOEA beats the strongest baseline AHP-TOPSIS by 1.23% and the strongest ablation by 3.71% after preserving v1/v2 weak and v3 near-miss evidence; expert labels and calibrated engineering economics remain required.

P6 now has an RTS-GMLC + SimBench + NERC-report-cache derived project-review experiment. BiLo-NSGA beats the strongest baseline AHP-TOPSIS by 3.87% and the strongest ablation by 3.57% after preserving v1/v2 weak evidence; expert labels and calibrated engineering economics remain required.

## Next Upgrade Path

1. Add PGLib/MATPOWER OPF or Grid2Op feasibility validation for P1.
2. Add stronger neural baselines and short-horizon feature extensions for P2 if the paper wants to claim 1h forecasting.
3. Add pandapower feasibility checks and repeated DER-hosting scenario variance for P3.
4. Add AC/pandapower feasibility and scenario variance for P4.
5. Add expert-labeled feasibility review outcomes and cost calibration for P5 and P6.
6. Preserve failed or weak runs in ARA traces instead of deleting inconvenient evidence.
