# 三轮独立专家评审门禁

机器权威清单为 `review_checklist.json`，共 41 个可追踪检查项（Round 1/2/3 分别为 15/13/13 项）。每条正式意见必须引用一个 `check_id`，并建立 comment → response → artifact/commit → independent verification 的闭环。

## Round 1：科学有效性

- Method：任务和主张边界、组件控制消融、基线公平性；MA validator 不得见 gold；C2 三种标签协议分离。
- Statistics：真实统计单元、完整配对、95% CI、McNemar/配对检验、Holm、种子与失败样本。
- Data：许可、来源、hash、切分泄漏、合成/AI 标签披露；MA sealed/gold；C2 真 document_id 与 NERC 人工审核。
- 出口：Critical=0、Major=0；受影响实验已重跑或主张书面降级。

## Round 2：应用价值与期刊适配

- Power Systems：谁使用、在哪个流程使用、支持何种决策、失败后果和禁用边界。
- Applied Sciences：具体应用验证、跨数据/场景、跨学科可读性、敏感性/效率/局限。
- Visual Narrative：每图绑定 RQ 和 E4 源数据，误差/单位清楚，色盲与缩放可读，讨论解释机制。
- 出口：Critical=0、Major=0；每项贡献回答用户、流程、量化收益和失败条件。

## Round 3：Reviewer 2 压力测试与投稿收口

- Skeptic：用泄漏、循环标签、强基线、替代指标和最差子组挑战主张； clean-room 重现。
- Claims/Citations：逐句 claim-evidence-citation；两篇论文重叠审计；标题到结论的强度一致。
- Submission：MDPI 编译、声明、数据/补充材料边界、引用/图/公式一致性及官方要求复核。
- 出口：Critical=0、Major=0；Minor 全关闭或书面 waiver；禁止再引入没有完整实验支持的大主张。

## 单条意见记录格式

```text
comment_id | check_id | paper | severity | location | evidence |
requested_action | acceptance_test
```

修改回复格式：

```text
comment_id | disposition | change_location | artifact_or_commit |
verification | response_text
```

`fixed_pending_verification` 不能计作关闭。评审者只读；修改由对应实验/写作智能体完成，原评审者或新的独立核验者确认后才可置 `closed`。
