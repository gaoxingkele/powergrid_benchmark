# Target-Journal Literature Dataset Coverage Analysis

Date: 2026-07-12. Scope: the 67 cached comparator PDFs under `pdfs/p1..p6`, checked against the local public dataset cache in `data/public_datasets/`.

Method: each PDF's case-study / experimental-setup section was read and its test systems and data sources extracted, then matched against the local dataset inventory (`data/public_datasets/CACHE_STATUS.md`: 12 fully downloaded sources, 7 metadata-only).

## Verdict

The comparator papers' data needs are **partially** covered locally:

- **Covered**: standard IEEE test cases (33/39/69/118/300-bus, RTS-24, Garver-style TNEP cases are literature tables), which dominate p1/p3/p4/p6 experiments, are available via local MATPOWER (`data/public_datasets/grid_cases/matpower`, includes case33bw, case39, case118, case300, case24_ieee_rts, case_RTS_GMLC, ACTIVSg series), PGLib-OPF, and RTS-GMLC.
- **Not covered (downloadable)**: the named public datasets listed below, most importantly the load-forecasting benchmarks used by every p2 comparator.
- **Not coverable**: roughly 25 of 67 papers rely on anonymized real utility/regional data (Chinese provincial grids, unnamed grid companies) that is not publicly released.

## Classification summary (67 papers)

| Group | Standard IEEE / literature benchmark | Named public dataset | Private/anonymized real data | Synthetic only | Review (no data) | Broken PDF |
|---|---|---|---|---|---|---|
| p1 dispatch/UC (12) | 5 | 2 (NREL-118, ECMWF) | 4 | 3 | 1 | 0 |
| p2 load forecasting (12) | 0 | 4 (Elia, ETT, Panama/Victoria/UCI, Tétouan/电工杯, PeMS-proxy) | 6 | 0 | 1 | 0 |
| p3 distribution planning (12) | 7 | 3 (Portugal 54-node, ESIOS Spain, Colombian 93-bus/CEC suites) | 2 | 1 | 2 | 0 (3 fixed 2026-07-12) |
| p4 resilience planning (12) | 5 | 2 (Ausgrid+SGSC, NREL wind) | 6 | 1 | 1 | 0 (2 fixed 2026-07-12) |
| p5 investment/feasibility (10) | 2 | 2 (World Bank/Ember/IRENA/NASA POWER stats) | 5 | 3 | 0 | 0 |
| p6 NSGA planning (9) | 1 | 0 | 6 | 1 | 1 | 0 |

(Some papers span multiple classes; primary class shown.)

## Named public datasets used by comparators vs. local cache

| Dataset | Used by | Local status |
|---|---|---|
| IEEE 33/39/69/118/300-bus, RTS-24 (MATPOWER) | p1, p3, p4, p6 (majority) | ✅ downloaded (`grid_cases/matpower`) |
| RTS-GMLC | p1-06 lineage, p3-07 | ✅ downloaded (`production_cost/rts-gmlc`) |
| PGLib-OPF | (dataset-paper group) | ✅ downloaded (`opf_benchmarks/pglib-opf`) |
| NREL-118 (extended IEEE-118 with time series) | p1-01 | ✅ downloaded 2026-07-12 (`grid_cases/nrel118`, NREL-Sienna repo mirror) |
| Elia (Belgian TSO) grid load | p2-04, likely p2-10 | ✅ downloaded 2026-07-12 (2022 full year, `time_series_market/load_forecasting_benchmarks`) |
| ETTh1/ETTm1 (ETT) | p2-06 | ✅ downloaded 2026-07-12 (same dir) |
| Australian (AEMO) load 2006–2011 | p2-06 | ✅ downloaded 2026-07-12 (Monash archive version, 2002–2015, same dir) |
| Panama Case Study load | p2-09 | ✅ downloaded 2026-07-12 (Mendeley full set, same dir) |
| Victoria (AUS) Daily Electricity Price & Demand | p2-09 | ⚠️ Kaggle-only; Monash Australian demand covers Victoria as substitute |
| UCI Household Electric Power Consumption | p2-09 | ✅ downloaded 2026-07-12 (same dir) |
| Tétouan (Morocco) power consumption (UCI) | p2-01 | ✅ downloaded 2026-07-12 (same dir) |
| 电工杯 competition load data | p2-01 | ❌ no stable public source |
| PeMSD4/7/8 (traffic, proxy benchmarks) | p2-11 | ❌ not grid data, intentionally skipped |
| Ausgrid rooftop PV (~300 homes) | p4-07 | ✅ downloaded 2026-07-12 (`renewable_weather/ausgrid_solar_home`, pierreh.eu mirror incl. official notes) |
| SGSC (Smart Grid Smart City, AUS) load | p4-07 | ✅ downloaded 2026-07-12 (`time_series_market/sgsc`; 1.7GB interval-reading 7z + companion CSVs) |
| NREL historical wind speed (WIND Toolkit) | p4-12 | ❌ absent (NSRDB is metadata-only; WIND Toolkit not cached) |
| Portugal 54-node planning benchmark (Miranda 1994) | p3-02, p3-10 | ❌ absent (literature tables) |
| Garver 6-node, IEEE 25-bus, Colombian 93-bus TNEP | p3-07, p3-11 | ❌ absent (literature tables) |
| CEC2020/CEC2022 test suites | p3-11 | ❌ absent (algorithm benchmarks, not grid data) |
| Spain ESIOS/REE demand & VRE 15-min series | p3-07 | ❌ absent (ENTSO-E cached metadata-only could substitute) |
| World Bank WDI/WGI, Ember, IRENA, OWID, NASA POWER, Eurostat | p5-02, p5-04 | ❌ absent |
| ECMWF weather forecasts | p1-09 | ❌ absent |

## Data that cannot be downloaded (by design)

~25 papers use anonymized real data: Chinese provincial/city grids (Zhejiang/Quzhou, Yunnan/Qujing, Hubei, Shanxi, Jiangxi, Guangdong, northeast China), unnamed grid-company investment project libraries (p5-03/p6-06, p6-07), Saskatchewan utility data (p5-10), Colombian CCGT plant (p1-10), Kenyan microgrid site (p4-02), ASU Campus Metabolism (on-request). These are cited context, not reproducible benchmarks; local coverage is not possible and reproduction should instead map onto the local public benchmarks.

## Dataset-benchmark paper group (24 PDFs)

By construction each maps to a `dataset_id`; 16 papers' datasets are fully downloaded locally (pandapower, pglib_opf, rts_gmlc, simbench, grid2op, psml, lbnl_pmu_event_library, c2ges_nerc_reports), 8 papers map to metadata-only sources requiring API keys/registration (acn_data ×1, eia_opendata ×1, nsrdb ×2, pjm_dataminer ×3, tamu_test_cases ×1).

## File integrity check (2026-07-12: false alarm, files intact)

The first-pass extraction reported 5 PDFs (p3-04/05/06, p4-05/06) as "stitched/mismatched". Re-downloading them from MDPI produced byte-identical files to the committed versions, and a page-by-page verification confirmed title/abstract/body are consistent in all five — the original files were never corrupted; the first-pass reading misattributed content. Corrected, verified case-study info:

1. p3-04 (WGAN-GP source–network–storage planning, Energies 2026, 19, 228) — Portuguese 54-bus (Miranda 1994) + real northern-China source-load measurements (State Grid Tianjin; data on request).
2. p3-05 (EBWO vulnerability-driven ESS planning, Energies 2026, 19, 210) — modified IEEE 33-bus + normalized field data from Northwest China.
3. p3-06 (Classification-based DG/CB/EVCS planning, Energies 2026, 19, 3262) — IEEE 33-bus and IEEE 69-bus standard cases.
4. p4-05 (EV charging infrastructure planning review, Energies 2026, 19, 1131) — review paper, no case study.
5. p4-06 (Flexible reconfiguration under uncertainty, Energies 2025, 18, 266) — IEEE 33-bus + TPC 83-bus (Taiwan Power Company) system.

## Actions completed 2026-07-12

1. ✅ Load-forecasting benchmarks for p2 cached under `data/public_datasets/time_series_market/load_forecasting_benchmarks/` (ETT, UCI Household, Tétouan, Monash/AEMO Australian demand, Panama, Elia 2022).
2. ✅ NREL-118 cached under `data/public_datasets/grid_cases/nrel118/` (225 files from NREL-Sienna PowerSystemsTestData).
3. ✅ Ausgrid solar home data cached under `data/public_datasets/renewable_weather/ausgrid_solar_home/` (mirror; official URL bot-blocked).
4. ✅ 5 suspect PDFs re-downloaded and verified — byte-identical to the cached copies; corruption report was a false alarm.

## Remaining known gaps

- NREL WIND Toolkit / NSRDB (API key), Spain ESIOS (token), ECMWF (registration), 电工杯 (no stable source), Victoria daily price&demand (Kaggle-only; Monash AEMO demand substitutes; AEMO's own CSV endpoint is bot-blocked), World Bank/Ember/IRENA country stats (API, not grid data), PeMS (traffic proxies, out of scope).
- Private/anonymized utility data used by ~25 comparator papers is not publicly available by design; plan the six manuscripts' experiments on the cached public benchmarks instead.
