# Public Dataset Registry

更新日期: 2026-07-06

本表统一登记电网 benchmark 所需公开数据集、仿真环境和数据入口。状态含义：`downloaded` 表示已在本地缓存核心数据；`metadata-only` 表示只保存了元数据、网页或索引；`planned` 表示候选资源，后续按题目需要获取。

| 类别 | 数据集/平台 | 本地路径 | 状态 | 访问方式 | 主要任务 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 标准网架 | MATPOWER case files | `data/public_datasets/grid_cases/matpower` | downloaded | GitHub sparse clone | PF, OPF, N-1, ML-OPF | 已缓存 `data/` 算例和项目元数据 |
| 标准网架 | pandapower networks/test cases | `data/public_datasets/grid_cases/pandapower` | downloaded | GitHub sparse clone | PF, OPF, short circuit, state estimation, distribution studies | 已缓存 `pandapower/networks` 入口 |
| OPF benchmark | PGLib-OPF | `data/public_datasets/opf_benchmarks/pglib-opf` | downloaded | GitHub clone | AC OPF, DC OPF, OPF 近似, 可行性评估 | 已缓存 IEEE/Pegase/RTE/GOC 等 case |
| 生产成本/可靠性 | RTS-GMLC | `data/public_datasets/production_cost/rts-gmlc` | downloaded | GitHub clone | production cost, unit commitment, reliability, renewable integration | 含 RTS 数据和说明 PDF |
| 配电/多电压等级 | SimBench | `data/public_datasets/grid_cases/simbench` | downloaded | GitHub clone | 配电网建模, DER 控制, load flow, time series simulation | 含 LV/MV/HV/EHV benchmark 结构 |
| RL 控制 | Grid2Op datasets index | `data/public_datasets/rl_control/grid2op-datasets` | downloaded | GitHub clone | topology control, L2RPN, sequential decision-making | 目前缓存索引；环境包体较大，按需下载 |
| 合成真实规模网架 | TAMU Electric Grid Test Cases | `data/public_datasets/grid_cases/tamu_test_cases_page.html` | metadata-only | 官网页面/按 case 下载 | PF, OPF, cascading, planning, market simulation | 包含 Texas2k、Hawaii、synthetic 80k 等公开 case |
| 欧洲时序 | Open Power System Data time series | `data/public_datasets/time_series_market/opsd_time_series` | downloaded | direct download/API | load forecasting, renewable forecasting, price forecasting | 已缓存 60-minute singleindex CSV 和 datapackage/README |
| 美国能源数据 | EIA Open Data | `data/public_datasets/time_series_market/eia_opendata_page.html` | metadata-only | API key/网页 | load, generation, price, fuel, regional analytics | API 使用需注册 key |
| 欧洲市场/系统 | ENTSO-E Transparency | `data/public_datasets/time_series_market/entsoe_transparency` | metadata-only | API token/网页 | load, generation, price, cross-border flow, forecasting | 入口页已缓存；数据 API 需要 token |
| 美国市场 | PJM Data Miner 2 | `data/public_datasets/time_series_market/pjm_dataminer` | metadata-only | UI/API | LMP/price forecasting, load forecasting, outage analytics | 访问说明页已缓存；数据需按 endpoint/API 获取 |
| 天气/太阳能 | NREL NSRDB | `data/public_datasets/renewable_weather/nsrdb_api_page.html` | metadata-only | API | PV forecasting, irradiance forecasting, solar scenario | API 大批量获取需 key 和参数约束 |
| 大规模合成 ML | Large synthetic power grid ML dataset | `data/public_datasets/renewable_weather/large_synthetic_power_grid_ml_zenodo_record.json` | metadata-only | Zenodo | power flow ML, surrogate modeling, weather-grid coupling | 总量约 TB 级，默认不全量下载 |
| 多尺度时序 | PSML / Open-source power dataset | `data/public_datasets/renewable_weather/psml` | downloaded | GitHub clone | load/PV/wind temporal ML, scenario generation | 仓库已缓存 |
| EV 充电 | ACN-Data | `data/public_datasets/distribution_ev/acn_data_dataset_page.html` | metadata-only | API token | EV charging scheduling, demand response, user behavior | API 需注册 token |
| 设备诊断 | DGANN / Duval DGA candidate | `data/public_datasets/equipment_fault_pmu/dgann_duval` | downloaded | GitHub clone | transformer fault diagnosis, rule + ML diagnosis | 实验前需审计标签定义 |
| 设备诊断 | dgadb DGA candidate | `data/public_datasets/equipment_fault_pmu/dgadb` | downloaded | GitHub clone | transformer fault diagnosis, rule + ML diagnosis | 实验前需审计标签定义 |
| PMU/故障 | LBNL PMU Event Library | `data/public_datasets/equipment_fault_pmu/lbnl_pmu_event_library` | downloaded | GitHub clone | event detection, disturbance analysis | 仓库已缓存 |
| PMU/故障 | PNNL GridSTAGE | `data/public_datasets/equipment_fault_pmu/gridstage` | downloaded | GitHub clone | synthetic PMU, disturbance simulation | 仓库已缓存 |
| 文本/NLP | C2GES NERC reliability reports | `data/public_datasets/reliability_reports/c2ges_nerc_reports` | downloaded | NERC official PDFs | causal-role evidence selection, reliability report NLP, sentence retrieval | 已下载 40 个官方 NERC PDF；C2GES 的 agent-verified evidence labels 未随公开报告提供 |

## 推荐下载策略

1. 默认只下载小到中等体量且许可证清晰的核心 benchmark。
2. 对 API/token 数据保存获取脚本和 metadata，不把私钥写入仓库。
3. 对 TB 级数据只保存 DOI、record JSON、下载清单和子集选择策略。
4. 每个进入实验的数据集都要补充字段字典、split 策略和 baseline whitelist。
