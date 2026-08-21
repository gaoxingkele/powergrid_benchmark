#!/usr/bin/env python3
"""Independent evidence audit and publication assets for MA-SQLGrid E1/E2/E4.

This script reads, but never changes, the prospectively frozen ledgers and formal
runs.  Statistical routines are implemented locally rather than imported from
the registered aggregator so the release is an independent recomputation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
MA = HERE.parent
SRC = MA / "prospective_component_experiments"
ROWS = MA / "canonical_v2_reanalysis" / "canonical_rows_v2.jsonl"
MODELS = ("qwen", "granite")
V0, V1 = "V0_NoValueEvidence", "V1_WithValueEvidence"
BASE_SEED = 20260805
BOOT_N, RAND_N = 20_000, 100_000


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def sha(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def dump_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def grouped(values):
    out = defaultdict(list)
    for qid, cluster, value in values:
        out[cluster].append(float(value))
    keys = sorted(out)
    sums = np.array([sum(out[k]) for k in keys], float)
    counts = np.array([len(out[k]) for k in keys], float)
    return sums, counts


def bootstrap(values, seed):
    sums, counts = grouped(values)
    rng = np.random.default_rng(seed)
    draws = np.empty(BOOT_N)
    for start in range(0, BOOT_N, 2000):
        stop = min(start + 2000, BOOT_N)
        ix = rng.integers(0, len(sums), size=(stop - start, len(sums)))
        draws[start:stop] = sums[ix].sum(1) / counts[ix].sum(1)
    lo, hi = np.quantile(draws, [0.025, 0.975], method="linear")
    return float(sums.sum() / counts.sum()), float(lo), float(hi)


def randomization(values, seed):
    sums, counts = grouped(values)
    observed = float(sums.sum() / counts.sum())
    threshold, extreme = abs(observed) - 1e-15, 0
    rng = np.random.default_rng(seed)
    for start in range(0, RAND_N, 5000):
        n = min(5000, RAND_N - start)
        signs = rng.integers(0, 2, size=(n, len(sums)), dtype=np.int8) * 2 - 1
        stats = (signs * sums).sum(1) / counts.sum()
        extreme += int(np.count_nonzero(np.abs(stats) >= threshold))
    return (extreme + 1) / (RAND_N + 1), extreme


def effect(values, bseed, rseed):
    est, lo, hi = bootstrap(values, bseed)
    p, extreme = randomization(values, rseed)
    return {"questions": len(values), "clusters": len({x[1] for x in values}), "estimate": est,
            "ci_low": lo, "ci_high": hi, "p_value": p, "extreme_draws": extreme,
            "bootstrap_samples": BOOT_N, "randomization_samples": RAND_N,
            "bootstrap_seed": bseed, "randomization_seed": rseed}


def holm(rows):
    order = sorted(range(len(rows)), key=lambda i: rows[i]["p_value"])
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(rows) - rank) * rows[i]["p_value"]))
        rows[i]["holm_adjusted_p"] = running


def label(row, modifier=False):
    if row["estimate"] > 0 and row["ci_low"] > 0 and row["holm_adjusted_p"] < .05:
        return "positive_granite_minus_qwen_modifier" if modifier else "positive_component_efficacy"
    if row["estimate"] < 0 and row["ci_high"] < 0 and row["holm_adjusted_p"] < .05:
        return "negative_granite_minus_qwen_modifier" if modifier else "significant_harm"
    return "no_detectable_backbone_modifier" if modifier else "no_detectable_improvement"


def paired_metric(rows, clusters, getter):
    by = {(r["question_id"], r["condition"]): r for r in rows}
    qids = sorted({q for q, c in by if c == V0} & {q for q, c in by if c == V1})
    return [(q, clusters[q], getter(by[(q, V1)]) - getter(by[(q, V0)])) for q in qids]


def ratio_ci(values, seed):
    transformed = [(q, c, math.log((b + 1) / (a + 1))) for q, c, a, b in values]
    est, lo, hi = bootstrap(transformed, seed)
    return math.exp(est), math.exp(lo), math.exp(hi)


FORBIDDEN_SQL = re.compile(r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|replace\s+into)\b", re.I)


def split_statements(sql):
    sql = re.sub(r"--.*?$", "", sql, flags=re.M)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.S).strip()
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", sql, flags=re.I | re.S)
    if fenced: sql = fenced.group(1).strip()
    out, buf, quote, i = [], [], None, 0
    while i < len(sql):
        ch = sql[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                if i + 1 < len(sql) and sql[i + 1] == quote:
                    buf.append(sql[i + 1]); i += 1
                else: quote = None
        elif ch in ("'", '"'): quote = ch; buf.append(ch)
        elif ch == ";":
            if "".join(buf).strip(): out.append("".join(buf).strip())
            buf = []
        else: buf.append(ch)
        i += 1
    if "".join(buf).strip(): out.append("".join(buf).strip())
    return out


def execute_read_only(conn, sql):
    if not sql: return None
    statements = split_statements(sql)
    if len(statements) != 1: return None
    statement = statements[0]
    if not re.match(r"^(select|with)\b", statement, re.I) or FORBIDDEN_SQL.search(statement): return None
    try:
        cur = conn.execute(statement)
        return ([d[0] for d in (cur.description or [])], [tuple(x) for x in cur.fetchall()])
    except sqlite3.Error:
        return None


def normalized_rows(rows):
    def value(x):
        if x is None: return ("__NULL__",)
        if isinstance(x, float):
            if math.isnan(x): return ("__NAN__",)
            return round(x / 1e-6) * 1e-6
        return x
    return [tuple(value(x) for x in row) for row in rows]


def independent_equal(conn, record, sql):
    gold, pred = execute_read_only(conn, record["gold_sql"]), execute_read_only(conn, sql)
    if gold is None or pred is None: return False
    if len(gold[0]) != record["answer_shape"]["column_count"] or len(pred[0]) != record["answer_shape"]["column_count"]: return False
    g, p = normalized_rows(gold[1]), normalized_rows(pred[1])
    return p == g if record["order_sensitive"] else Counter(p) == Counter(g)


def write_csv(name, rows, fields):
    with (HERE / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def esc(s):
    return str(s).replace("_", "\\_").replace("%", "\\%")


def savefig(fig, stem):
    for ext in ("svg", "pdf"):
        fig.savefig(HERE / f"{stem}.{ext}", bbox_inches="tight")
    fig.savefig(HERE / f"{stem}.png", dpi=450, bbox_inches="tight")
    plt.close(fig)


def main():
    freeze = read_json(SRC / "PROTOCOL_FREEZE.json")
    clusters = {r["question_id"]: r["template_cluster"] for r in read_jsonl(ROWS)}
    assert len(clusters) == 180 and len(set(clusters.values())) == 70
    frozen = read_jsonl(SRC / "frozen_prompts.jsonl")
    frozen_by = {(r["question_id"], r["condition"]): r for r in frozen}
    assert len(frozen) == 360 and sha(SRC / "frozen_prompts.jsonl") == freeze["prompt_ledger_sha256"]

    data = MA.parent.parent / "2026_ma_sqlgrid_cmc" / "source" / "data" / "griddb_maintenance_v2_v0_1"
    question_path, db_path = data / "questions.jsonl", data / "database.sqlite"
    frozen_inputs = freeze["input_hashes"]
    qkey = next(k for k in frozen_inputs if k.endswith("questions.jsonl"))
    dbkey = next(k for k in frozen_inputs if k.endswith("database.sqlite"))
    assert sha(question_path) == frozen_inputs[qkey]["sha256"] and sha(db_path) == frozen_inputs[dbkey]["sha256"]
    records = {r["question_id"]: r for r in read_jsonl(question_path)}

    audit_models, model_data = {}, {}
    forbidden = {"gold", "gold_sql", "gold_result", "reference_sql", "candidate_correctness_gold_only"}
    for model in MODELS:
        run = SRC / "runs" / model
        pred = read_jsonl(run / "predictions.jsonl")
        sel = read_jsonl(run / "candidate_selections.jsonl")
        scored = read_jsonl(run / "scored_rows.jsonl")
        rm, seal, sm = (read_json(run / x) for x in ("RUN_MANIFEST.json", "SELECTION_SEAL.json", "SCORING_MANIFEST.json"))
        order = read_jsonl(SRC / f"call_order_{model}.jsonl")
        expected = [(r["question_id"], r["condition"]) for r in order]
        pred_keys = [(r["question_id"], r["condition"]) for r in pred]
        sel_keys = [(r["question_id"], r["condition"]) for r in sel]
        score_keys = [(r["question_id"], r["condition"]) for r in scored]
        assert len(pred) == len(sel) == len(scored) == len(expected) == 350
        assert len(set(expected)) == 350 and set(pred_keys) == set(sel_keys) == set(score_keys) == set(expected)
        assert all(r["status"] == "success" and r["retry_count"] == 0 for r in pred)
        assert all(r["model_sha256"] == freeze["models"][model]["model_sha256"] for r in pred)
        assert all(r["served_model_id"] == freeze["models"][model]["served_model_id"] for r in pred)
        assert all(r["prompt_sha256"] == frozen_by[(r["question_id"], r["condition"])]["prompt_sha256"] for r in pred)
        assert not any(forbidden & set(r) for r in pred + sel)
        assert rm["freeze_sha256"] == sha(SRC / "PROTOCOL_FREEZE.json")
        assert rm["prediction_ledger_sha256"] == sha(run / "predictions.jsonl")
        assert seal["selection_ledger_sha256"] == sha(run / "candidate_selections.jsonl")
        assert sm["scored_rows_sha256"] == sha(run / "scored_rows.jsonl")
        assert sm["selection_ledger_sha256"] == seal["selection_ledger_sha256"]
        assert seal["gold_loaded"] is False and sm["gold_loaded_only_after_selection_seal"] is True
        cond = Counter(r["condition"] for r in pred)
        assert cond == Counter({V1: 180, V0: 170})
        scored_by = {(r["question_id"], r["condition"]): r for r in scored}
        rescored_candidates, rescored_rows = 0, 0
        with sqlite3.connect(db_path) as conn:
            for row in sel:
                key = (row["question_id"], row["condition"])
                truth = scored_by[key]
                candidate_equal = [independent_equal(conn, records[row["question_id"]], sql) for sql in row["candidates"]]
                first_equal = independent_equal(conn, records[row["question_id"]], row["first_candidate_sql"])
                selected_equal = independent_equal(conn, records[row["question_id"]], row["selected_sql"])
                assert candidate_equal == truth["candidate_correctness_gold_only"]
                assert first_equal == truth["first_correct"]
                assert selected_equal == truth["validator_selected_correct"]
                assert any(candidate_equal) == truth["oracle_at_3_correct_diagnostic_only"]
                rescored_candidates += len(candidate_equal); rescored_rows += 1
        audit_models[model] = {
            "formal_rows": 350, "condition_rows": dict(cond), "success_rows": 350,
            "zero_retry_rows": 350, "unique_call_keys": 350, "model_identity_match": True,
            "prompt_hash_match_rows": 350, "prediction_and_selection_gold_field_absence": True,
            "selection_sealed_before_gold_statement": True, "scoring_tied_to_selection_hash": True,
            "independent_sqlite_rescored_rows": rescored_rows,
            "independent_sqlite_rescored_candidates": rescored_candidates,
            "independent_scoring_mismatches": 0,
            "source_hashes": {n: sha(run / n) for n in ("predictions.jsonl", "RUN_MANIFEST.json",
                "candidate_selections.jsonl", "SELECTION_SEAL.json", "scored_rows.jsonl", "SCORING_MANIFEST.json")}}
        model_data[model] = {"pred": pred, "sel": sel, "scored": scored}

    # Frozen intervention and eligibility reconstruction.
    pairs = defaultdict(dict)
    for r in frozen: pairs[r["question_id"]][r["condition"]] = r
    eligible = sorted(q for q, x in pairs.items() if V0 in x and V1 in x and x[V0]["context_sha256"] != x[V1]["context_sha256"])
    assert len(eligible) == 170 and len({clusters[q] for q in eligible}) == 61
    eligible_hash = hashlib.sha256(json.dumps(eligible, ensure_ascii=False, sort_keys=True,
                                               separators=(",", ":")).encode("utf-8")).hexdigest()
    assert eligible_hash == freeze["eligible_question_ids_sha256"]
    invariance = all(pairs[q][V0][k] == pairs[q][V1][k] for q in eligible for k in
                     ("question", "selected_tables_sha256", "selected_columns_sha256", "inferred_shape_sha256"))
    assert invariance

    effects = {"E1": [], "E2": [], "cross_backbone": []}
    raw_values = {"E1": {}, "E2": {}}
    for mi, model in enumerate(MODELS, start=1):
        score = {(r["question_id"], r["condition"]): r for r in model_data[model]["scored"]}
        e1v = [(q, clusters[q], int(score[(q, V1)]["first_correct"]) - int(score[(q, V0)]["first_correct"])) for q in eligible]
        e2v = [(q, clusters[q], int(score[(q, V1)]["validator_selected_correct"]) - int(score[(q, V1)]["first_correct"])) for q in sorted(clusters)]
        raw_values["E1"][model], raw_values["E2"][model] = e1v, e2v
        e1 = effect(e1v, BASE_SEED + 1100 + mi, BASE_SEED + 1200 + mi)
        e1.update(family="E1", model=model, contrast="V1_minus_V0_first_candidate_frozen_state_execution_equality")
        e2 = effect(e2v, BASE_SEED + 2100 + mi, BASE_SEED + 2200 + mi)
        e2.update(family="E2", model=model, contrast="validator_minus_first_V1_frozen_state_execution_equality")
        effects["E1"].append(e1); effects["E2"].append(e2)
    for fam in ("E1", "E2"):
        holm(effects[fam])
        for r in effects[fam]: r["claim_label"] = label(r)
    for fi, fam in enumerate(("E1", "E2"), start=1):
        q = {x[0] for x in raw_values[fam]["qwen"]}
        qv = {x[0]: x for x in raw_values[fam]["qwen"]}; gv = {x[0]: x for x in raw_values[fam]["granite"]}
        vals = [(x, qv[x][1], gv[x][2] - qv[x][2]) for x in sorted(q)]
        row = effect(vals, BASE_SEED + 3100 + fi, BASE_SEED + 3200 + fi)
        row.update(family="cross_backbone", component=fam, model="", contrast="Granite_effect_minus_Qwen_effect")
        effects["cross_backbone"].append(row)
    holm(effects["cross_backbone"])
    for r in effects["cross_backbone"]: r["claim_label"] = label(r, True)

    # Candidate selection descriptives and E4 diagnostic metrics.
    descriptives, efficiency = [], []
    for mi, model in enumerate(MODELS, start=1):
        score = {(r["question_id"], r["condition"]): r for r in model_data[model]["scored"]}
        sel = {(r["question_id"], r["condition"]): r for r in model_data[model]["sel"]}
        v1 = [score[(q, V1)] for q in sorted(clusters)]
        selection_changes = sum(sel[(q, V1)]["selected_candidate_index"] != 0 for q in clusters)
        rescue = sum((not r["first_correct"]) and r["validator_selected_correct"] for r in v1)
        harm = sum(r["first_correct"] and (not r["validator_selected_correct"]) for r in v1)
        descriptives.append({"model": model, "questions": 180,
            "first_execution_equal_count": sum(r["first_correct"] for r in v1),
            "validator_execution_equal_count": sum(r["validator_selected_correct"] for r in v1),
            "first_execution_equality_rate": sum(r["first_correct"] for r in v1) / 180,
            "validator_execution_equality_rate": sum(r["validator_selected_correct"] for r in v1) / 180,
            "selection_changes": selection_changes, "rescues": rescue, "harms": harm,
            "oracle_at_3_diagnostic": sum(r["oracle_at_3_correct_diagnostic_only"] for r in v1) / 180})
        pred = model_data[model]["pred"]
        by = {(r["question_id"], r["condition"]): r for r in pred}
        paired_latency = [(q, clusters[q], by[(q,V0)]["latency_ms"], by[(q,V1)]["latency_ms"]) for q in eligible]
        ratio, rlo, rhi = ratio_ci(paired_latency, BASE_SEED + 4100 + mi)
        token_vals = [(q, clusters[q], by[(q,V1)]["token_total"] - by[(q,V0)]["token_total"]) for q in eligible]
        td, tdlo, tdhi = bootstrap(token_vals, BASE_SEED + 4400 + mi)
        efficiency.append({"model": model, "questions": 170, "clusters": 61,
            "geometric_latency_ratio": ratio, "ratio_ci_low": rlo, "ratio_ci_high": rhi,
            "total_token_delta": td, "token_delta_ci_low": tdlo, "token_delta_ci_high": tdhi,
            "zero_retry_fraction": 1.0, "formal_latency_eligible": False,
            "demotion_reason": "efficiency_attestation_missing", "reporting_boundary": "diagnostic_only"})

    canonical = {"schema_version": "ma-sqlgrid-component-canonical-release-v1",
        "effects": effects, "descriptives": descriptives, "efficiency": efficiency,
        "replication": {"E1": False, "E2": False},
        "reporting_constraints": ["Qwen E1 has a positive frozen-state execution-equality effect under the preregistered rule; Granite E1 does not.",
          "Neither E2 backbone is promoted after within-family Holm adjustment.",
          "The two backbones are sensitivity analyses on one benchmark, not independent replications.",
          "Latency is diagnostic because the required efficiency attestation is absent."]}
    dump_json(HERE / "CANONICAL_RESULTS.json", canonical)

    flat = effects["E1"] + effects["E2"] + effects["cross_backbone"]
    fields = ["family","model","component","contrast","questions","clusters","estimate","ci_low","ci_high","p_value","holm_adjusted_p","claim_label"]
    write_csv("table_primary_effects.csv", flat, fields)
    write_csv("table_selection_descriptives.csv", descriptives, list(descriptives[0]))
    write_csv("table_efficiency_diagnostic.csv", efficiency, list(efficiency[0]))

    tex = ["% Auto-generated independent audit table", "\\begin{tabular}{llrrrrrr}",
           "\\toprule", "Experiment & Backbone & $n$ & Effect & 95\\% CI & $p$ & Holm $p$ & Decision \\\\", "\\midrule"]
    for r in effects["E1"] + effects["E2"]:
        decision = "positive" if r["claim_label"] == "positive_component_efficacy" else "not promoted"
        tex.append(f"{r['family']} & {esc(r['model'].title())} & {r['questions']} & {r['estimate']:.3f} & [{r['ci_low']:.3f}, {r['ci_high']:.3f}] & {r['p_value']:.4f} & {r['holm_adjusted_p']:.4f} & {decision} \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    (HERE / "table_primary_effects.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")
    tex2 = ["% Auto-generated independent audit table", "\\begin{tabular}{lrrrrrr}", "\\toprule",
            "Backbone & First equality & Selected equality & Changes & Rescues & Harms & Oracle@3$^{\\dagger}$ \\\\", "\\midrule"]
    for r in descriptives:
        tex2.append(f"{r['model'].title()} & {r['first_execution_equality_rate']:.3f} & {r['validator_execution_equality_rate']:.3f} & {r['selection_changes']} & {r['rescues']} & {r['harms']} & {r['oracle_at_3_diagnostic']:.3f} \\\\")
    tex2 += ["\\bottomrule", "\\multicolumn{7}{l}{$^{\\dagger}$Gold-only diagnostic; not deployable.}", "\\end{tabular}"]
    (HERE / "table_selection_descriptives.tex").write_text("\n".join(tex2) + "\n", encoding="utf-8")
    tex3 = ["% Auto-generated independent audit table", "\\begin{tabular}{lrrrl}", "\\toprule",
            "Backbone & Latency ratio & 95\\% CI & Total-token $\\Delta$ & Status \\\\", "\\midrule"]
    for r in efficiency:
        tex3.append(f"{r['model'].title()} & {r['geometric_latency_ratio']:.3f} & [{r['ratio_ci_low']:.3f}, {r['ratio_ci_high']:.3f}] & {r['total_token_delta']:.1f} & diagnostic only \\\\")
    tex3 += ["\\bottomrule", "\\end{tabular}"]
    (HERE / "table_efficiency_diagnostic.tex").write_text("\n".join(tex3) + "\n", encoding="utf-8")

    plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(7.1, 3.5))
    primary = effects["E1"] + effects["E2"]
    y = np.arange(4)[::-1]
    colors = ["#2271B2", "#D55E00", "#2271B2", "#D55E00"]
    for yi, r, c in zip(y, primary, colors):
        ax.errorbar(r["estimate"], yi, xerr=[[r["estimate"]-r["ci_low"]],[r["ci_high"]-r["estimate"]]], fmt="o", color=c, capsize=3)
    ax.axvline(0, color="black", lw=.8); ax.set_yticks(y, ["E1 Qwen", "E1 Granite", "E2 Qwen", "E2 Granite"])
    ax.set_xlabel("Paired frozen-state execution-equality difference"); ax.set_title("Cluster-aware primary component effects")
    ax.grid(axis="x", alpha=.25); savefig(fig, "figure_01_primary_effects")

    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    x = np.arange(2); w=.32
    ax.bar(x-w/2, [r["first_execution_equality_rate"] for r in descriptives], w, label="First candidate", color="#8CBBD9")
    ax.bar(x+w/2, [r["validator_execution_equality_rate"] for r in descriptives], w, label="Validator selected", color="#2A6F97")
    for i, r in enumerate(descriptives): ax.text(i, max(r["first_execution_equality_rate"],r["validator_execution_equality_rate"])+.025, f"{r['rescues']} rescue / {r['harms']} harm", ha="center", fontsize=8)
    ax.set_xticks(x, ["Qwen", "Granite"]); ax.set_ylim(0,.75); ax.set_ylabel("Frozen-state execution equality rate (n=180)")
    ax.set_title("Reference-free candidate selection on V1"); ax.legend(frameon=False); ax.grid(axis="y", alpha=.25)
    savefig(fig, "figure_02_selection_descriptives")

    fig, axes = plt.subplots(1,2,figsize=(7.4,3.3))
    for i,r in enumerate(efficiency):
        axes[0].errorbar(i,r["geometric_latency_ratio"],yerr=[[r["geometric_latency_ratio"]-r["ratio_ci_low"]],[r["ratio_ci_high"]-r["geometric_latency_ratio"]]],fmt="o",capsize=4,color=colors[i])
        axes[1].errorbar(i,r["total_token_delta"],yerr=[[r["total_token_delta"]-r["token_delta_ci_low"]],[r["token_delta_ci_high"]-r["total_token_delta"]]],fmt="o",capsize=4,color=colors[i])
    axes[0].axhline(1,color="black",lw=.8); axes[1].axhline(0,color="black",lw=.8)
    for ax in axes: ax.set_xticks([0,1],["Qwen","Granite"]); ax.grid(axis="y",alpha=.25)
    axes[0].set_ylabel("V1/V0 geometric latency ratio"); axes[1].set_ylabel("V1-V0 total tokens")
    fig.suptitle("E4 diagnostics (latency is not eligible for a controlled claim)")
    savefig(fig, "figure_03_efficiency_diagnostics")

    registered = read_json(SRC / "analysis" / "RESULTS.json")
    comparisons = []
    regrows = registered["primary_effects"]
    for fam in ("E1","E2","cross_backbone"):
        for ours, theirs in zip(effects[fam], regrows[fam]):
            maxdiff = max(abs(ours[k]-theirs[k]) for k in ("estimate","ci_low","ci_high","p_value","holm_adjusted_p"))
            comparisons.append({"family": fam, "model_or_component": ours.get("model") or ours.get("component"), "maximum_absolute_difference": maxdiff})
            assert maxdiff < 1e-15
    efficiency_comparisons = []
    for ours, theirs in zip(efficiency, registered["efficiency"]):
        diffs = {
            "geometric_latency_ratio": abs(ours["geometric_latency_ratio"] - theirs["latency"]["geometric_ratio"]),
            "latency_ci_low": abs(ours["ratio_ci_low"] - theirs["latency"]["ratio_ci_low"]),
            "latency_ci_high": abs(ours["ratio_ci_high"] - theirs["latency"]["ratio_ci_high"]),
            "total_token_delta": abs(ours["total_token_delta"] - theirs["total_token_delta"]["estimate"]),
        }
        assert max(diffs.values()) < 1e-15
        efficiency_comparisons.append({"model": ours["model"], "absolute_differences": diffs,
                                       "formal_latency_eligible": False})
    audit = {"schema_version":"ma-sqlgrid-component-independent-audit-v1", "status":"pass",
        "freeze_sha256": sha(SRC/"PROTOCOL_FREEZE.json"), "freeze_verification":"internally consistent",
        "frozen_prompt_rows":360, "formal_call_rows_per_backbone":350, "eligible_questions":170, "eligible_clusters":61,
        "intervention_invariance_recomputed": invariance, "models":audit_models,
        "selection_before_gold_evidence_scope":"Ledger schemas contain no gold fields; seals bind the selection hashes and scoring manifests bind those same hashes. This verifies artifact ordering declarations, not an external timestamp/notary proof.",
        "independent_statistical_recomputation": {"bootstrap_samples":BOOT_N,"randomization_samples":RAND_N,
            "registered_output_comparisons":comparisons, "registered_efficiency_comparisons":efficiency_comparisons},
        "claim_boundary":canonical["reporting_constraints"],
        "overall_conclusion":"All candidate and selected SQL were independently re-executed on the frozen database state; E1/E2 registered statistics reproduced exactly; E4 remains diagnostic."}
    dump_json(HERE / "INDEPENDENT_AUDIT.json", audit)
    md = """# Independent Audit of Prospective Component Experiments\n\n## Verdict\n\n**PASS with a mandatory latency boundary.** The frozen prompt/call-order ledgers, two 350-call formal runs, sealed reference-free selections, scored ledgers, and registered aggregate numbers were independently checked. No source freeze, run, scoring, or analysis artifact was changed.\n\n## Recomputed evidence\n\n- Each backbone has exactly 350 unique formal calls: 170 paired V0/V1 questions plus 10 additional V1-only questions, giving 180 V1 questions. Both runs contain 350 successes, zero provider failures, and 350 zero-retry calls.\n- The intervention-eligible set independently reconstructs to 170 questions in 61 frozen template clusters. Question text, selected-table hash, selected-column hash, and inferred-shape hash are invariant within every V0/V1 pair.\n- Prediction and candidate-selection ledgers contain no gold/reference fields. The selection seals bind their ledgers, and scoring manifests bind the same selection hashes. This is strong ledger-level evidence for selection-before-gold, but it is not an external timestamp or notarial proof.\n- All 700 scored rows and every parsed candidate were independently re-executed against the frozen SQLite state; the execution-equality flags match the sealed scored ledgers exactly.\n- For the frozen-state execution-equality outcome, Qwen E1 is +0.1059 (95% cluster bootstrap CI +0.0282 to +0.2013; Holm p=0.0310), satisfying the preregistered positive-efficacy rule. Granite E1 is 0.0000 (CI -0.1902 to +0.1705; Holm p=1.0000).\n- For the same outcome, Qwen E2 is +0.0389 (CI -0.0081 to +0.1071; Holm p=0.5008). Granite E2 is +0.0556 (CI +0.0075 to +0.1232; Holm p=0.1285). Neither E2 result is promoted because the complete preregistered rule includes Holm-adjusted p<0.05.\n- The backbones are sensitivity analyses on the same 180-question benchmark, not independent replications. Replication is false for E1 and E2.\n- Zero retries preserve token accounting. Latency remains **diagnostic only** because the required exclusive-GPU/thermal/competing-process efficiency attestation is absent.\n\n## Publication use\n\nUse `table_primary_effects` for confirmatory frozen-state execution-equality results, `table_selection_descriptives` for E2 mechanism diagnostics, and `table_efficiency_diagnostic` only with the explicit diagnostic label. Figures use the same separation. Do not state that E2 improved either model, do not call the two backbones replications, and do not make a controlled latency claim.\n"""
    (HERE / "INDEPENDENT_AUDIT.md").write_text(md, encoding="utf-8")

    # Manifest is last and excludes itself for stable verification.
    files = {}
    for path in sorted(HERE.rglob("*")):
        if (path.is_file() and path.name != "release_manifest.json"
                and "__pycache__" not in path.parts):
            name = path.relative_to(HERE).as_posix()
            files[name] = {"bytes":path.stat().st_size,"sha256":sha(path)}
    manifest = {"schema_version":"ma-sqlgrid-component-release-manifest-v1", "status":"complete_and_verified",
                "generated_by":"build_release.py", "source_directory":str(SRC.relative_to(MA.parent.parent.parent)), "files":files}
    dump_json(HERE/"release_manifest.json",manifest)
    print(f"PASS: wrote {len(files)} canonical audit/publication artifacts")


if __name__ == "__main__":
    main()
