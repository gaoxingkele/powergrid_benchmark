# 同期刊 × 同任务校准对照（第一轮）

这是14篇的来源筛选与提取器校准，不是完整论文难度评定。n<10 按本库协议只展示个案，不给期刊平均值。公式/图表的v2仍是候选；双解析器一致也不等于人工金标准。

| 期刊 / 任务 | 已核对任务的篇数 | 子类型 | 状态 |
|---|---|---|---|
| Applied Sciences|electric_load_forecasting|empirical_method | 2 | attention_hybrid, decomposition_hybrid | CASE_SERIES_ONLY |
| Applied Sciences|energy_time_series_mixed_target|empirical_method | 1 | graph_transformer | CASE_SERIES_ONLY |
| Electronics|electric_load_forecasting|empirical_method | 3 | decomposition_hybrid, graph_recurrent_boosting, multichannel_hybrid | CASE_SERIES_ONLY |
| Energies|distribution_resilience_planning|empirical_method | 3 | distributionally_robust, reliability_reinforcement, storage_siting_sizing | CASE_SERIES_ONLY |
| Energies|multi_energy_load_forecasting|empirical_method | 1 | adaptive_graph_attention | CASE_SERIES_ONLY |
| IEEE Access|electric_load_forecasting|empirical_method | 2 | periodic_transformer_recurrent, residential_encoder_decoder | CASE_SERIES_ONLY |
| IEEE Access|traffic_proxy_plus_electric_load|empirical_method | 1 | tensor_graph_transformer | CASE_SERIES_ONLY |
| Sensors|electric_load_forecasting|empirical_method | 1 | transfer_learning | CASE_SERIES_ONLY |

## 逐篇数量对照

页数经页树检查；其他列为严格图题/行级公式标签候选，不是最终人工计数。

| 论文ID | 期刊 | 页数 | 公式候选 | 图候选 | 表候选 |
|---|---|---|---|---|---|
| p_ba8e73559896f121 | Applied Sciences | 15 | 15 | 13 | 1 |
| p_c8763eed4f1a695a | Applied Sciences | 24 | 20 | 9 | 4 |
| p_8685474523df0850 | Applied Sciences | 34 | 14 | 19 | 7 |
| p_9711769edf1bafa5 | Electronics | 23 | 37 | 14 | 9 |
| p_10518b844b194e90 | Electronics | 19 | 24 | 12 | 4 |
| p_e90a29790e1667db | Electronics | 15 | 8 | 12 | 5 |
| p_320f77a542175910 | Energies | 23 | 56 | 6 | 9 |
| p_d2e16e5d3f9b1b3f | Energies | 28 | 37 | 16 | 6 |
| p_e5502fa6e3ee1a5f | Energies | 27 | 33 | 23 | 11 |
| p_e2822d4e02526031 | Energies | 19 | 15 | 4 | 5 |
| p_9054a62c1e9b25b4 | IEEE Access | 15 | 23 | 14 | 5 |
| p_5fd7d69670cfc8e8 | IEEE Access | 13 | 14 | 5 | 7 |
| p_5908282d0c137859 | IEEE Access | 10 | 5 | 7 | 4 |
| p_a1adf441aa349153 | Sensors | 17 | 14 | 7 | 7 |

## 每篇框架与证据使用方式

### A Combined Method for Short-Term Load Forecasting Considering the Characteristics of Components of Seasonal and Trend Decomposition Using Local Regression

ID `p_ba8e73559896f121`；原件 `F:\aicoding\powergrid_benchmark\papers\literature\applied_sciences_power_grid_recent\pdf\applsci-14-02286.pdf`；定位页 [1, 14]。

- 框架：STL分解后分别以LSTM、CNN、GPR预测趋势、季节与残差，最后相加。
- 实验分类：Table 1为预测方法的MAPE/MAE/RMSE对照；不能从一个汇总表推断独立实验设计总数。
- 不可照搬之处：PDF出现重复文字与Figure 77/99等伪标签，先修复图题检测。

### Power Grid Load Forecasting Using a CNN-LSTM Network Based on a Multi-Modal Attention Mechanism

ID `p_c8763eed4f1a695a`；原件 `D:\aicoding\papers\Applied Sciences\2025_Power Grid Load Forecasting Using a CNN-LSTM Network Based on a Multi-Modal Attention Mechanism.pdf`；定位页 [1, 8, 17, 21]。

- 框架：CNN/池化→MHSA→LSTM→GAM→CAM/SE→输出。
- 实验分类：Table 3为4级递增组件链，Table 4为heads/计算成本敏感性；不能合并消融数量。
- 不可照搬之处：表中单值及稳定后取值不自动提供独立样本区间。

### Short-Term Power Load Forecasting Using an Improved Model Integrating GCN and Transformer

ID `p_8685474523df0850`；原件 `D:\aicoding\papers\Applied Sciences\2025_Short-Term Power Load Forecasting Using an Improved Model Integrating GCN and Transformer.pdf`；定位页 [1]。

- 框架：随机森林预处理→多尺度GCN→MLLA改进Transformer。
- 实验分类：摘要列ETTh1、ETTm1及Australian数据；尚未核对各数据实际预测目标。
- 不可照搬之处：先单列混合能源时间序列组，核对ETT输出变量后才可与纯负荷组归并。

### A Short-Term Power Load Forecasting Method Based on SBOA–SVMD-TCN–BiLSTM

ID `p_9711769edf1bafa5`；原件 `D:\aicoding\papers\Electronics\2024_A Short-Term Power Load Forecasting Method Based on SBOA–SVMD-TCN–BiLSTM.pdf`；定位页 [1, 14, 15, 16, 17, 18, 19, 20, 21]。

- 框架：SBOA优化SVMD分解→TCN–BiLSTM预测分量。
- 实验分类：表包含分解参数、分解方法比较、预测器比较、耗时、季节及峰值测试，不能全部称为消融。
- 不可照搬之处：摘要对R²下降的措辞需与指标方向核对；不能照搬其主张强度。

### Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting

ID `p_10518b844b194e90`；原件 `D:\aicoding\papers\Electronics\2025_Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting.pdf`；定位页 [1, 11, 12, 13, 16]。

- 框架：GCN提取相关结构→BiLSTM→贝叶斯优化的AdaBoost组合。
- 实验分类：表有区域负荷输入、周/日性能和结构参数。
- 不可照搬之处：贝叶斯优化属于算法调参机制，不能据此认定完成贝叶斯统计推断。

### Research on a Short-Term Power Load Forecasting Method Based on a Three-Channel LSTM-CNN

ID `p_e90a29790e1667db`；原件 `D:\aicoding\papers\Electronics\2025_Research on a Short-Term Power Load Forecasting Method Based on a Three-Channel LSTM-CNN.pdf`；定位页 [1, 10, 11, 13]。

- 框架：时间、天气、历史负荷三路LSTM→拼接→1D CNN→24h预测。
- 实验分类：激活函数、优化器、历史窗口比较应与两数据集主比较分别分类。
- 不可照搬之处：窗口与优化器试验是敏感性/配置选择，不自动证明三通道的独立贡献。

### A Differential Planning Strategy for Distribution Network Resilience Enhancement Considering Decision Dependence Uncertainty

ID `p_320f77a542175910`；原件 `D:\aicoding\papers\Energies\2025_A Differential Planning Strategy for Distribution Network Resilience Enhancement Considering Decision Dependence Uncertainty.pdf`；定位页 [1, 14, 15, 16, 17, 18, 19, 20]。

- 框架：决策相关故障不确定性→三级分布鲁棒加固规划→Sobol敏感性解释。
- 实验分类：预算、置信集、场景缩减、Sobol指标与33/123节点案例分开记录。
- 不可照搬之处：概率/不确定性建模不等同于在多个独立网络上进行统计推断。

### A Distributed Energy Storage-Based Planning Method for Enhancing Distribution Network Resilience

ID `p_d2e16e5d3f9b1b3f`；原件 `D:\aicoding\papers\Energies\2026_A Distributed Energy Storage-Based Planning Method for Enhancing Distribution Network Resilience.pdf`；定位页 [1, 20, 21, 22]。

- 框架：改进GMM风光情景→分区需求优先级→混合整数规划→节点/区块/全网评价。
- 实验分类：Table 3映射输入、工具、结果及章节；Table 5比较储能规划案例，Table 6比较电气性能。
- 不可照搬之处：网络信息不完整的规划口径与完整馈线物理认证不能等同。

### Reliability-Oriented Distribution System Reinforcement Planning with Renewable Resources Considering Network Restoration and Intentional Islanding

ID `p_e5502fa6e3ee1a5f`；原件 `D:\aicoding\papers\Energies\2026_Reliability-Oriented Distribution System Reinforcement Planning with Renewable Resources Considering Network Restoration and Intentional Islanding.pdf`；定位页 [1, 15, 18, 20, 21, 24]。

- 框架：多阶段加固/开关与容量决策→恢复及孤岛运行→概率可靠性评估→GA搜索。
- 实验分类：两个case的建设动作和NPV费用表需与可靠性参数表分开。
- 不可照搬之处：GA、可靠性概率与规划经济三个理论接口分别评分，不能以公式总数统一代替。

### Short-Term Multi-Energy Load Forecasting Method Based on Transformer Spatio-Temporal Graph Neural Network

ID `p_e2822d4e02526031`；原件 `D:\aicoding\papers\Energies\2025_Short-Term Multi-Energy Load Forecasting Method Based on Transformer Spatio-Temporal Graph Neural Network.pdf`；定位页 [1, 12, 13, 14, 15]。

- 框架：多头时空注意力＋物理拓扑/相似性自适应图→encoder–decoder联合预测。
- 实验分类：主比较、训练/推断时间、联合/单独预测、辅助信息与模块消融分别对应Table 1–5。
- 不可照搬之处：电、冷、热输出不同，不与单一电负荷误差跨量纲汇总。

### Enhancing Short-Term Power Load Forecasting With a TimesNet-Crossformer-LSTM Approach

ID `p_9054a62c1e9b25b4`；原件 `F:\aicoding\powergrid_benchmark\papers\literature\target_journal_related\pdfs\p1_ieee_access_extension\ieee_access_2024_timesnet_crossformer_lstm.pdf`；定位页 [1, 9, 11, 13, 14]。

- 框架：TimesNet将时序映射为二维→Crossformer建模维度关系→LSTM输出。
- 实验分类：滑动窗口、主比较、多步预测、参数表及参数敏感性分别记录。
- 不可照搬之处：两个地区结果不直接证明节能减排收益；双栏图题及公式计数需要布局修复。

### Fusion ConvLSTM-Net: Using Spatiotemporal Features to Increase Residential Load Forecast Horizon

ID `p_5fd7d69670cfc8e8`；原件 `D:\aicoding\papers\IEEE Access\2025_Fusion ConvLSTM-Net for Enlarging Forecast Horizon of Residential Load Prediction.pdf`；定位页 [1, 7, 8, 9, 10]。

- 框架：融合时空特征的ConvLSTM encoder–decoder，考察最长24h居民负荷预测。
- 实验分类：窗口范围、10户平均和100户聚合预测是不同设计；参数数与超参数表用于核查比较公平性。
- 不可照搬之处：户数、窗口数、聚合输出数不应全部作为独立数据集。

### LoadSeer: Exploiting Tensor Graph Convolutional Network for Power Load Forecasting With Spatio-Temporal Characteristics

ID `p_5908282d0c137859`；原件 `D:\aicoding\papers\IEEE Access\2024_LoadSeer Exploiting Tensor Graph Convolutional Network for Power Load Forecasting With Spatio-Temporal Characteristics.pdf`；定位页 [1, 7, 8]。

- 框架：距离邻接＋GCN＋T-Transformer，包含PeMS交通基准及Flowload负荷验证。
- 实验分类：Table 1是PeMS，Table 2是Flowload；GCN与T-Transformer消融须保留各自数据集身份。
- 不可照搬之处：从纯电力负荷同类均值剔除，保留跨领域代理验证案例；不能以标题替代数据语义。

### Affinity-Driven Transfer Learning for Load Forecasting

ID `p_a1adf441aa349153`；原件 `D:\aicoding\papers\Sensors\2024_Affinity-Driven Transfer Learning for Load Forecasting.pdf`；定位页 [1, 7, 10, 12, 13, 14]。

- 框架：任务亲和分数选择预训练任务/模型→ADTL迁移预测。
- 实验分类：合成任务相似性验证与AEMO/Smart Australian实证分开，另有随机模型及降采样比较。
- 不可照搬之处：不把合成验证当真实负荷外部验证；本地该刊仅一篇，不能形成期刊均值。
