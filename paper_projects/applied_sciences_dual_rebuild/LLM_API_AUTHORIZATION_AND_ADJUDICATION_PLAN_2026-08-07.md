# CMC 两篇论文：LLM API 申请、标注裁决与实验授权执行方案

**适用论文：** C2GES 与 MA-SQLGrid（作者及单位信息沿用原 CMC 稿件）  
**目标期刊：** MDPI *Applied Sciences*  
**版本：** v1.0，2026-08-07  
**文档性质：** 作者决策与执行手册；不构成伦理审批、法律意见或真人专家签字

## 一、结论先行

本项目涉及两种完全不同的“授权”，不能混为一谈。

1. **厂商 API 访问授权**：在 OpenAI、Google、DeepSeek、阿里云百炼、火山方舟、智谱或 Perplexity 等官方控制台注册账户、开通计费并创建 API Key。API Key 只证明账户有权调用模型。
2. **论文项目运行授权**：由作者对具体冻结协议、数据范围、模型、调用量、预算、硬件占用和停止条件作出书面批准。它不是向外部机构申请的 API，也不能由 LLM、代码代理或 API Key 自动代替。

因此，您问的“授权 API 去哪里申请”如果指模型调用权限，应去相应厂商官方控制台申请 API Key；如果指 MA-SQLGrid 的 BIRD 正式实验启动，则**无需向外部申请任何授权 API**，只需作者对当前冻结协议作出明确、可追溯的书面批准。

LLM 可以承担预标注、双盲机器标注、冲突解释和候选裁决，但它产生的是 **LLM-assisted / machine-adjudicated silver labels**，不是“真人专家金标”。若论文要声称“由领域专家标注并裁决”，仍必须有真实、具备相应资质的人员完成或复核。没有真人参与时，应修改证据等级和论文表述，而不能把大模型冒充专家。

## 二、API Key 去哪里申请

### 2.1 推荐的直接申请入口

以下均为厂商官方入口。申请流程通常是：注册/登录 → 必要时完成实名认证或组织验证 → 开通模型服务/计费 → 创建项目或工作空间 → 创建 API Key → 设置额度与权限 → 进行最小测试。

| 提供方 | 官方申请或管理入口 | 本项目建议用途 | 备注 |
|---|---|---|---|
| OpenAI | https://platform.openai.com/api-keys | 独立标注或第三模型裁决 | API 与 ChatGPT 订阅分开计费；密钥创建后应立即安全保存。官方说明：https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key |
| Google Gemini | https://aistudio.google.com/app/apikey | 异构第二标注器或裁决器 | 新 Key 优先使用当前的授权型 Key；限制到 Gemini API。官方说明：https://ai.google.dev/gemini-api/docs/api-key |
| DeepSeek | https://platform.deepseek.com/api_keys | 中文/代码任务标注器、SQL 候选复核 | 需有余额；401 表示鉴权失败。官方文档：https://api-docs.deepseek.com/api/deepseek-api |
| 阿里云百炼 / Qwen | https://bailian.console.aliyun.com/ | 中文标注器或结构化输出模型 | 在目标地域创建 API Key，并记录对应 API Host。官方说明：https://help.aliyun.com/zh/model-studio/get-api-key |
| 火山方舟 / Doubao | https://console.volcengine.com/ark/region:ark+cn-beijing/apikey | 异构复核或成本敏感批处理 | 创建 Key 后调用方舟端点；官方示例：https://www.volcengine.com/docs/82379/1795150 |
| 智谱开放平台 / GLM | https://open.bigmodel.cn/usercenter/apikeys | 中文裁决或独立复核 | 通用 API 与 Coding 套餐 Key/端点不可混用。官方说明：https://docs.bigmodel.cn/cn/guide/develop/http/introduction |
| Perplexity | https://console.perplexity.ai/ | 需要联网检索的辅助核查，不宜作为唯一标注器 | 先创建 API Group，再创建 Key。官方说明：https://docs.perplexity.ai/docs/getting-started/api-groups |
| Moonshot / Kimi | https://platform.moonshot.cn/console/api-keys | 可选中文异构标注器 | 应使用官方开放平台账户；不要把网页会员当作 API 额度。若本地仍走代理，必须先确认代理身份、上游模型和日志政策。 |
| xAI / Grok | https://console.x.ai/ | 可选异构标注器 | 使用官方控制台创建并管理 Key；运行前锁定确切模型版本。 |

### 2.2 当前本地配置状态

根据 2026-08-07 对项目 `.env` 的脱敏连通性检查：

- 已可访问：DeepSeek、Qwen、Grok、Gemini、Perplexity、Cloubic。
- 当前未通过：Doubao 与 GLM 返回 401，应在各自官方控制台重新创建或核对 Key、套餐类型、地域和 Base URL。
- Kimi 当前配置指向 `http://127.0.0.1:18182`，但本地代理端口未监听；应启动并审计该代理，或改为 Moonshot 官方端点。
- `GROK_API_KEY` 在 `.env` 中存在重复定义；应保留一个有效值，避免加载顺序不确定。
- `.env` 已被忽略，但 `.env.cloubic` 目前存在被误提交风险；应加入忽略规则或迁移到受控的本地密钥文件，并轮换任何可能暴露过的 Key。

这些状态只表示“能否调用”，不表示模型适合充当金标专家，也不等于作者已经批准正式实验。

## 三、为什么 API 不能替代真人专家责任

### 3.1 可以由 LLM 完成的工作

- 按冻结标注手册生成第一轮结构化标签。
- 两个不同模型家族独立、互盲标注同一批样本。
- 对冲突样本列出证据、冲突类型与建议结论。
- 运行确定性检查：JSON Schema、引用句 ID、SQL 语法、只读安全、可执行性、结果形状和单位一致性。
- 对高置信一致样本形成机器银标，并保留完整调用账本。
- 为真人复核人员排序高风险案例，显著减少人工工作量。

### 3.2 不能由 LLM 冒充完成的工作

- 不能签署作者的实验启动授权。
- 不能被写成“电力领域专家”“两名独立人工标注者”或“人工裁决者”。
- 不能提供作者贡献、利益冲突、资金声明、许可审查或最终投稿同意。
- 不能把模型生成的标签自动升级为 human gold。
- 不能因为模型一致率高就证明标签正确；共同训练数据、提示偏差和同源模型会产生相关错误。

### 3.3 对“数据是否不完整”的正确解释

“等待真人专家标注/裁决”并不等于已有实验数据造假或文件缺失，而是表明**某些更强的外部有效性主张缺少相应证据层级**。当前两篇稿件已有可审计的机器实验，但以下主张仍有边界：

- C2GES 的 NERC 派生标签属于机器银标，若无真人复核，不能写成人工金标性能。
- MA-SQLGrid 的 91 个外部 grid question–SQL 候选尚无双专家审查和争议裁决，不能把自动候选匹配称为外部准确率。
- BIRD 是公开基准，不需要专家逐条造金标；它缺的是作者对已冻结 5000-call 正式运行的启动批准，而不是数据本身缺失。

在没有真人专家资源时，合法的策略是降低表述强度、明确 silver-label provenance、报告机器一致性和误差边界，并把真人验证列为后续工作。不能用术语替换来伪装证据等级。

## 四、适用于两篇论文的标注—裁决方案

### 4.1 总体架构

采用“三模型、两验证器、一真人门禁”的分层流程：

1. **冻结任务**：先冻结标注手册、标签模式、纳入排除标准、样本清单、提示词、模型快照、随机种子和统计计划。
2. **标注器 A**：模型家族 A 独立输出结构化 JSON，不得看到 B 的结论。
3. **标注器 B**：不同供应商、不同模型家族独立输出相同 Schema，不得看到 A 的结论。
4. **确定性验证**：代码检查格式、证据可追溯性、SQL 安全/执行、引用范围、重复项和越权标签。
5. **裁决器 C**：第三个不同模型仅查看原始材料、A/B 标签及确定性检查结果；模型名称匿名化；允许 `ABSTAIN`。
6. **真人复核门禁**：复核全部分歧、全部 `ABSTAIN`、全部高风险样本，以及一致样本中预先随机抽取的 15%–25%。
7. **冻结最终账本**：记录原始响应、解析响应、最终标签、裁决原因、人工修改、时间戳、模型版本、token、成本和错误。

若完全不安排真人复核，则第 6 步改为“作者审阅证据等级与表述”，最终数据必须命名为 `machine-adjudicated silver set`，不得命名为 `expert-adjudicated gold set`。

### 4.2 模型选择规则

- A、B、C 尽量来自三个不同提供方，避免同一基础模型经不同聚合商重复出现。
- 若使用 Cloubic 或其他聚合路由，必须记录实际 upstream provider、模型 ID 和版本；无法确认上游时，不计作“独立模型家族”。
- 被评测模型原则上不担任裁决器，避免自我偏好。
- SQL 任务优先选择代码/结构化输出稳定的模型；证据句选择优先选择长文本定位稳定的模型。
- 固定温度或最低随机性，固定 `max_tokens`，记录系统指令与 JSON Schema 的 SHA-256。
- 允许模型拒答和裁决器弃权；不得强迫每个样本都给确定结论。

推荐起始组合可为：Qwen 或 DeepSeek 作为 A，Gemini 或 Grok 作为 B，OpenAI/GLM/Doubao 中与 A、B 均不同的一家作为 C。最终组合应以 20–30 条盲测 pilot 的格式通过率、冲突质量、成本和稳定性决定，而不是只看排行榜。

### 4.3 C2GES 专项标注设计

**对象：** NERC 报告或其许可允许使用的派生文本与 evidence candidates。  
**核心单位：** 文档—声明—证据句集合，而不是单独句子。

每条标签至少包含：

- `document_id`、`claim_id`、原文句 ID。
- 证据角色：支持、反驳、背景、方法、结果、无关或信息不足。
- 证据句集合；必须引用原始句 ID，不允许只生成摘要。
- 是否存在跨句依赖、否定、条件、时间限定和实体歧义。
- 置信档位与可验证理由；置信度仅用于排序，不作为正确性概率。
- `ABSTAIN` 与原因。

确定性检查包括：句 ID 必须存在；引用不得超出原文；证据集合不得为空却标为支持/反驳；重复句规范化；数据许可与来源映射完整。统计至少报告原始一致率、Cohen’s kappa 或 Krippendorff’s alpha、证据集合 F1、分歧率、裁决率、弃权率，以及真人抽检后的错误率和置信区间。

当前开发可见的约 200 条 NERC 候选可以用于完善手册和 pilot，但不能事后宣称为真正 sealed set。若要形成新 sealed set，建议先做功效/精度目标计算，再在模型输出不可见的条件下抽取新样本；工程起始范围可设为 50–100 条，最终数量由预先设定的置信区间宽度决定。

### 4.4 MA-SQLGrid 专项标注设计

**对象一：** 91 个现有外部 grid question–SQL 候选。  
**对象二：** 新建的 sealed grid-domain follow-up set。  
**对象三：** BIRD Mini-Dev 公开比较（无需人工造 gold SQL，但需正式运行授权和独立复算）。

对 question–SQL 候选，每条标签至少包含：

- 问题是否可由给定数据库回答。
- 所需表、列、连接路径、过滤条件、聚合、分组、排序、单位和时间范围。
- SQL 是否只读、安全、语法有效、可执行。
- 执行结果是否满足问题语义，而非只判断“能执行”。
- 结果列、顺序、重复值、空值和 tie handling 是否正确。
- 错误分类与最小修正建议。
- `ABSTAIN` 与需要的额外领域信息。

确定性验证必须在 SQLite 只读沙箱执行：URI `mode=ro`、`PRAGMA query_only`、authorizer 拒绝写操作、进度超时和输出上限。LLM 不得直接执行 shell 命令，也不得通过生成 SQL 修改数据库。

现有 91 条是开发可见样本，适合双模型复标和真人高风险复核，但不能追溯升级为 sealed。新的 sealed set 可从许可明确、尚未被提示开发使用的 RTS-GMLC/SimBench 派生问题中建立；工程起始范围可设为 80–120 条，并在任何被测模型看到样本前冻结任务与答案。样本量最终由预期错误率和目标区间宽度决定。

## 五、BIRD 5000-call 正式运行授权

### 5.1 当前冻结状态

本地权威冻结文件为：

`paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/public_baseline_protocol/BASELINE_PROTOCOL_FREEZE.json`

- 协议 ID：`MA-PUBLIC-BIRD-MINIDEV-v1.0`
- 冻结文件 SHA-256：`29C780C63A2DC2BAAE221CFCE52252C716D8720DBEECDC2F7A2FDD5756B42AF5`
- 状态：`FROZEN_NOT_RUN`
- 数据：BIRD Mini-Dev，500 题、11 个 SQLite 数据库
- 模型：冻结的本地 Qwen2.5-Coder-7B 与 Granite-3.3-8B 快照
- 方法：Direct、Decomposition、deterministic Schema Selection、mandatory two-call Execution Repair
- 调用量：每模型 2500 次，共 5000 次；最终 SQL 输出 4000 个
- 前置验证：500/500 gold SQL 在 SQLite 3.40.1 下完成；独立技术审计 39/39 PASS
- 正式结果：0 次正式调用、0 个正式输出；不得在授权和执行前写入任何 BIRD 分数

该运行使用本地 RTX 3090，不需要任何外部 LLM API Key。所谓“人工启动授权”是防止未经作者同意消耗数小时 GPU、产生正式研究结果和改变投稿证据边界的本地治理门禁。

### 5.2 可复制的作者授权文本

> 我授权执行冻结协议 `MA-PUBLIC-BIRD-MINIDEV-v1.0`，并确认冻结文件 SHA-256 为 `29C780C63A2DC2BAAE221CFCE52252C716D8720DBEECDC2F7A2FDD5756B42AF5`。我知悉本次运行包含 500 个 BIRD Mini-Dev 项目、11 个数据库、2 个本地模型、4 种方法、共 5000 次生成调用和约 4000 个最终 SQL 输出，将占用本地 RTX 3090 数小时。授权仅限该冻结协议，不授权修改协议、删除失败记录、对外上传数据、宣称 DKA-SQL 复现或自动投稿。批准人：[姓名或稳定身份]；批准时间：[YYYY-MM-DD HH:MM，Asia/Shanghai]。

作者可直接在对话中发送完整文本，也可填写本项目的 `HUMAN_ACTION_PACKET.md`。执行代理必须核对协议 ID、SHA-256、批准人、时间和明确的 5000-call/GPU 确认；任何字段缺失均应 fail closed。

### 5.3 通用 API 批处理授权模板

对于云端 LLM 标注，应新建不含密钥的授权记录，例如：

```json
{
  "approval_id": "DUAL-LLM-ANNOTATION-YYYYMMDD-01",
  "approved_by": "作者姓名或稳定身份",
  "approved_at": "2026-08-07T20:00:00+08:00",
  "scope": ["C2GES_NERC_PILOT", "MA_GRIDSQL_PILOT"],
  "protocol_sha256": "待冻结后填写",
  "providers_and_models": [
    {"role": "annotator_a", "provider": "...", "model": "精确版本"},
    {"role": "annotator_b", "provider": "...", "model": "精确版本"},
    {"role": "adjudicator_c", "provider": "...", "model": "精确版本"}
  ],
  "max_calls": 1000,
  "max_cost_cny": 500,
  "data_scope": ["允许上传的具体文件或脱敏字段"],
  "prohibited_actions": [
    "不得上传未授权或保密材料",
    "不得把 LLM 标签称为真人专家金标",
    "不得覆盖原始数据",
    "不得删除失败或分歧记录",
    "不得自动投稿或公开发布"
  ],
  "stop_conditions": [
    "预算达到 80% 时暂停",
    "连续 5 次鉴权或格式错误时暂停",
    "检测到敏感信息或许可冲突时立即暂停",
    "实际模型版本与冻结记录不一致时立即暂停"
  ]
}
```

API Key 永远不能写入该授权 JSON、论文、日志或聊天内容；程序只从本地环境变量或秘密管理器读取。

## 六、分阶段执行与验收门禁

### 阶段 0：许可、数据和声明确认

- 逐数据集确认下载、派生、上传第三方 API、再发布和论文展示权限。
- 对不能上传云端的数据，只使用本地模型或脱敏、最小化字段。
- 冻结 C2GES 和 MA-SQLGrid 各自的 label schema、手册和排除规则。
- 作者确认 LLM 使用披露方案。

**验收：** 无未知许可；无 API Key 入库；数据范围有明确授权。

### 阶段 1：20–30 条双模型 pilot

- 每篇论文抽取 20–30 条，A/B 独立标注，C 只裁决分歧。
- 统计 JSON 通过率、平均 token、成本、延迟、分歧率、弃权率。
- 人工检查全部分歧和至少 20% 一致样本。

**验收：** 结构化输出通过率建议不低于 98%；无法解析记录不丢弃；分歧类型可解释；成本外推在预算内。

### 阶段 2：开发可见集完整处理

- C2GES：处理现有 NERC 候选；最终名称保持 machine-adjudicated silver。
- MA-SQLGrid：处理现有 91 条外部候选；真人未完成前不报告 external gold accuracy。
- 生成按样本的 provenance ledger 和聚合一致性报告。

**验收：** 全样本分母保留；调用失败、解析失败、裁决和人工修改均计数。

### 阶段 3：新 sealed set

- 由数据保管人生成/封存；被测模型和提示开发人员在冻结前不得看到答案。
- 样本量由统计精度目标确定，不以“凑够论文数量”为原则。
- 先冻结方法和统计计划，再一次性解封运行；不得看结果删样本。

**验收：** freeze hash、custodian、时间戳、无泄漏声明和完整运行账本齐全。

### 阶段 4：BIRD 或其他正式实验

- BIRD 仅在作者签署第 5 节授权后运行精确冻结协议。
- 云 API 批处理仅在通用授权 JSON 完成后运行。
- 所有失败保留；无结果导向重试；重试策略必须预先冻结。

**验收：** 调用数、唯一记录数、最终输出数、数据库复执行和协议 hash 全部匹配。

### 阶段 5：论文集成与三轮评审

- 第一轮：方法、数据许可、泄漏与证据等级。
- 第二轮：统计、复算、失败分母、图表和主张边界。
- 第三轮：Applied Sciences 合规、GenAI 披露、作者声明、可复现性和最终 PDF。
- 每轮形成 issue matrix、逐项回复、修改后独立复核；未关闭项不得标记 submission-ready。

## 七、统计与报告最低要求

### 7.1 标注质量

- 原始一致率与分歧率。
- Cohen’s kappa（两标注器、类别标签）或 Krippendorff’s alpha（更一般情形）。
- 集合标签报告 micro/macro F1 或 Jaccard，并按文档聚类 bootstrap。
- 裁决率、弃权率、格式失败率、API 失败率和人工推翻率。
- 对真人抽检错误率给出二项置信区间；不要把 LLM 自报置信度当作校准概率。

### 7.2 实验结果

- 保留 all-attempt denominator，失败不能从分母剔除。
- 对重复样本、模板或数据库使用适当聚类单位。
- 多重比较预先定义检验家族并校正。
- 同时报效应量、置信区间和原始计数，不只报 p 值。
- 模型、端点、版本、日期、温度、token、成本、延迟、重试和错误必须可追溯。

### 7.3 建议图表

- 一张标注—裁决—真人门禁流程框图。
- 每篇一张样本流转图：总样本、一致、分歧、弃权、人工复核、最终保留。
- 一张 A/B/C 与真人抽检的一致性热图或混淆矩阵。
- 一张成本—延迟—质量 Pareto 图。
- MA-SQLGrid 增加 BIRD 四方法 × 两模型结果图和数据库级误差图；仅在正式运行后生成。
- C2GES 增加 evidence-role 分层结果和文档级 bootstrap 区间图。

## 八、安全、隐私与复现要求

- `.env`、`.env.local` 和供应商密钥文件全部加入忽略规则；提交前运行 secret scan。
- 对已暴露、重复或来源不明的 Key 立即轮换；不要在论文补充材料中发布。
- 为每个项目创建独立 Key，设置最低模型权限、IP 白名单、调用限额和账单告警。
- 原始文档视为不可信输入，提示中使用明确的数据分隔符，防止文档内 prompt injection 改写标注规则。
- 原始响应 append-only 保存；解析结果和最终标签另存，不覆盖原文。
- 日志中屏蔽 Authorization header、Key、个人信息和不允许再发布的原文。
- 云端上传前确认服务条款、数据保留和训练使用选项；敏感数据优先本地模型。
- 固定模型完整 ID；若供应商使用滚动别名，应记录请求日期与响应返回的模型标识，并做版本漂移检查。

## 九、Applied Sciences 披露边界

MDPI 当前政策要求：如果 GenAI 被用于研究设计、数据收集、生成数据/图形、分析或解释，应在投稿过程中声明，并在 Materials and Methods 中说明使用方式，在 Acknowledgments 中给出工具产品信息；作者对有效性、原创性和完整性负全部责任。单纯语法、结构、拼写和格式编辑通常不在该披露要求内。政策原文：https://www.mdpi.com/ethics

若执行本方案，建议在两篇论文 Methods 中披露：

- 使用的模型、版本、提供方、访问日期、温度和结构化输出模式。
- A/B 独立标注、C 裁决、确定性验证和真人抽检比例。
- 哪些标签是 human-reviewed，哪些只是 machine-adjudicated silver。
- 提示词、标签 Schema、protocol hash、失败处理和数据上传边界。
- LLM 未被列为作者，最终责任由署名作者承担。

建议致谢模板：

> During the preparation of this study, the authors used [tool, provider, model/version, access date] for [machine-assisted annotation/adjudication and/or analysis support]. All outputs were subjected to the validation and human-review procedures described in the Materials and Methods. The authors reviewed and edited the outputs and take full responsibility for the content of this publication.

若没有真人抽检，应把其中的 `human-review procedures` 删除，并明确写为 deterministic validation and author verification；不得暗示专家金标。

## 十、预算和停止策略

先做 pilot 再定总预算。预算计算使用每家 API 实际返回的 input/output token 与账单，不使用网页估计代替。建议：

- Pilot：每篇 20–30 条 × 2 标注器 + 分歧裁决。
- 正式预算上限：根据 pilot 的 P90 单条成本乘以计划调用数，再留 20% 异常余量。
- 当费用达到批准上限 80% 时自动暂停并汇报。
- 相同输入不得因“不喜欢结果”而反复调用；仅允许冻结规则定义的技术失败重试。
- 聚合商与直连供应商不要重复计费；先确定一条权威路由。
- BIRD 本地 5000-call 与云端标注预算分开审批、分开记账。

## 十一、作者现在需要做的最小决策

1. 决定是否授权精确的 BIRD 本地 5000-call 冻结运行；如授权，发送第 5.2 节完整文本。
2. 选择云端标注的 A/B/C 提供方，并给出最大调用数和人民币预算。
3. 确认哪些 NERC、RTS-GMLC、SimBench 或内部材料允许上传第三方 API；不允许的部分改用本地模型。
4. 决定证据路线：
   - **推荐路线：** LLM 双标 + 第三模型裁决 + 真人复核全部分歧和 15%–25% 一致样本。
   - **无真人资源路线：** 全程机器标注/裁决，但论文只声称 silver-label validation，不声称专家金标。
5. 批准最终 MDPI GenAI disclosure 与作者责任声明。

## 十二、推荐的立即执行顺序

1. 修复或弃用 Doubao、GLM 和 Kimi 的失效/代理配置；清理重复 Grok 变量和 `.env.cloubic` 风险。
2. 为 C2GES 与 MA-SQLGrid 分别冻结 annotation protocol v1，并生成 hash。
3. 使用三家不同模型完成每篇 20–30 条 pilot，生成成本与一致性报告。
4. 作者根据 pilot 决定模型组合、真人抽检比例和正式预算。
5. 完成开发可见集处理，再决定是否投入新 sealed set。
6. 独立处理 BIRD 本地授权；运行后先审计，后看统计结果，再写入 MA-SQLGrid。
7. 集成论文并完成三轮评审和三轮修改。

---

**最终治理原则：** API Key 解决“能否调用模型”；作者授权解决“是否允许开展这项正式研究”；真人专家复核解决“能否声称专家金标”。三者缺一时，应降低相应主张，不得用另一个环节代替。
