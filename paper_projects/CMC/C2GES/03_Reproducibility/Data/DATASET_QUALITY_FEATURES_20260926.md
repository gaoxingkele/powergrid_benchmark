# C2GES 数据集特征总结：支撑实验结果的"优质数据集"画像

日期：2026-09-26。范围：C²GES（Information 在投）全部五层语料。
判定口径：所谓"优质支撑"= 实验结论的可信度直接依赖该层数据的这些工程与治理特征；每层列出其支撑的具体结果、特征清单、原始数据位置与发布边界。

## 总览

| 层 | 语料 | 规模 | 支撑的结果 | 声称边界 |
|---|---|---|---|---|
| L1 | 历史 NERC 语料 | 27 份 = 12 开发 + 15 保留测试 | 历史 K=5 系统对比（Full 对 Semantic-MMR/TextRank 的 Holm 0.0117 胜出）、等单位长度诊断 | post-access，非未见确认 |
| L2 | 七系列试点语料 | 7 份，3 组织 7 系列 | 匹配词预算析因（角色层 +0.0186 [0.0078, 0.0320]；AB-0–6/RP/G-U-G-T 全链） | post-access exploratory |
| L3 | 外部前瞻语料 | 19 份（6 ENTSO-E 电网 + 7 市场耦合 + 6 NERC） | §4.4 外部复现：TextRank−no-path @260 +0.022940（Holm 0.0324）；Full−no-path @260 −0.002906（Holm 0.0469，7 负 0 正） | prospective frozen external，非未见 |
| L4 | 构念审计语料 | GUM 64 文档 / EBM-NLP 191 摘要 | §4.11 角色线索精确率 0.610/0.807（召回 0.064/0.060） | 相邻语料，不关闭证据门 |
| L5 | 合成 fixtures | 虚构文本若干 | §4.6 负对照（Holm 调整后路径对比 p=1.0） | 仅压力测试 |

另有开发期校准语料（12 份开发报告复用 L1 开发侧）：147 组配置 12/12 折选零路径权重、路径长度 3/4/5 的相邻 Spearman 稳定性 0.979–1.000。

## 逐层特征

### L1 历史 NERC 语料（主结果的骨架）

**支撑结果**：历史保留测试层的系统对比、端点贡献分解（§4.7–4.10）、输出长度诊断（§4.8）。

**优质特征**：
1. **真实公开来源 + 逐份权利台账**：全部为 NERC 官方公开事故报告；`rights_ledger.csv/.jsonl` 逐份记录 source_url、SHA-256、获取日期、权利状态与转发限制——每条数据可回溯到原始 URL。
2. **抽样框透明**：40 份完整检查 → 27 份保留，13 份排除的逐条理由写入补充材料 Table S1；排除发生在结果计算之前。
3. **开发/测试硬隔离**：12 份开发 + 15 份保留测试，冻结后不再改动（`TEST_FREEZE_MANIFEST_v0_3_1.json` 哈希锁定）。
4. **参考摘要与正文结构性分离**：Executive Summary 检测规则文档化，`reference_provenance` 逐份标注；参考文本不参与候选。
5. **布局与编码审计随数据走**：505 个表格区域检测零页级失败；12,924 个候选单元的 tokenizer 暴露审计（仅 0.294% 超 256 token）。
6. **报告级分析单元**：明确候选单元不独立、推断以报告为单位，避免伪重复。

**原始数据位置**：
- 原始 PDF：`data/public_datasets/reliability_reports/c2ges_nerc_reports/raw_pdfs/`（27 份，逐份 SHA-256）；
- 权利台账与派生数据集：`paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_rebuild/R2_v0_3/diagnostic_build_08/`（`nerc_full_pdf_dev_v0_3.jsonl`、`nerc_full_pdf_test_v0_3.jsonl`、`rights_ledger.*`、`per_report_extraction_audit.jsonl`）；
- 证据锁：`03_Reproducibility/Data/submission_final/DIAGNOSTIC_SUBMISSION_EVIDENCE_LOCK.json`。

### L2 七系列试点语料（角色层正结果的载体）

**支撑结果**：§4.2–4.3 匹配词预算（110/260 词）下的组件析因；角色证据 +0.0186（区间 [0.0078, 0.0320]）与角色线索精确率进入摘要的唯一正结果。

**优质特征**：
1. **跨组织分层**：7 份报告分属 ENTSO-E、NERC、Transpower 三个机构的 7 个独立事件系列，系列间机构语言不互相泄漏（LOSO 逐系列敏感性随包）。
2. **匹配信息预算设计**：110/260 词预算直接消解历史层的等单位长度混杂——该层是"先诊断问题、再修正设计"的产物，证明数据集迭代受分析驱动而非结果驱动。
3. **诚实分级**：因协议冻结前已接触来源，主动降级为 post-access exploratory（`README.md` 开篇即声明不能支撑 E1 未见声称）——不冒称是它能进入论文的前提。
4. **析因全覆盖**：AB-0–AB-6 增量链 + RP 2×2 + G-U/G-T 在**同一候选集、同一预算**下运行，组件效应可归因。

**原始数据位置**：
- 原始 PDF：`03_Reproducibility/Data/exploratory_external_v0/source_pdfs_private/`（7 份，私有，README 说明原因）；
- 派生数据集：`derived_private/exploratory_reports_v3.jsonl`（哈希锁定于 `BUILD_MANIFEST_v3.json`）；
- 发布件（非逐字）：`EXPLORATORY_EXTERNAL_INVENTORY.csv`、各 `e1/e3` 运行目录的聚合 CSV 与 `factorial_selected_ids.jsonl`。

### L3 外部前瞻语料（外部复现层）

**支撑结果**：§4.4 外部复现——唯一过 Holm 校正的系统级对比（TextRank 优势）与路径项的显著负效应。

**优质特征**：
1. **协议先于跑分冻结**：`PROTOCOL_external_prospective_v1.md` 冻结于结果计算之前，且保留 v1.1（摘要搜索窗）、v1.2（Management Summary 标题）、v1.3（章节号前缀）、v1.4（参考 ≥100 词、候选上限 2000）四段修订记录——冻结后修订全部留痕。
2. **系列与历史语料不相交**：含 2024 南欧、2025 伊比利亚等近期事件；与 L1/L2 不合并、不混池。
3. **组成与抽取规则全文档化**：6 电网事故 + 7 市场耦合 + 6 NERC；候选 21–2,000 单元、参考 102–10,935 词；pymupdf4llm 结构化 Markdown 抽取 + 摘要标题检测规则（Executive/Management Summary/Summary）写入协议。
4. **逐文件哈希清单**：`INVENTORY_ALL_RAW.json` / `INVENTORY_GRID_FAMILY.json` + 获取报告 + 发现报告，审计链完整。

**原始数据位置**：
- 冻结原始 PDF：`paper_projects/CMC/C2GES/05_External_Prospective_20260922/source_pdfs*/`（发布范围外，不随包分发）；
- 发布件（协议、清单、聚合、脚本）：`03_Reproducibility/Data/external_prospective_v1/`。

### L4 构念审计语料（角色/边线索的构念边界）

**支撑结果**：§4.11——角色线索"触发时精确、泛文中稀疏"的边界陈述（精确率 0.610/0.807，召回 6%）。

**优质特征**：直接借用**带人工标注的公共语料**（GUM enhanced-RST 7,678 EDU / 7,285 关系对；EBM-NLP 2,139 句专业医学标注）做相邻域构念审计；**第三方语料不转发**，只随包发布审计脚本与聚合结果（`Data/construct_audit_v1/`），来源须从原分发方获取。

**原始数据位置**：GUM — Georgetown University Multilayer 官方分发；EBM-NLP — 其官方仓库/分发页。均不入本地发布树。

### L5 合成 fixtures（机制负对照）

**支撑结果**：§4.6 合成压力测试——当参考由同一角色链生成时路径对比仍 p=1.0，证明负结果不是"参考与机制对齐不足"的伪影。

**优质特征**：虚构文本与参考由同一可控角色链生成，机制完全可知；与真实语料结论方向分离记录，不外推。

**原始数据位置**：`03_Reproducibility/Data/synthetic_stress_v1/`（代码生成、可复现，随包分发）。

## 跨层共性：让这些数据集"支撑力强"的六个工程特征

1. **真实性 + 权利治理**：全部为官方公开事故报告或带标注公共语料；逐份 URL/哈希/权利状态台账，转发边界明确。
2. **隔离与分层**：开发/测试硬隔离；系列 × 组织分层；外部语料系列不相交；LOSO 敏感性随包。
3. **协议先冻结后跑分**：修订留痕（v1.1–v1.4）；接触过的语料诚实降级（post-access），不冒称未见。
4. **参考分离与规则文档化**：摘要检测规则、抽取管线、候选构造全部写入协议，且先冻结。
5. **审计随数据走**：布局审计（505 表格区域、14,290 布局单元）、tokenizer 审计、抽样框排除理由——数据质量证明是数据的一部分。
6. **可复算 + 声称边界**：全部聚合可由随包 artifacts 确定性重算；每层携带"可声称/不得声称"清单（正文 Table 15 证据层表）。

## 限制（如实）

- L1/L2 的原始 PDF 与逐字派生文本因第三方权利**不公开转发**；公开件为哈希、清单、聚合与非逐字审计。
- L4 的 GUM/EBM-NLP 须从原分发方获取，本地不留副本入包。
- 全部层均非"未见确认性"语料；真正的未见、系列不相交、预注册对称调参语料属 E1 路线（正文 §5.6 与 Table 15 的 e2-gate）。

---
索引：发布范围内全部数据文档见 `03_Reproducibility/Package_Metadata/RELEASE_MANIFEST.json`；全仓公共数据集总账见 `data/public_datasets/manifests/public_dataset_manifest.csv`。
