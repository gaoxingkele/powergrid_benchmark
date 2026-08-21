# MA-SQLGrid 第三轮终审：逻辑与证据边界

## 最终建议

**Major Revision（接近 Minor，但原标题下仍有外部效度阻断项）**。

稿件的内部证据结构已经基本闭环：没有把历史池结果称为五角色增益，没有把零弃权称为置信度，也没有混合 v3 与 FINAL 版本。剩余主要问题不是可疑统计，而是标题级“robust multi-agent … in power grid databases”缺少端到端五角色效益和合格电网语义验证。若改为 architecture/evidence-audit 定位，可降至 Minor；若坚持当前标题的通常算法含义，需要新实验。

## 第二轮修复闭环验证

| 检查项 | 终审状态 | 最新稿证据 |
|---|---|---|
| 三个组件 Holm 家族和六项效应不完整 | **CLOSED** | Component Results lines 432–476 新增六行效果表、三个二成员家族、N/groups/pointwise interval/raw and Holm p。 |
| pointwise interval 与 Holm 决策表面冲突 | **CLOSED** | Factorial line 422 和 component table caption line 459 明确 intervals 非 simultaneous、非 Holm inversion。 |
| 非 factorial 分析的加权/交换性不清 | **CLOSED** | Methods lines around 320–324 明确 component group signs、12-group states 和11-database BIRD 的单位、权重与 sign-exchangeability 限制。 |
| 40/40安全执行分数在 eligibility 后为常数 | **CLOSED** | Adjudication 已改述为 hard gates 后的有效10/5/5 evidence score，稳定顺序与空集弃权；与归档实现等价。 |
| 零弃权被误读为高置信度 | **CLOSED** | Results line 572 明确零弃权来自至少一个 eligible slot 加强制 stable-order tie resolution，不是 calibrated confidence。 |
| robust 与顺序敏感矛盾 | **CLOSED（披露层面）** | Robustness matrix 已加入 candidate-order stability not established；Results lines 622–673 和 Conclusions line 732 保留101 versus117–118及130/180并列。 |
| v3/FINAL、New/descriptive、170分母、六图等前轮问题 | **CLOSED** | Version matrix、protocol master、component counts、Supplement and Acknowledgments 保持一致。 |

## 残余投稿阻断项

### B1 — 五角色 architecture 有软件合规证据，但无效益识别

- **严重度：MAJOR；状态：OPEN。**
- **锚点：** Title line 15；Introduction RQ1；Results line 360；Limitations line 718；Conclusions lines 730–732。
- **判定：** 当前稿没有虚假声称 superiority，因此不存在内部数值矛盾；但 Analyst/Cartographer 是 skeleton，Synthesizer 包装外部候选，没有 call-matched single/monolithic versus five-role 试验。标题仍可能被编辑理解为已验证的多智能体方法。
- **必须新数据/或改标题：** 全新未见、调用/候选/模型/解码匹配的端到端比较；否则标题/副标题明确为 “Auditable Five-Role Software Architecture and Retrospective Evidence Study”。

### B2 — 电网语义效度仍来自小型合成、开发可见资源

- **严重度：MAJOR；状态：OPEN。**
- **锚点：** Data Resources: GridDB 1 DB/8 tables/98 rows；RTS-GMLC and SimBench machine silver with zero qualified review；BIRD non-grid；Limitations lines 718–724。
- **判定：** SQLite安全与可复现性可以成立，但 “in Power Grid Databases” 的业务语义正确性未被合格专家或真实外部数据库验证。
- **必须新数据：** 双专家独立审核的 grid question–SQL gold，封存数据库/站点外部测试，并评价 projection、单位、时间边界、排序、并列和结果粒度。

### B3 — public repository 尚未形成投稿时可复现对象

- **严重度：投稿阻断；状态：OPEN external action。**
- **锚点：** Supplementary/Data Availability 明确 repository must still be synchronized and tagged。
- **外部动作：** 同步 `ma-sqlgrid`、许可证、不可变 tag/archive、fresh clone 运行与哈希核验；完成前不能在投稿材料中暗示公开仓库已复现最终稿。

## 最终回归：是否还有互相矛盾的强主张

未发现 Results、Discussion 与 Conclusions 之间重新出现五角色 superiority、universal robustness、semantic rescue 或 prospective-v3 强主张。`counterfactual testing` 关键词仍比正文更宽，建议文字改成 `metamorphic testing`，但属于 Minor。

## 投稿前动作分类

### 可由文字关闭

1. 标题/副标题明确 architecture/evidence-audit，而非端到端效益。
2. keyword 将 counterfactual testing 改为 metamorphic testing。
3. `Gold-isolated` caption 限定为 within-run raw-gold isolation。
4. Robustness 表继续按 v3/FINAL 分行，避免第一印象混合。

### 必须新数据或外部动作

1. 五角色 matched-call untouched experiment（若主张方法效益）。
2. 合格电网专家 gold 与真实/外部 grid database evaluation（若坚持现标题强度）。
3. 仓库同步、tag/archive 和 fresh-clone verification。

## 终审结论

论文不应 Reject：其软件边界、版本审计和负结果有明确价值。若作为 architecture/evidence-audit 论文并调整标题定位，可进入 Minor Revision；在现标题且不补外部验证时，最终建议仍为 Major Revision。

