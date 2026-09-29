# C2GES 当前基准

更新日期：2026-09-29

## 2026-09-29 独立核查轮（对 09-27/28 并行扩展的复核，当前）

对 09-27 扩展轮（24 报告延伸、arm 层分离、GovReport 迁移、界限层、合成 parent/held-out）做了独立核查：摘要/结论中 100/970/160 三处文档数与 `govreport_transfer_v1` 三个 bounds JSON 逐一相符（n=100 上限全负、n=970 上限全负、n=160 在 +0.005 界内）；24 报告四个对比（−0.006908、10 负 1 正 13 平、exact 0.444、Holm 0.678；TextRank exact 0.130/Holm 0.390）与 `external_prospective_v2_expanded.json` 一致；arm 层数字（−0.03510、18/22、p 0.00387、Holm 0.0774、+0.01079）与 `external_arms_v3.json` 一致；界限 +0.0047/+0.0059 在 `equivalence_bounds_v1.json` 在账。

核查修掉两处缺陷：①补充材料 Contents 误写 "nineteen tables"（实为 20 表 2 图）；②§3.11 边界句 "None of these sensitivities is a fresh confirmatory test." 在改写中被误删，已恢复。

- 正文 tex：`d425441f7b6b83a370f3d61ba928d8beee4fed1689ee644a3dac0022c2b41f28`
- 主稿 PDF：`9a31e0e4ca4e63a027b4615374dbbd17855654b4f6e86926ed55f24742b1a2e2`；34 页，6 图 14 表 46 参考文献，0 错误 / 0 Overfull / 0 未定义引用
- 补充 PDF：`e42488ea3d3ba989637950e53b44c2fa163100441da3b0e6a044731fb539a103`；12 页，S1–S20 + Figure S4–S5
- 作者审阅 Word：`d9e69ee5db397261392e0068b989ee4fbfe91c0085f3976fc0ef5728229fdda1`
- 投稿 ZIP `96eade217e2c380aad1fd4296689cf21e055c772160c7a1c41de6ce01645ae81`；评审 ZIP `daf329e9861c20a342d3b89477a0cfdea53265770d11c372dfc29f0ae15e7c16`；补充 ZIP `20f1d12b99f296fb7e3289feeab659ffec349ca83ed023b147f82b963528c428`；均 `fresh_extract: PASS`
- 公共验证 route `diagnostic` **PASS** 0 failures；展示审计 `problems: none`；发布清单 **670 文件** PASS

## Information 版（2026-09-28 L5 合成层升级：冻结 parent/held-out 夹具，历史）

把 GenData 侧新产出的 parent-v3r1 + heldout-v2r3 两套合成压力夹具正式纳入论文，作为 L5 层的升级（替换旧的单套 8 篇 v8）。**仅动合成层**，所有真实语料数字、E1/E2/E3 三道证据门与"合成不进确认链"的边界语句原样保留。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `13e7a3517d8e858b34dc70acc97e947fc3d2bbadf53288595f0180a96d92e2be`
- 主稿 PDF：SHA-256 `6ded248d6f5983fba488a8cb3127cfb2d07bcccd7310d9e4deb6777dbaaf3a1f`；**34 页**，6 图 **14 表**（合成小表移入补充材料 S20）46 参考文献，摘要 197 词，0 错误 / 0 Overfull / 0 未定义引用
- 补充 PDF：SHA-256 `e76cde2369663568c7ec5bc859c20248006c036afe73c6162dcb94fba5549881`；**12 页**，Table **S1–S20** + Figure S4–S5
- 作者审阅 Word：SHA-256 `d9b89fd5a5706a6735492463b10738177ec498f71e2d2fb86878a4d0e6416811`（12 图 / 14 表）
- 投稿 ZIP `ad87442b500a16339ae192dbc3c21f1419c53c1c455dbd43bc707a360f7d1281`（20 文件）；评审 ZIP `558f3b93b7d175a3049d7eb49dafc70696d7a6670fc4e02a765b8a124a9c3252`（24 文件）；补充 ZIP `bee2d5b1aa21cb6e5c672fa8421cf1abb7227eaf91c35258be126f4aca29c4da`（4 文件）；均 `fresh_extract: PASS`
- 公共验证 route `diagnostic` **PASS** 0 failures（新增 `gendata_synthetic_checks()`，共 11 个检查组）；发布清单 **670 文件** `--check` PASS

### L5 升级内容（只动合成层）

- 夹具：`03_Reproducibility/Data/synthetic_stress_v1/run_20260927_gendata_parent_v3r1/` 与 `run_20260927_gendata_heldout_v2r3/`（各 8 篇 4 系列；主题互斥、生成器族 A↔B 交换；冻结协议 `PROTOCOL_synthetic_c2ges_gendata_v1.md` sha256 daf7c969、19 门全过、双评审 accept）+ 数据集卡片与冻结记录。
- 组件析因（论文自己的评估器，不调参）：Full−no_path 宏均值 parent +0.0103/+0.0098、heldout −0.0003/+0.0043（Holm 全 1.0）；系列等权 path_main parent +0.0147/+0.0178、heldout −0.0007/+0.0032；G-T−G-U 两集为正（Holm 0.25）。**核心主张保持：两集中均无校正后非零路径对比**。
- 正文 §4.9 重写为冻结 parent/held-out 设计并指向 S20；L5 证据行更新为 16 篇 8 系列；合成小表移入补充材料（保持 34 页且不丢表）；Data Availability 增列新夹具与协议/卡片。
- 单元测试 `test_heldout_synthetic_v8` 更新为"新夹具 CSV ↔ 补充材料 S20 逐位一致"。

### 边界（未改变）

合成夹具仍标记 `SYNTHETIC_STRESS_NONCONFIRMATORY / confirmatory_claims_allowed=false`，**不进 E1/E2/E3 确认性证据链**，不替代未见系列、真人标注或伦理决定；AUROC(syn-vs-real)=0.998 仅作描述性记录（文档身份而非真实性）。

### 2026-09-29 增补（按用户边界清单）

- 把 GenData 侧用户版 `README.md` 与 `STAGING_CONTAMINATION_REPORT.md` 一并带入发布目录（`synthetic_stress_v1/`），发布资产现含：README / DATASET_CARD / PROTOCOL / FREEZE_RECORD / 污染报告 + 两个跑次目录；公共验证断言 README 在位。
- 补充材料 Table S20 的注记补上三条诚实边界：**可见接缝纹理、极易区分的文档身份（AUROC 0.998）、每套仅 8 篇不支持统计推断**；并写明"parent 线看过中间门结果做过生成器调优（阈值未动）、held-out 线才是独立检验"。

## Information 版（2026-09-26 跨域迁移 L7 + 定稿，历史）

计划 v2 的 **G2 证据性试点已完成**：在 GovReport 上用冻结臂集合做跨域迁移检验（n=100 分层样本，跑分前冻结协议）。这是全文目前效力最强的一条证据，已按"边界层"写入正文与补充材料。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `ff670d8d692bafaf3d937058c7a7cd113cef957d69b9a43b46658eaa30c1de21`
- 主稿 PDF：SHA-256 `4df8fb6e1692c88468bc903b3e0902ce92b98e6093817d405dfea97d94c7b8b1`；**34 页**（正文 p31 止、缩写表 p32、参考文献 p33–34），6 图 15 表 46 参考文献，摘要 **197 词**（含跨域界值句），0 错误 / 0 Overfull / 0 未定义引用
- 补充 PDF：SHA-256 `da89fc4943a8fb294990b68a1b6ee5a85dc0c81f1c3e3368b34ed74d104c0cdf`；**11 页**，Table **S1–S19**（S18 = 冻结试点 + 全量 970 + 能源子集 160；S19 = 参考类型敏感性）+ Figure S4–S5
- 作者审阅 Word：SHA-256 `0323618853fce58dfdddfd7cc03602f936e8790f281d648ef261bfc1bf7cb9a5`
- 投稿 ZIP `3b10170913fe8d1e67e2d8b154949df3f13a0c737977f160ed5ff630d4d0c189`（20 文件）；评审 ZIP `d19ef280abfa16087c237d2ac0f248e958dca13c6ef4c3b07233fa976f7c39ea`（24 文件）；补充 ZIP `1d611cfacb7afd4cf0f056dfc79e197b85b492cfd84f867f99227a643855e7f6`（4 文件）；均 `fresh_extract: PASS`
- 公共验证 route `diagnostic` **PASS** 0 failures，含 `govreport_transfer_checks()` 与 `reference_type_checks()`（10 个检查组）；发布清单 **639 文件** `--check` PASS

### G2 结果（100 份 GovReport test 文档，冻结协议）

| 对比 | 110 词 | 260 词 | K=5 | K=10 |
|---|---|---|---|---|
| **路径层 Full − no_path** | −0.00305（24/15/61） | −0.00259（37/25/38） | **−0.00515（39/13/48，Holm 0.0017）** | −0.00277（30/21/49） |
| 单侧 95% 上界 | **−0.00105** | **−0.00071** | **−0.00295** | **−0.00100** |
| 角色层 AB2 − AB0 | **−0.02124（Holm 0.0002）** | −0.02043（Holm 0.0002） | −0.00070 | −0.00977（Holm 0.084） |
| TextRank − no_path | +0.02149（Holm 0.0002） | +0.02728（Holm 0.0002） | +0.00053 | +0.01186（Holm 0.033） |

**全量敏感性（冻结分层全取，970/973 篇，12 分片并行）**：

| 对比 | 110 词 | 260 词 | K=5 | K=10 |
|---|---|---|---|---|
| 路径层 Full − no_path | −0.00208（233/156/581） | −0.00165（330/224/416） | −0.00318（316/166/488） | −0.00197（306/197/467） |
| 单侧 95% 上界 | **−0.00132** | **−0.00083** | **−0.00236** | **−0.00135** |
| 角色层 AB2 − AB0 | −0.01934 | −0.02202 | −0.00304 | −0.01342 |

全量下路径层四个预算**全部 Holm 显著**（0.0002–0.0040），上界最坏 −0.0008；角色层四预算也全为负。这使"路径项无正增益"从单层结论变成**跨域、大样本、人类参考下的稳定界**。

**能源主题子集（同一协议，160 篇）**：按冻结关键词表（energy / grid / transmission / power plant / electricity / renewable / nuclear …，正文命中 ≥3 个）选出，路径层四预算均值 −0.00091 / −0.00155 / −0.00181 / −0.00247，正号占非平 41%/42%/36%/34%，单侧 95% 上界最坏 **+0.00082**（满足 +0.005 边际），K=10 通过 Holm（0.0174）；角色层在等词预算显著为负（Holm 0.0002）。这层最接近本文目标域，结论与全量一致。

### G3 参考类型敏感性（400 篇，人类抽取式参考）

冻结协议 `Data/reference_type_v1/PROTOCOL_reference_type_v1.md`；参考换成 CNN/DailyMail 人类撰写的 highlight 要点（大量逐字取自原文），其余设置不变：

| 对比 | 110 词 | 260 词 | K=5 | K=10 |
|---|---|---|---|---|
| 路径层 Full − no_path | +0.00047（14/10/376） | −0.00027（18/14/368） | −0.00000（4/4/392） | +0.00000（1/4/395） |
| 单侧 95% 上界 | +0.00158 | +0.00016 | +0.00016 | +0.00004 |
| 角色层 AB2 − AB0 | −0.00920（Holm 0.0012） | −0.00184 | −0.00649（Holm 0.0071） | −0.00128 |

判定：**H3 成立**（四预算上界 ≤ +0.0016，远在 +0.005 内）；路径项在此参考下**惰性**而非有害——92–99% 的文档选择完全相同（等句数预算下 98–99%）。Lead 位置基线在四个预算全部显著领先（Holm ≤0.0002），符合新闻导语特性。结论：**路径层的"零"不是"用抽象式参考去比抽取式输出"造成的假象**。诚实边界：新闻语料 + 短文档（中位 23 个候选单元）+ 域内词表覆盖仅 0.116，故只作参考类型敏感性，不作域内证据。

- **H2 成立**（四预算均值全为负、正号占比 ≤41%）；**H3 更强成立**：单侧上界四个预算**全部小于 0**，即"路径项为正"被排除，不只是"没检出"；K=5 通过 Holm（0.0017）。
- **H1 再次不成立且方向相反**：角色条件化在等词预算显著**有害**（−0.021），与"电力域线索词表跨域错配"一致（平均角色覆盖 0.246）。
- **基线排序再次翻转**：TextRank 在等词预算显著领先（+0.021/+0.027），在 K=5 归零。
- 诚实边界（已写入正文与协议）：线索词表是域内词表、参考是人类抽象式摘要 → 该层只"限定风险"，不支撑机制。

### 产物与协议

- 协议（跑分前冻结）：`../03_Reproducibility/Data/govreport_transfer_v1/PROTOCOL_govreport_transfer_v1.md`
- 结果：`.../govreport_transfer_v1.json`（100 文档 × 7 臂 × 4 预算，2,800 行）、`.../govreport_transfer_bounds_v1.json`（界值与留一法）
- 代码：`../03_Reproducibility/Code/govreport_transfer_v1/`（抓取 / 运行 / 界值分析）
- 语料：`../05_External_Prospective_20260922/govreport/govreport_test_full.jsonl`（973 行，**发布范围外**；CC BY 4.0 但按既有边界不随包分发）
- 论文位置：证据层表新增 **L7**；正文 §4.3 末段为界值化指针；补充材料 **Table S18**

### 篇幅

34 页（同刊对照实测区间 16–33 页，超 1 页）。为控制在 34 页内，本轮删去五处与相邻表注/方法段重复的告诫句，并把迁移细节压到补充材料，正文只保留界值结论与指针。

### 同轮附带完成（G4/G6）

- **G4 人工标注方案（可执行 + 预算）**：`../03_Reproducibility/Data/human_structure_validation_v1/E2_COSTED_EXECUTION_PLAN_20260926.md` —— 比例区间半宽的样本量算术（p=0.7 时 w=0.10 需 81 单元、w=0.05 需 323）、两档方案（Tier A 120 单元 / Tier B 320 单元 + 100 结构项）、工时模型（Tier A ≈40 人时、Tier B ≈102 人时）、费用行（费率留空待作者填）、六周日历与三道门禁；红线：LLM 与作者不得充当独立标注者、伦理决定前不得招募。
- **G6 方法下沉 mylib**：`D:/aicoding/mylib/Codex-Academic-Research/tools/paired_diagnostic_stats.py`（纯标准库，零质量/符号翻转/单侧上界/留一法/功效天花板，`--self-test` 复现本文 −0.006908、10/1/13）；`digests/powergrid-diagnostic-eval-2026-09.md`（五个统计陷阱、把零结果写成界、分层证据表、预注册、发布边界工程、长度纪律、投稿前清单）；`playbooks.md` 新增 **J 节**（诊断/负结果评测路由）；`README.md` 入口表登记两项。
- **摘要升级**：197 词（≤200），结尾改为"跨域政府报告上单侧上界在每个预算都低于零 + 无类型基线在等词预算胜出"。

## Information 版（2026-09-26 G1 界值 + 评审增量 + 边界修复，历史）

计划的 G1（零新数据、把"不显著"改写成"上界"）已执行，并顺带修掉两处发布边界/打包缺陷。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `94953407d738aeedb49526d24f0af934e630688587ed4faf43c24e0e5933de36`
- 主稿 PDF：SHA-256 `d5e7fde7a46839891d82c3e685b68313d839cbb097dfdec4f92ff4f9b853c9a7`；**34 页**（正文终于 p31，缩写表 p32，参考文献 p33–34），6 图 15 表 46 参考文献，摘要 192 词，0 错误 / 0 Overfull / 0 未定义引用
- 补充 PDF：SHA-256 `ada3399954fb785ec45858be34dca17070f21823c907bb502ed255586585a972`；**10 页**，Table **S1–S17** + Figure **S4–S5**
- 作者审阅 Word：SHA-256 `e5eff6b0f2379bea6f41865b15bbce5bcda74862e2af6e422fe9f0f190c3bfed`
- 投稿 ZIP `7394182a370cf5fe030e3db80e489cb0046eb1c593084c3211beb7e45ac8364d`（20 文件）；评审 ZIP `9341d5f5ff8afcf2042dc0ac715a0b603353c242ff585e835ccdc28a07b68cb0`（24 文件）；补充 ZIP `400638a58217ef92ea7b89e96ea7796e9aff33867c7018f55e9d86af3640a67a`（**4 文件**，含新增 Figure S5）；三者 `fresh_extract: PASS`
- 公共验证 route `diagnostic` **PASS** 0 failures；新增检查组 `release_boundary_and_addenda_checks()`；发布清单 **612 文件** `--check` PASS

### 本轮科学改动（G1：把负结果写成界）

- 路径层界：四个预算的单侧 95% bootstrap 上界 ≤ **+0.0047**（110 词 +0.0006、260 词 +0.0021），留一法最坏 **+0.0059** → 正文写明"路径项增益超过 +0.005 ROUGE-L 被排除"（明确标注 post hoc）。
- 机制证据：等词预算下角色臂到 260 词都落后、400 词才追平；等句数预算下领先且每单元多装约 1.5×（对 AB-0）/3×（对 TextRank）词数。
- 分族描述：260 词路径差由两篇频偏报告主导（−0.0799），电网事故 −0.0028、市场耦合 +0.0036、NERC −0.0031（Table S15）。
- 新增数据产物：`Data/equivalence_bounds_v1/`（含留一法包络）、`Data/budget_curve_v1/`（Figure S5 源数据）、`Data/external_prospective_v1/external_arms_curve_v4.json`（1,512 行）、`Data/descriptive_addenda_v2/`（S14/S15/S16 源数据 + 清单）
- 新增代码：`Code/equivalence_bounds_v1/`、`Code/budget_curve_figure_v1/`、`Code/descriptive_addenda_v2/`（生成器直接产出补充材料表格，数字不可能与数据漂移）

### 本轮修复的两处缺陷

1. **逐字文本越界（既有问题）**：`Data/rsi_path_v1/run/SEALED_CHOICES.jsonl` 含 `selected_text`/`reference_text` 逐字第三方原文且原在发布范围内。已生成权利安全版 `SEALED_CHOICES_rights_safe.jsonl`（同 id/预算/长度/分数，90 行），并在 `generate_release_manifest.py` 中把逐字件排除；公共验证新增"任何已发布数据记录不得含 ≥300 字符、≥40 词的连续散文"断言。
2. **补充包漏图**：`package_information.py` 原先硬编码只打包 Figure S4，新增的 S5 会被漏掉。已改为打包 `Supplementary/figures/*.pdf`，并新增断言"tex 中每个 `\includegraphics` 目标必须在压缩包内"（正文包同样适用）。

### 篇幅

33 → 34 页（同刊对照实测区间 16–33 页）。为控制篇幅已删两处与各自表注/方法段重复的告诫句，并把新段落压到 7 行；正文止于 p31，多出的一页是参考文献尾部。

## Information 版（2026-09-26 臂级判定 + 重打包，历史）

在"外部语料 19 → 24 + 臂级决策实验"之上完成的构建与打包轮。本文件此前记录的"docx/三包/公共验证未重算"待办**已关闭**。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `73095b4cf67b9b0255f6890f5215987e5123b4183534dc16dabcea48ef6e1b7c`
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf` SHA-256 `4f6f5b039e04ab6220d44d35d5511e2226cb84a4d19149f35d9d9dcdf14b9490`；**33 页**，6 图 15 表 **46** 参考文献，摘要 **192 词**，0 错误 / 0 Overfull / 0 未定义引用
- 补充 PDF：SHA-256 `3006759792adb90f2da4b531d5014a5924ef45de83f6a356369d4a75875377ef`，**7 页**，Table **S1–S13** + Figure S4
- 作者审阅 Word：`../01_Manuscript/LaTeX/paper_information.docx` SHA-256 `15c8c8f1351e14e4d079a8bbc5ce6a5c339c6bd21ac32542c8e363e1cad19477`（由当前 tex 重建，12 内嵌图 / 15 表）
- 投稿 ZIP：`5de1c1332b6e77e61b7de80161fec0c49597096d46aee7bfd291f820f3c913b0`（20 文件）；评审 ZIP：`2a68ae967005fe80b177992db8e572db1923a20beb219ca1dd17e5ba51fc259b`（24 文件）；补充 ZIP：`33f35073ced5e390dcff905bb38eb6f9359f9289d33d0702ab17547dd0db925b`（3 文件）；三者均 `fresh_extract: PASS`
- 公共验证 route `diagnostic` **PASS**，0 failures；`external_prospective_checks()` 新增 6 条臂级断言（`arms_documents_and_families`、`role_layer_reverses_under_equal_word_budget`、`role_layer_only_positive_under_equal_unit_budget`、`path_layer_stable_across_all_budgets`、`baseline_ordering_flips_with_budget_type`、`arm_numbers_bound_to_manuscript`），把正文里的 −0.03510 / 18 of 22 / 0.0039 / 0.0774 / +0.01079 绑定到 `external_arms_v3.json`
- 发布清单：`../03_Reproducibility/Package_Metadata/RELEASE_MANIFEST.json` **591 文件**，`--check` PASS（0 缺失 / 0 未列入 / 0 哈希不符）；`submission_ready: true`，`technical_verification` 指向本轮验证报告
- 展示审计（`manuscript_display_audit.py`）：6 图 15 表、33 页、0 Overfull / 0 错误 / 0 未定义引用，末页余量 14.3 pt，`problems: none`
- 本轮论文改动（仅两处，均为收紧表述）：① §5.1 角色层句改为"seven-series pilot 中有 +0.0186，但等词预算外部语料下没有"；② 外部敏感性段追加臂级一段（角色层为长度产物、路径层四预算均 ≤0），附 18/22 与 +0.01079 的原始读数

### 本轮新增的分析产物（发布范围外，wiki）

- `../04_Wiki/C2GES_DATASET_QUALITY_AND_STATISTICS_20260926.md`：新增 **§7.5 逐篇影响分析（留一法）** 与 **§9 收口**（三问答案、资产结论、发布边界）
- `../04_Wiki/C2GES_NEXT_EXPERIMENT_PLAN_v2_20260926.md`：替代 v1 的取数主线（结论：继续扩同类语料不划算，改为"等价上界 + 公开基准换功效 + 语料资产化"）

### §7.5 的核心读数（留一法，`Full − no_path @ word:260`）

全样本均值 −0.006908 中 **−0.00634（92%）来自同一篇文档**（2012 频偏报告，−0.15218）；删掉它均值变为 −0.00059。但三组样本的**符号方向（10/11、9/10、10/10 为负）与单侧 95% 上界（+0.0021 / +0.0040 / −0.0017）都不变**——均值不可靠、上界可用，这是下一阶段把主判据换成等价上界的直接依据。

## Information 版（2026-09-26 探索性补充，历史）

在 09-25 评审处置轮之上，补入 Q1/Q6/Q10 三个探索性描述分析（补充材料 Table S11–S13 + 随包数据 `03_Reproducibility/Data/descriptive_addenda_v1/`）。不动任何实验数值与声称边界；无新推断检验、无新 Holm 校正。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `dd70896031989ae889b82444c906562751a4a5c590d8bc1a3aad7cfd36e8198e`
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf` SHA-256 `19e9c1477fcb823b2f82aa83f0de396b67f1467fa38289e2ad5d0a5f865af92f`；**34 页**（正文终于 p30），6 图 15 表 46 参考文献，摘要 200 词，0 错误 / 0 Overfull / 0 未定义引用
- 补充 PDF：SHA-256 `518e563bfa2539bc568a2012f3d8067d59fd231d543bc1303202d01bcb7a48b4`，**7 页**，Table S1–S13 + Figure S4
- 投稿 ZIP：`79d4ab0dc8168f4bf2b56a91cce952e4b393c571450bfc68d8d5a7f2ae602f87`；评审 ZIP：`153813c52e1dd08ea30fb234a9f7c204ff410505d4f3f06ab900e1d6d1756549`；补充 ZIP：`6f592cf5df133b44a2483311ce7ddd52e9738c863c929eb355ae53dcb9f2aa36`；均 `fresh_extract: PASS`（评审包 docx 已从当前 tex 重建）
- 公共验证 route `diagnostic` **PASS** 0 failures；展示审计 `problems: none`（6 图 15 表）；发布清单 **580 文件** `--check` PASS
- 分析代码：`03_Reproducibility/Code/descriptive_addenda_v1/`（5/5 单测通过；无随机性；输入哈希记入 `ADDENDA_MANIFEST.json`）

### 本轮改动

| 项 | 内容 |
|---|---|
| Q1 → Table S11 | 路径改选单元的错误剖面：改动单元 92–98% 与类型化边相连；相连者 80–100% 触及至少一条逆时序边（设计属性，非错误计数）；12 位窗口外每改动单元有数十至数百条角色相容对被阻断——长程依赖"按设计未测"而非"被证据否定" |
| Q6 → Table S12 | 逐角色 token 对齐（同 cue 词典、双侧标注、弃权一致）：角色层效应集中在 propagation/impact/mitigation；Full 在 propagation 精确率两预算领先但 mitigation 精确率 @110 与覆盖率落后 no-path——路径项不系统性提升对齐 |
| Q10 → Table S13 | 旧切分长单元逐条件计数（Full@K10：25 个 >100 词单元、26 个表标记单元）+ 块保留审计分布（27 报告 14,290 单元，仅 39 个 >100 词，最差 522 词）+ 非逐字实例（270 词单元含 21 个参考内容 token；162 词单元含 40 个）；排序是否改变明确不答 |
| 方法记录 | 句级 ROUGE-L 匹配在开发中先试过、几乎从不触发（执行摘要句长且措辞不同），故 Q6 采用 token 级对齐——已在表注与 README 声明 |
| 主文本 | §4.3 末增 S11/S12 指引句；§4.8 长单元段末增 S13 指引句；`\supplementary` 声明 S1–S10→S1–S13；Data Availability 增列 `descriptive_addenda_v1/` |

## Information 版（2026-09-25 修订，历史）

paperreview.ai 评审处置轮（D1–D3 缺陷修复 + 评审响应写作）后的版本。逐条处置记录：`../02_Revision_and_QA/04_Build_Reports/C2GES_PAPERREVIEW_AI_DISPOSITION_20260925.md`。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `53dba9d2de3511787337307466c365dedcb84abc07075df01499fbad72aea0bc`
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf` SHA-256 `936d16af7837cc5ec6ec7baa1f447f2757f54d537c9cdf8bedcc9c5f64756762`；**34 页**（正文仍终于 p30，增页在参考文献），6 图 15 表 **46** 参考文献，摘要 **200 词**，0 错误 / 0 Overfull / 0 未定义引用
- 投稿 ZIP：`../C2GES_Information_20260922_submission.zip`（`257de41dece1dd8b5ce71ffa40b2fa8c4ad6092769f6492efa24306eeefc87a0`，`fresh_extract: PASS`）
- 评审 ZIP：`../C2GES_Information_20260922_review.zip`（`27fc71f66d64215a2319c96760f676017f5ac8d72d9fed2718a645a254d51d6d`；含本轮重建的作者审阅 docx）
- 补充 ZIP：`../C2GES_Information_20260922_supplementary.zip`（`411b95a9f2ebd4ac737a68ccad38ccebd3dca2165fa26e4f08e31b0f89d33f89`）
- 公共验证：route `diagnostic`，**PASS**，0 failures（2026-09-25T15:24Z）；展示审计 `problems: none`；发布清单 **569 文件** `--check` PASS
- git 提交：`38ade466`（D1–D3）→ `7cf7eb56`（MemSum + E1 冗余系数）→ `c85b0405`（Sem-nCG + 两段式）→ `ee3e7f01`（结论点名 TextRank）→ 本轮打包提交

### 本轮改动（不动任何实验数值与声称边界）

| 项 | 内容 |
|---|---|
| D1 | 删 §3.9 重复段（两个改写版本并存，PDF p11 可复现；评审 W7 命中） |
| D2 | 6 处硬编码节号全改 `\ref`（新设 5 个 `\label`）：3 处错指（§3.9 误作 3.8 ×2、§4.8 误作 4.3）+ 1 处歧指（`:603` 现指 §4.3 主 estimand，**作者可改判 §4.5/§4.9**）+ 2 处本就正确；grep 确认全文零残留 |
| D3 | §3.12 删与 §4.10 近似复述的结果句（J=0.76），只留设计描述 |
| R1 | §2.1 新增 MemSum 对照句（历史感知/状态冗余 vs 本文固定罚；已核实 ACL 2022，`gu2022memsum`），并声明系数校准推迟到预冻结协议 |
| R2 | §5.6 E1 显式纳入"开发集选定冗余系数 + 对称调参预算"（回应 Q4：−0.50 确未入过任何网格） |
| R3 | §5.6 指标句加 redundancy-aware Sem-nCG（**正确编号** KONVENS 2024 `2024.konvens-main.21`；评审给的 arXiv 2310.03414 系误植）；同节写入两段式 tiebreaker 候选重设计（Q9） |
| R4 | 结论点名 TextRank（保留"该语料上唯一家族校正对比"限定，不与历史 K=5 Holm 胜出冲突） |
| 评审核验 | "相关工作缺失"6 项中 4 项稿内已引（ARedSum/GraphLSS/Bi-GAE/StrucSum）；根因是评审副本省略参考文献页；"图表只描述不展示"不成立（6 图 15 表全在 p4–29） |

## Information 版（2026-09-24 打包，历史）

外部前瞻评测（ENTSO-E + NERC 新语料，n=19）入稿后的版本。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `6f38ddd63e31ab3eee6f501962700fd6259a852e4c3ce5b9c2858c56e8e1e6c5`
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf` SHA-256 `6c1947ab950071389f41ed8bf5f34b85a53753a3082797e25828f3c2cadec2d4`；**33 页**，6 图 15 表 44 参考文献，摘要 **192 词**，0 错误 / 0 Overfull / 0 未定义引用
- 投稿 ZIP：`../C2GES_Information_20260922_submission.zip`（20 文件，`dc5b2640dd0d2c21775a5ae33be84ebbdbf7c132ac520d7f332450c46e7d6242`，`fresh_extract: PASS`）
- 评审 ZIP：`../C2GES_Information_20260922_review.zip`（24 文件，`b7c71a094858bc33234a3f7b14c9a0d885c87f954668a902c97f90c75814fb06`）
- 补充 ZIP：`../C2GES_Information_20260922_supplementary.zip`（3 文件，`7d23b9eda6221430a4486f35665d96dd98ae5395c6ad5f25643cb92787355654`；补充 PDF 6 页，新增 **Table S10**）
- 公共验证：`../02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json` —— route `diagnostic`，**PASS**，0 failures（新增 `external_prospective_checks()`）
- 发布清单：`RELEASE_MANIFEST.json` **588 文件**，`--check` PASS

### 外部 AI 评审提交（2026-09-25）

### 数据集质量与统计特征 wiki（2026-09-26）

`../04_Wiki/C2GES_DATASET_QUALITY_AND_STATISTICS_20260926.md` —— 六层数据集的质量画像、六个统计特征（零膨胀、效应量与噪声同阶、重尾、方向随预算翻转、符号一致性、跨语料不可比），以及"为什么后续增补数据都没超过第一个"的五条原因（最重要的是：第一个赢在**等单元数下的信息预算不对等**，C²GES 多得 56–63% 正文；而后续改为等词预算后优势消失）。另含**功效天花板**计算：7 系列在 Holm 校正下即使 7/7 符号一致也过不了 0.05（k=4 时最小 adjusted p=0.0625），因此该层"不显著"不能读作"无效应"。

同目录另有增补数据资产盘点（§6：通用性/价值排序）与 **下一步实验增补计划** `../04_Wiki/C2GES_NEXT_EXPERIMENT_PLAN_20260926.md`：目标把外部语料扩到**电网事故族 ≥12、市场耦合族 ≥12**，用单一定义参考 + 一致词预算（110/260）重跑，预先声明 H1（角色层符号一致率 ≥65%）与 H2（路径层 ≤0），并强制报告**功效上限与零质量**；含取数通道（Wayback CDX + blob 直连）、入选门禁、协议 v2 设计、六阶段工作量与"不做清单"。

已把当前投稿版 PDF（33 页，pdf `01e41bf2…`）提交到 paperreview.ai（Stanford Agentic Reviewer），提交邮箱 `iamafan@126.com`，页面回显 "✓ Submission Successful!"。

**Review Token：`Y1fgiQDAfNoMyfLfyNze3nBILeCuhZVc4qNKCHSxxGY`** —— 系统提示部分邮箱收不到通知，取回评审用 https://paperreview.ai/review + 该 token。系统限制：**只分析前 15 页**（本稿 33 页，故结果章/讨论/结论不在覆盖内），处理可能数小时，且明确要求不要重复提交。完整记录见 `../PAPERREVIEW_AI_SUBMISSION_20260925.md`。

**第二次提交（15 页压缩评审副本，覆盖全文正文）**：用 `06_External_Review/build_review_copy_15p.py` 把原始 p1–p30（摘要→结论）以 **A3 横向两页并排、1:1 原尺寸** 压成 **15 页**（`C2GES_reviewcopy_15p_A3.pdf`，0.50 MB），省略 p31–33 的声明与参考文献；投稿版 PDF 未改动。已提交（邮箱同上），回显 "✓ Submission Successful!"，**Token：`sjA3oxGSe0bRDX3iam9A5ab4pqL7YlynFmNWozfo3FM`**。解读时注意两页并排可能引起解析错位，以及副本不含参考文献。

### 本轮改动：外部前瞻评测（F-11）

| 项 | 内容 |
|---|---|
| 语料 | 27 份公开事故报告（ENTSO-E 21 + NERC 6），冻结于 `05_External_Prospective_20260922/`（发布范围外，不随包分发） |
| 协议 | `PROTOCOL_external_prospective_v1.md`：跑分前冻结，含 v1.1（摘要搜索窗）、v1.2（Management Summary）、v1.3（章节号前缀 + 目录点线）、v1.4（参考 ≥100 词、候选上限 2000）四处修订记录 |
| 抽取 | `convert_to_markdown.py`（pymupdf4llm 结构化 Markdown）+ `run_external_prospective_v2.py`（摘要切到同级/更高级标题） |
| 结果 | n=**19**（6 ENTSO-E 电网 + 7 市场耦合 + 6 NERC）；Full−no-path @110 −0.002422（Holm 0.317）、@260 **−0.002906（Holm 0.046875，7 负 0 正）**；TextRank−no-path @110 +0.023273（Holm 0.317）、@260 **+0.022940（Holm 0.032380）** |
| 写作 | 新增 Results 外部复现小节（现为 §4.4，紧随分量因子之后）、Limitations 与 §5.1、摘要（199 词）、补充 **Table S10**、Data Availability 增列发布物 |
| 边界 | 只写 prospective frozen external evaluation；不称未见确认、不与 NERC 15 题或 7 系列合并；TextRank 优势仅出现在 260 词且已注明 |
| 叙事复审（2026-09-25） | N-1 外部复现前移至 §4.4；N-2 §5.1 以角色层开篇；N-3 角色线索精确率进入讨论与结论；**N-4 证据层合并为 L1–L6 单表**；**N-5 摘要点明历史层校正胜出**（页数 32→33，仍在同刊实测 16–33 页区间顶端）；层号硬编码改为 `\\ref` 标签。复查记录见 `../02_Revision_and_QA/04_Build_Reports/C2GES_RESULTS_NARRATIVE_REVIEW_20260925.md` |

## Information 版（2026-09-22 打包，当前）

同刊对标评审（`../02_Revision_and_QA/04_Build_Reports/C2GES_INFORMATION_BENCHMARK_REVIEW_20260922.md`）后的落地版本。

- 正文：`../01_Manuscript/LaTeX/paper_information.tex`
  SHA-256 `f5bfb364ce3acdeacb9d8dc10876b732c19be0ece72902b6498421dfa4c802c2`；103,900 字符
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf`
  SHA-256 `9bcc819da0f2eb47ce3627df5106d040de16c18469fb46722691bcb8c4edbf58`；**31 页**，6 图 15 表 44 条参考文献，摘要 199 词，0 错误 / 0 Overfull / 0 未定义引用
- 投稿 ZIP：`../C2GES_Information_20260922_submission.zip`（20 文件，`0f255a4bb14b85916ae136938d62ad6a75b4afc2ba575937b1297a7415d6e9f8`，`fresh_extract: PASS`）
- 评审 ZIP：`../C2GES_Information_20260922_review.zip`（24 文件，`d4a6d12d0dbf9b0520c524d1aabcd386db5a14dc26f40051a066ff02a280952e`）
- 补充 ZIP：`../C2GES_Information_20260922_supplementary.zip`（3 文件，`c19505897b7bc0920d84c62e3c284ca7fdb0c9eb0cba48888e59ac90be3185cd`；新增 Table S9 构念审计表）
- **公共验证（F-1 已关闭）**：`../02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json` —— route `diagnostic`，**PASS**，0 failures。验证脚本含 `revision_evidence_checks()`（RSI + 合成 v8）与新增 `construct_audit_checks()`（构念审计聚合值）；`manuscript_checks()` 与 LaTeX 构建检查使用 `paper_information`。

### 本轮改动（不改任何实验数值）

| 项 | 内容 |
|---|---|
| F-1 | 公共验证覆盖缺口关闭：脚本扩展后重跑，RSI 与合成集进入检查清单 |
| F-2 | 补 4 条同刊 *Information* 算法同族对照（Verma 2023 图式抽取摘要；Koniaris 2023 法律长文摘要评测；Azhar 2025 摘要系统系统综述+实验评测；Nechakhin 2024 结构化摘要的 LLM + 人类评估），相关工作新增两句差异说明 |
| F-3 | 新增 `tab:e2-gate`：E1/E2/伦理三道前置 + "关闭前不得声称"清单 |
| F-4 | `tab:all-results` 中 unrenormalized 诊断行移出主对照区，用 `\cmidrule` 分隔 |
| F-5 | 摘要首句改为信息学问题句（原结论句下沉） |
| F-6 | §3.1 增补命名与三次开发动作的说明段 |
| F-7 | Figure 6（`fig:component-diagnostic`）在 §5.2 获得正文引用 |
| F-9 | 结论压缩冗余复述；RSI 明确写出"260 词领先、110 词未领先" |
| 归档 | 旧的 `C2GES_Information_20260920_*.zip` 移入 `90_Archive/05_Superseded_Packages_20260922/`，避免与当前构建混淆 |
| 漂移复核 | 最后一次正文补句后曾出现 tex/PDF 不同步（PDF 早于 tex）；已重编并复核：PDF 文本包含该句，`manuscript_display_audit.py` 报告 0 未引用浮动体、0 孤儿图、0 Overfull，包按新 PDF 重建 |
| F-10（构念审计，本轮新增） | 新增 §4.10「Adjacent-Corpus Construct Audit of Role and Edge Evidence」+ Methods/§3.8 说明 + Limitations 续句 + 补充材料 **Table S9**；审计脚本与聚合结果随包分发于 `03_Reproducibility/Data/construct_audit_v1/`，第三方语料（GUM、EBM-NLP）不随包分发并已在正文与数据可用性中声明。页数 30→31；公共验证新增 `construct_audit_checks()` |
| 发布账目 | `RELEASE_MANIFEST.json` 重算为 **545 文件**（含构念审计的 4 个文件、同刊对标报告与公共验证报告），`--check` PASS：0 缺失 / 0 未列入 / 0 哈希不符；`technical_verification` 指向 `02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json`（route `diagnostic`，PASS） |
| 范围隔离 | 新下载的 4 篇同刊参考件放在 **发布范围之外** 的 `04_Reference_Literature/Information_Benchmark_20260922/`（附 README 说明来源与 CC BY 许可，不随投稿包/发布包分发） |

### Information 版（2026-09-19 打包，历史）

## Information 版（2026-09-19 打包，当前）

- 正文：`../01_Manuscript/LaTeX/paper_information.tex`
  SHA-256 `f761bd110ffafca79382194af496689a3d6f6eae65f9ddc6c12037a787587898`
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf`
  SHA-256 `57501a0e606c9328c24b854c17075dac1c28c9fde1179109b504cc61f873ebb9`；**29 页**，0 错误 / 0 Overfull / 0 未定义引用
- 投稿 ZIP：`../C2GES_Information_20260919_submission.zip`（20 文件，SHA-256 `2822dbd050d2278ae6638c4a88880b5b07feae63677733b5107ebb860d2c0b3e`）——tex/pdf/bib + Definitions + figures，**不含**封面信与内部文档
- 评审 ZIP：`../C2GES_Information_20260919_review.zip`（24 文件，SHA-256 `f41c32c761ec8ed6c6d3e8e3b89e0d6853c2084fce85f4c1e4334d59a77afecf`）
  - 含 `paper_information.docx`（作者审阅 Word，SHA-256 `7e2bab36974cbfd4…`），由 `tex_to_docx.py` 从当前 tex 生成。
  - `FORMAT_CHECK.md` 被排除在自述哈希之外：它本身在该 ZIP 内，写入自己的包哈希会随每次重打包自失效，故指向 `PACKAGE_VERIFICATION.json`。
- 补充 ZIP：`../C2GES_Information_20260919_supplementary.zip`（3 文件，SHA-256 `ee3f36897510e28786a695805a151d8e05e144617c0dbd29a00dbcf184d9c930`）；补充 PDF SHA-256 `5356aeeadc2c4fd2e7f752deeb6ec1545a74a586a84f7f5a93141700b5e3538b`（5 页）
- 参考文献 38 条。通讯作者仍为 `yangyong1@sgepri.sgcc.com.cn`。
- 打包脚本 `../01_Manuscript/LaTeX/package_information.py`（`--submission` 排除内部文档并断言未泄漏）。

### 第三轮评审（2026-09-19）

- 记录：`../02_Revision_and_QA/04_Build_Reports/C2GES_INFORMATION_ROUND3.md`。**0 CRITICAL / 3 MAJOR / 10 MINOR**，7/10。
- 评审结论原文：**"Did it improve? Yes — clearly, and in the places that mattered most." / "Nothing blocks submission."** 评分 7→8→7 非退步，而是新增内容快于周边文本更新；评审称实质与诚实度"reads at 8–9 level"。
- **已修三条 MAJOR**：
  1. **冻结协议的开发集证据**——`FREEZE.json` 显示冻结变体在 12 报告开发集**两个预算都赢** no-path（0.08541/0.12532 vs 0.08265/0.12197，`wins_both_dev_budgets: true`），而 §3.11 又报告 147 组配置搜索 12/12 折选出零权重。正文原本未解释。已写入开发集分数、`freeze_rule`（no-path 是开发参照而非冻结候选）、以及两次分析在设计空间与时间上的区别。此修**增强**论文：开发集赢→测试集输是赢家诅咒。
  2. **导航装置**——补 **RQ4**、§4.2"三层"改"四层"、贡献列表补齐四层、§5.1 改写为"冻结研究已做但非未见系列"。
  3. **发布元数据**——`RELEASE_MANIFEST.json` 已重建：**534 文件（原 479），PASS，0 缺失 / 0 未列入 / 0 哈希不符**；SHA-256 `5d74357d63ee4ab6616c45188ebc8580770415aca8c628d5ebb40c03999e778f`。同时修 `generate_release_manifest.py` 两处：
     - 加排除项（`Definitions_20260623_backup`、`_mdpi_template_acs`、`_docx_assets`、模板 zip），这些是工作副本不是发布内容；
     - **根目录定位从 `parents[1]` 改为向上查找 `C2GES_RELEASE_MARKER.json`**。项目在 2026-09-12 23:06 重组时建了符号链接 `CMC/C2GES → C2GES/Workspace`，`resolve()` 展开后目录名变成 `Workspace`，原脚本按名字分支会去找 `MA_SQLGRID_...json` 而崩溃——**该生成器在现布局下原本跑不起来**。

### ⚠️ 未关闭：验证覆盖缺口

`RELEASE_MANIFEST.json` 的 `submission_ready: True` 与 `technical status: PASS` 继承自 **2026-09-12** 的 `C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json`，而 `run_public_verification.py` 的检查清单是**硬编码**的，只覆盖 `exploratory_external_v0`（E1/E3），**对 `rsi_path_v1` 与 `synthetic_stress_v1` 零覆盖**。

因此：清单索引已正确，但它所依据的验证**不覆盖新实验**。真正的修复需要扩展该脚本的检查清单并重跑（脚本硬性要求 Python 3.12；`../.venv_mintou_cuda/Scripts/python.exe` 为 3.12.10，可运行）。

### 同刊对标评审（2026-09-22）

记录：`../02_Revision_and_QA/04_Build_Reports/C2GES_INFORMATION_BENCHMARK_REVIEW_20260922.md`。

本轮用 MA-SQLGrid 的 Information 对标流程做了三件事：同刊分段比较（A1–A4 全文对照）、学术贡献比较、内在逻辑审查，并给出 F-1…F-9 与分层改进路线。

本轮另发现两条**一致性问题**（均为记录/导航级，不涉数值）：

1. **本文件落后一个构建**：这里记录的是 tex `f761bd11…` / 29 页，而磁盘与 0920 包是 tex `415fb864…` / **30 页**（`FORMAT_CHECK.md` 与 `PACKAGE_VERIFICATION.json` 均为 0920）。索引需回写到当前构建。
2. **Figure 6 未被引用**：`paper_information.tex` L617 的 `\label{fig:component-diagnostic}` 在全文中没有 `\ref`；在 §5.2 末尾补一句引用即可。

最高优先的**验证覆盖缺口（F-1）**是把 `rsi_path_v1` 与 `synthetic_stress_v1` 纳入 `run_public_verification.py` 的检查清单后重跑。**状态（2026-09-22）：已关闭** —— 见本文件顶部 2026-09-22 构建节与 `../02_Revision_and_QA/04_Build_Reports/C2GES_PUBLIC_VERIFICATION_20260922.json`（route `diagnostic`，PASS，0 failures）。

---

## Information 版（2026-09-16 打包，历史）

- 正文：`../01_Manuscript/LaTeX/paper_information.tex`；PDF：`../01_Manuscript/LaTeX/paper_information.pdf`；副本 `../01_Manuscript/PDF/C2GES_Information_2026-09-16_diagnostic_submission.pdf`
- SHA-256：正文 `251c6f5d2153158cf97fbeb36c3881a79d1355ee929de57a982aaab47aaa923b`；PDF `a5c032f7ec4b1bdabb599c1598a8ba36c40f76c7c85f5cbb1ab9cbf53e870289`
- 投稿 ZIP：`../C2GES_Information_20260916_submission.zip`（19 文件，SHA-256 `2bb442fe98ca758750a4c38c05b8dc48146d93109b6848baa4bb6bee33c4adfd`），内含 tex/pdf 与磁盘一致，不含封面信。
- RSI 路径效用（2026-09-17）：协议 seed 20260917，SHA `f24cd0ea22d93a8d83a859b3255e662c00e78943b0cb9cf4f8f7dff5fdd77d46`；12-dev 冻结 historical@0.10；15-test held-out 110/260 为 redesigned 0.0652/0.1044 vs no-path 0.0654/0.1020 vs TextRank 0.0675/0.1031（非双预算全胜，非未见确认性）。历史 Full/no-path/unrenorm 数字未改。
- 补充 ZIP：`../C2GES_Information_20260916_supplementary.zip`（3 文件，SHA-256 `c8ce4d0ea37460b3eb1a142f4e3f68a1b87922dae4b2427ce1b96602f7565a2a`）；补充 PDF SHA-256 `8a8ecf3dc4176e4feab92f2e97df450453e26b018b01d45c765b757be791901b`
- 作者审阅 Word：`../01_Manuscript/LaTeX/paper_information.docx`；封面信 `INFORMATION_COVER_LETTER.md`；版式自检 `FORMAT_CHECK.md`
- 28 页，0 错误 / 0 Overfull / 0 未定义引用；参考文献 38 条；摘要 179 词；关键词 6。
- 通讯作者仍为 `yangyong1@sgepri.sgcc.com.cn`（未改成 126 邮箱）。
- 迁移自 Applied Sciences 版（`paper_applsci.tex`，原件保留为 `paper_applsci.tex.ORIG`）。
- **迁移陷阱记录**：`mdpi.cls` 的 Featured Application 块未按刊名门控，换刊后导致正文与摘要重叠，已移除（该块属 Applied Sciences 栏目）。
- 补充材料用通用 `article` 类，journal-agnostic，无需迁移。
- 评审记录：`../02_Revision_and_QA/04_Build_Reports/C2GES_INFORMATION_PREREVIEW.md`（7/10，4 MAJOR）与 `C2GES_INFORMATION_REREVIEW.md`（8/10，1 MAJOR）。
- 已修：信息科学定位贯穿（摘要/§2.1/§5.3/结论）；期刊中立化（正文 Applied Sciences 引用清零）；**MMR 归属错误**（原误归 Sentence-BERT，实为 Carbonell & Goldstein SIGIR 1998）；补 StrucSum（EACL Findings 2026）与 LexRank（JAIR 2004）；**Table 4 Role-only 值 0.1564→0.1563**（经源数据核验的四舍五入错误）。
- **二次评审抓到一处由修复引入的过度声称**（我曾把"未发现优势"写成"确证冗余"），已改回论文自身的保守措辞并补上实际证据（两个效应符号不一致、区间跨零、未做等价性检验）。打包前将摘要从 206 词压到 200 词（去掉“from three organizations”和“after extraction-rule revisions”），不改变任何数值或主张。

---

更新日期：2026-09-12  
目标期刊：MDPI *Applied Sciences*  
当前路线：诊断性、非确认性投稿  
诊断投稿门：`READY`，0 findings  
当前投稿必要项：`RESOLVED`，0 open（作者门户签核按用户要求暂不计技术包门禁）  
确认性路线：`NOT_READY_BY_DESIGN`，41 findings（保留为未来升级路线）

## 当前投稿文件

- LaTeX：`../01_Manuscript/LaTeX/paper_applsci.tex`
- 主稿 PDF：`../01_Manuscript/PDF/C2GES_Applied_Sciences_2026-09-12_diagnostic_submission.pdf`
- 补充材料 PDF：`../01_Manuscript/PDF/C2GES_Supplementary_2026-09-12_diagnostic_submission.pdf`
- 页数：主稿 27 页；补充材料 5 页
- 标题：*C²GES: A Diagnostic Evaluation of Role-Conditioned Extractive Summarization for Long Power-System Technical Reports*
- 投稿门报告：`../02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_SUBMISSION_READINESS.json`
- 公共验证报告：`../02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json`
- 证据锁：`../03_Reproducibility/Data/submission_final/DIAGNOSTIC_SUBMISSION_EVIDENCE_LOCK.json`
- 原 42 项处置记录：`../03_Reproducibility/Data/submission_final/CONFIRMATORY_42_FINDINGS_DISPOSITION.json`
- 当前要求解析：`../03_Reproducibility/Data/submission_final/CURRENT_SUBMISSION_REQUIREMENTS_RESOLUTION.json`

## 已完成的本地证据闭环

- E1 后访问探索性比较：112/112 单元通过；7 份报告、7 个系列、110/260-word 匹配预算。
- E3 探索性组件实验：182/182 单元通过；AB-0--AB-6、RP-00--RP-11、G-U/G-T 均已运行。
- E3 补充诊断：154 行 selection Jaccard、140 行 series effects、140 行 LOSO、26 行资源统计，以及明确的 `NOT_RUN` 人工指标记录。
- 论文回填：正文加入 Component Factorial Ablation 主表、LOSO/Jaccard/资源解释和可迁移的方法论经验。
- 补充材料：新增 Table S5--S8 和 Figure S4。
- 软件验证：43 项单元测试通过；诊断性公共验证 PASS。
- 发布验证：473 个文件，0 missing、0 mismatch、0 unlisted。
- PDF QA：主稿与补充材料均无未定义引用、LaTeX error 或 overfull box；重点页已逐页视觉检查。

## 科学边界

- 7 个外部报告系列在协议冻结前已经访问，只能称为 post-access exploratory pilot，不能称为未见确认性测试。
- DeepSeek 与 Codex 标签仅用于机器错误发现，不能称为两名真人或专家标注。
- 当前未招募人类参与者、未执行真人标注；未来真人研究必须在招募前取得适用的机构伦理决定。
- E3 支持负向或不确定的机制诊断，不支持确认性优越结论。
- 当前论文不主张系统优越性、结构代理的语义有效性或工程任务效用。
- 推荐配置为 no-path C²GES（provisional simpler configuration）。

## 未来恢复强主张时所需的确认性证据（不阻塞当前投稿）

若要恢复“Structure-Aware”、系统优越性或工程效用等强主张，仍须：

1. 由作者团队取得一批此前未查看、合法访问并按系列隔离的真实报告；
2. 招募两名独立真人标注者，其中至少一名具备电力系统或可靠性事件分析经验；
3. 在招募或数据采集前取得机构伦理批准或正式豁免决定。

合成数据、既有已访问报告和 LLM 标签只能用于压力测试或方法开发，不能关闭以上三道证据门。

### 增补计划执行状态（2026-09-26）

按 `../04_Wiki/C2GES_NEXT_EXPERIMENT_PLAN_20260926.md` 执行 P0–P1：CDX 深扫 21 个机构/主机（ENTSO-E 五个路径、NERC 根前缀、UK NESO/NGESO、ERCOT、AESO、北欧 TSO 等），新增下载 **30 份 PDF**；协议门禁后外部语料由 19 → **24 份**（grid 7 / market 9 / NERC 6 / 频偏 2）。

1. **方向稳定、均值检验脆弱**：路径层 260 词由 7 负 0 正（Holm 0.0469）变为 **10 负 1 正**（均值 −0.006908），但随机符号翻转 p 升到 0.444（Holm 0.678）——一份大正差文档支配均值；TextRank 也从 Holm 0.0324 降到 p=0.130。
2. **论文处置**：主结果保持预注册的 19 份；24 份作为**敏感性**写入 §4 外部小节与补充材料 Table S10；摘要删除 "after correction" 以便不再暗示稳健显著。
3. **臂级实验（P2 主体）已完成**：`run_external_arms_v3.py` 在冻结的 24 份语料上跑 7 臂 × 4 预算（`03_Reproducibility/Data/external_prospective_v1/external_arms_v3.json`）。判定：**H1（角色层可复现增益）不成立** —— 等词 110 下 AB2−AB0 = −0.03510（18 负 / 4 正 / 2 平，p = 0.0039，Holm 0.0774），等句数下才转正（+0.00626 / +0.01079，均不显著）；**H2（路径层无信息）成立** —— 四种预算下 Full−no_path 均值 ∈ [−0.00691, +0.00099]，bootstrap 单侧 95% 上界 ≤ +0.0047。结论：角色层的"增益"是**输出长度**的产物，路径层的"零"最稳健。
4. **产物**：`03_Reproducibility/Data/external_prospective_v1/{external_arms_v3.json, run_external_arms_v3.py, external_prospective_v2_expanded.json, run_external_prospective_v2.py, convert_to_markdown.py, fetch_with_snapshot_fallback.py}`。
5. **已完成（同日收尾）**：docx、三个 ZIP、公共验证报告与发布清单均已按新 tex/PDF 重算，臂级断言已加入公共验证矩阵——见本文件顶部当前构建节。
6. **仍失败的下载**：CE 2021 主报告、NESO Odessa / 2019-08-09、ERCOT 2021、NERC 1989 Quebec、北欧统计 2011 等 8 份（快照缺失或 500）。下一阶段计划见 `../04_Wiki/C2GES_NEXT_EXPERIMENT_PLAN_v2_20260926.md`。
