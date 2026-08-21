# C2GES 与 MA-SQLGrid 论文补充材料需求清单

日期：2026-07-19
背景：两篇论文正在按 SCI 开放获取期刊标准升级（C2GES → IEEE Access；MA-SQLGrid → MDPI Electronics 首选 / IEEE Access 备选）。手稿修改、DeepSeek 第二模型对照实验（540 次调用 + 1080 次一致性检查）等已完成；剩余的实验强化被以下缺失文件阻断。这些文件应该都在原实验机器（Linux，路径含 `/media/lenovo/data2/cja/...`）上。

---

## 一、C2GES（最高优先级）

原机器参考根路径（来自实验元数据 `source_asset_root`）：

```
/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/paper_workspace/workspaces/c2ges-evidence-audit-krill/
```

### 1. 数据集工作区（最关键）

```
verification_pilot/agent_audit_40doc/
```

应包含：

- 40 份句子切分后的 `nerc_*.json`（句子级语料）
- 每文档 5 个因果角色问题（共 200 题）
- 证据句 ID 标签（608 个 evidence ID）
- `manifest.json`

**用途**：解锁已备好的三个基线实验（LLM zero-shot / cross-encoder / bge-reranker，脚本已写好并烟测通过，拿到数据当天可出结果）。这是 C2GES 达到 IEEE Access 实验强度门槛的最后一块。

说明：40 份 NERC 原始 PDF 及官方 URL 映射已在项目中缓存（`data/public_datasets/reliability_reports/c2ges_nerc_reports/`），**不需要**再传 PDF，只需要上面的加工产物。

### 2. 流水线脚本与配置

```
verification_pilot/scripts/run_baselines.py
verification_pilot/scripts/run_c2ges.py
three-pack/config.yaml
```

**用途**：使包内 `main.py` 可独立复现完整实验。

### 3. 主 Executor 工件

```
c2ges_role_selective_graph/
├── summary.json
├── details.jsonl
├── cv_protocol.json
├── heldout_predictions.jsonl
└── metadata.json（如有）
```

**用途**：论文 Table 3 中部分弱基线行与 Table 4 部分消融配对统计目前包内无凭据（补充材料 summary.json 已覆盖 7 个条件的主对比，但其余行仍需此工件）。这是评审指出的 P0 级复现缺口。

### 放置位置

拷贝到 Windows 工程机的：

```
D:\aicoding\powergrid_benchmark\paper_projects\2026_c2ges_engineeringletters\
```

按原目录名放即可（详见同目录 `MISSING_ARTIFACTS.md`）。打 zip 发回也可以。

---

## 二、MA-SQLGrid（次优先，仅冲 IEEE Access 时需要）

### 缺失的两个 Python 模块

```
dev_chess_style_pilot/        （C4/C5 紧凑上下文构建模块）
smoke.py                      （含 BASE_URL / MODEL_NAME / WIRE_API 定义）
```

原位置应在 MA-SQLGrid 实验工作区中，`experiment_final/main.py` 通过 `import smoke` 和 `dev_chess_style_pilot` 引用它们。

**用途**：解锁两个已备好的扩展实验——

1. ×10 扩大数据库重跑（`griddb_maintenance_v2_x10` 已构建完成，gold SQL 全部验证通过，只差为新库生成 C4/C5 紧凑上下文）；
2. Spider/BIRD 公开基准子集迁移探针（消除"toy benchmark"审稿风险的关键实验）。

说明：若最终只投 MDPI Electronics，这两项非必需（现有双模型证据已超该刊录用样本的常态水平）；若投 IEEE Access，强烈建议补齐。

### 放置位置

```
D:\aicoding\powergrid_benchmark\paper_projects\2026_ma_sqlgrid_cmc\source\code\experiment_final\
```

---

## 三、已完成事项（供了解进度，无需操作）

- MA-SQLGrid：DeepSeek 第二模型对照完成（紧凑上下文增益 +36.1pp 复现且更大；判分约定敏感性成为跨模型发现；直连端点真实 token 节省 74.7%）；3 次重复一致性检查完成（判定一致率 98.3%）；全部已写入手稿。
- C2GES：手稿按 IEEE Access 标准完成一轮修改（循环性讨论、透明性定位、文献补充等）；补充材料中的角色分层指标与 10000 次 bootstrap 配对比较正在写入正文。
- 两篇的评审评估报告见各自目录下 `PUBLICATION_ASSESSMENT.md`，修改台账见 `SCI_UPGRADE_CHANGELOG.md`。

## 四、其余待办（非本清单范围）

作者信息（姓名/单位/ORCID/通讯邮箱/基金号）、代码仓库发布方式（GitHub release 或 Zenodo DOI）、LaTeX 编译验证。
