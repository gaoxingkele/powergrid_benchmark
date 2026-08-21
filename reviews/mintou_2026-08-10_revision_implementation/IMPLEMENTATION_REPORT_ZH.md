# Mintou 六篇论文 1–6 项目标实施报告

日期：2026-08-10  
对象：`paper_projects/mintou_p1*` 至 `mintou_p6*` 最新 `MANUSCRIPT.md`

## 已完成

1. **证据冻结与主张矩阵**：建立 `REVISION_EVIDENCE_MATRIX.md`，明确每篇的可用数据、算法模块、负结果、允许主张和新增实验边界。
2. **算法框图**：对六篇分别调用 GPT Image 2 生成期刊风格母版；母版不直接作为投稿图。依据实际代码重绘了六套 `fig_architecture.svg/.pdf/.png`，统一白底、无斜线网格、蓝/青/橙配色、线宽和字号，并嵌入方法章节。
3. **结果图资产**：确认六篇现有结果图均有生成脚本和本地文件；新增框图后完成图号顺延、caption 与正文引用核对。六篇图号均从 1 连续排列，所有引用图文件存在。
4. **方法形式化**：补充输入、目标、约束、距离/注意力、变异、修复、选择、超体积、审计隔离和复杂度等定义。显示公式数现为 P1–P6：8、7、11、9、8、10。
5. **关键实验补强**：P4 新增 GA-only、DE-only、固定 worst-K 三项机制控制；使用原八个实验、30 seeds、相同种群/代数、相同搜索—评价隔离和相同归一化，共新增 720 个真实运行。新结果写入独立文件，未覆盖 2400 条主实验记录。
6. **结果回写与诚实归因**：P4 摘要、贡献、主结果、消融、讨论、局限和结论均写入新增负/零结果；删除“剩余增益可归因于 hybrid+screening”的过强表述。

## 当前量化状态

| 稿件 | 正文前英文词数 | 显示公式 | 正文图 | 图/Caption 连续 | 图文件存在 |
|---|---:|---:|---:|---|---|
| P1 | 6288 | 8 | 4 | 1–4 | 是 |
| P2 | 6336 | 7 | 4 | 1–4 | 是 |
| P3 | 7218 | 11 | 5 | 1–5 | 是 |
| P4 | 8078 | 9 | 5 | 1–5 | 是 |
| P5 | 8123 | 8 | 4 | 1–4 | 是 |
| P6 | 8536 | 10 | 5 | 1–5 | 是 |

词数统计用于内部比较，不等于排版页数。P4–P6 已进入目标期刊参考样本中位数附近或以上；P1/P2 保持较短，但新增篇幅集中在可复现方法而非背景扩写。

## P4 新实验结果

合并原 SHIELD-MOEA 结果后的 pooled mean HV：

| 方法 | Mean HV | Worst-case mean HV | Mean runtime (s) | 运行数 |
|---|---:|---:|---:|---:|
| DE-only | 0.274250 | 0.269179 | 0.0874 | 240 |
| Fixed worst-K after generation 1 | 0.274076 | 0.269189 | 0.0679 | 240 |
| SHIELD-MOEA | 0.273962 | 0.269114 | 0.0889 | 240 |
| GA-only | 0.270144 | 0.265418 | 0.0636 | 240 |

- Hybrid 对 DE-only：8/8 场景均不显著。
- 动态重筛对固定 worst-K：8/8 场景均不显著。
- Hybrid 对 GA-only：3/8 场景 Holm 校正后显著，其余不显著。
- 因此论文不再声称 hybrid 或周期重筛带来独立 HV 增益；可支持的是完整方法相对外部基线的结果、repair 的核心作用、screening 的调用次数节省，以及严格的搜索—评价隔离。

证据文件：

- `papers/mintou/mintou_p4_shield_resilience_planning/evidence/runs/real_shield_mechanism_controls_20260810.csv`
- `papers/mintou/mintou_p4_shield_resilience_planning/evidence/tables/real_shield_mechanism_controls_20260810_leaderboard.csv`
- `papers/mintou/mintou_p4_shield_resilience_planning/evidence/tables/real_shield_mechanism_controls_20260810_significance.csv`
- `papers/mintou/mintou_p4_shield_resilience_planning/src/configs/real_shield_mechanism_controls_20260810.json`

## 验证

- Mintou 资产测试：12 个测试函数全部通过（本机默认 Python 缺少 pytest 包，因此直接逐个执行了同一测试函数）。
- P4 新实验完整性：720 行；3 个控制方法；8 个实验；每实验每方法 30 seeds。
- 六篇框图：SVG、矢量 PDF、300 dpi PNG 均已生成；GPT Image 2 母版保留用于风格追溯。
- 六篇图片引用：无缺失资产，图号与 caption 一一对应。
- 参考文献：本轮未新增引用；沿用上一轮 200 条文献完整性审计结论。联网重跑核验因 120 秒执行窗口超时而未完成，不将其表述为新一轮通过。

## 尚未完成、不得替作者生成的投稿门禁

Stage 2.5 仍为 **FAIL**，原因不是算法或图片，而是六篇仍含作者输入占位符：作者顺序/单位、通信邮箱、ORCID（如有）、逐篇基金陈述、作者批准的 CRediT、最终仓库 URL/DOI。P1 还需要 IEEE Access biography/photo；P4 缺完整作者元数据。上述字段确认前，不应宣称六篇已经完成正式模板组装、专家三轮终审或可直接投稿。

## 后续高价值但未冒充完成的实验

- P3：JADE/SHADE/L-SHADE 类直接自适应 DE 基线，需要独立实现、统一二进制编码/repair/预算并重新冻结调参协议。
- P5：R-NSGA-II/NSGA-III/SPEA2 等偏好 MOEA，需要同一五目标、repair 和评价预算；不能把普通 NSGA-II 代称为偏好基线。
- P1：若继续强调算法竞争力，应在完全一致的 target/split/seed 下加入完整近期预测器；当前更适合 benchmark 与机制边界定位。
- P2：层级 reconciliation 与 Ausgrid 平衡 seeds 仍是最直接补强项。

这些项目不是当前数据真实性的缺陷，但决定是否能进一步提升算法创新或外部有效性主张。
