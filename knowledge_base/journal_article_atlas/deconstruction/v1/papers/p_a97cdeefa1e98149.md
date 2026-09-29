# Deep Learning Based Electric Pylon Detection in Remote Sensing Images

p_a97cdeefa1e98149；DOI 10.3390/rs12111857；Remote Sensing 2020,12,1857。

29 物理页含参考全文读完；16 图、13 表、3 编号式视觉检查。单助手临时解构，待独立复核，未人工校准；31 个正文层级标题、6 一级章、53 引文。未完成逐段计数及全部211字段。

## 来源

[原件](../sources/10.3390_rs12111857.pdf)，SHA256 a97cdeefa1e9814993a5dd6fec4622befc7cbf34c698a6697dbd5a64bba7354a。出版社v2 PDF经gold OA验证、aria2获取；CDN时间与API版本1592105105一致，未完整核实最新版本/更正链。

## 实质设计

这是十个既有检测器的杆塔检测比较研究，不是新网络论文。1500张1m/pixel图：Pleiades广东惠茂线720张，GoogleEarth780张。50张159塔有意选为复杂测试集EPD-C；余1450张EPD-S（>3000塔）每次8:1:1划分，验证AP选模型，10次重复报告均值±SD。复杂集只测试，不参与训练。还比较混合1–2m训练与2/4m降采样测试。

注意：重复随机图像划分并不等于十个独立地区；未写按线路/地理group分离。EPD-S上kmeans anchors是否限定每轮训练子集未说明。降采样只能模拟分辨率退化，不代表真实新传感器泛化。十模型训练预算与增强不一致，不能将比较当架构受控消融。

## 章节树与逻辑

- 1 Introduction（p.1–2）：巡检效率和卫星大范围观测动机→提出十检测器比较，不是新模型。
- 2 Related Work（p.2–4）：检测家族与塔线感知文献→光学卫星杆塔比较缺口。
- 2.1 Object Detection Based on Deep Learning（p.2–3）：两阶段/单阶段、有锚/无锚分类，明确比较轴。
- 2.2 Electric Pylon Detection（p.3–4）：SAR、视频、LiDAR与学习方法→光学任务未充分比较；此处仍称nine与实际10不符。
- 3 Electric Pylon Detection Based on Deep Learning（p.4–16）：EPD样本→统一/差异化实现→可重复测试条件。
- 3.1 EPD Dataset（p.4–6）：1500混源图分1450普通与50难例，给出选择标准与背景/目标数量。
- 3.2 Deep Learning Detectors for Comparison（p.6–15）：10个现成检测器覆盖架构轴；详述差异而非声称原创十模型。
- 3.2.1 Backbone Network（p.7–7）：ResNet101+FPN多尺度P2–P6，YOLO另用Darknet系列。
- 3.2.2 Faster R-CNN（p.7–9）：RPN/ROIAlign/分类回归/NMS，建立参照实现。
- 3.2.3 Cascade R-CNN（p.9–9）：三阶段IoU.35/.45/.55适配小塔目标；权重.25/1/.5。
- 3.2.4 Grid R-CNN（p.9–10）：GridPlus定位head/GN，14×14特征带来计算开销。
- 3.2.5 Libra R-CNN（p.10–11）：IoU平衡采样、平衡金字塔、balancedL1，原组件三类不平衡。
- 3.2.6 Retinanet（p.11–12）：P3–P7，focalγ2α.25与smoothL1，稀疏前景处理。
- 3.2.7 YOLOv3（p.12–12）：Darknet53+多尺度输出，EPD-S kmeans九anchor及focalγ.8α1。
- 3.2.8 YOLOv4（p.13–13）：CSPDarknet+SPP+PAN+tricks，九anchor与v3相同，random=0。
- 3.2.9 Retinanet FreeAnchor（p.13–14）：用原作MLE匹配替代手设anchor分配，候选袋选择。
- 3.2.10 FCOS（p.14–15）：无锚四偏移+centerness，focal/IoU/CE三损失等权。
- 3.2.11 Retinanet FSAF（p.15–15）：有锚/无锚分支及在线尺度选择，继承原作模块。
- 3.3 Training Details（p.15–16）：实现来源、预训练冻结与各模型调参设置。
- 3.3.1 Detector Implementation（p.15–16）：MMDetection/Ultralytics/Darknet来源；ResNet冻结C1/C2而YOLO不冻。
- 3.3.2 Details of Detector Training（p.16–16）：增强、优化器、epoch/stepLR/warmup；不同算力/参数预算而非严格匹配。
- 4 Experimental Results（p.17–24）：重复划分主比较→复杂难例→分辨率降采样→可视误检解释。
- 4.1 Experimental Settings（p.17–17）：EPD-S随机8:1:1，验证AP选模型，再测试；各10次，EPD-C仅测试。
- 4.2 Index for Evaluation（p.17–17）：IoU>.5、P/R、PR面积AP；同GPU速度/模型大小。
- 4.3 Performance of Detectors（p.18–20）：固定1m与混合1–2m两训练条件、S/C两测试层比较；混合最佳AP文字/粗体有误。
- 4.4 Robustness against Spatial Resolution（p.20–24）：将C降到2m/4m，评训练分辨率适配；同源重采样不是新传感器外测。
- 5 Discussion（p.24–26）：按性能/资源/分辨率给选型；机制解释未受控消融验证。
- 5.1 Analysis of Performance（p.24–25）：无统一最优模型→按AP、recall、速度、大小选择；勿将相关架构差异当因果。
- 5.2 Analysis of Resolution Robustness（p.25–25）：跨10模型均值概括1m→2m→4m退化；Table13一格均值不符。
- 5.3 Application Prospects（p.25–26）：遥感可得性与电力管理前景，未测端到端巡检业务效用。
- 6 Conclusions（p.26–26）：任务条件化选型与无全局最优；末尾FCOS混合分辨率优越说法需限定到1m训练/4m测试。

## 公式、框架与图

(1) IoU、(2) precision、(3) recall均在p.17，均为标准评价定义。AP仅以PR面积文字解释，无新增编号公式/证明。

输入为光学塔图和框标注；ResNet101+FPN等预训练/微调→十种检测head→框/置信度→AP/召回/速度/大小。原组件具体参数与训练超参数见JSON，不把十个算法名计算成十项创新。

- Figure 1 p.3，two/one-stage比较：RPN有无与dense采样示意；不是新架构
- Figure 2 p.4，样本：Pleiades两张+GoogleEarth两张，显示尺度和背景差异
- Figure 3 p.6，难例样本：2图说明颜色相近和框架建筑干扰
- Figure 4 p.7，ResNet101 FPN：底向上C层、顶向下P层及256输出channel
- Figure 5 p.8，Faster R-CNN：RPN→ROIAlign→分类回归
- Figure 6 p.9，Cascade R-CNN：3阈值级联逐步精化
- Figure 7 p.10，Grid R-CNN：ROIAlign14×14和grid特征融合
- Figure 8 p.11，Libra R-CNN：平衡特征/采样/loss；caption误称balancedL1分类而正文用于回归
- Figure 9 p.11，Retinanet：分类18/回归36通道，focal稀疏前景处理
- Figure 10 p.12，YOLOv3：三尺度Darknet输出
- Figure 11 p.13，YOLOv4：CSP/SPP/PAN聚合路径
- Figure 12 p.14，FreeAnchor：候选anchor bags学习匹配
- Figure 13 p.14，FCOS：无锚偏移、类别、centerness
- Figure 14 p.15，FSAF：在线层选择与有锚/无锚双分支
- Figure 15 p.22，结果矩阵：5模型×2场景×2分辨率=20图像单元；误检岛屿与低分辨率漏检
- Figure 16 p.23，结果矩阵续：另5模型20单元；虽caption continued但独立编号16，算独立图；FCOS密集塔漏检

## 逐表与数量审计

- Table 1 p.5：EPD-C来源/背景分层，20张Pleiades38塔+30张GoogleEarth121塔=50张159塔；图像数与目标数不可混。
- Table 2 p.6：十检测器backbone/category：4两阶段6单阶段；8纯有锚1无锚1混合。
- Table 3 p.16：逐模型lr/epoch/step/warmup/batch；epochs20–40而调参预算未给，Retinanet引文误为39。
- Table 4 p.18：EPD-S固定1m：FreeAnchor AP.893±.007最高，FSAF R.944±.011最高，YOLOv4 16.21±.24img/s最快。
- Table 5 p.18：EPD-C固定1m：Retinanet AP.695±.018、Libra R.771±.011。FSAF R SD.169/AP SD.084明显大于他法，原件如此不可改小。
- Table 6 p.19：混合1–2m分辨率分布：S[23.7,12.4,8.1,4.4,3.2,48.2]%，C[32,2,12,8,6,40]%，均合100%；仅原图降采样。
- Table 7 p.19：EPD-S混合：YOLOv4 AP.879±.018实际最高，FSAF.861±.032；粗体和正文错称FSAF最佳；v3召回.921最佳。
- Table 8 p.19：EPD-C混合：YOLOv4 R.743±.015/AP.648±.010最佳；速度FSAF16.42>v4 16.21，否定v4 always最快。
- Table 9 p.20：1m训练2m测试C：Retinanet AP.652±.033最佳，FCOS R.743±.021。
- Table 10 p.20：1m训练4m测试C：FCOS AP.449±.026/R.603±.023最佳；v3 AP.240±.038弱。
- Table 11 p.21：混合训练2m测试C：v4 AP.611±.019/R.688±.014最佳。
- Table 12 p.21：混合训练4m测试C：Libra AP.472±.020最佳，v3 R.590±.015最高（FCOS.585）。
- Table 13 p.25：10模型等权均值而非独立新实验；1m训练4m测试AP印.376，但Table10十项平均.3711→.371，差异超过舍入；其余5行均值核对通过。

Table 13以10模型等权重汇总EPD-C，不是新增实验。除1m训练→4m测试AP印.376而按Table10均值为.3711外，其余行核算到3位小数相符。Table7实际最佳AP是YOLOv4 .879而非正文/粗体FSAF .861。Table5 FSAF异常大的SD照录，不擅自“修正”。

## 结论与叙事边界

可以支持条件化选型：没有一个检测器同时最优，复杂背景和低分辨率造成明显退化。不能支持电气健康诊断、电网可靠性改善或跨区域普适最佳。图15/16将Libra误检、FCOS密集目标漏检归因单一模块属于解释猜测，未有消融。存储列“M”不等于实测峰值显存；所谓实时仅GPU吞吐，不含遥感获取/传输延时。

- Across [models], no single detector optimized [accuracy, speed, storage] under every [resolution regime].
- When [sensor resolution] changed from [a] to [b], [metric] declined under [fixed training protocol].
- The observed failure is consistent with [mechanism], but a matched component experiment is needed to isolate it.

## 六维临时难度

- theory: 1/4 [1–1]；标准IoU/P/R与继承方法，无新增证明
- algorithm: 2/4 [1–2]；十模型适配复现实验但不等于十个创新
- statistics: 2/4 [1–2]；10次重新划分/训练均值SD，依赖/配对未处理
- data: 2/4 [2–3]；混源真实卫星1500图及难例整理，缺地理独立外测
- engineering: 1/4 [1–2]；离线GPU基准，无现场电力系统闭环
- cross_discipline: 2/4 [1–2]；遥感分辨率/杆塔特性显式进入检测评测，无电气状态方程

仅DESIGN研究内锚点，不是录用概率/质量总分。源码、数据未重跑，链接只记录论文声明；逐段边界、词频、全部表格每格数字结构化、独立复核和人工校准未完成。

