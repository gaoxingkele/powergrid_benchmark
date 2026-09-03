# 闽投新四篇 MDPI 执行状态

**工作流：** ARS-Codex 3.19.0，pre-experiment/intake 入口  
**状态：** `WAVE_0_COMPLETE / HARNESS_V2_REGISTERED / AWAITING_PLAN_SHA_APPROVAL`  
**日期：** 2026-09-03  

> 后续状态：四篇锁定标题和作者合同预检已通过，12 阶段 v2 计划已注册但尚未获人工 SHA 批准。以 `08_HARNESS_V2_EXECUTION_PLAN.md` 和 `09_PLAN_APPROVAL_SHA256.csv` 为当前恢复入口；本文件其余内容记录 Wave 0 当时状态。

## 已锁定路线

| 论文 | 目标期刊 | 当前项目 | 新实验命名空间 | 执行状态 |
|---|---|---|---|---|
| P1 | Energies | `mintou_p5_trace_moea_feasibility_review` | `p5_s4_energies_investment_validation_v1` | 下一阶段首项 |
| P2 | Applied Sciences | `mintou_p6_bilonsga_project_review` | `p6_s4_applsci_grid_investment_v1` | 排队；SCN 安全分支不执行 |
| P3 | Energies | `mintou_p3_samode_distribution_planning` | `p3_s4_energies_samode_ac_planning_v1` | P1 后执行 |
| P4 | Electronics | `mintou_p2_hygraph_load_forecasting` | `p2_s4_electronics_hgcn_load_v1` | 先过图/HGCN 门禁 |

四个标题、作者顺序和通信作者保持作者锁定文本。`ORCID = NONE` 只作内部占位，不能作为真实编号提交。

## Wave 0 完成项

- 以当前工作树而非 Git HEAD 冻结四篇基线；记录 HEAD、相关未提交修改、关键文件哈希和预检查点项目树指纹。
- 每篇建立 `BASELINE_MANIFEST.md`、`CLAIM_EVIDENCE_REGISTER.md`、`REFERENCE_AUDIT.csv` 和 `NEXT_STAGE.md`。
- 新实验均分配独立命名空间，旧 `s3` 结果只读。
- P2 新建 Applied Sciences 电网投资主方案；SCN 网络安全方案保留为不激活备选。
- 现有参考文献仅完成数量盘点：P1 33、P2 33、P3 32、P4 30；逐条原文与元数据审计尚未开始。
- 未改动四篇科学正文、算法代码、原始结果或现有 PDF。

## 当前科学边界

- **P1：** 现有小幅 HV 优势只适用于代理基准；偏好增益未解决；缺真实成本和 AC/外部验证。
- **P2：** 现有 BiLo 对 NSGA-II 无胜场并有四个失利；双向机制归因未解决；不得改造为虚假的网络安全投资。
- **P3：** sampled/clipped HV 的 6.06% 结果受参考定义影响并会反转；自适应机制耦合；AC 检查仅示意。
- **P4：** 当前 CSA 不是 GCN/HGCN；Poincaré 权重增益未解决；DLinear 是更强的现有基线。

## 下一检查点（需作者确认后进入）

执行 P1 的投资效益验证门禁：优先检查可追溯成本和 AC/power-flow 后验验证的可行性，建立一个网络/场景、3–5 种子的最小闭环。试运行仅用于检验代码、数据和预算公平性，不能直接写入摘要或结论。

## 尚未完成

- 新实验配置和预注册统计方案尚未冻结。
- 未运行 s4 试验或正式试验。
- 未逐条核验文献，也未改写章节。
- 未执行 LaTeX 重新编译、图表一致性检查或投稿 preflight。

因此当前完成的是可恢复的执行基线，不是“论文已经符合期刊要求”的结论。
