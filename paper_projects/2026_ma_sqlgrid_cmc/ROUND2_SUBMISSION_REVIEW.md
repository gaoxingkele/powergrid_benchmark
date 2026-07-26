# Round-2 投稿前终审：MA-SQLGrid → MDPI Electronics（主选）/ IEEE Access（备选）

- **日期**: 2026-07-19
- **评审轮次**: Round 2（升级后终审；对抗式 paper_reviews 框架，参照 mintou_p3 ROUND_REVIEW 方法）
- **稿件**: `source/manuscript/paper.tex`（680 行，IEEE Access 模板，45 条已验证参考文献）
- **前序**: Round-1 `PUBLICATION_ASSESSMENT.md`（2026-07-17）：七维 Nov 3.0 / Snd 2.5 / Exp 3.0 / Rep 2.8 / RW 1.0 / Clr 1.5 / Eth 1.0；结论"不要以现稿投任何 SCI"
- **升级记录**: `SCI_UPGRADE_CHANGELOG.md`（2026-07-17 分析重算 + 2026-07-19 DeepSeek 真实二模型/一致性实验）
- **证据核对源**: `source/code/experiment_final/outputs/`（900 预测/评分/trace）、`outputs_deepseek_chat/`（540 调用）、`outputs_deepseek_consistency/consistency_report.json`（1080 调用）、`analysis/relaxed_metrics{,_deepseek}.json`、`analysis/efficiency_stats{,_deepseek}.json`、`source/evidence/component_ablation_results.json`、数据集 `source/data/griddb_maintenance_v2_v0_1/`
- **核验方式**: 本评审用独立 Python 脚本从原始 artifacts **逐项重算**（不只对照报告文件），含对新 DeepSeek 证据链的字节级 prompt 比对与 C5 排序器重放

---

## 0. Round-1 P0/P1 项解决状态核查（逐条核实，不信任 changelog）

| R1 # | 级 | 修改项 | 当前状态（本评审独立核实） | 判定 |
|---|---|---|---|---|
| P0-1 | P0 | 第二生成器对照实验 | **已完成且为真实 API run**：`outputs_deepseek_chat/` 540 条记录，`base_url=https://api.deepseek.com/v1`、temp 0、0 provider 错误；本评审抽查 Q021 的 C2/C4 prompt 与归档 trace **字节级一致**（sha256 相同）；strict 61/126/138 从 scores.jsonl 重算吻合 | **已解决** |
| P0-2 | P0 | 正文报告 order-insensitive 辅助指标 | §6.1 "Evaluation-Convention Sensitivity" 新增双松弛指标表（15 格全部与 relaxed_metrics.json 吻合），且比 R1 要求走得更远：主动披露 projection-tolerant 下 **C2 0.8722 > C4 0.7444 的反转**，并在 DeepSeek 上复现（0.8500 > 0.7944） | **已解决（超额）** |
| P0-3 | P0 | 发布包补齐核心代码 | 部分解决：评估器测试 13/13 通过（本评审实测）、`main.py` 硬编码 `/media/lenovo` 路径已删（grep 无残留）、分析脚本可重算全部数字；**但 `dev_chess_style_pilot`（C4 上下文构建核心）、smoke、LLM client、数据集生成脚本仍缺**，由 `MISSING_ARTIFACTS.md` 显式登记，二模型 run 通过复用归档 prompt 绕开了该依赖 | **部分解决**（可审计性达标，从零重跑 C4 上下文仍不可能） |
| P0-4 | P0 | 模板与投稿机械项 | GPU 句已删并换成准确陈述（§5 L209）；DA/AI/Funding/COI 四个后置声明骨架已加；**但作者仍为 Anonymous、4 个 [TODO] 未填、模板仍为 IEEE Access、LaTeX 编译未验证（本机无 TeX，paper.pdf 停留在 06-27 旧版，manuscript/ 下无 charts/ 目录与 ieeeaccess.cls）** | **部分解决**（内容✓，机械项全悬） |
| P0-5 | P0 | 标题与摘要去险 | 标题已改 "Multi-Stage Context-Grounding"（Multi-Agent/Robust 均移除）；§1 加术语声明（非交互式多智能体）；摘要重写为 63.5%（模板）/23.4%（原栈实测）/74.7%（直连端点实测）三数并报 | **已解决** |
| P0-6 | P0 | 多种子/一致性最小证据 | **已完成且超额**：DeepSeek 3 重复 × 180 × {C4,C5} = 1080 真实调用，consistency_report.json 与正文逐位吻合；另补原 run 898/900 首次成功的 trace 级证据 | **已解决**（原生成器仍无多次重复，正文已如实声明） |
| P1-3 | P1 | 特征对比表 | §2.2 新增 7 维能力表（DIN-SQL/MAC-SQL/CHESS/MAG-SQL/SQLFixAgent/CHASE-SQL vs 本文），标注"基于文献机制、无性能声明" | **已解决** |
| P1-4 | P1 | 清洗流水线行话 | grep 全稿：repaired Stage / protocol-B / bounded submission / multi-role 零残留 | **已解决** |
| P1-5 | P1 | 真实 token/成本表 | §6 新增两张实测资源表（gpt + DeepSeek），与 efficiency_stats{,_deepseek}.json 逐位吻合 | **已解决** |
| P2-2/2-3 | P2 | 案例分析扩充 / prompt 附录 | 3 个 verbatim 案例（Q021/Q110/Q161 家族）全部经本评审对 predictions/traces 核实；附录 A 四个模板 + Q021 渲染上下文 | **已解决** |

**小结**：R1 的 6 项 P0 中 4 项完全解决、2 项部分解决（P0-3 代码供给、P0-4 机械项）；且两项"对抗性地雷"（评测约定循环、token 压缩夸大）不是被绕开而是被**正面量化并跨模型复现**，这在方法论上是本轮最大的增值。

---

## 1. 数字核验（独立重算，27 项）

**核验强度说明**：以下所有 ✓ 均为本评审用独立脚本从 scores.jsonl / predictions.jsonl / traces / contexts.jsonl / SQLite 原始文件重算所得，非对照中间报告。

| # | 论文声明 | 独立核验结果 | 判定 |
|---|---|---|---|
| 1 | 五条件 strict 执行准确率 0.3944/0.4389/0.4000/0.7000/0.7278 | 从 scores.jsonl 重算 71/79/72/126/131 ÷ 180，逐项吻合 | ✓ |
| 2 | 答案形状准确率 0.3278/0.3667/0.5056/0.8889/0.9722 | 重算逐项吻合 | ✓ |
| 3 | 配对 sign test：C4vC2 49/2/77/52 p=1.179e-12；C5vC2 56/4/75/45 p=9.085e-13；C5vC4 12/7/119/42 p=0.3593 | 精确双侧 sign test 独立重算，12 个计数 + 3 个 p 值逐位吻合 | ✓ |
| 4 | 松弛指标表（Table 6，15 格）：C1 0.4056/0.8000 … C5 0.7722/0.8056 | 与 relaxed_metrics.json 全部吻合；**projection-tolerant 反转 C2 0.8722 > C4 0.7444 确认** | ✓ |
| 5 | 残差错误分类表：C1 71/95/14/0 … C4 126/0/34/20、C5 131/0/44/5 | 从 evaluator_error_type 重算全部吻合 | ✓ |
| 6 | 可执行率 1.0000/1.0000/0.9167/0.8889/0.9722 | 由执行错误计数反推（15/20/5），吻合 | ✓ |
| 7 | 标签级诊断表 9 行 × C2/C4/C5（join 0.382/0.598/0.657；order-by +0.404；top-k +0.889；time +0.533；topology +0.727；self-join +0.778；group-by −0.083 等） | 用 questions.jsonl 的 sql_feature_tags 独立重算，**27 格全部吻合**（含子集规模 102/59/114/18/30/12/11/9/170） | ✓ |
| 8 | 组件消融：去值提示 118/180=0.6556（shape 0.9167，provider fail 0.0056）；去形状提示 77/180=0.4278（shape 0.4389） | component_ablation_results.json 逐项吻合 | ✓ |
| 9 | C5 行为：22 次选非首候选；修复响应非空 16 例、15 例成为最终选择；5 个执行错误 = Q156/157/158/160/162，其中 4×`wo.schedule_date` + 1×`wo.schedule` | 从 predictions + traces 重算：22 ✓、16/15 ✓、五个问题号与错误列名**逐条逐字吻合**（Q160 确为 `wo.schedule`） | ✓ |
| 10 | 案例 1（Q021）：C2 缺 ORDER BY、C4 补齐 | 归档 SQL verbatim 吻合 | ✓ |
| 11 | 案例 2（Q110）：候选 0 引用不存在列 `wo.schedule` 失败，排序器选中候选 1（投影 work_order_id/priority/status） | selected_candidate_index=1，SQL 吻合 | ✓ |
| 12 | 案例 3（Q161）：单次 bounded repair 改写为 `scheduled_date` 成功 | Q161 selected index=4（修复候选），SQL 含 `wo.scheduled_date` ✓ | ✓ |
| 13 | 实测 token（gpt）：输入 5007.7/6346.7/4756.3/4859.0/5309.8，输出 45.0/45.8/47.3/52.0/197.5，latency 均值/中位数 10 格，23.4% 降幅，全程 4.73M 输入 + 69.8k 输出 | efficiency_stats.json 逐位吻合；总和重算 4,730,287 / 69,793 ✓ | ✓ |
| 14 | 模板估计 token 381.3/710.3/202.0/259.2/258.2，63.5% 降幅 | 吻合（0.6351） | ✓ |
| 15 | 单遍协议证据：898/900 首次成功，2 次重试各在 C1/C4 | retry 分布 {C1:1, C4:1} ✓ | ✓ |
| 16 | **DeepSeek strict：C2 0.3389 (61/180)、C4 0.7000 (126/180)、C5 0.7667 (138/180)**；safe-SQL 1.0、0 provider 错误 | 从 outputs_deepseek_chat/scores.jsonl 重算逐项吻合 | ✓ |
| 17 | **跨模型增量 +36.1pp（C4−C2）与 +6.7pp（C5−C4）**；C4 两代模型 126/180 巧合相同 | 0.7000−0.3389=0.3611 ✓；0.7667−0.7000=0.0667 ✓；126=126 ✓ | ✓ |
| 18 | DeepSeek 松弛指标：set-exact 0.3667/0.7944/0.8278；set-relaxed 0.8500/0.7944/0.8278；**反转复现（C2 0.8500 > C4 0.7944）、C4/C5 投影容忍下不变** | relaxed_metrics_deepseek.json 逐项吻合 | ✓ |
| 19 | **DeepSeek 实测 token：C2 2011.6 / C4 509.3 / C5 680.5，74.7% 降幅**；输出 49.9/46.6/186.2；latency 1051.9/1054.0/3014.2（中位 1021.0/1003.5/1965.5）；C5 2/180 重试；全程 576.3k 输入 + 50.9k 输出、540 调用 0 错误 | efficiency_stats_deepseek.json 逐位吻合（0.7468→74.7%）；总和重算 576,250 / 50,899 ✓ | ✓ |
| 20 | 一致性检查：C4 0.7056/0.6944/0.7000、C5 0.7667/0.7667/0.7611，最大 spread 1.1pp；verdict 一致率 98.3%（两条件同值）；SQL 串一致率 82.2%/77.2%；1080 调用 | consistency_report.json 逐项吻合 | ✓ |
| 21 | 二模型 prompt "byte-identical" | 本评审对 Q021 C2/C4 做 sha256 比对：**归档 trace 与 DeepSeek trace 的 prompt 哈希完全相同** | ✓ |
| 22 | C5 排序器重实现与归档一致率 "167/169 非修复决策（98.8%）" | 本评审**独立重放**重实现排序器于归档候选集：162/164 = 98.78%，同为 2 处分歧（Q067、Q198）。百分比与分歧数吻合；分母差异（169 vs 164）源于"非修复案例"的排除口径（16 个 repair 案 vs 11 个），属记账口径差异而非数字错误 | ✓（分母口径建议脚注化） |
| 23 | 值提示覆盖：170/180 题至少 1 条、330 实例、111 唯一渲染提示、20 个 matched value 列 | contexts.jsonl 重算 170/330/111 ✓；matched_values 恰跨 **20** 个不同列 ✓ | ✓ |
| 24 | 排序器权重表（safe +10/−20、exec +10/−15、shape +6/−5、order +3/−2、empty −2、value +4、missing −3） | 与 outputs_deepseek_chat/results.json 内记录的 ranker_weights 逐项吻合 | ✓ |
| 25 | 权重敏感性 132/132/131/136/136 | R1 已对 validator_diagnostics.md 核验吻合，本轮未重放（无变更） | ✓（承接 R1） |
| 26 | "值清单含 196 个不同值、28 个非 ID 列" | **无法复现**：本评审对 database.sqlite 直接计数得 268 值/34 非 ID 列（排除 REAL 列后 202/29）；生成该清单的 `dev_chess_style_pilot` 模块缺失，无法确认其精确排除规则 | ✗（不可核验，非矛盾） |
| 27 | 45 条参考文献、\cite 键全在 bib、\ref 全有 label、环境配平 | 结构检查通过：cited 45 键 0 缺失、0 undefined ref、0 unbalanced env | ✓ |

**核验通过率：26/27 完全通过（96.3%），1 项不可核验（#26，定义依赖缺失模块）。0 项造假迹象，0 项方向性错误。** 特别地，本轮新增的 DeepSeek 证据链（检查 #16–22）与原始证据链同等可审计：真实端点、真实 usage 记录、prompt 字节级同源、排序器重实现可独立重放。

---

## 2. 内部一致性与叙事审计

### 2.1 约定敏感性披露是否自洽贯通 —— 基本贯通，一处残留

R1 最危险的地雷（评测约定循环）现已被**制度化披露**：§5 显式声明两条标注协议约定 + 形状推断规则"按协议共同设计（coupling by construction）"；§6.1 用双松弛指标量化；claim 表第 1 行边界注明"strict 增益由投影/排序契约主导，非行内容检索"；摘要与结论均复述；且跨模型复现使其升级为"基准属性"而非单模型伪象。**"any claim that compact grounding improves row-content retrieval on this benchmark would be unsupported; the paper does not make that claim"（L303）是同类论文中罕见的自我限定。**

**残留不一致（本轮唯一实质文字问题）**：
- **[A-1, MODERATE]** §4 L115："The first component, compact schema/value selection, **is where most of the gain comes from**." 这与论文自己的两处证据相抵触：(i) 消融显示**形状提示才是最大单通道**（去形状 126→77，去值 126→118）；(ii) §6.1 结论是 strict 增益由**答案契约合规**（形状推断阶段的产物）主导。该句是升级前叙事的化石，应改为"the compact context bundle is where most of the gain comes from, with the answer-shape channel as its largest single component (Section 6)"或类似。
- **[A-2, MINOR]** 贡献 2（§1 L39）"compact domain context outperforms both schema-only and full-schema-values prompting"未标注"under the strict answer-contract metric"。贡献 5 已提及约定敏感性，故非矛盾，但补 5 个词可全稿闭环。
- **[A-3, MINOR]** §7 Discussion 前两段仍以"grounding/更好对齐"语言解释 C4 增益，未回指 §6.1 的契约主导解释；末段与结论已回收（"most of the measurable benefit comes from making the expected answer contract explicit"），建议在 §7 首段加一句约定回声。

### 2.2 compact-context 效率主张是否正确限定 —— 是

摘要与 §6 采用 63.5%（模板）/ 23.4%（原栈实测，~4.5k 固定开销）/ 74.7%（直连端点实测）三数三角互证，明确"两种视图不得混同"（L258）；claim 表 token 行边界同步。R1 的"误导风险"判定可撤销。**这是三数中任何一个单独呈现都会失真、合并呈现才诚实的教科书式处理。**

### 2.3 其他

- 术语：标题/正文已彻底"多阶段"化；"multi-agent"仅 2 处，均指他人系统或否定性自指 ✓。
- GPU 句已删，替换为准确的"无本地 GPU 参与任何报告数字" ✓。
- 行话清洗完成（grep 零残留）✓。
- 论文未具名原始 serving 栈（krill 代理）——以"original serving stack with a large fixed per-call overhead"描述。trace 内有 provider 记录，审稿人若追问可答；不构成阻断，但透明度上低于 DeepSeek 侧的具名披露。**[A-4, MINOR]**
- `gpt-5.4-mini` 经第三方代理、外部不可验证的问题（R1 F-snd-4）实质上被 DeepSeek 直连复现**对冲**：即使审稿人不信任第一生成器，第二证据链独立成立。

---

## 3. Desk Screen（双刊模拟）

### 3.1 MDPI Electronics（主选）

| 项 | 状态 | 严重度 |
|---|---|---|
| 模板 | IEEE Access 类 ≠ MDPI 模板。**但 MDPI 支持 free-format 首投**（格式在录用后生产阶段统一），故非 desk-reject 项，属提交时转换/或直接 free-format 投 | 低（需决策） |
| 摘要长度 | 实测约 **240 词** > Electronics 约 200 词上限 | **需压缩**（格式审查会退回） |
| 作者/单位/通讯/ORCID | "Anonymous" + "withheld for anonymous review"——MDPI 为**单盲**，必须实名 | **阻断——不可投** |
| Author Contributions（CRediT） | **整节缺失**（MDPI 硬性后置声明） | **阻断** |
| Funding / COI / Data Availability / AI 披露 | 骨架在，4 个 [TODO]（repo URL、funding、COI 确认、AI 措辞） | **阻断** |
| Institutional Review / Informed Consent | 未写；合成数据应填 "Not applicable" 两行 | 小（5 分钟） |
| 参考文献 | 45 条全验证、全被引、0 悬空；IEEEtran 编号式，free-format 可接受 | ✓ |
| 图表 | 4 图 10 表；**表格极多（10 张 table*）**，MDPI 双栏排版下压力大但非违规；图为流水线自动风格（R1 P2-1 未做） | 可接受 |
| 可编译性 | **未验证**：paper.pdf 为 06-27 旧版；manuscript/ 缺 charts/ 目录与 cls；本机无 TeX | **阻断**（投稿需最终 PDF） |
| Section 匹配 | Artificial Intelligence 或 Computer Science & Engineering Section 均对口 | ✓ |
| 英文 | 清楚、有纪律，超过该刊录用样本平均线 | ✓ |

**对照该刊蒸馏录用标准**（15 篇电力方向全文样本）：本文在每一项上都在录用线之上——实验底线是"1 案例 + ≥1 对照类"（本文 5 条件 × 2 生成器 + 消融 + 一致性）；显著性检验 0/15 要求（本文有精确 sign test）；开源代码 0/15（本文承诺全 artifact 包）；multi-run 1/14（本文有 3 重复）。**内容侧对 Electronics 无短板，全部阻断都是机械项。**

### 3.2 IEEE Access（备选）

| 项 | 状态 |
|---|---|
| 模板 | **已合规**（ieeeaccess.cls；\history/\doi 占位为模板惯例） |
| 作者信息 | Anonymous——单盲，须实名 + ORCID + 作者简介（bio + 照片，Access 惯例） + graphical abstract（推荐） |
| 摘要 | 240 词 ≤ 250 惯例上限，可不动 |
| 后置声明 | Access 无 MDPI 式强制 CRediT，现有 DA/AI/Funding/COI 骨架填实即可 |
| 评审模型 | 二元 Accept/Reject + 一次重投限制：**要求投稿时即近终稿**——当前科学内容已达该状态 |
| 可编译性 | 同上，须重编译出最终 PDF |

**Desk 判定**：两刊 desk-reject 风险（修复机械项后）均 <10%——主题在 scope 内、声明齐全、语言过关。当前状态**两刊都不可投**，原因 100% 是机械项（实名、TODO×4、CRediT[Electronics]、摘要压缩[Electronics]、重编译），无一是科学项。

---

## 4. 七维评分（对标 SCIE Q2 应用刊录用水位；括号内为 Round-1 分值，Sev 0–4 越低越好）

| 维度 | R1 | **R2** | 变化理由 |
|---|---|---|---|
| **Novelty** | 3.0 | **2.7** | 组件仍全为已知技术、无真实外部系统对手（C3 仍是自制 CHESS-lite），此项天花板未动。小幅改善来自：特征对比表明确了"值规范化 + 形状推断 + 单固定生成器"组合的空位；且**约定敏感性的跨模型量化本身构成一个可引用的方法论小贡献**（strict 基准增益可被契约合规主导——对 NL2SQL 评测设计者有独立价值）。对 soundness 型刊，2.7 不阻断 |
| **Soundness** | 2.5 | **1.5** | R1 两颗地雷均被真实数据拆除：评测循环→双松弛指标 + 跨模型反转复现 + "coupling by construction"自认；token 夸大→三数三角。残留：§4 "most of the gain" 化石句（A-1）、196/28 值清单不可核验（#26）、第一生成器经代理不可外验（已被二链对冲）。claim–evidence 表边界纪律为同档最强 |
| **Experiments** | 3.0 | **2.2** | 结构性补强：第二生成器家族（真实 540 调用、更大效应量复现）+ 3×180×2 一致性（1080 调用，spread ≤1.1pp）。**未解决的天花板**：仍是单一自建 ~100 行合成库、test 集 2/3 模板扩展题、无公开基准迁移（P1-1 未做；x10 扩库已建成并通过 gold 验证但 C4/C5 重跑被缺失模块卡住）。"toy benchmark"仍是审稿最大攻击面 |
| **Reproducibility** | 2.8 | **2.0** | 评估器测试 13/13（实测）、硬编码路径清零、分析脚本可重算全部数字、二模型 runner 为 stdlib 自足实现且排序器重放可独立验证（本评审 162/164）。**仍缺**：C4 上下文构建器等 4 个模块（MISSING_ARTIFACTS.md 已登记，作者须在投稿前入包，否则"从零重跑"承诺不成立）、repo URL 未落地 |
| **Related Work** | 1.0 | **1.0** | 45 条 0 缺 0 多、2026 preprint 明确降级为 contemporary context、新增 7 维特征表。维持 |
| **Clarity** | 1.5 | **1.0** | 行话清零、术语自洽、案例分析将机制具象化、附录模板完整。摘要 240 词偏长且信息密度极高（Electronics 需压缩）；表格数量偏多（10 张） |
| **Ethics** | 1.0 | **0.8** | GPU 凑数句已删；AI 双重角色披露（被试模型 + 写作辅助）诚实且超前于多数期刊要求；COI/Funding 待实名后落定 |

**加权印象**：R1 的判词是"证据链诚实度一流、实验野心三流"。R2 的准确判词是**"证据链诚实度一流、实验广度二流、机械完成度零分"**——科学内容已从"SCI 边缘"进入"soundness 型 SCI 舒适区"，剩余风险集中在基准外部效度（先天）与投稿机械项（人为）。

---

## 5. 判定（可投稿状态）

### (a) 科学上已完成 vs 未完成

**已完成**：主对比（5 条件 × 180 题）、双松弛指标、组件消融、标签诊断、错误分类、案例分析、排序器敏感性、第二生成器复现（含反转复现 + 74.7% 干净效率数）、3 重复一致性、prompt 附录、claim–evidence 边界表。**这套证据在目标两刊的录用样本分布里位于前 10–20%。**

**未完成（非阻断，属胜率增量）**：公开基准迁移探针（Spider/BIRD 子集）、x10 扩库上的 C4/C5 重跑（被缺失模块卡）、第一生成器的多次重复、图表期刊化重绘。

### (b) 硬性投稿阻断（全部为机械项，逐项枚举）

| # | 阻断项 | 位置 | 工作量 |
|---|---|---|---|
| B1 | 作者实名/单位/通讯/ORCID（现为 Anonymous/withheld） | L17–19 | 依赖作者信息到位，0.5 h |
| B2 | [TODO] repository URL（Data Availability） | L523 | 建 repo + 传 artifact 包，2–4 h |
| B3 | [TODO] Funding 声明 | L531 | 5 min |
| B4 | [TODO] COI 确认 | L535 | 5 min |
| B5 | [TODO] AI 披露按目标刊措辞适配 | L527 | 15 min |
| B6 | LaTeX 重编译出最终 PDF：paper.pdf 为 06-27 旧版；manuscript/ 缺 charts/（图在 ../assets/charts/）与 ieeeaccess.cls；本机无 TeX | — | TeX 机器上 1–2 h（含 \graphicspath 修复） |
| B7 | 【仅 Electronics】摘要 240→≤200 词 | L22 | 1 h |
| B8 | 【仅 Electronics】Author Contributions（CRediT）+ Institutional Review/Informed Consent（Not applicable）两节 | 后置声明 | 0.5 h |
| B9 | 【仅 Electronics】MDPI 模板转换或确认走 free-format 首投 | — | free-format 0 h / 转模板 0.5–1 天 |
| B10 | 【建议同 B2】将 `dev_chess_style_pilot` 等 4 个缺失模块入包（MISSING_ARTIFACTS.md 清单），否则 DA 声明的"从零重跑"不完全成立 | — | 依赖作者供给，入包 1–2 h |

### (c) 决策分布预测

| 状态 | 期刊 | Accept/Minor | Major(或修后重投) | Reject |
|---|---|---|---|---|
| 现稿（阻断未清） | 任一 | — | — | **不可投**（编务退回） |
| 清完 B1–B9 | **MDPI Electronics** | **~55%** | ~30% | ~15% |
| 清完 B1–B6 | **IEEE Access**（二元判） | **~55% Accept** | — | ~45%（多半附重投邀请） |
| 追加 P1-1 公开基准探针后 | Electronics | ~70% | ~22% | ~8% |

依据：Electronics 蒸馏样本显示其录用函数为"soundness × 完整性 × Section 匹配"，本文全面超线；主要失分场景是抽中一位坚持"合成 100 行库不足以支撑期刊论文"的审稿人（概率约 1/3，通常给 major 而非 reject，可用 x10 扩库 + 迁移探针在修稿轮回应）。Access 的二元模型下，约定敏感性的**自我披露是双刃**：多数审稿人会计为诚实加分，少数会引用论文自己的反转表主张"headline 是契约工程"——正文 §6.1 的部署契约论证是充分防线，但结果分布因此更极化。

### (d) P0 / P1 / P2

**P0（投稿前必须，合计 ~1 人日 + 作者信息）**：B1–B10 全部；外加 [A-1] §4 "most of the gain" 句修正（10 分钟，避免审稿人用论文自己的消融打脸）。

**P1（显著提升胜率，选做，合计 2–4 人日）**：
1. 补齐缺失模块后在 x10 扩库上重跑 C2/C4/C5（扩库与 gold 验证已就绪）——直接回应"toy"评语；
2. Spider/KaggleDBQA 单库探针跑 C2/C4；
3. [A-2]/[A-3] 贡献句与 §7 的契约回声（30 分钟）；
4. 196/28 值清单改为可从发布包重算的口径或加脚注（#26）；
5. 排序器一致率 167/169 的分母口径脚注（#22）。

**P2**：图表重绘统一风格；表格瘦身（10→7 张，部分并入附录）；graphical abstract（Access）。

### (e) 明确回答：本周能投吗？

**能——条件是作者信息（姓名/单位/ORCID/基金/COI）到位。**

- **IEEE Access：是，本周可投。** 模板已合规、摘要长度合规、科学内容完整；仅需 B1–B6（约 1 个工作日，其中编译需一台有 TeX 的机器）。
- **MDPI Electronics：是，本周可投**（走 free-format 首投），比 Access 多 B7/B8 约半天工作量；若坚持先转 MDPI 模板则 +0.5–1 天。
- 投稿顺序建议维持 changelog 现状：**Electronics 主选**（15 天首决、major-revision 通道可用于消化 toy-benchmark 质疑、P1 补强可在修稿轮兑现），Access 备选（更快的品牌通道，但二元判下建议先做完 P1-1 再投以免烧掉一次机会）。

---

## 6. 一句话总评

Round-1 说"这是一手可以变好的牌，别提前摊掉"；Round-2 核验证实这手牌确实变好了——**26/27 项数字逐位可复算，两颗地雷被真实的 540+1080 次 API 调用拆除并反向转化为跨模型发现，科学内容已无投稿级缺口**；现在唯一挡在投稿按钮前的是作者姓名、四个 [TODO]、一次 LaTeX 编译，以及一句应该删掉的旧叙事化石（§4 "most of the gain"）。

---

*本评审未修改稿件。所有重算脚本临时生成、未入库；关键重算路径已在 §1 各行注明数据源，可按需复跑。*
