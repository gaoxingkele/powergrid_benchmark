# 电网 Benchmark 跟踪目标（Grid Tracking Targets）

**用途**: 从国重/总部指南与电力 AI 叙事中抽取、与三地申报脱钩，统一纳入本仓库 **可复现 benchmark 跟踪**。  
**窗口**: 文献与开源资源优先 **2023–2026**；本地缓存对照 `data/public_datasets/`。  
**更新**: 2026-08-23  

### 本批下载状态（2026-08-23）

| 类型 | 结果 | 路径 |
|---|---|---|
| OA 论文 PDF | **52**（含 dataset_literature 批次 +16） | `papers/literature/grid_tracking_targets/pdfs/` |
| GitHub 浅克隆 | **20/20** | `data/public_datasets/grid_tracking/code/` |
| SMIB / MAPDN / WindFM / 故障定位 / 瑞士DER / UCI | 已落地 | `data/public_datasets/grid_tracking/datasets/` |
| PROTECT-90 波形 zip | ✅ ~12.05 GB | `…/protect90/` |
| InspecSafe train/test | ✅ ~23.6 GB | `…/inspecsafe/` |
| SIIB-Time 全量 | ✅ ~44.4 GB / 18009 files | `…/siib_time_full/` |
| DataPort 振荡/IEEE9 TSA | 仅 landing（需账号） | `…/dataport_landings/` |
| EnEnv 场景包 | ✅ ~7.96 GB | `…/datasets/enenv/scenarios/` |

清单：`data/public_datasets/grid_tracking/README.md`  
脚本：`download_grid_tracking_bundle.py` / `fill_grid_tracking_gaps.py` / `pull_grid_tracking_large.py` / `download_grid_tracking_dataset_literature.py`

---

## 0. 跟踪约定

| 字段 | 含义 |
|---|---|
| `PG-Txx` | 跟踪目标 ID |
| `task` | 可评测任务族（输入→输出→指标） |
| `local` | 本仓库已缓存资产（`dataset_id` 或路径） |
| `gap` | 公开缺口 / 需自建仿真 |

优先级（benchmark 可落地性）: **P0** 已有公开数据+代码可立刻立题 · **P1** 有数据需拼协议 · **P2** 指南热但开源稀缺。

---

## 1. 目标总表

| ID | 跟踪主题 | P | 指南锚点（摘要） | Benchmark 任务雏形 |
|---|---|---|---|---|
| PG-T01 | 暂态稳定科学计算 / PINN 轨迹代理 | P0 | 国重 3.3 | 轨迹预测 / 稳定分类 / CCT；vs 数值仿真误差与加速比 |
| PG-T02 | 配网数字孪生 + 反事实运行推演 | P0 | 国重 2.6 | 不完备量测状态估计；转供/消纳 what-if；Agent 工具调用正确率 |
| PG-T03 | 分布式光伏 hosting capacity | P0 | 国重 2.2 | 概率/鲁棒承载力；逆变器自治 vs 主动控制增益 |
| PG-T04 | VPP / 可调资源多智能体协同 | P0 | 国重 2.2/2.5 | MARL 调压/储能调度；峰削/频率/V2G 标准指标 |
| PG-T05 | 电力气象→新能源功率基础模型 | P0 | 2025-1.5；气象大模型 | 零样本/小样本风光预报；极端天气子集 |
| PG-T06 | 调度/运行 LLM 智能体 | P1 | 总部 232/235 | 故障处置 CoT；N-1/N-2 审计；工具调用合规 |
| PG-T07 | 宽频/强迫振荡辨识与溯源 | P1 | 国重 1.2 | 振荡分类；源定位；宽频 EMT 仍偏稀缺 |
| PG-T08 | 设备多物理场孪生 / PINN 状态推演 | P1 | 国重 3.9/4.8 | 热点温度；油中气体/热–电耦合；反事实故障 |
| PG-T09 | 具身智能巡检 / 多模态运维 | P1 | 总部 233/234 | 缺陷检测 mAP；多模态对齐；闭环处置协议 |
| PG-T10 | 边缘大小模型协同配网终端 | P1 | 总部 084 | 压缩后准确率–延迟–功耗；台区故障研判 |
| PG-T11 | 电网碳强度溯源 / 绿电归因 | P0 | 2025-3.11 | 小时 CI 预测；潮流碳追踪；负荷碳归因 |
| PG-T12 | 韧性配网与复合灾害预警 | P1 | 国重 2.1 | 故障定位；自愈重构；灾害–拓扑耦合（多需自建） |
| PG-T13 | 构网型 IBR / GFM 稳定与控制 | P0 | 2025-1.1/1.2；2026-1.1 | GFM/GFL 轨迹；小信号稳定边界；EMT–RMS 配对 |
| PG-T14 | 电–氢 / 多能耦合灵活运行 | P1 | 国重 1.5/1.6 | LCOH；调度+市场；sector-coupled OPF |
| PG-T15 | AI 可信评估与智能体安全 | P2 | 总部 227/229 | 幻觉/违规动作率；拒绝校准；联邦/隐私（公开少） |
| PG-T16 | OPF / 潮流代理与拓扑扰动 | P0 | 基础支撑/调度共性 | AC-OPF 可行性；拓扑扰动泛化 |
| PG-T17 | 拓扑/线路控制 RL（Grid2Op 族） | P0 | 柔性互联/安全运行 | L2RPN 风格奖励；N-1 存活 |
| PG-T18 | 负荷/电价/窃电时序预测 | P0 | 供需互动共性 | 标准 MAE/MAPE；窃电 F1 |
| PG-T19 | BESS 调频与平衡市场 | P0 | 储能协同 | FCR/aFRR；SOC 约束下收益 |
| PG-T20 | 变压器 DGA / 设备故障诊断 | P0 | 运检共性 | 故障类准确率；标签协议审计 |
| PG-T21 | EV/充电负荷与 V2G | P0 | 多元用户 | 调度成本；峰荷；V2G 利用率 |
| PG-T22 | PMU 扰动/事件检测 | P1 | 宽频/安全运行交叉 | 事件检测 PR；合成 PMU 泛化 |
| PG-T23 | 海上风电 / 海–岸–网组网（偏工程） | P2 | 国重 1.3/1.4 | 公开 EMT 数据极少；跟踪文献为主 |
| PG-T24 | 长时蓄热 / 电热耦合 | P2 | 国重 1.5 | 公开 benchmark 稀缺；多能模型旁路 |

---

## 2. 分目标：论文 / GitHub / 数据集（2023–2026 检索摘要）

### PG-T01 暂态稳定 / PINN
- **论文**: IEEE 9-bus TSA 图数据集 (arXiv:2608.18318)；SMIB PINN–CCT (IEEE Access + Zenodo)；PowerPINN 组件工具箱 (arXiv:2502.06412)；PINNacle NeurIPS 2024 (通用 PDE)
- **GitHub**: [i207M/PINNacle](https://github.com/i207m/pinnacle)；SMIB 复现仓（Zenodo 配套）
- **数据集**: IEEE DataPort 2万场景；[Zenodo SMIB splits](https://doi.org/10.5281/zenodo.19562416)
- **local**: 间接可用 `matpower` / ANDES 类仿真栈（需自建任务协议）
- **gap**: 省级规模公开轨迹仍缺

### PG-T02 配网孪生 / Agent
- **论文**: SoCal 28-Bus DT (arXiv:2504.06588)；CONDUCTOR LLM 孪生 (arXiv:2606.24609)
- **GitHub**: [caltech-netlab/digital-twin-dataset](https://github.com/caltech-netlab/digital-twin-dataset)；[kosmylo/PowerAgentBench](https://github.com/kosmylo/PowerAgentBench)；CONDUCTOR 开源栈
- **数据集**: SimBench；SoCal API（需白名单）
- **local**: `simbench`, `pandapower`
- **gap**: 反事实协议未标准化

### PG-T03 PV hosting capacity
- **论文/代码**: Caltech robust-scenario PVHC；Kortmann 概率承载力
- **GitHub**: [skortmann/probabilistic-pv-hosting-capacity](https://github.com/skortmann/probabilistic-pv-hosting-capacity)；caltech-netlab/pvhc-release
- **数据集**: SimBench LV；OpenDSS Ckt5；瑞士 DER Zenodo 16272961
- **local**: `simbench`, `ausgrid_solar_home`
- **gap**: 国内农网实测不可公开

### PG-T04 VPP / MARL
- **论文**: MAPDN (MARL 调压)；EnEnv 1.0 (AAMAS 2025)
- **GitHub**: [Future-Power-Networks/MAPDN](https://github.com/Future-Power-Networks/MAPDN)；[djbogucki/EnEnv](https://github.com/djbogucki/EnEnv)；[vinerya/virtual-power-plant](https://github.com/vinerya/virtual-power-plant)
- **数据集**: MAPDN HF zip；EnEnv 外部 data 链接；VPP 合成 4 数据集
- **local**: `grid2op_datasets`（拓扑控制近邻）；`acn_data_static`（负荷侧）
- **gap**: 真实 VPP 结算数据稀缺

### PG-T05 气象→功率 FM
- **论文**: WindFM (arXiv:2509.06311)；FuXi-Energy；SunCastNet / CorrDiffSolar
- **GitHub**: [shiyu-coder/WindFM](https://github.com/shiyu-coder/WindFM)；NVIDIA earth2studio / physicsnemo
- **数据集**: NREL WIND Toolkit；ERA5；KDDCup SDWPF
- **local**: `sdwpf_kddcup2022`, `era5_eu_supply_demand`, `renewables_ninja_country_sample`, `vce_rare_power`, `eia860_wind_solar_cf`
- **gap**: 物理机理嵌入的「电力气象大模型」公开权重少

### PG-T06 调度 LLM Agent
- **论文**: GAIA (arXiv:2408.03847)；Grid-Agent (arXiv:2508.05702)
- **GitHub**: PowerAgentBench
- **数据集**: IEEE 测试系统仿真生成任务（论文内）；尚无统一 CoT 语料库
- **local**: `matpower`, `pglib_opf`, `rts_gmlc`
- **gap**: 中文调度规程/思维链公开语料几乎无

### PG-T07 振荡辨识
- **论文/数据**: DPSYOR (IEEE DataPort DOI:10.21227/ebwk-j667) — NO/FO、Mini-WECC
- **GitHub**: 多依赖自建 EMT；GridSTAGE 合成 PMU
- **local**: `lbnl_pmu_event_library`, `gridstage`
- **gap**: **宽频 SSO（Hz–kHz）公开集仍稀缺（P1→P2 风险）**

### PG-T08 设备 PINN / 孪生
- **论文**: Sci Rep 2025 变压器 DETR+X+孪生；PowerPINN 组件路线
- **GitHub**: [mzaib1012/pinn-transformer-thermal-model](https://github.com/mzaib1012/pinn-transformer-thermal-model)
- **数据集**: 合成热模型 CSV；真实多物理场场测极少公开
- **local**: `dgann_duval`, `dgadb`（诊断近邻，非多物理场）
- **gap**: 电磁–热–力耦合公开真值缺

### PG-T09 具身巡检
- **论文**: InspecSafe-V1 (Sci Data)；电力具身政策叙事（跟踪非实验）
- **GitHub/HF**: [Tetrabot2026/InspecSafe-V1](https://huggingface.co/datasets/Tetrabot2026/InspecSafe-V1)；liuzy0708/InspecSafe
- **数据集**: 含电力设施多模态巡检点
- **local**: 无对等缓存（待纳入 manifest）
- **gap**: 国网缺陷大图库不公开；可用公开工业巡检作代理

### PG-T10 边缘轻量化
- **论文**: Frontiers 2024 LVDN 轻量 AI 编排；On-device AI survey (ACM CSUR 2025)
- **GitHub**: [TI tinyml grid_stability](https://github.com/TexasInstruments/tinyml-tensorlab/tree/main/tinyml-modelzoo/examples/grid_stability)
- **数据集**: UCI Electrical Grid Stability；自建压缩评测协议
- **local**: 无专用 edge 集；可用 `simbench`+量化管线自建
- **gap**: NPU≥4TOPS 类电力业务公开对照几乎无

### PG-T11 碳溯源
- **论文**: hyperscale DC 碳归因 (arXiv:2606.05420)
- **GitHub**: [singularity-energy/open-grid-emissions](https://github.com/singularity-energy/open-grid-emissions)；[codecexp/CarbonX](https://github.com/codecexp/CarbonX)
- **数据集**: OGE 美电网小时排放；CarbonX 多电网 CI
- **local**: `opsd_time_series`, `eia_opendata`, `entsoe_transparency`（强度需二次计算）
- **gap**: 中国省级溯源公开数据缺

### PG-T12 韧性 / 故障自愈
- **论文**: IEEE123 ML 故障定位；Powertech 实验行波集；自愈重构优化文
- **GitHub**: [fernando-barreira/ieee123-ml-fault-location](https://github.com/fernando-barreira/ieee123-ml-fault-location)；protect90-dataset
- **数据集**: Zenodo 15210584 (IEEE33+DER 短路)；PROTECT-90 Zenodo 18418330；52-bus 实验集
- **local**: `simbench`（拓扑）；无统一自愈奖励协议
- **gap**: 「全域自愈+AI」端到端公开 benchmark 未成形

### PG-T13 构网型 IBR
- **论文**: IBR 小信号数据生成 (arXiv:2512.06369)；Fraunhofer GFM-Benchmark（测量项目）
- **GitHub**: [MauroGarciaLorenzo/datagen](https://github.com/MauroGarciaLorenzo/datagen)；[pnnl/Grid-Cyber-Vulnerability-Dataset](https://github.com/pnnl/Grid-Cyber-Vulnerability-Dataset)（GFM-BESS）
- **数据集**: HF [neurips26-PSML/SIIB-Time](https://huggingface.co/datasets/neurips26-PSML/SIIB-Time)（3000 EMT–RMS 配对，GFM/GFL）
- **local**: 未缓存（**强烈建议纳入下一批下载**）
- **gap**: 厂商实测 GFM 曲线通常不开放

### PG-T14 电氢 / 多能
- **GitHub**: [IIT-EnergySystemModels/oHySEM](https://github.com/IIT-EnergySystemModels/oHySEM)；[CSEI-EU/Nord_H2ub](https://github.com/CSEI-EU/Nord_H2ub)；[PyPSA/pypsa-de](https://github.com/PyPSA/pypsa-de)
- **数据集**: PyPSA-DE solved networks Zenodo；各类 PtX 案例包
- **local**: 无氢专用；`rts_gmlc` / `secures_energy` 可作电力侧驱动
- **gap**: 「百兆瓦电氢」工程级公开运行数据无

### PG-T15 AI 可信 / 安全
- **论文**: 分散在 Agent/联邦学习文中；尚无电力专用可信 benchmark
- **GitHub**: PowerAgentBench 的 refusal/证据指标可作起点
- **数据集**: 几乎空白 → **自建协议优先**
- **local**: 无
- **gap**: P2，适合作为横切评测层而非独立数据集题

### PG-T16 OPF / 潮流 ML
- **论文**: OPFData (arXiv:2406.07234)；PGLearn
- **GitHub/数据**: pglib-opf；HF PGLearn；OPFData GCS
- **local**: `pglib_opf`, `pglearn_small`, `opfdata_landing`, `matpower`

### PG-T17 Grid2Op / 拓扑 RL
- **local**: `grid2op_datasets`
- **外部**: Grid2op / L2RPN 官方环境（按需拉全量）

### PG-T18 负荷/电价/窃电
- **local**: `ett`, `uci_*`, `monash_australian_demand`, `panama_load`, `elia_total_load`, `opsd_time_series`, `sgcc_electricity_theft`, `sgsc`

### PG-T19 BESS 市场
- **local**: `m5bat_bess`, `finland_afrr_weather`, `bess_european_balancing_inputs`

### PG-T20 DGA / 设备诊断
- **local**: `dgann_duval`, `dgadb`

### PG-T21 EV / V2G
- **local**: `acn_data_static`；API 版 `acn_data` 仍 metadata-only

### PG-T22 PMU 事件
- **local**: `lbnl_pmu_event_library`, `gridstage`

### PG-T23 / PG-T24
- **状态**: 文献跟踪为主；暂不建独立公开 benchmark 队列（除非后续出现开源 EMT/蓄热集）

---

## 3. 与本仓库缓存的覆盖矩阵

| 本地已强覆盖 | 跟踪目标 |
|---|---|
| 电网算例 / OPF / 生产成本 | T16, T17, T01(仿真底座), T06(工具调用底座) |
| 配网时序 / DER | T02, T03, T12(部分) |
| 新能源–气象 | T05 |
| 负荷/市场/窃电 | T18 |
| BESS 市场 | T19, T04(部分) |
| 设备 DGA / PMU | T20, T22, T07(部分) |
| EV | T21 |

| 建议下一批纳入 manifest | 理由 |
|---|---|
| SIIB-Time (HF) | T13 P0 构网轨迹 |
| MAPDN voltage_control_data | T04 P0 |
| WindFM 权重 + 评测脚本 | T05 P0 |
| PowerAgentBench | T06/T02/T15 |
| InspecSafe-V1 | T09 |
| IEEE9 TSA / SMIB PINN | T01 |
| DPSYOR | T07 |
| probabilistic-pv-hc + Ckt5 | T03 |
| CarbonX / OGE 子集 | T11 |
| PROTECT-90 或 IEEE123 fault package | T12 |

---

## 4. 建议的 benchmark 立题队列（与申报脱钩）

1. **Queue-A（立刻可复现）**: T01 ∪ T16 ∪ T05 ∪ T18 — 科学计算代理 + OPF + 预报标准赛道  
2. **Queue-B（Agent/孪生）**: T02 ∪ T06 ∪ T04 — PowerAgentBench + MAPDN + SimBench  
3. **Queue-C（新型主体）**: T13 ∪ T03 ∪ T19 — GFM/SIIB + hosting capacity + BESS  
4. **Queue-D（运检/可信）**: T09 ∪ T08 ∪ T15 — 公开代理数据 + 自建可信指标  

---

## 5. 检索备注

- 本文件资源均经 Web/HF/Zenodo/GitHub 检索汇总；DOI/星标/是否仍可下载需在纳入下载脚本前再核验一次。  
- 「待核实」项: 宽频 SSO 专用公开集、中文调度 CoT 语料、国内缺陷图库等价物。  
- 不绑定湖北/周口/冀北场景；场景仅可作为可选 stress profile，不进入目标 ID。
