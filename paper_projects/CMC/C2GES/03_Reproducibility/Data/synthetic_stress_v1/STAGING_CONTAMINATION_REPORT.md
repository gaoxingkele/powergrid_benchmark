# v2r13 矛盾点调查报告（staging 污染实证）

日期：2026-09-27。结论：**v2r13 的 s05/s09 四篇不是同架构的诚实样本——它们是
单测 MockCoreBackend 产物经 staging 污染混入的**；E1b/E2 未过全部是污染解释，
不需要任何协议/架构裁决。s08/s12 三篇（fresh）与 s12_r01（v2r12 生成）为真实样本。

## 1. staging 5 篇 arch 标签链（逐篇来源）

| doc_id | generator_model | created_at | 真实来源 |
|---|---|---|---|
| s05_r01 | **mock-deepseek** | 08:16:48 | **TestDualPlan 单测（mock 核）** |
| s05_r02 | **mock-local** | 08:16:48 | **TestDualPlan 单测（mock 核）** |
| s09_r01 | **mock-deepseek** | 08:16:48 | **TestDualPlan 单测（mock 核）** |
| s09_r02 | **mock-local** | 08:16:48 | **TestDualPlan 单测（mock 核）** |
| s12_r01 | deepseek-chat | 08:18:36 | v2r12 真实生成（真实样本） |

v2r13 fresh 3 篇：s08_r01（DeepSeek，08:30:27）、s08_r02（本地 27B，08:32:59）、
s12_r02（本地 27B，08:29:48）——均真实生成。

**污染链**：staging 特性加入 run.py 后，既有 `TestDualPlan`（tests/test_synth_c2ges_p2.py）
monkeypatch 了 `make_backend`/`RUNS_DIR` 但**未 monkeypatch `staging.STAGING_DIR`**，
单测用 MockCoreBackend 生成的 4 篇 mock 核写入了生产 staging 目录
（`data/synthetic/c2ges/_staging/parent_v2/`）。`load_artifact` 的 arch 标签是代码版本
（c2ges-arch-v3-pools1，mock 核同样满足 schema 校验）而非来源凭证 → 复核通过 →
v2r13 组装时把 4 篇 mock 核当作真实报告使用。

mock 核铁证（staging artifact 内文本）：
- s09_r01 首句 "The primary cause was a miswired test switch at Synthetic Ridge
  Substation 3 left in the test position..."（mockcore.py `_ROLE_TEXT['root_cause']` 模板原文）；
- seeds "Background note 1-0: synthetic channel 21 held nominal readings during
  routine interval 13..."（mockcore.py 种子模板原文）。

## 2. E2 口径一致性

pilot9 与 v2r13 使用**同一 gates.py**（anchor_tokens 切词、全篇统计含尾签，
两跑次间 gates.py 无改动）；扩展代码同为 arch-v3-pools1（词池/尾签/骨架公式一致）。
**口径无差异；差异全部来自核的 provenance**（真实 DeepSeek 核 vs mock 模板核）。

## 3. s09 E2 归因（pilot9 vs v2r13 描述统计）

| 指标 | pilot9 s09_r01（真实 DeepSeek 核） | v2r13 s09_r01（mock 核） |
|---|---|---|
| distinct-2 | **0.5782** | **0.3769** |
| unique bigrams | 8,339 | 5,442（−35%） |
| total bigrams | 14,423 | 14,439 |
| 骨架条数 | 55 | 28（mock 固定 14 模板 ×2 批） |
| 种子条数 | 36 | 33 |
| 核句作者文本词数 | 398 | 338 |

归因：确定性机械（词池/尾签/骨架公式）两边完全一致；mock 核的核句只有 5 个固定
模板、骨架只有 14 个固定模板，作者文本多样性坍缩 → unique bigrams −35%。

## 4. s05/s09 核近重复量化

- s05_r02 vs s09_r02 核 bigram Jaccard = **0.3087**（|∩|=71, |∪|=230）
- 对照 s08_r01（真实 A 族）vs s09_r02 = **0.0082**

mockcore._make_report 用 5 个固定 ROLE_TEXT 模板 + 随机数生成任意"核"——任意两个
mock 核天然共享 ~31% bigrams。staging 复用把这对 mock 核分别放到 s05_r02 与 s09_r02，
E1b 文档可分性随之坍缩（s05_r02 = 0.7895，全场唯一未过篇）。

## 5. 处置建议（供父代决策，本次未执行）

1. 删除 4 个污染 staging 制品（或给 `load_artifact`/`save_artifact` 加生成器族
   白名单：拒绝 `mock*` provenance 入生产 staging）。
2. 测试卫生修复：所有经 run() 的单测一律 monkeypatch `staging.STAGING_DIR` 到
   tmp_path（TestDualPlan 及后续）。
3. 按统一最终架构**重新生成** s05_r01、s05_r02、s09_r01、s09_r02 四篇
   （配置一致性修正而非 Goodhart：被替换的是测试污染产物，不是门低分样本；
   staging 的 s08/s12 真实样本全部保留复用，留痕于 DECISION.md）。


## 附录 A：污染制品删除记录（2026-09-27，父代批准的配置一致性修正）

经 Python shutil.rmtree 逐条执行并打印确认：

- deleted: synthetic_s05_r01（mock-deepseek，TestDualPlan 产物）
- deleted: synthetic_s05_r02（mock-local，TestDualPlan 产物）
- deleted: synthetic_s09_r01（mock-deepseek，TestDualPlan 产物）
- deleted: synthetic_s09_r02（mock-local，TestDualPlan 产物）

删除后 staging 剩余（均为真实生成样本，保留复用）：
synthetic_s08_r01（DeepSeek, v2r13 fresh）、synthetic_s08_r02（本地27B, v2r13 fresh）、
synthetic_s12_r01（DeepSeek, v2r12 fresh）、synthetic_s12_r02（本地27B, v2r13 fresh）。
