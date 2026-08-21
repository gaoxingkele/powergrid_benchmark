"""Promotion-gate audit final assembly: PROMOTION_GATE_AUDIT.json + PROMOTION_GATE_AUDIT.md."""
import json
from pathlib import Path

P = Path(r"D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\public_baseline_protocol")
OUT = P / "formal_runs" / "promotion_gate_20260807"

partA = json.loads((OUT / "_partA_results.json").read_text(encoding="utf-8"))
reexec = json.loads((OUT / "_reexecution_summary.json").read_text(encoding="utf-8"))
stats = json.loads((OUT / "_stats.json").read_text(encoding="utf-8"))

checks = dict(partA["checks"])
checks["B_reexecution_rows_4000"] = reexec["counts"]["rows"] == 4000
checks["B_gold_all_500_safe_executed"] = (
    reexec["gold_cache_size"] == 500 and reexec["counts"]["gold_not_safe"] == 0
    and reexec["gold_status_hist"] == {"SAFE_EXECUTED": 500}
)
checks["B_prediction_status_all_match"] = reexec["counts"]["status_mismatch"] == 0
checks["B_official_ex_all_match"] = reexec["counts"]["ex_mismatch"] == 0

n_pass = sum(1 for v in checks.values() if v)
all_pass = n_pass == len(checks)
verdict = "PROMOTE" if all_pass else "NOT-PROMOTE"

audit_json = {
    "audit_id": "promotion_gate_20260807",
    "protocol_id": "MA-PUBLIC-BIRD-MINIDEV-v1.0",
    "freeze_sha256": "c77699593d7752ffc2c5c0fa0e58ef4f48db1a05f2a827ff4dde1cb8c936a05b",
    "auditor": "delegated independent technical agent (promotion-gate audit, read-only re-execution)",
    "date": "2026-08-07",
    "environment": {
        "reexecution_python": reexec["python_version"],
        "reexecution_sqlite": reexec["sqlite_version"],
        "evaluator_ex_sha256": partA["details"]["evaluator_ex_sha256_matches"],
        "statistics_python": "3.12.10 (hash/statistics only; no SQL execution)",
        "bootstrap": {"cluster": "db_id", "n_clusters": 11, "resamples": stats["n_boot"], "seed": stats["seed"]},
    },
    "checks": checks,
    "n_checks": len(checks),
    "n_pass": n_pass,
    "partA_discrepancies": partA["discrepancies"],
    "reexecution": {
        "counts": reexec["counts"],
        "gold_status_hist": reexec["gold_status_hist"],
        "mismatches": reexec["mismatches"],
        "wall_seconds": reexec["wall_seconds"],
        "reexec_overrides_used_in_stats": stats["n_reexec_overrides_used"],
    },
    "legacy_artifacts": partA["details"]["legacy_attempt_dirs"],
    "statistics": {
        "ex_by_method": stats["ex_by_method"],
        "pairwise_holm": stats["pairwise"],
        "by_database_csv": "stats_by_database.csv",
    },
    "verdict": verdict,
}
(OUT / "PROMOTION_GATE_AUDIT.json").write_text(
    json.dumps(audit_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pct(x):
    return f"{x * 100:.2f}"


lines = []
lines.append("# MA-PUBLIC-BIRD-MINIDEV-v1.0（v1.0.1）晋级门禁独立审计报告")
lines.append("")
lines.append("- 审计日期：2026-08-07")
lines.append("- 冻结 SHA-256：`c77699593d7752ffc2c5c0fa0e58ef4f48db1a05f2a827ff4dde1cb8c936a05b`")
lines.append("- 复执行环境：Python " + reexec["python_version"].split()[0] +
            f" / SQLite {reexec['sqlite_version']}（钉住运行时 runtime_compat/python31011）")
lines.append(f"- 检查项：{n_pass}/{len(checks)} 通过")
lines.append(f"- **门禁结论：{verdict}**")
lines.append("")
lines.append("## A. 完整性核验")
lines.append("")
failed = [k for k, v in checks.items() if not v]
lines.append(f"全部 {len(checks)} 项程序化检查（manifest 字段与哈希绑定、模型文件 SHA-256、"
             "call_ledger 序号/重试/调用顺序一致性、提示词重渲染哈希绑定（含 B3 call2 动态替换重建）、"
             "final_scores 覆盖与全尝试分母、人类批准绑定、冻结输入哈希、11 库哈希、"
             "遗留 attempt 目录分离）："
             + ("全部通过。" if not failed else f"失败项：{failed}"))
lines.append("")
lines.append("B3_EXEC_REPAIR call=2 的动态替换按 `run_formal_public_baseline.py:102-105` 原样复现："
             "`{{FIRST_CANDIDATE_RUNTIME_MAX_400_TOKENS}}` ← 同题 call1 账本的完整 `extracted_sql`"
             "（占位符名含“400_TOKENS”但代码不做截断，本审计按代码语义执行）；"
             "`{{ONE_OF_FROZEN_FEEDBACK_VOCABULARY}}` ← call1 账本的 `validator_feedback`。"
             "两模型各 2500 条提示词哈希全部匹配。")
lines.append("")
lines.append("遗留产物（均与 v101 正式目录完全分离，不属于本次审计计分范围）：")
for d in partA["details"]["legacy_attempt_dirs"]:
    if d["dir"].startswith("MA_PUBLIC"):
        lines.append(f"- `{d['dir']}`：manifest={d['has_run_manifest']}，"
                     f"绑定 freeze={d['manifest_freeze_sha256'] or '（无 RUN_MANIFEST）'}")
lines.append("")
lines.append("## B. 独立复执行（钉住运行时，只读沙箱，timeout 180s）")
lines.append("")
c = reexec["counts"]
lines.append(f"- 复执行行数：{c['rows']}/4000；gold 缓存 500 条，全部 SAFE_EXECUTED："
             f"{'是' if checks['B_gold_all_500_safe_executed'] else '否'}")
lines.append(f"- prediction_status 不一致：{c['status_mismatch']}；official_ex 不一致：{c['ex_mismatch']}")
lines.append(f"- 复执行 prediction_status 分布：{json.dumps(c['pred_status_hist'], ensure_ascii=False)}")
lines.append(f"- 复执行总耗时：{reexec['wall_seconds']:.1f} s")
if reexec["mismatches"]:
    lines.append("")
    lines.append("### 不一致明细")
    lines.append("")
    lines.append("| model | question_id | db | method | 账本 status | 复执行 status | 账本 EX | 复执行 EX |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for m in reexec["mismatches"]:
        lines.append(f"| {m['model']} | {m['question_id']} | {m['db_id']} | {m['method']} | "
                     f"{m['ledger_status']} | {m['reexec_status']} | {m['ledger_ex']} | {m['reexec_ex']} |")
else:
    lines.append("- 不一致明细：无（4000/4000 逐行一致）。")
lines.append("")
lines.append("## C. 统计表（数据库聚类 bootstrap，11 簇，10000 次重抽样，种子 20260807）")
lines.append("")
if stats["n_reexec_overrides_used"]:
    lines.append(f"注意：复执行与账本存在 {stats['n_reexec_overrides_used']} 处不一致，统计采用复执行值。")
else:
    lines.append("复执行与账本 4000/4000 一致，统计值与账本值相同。")
lines.append("")
lines.append("### C1. 每模型 × 方法 EX（%，分母 500，全尝试分母）")
lines.append("")
lines.append("| model | method | EX% | 95% CI |")
lines.append("|---|---|---|---|")
for r in stats["ex_by_method"]:
    lines.append(f"| {r['model']} | {r['method']} | {pct(r['ex_mean'])} | "
                 f"[{pct(r['ci95_low'])}, {pct(r['ci95_high'])}] |")
lines.append("")
lines.append("### C2/C3. 配对差值 + Holm 校正（百分点）")
lines.append("")
lines.append("| scope | 对比 | 差值 | 95% CI | p_raw | p_holm |")
lines.append("|---|---|---|---|---|---|")
for r in stats["pairwise"]:
    lines.append(f"| {r['scope']} | {r['comparison']} | {pct(r['diff'])} | "
                 f"[{pct(r['ci95_low'])}, {pct(r['ci95_high'])}] | {r['p_raw']:.4f} | {r['p_holm']:.4f} |")
lines.append("")
lines.append("### C4. 按数据库 EX 明细")
lines.append("")
lines.append("见 `stats_by_database.csv`（88 行 = 2 模型 × 11 库 × 4 方法）。")
lines.append("")
lines.append("## 门禁结论")
lines.append("")
if verdict == "PROMOTE":
    lines.append(f"**PROMOTE**。{len(checks)}/{len(checks)} 项检查全部通过：完整性核验（含提示词哈希绑定、"
                 "人类批准绑定、遗留 attempt 分离）全部通过；4000 条最终预测与 500 条 gold 在钉住运行时"
                 "（Python 3.10.11 / SQLite 3.40.1）下独立复执行，prediction_status 与 official_ex "
                 "逐行 100% 一致；统计表由复执行分数重新生成（与账本值相同）。")
else:
    lines.append(f"**NOT-PROMOTE**。失败检查项：{failed}。详见 PROMOTION_GATE_AUDIT.json。")
lines.append("")
(OUT / "PROMOTION_GATE_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"verdict": verdict, "n_checks": len(checks), "n_pass": n_pass,
                  "failed": failed}))
