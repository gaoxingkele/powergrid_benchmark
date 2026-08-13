# mintou_p3 (CARS-MODE) 投稿差距评估与修改完善方案

评估日期：2026-07-13
评估基准：`Paper_CCF` 期刊画像中的 "Distilled review standards"（IEEE Access：4 篇电力/负荷全文 + 10 篇摘要蒸馏；Energies：34 篇电力系统全文蒸馏，2023–2026）
证据来源：ARA 工程 `papers\mintou\mintou_p3_samode_distribution_planning\`（含 v1–v5 全部保留证据）

---

## 一、论文概况

CARS-MODE（Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution）面向配电网扩展、DER 选址定容与储能配置的多目标规划问题，创新点为约束感知修复算子 + 由多样性/违约信号驱动的策略自适应。当前证据为 SimBench `1-complete_data-mixed-all-0-sw`（18 个子网、72 个候选动作）派生的 DER/storage stress v5 基准：CARS-MODE 平均 proxy hypervolume 0.55322842，**仅超最强基线 NSGA-II 0.46%、超最强消融 FixedDE 0.19%**，且经历了 v1/v2（-13.55%）、v3（-3.11%）两轮 weak 与 v4 near-miss（超基线 0.48% 但输给 NoDiversity 消融 1.00%）才在场景重设计后转正。核心局限：hypervolume 是**代理指标而非 AC 潮流验证的电气可行性**（pandapower 未安装，`src\environment.md` 明确记录），平均约束违约率仍有 7.04%，每方法仅 7 场景 × 3 重复 = 21 次运行，无统计显著性检验、无收敛曲线、无灵敏度分析。ARA 自身的 claims.md 也明确承认"narrow proxy-level positive signal"。

---

## 二、期刊匹配度对比

### IEEE Access — Fit: **Low**（当前状态）→ 修完统计协议后至多 Medium

| 维度 | 评估 |
|---|---|
| 范围 | 通过。power & energy 是 Access 最大板块之一 |
| soundness 标准 | **不通过**。Access 蒸馏结论明确：**元启发式论文的社区惯例是 50+ 独立 runs + Wilcoxon/Friedman + 收敛曲线/箱线图**。本论文每方法仅 3 seeds × 7 场景 = 21 runs，零显著性检验，`evidence\figures\` 目前只有 README 占位，无任何收敛/箱线图 |
| 增益说服力 | 0.46%/0.19% 的微弱增益在无统计检验支撑下，元启发式审稿人几乎必然质疑"随机波动"。3 个 seed 连 Wilcoxon 检验都无法做 |
| 决策模式风险 | Access 是**二元 accept/reject、仅允许一次重投**——不适合"边审边补"的半成品；当前状态投递大概率消耗掉唯一的重投机会 |
| 其他红线 | mean_runtime_s ≈ 1e-4 秒会暴露目标函数是廉价代理，触发"proxy dataset–task mismatch"这一 Access 蒸馏出的已知滑漏项，被认真审稿人抓住即拒 |

**理由汇总**：Access 不卡 novelty，但对元启发式这一具体社区的统计学惯例要求恰好是本论文最薄弱处。当前证据链投 Access 属于撞枪口。

### MDPI Energies — Fit: **Medium**（补齐 AC 验证 + 灵敏度分析后可达 High）

| 维度 | 评估 |
|---|---|
| 范围 | 通过。配电网规划 + DER/储能是 Energies 电力系统板块核心题材，可路由到 electrical power & energy systems 或 smart grids Section |
| novelty 门槛 | 通过。蒸馏结论：31 篇研究论文**零篇提出全新算法**，可命名的机制组合 + gap 陈述即够；**≤5% 的改进只要诚实报告就能过**——0.46% 诚实框定为 narrow gain 是可行的 |
| 实验门槛 | **部分通过**。蒸馏结论：≥1 个可识别 test case + scenario/scheme 自比较 + **灵敏度分析（近强制，缺失是第一大 major-revision 触发项）**。本论文有 7 场景自比较（规划类论文靠 scenario self-comparison 即可过关，外部基线只出现在约半数录用论文中——本文反而已有 6 个外部基线，超配）；但**灵敏度分析完全缺失**——这是 Energies 侧最确定的一刀 |
| 统计检验 | 不构成障碍。蒸馏结论：0/29 录用论文做显著性检验，无 30-run 协议要求——本论文 3 seeds 在 Energies 不是硬伤 |
| 验证底线 | **风险项**。"incremental, unvalidated simulation" 是 Energies desk-reject 触发器；proxy hypervolume 无 AC 潮流验证接近这条线，需要 pandapower 潮流校验把 simulation 变成 validated |
| 强制声明 | Funding / COI / Data Availability / Author Contributions 100% 硬底线，撰稿时必须齐备 |

### 最终推荐

**首选 MDPI Energies**（维持 ARA 原定目标），备选 Applied Sciences。不推荐现状投 IEEE Access：其元启发式统计协议缺口（50+ runs、Wilcoxon、收敛图）比 Energies 的缺口（灵敏度分析、AC 验证）修复成本高得多，且二元决策模式对 0.46% 级微弱增益极不友好。若未来补齐 30–50 runs + 统计检验，Access 可作为 Applied Sciences 之后的第三顺位。

---

## 三、写作修改清单（对照期刊惯例 + claims 越界审计）

### 3.1 超出证据边界的主张（必须收敛措辞）

| 位置 | 现有主张 | 问题 | 修改方向 |
|---|---|---|---|
| `logic\claims.md` C1 | "improves DER/storage **planning quality**" | 证据只是 proxy hypervolume，**proxy hypervolume ≠ 规划质量 ≠ AC 可行性** | 改为 "improves the proxy hypervolume indicator on a SimBench-derived planning benchmark" |
| `logic\claims.md` C3 | "remains **feasible or robust** under DER/storage stress" | 平均约束违约率 7.04%，且无任何潮流计算；"feasible" 未被建立 | 改为 "achieves lower constraint-violation-rate than non-repair variants"（NoRepair 为 21.5%，这才是有证据的对比） |
| `logic\solution\method.md` 创新点 3 | "Reports Pareto quality **and electrical feasibility** together" | electrical feasibility 从未经潮流计算 | 在补 pandapower 验证前删除 "electrical"，或如实改为 "proxy feasibility indicators" |
| `PAPER.md` 标题 | "…for **Reproducible Distribution Network Planning**…" | 可保留，但摘要/结论不得暗示工程级规划结论 | 摘要中显式写 "proxy-level benchmark evidence; AC feasibility validation reported in Section X"（补验证后） |

### 3.2 对照 Energies 惯例的写作项

1. **诚实报告微弱增益**：0.46%/0.19% 直接写数字，不做百分比通胀（Energies 蒸馏已点名 "inflated percentages on self-defined metrics" 是滑漏项，主动规避是加分）。
2. **hybrid 组件逐一 justification**：蒸馏点名 "hybrid algorithms with no per-component justification" 是录用论文的常见滑漏——审稿人若较真即中招。CARS-MODE 两个组件的证据现状：
   - **constraint-aware repair**：有强故事——NoRepair 消融 HV 掉至 0.54142 且违约率 21.5% vs 7.0%，正文应把这一对比放大为核心论据；
   - **strategy adaptation**：证据薄——FixedDE 差距仅 0.19%，且 v4 历史中 NoDiversity 消融曾反超全方法 1.00%。正文需按场景分解展示自适应在哪类场景（如 constraint_repair、load_growth）起作用，否则该组件的存在性论证不成立。
3. **test case 明确化**：Energies 要求"可识别的 test case"。SimBench `1-complete_data-mixed-all-0-sw`、18 子网清单、72 候选、总负荷 71.3 GW、RES 12.2 GW（`evidence\source\real_simbench_planning_source_profile.csv`）需完整写入 Case Study 小节并给出网络示意图。
4. **负面证据转化为叙事资产**：v1–v4 的保留证据（weak → near-miss → 场景重设计后转正）可写入 Discussion 作为 benchmark 设计敏感性的诚实讨论，同时必须说明 v4→v5 的场景重设计逻辑，否则有"为方法定制基准"（benchmark shopping）之嫌。
5. **MDPI 硬性件**：MDPI 模板、IMRaD、~200 词摘要、3–8 关键词、编号引用；Data Availability（SimBench 公开数据是优势，给出仓库/脚本路径）、CRediT、Funding、COI 全齐；自引克制；文献综述需覆盖近 3 年 Energies/AS 同题配电规划论文（`logic\related_work.md` 目前仅一行指针，撰稿量最大的空白）。
6. **贡献列表**：3–5 条编号贡献（两刊共同惯例），每条对应一个有证据的 claim，不写 "first time in literature" 式无证据措辞。

---

## 四、实验设计缺口

### 4.1 IEEE Access 侧（元启发式社区惯例）— 当前**全部不满足**

| 惯例要求 | 现状 | 缺口 |
|---|---|---|
| 50+（至少 30）独立 runs / 实例 | 3 repeats × 7 场景（`repeats: 3`，leaderboard runs=21） | 需 30–50 seeds/场景，代理目标函数极快（1e-4 s/评估），计算上完全可行 |
| Wilcoxon 秩和 / Friedman 检验 | 零 | 增至 30+ runs 后按场景做 CARS-MODE vs 各基线 Wilcoxon + 全方法 Friedman |
| 收敛曲线 | 无（figures 目录仅 README） | 记录每代 HV 轨迹并绘制 |
| 箱线图 | 无 | 各方法 HV 分布箱线图 |

### 4.2 MDPI Energies 侧

| 要求 | 现状 | 缺口 |
|---|---|---|
| **灵敏度分析（近强制）** | 完全缺失 | 至少 3–4 个参数扫描：种群规模、修复强度上限、自适应触发阈值、场景数（low_scenario_count 消融可升级为灵敏度维度）、目标权重/参考点 |
| 可识别 test case | SimBench 派生但描述散落在 CSV | 正文 Case Study 小节 + 网络图 + 候选动作表 |
| 验证（非 unvalidated simulation） | proxy 指标，无潮流 | **pandapower AC 潮流验证**（见 4.3） |
| 场景自比较 | 已有 7 场景 ✓ | 达标 |

### 4.3 两刊共同缺口：AC/pandapower 可行性验证（最高优先）

`src\environment.md` 明确 pandapower 未安装。最小闭环：安装 pandapower → 用本地 SimBench 缓存构网 → 对 CARS-MODE 与 top-2 基线的最终 Pareto 前沿解逐一跑 AC 潮流 → 报告电压越限率、线路过载率、网损，替换/支撑 C3。这一步同时消解 Access 的 "proxy mismatch" 风险和 Energies 的 "unvalidated simulation" 风险。

### 4.4 消融完整性缺口

`logic\experiments.md` 规划了 **8 个消融**，但 v5 leaderboard 只有 **4 个**（NoRepair、FixedDE、NoDiversity、NoDER）。缺失：`no_strategy_adaptation`（与 FixedDE 是否同一概念需澄清，若不同必须补跑——这是 strategy-adaptive 组件的直接消融）、`no_storage_candidates`、`weighted_sum_only`（现以基线 "Weighted Sum" 形式存在，角色需在文中说清）、`low_scenario_count`。**两个核心组件的 per-component 支撑现状：repair 有强消融证据（违约率 21.5%→7.0%）；strategy-adaptive 仅 0.19% 差距，在 3 seeds 下不构成支撑，必须靠多 seed + 统计检验或场景分解补强，否则建议在贡献表述中降级。**

### 4.5 其他

- runtime_scalability 场景与 1e-4 s 的运行时间自相矛盾——代理评估下"可扩展性"结论无意义，需在真实潮流评估下重做或删除该 claim。
- investment_cost_index 为自定义指标，需给出货币化标定或明确声明为无量纲指数（P5/P6 同款问题，portfolio_status.md 已记录 "calibrated investment assumptions" 待办）。

---

## 五、数据集缺口

| 数据集 | 文献地位 | 本地缓存 | 行动 |
|---|---|---|---|
| SimBench | 欧系基准，Energies 可接受但非配网规划文献主流 | ✓ 已缓存（`data/public_datasets/grid_cases/simbench/`） | 保留为主案例 |
| **IEEE 33-bus** | 配网 DER/储能规划**事实标准**，两刊同题论文几乎必备 | 间接可得：`matpower`（case33bw）与 `pandapower` 包源码已缓存（CACHE_STATUS.md "Downloaded"），pandapower.networks 内置 case33bw | **P0 补做**：安装 pandapower 后零下载成本 |
| **IEEE 69-bus** | 同上，第二常用 | 同上（case69 内置） | P1 补做，形成 33/69 双标准案例 |
| IEEE 118-bus（配网变体 / case118zh） | 大规模可扩展性展示用 | matpower/pandapower 缓存内含 | P2 可选，仅当保留 runtime_scalability claim 时需要 |
| PGLib-OPF / TAMU cases | 输电侧，非本文任务 | pglib 已缓存 / tamu metadata-only | 不需要 |

结论：**无需任何新下载**。加 IEEE 33（最好加 69）标准算例可直接对齐两刊文献惯例，并使结果可与已发表论文横向比较——这也部分弥补"单一 test system"的普遍性质疑（虽然 Energies 蒸馏显示约 2/3 录用论文仅单一系统，多一个是加分而非硬性）。

---

## 六、优先级行动清单

### P0（不做即有 desk-reject / major-reject 风险，投 Energies 前必须完成）

1. **pandapower AC 潮流验证**：安装 pandapower，对最终 Pareto 解做潮流校验，报告电压/载流可行性——消解 "unvalidated simulation" 红线（预计 1–2 天，数据全部本地）。
2. **claims 措辞收敛**：按 3.1 修改 C1/C3 与 method.md 创新点 3，全文杜绝 proxy hypervolume → 规划质量/电气可行性的越界推断。
3. **灵敏度分析**：≥3 参数扫描 + 结果表/图——Energies 第一大 major-revision 触发项。
4. **IEEE 33-bus 标准算例**：作为第二 test case 接入现有管线。

### P1（显著降低 major revision 概率）

5. **seeds 3 → 30**（代理评估成本近零；若未来转投 Access 则升至 50 并加 Wilcoxon/Friedman）。
6. **补齐缺失消融**：明确 FixedDE 与 no_strategy_adaptation 的关系，补 no_storage_candidates / low_scenario_count；用场景分解补强 strategy-adaptive 组件的 0.19% 弱证据。
7. **收敛曲线 + 箱线图**：填充空的 `evidence\figures\`（Energies 非强制但普遍存在，Access 强制）。
8. **文献综述实体化**：related_work.md 目前仅一行指针，需覆盖近 3 年同题 Energies/AS/Access 论文 30+ 篇。

### P2（打磨与保险）

9. IEEE 69-bus 第三案例；investment_cost_index 货币化标定。
10. v1–v4 演化史写入 Discussion 的诚实局限段 + benchmark 重设计说明。
11. MDPI 模板、Data Availability/CRediT/Funding/COI 四声明、英文润色、图表规范。
12. 若 Energies 被拒：Applied Sciences 直投（同 MDPI 体系，材料可复用）；IEEE Access 仅在完成 P1-5 统计协议升级后作为第三顺位。

---

### 附：期刊画像输出格式速览

```text
[Target] Energies (MDPI)
[Fit] Medium（能源相关性强 + 规划类实验模式匹配；被 proxy 验证缺口和灵敏度分析缺失压制）
[Contribution type] modeling / 算法改进型规划方法
[Main evidence gap] AC 潮流可行性验证；灵敏度分析；strategy-adaptive 组件消融支撑
[Top rejection risk] validation（unvalidated proxy simulation）
[Re-route suggestion] Applied Sciences（备选）；IEEE Access 需先补 50-run 统计协议

[Target] IEEE Access
[Fit] Low（soundness 达标线未过：元启发式社区惯例 50+ runs + Wilcoxon/Friedman + 收敛/箱线图全缺）
[Top rejection risk] rigor（0.46% 增益无统计支撑 + proxy–task mismatch）
```

---

## 进展更新（2026-07-13）

**P0-1（AC/pandapower 可行性验证）已完成**：新增 `src/powergrid_benchmark/mintou_pandapower_validation.py`，在 4 个真实 SimBench MV 网络（rural/semiurb/urban/comm）× 6 个压力场景（base / peak 1.3x / growth 1.5x / extreme 1.8x / high-DER 2.5x / growth+N-1）上对全部 12 个方法的规划构成做 AC 潮流校验，证据见 `papers/mintou/mintou_p3_samode_distribution_planning/evidence/runs/real_ac_validation_*` 与 `tables/real_ac_validation_summary.csv`。

结果（如实）：所有规划方案的 AC 可行率均优于 No-Plan（0.625 vs 0.500，压力场景 0.550 vs 0.400），电压裕度与线路载流显著改善；**但在构成粒度上 CARS-MODE 与 NSGA-II/MOEA/D 完全同分，GA（0.639）与 NoDER 消融（0.667）反而更高**——DER 重的方案在高 DER 场景有过电压代价。含义：AC 校验解决了 "unvalidated simulation" 桌拒红线，但不能作为 CARS-MODE 的差异化证据；场景轴（负荷增长/DER 渗透）可作为敏感性分析小节的骨架。**剩余关键缺口：将规划管线的代理方法替换为真实 MOEA 实现（同 p5/p6 的 v2 重写模式）+ 节点级选址定容实验以产生方法差异化。**

## 第二次进展更新（2026-07-13 下午）

**规划管线真实 MOEA 重写已完成**（`mintou_real_planning.py` v6，代理版产物保留为 `*_proxy_methods_deprecated.*`）：

- CARS-MODE 为真实二进制 MODE：jDE 自适应 F/CR + SaDE 双策略池（成功率驱动）+ 约束修复 + 拥挤度多样性；消融为单一机制开关。基线：pymoo NSGA-II / MOEA/D + 真实标量化 DE/PSO/GA + 加权和贪心。评价方法无关（标准 HV，固定归一化边界），30 seeds + Mann-Whitney/Holm（`tables/real_simbench_planning_significance.csv`）。
- **主结果**：CARS-MODE 平均 HV 比 NSGA-II 高 **6.34%**（v1 代理版只有 0.46%），42/42 基线对比全部 Holm 显著——统计协议现在同时满足 Energies 与 Access 的元启发式底线。
- **组件级发现（如实写）**：FixedDE 消融在代理 HV 上微超完整方法 0.60%（2 组显著）——策略自适应在 HV 上是轻微负贡献；但 AC 校验 v2 中 FixedDE 掉到 0.569 而 CARS-MODE 0.611——策略自适应在电气可行性上是正贡献。这个"HV-AC 权衡"是论文的诚实叙事素材。
- **重要方法学修正**：v1 的电压/托管"约束"在预算内不可满足（v1 用软惩罚静默掩盖）；v2 以预算为唯一硬约束，规划目标缺口降为描述性指标。
- AC 校验已用新方案构成重跑（v1 结果保留为 `*_v1_proxy_plans.*`）。

**剩余缺口**：节点级选址定容实验（AC 层差异化）、成本货币化标定、related_work 实体化、收敛曲线/箱线图。
