# 投稿前质量门清单（四篇共通 + 分篇）

**日期：** 2026-09-04
**用途：** /loop 迭代评审的对照基准；每轮修改/评审以本清单为准绳。终态判定由 harness `s11 final gate` 与 `s12 human gate` 执行，本清单是其输入。
**状态标记：** `[作者]` 需作者输入 · `[S3]` Stage-3 契约执行 · `[S4-6]` 冻结实验/正式实验 · `[S7]` Stage-7 统稿应用 · `[已指定]` 本轮已完成规格（见 18 号文档）

## 一、共通质量门

| 门 | 要求（依据） | 状态 |
|---|---|---|
| G1 作者字段 | Funding 填 "This research received no external funding"；CRediT 用既有作者信息填齐；P2 的 COI **必须具名披露对国网福建经研院的雇佣关系**（Applied Sciences 语料 11/11 硬规则）；ORCID 不虚构 | `[作者]` |
| G2 Data Availability | 提供可核验持久链接或各刊认可的标准措辞；P4 需把 "No persistent public archive is verified" 升级为实际存档声明 | `[S7]` |
| G3 MDPI 格式 | 摘要 ≤200 词（P2 现 ~220，压缩版已备于 18 号文档）；关键词 3–8 个（四篇均合规）；编号引用；模板版本投稿前复核 | `[S7]` |
| G4 三层声明一致 | 摘要/结论/局限的 claim 强度对齐；负结果保留条款逐条核对（各契约 §1 清单） | 每阶段持续 |
| G5 锁定标题补偿语义 | 标题逐字不变；摘要首句/引言/关键词/cover letter 连续出现该刊目标语义（P1/P2：power-grid investment portfolio；P4：graph convolutional + hyperbolic） | `[已指定]` |

## 二、分篇质量门

### P1 → Energies

| 门 | 要求 | 状态 |
|---|---|---|
| P1-1 | 摘要首句嵌入 power-grid investment portfolio optimization 连续语义（替换文本已备） | `[已指定]`→`[S7]` |
| P1-2 | H-Pref 条件定义与主指标预注册先于实验（可审计时间戳） | `[S3/S4]` |
| P1-3 | 全部基线公平调参、调参与评估分离、pymoo 钉扎 | `[S4]` |
| P1-4 | 0.89% 与调参后新数字并列；三张工程换算表随主表同报 | `[S6/S7]` |
| P1-5 | Table 9 归一化反转保留；H1 不通过时框架叙事（预写两版 headline） | `[S7]` |
| P1-6 | 事件共现摘要配解释性使用场景段落（2 个预注册场景），否则贡献降级为"记录完整性"（R2 新增） | `[S7]` |

### P2 → Applied Sciences

| 门 | 要求 | 状态 |
|---|---|---|
| P2-1 | 摘要压缩至 ≤200 词且保留红线句（压缩版已备） | `[已指定]`→`[S7]` |
| P2-2 | COI 具名披露雇佣关系（措辞模板已备，需作者确认） | `[作者]` |
| P2-3 | 成本校准（MTEP16 分位数映射）或 NO-GO 记录在案 | `[S3]` |
| P2-4 | MTEP16 第二任务族进入推断协议；3 个精确小实例参照 | `[S4-6]` |
| P2-5 | NSGA-II/PLS 公平调参；"loses four of eight and wins none" 保留在摘要 | `[S4]` + 持续 |
| P2-7 | 解释性结果族（跨情景重叠率/组一致性/修订路径长度）预注册（R2 新增） | `[S4]` |

### P3 → Energies

| 门 | 要求 | 状态 |
|---|---|---|
| P3-1 | 2×2 四臂代码拆分（两门独立随机源）——红线 1 | `[S3]` |
| P3-2 | action-aligned AC 映射 + 种子复现，或 NO-GO 记录——红线 2 | `[S3/S4]` |
| P3-3 | analytic HV 主指标预注册；等调用预算认证 + 共享种子流；MOEA/D 修复 | `[S4]` |
| P3-4 | "Self-Adaption" cover letter 一句话处置（标题锁定不修改） | `[已指定]` |
| P3-5 | H1/H2 均不通过时的降级决策门（标题豁免或改投 Algorithms）预注册触发 | `[S6]` |
| P3-7 | quality-per-evaluation 性价比度量预注册（R2 新增） | `[S4]` |

### P4 → Electronics

| 门 | 要求 | 状态 |
|---|---|---|
| P4-1 | 真实 HGCN 实现并通过"图卷积 ≠ 稠密注意力"自查清单——红线解除唯一路径 | `[S3]` |
| P4-2 | 匹配欧式 GCN 参数量差 ≤10%；图构造零测试期信息泄漏 | `[S4]` |
| P4-3 | persistence 基线补齐；MAE/RMSE 进主表；显存/数值失败上报 | `[S4/S6]` |
| P4-4 | 红线表述在实现产出结果前保留于四处（摘要/引言/方法/结论） | 持续 |
| P4-5 | pilot 门控资源预算；H1 不通过时路由决策门（转 Energies/IEEE Access + 标题豁免，或并入他稿） | `[S5/S6]` |
| P4-8 | 曲率定义先行条款（模型/exp-log 映射/参数语义显式定义；区分双曲聚合与图结构贡献）（R2 新增） | `[S3]` |

## 三、官方页面核验记录（2026-09-04）

**核验方法：** 直接抓取 mdpi.com 被 Akamai 拦截（HTTP 403），改用官方分页 URL + 搜索结果交叉确认；以下均为快照，投稿前须再按官方页面复核 APC/IF/开放 SI。

| 期刊 | 推荐 Section | 核验结果 | 备注 |
|---|---|---|---|
| Energies | F1 Electrical Power System；A1 Smart Grids 备选 | **存在**（Electrical Engineering 科目下） | 2026 开放的相关 SI 候选（P1/P3 可用）："Advances in Machine Learning Applications in Stability Analysis and Optimal Operation of Power Systems"（2026-09-10 截止）、"Advances in Low Carbon and AI in Power Energy System: 2nd Edition"（2026-11-25 截止）。IF 2024 = 3.9、CiteScore 8.3（技能包快照 IF≈4.0，小幅漂移，投稿前复核） |
| Applied Sciences | Energy Science and Technology；EEC Engineering 备选 | **两个均存在**（分别在 Physical Sciences / Engineering 科目下） | EEC 版块范围明确覆盖 microgrids、renewable energy harvesting、power electronics——P2 的推荐 Section 有效 |
| Electronics | Artificial Intelligence；CSE 备选 | **两个均存在** | AI 版块范围含 ML/DL 算法、XAI 等——P4 推荐 Section 有效 |

**结论：** 05 号前评估的 Section 建议仍然全部有效；四篇的 Section 层面 desk-reject 风险消除。SI 投稿与否由作者在 Stage-7 前按当时开放列表决定（P1/P3 的 ML×Power Systems SI 是现成候选）；APC/IF 数字以投稿日官方页面为准。

## 四、评审循环规则

1. 每轮迭代：对照本清单 + Paper_CCF 期刊画像，产出"评审意见 → 修改规格"，写入 18+ 号叙事修订文档。
2. **不直接修改四篇 canonical paper.tex**——Stage-2 分支尚未合并，工作树直接改动会造成合并冲突；且 harness Stage-7（s07 results_first_manuscript）会从实验 manifest 重生成正文，手改会被覆盖。所有叙事规格由 Stage-7 统一应用。
3. 终态判定："本阶段可推进项全部完成 + 其余项阻塞于 Stage-3~6 执行"即视为当前循环的自然终点，向用户交付交接清单并停止。
