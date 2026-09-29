# Grid-Tracking Dataset Literature Index

**更新**: 2026-08-24  
**路径**: `papers/literature/grid_tracking_targets/pdfs/`  
**总量**: 52 篇有效 PDF（本批新增 16）  
**脚本**: `scripts/data_acquisition/download_grid_tracking_dataset_literature.py`

## 按数据集映射

| dataset_id | 原论文 (primary) | 引用/相关 (citing/related) | 备注 |
|---|---|---|---|
| `grid_tracking_enenv` | EnEnv AAMAS 2025 | BenchMARL (arXiv) | EnEnv 太新，正式引用尚少 |
| `grid_tracking_mapdn` | MAPDN NeurIPS 2021 (+ arXiv) | SafetyLayer AAMAS 2023 · SafetyConstrained arXiv · OffTheGrid AAMAS 2023 · AAAI 2024 · Applied Energy 2025 综述 | MAPDN 引用生态最成熟 |
| `grid_tracking_protect90` | PROTECT-90 arXiv 2026 | ML fault comparison arXiv 2025 | 数据集刚发布，引用待增长 |
| `grid_tracking_inspecsafe` | InspecSafe Sci Data + arXiv | SafeSceneReason · SteelBench (arXiv) | 工业巡检/VLM 邻域 |
| `grid_tracking_siib_time` | HF datacard（独立论文待发布） | Neural Operators arXiv · Microgrid DT arXiv · IBR datagen | SIIB 主文可能在 NeurIPS PSML 流程 |
| `grid_tracking_smib_pinn` | Zenodo 19562416（IEEE Access 稿待刊） | PINN V&V SMIB arXiv · 既有 PINN-TSA 文 | 统一 SMIB 主文 OA 未公开 |
| `grid_tracking_swiss_der` | SwissDER Sci Data 2025 | SEGAN 2025 规划文 | **SEGAN 全文 Elsevier 403，待机构订阅** |
| `grid_tracking_fault_location_ieee33` | Zenodo 15210584（ISGT 2025 配套） | Data-driven fault localization Energies 2020 | ISGT 主文 IEEE 需账号 |
| `grid_tracking_uci_grid_stability` | DSGC EPJ 2016 (arXiv) | Smart-grid stability Energies 2020 | UCI 无独立论文，用理论+应用文 |

## 本批新增 PDF（16）

| PG-T | 文件 | 角色 | venue |
|---|---|---|---|
| T01 | PINN_surrogate_VV_framework_SMIB | related | arXiv |
| T03 | SwissDER_SciData_2025 | primary | Scientific Data |
| T04 | BenchMARL_benchmarking_MARL | framework | arXiv |
| T04 | MAPDN_NeurIPS2021_proceedings | primary | NeurIPS 2021 |
| T04 | MAPDN_SafetyConstrained_AVC | citing | arXiv |
| T04 | MAPDN_SafetyLayer_AAMAS2023 | citing | AAMAS 2023 |
| T04 | OffTheGrid_MARL_datasets_baselines | citing | AAMAS 2023 |
| T04 | MAPDN_AAAI_Imagine_Initialize_Explore_2024 | citing | AAAI 2024 |
| T04 | MAPDN_AppliedEnergy_data_driven_control_2025 | citing | Applied Energy (作者预印) |
| T09 | SafeSceneReason_industrial_hazard_benchmark | citing | arXiv |
| T09 | SteelBench_VLM_industrial_environments | citing | arXiv |
| T10 | DSGC_Taming_instabilities_power_grid_EPJ | primary | EPJ/arXiv |
| T10 | Smart_grid_stability_prediction_Energies | citing | Energies |
| T12 | Data_driven_fault_localization_DER_Energies | related | Energies |
| T13 | Neural_Operators_power_system_components | related | arXiv |
| T13 | Microgrid_digital_twin_dataset_IBR | related | arXiv |

## 未能 OA 下载（待人工）

| 论文 | DOI | 原因 |
|---|---|---|
| SwissDER SEGAN 规划文 | 10.1016/j.segan.2025.101678 | Elsevier 403 |
| IEEE33 fault ISGT 2025 | 10.1109/isgteurope64741.2025.11305498 | IEEE 需订阅 |
| SMIB unified PINN IEEE Access | 待刊 | 尚未公开 OA |
| SIIB-Time 主文 | HF DOI 10.57967/hf/8655 | 数据集卡已发布，独立论文待核实 |

## 复现

```powershell
$env:PYTHONPATH = "D:\aicoding\mylib;$env:PYTHONPATH"
python scripts/data_acquisition/download_grid_tracking_dataset_literature.py
```
