# MA-SQLGrid 第三轮理论与创新终审

## 最终建议

**理论内部一致性：通过。架构创新叙事：有条件通过。投稿建议：Major Revision，除非标题和文章类型明确收缩为 auditable/safety-bounded architecture study。**

最新稿已经把 archived 100-point representation 化简为 hard eligibility gates 加有效 10/5/5 evidence score，并把 candidate-order stability 明确列为未建立。五角色价值也被严格限制为 typed software conformance，而非自主多智能体效能。由此，现有正文在逻辑上已经可以作为“可审计协调架构、执行边界和历史证据诊断”成立。尚未解决的是：原标题的 `Robust Multi-Agent Framework` 仍会被自然理解为整体多智能体效能/稳健性，而这恰是未运行的实验。

## 终审核验

### 1. Gate--score 形式化

**状态：Closed。**

最新稿明确：unsafe 或 non-executable candidates 在排序前被排除；因而 archived safety/execution 40+40 对所有 ranked candidates 是常数。有效分数为

\[
e(y)=10I_{\mathrm{shape}}(y)+5I_{\mathrm{order}}(y)+5V(y),\qquad V(y)\in[0,1].
\]

no-state 模式从 eligible set 取 $\arg\max e(y)$，并列按冻结顺序；required-state 模式先执行完整 coverage/threshold gate；eligible set 为空才 abstain【最新 TeX L239--L245】。该 piecewise 描述与 archived implementation 数学等价，并正确说明 40/40 是 eligibility control，不是 discriminative evidence。

权重被明确称为 illustrative、uncalibrated、非理论最优，也未被包装成算法性能贡献【L241】。从定义精度和内部逻辑看，第二轮问题已关闭。

### 2. Robustness vector

**状态：Closed for the body; Partial for the title。**

摘要第二句把 robust 限定为 mutation denial、bounded execution、complete-evidence gating 和 constructed-witness behavior【L22】。Table `tab:robustness` 已改为 “Tested and untested robustness dimensions”，并把 candidate-order stability 明确列为 `Not established; current selector is materially order-sensitive`，附 101 vs 117--118 和 130/180 top ties【L247--L264】。零 abstention 也被正确归因于至少一个 eligible slot 加 forced stable-order tie resolution，而非 calibrated confidence【L572】。

因此，正文不再内部矛盾：它只主张局部 software robustness dimensions，并明确否认整体 order/semantic/deployment robustness。

标题仍使用无修饰 `A Robust Multi-Agent Framework`。在没有标题限定的情况下，编辑可能只读标题与摘要关键词并预期整体稳定性；这不能完全由正文 vector 消除。

### 3. 五角色/多智能体价值边界

**状态：Closed for claim discipline; Open for efficacy。**

稿件反复说明 inherited GridDB/BIRD 不是五角色运行，release v3 是历史候选池的 outcome-exposed descriptive selection，RQ1 只测试 software conformance，Results 没有 five-role benefit estimand【L38--L52, L180--L207, L314--L360】。Analyst/Cartographer 是 deterministic skeletons，Synthesizer 只封装 external candidates；因此“multi-agent”被定义为 typed role decomposition，而不是五个 autonomous LLMs【L84--L88, L718, L728】。

这一价值边界是诚实且内部一致的。但 conformance 只能证明架构按 contract 运行，不能证明五角色分解比 monolithic/single-agent 更有效、更安全或更经济。该缺口不是再加免责声明能关闭的。

### 4. 架构创新定位

**状态：Partial。**

当前最可信创新是：append-only typed trace、DB-enforced executor、gold boundary、complete named-state eligibility、incident retention、versioned evidence attribution 和 physical-call accounting 的组合。稿件没有声称新的 generator、schema linker 或 SQL reasoning algorithm，这是正确的。

Related Work 仍主要以 RGISQL、zero-shot prompting、schema retrieval、DKA-SQL 等为参照【L56--L116】，尚未完成 agentic Text-to-SQL、blackboard coordination、execution-control architecture 和 metamorphic database testing 的功能级 novelty audit。因此“该组合在领域中有多新”仍待文献核验。当前可称为 auditable architecture instantiation，不宜声称 first/unique。

### 5. Counterfactual/Metamorphic 术语

**状态：Partial；Minor。**

主要结果已使用 `complete-three-witness` 和 `constructed witnesses`，Q039 也只称 projection-stability trace【L338--L348, L622--L642】。但角色仍叫 `Counterfactual Critic`，关键词仍含 `counterfactual testing`【L23, L38, L231】。三个 witness 是 metamorphic database transformations，不是替代世界或因果反事实。建议科学名称改为 `Metamorphic-State Critic`，历史类名可括注保留。

## 现有证据下可以成立的最终贡献

1. 一个 five-role-compatible typed software architecture，而非已验证的 autonomous multi-agent team。
2. 一个在声明 threat model 下通过测试的 read-only、bounded SQLite execution boundary。
3. 一个形式清楚的 hard-gate/evidence-score/tie/abstention controller。
4. 多协议、版本、失败、调用和 gold visibility 的可审计证据体系。
5. 关于 historical-pool tie dominance、order sensitivity 和 constructed-witness 低增量区分度的负诊断。

## 现有证据下不能成立的主张

- five-role 或 multi-agent superiority；
- candidate-order robustness 或 calibrated abstention；
- universal semantic/deployment robustness；
- complete witnesses 的一般 correctness gain；
- 真实 power-grid database operational validity；
- 新的 Text-to-SQL generation/reasoning algorithm。

## 只能通过特定外部动作关闭的项目

### 只能通过改标题关闭

- `Robust Multi-Agent` 的整体效能预期。建议改为 `An Auditable and Safety-Bounded Five-Role Framework...`，或至少增加 `Architecture and Descriptive Evidence Study` 副标题。若原标题完全保留，该编辑风险持续存在。

### 只能通过文献检索关闭

- append-only blackboard、typed role contracts、DB authorizer、state completeness 和 deterministic adjudication 组合的创新优先权。需要对 agentic Text-to-SQL、blackboard systems 和 metamorphic DB testing 做已核验的功能矩阵。

### 只能通过新实验/新数据关闭

- five-role efficacy：需要 hash-locked、call/candidate/token-matched、untouched end-to-end comparison。
- order-independent robustness：需要 development-frozen tie-abstention/margin policy，并在 untouched set 报 permutation stability、selective risk 和 coverage。
- power-grid semantic value：需要 sealed multi-schema title-concordant 数据，电网专家和数据库专家独立评价 projection、join、units、time boundary、ordering 和 tie semantics。

## 最终裁决

从形式理论和内部逻辑看，最新稿已没有 gate-score、版本归因或 robustness-vector 的关键矛盾，可以作为**可审计且安全边界明确的协调架构研究**成立。但当前证据不支持标题自然暗示的 robust multi-agent efficacy。若标题/文章类型收缩、Counterfactual Critic 改为 metamorphic terminology，并完成最近架构文献定位，本席位可降为 **Minor Revision**；若坚持把原标题作为未经限定的科学价值主张，则因核心五角色实验缺失，最终仍建议 **Major Revision**。
