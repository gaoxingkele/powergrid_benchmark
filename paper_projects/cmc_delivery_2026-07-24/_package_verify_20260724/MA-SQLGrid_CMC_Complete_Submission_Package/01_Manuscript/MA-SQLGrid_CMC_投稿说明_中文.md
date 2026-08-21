# MA-SQLGrid 论文 CMC 投稿说明

## 一、投稿前准备

1. 确认题目、作者顺序、作者单位、通信作者和 ORCID 信息。
2. 将资助编号占位符 `[AUTHOR INPUT REQUIRED: grant number]` 替换为真实编号。
3. 核对正文、Cover Letter 与投稿系统中的通信作者信息完全一致。
4. **通信作者邮箱要重新申请方便接收邮件和修改。**
5. 确认所有作者同意投稿，并完成数据、代码和模型服务使用情况核查。

## 二、建议上传文件

1. `MA-SQLGrid_CMC_revised_20pages.pdf`：CMC 模板主文 PDF。
2. `MA-SQLGrid_CMC_LaTeX_revised.zip`：可编译 LaTeX 投稿源文件。
3. `MA-SQLGrid_CMC_Manuscript_Word.docx`：可编辑 Word 版本。
4. `MA-SQLGrid_CMC_Supplementary_revised.pdf`：补充材料。
5. Cover Letter：重点说明固定数据库上的 compact contract-aware pipeline、第二生成器复核及评估约定敏感性。
6. 数据和代码根据投稿系统要求作为 Supplementary File、Data Availability 链接或审稿附件提交。

## 三、在线投稿步骤

1. 进入 Tech Science Press 的 CMC 投稿系统，注册或登录作者账号。
2. 选择 `Computers, Materials & Continua`，稿件类型选择 `Article`。
3. 填写题目、摘要、关键词、作者、单位、通信作者、基金及利益冲突。
4. 上传主文 PDF、LaTeX 源文件、补充材料和 Cover Letter。
5. 填写 Data Availability、Author Contributions、Funding、Conflicts of Interest、Ethics Approval 和 AI 工具使用披露。
6. 如系统要求推荐审稿人，应排除同单位人员、近期合作者和其他利益冲突人员。
7. 生成系统合并 PDF，检查公式、SQL 示例、表格、图、作者信息和参考文献。
8. 所有作者确认后，由通信作者提交并保存稿件编号。

## 四、提交后处理

1. 定期检查通信作者邮箱、垃圾邮件和投稿系统。
2. 技术审查阶段及时补交源文件、高清图片、数据声明或作者信息。
3. 收到审稿意见后制作逐条回复，提交修订稿、清洁稿及 Response to Reviewers。
4. 统一文件版本编号，避免不同邮箱和聊天工具中出现多个未确认版本。

## 五、这篇论文需要特别说明的事项

- 研究只覆盖一个合成、确定性的维护数据库，不能外推为跨数据库结论。
- compact 条件同时包含 answer-shape guidance，缺少完整的 context-by-shape 2×2 因子实验。
- 投影容忍重评分会反转 full-schema 与 compact 条件的排序，严格指标增益主要来自答案契约一致性。
- 原生成器上的验证增益没有达到统计显著，应保持诊断性表述。
- 十倍扩容实验是非对称工程诊断，不能表述为对称的 schema-generalization 测试。
- 资助编号仍需作者确认。
