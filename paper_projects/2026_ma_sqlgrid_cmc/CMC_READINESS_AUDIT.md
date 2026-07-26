# MA-SQLGrid CMC 投稿就绪性终审报告（Final Submission-Readiness Audit）

审计日期：2026-07-22
审计对象：`source/manuscript_cmc/paper_cmc.tex`（PDF 24 页）+ `supplementary_cmc.tex`（PDF 9 页）
参照标准：`paper_projects/CMC_STYLE_PROFILE.md`（官方要求清单 + 10 篇语料库规范 + desk-reject 触发项）
审计方法：逐项核对官方要求；对新增章节（5.4 二代生成器、5.5 x10 规模实验）逐数字回溯证据文件；对照语料库中位数做水位评估；全量 desk-reject 触发项排查。**未修改任何稿件文件。**

---

## 一、官方要求合规清单（COMPLIANCE CHECKLIST）

| # | 检查项 | 状态 | 依据 |
|---|---|---|---|
| 1 | tsp.cls 模板，`cmc,article,submit,moreauthors,pdftex` 选项 | ✓ | tex 第 3 行：`\documentclass[cmc,article,submit,moreauthors,pdftex]{Definitions/tsp}`；编译干净（无 undefined citation、无 overfull box，仅 2 处轻微 underfull） |
| 2 | 单栏 US Letter、行号（submit 模式）、DOI 占位头 | ✓ | PDF 首页渲染确认（`http://doi.org/10.32604/cmc.2026.000000`、ARTICLE 标头、页边行号） |
| 3 | 标题实词大写 | ✓ | 标题符合 Capitalized Substantives 规范 |
| 4 | 作者/单位/通讯作者宏（`\Author`/`\address`/`\corres`） | ⚠ TODO | 宏全部就位，但内容为 `[TODO: Firstname Lastname]` 等占位符 —— **投稿前必须由作者填写**（题目已声明排除此项） |
| 5 | 摘要 200–400 词、单段、无引用、无换行 | ✓ | 实测 **349 词**；无 `\cite`；无 `\\` 断行；含 Background→Methods→Results→Conclusions 定量流（0.4389→0.7000→0.7278、+36.1、63.5%、74.7% 等直接进摘要，符合 CMC 数字化摘要风格） |
| 6 | 关键词 3–10 个、分号分隔 | ✓ | 7 个，分号分隔 |
| 7 | 顶层章节 5–8 个 | ✓ | 6 个：Introduction / Related Work / Method / Experimental Setup / Results and Discussion / Conclusions and Limitations（正是 §2 语料库众数区间） |
| 8 | 引言含明确贡献列表 + 组织段 | ✓ | 4 条编号贡献（语料库范围 0–4，中位数 3）+ "The rest of this paper is organized as follows" 段 |
| 9 | 后置声明块**精确顺序**：Acknowledgement→Funding→Author Contributions→Data Availability→Ethics→COI→(Supplementary)→References | ✓ | tex 第 437–455 行，六项声明顺序与模板完全一致，References 最后 |
| 10 | Acknowledgement 内含 AI 使用披露（TSP 标准措辞） | ✓ | 采用官方句式（"used ... in order to ... reviewed and edited ... take full responsibility"），并明确区分"被测 LLM 是研究对象"与"写作/编码辅助工具"两类，处理得比语料库先例（ChatGPT for readability）更完整 |
| 11 | Funding Statement | ⚠ TODO | 宏就位，内容为 TODO（用户填写；无基金则用官方句式） |
| 12 | Author Contributions（CRediT + 结尾句） | ⚠ TODO | 宏就位、含官方结尾句 "All authors reviewed and approved..."，CRediT 角色为 TODO |
| 13 | Data Availability 采用 5 种官方句式之一 | ✓ | "openly available in ... at URL" 句式 + GitHub 仓库 v0.2.0 + 明确列出遗留缺项（LLM client shim、v0.1 生成脚本）及其不影响复现的说明 —— 超出语料库 "on request" 默认水平 |
| 14 | Ethics Approval "Not applicable" | ✓ | 已按官方措辞给出 |
| 15 | COI 声明 | ✓/⚠ | 官方句式就位，尾随 `[TODO: confirm ...]` 需在投稿时删除确认 |
| 16 | Vancouver/NLM 参考文献（前 6 作者 + et al.、期刊缩写、DOI） | ✓（小瑕疵） | 46 条全部 Vancouver 格式，et~al. 截断正确，DOI/arXiv 链接齐全；**小瑕疵**：约 5 条期刊文献缺卷期页码（quamar2022、katsogiannis2023、huang2024survey、beyer2022、pauwels2024 只有年份+DOI），borovcak2026 的 ":80" 页码疑为 article number 误写 —— 属排版编辑可改正级别，非 desk-reject 项 |
| 17 | 单点连续引用 ≤5 条 | ✓ | 全文最大单处引用 4 条（正则全查 `\cite{}`，无 5 键及以上） |
| 18 | 图注下置 "Figure N:"、表注上置 "Table N:"、三线表、booktabs | ✓ | 全部 `\toprule/\midrule/\bottomrule`；表格均为可编辑 LaTeX（无图片表）；加粗有注（Table 2 注明 "Best execution accuracy in bold"）；无 1a/1b 子表 |
| 19 | 图片分辨率/格式（TIF 优先；线稿 ≥900 dpi、半调 ≥300、组合 ≥600） | ⚠ | 4 张 PNG：两张图表 300 dpi 元数据（1306×886 @11cm ≈ 301 dpi；2176×917 @\textwidth ≈ 335 dpi）、两张架构/流程图无 dpi 元数据但 1408px @11.9cm ≈ 300 dpi 有效分辨率。**满足 300 dpi 半调线，但按官方"线稿 900 / 组合 600"标准偏低，且非 TIF**。语料库实际多为 ~300 dpi PNG，被退回重制的风险低但存在 |
| 20 | 图片最大尺寸 16.51×20 cm | ✓ | 图宽 11–11.9 cm / \textwidth，合规 |
| 21 | 补充材料独立编译、S 编号、主文以 Table S1/Section S1 引用 | ✓ | 独立 9 页 PDF，S 编号重定义正确，主文 `\supplementary{}` 宏逐项列出 S1–S9；补充材料内无引用文献（"补充引用须入主列表"规则自动满足） |
| 22 | 页数与 APC | ✓（已知成本） | 24 页 → 超 15 页 9 页 → **APC = $1,600 + 9×$100 = $2,500**。低于 profile 预估的 28–35 页（供图/表/附录外移策略生效），语料库最长 32 页，24 页无长度风险 |
| 23 | Cover letter（原创性、非一稿多投、全体作者同意、COI、APC 承诺） | ⚠ 过期 | `cmc_cover_letter_draft.md` 已含原创性/非一稿多投/AI 披露/APC 承诺，但：(a) **缺一句显式 COI 声明**；(b) **内容已过期**：写的是 v0.1.0 + "四个 builder 模块 pending" + 2,520 条 trace，而稿件现为 v0.2.0 + builder 已收到 + 新增 x10 run（553 次调用）后 trace 总数应为 ~3,073；(c) 未提及新增的 x10 规模实验贡献点 |

**清单通过率：23 项实质检查中 17 项完全 ✓，5 项 ⚠（4 项为作者信息类 TODO——题目已声明排除；1 项为图片 dpi/格式警告），1 项 ⚠ 为 cover letter 过期（可由助手修复）。排除作者 TODO 后：17/19 ✓，2 项警告（图片 dpi、cover letter），0 项硬性不合规。**

---

## 二、新增章节数字抽查（SPOT-VERIFY，30 项全对）

### 2.1 x10 规模实验（§5.5，Table 7）↔ `source/code/experiment_final/outputs_deepseek_x10/RESULTS_SUMMARY.md` + `analysis/relaxed_metrics_deepseek_x10.json`

| # | 稿件数字 | 证据值 | 结果 |
|---|---|---|---|
| 1 | C2 x10 strict 0.3333 (60/180) | strict_acc 0.3333, strict_correct 60 | ✓ |
| 2 | C4 x10 strict 0.5944 (107/180) | 0.5944 / 107 | ✓ |
| 3 | C5 x10 strict 0.6500 (117/180) | 0.65 / 117 | ✓ |
| 4 | compact 优势 +26.1 点（vs v0.1 +36.1） | 0.5944−0.3333=0.2611；0.7000−0.3389=0.3611 | ✓ |
| 5 | 验证层 +5.6 点（vs v0.1 +6.7） | 0.6500−0.5944=0.0556；0.7667−0.7000=0.0667 | ✓ |
| 6 | C2 输入 token 2011.6→3042.6（+51%） | RESULTS_SUMMARY 表逐字一致 | ✓ |
| 7 | C4 输入 token 509.3→504.0（flat，~6× 便宜） | 同上（-1% flat；3042.6/504.0≈6.0×） | ✓ |
| 8 | C2 的 120 个 strict 错误中 99 个 shape mismatch | "99/120 errors are shape_mismatch" | ✓ |
| 9 | projection-tolerant 下 C2 0.8167 反超 C4/C5 0.6944/0.7000 | set_relaxed_acc 0.8167 / 0.6944 / 0.7000 | ✓ |
| 10 | 149/180 提示词跨尺度字节一致，其上 101/149 vs 102/149；跌幅全部集中于 31 个变更提示题（23/31→6/31） | anomaly 1 逐字一致 | ✓ |
| 11 | 540 次主调用 + 13 次修复调用、0 provider 错误、safe-SQL 1.0 | 逐字一致 | ✓ |
| 12 | 200 条 gold SQL 在 x10 库上复验 0 错误 | "200 questions, 0 gold-validation errors" | ✓ |
| 13 | LIMIT 80 字母序值清单截断机制（TX-* 名称掉出） | anomaly 1 完整对应 | ✓ |
| 14 | distractor 表仅对 C2 构成压力（C4/C5 builder 固定 8 表目录） | 判定 (a) caveat 逐字对应 | ✓ |

### 2.2 二代生成器与一致性（§5.4，Table 6）↔ `outputs_deepseek_chat/results.json` + `analysis/relaxed_metrics_deepseek.json` + `analysis/efficiency_stats_deepseek.json` + `outputs_deepseek_consistency/consistency_report.json`

| # | 稿件数字 | 证据值 | 结果 |
|---|---|---|---|
| 15 | deepseek C2/C4/C5 strict 0.3389(61)/0.7000(126)/0.7667(138) | results.json summary 完全一致 | ✓ |
| 16 | order-insensitive 0.3667/0.7944/0.8278 | relaxed_metrics_deepseek.json | ✓ |
| 17 | projection-tolerant 0.8500/0.7944/0.8278（C2 反超复现） | 同上（0.85/0.7944/0.8278） | ✓ |
| 18 | C4 509.3 vs C2 2011.6 输入 token，**74.7% 降幅** | efficiency derived: `c4_vs_c2_real_input_token_reduction: 0.7468` | ✓ |
| 19 | C5 输出 token 186.2 vs C4 46.6（≈4×），延迟 3014.2 vs 1054.0 ms（≈3×） | token_output_mean 186.2/46.6；latency 3014.2/1054.0 | ✓ |
| 20 | C2、C4 全部 360 次首次成功；C5 有 2 题各重试 1 次 | retry 分布 {0:180}/{0:180}/{0:178,1:2} | ✓ |
| 21 | 三条件共 576.3k 输入 / 50.9k 输出 token、540 调用、0 provider 错误 | 362093+91675+122482=576,250；8985+8396+33518=50,899 | ✓ |
| 22 | 一致性：C4 三次 0.7056/0.6944/0.7000，C5 0.7667/0.7667/0.7611，最大离散 1.1 点 | consistency_report.json 完全一致（0.7056−0.6944=0.0112） | ✓ |
| 23 | 判定一致率 98.3%（两条件），SQL 串一致率 82.2%/77.2% | verdict_agreement 0.9833/0.9833；exact_sql 0.8222/0.7722 | ✓ |
| 24 | C5 复现实现对档案 167/169 非修复选择一致（98.8%） | README_EXPANSION.md 第 62 行、MISSING_ARTIFACTS.md | ✓ |

### 2.3 原始正式 run 交叉复核（Table 2/3/4/5 及消融）↔ `analysis/relaxed_metrics.json` + `analysis/efficiency_stats.json` + `outputs/report.md` + `evidence/component_ablation_results.json`

| # | 稿件数字 | 证据值 | 结果 |
|---|---|---|---|
| 25 | C1–C5 strict 0.3944/0.4389/0.4000/0.7000/0.7278；relaxed 两列全部 10 个值 | relaxed_metrics.json 完全一致 | ✓ |
| 26 | 实测输入 token 5007.7/6346.7/4756.3/4859.0/5309.8；模板估计 381.3/710.3/202.0/259.2/258.2；63.5%/23.4% 两级降幅 | efficiency_stats.json（derived 0.6351/0.2344） | ✓ |
| 27 | 全 run 4.73M 输入 token；898/900 首次成功（C1、C4 各 1 次重试） | token_input_total 合计 4,730,287；retry 分布 | ✓ |
| 28 | shape accuracy 0.3278/0.3667/0.5056/0.8889/0.9722 | outputs/report.md | ✓ |
| 29 | 错误分类：C1 shape 95 / C2 90 / C3 67 / C4 34 denot+20 exec / C5 44+5；可执行率 0.9167/0.8889/0.9722 由 exec_error 反推吻合 | outputs/report.md | ✓ |
| 30 | 消融：去值提示 118/180 (0.6556)、去形状提示 77/180 (0.4278、shape acc 0.4389、provider failure 0.0056) | component_ablation_results.json 完全一致 | ✓ |

**抽查结论：30/30 全部与档案证据一致，零出入。** 新增章节（二代生成器 + x10）与既有章节的每个被查数字都能在版本化的 run 工件（results.json / relaxed_metrics / efficiency_stats / consistency_report / RESULTS_SUMMARY）中逐位对上，且稿件叙述（如"51% 增长""6 倍便宜""1.1 点离散"）的换算全部正确。

---

## 三、水位评估（vs 语料库中位数）

| 维度 | 语料中位数（范围） | 本文 | 相对水位 |
|---|---|---|---|
| 排版页数 | 18–19（14–32） | 24 | 高于中位，处于范围内；成本 $2,500 |
| 参考文献 | 30（22–56） | 46 | 高于中位 |
| 顶层章节 | 5–6（5–8） | 6 | 正中众数 |
| 摘要词数 | ~250（155–340） | 349 | 上限附近但合规（<400），定量密度高于全部语料 |
| 贡献条数 | 3（0–4） | 4 | 上限 |
| 图 | 5–6（4–9） | **4** | **唯一处于语料下沿的维度**（= 语料最小值，非低于范围） |
| 表 | 4–5（2–7） | 7 | 范围上限 |
| 数据集 | 1–2（自建常见，4/10） | 1 自建 + x10 变体 | 合规范内；自建有明确先例 |
| 基线/条件 | 4（0–7） | 4 基线条件 + 本法（C1–C3 + C4/C5），另有 6 系统能力对照表 | 达标中位 |
| 消融 | 6/10 有，正规表 4/10 | 正规消融表 + 通道归因 | 高于中位 |
| 显著性检验 | **2/10** 正式 | 配对符号检验（精确 p 值）+ Wilson 区间 + 三重复一致性界 | **远高于常模**（顶级差异化点） |
| 代码/数据释出 | **0/10** 代码 | 全量释出（数据+评测器+2,520+553 条 trace+分析脚本） | **远高于常模** |
| 期刊内先例引用 | — | 已引 CMC 2026;88(2) SQL-agents 论文并作定位对话 | 正确操作 |

**结论：除图数量处于语料下沿（4 张，恰为语料最小值）外，没有任何维度低于语料范围；实验强度（双生成器复现、一致性界、规模压力测试、显著性检验、全量开源）显著高于 CMC 常模。** 可选增强：把补充材料中 Table S5（按题型标签的准确率）画成分组条形图，即可到 5 张图、补齐语料中位——非必需。

一个"光学"层面注意点：strict 头名 0.7278/0.7667 低于 CMC 常见的 90%+ 准确率表。但 (a) 同刊 SQL-agents 先例本身报的也是任务准确率而非分类准确率，(b) 每张表都以相对增益（+26.1/+36.1 点）领句并加粗最优列，符合 profile §4.2 的缓解建议。风险可控。

---

## 四、Desk-Reject 触发项全排查

| # | 触发项 | 状态 |
|---|---|---|
| 1 | 错误模板/格式 | **通过**：tsp.cls + Vancouver + 单栏，编译零错误 |
| 2 | 六项声明缺失 / cover letter 不合规 | **有条件通过**：六项声明全部在位且顺序精确；但 Funding/CRediT/作者信息为 TODO（用户填写后才可投）；cover letter 草稿缺显式 COI 句且内容过期（见 §一#23） |
| 3 | iThenticate 相似度（含自有 Access 草稿回收） | **需用户确认**：本稿由 IEEE Access 版改写（`source/manuscript/` 同源）。只要 Access 版**从未投出、未挂 arXiv**，则无公开相似源，风险低；若存在任何预印本/在投记录，必须在 cover letter 披露 |
| 4 | 未披露生成式 AI 使用 | **通过**：Acknowledgement 双层披露（研究对象 vs 写作工具），措辞即官方句式 |
| 5 | 一稿多投/任何语言的先行发表 | **需用户确认**（cover letter 已含承诺句） |
| 6 | 摘要/关键词不合规 | **通过**：349 词、无引用、7 关键词 |
| 7 | 图表违规（<300 dpi、表为图片、无注加粗、1a/1b 子表、图内引用编号） | **基本通过，一项警告**：有效分辨率 ~300–335 dpi 达半调线但未达线稿 900 dpi 官方标准，且为 PNG 非首选 TIF；表格全部可编辑、加粗有注、无子表、图内无引用编号。最坏情形是编辑部要求重制图片（不致拒） |
| 8 | 英语质量 | **通过**：全文语言干净、句式受控，无机器翻译痕迹 |
| 9 | 数据可得性不足 | **通过（依赖仓库真实上线）**：声明为最强的"openly available at URL"档；**投稿前必须确认 `github.com/gaoxingkele/ma-sqlgrid` 公开可访问且 v0.2.0 release 真实存在**，否则该声明反而成为诚信风险点 |
| 10 | 引用操纵（>5 连引、自引集群） | **通过**：最大 4 连引；无自引集群 |

---

## 五、审计结论（VERDICT）

### (a) 现在是否达到 CMC 投稿标准（排除作者信息 TODO）？

**达到。** 排除作者信息类 TODO 后，全部硬性合规项通过（17/19 完全通过，2 项为软警告），30 项数字抽查零出入，实验强度在每个可比维度上等于或高于语料常模，且有精确的同刊先例锚点（borovcak2026, DOI 10.32604/cmc.2026.078330，已引用并做差异化定位）。稿件在格式层面不会被 pre-check 退回（前提是 TODO 填毕、仓库上线）。

### (b) 剩余阻塞项清单（含归属）

**用户必办（投稿硬前提）：**
1. 作者姓名/单位/通讯邮箱（tex 第 33–44 行 + supplementary 第 26 行 + PDF 元数据 `\AuthorNames`）；
2. Funding 声明内容（第 439 行）；
3. CRediT 作者贡献（第 441 行）；
4. COI 的 `[TODO: confirm]` 删除确认（第 447 行）；
5. 确认 GitHub 仓库公开、v0.2.0 release 真实可访问（Data Availability 声明的支点）；
6. 确认无预印本/无一稿多投；若有 Access 版投稿史或 arXiv 记录，在 cover letter 披露；
7. Cover letter 末端信息（全体作者同意、建议审稿人、通讯作者信息）；APC $2,500 预算确认。

**助手可办（建议投稿前完成，均为半小时级）：**
8. 更新 `cmc_cover_letter_draft.md`：v0.1.0→v0.2.0、"builder pending"→"已收到并字节级复验"、trace 数 2,520→~3,073、补一句显式 COI 声明、补 x10 规模实验贡献点；
9. （可选，降低编辑部退图概率）将 4 张 PNG 重渲染为 600–900 dpi（架构/流程图为线稿类，官方标准 900）或转 TIF；
10. （可选）修补 ~5 条缺卷期页码的期刊参考文献（quamar2022、katsogiannis2023、huang2024survey、beyer2022、pauwels2024）及 borovcak2026 的 ":80" 页码写法；
11. （可选）为 Table S5 增加一张按题型标签的分组条形图，使图数达到语料中位 5 张。

### (c) 预测决定分布（CMC，单盲，≥2 审稿人）

- **Desk-reject / pre-check 退回：<10%**（TODO 填毕且仓库上线的前提下；剩余风险主要来自图片 dpi 被要求重制——属可修复退回而非拒稿）。
- **小修后录用：~25%**（若两位审稿人都来自应用 NLP/LLM 应用方向，会把双生成器复现 + 全量开源 + 显著性检验读为超配）。
- **大修（最可能结果）：~45–50%**（预期意见集中于：公共基准缺失、数据库规模小/合成、convention-sensitivity 的口径质疑、要求补第三个生成器或公共 benchmark 验证）。
- **拒稿：~20%**（触发条件：遇到把"strict 增益主要来自 answer-contract 合规"读成"方法与评测器循环"的强硬审稿人，且编辑不给辩护机会）。
- 综合（含一轮大修后）最终录用概率估计：**70–80%**。CMC 大修的 5 天小修回合周转要求需要预留人力。

### (d) 诚实披露的可攻击性评估（LIMIT-80 工件 + convention sensitivity）

**1. Convention-sensitivity（最主要的攻击面）。**
最锋利的审稿人表述会是："C4/C5 的 shape-inference 规则是照着数据集标注协议写的，strict 指标恰好惩罚违反该协议的行为——所以头名增益是方法与评测器的构造性耦合（circularity），不是语义能力。" 稿件对此的处理是**先于审稿人把话说满**：§5.2 明文承认 "The shape-inference rules were designed against the dataset's annotation protocol, so this coupling is by construction"，并声明"任何 compact grounding 改善行内容检索的主张都不成立、本文不做此主张"。防线有四层，均可站住：(i) 所有条件收到相同的通用指令文本，差异只在逐题提示是否显式化——这是对"把答案契约显式化"这一机制本身的受控测量；(ii) strict 契约与部署契约同构（运维查询界面必须返回指定列、确定性排序），不是任意选择；(iii) 三套口径（strict / order-insensitive / projection-tolerant）全部报出，包括对本文不利的 C2 反超；(iv) 该模式跨两个生成器、跨两个数据库规模复现。**判定：框架完全可辩护，且论文已把"契约显式化比堆上下文更重要"上升为核心结论而非缺陷**。残余风险是审稿人要求"以行内容口径作为主指标重写"或"上公共 benchmark 证明非平凡性"——前者可用部署契约论辩回，后者是合理的大修要求（论文已列入 future work，但审稿人可能不接受推迟）。

**2. LIMIT-80 值清单截断工件。**
攻击面："规模实验恰好暴露你们的方法在 10 倍规模就退化 10 点，且 compact prompt 的 token 平坦性正是靠同一个缺陷（截断）买来的；外加 distractor 表只对 C2 构成压力，实验设计不对称。" 稿件同样已自曝全部三点（§5.5 两条 caveat + Conclusions 限制段），并给出杀伤力很强的归因证据：149/180 提示词跨尺度字节一致且得分不变（101/149 vs 102/149），全部跌幅精确定位于 31 个受截断影响的题（23/31→6/31），并点名修复路径（CHESS 式可扩展值索引，>80 distinct values/列阈值）。**判定：可辩护，且"缺陷被精确定位 + 修复路径具体"的写法在方法论上反而是加分项**；比隐藏该实验或只报 flat-token 结论的版本安全得多。残余风险：审稿人要求"实现值索引后重跑 x10 再投"——这是最昂贵的潜在大修项，建议预先准备（作为 rebuttal 备选实验或直接补做）。

**3. 其余披露（次要）。** C5 复现实现 98.8% 一致而非原始二进制、原 serving 栈不可用、单数据集合成基准、23.4% vs 63.5% vs 74.7% 三级 token 口径——全部已在正文以精确边界陈述，且三级 token 数字的三角互证逻辑（模板估计居中）严密。无一构成隐藏面。

**总评：这是一篇"把每个软肋自己先说穿并给出证据边界"的稿件。在 CMC 的审稿文化（2/10 论文做显著性检验、0/10 释出代码）里，其诚实披露密度远超常模，被武器化的净风险低于其带来的可信度收益。**

---

*审计人：Claude（Fable 5）。本报告未修改任何稿件文件；所有数字核对可由 `source/code/experiment_final/` 与 `source/evidence/` 下的版本化工件独立复验。*
