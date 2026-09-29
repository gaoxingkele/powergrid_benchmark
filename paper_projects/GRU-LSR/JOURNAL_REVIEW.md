# mintou_p1 (DSTAR-GRU) 投稿评审与修改完善方案

评审基准: `Paper_CCF` 期刊画像（IEEE Access / MDPI Energies 的 Distilled review standards）
ARA 证据源: `papers/mintou/mintou_p1_dstar_gru_dispatch`（evidence 版本 v1_weak → v2_marginal → v3）
日期: 2026-07-13

---

## 1. 论文概况

DSTAR-GRU（Digital-twin Siamese Temporal Alignment and Retrieval GRU）面向"相似度感知的负荷/拓扑约束调度推荐"，在公开 RTS-GMLC 基准派生的调度代理实验（v3, fixed + rolling + stress-subset）上给出当前证据信号：固定切分综合调度得分 `0.73965420`，相对最强基线 Renewable-First ED（`0.74024403`）增益仅 **0.08%**，相对最强消融 0.36%；rolling（仅 3 个窗口）增益 **0.07%** 且均值标准差 `0.0548` 比增益本身大近两个数量级；唯一较亮的信号是高新能源压力子集增益 **0.72%**（对最强消融 3.08%）；而 high_topology 与 ramp_stress 子集为 **0.00% 平局**。ARA 自身如实记录了 v1 为负增益（-0.12%）、v2 仅 0.01%、且"这只是标准库 RTS-GMLC 调度代理，不是 AC-OPF 或机组组合证明"。总体判断：工程链路完整、证据链诚实，但**主信号处于噪声量级，且核心可行性验证（OPF/UC）缺位**，现状不足以通过任一目标期刊的实验底线。

## 2. 期刊匹配度对比

### IEEE Access

```text
[Target] IEEE Access
[Fit] Medium（scope 完全契合 power & energy + AI；但 soundness 是唯一闸门，
      0.08% 主增益无统计检验、无 OPF/UC 可行性验证，按"claims 必须被 baselines/validation
      充分支撑"的标准现状过不了二元 Accept/Reject 闸门）
[Contribution type] method / application（组件组合 + 场景适配，正符合 Access 已发表论文形态）
[Soundness gaps] OPF/UC 可行性验证缺失（opf_transfer 槽位"planned 未做"）；主增益 0.08%
      在 rolling std 0.0548 面前统计不可区分；消融仅 smoke-tested；manifest 声称的
      8 个基线（DC OPF/AC OPF/GRU/LSTM/CNN-LSTM/Grid2Op Rule/PSO/GA）与实跑
      leaderboard 中的 Renewable-First ED 等不一致
[Official items to re-check] APC ≈ US$2,160 / 模板 / 一次重投限制
[Top rejection risk] rigor —— "insufficient rigor: weak experiments, unsupported claims"
[Re-route suggestion] 若补齐 OPF 验证后信号仍弱 → Electronics（备选刊）或降级为
      benchmark/framework 型论文框架
```

要点：Access 的 distilled standards 显示 DL 类可以 4–6 baselines、零显著性检验过审，**但那些论文的增益不是 0.08% 量级**；二元决策模型没有 major revision 救援轮，"补实验再审"不存在——必须投前把 soundness 补到位。Access 明确容忍 incremental，"incremental 且未严格验证"才致命——本文当前恰好落在致命象限。

### MDPI Energies

```text
[Target] Energies (MDPI)
[Fit] Medium-High（能源相关性无可挑剔：调度/新能源消纳/电网；Energies distilled
      标准明确"≤5% 改进只要诚实报告即可过"、31 篇 0 篇提出全新算法、0/29 要求统计
      检验——对本文的微弱但诚实的信号容忍度显著更高；扣分项是 sensitivity analysis
      缺失，这是该刊 top major-revision trigger）
[Contribution type] modeling / system（机制组合 + gap statement，符合该刊新颖性地板）
[Main evidence gap] sensitivity analysis（自定义 composite_dispatch_score 的权重敏感性
      尤其必须做——"self-defined metrics"是该刊已发表论文被点名的自查项）；
      OPF 可行性验证（"unvalidated simulation"是桌拒触发器）
[Official items to re-check] APC ≈ CHF 2,600 / Section（Electrical Power & Energy
      Systems 或 Smart Grids）/ 是否有匹配 Special Issue / Data Availability 模板
[Top rejection risk] validation —— 不做敏感性分析 + 纯代理仿真无可行性校验
[Re-route suggestion] Applied Sciences / Electronics（MDPI 姊妹刊）
```

### 推荐

**近期投稿推荐 MDPI Energies**；完成 P0 全部动作后 IEEE Access 才值得投（也符合原定目标）。理由：
1. Energies 有 1–2 轮修改机会，sensitivity analysis 缺失通常触发 major revision 而非拒稿；Access 是二元决策 + 仅一次重投，以当前 0.08% 噪声级主证据去赌二元闸门风险过高。
2. Energies 对 ≤5% 的诚实微弱改进、单测试系统、无统计检验、场景自比较均有已发表先例（34 篇 distilled 语料）；Access 虽不查统计检验，但 reviewer lens 是"claims 是否被证据支撑"，0.08% 主张在 3 窗口 std=0.0548 下无法自洽。
3. 本文能源应用叙事（新能源压力下的调度推荐、消纳、备用）在 Energies 是加分主线，在 Access 只是背景。
若坚持 IEEE Access：必须先完成 OPF/UC 验证 + 多次重复运行统计 + 把主打主张换成高新能源压力子集（0.72%/3.08%），否则最高风险即"rigor 拒稿且一次重投机会被浪费"。

## 3. 写作修改清单

### 两刊通用（源自 ARA 薄弱点）

- **related_work.md 是空壳**：仅一行指向 `papers/literature/target_journal_related/comparison_analysis.md`。两刊都要求"adequate, current literature review"（Energies 桌拒触发器之一；Access 需要 gap→contribution 完整叙事链）。必须写成真正的综述：相似检索/度量学习在电力系统的应用、数字孪生调度、learning-assisted OPF/ED 三条线，并落到一句可命名的 gap statement。
- **problem.md 的 gap 陈述过于泛化**（"must prove incremental value through stronger baseline coverage"是工程指令不是科学 gap）。需改写为：现有调度学习方法不利用历史运行状态相似性 / 不显式建模拓扑不确定性 → 本文填补。
- **命名与证据矛盾**：标题含 "Topology Uncertainty"、方法名含 topology-aware，但 high_topology 压力子集增益 0.00%（与最强基线、消融全平）。评审必然攻击。要么补 Grid2Op 拓扑实验，要么弱化标题/主张中的 topology 承诺，把 claims C3 的表述与 stress 证据对齐。
- **主张重心重排**：Abstract/Introduction 主打高新能源压力子集（0.72% over baseline、3.08% over ablation），把 overall 0.08% 作为"整体不劣化 + 压力场景显著获益"的诚实框架，而不是把 0.08% 当主卖点。
- **自定义 composite_dispatch_score 需正当化**：给出各分量（cost/violation/curtailment/topology risk/runtime）权重的依据 + 权重敏感性（见实验清单），否则触发"inflated percentages on self-defined metrics"自查项。
- **超参数披露**：Access distilled 语料点名"near-zero hyperparameter disclosure"是已发表论文的滑漏项——反向利用它，完整给出检索库规模、相似度阈值、GRU 结构、训练设置表。
- **Limitations 段落**：ARA 已诚实记录 proxy 边界（非 AC-OPF/UC），manuscript 必须保留这段诚实性——Access 明确把 honest limitations 视为加分。
- **结论不许外推**：不要写"可推广到其他电网/其他领域"这类 evidence-free generalization（Access 语料点名的滑漏项）。

### IEEE Access 专项

- **Numbered contribution list（3–6 条）是近刚性惯例**：按"组合式创新 + 场景适配"framing 写 3–4 条，围绕 rigor/validation 而非 novelty 措辞。
- **Fairness statement**：统一算力预算 / 参数量对齐声明在 2/4 语料论文出现且读作加分——DSTAR-GRU vs 各 DL 基线的参数量与训练预算对齐要写明。
- 使用 **IEEE Access 专用模板**（非 Transactions 模板），建议 <20 页；ORCID；英文清晰度是显式录用标准。
- 时间序列切分声明：本文用 rolling window（好），明确写出无随机 90/10 泄漏切分。

### MDPI Energies 专项

- **IMRaD 结构 + MDPI 模板**，摘要 ~200 词、3–8 个关键词、MDPI 编号引用格式。
- **硬性声明四件套 100% 必备**：Data Availability（RTS-GMLC 公开数据是现成优势，写明来源与获取方式）、Author Contributions（CRediT）、Funding、Conflicts of Interest。
- 能源应用先行：Introduction 首段即讲新能源消纳/调度可行性的能源系统问题，不要写成"通用方法论文 + 电力案例"。
- 自引克制、参考文献新近（近 3–5 年占比要够）。
- 选对 Section（Electrical Power and Energy Systems / Smart Grids），并核查是否有合适 Special Issue。

## 4. 实验设计缺口

对照两刊 distilled 实验底线逐条判断：

| # | 缺口 | 证据事实 | 对照标准 | 结论 |
|---|---|---|---|---|
| 1 | **OPF/UC 可行性验证缺失** | `experiments.md` 中 `opf_transfer` 槽位状态 "Not yet available / planned"；三份 analysis 均写明 "does not prove AC feasibility or production-cost optimality" | Energies: "unvalidated simulation" 是桌拒触发器；Access: claims 必须被 validation 支撑 | claims C3（压力下保持可行）**站不住**，必须补 PGLib/MATPOWER DC-OPF 校验层 |
| 2 | **主增益统计不可区分** | fixed 0.08%；rolling 0.07% 且仅 3 窗口、std `0.0548`（增益绝对值 `0.0006` 的 ~90 倍）；v1 曾为 -0.12%、v2 仅 0.01% | Access DL 惯例虽无统计检验，但增益需肉眼可辨；元启发式惯例 50+ runs + Wilcoxon | claims C1 以 overall 数字表述**站不住**；需多种子重复运行（≥10–30）+ 配对检验（Wilcoxon）+ 扩窗口（≥10 rolling windows），或把主张收缩到高新能源子集 |
| 3 | **敏感性分析缺失** | evidence/ 中无任何参数扫描表 | Energies: sensitivity analysis 近强制，缺失是 top major-revision trigger | 必补：composite score 权重、检索库规模（已有 `small_reference_bank` 消融雏形）、相似度阈值三维扫描 |
| 4 | **消融状态标签与实跑脱节**（2026-07-14 更正：经第三方审稿核查，fixed/stress leaderboard 实际已含全部 6 个消融的 RTS 实跑结果；本表原表述"stress 表只出现 2 个消融"有误） | `experiments.md` 6 项消融仍标 "smoke-tested"，与 RTS 实跑证据不符 | 两刊都要求声称-证据一致 | 更新 `experiments.md` 状态标签即可，无需重跑（从实验缺口降为文档修订） |
| 5 | **基线名单不一致** | `method.md` 声称 8 基线（DC OPF、AC OPF、GRU、LSTM、CNN-LSTM、Grid2Op Rule、PSO、GA），但 RTS leaderboard 最强基线是 Renewable-First ED——manifest 与实跑不符 | Access DL 惯例 4–6 个真实跑通的基线；声称而未跑等于 unsupported claim | 在 RTS 上至少实跑 GRU/LSTM/CNN-LSTM 三个 DL 基线 + DC-OPF + 规则型 ED，统一表格 |
| 6 | **单测试系统** | 仅 RTS-GMLC | Energies 单系统是常态（~2/3）可接受；Access 无硬性要求但第二系统显著加固 | P1 级：加 NREL-118（本地已缓存）做泛化 |
| 7 | **拓扑主张无实验** | `topology_disturbance` 槽位标 "proxy tie/limitation"；high_topology 子集 0.00% | 标题承诺 Topology Uncertainty | 要么补 Grid2Op 拓扑扰动实验（数据已缓存），要么删弱主张 |
| 8 | **公平性/运行时报告** | runtime_s 已在指标列表、`scalability_runtime` 有 source profile | Access 加分项 | 补齐参数量/算力预算对齐声明即可 |

## 5. 数据集缺口

- **已使用**：RTS-GMLC（`gen.csv`、`branch.csv`、日前负荷/风/光时序）——本地 `data/public_datasets/grid_cases/rts_gmlc` 已缓存。
- **声称使用但尚未进入证据链**（problem.md 列了 5 个数据集，实跑只用 1 个）：
  - `pglib_opf`、`matpower` —— **已缓存**，是 P0 的 DC-OPF 可行性校验层所需，零下载成本；
  - `grid2op_datasets` —— **已缓存**，是修复 topology 平局所需的拓扑扰动实验环境；
  - `opsd_time_series` —— **已缓存**，但与本文调度任务关联弱，建议从 problem.md 数据集列表中删除或明确其用途，避免"声称未用"被质疑。
- **已为 p1 专门缓存但未使用**：`nrel118`（2026-07-12 缓存，NREL-Sienna 官方仓库）——第二测试系统的现成材料。
- **结论：不存在数据下载缺口，全部所需公开数据本地已就绪；缺口在"缓存了但没用进实验"。** 唯一潜在软件缺口是 OPF 求解依赖（pandapower/PYPOWER，environment.md 已预告"future runs may require pandapower"，pandapower 数据也已缓存）。

## 6. 优先级行动清单

### P0（不做则两刊都过不了）

1. **补 DC-OPF 可行性验证层**（PGLib/MATPOWER + pandapower，数据已缓存）：这是 ARA 自己反复记录的边界（"Manuscript-level claims require OPF/UC solver validation"），也是 Energies "unvalidated simulation" 桌拒线和 Access soundness 闸门的共同要害。
2. **多种子重复运行 + 统计检验 + 扩 rolling 窗口**：0.08% 增益在 3 窗口 std 0.0548 下是噪声，任何一个认真的评审都能一眼看穿；≥10 种子 + Wilcoxon 配对检验 + ≥10 窗口，才能让"整体不劣化"这句话成立。
3. **主张重构**：主卖点改为高新能源压力子集（0.72%/3.08%），overall 结果改述为"不劣化"；同步修正标题/claims 中与 high_topology 0.00% 平局矛盾的 topology 承诺。
4. **在 RTS-GMLC 上实跑全部消融与 manifest 声称的基线**：消融目前只有 smoke 证据（constraints.md 明令不得用于 manuscript），基线名单与实跑不符——这是最容易被抓的"声称-证据不一致"。

### P1（应该做，直接对应两刊 distilled 惯例）

5. **敏感性分析**（composite 权重 / 检索库规模 / 相似度阈值）：Energies 缺它就是 major revision，Access 也能借它正当化自定义指标。
6. **NREL-118 第二测试系统**（已缓存）：破解单系统质疑，成本低。
7. **Grid2Op 拓扑扰动实验**（已缓存）：把标题里的 "Topology Uncertainty" 变成有证据的主张。
8. **重写 related_work.md 为真实综述 + 精确 gap statement**：现为一行空壳，是写作侧最大硬伤。
9. **写作合规包**：Access 的 numbered contributions（3–6 条）+ fairness statement + 超参数表；Energies 的 IMRaD + 四件套声明 + ~200 词摘要。

### P2（加分项）

10. **开源代码仓库**：Access reproducibility initiative 显式加分（虽然语料显示 0/4 已发表论文开源，做了即差异化优势），且本文已具备 `run_real_rts_dispatch.py` + config 的可复现基础。
11. **UC（机组组合）层验证**：把 proxy 升级为 production-grade 主张，为将来冲更高选择性期刊（TPWRS 等）留路。
12. **Graphical abstract**（Access 支持）+ 预印本（MDPI 允许且鼓励）。

---

## 最高退稿风险（一句话）

**以 0.08% 的统计不可区分主增益 + 无 OPF/UC 可行性验证去闯 IEEE Access 的二元 Accept/Reject 闸门，大概率被以 "insufficient rigor / unsupported claims" 直接拒稿并烧掉唯一一次重投机会**；同样的稿子投 Energies 最大风险是因缺敏感性分析和可行性校验触发 major revision 乃至拒稿，但至少有修改轮次可救。

---

## 进展更新（2026-07-14，curtailment 转向 v4 执行）

**用户决策执行**：审稿 §7.3 方案 2 的 curtailment 转向已实施，但**必须先重写管线**——审读发现 v3 调度实验与旧 p3/p4 同病（Method 手工常数 + DSTAR-GRU 独占 renewable_bias 加成公式，30 倍弃电差距大部分由该公式构造）。新管线 `src/powergrid_benchmark/mintou_real_curtailment.py`（`public_rts_curtailment_v4_real_models`）：固定参考调度策略（70% 瞬时非同步渗透上限，SNSP 类运行约束）下的弃电率为方法无关目标；DSTAR-GRU = 真实 GRU 编码器 + 学习嵌入空间 Siamese 检索 + 验证集混合权重；6 基线 + 5 真机制消融；4320 小时、10 种子、Mann-Whitney/Holm。v3 产物保留为历史证据。

**v4 真实结果（两面）**：
- ✅ **组件故事成立**：1h 上 DSTAR-GRU 显著优于全部学习型基线（LSTM/MLP p=0.001）与全部消融（NoSiamese p=0.0004、NoRetrievalBank p=0.001、SmallBank p=0.001、NoTopology p=0.042）——学习嵌入检索机制的贡献首次获得真实统计支撑。
- ❌ **优势主张不成立**：两个 horizon 都输给 Persistence（1h -6.4%，24h -51.6%；24h 时 Persistence 与 Seasonal-24h 按构造等价）。弃电序列高度持续且稀疏（9.5% 非零小时），MSE 训练的模型在 24h 尺度回归到近零，事件 F1 全体为 0。
- **含义**：审稿对 30 倍信号的乐观基于被构造的 v3 差距；真实任务下 naive 持续性主导。转向要成立需要第三次任务细化：**事件起始（onset/transition）预测**——在持续性失效的转折时刻评估（这是弃电预警的真实运营价值所在），或改走审稿方案 3 的 "检索即服务" framework 论文。当前证据支持的最大主张是组件级："Siamese 检索显著优于其消融与同类学习基线"。

**下一步决策点**：(a) onset 切片评估（改造 evaluate 为转折时刻子集，成本一次重跑约 40 分钟）；(b) 转 framework 论文叙事。建议先做 (a)——若 onset 上仍输 persistence 再降级到 (b)。

## 进展更新（2026-07-14 晚，v5 onset 评估 = p1 最终实验裁决）

全年 8760 小时、onset 阈值 0.02、检测阈值训练窗校准（对全方法一致）、10 种子（`public_rts_curtailment_v5_onset_eval`）。

**结果（三个评估角度全部无法支撑优势主张）**：
1. 整体 MAE：输 Persistence（v4 已知，v5 复现）。
2. **1h onset**：DSTAR-GRU F1 0.176 排第 3，**输给自己的 LSTMEncoder（0.185）与 NoTopology（0.185）消融**；onset MAE 显著差于 LSTM/NoRetrievalBank/LSTMEncoder。
3. **24h onset**：F1 排 7/12，**被 NoSiamese、NoRetrievalBank、LSTM、MLP 显著击败**——检索机制把预测拉向类持续性行为，在日前 onset 检测上是显著负贡献；Ridge（0.236）与 kNN 原始特征（0.226）反而最好。

**最终裁决**：拆除 v3 构造信号后，overall MAE、1h onset、24h onset 三个角度均无 DSTAR-GRU 的可辩护优势；检索组件"1h 平滑有益、24h 预警有害"。**优势型论文在此任务上不成立**，剩余诚实出路：
- **A（建议）**：转 framework/tool 论文（审稿方案 3："Operating-state retrieval for power system decision support"）——贡献 = 可复现弃电风险基准 + 检索框架 + 诚实组件分析（含负结果），投 Applied Sciences / Access（两刊都有 framework 先例）；v3→v5 的证据链本身是方法学叙事素材。
- **B**：组合层面搁置 p1，资源集中到已就绪的五篇。
- **C**：换任务重来（SDWPF 风电预测，等于新论文）。

在用户选择前，p1 不进入任何投稿排期。

## 进展更新（2026-07-15，A 路线执行）

**用户已拍板 A 路线**：p1 从方法优势论文转为 **framework/tool 论文**——"运行状态检索框架 + 可复现弃电风险基准"（对应本审稿 §7.3 方案 3 "Operating-state retrieval as a service"）。只改 ARA 逻辑/登记文件，实验代码与 evidence 不动。

**改动清单**：
1. `papers/mintou/manifest.csv` p1 行：title 改为 "An Operating-State Retrieval Framework and Reproducible Curtailment-Risk Benchmark for Power System Decision Support"；target_journal = IEEE Access，backup_journal = Applied Sciences；algorithm_name 保留 DSTAR-GRU（作为框架内检索组件名）。
2. `papers/mintou/mintou_p1_dstar_gru_dispatch/PAPER.md`：frontmatter 更新（status = `route_a_framework_pivot_v5`），Abstract 按三贡献重写（见下）。
3. `logic/claims.md`：主张体系重写为 C1/C2/C3 + 禁止条款（见下）。
4. `logic/problem.md`：gap 改写为"缺少可复现的公开弃电风险预警基准 + 对检索式决策支持缺乏跨尺度系统评估"；数据集列表收缩为实际使用的 RTS-GMLC。
5. `logic/solution/method.md`：加 "Framework pivot note (2026-07-15)"（转向原因 + v3→v5 证据链指针），基线/消融名单与 v4/v5 实跑对齐。
6. `papers/mintou/portfolio_status.md`：p1 行 Target = "IEEE Access (framework)"，signal = `route_a_framework_pivot_executed`，文末追加执行说明。

**新主张体系**：
- **C1 基准贡献（supported）**：方法无关的公开弃电风险基准——RTS-GMLC 全年 8760 小时、固定 70% SNSP 类参考策略、onset 切片协议（阈值 0.02、训练窗校准检测阈值全方法一致）、10 种子 Mann-Whitney+Holm 统计协议。
- **C2 检索组件尺度依赖效用（双向均有显著性支撑）**：1h 上学习嵌入 Siamese 检索显著优于全部学习型基线与消融（NoSiamese p=0.0004、NoRetrievalBank p=0.001）；24h onset 上同一机制显著有害（被 NoSiamese/NoRetrievalBank/LSTM/MLP 显著击败）。
- **C3 诚实负发现（如实呈现）**：Persistence 在两 horizon 整体 MAE 占优（1h -6.4%、24h -51.6%）；24h onset 上 Ridge（F1 0.236）/kNN 原始特征（0.226）最好；1h onset 上被自家 LSTMEncoder/NoTopology 消融（0.185）小幅超过——作为基准判别力的证明呈现。
- **禁止条款**：不得主张调度优化优势、拓扑不确定性能力、OPF 可行性、整体预测优势、无证据泛化。

**目标刊**：IEEE Access（framework/evaluation 论文，有 distilled 先例：纯内部比较可过）；备选 Applied Sciences。

**剩余待办（成稿前）**：
1. related work 三线综述（相似检索/度量学习在电力系统、弃电预测与消纳评估、公开基准与可复现性），落到 framework gap statement；
2. 敏感性小节：可用 SNSP cap 扫描（0.6/0.7/0.8）补——基准参考策略参数敏感性正当化；
3. 图件（onset 协议示意、尺度依赖效用对比图、基准管线图）；
4. 正文成稿（Access 模板、numbered contributions、超参数表、limitations 段）；
5. `logic/experiments.md` 消融状态标签更正（v4/v5 实跑，非 smoke-tested——第三方审稿已核实为标签问题）。
