# Short-Term Photovoltaic Power Forecasting Based on a Novel Autoformer Model

Symmetry2023,15,238；DOI 10.3390/sym15010238。SHA256 275a3fd0baafde9e09b936df7d279521419b86ab9d35378f2299783dd342a0b6。

29页全部文字/附录/参考已读，14图（含跨页附图）及5表均看图核查；单助手待复核，非人工校准。不是211字段完成，段落地图未做。

## 核心结论边界

多数表内MSE/MAE/RMSE/adjustedR²更优；特定一场站双分辨率数据；attention消融误差增幅最大。

不能支持：所有指标/所有DM比较最优显著、跨领域泛化、对称性保证、长数据导致过拟合的确定因果、真实运行效率优于所有基线。

## 章节逻辑

- 1 Introduction p1–3：电网PV不确定性→标准模型缺口→三项贡献
- 2 Related Work p3–4：统计/ML/RNN/Transformer/Autoformer逐类比较，存在LSTM只能单步的不当泛化
- 3 ADAMS Network Architecture p4–10：Autoformer+多尺度+去平稳注意力+鲁棒损失
- 3.1 Decomposition Architecture p5–6：分解编码解码
- 3.1.1 Series Decomposition Block p5–5：平均池化趋势+剩余季节
- 3.1.2 Model Inputs p5–5：历史24点，后半历史与0/均值占位
- 3.1.3 Encoder p5–5：季节残差编码，趋势剔除
- 3.1.4 Decoder p6–6：三处分解与趋势累加
- 3.2 Auto-Correlation Mechanism p6–7：跨周期序列级依赖
- 3.2.1 Period-Based Dependencies p6–6：自相关选周期
- 3.2.2 Time Delay Aggregation p6–7：TopK lag滚动加权
- 3.2.3 Efficient Computation p7–7：FFT推O(LlogL)
- 3.3 Multi-Scale Framework p7–8：共享参数粗到细预测+跨尺度中心化
- 3.4 De-Stationary Attention p8–9：实例标准化+原始统计MLP修正attention
- 3.5 Adaptive Loss Function p10–10：Barron鲁棒损失
- 4 Experimental Preparation and Framework p10–13：数据/基线/预处理/指标
- 4.1 Experimental Input Data p10–11：单Yulara1058.4kW两分辨率
- 4.2 Experimental Framework p11–12：7模型流程及超参
- 4.3 Data Pre-Processing p12–12：负值删除、插值、70/20/10
- 4.4 Evaluation Metrics p12–13：MSE/MAE/RMSE/adjustedR²
- 5 Experiment and Analysis p13–20：双分辨率预测、DM、消融、长度敏感性
- 5.1 Experiment I: 5-min PV Power Forecasting Experiment p13–15：4/8/12/24步20–120min预测
- 5.2 Experiment II: Hourly PV Power Forecasting Experiment p15–16：4–24h预测
- 5.3 Diebold-Mariano Test p17–17：MSE损失成对检验，宣称全显著与附表冲突
- 5.4 Ablation Study p17–17：去scale、attention、adaptive loss
- 5.5 Further Study p18–20：1–12月/1–6年数据长度比较，解释为未来假说
- 6 Conclusions p20–20：重申性能及长历史干扰假说
- Appendix A Metric scatter plots p21–22：2图各16小轴，重复主表非新试验
- Appendix B Forecast traces p23–27：每种模型单独7条曲线两分辨率
- Appendix C DM matrices p27–28：两表四horizon7×7矩阵
- backmatter Declarations and References p20–29：26参考，DKASC开放数据，代码未给

## 22个编号公式功能

- (1) p5：趋势AvgPool、季节X-Xt；基础Autoformer机制
- (2) p5：SeriesDecomp接口
- (3) p5：半历史+0/均值decoder占位
- (4) p5：残差auto-correlation与FFN后两次分解
- (5) p6：self/cross correlation和FFN三分解，累加趋势
- (6) p6：无限长时间均值定义相关，无有限样本假设证明
- (7) p7：TopK相关lag、softmax、Roll加权
- (8) p7：拼接各头+投影
- (9) p7：Wiener-Khinchin频谱逆变换，标准复杂度来源
- (10) p8：平均池化生成不同尺度历史和预测窗口
- (11) p8：印刷插值增量两项下标相同，相减0；非正常线性插值，代码待查
- (12) p8：历史和decoder预测/占位联合均值去中心，不能直接认定使用真实future泄漏
- (13) p8：尺度位置sin/cos，外加来源和尺度标志
- (14) p9：z-score不保证Gaussian；零方差epsilon未给
- (15) p9：印刷σ⊙(y′+μ)不是σ⊙y′+μ，不能严格逆式14；实现未核
- (16) p9：原始数据与均值/σ生成τ、Δ修正QK；与FFT autocorrelation整合细节不足
- (17) p10：Barron鲁棒loss，α/c训练或取值、特殊值极限未给
- (18) p12：MSE
- (19) p12：MAE
- (20) p12：RMSE应sqrt(MSE)同一聚合
- (21) p12：R² SSE/SST；视觉确认分母有均值bar不是同项相减
- (22) p12：adjustedR² k未给，实际可以负值非仅0–1

## 每图的证据角色

- Figure 1 p10：位置与场站属性。Yulara示意+1058.4kW设备规格表，系统共1.8MW不等所选站。
- Figure 2 p11：数据两分辨率。14堆叠变量曲线；小时轴2018–2022与正文2017–2020不符，实际输入变量数需核（正文列12，图另CPAM/AEDR）。
- Figure 3 p11：实验流程。预处理在split前画出，训练折拟合标准化/插值边界未说明；风险不是已证泄漏。
- Figure 4 p14：5min指标堆叠柱。不同模型误差直接堆叠无统计意义，仅视觉比较；以Table2为准。
- Figure 5 p14：5min所有预测曲线。kW曲线范围3000点，负预测存在，不同RNN曲线与附图差异待查。
- Figure 6 p16：1h指标堆叠柱。同Table3描述性数据重复。
- Figure 7 p16：小时所有预测。约300h重叠曲线，局部细节不能证明泛化。
- Figure 8 p17：消融指标和运行时间。MSE ADAMS .174,去scale .200,去attention .300,去loss .182；time92.261/41.717/104.414/96.579s。
- Figure 9 p18：5min数据长度敏感性。1–12个月指标曲线+2/9/11月代表预测；4月MSE最低，选择过程需独立验证。
- Figure 10 p19：小时数据长度敏感性。1–6年及2/5/6年预测；4年MSE最低但R²图约.9+与主表.824不符，归因假说未证。
- Figure A1 p21：5min指标散点。4指标×4horizon，不是预测真值散点也不是多次重复。
- Figure A2 p22：1h指标散点。同上；个别数值与主表待全面转录核查。
- Figure A3 p23,24,25：七方法5min单独曲线。LSTM/GRU明显峰值低估，不能凭测试误差称过拟合；ADAMS同样有负值。
- Figure A4 p25,26,27：七方法1h单独曲线。峰值偏差与RNN夜间负预测；仅一个示例片段。

## 每表与统计核查

- Table 1 p12：7模型配置。ADAMS/Autoformer/Informer/Transformer dmodel512,seq24,label12,horizon4/8/12/24,itr1,5epochs,lr.0001,dropout.05,batch64;ADAMSadaptive其他MSE。LSTM/GRU/RNN100epochs,相同lr/drop/batch/seq/horizon。无head/layer/scale列表、MLP宽度、lossαc、seed；训练预算异质且作者不比较跨模型收敛时间。
- Table 2 p13：5min7模型4horizon4指标。length4 TransformerMAE.120<ADAMS.146；LSTM MSE.234而正文.304；Informerlength12MSE.130而RMSE.355不相容。
- Table 3 p15：1h同结构指标。ADAMSlength4RMSE.455²=.207025不吻合MSE.197；AutoformerRMSE.448更低。length8adjustedR²Autoformer.857>.856。length24GRUMAE.301<.302。GRUlength12MSE.280与RMSE.540不吻合（平方.2916）。
- Table A1 p27,28：5min DM4个7×7p矩阵。ADAMS12-step对Informer.052、Transformer.714不显著。部分上下三角不对称（如4stepADAMS-LSTM1.39e-133,反向0），若双侧同法不应不同；0可能舍入/下溢非精确零。
- Table A2 p28：小时DM4个7×7p矩阵。ADAMS对6基线均印刷p<.05，但其他配对并非全显著：4hLSTM-GRU.918，8hTransformer-RNN.822。没有原始损失序列无法复算DM。

5min ADAMS不是所有指标最佳：4步Transformer MAE .120小于.146。1h ADAMS4步MSE .197与RMSE .455平方不相符，Autoformer RMSE .448更低；8步adjustedR² .857>.856；24步GRUMAE .301<.302。附表A1 12步ADAMS对Informer p=.052、Transformer p=.714直接反驳全部显著。没有原始损失序列不能复算DM。

消融图8：MSE .174/.200/.300/.182、运行秒92.261/41.717/104.414/96.579；去scale增14.943%、去loss增4.598%，正文对调。没有重复误差条。

## 输入、数据与复现

24历史点多变量PV/天气；decoder后12点历史+0/均值占位 → 4/8/12/24步PV序列：5min为20/40/60/120min，1h为4/8/12/24h。

单Yulara站，70/20/10未给明确时序边界；5min声称2020Sep–Dec34080样本；小时声称2017–202033740但Figure2显示2018–2022。删负值/插值未给日志。dmodel512/seq24/label12/batch64/lr.0001/drop.05，Transformer类5epoch、RNN类100epoch；尺度表/heads/MLP/损失参数缺失。选4月/4年最佳数据跨度是否独立于测试未知。

## Symmetry与机制

周期同相/平移尺度标准化是实际设计；p9宣称平移缩放等变但没有证明，Eq15印刷逆变换错误且MLP依赖rawx使整体等变不能自动推出；非仅标题修辞但严格性质未验证

## 写作机制与难度

问题背景→模型类别短板→模块公式叠加→双时间尺度→显著性→消融→反直觉数据长度现象→假说和未来验证

p15同时说比较成功又未比较，表述自相矛盾。 p3重复ML缺点并p4把RNN限定单步，非方法学必然。 p3GaoLSTM[11]参考实际wordembedding论文，Zang[10]实际He等，引用内部错配。 强肯定语言多，但5.5和结论承认长数据机制证据不足。

原创句式框架：在相同[预测跨度]下，以[基准结构]为载体增加[机制]，再通过[单模块移除]评估其边际贡献。 观察到[经验趋势]尚不足以确认[因果机制]，因此将[固定测试集/注意力诊断]列为后续验证。

- theory：2（1–2），标准FFT/去平稳/多尺度公式重组，无新证明p5–10
- algorithm：3（2–3），多个耦合模块、多尺度共享和loss，细节仍不足
- statistics：2（2–3），DM成对检验有序列相关背景但实现未披露，消融和长度实验
- data：1（1–2），公开单站两分辨率，非多地独立验证
- engineering：1（1–2），离线预测未闭环约束部署
- cross_domain：2（1–2），天气+PV特征时序预测接口明确

版本：公开CDN v2与API时间戳吻合，但未完整取得该文章notes，不宣称已知最新。完整数值转录、逐段地图、211字段、代码和人工校准均未完成。

