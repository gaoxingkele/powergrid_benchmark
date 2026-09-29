# Applied Sciences 投稿前工作流

## 1. 为什么升级

旧的 `scripts/papers/build_applied_sciences_versions.ps1` 是一次性迁移脚本：它从历史 CMC 稿截取正文，以字符串替换方式写入旧目录，并在脚本中硬编码标题、摘要、实验数字、作者占位符和 Data Availability。它适合追溯，不适合作为持续投稿工具。继续运行可能覆盖已审计的科学表述、恢复旧结果或产生新的版本漂移。

新的默认原则是：**论文内容由受控修订产生，投稿代码只做只读审计、复现验证和发布收口。**

## 2. CMC 两篇论文沉淀出的七段式模式

1. **恢复唯一基线**：以最新 LaTeX 为唯一正文源；旧 PDF、Word 和旧投稿包只进入 `90_Archive`。
2. **意见结构化**：把评审意见拆成 `问题 → 主张风险 → P0/P1/P2 → 证据需求 → 验收标准`，而不是直接逐句润色。
3. **先冻结口径再跑实验**：先定义 evaluator、split、预算、seed、cluster、主要终点、多重比较族和权利边界，再生成结果。
4. **证据或降级二选一**：强主张必须有对应实验；若外部数据、专家或许可不可得，就收缩标题、摘要和结论，不能用事后诊断冒充确认性证据。
5. **内容与表达分两轮**：先锁定数字、表图、引用和结论，再优化叙事。表达轮不得改变数字、引用键、限定词和证据等级。
6. **双完整性门禁**：正文完整性（claim--evidence、引用、统计、反选择性报告）与制品完整性（代码、数据、图表、PDF、hash、manifest、rights）分别检查。
7. **冻结与人工签核分离**：技术包可以 `PASS`，但 SuSy 中的作者身份、原创性、无一稿多投、全体作者批准和最终上传仍是通讯作者的人工动作。

## 3. Applied Sciences 决策链路

### Gate A：期刊与 Section 适配

- 明确应用对象、工程受益者和使用场景。
- 选择一个主 Section；AI、数据库、信息检索和多智能体系统通常先核对 `Computing and Artificial Intelligence`。
- 若论文只有抽象方法而没有应用验证，先补应用证据或改投更合适的理论/专业期刊。

### Gate B：主张—证据路线

每个核心主张归入以下一类：

- `CONFIRMATORY`：协议先于结果冻结，可支持预设主张。
- `RETROSPECTIVE_DIAGNOSTIC`：结果后分析，只支持诊断与假设生成。
- `IMPLEMENTATION_AUDIT`：证明软件接口或机制被执行，不证明科学效果。
- `EXTERNAL_REQUIRED`：需要未见数据、专家、现场或许可材料；未完成时必须删减对应强主张。

### Gate C：写作保真

- 先写 evidence spine：问题、方法、数据、主要结果、限制、应用含义。
- 摘要按 Background → Methods → Results → Conclusion 单段组织，控制在约 200 词以内。
- Introduction 只承诺 Results 真正回答的问题。
- Discussion 必须解释负结果、敏感性、外部有效性和适用边界。
- 表达优化采用最小差异原则；数字、引用键、统计限定和证据等级变更必须进入 revision ledger。

### Gate D：机械预检

```powershell
python scripts/papers/applsci_preflight.py `
  paper_projects/CMC/C2GES `
  --baseline-ref 840dcce5 `
  --run-project-verifier `
  --output artifacts/applsci_preflight_c2ges.json

python scripts/papers/applsci_preflight.py `
  paper_projects/CMC/MA-SQLGrid `
  --baseline-ref 840dcce5 `
  --run-project-verifier `
  --output artifacts/applsci_preflight_ma_sqlgrid.json
```

预检器检查：

- MDPI `applsci` 文档类和模板文件；
- front matter、IMRaD 和 back matter；
- 摘要词数、关键词数、作者/通讯信息占位符；
- Data Availability 冻结链接或受限说明、GenAI 使用披露；
- citation↔BibTeX、ref↔label、figure↔file 双向关系；
- PDF、代码、数据、图、rights notice、release manifest 和 checksums；
- integrity/reference/visual/build/plan QA、cover letter、author approval；
- SuSy 未签核项目和需要人工复核的强主张词；
- 相对 Git 基线的字数、句长、长句率、数字 token 和引用键变化；
- 每篇论文自己的公共复现验证器（可选）。

`PASS_WITH_MANUAL_GATES` 不是失败。它表示机械与技术门禁已过，但仍有科学判断或通讯作者签核；`FAIL` 才表示存在可自动确认的阻塞项。

## 4. 最终冻结顺序

1. 冻结 LaTeX、BibTeX、图表和补充材料。
2. 运行引用、claim--evidence、统计与选择性报告审计。
3. 运行项目复现验证器和测试。
4. 编译 PDF，逐页视觉检查。
5. 生成 release manifest 与 SHA-256，并从冻结树验证。
6. 生成 cover letter、投稿 checklist 和 author approval form。
7. 建 Git commit + immutable tag；Data Availability 只指向该 tag/DOI。
8. 从冻结 tag 打包，不从含未提交修改的工作区打包。
9. 通讯作者在 SuSy 逐字段核对并完成全部人工声明。

## 5. 不再采用的模式

- 用字符串替换脚本批量重写标题、摘要和实验数字。
- 先润色强主张、后寻找实验支撑。
- 用旧 PDF 判断最新版内容。
- 把事后敏感性、自动审计或实现测试写成前瞻性科学验证。
- 为了“看起来完整”推断邮箱、ORCID、审稿人或权利状态。
- 技术测试通过后直接称为 `submission ready`，忽略人工门户签核。
- 修改 LaTeX 后不重新编译、不更新 manifest/hash 或不做视觉 QA。
