# paperreview.ai（Stanford Agentic Reviewer）投稿记录

## 提交信息

| 项 | 内容 |
|---|---|
| 系统 | https://paperreview.ai/ — "Stanford Agentic Reviewer - Submit Paper"（页面自述 By Stanford ML Group，免费） |
| 提交时间 | 2026-09-25（本机时间） |
| 上传文件 | `01_Manuscript/LaTeX/paper_information.pdf`（C²GES Information 版，33 页，611{,}930 字节，SHA-256 前缀 `01e41bf2…`） |
| 对应 tex | `01_Manuscript/LaTeX/paper_information.tex`，SHA-256 前缀 `fefc2801…` |
| 提交邮箱 | `iamafan@126.com` |
| Target Venue | 留空（下拉列表只有 ICLR/NeurIPS/ICML/CVPR/AAAI/IJCAI/ACL/EMNLP/OSDI/SOSP/VLDB/SIGMOD/Other，没有 MDPI 期刊选项） |
| 结果 | 页面显示 **"✓ Submission Successful!"**，PDF 上传成功 |

## ⚠️ 必须保存的 Review Token

系统提示："We're experiencing delivery issues with certain email addresses. Please copy and save your token below - you may not receive an email notification."

```
Y1fgiQDAfNoMyfLfyNze3nBILeCuhZVc4qNKCHSxxGY
```

取回评审的方式：回到 https://paperreview.ai/review ，用该 token 查询（不依赖邮件）。

## 系统声明的限制（需记住）

1. **只分析前 15 页**（表单原文："Max 10MB • First 15 pages analyzed"）。本稿 33 页，因此评审覆盖的是摘要、引言、相关工作与方法前半部分；结果章（含新增的 L1–L6 证据层、外部前瞻评测、构念审计）与讨论、结论**不在分析范围内**。
2. 处理时间可能数小时甚至更久；**不要重复提交**。
3. 页面免责声明：评审由 AI 生成、可能有错，只作参考。

## 后续动作

- 收到或取回评审后，按项目惯例落盘到 `02_Revision_and_QA/04_Build_Reports/` 并在叙事复审记录里登记处置结论。
- 若关注后半部分（结果/讨论/结论），需另想办法：该系统固定只取前 15 页；可考虑改用只读长文评审渠道，或把结果章要点压成一份 ≤15 页的评审稿单独提交（但那会偏离正式投稿版，需明确标注）。

---

## 取回记录（2026-09-26）

两份评审均已取回（`GET /api/review/{token}`，页面同源 API）：

- **评审 1**（33 页投稿版，token `Y1fgiQDA…`）：评审完成 2026-09-25T10:40Z。**重要更正：该提交实际获得了全文覆盖**——评审引用了 ~6% recall、19 报告外部语料等仅 §4.11/Table S10 区域（p17+）出现的内容，"只分析前 15 页"的限制未生效。原文落盘 `02_Revision_and_QA/04_Build_Reports/C2GES_PAPERREVIEW_AI_REVIEW1_RAW_20260926.md/.json`，处置与双评审对照见 `C2GES_PAPERREVIEW_AI_REVIEW1_DISPOSITION_20260926.md`。二元评分：Claims 0 / Soundness 0 / Clarity 0 / Prior +1 / Importance +1 / Originality +1 / Value +1。
- **评审 2**（15 页 A3 副本，token `sjA3oxGS…`）：评审完成 2026-09-25T10:41Z。原文落盘 `C2GES_PAPERREVIEW_AI_REVIEW2_RAW_20260926.md/.json`，处置见 `C2GES_PAPERREVIEW_AI_DISPOSITION_20260925.md`。二元评分：Claims +1 / Soundness 0 / Clarity 0 / Prior +1 / Importance 0 / Originality 0 / Value 0。

解读注意（维持原判）：评审 2 的副本省略参考文献页，其"相关工作缺失/图表未展示"类意见多数因此产生，核验详见处置报告第一节。

---

## 第二次提交（2026-09-25，15 页压缩评审副本）

为让系统看到**全文科学内容**（第一次提交只覆盖前 15 页，即摘要→方法前半），另建了一份压缩评审副本再提交。

### 压缩方式（不改动投稿版）

- 工具：`06_External_Review/build_review_copy_15p.py`（PyMuPDF）
- 版面：**A3 横向（1191×842 pt）每张平铺 2 个原始 A4 页**。A3 横向恰好等于两张 A4 竖排并放，所以**文本 1:1 原尺寸、不缩小**，只有左右分栏
- 覆盖：原始 **p1–p30**（标题→摘要→引言→相关工作→方法→结果（含 L1–L6 证据层、外部前瞻评测、构念审计）→讨论→Limitations→Future Validation→**结论**）
- 页数：30/2 = **15 页**（正好等于该站分析窗口）
- 省略：p31–33 的声明段、缩写表与参考文献（仅此副本省略；**投稿版 PDF 未改动**，仍是 33 页 `01e41bf2…`）
- 校验：文本层完整（探针命中 "the only corrected internal win"、"External Prospective Evaluation"、"0.022940"、"Adjacent-Corpus Construct Audit"）；文件 0.50 MB，文件名 `C2GES_reviewcopy_15p_A3.pdf`

### 提交信息

| 项 | 内容 |
|---|---|
| 上传文件 | `06_External_Review/C2GES_reviewcopy_15p_A3.pdf`（15 页，A3 横向） |
| 邮箱 | `iamafan@126.com` |
| 结果 | **"✓ Submission Successful!"** |
| **Review Token** | **`sjA3oxGSe0bRDX3iam9A5ab4pqL7YlynFmNWozfo3FM`** |

取回：https://paperreview.ai/review + 该 token。

### 两次提交的用途区分

| 提交 | 上传件 | 覆盖范围 | Token | 用途 |
|---|---|---|---|---|
| 第 1 次 | 投稿版 33 页 PDF | 前 15 页（摘要→方法前半） | `Y1fgiQDAfNoMyfLfyNze3nBILeCuhZVc4qNKCHSxxGY` | 看"编辑初审视角"（标题/摘要/引言/方法是否立得住） |
| 第 2 次 | 15 页 A3 评审副本 | **全文正文（p1–30）** | `sjA3oxGSe0bRDX3iam9A5ab4pqL7YlynFmNWozfo3FM` | 看"全文视角"（含结果与讨论的叙事是否成立） |

### 已知风险（需在解读时注意）

- 该站解析器面对"两页并排"的版面时可能出现阅读顺序错乱或跨页错配；若第二份评审里出现"内容错位/图表编号混乱"之类意见，应先怀疑解析而非稿件。
- 副本省略了参考文献，评审若提"引用覆盖不足"，需按此解释。
