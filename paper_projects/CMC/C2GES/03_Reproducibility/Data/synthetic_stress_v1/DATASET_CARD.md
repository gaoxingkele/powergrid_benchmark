# Dataset card — GenData × C²GES 合成电网事故报告压力测试集（parent-v3r1 + heldout-v2r3）

日期：2026-09-28。协议：`docs/PROTOCOL_synthetic_c2ges_gendata_v1.md`
（SHA-256 `daf7c969…19c8`，冻结记录见 `docs/FREEZE_RECORD.json`）。
声明：**SYNTHETIC_STRESS_NONCONFIRMATORY**；所有记录 `confirmatory_claims_allowed=false`。

## 1. What this asset is

两套虚构电网事故报告数据集（合成压力测试 fixture，绝非真实事件）：

| 数据集 | 跑次目录 | 系列 × 篇 | 主题 | 生成器指派 |
|---|---|---|---|---|
| parent（child 修订后） | `run_20260927_parent-v3r1/` | 4 × 2 | s05/s08/s09/s12 | r01=DeepSeek（A 族），r02=本地 Qwen3.8-27B（B 族） |
| held-out | `run_20260927_heldout-v2r3/` | 4 × 2 | s01/s03/s04/s11（THEMES 池从未使用的 4 个） | A↔B 交换（r01=本地、r02=DeepSeek）+ prompt v3 变体 |

每篇记录（`synthetic_reports.jsonl`）：`doc_id, split="synthetic_stress", synthetic=true,
candidate_sentences[{sid,text,page,unit_type,synthetic_ground_truth_role,synthetic_stress_tags}],
reference_summary, reference_unit_ids, provenance{generator_model,run_id,seed,protocol,protocol_sha256}`。
语义核（含因果 DAG 与优先级）随跑次存于 `semantic_cores.json`。

## 2. What ships, and what does not

| Shipped（本仓 GenData 侧） | Not shipped |
|---|---|
| 两个跑次目录（JSONL/门账本/原始响应/清单/DECISION/评审） | 真实语料指纹库与嵌入（`data/anchors/`，仅本地门评估用，不入发布包） |
| 冻结协议与 FREEZE_RECORD | C²GES 仓任何文件（全程只读） |
| 本卡片与交接手册（`docs/HANDOFF_synthetic_c2ges.md`） | 任何"与真实等价"的声称（协议红线） |

## 3. How to rebuild it

```bash
# 门复算（任一跑次）
python -m gendata.synth.c2ges.run --backend mock --plan dual --series 1 \
    --version smoke-check  # mock 干跑验证管线（不进 staging 白名单外的生产路径）
# 真实复算门账本：
#   读跑次目录 evaluation/gate_ledger.json；重算用 gendata.synth.c2ges.gates.evaluate_all
# C²GES 侧复算（只读调用其评估器，输出落 GenData 侧）：
python <C²GES>/03_Reproducibility/Code/prospective_v1/evaluate_synthetic_distribution.py \
    --dataset <run>/synthetic_reports.jsonl --metadata-csv <rights_safe_metadata.csv> \
    --layout-csv <layout_candidate_audit.csv> --output <run>/evaluation/c2ges_crosscheck
```

生成器接入：A 族 DeepSeek 经 `.env`（`DEEPSEEK_API_KEY/DEEPSEEK_BASE_URL/DEEPSEEK_MODEL`，
密钥仅内存）；B 族本地 KoboldCPP（`tools/koboldcpp.exe --model models/Qwen3.8-27B-Uncensored-Q4_K_M.gguf
--port 8080 --contextsize 16384 --gpulayers 99 --quiet`）。
新跑次：`python -m gendata.synth.c2ges.run --backend deepseek --plan dual --series 4
--version <新版本> --seed <种子>`（held-out 形态加 `--series-list/--swap-ab/--prompt-variant/--staging-tag`）。
断点续跑：`data/synthetic/c2ges/_staging/<tag>/` 篇级缓存，arch 标签一致且复核通过才复用。

## 4. Intended use, and misuse

**Intended.** 解析器/schema/长文档内存与运行时的软件压力测试；E3 表格与统计管线的
干跑实现；端点与种植结构对齐的机制诊断（全部在 SYNTHETIC_STRESS_NONCONFIRMATORY 声明下）。

**Misuse.** 不得替代 E1 未见系列；不得替代 E2 真人标注或训练标注者；不得报告论文性能
估计；不得支撑伦理/运维收益/外部效度声称；AUROC/KS 不显著或落于参考带≠与真实等价。
合成线任何结果不进 E1/E2/E3 确认性证据链。

## 5. 门账本摘要（全门 19/19，两跑次均过）

| 门族 | parent-v3r1 | heldout-v2r3 |
|---|---|---|
| S1–S8 结构 | 全过（S7 零命中、S2 逐字、DAG 无环） | 全过 |
| D1/D2/D3 | 0.208 / 0.1311 / 0.0002 | 0.208 / 0.1311 / 0.0002 |
| D4/D5/D7 | 0.0004 / 0.1885 / ≤0.25 | 0.0 / 0.1745 / ≤0.24 |
| D8 泄漏 | 0.12（≤0.15，命中占比 0.04%≤2%） | 0.0625 / 0% |
| D9 模板族 | ≥408 族/篇、单族 ≤0.9% | ≥415 族/篇、≤0.5% |
| E1b 自洽 | min 0.894 | min 0.875 |
| E2 distinct-2 中位 | 0.586 | 0.581 |
| E3 词表重合 | 0.675 | 0.627 |

C²GES 侧 `evaluate_synthetic_distribution.py` 复算（两跑次
`evaluation/c2ges_crosscheck/`）：其 6 门全过，D1/D2/D3/D4 与本地账本逐位一致。
双评审（咨询性）：两跑次均本地 27B accept + 手工替代 accept，逐维 |Δ| 全 ≤1、裁决一致。
生成期 D8 预检（arch-v4-d8guard 起为生成规格）：两跑次拒收 0 句。

## 6. Known limitations

1. **纹理残留（minor，双评审一致记录）**：干扰句的子句装配接缝与括号数值尾签
   在文本层面可见；D9/E2 均过门，属压力测试 fixture 的可接受特征。
2. **E1 描述性指标**：AUROC(syn-vs-real)=0.998（远高于真实 LORO 带 [0.929,0.948]）——
   单元级分类器测"文档身份"而非"真实性"（协议 §0.1）；不构成等价性证据。
3. **大报告 E2 偏低**：703 单元报告逐篇 distinct-2 ≈0.45（冻结门为中位判定，已按
   父代裁定执行；逐篇值只报告）。S8 种子窗（24–36 条/篇）冻结是硬约束。
4. **生成器合规方差**：本地 27B 长 JSON + 多约束输出需要校验-回填重试（全部落盘、
   有日志）；v3 链已用拆分调用 + 计数归一化把停跑率降到零，但重试仍是常态。
5. **可见性史**：parent 线（v2final/v3/v3r1）看过中间门结果后做过生成器侧调优
   （阈值从未改动）；heldout-v2r3 是未用主题 + 换族 + prompt 变体的独立检验，全门通过。
6. **staging 污染事件**：v2r13 曾混入单测 mock 核（已根因修复：删除+白名单+测试隔离，
   见 `STAGING_CONTAMINATION_REPORT.md`）；本卡片两跑次不含任何 mock 产物
   （manifest 逐篇 source/core_sha256 可审计）。

## 7. 血缘与引用

血缘链：P1 pilot（pilot-v1r6 首过全链）→ P2 parent-v2final → v3 parent-v3 →
**parent-v3r1（child，终裁修订 s09_r01）**；heldout-v1r5（D8 未过，历史记录保留）→
**heldout-v2r3（通过）**。各代失败跑次 FAILURE_RECORD 与原始响应全部保留于
`data/synthetic/c2ges/run_*/`。

引用方式：引用本卡片 + 协议版本（synthetic_c2ges_gendata_v1, sha256 daf7c969…）+
跑次目录名与各自 SYNTHETIC_RUN_MANIFEST.json 的 SHA-256 清单。
