# C2GES CMC 投稿就绪度终审报告（Final Submission-Readiness Audit）

- 审计日期：2026-07-22
- 审计对象：`source/manuscript_cmc/paper_cmc.tex`（PDF 26 页）+ `supplementary_cmc.tex`（PDF 5 页）
- 参照标准：`paper_projects/CMC_STYLE_PROFILE.md`（官方要求清单 + 10 篇语料库常模 + desk-reject 触发项）
- 审计方式：逐项核对 tex/pdf/bbl/log/图片二进制/运行工件 JSON/GitHub 发布页；未改动稿件任何文件

---

## 一、官方要求合规清单（Compliance Checklist）

**通过率：21/24 全项通过（✓），3 项为作者待办或轻微警告（⚠），0 项硬性不合规（✗）**

| # | 检查项 | 结果 | 依据 |
|---|---|---|---|
| 1 | 模板：`tsp.cls`，类选项 `cmc,article,submit,moreauthors,pdftex` | ✓ | paper_cmc.tex L3；PDF 首页呈现 TSP 刊头、"Version July 20, 2026 submitted to Comput Mater Contin"、CC-BY 脚注 |
| 2 | 单栏 US Letter、编号标题、单倍行距 | ✓ | PDF 目视核验（第 1–2 页） |
| 3 | 标题：精确、实词大写 | ✓ | "Causal-Role-Aware Extractive Evidence Selection for Power Grid Reliability Reports" |
| 4 | 作者全名 + 上标机构 + 通讯作者 * + 公开邮箱 | ⚠ 作者待办 | `\Author`、`\address`、`\corres` 均为 `[TODO:...]` 占位符（共 8 处 TODO），格式框架正确 |
| 5 | 摘要 200–400 词、单段、无引用、无换行 | ✓ | 实测 347 词；无 `\cite`；无 `\\` |
| 6 | 摘要含定量结果（对标 2025–2026 语料库风格） | ✓ | 内嵌 0.2983 / +41% / +31% / +51% / CI / p 值 / 0.2604 / 0.2787 / 0.5887 |
| 7 | 关键词 3–10 个、分号分隔 | ✓ | 6 个，分号分隔 |
| 8 | 顶层结构 5–8 节 | ✓ | 6 节（Intro / Related Work / Task & Benchmark / Method / Experiments-Results-Discussion / Conclusions），恰为语料库众数区间 |
| 9 | 引言含明确贡献列表 + 组织段 | ✓ | 3 条 itemize 贡献 + "The rest of this paper is organized as follows" |
| 10 | 后置声明块六项、顺序精确 | ✓ | 程序化核验顺序：Acknowledgement → Funding → Author Contributions → Availability → Ethics Approval → Conflicts → Supplementary → References，与 §1.3 完全一致 |
| 11 | AI 披露置于 Acknowledgement，且**同时覆盖**(a) 稿件撰写辅助 (b) agent 生成/验证标签的来源 | ✓ | L519：先声明 "used large-language-model-based agent tooling in order to construct and verify the benchmark labels"（标签来源），再声明 "used large-language-model-based tools in order to assist with drafting and editing"（撰写辅助），并以 TSP 规定句式收尾 "reviewed and edited the content as needed and take full responsibility" |
| 12 | Funding Statement | ⚠ 作者待办 | TODO 占位符（已附标准句式提示） |
| 13 | Author Contributions（CRediT + 规定结尾句） | ⚠ 作者待办 | TODO 占位符（模板句已含 "All authors reviewed and approved..."） |
| 14 | Availability：五种许可句式之一 | ✓ | 采用 "openly available in ... repository at URL" 句式；**已在线验证** github.com/gaoxingkele/c2ges release v0.2.0 真实存在，发布说明与稿件承诺内容一致（数据集、Executor 工件、learned/LLM baseline 输出、验证代码） |
| 15 | Ethics Approval "Not applicable" | ✓ | 已给出并说明仅分析公开 NERC 报告 |
| 16 | Conflicts of Interest | ✓ | 标准句 |
| 17 | Vancouver/NLM 参考文献（vancouver.bst、前 6 作者 + et al.、缩写刊名、DOI/CrossRef） | ✓ | bbl 抽查：`Xie L, Zheng X, ... Proc IEEE. 2022;110. [CrossRef]`；`Hamann HF, ... et al. arXiv:2407.09434. 2024.`（含 `\adot` 保护）；会议条目符合 Proceedings 格式 |
| 18 | 单点连续引用 ≤5 | ✓ | 43 个 `\cite` 命令，单命令最多 4 个键，无相邻堆叠 |
| 19 | 引用全闭合（无未引用 bib 条目 / 无缺失键） | ✓ | 47 条 bib = 47 条被引，0 缺失；参考文献数 47 高于语料库中位数 30 |
| 20 | 图：≥300 dpi、"Figure N:" 置下 | ✓ | 4 图；按 0.72/0.6 版面宽换算有效分辨率 ≈289–402 dpi（bar chart 二图带 220 dpi 元数据但像素量按印刷宽度足够）；caption 由 cls 排为 "Figure N:" |
| 21 | 表：可编辑 LaTeX 三线表、"Table N:" 置上、无子表编号 | ✓ | 8 表全部 booktabs 三线表（8 表略高于语料库最大值 7，属可接受偏高） |
| 22 | 补充材料单独成册、S 编号（Table S1/Section S1） | ✓ | supplementary_cmc.pdf 5 页，S1–S6；补充材料内无引用文献，规避了"补充引用须同录主表"问题 |
| 23 | 页数/APC 测算 | ✓ | 主文 26 页（log 实测），在语料库 14–32 页区间内；APC = $1,600 + 11 页超页费 $1,100 = **约 $2,700**（低于 profile 对 C2GES 预估的 $2,600–3,100 上限内） |
| 24 | 编译健康度 | ✓ | 无 undefined/multiply-defined 引用；6 处 Overfull（轻微）；19 条 BibTeX "empty pages" 警告（会议/arXiv 条目无页码，NLM 格式允许；见遗留小项） |

**遗留小项（非阻塞）**：① `xie2022massively`（Proc IEEE 缺页码）、`madabhushi2023survey`（缺卷期页码）等少数期刊条目字段不全，建议补齐；② 摘要中 "stays ahead of two neural rerankers" 为点估计措辞（未称显著），建议加 "in point estimate" 更稳（见叙事风险节）；③ 主结果柱状图 fig_2 未纳入 BM25 与三个新 baseline（正文已说明"original main-condition chart"），审稿人可能要求更新图。

---

## 二、新增 "Learned and LLM Baselines" 内容数字抽查（Spot-Check）

对照 `baseline_runs_2026-07-20/` 三个 `summary.json` 原始工件 + `RESULTS_SUMMARY.md`，逐项核对主文 5.5 节（Table 8）与补充材料 S6（Table S6）。**结果：25+ 项全部一致，0 处不符。**

| 稿件数字 | 工件值 | 结果 |
|---|---|---|
| BGE F1/P/R/ROUGE-L = 0.2604/0.2517/0.3013/0.3490 | 0.26036/0.25167/0.30125/0.34897 | ✓ |
| BGE vs C2GES：−0.0379 [−0.0739, −0.0010], p=0.0448 | −0.03786 [−0.0739, −0.0010], p=0.0448 | ✓ |
| BGE 自身 95% CI [0.2278, 0.2946] | [0.22781, 0.29458] | ✓ |
| BGE vs TF-IDF +0.0482 [0.0210, 0.0747] p<0.001；vs SBERT +0.0632 [0.0260, 0.0995] p=0.0006 | 工件 p=0.0002 / 0.0006 | ✓ |
| Cross-encoder F1/P/R/ROUGE-L = 0.2787/0.2717/0.3188/0.3667 | 0.27871/0.27167/0.31875/0.36668 | ✓ |
| CE vs C2GES：−0.0196 [−0.0539, +0.0140], p=0.246 | −0.01957 [−0.05386, +0.01398], p=0.2464 | ✓ |
| CE 自身 95% CI [0.2492, 0.3095] | [0.24919, 0.30945] | ✓ |
| CE vs TF-IDF +0.0665 [0.0389, 0.0941]；vs SBERT +0.0815 [0.0544, 0.1069]，均 p<0.001 | 0.06652 [0.03886, 0.09412] / 0.08148 [0.05443, 0.10686]，p=0.0 | ✓ |
| LLM F1/P/R/ROUGE-L = 0.5887/0.5950/0.6342/0.5942 | 0.58869/0.59500/0.63417/0.59421 | ✓ |
| LLM vs C2GES：+0.2905 [+0.2533, +0.3255], p<0.001 | +0.29048 [0.2533, 0.3255], p=0.0（即低于 10000 样本分辨率） | ✓ |
| LLM 自身 95% CI [0.5569, 0.6182]；vs TF-IDF +0.3765、vs SBERT +0.3915 | 完全一致 | ✓ |
| 运行成本：200 次调用、约 8.5 分钟、约 0.8M 输入 token、约 US$0.2–0.3 | RESULTS_SUMMARY §4 完全一致（并如实注明 token 为字符换算估计） | ✓ |
| 200 题全部有效预测、K=3、CPU 本地运行、文档簇 bootstrap 10000 样本 | 工件 ok_questions=200、device=cpu、samples=10000 | ✓ |
| 摘要相对增益 41%/31%/51% | 复算 0.2983/0.2122=1.406、/0.2273=1.312、/0.1972=1.513 | ✓ |

**关键否定性核验：全文任何位置均未声称对 cross-encoder 的显著优势。** 四处相关表述均合规：5.5 节明确写 "no statistically significant advantage over the cross-encoder is claimed"；结论写 "statistically indistinguishable from a cross-encoder"；S6 写 "the cross-encoder deficit is not statistically significant; no significant advantage ... is claimed"；讨论节仅称 "strongest tested reranker in the deterministic-or-local deployment class"（点估计类内表述）。唯一稍弱处是摘要的 "stays ahead of two neural rerankers"（未标注仅为点估计），属措辞级警告而非虚假声明。

另：主文其余表格（Table 3–7）此前已由独立复核脚本对 Executor `details.jsonl`（2400 行）完成 108/108 校验（RESULTS_SUMMARY §5），本次抽查其中 6 项（0.2983±0.2409、+0.0861 [0.0581,0.1145]、+0.0060 p=0.0254、BM25 0.2273、query-only 0.2152、fixed-legacy +0.0403）均一致。

---

## 三、水平评估（vs CMC 语料库常模）+ 叙事风险对抗评估

### 3.1 各维度对标

| 维度 | 本稿 | CMC 常模（10 篇语料库） | 评级 |
|---|---|---|---|
| Baseline 数量 | 8 个基线条件 + 4 个消融变体 + 3 个 learned/LLM 条件（共 12+ 条件） | 中位数 4，≥5 者仅 4/10 | **远高于常模** |
| 数据集 | 1 个自建域内基准（自建常见，4/10） | 1–2 | 达标 |
| 统计严谨性 | 文档簇配对 bootstrap、95% CI、p 值、预注册主比较、多重比较自谨、K 敏感性 | 仅 2/10 有正式显著性检验 | **远高于常模**（本刊差异化优势） |
| 代码/数据开放 | GitHub 完整 deposit（已在线验证 v0.2.0） | 0/10 放代码 | **远高于常模** |
| 图数 | 4 | 中位 5–6 | 略低（可接受；已含架构图 Fig.1 与流水线图） |
| 表数 | 主文 8 | 中位 4–5、最大 7 | 略高（可接受） |
| 消融 | 3 变体 + 角色分层 + fixed-legacy 对照 | 6/10 有、典型 2–6 变体 | 高于常模 |
| 诚实性/局限披露 | 标签来源、cue-label 循环性、单次执行、K 预算局限全披露 | 语料库极少见 | 远高于常模 |

**结论：没有任何维度低于 CMC 发表水平；统计严谨性、开放性、baseline 广度均显著高于本刊常模。** 绝对分数偏低（0.2983）的观感风险已按 profile §4.2 建议全部落实：相对增益领跑表述、任务难度校准段（并引用两篇 CMC 在刊论文的 strict-match 低分先例 `borovcak2026evaluating`、`ahmad2026mitigating`，这是很聪明的"以刊证刊"策略）、bootstrap 前置、按列加粗。

### 3.2 叙事风险对抗评估（"LLM 翻倍"是否杀死方法贡献？）

**对抗性结论：不致命，但确实将论文的重心从"方法论文"移向"基准 + 类内最优方法论文"，录用命运更多取决于审稿人是否认可基准贡献。**

支撑面（稿件已构筑的防线）：
1. **类内定位闭环**：透明/确定性/CPU 可部署类内 C2GES 仍是实测最强（对 BGE 边缘显著、对 CE 不可区分但点估计领先），且该类的合规性论证具体（监管性事后审查要求可分解、确定性、离线——5.5 与 5.7 两处落地）。
2. **循环性反向套利**：4.4 节明确指出标签为 LLM-agent 生成/验证，LLM 的 0.5887 部分可能是 LLM–LLM 一致性而非纯任务优势——这把"LLM 翻倍"从"方法失败"重构为"上界参考 + 标签可学习性证明 + 基准区分度证明（0.05–0.59 无饱和）"。这是全稿最强的一步棋。
3. **一致性核验**：摘要（"honest upper reference"）、引言（无 SOTA 声称）、5.5、5.7、结论五处口径完全一致；全文 grep 无 "state-of-the-art"/"SOTA"/"outperforms all" 类语言。**论文任何位置都没有把 C2GES 卖成 SOTA。**

暴露面（审稿人仍可攻击、稿件未完全封堵的点）：
1. **"本地开源 LLM"缺口（最锐利的攻击）**：稿件把 LLM 一侧等同于"remote proprietary endpoint"，但审稿人可以指出：本地部署的开源权重 LLM（Qwen/Llama 级）既离线、又可能大幅超过 0.2983，这会击穿"部署类"二分法。稿件仅在局限节承认"LLM baseline is a single model evaluated zero-shot"，未正面处理本地 LLM 选项。**建议在回复信预案或局限节补一句**（可分解性论证仍然成立——本地 LLM 依旧无 per-term 分解——这一防线要讲清楚是"可审计性"而非"离线性"在承重）。
2. **成本论证偏弱**：$0.2–0.3/200 题的 API 成本对任何机构都可忽略，"零边际成本"不是有效卖点；承重的应是确定性/可分解/无版本漂移，稿件 5.7 已把重心放对，但 5.5 仍并列列举成本，可能被指避重就轻。
3. **审稿人可要求把人工金标子集做掉而非承诺**：循环性披露越诚实，"先做 50–100 题双人标注再谈"的大修要求越可能出现。这是最可能的 major revision 内容。

---

## 四、Desk-Reject 扫描（对照 profile §5 十项触发器）

| 触发器 | 状态 |
|---|---|
| 1. 错误模板/格式 | 安全（tsp.cls + Vancouver + 完整后置块） |
| 2. 缺失强制声明 | 安全（六项齐全；**但 Funding/Contributions/作者信息为 TODO，带占位符提交必被退回** — 属作者填写项）；投稿信（原创性、非一稿多投、全体作者同意、COI、APC 承诺）**尚未见成稿** |
| 3. iThenticate 相似度 | 需注意：本稿由 IEEE Access 版改写而来，正文经过实质重写（结构、句式均已重排）；若存在 arXiv 预印本或曾投他刊，**必须在投稿信中披露** — 作者确认项 |
| 4. 未披露生成式 AI | 安全（双重披露：标签来源 + 撰写辅助，句式符合 TSP 规定） |
| 5. 一稿多投/已发表 | 作者确认项（Engineering Letters 目录名暗示曾定位他刊，须确认已撤回/未投） |
| 6. 摘要/关键词不合规 | 安全（347 词、无引用、6 关键词） |
| 7. 图表违规 | 安全（无截图图、无图内引用编号、无子表；有效 dpi ≈289–402；fig_4 若被排至更宽版面建议导出更高像素版备用） |
| 8. 英语质量 | 安全（全文语言为出版级；无需强制编辑证书） |
| 9. 数据可用性不足 | 安全（五句式之一 + 仓库在线可达、release 与稿件描述一致） |
| 10. 引用操纵 | 安全（最长连引 4；无期刊自引集群） |

**结论：0 个内容性 desk-reject 触发；仅"占位符未填 + 投稿信未备"两项形式性事项，均为作者动作。**

---

## 五、终审裁定（Verdict）

### (a) 现在是否达到 CMC 投稿标准？

**是（排除作者待办后）。** 稿件在格式合规、实验强度、统计严谨性、开放性、诚实披露五个维度全部达到或显著超过 CMC 2025–2026 在刊水平；全部数字与运行工件逐项吻合；无内容性 desk-reject 风险。这是可以按下提交键的稿件——前提是完成下述作者动作。

### (b) 剩余阻塞项（全部为作者动作，稿件本身无阻塞）

| # | 阻塞项 | 责任方 | 说明 |
|---|---|---|---|
| 1 | 作者姓名/单位/城市/通讯邮箱（6 处 TODO） | 作者 | 硬阻塞，占位符提交必退 |
| 2 | Funding Statement（1 处 TODO） | 作者 | 硬阻塞 |
| 3 | Author Contributions CRediT（1 处 TODO） | 作者 | 硬阻塞（单作者亦建议保留声明） |
| 4 | 投稿信：原创性、非一稿多投、全体作者同意、COI、APC 支付承诺，及预印本/前投披露 | 作者 | 硬阻塞（TSP 预审查核） |
| 5 | 确认 Engineering Letters/其他刊无在投状态 | 作者 | 合规确认 |
| 6 | （建议）补齐 2–3 条参考文献缺失卷页码；摘要 "stays ahead" 加 "in point estimate"；fig_2 更新纳入新 baseline | 作者/可选 | 非阻塞打磨 |

### (c) 预测决策分布（假设待办完成后提交）

- Desk reject / 预审退回：**<5%**（格式全合规、域内先例充分）
- 直接 Accept / minor revision：**15%**
- **Major revision（最可能，约 55%）**：预计意见集中在 ① 人工金标子集（把承诺变成结果）② 本地开源 LLM 对照 ③ 40 文档规模外推性 ④ 图表更新
- Reject：**25–30%**：触发条件是遇到"绝对分 0.30 无实用价值 + LLM 已解决该任务"立场的审稿人且其不认可基准贡献；两名审稿人同时持此立场的概率不高，但非零

修回后最终录用的综合概率估计：**60–70%**。

### (d) Top-3 审稿攻击向量与稿件应答现状

| # | 攻击向量 | 稿件是否已答 | 评估 |
|---|---|---|---|
| 1 | "零样本 LLM 得分翻倍，为什么还需要你的方法？——尤其是本地开源 LLM 也能离线跑" | **部分已答**：类内定位、可审计性/确定性/监管场景论证（5.5/5.7/结论三处）+ LLM–LLM 循环性反制（4.4）均已就位；但"本地开源 LLM"缺口未正面处理，防线须从"离线性"收缩到"可分解性/确定性" | 最大风险点；建议备好回复预案或补一句限定 |
| 2 | "标签是 agent 生成 + agent 验证，循环性让所有结论存疑；请提供人工金标" | **已诚实应答但未解决**：4.4 + 局限节完整披露循环性双向影响，预告 50–100 题双人标注 + Cohen's κ 计划 | 大概率成为 major revision 的核心要求；建议提前启动金标子集 |
| 3 | "0.2983 的 F1 太低 / 40 篇文档太小，结论站不住" | **已充分应答**：任务难度校准段（含两篇 CMC 在刊 strict-match 低分先例）、相对增益主导表述、文档簇 bootstrap、逐文档离散度全披露（0.08–0.52）、明确不做广义外推声明 | 防御最完备的一项；残余风险低 |

---

*审计人注：本审计未修改稿件任何文件。所有数字核对基于 `baseline_runs_2026-07-20/{crossencoder,bge_reranker,llm_zeroshot_deepseek}/summary.json`、`RESULTS_SUMMARY.md`、`paper_cmc.log/.bbl/.blg` 及 GitHub release 页面在线核验。*
