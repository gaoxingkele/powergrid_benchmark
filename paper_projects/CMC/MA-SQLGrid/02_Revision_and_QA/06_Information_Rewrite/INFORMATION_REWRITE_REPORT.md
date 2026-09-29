# MA-SQLGrid：Information 文献蒸馏与改写交付报告

日期：2026-09-12。状态：本轮文献学习与稿件改写完成；不是录用保证或全套投稿门禁通过证明。

## 1. 交付版本

- [Information LaTeX 主稿](../../01_Manuscript/LaTeX/paper_information.tex)
- [Information PDF 主稿](../../01_Manuscript/LaTeX/paper_information.pdf)：28 页，12 张表，6 幅图，39 条参考文献。
- [新增参考文献](../../01_Manuscript/LaTeX/references_information.bib)
- [编译说明](../../01_Manuscript/LaTeX/BUILD_INFORMATION.md)
- [机器核验结果](REWRITE_AUDIT.json)

题名保持为 *MA-SQLGrid: An Auditable Coordination and Evaluation Framework for Power-Grid Text-to-SQL*。作者顺序、单位、通讯邮箱、基金等沿用原稿。原 Applied Sciences 文件未覆盖。本轮没有发送邮件、提交期刊、创建 Git 提交或推送远端，也不把历史作者批准自动视为对新稿的批准。

## 2. 下载并精读的四篇样本

| 样本 | 全文 | 用途及不能外推的边界 |
|---|---|---|
| Wardani 等，2026，*An SQL Query Description Problem with AI Assistance for an SQL Programming Learning Assistant System*，Information 17, 65，[DOI](https://doi.org/10.3390/info17010065) | [33 页 PDF](literature/pdf/info17010065.pdf) | 学习任务、参与者和验证层次的说明方式；其学生研究不能替代本稿的用户实验 |
| Avignone 等，2025，*Exploring Large Language Models’ Ability to Describe Entity-Relationship Schema-Based Conceptual Data Models*，Information 16, 368，[DOI](https://doi.org/10.3390/info16050368) | [19 页 PDF](literature/pdf/info16050368.pdf) | 学习语义对象、结构提示和指标的对应；ER-to-text 不是本稿的直接性能基线 |
| Çetinkaya，2025，*A Systems Approach to Validating Large Language Model Information Extraction: The Learnability Framework Applied to Historical Legal Texts*，Information 16, 960，[DOI](https://doi.org/10.3390/info16110960) | [16 页 PDF](literature/pdf/info16110960.pdf) | 学习分层验证及分歧分析；内部可预测性不能替代语义真值 |
| Gharbi，2020，*A Social Multi-Agent Cooperation System Based on Planning and Distributed Task Allocation*，Information 11, 271，[DOI](https://doi.org/10.3390/info11050271) | [21 页 PDF](literature/pdf/info11050271.pdf) | 学习协议对象、条件和形式性质的组织；有限模型性质不能推出整体系统正确性 |

检索主题覆盖 SQL、数据库自然语言接口、模式解释、LLM 验证与多智能体协调。这是用于编辑决策的目的性样本，不是系统综述，也不能推导期刊录用概率。四篇均保留全文、文本提取、Crossref 身份信息、OpenAlex/Unpaywall 查询记录和下载 SHA-256，见 [manifest](literature/manifest.json)。未取得的引用次数保留 null，不据此排序。

初始 MDPI 主站 PDF 路由出现 403；实际获取使用冈山大学机构仓储及 MDPI 自有资源域名上的合法开放 PDF。下载遵循项目的 aria2 优先流程，下载入口与备用来源保留在 `acquire_literature.py`。最终四份均通过文件哈希和首页 DOI 核验；不能把初始路由失败表述为一次全部成功。

逐篇全文分析、页码依据及不足分别见：

- [SQL 与模式解释两篇蒸馏](literature/sql_schema_distillation.md)
- [验证与协同两篇蒸馏](literature/validation_coordination_distillation.md)

## 3. 三个维度的合并蒸馏

### 3.1 语句风格

采用具体对象作主语，说明输入、动作、输出和限制。减少模块名堆叠、笼统赞誉和重复导航句；每个结果段先给比较对象和实测现象，再给有限解释。样本文献中部分“可靠”“可扩展”“减负”措辞超过其测量范围，本稿没有模仿这些强结论，也没有复制原句。

新稿中的表达实例是本轮原创改写，不是样本文献引文：

- `Executable SQL is not necessarily a correct answer to a natural-language question.` 把研究对象和关键区别放在摘要第一句。
- `This separation supports reproducible inspection of selection failures; it is not, by itself, evidence of better answers.` 在提出设计价值的同一句中限定证据边界。
- `Changing a source-order tie breaker alone supplies no missing meaning.` 将形式性质转为读者能理解的设计含义。

### 3.2 叙事逻辑

从“介绍五个角色，然后罗列实验”转为“提出可执行与答对之间的缺口，定义可用证据，说明规则能保证什么，用候选池结果检验局限，再讨论生成与状态证据”。

贯穿主线为：任务歧义 → 资格门与评分 → 有限性质 → 选择失败及并列原因 → 上下文、状态与跨库的补充证据 → 设计启示及未验证部分。摘要、三个 RQ、结果小节、讨论和结论采用一致问题框架。引言维护日期例子明确标为 illustrative；真实 Q039 保留现有记录，不虚构新案例。

### 3.3 理论深度

没有为增加公式而附会信息论或认知理论。新增三条针对现有确定性选择规则的有限性质，并给出假设、证明和解释：

1. **资格集合与候选池上界**：选择不能超出合格池；正确候选不存在、被门禁排除与存在但未选中是不同失败来源。逐题 oracle 上界不等于最佳固定来源，更不是可部署选择器。
2. **最高分集合的次序依赖**：唯一最高分不受次序影响；并列项可因排列而被选中。只有并列集混有评估正确和错误候选，正确率才可能随次序变化。逐题可达结果不能直接相加为单一全局排序可达结果。
3. **观测证据的不可区分性**：相同选择器输入若对应互斥的正确解释，确定性选择无法同时满足二者。该性质不说明所有实测并列都来自业务歧义，也不证明当前特征已经捕获真实含义。

这些是解释性性质，不宣称数学新颖性、一般 SQL 等价保证或性能提升。512 个三候选穷举例子只是证明的代码健全性检查，不计作新增模型实验，也不能替代一般证明。

## 4. 逐章实际改动

| 章节 | 本轮改动 | 证据边界 |
|---|---|---|
| 摘要与关键词 | 重写为问题、接口、有限性质、实验结果、解释边界；187 词、7 个关键词 | 明示 76/99/100 与最佳固定来源 129，不隐去负向比较 |
| Introduction | 重写问题动机、示例、三个 RQ 和贡献；解释候选产生与选择是不同能力 | 不把五角色数量当作已验证的创新效果 |
| Related Work | 新增 Information 中数据库解释与 SQL 教学两篇的准确定位；区分 SQL 记忆系统与 Text-to-SQL | 仅两篇与论证直接有关者进入参考文献，另外两篇仅用于写作蒸馏，不为同刊引用而堆砌 |
| Methods | 将 gate-score-tie 规则放在角色介绍之前；新增 Formal Scope 小节与三条性质 | 历史执行器、后续加固、离线金标准与在线选择严格区分 |
| 数据与实验协议 | 保留并审阅分母、开发可见性、调用预算、模型快照、统计族及状态限制 | 未重跑模型，未把合成 GridDB 写成真实生产基准 |
| Results | 重排为选择比较、并列与 Q039、生成组件、状态、BIRD、实现；与 RQ 对应 | 12 个表格块原样保留，6 幅图沿用；重排自动更新编号 |
| Discussion | 重写为过滤与选择的区别、witness 的区分能力、次序政策、模型依赖、信息系统启示和限制 | 未把统计不显著解释为等价；未把状态一致解释为业务正确 |
| Conclusions | 回答规则范围、实测短板与后续证据需求 | 不主张端到端协同优势或工程效率收益 |
| 格式与声明 | 使用 MDPI `information` 类选项，移除 Applied Sciences 专用应用段及模板虚拟 DOI；保留声明并说明旧发布标签不含新稿 | 新稿是本地草稿，模板中的 submitted 字样不是已完成投稿的事实 |

## 5. 验收结果与范围

| 用户要求或不变量 | 当前可核查证据 | 结果 |
|---|---|---|
| 搜集相关 Information 文章并下载 | 4 个 PDF、manifest、来源脚本、首页 DOI 与 SHA 检查 | 完成 |
| 提炼句式、叙事、理论深度 | 两份全文逐篇分析及本报告第 3 节 | 完成 |
| 应用于本论文而非只给建议 | 独立 `paper_information.tex`、新增文献库和 28 页 PDF | 完成 |
| 原稿不覆盖 | 原 LaTeX SHA 与起点完全相同 | 通过 |
| 表格和图内容不漂移 | 12 个带标签表格块逐一一致；6 个图文件引用集合一致，只有顺序改变 | 通过 |
| 引用与交叉引用 | 缺失 bibkey、缺失 label、重复 label 均为空；最终参考文献 39 条 | 通过 |
| 理论内容有边界 | 正文 3.3 的假设、证明、oracle/次序/歧义限制及 512 个有限例子 | 通过本轮解释性理论检查 |
| 编译与版面 | 最终编译日志无 LaTeX 错误、Overfull、未定义引用或 rerun 请求；28 页全部渲染检查 | 通过 |

视觉检查涵盖第 1–28 页的页眉页码、标题、表格、公式、算法、图注、参考文献和声明；没有发现裁切、重叠或缺字。密集结果表保留原内容和缩放方式。本次为代理视觉审阅，不冒称独立人工或作者签核。

最终检查绑定：

- 原稿 SHA-256：`75a3cbb673ee687522e41dc296440bb1433c098a52bbccdfbeeb1a44d7410a5d`
- Information LaTeX SHA-256：`bcee5e325d140dbf949d3012c12644e876b46f8f4a71c7eeb1b7b783735cf95b`
- Information PDF SHA-256：`66990e91cc4a3375a1c5bdefdca052a617ba57872249f627022884549985ba43`
- 环境：Python 3.12.10；MiKTeX-pdfTeX 4.23 / MiKTeX 25.12。MiKTeX 提示尚未检查更新，属于环境维护提醒，不是本稿编译错误。

## 6. 不应被本轮完成状态掩盖的事项

本轮完成的是用户指定的“搜集、下载、蒸馏、格式与内容改写”，不是新增确认性实验、全参考文献重新查新、作者签核或正式投稿。原有开发可见性、小型合成数据库、负向选择结果、缺少独立电力语义验证等科学限制仍存在；文字改写不能消除它们。

格式使用本地 MDPI 模板的 Information 选项，并参考 [MDPI 通用排版说明](https://www.mdpi.com/authors/layout) 与 [MDPI 模板](https://www.overleaf.com/latex/templates/mdpi-article-template/fcpwsspfzsph)。Information 专用 instructions 页面本轮自动访问受限，未据此声称所有实时门户政策已复核。正式转投仍需核对当时投稿要求、补充材料上传组合、版权和作者批准；旧投稿信不应直接作为新刊投稿信。

历史补充材料及发布标签继续作为原实验的溯源，不被本轮重写。补充目录 README 已区分历史 row-only 与后续统一评估口径；本稿明确旧标签不含 Information 改写。若下一步制作正式提交包，应另建版本化清单，不能沿用旧清单声称它绑定新 PDF。
