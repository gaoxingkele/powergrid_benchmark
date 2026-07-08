# Public Dataset Pool Logic

## Core Idea

公共数据集池是整个项目的实验地基。没有稳定数据集和任务分类，论文 idea 很容易变成无法复现的孤立实现。

## Dataset Logic

数据源按能力分为：

- grid cases: MATPOWER, pandapower, PGLib-OPF, TAMU
- operation simulation: RTS-GMLC, SimBench, Grid2Op
- time series/market/weather: OPSD, EIA, ENTSO-E, PJM, NSRDB
- equipment/PMU/fault: DGA, PMU Event Library, GridSTAGE
- reliability report text: C2GES NERC reports

## Method Logic

数据源不是越多越好，而是要进入同一张任务矩阵：

```text
Dataset -> Task -> Baseline -> Metric -> Evidence
```

## Key Insight

不同数据源有不同可用层级：

- downloaded: 可直接实验或可进一步处理。
- metadata-only: 有入口但需要 API/token/子集策略。
- source-only: 原始文档可用，但标签层需要重建。

C2GES NERC reports 属于 source-only source layer downloaded。

## Reusable Value

这个池子让后续论文选题可以快速回答：

- 用什么数据？
- 做什么任务？
- 和谁比？
- 指标是什么？
- 缺什么证据？
