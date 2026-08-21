# 第二轮理论与创新复审（P1–P6）

**复审角色：** 理论基础、算法创新与期刊适配审稿人  
**日期：** 2026-08-12  
**范围：** 六篇当前 `MANUSCRIPT.md`；只读主稿。  
**复审目标：** 回归第一轮问题，并检查当前创新边界、理论动机、消融负结果、贡献充分性及期刊范围。`BLOCKER` 表示内部错误会直接破坏当前定量主张，提交前必须修正；`MAJOR` 表示核心仍可成立但需实质性重构；`MINOR` 表示无需改变核心证据即可修正。

## 1. 回归总表

| 论文 | 第一轮关键问题 | 当前状态 | 第二轮判定 |
|---|---|---|---|
| P1 DSTAR-GRU | 代理标签被读成实测弃电；确定性比较口径；跨系统全零 | 摘要已明确非实测记录，确定性基线单次描述，跨系统不再声称 transfer | **MAJOR** |
| P2 CSA-LoadNet | 10-seed 与早期 3-seed 基线混写；后验收窄 | 已明确 MLP 是正式十种子对照，其余四个仅 preliminary screen；后验改名已披露 | **MINOR** |
| P3 CARS-MODE | adaptation 无 HV 增益；AC 因果过度；Weighted Sum 伪重复 | 三项均已实质修正；适应性 AC 仅作 qualitative hypothesis | **MAJOR** |
| P4 SHIELD-MOEA | 场景调用量公式不闭合；动态重筛过度归因；确定性推断 | 分项计数已补，但旧公式仍矛盾；贡献列表仍保留旧“40/40”统计 | **BLOCKER** |
| P5 TRACE-MOEA | 确定性伪重复；zero metric cost；偏好层过度归因 | 已分离 12 个随机对照与 3 个确定性规则；archive 改为 metric-quarantined；组件效应降格 | **MINOR** |
| P6 BiLo-NSGA | 确定性伪重复；forward/substitution 过度归因 | 已分离推断族；标题、摘要、结论均限定 resolved forward cells；substitution 仅保留审计语义 | **MINOR** |

当前最优先事项不是新增图表或公式，而是清除 P4 的内部矛盾，并决定 P1、P3 是否接受“创新主要来自评估框架、组件负结果和边界识别”这一论文身份。

---

## 2. P1：Operating-State Retrieval / Curtailment-Risk Benchmark

### 判定：MAJOR

### 已解决

- Abstract 已写明 70% cap 生成的是 `curtailment-rate proxy`，且“not an observed dispatch-curtailment record”。
- III-D 已将 persistence、seasonal、ridge、raw kNN 作为单次确定性结果描述，不再伪造 seed-level 显著性。
- TCN/DLinear 和 paired sensitivity 的地位被区分为冻结分析与 post-freeze sensitivity。
- Discussion 已将检索在 onset 上失效的解释明确称为 mechanism hypotheses，而非因果证明。

### MAJOR 2.1：代理身份尚未贯穿贡献定义

**证据位置：** Abstract 与 Introduction Contribution 1。  
摘要已改为 proxy，但贡献 1 仍写“converts ... into a curtailment-rate target”，且标题仍使用未限定的 curtailment-risk benchmark。读者可能只读贡献列表并重新把它理解为真实调度标签。

**要求：** 贡献 1、III-A 首句、表题和结论统一使用 `reference-policy curtailment-risk proxy target`。标题可保留，但摘要/引言必须持续保留 operational proxy 限定。

### MAJOR 2.2：机制主张仍限定于单 cap、单年、单系统

**证据位置：** III-E、Figure 8、Limitations。  
NREL-118 冻结 cap 为全零，其他 cap 只做标签稀疏度而未复跑方法。由此，检索的 1 h/24 h 符号反转是有价值的实例级发现，但不是跨政策机制规律。

**可接受处理：** 不一定必须新增实验；可以把创新明确定位为“benchmark-enabled discovery on RTS-GMLC under one reference policy”。若继续使用 `scale-dependent utility`，应加 `in this benchmark`。

### MINOR

- III-D 的 27 tests 应在表注明确其九个 seeded opponents，便于读者复算检验族。
- paired sign-flip/paired bootstrap 是 post-freeze sensitivity，摘要不宜与 primary Mann–Whitney 并列成同等验证性结论。
- 不需要增加算法框图。若后续做新实验，优先做第二系统的非退化政策校准，而非增加模型结构。

### 创新与期刊适配

创新足够支撑 **benchmark/mechanism-audit article**，不足以支撑 forecasting-superiority article。IEEE Access 范围契合，前提是方法开放性和负结果是主要贡献。

---

## 3. P2：CSA-LoadNet

### 判定：MINOR

### 已解决

- Abstract/Contribution 1 已将正式正结论限定为十种子 MLP 与 no-aggregation 对照上的 OPSD-24 h。
- 其他 TCN、PatchTST-lite、DLinear、LSTM 已明确为 preliminary three-seed screen，不再与正式推断同级。
- `non-significant` 已改为 unresolved，而非 statistically equivalent。
- Discussion 明确 claim downgrade and renaming 是 v7 结果后的后验行为，未声称 preregistration。

### MAJOR

无新的提交级理论断点。

### MINOR 3.1：创新类型必须保持为组件审计

**证据位置：** Abstract、Introduction Contributions、VI-6.3、Conclusion。  
唯一稳定的正知识是“OPSD-24 h 上 aggregation existence 有效”；Poincaré/Euclidean/equal weighting 未分离，其他设置有负结果。因此创新不是新几何注意力机制，而是对 cross-series aggregation 的可分离实证审计。

**要求：** 保持当前标题和 CSA-LoadNet 名称可以，但 cover letter 不应使用 “novel hyperbolic attention architecture outperforms baselines”。建议使用：

> The contribution is a component-level audit that isolates when cross-series aggregation helps and when weighting geometry does not matter at the available precision.

### MINOR 3.2：理论动机与实验结果的反馈已经成立，但不可普遍化

Discussion 7.2 将 horizon asymmetry 解释为 shared daily/weekly structure，并明确是 interpretation。应继续保持，不要在结论中升级为证明。当前未使用 weather inputs、单一 temporal split，也使该解释仍是待检验假设。

### 图表/公式

现有层次矩阵、显著性图和 reconciliation 结果已足够。无需新增框图；最有价值的后续证据是 rolling-origin/weather-year replication。

### 期刊适配

Electronics 方向匹配。论文价值是可复现、诚实的模型组件评估；在这一定位下贡献充分且不过度。

---

## 4. P3：CARS-MODE

### 判定：MAJOR

### 已解决

- Weighted Sum 已明确 effective sample size=1，七个差异只作描述；正式 Holm family 只含十二个 stochastic opponents。
- Abstract/Contributions/Results 已明确 FixedDE pooled +0.60%、7/7 unresolved，adaptation 不是 proxy gain 的来源。
- AC 结果已改成 composition-level qualitative hypothesis，不再称自适应机制的真实因果功能。
- GDE3 与 NSDE 提供了直接 MO-DE controls，框架级比较价值明显增强。

### MAJOR 4.1：题名中心与已证实贡献仍存在张力

**证据位置：** Title、Contribution 1、VI-6.2、Conclusion。  
算法名与题名突出 Strategy-Adaptive，但唯一直接 adaptation ablation 在全部场景均未分离，且 FixedDE nominally higher。当前文本已诚实披露，这消除了过度主张，却没有消除论文身份问题：读者仍会问“为何以未产生可测代理收益的组件命名算法”。

**要求：** 两条路径任选其一：

1. 保留题名，但在引言贡献 1 后立即说明 strategy adaptation is an audited design feature, not the demonstrated source of gain；把标题下的 short title/cover letter 主身份写成 constrained MO-DE framework；或
2. 轻度调整副标题，突出 `Constraint-Aware Multi-Objective Differential Evolution`，将 strategy-adaptive 放到方法描述而非价值主张。

不建议为了让数据“好看”再做后验调参来制造 adaptation advantage。

### MAJOR 4.2：AC 层只能支持代理—物理不一致，不能救回适应性创新

**证据位置：** V-5.4、VI-6.3、Limitations 1。  
每方法仅选 seed-0 compromise plan，再压缩为 action composition 并确定性映射。0.611 对 0.569 可作为设计假设生成，不能证明 adaptation improves electrical behavior。当前正文大部分已正确降格，但 Figure 3 caption 仍写 “FixedDE ... loses AC feasibility”，语气强于方法证据。

**修改建议：** caption 改为 `has a lower descriptive AC-feasible rate under the fixed composition mapping`。

### MINOR

- “55 significant wins among 56 stochastic-baseline comparisons”包含多个较弱/不同范式 baseline；摘要应继续把最重要的 matched-repair NSGA-II、GDE3、NSDE 单独报告，而不是以总胜场替代创新证据。
- `robust proxy optimizer`仅能表示在测试场景和参数范围内稳定；当前最好使用 `competitive constrained proxy optimizer`。
- 现有 9 幅图充分。增强理论价值应来自多 seed/front-sampled AC，而非新框图。

### 期刊适配

Energies 主题契合。可发表贡献是 **constraint-aware MO-DE + direct DE controls + null adaptation audit + proxy/physics disagreement**，而不是新的自适应 DE 性能突破。

---

## 5. P4：SHIELD-MOEA

### 判定：BLOCKER

### 已解决

- IV-4.3 已分别定义 $N_p=40$、$N_u=80$、$N_r=8$，并将 12,800 active-union calls 与 5,120 full ranking calls 相加为 17,920；该分项计数本身闭合。
- Abstract/Discussion 已明确 no-screening、DE-only 和 fixed worst-K 是 unresolved，而非等效或被 full 击败。
- 确定性规则已从推断族中分离，Abstract/Conclusion 使用 32 stochastic comparisons + 16 descriptive deterministic gaps。
- worst-case HV 已明确是 per-objective sampled worst envelope，并承认 sample-dependent diagnostic，而非真正鲁棒性证书。

### BLOCKER 5.1：旧调用公式与新分项公式仍互相矛盾

**证据位置：** IV 正式定义、紧邻 Section 4.1 前；IV-4.3。  
旧句仍写：

> `N_p K G + N_p |S_search| N_screen` is an exact objective-call count.

但 IV-4.3 的正确实现定义是：

> `G N_u K + N_r N_p |S|`, with `N_u=2N_p`.

代入 $N_p=40$，旧式得到 11,520，而不是 17,920。两条公式不能同时为 exact。

**必须修改：** 删除旧式，或统一改为

$$
C_{\rm screened}=G N_uK+N_rN_p|\mathcal S|=12{,}800+5{,}120=17{,}920.
$$

提交前还应由代码计数器逐项核对这些 calls 是否互斥、是否包含缓存复用；正文当前已经声明其是 implementation counter，保持该限定即可。

### BLOCKER 5.2：贡献列表仍保留旧的 40/40 显著基线主张

**证据位置：** Introduction Contribution 3 对比 Abstract、Discussion、Conclusion。  
Contribution 3 仍写 `40 of 40 Holm-corrected baseline comparisons significant`；最新版其他位置已经修成“四个随机基线 × 八场景 = 32 个推断比较，另有两个确定性规则 × 八场景 = 16 个描述差异”。40 既不等于 32，也不等于 48，且把确定性规则重新混回推断印象。

**必须修改：** Contribution 3 与全文统一为：

> all 32 comparisons with four stochastic baselines are Holm-significant; sixteen gaps to two deterministic rules are descriptive.

随后全文搜索并清除 `40/40`、`five baselines` 与旧 family size。

### MAJOR 5.3：动态 screening 不是创新效果来源

当前已诚实写明 fixed generation-1 worst-K 与 periodic re-screening 8/8 unresolved。因而贡献应是 selective scenario exposure、audited call reduction 和 disjoint-draw scoring。`adaptive interface` 可以作为设计描述，但不能作为性能已证实机制。

### MAJOR 5.4：sampled worst-case HV 的解释仍有一句偏强

VI-6.2 的 “fronts ... are not specialized to benign scenarios; they degrade gracefully” 超过了证据。per-objective worst vector 可由不同场景坐标拼成，且只有 16 个 sampled scenarios。建议改为：

> The sampled worst-envelope diagnostic does not reveal an adverse reversal relative to the tested baselines; it does not certify tail robustness outside the sampled scenarios.

### MINOR

- “direct-reuse-leakage-controlled”比 “leakage-proof”更准确，应统一采用前者。
- AC NoOutage 差异继续保持 composition-level descriptive，不要对 108 个共享方案/网络 cases 进行独立样本推断。
- 图表数量充分。修复公式和统计计数比增加任何图更优先。

### 期刊适配

Energies 高度匹配；修复两个 BLOCKER 后，核心可成立。贡献是场景暴露与评估隔离的工程方法，不是动态重筛的性能优势。

---

## 6. P5：TRACE-MOEA

### 判定：MINOR

### 已解决

- V-5.2 已明确 12 个 stochastic opponents；AHP-TOPSIS、Weighted Sum、Greedy BCR 的 30 个重复行仅为 provenance，有效样本量为 1。
- 摘要/结果/结论已改为 24/28 stochastic-baseline significant wins，21 deterministic gaps descriptive。
- Preference adaptation 的直接跨场景校正结果为 unresolved，不再从 NSGA-II 场景模式反推组件因果。
- archive 已明确 metric-quarantined，但不代表零计算或人工成本。
- NERC/MTEP p 值已降为 nominal diagnostics，并承认 portfolio dependence、construct overlap 和 strict-label power 不足。

### MAJOR

无新的内部理论或统计阻断项。

### MINOR 6.1：偏好层的已证实作用是轨迹内容，不是优化收益

**证据位置：** VI-6.2、VI-6.3、Conclusion。  
NoPreferenceRanking 的 pooled 差异 0.17%，跨场景校正后未分离。当前结论已经正确写成 its demonstrated function is the preference-elite portion of the audit record。该边界必须延续到 cover letter 和 Highlights。

### MINOR 6.2：trace coverage 不是解释质量

98.6% 只说明最终 front 项目至少出现在一次 recorded event 中，不说明事件与最终入选之间形成完整因果链，也不说明人类能理解或接受。当前 Limitations 已说明 human study 缺失；建议将 `decision trace archive` 始终描述为 event provenance，而不是 validated explanation。

### MINOR 6.3：investment-effectiveness 仍应带 proxy 限定

成本是 synthetic units，MTEP 外部检查又仅是描述性 consistency。标题可以保留，但 Abstract/Conclusion/cover letter 应使用 `proxy investment-effectiveness review benchmark`，不得宣称经济效益或真实审查质量。

### 图表/公式

quarantine invariant、preference update、repair 与 HV 定义已经闭合。无需补公式或框图。真正提升价值的是专家使用性评估，而非视觉扩充。

### 期刊适配

Energies 范围匹配。当前贡献足以作为 auditable optimization/provenance framework，但不应包装为已验证的人机决策支持系统。

---

## 7. P6：BiLo-NSGA

### 判定：MINOR

### 已解决

- Protocol 已将 14 stochastic opponents 与 3 deterministic rules 分开；推断表改用 `real_project_review_inference_v2.csv`。
- 摘要、贡献、结果、结论统一为 36/40 stochastic-baseline wins，16 deterministic gaps descriptive。
- PLS 的 1600 evaluations 仅称 numerical ceiling，不再称等计算工作，并保留 runtime。
- `forward-dominant` 已严格定义为 resolved local-operator gains 出现在 forward side，不代表 pooled improvement。
- atomic substitution 已明确无 accuracy evidence，full/lean deployment trade-off 已进入正文。
- NERC/MTEP 外部结果已改为 descriptive consistency，不再称 confirmatory validity。

### MAJOR

无新的内部阻断项。

### MINOR 7.1：完整算法的主要创新应是审计语义组合

**证据位置：** Abstract、Contribution 1、VI-6.3、VI-6.7。  
NoForward pooled mean 更高，NoBackward 也更高且运行更快。因此 full BiLo-NSGA 的独特价值不是统一的 HV gain，而是项目语义移动、部分场景 forward gains、预算恢复和 dense audit log 的组合。当前标题 “Forward-Dominant Auditable”已基本匹配，需防止 cover letter 重新写成 local search consistently improves NSGA-II。

### MINOR 7.2：atomic substitution 的保留理由尚未被人类验证

“more faithful to project substitution”是合理设计动机，但 archive 是否对评审人有用没有实验。full 只应被推荐给“需要替换事件记录的假设性部署”，不能说它已提高 auditability outcomes。lean variant 是仅关心 HV/runtime 时的合理默认。

### MINOR 7.3：跨场景预算趋势不可作预算因果

当前 Introduction 已承认 budget 和 scalar weights 同时变化，属于 boundary description。该限定应保持；不要把 1.20x 的 +3.30% 归因于 slack mechanism。

### 图表/公式

现有复杂度、移动定义、直接 PLS 和 operator control 图充分。feasibility recovery 的有限终止性可用一句话说明，但无需增加定理。

### 期刊适配

Applied Sciences 适配良好。稿件贡献是应用型、可复现、审计导向的算法边界研究；以当前收窄口径，创新充分且不过度。

---

## 8. 第二轮最终意见与进入第三轮条件

### 必须先完成

1. **P4 删除或修正旧 scenario-call 公式**，保证唯一正式计数为 17,920 的闭合分项式。
2. **P4 将 Contribution 3 的 40/40 修正为 32 stochastic inferential + 16 deterministic descriptive**，并全文搜索旧计数。

### 建议在第三轮前完成

3. P1 将 `reference-policy proxy` 贯穿贡献、表题和结论。
4. P3 将 Figure 3 caption 的 “loses AC feasibility” 改为固定映射下的描述性较低率，并进一步弱化题名中心与 adaptation null 之间的张力。
5. P2/P5/P6 保持当前边界，不再通过摘要压缩把负结果或描述性外部检查删掉。

### 复审结论

- **P4：BLOCKER，当前不可进入投稿定稿。**
- **P1、P3：MAJOR，科学核心仍成立，但论文身份必须稳定为基准/框架与负组件审计。**
- **P2、P5、P6：MINOR，理论与创新边界已基本闭合。**

完成上述条件后，可进入第三轮综合终审；第三轮应重点检查六篇摘要、贡献、结果和结论的数值与限定词是否逐字一致，以及 companion-paper 之间的创新资产是否足够分离。
