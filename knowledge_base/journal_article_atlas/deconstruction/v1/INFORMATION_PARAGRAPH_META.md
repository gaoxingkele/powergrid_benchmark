# Information逐段映射与元解构台账

每行绑定原文位置；词数沿用已声明tokenizer。新增语义字段尚待逐项标注，见配套JSON字段字典。
阅读顺序不代表论证关系；文本分区闭合不代表所有科学字段已完成。

## p_71fe4f1acd7e01c5

| 段ID | 章节 | 原文页/块/行（行区间左闭右开） | 类型 | 主要作用 | 词数 | 功能概括 |
|---|---|---|---|---|---:|---|
| P001 | S1 | 1/28/[0, 8] | prose | background | 92 | 电力运行协调与负荷预测的作用 |
| P002 | S1 | 1/29/[0, 9] | prose | definition | 111 | 区分短中长期运行规划时间尺度 |
| P003 | S1 | 1/30/[0, 6]; 2/1/[0, 8] | prose | background | 185 | 以巴拿马公开数据与调度流程界定应用场景 |
| P004 | S1 | 2/2/[0, 10] | prose | problem | 126 | 定义168小时周预测及预期调度用途 |
| P005 | S1 | 2/3/[0, 9] | prose | objective | 112 | 说明更新预测工具与比较研究的目标 |
| P006 | S1 | 2/4/[0, 4] | prose | contribution | 35 | 预告XGB结果与重要性分析 |
| P007 | S1 | 2/5/[0, 4] | prose | transition | 51 | 介绍全文结构 |
| P008 | S1L | 2/7/[0, 13] | prose | background | 160 | 按应用规模和预测跨度梳理STLF研究 |
| P009 | S1L | 2/8/[0, 4]; 3/1/[0, 3] | prose | comparison | 78 | 由持续性基线引入预测方法综述 |
| P010 | S1L | 3/1/[3, 13] | prose | comparison | 124 | 比较经典时序模型与外部输入的作用 |
| P011 | S1L | 3/2/[0, 11] | prose | comparison | 133 | 比较近期ML与经典时序模型文献 |
| P012 | S1L | 3/3/[0, 10] | prose | comparison | 131 | 描述MLR预测相关研究 |
| P013 | S1L | 3/4/[0, 13] | prose | comparison | 167 | 描述ANN灵活性与既有应用 |
| P014 | S1L | 3/5/[0, 7]; 4/1/[0, 7] | prose | comparison | 199 | 讨论SVR及相关变体的预测应用 |
| P015 | S1L | 4/2/[0, 6] | prose | comparison | 72 | 介绍RF集成与负荷预测案例 |
| P016 | S1L | 4/3/[0, 9] | prose | comparison | 112 | 比较建筑负荷的多种模型及XGB |
| P017 | S1L | 4/4/[0, 14] | prose | comparison | 194 | 介绍XGB天气输入和调参研究 |
| P018 | S1L | 4/5/[0, 5] | prose | comparison | 58 | 说明相似日训练对XGB的改进思路 |
| P019 | S1L | 4/6/[0, 8] | prose | comparison | 102 | 介绍重要性驱动聚类和混合建模 |
| P020 | S1L | 4/7/[0, 5]; 5/1/[0, 4] | prose | comparison | 116 | 区分多步直接与递归预测策略 |
| P021 | S1L | 5/2/[0, 6] | prose | comparison | 67 | 引入水电来水的分解预测案例 |
| P022 | S1L | 5/3/[0, 11] | prose | comparison | 141 | 介绍ANN与bagging/boosting集成 |
| P023 | S1L | 5/4/[0, 16] | prose | comparison | 211 | 介绍RNN和LSTM等时序网络 |
| P024 | S1L | 5/5/[0, 5] | prose | comparison | 54 | 补充SGTM混合方法案例 |
| P025 | S2 | 5/7/[0, 3] | prose | experimental_setup | 35 | 报告硬件、Python和Colab环境 |
| P026 | S21 | 5/9/[0, 2] | prose | experimental_setup | 30 | 给出数据公开性、采样频率和期间 |
| P027 | S21 | 5/10/[0, 3] | list_item | experimental_setup | 22 | 列出CND负荷与历史预测来源 |
| P028 | S21 | 6/1/[0, 3] | list_item | experimental_setup | 22 | 列出日历假日与学校数据来源 |
| P029 | S21 | 6/1/[3, 7] | list_item | experimental_setup | 24 | 列出三个城市的卫星天气来源 |
| P030 | S21 | 6/2/[0, 7] | prose | experimental_setup | 91 | 解释异构文件读取、二值日历和天气整合 |
| P031 | S21 | 6/3/[0, 4] | prose | experimental_setup | 50 | 定义整合后时间索引、列数和记录数 |
| P032 | S21 | 6/11/[0, 3] | prose | experimental_setup | 44 | 说明缺失检查和保留停电异常值 |
| P033 | S21 | 6/12/[0, 9] | prose | algorithm_explanation | 145 | 构造日历变量及工作日指示变量 |
| P034 | S21 | 6/13/[0, 4] | prose | algorithm_explanation | 51 | 构造负荷周滞后、移动均值和离散性变量 |
| P035 | S21 | 6/14/[0, 8]; 7/1/[0, 13] | prose | algorithm_explanation | 277 | 筛选35个候选变量到13个，并解释天气关联 |
| P036 | S22 | 7/4/[0, 11]; 8/1/[0, 2] | prose | experimental_setup | 189 | 裁剪完整周并选择14个测试周 |
| P037 | S22 | 8/2/[0, 6] | prose | implication | 74 | 解释可解释模型对决策者信任的价值 |
| P038 | S22 | 8/3/[0, 6] | prose | definition | 67 | 列出五个ML候选模型与实现工具 |
| P039 | S22 | 8/4/[0, 6] | prose | algorithm_explanation | 74 | 说明MLR与作者给出的假设 |
| P040 | S22 | 8/5/[0, 6] | prose | algorithm_explanation | 78 | 说明KNN近邻预测机制 |
| P041 | S22 | 8/6/[0, 6] | prose | algorithm_explanation | 82 | 说明SVR目标及核映射 |
| P042 | S22 | 8/7/[0, 4] | prose | algorithm_explanation | 56 | 说明RF独立树与均值集成 |
| P043 | S22 | 8/8/[0, 6] | prose | algorithm_explanation | 73 | 说明XGB加性树与正则化 |
| P044 | S22 | 8/9/[0, 11] | prose | experimental_setup | 147 | 定义滑动时间交叉验证、验证周与72小时信息缺口 |
| P045 | S22 | 9/2/[0, 7] | prose | experimental_setup | 86 | 说明随机搜索后细化网格搜索 |
| P046 | S22 | 9/3/[0, 15]; 9/4/[0, 5] | prose | experimental_setup | 260 | 解释各模型搜索参数与默认值处理 |
| P047 | S22 | 9/5/[0, 12] | prose | definition | 173 | 介绍MAPE、RMSE及峰谷能量指标 |
| P048 | S3 | 11/30/[0, 9] | prose | result_description | 124 | 先报告全测试周小时误差分布 |
| P049 | S3 | 12/17/[0, 9] | prose | comparison | 106 | 解释总体误差离散性与模型差异 |
| P050 | S3 | 12/18/[0, 3] | prose | transition | 30 | 转向逐周及不同负荷情境比较 |
| P051 | S3 | 14/1/[0, 15] | prose | comparison | 209 | 解读逐周模型性能和假期峰谷表现 |
| P052 | S3 | 15/5/[0, 12] | prose | mechanism | 161 | 以周末、疫情及星期差异解释误差情境 |
| P053 | S3 | 15/6/[0, 12] | prose | experimental_setup | 151 | 说明各模型不同的特征重要性计算方法 |
| P054 | S3 | 16/8/[0, 10] | prose | mechanism | 143 | 解释滞后、天气和日历重要性差异 |
| P055 | S3 | 16/9/[0, 6] | prose | comparison | 85 | 将输入特征发现联系到既有研究 |
| P056 | S3 | 16/10/[0, 8] | prose | contribution | 102 | 总结长预测跨度、实际基线和实用指标区别 |
| P057 | S4 | 16/12/[0, 6] | prose | contribution | 70 | 总结XGB推荐及训练灵活性与解释性理由 |
| P058 | S4 | 16/13/[0, 5]; 17/1/[0, 2] | prose | contribution | 95 | 列举模型性能、天气作用、长跨度与公开数据贡献 |
| P059 | S4 | 17/2/[0, 10] | prose | implication | 123 | 提出替代现有模型、成本与市场风险等工程推论 |
| P060 | S4L | 17/4/[0, 5] | prose | future_work | 64 | 提出假日样本扩展与专门模型 |
| P061 | S4L | 17/5/[0, 12] | prose | limitation | 150 | 说明自备电特殊用户干扰与用电分解需求 |
| P062 | S4L | 17/6/[0, 6] | prose | limitation | 69 | 承认未比较DL并提出后续比较 |
| P063 | S4L | 17/7/[0, 4] | prose | future_work | 43 | 提出配套天气预测作为必要输入改进 |
| P064 | S4L | 17/8/[0, 7] | prose | limitation | 83 | 解释疫情、电动汽车与分布式光伏引发漂移 |
| P065 | S4L | 17/9/[0, 4] | prose | future_work | 47 | 提出每周更新与champion-challenger机制 |
| P066 | S4L | 17/10/[0, 2]; 18/1/[0, 3] | prose | future_work | 56 | 提出联合风光预测以减少调度不确定性 |

## p_654ca5ab287c1e14

| 段ID | 章节 | 原文页/块/行（行区间左闭右开） | 类型 | 主要作用 | 词数 | 功能概括 |
|---|---|---|---|---|---:|---|
| P001 | S1 | 1/31/[0, 8] | prose | background | 91 | 电力调度需求和预测准确性背景 |
| P002 | S1 | 1/32/[0, 12]; 2/1/[0, 4] | prose | definition | 208 | 预测时间尺度与外生因素复杂性 |
| P003 | S1 | 2/2/[0, 19] | prose | comparison | 222 | 线性统计方法与非线性神经方法对照 |
| P004 | S1 | 2/3/[0, 7] | prose | gap | 78 | 循环网络梯度问题与LSTM补救 |
| P005 | S1 | 2/4/[0, 9] | prose | contribution | 106 | 提出Transformer和相似日选择组合 |
| P006 | S1 | 2/5/[0, 7] | prose | transition | 75 | 说明文章后续章节组织 |
| P007 | S2 | 2/7/[0, 5] | prose | transition | 57 | 用统计与机器学习两类组织文献 |
| P008 | S2 | 3/1/[0, 26] | prose | comparison | 341 | 综合讨论回归预测的应用与优缺点 |
| P009 | S2 | 3/2/[0, 14] | prose | comparison | 165 | 梳理模糊时序和混合模糊模型 |
| P010 | S2 | 3/3/[0, 13]; 4/1/[0, 2] | prose | comparison | 184 | 讨论SVM预测和ARIMA对照 |
| P011 | S2 | 4/2/[0, 24] | prose | comparison | 294 | 讨论ANN、BP和残差网络研究 |
| P012 | S2 | 4/3/[0, 18] | prose | comparison | 228 | 介绍CNN与TCN的时序应用 |
| P013 | S2 | 4/4/[0, 10]; 5/1/[0, 24] | prose | comparison | 438 | 梳理Elman、LSTM、GRU及序列限制 |
| P014 | S2 | 5/2/[0, 15] | prose | comparison | 195 | 说明CNN-RNN混合与seq2seq预测 |
| P015 | S31 | 5/4/[0, 9] | prose | experimental_setup | 125 | 给出AEMO数据期间与训练测试切分 |
| P016 | S31 | 5/5/[0, 3]; 6/1/[0, 3] | prose | result_description | 89 | 描述周负荷均值与工作日差异 |
| P017 | S31 | 6/14/[0, 7] | prose | mechanism | 87 | 解释天气和季节关联的可能原因 |
| P018 | S32 | 6/16/[0, 6] | prose | definition | 82 | 定义多步监督预测输入输出 |
| P019 | S32 | 6/17/[0, 10]; 7/1/[0, 2] | prose | algorithm_explanation | 149 | 说明相似日选择与编解码预测总流程 |
| P020 | S33 | 8/40/[0, 7] | prose | problem | 91 | 讨论外生特征可能干扰与相似日策略 |
| P021 | S33 | 8/41/[0, 7] | prose | algorithm_explanation | 94 | 提出以重要性修正聚类距离 |
| P022 | S331 | 8/43/[0, 13] | prose | algorithm_explanation | 177 | 介绍LightGBM与特征评分口径 |
| P023 | S331 | 9/1/[0, 5] | prose | algorithm_explanation | 67 | 说明叶优先树生长与深度限制 |
| P024 | S331 | 9/2/[0, 10] | prose | result_description | 138 | 给出噪声扰动重要性解释及天气排序 |
| P025 | S332 | 9/11/[0, 11] | prose | definition | 143 | 定义聚类目标、中心和加权距离 |
| P026 | S332 | 10/1/[0, 9] | prose | algorithm_explanation | 123 | 解释伪代码初始化与分配流程 |
| P027 | S332 | 10/12/[0, 3] | prose | contribution | 42 | 总结加权相似日选择的声称收益 |
| P028 | S341 | 11/2/[0, 9] | prose | background | 108 | 从注意力既有研究引出Transformer |
| P029 | S341 | 11/3/[0, 17] | prose | algorithm_explanation | 255 | 类比视觉注意并解释相似度、权重和聚合 |
| P030 | S342 | 11/12/[0, 11] | prose | algorithm_explanation | 154 | 说明六层编解码架构 |
| P031 | S342 | 12/19/[0, 14]; 13/1/[0, 2] | prose | algorithm_explanation | 211 | 说明自注意、多头与残差机制 |
| P032 | S342 | 13/5/[0, 3] | prose | definition | 41 | 定义前馈两层激活与投影 |
| P033 | S342 | 13/6/[0, 12] | prose | algorithm_explanation | 151 | 说明交叉注意力和解码遮蔽 |
| P034 | S342 | 13/21/[0, 7]; 14/1/[0, 5] | prose | algorithm_explanation | 164 | 定义时间协变量位置编码和归一化 |
| P035 | S342 | 14/12/[0, 16] | prose | algorithm_explanation | 198 | 总结预测输出流程及Transformer局限 |
| P036 | S351 | 14/14/[0, 8] | prose | algorithm_explanation | 117 | 解释RNN记忆和输入输出机制 |
| P037 | S352 | 15/2/[0, 10] | prose | algorithm_explanation | 141 | 说明LSTM门控和状态更新 |
| P038 | S352 | 15/7/[0, 7] | prose | definition | 106 | 解释门变量、Sigmoid和候选状态 |
| P039 | S4 | 15/9/[0, 5] | prose | experimental_setup | 55 | 重述实验数据与TensorFlow实现 |
| P040 | S41 | 15/11/[0, 8] | prose | definition | 113 | 定义MAPE/RMSE与误差解释 |
| P041 | S42 | 15/25/[0, 3]; 16/1/[0, 8] | prose | experimental_setup | 167 | 四季周数据扫描k并选择10 |
| P042 | S43 | 16/15/[0, 14] | prose | comparison | 175 | 以一天曲线比较三种相似日组件配置 |
| P043 | S44 | 17/12/[0, 19] | prose | result_description | 254 | 介绍七模型误差和季节样例的表现 |
| P044 | S44 | 18/21/[0, 6] | prose | transition | 62 | 引出模型月度MAPE结果表 |
| P045 | S44 | 19/54/[0, 15]; 20/1/[0, 2] | prose | comparison | 226 | 比较模型误差并给出相对改进和机制解释 |
| P046 | S44 | 20/2/[0, 10] | prose | result_description | 145 | 季节解释并引出Wilcoxon统计检验 |
| P047 | S5 | 20/12/[0, 16] | prose | contribution | 205 | 总结混合方法、平均结果和假期表现 |
| P048 | S5 | 20/13/[0, 8] | prose | limitation | 103 | 承认峰值不足并提出CNN与新特征方向 |

## p_61e82cc0ce8ee029

全文逐段映射缺失；当前未归类提取行：3743。原有10个示例不能作为全篇段落分母。

