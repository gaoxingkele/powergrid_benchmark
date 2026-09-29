# P4 Stage-3 候选评审（p4_v2_s03_graph_data_model_implementation_contract）

**日期：** 2026-09-04
**候选分支：** `paper-harness/mintou_p2_hygraph_load_forecasting/v2-p4_v2_s03_graph_data_model_implementation_contract`
**评审基准：** 16 号契约 + 08 号执行计划 §4 + 17 号质量门
**结论：** **建议接受，无必改项**（三篇 s03 候选中最强）

## 一、对照 16 号契约的核验

| 契约条目 | 候选产出 | 判定 |
|---|---|---|
| §2.1 真实 HGCN 实现（红线解除路径） | `models.py`：邻接归一化聚合卷积、**无注意力模块**（验证器断言）；Poincaré 球 exp/log 显式公式；fixed c=1 / learnable c=softplus+1e-4；**fixed-zero 几何 = 欧式 GCN 本身**（避免数值伪零曲率 HGCN 的取巧） | ✅ 验收级 |
| §2.2 匹配欧式 GCN | 同图/同编码器(168-96-48)/同头/同调参预算，仅几何变化；可学曲率仅 +1 标量；参数差实测 **0.003%**（门槛 ≤10%） | ✅ 超配 |
| §2.3 图零泄漏 | Ausgrid 17 节点会计层级（非伪装拓扑）；OPSD 功能图 |Pearson|≥0.7、训练前缀内重算、逐外层切分重建；验证/测试值、未来缺失、标签、误差**禁止入图**；归一化仅训练前缀拟合 | ✅ 严格 |
| §2.4 baseline 补全（s04 项） | persistence 等基线留待 s04 冻结协议（EXPERIMENT_PROTOCOL +4） | ✅ 前移合理 |
| P4-8 曲率定义先行（R2 新增） | 模型/exp-log/曲率参数语义与方法章节一一对应 | ✅ |
| 红线保留 | 明确"no GCN or HGCN experiment or result is reported" 语句在产出结果前**仍属科学必要**——实现 ≠ 结果，红线未提前解除 | ✅ |
| 遗留阻塞 | Ausgrid leaf 身份与区域成员不在工作树 → 要求**哈希源清单**而非编造映射（s04/s05 pilot 门解决） | ✅ 诚实记录 |

## 二、候选技术质量

- 验证套件：图构造未来扰动免疫、无注意力邻接聚合、exp/log 往返、1/2 层有限前向/反向、参数匹配、`git diff --check` 全过；仅合成张量验证不变量，**未产生任何实验指标**。
- 候选未改动 `journal_submission/paper.tex`（无转义缺陷风险）；builder 触碰过的 TeX/Markdown 已恢复并哈希一致。
- CSA-LoadNet 不得改名 GCN/HGCN、DLinear 优势保留——历史证据边界原样。

## 三、与 16 号契约 §7 的衔接

- 实现完成 → 下一步 s04 冻结协议（Hier/Dense 条件、WAPE 主指标、消融正交表）→ s05 pilot 门（资源预算 + Ausgrid 源清单）。
- H1 不通过时的路由决策门（P4-5）保持预注册状态。

## 四、建议

1. **接受** `p4_v2_s03_graph_data_model_implementation_contract`；
2. 接受后按资源顺序启动 **P2** 的 `p2_v2_s03_method_task_implementation_contract`（14 号契约已注入）；
3. P3 的 action registry 可行性答复仍需在各自 s04 启动前给出。
