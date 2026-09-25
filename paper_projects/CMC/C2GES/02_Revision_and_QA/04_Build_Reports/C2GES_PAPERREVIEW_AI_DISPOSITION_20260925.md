# C²GES 对 paperreview.ai 评审的处置记录（2026-09-25）

评审来源：paperreview.ai（Stanford Agentic Reviewer），提交件为 15 页 A3 并排评审副本（覆盖正文 p1–30，省略参考文献页），Token `sjA3oxGSe0bRDX3iam9A5ab4pqL7YlynFmNWozfo3FM`。提交与副本说明见 `../../PAPERREVIEW_AI_SUBMISSION_20260925.md`。

处置对象版本（2026-09-26 探索性补充轮之后；09-25 修订轮的哈希见 `../../00_Status_and_Index/CURRENT_BASELINE.md` 历史节）：

- 正文 `01_Manuscript/LaTeX/paper_information.tex` SHA-256 `dd70896031989ae889b82444c906562751a4a5c590d8bc1a3aad7cfd36e8198e`
- PDF `19e9c1477fcb823b2f82aa83f0de396b67f1467fa38289e2ad5d0a5f865af92f`，34 页，6 图 15 表 46 参考文献，摘要 200 词；补充 PDF 7 页，Table S1–S13
- 公共验证 route `diagnostic` PASS，0 failures；发布清单 580 文件 PASS

处置分级：**FIXED**（本轮改稿）/ **ALREADY**（稿内已有，评审未看到）/ **FUTURE**（属 E1–E5 确认性路线，不动当前诊断边界）/ **DECLINED**（含理由）。

## 一、评审事实准确性核验

| 评审陈述 | 核验 |
|---|---|
| §3.9 有重复句 | **属实**。tex 246/247 行两个改写版本同段并存，PDF p11 可复现 |
| 角色线索 recall ≈6% | 属实（0.064/0.060，§4.11 + Table S9），稿内已透明报告 |
| 12 位窗口 / 边方向可逆时序 / 平局弃权 / 词重叠边权 | 属实，且 §3.4 全部明确列为 known blind spots |
| 基线调参不对称 | 属实，§3.10 有专表（tuning-opportunity）声明，RQ1 已限 descriptive |
| "only familywise-corrected system contrast" | **丢了限定**：仅外部语料内成立；历史 K=5 层 Full 对 Semantic-MMR/TextRank 亦有 Holm 胜出（0.0117） |
| "Some figures/tables are described textually rather than shown" | **不成立**：6 图 15 表全部落在 p4–29，评审副本覆盖完整；副本省略参考文献页是评审无法核对引用的根因 |
| Bi-GAE / GraphLSS / AREDSUM-CTX "缺失" | **不成立**：三者均已引用（§2.1×2、§2.2×2），GraphLSS 与 StrucSum 的对齐讨论稿内已有 |
| Sem-nCG (arXiv 2310.03414) | **编号错误**：该号为 Kurisinkel & Chen 的 LLM 多文档摘要；正确条目 Akter & Karmaker, KONVENS 2024, 2024.konvens-main.21 |
| "min–max 缩放导致对特定报告分布过拟合" | 措辞不准：选择逐报告进行，跨报告分数可比性不影响选择；真实问题是通道内极值压缩（§5.2 已讨论 scale coupling） |

## 二、弱点（Weaknesses）处置

| # | 评审点 | 处置 |
|---|---|---|
| W1 | 词汇线索边 / 逆时序 / 12 位窗口 | ALREADY（§3.4 声明）+ FUTURE（§5.6：窗口与时序规则若修订须在 E1 开结果前冻结） |
| W2 | 路径项加性竞争、缩放掩盖 | ALREADY（§5.2；RP 2×2 析因正是为此；Figure S4） |
| W3 | 角色线索 recall ≈6% | ALREADY（§4.11 透明报告）+ FUTURE（§5.6 已写弱监督角色标签为 E2 条件备选） |
| W4 | 无人工评估 | ALREADY（§3.9 冻结协议 + 伦理声明 + Table 15 e2-gate）；评审建议即 E2/E4 |
| W5 | 历史层调参不对称 | ALREADY（§3.10 专表）；对称调参已预选（§4.10：MMR 0.9、TextRank 0.65），属 E1 |
| W6 | 外部语料非严格未见 | ALREADY（稿内从未声称未见； qualifier 保留）；预注册未见实验 = E1 |
| W7 | §3.9 重复句 | **FIXED**（删除旧版；PDF p11 复查确认单份） |
| W8 | 图表"只描述不展示"、交叉引用多 | DECLINED（事实核验不成立，见上表；交叉引用多为诊断分层所需） |

## 三、十个 Q 处置

| Q | 内容 | 处置 |
|---|---|---|
| Q1 | 路径改选但变差的逐案例错误分类 | **FIXED-探索性**（2026-09-26）：Table S11 + `descriptive_addenda_v1/`；改动单元 92–98% 边相连、80–100% 触及逆时序边、窗口外阻断对数十至数百；描述性，无因果分摊 |
| Q2 | 24/48 窗口、硬时序约束消融 | ALREADY 一半：路径**长度** 3/4/5 已扫（相邻 Spearman 0.979–1.000，`dev_calibration/artifacts/`）；**窗口本身从未扫描**（`max_distance=12` 硬编码），§5.6 已承诺修订前先冻结 |
| Q3 | 词典扩展 / 否定检测 / 弱监督角色分类器 | ALREADY（§5.6 已列 E2 条件备选）；改动词典会脱离冻结系统，不属本轮 |
| Q4 | 冗余系数 −0.50 从未校准 | **FIXED-文本**：§2.1 新增 MemSum 对照并声明固定罚出于确定性/可审计；§5.6 E1 显式纳入"开发集选定冗余系数 + 对称调参预算"。网格扫描本身属 E1 |
| Q5 | 确定性 typed edges + R-GCN/GAT 混合 | FUTURE：GraphLSS 对比已在 §2.2；学习化混合属确认性路线 |
| Q6 | 逐角色覆盖/收益（如 mitigation 精确率） | **FIXED-探索性**（2026-09-26）：Table S12；句级 ROUGE-L 匹配几乎不触发（已在表注声明），改用 token 级对齐；参考侧角色稀疏（root cause 0/7）为结构性空缺 |
| Q7 | 完全冻结、系列不相交、对称调参、预选提交 | ALREADY：即 E1 定义；比较器参数已预选（§4.10） |
| Q8 | Sem-nCG / 实体事件覆盖 / NERC 属性清单 | **FIXED-文本**：§5.6 指标句加入 redundancy-aware Sem-nCG（**正确编号**，见引用核验）；NERC 属性清单留 E2/E4 |
| Q9 | 为何保留删除效用；两段式 tiebreaker | ALREADY 一半：§3.11 赢家诅咒解释 + freeze_rule；**FIXED-文本**：两段式（保留负责覆盖 + 路径仅作 tiebreaker）写入 §5.6 候选重设计 |
| Q10 | 分段审计长块分布 / 是否改变排序 | **FIXED-探索性**（2026-09-26）：Table S13；长块分布 + 非逐字实例已报；排序是否改变明确不答（审计未用于重跑，Limitations 边界保持） |

## 四、总体建议 (i)–(iv) 映射

(i) 未见系列不相交语料上执行 freeze-before-eval = **E1**；(ii) 专家评估 = **E2/E4**；(iii) 混合结构模型、时序与更长窗口 = **E1 冻结重设计项**（§5.6 已写）；(iv) 冗余/覆盖感知指标 = **E2 后描述性伴随**（§5.6 已写，本轮补 Sem-nCG）。评审的总体建议与论文自身路线图一一对应，无路线冲突。

## 五、引用核验（四项齐全才入库）

| 评审建议 | 结果 | 处置 |
|---|---|---|
| MemSum | 真实：Gu, Ash, Hahnloser，ACL 2022 Long，pp. 6507–6522，DOI 10.18653/v1/2022.acl-long.450 | **已入稿**（§2.1，`gu2022memsum`） |
| AREDSUM-CTX | 真实：Bi et al.，EACL 2021，2021.eacl-main.22 | 稿内已引（`bi2021aredsum`），无需动作 |
| GraphLSS | 真实：Bugueño et al.，NAACL 2025 Short，2025.naacl-short.67 | 稿内已引（`bugueno2025graphlss`），无需动作 |
| Bi-GAE | 真实 | 稿内已引（`mao2023bigae`），无需动作 |
| Sem-nCG 冗余版 | 论文真实但评审编号错误；正确：Akter & Karmaker，KONVENS 2024，pp. 182–195，2024.konvens-main.21 | **已入稿**（§5.6，`akter2024semncg`），未采用评审的错误 arXiv 号 |
| StrucSum | 稿内已引（`yuan2026strucsum`）且已作负结果对齐 | 无需动作 |

## 六、本轮自查新发现（评审未抓到）

1. 硬编码节号 3 处错指（§3.9 误作 §3.8 ×2；§4.8 误作 §4.3）+ 1 处歧指（§4.4）——N-1 重排残留，本轮全部改 `\ref`（新设 5 个 `\label`），并 grep 确认全文零残留；
2. §3.12/§4.10 跨节近似复述句（J=0.76）——§3.12 删结果句、只留设计描述；
3. 节号歧指（tex 原 `:603`）由执行者判定指向 §4.3（主 estimand）；若作者更属意 §4.5（RSI）或 §4.9（历史端点贡献），改 `\ref` 目标即可——**作者待决项**。

## 七、验证链（本轮全部重跑）

pdflatex×1 + bibtex + pdflatex×2：34 页，0 错误 / 0 Overfull / 0 未定义引用；摘要 200 词；公共验证 route diagnostic PASS 0 failures；展示审计 problems: none；投稿/评审/补充三包 fresh_extract PASS；发布清单 568 文件 PASS。

## 八、不影响的事项

- ~~第一次提交（33 页投稿版，Token `Y1fgiQDA…`，仅前 15 页视角）的评审~~ **已于 2026-09-26 取回**：实际覆盖全文（"前 15 页"限制未生效），处置与双评审对照见 `C2GES_PAPERREVIEW_AI_REVIEW1_DISPOSITION_20260926.md`。本报告 09-25 轮的 §2.1 修订（MemSum 两句）位于前 15 页区段内——原注记"未触及该区段"作废。
- paperreview.ai 已分析的副本是修订前版本；评审意见中"§3.9 重复"等已随本轮修复过期，不影响其其余意见的有效性。
