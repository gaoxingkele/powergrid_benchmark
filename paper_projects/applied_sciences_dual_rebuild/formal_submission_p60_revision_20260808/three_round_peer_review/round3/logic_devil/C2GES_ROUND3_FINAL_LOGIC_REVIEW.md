# C²GES 第三轮终审：逻辑与证据边界

## 最终建议

**Major Revision（不是 Reject）**。

修订稿已消除主要实现—文本矛盾，负结果和统计边界也保持一致。剩余阻断项集中在原标题：现有数据支持“可审计的固定文本图路径参与度及其负消融”，不支持标题通常暗示的因果/反事实语义或维护报告有效性。若允许调整标题/副标题和贡献定位，可由文字关闭到可投稿；若原标题必须原样维持，则需要新数据。

## 第二轮修复闭环验证

| 检查项 | 终审状态 | 最新稿证据 |
|---|---|---|
| 文档顺序与边方向矛盾 | **CLOSED** | Related Work line 75 已改为 monotone role-stage progression，并明确“不一定是文档句子时间顺序”；Methods lines 183–191 使用绝对句距并允许边逆文档 chronology。 |
| 边权定义不完整 | **CLOSED** | Methods lines 183–187 给出 $d_{ij}=|pos(i)-pos(j)|$、Jaccard、角色置信度、12位舍入和完整 $w_{ij}$ 公式。 |
| 复杂度错误写成局部 $12n$ 扫描 | **CLOSED** | Methods line 249 明确冻结实现扫描全部有序对，构图为 $O(n^2)$；约 $24n$ 只描述通过距离门的候选边。 |
| no-CF 被误称为纯组件隔离 | **CLOSED** | RQ map lines 118–129、Methods lines 241–245、Results RQ2 line 522 均称 unrenormalized coefficient removal，并量化 redundancy 相对尺度由0.50变为0.5882。 |
| accounting identity 被当作效能理论 | **CLOSED（主张层面）** | Contributions line 49 改为“instantiate and audit”；Methods line 212 明确固定图 accounting identity，不是 causal-identification theorem；未声称理论效能保证或 path-centrality 首创。 |
| 负消融、长度混杂、调参不对称漂移 | **CLOSED** | Abstract line 19、Results lines 353–484、RQ2 line 522、Conclusions lines 570 onward 一致保留 no-CF 更高、长度不匹配与不构成总体 superiority。 |

## 残余投稿阻断项

### B1 — 标题级 causal/counterfactual 证据仍未建立

- **严重度：MAJOR；状态：OPEN。**
- **锚点：** Title line 12；Contributions line 49；Equations (1)–(2) and Methods line 212；Results line 430 and RQ2 line 522；Conclusion paragraph reporting zero-weight calibration.
- **判定：** 数学对象已清楚，但它是固定角色图中的路径参与度/删除记账量。严格消融不利、12/12开发折选零权重，且无专家角色/边标签。当前稿没有互相矛盾地声称增益，但标题仍比证据强。
- **必须新数据/或改标题：** 保留原标题需新增盲法专家角色—边—链条标注、非因果路径中心性对照、预注册新冻结集；否则将标题/副标题改为 typed-path structural sensitivity/proxy study。

### B2 — “for Power Grid Maintenance Reports” 仍是未测试应用

- **严重度：MAJOR；状态：OPEN。**
- **锚点：** Abstract and Featured Application lines 19–21；Introduction line 39；Discussion maintenance transfer；Conclusions line 570 onward。
- **判定：** 全文诚实称 NERC proxy，但没有工单、巡检记录或维护人员结果。该限制不能由更多文字变成验证。
- **必须新数据/或改标题：** 新的许可清晰维护语料、未见外部集、合格电网人员对忠实性/链覆盖/危险遗漏/导航价值的独立评价；否则标题须显式含 proxy/NERC technical reports。

### B3 — 正 CF 权重的保留决策仍无事前科学理由

- **严重度：MAJOR；状态：OPEN。**
- **锚点：** Development Selection line 263；post-unblinding calibration；Results and Conclusions negative ablation。
- **判定：** 稿件已不再把 Full 当成优胜组件，但仍称 Full C²GES，而开发数据在正式测试前已经显示 Full-minus-no-CF 为负。没有展示事前组件保留规则。
- **文字可关闭：** 若冻结协议确无规则，直接称 Full 为“registered but unsupported candidate integration”，并把 no-CF 作为经验参考配置；不能补造事前理由。

## 最终回归：是否还有互相矛盾的强主张

正文内部未再发现“组件显著有效”“物理因果”“维护部署就绪”之类反向强主张。剩余冲突主要存在于**标题普通语义与正文主动降格之间**，不是 Results—Conclusion 数值矛盾。

## 投稿前动作分类

### 可由文字关闭

1. 调整标题/副标题，使 causal/counterfactual 和 maintenance 明确为 textual proxy study。
2. 将 Full 明确称为未获支持的注册候选集成，不暗示推荐配置。
3. 投稿信、Highlights、Graphical Abstract、仓库 README 沿用正文边界。

### 必须新数据或外部动作

1. 专家语义标注与维护外部集（若坚持原标题）。
2. 同等词预算、版面感知切分和对称调参的新冻结实验（若声称 baseline superiority）。
3. 同步并不可变标记 GitHub 仓库，完成 fresh-clone verification。

## 终审结论

论文具备透明负结果论文和审计型方法论文的价值，不建议 Reject；但在原标题不变且无新数据的条件下，仍建议 Major Revision，不能宣告标题级科学闭环。

