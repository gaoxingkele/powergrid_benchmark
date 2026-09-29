# 原始62篇候选覆盖审计

当前源绑定快照：**13/62** 已有实质全文解构文件，**49/62** 尚未形成个案；全字段验收完成 **0**。49个case文件中的另外36个新增/替代样本不抵扣原候选。

## 权威清单与过滤规则

权威数据为 `calibration/2026-09-13_power_ai_scope/scope_records.json`，169行中选择 `journal_core_candidate === true`，恰好62条。该字段由 `scripts/finalize_power_ai_scope.py:71–73` 定义：核心AI、源完整性/范围筛查通过、期刊身份可用。`validation_report.json` 与 `SCOPE_REPORT.md`候选列交叉吻合；报告绑定的7项输入哈希和原manifest哈希均匹配。完整来源SHA见JSON。

`core_ai_reading_list.json`是63条范围核心清单，不是62条期刊候选；多出的 `p_cfabc8737fb852fe` 因Machines身份冲突不计62，原记录保留。169总池也不能当62队列。CHECKPOINT早先9/62只是历史快照。

按规范化DOI精确匹配，ID/原件SHA仅确认。62条DOI均存在且唯一；13个匹配案例原件SHA均相同，源/页数/实质对象/MD存在检查通过。此处不重新认证阅读全文，不升级科学审核状态；后续即使范围排除也应保留原候选历史。

## 分刊覆盖

| 期刊 | 原候选 | 已有全文个案 | 尚未完成 |
|---|---:|---:|---:|
| Applied Sciences | 19 | 3 | 16 |
| Electronics | 11 | 3 | 8 |
| Energies | 21 | 3 | 18 |
| IEEE Access | 10 | 3 | 7 |
| Sensors | 1 | 1 | 0 |

## 逐条原候选

状态“已有”仅指单助手全文解构存在，仍待字段补全/独立复核；“未完成”不表示已排除。

| 原ID | DOI | 期刊 | 匹配case / 状态 | 原范围边界 |
|---|---|---|---|---|
| p_1c6227810781bc96 | 10.3390/app16125815 | Applied Sciences | 未完成：无DOI匹配case | 变电站日前负荷预测；混合统计与学习框架。 |
| p_ba8e73559896f121 | 10.3390/app14062286 | Applied Sciences | [p_ba8e73559896f121](papers/p_ba8e73559896f121.md) 已有全文个案/字段未全验收 | 短期电力负荷预测；分别用LSTM、CNN和高斯过程回归预测电负荷分解分量。 |
| p_c0555a332fe74ffa | 10.3390/app131911074 | Applied Sciences | 未完成：无DOI匹配case | 电网文本实体关系抽取；电力信息/NLP层，不与物理负荷预测共组。 |
| p_326a82408d768808 | 10.3390/app14093682 | Applied Sciences | 未完成：无DOI匹配case | 微网能量传输和储能调度；以线路潮流和电池充放电为动作，采用双层深度Q网络降低微网运行成本。 |
| p_2766f9f59b4da813 | 10.3390/app16010466 | Applied Sciences | 未完成：无DOI匹配case | 超短期风电功率预测；摘要说明用实际风场数据评估图结构和时序深度学习预测风电输出。 |
| p_bad7cdc0d2139c2d | 10.3390/app14083253 | Applied Sciences | 未完成：无DOI匹配case | 韧性微网能量管理；将多阶段约束处理进化算法用于发电机、储能及负荷协同管理。 |
| p_ab865359b59b62f3 | 10.3390/app132312946 | Applied Sciences | 未完成：无DOI匹配case | 中期电负荷预测；摘要的因果措辞不视为已证明因果。 |
| p_452473d6065c05bf | 10.3390/app16125952 | Applied Sciences | 未完成：无DOI匹配case | 孤岛可再生微网低碳经济调度；统计检验及改善数值尚未逐项复算。 |
| p_a4aef6fe4f69a3c6 | 10.3390/app15179578 | Applied Sciences | 未完成：无DOI匹配case | 高耗能工业园区电力负荷预测；是工业用电任务，不是通用工业过程预测。 |
| p_cbdf74a0a3ee1879 | 10.3390/app16136581 | Applied Sciences | 未完成：无DOI匹配case | 电网应急通信无人机设备部署与路由；电网应急支撑/通信子层；p16数值场景含随机生成部署点，不能称真实电网实证或并入纯潮流调度组。 |
| p_ad68e8fbf5ffaa73 | 10.3390/app16094476 | Applied Sciences | 未完成：无DOI匹配case | 风场一次调频及疲劳负荷优化；AI代理辅助物理控制优化。 |
| p_489c49e78e51b9d3 | 10.3390/app132312690 | Applied Sciences | 未完成：无DOI匹配case | 含分布式电源及充电站的配网电压控制；EV为配电网负荷组成，不是通用交通数据混入。 |
| p_a7e072dc13799581 | 10.3390/app14156486 | Applied Sciences | 未完成：无DOI匹配case | 输电网络与储能多阶段规划；AI仅为无监督场景预处理；不得描述为AI主导规划创新，建议与纯AI预测分层。 |
| p_c8763eed4f1a695a | 10.3390/app15052435 | Applied Sciences | [p_c8763eed4f1a695a](papers/p_c8763eed4f1a695a.md) 已有全文个案/字段未全验收 | 短期电网负荷预测；摘要明确以电网负荷为预测对象并设计多注意力深度网络。 |
| p_8685474523df0850 | 10.3390/app15137003 | Applied Sciences | [p_8685474523df0850](papers/p_8685474523df0850.md) 已有全文个案/字段未全验收 | 电力负荷及变压器时序预测；ETT包含负荷与油温，具体预测目标列需另核；不能把所有ETT实验默认称纯负荷预测。 |
| p_9c09ca32bb944981 | 10.3390/app152211944 | Applied Sciences | 未完成：无DOI匹配case | 电网侧储能选址定容及收益分析；manifest标题错误：Type of the Paper (Article；首页为 Optimal Planning and Investment Return Analysis of Grid-Side Energy Storage System Addressing Multi-Dimensional Grid Security Requirements。AI为辅助聚类。 |
| p_00f2109a3c4a11f7 | 10.3390/app14031077 | Applied Sciences | 未完成：无DOI匹配case | 分布式电源配置与配网降损稳压；manifest标题错误：Type of the Paper (Article；首页为 A New Framework for Active Loss Reduction and Voltage Profile Enhancement in a Distributed Generation-Dominated Radial Distribution Network。 |
| p_e313e20741205e6c | 10.3390/app13021165 | Applied Sciences | 未完成：无DOI匹配case | 居民群体日负荷预测；manifest标题为文件名；首页为 A Group Resident Daily Load Forecasting Method Fusing Self-Attention Mechanism Based on Load Clustering。 |
| p_6b0ed6f66f1120d0 | 10.3390/app15084498 | Applied Sciences | 未完成：无DOI匹配case | 大规模机组组合求解加速；manifest标题为文件名；首页为 Stable Variable Fixation for Accelerated Unit Commitment via Graph Neural Network and Linear Programming Hybrid Learning。 |
| p_1445a9c9cbf22bc0 | 10.3390/electronics12163441 | Electronics | 未完成：无DOI匹配case | 电力负荷预测；分解是预处理，AI主体为LSTM。 |
| p_9711769edf1bafa5 | 10.3390/electronics13173441 | Electronics | [p_9711769edf1bafa5](papers/p_9711769edf1bafa5.md) 已有全文个案/字段未全验收 | 短期电力负荷预测；不核验摘要所报误差改善数值。 |
| p_10518b844b194e90 | 10.3390/electronics14163332 | Electronics | [p_10518b844b194e90](papers/p_10518b844b194e90.md) 已有全文个案/字段未全验收 | 电力负荷预测；摘要明确图卷积、时序网络及集成学习用于区域电网负荷。 |
| p_cc51cb0656cf5d5a | 10.3390/electronics14214324 | Electronics | 未完成：无DOI匹配case | 配电网韧性与重构；证明概念研究，不据此升级真实运行验证。 |
| p_42baf903da8032db | 10.3390/electronics13173552 | Electronics | 未完成：无DOI匹配case | 电力负荷预测；标题智能控制主张不在本轮验证范围。 |
| p_420070420330785c | 10.3390/electronics15050933 | Electronics | 未完成：无DOI匹配case | 含电综合能源系统低碳经济调度；混合多能源任务单列，不与纯电网调度无差别合并。 |
| p_8db7e3f02e6f241a | 10.3390/electronics14020264 | Electronics | 未完成：无DOI匹配case | 数据中心AC/DC配电系统规划；不能因摘要仅背景提AI而排除；实际群智能证据位于物理页10。 |
| p_e95ce080bf642a40 | 10.3390/electronics14010151 | Electronics | 未完成：无DOI匹配case | 配电网EV充电站选址定容与共享储能；EV直接参与配电网而非泛交通路线优化。 |
| p_20e6b14a4f6e1ca0 | 10.3390/electronics13163139 | Electronics | 未完成：无DOI匹配case | 微电网群经济调度；摘要明确改进灰狼算法求解微网群含运行费用和储能损耗的调度模型。 |
| p_e90a29790e1667db | 10.3390/electronics14112262 | Electronics | [p_e90a29790e1667db](papers/p_e90a29790e1667db.md) 已有全文个案/字段未全验收 | 短期电力负荷预测；摘要明确天气、时间与历史负荷分别输入LSTM，CNN融合后预测未来24小时负荷。 |
| p_ef3d60435149c14f | 10.3390/electronics13204086 | Electronics | 未完成：无DOI匹配case | 微电网经济调度；摘要明确含风、光、火电和储能的微网经济调度由SCMPSO求解。 |
| p_d2e16e5d3f9b1b3f | 10.3390/en19020574 | Energies | [p_d2e16e5d3f9b1b3f](papers/p_d2e16e5d3f9b1b3f.md) 已有全文个案/字段未全验收 | 配电网分布式储能规划与新能源场景建模；AI用于场景生成子模块，规划主体为MILP；应与端到端学习规划分层。 |
| p_81e108fa8de5a743 | 10.3390/en19092172 | Energies | 未完成：无DOI匹配case | 风电-氢能投资规划；含电风氢耦合任务；群智能/元启发式与数学规划混合。 |
| p_b443ed05be72539e | 10.3390/en13102559 | Energies | 未完成：无DOI匹配case | 智能电网稳定性预测；实际知识规则学习与进化优化，不仅泛称智能电网。 |
| p_1c7fc21a51320111 | 10.3390/en18184986 | Energies | 未完成：无DOI匹配case | 高新能源电网混合储能双层规划；群智能用于规划/功率分配，不是神经网络预测。 |
| p_636aa83561e7827a | 10.3390/en13010275 | Energies | 未完成：无DOI匹配case | 含DER配电系统故障定位；摘要明确支持向量数据描述与核密度估计构建子区域故障置信度并定位。 |
| p_75dc0a979dc647a3 | 10.3390/en18184833 | Energies | 未完成：无DOI匹配case | 配电网重构、柔性提升与设备维护；摘要的预测性维护主张不等同已验证独立故障预测模型。 |
| p_b06c883a7ef9d449 | 10.3390/en18133414 | Energies | 未完成：无DOI匹配case | 混合水火风光发电经济调度；摘要明确DE作为水火等混合电源经济调度的重点求解器。 |
| p_db549ba9e7671d5d | 10.3390/en18020266 | Energies | 未完成：无DOI匹配case | 不确定新能源与负荷下配电网动态重构；摘要明确COA元启发式求解非凸配网小时重构问题。 |
| p_d8a62a241050f735 | 10.3390/en16196838 | Energies | 未完成：无DOI匹配case | 可再生微网容量和运行联合规划；摘要明确LSTM预测与多目标PSO容量/运行规划结合，对象为PV风机储能微网。 |
| p_dc237b1f29c2fbc0 | 10.3390/en18112842 | Energies | 未完成：无DOI匹配case | 智能电网负荷预测；manifest为Word伪标题；原文：Optimizing Smart Grid Load Forecasting via a Hybrid Long Short-Term Memory-XGBoost Framework: Enhancing Accuracy, Robustness, and Energy Management。 |
| p_186436a46ccda89d | 10.3390/en19061473 | Energies | 未完成：无DOI匹配case | 电力负荷预测；manifest为Word伪标题；原文：Research on BiLSTM–Transformer Power Load Forecasting Method Based on Dynamic Adaptive Fusion。 |
| p_01738d96ed4b1b6b | 10.3390/en18195232 | Energies | 未完成：无DOI匹配case | 配电网储能与EV协调规划；摘要明确改进NSGA-II带混合编码与可行性处理，规划IEEE33节点储能和电动汽车。 |
| p_bb40bf8ee9fed921 | 10.3390/en18092283 | Energies | 未完成：无DOI匹配case | 含电综合能源低碳运行；混合多能源任务单列。 |
| p_61ed73c9fcb24943 | 10.3390/en18102527 | Energies | 未完成：无DOI匹配case | 温控负荷柔性下储能电站配置；温控负荷为电力灵活资源，而非纯供热系统。 |
| p_d74988cdb21ea70c | 10.3390/en18123061 | Energies | 未完成：无DOI匹配case | 海上风场储能配置；摘要明确NSGA-II权衡风电波动和储能成本，包含现货交易情景。 |
| p_e5502fa6e3ee1a5f | 10.3390/en19061581 | Energies | [p_e5502fa6e3ee1a5f](papers/p_e5502fa6e3ee1a5f.md) 已有全文个案/字段未全验收 | 配电系统可靠性加固与恢复规划；摘要明确GA元启发式求解联络线、开关、馈线和变电站加固规划。 |
| p_e2822d4e02526031 | 10.3390/en18174466 | Energies | [p_e2822d4e02526031](papers/p_e2822d4e02526031.md) 已有全文个案/字段未全验收 | 电-冷-热多能源负荷预测；含电综合能源预测单列。 |
| p_60b5e935f0348a75 | 10.3390/en16207215 | Energies | 未完成：无DOI匹配case | 电网投资组合风险收益优化；电网投资任务单列；ILA按群体元启发式纳入，不把Bayesian BWM本身称为AI。manifest为模板伪标题；原文：A Novel Hybrid Power-Grid Investment Optimization Model with Collaborative Consideration of Risk and Benefit。 |
| p_0d92b515c43bb9a7 | 10.3390/en19010228 | Energies | 未完成：无DOI匹配case | 主动配电网源网储扩张及场景生成；AI场景生成与传统优化混合；manifest为模板伪标题；原文：Coordinated Source–Network–Storage Expansion Planning of Active Distribution Networks Based on WGAN-GP Scenario Generation。 |
| p_43dadead02f76c04 | 10.3390/en19010210 | Energies | 未完成：无DOI匹配case | 配网韧性与储能配置；manifest为模板伪标题；原文：Vulnerability-Driven Multi-Objective Energy Storage Planning Using Enhanced Beluga Whale Optimization for Resilient Distribution Networks。 |
| p_bc05d46c81264e27 | 10.3390/en19122798 | Energies | 未完成：无DOI匹配case | 抽水储能与骨干电网韧性规划；manifest为模板伪标题；原文：Bi-Objective Resilient Backbone-Grid Planning via a Three-Stage TER-NSGA-II Approach Considering Pumped-Storage Hub Effects。 |
| p_76bd3403ef95b3c1 | 10.1109/ACCESS.2023.3262171 | IEEE Access | [p_76bd3403ef95b3c1](papers/p_76bd3403ef95b3c1.md) 已有全文个案/字段未全验收 | 电力物联网负荷预测与通信压缩；在电负荷基准数据上实际训练联邦预测模型，并降低模型上传通信开销。 |
| p_2c8c3d6427f3b9f8 | 10.1109/ACCESS.2025.3544523 | IEEE Access | 未完成：无DOI匹配case | 静态及动态输电网扩展规划；通用函数与电网规划实验须分开聚合。 |
| p_9054a62c1e9b25b4 | 10.1109/ACCESS.2024.3383912 | IEEE Access | 未完成：无DOI匹配case | 短期电力负荷预测；摘要明确澳大利亚和美国电负荷数据上的混合深度模型。 |
| p_5fd7d69670cfc8e8 | 10.1109/ACCESS.2025.3528072 | IEEE Access | 未完成：无DOI匹配case | 居民24小时电负荷预测；针对家庭能源消费预测，评估跨家庭与汇总负荷的深度网络。 |
| p_5908282d0c137859 | 10.1109/ACCESS.2024.3514174 | IEEE Access | 未完成：无DOI匹配case | 电力及交通时空序列预测；混合电力+交通证据；PeMSD4/D7/D8不能当电力数据，禁止将整篇全部实验并入纯电力组。 |
| p_03241b3797adbc1f | 10.1109/ACCESS.2024.3384246 | IEEE Access | 未完成：无DOI匹配case | 短期电力负荷组合预测；用西班牙电负荷数据评估分解特征选择及混合深度预测。 |
| p_b02e33f9916fbf9f | 10.1109/ACCESS.2024.3432647 | IEEE Access | 未完成：无DOI匹配case | 配电系统短期负荷预测；以埃塞俄比亚Jimma配电负荷为对象，遗传算法组合输入并用LSTM预测。 |
| p_0e43fa69b58683db | 10.1109/ACCESS.2024.3437247 | IEEE Access | [p_0e43fa69b58683db](papers/p_0e43fa69b58683db.md) 已有全文个案/字段未全验收 | 短期电力负荷预测；实际用差分进化与改进Harris hawk优化BiLSTM超参数预测电负荷。 |
| p_1d0f96081ce9a6ff | 10.1109/ACCESS.2023.3273596 | IEEE Access | [p_1d0f96081ce9a6ff](papers/p_1d0f96081ce9a6ff.md) 已有全文个案/字段未全验收 | 短期电力负荷预测；对电负荷进行模态分解并用金字塔注意力网络预测。 |
| p_9a7efe82b64a0429 | 10.1109/ACCESS.2024.3377097 | IEEE Access | 未完成：无DOI匹配case | 电力负荷组合预测；结合进化ELM和优化SVM预测，并用混沌麻雀搜索求组合权重。 |
| p_a1adf441aa349153 | 10.3390/s24175802 | Sensors | [p_a1adf441aa349153](papers/p_a1adf441aa349153.md) 已有全文个案/字段未全验收 | 电力负荷迁移预测；合成验证与电负荷案例分开聚合。 |

## 非原62的新增/替代个案（不抵扣）

| case | DOI | 场所 |
|---|---|---|
| [p_014c0607794b2647](papers/p_014c0607794b2647.md) | 10.3390/s24237440 | Sensors |
| [p_08572729ec0b3fc8](papers/p_08572729ec0b3fc8.md) | 10.3390/math11122786 | Mathematics |
| [p_1544450a4942af00](papers/p_1544450a4942af00.md) | 10.1109/pesgm51994.2024.10688596 | IEEE PES General Meeting |
| [p_1725337431f8f83f](papers/p_1725337431f8f83f.md) | 10.1109/smartgridcomm47815.2020.9302996 | IEEE SmartGridComm |
| [p_1e317ca084d206d7](papers/p_1e317ca084d206d7.md) | 10.3390/a19030208 | Algorithms |
| [p_225cc673551ef0cf](papers/p_225cc673551ef0cf.md) | 10.3390/atmos14030430 | Atmosphere |
| [p_275a3fd0baafde9e](papers/p_275a3fd0baafde9e.md) | 10.3390/sym15010238 | Symmetry |
| [p_2913e7fc055e5e46](papers/p_2913e7fc055e5e46.md) | 10.3390/machines8040080 | Machines |
| [p_2b4d013c99a281e1](papers/p_2b4d013c99a281e1.md) | 10.3390/a19080661 | Algorithms |
| [p_3df614f4a424e0bb](papers/p_3df614f4a424e0bb.md) | 10.1109/smartgridcomm57358.2023.10333971 | IEEE SmartGridComm |
| [p_427b90ee2df2e13b](papers/p_427b90ee2df2e13b.md) | 10.1109/ISGT.2017.8085971 | IEEE ISGT |
| [p_47db259422c40ab4](papers/p_47db259422c40ab4.md) | 10.1109/ISGTEurope64741.2025.11305544 | IEEE ISGT |
| [p_4c705a124b1bc0ac](papers/p_4c705a124b1bc0ac.md) | 10.1109/ISGT51731.2023.10066368 | IEEE ISGT |
| [p_553868363ca56d5c](papers/p_553868363ca56d5c.md) | 10.3390/pr8020157 | Processes |
| [p_5c0141040ef94262](papers/p_5c0141040ef94262.md) | 10.1109/pesgm48719.2022.9916594 | IEEE PES General Meeting |
| [p_61e82cc0ce8ee029](papers/p_61e82cc0ce8ee029.md) | 10.3390/info17080789 | Information |
| [p_6236919871ae2948](papers/p_6236919871ae2948.md) | 10.3390/sym18020343 | Symmetry |
| [p_654ca5ab287c1e14](papers/p_654ca5ab287c1e14.md) | 10.3390/info12120516 | Information |
| [p_65b239ff31e3927e](papers/p_65b239ff31e3927e.md) | 10.3390/s20092668 | Sensors |
| [p_6d1797c83b82e1d9](papers/p_6d1797c83b82e1d9.md) | 10.3390/math13101584 | Mathematics |
| [p_71fe4f1acd7e01c5](papers/p_71fe4f1acd7e01c5.md) | 10.3390/info12020050 | Information |
| [p_72af029b1d18f736](papers/p_72af029b1d18f736.md) | 10.3390/sym16030322 | Symmetry |
| [p_7ecd008505a3dcdd](papers/p_7ecd008505a3dcdd.md) | 10.3390/rs15061570 | Remote Sensing |
| [p_8d3953ef8ba14b34](papers/p_8d3953ef8ba14b34.md) | 10.3390/atmos15080929 | Atmosphere |
| [p_90629d39fb165b31](papers/p_90629d39fb165b31.md) | 10.3390/pr12030546 | Processes |
| [p_925a950e7eb34105](papers/p_925a950e7eb34105.md) | 10.3390/machines10090785 | Machines |
| [p_99d5789225866f6f](papers/p_99d5789225866f6f.md) | 10.1109/pesgm48719.2022.9916659 | IEEE PES General Meeting |
| [p_9ec5b270f1dfd020](papers/p_9ec5b270f1dfd020.md) | 10.3390/pr12040793 | Processes |
| [p_bea727023577260b](papers/p_bea727023577260b.md) | 10.3390/a17110510 | Algorithms |
| [p_c6289136e937a5f3](papers/p_c6289136e937a5f3.md) | 10.3390/su16041710 | Sustainability |
| [p_d564ed78dc6f82bd](papers/p_d564ed78dc6f82bd.md) | 10.3390/su162411252 | Sustainability |
| [p_d712031a5104eac4](papers/p_d712031a5104eac4.md) | 10.3390/math11214561 | Mathematics |
| [p_ebd2bfc3b931715c](papers/p_ebd2bfc3b931715c.md) | 10.3390/machines10080687 | Machines |
| [p_f6b2f76f829fe8f8](papers/p_f6b2f76f829fe8f8.md) | 10.3390/fi15010022 | Future Internet |
| [p_fc67db3300b37eb4](papers/p_fc67db3300b37eb4.md) | 10.3390/atmos12010124 | Atmosphere |
| [p_fd65e61809676d21](papers/p_fd65e61809676d21.md) | 10.1109/smartgridcomm51999.2021.9632307 | IEEE SmartGridComm |

## 审计边界

这是49份case的文件哈希快照，不是实时索引。新增个案后应重跑核对。未修改全局索引、候选清单或论文。逐条标题、来源哈希、既有范围理由、case技术检查结果均见配套JSON；本轮不重新科学裁决范围或验证参考文献。

