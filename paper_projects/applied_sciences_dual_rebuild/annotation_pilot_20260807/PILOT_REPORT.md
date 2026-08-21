# 双模型独立标注 + 第三模型裁决 Pilot 报告

- 日期：2026-08-07
- 运行器：`run_annotation_pilot.py`（同目录），`--paper c2ges|ma|both [--limit N]`
- 冻结协议（运行前已校验 SHA-256，不匹配即中止）：
  - `C2GES_ANNOTATION_PROTOCOL_v1.json` = `030ae44a…dc706d` ✔
  - `MA_SQLGRID_ANNOTATION_PROTOCOL_v1.json` = `6d5a0398…dd1ff5` ✔
- **全部产出均为 machine-adjudicated silver labels，不是 human/expert gold，不得以此名义引用。**

## 模型角色

| 角色 | 提供方 | 冻结 model id | 实际 served id | 说明 |
|---|---|---|---|---|
| 标注器 A | DeepSeek 直连 | `deepseek-chat` | `deepseek-v4-flash` | 滚动别名，任务简报中已声明为预期行为，逐次记录，不触发停止门禁 |
| 标注器 B | Google Gemini 直连 | `gemini-2.5-flash` | `gemini-2.5-flash` | 一致 |
| 裁决器 C | Cloubic 网关 | `gpt-5.4` | `gpt-5.4` | 一致 |

生成参数：temperature=0，max_tokens/maxOutputTokens=1024，要求只输出单个 JSON 对象。
唯一补充：Gemini 侧设置 `thinkingConfig.thinkingBudget=0`（见"冒烟测试发现的问题"），输出上限仍为 1024。

## 冒烟测试发现的问题（正式运行前修复）

正式运行前按流程先跑 2+2 条冒烟。发现两个**运行器侧**缺陷（非模型行为）：

1. 冻结的 prompt_template 的 `[QUESTION]` 行不含 qid/question_id，而冻结的确定性检查要求"qid 回显输入"——该检查在原始模板下不可能通过（冒烟中三个模型全部自行编造 qid，100% format failure）。修复：在 `[QUESTION]` 行中显式给出 id 并要求逐字回显（`[QUESTION] (qid: …, role: …) …`），这是对冻结模板为满足其自身冻结检查所做的最小补充，在此披露。
2. `gemini-2.5-flash` 是思考型模型，思考 token 会吞掉 1024 输出预算，导致 JSON 被截断（冒烟中 B 输出仅 38–53 token 即断）。修复：`generationConfig` 增加 `thinkingConfig: {thinkingBudget: 0}`，输出上限保持 1024 不变。

冒烟共产出 14 次 LLM 调用，全部记录**未删除**，归档于 `runs/_smoke_archive_20260807/`（含 README 说明），不计入正式 pilot 统计（测量工具不合规），但计入 400 次全局调用上限。

## C2GES pilot（NERC 证据标注，25 题）

- 抽样：`random.Random(20260807)` 对 75 题洗牌后三轮选取（先覆盖 15 文档 → 补齐 5 种 role → 填满 25），清单冻结于 `runs/c2ges_pilot/sample_manifest.json`。实际覆盖 15/15 文档、5/5 role。
- 完成：25/25，无 format failure、无 API 失败、无弃权遗留。

| 指标 | 数值 |
|---|---|
| A/B answerable 原始一致率 | 0.88（22/25） |
| answerable Cohen's kappa | 0.00（B 全部判 true、A 22/25 判 true，边际分布极端偏斜使 pe=0.88=po，kappa 无区分度，仅供参考） |
| evidence sid 集合完全一致率 | 0.28（7/25） |
| evidence Jaccard 均值 | 0.5505 |
| evidence_role 不一致对数 | 5/25 |
| 裁决率 | 0.76（19/25；触发原因：answerable 不一致 3、sid 集合不一致、evidence_role 不一致、A 弃权 2） |
| 弃权率 | A 2/25，B 0/25，C 0/19 |
| 格式失败率 | 0（A 0/25，B 0/25，C 0/19） |
| API 失败率 | 0（本次正式运行 69 次调用全部成功） |

Token 与延迟（C2GES）：

| 模型 | 调用 | input tokens | output tokens | 平均延迟 | 中位延迟 |
|---|---|---|---|---|---|
| A (deepseek-v4-flash) | 25 | 84,971 | 5,634 | 2.36s | 2.27s |
| B (gemini-2.5-flash) | 25 | 96,221 | 6,715 | 3.20s | 3.03s |
| C (gpt-5.4) | 19 | 75,683 | 4,285 | 5.35s | 5.38s |

三家提供方本次均返回了 usage 字段（Gemini 为 `usageMetadata`），无 null 缺口。

最终结论汇总（qid → A / B / C / final；完整证据 sid 见 `final_labels.jsonl`）：

| qid | A | B | C | final answerable | final evidence |
|---|---|---|---|---|---|
| nerc_035…technical::mitigation | ans=T | ans=T | adjudicated | true | s012 |
| nerc_028…assessment::propagation_or_response | abstain | ans=T | adjudicated | true | s001,s009,s025,s026 |
| nerc_030…blac::trigger_event | ans=T | ans=T | adjudicated | true | s008,s009 |
| nerc_042_2016…::root_cause | ans=F | ans=T | adjudicated | true | s036 |
| nerc_029…elliott_report::trigger_event | ans=T | ans=T | adjudicated | true | s031 |
| nerc_032…eip::root_cause | ans=T | ans=T | adjudicated | true | s004 |
| nerc_027…loss_of_::impact | ans=T | ans=T | –（一致） | true | s005 |
| nerc_031…8_and_::trigger_event | ans=T | ans=T | adjudicated | true | s001,s005 |
| nerc_026_aep…::trigger_event | ans=T | ans=T | –（一致） | true | s001,s023 |
| nerc_036_2022…::trigger_event | ans=T | ans=T | –（一致） | true | s039 |
| nerc_047_lessons…::mitigation | ans=T | ans=T | –（一致） | true | s049 |
| nerc_034_2025…overview::root_cause | ans=T | ans=T | adjudicated | true | s031 |
| nerc_033_2025…technical::mitigation | ans=T | ans=T | adjudicated | true | s055,s056,s057 |
| nerc_041_2017…::propagation_or_response | ans=T | ans=T | adjudicated | true | s058,s059,s060,s062,s063,s064 |
| nerc_040_2018…::mitigation | ans=T | ans=T | adjudicated | true | s015,s016,s017 |
| nerc_028…assessment::impact | ans=T | ans=T | –（一致） | true | s004 |
| nerc_030…blac::root_cause | ans=T | ans=T | adjudicated | true | s015,s023,s031,s040,s050,s063 |
| nerc_029…elliott_report::root_cause | ans=T | ans=T | adjudicated | true | s042,s043 |
| nerc_035…technical::propagation_or_response | ans=T | ans=T | adjudicated | true | s008,s009,s011 |
| nerc_030…blac::propagation_or_response | ans=T | ans=T | adjudicated | true | s002,s010 |
| nerc_028…assessment::root_cause | ans=T | ans=T | adjudicated | true | s015,s016,s074,s076,s079,s080 |
| nerc_029…elliott_report::propagation_or_response | ans=T | ans=T | adjudicated | true | s047,s053,s056,s058,s061–s065 |
| nerc_032…eip::trigger_event | ans=T | ans=T | –（一致） | true | s001 |
| nerc_029…elliott_report::mitigation | ans=T | ans=T | adjudicated | true | s044,s053,s056,s058,s061,s063,s064,s066,s067,s069 |
| nerc_031…8_and_::impact | abstain | ans=T | adjudicated | true | s006 |

解读：answerable 层面一致性高（0.88），但证据句选择分歧大（完全一致仅 0.28），76% 的条目进入裁决——说明"最小充分证据集"的界定是主要分歧源，裁决器负担重，后续扩大规模前值得在协议中细化证据充分性准则。

## MA-SQLGrid pilot（候选参考 SQL 审核，25 条）

- 抽样：`random.Random(20260807)`，RTS 55 → 14、SimBench 36 → 11（各自按 template_family 洗牌后轮转抽取），清单冻结于 `runs/ma_pilot/sample_manifest.json`，覆盖 17 个 template_family。
- 确定性沙箱：25/25 条候选 SQL 在提示任何 LLM **之前**完成只读执行（URI `mode=ro`、`PRAGMA query_only=ON`、authorizer 拒绝写操作、10s 超时、5000 行上限），**25/25 可执行、0 错误**，事实记录于 `runs/ma_pilot/execution_facts.jsonl`。
- 完成：25/25，无 format failure、无 API 失败。

| 指标 | 数值 |
|---|---|
| A/B semantically_correct 原始一致率 | 1.00（25/25） |
| semantically_correct Cohen's kappa | 不可计算（双方全部判 true，单一类别，pe=1，kappa 无定义） |
| 裁决率 | 0.00（0/25；answerable_by_schema、semantically_correct、error_classification 三项全部一致，且无弃权） |
| 弃权率 | A 0/25，B 0/25 |
| 格式失败率 | 0 |
| API 失败率 | 0（本次 50 次调用全部成功） |

Token 与延迟（MA）：

| 模型 | 调用 | input tokens | output tokens | 平均延迟 | 中位延迟 |
|---|---|---|---|---|---|
| A (deepseek-v4-flash) | 25 | 25,196 | 4,136 | 1.67s | 1.66s |
| B (gemini-2.5-flash) | 25 | 27,769 | 5,025 | 2.79s | 2.25s |
| C (gpt-5.4) | 0 | – | – | – | – |

最终结论汇总（question_id → A / B / C / final）：25 条全部为 `A=sem=true, B=sem=true, error_classification=none, final_source=agreement`，即两个独立标注器一致认为全部 25 条候选 SQL 在 schema 下可回答且语义正确（RTS_AUTO_002/005/008/013/016/024/030/031/033/037/042/045/046/051；SB-AUTO-001/006/010/015/017/021/023/027/028/033/035）。

解读：0 裁决、κ 无定义说明该 auto-candidate 集合在本抽样下"质量过好、无区分度"——两个标注器找不到任何可分歧点。这是抽样本的观察结果，不能外推为"91 条候选全部正确"，更不能表述为外部 gold 准确率。若后续需要区分度，应考虑注入已知错误的负样本对标注器做探测性验证。

## 停止门禁合规声明

| 门禁 | 结果 |
|---|---|
| 同一模型连续 5 次鉴权/格式失败 → 停止 | 未触发（正式运行 0 次鉴权失败、0 次格式失败） |
| served model id 与冻结不符 → 停止 | 未触发。A 的 served id 恒为 `deepseek-v4-flash`，属任务简报中声明的 `deepseek-chat` 滚动别名，逐次记录于 raw ledger 与 gate 事件日志；B、C 与冻结 id 完全一致 |
| 总调用数 ≤ 400 | 合规：合计 **133 次**（正式运行 119 + 归档冒烟 14），其中 A 50、B 50、C 19、冒烟 14 |

其他治理红线：失败/分歧记录全部保留（含归档的冒烟记录）；未发生任何"因不喜欢结果而重试"（唯一重试机制是技术失败——超时/5xx/网络错误——自动重试 1 次并双条记录，正式运行未用到；归档冒烟中 DeepSeek 曾出现 ~120s 网络错误 3 次，重试成功 1 次）；API key 仅从 `.env`/`.env.cloubic` 环境文件读取，任何日志/账本/输出中均无 key（ledger 仅记录 prompt 的 SHA-256）；数据库全程只读，未做任何修改；未上传任何超出公开 NERC 数据包与既有 auto-candidate 工件的内容。

## 产出文件清单

```
annotation_pilot_20260807/
├── run_annotation_pilot.py                 # 运行器（含门禁/账本/沙箱/统计）
├── PILOT_REPORT.md                         # 本报告
├── runs/
│   ├── _smoke_archive_20260807/            # 冒烟记录归档（14 次调用，未删除，附 README）
│   ├── c2ges_pilot/
│   │   ├── sample_manifest.json            # 冻结抽样清单（25 题）
│   │   ├── raw_ledger.jsonl                # append-only 原始响应账本（69 条调用记录）
│   │   ├── labels_A.jsonl / labels_B.jsonl # 解析后标签 + 确定性检查结果
│   │   ├── adjudicated.jsonl               # 19 条裁决记录（含匿名化映射、adjudication_note）
│   │   ├── final_labels.jsonl              # 25 条最终 silver 标签
│   │   └── stats.json                      # 机器可读统计
│   └── ma_pilot/
│       ├── sample_manifest.json            # 冻结抽样清单（14 RTS + 11 SimBench）
│       ├── execution_facts.jsonl           # 沙箱执行事实（账本组成部分）
│       ├── raw_ledger.jsonl                # 50 条调用记录
│       ├── labels_A.jsonl / labels_B.jsonl
│       ├── final_labels.jsonl              # 25 条最终 silver 标签（全部 agreement）
│       └── stats.json
│       （无 adjudicated.jsonl：裁决率 0，未产生裁决记录）
```

再次声明：以上全部标签为 **machine-adjudicated silver labels**，不构成 human/expert gold，也不得作为外部 gold 准确率引用。
