# Round 3 — mintou_p3 (CARS-MODE) 投稿前全面自检评审

- **日期**: 2026-07-16
- **评审类型**: paper_reviews 离线模式 round-3（投稿前自检；Desk Screen → 7 维 → 对抗核验 → Meta 决策）
- **稿件**: `D:\aicoding\powergrid_benchmark\mintou_p3_samode_distribution_planning\manuscript\MANUSCRIPT.md`（v6 real-MOEA 证据版）
- **校准框架**: `paper_reviews/config/journals/mdpi_energies.yaml`（accept RRI 中位 61.5，区间 [14,76]）+ `mdpi_energies_accepted_profile.md`（20 正样本 + 34 全文蒸馏）
- **数字核对源**: `papers/mintou/mintou_p3_samode_distribution_planning/evidence/` 之 `real_simbench_planning_leaderboard.csv`、`real_simbench_planning_significance.csv`、`real_ac_validation_summary.csv`、`real_ac_validation_results.csv`（864 行逐案）、`real_simbench_planning_compromise_compositions.csv`、`real_sensitivity_sweep.csv`、`real_simbench_planning_source_profile.csv`、两个 config json
- **前序**: Round-2（2026-07-13，v5 证据，RRI 11.75/28 = 42%，Major 60%）

---

## 〇、数字核对总表（全部通过）

对稿件全部量化主张逐条对表核验，**无一处数字错误**：

| 稿件主张 | 证据值 | 判定 |
|---|---|---|
| 池化 HV 0.04218，NSGA-II 0.03966，+6.34% | 0.04217835 / 0.03966261 = 1.06343 | ✓ |
| FixedDE +0.60%（0.04243），7 场景 Holm p ∈ [0.22, 0.76] 全不显著 | 0.04243314；p_holm 0.217–0.758，diff 全为 FixedDE 名义占优 | ✓（0.217 写作 0.22 属四舍五入） |
| NoRepair −6.84%（6/7 场景显著）；NoDiversity −33.56%（7/7 显著，front 38.6→8.1，std 翻倍以上） | 0.03929/0.04218=0.9316；storage_allocation p=0.0529 不显著；0.02802/0.04218=0.6644；std 0.00977 vs 0.00381 | ✓ |
| NoDER +0.12%，2 显著负（constraint_repair、der_siting）+1 显著正（loose budget） | significance.csv 完全一致 | ✓ |
| 42/42 Holm 显著基线胜 | 6 基线 × 7 场景全 True | ✓ |
| 表 5 七行（+1.87% ~ +9.84%，各 Holm p） | 逐行核对一致 | ✓ |
| 表 6 AC 全 12 行（0.500–0.681；电压/载流均值） | ac_validation_summary.csv 逐行一致 | ✓ |
| 表 7 灵敏度六点（均值±std、NSGA-II 参照、MWU p）；最小绝对差 0.0022；τ 轴 2.3% / Np 轴 10.5% 极差；无秩反转 | sweep CSV 逐行一致；0.04069−0.03847=0.00222 | ✓ |
| 组成 6/7/1/0（CARS-MODE base）与 5/4/6/0（NSGA-II base） | compositions.csv 一致 | ✓ |
| 协议：30 seeds × 11 方法 × 7 实验，pop 40 / gen 40；预算因子 1.0/0.82/1.2；负荷 1.3 | config json 一致 | ✓ |
| 表 1 源画像（18 子网、72 候选、71,348.9 MW、12,234.9 MW、34,296.2 km） | source_profile.csv 一致 | ✓ |
| 4 图存在（300 dpi PNG） | manuscript/figures/ 四文件齐 | ✓ |

**可复现性一致性彩蛋**：storage_allocation 实验中 CARS-MODE 与 NSGA-II 组成完全相同（8/5/0/0），其 72 案中该实验 24 案 AC 结果逐值相等——映射管线确定性、方法无关性得到独立佐证。

---

## 一、Desk Screen（MDPI Energies pre-check 模拟）

| 项 | 状态 |
|---|---|
| 题目–内容一致 | ✓（但见 F-sound-4：18 子网含 EHV1/HV，"distribution planning" 需一句边界声明） |
| 摘要含量化结果 | ✓，但 **~255 词，超 Energies ≤200 词指引**，需压缩 |
| 关键词 | ✓ 8 个，合规 |
| 作者/单位/通讯 | ✗ **[TODO] 未填——现状不可投** |
| 参考文献完整性 | ✗ **9/26 条 `[authors TODO]`；另 3 条年–卷号矛盾（见 F-rw-2）** |
| 图表 | ✓ 4 图 4+3 表，图注齐 |
| 后置四件套 | Author Contributions/Funding/DA/COI 骨架在，均 TODO；**缺 Institutional Review Board 与 Informed Consent 两条模板声明**（补 "Not applicable"） |
| Data Availability | ✓ 声明完整，仓库 URL 为 TODO |
| AI 使用披露 | ✗ 缺（ARA 全链 ai-executed provenance；MDPI 政策要求，实践中 0/34 有——提醒级） |
| 自引 | 无法评估（作者未定）；当前引文无异常凑引 |

**结论**：内容层可过 pre-check；形式层有 2 个硬阻断（作者信息、参考文献 TODO）。

---

## 二、7 维逐条 Findings（severity 0–4 × confidence × fixability）

### 2.1 Novelty — severity 1 | conf 0.80 | fix 0.90

- **[F-nov-1, 正面]** 可命名机制组合（jDE 自适应 + SaDE 双策略池 + 贪心预算修复 + 拥挤度）+ 清晰 gap 句 + 每机制单开关消融，超出 Energies 常态（31 篇 research 全新算法 0 篇）。"以 AC 层证据为自适应组件辩护"是本文独有的论证角度，2.3 节明确声明 DE 文献未提供过此类理由。
- **[F-nov-2, MINOR]** 缺特征对比表（proposed vs 最接近 5–8 篇：组件/约束处理/统计协议/AC 验证有无）。这是画像中"说清组合点"的常见手法，加表可堵"该组合是否真未被做过"的追问。
- **[F-nov-3, MINOR]** 增益 6.34%（vs 基线）如实标注、不夸张，符合"≤5% 如实标注也被接受"的画像；FixedDE 微超已在摘要正面披露，无 novelty 膨胀。

### 2.2 Soundness — severity 3 | conf 0.90 | fix 0.85

- **[F-sound-1, SEVERE｜叙事与自证据矛盾]** §6.3 机制句："CARS-MODE's compromise plans are **storage- and DER-rich** … **DER-heavy mixes carry an over-voltage cost in the high-DER stress scenario**"。对 `real_ac_validation_results.csv` 逐案聚合后**不成立**：
  - CARS-MODE 三个被映射实验的 DER 动作数为 1/3/0（合计 4），NSGA-II 为 6/7/0（合计 13）——CARS-MODE 是 **storage-rich 而 DER-poor**；真正 DER-heavy 的 NSGA-II AC 反而更好（0.667 > 0.611）。
  - 在 high_der 场景本身，CARS-MODE 2/12 可行 ≥ Standard DE 2/12 > NSGA-II 0/12——CARS-MODE **并非**输在 high-DER 场景。
  - CARS-MODE 真正的失分点：base 实验 rural 网 **base/含 peak 场景储能注入引致过电压**（base 场景 9 个越上限母线，max_vm 1.0537）与 urban 网 growth 系列**线路过载**（少 1 条加固，103–154% 载流）。FixedDE（8 storage/5 reinf）同型失效更重（rural base 10 越限 + peak/growth/n1 三案再失）。
  - 正确的机制故事是：**代理目标奖励储能/托管容量指数 → 储能富集组合在弱网基础场景即过电压、且挤占加固预算 → 电气层失分**；"自适应保护电气可行性" = FixedDE 多收敛出 1 个储能动作的差异。§7 "less aggressively specialized to the proxy's DER-friendly gradient" 同源错误。
- **[F-sound-2, MODERATE｜量词过强]** 摘要"**every optimizer's plan mix improves AC feasibility** over the no-plan reference"、§6.3 "every optimizer that returns a non-empty plan beats the No-Plan reference"、§9 同句——对 Weighted Sum 为**假**：其计划非空（如 0/0/1/3，自动化为主）而 AC 率 = 0.500 = 参照，同段下一句自己承认"Weighted Sum sit[s] at the reference level"，构成段内自相矛盾。
- **[F-sound-3, MODERATE｜"largest drop"不精确]** 摘要"loses **the most** AC feasibility (0.569)"、§6.3 "records **the largest** AC-feasibility drop among the algorithmic ablations"——总率上 FixedDE 与 NoDiversity **并列** 0.5694，stress-only 上 NoDiversity（0.483）**低于** FixedDE（0.517）。同句虽有"tied with NoDiversity"补丁，但"largest"在 stress-only 维度为假。
- **[F-sound-4, MINOR｜口径边界]** 18 子网含 EHV1/HV1/HV2（总负荷 71.3 GW 覆盖 EHV–LV），而标题/任务是 distribution planning，AC 验证又在 4 个 **MV** 网（不在 18 子网内）。§3.2 已自认"reproducible public proxy"，但建议加一句显式声明：候选池取自 EHV–LV 子网统计、"distribution"指投资组合决策粒度、AC 层是异级组成映射（构成级映射边界声明需覆盖电压等级错位这一点）。
- **[F-sound-5, MINOR]** high_der 场景里 NoPlan 可行率 0.25 **高于** 多数带计划方法（NSGA-II 0、PSO 0、NoRepair 0）：映射规则按计划 DER 数 × 2.5 因子注入 PV，计划越多注入越多，机制性地劣于不注入——该场景 AC 信号部分是**映射规则伪影**而非计划质量，正文未提示。加一句可防审稿人反向解读。

### 2.3 Experiments — severity 2 | conf 0.85 | fix 0.60

- **[F-exp-1, 已达标]** 灵敏度分析（round-2 第一大 P0）已补：2 参数 × 3 水平 × 10 seeds，NSGA-II 匹配参照，MWU 全显著、无秩反转。满足"近乎硬性常态"。
- **[F-exp-2, MODERATE｜AC 层证据薄]** AC 层每方法仅 seed-0 一个折衷计划 × 3 实验 = 72 个二元案；CARS-MODE vs FixedDE 之差 = **3/72 案**（44 vs 41，Fisher p≈0.73），且全部源于 base 实验 rural 网、由**一个储能动作之差**驱动。稿件已两处披露"qualitative pattern, not statistically powered"（§6.3、§8.1），符合画像"重诚信胜于重数量"；但摘要与结论把它抬升为标题级发现（"the adaptive component buys electrical robustness invisible to the indicator"）。**最便宜的加固**：AC 阶段扩至 seeds 0–9 的折衷计划（10×72 案/方法，pandapower 分钟级），若模式保持则叙事获得统计脚；若不保持则现在知道好于审稿人替你发现。
- **[F-exp-3, MINOR]** 第二算例族（IEEE 33/69）仍缺——§8.4 已诚实列为 future work；画像显示 ~2/3 录用论文单算例，非硬伤。
- **[F-exp-4, MINOR]** 表 7 两个"default"行是同一配置的两次独立重跑（0.0409 vs 0.0410，种子流不同），未加脚注说明，细心审稿人会问。
- **[F-exp-5, MINOR]** CARS-MODE vs NSGA-II 的 AC 对比中 24/72 案组成相同（storage_allocation 8/5/0/0 撞车），实际差异来自 48 案——可在 §6.3 括注一句，反而佐证映射方法无关。

### 2.4 Reproducibility — severity 1 | conf 0.90 | fix 0.95

- **[F-rep-1, 正面]** 本次评审逐数核对 5 个 CSV + 2 个 config，稿件所有表格与统计**零偏差**；种子哈希派生、固定归一化边界、方法无关指标、v1–v5 弃用证据全保留。远超"1/34 open code"的领域常态。
- **[F-rep-2, MINOR]** 仓库 URL/DOI 为 TODO——DA 声明的落地动作（Zenodo/GitHub release）须在投稿前完成，否则声明为空头。
- **[F-rep-3, MINOR]** 初始化稀疏度 ~8%、成功质量衰减 0.95/下限 0.2 等超参在正文有，但建议补一张完整超参表（或指向 config 文件清单）以便复跑。

### 2.5 Related Work — severity 3 | conf 0.95 | fix 0.95

- **[F-rw-1, SEVERE｜投稿阻断]** 9/26 条参考文献 `[authors TODO]`（classification 2026、datacenter、dispatch-DE、Gonzalez-Longatt、reliability、review、TSO-DSO、Wasserstein、WGAN）。其中 **[Gonzalez-Longatt et al., 2024] 正文已按人名引用而参考条目作者未核**——若 DOI 记录作者不同即为张冠李戴。§2 首注自认"one-line characterizations are title-level and must be checked against the PDFs"。
- **[F-rw-2, MODERATE｜年–卷矛盾]** 3 条目年份与卷号冲突：[Qi et al., 2025] "Energies **2025, 19**(1), 210"、[review, 2025] "**2025, 19**(1), 116"、[WGAN, 2025] "**2025, 19**(1), 228"——Energies 卷 19 = **2026**（卷 18 = 2025；同稿 [reliability, 2026] 19(6) 与 [classification, 2026] 19(14) 标注正确）。补作者时一并按 DOI 核正年份或卷号，并同步正文引用标签年份。
- **[F-rw-3, MINOR]** 26 条、近 5 年约 13 条（≈50%）——踩画像底线（≥50%，中位 ~70%）。补 2–4 篇 2024–2026 同题（自适应 DE 应用/配网多目标规划）可稳过。
- **[F-rw-4, 正面]** 三线综述有实质逐条点评并收敛到 gap 句，2.4 gap statement 与贡献列表首尾呼应；相比 round-2 的"实质空白"已根本改观。

### 2.6 Clarity / 读者价值 — severity 1.5 | conf 0.80 | fix 0.95

- **[F-clar-1, 正面]** 两级评估的"有界主张"叙事对 Energies 读者有真实价值（proxy-AC gap 的量化是可迁移教训，DORA 框架下负面/反转结果受保护）；限制 6 条分点、结论克制、v1–v6 演化史坦白（§7）是画像加分项。
- **[F-clar-2, MODERATE]** 摘要 ~255 词超限，且承载了 F-sound-2/3 两处过强量词——压缩与纠偏一次完成。
- **[F-clar-3, MINOR]** "storage- and DER-rich"（§6.3）等表述与组成 CSV 直接冲突（DER=1），属 F-sound-1 的文字面。
- **[F-clar-4, MINOR]** `runtime_scalability` 场景名保留但已声明只按预算角色使用——处理得当，无需改。

### 2.7 Ethics — severity 1 | conf 0.85 | fix 1.00

- **[F-eth-1]** 四件套骨架齐、SimBench 公开数据无隐私问题、benchmark 演化史主动披露（诚信正资产）。
- **[F-eth-2, MINOR]** 缺 IRB/Informed Consent 两条 "Not applicable" 模板声明；缺 AI 辅助研发披露（ARA 证据链 provenance 全 ai-executed，MDPI 政策要求声明，实践中普遍缺失——提醒级，但本项目证据链公开后审稿人可见 provenance，主动披露优于被发现）。

---

## 三、对抗核验（最严重 3 条，对照证据 CSV 试图反驳）

### A1 = F-sound-1（HV–AC 权衡机制叙事）

**反驳尝试**：映射规则中储能被建模为 sgen 注入（load stress 放电），故"storage-rich"电气上近似"注入富集"，宽容解读下"DER-heavy"可读作"注入-heavy"，过电压代价确实存在（rural 网注入越限为实）。
**反驳失败点**：(a) 稿件同句显式区分并列出组成数字（6/7/1），"DER-rich"与 DER=1 直接冲突；(b) 因果链"→ high-DER 场景付出代价 → 因此 mid-pack"被逐案数据否定——CARS-MODE 在 high_der 不输于任何非退化方法（2/12 ≥ DE 2/12 > NSGA-II 0/12），失分在 base/peak/growth 系列（rural 储能过电压 + urban 加固不足过载）；(c) 真 DER-heavy 的 NSGA-II AC 排名更高。
**裁定：成立（severity 3 维持）**。这是全稿唯一能被审稿人拿公开 CSV 直接证伪的印刷主张，且位于论文核心卖点段。改写 §6.3 第二读段 + §7 第二段 + 摘要一处即可修复，计算结果不受影响。

### A2 = F-sound-2（"every optimizer beats No-Plan" 量词）

**反驳尝试**：Weighted Sum 的连续指标确有边际改善（min_vm 0.9636 > 0.9619；loading 88.4 < 90.8），"improves"或可指综合电气状态；或以"optimizer"隐含排除贪心填充。
**反驳失败点**：摘要明写 "improves **AC feasibility**"，可行率 0.500 = 0.500 无改善；Weighted Sum 计划非空、名列 Table 3 "baseline"，无排除依据；且同段落自己陈述其"sit at the reference level"，构成内部矛盾。
**裁定：成立（moderate）**。三处（摘要、§6.3、§9）改为"every front-returning optimizer"或"all methods except the degenerate MOEA/D (empty plan) and the automation-dominated Weighted Sum"。

### A3 = F-exp-2（AC 层证据强度 vs 结论权重）

**反驳尝试**：稿件已在 §6.3 末与 §8.1 两处明确降格为"consistent qualitative pattern, not a second statistically powered comparison"；画像明示"诚实交代不足的论文也被接受"；FixedDE 失效在 rural 网 peak/growth/n1 三场景方向一致，非单点噪声；NoDiversity 的 AC 同步下滑提供了侧向印证。
**反驳部分成功**：披露充分，非隐瞒型问题，severity 从 3 降为 2。
**残余风险**：摘要与结论仍以无 hedge 的因果句陈列（"loses the most AC feasibility"；"the adaptive component **buys** electrical robustness"），而底层差异 = 3/72 案（Fisher p≈0.73）、源于 seed-0 单计划一个储能动作。审稿人若做这道除法，会要求重述或补数据。
**裁定：部分成立**。最低成本修复 = 摘要/结论加 hedge（"consistently, though on a small per-method sample"）；最优修复 = AC 扩到 seeds 0–9（成本分钟级，864→8640 行），使权衡叙事获得统计支撑或被提前证伪。

---

## 四、Meta 决策

### RRI

| 维度 | Sev | Conf | 加权 | vs 录用基线 dim_mean | 超额 |
|---|---|---|---|---|---|
| Novelty | 1 | 0.80 | 0.80 | 2.87 | −2.07 |
| Soundness | 3 | 0.90 | 2.70 | 2.14 | **+0.56** |
| Experiments | 2 | 0.85 | 1.70 | 2.06 | −0.36 |
| Reproducibility | 1 | 0.90 | 0.90 | 2.16 | −1.26 |
| Related Work | 3 | 0.95 | 2.85 | 2.10 | **+0.75** |
| Clarity | 1.5 | 0.80 | 1.20 | 2.48 | −1.28 |
| Ethics | 1 | 0.85 | 0.85 | 1.79 | −0.94 |
| **合计** | | | **11.00/28 ≈ 39%** | | |

仅 **soundness（叙事矛盾）与 related_work（TODO 条目）**两维超出已录用论文基线，且二者 fixability 0.85–0.95（纯文本/文献作业，不动实验）。对照 accept_rri_stats（中位 61.5、P75 68 的绝对偏严尺度），本稿修复后落 accept/minor 区间概率高；round-2 的三个 severity-3 结构性缺口（灵敏度、真实基线、文献空白）已消解两个半。

### 预测决策

- **现状直接投**（假设 TODO 硬阻断已机械填完但叙事未改）：**Major Revision 45% / Minor 40% / Reject 5% / Accept 10%** —— F-sound-1 若被抓即 major；未被抓则 minor。
- **完成下方 P0/P1 清单后投**：**Minor Revision 55% / Accept 25% / Major 20%**。
- 期刊适配无变化：Energies 首选合理（DORA 保护负面/反转结果的叙事正是本稿卖点）。

### 优先级修改清单

| # | 级 | 修改 | 位置 | 工作量 |
|---|---|---|---|---|
| 1 | **P0** | 重写 HV–AC 机制叙事：改为"代理奖励储能/托管指数 → 储能富集组合在 rural 网基础/峰荷场景过电压、并挤占加固致 urban 过载"；删除/修正 "storage- and DER-rich" 与 "DER-heavy … high-DER" 因果链；补一句 NSGA-II（DER-rich）AC 更好、high_der 场景 NoPlan 反超是映射规则伪影 | 摘要、§6.3 第 2–3 读段、§7 第 2 段 | 半天 |
| 2 | **P0** | 参考文献收口：9 条补作者、3 条年–卷矛盾核正（Qi/review/WGAN：卷 19=2026）、Gonzalez-Longatt 人名核实、题级点评对 PDF 复核 | References、§2 | 1 天 |
| 3 | **P0** | 量词纠偏："every optimizer's plan mix improves…"（×3 处）改为限定式；"loses the most / largest drop" 改"tied for the largest overall; NoDiversity lower under stress" | 摘要、§6.3、§9 | 1 小时 |
| 4 | **P1** | AC 验证扩至 seeds 0–9 折衷计划（10 计划 × 72 案/方法），重出 Table 6 带均值±区间；若不可行则在摘要/结论为权衡句加 small-sample hedge | §5.4、§6.3、Table 6 | 1–2 天（算力分钟级） |
| 5 | **P1** | 投稿机械项：作者/单位/通讯/贡献/基金填写；仓库 Zenodo/GitHub DOI 落地；摘要压至 ≤200 词；补 IRB/Consent "Not applicable" 与 AI 辅助声明；MDPI 模板转换 | 头尾matter | 1 天 |
| 6 | P2 | §2 加特征对比表（本文 vs 5–8 篇最近工作：组件/约束处理/统计协议/AC 验证）；补 2–4 篇 2024–2026 引文拉高近 5 年占比 | §2 | 半天 |
| 7 | P2 | 表 7 双 default 行加脚注（独立重跑）；§6.3 括注 CARS-MODE/NSGA-II storage_allocation 组成撞车（24 案共享，恰证映射方法无关）；§3.2 加一句 EHV–LV 候选池 vs MV 验证网的电压等级边界声明 | §6.4、§6.3、§3.2 | 2 小时 |

### 一句话总评

数字层无懈可击（全表零偏差、种子/归一化/统计协议规范、证据链公开可核），round-2 的结构性 P0 已基本清偿；剩余风险集中在**一段可被自家 CSV 证伪的机制叙事**、**9+3 条参考文献作业**与**AC 层小样本上的结论权重**——全部是文本与文献级修复，不需要新实验（AC 扩种子除外，且便宜）。修完即达该刊已录用论文的中位画像之上。
