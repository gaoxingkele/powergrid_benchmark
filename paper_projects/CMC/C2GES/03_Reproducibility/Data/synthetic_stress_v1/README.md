# C²GES 合成电网事故报告压力测试集 — 使用说明

> **声明**：本数据集为 **SYNTHETIC_STRESS_NONCONFIRMATORY**（合成压力测试 fixture），
> 所有记录 `confirmatory_claims_allowed=false`。**它不是、也不能替代真实语料证据**。
> 完整边界见同目录 `DATASET_CARD.md`；协议与冻结哈希见 `../../docs/PROTOCOL_synthetic_c2ges_gendata_v1.md`。

## 1. 这是什么

两套虚构电网事故报告数据集（共 16 篇），用于对 C²GES 论文的解析器 / schema /
长文档内存 / 表格统计管线做**软件层面的压力测试与机制诊断**：

| 数据集 | 目录 | 规模 | 主题 | 生成器指派 |
|---|---|---|---|---|
| parent | `run_20260927_parent-v3r1/` | 4 系列 × 2 篇 | s05/s08/s09/s12 | r01=DeepSeek，r02=本地 Qwen3.8-27B |
| held-out | `run_20260927_heldout-v2r3/` | 4 系列 × 2 篇 | s01/s03/s04/s11 | A↔B 交换 + prompt 变体 |

两套均通过全部 19 道冻结确定性门（结构 S1–S8、分布 D1–D5/D7–D9、
词汇 E1b/E2/E3）+ 双评审一致 accept + C²GES 官方评估器复算逐位一致。

## 2. 目录导航

```
data/synthetic/c2ges/
├── README.md                      ← 本文件
├── DATASET_CARD.md                ← 数据集卡片（用途边界/门账本/血缘/已知限制）
├── run_20260927_parent-v3r1/      ← 【发布】parent 数据集
│   ├── synthetic_reports.jsonl    ← 8 行 = 8 篇报告（核心数据文件）
│   ├── semantic_cores.json        ← 语义核（因果 DAG、角色、优先级）
│   ├── evaluation/gate_ledger.json← 门账本（逐门 threshold/measured/pass）
│   ├── evaluation/c2ges_crosscheck/ ← C²GES 官方评估器复算输出
│   ├── SYNTHETIC_RUN_MANIFEST.json← SHA-256 清单 + 逐篇血缘
│   ├── raw_responses/             ← 全部 LLM 原始响应（审计用）
│   └── DECISION.md                ← 验收决策记录
├── run_20260927_heldout-v2r3/     ← 【发布】held-out 数据集（结构同上）
└── run_2026092*-*/                ← 历史/失败跑次（留档审计，勿用于实验）
```

**只用上面两个标【发布】的目录**，其余是过程留档。

## 3. 快速开始

### 加载数据

```python
import json

RUN = "data/synthetic/c2ges/run_20260927_parent-v3r1"
reports = [json.loads(l) for l in open(f"{RUN}/synthetic_reports.jsonl", encoding="utf-8")]

for r in reports:
    print(r["doc_id"], len(r["candidate_sentences"]), "个候选单元")
```

### 记录结构（每篇报告一行 JSONL）

| 字段 | 含义 |
|---|---|
| `doc_id` / `report_series_id` | 篇 ID / 系列 ID（同系列 2 篇共享事件主题） |
| `title` | 报告标题（全部虚构，设施名一律 `Synthetic` 前缀） |
| `candidate_sentences` | 候选单元列表（170–703 个/篇），见下表 |
| `reference_summary` | 参考摘要（110–180 词） |
| `reference_unit_ids` | 参考摘要对应的单元 sid 列表（摘要=这些单元拼接，逐字相等） |
| `lexical_regime` | `ambiguous` / `paraphrased`（词汇难度档位） |
| `provenance` | 生成器模型、跑次、种子、协议哈希 |
| `split` / `synthetic` / `confirmatory_claims_allowed` | 固定 `synthetic_stress` / `true` / **`false`** |

### 候选单元结构（`candidate_sentences[i]`）

| 字段 | 含义 |
|---|---|
| `sid` | 单元 ID（如 `u00018`），被 `reference_unit_ids` 引用 |
| `text` | 单元文本（句级） |
| `page` | 页码（版面分布对齐真实锚点） |
| `unit_type` | 版面类型：`body` / `caption` / `table` / `heading` / `list` / `footnote` |
| `synthetic_ground_truth_role` | **合成真值角色**：`cause` / `failure` / `impact` / `mitigation` / `timeline` 或 `distractor`（干扰句） |
| `synthetic_stress_tags` | 压力标签（如 `distractor_family:frame`、`deterministic_layout_distractor`） |

### 典型用法

**① 解析器/schema 压力测试**：直接喂给管线，验证长文档（703 单元/篇）、
多版面类型、因果 DAG 结构的处理不崩。

**② 抽取/摘要机制诊断**：用 `synthetic_ground_truth_role` 作已知真值，
测量你的抽取器对五类核心角色 vs 干扰句的区分能力；
用 `reference_unit_ids` → `reference_summary` 验证摘要一致性逻辑。

**③ 复算门账本**：

```python
from gendata.synth.c2ges.gates import evaluate_all  # 见 docs/HANDOFF_synthetic_c2ges.md
```

**④ C²GES 官方评估器复算**（只读调用其仓，输出落本侧）：

```bash
python <C²GES仓>/03_Reproducibility/Code/prospective_v1/evaluate_synthetic_distribution.py \
    --dataset <run>/synthetic_reports.jsonl \
    --metadata-csv <rights_safe_metadata.csv> \
    --layout-csv <layout_candidate_audit.csv> \
    --output <run>/evaluation/c2ges_crosscheck
```

## 4. 使用红线（务必遵守）

1. **不得**用本数据集支撑任何"与真实语料等价"的声称（AUROC/KS 落带 ≠ 等价）。
2. **不得**进 C²GES 论文 E1/E2/E3 确认性证据链；不得报告论文性能估计。
3. **不得**替代真实未见系列（E1）、真人标注（E2）或伦理/运维收益论证。
4. 引用时标注：`SYNTHETIC_STRESS_NONCONFIRMATORY` + 协议版本
   （`synthetic_c2ges_gendata_v1`, sha256 `daf7c969…19c8`）+ 跑次目录名。

## 5. 已知限制（使用前请读）

1. **文本纹理可见**：干扰句是"LLM 骨架 + 确定性槽位填充"装配产物，
   接缝处有生硬/破语法片段（如 `[16:52 ch1 parameterized item 6 5hz …]` 尾签）。
   这是压力测试 fixture 的可接受特征（D9/E2 均过门），但**别拿它当自然英文散文用**。
2. **与真实语料极易区分**：E1 描述性 AUROC = 0.998——任何嵌入分类器都能
   一眼分出合成/真实。这是预期行为（测的是文档身份），但也意味着
   本数据集**不能**用于"骗过"或等价替代真实分布的场景。
3. **规模小**：每套 8 篇，用于压力测试与机制诊断足够，用于统计推断不够。
4. **大报告词汇多样性偏低**：703 单元报告逐篇 distinct-2 ≈ 0.45
  （冻结门按 8 篇中位判定，已过；逐篇值见门账本）。
5. **血缘知情**：parent 线经历过生成器侧调优（阈值从未改动）；
   held-out 线（换主题+换生成器分工+换 prompt）独立全门通过。
   staging 污染事件及修复见 `STAGING_CONTAMINATION_REPORT.md`。

## 6. 增量生成与扩展

- 新跑次入口：`python -m gendata.synth.c2ges.run --backend deepseek --plan dual ...`
  （完整参数见 `docs/HANDOFF_synthetic_c2ges.md`）
- **THEMES 主题池 12 个已用尽**（parent 4 + heldout-v1 4 + heldout-v2 4）。
  再扩规模须先扩充虚构主题池，否则 held-out 无新主题可用。
- 断点续跑缓存 `_staging/<tag>/`：arch 标签一致且复核通过才复用；
  门结果驱动的重抽样是 Goodhart，被纪律禁止。
