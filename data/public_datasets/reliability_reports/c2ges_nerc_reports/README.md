# C2GES NERC Reliability Reports

本目录缓存 C2GES 论文中 40-document benchmark 对应的公开 NERC 原始报告 PDF。

## What Is Cached

- `raw_pdfs/`: 40 个官方 NERC PDF。
- `metadata/c2ges_nerc_report_manifest.csv`: C2GES `doc_id` 到官方 PDF URL 的映射。
- `metadata/c2ges_nerc_report_manifest.json`: 同一映射的 JSON 版本。
- `metadata/nerc_pdf_index.json`: 从 NERC 页面抽取的 PDF 索引。
- `metadata/c2ges_doc_id_candidates.json`: 初始模糊匹配候选记录。
- `metadata/*.html`: NERC 页面缓存。

## Important Limitation

这里缓存的是公开 NERC 原始报告，不是完整 C2GES agent-verified candidate benchmark。

C2GES 论文中的实验数据还需要：

- sentence-segmented `nerc_*.json`
- five causal-role questions per document
- evidence sentence ID labels
- `manifest.json`

这些文件在上传的 C2GES 工程中应位于 `verification_pilot/agent_audit_40doc/`，但当前上传包未包含该目录。因此本目录可以支撑重新构建/再标注 C2GES 数据集，但不能直接替代缺失标签集。

## Refresh

```powershell
python scripts/data_acquisition/download_c2ges_nerc_reports.py
```
