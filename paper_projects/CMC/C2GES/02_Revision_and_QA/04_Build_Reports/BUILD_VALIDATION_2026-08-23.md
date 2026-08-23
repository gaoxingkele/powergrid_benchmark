# C2GES 构建验证记录

## 正文

- 源文件：`../../01_Manuscript/LaTeX/paper_applsci.tex`
- 构建链：`pdflatex -> bibtex -> pdflatex -> pdflatex`
- 退出状态：四步均为 0
- 输出：`../../01_Manuscript/PDF/C2GES_Applied_Sciences_2026-08-23.pdf`
- 页数与纸型：20 页，A4
- 文件大小：512,863 bytes
- SHA-256：`812B7B66D258EDF74539D0B62C01B61C03252DAED95E6DF5B766723C829DE598`
- LaTeX error：0
- undefined citation/reference：0
- overfull box：0
- underfull box：38（非阻塞排版警告，终稿视觉 QA 时复查）

## 补充材料

- 源文件：`../../01_Manuscript/Supplementary/supplementary_materials.tex`
- 构建链：两次 `pdflatex`
- 输出：`../../01_Manuscript/PDF/C2GES_Supplementary_2026-08-23.pdf`
- 页数与纸型：2 页，A4
- 文件大小：124,098 bytes
- SHA-256：`3E6AE6DB47DD858F9B73F3770603221D3418F4AE2E851017F698CE7CAFAA9751`
- LaTeX error、undefined citation/reference、overfull box：均为 0

## 说明

MiKTeX 输出了“尚未检查更新”的环境提示，不影响退出码和 PDF 生成。旧论文输出已移出活动目录并集中标为 `.pdf.obsolete`。完整日志保存在本目录。
