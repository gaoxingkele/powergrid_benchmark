# CMC 两篇论文工作区

`CMC` 是历史别名。两篇论文当前目标期刊均为 MDPI *Applied Sciences*，当前正文基准统一为 2026-08-23 收到的 LaTeX，不再以旧 Word、旧 PDF 或 2026-08-05 源文件判断版本。

## 当前稿入口

| 论文 | 唯一正文源 | 当前编译 PDF | 修订计划 |
|---|---|---|---|
| C2GES | `C2GES/01_Manuscript/LaTeX/paper_applsci.tex` | `C2GES/01_Manuscript/PDF/C2GES_Applied_Sciences_2026-08-23.pdf` | `C2GES/02_Revision_and_QA/02_Working_Plan/DETAILED_REVISION_PLAN_2026-08-23.md` |
| MA-SQLGrid | `MA-SQLGrid/01_Manuscript/LaTeX/paper_applsci.tex` | `MA-SQLGrid/01_Manuscript/PDF/MA-SQLGrid_Applied_Sciences_2026-08-23.pdf` | `MA-SQLGrid/02_Revision_and_QA/02_Working_Plan/DETAILED_REVISION_PLAN_2026-08-23.md` |

## 两篇论文的统一结构

1. `00_Status_and_Index/`：基准版本、哈希、投稿状态和硬阻塞项。
2. `01_Manuscript/LaTeX/`：唯一活动正文源及编译所需模板、参考文献和图。
3. `01_Manuscript/PDF/`：仅存由活动 LaTeX 新编译的论文输出 PDF。
4. `01_Manuscript/Supplementary/`：补充材料源文件或投稿补充文档。
5. `02_Revision_and_QA/`：0823 修改意见、执行计划、包内 QA 和本次构建日志。
6. `03_Reproducibility/`：代码、数据、图源及原发布包元数据。
7. `90_Archive/`：原始 0823 ZIP、0823 前的工作区和历史 Word；不得从这里选投稿稿件。

## 版本规则

- 只修改 `01_Manuscript/LaTeX/paper_applsci.tex`；不要回写 `90_Archive/` 中的历史稿。
- 每轮正文、表格或图修改后重新编译 PDF，并在 `02_Revision_and_QA/04_Build_Reports/` 记录哈希和 QA。
- `03_Reproducibility/Package_Metadata/` 中的旧 manifest/hash 只代表收到的 0823 包；目录重组或正文修订后必须重新生成，不能直接作为最终发布证明。
- 标有 `.pdf.obsolete` 的文件是旧输出的可恢复归档，不是可打开的当前 PDF。
- 不得编造引用、实验结果、作者信息或权利状态；证据不足处标为“待核实”。

## 构建方式

在每篇论文的 `01_Manuscript/LaTeX/` 中运行：

```text
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
bibtex paper_applsci
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
```

本目录于 2026-08-23 完成统一整理。历史说明保存在 `90_Workspace_History/`。
