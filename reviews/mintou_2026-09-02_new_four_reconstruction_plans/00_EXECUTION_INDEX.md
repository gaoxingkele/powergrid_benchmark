# 闽投新四篇：重构计划总索引

**版本日期：** 2026-09-03  
**状态：** `MDPI_ROUTE_CONFIRMED / HARNESS_V2_REGISTERED / AWAITING_PLAN_SHA_APPROVAL`  
**证据原则：** 不虚构数据、实验结果或参考文献；已有负结果与未显著结果必须保留。  
**标题原则：** 下列四个英文标题逐字锁定，不做语法或大小写修改。  

> 2026-09-03 更新：四篇 12 阶段 `paper_harness v2` 计划已经注册；最新执行入口、SHA 和质量门见 `08_HARNESS_V2_EXECUTION_PLAN.md` 与 `09_PLAN_APPROVAL_SHA256.csv`。下文 Wave 0 记录保留为历史基线。

## 1. 目标、上下文、约束与完成标准

- **目标：** 将现有四篇稿件重构为“标题—研究问题—方法—实验—结论”一致的投稿候选稿。
- **现有工程映射：**
  - 论文1 → `paper_projects/mintou_p5_trace_moea_feasibility_review`
  - 论文2 → `paper_projects/mintou_p6_bilonsga_project_review`
  - 论文3 → `paper_projects/mintou_p3_samode_distribution_planning`
  - 论文4 → `paper_projects/mintou_p2_hygraph_load_forecasting`
- **硬约束：** 标题、作者排序与通信作者锁定；不删除不利结果；新增引用须经元数据和正文核验；原实验目录只读，新实验使用新命名空间。
- **本轮完成标准：** 每篇均形成章节级改造方案、实验矩阵、参考文献处理方案、图表蓝图、验收门槛和执行依赖。
- **执行阶段完成标准：** 新实验可复现，主张可追溯到结果表/图，LaTeX 可编译，引用完整性检查通过，并完成目标期刊格式迁移。

## 2. 四篇的锁定信息与重构强度

| 论文 | 锁定标题 | 目标期刊 | 现有项目 | 重构强度 | 核心原因 |
|---|---|---|---|---|---|
| 1 | Investment Effectiveness Optimization Strategy based on Hybrid Multi-objective Evolution | Energies | P5 TRACE-MOEA | 中等 | 方法与题目大体相容，但“投资效益”验证不足，当前偏向偏好搜索与追踪记录 |
| 2 | Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization | Applied Sciences | P6 BiLo-NSGA | 大修 | 电网投资主题与栏目相容，但双向局部搜索优势尚未成立，且投资效益仍需成本/物理验证 |
| 3 | Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm | Energies | P3 CARS-MODE | 大修 | 当前是规划代理问题；自适应贡献与固定 DE 未隔离，物理可行性证据不足 |
| 4 | Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting | Electronics | P2 CSA forecasting | 近乎重建 | 现有模型是双曲距离注意力，不是图卷积；已有匹配检验显示几何增益未解决 |

### 2.1 2026-09-03 路线决定

- 根据 `05_MDPI_ORIGINAL_TARGET_PREASSESSMENT_2026-09-03.md` 的范围核验与相似论文检索，主执行路线确定为：P1→Energies、P2→Applied Sciences、P3→Energies、P4→Electronics。
- 现有四份 `paper.tex` 已分别使用 `energies`、`applsci`、`energies`、`electronics` 文档类，不需要跨出版商迁移；仍须在投稿前重新核对栏目、模板版本、声明、费用和编辑政策。
- P2 的 Security and Communication Networks 网络安全重构只保留为备选研究分支，不再作为当前投稿路线的强制门禁；不得为了期刊适配而把一般投资项目改名为安全项目。
- `ORCID = NONE` 仅作为作者未提供 ORCID 时的内部工作稿占位。最终投稿表单按各期刊当时要求处理，不虚构 ORCID。

> 标题和目标期刊来自作者锁定文本；期刊页面仍可能更新。内部篇幅目标不是期刊硬规则，正式提交前再运行一次官网 preflight。

## 3. 共同科学重构规则

### 3.1 主张分层

每篇先建立三层主张登记表，写作时不得跨层升级：

1. **已证实：** 有冻结实验、可复现代码、表图和统计检验直接支持。
2. **待检验：** 是新实验的研究假设，只能用“we investigate/evaluate”，不能写成结果。
3. **不可主张：** 当前数据或设计无法识别，例如工程部署有效性、专家偏好真实性、真实投资收益或安全干预效果。

### 3.2 负结果保留

- 论文1：偏好自适应独立效应目前未解决，不能改写成已显著有效。
- 论文2：现有等预算实验中 BiLo 对 NSGA-II 无胜场且有显著失利，不能隐藏；新 Applied Sciences 电网投资任务必须把旧结果作为预研边界或补充材料披露。
- 论文3：指标选择会改变排名，自适应作用未隔离，不能只报告有利 HV。
- 论文4：当前双曲距离权重相对匹配基线未显著改善，DLinear 在现有层级任务上更强，必须保留为旧模型基线。

### 3.3 证据与统计规则

- 先冻结研究问题、主要指标、比较族和随机种子，再运行正式实验。
- 随机算法采用成对种子；报告效应量、置信区间、原始与多重校正后检验结果。
- 不把单次运行、最佳种子或逐时间点样本当作独立统计单位。
- 超参数调优与最终评估严格分离；测试集不得参与建图、归一化或模型选择。
- 新实验输出目录不可覆盖，必须包含配置、环境、日志、原始结果和汇总脚本。

### 3.4 参考文献规则

- 现有引用先做“正文支持性、元数据、可访问原文”三重审计。
- 新引用先进入 `待检索/待核实` 队列；核对题名、作者、年份、期刊/会议、DOI 后才进入 BibTeX。
- 引言和相关工作按研究问题组织，不按作者年份罗列。
- 方法经典文献只能支持算法来源，不能代替领域问题、数据集和工程约束文献。

## 4. 执行波次

### Wave 0：基线冻结与可恢复检查点

- 为四个现有项目记录当前提交、主稿哈希、PDF、实验配置和结果清单。
- 不修改旧实验输出；建立四个新的 `s4/s5` 实验目录。
- 每篇建立 `CLAIM_EVIDENCE_REGISTER.md` 与 `REFERENCE_AUDIT.csv`。
- 工作稿中按作者要求把未知 ORCID 标为 `NONE`；最终投稿表单不得把 `NONE` 当成真实 ORCID。

### Wave 1：四个可行性门禁

| 门禁 | 要回答的问题 | 通过条件 | 未通过处理 |
|---|---|---|---|
| P1 投资效益 | 是否能给成本、工程可行性或外部验证增加至少一类可审计证据？ | 数据来源和计算路径可追溯 | 将结论严格限制为代理筛选，不写实际投资效益 |
| P2 电网投资 | 双向局部搜索能否在第二个独立任务族、等评价预算和真实/校准成本下产生可归因价值？ | 至少完成第二任务族、NDS/前向/后向/双向正交消融和一层成本或物理验证 | 保留负结果，将方法定位为边界研究；不强造网络安全语义 |
| P3 规划动作 | 决策变量能否映射到真实配电规划动作并进行 AC 校验？ | 至少一个网络、一个动作集端到端运行 | 保留代理研究，降低规划工程主张 |
| P4 双曲 GCN | 是否能构造无泄漏图并实现真正的双曲图卷积？ | 欧式 GCN 与双曲 GCN 在同一数据管线可运行 | 不再以锁定标题投稿，除非模型实现补齐 |

### Wave 2：最小可运行实验

- 每篇先在一个数据集/场景和 3–5 个种子上完成端到端试运行。
- 只验证代码、指标和资源开销，不把试运行数字写入论文结论。
- 通过单元测试、数据泄漏检查、预算/约束一致性检查后再扩大。

### Wave 3：正式实验与消融

- 冻结正式配置，运行主比较、关键消融、跨场景稳健性和计算代价。
- 自动生成主表、统计表、图和机器可读结果。
- 失败、无效和不显著结果同样进入证据登记表。

### Wave 4：章节重写

顺序固定为：结果事实表 → 方法与实验 → 讨论与局限 → 相关工作 → 引言 → 摘要 → 结论。摘要与结论最后写，避免先写结论再寻找证据。

### Wave 5：投稿前门禁

- 标题—摘要—贡献—结论逐句一致性检查。
- 引用完整性、图表数值一致性、代码/数据可复现检查。
- 迁移至目标期刊模板，编译 PDF，检查匿名、作者信息、声明、补充材料。
- 期刊适配不改变科学事实；若期刊范围与证据仍冲突，明确标记 `NO-GO`。

## 5. 推荐执行优先级

1. **先执行论文1。** 现有证据最完整，优先补成本/AC/外部验证并验证整套工作流。
2. **随后执行论文3。** 拆分自适应开关并建立规划动作—AC 校验闭环。
3. **再执行论文4的图与模型门禁。** 先证明数据可以无泄漏建图、模型确为 HGCN，再投入完整训练。
4. **最后执行论文2正式实验。** 先建立第二个独立电网投资任务族，再做双向局部搜索正交消融；网络安全分支暂不执行。

## 6. 独立计划文件

- `01_PAPER1_HYBRID_MOEA_PLAN.md`
- `02A_PAPER2_APPLIED_SCIENCES_GRID_INVESTMENT_PLAN.md`：当前主执行方案。
- `02_PAPER2_BIDIRECTIONAL_NDS_PLAN.md`：Security and Communication Networks 备选分支，当前不执行。
- `03_PAPER3_SELF_ADAPTION_MODE_PLAN.md`
- `04_PAPER4_HYPERBOLIC_GCN_PLAN.md`
- `05_MDPI_ORIGINAL_TARGET_PREASSESSMENT_2026-09-03.md`：原 Energies / Applied Sciences / Electronics 的期刊适配、同刊相似论文和路线调整建议。
- `06_MDPI_EXECUTION_STATE_2026-09-03.md`：Wave 0 完成状态、基线边界和下一检查点。

## 7. 当前检查点

作者已用“继续下一步”确认进入执行阶段。Wave 0 已以当前工作树为基线建立哈希、主张边界、参考文献审计入口和四个 s4 实验命名空间，**未回退或覆盖已有未提交修改，也未改动现有实验结果**。下一步在作者检查点确认后进入 P1 投资效益验证门禁；任何新科学主张仍必须等待对应实验完成。
