# DECISION（heldout-v2r3：**held-out 同门通过**）

日期：2026-09-27。跑次：`run_20260927_heldout-v2r3`（held-out：主题 s01/s03/s04/s11
——THEMES 池最后 4 个从未使用主题（protection-setting mismatch / inverter ride-through /
telemetry delay / load-shedding threshold）；A↔B 交换（r01=本地 27B 拆分路径，
r02=DeepSeek 单调用）；prompt v3 变体；独立 staging heldout_v2；arch=c2ges-arch-v4-d8guard）。
协议：synthetic_c2ges_gendata_v1（冻结，未动阈值）。

## 裁决：**ACCEPT（held-out 独立检验通过）**

1. **门账本（evaluation/gate_ledger.json）：19/19 全过**。
   D8 max Jaccard 0.0625（生成期预检在位，本轮 0 拒收）；S7 零命中（装配级后滤生效）；
   E1b min 0.8753（8/8 全过）；E2 中位 0.5806（逐篇 0.5352–0.6557）；E3 0.6273；
   D 系列与 parent 逐位一致（D1 0.208 / D2 0.1311 / D3 0.0002 / D4 0.0）。
2. **双评审（咨询性）**：本地 27B accept（4/4/4/4/3）+ 手工替代 accept（4/4/4/4/3），
   逐维 |Δ| 全 0，裁决一致。无 major 矛盾。
3. **门的稳健性不依赖"谁写哪篇"**：A↔B 交换后 E1b/E2/E3/D 全部复现，
   未用主题上无过拟合迹象（对照 heldout-v1r5 的 D8 碰撞：v3 链的反套话指令 +
   生成期预检使同类碰撞未再发生）。
4. 血缘：v3 链 held-out 代；v2r2/v2r1/v2 三个中途失败跑次 FAILURE_RECORD 留档；
   断点续跑 4 staging + 4 fresh（增量 token 仅 15k）。
5. C²GES 侧复算：evaluation/c2ges_crosscheck/，其 6 门全过、与本地账本逐位一致。

## 对验收链的影响（协议 §6）

- held-out 同门通过 ✅（v1 链失败点 D8 已修复且未复发）。
- parent-v3 门全过但双评审分裂（见其 DECISION.md）——整条 v3 链的最终晋升
  取决于父代对 parent-v3 评审分裂的处置。
- P4（数据集卡片/交接文档）待父代指令。
