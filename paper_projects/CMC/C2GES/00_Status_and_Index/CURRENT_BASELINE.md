# C2GES 当前基准

更新日期：2026-09-25

## Information 版（2026-09-25 修订，当前）

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

- 正文：`../01_Manuscript/LaTeX/paper_information.tex` SHA-256 `fefc28015e9754bec5efc87fca10c082720a951f250224df38676a814db87361`
- 主稿 PDF：`../01_Manuscript/LaTeX/paper_information.pdf` SHA-256 `01e41bf20d0a2d6d43117854a4d62da1e2d5087315b37d03788546544b61cd3e`；**33 页**，6 图 15 表 44 参考文献，摘要 **200 词**，0 错误 / 0 Overfull / 0 未定义引用
- 投稿 ZIP：`../C2GES_Information_20260922_submission.zip`（20 文件，`fc2504f6b66ef6e957f5829d2d4e5ba6abed110add318120c615a693babd7c4f`，`fresh_extract: PASS`）
- 评审 ZIP：`../C2GES_Information_20260922_review.zip`（24 文件，`bd965d03365942c07efd0bf165776244b6221cf9e367bad117c93aa68f08ab75`）
- 补充 ZIP：`../C2GES_Information_20260922_supplementary.zip`（3 文件，`8cb652a66f9a12a7e16f6003948e321dd68e041395cf2867a00b5ab2bcf08120`；补充 PDF 6 页，新增 **Table S10**）
- 公共验证：`../02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json` —— route `diagnostic`，**PASS**，0 failures（新增 `external_prospective_checks()`）
- 发布清单：`RELEASE_MANIFEST.json` **567 文件**，`--check` PASS

### 外部 AI 评审提交（2026-09-25）

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
