# Applied Sciences 双论文最终交付记录

日期：2026-08-06  
范围：MA-SQLGrid 与 C2GES 的本地科学、实验、稿件、图表、复现包和三轮复核闭环。

## 1. 同刊十篇样本的结构基准

本地参考语料包含 10 篇 Applied Sciences PDF 和对应的 10 份 JATS XML。经核验的中位数为：24 页、7098 个正文词、5 个一级章节、26 个编号公式、1 个评价数据集、9 幅图、5 张表和 2 幅框架图。该语料用于结构与实验密度校准，不用于替代两篇论文各自的科学证据。

## 2. MA-SQLGrid

- 题目、作者顺序、两家单位、通讯作者及邮箱沿用原 CMC 稿。
- 最终稿：26 页；6 个一级章节、27 个二级章节、9 张表、9 幅图、7 个 equation 环境；摘要约 187 词。
- 主要实证：1440 次双骨干 2×2 因子预测、700-call 组件实验、25,920 行 15 个语义状态与 3 个物理顺序诊断、多重校正和独立复算。
- 结论保留负结果：9 个主因子执行效应均未通过家族校正；值证据只在 Qwen 条件达到既定规则；确定性选择未在两模型上达到规则；多状态 9 个效应均未通过 Holm 校正。
- 91 个 RTS-GMLC/SimBench 外部候选仍是开发可见的自动候选，不冒充专家金标准或 sealed test。
- BIRD 协议为 `FROZEN_NOT_RUN`：500/500 gold-query preflight，计划 5000 次调用，正式调用为 0；没有伪造授权或结果。
- 证据验证：v2=26、v3=15、component=4；9 幅图、23 个引用键通过。
- 可移植语义包在原目录与全新复制目录均通过 19 文件检查；连续两次 PDF 构建字节一致。

当前身份：

- TeX SHA-256：`DE9DDB9EFF1FCF977715529C037FAD2BBEF129AFDD95AAB2940B5CDD139A9C7B`
- PDF SHA-256：`A9DEDF763D7F4F6F0154157DD35B0CB1616098CBD84543ED095B539465B288FA`
- portable manifest SHA-256：`E6313B274CFB396835C099059E8105FC4D98D4D6FF895F2FE0E4127C1261AB07`

## 3. C2GES

- 题目、作者顺序、两家单位、通讯作者及邮箱沿用原 CMC 稿。
- 最终稿：24 页；6 个一级章节、18 个二级章节、10 张表、9 幅图、5 个 equation 环境；摘要约 184 词。
- 主研究完整披露为 1 个已检查 pilot seed 加 4 个前瞻 continuation seeds，不将五个种子全部称为前瞻实验。
- 现代强基线包括 frozen MiniLM 和 BGE cross-encoder；MiniLM 差值与 BGE 三比较族均未产生 Holm-adjusted promoted finding。
- 新增 5 upstream × 5 downstream 的 25-pipeline 矩阵：30/30 child 成功，25 个 ledger 各 54,000 行；分析选择 450,000 行，主单元含 37,500 条 full@K=3 记录。
- 5×5 主均值 F1 为 0.4905990053；上游、下游、交互/残差描述性方差分量分别为 0、2.1550742e-6、2.8572893e-6；文档组成敏感性区间为 [0.4730345, 0.5080023]，不是总体置信区间。
- 独立流式复算未导入 analyzer、未读取其 cell summary；主均值完全一致，方差分量最大绝对差为 3.22e-20。
- 正文明确 5×5 不重新估计 role effect、no_role 不是重训的 label-blind 模型；BGE 区间条件于完整 frozen five-seed bundle。
- 43 个源哈希、11 个生成片段、9 幅图、28 个引用键通过；superseded-claim audit 通过。
- 探索图已复制进独立稿件目录并与冻结源同哈希；连续两次 PDF 构建字节一致。
- 本地复现清单：11,673 个文件，2,196,680,670 bytes；全部 SHA-256 和 5 项 canonical gzip 检查通过。

当前身份：

- TeX SHA-256：`3901BD8BAF58C371522FEAB76112B02195828394856484B851ED672C24B86FDB`
- PDF SHA-256：`022208A0CA1E1282CCF3058B705EBCEB60E1B1DF98CEEB483AC45643585C4ADB`
- claim-source map SHA-256：`BF97F0AB00C7F29488E7822512F4012F6D90AF2FBACD86149165B83B461BD51D`
- bundle manifest SHA-256：`613C50522238FFE52CE59DA637114BD677E5625FD1380B4988186F5DE884E4BA`
- 5×5 results SHA-256：`5A04D3F315821E899583819E6654CEDF29B2D366ECBB7133D01C543D41A8AD9F`
- independent audit SHA-256：`BC1F7A02D4D567542B0E862F784045AEEA47E74C988E202CF46D53F83E38C297`

## 4. 复核闭环

两篇论文均完成方法/统计、期刊/领域、图表/版面和最终反方复核。C2GES 的后集成复核提出的本地问题均已修复并重新验证：标题与应用陈述一致、孤立稿件图路径、BGE 条件边界、MoM 公式与自由度、未校正主表注释、讨论措辞和 PDF metadata 均已闭环。最终日志无未定义引用、overfull、underfull 或 LaTeX fatal error。

正文及其生成表未发现 W*、Round*、agent reviewer、response letter、post-review、NO-GO 等内部过程措辞。期刊合规的生成式 AI 使用披露保留在 Acknowledgments；这不是把内部协作过程写入学术论证，也不能为满足“无痕迹”而隐瞒真实使用。

## 5. 仍需真人完成的投稿动作

以下项目没有由自动化过程代填或伪造：

1. 两篇论文的资助编号。
2. 全体作者对 CRediT、利益冲突、资助方角色、伦理/知情同意和生成式 AI 披露的书面确认。
3. FEVER、NERC、GridDB、RTS-GMLC 和 SimBench 相关再分发与许可审查。
4. 永久公开仓储 URL/DOI。
5. 若要提升 MA-SQLGrid 的外部准确率主张：真实双专家审查、争议裁决和新的 sealed set；若保留 BIRD 正式比较，则还需明确的人类启动授权。
6. 若要提升 C2GES 的电网域性能主张：独立 NERC 专家标注、裁决和 sealed validation。

在这些真人动作完成前，两篇稿件是“本地科学与制品闭环、投稿声明尚未最终签署”，不能表述为已经具备无条件投稿状态。
