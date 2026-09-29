# 新公开报告族外测：语料获取尝试与结论（2026-09-22）

## 目标

为 C²GES 补一条**预注册冻结的跨机构/新系列外部评测**：新报告族 → 冻结清单/切分/端点/排除规则 → 跑 C²GES(Full/no-path) 与 TextRank @110/260 词。要求：协议与清单在跑分前冻结并留哈希，跑完再开封；结论只能标为 "prospective frozen external evaluation"，不得写成 author-attested unseen。

## 尝试过的获取路径（全部实测）

| 来源 | 方法 | 结果 |
|---|---|---|
| NERC 报告页 | HTTP 抓取 sitemap 中 139 个候选页 | 页面为 JS 渲染，**0** 个 PDF 链接可静态提取 |
| NERC 直连 PDF | aria2c（带代理）直取 `nerc.com/globalassets/.../*.pdf` | **403**（站点屏蔽本环境直连） |
| NERC 归档 | Wayback CDX（`event-reports/` 前缀，33 条；`reports/` 前缀，596 条） | **枚举成功**；其中论文 40 篇抽样框**未使用过**的事件/事故类报告 6 篇 |
| NERC 归档下载 | `web.archive.org/web/<ts>id_/...` | **6 篇全部下载成功**（见 `INVENTORY_RAW.json`） |
| ENTSO-E | sitemap（404）、Azure 容器列表（`comp=list` 404）、出版物页（JS） | 无法枚举；仅能直连已知 blob URL |
| EIA | sitemap（133 URL）、8 个报告列表页 | 列表页**不含**直接 PDF 链接（报告以 HTML 发布） |
| DOE OE-417 / AEMO / NESO / GAO | 直连 | 000 / 403 / 403 / 403 |

## 拿到的语料与可用性判定

`source_pdfs/` 共 6 篇（Wayback 副本，NERC 公开报告，未在论文 40 篇抽样框内）：

| 报告 | 页 | 含 Executive Summary | 按论文入选门禁是否可用 |
|---|---:|---|---|
| blackstart-resource-availability-and-readiness…-20251121 | 36 | 是 | **可用**（有可检测的参考摘要 + 后摘要候选区） |
| incident-review-load-pocket-shoulder-season-challenges | 7 | 否 | 不可用（无可检测参考摘要，会被论文自身门禁排除） |
| incident_review_considering_voltage-sensitive_crypto_load_reductions | 10 | 否 | 不可用 |
| incident_review_future_wind_planning | 8 | 否 | 不可用 |
| incident_review_large_load_loss | 9 | 否 | 不可用 |
| incident_review_low_wind_event | 13 | 否 | 不可用 |

**结论（2026-09-22 更新）：该路线的结论已被后续突破取代。** 通过 Wayback CDX 枚举 ENTSO-E 公开对象存储，已从其 live blob **直连下载 21 份 ENTSO-E 事故类文档**（其中电网事故族 7 份、市场耦合事故族 11 份，页数 1–472，含 2025 伊比利亚事件最终报告与 2024 东南欧事件报告）；加上 NERC 的 6 份新报告，外部语料规模已足以支撑冻结外测。见 `PROTOCOL_external_prospective_v1.md` 与 `INVENTORY_ALL_RAW.json`。以下为原始尝试记录，保留作为负结果。

原始结论（仅 NERC 单来源时）：新语料只能支撑 1 篇（最多 2 篇）符合论文入选门禁的报告，低于论文 7 系列试点所能支撑的比较规模。

## 为什么不硬做

- 用 1–2 篇报告做"外部验证"会引入比结论更大的不确定性；论文自身的入选门禁（可检测参考摘要 + 非空后摘要候选区）会先排除其中 5 篇。
- 把 incident review 的 "Summary" 段改造成参考，会改变参考定义，属**方法改动**而非外部评测，必须另立协议与消融，不能塞进这一轮。
- 用合成报告或 LLM 生成报告补数会退化为 v8 合成压力集同类证据，论文已明确其不能支撑外部效度。

## 冻结与后续

- 本轮已把 6 篇 PDF 的字节身份写入 `INVENTORY_RAW.json`（pages / bytes / sha256 / exec-summary 标记）。这份清单**不用于跑分**，只作为"获取阶段"的如实记录。
- 打通外测仍需下列之一：① NERC 归档更广覆盖（该站 `reports/` 目录 CDX 已达 596 条，但同族事件报告已被论文抽样框覆盖大半；其余为 FRCC/NPCC/RFC 审计类，非同类叙事报告）；② 能静态枚举 PDF 的机构站（需逐站探测或站点 API）；③ 作者侧提供的权利清晰报告 PDF（用户表示无法人工补充）。
- 在此之前，C²GES 追加的对外证据保持为已落地的**相邻语域构念审计**（§4.10 + Table S9），不新增外部效度主张。
