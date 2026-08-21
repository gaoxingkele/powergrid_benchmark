# Applied Sciences 两篇：写作、实验与发布流程回顾

## 1. 目标和当前结论

该项目经历了从 CMC 原稿、标题保留方案、数据与实验补缺、Applied Sciences 模板化、
三轮评审、句式/图表修订到当前发布校正的完整链路。最终标题保持为：

- *Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports*；
- *MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases*。

当前权威产物是 2026-08-09 reference revision，并由 2026-08-11 correction audit 重新
确认：C²GES 25 页、6 图；MA-SQLGrid 28 页、6 图。8 月 8 日的 20 页/4 图 Visual QA
以及被搬入新目录后路径失效的旧脚本均不再代表当前稿。

## 2. 端到端阶段

### 阶段 A：原稿恢复、标题与新贡献边界

先从两份原始 Word 稿恢复题目、领域问题、作者单位和可复用材料，再把上午版本的代码、
算法和数据资产按“可直接复用、需重新验证、仅供历史参考”分类。保留标题不等于保留未经
验证的原结论：标题下的每个算法词必须在方法定义、消融、实验和限制中形成闭环。

### 阶段 B：期刊要求与对照样本

围绕 Applied Sciences 的电网应用论文、摘要/文本方法论文和 Text-to-SQL/多智能体论文
建立对照样本，统计章节、段落、公式、数据集、实验、图表、参考文献和语言模式。样本用于
规划“中位数偏上”的信息密度，但期刊没有统一的页数或图数录用阈值。扩写的依据必须是
缺少方法解释、实验问题、统计证据或工程讨论，而不是凑页数。

### 阶段 C：总计划、实验注册和声明账本

`MASTER_EXECUTION_PLAN.md` 规定数据、实验、写作、图表、评审和组装分工；
`EXPERIMENT_REGISTRY.md` 登记比较矩阵；`CLAIM_LEDGER.md` 约束标题、摘要、结果和结论。
早期 registry 中的 `registered` 或 `blocked` 是历史计划状态，当前完成状态必须由数据处理
总结、正式运行 manifest、post-run audit 和 current release manifest 联合判断，不能只读
旧状态字段。

### 阶段 D：数据分级与处理

C²GES 使用公开和本地的维护/可靠性文本资产，并区分 oracle、predicted 和 label-blind 协议。
机器辅助或大模型裁决形成的标签属于 silver/provenance，不得写成真实专家 gold；真实人工
评审包可以保留为未来扩展，但空白表单不能被当作已完成人工标注。MA-SQLGrid 区分本地
GridDB 验证和公开 BIRD Mini-Dev 正式基线。第三方许可受限材料只能按许可边界供编辑和
审稿人核查。

### 阶段 E：冻结、授权与 BIRD 正式执行

BIRD v1.1 冻结协议为 `MA-PUBLIC-BIRD-MINIDEV-v1.1`，SHA-256：
`0ABA454650C569D51183D4A96248FF977A5DBDF3A82A77C62592162F28F9F640`。运行时固定为
Python 3.10.11 / SQLite 3.40.1，Qwen 后 Granite 顺序执行，新增 5000 次调用。书面授权
是作者对冻结协议与资源使用的批准，不是外部“授权 API”。

v1.0 的 Qwen 原始目录、attempt2 和 attempt3 均是事故证据：原样保留、禁止续跑/覆盖/
删除、禁止计入论文。v101 Qwen/Granite 与旧 promotion gate 属于早期冻结血缘，也不能替代
v1.1 当前证据。v1.1 的 `qwen_clean1` 和 `granite_clean1` 才是当前正式运行；独立 post-run
audit 的 SHA-256 固定在 profile 中。

### 阶段 F：统计、负结果和可主张范围

正式统计从不可变账本重建，使用配对比较、数据库聚类 bootstrap 置信区间和 Holm 校正。
事故调用不进入分母或结果。C²GES 的反事实路径可作为算法机制保留，但在注册消融没有证明
准确率增益时，摘要、结果和结论必须明确负/不显著发现。禁止在看到结果后只调有利超参数、
子集或指标；新的探索必须新建协议，并标注 exploratory。

### 阶段 G：逐章节写作与图表

论文按 Applied Sciences 模板重写问题定义、理论基础、算法、复杂度、数据、实现、比较、
消融、稳健性、效率、案例、局限和工程意义。两篇均有六幅图；框架图和详细模块图承担不同
功能。当前矢量/出版图的源、生成脚本和 PDF 引用关系由 release lineage 管理。生成式图像
只用于非数值概念草图，最终算法图需重绘为可复现的 SVG/PDF；任何结果图必须来自真实数据。

### 阶段 H：三轮评审和修改

三轮覆盖逻辑、方法统计、理论创新以及电网应用/期刊完整性。第一轮检查任务边界、基线公平、
泄漏和统计单位；第二轮检查工程价值、跨场景验证、敏感性、效率和图表叙事；第三轮以苛刻
审稿人视角检查声明、引用、两篇之间的独立性、编译和投稿声明。评审材料与当前 release
分开保存，最终 release 的小范围修正仍需通过 current audit，而不能假定旧 checklist 自动
覆盖新文件。

### 阶段 I：当前版本校正与发布完整性

`VERSION_BOUNDARY.md` 明确新旧目录；`CURRENT_RELEASE_MANIFEST.json` 绑定当前 TeX、PDF、
图片和生成脚本；`CURRENT_AUDIT_CORRECTION_REPORT_2026-08-11.md` 修正 MA-SQLGrid 页数/
图数以及旧材料混装问题。核心 harness 再校验四个 TeX/PDF 哈希和 BIRD 两个关键哈希。
构建脚本能从自身文件位置解析路径，但默认不运行，因为它们会写 manifest 或 QA 输出。

### 阶段 J：人工投稿门禁

作者/单位、基金号 521300250006、CRediT、数据可用性和“all authors have read and agreed”
需在最终 TeX 中复核。Yang Yong 为通信作者，其独立投稿邮箱仍需作者确认；不能用另一作者
邮箱替代而不说明。Harness 不发送邮件、不上传受限数据、不自动投稿。

## 3. 标准变更流程

任何改动先分类：

1. 仅元数据：改 TeX → 编译 → 视觉/引用检查 → 新 release manifest 与 ZIP；不重跑实验。
2. 文字但不改声明：改 TeX → claim/引用/句式审计 → 编译与视觉 QA → 新 release。
3. 改定量结果或方法：新实验注册 → 新冻结/授权 → 新目录执行 → 独立统计审计 → 更新
   claim ledger、正文、图表 → 三轮复核 → 新 release。
4. 修复冻结实现缺陷：修订协议、回归测试、重新冻结、独立审计和重新授权；原事故目录保留。

不得直接覆盖当前发布，也不得把 `_archive_pre_current_audit` 中的旧审计或脚本复制回当前目录。

## 4. Harness 解决的核心问题

- 用路径与 SHA-256 明确“当前稿是谁”；
- 用 DAG 阶段阻止未冻结实验直接进入正文；
- 用 canonical/legacy/incident 三类根目录阻止事故运行和历史稿混入；
- 把统计和声明门禁放在写作之前；
- 把写作完成与投稿授权分开；
- 默认只读，所有会重跑实验或改写发布物的命令均需人工启动。

