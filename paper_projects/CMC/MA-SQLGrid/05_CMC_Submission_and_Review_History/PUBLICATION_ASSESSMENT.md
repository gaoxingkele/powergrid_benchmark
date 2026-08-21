# MA-SQLGrid 投稿前发表能力评估（Publication Assessment）

- **日期**: 2026-07-17
- **评审模式**: 对抗式投稿前终审（paper_reviews 框架，参照 mintou_p3 ROUND_REVIEW 方法：claim–evidence 逐条核验 + 七维评分 + P0/P1/P2 + 决策预测）
- **稿件**: `source/manuscript/paper.tex`（14 页 PDF，45 条已验证参考文献）
- **当前目标**: CMC — Computers, Materials & Continua（Tech Science Press，SCIE，IF≈2–3）
- **证据核对源**: `source/code/experiment_final/outputs/`（900 条 prediction/score + 900 个 trace）、`formal_dry_run/`、`source/evidence/`（component ablation、mechanism/validator diagnostics）、`source/data/griddb_maintenance_v2_v0_1/`、`source/verification/`
- **核验方式**: 全部数字由本评审用独立脚本从原始 artifacts 重算，而非只对照报告文件

---

## 1. 论文内容与声明体系概述

**做什么的**：MA-SQLGrid 是一个面向电网检修数据库的 LLM Text-to-SQL 多角色（"multi-agent"）提示框架。在一个自建的合成 SQLite 基准 GridDB-Maintenance-v2 v0.1（8 张表、约 100 行数据、200 个问题-SQL 对，dev 20 / test 180）上，用一个固定的托管模型（`gpt-5.4-mini-2026-03-17`，经第三方代理 `api.krill-ai.com`，temperature=0、单种子单次确定性通过）比较 5 个条件：

- C1 仅 schema 直连提示 → 执行准确率 0.3944
- C2 全 schema+全值直连提示 → 0.4389
- C3 通用 CHESS-lite 多角色提示 → 0.4000
- **C4 紧凑领域上下文（本文核心机制：schema 选择 + 值规范化 + 答案形状推断）→ 0.7000**
- C5 = C4 + 无参考验证/候选重排/一次修复 → 0.7278

**核心 claims**（论文自己的 claim-to-evidence 表已明确写出边界）：
1. 紧凑领域上下文是主要机制收益（C4 vs C2：+0.2611，sign test p≈1.2e-12）；
2. 紧凑提示 token 估计 259.2 vs 全 schema 710.3；
3. 验证层只带来小幅增益（C5 vs C4：+0.0278，p=0.36，论文如实报告不显著）；
4. 形状提示是最大单一组件（去掉后 126/180→77/180），值提示贡献较小（→118/180）；
5. 全部主张限定于该本地基准，明确否认跨基准/生产就绪/多种子稳定性。

**定位**：这是一篇"领域实例化 + 消融解释"型的 LLM-based NL2SQL 应用论文，claim 纪律异常克制（大量 bounded/limitation 语句），但外部效度天花板由自建微型合成基准决定。

---

## 2. Claim–Evidence 核查（独立重算）

**首要问题澄清（任务指定核查项）**：`formal_dry_run/` 只有 1 个问题 × 5 条件 = 5 条 prediction（results.json 中 `question_count: 1`），**它只是流水线烟囱测试，不是论文证据来源**。论文数字全部来自 `outputs/`（正式重跑 run：180 问 × 5 条件 = 900 条 prediction/score/trace，elapsed 3168.8s）。trace 为真实 API 调用痕迹：模型串 `gpt-5.4-mini-2026-03-17`、provider `krill`、latency 1247–64438 ms 自然分布、900 条记录全部有非零 API token 计数、含原始 raw_response 与 rank_trace。**不是 mock，不是仅 dry-run。**

| # | 论文声明 | 独立核验结果 | 判定 |
|---|---|---|---|
| 1 | 五条件执行准确率 0.3944/0.4389/0.4000/0.7000/0.7278 | 从 scores.jsonl 重算 71/79/72/126/131 除以 180，逐项吻合 | ✓ |
| 2 | C4 vs C2 配对：49/2/77/52，均差 0.2611，p=1.179e-12；C5 vs C2：56/4/75/45，p=9.085e-13；C5 vs C4：12/7，p=0.3593 | 本评审用精确双侧 sign test 独立重算，六组数字与三个 p 值全部逐位吻合 | ✓ |
| 3 | 答案形状准确率 0.3278/0.3667/0.5056/0.8889/0.9722 | results.json 与 scores.jsonl 重算吻合 | ✓ |
| 4 | 组件消融：去值提示 118/180=0.6556、去形状提示 77/180=0.4278（shape acc 0.9167/0.4389） | `evidence/component_ablation_results.json`（真实 addendum run，360 条 prediction）逐项吻合 | ✓ |
| 5 | C5 行为：22 次选非首候选、15 次修复成为最终选择、5 个执行错误全为 `wo.schedule_date`(4)/`wo.schedule`(1) 列名错误 | 从 predictions.jsonl 重算 22 次非首候选 ✓；validator_diagnostics 记 15/180 修复接受 ✓；5 个执行错误的问题号与错误串逐条吻合 ✓（论文写"修复响应非空 16 例、15 例被接受"，diagnostics 文件只记录 15 例接受，16 无法直接核验，差异不实质） | ✓（细节 1 项无法核验） |
| 6 | 排序器权重敏感性：default 重算 132/180，no-shape 132，no-order/empty 131，exec-only 与 no-value 136 | validator_diagnostics.md 五个变体逐项吻合 | ✓ |
| 7 | 标签级诊断表（join 102 题 C2=0.382→C4=0.598；order-by +0.404；top-k +0.889；time +0.533；topology +0.727；self-join +0.778；group-by −0.083 等） | 用 questions.jsonl 的 sql_feature_tags × scores.jsonl 独立重算，9 行 × 4 列全部吻合 | ✓ |
| 8 | 数据集画像：200 对、dev20/test180、难度 74/102/24、filter 187、order-by 131、join 113、aggregation 66 等 | 从 questions.jsonl/splits.json 重算全部吻合；DB 行数（assets 18、work_orders 15、sensor_readings 26 等）与 SQLite 实测吻合 | ✓ |
| 9 | 值提示覆盖审计：170/180 题至少 1 条规范化值提示、330 个提示实例、111 个唯一渲染提示 | 从 contexts.jsonl 重算 170/330/111，逐项吻合 | ✓ |
| 10 | "紧凑提示将估计 token 从 710.3 降到 259.2"（摘要头条之一） | 估计值本身吻合（runner 内置估计器）。**但真实 API 输入 token：C2≈6347 vs C4≈4859，实际压缩仅 ~23%，而非表面上的 2.7 倍**——因为服务端存在 ~4500 token 的固定开销。论文在 claim 表里标注了"估计值"，但摘要未提示真实调用开销差距远小于此 | **部分 ✓（有误导风险）** |
| 11 | "形状推断是问题文本驱动的规则，未使用数据集元数据"；机制诊断 0 列数不匹配/180 | mechanism_diagnostics 确实显示推断分布与 gold 元数据 180/180 完全一致。规则与标注协议**共同设计**的痕迹明显（合成基准与方法出自同一流水线）：这不是造假，但推断规则实质上编码了标注规范（如"列表题投影 asset_name""需要确定性排序"），基线因不知道这些评测约定而被扣分 | **⚠ 循环性风险（见 §3 Soundness）** |
| 12 | 复现声明："发布包含数据集、评估器、条件提示、prediction/score、trace、消融输出……" | **✗ 关键实现代码缺失**：`main.py` 依赖的 `dev_chess_style_pilot`（即 MA-SQLGrid 核心——schema 选择/值规范化/形状推断/ranker 的全部实现）、`minimal_text2sql_smoke`（模型名/BASE_URL/SQL 提取）、`researchclaw.llm.client`、数据集生成脚本 `build_griddb_maintenance_v2.py` 均不在包内（代码内硬编码回退路径 `/media/lenovo/data2/cja/GridMind/...`）。评估器测试当前 11 failed / 2 passed（路径不匹配）。**从本包无法重跑实验，也无法审计核心方法实现** | **✗** |
| 13 | "本地 run 使用 NVIDIA RTX A6000 GPU（49,140MB VRAM）" | 生成全部经托管 API 完成，GPU 与实验无关——凑数式硬件声明，审稿人会质疑 | ✗（应删除） |
| 14 | 45 条参考文献 0 缺 0 多；8 条 2026 preprint 已外部核查 | verification_report.json 与 bib 逐键吻合；recent_reference_external_check.md 列出各 arXiv ID | ✓ |

**附加对抗性重算（论文未报告）**：本评审用集合不敏感（忽略行序）+ 允许多余投影列的宽松判分重算：C1 0.394→0.500，C2 0.439→**0.572**，C3 0.400→0.461，C4 0.700→**0.744**，C5 0.728→**0.806**。**C4−C2 差距从 +26.1pp 缩到 +17.2pp**：主效应真实存在，但头条数字约有 1/3 来自"基线不知道评测排序/投影约定"而非语义接地本身。论文在案例分析（Q021 正是此类）与 future work（"补充集合不敏感指标"）中已暗示此点，但未在正文量化。

**证据质量总评**：这是一套罕见地自洽、可审计的证据链——抽查 14 项，11 项完全吻合、1 项部分吻合、2 项不利发现（核心代码缺失、GPU 凑数）。问题不在数字真伪，而在**实验设计的外部效度**：微型自建合成库（约 100 行数据；且 Q081–Q200 即 test 集的 2/3 是模板扩展题）、单模型、单种子、无任何真实外部基线系统、评测约定与方法提示存在循环。

---

## 3. 七维评分（对标 SCIE Q2/Q3 应用刊录用水位）

| 维度 | Sev(0-4，越低越好) | 主要 findings |
|---|---|---|
| **Novelty** | **3.0** | [F-nov-1, SEVERE] 组件全部为已知技术（CHESS 式上下文构造、值链接 ValueNet/BRIDGE、执行引导重排），贡献 = 领域实例化 + 自建微基准。无真实系统级对手（C3 是自制 CHESS-lite，不是运行原版 CHESS/DIN-SQL/MAC-SQL）。[F-nov-2, MODERATE] 标题 "Multi-Agent" 名不副实——实为固定规则的多阶段提示流水线，无角色间交互/辩论，审稿人易以此发难。[F-nov-3, 正面] 问题定位（电网检修 NL2SQL）在应用刊有场景价值 |
| **Soundness** | **2.5** | [F-snd-1, SEVERE] 评测约定循环：gold 强制确定性 ORDER BY + 精确列数，C4/C5 通过 hint 获知该约定（形状推断与 gold 元数据 180/180 一致），基线被约定扣分；宽松判分下增益缩水 1/3（见 §2 附加重算）。[F-snd-2, MODERATE] token 压缩头条基于估计器，真实 API token 只降 23%。[F-snd-3, 正面] 单种子、C5 不显著、验证层定位为"次要收益"均如实陈述；泄漏扫描/契约检查真实存在。[F-snd-4, MINOR] `gpt-5.4-mini` 经第三方代理 krill，模型可信度无法外部验证 |
| **Experiments** | **3.0** | [F-exp-1, SEVERE] 单模型 × 单种子 × 单自建基准：无第二 LLM（开源模型 0 个）、无公开基准（Spider/BIRD/KaggleDBQA 均只在引文中出现）、无真实外部方法复现。[F-exp-2, MODERATE] 数据库仅 ~100 行、test 集 2/3 为模板扩展题，"benchmark"名义大于实质。[F-exp-3, 正面] 消融（2 通道）、标签级诊断、错误分类、ranker 敏感性分析在此规模下做得很完整 |
| **Reproducibility** | **2.8** | [F-rep-1, SEVERE] 核心方法实现（dev_chess_style_pilot 等 3 个模块）+ 数据集生成脚本不在发布包，硬编码原作者机器路径；从包无法重跑。[F-rep-2, MODERATE] 评估器测试 11/13 失败（路径问题，易修）；pdflatex 未验证可编译。[F-rep-3, 正面] 900 trace + prompt/context hash + 原始响应留档，审计粒度高于该档期刊常态 |
| **Related Work** | **1.0** | 45 键 0 缺 0 多、8 条 2026 preprint 已做外部可见性核查并明确降级为"contemporary context"；覆盖 prompting/分解/多智能体/执行验证四条线。[F-rw-1, MINOR] 缺与最相近工作的特征对比表 |
| **Clarity** | **1.5** | 写作清楚、边界语句纪律好。[F-clr-1, MODERATE] 大量流水线防御性行话（"repaired Stage 13/14 artifacts""bounded submission polish""protocol-B"）残留在正文，暴露自动化生成痕迹，投稿前须清洗。[F-clr-2, MINOR] "Robust"入题但正文用一整段消解，不如直接改题 |
| **Ethics** | **1.0** | 合成数据无隐私问题；限制章节诚实。[F-eth-1, MODERATE] GPU 声明与实际无关（凑数），须删；作者/单位为匿名占位（"Anonymous"+State Grid），CMC 为单盲，需补实名；AI 使用披露缺失（多数出版社 2025 起要求） |

**加权印象**：证据诚实度/自洽性远高于同档均值，但 Novelty×Experiments×Reproducibility 三项同时踩在"SCI 审稿人一眼可见"的软肋上：*自建 100 行玩具库 + 单模型单种子 + 核心代码缺失*。

---

## 4. 对 CMC（SCI）的可投性判断

**格式层硬阻断（当前不可投）**：
1. `paper.tex` 用的是 **IEEE Access 模板**（`\documentclass{ieeeaccess}` + `\doi{10.1109/ACCESS...}` 占位）——根本不是 CMC（Tech Science Press 有自己的 Word/LaTeX 模板与结构要求）。此稿显然原生目标是 IEEE Access，"CMC"目前只存在于项目命名中。
2. 作者/单位/通讯为匿名占位；CMC 单盲评审需实名 + ORCID + 基金 + 利益冲突 + （2025 起）AI 使用声明。

**口味匹配度：中等偏好**。CMC 大量刊发"LLM/深度学习 + 垂直行业应用"类论文，评审重 soundness 与完整性、对 novelty 容忍度较高、周期快；本文的诚实消融与诊断链在 CMC 属于加分项。**但**：
- CMC 审稿人对 NL2SQL 论文的最低期待通常包含**公开基准（至少 Spider 子集）或多模型对照**，"全自建 200 题合成库 + 单个经代理的闭源模型"很容易触发 "insufficient validation / limited significance" 类 major revision 甚至拒稿；
- 数据库仅 ~100 行会被至少一位审稿人写成 "toy example"；
- 无法验证的模型名（gpt-5.4-mini via krill）+ 包内缺核心代码，一旦被要求提供代码即卡壳。

**Desk-reject 风险**：按现稿（换模板、补实名后）投 CMC，desk 阶段风险约 10–15%（主题在 scope 内）；实质评审阶段预测：

| 状态 | Accept/Minor | Major | Reject |
|---|---|---|---|
| 现稿直接投 CMC（仅修格式） | ~15% | ~40% | ~45% |
| 完成下方 P0 后投 CMC | ~50% | ~35% | ~15% |

另请在投稿前自行核查当年**中科院预警期刊名单**及本单位期刊白名单对 Tech Science Press/CMC 的最新认定（逐年变动，本评审不作断言）。

---

## 5. 备选路线

| 路线 | 评估 |
|---|---|
| **A. 降档 EI（Engineering Letters / IAENG 系、或国内 EI 核心）** | **最稳**。现稿证据量（180 题 × 5 条件 + 消融 + 诊断）在 EI 层面属于上位水平；仅需换模板 + 实名 + 清洗行话 + 删 GPU 句，**约 2–3 人日、零新实验**即可投。缺点：EI 对职称/毕业的效力低于 SCI，需与作者需求匹配 |
| **B. 补实验后投 MDPI Electronics（SCIE, IF≈2.9, Q2, ~15 天首决）** | **性价比最高的 SCI 路线**。Electronics 对"应用 ML 组合 + 电力场景载体"高度对口，实测录用样本中显著性检验/多种子并非硬要求；本文的配对 sign test 已超其常态。需要补的核心是**多模型对照**（其录用底线是"有对照类"，本文已有 5 条件，但审稿人大概率追问第二个 LLM）。补 P0 的 1、2 两项（≈5–7 人日）后投，胜率明显高于 CMC 现稿 |
| **C. IEEE Access（SCIE, IF≈4.2, Q2, 二元决定, ~4 周）** | 模板已经是它的（讽刺的是现稿格式上只对 Access 合规）。soundness-not-novelty 完全对口本文气质；但 Access 二元判且一次重投限制，**必须先解决"单模型 + 玩具库"两个可见软肋再投**，否则一次 reject 就烧掉机会。建议完成 P0 全部 + P1 第 5 项后投 |
| **D. MDPI Applied Sciences** | 兜底 SCI；要求与 Electronics 类似而对口性稍差（Computing & AI section 可投）。作为 B/C 被拒后的改投站 |
| **不建议**：以现稿冲 IEEE TKDE/TII 或 NLP 会议——novelty 与基准规模差距为档位级，不是修补级 | |

---

## 6. 明确推荐

> **推荐：不要以现稿投任何 SCI（含 CMC）。执行下方 P0（约 6–9 人日，含一轮新实验），然后首选投 MDPI Electronics 或 IEEE Access；CMC 作为二选。若作者只需 EI 且要快，走路线 A（2–3 人日）现在就能动。**

理由：本文最稀缺的资产是"逐位可复算的诚实证据链"（本评审 14 项抽查 11 项精确吻合，这在同类稿件中极罕见），最致命的负债是外部效度（单模型/单库/循环评测约定）。负债恰好都是**可以用 1 周量级实验偿还**的——补上后这篇论文从"SCI 边缘"变成"SCI 舒适区"；不补则任何 SCIE 刊都在赌审稿人不问那三个必然的问题。

### P0 —— 投 SCI 前必须完成（合计 ≈ 6–9 人日）

| # | 修改项 | 说明 | 工作量 |
|---|---|---|---|
| P0-1 | **第二/第三生成器对照实验** | 至少加 1 个开源模型（如 Qwen2.5-Coder / DeepSeek 系）+ 可选 1 个不同闭源模型，重跑 C2/C4/C5（C1/C3 可省）。这是所有 NL2SQL 审稿人的第一问，也顺带回应"krill 代理模型不可验证"的质疑 | 2–3 人日 |
| P0-2 | **正文报告集合不敏感（order-insensitive）辅助指标** | 本评审已重算：C2 0.572 / C4 0.744 / C5 0.806——结论方向不变，主动报告可拆除"评测约定循环"这颗最危险的对抗性地雷；同时在 §5 明确说明形状推断规则与标注协议的关系 | 1 人日 |
| P0-3 | **发布包补齐核心代码** | 将 `dev_chess_style_pilot`、smoke、LLM client 接口、数据集生成脚本入包；修评估器测试路径（11 failed→0）；删除 `/media/lenovo/...` 硬编码 | 1 人日 |
| P0-4 | **模板与投稿机械项** | 按目标刊换模板（CMC/Electronics/保持 Access 三选一）；实名作者/单位/通讯/基金/COI/AI 声明；删 GPU 句；本地验证 LaTeX 可编译 | 1 人日 |
| P0-5 | **摘要与标题去险** | 摘要 token 压缩句改为"估计提示 token"并加真实 API token 脚注（或删）；标题 "Multi-Agent"→"Multi-Stage"/"Multi-Role"（或正文首段即定义），"Robust" 建议移出标题 | 0.5 人日 |
| P0-6 | **多种子敏感性最小证据** | temperature=0 下至少做 3 次重复调用一致性检查（或 3 seeds × C4/C5），把"单次确定性通过"从纯话术升级为有数据支撑 | 1 人日 |

### P1 —— 显著提升胜率（选做，合计 ≈ 4–7 人日）

| # | 修改项 | 工作量 |
|---|---|---|
| P1-1 | Spider/BIRD 抽取 1 个小型公开子集（或 KaggleDBQA 单库）跑 C2/C4，证明紧凑接地思想可迁移——直接消灭"toy benchmark"评语 | 2–3 人日 |
| P1-2 | 扩充 GridDB 数据规模（行数×10）或增加干扰表，说明选择机制在更大值空间下仍有效 | 1–2 人日 |
| P1-3 | §2 加特征对比表（vs CHESS/MAC-SQL/DIN-SQL/CORE-T 等 6–8 项能力维度） | 0.5 人日 |
| P1-4 | 清洗全稿流水线行话（repaired/Stage 13/protocol-B/bounded submission polish → 常规学术表述） | 0.5 人日 |
| P1-5 | 报告 API 成本与真实 token 消耗表（补强 efficiency 叙事的可信度） | 0.5 人日 |

### P2 —— 锦上添花

| # | 修改项 | 工作量 |
|---|---|---|
| P2-1 | 图 3/4 重绘（当前 charts 为流水线自动生成风格，期刊版建议统一配色与字号） | 0.5 人日 |
| P2-2 | 案例分析扩到 2–3 例（含一个 C5 修复失败案例，与 5 个 schedule_date 错误呼应） | 0.5 人日 |
| P2-3 | 附录给出 5 条件完整 prompt 模板 | 0.25 人日 |

---

## 7. 一句话总评

**这是一篇"证据链诚实度一流、实验野心三流"的论文**：所有能核的数字都核得上（真实 API 全量 900 次调用，绝非 dry-run 充数），但它把一套一流的审计纪律花在了一个 100 行数据的自建玩具库、一个模型、一个种子上，且约三分之一的头条增益来自基线不知道的评测约定。以现稿投 CMC 是把一手可以变好的牌提前摊掉；花 6–9 人日补齐多模型对照与宽松指标后，Electronics/IEEE Access/CMC 三个 SCIE 目标都从"赌"变成"稳中求进"；若只要 EI，现稿修格式即可出手。
