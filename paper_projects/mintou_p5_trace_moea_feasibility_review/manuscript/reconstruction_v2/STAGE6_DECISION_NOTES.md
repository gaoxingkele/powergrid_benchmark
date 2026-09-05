# P1 Stage-6 阻塞处置决策（作者决定，2026-09-05）

**本文件是 s06 重跑的执行器输入。** 决策由作者明确作出，执行器据此修订证据绑定值并重跑正式实验。

## 决策 1：环境重冻结（NERC 无关，机械修订）

s04 冻结的 NumPy 1.26.4 / SciPy 1.12.0 与可用运行时（Python 3.14，NumPy 2.4.6 / SciPy 1.18.0）不兼容，冻结值本身不可执行。

**处置：** 将 `experiments/p5_s4_energies_investment_validation_v1/environment.json` 重冻结为实际安装版本（numpy 2.4.6 / scipy 1.18.0 / python 3.14），作为**证据绑定值的运行前修订**，更新对应哈希并记录修订日志（revision reason: "frozen versions incompatible with available Python 3.14 runtime; author-approved re-freeze 2026-09-05"）。此修订不得改动臂、种子索引、计算上限、指标规则、比较族、校正或失败/负结果政策（协议 §6 允许）。

## 决策 2：NERC 元数据处置 —— 方案 A（作者选定）

**处置：** 代理池中源自 NERC 文档元数据的属性，改用开放许可来源重新推导：

- 首选 RTS-GMLC（CC-BY）与 SimBench（开放数据）对应属性；
- 重推导过程、来源 URL、许可与变换公式逐项记录进 `data_manifest.json`（provenance 字段）；
- NERC 文档仅保留 URL 引用，不再派生/再分发属性；
- legacy 已冻结的 120 项目池与全部历史结果保持只读不动——重推导只作用于新正式实验命名空间（`p5_s4_*`），历史对比在论文中以预注册历史保留。

## 决策 3：s06 重跑

- 0/900 运行的候选不构成正式实验完成形态；拒绝后按上述两决策重跑 `p1_v2_s06_formal_experiments_statistics`。
- 重跑必须产出：运行清单、原始结果、主要结果、负结果表、失败账本、统计审计与最终主张证据（08 号计划 §5）。
- 全部 18 个预注册对比按冻结协议估计；不得因历史 0.89%/0.17% 结果选择性地报告任何家族。
