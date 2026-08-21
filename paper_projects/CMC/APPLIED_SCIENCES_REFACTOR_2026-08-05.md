# 两篇 CMC 历史稿转投 MDPI Applied Sciences：重构与实验审计

日期：2026-08-05

## 版本判定

- **MA-SQLGrid**：内容基线为
  `paper_projects/2026_ma_sqlgrid_cmc/source/manuscript_cmc/paper_cmc.tex`
  （2026-07-24）。该版本包含第二生成器、确定性重复、评价口径敏感性、
  x10 行扩展与最新可复现性声明。
- **C2GES**：内容基线为
  `paper_projects/2026_c2ges_engineeringletters/source/manuscript_cmc/paper_cmc.tex`
  （2026-08-04）。它已把主评测从 AI simulated-expert NERC 标签改为 FEVER
  人工金标准，并把 NERC 限定为定性应用案例；这是比 2026-07-24 CMC
  别名稿更晚、证据边界更可靠的版本。
- 原 CMC/TSP 文件均保留，没有覆盖历史投稿材料。新稿统一放在两项目的
  `06_Applied_Sciences_Current/`。

## Applied Sciences 适配结果

### MA-SQLGrid

- **Target**: Applied Sciences (MDPI)
- **Fit**: Medium--High。工程受益人和维护数据库应用明确，比较、消融、
  第二生成器与资源指标充分；主要风险是仅有单个合成数据库。
- **Contribution type**: applied-method / benchmark validation。
- **Best-fit Section**: Computing and Artificial Intelligence；也可由编辑部
  判断是否转 Electrical, Electronics and Communications Engineering。
- **Top rejection risk**: synthetic-only validation and unexecuted full
  context-by-shape factorial。
- **Title policy**: 题目完全保留。

### C2GES

- **Target**: Applied Sciences (MDPI)
- **Fit**: Medium。FEVER 人工标注主实验方法学更可靠，NERC 应用场景明确；
  但当前 NERC 只有定性案例，且 C2GES 与 BM25 在主指标上统计持平。
- **Contribution type**: applied-method / interpretable information retrieval。
- **Best-fit Section**: Computing and Artificial Intelligence。
- **Top rejection risk**: title/application domain stronger than current
  quantitative domain validation。
- **Title policy**: 保留原题核心，仅增加
  “An Interpretable Learnable Reranker” 以反映 8 月 4 日的新方法。

## 论文结构改动

- 使用官方 MDPI 2026-06-23 模板快照与 `applsci` class 选项。
- 摘要压缩至约 200 词，加入 `Featured Application`，直接说明工程使用者。
- 重排为 Introduction / Related Work / Materials and Methods (or Data) /
  Experimental Design or Results / Discussion / Conclusions。
- 参考文献改用 `Definitions/mdpi.bst` 的 MDPI 编号制；历史 `webpage`
  BibTeX 类型机械转换为兼容的 `misc`，不改变文献身份。
- 加入 Author Contributions、Funding、IRB、Informed Consent、Data
  Availability、Acknowledgments/AI disclosure 与 Conflicts of Interest。
- MA-SQLGrid 明确不把多阶段流程称为多智能体，也不把严格准确率提升误写成
  更好的行内容检索。
- C2GES 明确 FEVER 是定量人工金标准，NERC 不是金标准排行榜；删除将
  simulated-expert 标签描述为专家证据的路径。

## 实验制作与完成状态

### MA-SQLGrid

- 新增 `applsci_factorial.py`，注册完整 2x2：full/compact context ×
  without/with answer-shape hints。
- 已对冻结测试集生成 **180 × 4 = 720** 个正式提示、上下文哈希和 manifest；
  状态为 `prompts_frozen_not_executed`。
- 未擅自执行外部模型调用，因为完整运行涉及 720 次付费请求。运行前需作者
  确认模型 endpoint、版本与预算。
- 仍需：对称 distractor-schema 扩展、第二独立数据库或脱敏真实库。

### C2GES

- `c2ges_learnable.py` 已支持注册的训练 K、K={1,3,5,10} 敏感性、可配置
  bootstrap 次数；新增五种子聚合入口 `run_applsci_seed_sweep.py`。
- 完成 4-question smoke run，验证训练、K 敏感性和统计产物链路。
- 完成正式 **4000/800/800** FEVER 运行与 **2000 次**文档聚类 bootstrap。
  K=3 主结果保持 F1=0.5066；相对 no-role 的新 CI 为
  [0.0020, 0.0177]，p=0.012；相对 BM25 仍不显著（p=0.451）。
- K 敏感性表已写入论文：no-role 增益在 K=3、5 有支持，在 K=1、10 的
  CI 跨零；所有 K 下均不能声称优于 BM25。
- 仍需：5 个训练随机种子、第二编码器、跨编码器/更强 reranker，以及至少
  200 个问题的双人电力专家 NERC 标注与第三人仲裁。

## 验证

- 两个新增 Python 入口均通过 `py_compile`。
- MA 2x2 dry run 成功生成 720 prompts。
- C2GES smoke 与正式主运行成功。
- 两篇稿件均通过 `pdflatex -> bibtex -> pdflatex -> pdflatex`，最终日志中
  无 undefined citation、undefined reference 或 LaTeX fatal error。
- `latexmk` 因本机没有 Perl 不可用，已用等价手动编译链完成验证。

## 投稿前必须由作者补齐

1. 两篇稿件所有作者公开邮箱。
2. 资助项目的正式 grant number，以及资助方角色声明是否准确。
3. C2GES 的永久公开代码/数据仓库 URL。
4. 确认实际作者贡献、利益冲突与 AI 使用披露措辞。
5. 提交当日重新核对 Applied Sciences 的 Section、APC、模板、Special
   Issue、数据政策和 AI 政策。本次访问 MDPI 官方页面被 HTTP 403 拒绝，
   因而没有把本地 skill 中的 2026-07 数值当作已在线复核的最新事实。
