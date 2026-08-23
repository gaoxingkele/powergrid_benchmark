# C2GES 修订执行证据台账

更新日期：2026-08-23
基准提交：`840dcce5835423a5cdc3ee9f84eccfc601a6f4f6`
当前路线：范围收缩的技术报告代理稿；技术包 `PASS`，`submission_ready=false`。
状态只依据可复核制品；作者身份、权利、专家判断和新外部数据不由自动系统代填。

| ID | 状态 | 执行证据 | 尚未关闭的边界 |
|---|---|---|---|
| C-P0-01 | 已验证 | `03_Reproducibility/Data/formal_protocol/C2GES_REVISION_PROTOCOL_2026-08-23.md`；输入哈希、split、seed、cluster、终点和多重比较族已记录 | 未见外部系列仍须在冻结后才可揭盲 |
| C-P0-02 | 已验证 | Supplement 全部改为 `03_Reproducibility/Data/` 实际路径；2 页无 overfull/未定义引用编译通过 | 无 |
| C-P0-03 | 已验证 | rights-safe CSV/JSON 恰好 40 行、27 included、15 test、10 series；公开验证器核对 | 无 |
| C-P0-04 | 已验证 | Python 3.12 环境锁、requirements、单入口；49 tests 通过，3 个受限输入明确 skip；主文/补充均干净编译 | 受限原始 PDF/逐句文本不公开 |
| C-P0-05 | 已验证 | 当前布局 Package_Metadata manifest/checksum 已重建；独立 `--check` 要求零 missing、unlisted 和 mismatch | 修改任何 release 文件后必须重新冻结 |
| C-P0-06 | 待作者输入 | `AUTHOR_AND_EXTERNAL_GATES_2026-08-23.md` | 邮箱、姓名、贡献、基金、利益冲突、AI 声明、仓库 release 需作者书面批准 |
| C-P0-07 | 已验证 | `C2GES_CLAIM_EVIDENCE_AUDIT_2026-08-23.md`；未保留无条件 superiority/effectiveness/causality/reproducibility 升级 | 作者终稿仍需逐字批准 |
| C-P1-01 | 已验证（诊断范围） | 27 报告布局块审计：14,290 单元、505 表格、0 检测失败；>100 词从 214 降至 39 | 未将启发式块规则提升为新主实验；人工单元有效率待外部标注 |
| C-P1-02 | 已验证（事后敏感性） | 冻结 top-10 下 110/260 词帽，210 行、六个系列对比；全部区间跨 0、无 Holm 支持 | 不是前瞻性全候选匹配预算主实验；正文已降级主张 |
| C-P1-03 | 已验证（同语料诊断） | 模型 revision/tokenizer/256 上限、12,924 候选与截断率；512/chunk 排名敏感性四对比 | 未确定通用首选长文本表示 |
| C-P1-04 | 已验证（未来配置） | MMR、TextRank、normalized-path C2GES 各 9 个开发配置；`test_input_accessed=false`；选 0.9/0.65/0.0 | 仅授权未来外部系列，不能回写 retained test |
| C-P1-05 | 已验证（最小干净消融） | normalized no-path 保持剩余正向尺度；相对 strict 改变 1/3 个 K5/K10 选择；两系列区间跨 0 | 完整逐模块因子消融和人工结构指标仍未执行；路径项已从效果贡献降级 |
| C-P1-06 | 待外部研究 | 盲化/双标注要求保留于协议和门禁 | 缺合格标注者、原始判断、一致率和仲裁 |
| C-P1-07 | 已验证 | 10 系列 equal-weight cluster bootstrap、全部 1,024 次 sign flip、LOSO、Holm 六对比 | 仍是事后 retained-corpus 敏感性 |
| C-P1-08 | 待外部研究 | 外部系列配置和冻结边界已写明 | 缺合法未见系列和一次性评测 |
| C-P2-01 | 待外部研究 | 专家效用主张已从正文删除/限制 | 缺招募、同意、预设终点和结果 |
| C-P2-02 | 待外部研究 | 正文明确 NERC 技术报告是维护导向代理 | 缺许可维护工单/检查记录 |
| C-P2-03 | 已验证（自动层） | `C2GES_AUTOMATED_FAILURE_MODE_AUDIT_2026-08-23.md` 汇总布局、长度、截断、系列、路径尺度和调参失败模式 | 受限原文成功/失败语义样本需专家执行 |

## 最终技术验收

- 公共验证报告：`02_Revision_and_QA/04_Build_Reports/C2GES_PUBLIC_VERIFICATION.json`，技术状态 `PASS`。
- PDF：主文 22 页，补充 2 页；逐页渲染和 contact sheet 检查通过。
- 最终投稿阻塞项只保留在作者/权利/外部研究门禁中，未伪装成已完成证据。
