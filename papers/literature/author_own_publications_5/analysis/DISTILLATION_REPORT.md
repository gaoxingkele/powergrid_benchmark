# 作者本人 5 篇已发表电网论文：结构蒸馏报告

蒸馏日期：2026-08-09。自动统计脚本：`analysis/extract_stats.py`（pymupdf 6.x），
逐篇数据见 `analysis/per_paper_stats.json`，全文纯文本缓存见 `analysis/fulltext/`。

**语料可得性**：5 篇中成功下载并解析 3 篇（Scientific Reports、Atmosphere、Discover Computing）。
Journal of Energy Storage（非 OA + ScienceDirect 403 反爬）与 Unconventional Resources
（diamond OA 但全文仅在 ScienceDirect，同样 403；Unpaywall/OpenAlex/S2 均无仓储镜像）未获全文，
本报告不含其统计数据，对应期刊画像仅依据官方规范与作者提供元数据。

---

## 1. Scientific Reports 2025, 15:19440（DOI 10.1038/s41598-025-03728-8）

**主题**：RPA + 灰狼优化（GWO）的微电网需求侧鲁棒调度。

### 骨架节序（一级节不编号，Nature 风格）
1. Introduction（无标题，正文直接开始，末段点明贡献）
2. System description（风机/光伏/柴油/储能/负荷逐个子模型，公式密集）
3. Proposed method（Problem formulation + RPA-GWO 算法流程，含 6 步编号算法框）
4. System validation（Cases：Case 1–4 优先级场景；System optimization）
5. Conclusion（bullet 式量化结论）
6. Data availability

### 量级与证据链
- 15 页，摘要 210 词（单段非结构化），正文约 6.4k 词
- 编号公式 37 个（5 篇中最密）；Fig. 1–7；Table 1–7；参考文献 38 条
- 基线 3 个：GA / PSO / AHP，对比维度含成本、排放、可靠性、计算耗时（50.5s vs 100.2s 等）
- 算例：单一微电网仿真系统，4 个 Case = AHP 赋权的不同利益方优先级场景（场景对比代替敏感性分析）
- 无消融、无统计检验

### 格式特征
单栏；摘要单段；声明仅 Data availability（"available from corresponding author on reasonable request"）+
Received/Accepted 日期（审稿周期约 4 个月：2025-01-29 → 2025-05-22）；参考文献 Nature 编号制（上标引用）。

---

## 2. Atmosphere 2024, 15(12):1429（DOI 10.3390/atmos15121429）

**主题**：RPA + 协调调度（SOP/DG/ES/SVG/CB）的智能配电网络减排优化。

### 骨架节序（MDPI 标准编号）
1. Introduction → 2. Related Work（2.1 RPA；2.2 Coordinated Dispatching Model）
→ 3. Proposed Model → 4. Result and Discussion（4.1 Simulation Parameters；
4.2 Evaluation of the Pre-Scheduled Dispatching Strategy；4.3 Sensitivity Analysis）→ 5. Conclusions

### 量级与证据链
- 24 页（5 篇中最长），摘要 210 词，正文约 10.3k 词
- 公式 15 个；Figure 1–15（图最多）；Table 1–3；参考文献 39 条
- 证据链：改进 IEEE 32/33 节点测试系统（**摘要/引言写 33-bus、4.1 节写 32-bus，文内不一致，
  是值得注意的审稿隐患**）；对比为 3 个运行场景（无 SOP / 仅 SOP / SOP+ES），非算法基线
- 有独立敏感性分析（补偿率 CR 0%→100% 扫描）+ 夏/冬季节对比
- 无消融、无统计检验；头牌结果"PV-based DG 利用率 +62%"

### 格式特征
MDPI 单栏；声明全套（Author Contributions / Funding / Data Availability Statement /
Conflicts of Interest，并披露国网福建雇佣关系）；参考文献 [n] 编号制。

---

## 3. Discover Computing 2026, 29:173（DOI 10.1007/s10791-026-10043-x）

**主题**：多任务学习知识图谱补全（BERT+TransE+Siamese，KGCM）用于电网故障处置。

### 骨架节序（Springer 编号）
1 Introduction → 2 Related works（3 小节）→ 3 Proposed model（4 小节）
→ 4 Experimental settings and analysis（8 小节：数据集/KG 构建/指标/参数/对比/消融/效率/参数）
→ 5 Experimental details → 6 Conclusion → Declarations

### 量级与证据链
- 19 页，摘要 178 词，正文约 7.8k 词
- 公式约 10 个；Fig. 1–3；Table 1–4；参考文献 45 条（5 篇中最多）
- 数据集 3 个：WN18RR、UMLS（公开基准）+ 自建电网故障数据集（State Grid，2020-01~2023-12，
  1200 设备节点 / 8900 三元组 / 80-20 划分）——公开+私有双轨是规范的 KG 论文证据链
- 基线 1 个（LMKE-TransE）；有消融（Table 4：full / w/o Siamese / baseline 三变体）；
  有计算效率与增量更新分析
- 统计：Table 3 报 ±std，但正文自述"single runs without standard deviations"，存在表述矛盾

### 格式特征
Springer SN 单栏；OA（CC BY-NC-ND 4.0）；标准 Declarations 块
（Author contributions / Funding / Data availability / Competing interests）；参考文献编号制。

---

## 4–5. 未获全文的两篇（仅元数据）

- **Journal of Energy Storage 2025, 128:117213**（Elsevier，非 OA）：多微电网共享储能动态协同调度
  与自适应收益分配（源荷不确定性下）。JCR Q1。按 JEST 惯例：双栏、结构化声明
  （CRediT + Declaration of competing interest + Data availability）、实验权重高。
- **Unconventional Resources 2026, 13:100405**（KeAi/Elsevier，OA）：碳捕集 + P2G 多微电网
  热-经济分层目标优化。ESCI。KeAi 采用 Elsevier 双栏模板、OA 许可。

两篇的具体骨架与统计待日后补库（机构访问或作者提供稿件）。

---

## 跨论文共性（作者风格画像，供期刊 skill 参考）

1. **方法命名套路**：RPA/AI 技术 × 电网场景的组合式创新（RPA-GWO、RPA-IDN、KGCM）。
2. **证据链以"场景对比 + 少量基线"为主**：基线 1–3 个；偏好场景/Case 设计与敏感性扫描，而非大规模基线横评。
3. **公式密度随期刊工程属性上升**：Sci Rep 37 式 ≫ Atmosphere 15 式 > Discover 10 式（CS 刊反而最少）。
4. **弱项（投稿风险点）**：均无严格统计检验；Discover Computing 出现 std 表述矛盾；Atmosphere 出现
   32/33-bus 不一致；Sci Rep 数据"应要求提供"在 Nature 系数据政策下属勉强达标。
5. **声明段落随出版社模板走**：Nature/Springer/MDPI 三家模板差异显著，投稿时直接套对应模板即可。
