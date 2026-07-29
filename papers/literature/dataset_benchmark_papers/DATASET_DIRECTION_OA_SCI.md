# 公共数据集：研究方向 × 近五年 SCI × Open Access 期刊匹配

更新日期：2026-07-26  
范围：manifest 中 **49** 个公共数据集  
检索窗口：优先 **2021–2026**；Open Access 以 gold/diamond/hybrid 可开放获取为主  

## 文档用途

1. 按数据集列出**适合的论文方向**。  
2. 给出近五年有代表性的 **SCI/SCIE** 引用/使用示例（需再以 WoS/JCR 核验）。  
3. 单独匹配 **Open Access SCI 期刊**（如 *IEEE Access*、*Energies*、*Scientific Reports*），便于走 OA 投稿路径且能用上本地已缓存数据。

相关机器可读表：

- `metadata/dataset_direction_sci_exemplars_curated.csv` — 方向 + 代表论文  
- `metadata/dataset_paper_candidates_filtered.csv` — OpenAlex 过滤候选  
- `metadata/curated_extension_papers.csv` — 扩展集精选 OA PDF  
- `metadata/dataset_sci_oa_pdf_summary.csv` / `dataset_sci_oa_pdf_registry.csv` — **每库 ≥5 篇本地 PDF 索引**  
- 本地 PDF 目录：`pdfs/<dataset_id>/`（已有则跳过，不重复下载）

### 本地 PDF 下载状态（2026-07-26）

- **49/49** 数据集均已达到 ≥5 篇可开放获取 PDF（合计约 245 篇）。  
- 优先源：arXiv PDF（多为 SCI/顶会论文预印本）+ Nature *Scientific Data/Reports* OA。  
- MDPI / IEEE Xplore stampPDF 经代理常返回 **403**，未纳入默认批量下载；可用时再手工补官方 OA 版。  
- 下载脚本：`scripts/literature/download_dataset_sci_oa_pdfs_aria2.py`（aria2 + 本地代理）。

---

## 1. Open Access SCI 期刊池（优先匹配）

下列期刊均为常见 **OA 或强 hybrid**、且近年常出现电力/能源/电池/负荷预测论文的 SCI/SCIE 出口（投稿前请核验当年 JCR 分区与 APC）：

| 期刊 | 类型 | 更适配的本库方向 |
|---|---|---|
| *IEEE Access* | Gold OA | OPF/调度、电池 SOH、窃电、负荷预测、EV |
| *Energies* (MDPI) | Gold OA | 负荷预测、配网、SimBench/Ausgrid、储能 |
| *Scientific Reports* | Gold OA | 窃电检测、通用 ML 能源应用 |
| *Scientific Data* | Gold OA | 数据集论文本身（如 SDWPF） |
| *Energy Reports* | Gold OA | 负荷/可再生预测、案例研究 |
| *Sustainability* (MDPI) | Gold OA | 规划、可持续电源选择、政策向 |
| *Applied Sciences* / *Electronics* (MDPI) | Gold OA | 算法验证、嵌入式/边缘、BMS |
| *Frontiers in Energy Research* | Gold OA | 储能、可再生并网、市场 |
| *Heliyon* | Gold OA | 探索性/跨学科能源 ML |
| *World Electric Vehicle Journal* | Gold OA | EV 充电负荷预测（ACN 生态） |
| *Processes* (MDPI) | Gold OA | DER 协调优化、配网运行 |
| *Protection and Control of Modern Power Systems* | OA | 继电保护/运行控制交叉 |
| *IET Generation, Transmission & Distribution* | 常 hybrid/OA | pandapower/配网运行 |
| *IET Energy Systems Integration* | 常 hybrid/OA | OPF/集成能源 |
| *Journal of Energy Storage* | hybrid/OA 可选 | 场站 BESS、FCR/aFRR |
| *Energy and AI* | hybrid | 电池 SOH、时序预测 |

**说明**：*Applied Energy*、*Energy*、*IEEE TPWRS/TSG* 影响大但多为 hybrid/订阅；若必须 OA，优先上表 gold 刊，或选这些刊的 OA 选项（APC）。

---

## 2. 全库一览：方向 + 代表 SCI + OA 出口建议

证据标记：

- `harvest`：本地 OpenAlex 过滤候选中有记录  
- `web`：人工核验的代表性论文  
- `curated`：主题匹配的典型 OA/SCI 出口（投稿导向）  
- `dataset`：数据集本身较新，SCI 引用仍稀，先跟数据集记录写方法文  

### 2.1 电网算例 / OPF / 规划

| 数据集 | 适合方向 | 近五年代表论文（示例） | 代表杂志 | **OA SCI 匹配建议** | 证据 |
|---|---|---|---|---|---|
| `matpower` | 潮流/OPF/N-1/ML-OPF | Enhancing LLMs for Power System Simulations… (2025) | *IEEE TSG* | **IEEE Access**（已有 2024 Robust KDE scheduling 等 OA 文）；*Sustainability* | harvest |
| `pandapower` | 配网仿真/潮流/DER | Security-constrained active power curtailment… (2023) | *IET GTD* | **IET GTD**（OA）；*Energies*；*Processes* | harvest |
| `pglib_opf` | AC/DC OPF、学习型 OPF | Physics-Informed Typed GNN OPF (2024) | *IEEE TPWRS* | **IET Energy Systems Integration**（OA）；*IEEE Access*；*Energies* | harvest |
| `pglearn_small` | ML-OPF、可行性 | PGLearn toolkit (2025) | arXiv | **IEEE Access** / *Energies*（方法复现文）；数据集文可投 *Scientific Data* | curated |
| `opfdata_landing` | 拓扑扰动 OPF、GNN-OPF | OPFData (2024) | arXiv | **IEEE Access**；*Scientific Data*（数据集扩展） | curated |
| `simbench` | 配网规划/时序/DER | DER coordinated optimization 等 (2025) | *Processes* | **Processes**；*Energies*；*IEEE Access* | harvest |
| `tamu_test_cases` | 大系统级联/规划 | Vulnerable Sequence Identification… (2025) | *IEEE TII* | **IEEE Access**；*Energies*；*Chaos*（hybrid） | harvest |
| `nrel118` | UC、生产成本、风光调度 | NREL-118 UC/生产成本研究线 (2022+) | *IEEE TPWRS* | **Energies**；*IEEE Access*；*Energy Reports* | curated |
| `rts_gmlc` | UC、可靠性、可再生并网 | Beyond price taker… (2023) | *Applied Energy* | **Energies**；*IEEE Access*；*Sustainability* | harvest |
| `miso_mtep` | 输电网扩展、投资回溯 | MTEP 项目表回溯类研究 (2023+) | *EPSR* / *TPWRS* | **Energies**；*Sustainability*；*IEEE Access* | curated |

### 2.2 负荷 / 市场 / 时序

| 数据集 | 适合方向 | 近五年代表论文（示例） | 代表杂志 | **OA SCI 匹配建议** | 证据 |
|---|---|---|---|---|---|
| `opsd_time_series` | 负荷/风光/电价预测 | Few-shot online learning… (2025) | *Energy* | **Energy Reports**；*Energies*；*IEEE Access* | harvest |
| `eia_opendata` | 美 RTO 负荷/价格 | EV Scheduling… (2025) | *IEEE TSG* | **IEEE Access**；*Energies*；*Sustainability* | harvest |
| `entsoe_transparency` | 欧负荷/发电/价格 | Optimized siting/sizing BESS (2023) | *Energy* | **Energies**；*Energy Reports*；*IEEE Access* | harvest |
| `pjm_dataminer` | LMP、负荷、停运 | Day-Ahead Scheduling of Energy Hubs (2023) | *IEEE TSG* | **IEEE Access**；*Energies* | harvest |
| `ett` | 长序列负荷/油温 | Informer（提出 ETT，2021） | *AAAI* | **IEEE Access**；*Energies*；*Energy Reports*（跟测 Informer/TimesNet） | web |
| `uci_household_power` | 户用负荷、NILM | NILM/户用预测系列 (2022+) | *Energies* 等 | **Energies**；*Applied Sciences*；*IEEE Access* | curated |
| `uci_tetouan_power` | 多区域短时负荷 | Tetouan 负荷预测 (2022+) | *Energies* | **Energies**；*Energy Reports* | curated |
| `monash_australian_demand` | 州级负荷基准 | Monash electricity demand track (2021+) | *Int. J. Forecasting* | **Energies**；*IEEE Access* | curated |
| `panama_load` | 负荷+天气联合预测 | Panama STLF (2022+) | *Energies* | **Energies**；*Energy Reports* | curated |
| `elia_total_load` | 15min 负荷预测 | Elia 负荷评估研究 (2023+) | *Applied Energy* | **Energies**；*Energy Reports* | curated |
| `sgsc` | 智能电表、DR、聚类 | SGSC 户用 DR 分析 (2022+) | *Applied Energy* | **Energies**；*Sustainability*；*IEEE Access* | curated |
| `sgcc_electricity_theft` | 窃电/异常检测 | Efficient electricity theft detection (2025)；Dynamic Generative Residual GCN (2024) | *Scientific Reports*；**IEEE Access** | **Scientific Reports**；**IEEE Access** | harvest/curated |

### 2.3 新能源 / 天气 / 充裕度

| 数据集 | 适合方向 | 近五年代表论文（示例） | 代表杂志 | **OA SCI 匹配建议** | 证据 |
|---|---|---|---|---|---|
| `nsrdb` | 辐照、PV 出力 | Global/direct irradiance DL + NSRDB (2023) | *Applied Energy* | **Energies**；*IEEE Access*；*Sustainability* | harvest |
| `sdwpf_kddcup2022` | 风电时空预测 | SDWPF dataset paper (2024) | ***Scientific Data*** | **Scientific Data**；*Energies*；*IEEE Access* | curated |
| `ausgrid_solar_home` | 户用光伏+负荷 | End-to-End Top-Down Load Forecasting (2024) | ***Energies*** | **Energies**；*Energy Reports*；*IEEE Access* | harvest |
| `psml` | 多尺度能源时序 ML | PSML 数据集及应用线 (2022+) | *IEEE TSG* 生态 | **IEEE Access**；*Energies* | curated |
| `large_synthetic_power_grid_ml` | 天气–电网 ML | Zenodo 数据集 (2024)；SCI 引用仍稀 | Zenodo | **IEEE Access**；*Scientific Data*；*Energies* | dataset |
| `renewables_ninja_country_sample` | 国别风光 CF | Renewables.ninja CF 规划应用 (2022+) | *Renewable Energy* | **Energies**；*Sustainability*；*Energy Reports* | curated |
| `vce_rare_power` | 资源充裕度 | RARE Power (2024) | Zenodo | **Energies**；*Sustainability*；*IEEE Access* | dataset |
| `eia860_wind_solar_cf` | 电厂级 CF | EIA-860 CF 包 (2024/25) | Zenodo | **Energies**；*Energy Reports* | dataset |
| `secures_energy` | 气候–能源情景 | SECURES-Energy (2025) | Zenodo | **Energies**；*Sustainability*；*Frontiers in Energy Research* | dataset |
| `era5_eu_supply_demand` | 气候驱动供需 | ERA5 EU CF/demand (2024) | Zenodo | **Energies**；*Scientific Data*；*IEEE Access* | dataset |

### 2.4 电池 BMS / 电网侧 BESS

| 数据集 | 适合方向 | 近五年代表论文（示例） | 代表杂志 | **OA SCI 匹配建议** | 证据 |
|---|---|---|---|---|---|
| `nasa_pcoe_battery` | SOC/SOH/RUL | ARNS SoH estimation (2022) | ***IEEE Access*** | **IEEE Access**；*Energies*；*Electronics* | web |
| `calce_battery` | SOC、DST/FUDS | 常与 NASA 同文验证 (2022) | ***IEEE Access*** | **IEEE Access**；*Energies* | web |
| `oxford_battery_degradation` | SOH/RUL | GPR for battery SOH (2024) | *Energy and AI* 线 | **Energies**；*IEEE Access*；*Electronics* | curated |
| `nasa_randomized_recommissioned_battery` | 二手电芯、变负载 | NASA randomized usage SOH (2023+) | *J. Electrochem. Soc.* | **Energies**；*IEEE Access*；*Batteries* (MDPI) | curated |
| `stanford_tri_high_power_battery` | 高倍率、随机工况 | TRI/Stanford 高功率数据生态 (2022+) | *Nature Energy* 线 | **Energies**；*IEEE Access*；*Batteries* | curated |
| `battery_archive` | 跨实验室老化 | Battery Archive 引用研究 (2023+) | *J. Power Sources* | **Energies**；*Batteries*；*IEEE Access* | curated |
| `m5bat_bess` | 场站 BESS、FCR | 欧洲平衡市场 BESS (2024) | *J. Energy Storage* | **Energies**；*Frontiers in Energy Research*；*IEEE Access* | curated |
| `finland_afrr_weather` | aFRR、调频 | 芬兰 aFRR+天气开放集 (2024–25) | Zenodo | **Energies**；*Energy Reports*；*IEEE Access* | dataset |
| `bess_european_balancing_inputs` | FCR/aFRR 仿真 | 欧平衡市场 BESS 输入 (2025) | Zenodo | **Energies**；*J. Energy Storage*（OA 选项）；*IEEE Access* | dataset |

### 2.5 EV / 故障诊断 / PMU / 可靠性文本 / RL

| 数据集 | 适合方向 | 近五年代表论文（示例） | 代表杂志 | **OA SCI 匹配建议** | 证据 |
|---|---|---|---|---|---|
| `acn_data` | EV 充电调度、DR | Adaptive Charging Networks… (2021) | *IEEE TSG* | **World Electric Vehicle Journal**；*Energies*；*IEEE Access* | web/harvest |
| `acn_data_static` | 充电曲线聚类、V2G | Forecasting EV charging flexibility (2023) | *Applied Energy* | **WEVJ**；*Energies*；*IEEE Access* | harvest |
| `dgann_duval` / `dgadb` | 变压器 DGA | ML-DGA / Duval 公开数据研究 (2022–23) | *Energies* / *IEEE TDEI* | **Energies**；*Applied Sciences*；*IEEE Access* | curated |
| `lbnl_pmu_event_library` | PMU 事件检测 | 开放 PMU 事件检测 (2022+) | *IEEE TSG* | **IEEE Access**；*Energies*；*Electronics* | curated |
| `gridstage` | 合成 PMU 验证 | GridSTAGE 类扰动仿真 (2023+) | *IEEE TPWRS* | **IEEE Access**；*Energies* | curated |
| `c2ges_nerc_reports` | 可靠性报告 NLP | C2GES/NERC 证据检索项目线 | Engineering Letters / CMC | **IEEE Access**；*Applied Sciences*；*Electronics*（NLP+电力） | curated |
| `grid2op_datasets` | 拓扑 RL、L2RPN | 混合系统能量/备用调度等 (2024) | *Applied Energy* | **Energies**；*IEEE Access*；*APL Machine Learning*（diamond） | harvest |

---

## 3. 按 OA 期刊反查：哪些本地数据最对口

| OA SCI 期刊 | 优先可用本地数据集 |
|---|---|
| **IEEE Access** | `matpower`、`pglib_opf`、`nasa_pcoe_battery`、`calce_battery`、`sgcc_electricity_theft`、`ett`、`opsd_time_series`、`acn_data_static`、`grid2op_datasets`、`pglearn_small` |
| **Energies** | `ausgrid_solar_home`、`simbench`、`uci_*`、`panama_load`、`elia_total_load`、`sgsc`、`nsrdb`、`renewables_ninja_*`、`m5bat_bess`、`finland_afrr_weather` |
| **Scientific Reports** | `sgcc_electricity_theft`、通用异常检测/窃电 |
| **Scientific Data** | `sdwpf_kddcup2022`；新数据集论文（`large_synthetic_*`、`era5_eu_*`、`pglearn`/`opfdata` 数据描述） |
| **Energy Reports** | `opsd_time_series`、`entsoe_transparency`、`eia_opendata`、`ett` |
| **Sustainability** | `rts_gmlc`、`miso_mtep`、`renewables_ninja_*`、`vce_rare_power`、`secures_energy` |
| **World Electric Vehicle Journal** | `acn_data`、`acn_data_static` |
| **Processes** | `simbench`、`pandapower`、DER 协调 |
| **Frontiers in Energy Research** | `m5bat_bess`、`bess_european_balancing_inputs`、`finland_afrr_weather` |
| **Electronics / Applied Sciences / Batteries** | `nasa_*`、`oxford_*`、`calce_battery`、`stanford_tri_*`、BMS 算法文 |

---

## 4. 投稿落地建议（简）

1. **想快投 OA**：优先 *IEEE Access* / *Energies* / *Energy Reports*；电池类再加 *Batteries*；EV 加 *WEVJ*。  
2. **想发数据集本身**：*Scientific Data*（已有 SDWPF 先例）。  
3. **本地已有数据即可开实验**：上表「OA SCI 匹配建议」列对应数据集均已在 `data/public_datasets/` 缓存（🔒 metadata-only 的除外：`nsrdb`/`pjm`/`acn_data` API/`nasa_randomized_*`/`battery_archive` 等）。  
4. **引用核验**：正式投稿前用 WoS/Scopus 核验「是否真的用了该数据集」与期刊当年 JCR；OpenAlex 全文检索会有误匹配。  
5. **APC**：IEEE Access / MDPI 需预算；部分 IET / hybrid 可选 OA。

---

## 5. 维护命令

```powershell
# 刷新候选（可能遇 OpenAlex 429，需限流）
python scripts/literature/search_dataset_benchmark_papers.py --dataset matpower nasa_pcoe_battery sgcc_electricity_theft

# 过滤阅读清单
python scripts/literature/filter_dataset_paper_candidates.py

# 每数据集补齐 ≥5 篇 SCI/OA 可下载 PDF（跳过已有）
python scripts/literature/download_dataset_sci_oa_pdfs_aria2.py
# 可选：OpenAlex 顶刊补缺（易 429）
python scripts/literature/download_dataset_sci_oa_pdfs_aria2.py --openalex
```

本地精选表：

```text
papers/literature/dataset_benchmark_papers/metadata/dataset_direction_sci_exemplars_curated.csv
papers/literature/dataset_benchmark_papers/metadata/dataset_sci_oa_pdf_summary.csv
papers/literature/dataset_benchmark_papers/DATASET_DIRECTION_OA_SCI.md   # 本文档
papers/literature/dataset_benchmark_papers/pdfs/<dataset_id>/
```
