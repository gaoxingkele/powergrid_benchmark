# Grid Tracking Bundle — 下载清单（含补全批次）

**更新**: 2026-08-28  
**脚本**:
- `download_grid_tracking_bundle.py`（首批）
- `fill_grid_tracking_gaps.py`（论文+中小数据补全）
- `pull_grid_tracking_large.py`（大包后台：PROTECT-90 / InspecSafe / SIIB-Time）
- `pull_grid_tracking_gaps.py` / `download_dataport_gap_s3.py`（2026-08-28 国网指南补数）

## 论文

路径：`papers/literature/grid_tracking_targets/pdfs/`  
当前有效 PDF：**52 篇**（含 dataset_literature 批次 +16）。索引见 `papers/literature/grid_tracking_targets/metadata/dataset_literature_index.md`。

补全批次新增（节选）：
| 方向 | 论文 |
|---|---|
| T07 振荡 | Forced oscillation locating with IBR (arXiv:2508.17505) |
| T09 巡检 | InspecSafe-V1 arXiv:2601.21173 |
| T12 故障 | PROTECT-90 论文 + ML fault comparison |
| T04 VPP | EnEnv AAMAS 2025 |
| T14 电氢 | PyPSA-Eur sector-coupled |
| T11 碳 | Open Grid Emissions methods |
| T22 PMU | GNN PMU event detection |
| T18 预报 | SDWPF Scientific Data |
| T16 OPF | Scalable heterogeneous GNN OPF |
| T05 气象功率 | FuXi-Energy 相关 OA |

## 数据集

| 资源 | 状态 | 路径 / 说明 |
|---|---|---|
| SMIB PINN CSV | ✅ | `datasets/smib_pinn/` |
| MAPDN HF zips | ✅ | `datasets/mapdn/` ~6.0GB |
| WindFM 权重 | ✅ | `datasets/windfm/NeoQuasar_WindFM/` |
| IEEE33+DER 故障 xlsx | ✅ | `datasets/fault_location/` |
| PROTECT-90 labels+README | ✅ | `datasets/protect90/` |
| PROTECT-90 波形 zip (~12GB) | ✅ | `protect90/hv_double_line_90kv_preprocessed_data.zip` |
| 瑞士 DER 分配 zip | ✅ | `datasets/swiss_der_allocation/SwissDN_DERs.zip` ~4.5GB |
| UCI 电网稳定 CSV | ✅ | `datasets/uci_electrical_grid_stability/` |
| InspecSafe-V1 (~23.6GB) | ✅ | `datasets/inspecsafe/` |
| SIIB-Time 全量 (~44.4GB) | ✅ | `datasets/siib_time_full/`（18009 files） |
| WindFM Tokenizer | ✅ | `datasets/windfm/` |
| DPSYOR / DPSYFOR / IEEE9 DataPort | ✅ | `datasets/dataport/`（15 文件，约 354 GiB，已校验） |
| EnEnv 场景包 | ✅ | `datasets/enenv/scenarios/`（3 场景完整 ~7.96GB） |
| OGE outputs 2023–2025 | ✅ | `datasets/open_grid_emissions/` ~3.7GB |
| PGLearn 14_ieee 全量 | ✅ | `opf_benchmarks/pglearn_small/PGLearn-Small-14_ieee_full/` ~5.7GB |
| CarbonX CI CSV | ✅ | `datasets/carbonx/` ~2.9GB |
| IRTSD 脚本/文档 | ✅ | `datasets/gap_dataport/irtsd_scripts/` |
| UTK WECC 振荡用例 | ⏳ | `datasets/oscillation_testcases_utk/` |

## 仍需人工 / S3 URI

| 资源 | 约体积 | 操作 |
|---|---|---|
| IRTSD Event_Data | ~30 GB | DataPort 登录 → AWS S3 tab → 写入 `download_dataport_gap_s3.py` |
| FO ksv8-sp77 | ~5.3 GB | 同上 |
| Test Cases Library (14bus PoW 等) | ~0.8 GB | 同上 |
| OPFData 全量 | 数十 GB | 安装 `gcloud` → `gs://gridopt-dataset/` |
| ACTIVSg 时序 | 视案例 | TAMU 填表下载 |

状态 JSON：`datasets/gap_pull_status.json`

## 复现

```powershell
$env:PYTHONPATH = "D:\aicoding\mylib;$env:PYTHONPATH"
python scripts/data_acquisition/fill_grid_tracking_gaps.py
python scripts/data_acquisition/pull_grid_tracking_large.py
```
