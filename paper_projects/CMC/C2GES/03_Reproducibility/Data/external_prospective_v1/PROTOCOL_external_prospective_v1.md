# 外部前瞻评测协议 v1（冻结于跑分前）

冻结时间：2026-09-22（本文件与 `INVENTORY_ALL_RAW.json`、`INVENTORY_GRID_FAMILY.json` 的 SHA-256 一并冻结；**在任何评分运行之前**）。

## 0. 这一轮证据的类别（先声明，防止事后漂移）

这是 **prospective frozen external evaluation**：语料与协议在跑分前冻结并留哈希，但报告**不是**作者未查看过的语料（作者在获取过程中已打开、核验页数与摘要结构）。因此它可以支撑"在新机构、新系列上的冻结外测"，**不能**写成 author-attested unseen confirmatory，也不能关闭 `tab:e2-gate` 的第一行。

## 1. 语料来源与获取方式（均为公开可下载、权利清晰）

| 机构 | 获取方式 | 结果 |
|---|---|---|
| **ENTSO-E**（欧洲输电运营商联盟） | 用 Wayback CDX 枚举其公开对象存储 `eepublicdownloads.blob.core.windows.net` 下的 PDF（2,097 条 CDX 记录 → 1,994 个唯一 PDF），筛出事故类文档后**从 live blob 直连下载**（直连可用，无 403） | 下载 21 份，其中**电网事故族 7 份**、市场耦合事故族 11 份 |
| **NERC**（北美电力可靠性公司） | Wayback CDX 枚举 `nerc.com/globalassets/our-work/reports/`，取论文 40 篇抽样框**未使用过**的事件类报告，经 `web.archive.org/web/<ts>id_/` 下载（直连 403） | 下载 6 份（1 份含 Executive Summary，5 份为短 incident review） |

两个来源都是公开出版物；ENTSO-E 文档为其公开发布物，NERC 报告为公开监管文档。全部存放于发布范围之外的 `05_External_Prospective_20260922/`，不随投稿包或公开发布包分发。

## 2. 语料清单（按家族，含页数与摘要结构）

### 2.1 电网事故族（主家族，ENTSO-E）

| 文档 | 页 | 检测到 Summary | 备注 |
|---|---:|---|---|
| Final Report on the Grid Incident in Spain and Portugal on 28 April 2025 | 472 | Summary | 伊比利亚事件最终报告 |
| entso-e_incident_report_240621_250225_02（SEE 2024 最终版） | 146 | Summary | 与 interim 同族，保留最终版 |
| entso-e_grid_incident_240621_interim_factual_report（SEE 2024 中期版） | 96 | Summary | 与上一份重复，按去重规则排除 |
| ENTSO-E Interim (factual) Report … South-East Europe 21 June 2024 | 96 | Summary | 同上（URL 变体） |
| 251106_factual_report_on_MEPSO_incident_18_May_2025 | 90 | Summary | 2025 事故 |
| Nordic and Baltic Grid Disturbance Statistics 2018 | 96 | Executive Summary | 北欧-波罗的海扰动统计 |

### 2.2 市场耦合事故族（次家族，ENTSO-E SDAC/SIDC）

11 份（1–21 页），其中多数含 Executive Summary；代表：SDAC 2022-05-10、2023-10-28、2024-06-25、2024-07-24 部分解耦报告，SIDC IDA/IDCT 公共事故报告。该族是"市场运行事故"，与电网物理事故不同类，**单列**报告，不与电网族合并统计。

### 2.3 NERC 新系列（次要）

6 份；其中 `blackstart-resource-availability…-20251121`（36 页）含 Executive Summary 可用，其余 5 份短 incident review 无摘要章节，按入选门禁排除。

## 3. 冻结的协议规则

| 项 | 规则 | 与论文既有规则的关系 |
|---|---|---|
| 参考摘要检测 | 前 12 页内首个匹配 `^\s*(Executive\s+)?Summary\b`（大小写不敏感）的标题；候选单元取该摘要结束之后的正文 | 论文 NERC 版用 "Executive Summary"；本轮**显式放宽**到 Summary，属协议变更，已冻结在此 |
| 去重 | 标题归一化 + 页数一致时保留**最终版**（final > interim > note） | 新增 |
| 排除 | 无可检测参考摘要、正文候选区为空、PDF 不可解析者 | 与论文入选门禁同构 |
| 预算 | 110 与 260 词，整排序词预算选择器（不截断单元） | 与 RSI/后访问试点一致 |
| 比较对象 | no-path C²GES、Full C²GES（历史 utility，权重 0.10）、TextRank；若环境具备 MiniLM 快照则加 Semantic-MMR | 与 RSI 一致 |
| 端点 | 与官方摘要的 ROUGE-L F1 均值；补充 ROUGE-1/2 与冗余度 | 与论文主端点一致 |
| 分析单元 | 文档；家族（电网/市场耦合/NERC）作为分组，不跨家族合并 | 与论文"各研究不合并"一致 |
| 统计 | 与 no-path 的成对差；文档级 bootstrap 区间；若 n ≤ 20 则做精确符号翻转枚举并给 Holm；报告留一（leave-one-document-out）稳定性 | 与论文统计纪律一致 |
| 可声称 | "在新机构（ENTSO-E）新系列上的冻结外测中，路径项相对 no-path 的效应为 X" | — |
| 不可声称 | 未见确认、专家金标准、系统优越性、运维效用；不得与 NERC 15 题或 7 系列结果合并成总准确率 | — |

## 4. 执行顺序（冻结后）

1. 按 §3 规则构建候选/参考单元并输出构建清单（含每份文档的单元数、参考词数、边界哈希）；
2. 对同一候选集运行 no-path、Full(0.10)、TextRank（＋可选 Semantic-MMR）于 110/260 词；
3. 计算端点与统计，写出 `external_prospective_v1/` 结果目录；
4. 若结果方向与主结论一致或出现可解释的反转，再决定是否升级正文（新增小节 + 补充表 + 重建包 + 公共验证 + 发布清单）。

## 5. 冻结哈希

本协议与语料清单的字节身份记录在 `INVENTORY_ALL_RAW.json`（27 份 PDF 的 pages/bytes/sha256/摘要标记）。执行 §4 前不得再替换或新增语料；若必须变更，须另建 v2 协议并保留 v1 记录。

## 6. 修订 v1.1（2026-09-22，第一次构建运行之后、评分结果用于任何主张之前）

第一次构建运行（记为 **pilot run，不用于任何主张**）显示：按 v1 的"前 12 页内检测 Summary"规则，ENTSO-E 大型事件报告（如 472 页的伊比利亚最终报告、146 页的 SEE 报告）与 NERC 新报告全部被排除，仅 4 份文档通过，样本不足以支撑比较。

**修订内容（只放宽参考摘要的定位窗与标题长度，不改端点、预算、选择器、统计或语料清单）**：

| 项 | v1 | v1.1 |
|---|---|---|
| 摘要标题搜索窗 | 前 12 页 | **前 25 页** |
| 标题词数上限 | 6 | **8** |
| 其余规则（去重、候选最小单元数、预算、比较对象、端点、统计、可/不可声称） | 不变 | 不变 |

理由：大型机构事件报告的封面、目录、缩略语表通常占 10–20 页，正文摘要出现在 12 页之后属常规排版；v1 的窗口是照搬 NERC 短报告的排版，跨机构时不成立。

**纪律**：本次修订发生在任何评分结果被用于论文陈述之前；v1 pilot 的 n=4 结果仅作为构建诊断保留在 `external_prospective_v1_pilot.json`，不作为证据。

## 7. 修订 v1.2（2026-09-22，构建诊断之后、结果用于任何主张之前）

v1.1 之后仍只有 4 份文档通过，构建诊断（逐块打印候选标题）显示原因不是页面窗口，而是**标题词表**：ENTSO-E 的大型事件报告使用 **"MANAGEMENT SUMMARY"** 作为摘要章节标题（例如 472 页伊比利亚最终报告第 6 页、146 页 SEE 报告第 6 页），而 v1/v1.1 只匹配 `(Executive )?Summary`。

**修订内容**：参考标题正则放宽为 `^\s*(executive\s+|management\s+)?summary\b`（大小写不敏感）。其余规则全部不变。

**纪律**：此次修订同样发生在任何结果进入论文之前；v1.1 的 n=4 结果保留为构建诊断，不作为证据。
