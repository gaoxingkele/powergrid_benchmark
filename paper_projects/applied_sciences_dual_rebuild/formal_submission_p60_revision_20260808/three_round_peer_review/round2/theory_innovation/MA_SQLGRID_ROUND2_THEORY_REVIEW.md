# MA-SQLGrid 第二轮理论与创新性复审

## 复审结论

**建议：Major Revision；核心证据边界已显著改善，但框架价值的主实验仍缺失。**

第一轮后，摘要已在第二句限定 robust，RQ1 改为软件 conformance，Results 开头明确没有结果估计 five-role benefit，并新增 protocol master table、版本证据矩阵和 uncalibrated-weight 声明。这些修改有效阻止了多实验拼接成“框架准确率”。然而，论文的标题和创新核心仍是 “Robust Multi-Agent Framework”，而现有主要生成实验不是五角色运行，历史池 selector 又在 130/180 问题上并列并高度依赖任意候选顺序。该矛盾被正确披露，但尚未被实验证据解决；这是最可能导致编辑以 novelty/value 不足拒稿的开放问题。

## 第一轮问题逐项核验

| 第一轮问题 | 状态 | 严重度 | 第二轮证据与裁决 |
|---|---|---:|---|
| “multi-agent” 未被端到端识别 | **Open—new experiment required** | Major | RQ1 和 Results 已明确只测试 software conformance，不估计 five-role benefit【TeX L46, L50--L52, L359】；Analyst/Cartographer 是 skeleton、Synthesizer 封装外部候选【L221--L235, L695】。披露关闭了过度主张，但没有关闭核心价值缺口。 |
| “robust” 未及早限定 | **Closed for prose; Partial for title identity** | Major | 摘要第二句立即限定 mutation denial、bounded execution、complete-evidence gating、constructed witnesses【L22】；robustness vector 和 version matrix 清楚【L247--L280】。但标题仍无修饰，selector 对顺序高度敏感【L579--L623】，所以框架整体 robust 身份仍只部分成立。 |
| protocol/estimand/visibility 分散 | **Closed** | — | 新 master table 同时给 unit/N、dependence proxy、calls、endpoint、gold visibility、multiplicity 和 claim ceiling【L170--L188】；chronology 继续保留【L190--L210】。 |
| agent/state/adjudication 形式定义不足 | **Partial** | Major | 新增五条 formal invariants，并正确声明 40/40/10/5/5 是 illustrative、uncalibrated、非性能贡献【L237--L245】。但仍无完整状态空间、消息类型集合、转移函数或显式 score 方程；agent 与 module 的最小判据仍是“typed role”。 |
| safety/execution 既 gate 又各计 40 分 | **Open** | Major | 稿件没有回答重复编码的算法作用。在 eligibility 已要求 safety/execution 后，所有 eligible candidates 的前 80 分恒相同，因此这 80 分不提供排序信息；真正排序仅依赖剩余 20 分、witness gate 和 source order【L126, L237--L245】。这应在理论上化简，而不是继续呈现为 100-point adjudicator。 |
| 高并列与顺序敏感 | **Open—new rule/new test required** | Major | 130/180 top ties、约 5.4 tie size、178/180 Qwen-origin 和 reverse-order 101→117--118 全部保留并正确解释【L579--L623, L681】。现有框架没有 post-ranking ambiguity abstention，因此不是 order robust。 |
| Counterfactual Critic / witness 术语过强 | **Partial** | Minor | selector 已改称 complete-three-witness，witness 被描述为 constructed operator families【L46, L347, L679】；但角色仍叫 `Counterfactual Critic`，图注和正文仍用 counterfactual-required/CF-aware【L38, L217, L231, L261】，关键词仍为 `counterfactual testing`【L23】。 |
| 核心 witness 增量仅 Q039 且语义歧义 | **Closed as a bounded mechanism trace** | — | 稿件不再把 Q039 称为工程 correctness rescue，明确两条查询都未解决 status/date ambiguity，只称 projection-stability trace【L599--L623】。 |
| 创新定位缺 agentic Text-to-SQL/blackboard/metamorphic 最近方法比较 | **Open** | Major | Related Work 仍主要将既有工作概括为 generation/contextualization，Table `tab:literature-position` 未新增功能级 priority matrix【L56--L116】。当前无法从稿件判断 role contracts + append-only board + DB-enforced execution + state gating 的组合是否真正超出已有系统工程模式。 |
| 电网领域有效性不足 | **Open—new data required** | Major | GridDB 仍是 1 DB/8 tables/98 rows 且 development-visible；RTS-GMLC/SimBench 为 0 human-reviewed silver，BIRD 非电网【L134--L166, L691--L701】。 |

## 理论与算法逻辑核查

### 正确之处

1. **eligibility 与 correctness 被严格区分。** admissible、executable、frozen-evaluator correct 三层定义正确【L126--L132】。
2. **gold isolation 的运行内事实与研究级 outcome blindness 被分开。** v3 board seal 后才直接加载 raw gold，但同题 derived outcomes 已被 frozen tests 访问，因此只允许 descriptive re-execution【L190--L207, L677】。
3. **完整 coverage gate 的不变量合理。** 不完整 state set 不能用较少证据取得更高资格；该性质支持 conformance，不支持 semantic correctness【L231--L245】。
4. **版本归因正确。** FINAL controls 没有被追溯用于 5760/80/100/101，version evidence matrix 解决了第一轮的时间混淆【L268--L280】。

### 尚未闭合之处

对 eligible candidate $y$，safety=1 且 execution=1 已由 gate 保证。因此若 score 写为

\[
s(y)=40I_{safe}+40I_{exec}+10I_{shape}+5I_{order}+5I_{value},
\]

则前 80 分对所有参与排序的候选都是常数。排序等价于只比较后 20 分，再按 witness eligibility 和 source order 决胜。当前“100-point adjudicator”在数学上比实际决策复杂，可能使读者误以为 safety/execution 对 eligible candidates 有区分度。

**可执行修改：** 将 safe/executable 移到 hard gate，score 只定义为 remaining evidence；完整写出 witness gate、score、argmax、tie fallback 和 abstention 的分段决策函数。无需新数据。

## 仍可能导致编辑拒稿的缺口

### 1. 标题所指核心框架没有对应效能实验

**状态：Open；严重度：Major。** 当前最强正证据是 executor/control conformance 与既有实验资产的审计整合；没有 five-role vs monolithic/call-matched 对比。对一篇以 `Multi-Agent Framework` 为题的算法应用稿，这不是单纯 limitation，而是核心 estimand 缺失。

**可执行修改（不新增数据）：** 把文章类型和贡献明确定位为 `architecture and evidence-boundary study`；标题最低限度加入 `Auditable` 或 `Safety-Bounded`，并弱化 `Robust`。

**彻底关闭所需：** 新 hash-locked、call/candidate/token-matched、untouched end-to-end experiment；稿件 L699 已给出合理四条件协议。

### 2. “robust” 与 order-sensitive always-answer 行为不一致

**状态：Open；严重度：Major。** 框架倡导缺证 abstention，但 post-ranking ambiguity 没有 abstain；130/180 unresolved top ties 仍返回答案，reverse order 改变大量 gold matches【L243--L245, L579--L623】。

**可执行修改：** 在当前论文中把 order robustness 明确列入 `Not established`，并将 Table `tab:robustness` 的标题从 “Operational robustness dimensions” 改为 “Tested and untested robustness dimensions”。

**新实验：** 在 development-only 冻结 tie-abstention/margin policy，在 untouched set 报 selective risk、coverage 和 permutation stability。

### 3. 创新性仍像“审计封装”而不是新算法

**状态：Open；严重度：Major。** 当前 Cartographer 是 lexical baseline，Synthesizer 无生成，Validator 和 Critic 是规则执行，Adjudicator 权重未校准。若缺少最近系统的功能比较，编辑可能把贡献视为规范工程，而非算法/应用科学创新。

**可执行修改：** 用已核验文献建立 capability matrix：candidate provenance、role ownership、blackboard immutability、DB authorizer、gold boundary、state completeness、failure retention、physical-call accounting、order/tie disclosure。明确创新是“evidence contract and executable control boundary”，不声称新的 SQL reasoning algorithm。

### 4. 电网标题的应用价值仍没有 qualified semantic evidence

**状态：Open；严重度：Major。** 合成 GridDB 可测试接口，但不能证明真实电网 schema、单位、权限和业务问题语义。BIRD 不能补足领域外部效度。

**彻底关闭所需：** 至少一个 sealed title-concordant 多 schema 数据集；电网专家和数据库专家独立评价 projection、join、units、time boundary、ordering、ties 与 result granularity；报告 adjudication 前 agreement。

## 第二轮通过条件

1. 将 eligibility gate 与 ranking score 数学分离，给出完整分段 decision function。
2. 在 robustness matrix 明确加入 `candidate-order stability: not established/failed descriptively`。
3. 将 Counterfactual Critic 的科学名称改为 `Metamorphic-State Critic`，或至少在首次出现即给等价限定，并移除无法支撑的关键词。
4. 完成最接近 agentic Text-to-SQL、blackboard control 和 metamorphic DB testing 的可核验 novelty matrix。
5. 若本轮不执行新实验，则 cover letter 和 contribution 不得将 conformance、historical-pool selection 或 BIRD 解释为 multi-agent efficacy。

## 第二轮最终评价

修订稿现在对“没有证明什么”表述得很准确，且协议/版本逻辑已基本闭合。但从编辑视角，**诚实承认核心框架效能未测试，并不会自动产生核心框架价值证据**。若投稿前不能完成新 end-to-end 实验，最可行的路线是把论文彻底定位为 auditable/safety-bounded coordination architecture，并让标题、novelty matrix 和算法形式定义与该较窄贡献一致。否则理论/创新席位仍维持 Major Revision。
