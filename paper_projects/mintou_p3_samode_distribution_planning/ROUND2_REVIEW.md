# Round 2 — mintou_p3 (CARS-MODE) 完整 7 维评审

- **日期**: 2026-07-13
- **评审类型**: paper_reviews 标准 7 维离线结构化评审（离线、确定性、基于 ARA 证据链 + Paper_CCF 期刊画像蒸馏标准）
- **论文**: *Self-Adaptive Multi-Objective Differential Evolution for Reproducible Distribution Network Planning with DER and Storage Integration*
- **算法**: CARS-MODE（Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution）
- **目标刊**: MDPI Energies（首选）/ MDPI Applied Sciences（备选）
- **优先级**: FAST PUBLICATION（允许算法/数据集/下游任务大幅修改，保留"多目标差分进化 + 配电网规划 + DER/储能"大方向）
- **证据基线**: ARA 工程 `papers/mintou/mintou_p3_samode_distribution_planning/`（v1–v5 全保留证据 + AC 潮流验证 v1）
- **校准锚点**: Paper_CCF mdpi-energies SKILL.md（34 篇电力系统全文蒸馏，2023–2026）+ mdpi-applied-sciences SKILL.md（11 篇电力/能源全文蒸馏）

---

## 一、Summary

CARS-MODE 将约束感知修复算子与多样性/违约信号驱动的策略自适应组合为多目标差分进化算法，用于配电网扩展规划、DER 选址定容与储能配置。当前证据基于 SimBench `1-complete_data-mixed-all-0-sw`（18 子网、72 候选动作）派生的 DER/storage stress v5 基准：代理 hypervolume 0.55322842，仅超最强基线 NSGA-II 0.46%、超最强消融 FixedDE 0.19%。该信号经历了 v1（-13.55%）/v2（-13.55%）/v3（-3.11%）三轮 weak 与 v4 near-miss（+0.48% vs 基线但 -1.00% vs NoDiversity 消融）才在场景重设计后转正。新增的 pandapower AC 潮流验证（4 个 SimBench MV 网络 × 6 压力场景）解决了"unvalidated simulation"桌拒红线，但显示 CARS-MODE 与 NSGA-II/MOEA/D 在 AC 可行率上完全同分（0.625），且 GA（0.639）和 NoDER 消融（0.667）反而更高。两个核心组件中，constraint-aware repair 有强消融支撑（NoRepair 违约率 21.5% vs 7.0%），但 strategy-adaptive 仅 0.19% 差距且 3 seeds 下无法统计区分。**整体判断：当前状态距 Energies 投稿有 2 个 P0 缺口（灵敏度分析、IEEE 33-bus 标准算例），距 Applied Sciences 有 1 个 P0 缺口（量化经济效益 or 强灵敏度分析替代）。修复周期 3–5 周。**

---

## 二、Target Venue 适配评估

### MDPI Energies（首选）

```
[Target] Energies (MDPI)
[Fit] Medium（AC 验证已补齐；被灵敏度分析缺失 + 单一非标准测试系统 + strategy-adaptive 消融薄弱压制）
[Contribution type] modeling / 算法改进型规划方法
[Main evidence gap] 灵敏度分析（近强制，缺失=第一大 major-revision 触发项）；IEEE 33/69-bus 标准算例
[Top rejection risk] validation（已部分消解）/ experiments（灵敏度缺失）/ related_work（实质空白）
[Re-route suggestion] Applied Sciences（备选，应用价值逻辑主导）
```

### MDPI Applied Sciences（备选）

```
[Target] Applied Sciences (MDPI)
[Fit] Medium-Low（缺乏真实 utility/field case study + 量化经济效益；灵敏度分析可替代但同样缺失）
[Contribution type] applied-method / simulation-with-validation
[Main evidence gap] 量化经济收益（"30% investment saved"类）或强灵敏度分析；真实案例
[Best-fit Section] Electrical/Electronics & Communications 或 Energy
[Top rejection risk] too-theoretical / weak-applied-value / scope-Section
[Re-route suggestion] MDPI Energies（能源对口度更高）
```

---

## 三、7 维评审

### 3.1 Novelty（新颖性）

**Severity: 1 | Confidence: 0.85 | Fixability: 0.9**

**Findings:**

1. **[F-novelty-1] 命名机制组合通过 Energies 门槛** — Energies 蒸馏标准明确："zero of 31 research papers introduced a fundamentally new algorithm"，"a nameable mechanism-combination / framework integration / modest algorithm improvement tied to a gap statement" 即够。CARS-MODE 组合了 constraint-aware repair + strategy-adaptive DE，属于可命名的机制组合，且规划类论文中这一具体组合确实未被报告过。`logic/solution/method.md` 创新点 1-2 对此有清晰陈述。

2. **[F-novelty-2] Strategy-adaptive 组件的存在性论证薄弱** — FixedDE 消融仅差 0.19%（`evidence/tables/real_simbench_planning_leaderboard.csv`：CARS-MODE 0.55322842 vs FixedDE 0.55217215），在 3 seeds × 7 scenarios = 21 runs 下无法排除随机波动。更严重的是，v4 near-miss 阶段 NoDiversity 消融曾反超全方法 1.00%（`evidence/runs/real_simbench_planning_analysis_v4_near_miss.md`），暗示 strategy-adaptive 的效果高度依赖场景设计。Energies 蒸馏标准中明确点出 "hybrid algorithms with no per-component justification" 是已知滑漏项。

3. **[F-novelty-3] 增益幅度处于诚实报告的可行范围** — 0.46% 在 Energies 蒸馏标准"≤5% improvement passes if honestly reported"范围内，但必须框定为 "narrow proxy-level gain"，不可膨胀为 "significant improvement"。

**Top fix**: 在正文中按场景分解展示 strategy-adaptive 在哪些具体场景（如 constraint_repair、load_growth）提供差异化增益，补强组件级论证。若场景分解后仍无差异化，在贡献表述中将 strategy-adaptive 降级为 "implementation feature" 而非核心创新。

---

### 3.2 Soundness（方法健全性）

**Severity: 3 | Confidence: 0.90 | Fixability: 0.7**

**Findings:**

1. **[F-sound-1, SEVERE] AC 潮流验证暴露方法无差异化** — `evidence/tables/real_ac_validation_summary.csv` 显示 CARS-MODE 与 NSGA-II、MOEA/D 在所有 AC 指标上完全同分（ac_feasible_rate=0.625, stress_feasible=0.550, mean_min_vm=0.972263 pu, mean_max_loading=75.8268%, mean_losses=0.517248 MW）。GA（0.639）和 NoDER 消融（0.667）的 AC 可行率反而更高。这意味着：(a) 代理 hypervolume 的 0.46% 增益未传导到 AC 可行性层面；(b) 规划组合的构成粒度（action-kind counts）太粗，不同优化器收敛到几乎相同的组合。`evidence/runs/real_ac_validation_analysis.md` 的 Mapping Assumptions 明确承认 "it is not a nodal siting/sizing study"。

2. **[F-sound-2, SEVERE] 代理目标函数与规划任务脱节** — `mean_runtime_s ≈ 1e-4`（`evidence/tables/real_simbench_planning_leaderboard.csv`：CARS-MODE 0.00012223s）暴露目标函数是廉价代理而非真实潮流计算。这使得"runtime_scalability"场景的结论（规划可扩展性）毫无意义——在 1e-4s 评估下讨论可扩展性是自欺欺人。`logic/experiments.md` 中的 runtime_scalability 实验存在逻辑缺陷。

3. **[F-sound-3, MODERATE] 约束违约率仍然偏高** — CARS-MODE 平均约束违约率 7.04%（`evidence/tables/real_simbench_planning_leaderboard.csv`），虽然比 NoRepair 的 21.5% 低很多，但 7% 的违约率在规划论文中不可被框定为 "feasible"。`logic/claims.md` C3 原文 "remains feasible or robust" 严重越界。

**Top fix**: (a) 将规划管线从代理目标函数升级为真实 MOEA 实现（节点级选址定容），使不同方法在 AC 可行率上产生差异化——这是 JOURNAL_REVIEW.md 进展更新中已识别的"剩余关键缺口"；(b) 若短期内无法实现节点级优化，将论文定位从"方法优越性"转向"规划框架 + 约束修复机制"，以 repair 组件（21.5%→7.0% 违约率降低）为核心论据，弱化方法间横向比较。

---

### 3.3 Experiments（实验充分性）

**Severity: 3 | Confidence: 0.95 | Fixability: 0.85**

**Findings:**

1. **[F-exp-1, SEVERE] 灵敏度分析完全缺失** — 这是 Energies 蒸馏标准中的**第一大 major-revision 触发项**（"near-mandatory; its absence is the top major-revision trigger"）。当前证据无任何参数扫描。`logic/experiments.md` 规划的 `low_scenario_count` 消融可升级为灵敏度维度，但未执行。Energies 34 篇蒸馏论文中灵敏度分析几乎普遍存在。

2. **[F-exp-2, SEVERE] 仅单一非标准测试系统** — SimBench `1-complete_data-mixed-all-0-sw`（18 子网、72 候选、总负荷 71.3 GW、RES 12.2 GW，见 `evidence/source/real_simbench_planning_source_profile.csv`）是欧系综合基准，但**不是配网 DER/储能规划文献的事实标准**。IEEE 33-bus 和 69-bus 才是两刊同题论文几乎必备的标准算例（JOURNAL_REVIEW.md §五明确指出"两刊同题论文几乎必备"）。Energies 蒸馏显示约 2/3 录用论文仅单一系统，但该系统需是"可识别的 test case"——SimBench 在配网规划文献中的辨识度远低于 IEEE 33/69。

3. **[F-exp-3, MODERATE] 消融实验不完整** — `logic/experiments.md` 规划了 8 个消融，v5 leaderboard 仅报告 4 个（NoRepair、FixedDE、NoDiversity、NoDER）。缺失：`no_strategy_adaptation`（与 FixedDE 关系未澄清）、`no_storage_candidates`、`weighted_sum_only`（以基线形式存在但角色未说明）、`low_scenario_count`。特别是 `no_strategy_adaptation` 是 strategy-adaptive 组件的直接消融，缺失使 C2 主张的证据链断裂。

4. **[F-exp-4, MINOR] 重复次数不足** — 每方法 3 seeds × 7 场景 = 21 runs。Energies 蒸馏标准显示"not required: 30-run protocols"，因此 3 seeds 不构成硬伤。但 proxy 目标函数极快（1e-4s/eval），增至 30 seeds 的计算成本近零，且可为策略自适应组件提供更稳健的证据。

5. **[F-exp-5, MINOR] 无收敛曲线/箱线图** — `evidence/figures/` 目录仅有 README 占位。Energies 非强制但普遍存在。

**Top fix**: (a) **P0 补灵敏度分析**：至少 3-4 个参数扫描（种群规模、修复强度上限、自适应触发阈值、DER 渗透率/负荷增长率——后者可从 AC 验证的 6 场景轴直接提取）；(b) **P0 加 IEEE 33-bus**：pandapower.networks 内置 case33bw，零下载成本，接入现有管线即可；(c) 补齐缺失消融或澄清 FixedDE ≡ no_strategy_adaptation。

---

### 3.4 Reproducibility（可复现性）

**Severity: 1 | Confidence: 0.80 | Fixability: 0.95**

**Findings:**

1. **[F-repro-1] 公共基准 + 完整证据链是优势** — SimBench 是公开数据（`evidence/source/real_simbench_planning_source_profile.csv` 记录了精确的子网来源），实验代码路径（`src/code/run_real_simbench_planning.py`）、配置（`src/configs/real_simbench_planning_config.json`）和环境说明（`src/environment.md`）均存在。v1-v5 全部证据保留（含负面结果），exploration_tree.yaml 记录完整决策链。这超过了 Energies 蒸馏标准中"1/34 open code"的普遍水平。

2. **[F-repro-2, MINOR] 代码/数据未公开发布** — 虽然 ARA 工程完整，但未发布到公共仓库（GitHub/Zenodo）。Energies 不强制 open code（1/34），但 Data Availability Statement 需说明数据获取方式。SimBench 公开可获取是加分项。

3. **[F-repro-3, MINOR] AC 验证为单次 repeat** — `evidence/runs/real_ac_validation_analysis.md` 注明 "repeat=1"，不构成方法间可比较的稳健证据。

**Top fix**: 准备 Zenodo/GitHub release，在 Data Availability Statement 中给出仓库路径。AC 验证至少对 CARS-MODE 和 top-2 基线增至 3 repeats。

---

### 3.5 Related Work（文献综述）

**Severity: 3 | Confidence: 0.95 | Fixability: 0.80**

**Findings:**

1. **[F-rw-1, SEVERE] 文献综述实质空白** — `logic/related_work.md` 仅包含一行指针："Comparator evidence source: `papers/literature/target_journal_related/comparison_analysis.md`"，无实际内容。Energies 蒸馏标准要求"adequate, current literature review"，且 desk-reject triggers 明确包含"inadequate literature review"。配网 DER/储能规划是两刊高密度题材，审稿人期望看到近 3 年 30+ 篇同题文献的覆盖。

2. **[F-rw-2, MODERATE] 无 gap 陈述的文献锚定** — CARS-MODE 的两个组件（constraint-aware repair + strategy-adaptive DE）需要分别锚定到已有文献：(a) 配网规划中的约束处理策略（repair vs penalty vs feasibility rules）；(b) MOEA 中的自适应机制（JADE、SaDE 等经典自适应 DE 文献）；(c) 配网 DER/储能规划的最新综述和代表性方法。这三块目前全部缺失。

3. **[F-rw-3, MINOR] 自引风险低** — 当前无自引内容，但也意味着无任何引文。撰写时需注意自引克制（Energies 蒸馏标准："excessive self-citation is an integrity flag"）。

**Top fix**: 这是撰稿工作量最大的空白。需覆盖：(a) 配网扩展规划经典与最新方法（5-8 篇）；(b) DER/储能选址定容（5-8 篇）；(c) MOEA 在电力系统规划中的应用（5-8 篇）；(d) 自适应 DE 变体（JADE、SaDE、SHADE 等，3-5 篇）；(e) 约束处理技术综述（2-3 篇）。优先覆盖近 3 年 Energies/Applied Sciences/Access 同题论文。

---

### 3.6 Clarity（表述清晰度）

**Severity: 2 | Confidence: 0.85 | Fixability: 0.95**

**Findings:**

1. **[F-clar-1, MODERATE] Claims 措辞超出证据边界** — 已在 JOURNAL_REVIEW.md §3.1 详细审计：
   - C1 "improves planning quality" → 证据只是 proxy hypervolume，不是规划质量
   - C3 "remains feasible or robust" → AC 验证显示仅 0.625 可行率，且与基线同分
   - `method.md` 创新点 3 "Reports Pareto quality and electrical feasibility together" → AC 验证是后加的，且是 composition-level 映射而非 nodal siting
   - 这些越界主张若进入稿件会被认真审稿人直接指出

2. **[F-clar-2, MODERATE] 论文叙事架构未建立** — 当前 ARA 材料是工程文档，不是论文草稿。缺少：IMRaD 结构、~200 词摘要、3-8 关键词、编号贡献列表（3-5 条）、Case Study 小节（含网络示意图）、MDPI 模板格式。

3. **[F-clar-3, MINOR] v1-v5 演化史是潜在叙事资产** — 从 v1 的 -13.55% 到 v5 的 +0.46%，经历了约束修复引入、NoDER 消融修正、DER/storage 场景重设计、多样性消融语义修正。这段演化史若写入 Discussion 的 Limitations 段落，可展示 benchmark 设计敏感性和方法论诚实性——Energies 蒸馏标准显示 "honest limitations sections correlate with acceptance"。

**Top fix**: (a) 按 JOURNAL_REVIEW.md §3.1 收敛所有 claim 措辞；(b) 按 MDPI 模板建立 IMRaD 结构；(c) 将 v1-v5 演化史转化为 Discussion 中的诚实局限段。

---

### 3.7 Ethics（伦理合规）

**Severity: 0 | Confidence: 0.90 | Fixability: 1.0**

**Findings:**

1. **[F-eth-1] MDPI 硬性声明为流程项** — Funding / COI / Data Availability / Author Contributions 是 Energies 100% 硬底线（蒸馏标准："100% hard floor"）。这些是投稿系统中的表单字段，撰稿时确保齐备即可，无技术障碍。

2. **[F-eth-2] SimBench 公开数据是伦理优势** — 不涉及保密/隐私/utility NDA。Data Availability Statement 可直接声明"SimBench 公开数据集 + 复现脚本存于 [repository]"。

3. **[F-eth-3] 无 AI 生成内容风险** — 论文为算法/实验类，不涉及人类受试者。但 ARA 工程为 AI-executed（`exploration_tree.yaml` provenance: ai-executed），MDPI 要求披露 AI 工具使用——需在 Methods 或 Acknowledgments 中说明 ARA 开发流程。

**Top fix**: 投稿前按 MDPI 清单逐项确认。在 Methods 中加一句 AI-assisted development 声明。

---

## 四、RRI（Rejection Risk Index）

| 维度 | Severity | Confidence | Weighted Risk |
|---|---|---|---|
| Novelty | 1 | 0.85 | 0.85 |
| Soundness | 3 | 0.90 | 2.70 |
| Experiments | 3 | 0.95 | 2.85 |
| Reproducibility | 1 | 0.80 | 0.80 |
| Related Work | 3 | 0.95 | 2.85 |
| Clarity | 2 | 0.85 | 1.70 |
| Ethics | 0 | 0.90 | 0.00 |
| **Total RRI** | | | **11.75 / 28** |

**RRI 解读**: 11.75/28 = 42% 风险指数。Energies 的 major-revision 门槛约 30-40%，desk-reject 门槛约 55-60%。当前状态处于 **major-revision 区间上沿**——三个 severity-3 维度（soundness、experiments、related_work）任何一个单独触发 major revision 的概率都很高，但尚不构成 desk-reject（因为 AC 验证已消解"unvalidated simulation"这一最致命的桌拒触发器）。

---

## 五、Predicted Decision

### 当前状态投稿 → **Major Revision（60%）/ Desk-Reject（25%）/ Minor Revision（15%）**

**理由**:
- **Major Revision 60%**: 灵敏度分析缺失是 Energies 蒸馏标准中最确定的 major-revision 触发项（"near-mandatory; its absence is the top major-revision trigger"）。文献综述空白、IEEE 33/69 标准算例缺失、strategy-adaptive 消融支撑薄弱，任一项都足以触发 major revision。
- **Desk-Reject 25%**: 若编辑在 pre-check 阶段发现文献综述实质空白 + claims 越界（"planning quality"/"electrical feasibility" 无充分支撑），可能以"incremental, unvalidated"为由桌拒。AC 验证的完成降低了这一风险，但 AC 验证显示方法无差异化可能引发新的质疑。
- **Minor Revision 15%**: 若遇到宽容审稿人（接受"narrow proxy-level gain + AC validation"的诚实框定），可能仅要求补灵敏度分析和文献综述。

### 修复 P0 后投稿 → **Minor Revision（55%）/ Accept（25%）/ Major Revision（20%）**

---

## 六、Top-3 Revisions（P0 级，投稿前必须完成）

### Revision 1: 灵敏度分析（预计 3-5 天）

**必要性**: Energies 蒸馏标准第一大 major-revision 触发项。Applied Sciences 蒸馏标准："sensitivity analysis is the journal's currency of applied credibility（present in 6/11）"。

**具体方案**:
- **参数 1**: 种群规模 ∈ {30, 50, 100, 150, 200}，记录 HV 收敛轨迹与最终 HV
- **参数 2**: 修复强度上限 ∈ {0.1, 0.2, 0.3, 0.5, 0.8}（最大修复比例）
- **参数 3**: 自适应触发阈值（多样性窗口/违约率阈值）∈ 3-5 个级别
- **参数 4**: DER 渗透率/负荷增长率（直接复用 AC 验证的 6 场景轴：base / peak 1.3x / growth 1.5x / extreme 1.8x / high-DER 2.5x / growth+N-1），形成场景维灵敏度

**证据路径**: 新增 `evidence/runs/sensitivity_analysis_*` + `evidence/tables/sensitivity_summary.csv`。

### Revision 2: IEEE 33-bus 标准算例（预计 2-3 天）

**必要性**: 配网 DER/储能规划文献的事实标准。JOURNAL_REVIEW.md §五："两刊同题论文几乎必备"。pandapower.networks 内置 case33bw，零下载成本。

**具体方案**:
- 安装 pandapower → `pnw.case33bw()` 构网 → 适配现有规划管线（DER 候选节点、储能候选节点、线路升级候选）
- 在 IEEE 33-bus 上运行 CARS-MODE + top-3 基线（NSGA-II、MOEA/D、GA）+ NoRepair 消融
- 报告代理 HV + AC 潮流验证指标（电压越限率、线路过载率、网损）
- 与已发表的同题 IEEE 33-bus 论文做横向比较（至少 2-3 篇参考值）

**证据路径**: 新增 `evidence/runs/ieee33bus_*` + `evidence/tables/ieee33bus_leaderboard.csv`。

### Revision 3: 文献综述实体化（预计 5-7 天）

**必要性**: Energies desk-reject trigger 包含 "inadequate literature review"。当前 `logic/related_work.md` 实质空白。

**具体方案**（30+ 篇，5 个板块）:
1. **配网扩展规划方法**（5-8 篇）: 经典 MILP/MINLP + 近 3 年元启发式（Energies/Access/AppliedSci 同题论文）
2. **DER 选址定容**（5-8 篇）: 含 PV/wind/储能，多目标优化，灵敏度分析范例
3. **MOEA 在电力系统规划中的应用**（5-8 篇）: NSGA-II/MOEA/D/SPEA2 在配网规划中的代表性应用
4. **自适应 DE 变体**（3-5 篇）: JADE (Qin & Suganthan 2009)、SaDE (Qin et al. 2009)、SHADE (Tanabe & Fukunaga 2013) 等经典文献
5. **约束处理技术**（2-3 篇）: repair operators、penalty functions、feasibility rules (Deb 2000) 在配网规划中的对比

**证据路径**: `logic/related_work.md` 扩展为完整文献综述文档。

---

## 七、Allowable Modifications（保留大方向的可修改范围）

在保持"多目标差分进化 + 配电网规划 + DER/储能"大方向不变的前提下，以下修改被允许且可加速投稿：

| 修改类型 | 允许范围 | 影响评估 |
|---|---|---|
| **算法** | 可将 CARS-MODE 简化为"constraint-repair DE"（去掉 strategy-adaptive 组件，因其证据薄弱），聚焦 repair 组件的强故事（21.5%→7.0% 违约率降低） | 降低 novelty severity 从 1→0，大幅降低 soundness severity |
| **数据集** | 可替换/增加 IEEE 33-bus 和 69-bus 作为主要/次要测试系统；SimBench 可保留为第三案例或 scalability 案例 | 直接解决 experiments F-exp-2 |
| **下游任务** | 可从"扩展规划 + DER 选址 + 储能配置"缩窄为"DER/储能选址定容"（去掉线路扩展），简化问题维度 | 使节点级 AC 优化更可行，消解 soundness F-sound-1 |
| **目标函数** | 可将代理 hypervolume 替换为 AC 潮流验证指标（电压偏差、网损、投资成本）作为主要评价指标 | 消解 soundness F-sound-2（1e-4s runtime 问题） |
| **框架定位** | 可将论文从"算法优越性"重新定位为"规划决策支持框架"，以 repair 机制 + 场景分析为核心贡献 | 降低 soundness/experiments 的要求阈值 |
| **投稿刊** | 可在 Energies ↔ Applied Sciences 间切换（同 MDPI 体系，材料可复用） | Applied Sciences 对经济效益要求更高但基线要求更松 |

**推荐修改路径**: 将算法简化为 CARS-DE（去掉 strategy-adaptive），将下游任务缩窄为 DER/储能选址定容（保留 IEEE 33/69-bus + SimBench），以 repair 机制为核心贡献 + AC 潮流验证为主要评价指标 + 场景轴作为灵敏度分析。这一路径可将修复周期从 5 周缩短到 3 周。

---

## 八、Honest Boundary（诚实边界）

1. **代理 hypervolume ≠ 规划质量 ≠ AC 可行性** — AC 验证已证明 CARS-MODE 的 AC 可行率与 NSGA-II/MOEA/D 完全同分（0.625），且低于 GA（0.639）和 NoDER 消融（0.667）。代理层面的 0.46% 增益未传导到工程可行性层面。任何"improves planning quality"的主张必须附带 AC 验证的诚实数据。

2. **Composition-level 映射 ≠ 节点级选址定容** — AC 验证的 mapping 假设（`evidence/runs/real_ac_validation_analysis.md`）明确承认"it is not a nodal siting/sizing study"，规划组合是按 action-kind counts 映射到具体网络的。这意味着不同方法可能在节点级产生完全不同的结果，但当前实验无法区分。

3. **v1-v5 的场景重设计存在 benchmark shopping 风险** — 从 v1 的 -13.55% 到 v5 的 +0.46%，经历了 4 轮场景/消融重设计。若不在文中诚实披露这一演化过程（含 v4 near-miss 中 NoDiversity 消融反超全方法 1.00%），审稿人若从 supplementary material 或 ARA 公开仓库中发现，将严重损害可信度。

4. **Strategy-adaptive 组件证据不足** — FixedDE 差距仅 0.19%，3 seeds 下无法统计区分。v4 历史中 NoDiversity 消融曾反超全方法。如果场景分解后仍无法展示 strategy-adaptive 的差异化作用，该组件不应作为核心创新点声称。

5. **所有数据集/期刊指标均为 2026-07 快照** — 投稿前需在官网复核 APC、IF/分区、Section 列表、Special Issue 开放状态。

6. **AI-executed provenance** — `exploration_tree.yaml` 记录所有节点为 `provenance: ai-executed`。MDPI 要求披露 AI 工具使用，且审稿人可能对 AI 生成的实验设计持更高怀疑——需要在 Methods 中详细说明人工监督和质量控制流程。

---

## 九、Fastest Path to Publication

### 路径 A: Energies 直投（修复 P0 后）— 预计 4-5 周

| 周次 | 行动 | 产出 |
|---|---|---|
| W1 | 灵敏度分析（参数 1-4）+ 补 IEEE 33-bus 算例 | `evidence/runs/sensitivity_*` + `evidence/runs/ieee33bus_*` |
| W2 | 文献综述撰写（30+ 篇）+ claims 措辞收敛 | `logic/related_work.md` 完整版 + 修正后 claims |
| W3 | 稿件撰写（IMRaD + MDPI 模板）+ 收敛曲线/箱线图 | 完整稿件草稿 |
| W4 | 内部审查 + 润色 + 投稿 | 投稿确认 |
| W5+ | 审稿周期（~16-17 天首决）+ 1-2 轮修改 | 预计 6-7 周见刊 |

### 路径 B: 简化重定位 + Applied Sciences — 预计 3-4 周（最快）

| 周次 | 行动 | 产出 |
|---|---|---|
| W1 | 算法简化为 CARS-DE（去 strategy-adaptive）+ 任务缩窄为 DER/储能选址定容 + IEEE 33-bus 算例 | 简化实验 + `evidence/runs/ieee33bus_*` |
| W2 | 灵敏度分析（场景轴 + 种群规模）+ 文献综述（20+ 篇即可）+ 经济效益估算 | 完整证据链 |
| W3 | 稿件撰写（Applied Sciences 模板，突出应用价值）+ 投稿 | 投稿确认 |
| W4+ | 审稿周期（~15-16 天首决）+ 修改 | 预计 5-6 周见刊 |

### 路径 C: 最激进简化 + Energies — 预计 3 周

将论文重新定位为 **"Constraint-Aware Repair for DER/Storage Planning: A Scenario-Sensitivity Study on IEEE 33/69-bus"**：
- 核心贡献: repair 机制（21.5%→7.0% 违约率）+ 场景灵敏度分析
- 不做方法间横向比较（Energies 蒸馏标准：external baselines appear in only ~half of accepted papers）
- 以 IEEE 33-bus + 69-bus 为主案例，SimBench 为 scalability 案例
- AC 潮流验证为主要评价指标
- 3-5 参数灵敏度分析作为核心实验证据

**推荐**: 路径 B 或 C（取决于是否愿意放弃 strategy-adaptive 组件）。路径 A 更稳健但耗时更长。

---

## 附录：证据路径索引

| 证据 | 路径 |
|---|---|
| v5 主实验结果 | `evidence/tables/real_simbench_planning_leaderboard.csv` |
| v5 分析 | `evidence/runs/real_simbench_planning_analysis.md` |
| AC 验证结果 | `evidence/tables/real_ac_validation_summary.csv` |
| AC 验证分析 | `evidence/runs/real_ac_validation_analysis.md` |
| v1 weak | `evidence/runs/real_simbench_planning_analysis_v1_weak.md` |
| v2 weak | `evidence/runs/real_simbench_planning_analysis_v2_weak.md` |
| v3 weak | `evidence/runs/real_simbench_planning_analysis_v3_weak.md` |
| v4 near-miss | `evidence/runs/real_simbench_planning_analysis_v4_near_miss.md` |
| SimBench 源数据画像 | `evidence/source/real_simbench_planning_source_profile.csv` |
| Claims | `logic/claims.md` |
| 实验设计 | `logic/experiments.md` |
| 方法描述 | `logic/solution/method.md` |
| 文献综述 | `logic/related_work.md` |
| 探索树 | `trace/exploration_tree.yaml` |
| 环境说明 | `src/environment.md` |
| JOURNAL_REVIEW 差距评估 | `mintou_p3_samode_distribution_planning/JOURNAL_REVIEW.md` |
