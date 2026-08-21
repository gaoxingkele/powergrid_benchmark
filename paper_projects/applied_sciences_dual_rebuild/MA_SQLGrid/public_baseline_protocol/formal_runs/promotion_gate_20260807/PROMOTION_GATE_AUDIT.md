# MA-PUBLIC-BIRD-MINIDEV-v1.0（v1.0.1）晋级门禁独立审计报告

- 审计日期：2026-08-07
- 冻结 SHA-256：`c77699593d7752ffc2c5c0fa0e58ef4f48db1a05f2a827ff4dde1cb8c936a05b`
- 复执行环境：Python 3.10.11 / SQLite 3.40.1（钉住运行时 runtime_compat/python31011）
- 检查项：60/60 通过
- **门禁结论：PROMOTE**

## A. 完整性核验

全部 60 项程序化检查（manifest 字段与哈希绑定、模型文件 SHA-256、call_ledger 序号/重试/调用顺序一致性、提示词重渲染哈希绑定（含 B3 call2 动态替换重建）、final_scores 覆盖与全尝试分母、人类批准绑定、冻结输入哈希、11 库哈希、遗留 attempt 目录分离）：全部通过。

B3_EXEC_REPAIR call=2 的动态替换按 `run_formal_public_baseline.py:102-105` 原样复现：`{{FIRST_CANDIDATE_RUNTIME_MAX_400_TOKENS}}` ← 同题 call1 账本的完整 `extracted_sql`（占位符名含“400_TOKENS”但代码不做截断，本审计按代码语义执行）；`{{ONE_OF_FROZEN_FEEDBACK_VOCABULARY}}` ← call1 账本的 `validator_feedback`。两模型各 2500 条提示词哈希全部匹配。

遗留产物（均与 v101 正式目录完全分离，不属于本次审计计分范围）：
- `MA_PUBLIC_BIRD_v1_1_granite_clean1`：manifest=True，绑定 freeze=0aba454650c569d51183d4a96248ff977a5dbdf3a82a77c62592162f28f9f640
- `MA_PUBLIC_BIRD_v1_1_postrun_audit`：manifest=False，绑定 freeze=（无 RUN_MANIFEST）
- `MA_PUBLIC_BIRD_v1_1_qwen_clean1`：manifest=True，绑定 freeze=0aba454650c569d51183d4a96248ff977a5dbdf3a82a77c62592162f28f9f640
- `MA_PUBLIC_BIRD_v1_qwen`：manifest=False，绑定 freeze=（无 RUN_MANIFEST）
- `MA_PUBLIC_BIRD_v1_qwen_attempt2`：manifest=False，绑定 freeze=（无 RUN_MANIFEST）
- `MA_PUBLIC_BIRD_v1_qwen_attempt3`：manifest=False，绑定 freeze=（无 RUN_MANIFEST）

## B. 独立复执行（钉住运行时，只读沙箱，timeout 180s）

- 复执行行数：4000/4000；gold 缓存 500 条，全部 SAFE_EXECUTED：是
- prediction_status 不一致：0；official_ex 不一致：0
- 复执行 prediction_status 分布：{"SAFE_EXECUTED": 2420, "TYPE_OR_FUNCTION_ERROR": 218, "UNKNOWN_COLUMN": 928, "OTHER_EXECUTION_ERROR": 54, "AMBIGUOUS_COLUMN": 101, "PARSE_ERROR": 241, "UNKNOWN_TABLE": 32, "TIMEOUT": 6}
- 复执行总耗时：1316.7 s
- 不一致明细：无（4000/4000 逐行一致）。

## C. 统计表（数据库聚类 bootstrap，11 簇，10000 次重抽样，种子 20260807）

复执行与账本 4000/4000 一致，统计值与账本值相同。

### C1. 每模型 × 方法 EX（%，分母 500，全尝试分母）

| model | method | EX% | 95% CI |
|---|---|---|---|
| qwen | B0_DIRECT | 37.80 | [28.45, 47.01] |
| qwen | B1_DECOMP | 30.20 | [20.46, 40.21] |
| qwen | B2_SCHEMA_SELECT | 39.40 | [27.96, 51.42] |
| qwen | B3_EXEC_REPAIR | 34.80 | [25.05, 45.05] |
| granite | B0_DIRECT | 20.40 | [12.69, 28.30] |
| granite | B1_DECOMP | 21.00 | [13.05, 29.33] |
| granite | B2_SCHEMA_SELECT | 20.20 | [13.66, 27.20] |
| granite | B3_EXEC_REPAIR | 23.60 | [15.95, 31.92] |

### C2/C3. 配对差值 + Holm 校正（百分点）

| scope | 对比 | 差值 | 95% CI | p_raw | p_holm |
|---|---|---|---|---|---|
| within_model:qwen | B0_DIRECT - B1_DECOMP | 7.60 | [4.30, 11.21] | 0.0000 | 0.0000 |
| within_model:qwen | B0_DIRECT - B2_SCHEMA_SELECT | -1.60 | [-5.15, 2.16] | 0.4328 | 0.4328 |
| within_model:qwen | B0_DIRECT - B3_EXEC_REPAIR | 3.00 | [-0.19, 6.04] | 0.0680 | 0.1360 |
| within_model:qwen | B1_DECOMP - B2_SCHEMA_SELECT | -9.20 | [-13.33, -5.34] | 0.0000 | 0.0000 |
| within_model:qwen | B1_DECOMP - B3_EXEC_REPAIR | -4.60 | [-9.39, -0.59] | 0.0276 | 0.1104 |
| within_model:qwen | B2_SCHEMA_SELECT - B3_EXEC_REPAIR | 4.60 | [0.38, 8.76] | 0.0398 | 0.1194 |
| within_model:granite | B0_DIRECT - B1_DECOMP | -0.60 | [-4.36, 3.11] | 0.7998 | 1.0000 |
| within_model:granite | B0_DIRECT - B2_SCHEMA_SELECT | 0.20 | [-3.79, 4.23] | 0.9516 | 1.0000 |
| within_model:granite | B0_DIRECT - B3_EXEC_REPAIR | -3.20 | [-6.65, 0.42] | 0.0962 | 0.4810 |
| within_model:granite | B1_DECOMP - B2_SCHEMA_SELECT | 0.80 | [-4.28, 6.01] | 0.7850 | 1.0000 |
| within_model:granite | B1_DECOMP - B3_EXEC_REPAIR | -2.60 | [-8.37, 3.19] | 0.3878 | 1.0000 |
| within_model:granite | B2_SCHEMA_SELECT - B3_EXEC_REPAIR | -3.40 | [-6.53, -0.70] | 0.0132 | 0.0792 |
| between_models:qwen-granite | B0_DIRECT | 17.40 | [13.26, 20.78] | 0.0000 | 0.0000 |
| between_models:qwen-granite | B1_DECOMP | 9.20 | [4.00, 14.34] | 0.0008 | 0.0008 |
| between_models:qwen-granite | B2_SCHEMA_SELECT | 19.20 | [13.81, 24.91] | 0.0000 | 0.0000 |
| between_models:qwen-granite | B3_EXEC_REPAIR | 11.20 | [6.27, 16.57] | 0.0000 | 0.0000 |

### C4. 按数据库 EX 明细

见 `stats_by_database.csv`（88 行 = 2 模型 × 11 库 × 4 方法）。

## 门禁结论

**PROMOTE**。60/60 项检查全部通过：完整性核验（含提示词哈希绑定、人类批准绑定、遗留 attempt 分离）全部通过；4000 条最终预测与 500 条 gold 在钉住运行时（Python 3.10.11 / SQLite 3.40.1）下独立复执行，prediction_status 与 official_ex 逐行 100% 一致；统计表由复执行分数重新生成（与账本值相同）。

