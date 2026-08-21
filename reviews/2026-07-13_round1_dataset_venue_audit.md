# Round 1 — 数据集 × 快刊适配审计

- **日期**: 2026-07-13
- **评审类型**: 数据集 × venue 适配审计(离线,基于 Paper_CCF skill 画像 + 项目 ARA 证据)
- **评审范围**: `data/public_datasets/` 已缓存 24 个数据集 + 6 个 mintou 在研项目
- **评估视角**: Paper_CCF(155 会议 + 15 期刊画像)× paper_reviews(7 维 rubric + 目标刊 distilled standards)× ARA(四层结构 + 证据链完整性)
- **目标**: 找出**最快发表路径**(以 fast-OA 优先,允许算法/数据集/下游任务改动)
- **产出**: 优先级排序 + 每项目具体行动清单 + 未被利用的高潜数据集清单
- **下一轮(Round 2)**: 对 6 个 mintou 项目做完整 paper_reviews 7 维评审,允许大幅修改算法/数据集/下游任务以换取快速投稿

---

## 1. 总览

- **已缓存公共数据集**:24 个已下载 + 7 个 API-ready(共 31 个 manifest 条目)
- **在研项目**:6 个 mintou 系列(p1–p6),均已完成 ARA 工程 + JOURNAL_REVIEW 差距评估
- **已有 ARA artifacts**:2 个已编译(`2026_c2ges_engineeringletters`、`2026_ma_sqlgrid_cmc`)+ 6 个 mintou 系列
- **Paper_CCF 已覆盖 fast-OA 期刊**:PCMP(免费/~4周/IF 11.9)、CSEE JPES(Q1/~2–3 月)、OAJPE、MDPI Energies/Electronics/Applied Sciences/Sensors/Machines/Mathematics/Sustainability、Energy Reports、Frontiers in Energy Research、Scientific Reports、Heliyon、IEEE Access

---

## 2. 在研项目快刊适配排序(从近到远)

### 🥇 p2 HyG-LoadFormer(负荷预测)→ MDPI Electronics / Applied Sciences | 2–3 周

| 维度 | 当前状态 | 目标刊要求 | 判定 |
|---|---|---|---|
| 核心信号 | OPSD 24h/day-ahead MAPE 0.0397 vs 0.0563,rolling +39.16% | 远超 Electronics "增量即可" 底线 | ✅ |
| 方法类型 | 双曲图神经网络 + Transformer | Electronics 11/15 已发论文 = "ML-架构组合 + 场景载体" | ✅ |
| 实验底线 | 多版本 OPSD/SimBench + rolling | ≥1 case study + ≥1 comparison + 量化指标 | ✅ |
| 缺失项 | 无显著性检验/多 run/开源代码 | 0/15、1/14、0/15 已发论文均不做 | ⚠️ 不必补 |
| 边界 | 1h 短时预测为记录 limitation | 主张必须限定 day-ahead | 必须守 |

**行动**: ① 加 sensitivity analysis(Energies/AppliedSci "隐性必需项");② 润色;③ 投稿 MDPI Electronics(~15 天首决)。

### 🥈 p4 SHIELD-MOEA(韧性规划)→ MDPI Energies | 4–6 周

| 维度 | 当前状态 | 目标刊要求 | 判定 |
|---|---|---|---|
| 核心信号 | hypervolume +2.78% vs MOEA/D, +3.26% vs NoScenarioScreen | 接近 Energies "≤5% 诚实报告" 底线 | ⚠️ 中等 |
| 场景设计 | 场景筛选 + DER/负荷不确定性 | 偏好"场景/方案自比较 + 敏感性分析" | ✅ |
| 缺失项 | **无 AC/pandapower 潮流可行性验证**、无场景方差 | **Energies 硬底线(29/29 已发都做)** | 🔴 |

**行动**: ① 加 pandapower 可行性验证;② 加 ±20% 参数 sensitivity;③ 多 run。

### 🥉 p3 CARS-MODE(配网规划)→ MDPI Applied Sciences | 4–6 周

| 维度 | 当前状态 | 目标刊要求 | 判定 |
|---|---|---|---|
| 核心信号 | hypervolume 0.553,超 NSGA-II 0.46% | Applied Sciences 接受"应用价值逻辑替代基线优势"(7/11 已发用真实案例)| ⚠️ 可救 |
| 任务定位 | 配网扩展规划 + DER 选址定容 + 储能 | Civil/Electrical 分区对口 | ✅ |
| 缺失项 | 无真实 utility case、无 IRR/回收年限 | Applied Sciences 要求"量化经济效益" | 🔴 |

**行动**: ① 加真实案例或强 sensitivity;② 量化经济收益("30% 投资节省" 类表述);③ 命名受益者。

### 🏅 p6 BiLo-NSGA(预算约束项目评审)→ MDPI Applied Sciences | 3–4 周

| 维度 | 当前状态 | 目标刊要求 | 判定 |
|---|---|---|---|
| 核心信号 | +3.87% vs AHP-TOPSIS, +3.57% vs 消融 | 增益清晰 | ✅ |
| 差异化风险 | 与 p5(TRACE-MOEA)同源姊妹 | "not distinct" 高风险 | 🔴 |

**行动**: ① 加差异化论证;② 加真实案例经济量化;③ **与 p5 错开投稿**(先 p6 后 p5,间隔 ≥3 个月)。

### ⚠️ p5 TRACE-MOEA(项目评审)→ MDPI Applied Sciences / IEEE Access | p6 后 3 个月

- 信号弱于 p6(+1.23% vs AHP-TOPSIS、+3.71% vs 消融)
- 与 p6 同源姊妹,同时投稿会被交叉检索
- **建议**: 错开 3 个月投稿;或转 IEEE Access 声称为 soundness-based 框架验证

### 🔴 p1 DSTAR-GRU(调度推荐)→ 需重大改造,暂不宜投 | 8–12 周

| 维度 | 当前状态 | 判定 |
|---|---|---|
| 核心信号 | 综合得分增益 0.08%,噪声量级 | 🔴 |
| rolling 结果 | 3 窗口增益 0.07%,标准差 0.0548 比增益大两个数量级 | 🔴 |
| 唯一亮点 | 高新能源压力子集增益 0.72%(vs 消融 3.08%) | ⚠️ 可救 |
| 可行性验证 | 无 OPF/UC 可行性验证 | 🔴 任一快刊都过不去 |

**行动**: ① 重新定位到"压力子集";② 加 OPF/UC 验证;③ 多 run + 显著性;④ 重新实验。

---

## 3. 未被利用的高潜数据集(可起新文)

### 🥇 `sgcc_electricity_theft`(国家电网真实窃电检测,42,372 户 × 1,034 天)

- **独特性**:极高 —— 中国电网真实用户级窃电数据,全球稀缺
- **可投角度**:
  - MDPI Sensors(if 突出 AMI 智能电表/异常检测的"传感"角度,~18 天首决)
  - MDPI Electronics(AI/ML 异常检测,~15 天首决)
  - MDPI Applied Sciences(应用工程验证,~16 天首决)
  - IEEE Access(soundness-based,~4 周)
- **所需方法**:异常检测 + 类别不平衡处理 + 可解释性(SHAP/LIME)
- **预估工作量**:6–8 周

### 🥈 `sdwpf_kddcup2022`(龙源电力风电 SCADA,134 台风电 × 245 天 × 10 分钟)

- **独特性**:中高 —— 真实风电 SCADA,2022 KDD Cup
- **可投角度**:
  - MDPI Energies(风电预测/健康诊断,~17 天)
  - MDPI Machines(风机故障诊断/状态监测,~16 天,契合"具体机器/驱动/控制")
  - IEEE Access(soundness-based,~4 周)
- **所需方法**:时序预测 / 异常检测 / 功率曲线建模
- **预估工作量**:6–8 周

### 🥉 `lbnl_pmu_event_library`(LBNL PMU 事件库)

- **独特性**:高 —— PMU 真实事件数据,适合故障诊断/事件分类
- **可投角度**:
  - MDPI Sensors(PMU 传感 + 事件检测,~18 天)
  - MDPI Electronics(AI-for-PMU,~15 天)
  - **PCMP**(若聚焦保护/控制/故障,免费+最快+最高IF)
- **所需方法**:事件检测 / 分类 / 异常识别
- **预估工作量**:6–8 周

### 🏅 其他高潜

| 数据集 | 可投角度 | 推荐刊 |
|---|---|---|
| `opsd_time_series` + `ett` + `uci_household_power` + `monash_australian_demand` | 多数据集联合 day-ahead 负荷预测对比(p2 延伸或新文) | Electronics / Applied Sciences |
| `ausgrid_solar_home` + `nrel118` + `renewable_weather` | 分布式光伏 / 光储协同预测 / 可再生出力不确定性 | Energies / Electronics |
| `equipment_fault_pmu` + `dgann_duval` + `dgadb` | 变压器 / 设备 DGA 故障诊断 | Sensors / Machines / Energies |
| `grid2op_datasets` + `rl_control` | 基于 RL 的电网调度控制 | IEEE Access / Applied Sciences |
| `gridstage` + `c2ges_nerc_reports` | 电网韧性评估 / 风险建模 | Energies / Energy Reports |
| `pglib_opf` + `opf_benchmarks` | OPF 求解方法对比(纯优化,偏理论) | MDPI Mathematics(Q1,~17 天)—— 需 genuine 数学贡献 |

---

## 4. 三 skill 协同建议

### 4.1 ARA:锁定 evidence 链

- 对 **p2(最接近投稿)** 立即执行 `/ARA 编译` 到完整 ARA,锁定 evidence 链
- 对 **p4/p3** 同步编译,为 sensitivity + pandapower 验证提供稳定基线
- 在 CLAUDE.md 加 `## ARA: end-of-session research capture` 让后续每轮自动记录

### 4.2 paper_reviews:投稿前最后一道闸

- 对 p2/HyG-LoadFormer 跑 `py scripts/run_review.py <稿件> --venue mdpi_electronics --recommend -v`
  - → 7 维独立评审 + 对抗核验 + 校准后 RRI + 推荐刊
  - → 与 ARA JOURNAL_REVIEW.md 交叉验证
- 等 Cloubic 端点通后,把 **p2 的真实稿件** 跑一遍,作为"真实 LLM 跑测"的第一个案例

### 4.3 Paper_CCF:选刊"最后一公里"

- 对每个项目,用 `/Paper_CCF` 问"这个主题投 PCMP 还是 CSEE JPES 还是 MDPI Energies"
- 对 **p4(SHIELD-MOEA,韧性规划)** 特别评估:若角度能拉到"保护/控制/故障"→ **PCMP(免费/~4周/IF 11.9 Q1)** 是最佳选刊;若仍是"规划优化" → **Energies**(当前目标)

---

## 5. 优先级行动清单

| 优先级 | 行动 | 耗时 | 预期产出 |
|---|---|---|---|
| **P0** | 跑 **p2 → MDPI Electronics**(加 sensitivity,润色,投) | 2–3 周 | 1 篇快发 OA(IF 2.9 Q2) |
| **P1** | 跑 **p4 → MDPI Energies**(加 pandapower + sensitivity) | 4–6 周 | 1 篇 IF 4.0 Q2 |
| **P1** | 跑 **p3 → MDPI Applied Sciences**(加经济量化) | 4–6 周 | 1 篇 IF 2.9 Q2 |
| **P2** | **错开 p6/p5**(先 p6 投 Applied Sciences,3 个月后投 p5) | 7–8 周 | 避免"not distinct"拒稿 |
| **P2** | 用 **sgcc_electricity_theft** 起新文(Sensors/Electronics/AppliedSci 任选) | 6–8 周 | 1 篇中国电网真实数据文 |
| **P3** | 用 **sdwpf_kddcup2022** 起新文(Energies/Machines/IEEE Access) | 6–8 周 | 1 篇真实风电 SCADA 文 |
| **P3** | 用 **lbnl_pmu_event_library** 评估是否够 PCMP 角度 | 6–8 周 | 1 篇 PMU 事件文 |
| **P4** | **暂缓 p1**:重新定位到压力子集 + 加 OPF/UC 验证 | 8–12 周 | 1 篇改造文 |

---

## 6. 总览表

| 项目 | 数据集 | 首选刊 | 次选 | 预计投稿时间 |
|---|---|---|---|---|
| p2 HyG-LoadFormer | OPSD / SimBench | **MDPI Electronics**(~15天) | Applied Sciences | **2–3 周** |
| p4 SHIELD-MOEA | SimBench 韧性 v2 | **MDPI Energies**(~17天) | PCMP(如拉角度) | **4–6 周** |
| p3 CARS-MODE | SimBench DER/storage | **Applied Sciences**(~16天) | Energies | **4–6 周** |
| p6 BiLo-NSGA | 公共基准 | **Applied Sciences** | IEEE Access | **3–4 周**(错开 p5) |
| p5 TRACE-MOEA | 公共基准 | **Applied Sciences** | IEEE Access | **p6 后 3 个月** |
| p1 DSTAR-GRU | RTS-GMLC | **暂缓** | — | 8–12 周 |
| **新文机会** | sgcc_theft | Sensors / Electronics | Applied Sciences | 6–8 周 |
| **新文机会** | sdwpf_kddcup2022 | Energies / Machines | IEEE Access | 6–8 周 |
| **新文机会** | lbnl_pmu_event_lib | Sensors / Electronics | PCMP | 6–8 周 |

---

## 7. 诚实边界

- **p2** 的 1h 短时预测是记录在案的 limitation,主张必须严格限定 day-ahead
- **p5/p6** 同源姊妹工程,同时投稿会被交叉检索
- **p1** 增益处于噪声量级,需彻底改造
- **Cloubic LLM 端点仍超时**:本轮审计基于 Paper_CCF 的 distilled standards + ARA evidence,非实时 LLM 跑测;Round 2 用 paper_reviews 的 7 维 rubric 做离线结构化评审
- 所有数据集/期刊指标均为 2026-07 快照,投稿前需在官网复核

---

## 8. 下一轮(Round 2)计划

对 6 个 mintou 项目执行完整 paper_reviews 7 维评审(离线结构化,模拟 LLM pipeline):
- novelty / soundness / experiments / reproducibility / related_work / clarity / ethics
- 每个维度按 paper_reviews 的 severity(0-4)× confidence(0-1)× fixability(0-1)打分
- 应用目标刊的 distilled review standards 作为校准锚点
- 允许大幅修改算法/数据集/下游任务以换取快速投稿(优先级 = 快发,不追求原创高度)
- 产出:每项目 1 份结构化评审 + 可操作修改清单
