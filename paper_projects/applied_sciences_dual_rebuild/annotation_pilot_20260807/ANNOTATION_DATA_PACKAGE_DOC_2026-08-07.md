# C2GES / MA-SQLGrid 数据标注与数据处理说明文档

**日期：** 2026-08-07
**范围：** 两篇 Applied Sciences 投稿的全部 LLM 模拟专家标注（machine-adjudicated silver labels）与相关数据处理
**治理依据：** `../LLM_API_AUTHORIZATION_AND_ADJUDICATION_PLAN_2026-08-07.md`
**工作目录：** `paper_projects/applied_sciences_dual_rebuild/annotation_pilot_20260807/`

---

## 1. 一句话结论

两篇论文的开发可见集与新建 sealed set 均已完成"双模型独立标注 + 第三模型裁决 + 确定性校验"全流程，产出带完整 provenance 账本的 **机器银标（machine-adjudicated silver labels）**。这些标签**不是真人专家金标**，论文中不得表述为 expert/human gold。

## 2. 标注体系与模型

- **标注器 A**：DeepSeek 直连 `deepseek-chat`（实际服务 `deepseek-v4-flash`，滚动别名，逐次记录）
- **标注器 B**：Google Gemini 直连 `gemini-2.5-flash`
- **裁决器 C**：OpenAI `gpt-5.4`（经 Cloubic 网关），仅裁决实质分歧
- 三家不同供应商/模型家族；temperature=0；要求单 JSON 输出；A/B 互盲；C 看到的 A/B 标签匿名化
- 确定性校验：JSON Schema、sid 存在性、qid 回显、SQLite 只读沙箱（`mode=ro` + `query_only` + authorizer 拒写 + 10s 超时 + 5000 行上限）、结果列校验
- 原始响应 append-only 账本；任何文件不落 API key（每批均程序化扫描，结果 NONE）

## 3. 协议演化（每版均冻结哈希）

| 版本 | 协议 | SHA-256（前缀） | 变更原因 |
|---|---|---|---|
| v1.0 | C2GES/MA PILOT | 030AE44A / 6D5A0398 | 初始 pilot（各 25 条） |
| v1.1 | C2GES STAGE2 | 41053D9B | 增加证据充分性准则 R1–R7；验证门未过（0.75>0.50） |
| v1.2 | C2GES STAGE2 | 40D5CC57 | 分歧分析证明主因是证据集粒度差异；改两级消解：粒度差走确定性规则（子集取小/交集共识），实质冲突才交 C；验证门通过（0.417≤0.50） |
| v1.1 | MA STAGE2 | 926A0826 | pilot 无区分度 → 增加 30 条盲测负样本控制 |
| v1.0 | MA/C2GES SEALED | FC422FEF / F1929EE6 | 阶段 3 sealed set 生成与冻结规范 |

授权记录：`STAGE2_AUTHORIZATION_20260807.json`（上限 700，实用 518）、`STAGE3_AUTHORIZATION_20260807.json`（上限 550，实用 427）。

## 4. 数据资产清单

### 4.1 C2GES（NERC 公开事件报告，文档—问题—证据句标注）

| 集合 | 规模 | 状态 | 位置 |
|---|---|---|---|
| dev 集（15 文档 × 5 角色） | 75 题 | 标注完成 | `runs/c2ges_stage2/` |
| sealed 集（nerc_001–015 × 5 角色） | 75 题 | 冻结后标注完成 | `runs/c2ges_stage3/` |

- sealed packet 集合级 sha256：`36ab3b8f…73c7`（见 `runs/c2ges_stage3/sealed_manifest.json`）
- dev 集终态：agreement 30 / 确定性消解 20 / 裁决 25 / unresolved 0
- sealed 集终态：0 unresolved、0 格式失败、0 API 失败

### 4.2 MA-SQLGrid（question–SQL 候选语义审查）

| 集合 | 规模 | 状态 | 位置 |
|---|---|---|---|
| dev 集（RTS 55 + SimBench 36） | 91 条 + 30 盲测负样本 | 标注完成 | `runs/ma_stage2/` |
| sealed 集（17 个新模板族：RS01–09 / SS01–08） | 85 条 + 30 盲测负样本 | 冻结后标注完成 | `runs/ma_stage3/` |
| 修复版候选 v2 | 3 条 | 见 §5.2 | `runs/ma_stage2/candidate_fixes_v2.jsonl` |

- sealed 题库集合级 sha256：`5d1ed4ea…5dc3`（见 `runs/ma_stage3/sealed_manifest.json`）
- 原始 91 条候选文件**未做任何改动**；修复以独立 v2 产物存在

## 5. 核心结果

### 5.1 标注一致性

| 指标 | C2GES dev 75 | C2GES sealed 75 | MA dev 121 | MA sealed 115 |
|---|---|---|---|---|
| 主标签一致率 | 0.853（answerable） | 0.973 | 0.926 | 0.878 |
| Cohen's κ | 0.132* | — | 0.764 | 0.668 |
| 证据 exact / Jaccard | 0.413 / 0.599 | 0.24 / 0.631 | — | — |
| Tier-2 裁决率 | 0.333 | 0.173 | 0.107 | 0.148 |
| 格式/API 失败率 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

*C2GES κ 低是边际分布极端偏斜（几乎全部 answerable=true）所致，kappa 在此无区分度，报告原始一致率为准。

### 5.2 MA 候选质量结论

- dev 91 条：**88 条通过**，3 条判语义错误——SB-AUTO-005、SB-AUTO-014、RTS_AUTO_047
- 修复重标注：SB-AUTO-005 修复版通过；**SB-AUTO-014 与 RTS_AUTO_047 修复版仍判 false**（前者暴露裁决器对"分布式机组"语义的前后不一致；后者是问题文本歧义，机器裁决无法收敛）
- **处理建议（已执行）：人工修订/确认前，这 3 条不得进入任何 benchmark 声明**
- sealed 85 条：83 条通过，RTS_SEALED_033/043 判 false（"措辞写了 spinning 但 SQL 未显式过滤"，与 RTS_AUTO_047 同源问题），同样需人工复核

### 5.3 标注器可靠性（负样本盲测）

| 扰动族 | dev 检出率 | sealed 检出率 |
|---|---|---|
| wrong_filter_value | 1.00 | 1.00 |
| wrong_aggregation | 1.00 | 1.00 |
| drop_order | 1.00 | 1.00 |
| drop_filter | 0.89 | 1.00 |
| wrong_column | **0.30** | 0.75 |
| **总体** | 0.733 | 0.933 |

- 发现标注器系统性漏检"SELECT 列偷换"→ 增加**确定性列校验防线**（执行结果列 vs 期望列比对）
- **标注器 + 列校验联合覆盖：dev 29/30 = 0.967，sealed 30/30 = 1.000**；两层互补（列校验捕获全部 wrong_column，标注器捕获列校验覆盖不了的语义类）

## 6. 已知限制（论文局限性章节可直接引用的事实）

1. 全部标签为机器银标；无真人专家复核门禁；不能声称专家金标或 external gold accuracy。
2. C2GES 证据集完全一致率偏低（0.24–0.41）：两个标注器在"最小充分证据集"粒度上有系统性差异，已由 v1.2 确定性规则消解，Jaccard（0.60–0.63）更能反映实质一致性。
3. MA 标注器单独使用时对列偷换错误漏检率高（0.30–0.75），必须配合确定性列校验使用。
4. 裁决器 C 在 SimBench"分布式机组"语义上出现过前后不一致的裁决（SB-AUTO-005 vs SB-AUTO-014），相关条目已隔离待人工确认。
5. RTS_AUTO_047 / RTS_SEALED_033 / RTS_SEALED_043 暴露"问题措辞严格性"缺陷：自然语言提到过滤条件而 SQL 依赖表内容巧合满足，需人工修订问题文本。
6. DeepSeek 滚动别名（deepseek-chat → 实际 deepseek-v4-flash）属版本漂移，已逐次记录；跨时段复跑需注意。

## 7. 论文表述边界

**可以写：** dual-model independent annotation with third-model adjudication and deterministic validation（含沙箱执行与列校验）；报告一致率、Jaccard、裁决率、负样本检出率；sealed set 的先冻结后标注流程与哈希。

**不可以写：** human/expert gold、expert-annotated、人工准确率；不得隐去负样本检出率与列校验依赖；不得把修复 v2 说成原始候选。

MDPI GenAI 披露模板见治理文档第九节；若无真人抽检，删去其中 "human-review procedures" 措辞。

## 8. 文件索引

```
annotation_pilot_20260807/
├── 协议（冻结）：C2GES/MA ANNOTATION_PROTOCOL v1.0/v1.1/v1.2、SEALED_SET_PROTOCOL v1
├── 授权：STAGE2/STAGE3_AUTHORIZATION_20260807.json
├── run_annotation_pilot.py        # 标注运行器（--stage2/--stage3，协议哈希自检，预算门禁）
├── build_sealed_packet.py         # C2GES sealed 组包
├── build_ma_sealed_set.py         # MA sealed 题库生成
├── generate_negative_controls.py  # 盲测负样本生成
├── column_check.py                # 确定性列校验
├── fix_candidates_v2.py           # 3 条问题候选修复
├── PILOT_REPORT.md / STAGE2_REPORT.md / STAGE3_REPORT.md   # 各阶段详细报告
└── runs/
    ├── c2ges_pilot/  ma_pilot/            # 阶段 1（各 25 条）
    ├── c2ges_stage2/ ma_stage2/           # 阶段 2（75 / 91+30）+ 修复 v2 + 列校验报告
    ├── c2ges_stage3/ ma_stage3/           # 阶段 3 sealed（75 / 85+30）
    └── _smoke_archive_20260807/           # 冒烟归档（不计入正式统计）
```

每套 runs 目录含：sample_manifest（含盲化映射）、raw_ledger（append-only 原始调用）、labels_A/B、adjudicated、final_labels、stats.json；sealed 目录另含 sealed manifest（冻结哈希）。

## 9. 复现方法

```bash
cd paper_projects/applied_sciences_dual_rebuild/annotation_pilot_20260807
# 环境：.env（DEEPSEEK/GEMINI key）与 .env.cloubic（CLOUBIC key）在仓库根目录
python run_annotation_pilot.py --stage2 c2ges   # C2GES dev 75
python run_annotation_pilot.py --stage2 ma      # MA dev 91+30
python run_annotation_pilot.py --stage3 c2ges   # C2GES sealed 75
python run_annotation_pilot.py --stage3 ma      # MA sealed 85+30
python column_check.py --stage3                 # 列校验
```

运行器会先校验协议文件 SHA-256，不匹配即拒绝执行；sealed 集先验冻结哈希再允许标注。

## 10. 作者决定记录（2026-08-07 更新）

1. ~~人工确认/修订 5 条隔离条目~~ → **作者已于 2026-08-07 确认**（维持隔离处置：SB-AUTO-014、RTS_AUTO_047、RTS_SEALED_033、RTS_SEALED_043 不进入 benchmark 声明；SB-AUTO-005 修复版可用）。
2. ~~真人抽检~~ → **作者决定不安排真人复核，论文也不作相关声明**；全部标签维持 machine-adjudicated silver 表述。
3. ~~BIRD 授权~~ → **已签署**：批准人 DONG LUN HAI，2026-08-07；见 `../HUMAN_ACTION_PACKET.md` 第 3 节与 `../MA_SQLGrid/human_launch_approval_bird_20260807.json`。
4. 稿件集成与三轮评审（本次未动稿件）。
