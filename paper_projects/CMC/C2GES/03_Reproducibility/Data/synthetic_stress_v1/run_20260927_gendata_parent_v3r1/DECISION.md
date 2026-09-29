# DECISION（parent-v3r1：**最终候选数据集（child 修订完成）**）

日期：2026-09-28。跑次：`run_20260927_parent-v3r1`（parent-v3 的 child：仅修订 s09_r01）。
协议：synthetic_c2ges_gendata_v1（sha256 daf7c969…19c8，冻结，未动阈值）。
声明：SYNTHETIC_STRESS_NONCONFIRMATORY；confirmatory_claims_allowed=false。

## 裁决：**ACCEPT（accept_for_synthetic_stress_only）——v3 链最终候选**

### 修订原因（parent-v3 评审 nit）

parent-v3 本地评审（revise）指出 s09_r01 的数值一致性 nit："94% of 8.6 MVA 馈线 vs
12.4 MW 放电"——视在/有功混用且负载超过馈线额定。用户终裁：child 修订该篇。

### 修订内容

- 仅重新生成 s09_r01 语义核（A 族 DeepSeek；断点续跑只动这 1 篇，其余 7 篇
  staging 复用，manifest 逐篇 source 与 core_sha256 可查）；
- prompt 附加修订指令（critic_amendment 槽）：百分比与其基数一致、MVA/MW
  不混用（除非声明功率因数）、负载不超过馈线额定、时序先后一致；
- 其余约束与生成配置逐项不变（arch-v4-d8guard、种子 20260926、骨架公式、
  词池/尾签/D8 预检/S7 后滤全部同 parent-v3）。

### 修订前后账本对照

| 指标 | parent-v3 | parent-v3r1 | 变化 |
|---|---|---|---|
| 全门 | 19/19 ✅ | 19/19 ✅ | 保持 |
| D8 max Jaccard | 0.0769 | 0.12 | 略升（仍 ≤0.15，hit_share 0.04%） |
| E1b min | 0.8458 | 0.894 | 改善 |
| E2 中位 | 0.589 | 0.5857（s09_r01 逐篇 0.5745→0.5678） | 保持 |
| E3 | 0.6741 | 0.6752 | 保持 |
| D8 预检拒收 | 0 | 0 | — |

### 双评审（修订后重跑）

- 本地 27B：**accept_for_synthetic_stress_only**（4/4/3/4/3），数值张力 nit 消失；
- 手工替代评审（Codex CLI 仍 401）：**accept**（4/4/4/4/3）；
- 逐维 |Δ| 全 ≤1（仅 lexical_diversity 差 1），裁决一致 accept/accept，无 major。

### 验收链 §6 全项状态

| 判据 | 状态 |
|---|---|
| parent 全确定性门 | ✅ parent-v3r1 |
| 双评审均 ≥ accept 且无 major | ✅（本跑次） |
| held-out 同门通过 | ✅ heldout-v2r3 |
| C²GES 侧复算一致 | ✅ 两跑次逐位一致（见各自 evaluation/c2ges_crosscheck/） |

### 血缘

P1 pilot（pilot-v1r6 首过全链）→ P2 parent-v2final（首过 19 门）→ v3 链
parent-v3（D8 预检/S7 装配级后滤加入）→ **parent-v3r1（本跑次，child）**；
heldout-v1r5（D8 未过，历史阻断记录保留）→ heldout-v2r3（通过）。
staging 污染事件与修正：`../STAGING_CONTAMINATION_REPORT.md`。
