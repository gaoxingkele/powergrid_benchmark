# Parent-v2b：第一套合成数据的流程、内容、分布与算法

绑定跑次：`run_20260910_parent_v2b/`  
版本：`parent-v2b`  
协议：`SYNTHETIC_EXPERIMENT_PLAN.md`（DeepSeek + 本地展开 + Codex 盲审）  
生成器：`03_Reproducibility/Code/prospective_v1/generate_deepseek_synthetic.py`  
分布门：`evaluate_synthetic_distribution.py`  
种子：`20260908`  
模型：DeepSeek `deepseek-v4-flash`，温度 0.65  
数据集 SHA-256：`9D33EFE37EE71B8B5E5A6E1D29AF463DE0BBEF5B7AE98481BD6B5AF44451C92A`

这是三代合成线的 **parent（第一套）**。用途是软件压力测试与机制对齐，**不是**真实事故报告，**不能**替代 E1 未见系列或 E2 真人标注，`confirmatory_claims_allowed = false`。

本跑次 **未通过** 冻结数字门（精确重复率 0.530 > 0.20）。下文记录的是设计逻辑与实测分布，不是晋升结论。

---

## 1. 流程（三道工序）

```text
权利安全锚点（12 篇开发集的页数/候选数/版面类型计数，不含正文）
        │
        ▼
① DeepSeek 语义核（每系列 2 篇虚构事故短句 + 干扰种子）
        │  失败则停，不重试、不覆盖
        ▼
② 本地确定性展开（按锚点剖面铺成长文档、抽 110–180 词抽取式 reference）
        │
        ▼
③ 分布门 + Codex 盲审（数字门先判；LLM 分咨询性）
```

调用（协议冻结命令，路径相对于 C2GES 根）：

```text
python generate_deepseek_synthetic.py --env <workspace>/.env \
  --metadata-csv 03_Reproducibility/Data/rights_safe_metadata/rights_safe_report_metadata.csv \
  --layout-csv 03_Reproducibility/Data/prospective_external_v1/layout_dev_pilot_v2/layout_candidate_audit.csv \
  --model deepseek-v4-flash \
  --output 03_Reproducibility/Data/synthetic_stress_v1/run_20260910_parent_v2b \
  --seed 20260908 --series 4 --version-id parent-v2b

python evaluate_synthetic_distribution.py \
  --dataset <run>/synthetic_reports.jsonl \
  --metadata-csv <metadata> --layout-csv <layout> \
  --output <run>/evaluation

python run_codex_synthetic_critic.py \
  --packet <run>/evaluation/codex_critic_packet.json \
  --output <run>/codex_critic --model gpt-5.6-sol
```

隐私篱笆：提示词只含虚构主题与制度约束；不发送真实报告正文、手稿、作者信息或 URL。设施名必须以 `Synthetic` 开头。禁词按词边界匹配：NERC、FERC、WECC、ERCOT、PJM、CAISO、MISO、ENTSO-E、State Grid。

---

## 2. 内容

### 2.1 规模与主题

| 项 | 值 |
|---|---|
| 系列数 | 4 |
| 每系列报告 | 2（硬门：`two_reports_per_series`） |
| 报告数 | 8 |
| 主题池 | 12 个虚构主题，`Random(20260908)` 洗牌后取前 4 个 |
| 本跑次抽中系列 | `synthetic_series_02`, `07`, `01`, `05` |

主题对照（`THEMES` 1-index）：

| series_id | 主题 | 词面体制 `regime` |
|---|---|---|
| 02 | transformer cooling-control failure during a heat wave | paraphrased（`(2-1) mod 3 = 1`） |
| 07 | distribution automation loop during storm restoration | explicit（`(7-1) mod 3 = 0`） |
| 01 | protection-setting mismatch during feeder restoration | explicit |
| 05 | substation auxiliary-power loss after a fictional cable fault | paraphrased |

`regime` 只约束语义核用词：explicit 可用常规因果词；paraphrased 少用线索词；ambiguous 允许多个次要功能但仍有一个最优角色。

### 2.2 每篇报告里有什么

每篇 JSONL 记录字段要点：

- `split = synthetic_stress`，`synthetic = true`
- `candidate_sentences[]`：`sid`, `text`, `page`, `unit_type`, `synthetic_ground_truth_role`, `synthetic_stress_tags`
- `reference_summary`：从语义核抽取、且必须与 `reference_unit_ids` 指向的候选原文拼接 **逐字相等**
- 版面类型：`body`, `heading`, `list_item`, `table_unit`, `caption`, `footnote`
- 角色：五个核心角色 + `distractor`

语义核（LLM）约束：

- 每篇 18–26 条核心句；每角色出现 2–6 次，且不得五角色完全均分模板
- 每角色恰好 1 条 `summary_priority = 2`
- 句长约 12–24 词（校验窗 10–28）
- `causal_predecessors` 构成 **有向无环图**（允许叙述顺序与因果顺序不一致）
- 干扰种子 24–36 条、互异、10–24 词量级

本地展开后：候选条数 `max(40, 锚点 candidate_count)`；页码按槽位均匀切分  
`page = 1 + slot * page_count // target_count`。

语义核只允许落在 `body` 或 `list_item` 槽；其余槽为确定性干扰句（`deterministic_layout_distractor`）。

### 2.3 抽取式 reference 的内容逻辑

不是另写摘要，而是从核心句里挑：

1. 每个核心角色取优先级最高的一句；
2. 并上所有 `priority = 2` 的句；
3. 总词数 > 180 则丢掉可删的低优先级重复角色句；
4. 总词数 < 110 则按优先级从高到低补句。

因此 parent 的“标准答案”在构造上就是 **种植角色链的抽取**，不是真人 Executive Summary。这决定了后面适用算法（C²GES 路径项）会偏向对齐这套金标准。

---

## 3. 概率分布与锚点

锚点来自 12 篇 **开发集** 的权利安全元数据 + 版面计数，不读正文。合成侧 n = 8。

### 3.1 报告级边际（实测）

| 量 | 锚点 n=12：min / q25 / median / q75 / max / mean | 合成 n=8 | 归一化 W1 | KS |
|---|---|---|---:|---:|
| 候选条数 | 170 / 221 / 286 / 342.25 / 703 / 315.17 | 170 / 220 / 300.5 / 397.5 / 703 / 340.75 | 0.208 | 0.167 |
| 页数 | 15 / 28.25 / 35.5 / 39.5 / 66 / 35.33 | 15 / 28 / 35.5 / 42.25 / 66 / 36.38 | 0.131 | 0.125 |
| reference 词数 | 256–2218（开发集真实摘要，仅诊断） | 143–179，均值 162.9 | 1.052 | 1.0 |

reference 词数 **不设分布门**：合成任务故意锁在 110–180，与真实 Executive Summary 长度不可比。

### 3.2 版面类型比例（全局计数差的绝对值）

相对锚点全局比例：

| unit_type | \|p_syn − p_anchor\| |
|---|---:|
| body | 0.0190 |
| caption | 0.0116 |
| table_unit | 0.0107 |
| heading | 0.0035 |
| footnote | 0.0016 |
| list_item | 0.0013 |
| **最大** | **0.0190 ≤ 0.03 门** |

### 3.3 生成时如何把锚点“变成”合成分布

不是从连续密度抽样，而是 **离散剖面的分位跨步取样 + 最大余数配比**：

1. **主题**：12 个主题等权，`rng.shuffle` 后取 k=4（无放回排列的前缀）。  
2. **开发剖面**：12 个经验剖面按原顺序视为经验分布的支撑。对第 i 篇合成报告（i=0…7）取  
   `index = min(n−1, floor((i+0.5)·n / 8))`  
   即 8 个点落在 12 个剖面的分位上（本跑次下标 0,2,3,5,6,8,9,11）。  
3. **版面类型**：把该剖面的类型计数当作多项比例 π，把目标条数 N 按 Hamilton/最大余数法配成整数，再 `rng.shuffle` 打乱槽位。  
4. **语义核落点**：在 `body∪list_item` 槽上 **无放回均匀** `rng.sample` 出 \|core\| 个位置。  
5. **干扰句**：种子循环取模 + 由 `doc_id` SHA 前 8 位导出的时间/通道盐；这是确定性模板，不是 i.i.d. 语言模型采样——这也是 parent 重复率偏高的机制来源。

DeepSeek 一侧：温度 0.65 的聊天采样；角色次数 2–6、优先级、DAG 由 schema 截断，而不是显式的概率质量函数。

### 3.4 冻结数字门（阈值事先锁定，看结果后不改）

| 门 | 规则 | parent-v2b |
|---|---|---|
| 结构 | 4 系列、每系列恰 2 篇；抽取式 reference 可还原 | 过 |
| 候选数分布 | 归一化 W1 ≤ 0.75 | 过（0.208） |
| 页数分布 | 归一化 W1 ≤ 0.75 | 过（0.131） |
| 版面比例 | max \|Δπ\| ≤ 0.03 | 过（0.019） |
| 精确重复率 | 1 − \|unique texts\| / n ≤ 0.20 | **不过（0.530）** |
| 角色覆盖 | 每篇五个核心角色至少各 1 | 过 |

总判：`deterministic_gate_pass = false`。

Codex 五维（因果 / 数值 / 词多样 / 领域 / 模板）：3 / 3 / 1 / 2 / 1，裁决 `revise`。咨询性，不覆盖数字门。

---

## 4. 适用算法

### 4.1 生成本身用的算法

| 步骤 | 算法 | 作用 |
|---|---|---|
| 主题选择 | 固定种子 Fisher–Yates 洗牌，取前 4 | 无放回主题样本 |
| 剖面分配 | 分位跨步 `floor((i+0.5)n/m)` | 让 8 篇覆盖 12 个经验剖面的分位 |
| 类型配比 | Hamilton / 最大余数（先 floor(Nπ)，余数最大者 +1） | 把多项比例变成整数槽 |
| 槽位打乱 | `Random.shuffle` | 避免语义核总在文首 |
| 语义核放置 | 无放回均匀抽样 | 核心句散布在 body/list |
| 因果核校验 | 三色 DFS 判有向无环 | 允许倒叙，禁止循环因果 |
| reference | 优先级贪心 + 词数盒约束 | 110–180 词抽取式金标准 |
| 重复率 | 大小写折叠后的集合基数 | 模板复制的硬指标 |

### 4.2 分布比较算法

对候选数、页数（reference 词数只报告）：

- **分位数**：线性插值，位置 `(n−1)p`。  
- **归一化 1-Wasserstein**：在 p = 0.005, 0.015, …, 0.995 上取  
  `mean |Q_syn(p) − Q_anchor(p)| / max(1, IQR_anchor)`。  
  这是一维 W1 的分位近似，用锚点四分位距做尺度，避免量纲。  
- **KS**：在联合支撑上  
  `sup |F_syn(x) − F_anchor(x)|`（经验 CDF，点质量用 ≤）。  
  KS **不设门**，只记账。

版面类型用 **全局比例的 L∞ 差**，不是逐篇 Dirichlet。

### 4.3 生成之后允许跑、但不构成确认性结论的算法

仅当调用方声明 `SYNTHETIC_STRESS_NONCONFIRMATORY` 时，同一套 C²GES 选择器可以在这 8 篇上做机制实验：

| 算法 | 在合成集上的含义 |
|---|---|
| 词面质心相关 `Q` | 对虚构全文词袋的代表性 |
| 词法角色 `R` | 对种植 cue 的可执行代理，不是专家角色 |
| 有类型图 `G-T` / 无类型图 `G-U` | 角色转移门 vs 仅距离+Jaccard |
| 路径删除 `C_i = U(G)−U(G_{-i})` | 合格 2–4 边角色路径的结构敏感项 |
| 角色组预留 + Jaccard 冗余惩罚 | AB/RP 因子 |
| 完整排序词预算（110/260，装不下就跳过） | 与探索性试点同一选择器 |
| ROUGE-L F1（porter stemmer） | 相对 **种植抽取式 reference**，不是真实 ES |
| 系列等权配对差、符号翻转、Holm | n_series=4，检验力低；parent 本跑次未作为正式因子晋升 |

因为金标准由同一角色链抽出，路径项在合成集上容易看起来“有用”；这只能诊断 **端点是否与种植结构对齐**，不能外推到 NERC Executive Summary。

### 4.4 明确不适用

- 把 parent 当未见真实系列（E1）  
- 用语义核角色当真人/专家金标准（E2）  
- 用 ROUGE 优势主张系统优越或运维效用  
- 看过重复率之后再改 0.20 阈值  
- 静默重试失败的 API 调用  

---

## 5. 与后两代的关系

| 代 | 角色 |
|---|---|
| **Parent（本文件）** | 第一套；本跑次死在重复率与模板 |
| Child | 只用 Codex 的 `mutation_amendment` 改提示，门阈值不变 |
| Held-out | 换 parent/child 没用过的虚构主题，防把提示调到过拟合 |

Parent 未晋升。Child 即使数字门通过，仍须独立语义门与 held-out 主题；任一失败则整条合成线不得当作论文成绩。

## 6. 产物路径

- 数据：`run_20260910_parent_v2b/synthetic_reports.jsonl`  
- 清单：`SYNTHETIC_RUN_MANIFEST.json`  
- 分布账本：`evaluation/distribution_evaluation.json`  
- Codex：`codex_critic/codex_critic_result.json`（`revise`）  
- 银行决定：`../BANK_DECISION_20260910.json` → `REJECT_BOTH_NO_HELDOUT_ACCESS`
