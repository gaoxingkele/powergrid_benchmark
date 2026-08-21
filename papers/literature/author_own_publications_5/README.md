# 作者本人已发表电网论文（5 篇）：下载、蒸馏与期刊 skill 注册

建立日期：2026-08-09。用途：从作者本人 5 篇已发表论文蒸馏期刊录用画像，
注册到多智能体审稿系统（`D:/aicoding/paper_reviews/config/journals/`）。

## 1. 论文元数据与下载状态

| # | 期刊 | 论文 | DOI | 收录/分区（作者提供，核对 2026-08-04） | 下载状态 |
|---|------|------|-----|------|----------|
| 1 | Scientific Reports (Nature Portfolio) | 2025, 15:19440, RPA+GWO 微电网需求侧鲁棒优化 | 10.1038/s41598-025-03728-8 | SCIE；JCR Q1；中科院综合 3 区 | ✅ `pdf/sci_rep_2025_19440.pdf`（15 页，2.2MB，nature.com 直下） |
| 2 | Atmosphere (MDPI) | 2024, 15(12):1429, RPA 智能电网减排优化 | 10.3390/atmos15121429 | SCIE；JCR Q3；中科院地学/环境 4 区 | ✅ `pdf/atmosphere_2024_1429.pdf`（24 页，2.9MB，www.mdpi.com 403，改走 mdpi-res.com v2 成功） |
| 3 | Journal of Energy Storage (Elsevier) | 2025, 128:117213, 多微电网共享储能协同调度与收益分配 | 10.1016/j.est.2025.117213 | SCIE；JCR Q1；中科院工程技术 2 区/能源燃料 3 区 | ❌ 非 OA（Unpaywall is_oa=false）+ ScienceDirect 403 反爬（PII S2352152X25019267） |
| 4 | Unconventional Resources (KeAi/Elsevier) | 2026, 13:100405, 碳捕集+P2G 多微电网热-经济分层优化 | 10.1016/j.uncres.2026.100405 | ESCI；JCR Energy&Fuels Q3 / Geosciences Q1；中科院地学 4 区 | ❌ diamond OA 但全文仅在 ScienceDirect（PII S2666519026001020），403；Unpaywall/OpenAlex/S2 无镜像 |
| 5 | Discover Computing (Springer Nature) | 2026, 29:173, 多任务学习 KG 补全电网故障管理 | 10.1007/s10791-026-10043-x | SCIE；JCR Q3 | ✅ `pdf/discover_computing_2026_173.pdf`（19 页，1.8MB，link.springer.com 直下） |

Elsevier 阻断细节：ScienceDirect 对本环境全部请求（curl 直连/代理 127.0.0.1:17890/
cookie 会话/aria2c/jina reader）均返回 403 Cloudflare 挑战页（"Just a moment..."）。
未使用 sci-hub。两篇缺失论文的期刊画像已按"无本地语料"标注建立，待机构访问或
作者提供稿件后补库重写。

分区数据随年度变动，以最新 JCR/中科院分区表为准。

## 2. 蒸馏产物（本目录）

- `analysis/per_paper_stats.json` — 逐篇结构统计（页数/摘要词数/正文词数/节标题/
  公式/图表/参考文献/基线/消融/敏感性/统计检验/声明），含 2 篇失败原因记录
- `analysis/DISTILLATION_REPORT.md` — 中文蒸馏报告：每篇骨架节序、证据链特征、
  期刊格式特征（栏数/摘要结构/声明段落）、跨论文作者风格画像
- `analysis/extract_stats.py` — 自动统计脚本（pymupdf）
- `analysis/fulltext/*.txt` — 3 篇成功论文的全文纯文本缓存
- `analysis/auto_stats_raw.json` — 脚本原始输出（含节标题候选，供复核）

关键数字：Sci Rep 15 页/37 式/7 图 7 表/38 参/3 基线（GA,PSO,AHP）/4 Case；
Atmosphere 24 页/15 式/15 图 3 表/39 参/3 场景对比/独立敏感性分析；
Discover Computing 19 页/10 式/3 图 4 表/45 参/3 数据集/1 基线（LMKE-TransE）/3 变体消融。

## 3. 期刊 skill 注册位置（`D:/aicoding/paper_reviews/config/journals/`，10 个新文件）

| 期刊 | YAML 画像 | 录用论文画像 |
|------|-----------|--------------|
| Scientific Reports | `scientific_reports.yaml`（strong） | `scientific_reports_accepted_profile.md`（有语料） |
| Atmosphere (MDPI) | `mdpi_atmosphere.yaml`（standard） | `mdpi_atmosphere_accepted_profile.md`（有语料） |
| J. Energy Storage | `elsevier_j_energy_storage.yaml`（strong） | `elsevier_j_energy_storage_accepted_profile.md`（⚠ 无本地语料） |
| Unconventional Resources | `keai_unconventional_resources.yaml`（regional） | `keai_unconventional_resources_accepted_profile.md`（⚠ 无本地语料） |
| Discover Computing | `springer_discover_computing.yaml`（standard） | `springer_discover_computing_accepted_profile.md`（有语料） |

注册机制：`src/paper_reviews/config.py` 的 `load_journal(venue)` 按文件 stem 直接加载
`config/journals/<venue>.yaml`（curated yaml 优先于目录合成回退），无需登记索引。
已用真实管线逐一验证 5 份画像可加载（venue/level/threshold/7 维均正确解析）。
