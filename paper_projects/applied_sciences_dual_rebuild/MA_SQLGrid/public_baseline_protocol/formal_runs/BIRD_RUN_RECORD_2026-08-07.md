# BIRD Mini-Dev 公开基线正式运行记录（MA-PUBLIC-BIRD-MINIDEV-v1.0, 修订 v1.0.1）

**完成日期：** 2026-08-07
**授权：** DONG LUN HAI，2026-08-07（`../../human_launch_approval_bird_20260807.json`；重签绑定修订后冻结哈希）
**冻结 SHA-256：** `c77699593d7752ffc2c5c0fa0e58ef4f48db1a05f2a827ff4dde1cb8c936a05b`（FROZEN_NOT_RUN，12/12 门禁；独立审计 39/39 PASS）
**运行时：** 钉住 Python 3.10.11 / SQLite 3.40.1（runtime_compat），llama.cpp b9637，RTX 3090，单服务器串行

## 正式运行产物（本目录下，immutable）

| 模型 | 目录 | 调用 | 最终行 | 重试 | manifest |
|---|---|---|---|---|---|
| Qwen2.5-Coder-7B-Instruct q4_k_m | `MA_PUBLIC_BIRD_v101_qwen/` | 2500 | 2000 | 0 | formal_run_complete: true |
| Granite-3.3-8B-Instruct Q4_K_M | `MA_PUBLIC_BIRD_v101_granite/` | 2500 | 2000 | 0 | formal_run_complete: true |

- Qwen 账本哈希：call_ledger `1893957f…b7ab2`，final_scores `1266fbca…b0a797`
- Granite 账本哈希：call_ledger `3fa344ad…0677ae`，final_scores `a88cb2b6…ede05d6`
- 预测状态分布（运行健康指标，非论文结果）：Qwen SAFE_EXECUTED 1420/2000，含 OTHER_EXECUTION_ERROR 12；Granite SAFE_EXECUTED 1000/2000，含 OTHER_EXECUTION_ERROR 42

## 事件链（全部保留，不可用于分数）

- `INCIDENT_20260807_qwen_attempt1.md`：三次失败尝试的完整记录
  - attempt 1（旧冻结）：llama-server 原生进程无声崩溃，261 调用
  - attempt 2（旧冻结）：操作失误——误用系统 Python 3.12/SQLite 3.49.1，Q701 gold 超时中止，341 调用
  - attempt 3（旧冻结）：2135/2500 处撞冻结代码缺陷（sqlite3.Warning 未分类），促成修订 v1.0.1
- 修订 v1.0.1 内容见 `../BASELINE_PROTOCOL_FREEZE.md` 末尾 Amendment 节；三个失败目录 `MA_PUBLIC_BIRD_v1_qwen{,_attempt2,_attempt3}/` 原样保留

## 晋级门禁（未完成前分数不得入稿）

按 FORMAL_RUNBOOK.md：独立审计员须复执行全部 4000 个最终预测、核验 5000 条唯一调用记录、零重试/零丢弃、提示词/模型/数据/运行时哈希、官方 EX 集合语义，并从 immutable 账本重新生成数据库聚类区间与 Holm 校正表。在此完成前，本记录不含、也不得被引用为论文结果数字。

## 晋级门禁结果（2026-08-07，delegated independent technical agent）

**PROMOTE——60/60 检查全部通过，复执行 4000/4000 行与账本零不一致。**

- 审计目录：`promotion_gate_20260807/`（PROMOTION_GATE_AUDIT.json/.md + 统计表 + 可复现脚本）
- 复执行环境：钉住 Python 3.10.11 / SQLite 3.40.1，官方评估器哈希 `da1bbcd4…cf89` 一致
- 核验覆盖：manifest/冻结/模型/账本哈希绑定、2500 调用唯一性与顺序、提示词逐条哈希绑定（含 B3 动态替换原样复现）、2000 最终行覆盖、批准文件绑定、失败 attempt 目录分离
- 从此刻起，下列 EX 数字可用于 MA-SQLGrid 稿件（%，分母 500，db 聚类 bootstrap 95% CI）：

| model | B0_DIRECT | B1_DECOMP | B2_SCHEMA_SELECT | B3_EXEC_REPAIR |
|---|---|---|---|---|
| qwen | 37.80 [28.45, 47.01] | 30.20 [20.46, 40.21] | 39.40 [27.96, 51.42] | 34.80 [25.05, 45.05] |
| granite | 20.40 [12.69, 28.30] | 21.00 [13.05, 29.33] | 20.20 [13.66, 27.20] | 23.60 [15.95, 31.92] |

- 模型间差值（qwen−granite，Holm 校正）：四个方法 +9.2pp ~ +19.2pp，全部 p_holm ≤ 0.0008；模型内方法差仅 qwen 的 B0−B1 与 B1−B2 显著
- 注意：审计发现遗留目录 `MA_PUBLIC_BIRD_v1_1_*_clean1` 绑定另一冻结哈希 `0aba4546…f640`（非本次授权范围），已记录在审计 JSON 的 legacy_artifacts，使用前需另行甄别
