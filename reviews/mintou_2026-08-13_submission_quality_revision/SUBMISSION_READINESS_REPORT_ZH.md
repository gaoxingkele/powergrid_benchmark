# 闽投六篇投稿质量提升与就绪性报告

日期：2026-08-13  
方法：academic-research-suite 的 revision coach、structure architect、peer reviewer 与 journal-fit 流程；目标期刊规则分别采用 IEEE Access、MDPI Electronics、MDPI Energies 和 MDPI Applied Sciences。

## 结论

六篇论文已完成一次以“标题—研究问题—贡献—方法—实验—讨论—结论”闭环为中心的实质性修订，并重新生成正式期刊版 PDF/LaTeX。修订显著降低了标题过度承诺、组合消融误归因、负结果被叙事化掩盖、trace 与效用混同以及内部审计语言主导正文等风险。

不能诚实保证“一投必中”。当前可以实现的是：把可由现有数据解决的科学叙事、方法归因、统计口径和排版问题尽量在投稿前消除；作者信息、基金和真实专家效用评价不能由系统代填或虚构。

## 六篇当前定位

| 论文 | 目标期刊 | 修订后的核心主张 | 仍需避免的过度解释 |
|---|---|---|---|
| P1 | IEEE Access | 公共削减风险代理基准；检索效用具有时间尺度依赖 | 不能写成普遍预测优势或真实调度削减记录 |
| P2 | Electronics | OPSD 日前设置中，跨序列聚合有效；权重几何未分出差异 | 不能写成 Poincaré/双曲结构优势或全数据集优势 |
| P3 | Energies | 约束修复、前沿多样性和整体框架得到支持 | 固定参数与单策略是组合控制，不能单独归因参数或策略自适应 |
| P4 | Energies | 场景筛选、搜索/评价分离和修复机制用于韧性规划 | 筛选减少调用数不等于已证明运行时优势；hybrid 与周期重筛未分出增益 |
| P5 | Energies | 可追踪投资组合优化工作流，决策轨迹与优化性能分别测量 | trace coverage 不等于人类评审效用或真实投资决策正确性 |
| P6 | Applied Sciences | 项目语义局部搜索及情景依赖的前向操作效应 | 不再声称 forward-dominant；替换操作保留的是可审阅语义而非已证实精度增益 |

## 已完成的关键修改

1. P1 将 Siamese 明确为 shared-encoder/Siamese-style 权重共享，不暗示未实现的对比学习目标。
2. P2 将贡献从显著性清单改为组件可识别设计、跨设置评价和机制适用范围；MLP 被准确标为初筛后确认的 targeted comparator。
3. P3 全文统一把 FixedDE 解释为“固定参数+单策略”组合对照，停止把结果单独归因于 strategy adaptation。
4. P4 删除标题中没有实现对应的 Lookahead，改为 `Scenario Screening with Disjoint Evaluation`，并区分主消融与多选项 targeted controls。
5. P5 将主线从“审计证据层级”改为可检查的 portfolio-search workflow，明确 trace 是隔离的输出通道。
6. P6 从标题和中心结论移除证据不足的 Forward-Dominant，改为 scenario-dependent forward effects，并更新伴生论文引用。
7. P4↔P3、P5↔P6 的共享候选生成与独立方法/运行/结论关系已在正文中对称披露。
8. 压缩 `frozen`、`audit`、`post-freeze` 等内部过程词，保留真正影响实验解释的预设范围与统计界限。
9. 修复公共构建器的标题层级错误：IEEE 的 Introduction 现为 `I. INTRODUCTION`，MDPI 的 Introduction 现为 `1. Introduction`。

完整逐项记录见 `REVISION_TRACEABILITY.md`。

## 构建与验证

- 正式期刊模板构建：6/6 成功。
- 审阅预览构建：6/6 成功。
- LaTeX undefined control sequence / undefined reference / missing character：6 篇均为 0。
- 实验回归：`pytest -q tests/test_mintou_experiments.py`，12/12 通过。
- 伴生论文独立性审计：P3/P4 与 P5/P6 均无相同结果表；完全相同图形仅为 MDPI ORCID 模板标识。句子重合主要来自标准参考文献、公共统计表述和作者占位语，不构成相同实验结果复用；共享候选生成已在两边正文披露。
- 正式 PDF 页数：P1 15；P2 19；P3 22；P4 24；P5 23；P6 24。
- 首页和末页已做图像化 QA；未发现裁切、乱码、图层网格或正文重叠。
- 参考文献本轮未重新进行联网全量核验；沿用 2026-08-12 的结果：202 条中 196 条 DOI/Crossref 已核验，6 条无 DOI 需人工复核。不得把该历史结果表述为本轮新验证。

## 投稿阻断项

1. **P1**：作者、单位、通信作者、基金、作者简介/照片仍为明确占位符。
2. **P4**：作者、单位、通信作者、CRediT 和基金仍为明确占位符。
3. **P2/P3/P5/P6**：作者名单已存在，但 CRediT 与基金仍需作者确认；不可从其他论文或历史会话猜测复制。
4. 六篇均需由作者最终确认利益冲突、数据许可、代码仓库公开状态和 AI 使用声明。
5. P5/P6 的 human-review value 与 P1/P3/P4 的跨系统物理外部效度仍属于新实验问题；本轮没有制造不存在的专家评价或仿真结果。

## 投稿策略判断

- P1、P2 的方法论和负结果叙事已经较成熟，补齐元数据后可进入投稿前人工终审。
- P3、P4 的代理目标与 AC 检查不完全一致已被转化为清楚的二层评价发现；审稿人仍可能要求更强的独立网络验证，但不再是叙事失控。
- P5、P6 已把两个相邻稿件的身份区分清楚；若同一编辑或审稿人同时看到两篇，共享资产披露能够说明其数据来源关系，但作者仍应准备解释两篇的独立研究问题和不重叠结论。

## 不能承诺的事项

录用由编辑范围判断、审稿人意见、同期竞争、伦理与合规核查共同决定。因此，本报告不把“质量提高”表述为“保证录用”。当前版本的目标是减少可预见的 desk-reject 和 Major Revision 触发点，并让剩余风险清晰、可回答、不可伪造。
