# mintou_p4（SHIELD-MOEA）期刊投稿评审：IEEE Access vs MDPI Energies

评审基准：两刊 SKILL.md 中 "Distilled review standards"（IEEE Access 为 4 篇电力/负荷全文 + 10 篇摘要蒸馏；Energies 为 34 篇电力系统全文蒸馏，2023–2026）。ARA 事实来源：`papers\mintou\mintou_p4_shield_resilience_planning\`。评审日期 2026-07-13。

---

## 一、论文概况

SHIELD-MOEA 是一个"场景筛选 + 局部修复 + 韧性感知 Pareto 优化"的混合多目标进化框架，面向 DER/负荷/停电不确定性下的配电网韧性规划。当前公共证据为 SimBench 衍生规划实验 v2（单一测试系统：`1-complete_data-mixed-all-0-sw`，18 个子网、72 个候选规划动作），主指标为自定义 **hypervolume proxy**：SHIELD-MOEA 均值 `0.79432775`，领先最强 baseline MOEA/D（`0.77286075`）`+2.78%`，领先最强 ablation NoScenarioScreen（`0.76928208`）`+3.26%`（`evidence/runs/real_simbench_planning_analysis.md`）。关键边界：**该实验是基准衍生的规划代理，不含任何 AC/pandapower 潮流可行性验证**；每方法仅 3 次 repeat 且多数 repeat 数值完全相同（近确定性运行，无方差可报告）；ARA 中保留的 v1 弱结果（`real_simbench_planning_analysis_v1_weak.md`）显示改进前信号为 `-1.71%`，说明当前优势对场景/修复配置敏感。claims.md 也自我约束："在补齐 AC/pandapower 可行性检查前，数值性稿件声明必须限定在基准衍生规划指标内"。

---

## 二、期刊匹配度对比

### MDPI Energies — **Fit: Medium-High（推荐首选）**

**题材契合度（High）**：配电网韧性规划 + DER/负荷不确定性 + 多目标规划，正中 Energies "electrical power & energy systems / smart grids" section 的核心射程；Energies 蒸馏语料本身就是"规划-调度-预测"类论文，韧性规划是其常见选题。scope 是 MDPI 第一desk-reject 杠杆（mdpi-common.md），本文在此项无风险。

**对照 Energies 蒸馏标准逐条核对**：
- 新颖性下限（可命名的机制组合 + gap 陈述，31/31 无全新算法）——SHIELD-MOEA 的"场景筛选 × 局部修复 × 韧性目标"组合式创新**达标**；+2.78% 的诚实幅度符合"≤5% 改进如实报告即可通过"的惯例。
- 实验下限（≥1 个可识别测试系统 + 方案自对比）——单一 SimBench 系统符合"约 2/3 论文单测试系统"的常态；5 个外部 baseline 超过"仅约半数录用论文有外部算法对比"的水平，**达标且有富余**。
- **敏感性分析（近强制；缺失是第一大 major-revision 触发器）——当前完全缺失**。experiments.md 的 8 个主实验均为场景切换对比，没有任何参数敏感性（场景数、筛选阈值、种群规模、目标权重）扫描。`low_scenario_count` ablation 只在 synthetic smoke 中有数据，未进入 SimBench v2 结果表。**这是投 Energies 的第一缺口**。
- 统计检验/30 次运行/开源代码——Energies 实践中不要求（0/29、1/34），本文 3-repeat 不构成 Energies 硬伤。
- 硬性下限（Funding/COI/Data Availability/Author Contributions 100% 必备）——ARA 未涉及，成稿时必须补。
- **"未验证仿真"是明示 desk-reject 触发器**——本文最大风险点：hypervolume proxy、survivability_rate、expected_loss_index 均为自定义代理指标，无 AC 潮流、无实测/数值验证闭环。Energies 蒸馏虽指出"自定义指标上的夸大百分比"是已发表论文的漏网点，但主动依赖漏网点不是投稿策略；pandapower 本地已缓存，补验证成本低。

### IEEE Access — **Fit: Medium（备选）**

**题材契合度（High）**：power & energy 是 Access 五大高产领域之一，跨"进化计算 × 电力系统"的组合正合其鼓励的跨领域应用型工作。

**对照 Access 蒸馏标准逐条核对**：
- soundness-not-novelty：组合式创新在 Access 不是问题；3–6 条编号贡献列表是准刚性惯例，成稿需遵守。
- **元启发式社区统计惯例：50+ 独立运行 + Wilcoxon/Friedman + 收敛曲线/箱线图**。本文是典型 MOEA 论文，会被按此标尺审：当前 SimBench v2 每方法 **3 次 repeat 且多组 repeat 数值逐位相同**（如 SHIELD-MOEA 在 `deterministic_vs_scenario` 三次全为 `0.80131149`），既无独立随机种子也无可检验方差。**这是投 Access 的第一缺口，且比 Energies 的缺口更硬**。
- 二元裁决（无 major/minor revision 往返，一次 resubmission 机会）：论文必须在提交时接近终稿。当前证据链（proxy-only + 3-repeat + 无敏感性分析）距离"提交即终稿"较远，二元模型下容错率低。
- 公平性声明（统一计算预算/参数对齐）在 2/4 录用论文中出现并被视为加分——当前 ARA 未记录各算法的种群/评估次数预算对齐情况，需补。

### 最终推荐

**首选 MDPI Energies**（与 PAPER.md frontmatter 一致）。理由：(1) 韧性规划题材与 Energies scope 契合度最高；(2) Energies 不要求 50-run 统计协议，本文最难补的重复实验缺口在 Energies 侧代价最小；(3) 需要补的两件事（AC 可行性验证、敏感性分析）都是 Energies 明示的通过条件，目标明确。**IEEE Access 保留为备选**，但若转投必须先补 30–50 次独立运行 + 非参数检验 + 收敛/箱线图，否则在元启发式社区标尺下大概率一轮被拒（且 Access 只允许一次重投）。

---

## 三、写作修改清单（对照期刊惯例与 ARA 薄弱点）

1. **related_work.md 实质为空**（仅一行指向 `comparison_analysis.md` 的占位）。Energies 明示"文献综述不充分"是 desk-reject 触发器。需成体系撰写三线综述：韧性规划（防灾加固/灾后恢复两阶段范式）、场景生成与削减（scenario generation & reduction）、多目标进化算法在配网规划的应用，并落到"场景筛选嵌入 MOEA 循环"这一 gap 上。
2. **韧性指标定义不清晰**。concepts.md 只定义了 4 个概念，`survivability_rate`、`expected_loss_index`、`voltage_violation_probability`（experiments.md 所列）与结果 CSV 中实际字段 `voltage_risk`、`reliability_proxy` 存在**命名不一致**；hypervolume proxy 与标准 hypervolume（参考点、归一化方式）的关系未在任何 logic 文件中写明。稿件必须给出每个韧性指标的数学定义、参考点选择及其与韧性文献标准指标（EENS、load not served、resilience trapezoid）的映射关系，否则"自定义指标 + 夸大百分比"会触发两刊共同的审稿质疑。
3. **场景筛选机制的动机论证缺失**。method.md 只有一句"Combines scenario screening with resilience-aware Pareto optimization"。需论证：为什么筛选而非全场景评估（计算预算论证——但当前 runtime ~0.0003 s 反而削弱该动机，见实验缺口第 5 条）；筛选准则是什么（代表性？极端性？）；筛掉的场景如何保证不低估风险。v1 弱结果显示筛选配置直接决定正负信号（-1.71% → +2.78%），审稿人会追问筛选机制的稳定性依据。
4. **claims 与证据的措辞对齐**。claims.md C3"remains feasible or robust under stress"仅"Partially supported"；成稿中 outage/stress 相关声明必须降格为 proxy 指标层面的表述，或在补 AC 验证后再升格。C1 的"target-journal-level baselines"措辞在稿件中应替换为具体 baseline 列表。
5. **贡献列表与限制段**。两刊都吃"完整叙事：gap → contribution → experiment → limitation"。ARA 的 Interpretation Boundary 写得很好，应转写为正文 Limitations 段（proxy 验证边界、单测试系统、场景模型简化），诚实限制在两刊蒸馏中均为加分项。
6. **避免已知漏网点**：结论不做"可推广到输电网/其他基础设施"之类无证据泛化（Access 蒸馏点名）；自引控制；标题-案例匹配（标题含 "Distribution Network" 而实验用 SimBench mixed EHV/HV/LV 全电压层级网络，需在稿中说明子网抽取如何对应"配电网"——source profile 显示 18 个子网含 EHV1/HV1/HV2，严格说不全是配电层级）。
7. **MDPI 格式硬性项**：Data Availability Statement（SimBench 公开数据 + 代码可给出仓库）、Author Contributions（CRediT）、Funding、COI 四件套 100% 必备；摘要 ~200 词、IMRaD、MDPI 编号引用格式。

---

## 四、实验设计缺口

1. **Baseline 数量与质量（5 个，六篇组合中最少）**。对元启发式规划论文，5 个在 Energies 够用（超过其"约半数有外部对比"惯例），在 Access 属于下限。真正的问题是**质量**：(a) 结果 CSV 中 `Weighted Sum` 与 `Deterministic Planning` 两条 baseline 在所有实验、所有 repeat 中数值**逐位完全相同**（如均为 `0.45465591/0.03240373/0.43017204…`），实际退化为同一方法记两个名字，有效外部 baseline 只有 4 个，审稿人核表即穿；(b) method.md 承诺的 `Stochastic MILP-small` 只出现在 synthetic smoke，**未进入 SimBench v2 公共结果**，规划文献最强的两阶段随机规划对照缺席；(c) 无 2015 年后的现代 MOEA（NSGA-III、SPEA2、MOPSO、C-TAEA 任选其二）。建议：修复重复 baseline、把 MILP 补进公共实验、加 1–2 个现代 MOEA，达到 6–7 个有效对照。
2. **重复运行与统计检验**。SimBench v2 仅 3 repeat，且 SHIELD-MOEA/NSGA-II/MOEA/D 的多数 repeat 结果完全相同（未变随机种子或算法退化为确定性）。Access 元启发式惯例为 **50+ 独立运行 + Wilcoxon/Friedman + 收敛曲线/箱线图**；Energies 虽不强制（0/29 有显著性检验），但当前 +2.78%（对 MOEA/D）、且对 NSGA-II 的单场景差距仅约 0.96%（`0.80131` vs `0.79372`，deterministic_vs_scenario），**无方差的 3-repeat 无法支撑这么窄的优势**。最低要求：30 次独立种子运行 + 均值±标准差 + Wilcoxon 秩和检验；投 Access 则升到 50 次。
3. **敏感性分析（Energies 第一大 major-revision 触发器）完全缺失**。至少需要：筛选场景数 K 的扫描（把 `low_scenario_count` 从 smoke 升级进公共实验即可复用）、种群规模/评估预算、韧性目标权重或参考点、不确定性幅度（DER 出力方差、负荷增长率）四个维度中的 2–3 个。
4. **AC/pandapower 可行性验证缺失（两刊共同的最高退稿风险）**。所有电气量均为 proxy；Energies 明示"unvalidated simulation"desk-reject。pandapower 已本地缓存（CACHE_STATUS.md），portfolio_status.md 的 Next Upgrade Path 第 4 条也已排期"Add AC/pandapower feasibility and scenario variance for P4"。最低闭环：对 Pareto 前沿代表解跑 AC 潮流，报告电压/载流可行率，并用 AC 结果校准 voltage_risk proxy 的保守性。
5. **问题规模可信度**。72 个候选动作、单方法 runtime ~0.0003 s 的问题规模，无法支撑"场景筛选降低计算负担"的动机，也易被质疑为 toy problem。需扩大候选空间（更多子网/更细动作粒度）或增加第二个测试系统，同时报告有意义的计算时间。
6. **N-k / 极端天气场景设计不符合韧性文献惯例**。当前 `outage_contingency` 实验中所有方法的 survivability_rate 均为常数 `0.94`、`unseen_stress_generalization` 中均为 `0.91`——故障场景对方法**无区分度**，说明停电模型过于简化（疑似全局折减系数而非元件级故障）。韧性文献惯例是：显式 N-1/N-2 线路故障枚举，或基于脆弱性曲线（fragility curve）的极端天气（台风/冰灾）空间相关多重故障场景 + 恢复时序。至少应实现元件级随机 N-k 抽样，使 survivability 在方法间产生可比差异；`restoration_aware_evaluation` 目前与主实验结果完全相同（CSV 中数值逐行一致），需要真实的恢复过程模型支撑，否则应从稿件删除该实验名义。

---

## 五、数据集缺口

**已缓存且够用（CACHE_STATUS.md, 2026-07-12）**：
- `simbench`（主实验，已用）；`pandapower`（AC 验证依赖，**已缓存未使用**——P0 直接可做）；`matpower`/`pglib_opf`（含 IEEE 33-bus 等标准配网算例）；`rts_gmlc`；`c2ges_nerc_reports`（NERC 停电/灾害报告缓存）。
- 已标注"对标 p4"的新增缓存：`ausgrid_solar_home`（真实屋顶光伏+用户负荷，可替换 DER/负荷不确定性的合成分布）、`sgsc`（半小时智能电表 1.7GB，负荷不确定性实测来源）。两者已下载但尚未接入 p4 实验。

**建议补齐**：
1. **IEEE 33-bus / 123-bus 标准配网测试系统**（韧性规划文献的事实标准算例）：本地 `matpower`/`pandapower` 缓存已含 case33bw 等，**零下载成本**即可作为第二测试系统，同时化解"SimBench mixed 网含 EHV/HV 与标题不符"的问题。
2. **历史灾害/停电数据用于场景动机与参数标定**：`c2ges_nerc_reports` 已缓存，可用于引言动机与故障率参数引用；若要做数据驱动的极端天气场景，可选补 DOE **EAGLE-I** 县级历史停电数据集（未缓存）或 NOAA Storm Events（未缓存）——属 P2 增强项，非必需。
3. **DER/负荷不确定性实测化**：把已缓存的 `ausgrid_solar_home`（光伏）与 `sgsc`（负荷）分布接入场景生成器，替代当前合成扰动，可显著提升 Energies 审稿人对"validation against real data"的认可。
4. problem.md 声称的数据集列表（SimBench、pandapower、OPSD、RTS-GMLC、NERC/C2GES）与实际只用 SimBench 的现状不一致——要么补用，要么在 ARA 与稿件中收窄声明。

---

## 六、优先级行动清单

### P0（不做即有 desk-reject / 一轮拒稿风险）
1. **补 pandapower AC 潮流可行性验证**：对各方法 Pareto 代表解跑 AC 潮流，报告电压越限率/线路载流可行率，校准 proxy 指标（依赖已缓存，portfolio 已排期）。
2. **修复 baseline 表**：消除 `Weighted Sum` ≡ `Deterministic Planning` 的逐位重复；把 `Stochastic MILP-small` 补进 SimBench 公共实验。
3. **30 次独立种子重复 + 方差报告**：修复当前 repeat 间数值完全相同的种子问题；报告均值±标准差；窄优势（+2.78%）必须有方差背书。投 Access 则升级为 50 次 + Wilcoxon/Friedman。
4. **敏感性分析**（Energies 近强制）：至少做筛选场景数 K、不确定性幅度、评估预算三选二的扫描。
5. **撰写 related work**（当前为空）与韧性指标的数学定义（统一 experiments.md/CSV/稿件的指标命名）。

### P1（大幅降低 major revision 概率）
6. **重做 outage 场景模型**：元件级 N-1/N-k 随机故障抽样替代全局折减（当前所有方法 survivability 恒为 0.94/0.91，无区分度）；`restoration_aware_evaluation` 要么实现真实恢复时序，要么删除。
7. **加第二测试系统**（IEEE 33-bus，本地 matpower/pandapower 零成本），并扩大候选动作空间以支撑"筛选降低计算负担"的动机。
8. **接入实测不确定性数据**：`ausgrid_solar_home`（PV）+ `sgsc`（负荷）驱动场景生成。
9. **补 1–2 个现代 MOEA baseline**（NSGA-III / SPEA2 / MOPSO 任选），并记录各算法统一评估预算的公平性声明。
10. 场景筛选机制的动机论证与稳定性说明（引用 v1 弱结果 → v2 的改进路径作为筛选配置敏感性的诚实披露）。

### P2（锦上添花）
11. Pareto 前沿可视化 + 收敛曲线 + 箱线图（Access 惯例图件，Energies 亦加分）。
12. 引入 EAGLE-I / NOAA 历史灾害数据做数据驱动的极端天气场景（当前用 NERC 报告缓存做动机引用即可）。
13. 代码开源（两刊均不强制，但 Access 的 reproducibility initiative 可作 soundness 加分）。
14. 排查 MDPI 四件套声明、匹配的 Special Issue（配网韧性/智能电网方向常年有开放 SI），核对最新 APC（Energies ≈ CHF 2,600 / Access ≈ USD 2,160，以官网为准）。

---

*本评审基于 ARA 工程 2026-07 快照；期刊数字（IF/APC/时限）须在投稿前于官方页面复核。*

---

## 进展更新（2026-07-13）

**P0（AC/pandapower 可行性验证）已完成**：`src/powergrid_benchmark/mintou_pandapower_validation.py` 在 4 个 SimBench MV 网络 × 6 个压力场景（含 1.5x 增长 + N-1 线路故障）上校验了全部 11 个方法（3 个实验）的规划构成，证据见本论文 `evidence/runs/real_ac_validation_*` 与 `tables/real_ac_validation_summary.csv`。

结果（如实）：SHIELD-MOEA 与 MOEA/D 并列全方法最高 AC 可行率（0.653 vs No-Plan 0.500），且平均最大线路载流全场最低（60.3% vs No-Plan 90.8%）——韧性叙事有了真实潮流数据支撑；N-1 与极端增长场景同时兼作敏感性分析轴。**注意**：NoOutage 消融与 SHIELD-MOEA 同分，说明构成粒度的 AC 校验尚不能为 outage 筛选组件提供差异化证据，须与 P1-6（元件级 N-1/N-k 故障模型重做）配合。剩余关键缺口不变：3-repeat 无方差问题（应参照 p5/p6 的 v2 模式把规划管线也重写为真实 MOEA + 30 seeds + 统计检验）。

## 第二次进展更新（2026-07-13 下午）

**规划管线真实 MOEA 重写已完成**（`mintou_real_planning.py` v2，代理版产物保留为 `*_proxy_methods_deprecated.*`）：

- SHIELD-MOEA 为真实实现：NSGA-II 内核 + GA/DE 混合变异 + **真实场景筛选机制**（每 5 代在 16 个固定随机场景中筛选种群表现最差的 K=4 个作为搜索期适应度；最终评价永远用不相交种子的全场景集，筛选无法泄漏进打分）+ 可行性修复。场景不确定性（负荷/DER/故障因子）是方法无关的问题属性；另报告 worst-case HV 作为鲁棒性读数。30 seeds + Mann-Whitney/Holm。
- **主结果**：SHIELD-MOEA 平均 HV 比 NSGA-II 高 **5.56%**，40/40 基线对比全部 Holm 显著、零显著败绩——信号 `significant_public_signal`，统计协议达到两刊底线。
- **组件级发现（如实写）**：修复算子是主要贡献源（NoRepair 0.252 vs 0.274）；场景筛选对均值 HV 贡献小（vs NoScenarioScreen +0.5%）但搜索更省时；NoResilienceObj 微超 0.26%（不显著）。
- **AC 校验 v2（新方案构成）**：SHIELD-MOEA 并列最高 AC 可行率（0.708 vs No-Plan 0.500）；**NoOutage 消融掉到 0.625、最大载流恶化到 82.3%——故障感知搜索组件首次获得 AC 层面的真实差异化证据**（上一轮同分的问题已解决）。

**剩余缺口**：成本货币化标定、元件级 N-1/N-k 模型（若要加深韧性主张）、related_work、收敛曲线/箱线图。3-repeat 无方差问题已随重写消除。
