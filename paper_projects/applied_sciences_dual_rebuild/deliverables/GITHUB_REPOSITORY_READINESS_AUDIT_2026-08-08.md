# GitHub Repository Readiness Audit — 2026-08-08

## 1. 审计范围与结论

本审计对以下两个指定 GitHub 仓库进行匿名、只读核验；没有执行 push、tag、release、issue、PR 或其他远端写操作。

- [gaoxingkele/c2ges](https://github.com/gaoxingkele/c2ges)
- [gaoxingkele/ma-sqlgrid](https://github.com/gaoxingkele/ma-sqlgrid)

核验时间：2026-08-08 18:55（Asia/Shanghai）。远端事实来自 GitHub 公开网页及 GitHub REST API；本地对照来自当前工作区内的 2026-08-08 最终候选文件。由于 C2GES 的 `FINAL_CANDIDATE` 仍在收口而尚未形成最终不可变投稿 ZIP，其比对结论应视为“对当前候选状态的充分不一致证据”，而不是对尚未生成 ZIP 的逐字节等同性审计。

**总判定：两个仓库均公开可访问、均有 README、MIT 代码许可证、标签和正式 Release；但两个仓库的当前 `main`/`v0.2.0` 均不能证明与 2026-08-08 原标题最终候选稿及其新实验资产一致。投稿前必须同步并建立新的、提交哈希绑定的不可变 Release，然后从全新克隆目录复验。**

| 项目 | C2GES | MA-SQLGrid |
|---|---|---|
| 匿名访问 | PASS：Public | PASS：Public |
| 默认分支 | `main` | `main` |
| README | PASS | PASS |
| GitHub 识别的代码许可证 | MIT | MIT |
| 标签/正式 Release | `v0.1.0`, `v0.2.0` | `v0.1.0`, `v0.2.0` |
| 最新 Release | `v0.2.0` | `v0.2.0` |
| 与 2026-08-08 当前最终候选明显一致 | **FAIL/未同步** | **FAIL/未同步** |
| 当前能否在稿件中声称“公开仓库精确复现本稿” | **不能** | **不能** |

当前两篇稿件中“仓库必须同步、打标签并从 fresh clone 验证后方可作精确复现声明”的保守文字与本次审计证据一致，不应在完成同步前删去。

## 2. C2GES 仓库

### 2.1 远端状态（可核验事实）

- 仓库：`gaoxingkele/c2ges`，Public，未 archived，未 disabled。
- 默认分支：`main`。
- `main` 最新提交：[`d247219e0f8685186616298a338a475bee1810c4`](https://github.com/gaoxingkele/c2ges/commit/d247219e0f8685186616298a338a475bee1810c4)。
- 提交作者/提交者时间：2026-07-20 14:34:48 UTC，即 2026-07-20 22:34:48 Asia/Shanghai。
- 仓库 `pushed_at`：2026-07-20 14:35:32 UTC，即 2026-07-20 22:35:32 Asia/Shanghai。
- 最新提交信息首行：`Add dataset workspace, executor artifacts, and learned/LLM baseline runs`。
- 递归树：94 个条目，GitHub API 返回 `truncated=false`，因此本次文件名缺失检查覆盖完整远端树。
- 根目录可见：`README.md`, `LICENSE`, `MISSING_ARTIFACTS.md`, `baseline_runs/`, `code/`, `corpus_manifest/`, `dataset/`, `pipeline/`, `supplement/`。
- README Git blob SHA：`6a5fb95b46ac2625a2c48a22239b4a11d8f03876`，9085 bytes。
- LICENSE Git blob SHA：`8655bd98223276ad02bacd3a97e37aa1916236d5`，1068 bytes；GitHub 识别 SPDX 为 `MIT`。
- 标签：`v0.1.0`、`v0.2.0`。
- 正式 Release：
  - [`v0.2.0`](https://github.com/gaoxingkele/c2ges/releases/tag/v0.2.0)，非 draft、非 prerelease，发布于 2026-07-20 14:35:33 UTC（22:35:33 Asia/Shanghai），指向上述 `d247219...`；无独立上传 assets，仅由 GitHub 提供源码压缩包。
  - [`v0.1.0`](https://github.com/gaoxingkele/c2ges/releases/tag/v0.1.0)，非 draft、非 prerelease，发布于 2026-07-19 08:45:07 UTC。

### 2.2 README/许可证所描述的远端研究资产

远端 README 将论文 working title 写为 **“C2GES: Causal-Role-Conditioned Evidence Sentence Selection for NERC Reliability Reports”**，并描述：

- 40 个已处理 NERC 文档、2940 句、200 个角色条件问题、608 个候选 evidence IDs；
- 12 个条件乘 200 个问题的 2400 行 Executor 结果；
- 主要以 `K=3` 评价，并有 `K in {1,3,5}` 敏感性分析；
- BGE、Cross-Encoder 和 DeepSeek 零样本基线；
- README/Release 声称 `v0.2.0` 已补全其所对应旧稿所需的 material artifacts。

README 对权利的表述是：代码采用 MIT；NERC 原始文档仍受 NERC 条款约束；处理数据是由公开文档派生的 agent-generated candidate labels。仓库根目录只有一个 GitHub 可识别的 MIT `LICENSE`；派生数据的适用许可边界主要依靠 README 文字说明。

### 2.3 与本地当前最终候选的比对

本地对照稿：

- 标题：**“Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports”**；
- `paper_applsci.tex` SHA-256：`5C56F9751515F03E5FEBA7C4DFF380CF57280121B5592CD306046322929A03D6`；
- 当前研究流程：40 份完整 PDF 经确定性门控保留 27 份，12 份 development、15 份 test；正式测试为 7 个条件、`K=5/10`、共 210 个 predictions；另含 v0.3.1 冻结协议、精确 sign-flip 敏感性分析、开发集 counterfactual calibration、输出长度审计和 1575 条选择项页码定位记录。
- v0.3.1 冻结清单 SHA-256：`DE3205B0BC8DF65706B40B696F7313953E5905AA875128B569EECB685DAB19B5`。
- 输出长度审计 SHA-256：`3C5420A576CB024307541C6EA29CE36098897F6C8D1148ACC9F540C4E1617878`。
- 页码定位表 SHA-256：`26AD087BA7355C0AD7A6EFF93948167C21C150DA759A55FE4F2EE76ECF304DBC`。

完整远端树中未发现 `TEST_FREEZE_MANIFEST_v0_3_1.json`、`OUTPUT_LENGTH_AUDIT.json`、`selected_page_locator.csv`、`posthoc_dev_cf_calibration` 或 `postrun_sensitivity` 等当前候选关键资产，也未发现当前稿件源文件 `paper_applsci.tex`。

**一致性判断：**二者有 C2GES 方法家族、40 份 NERC 来源文档及可复现性方向上的历史连续性，但研究问题、标题、样本单位、筛选流程、测试划分、评价预算、正式结果和补充审计均明显不同。远端 `v0.2.0` 是旧研究包，不能作为当前原标题候选的精确代码/数据版本。尤其不能因 README 写有“no material artifact remains missing”而推断当前 8 月 8 日稿件的材料已经同步；该表述只适用于其 7 月 20 日对应版本。

### 2.4 投稿前必做

1. 待 `FINAL_CANDIDATE` 真正冻结后，只同步权利允许公开的代码、配置、非逐字元数据、审计和结果；不得上传受限 PDF、抽取原文或 restricted-local ledger。
2. README 改为当前准确标题，并清楚区分：标题所指维护应用是预期用途、实证人口是 NERC technical-report proxy、反事实项未显示 ROUGE 增益。
3. 建立新的不可变标签/正式 Release；版本号不得复用或移动现有 `v0.2.0` 标签。Release notes 应记录稿件/冻结清单/安全公开包的 SHA-256 和适用权利边界。
4. 从匿名全新克隆运行仓库自带检查，核对其生成结果与稿件及投稿 ZIP 的精确哈希/数值一致，再更新 Data Availability 的肯定式措辞。

## 3. MA-SQLGrid 仓库

### 3.1 远端状态（可核验事实）

- 仓库：`gaoxingkele/ma-sqlgrid`，Public，未 archived，未 disabled。
- 默认分支：`main`。
- `main` 最新提交：[`837b4fdaf9e39d5dd4ab7704a804144e2461bad4`](https://github.com/gaoxingkele/ma-sqlgrid/commit/837b4fdaf9e39d5dd4ab7704a804144e2461bad4)。
- 提交作者时间：2026-07-20 14:06:33 UTC（22:06:33 Asia/Shanghai）；提交者时间：2026-07-20 14:07:01 UTC（22:07:01 Asia/Shanghai）。
- 仓库 `pushed_at`：2026-07-20 14:17:56 UTC，即 2026-07-20 22:17:56 Asia/Shanghai。
- 最新提交信息首行：`Add x10 scale experiment + received builder modules`。
- 递归树：4118 个条目，GitHub API 返回 `truncated=false`，因此本次文件名缺失检查覆盖完整远端树。
- 根目录可见：`.gitignore`, `README.md`, `LICENSE`, `MISSING_ARTIFACTS.md`, `assets/`, `code/`, `data/`, `evidence/`。
- README Git blob SHA：`79723ed588d3e36fc00b3e915f66ac067589f373`，11499 bytes。
- LICENSE Git blob SHA：`8655bd98223276ad02bacd3a97e37aa1916236d5`，1068 bytes；GitHub 识别 SPDX 为 `MIT`。
- 标签：`v0.1.0`、`v0.2.0`。
- 正式 Release：
  - [`v0.2.0`](https://github.com/gaoxingkele/ma-sqlgrid/releases/tag/v0.2.0)，非 draft、非 prerelease，发布于 2026-07-20 14:17:56 UTC（22:17:56 Asia/Shanghai），指向上述 `837b4fd...`；无独立上传 assets。
  - [`v0.1.0`](https://github.com/gaoxingkele/ma-sqlgrid/releases/tag/v0.1.0)，非 draft、非 prerelease，发布于 2026-07-19 08:45:06 UTC。

### 3.2 README/许可证所描述的远端研究资产

远端 README 将论文 working title 写为 **“A Multi-Stage Context-Grounding Framework for Reliable Text-to-SQL over Power-Grid Maintenance Databases”**，并描述：

- 200 个 GridDB 问题，20 dev / 180 test，及一个确定性 x10 数据库变体；
- `gpt-5.4-mini` 的五条件 900 条预测/评分记录；
- `deepseek-chat` 的 C2/C4/C5 复现、温度零一致性检查和 x10 的 540-call 运行；
- 旧 evaluator、原始 builder/smoke modules 及分析脚本；
- 两项仍不可得的历史上游资产：原 `researchclaw.llm.client` 和 v0.1 数据集生成器。

README 对权利的表述是：`code/` 为 MIT；`data/`、`evidence/`、`assets/` 和 `outputs*` 为 CC BY 4.0。根目录的 GitHub 许可证检测只识别一个 MIT `LICENSE`；数据/运行资产的 CC BY 4.0 主要写在 README，而不是单独的机器可识别数据许可文件中。

### 3.3 与本地 FINAL 包的比对

本地对照稿：

- 标题：**“MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases”**；
- `paper_applsci.tex` SHA-256：`57F21F8AD8A7031BC3CA1F7B360C2E3FD17AB11B138A88E098CC01FEED41B5CA`；
- 新架构明确为五角色、append-only blackboard、确定性 adjudicator 和数据库强制只读执行；
- 当前稿件综合 1440-prediction GridDB factorial、700-call prospective component、25,920-row multi-state ledger、5000-call BIRD Mini-Dev Qwen/Granite 对比，以及对 5760-attempt 历史候选集合的 release-v3 描述性重执行；
- FINAL executor SHA-256：`15723D46506806AE2ED15828AB980187B4828948C4FD3269010B5957E735B6B1`；
- 五角色代码 SHA-256：`EA8105FC3AB6F8F54B59E74B0AD9AC96D5CD1ABB073469C51E9DB5A7066915BE`；
- release-v3 summary SHA-256：`90179DEE2200B924E2BB2DBA23445B0B5AB585FE65FC0D4D299ECCC559372E4E`。

完整远端树中未发现当前 FINAL 的 `sqlite_readonly_executor_final.py`、`ma_sqlgrid_agents.py` 或 `release_v3` 资产；亦未发现 BIRD/Qwen/Granite 当前正式实验资产或当前稿件源文件 `paper_applsci.tex`。远端主要生成器仍是 `gpt-5.4-mini` 和 `deepseek-chat`，与当前稿件中 Qwen/Granite 的正式 BIRD 研究及另外的组件/状态/选择器证据不是同一实验版本。

**一致性判断：**二者共享 GridDB 180-test 历史资产、Text-to-SQL 主题、SQLite evaluator 和上下文/验证模块的历史连续性，但远端尚不包含当前 FINAL 的五角色实现、安全执行器、BIRD 正式结果、prospective component study、multi-state ledger、release-v3 选择器证据、supersession notice 或最终测试/审计。因此 `v0.2.0` 不能作为当前原标题 FINAL 的精确复现版本。

### 3.4 投稿前必做

1. 将当前 FINAL 安全公开子集同步到仓库；保留 BIRD、第三方 grid data、事故目录和受限材料的许可边界，不把“可向作者申请核查”误写成公开再分发授权。
2. README 改为准确标题和当前证据层次，明确历史 prompting experiments、prospective component experiment 与五角色架构不是同一个端到端多智能体实验。
3. 加入 FINAL executor、五角色代码、测试、release-v3 supersession authority、完整数值表和 figure lineage；不得用远端旧实验的通过状态替代当前 FINAL 的 14-test/30-test 和 clean-extraction 证据。
4. 建立新的不可变标签/正式 Release，记录最终稿、代码、清单和安全公开包 SHA-256；不得移动现有 `v0.2.0`。
5. 建议为 CC BY 4.0 数据/派生资产增加独立、明确的许可证/NOTICE 和逐目录适用范围，避免根 MIT 许可证与 README 数据许可证之间产生歧义。
6. 从匿名全新克隆按 README 运行测试和复算，核对与本地最终投稿 ZIP 一致后，再把稿件中“必须同步”改为已完成事实。

## 4. 最小发布门槛

两仓库均应在投稿前满足以下同一闭环：

1. **内容冻结：**先冻结投稿 ZIP 和 public-safe 仓库 allowlist，生成 SHA-256 manifest。
2. **远端同步：**只提交 allowlist 文件；不上传密钥、受限原文、第三方数据库、事故输出或不可授权 traces。
3. **不可变引用：**新 tag 指向唯一 commit；Release 记录 commit、稿件 PDF/TeX、清单及关键代码的 SHA-256。
4. **fresh-clone 复验：**在无工作区隐式依赖的全新目录运行测试、分析和图表生成；记录操作系统、Python/SQLite 版本、命令、退出码和产物哈希。
5. **权利核对：**代码、作者生成元数据、第三方数据、派生文本、模型输出分别给出适用许可证或限制；README、Data Availability 和 Release notes 必须一致。
6. **稿件更新：**只有上述检查通过后，才可把两篇论文的 Data Availability 改为“该 tag/Release 精确对应本稿”；建议引用具体 tag/DOI，而不是仅引用可变的仓库首页或 `main`。

## 5. 审计证据端点

本次使用的公开只读端点包括：

- `https://api.github.com/repos/gaoxingkele/c2ges`
- `https://api.github.com/repos/gaoxingkele/c2ges/commits/main`
- `https://api.github.com/repos/gaoxingkele/c2ges/git/trees/217283f1586e3ec5618af3f87d4b8e7675408c97?recursive=1`
- `https://api.github.com/repos/gaoxingkele/c2ges/tags?per_page=100`
- `https://api.github.com/repos/gaoxingkele/c2ges/releases?per_page=100`
- `https://api.github.com/repos/gaoxingkele/ma-sqlgrid`
- `https://api.github.com/repos/gaoxingkele/ma-sqlgrid/commits/main`
- `https://api.github.com/repos/gaoxingkele/ma-sqlgrid/git/trees/6e6f32d45b9c57c1238aff51a4d4eb5587f327b0?recursive=1`
- `https://api.github.com/repos/gaoxingkele/ma-sqlgrid/tags?per_page=100`
- `https://api.github.com/repos/gaoxingkele/ma-sqlgrid/releases?per_page=100`

匿名查询全部成功，无需认证。该事实只证明本次核验时的公开可读性，不证明未来可用性、归档持久性或与本地候选包的等同性。
