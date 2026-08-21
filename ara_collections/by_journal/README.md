# ARA Collection — by Journal

整理日期: 2026-07-13。方法: ARA Universal Compiler（Seal Level 1 校验），对每个对标论文 PDF 做了完整认知抽取——可证伪的机制级 claims、声明式实验计划、逐表逐图的文字转录与页面级 PNG 截图、研究探索轨迹 DAG、跨层绑定（claim↔experiment↔evidence↔trace）。

## 设计目的

把 Energies / Electronics / IEEE Access 三个 MDPI/开放获取期刊中 52 篇对标论文变成"可直接对标的投稿知识库"——你和编辑/审稿人对话时，每篇论文的**真正贡献机制**（不是论文自己的摘要语言）、**成立条件与边界**、以及**源码中的数值瑕疵**都可以在这套 ARA 里溯源。

## 规模概览

| 期刊 | 论文章 | 文件数 | 图表 PNG 数 |
|---|---|---|---|
| Energies | 34 | ~1,600 | ~700 |
| Electronics | 15 | ~650 | 263 |
| IEEE Access | 3 | 178 | 70 |
| **合计** | **52** | **~2,500** | **~1,030** |

全量约 432MB（`.png` 占多数）。

## 提交定位速查

提交稿需要引用"同类在目标期刊的做法"时，在这套 ARA 里找：
- `logic/claims.md` — 同类论文发表的**可证伪机制**与成立边界（不是摘要宣传）：你的论文超越它的可证伪声称
- `logic/solution/constraints.md` — 同类论文的局限与未测试边界：用你的实验填补缺口
- `logic/experiments.md` — 同类论文的实验方案，方向级：你可以在同样基线上跑更好的消融
- `evidence/tables/` + `evidence/figures/` — 同类论文的精确结果数据：确定你的方法达到的数量级

每个目录下都是完整四层结构（PAPER.md → logic/ → src/ → evidence/），按需深入。渐进披露: PAPER.md 约 200 tokens 做第一眼过滤。
