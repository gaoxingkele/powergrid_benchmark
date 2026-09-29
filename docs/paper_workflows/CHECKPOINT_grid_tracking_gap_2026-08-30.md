# Checkpoint — 国网指南补数 / DataPort 缺口（2026-08-30）

**用途**：下次会话恢复 powergrid_benchmark 数据抓取与协作状态。  
**恢复口令**：`继续 grid_tracking gap checkpoint 2026-08-30`

---

## 1. 当前阻塞（P0）

| 事项 | 状态 | 说明 |
|------|------|------|
| IRTSD `Event_Data.zip` (~30 GB) | ⏳ 等丁威 | S3 URI 未在桶内自动发现 |
| FO `ksv8-sp77` / `FO_datasets.zip` (~5.3 GB) | ⏳ 等丁威 | 同上 |
| Test Cases Library `a6hg-n822` (~0.8 GB) | ⏳ 等丁威 | 同上 |

**已发邮件**（2026-08-28）：`dingwei@stu.xmu.edu.cn`，抄送 `iamafan@126.com`  
主题：【powergrid_benchmark 协作】请协助提供 IEEE DataPort 缺口数据集的 AWS S3 URI  
脚本：`D:\aicoding\mylib\email_tools\send_dataport_s3_uri_request.py`

**收到 URI 后**：
1. 粘贴到 `scripts/data_acquisition/download_dataport_gap_s3.py` → `GAP_DATASETS`
2. 设置 DataPort AWS 环境变量（见 `data/_grid_tokens/checkpoint_2026-08-30.json`，勿提交 git）
3. 运行：
   ```powershell
   $env:DATAPORT_AWS_ACCESS_KEY_ID = $env:AWS_ACCESS_KEY_ID
   $env:DATAPORT_AWS_SECRET_ACCESS_KEY = $env:AWS_SECRET_ACCESS_KEY
   python scripts/data_acquisition/download_dataport_gap_s3.py
   ```

---

## 2. 已完成 ✅

| 资源 | 约体积 | 路径 |
|------|--------|------|
| DPSYOR / DPSYFOR / IEEE9 TSA | ~354 GiB | `data/public_datasets/grid_tracking/datasets/dataport/` |
| OGE outputs 2023–2025 | ~3.5 GiB | `…/datasets/open_grid_emissions/` |
| PGLearn 14_ieee 全量 | ~5.3 GiB | `data/public_datasets/opf_benchmarks/pglearn_small/PGLearn-Small-14_ieee_full/` |
| CarbonX CI CSV | ~2.7 GiB | `…/datasets/carbonx/` |
| UTK WECC 振荡用例 | ~0.2 GiB | `…/datasets/oscillation_testcases_utk/` |
| SIIB-Time / EnEnv / InspecSafe 等 | 见 README | `data/public_datasets/grid_tracking/README.md` |

**磁盘**（2026-08-30）：D: **~47.5 GB 空闲**（补 IRTSD+FO+TestCases ~36 GB 仍够，勿并行 OPFData 全量）。

---

## 3. 仍未做 / 低优先级

| 资源 | 门槛 |
|------|------|
| OPFData 全量 | `gcloud` → `gs://gridopt-dataset/` |
| ACTIVSg 时序 | TAMU 填表 |
| IRTSD 脚本包 | `gap_dataport/irtsd_scripts/` 目录当前为空，可重跑 `download_dataport_gap_s3.py`（open-access 路径） |

---

## 4. 脚本与状态文件

| 文件 | 作用 |
|------|------|
| `scripts/data_acquisition/pull_grid_tracking_gaps.py` | OGE / PGLearn / CarbonX / UTK 批次 |
| `scripts/data_acquisition/download_dataport_gap_s3.py` | DataPort 缺口 S3（待 URI） |
| `scripts/data_acquisition/download_dataport_s3.py` | 已完成的三套 DataPort |
| `data/.../datasets/gap_pull_status.json` | 机器可读进度 |
| `data/.../datasets/dataport/download_status.json` | 354 GiB 批次校验 |

**PYTHONPATH**：`D:\aicoding\mylib`（`download_tools` 在此，非 `D:\aicoding\Lib`）

---

## 5. 邮件 / 全局配置

- SMTP 配置：`D:\aicoding\Lib\email_tools\xmu_mail_global_config.json`
- 发送 helper：`D:\aicoding\mylib\email_tools\xmu_send.py`
- 默认 Cc：`iamafan@126.com`

---

## 6. Semantic Scholar API（文献检索用，非 S3 必需）

- 环境变量：`S2_API_KEY`（见 gitignore 本地文件 `data/_grid_tokens/checkpoint_2026-08-30.json`）
- 与 DataPort 下载无关；用于 deep-research / 引文核实 / Prior art

---

## 7. 下次恢复建议步骤

1. 读本文 + `CHECKPOINT_grid_tracking_gap_2026-08-30.json`
2. 查丁威是否回复 S3 URI → 有则写入 `download_dataport_gap_s3.py` 并下载
3. 若无回复，可跟进邮件或浏览器 DataPort AWS tab 手工复制
4. 核对 D: 空闲 ≥ 40 GB 后再拉 IRTSD Event_Data
5. 更新 `grid_tracking/README.md` 与 `gap_pull_status.json`

---

## 8. 指南锚点

- 跟踪目标：`docs/benchmark_design/grid_tracking_targets.md`
- 国网策划对照：`docs/国网项目策划/`
- 缺口分析会话：agent transcript `2063a8c6-3953-41fe-b9d8-ccb4ce10cc4d`
