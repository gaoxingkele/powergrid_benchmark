# Claims

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | `HyG-LoadFormer` improves day-ahead 24h OPSD load forecasting against target-journal-level lightweight baselines. | Supported on fixed and rolling public-data splits | E-real-OPSD; fixed MAPE `0.03972575` vs `0.05632632`; rolling mean MAPE `0.03931968` vs `0.05471780` |
| C2 | The hyperbolic graph/residual forecasting component contributes independently beyond the strongest ablation for 24h OPSD forecasting. | Supported on fixed and rolling public-data splits | E-real-OPSD; fixed strongest ablation MAPE `0.06915059`; rolling strongest ablation MAPE `0.07061538` |
| C3 | The method transfers to feeder/profile-level SimBench day-ahead forecasting with useful normalized-MAE reduction. | Supported for 24h normalized MAE; MAPE and 1h remain limitations | E-real-SimBench; fixed normalized MAE `0.07822078` vs `0.08103131`; rolling `0.07951836` vs `0.08361752` |
| C4 | The experiment package is reproducible from public or benchmark-derived data. | Supported structurally | E-repro; `src/code/run_real_opsd_forecasting.py`; `src/configs/real_opsd_config.json`; rolling evidence files |

Exact numerical manuscript claims must be scoped to the evidence file used. Current public-data claims are limited to day-ahead/24h behavior on OPSD and normalized-MAE behavior on SimBench; all 1h results and SimBench MAPE remain recorded limitations requiring further compliant optimization.
