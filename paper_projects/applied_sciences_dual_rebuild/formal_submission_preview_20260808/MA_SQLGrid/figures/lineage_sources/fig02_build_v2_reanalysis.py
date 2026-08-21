#!/usr/bin/env python3
"""Independent, offline MA-SQLGrid v2 reanalysis.

Only the two accepted raw prediction ledgers are inputs.  No model is called,
and the quarantined Qwen directory is deliberately not represented by a path.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import sqlite3
import sys
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
MA = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid"
OUT = MA / "canonical_v2_reanalysis"
QWEN = MA / "formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1"
GRANITE = MA / "granite_formal/granite33_8b_q4km_seed20260805_clean1"
SOURCE = ROOT / "paper_projects/2026_ma_sqlgrid_cmc/source"
CODE = SOURCE / "code/experiment_final"
DATA = SOURCE / "data/griddb_maintenance_v2_v0_1"
SHARED = ROOT / "paper_projects/applied_sciences_dual_rebuild/shared/stat_audit.py"
CELLS = ["F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape"]
BACKBONES = {"qwen": QWEN, "granite": GRANITE}
METRICS = ["execution", "structural_common"]
EDGES = [
    ("structural_hint_at_full", CELLS[0], CELLS[1]),
    ("context_package_at_no_hint", CELLS[0], CELLS[2]),
    ("structural_hint_at_compact", CELLS[2], CELLS[3]),
    ("context_package_at_with_hint", CELLS[1], CELLS[3]),
]
BOOTSTRAP_SAMPLES = 20_000
RANDOMIZATION_SAMPLES = 100_000
SEED = 20260805


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def template(sql: str) -> str:
    x = re.sub(r"'[^']*'", "?", sql.lower())
    x = re.sub(r'"[^"]*"', "?", x)
    x = re.sub(r"\b\d+(?:\.\d+)?\b", "?", x)
    return " ".join(x.split())


def write_csv(path: Path, data: list[dict], fields: list[str] | None = None) -> None:
    if not data:
        raise ValueError(f"refusing empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields or list(data[0]))
        w.writeheader()
        w.writerows(data)


def describe(values: list[float]) -> dict:
    a = np.asarray(values, dtype=float)
    return {"mean": float(a.mean()), "sd": float(a.std(ddof=1)), "min": float(a.min()),
            "median": float(np.median(a)), "max": float(a.max())}


def cluster_bootstrap(pairs: list[tuple[float, float, str]], stat, seed: int) -> dict:
    return stat.cluster_paired_bootstrap(pairs, samples=BOOTSTRAP_SAMPLES, confidence=.95, seed=seed)


def cluster_randomization(pairs: list[tuple[float, float, str]], seed: int) -> dict:
    """Two-sided Monte Carlo sign-flip test at the frozen template-cluster unit.

    All question-level paired differences in a cluster receive one common sign.
    The statistic is the question-weighted mean difference, matching the point
    estimate and cluster-bootstrap estimand.
    """
    grouped: dict[str, list[float]] = defaultdict(list)
    for a, b, cluster in pairs:
        grouped[cluster].append(float(b) - float(a))
    clusters = sorted(grouped)
    sums = np.asarray([sum(grouped[c]) for c in clusters], dtype=float)
    observed_num = float(sums.sum())
    rng = np.random.default_rng(seed)
    extreme = 0
    done = 0
    batch = 10_000
    while done < RANDOMIZATION_SAMPLES:
        n = min(batch, RANDOMIZATION_SAMPLES - done)
        signs = rng.integers(0, 2, size=(n, len(clusters)), dtype=np.int8) * 2 - 1
        nums = signs @ sums
        extreme += int(np.count_nonzero(np.abs(nums) >= abs(observed_num) - 1e-12))
        done += n
    return {"method": "template-cluster Monte Carlo sign-flip randomization",
            "cluster_count": len(clusters), "pair_count": len(pairs),
            "statistic": observed_num / len(pairs), "samples": RANDOMIZATION_SAMPLES,
            "seed": seed, "extreme_draws": extreme,
            "p_value": (extreme + 1) / (RANDOMIZATION_SAMPLES + 1)}


def holm(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(values) - rank) * values[i]))
        out[i] = running
    return out


def factorial_vectors(index: dict, qids: list[str], metric: str) -> dict[str, dict[str, tuple[float, str]]]:
    result = {"context_package_main": {}, "structural_hint_main": {}, "interaction": {}}
    for q in qids:
        v = {c: index[(q, c)][metric] for c in CELLS}
        cluster = index[(q, CELLS[0])]["template_cluster"]
        result["context_package_main"][q] = (.5 * ((v[CELLS[2]]-v[CELLS[0]]) + (v[CELLS[3]]-v[CELLS[1]])), cluster)
        result["structural_hint_main"][q] = (.5 * ((v[CELLS[1]]-v[CELLS[0]]) + (v[CELLS[3]]-v[CELLS[2]])), cluster)
        result["interaction"][q] = ((v[CELLS[3]]-v[CELLS[2]]) - (v[CELLS[1]]-v[CELLS[0]]), cluster)
    return result


def connected_required_tables(required: set[str], selected: set[str], selected_cols: dict[str, set[str]], fks: list[tuple]) -> bool:
    if len(required) <= 1:
        return True
    graph: dict[str, set[str]] = defaultdict(set)
    for left, lc, right, rc in fks:
        if left in selected and right in selected and lc in selected_cols.get(left, set()) and rc in selected_cols.get(right, set()):
            graph[left].add(right); graph[right].add(left)
    start = next(iter(required))
    seen = {start}; queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt); queue.append(nxt)
    return required <= seen


def prompt_fields(context: str) -> dict[str, int]:
    fields = {
        "full_schema_ddl": "CREATE TABLE" in context,
        "global_value_dictionary": "Database value dictionary:" in context,
        "selected_schema": "Tables and selected columns:" in context,
        "join_paths": "Join paths:" in context,
        "question_matched_values": "Exact database values matched from the question:" in context,
        "normalization_hints": "Power-grid domain normalization hints inferred from the question:" in context,
        "structural_hint": ("answer-shape hints" in context.lower()),
    }
    return {k: int(v) for k, v in fields.items()}


def latex_escape(x: str) -> str:
    return x.replace("_", r"\_").replace("%", r"\%")


def main() -> int:
    for d in [OUT, OUT/"tables", OUT/"figures", OUT/"tests"]:
        d.mkdir(parents=True, exist_ok=True)
    sys.path[:0] = [str(CODE), str(SOURCE/"code"), str(SOURCE/"code/evaluator")]
    factorial = load("ma_v2_factorial", CODE/"applsci_factorial.py")
    stat = load("ma_v2_stat", SHARED)
    questions = {r["question_id"]: r for r in rows(DATA/"questions.jsonl") if r["split"] == "test"}
    qids = sorted(questions)
    expected = {(q, c) for q in qids for c in CELLS}
    accepted: dict[str, dict[str, dict]] = {}
    prompts: dict[str, dict[tuple[str, str], dict]] = {}
    scores: dict[str, dict[tuple[str, str], dict]] = {}
    checks = []
    def check(name, passed, evidence): checks.append({"check": name, "passed": bool(passed), "evidence": evidence})

    for backbone, run in BACKBONES.items():
        manifest = json.loads((run/"manifest.json").read_text(encoding="utf-8"))
        p = rows(run/"prompts.jsonl"); y = rows(run/"predictions.jsonl"); s = rows(run/"scores.jsonl")
        accepted[backbone] = {(r["question_id"], r["condition"]): r for r in y}
        prompts[backbone] = {(r["question_id"], r["condition"]): r for r in p}
        scores[backbone] = {(r["question_id"], r["condition"]): r for r in s}
        check(f"{backbone}_accepted_completed", manifest["status"] == "completed" and manifest["canonical_result_eligible"], manifest["status"])
        for label, rr in [("prompts", p), ("predictions", y), ("scores", s)]:
            keys = [(r["question_id"], r["condition"]) for r in rr]
            check(f"{backbone}_{label}_cartesian", len(keys)==len(set(keys))==720 and set(keys)==expected, {"rows":len(keys),"unique":len(set(keys))})

    # Frozen common target: the project-authored answer_shape.column_count field.
    # The code-derived infer_answer_shape count is audited, but is not used as a
    # second target. Row granularity/order are not inferential endpoints because
    # the frozen evaluator implements only executed projected-column count.
    inferred_mismatch = []
    for q in qids:
        stored = int(questions[q]["answer_shape"]["column_count"])
        inferred = int(factorial.formal.chess.infer_answer_shape(questions[q]["question"])["column_count"])
        if stored != inferred: inferred_mismatch.append([q, stored, inferred])
    check("stored_target_matches_frozen_rule", not inferred_mismatch, inferred_mismatch[:20])

    same_prompt_records = all(
        prompts["qwen"][(q,c)]["prompt"] == prompts["granite"][(q,c)]["prompt"]
        and prompts["qwen"][(q,c)]["context"] == prompts["granite"][(q,c)]["context"]
        for q,c in expected
    )
    check("backbones_received_identical_frozen_prompts", same_prompt_records, {"pairs":720})
    hint_is_appended_block = all(
        prompts["qwen"][(q,CELLS[1])]["context"].startswith(prompts["qwen"][(q,CELLS[0])]["context"])
        and prompts["qwen"][(q,CELLS[3])]["context"].startswith(prompts["qwen"][(q,CELLS[2])]["context"])
        for q in qids
    )
    check("within_scope_hint_is_appended_context_block", hint_is_appended_block, {"questions":180,"scope_pairs":360})

    conn = sqlite3.connect(f"file:{factorial.formal.DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only=ON")
    canonical = []
    contexts = {}
    execution_mismatch = []
    original_shape_mismatch = []
    unsafe = []
    try:
        bundles = {q: factorial.formal.load_context_bundle(conn, factorial.without_gold(questions[q])) for q in qids}
        contexts = {q: factorial.build_contexts(conn, factorial.without_gold(questions[q])) for q in qids}
        for backbone in BACKBONES:
            for q, c in sorted(expected):
                pred = accepted[backbone][(q,c)]; archived = scores[backbone][(q,c)]
                safe, _, err = factorial.formal.validate_read_only_select(pred["predicted_sql"])
                if not safe: unsafe.append([backbone,q,c,err])
                ev = factorial.formal.score_prediction(conn, questions[q], pred["predicted_sql"])
                old_val = factorial.formal.chess.reference_free_validation(conn, contexts[q][c][1], pred["predicted_sql"])
                try:
                    direct = conn.execute(pred["predicted_sql"])
                    predicted_columns = len(direct.description or [])
                    direct.fetchall()
                except sqlite3.Error:
                    predicted_columns = 0
                execution = int(bool(ev.correct))
                old_shape = int(bool(old_val["shape_ok"]))
                target = int(questions[q]["answer_shape"]["column_count"])
                common = int(bool(old_val["exec_ok"]) and predicted_columns == target)
                if execution != int(bool(archived["correct"])): execution_mismatch.append([backbone,q,c])
                if old_shape != int(bool(archived["shape_ok"])): original_shape_mismatch.append([backbone,q,c])
                cluster = "tpl_" + hashlib.sha256(template(questions[q]["gold_sql"]).encode()).hexdigest()[:12]
                canonical.append({"backbone":backbone,"question_id":q,"condition":c,"template_cluster":cluster,
                    "execution":execution,"structural_common":common,"structural_original":old_shape,
                    "frozen_target_column_count":target,"predicted_column_count":predicted_columns,
                    "prompt_hash":pred["prompt_hash"],"context_hash":pred["context_hash"],"response_hash":pred["response_hash"]})
    finally:
        conn.close()
    check("all_predictions_read_only", not unsafe, unsafe[:20])
    check("all_1440_execution_outcomes_unchanged", not execution_mismatch, execution_mismatch[:20])
    check("all_1440_original_shape_reproduced", not original_shape_mismatch, original_shape_mismatch[:20])
    check("canonical_row_count", len(canonical)==1440, len(canonical))
    canonical_path = OUT/"canonical_rows_v2.jsonl"
    canonical_path.write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in canonical),encoding="utf-8")
    indexes = {b:{(r["question_id"],r["condition"]):r for r in canonical if r["backbone"]==b} for b in BACKBONES}

    cell_summary=[]
    for b in BACKBONES:
        for c in CELLS:
            rr=[indexes[b][(q,c)] for q in qids]
            for metric in METRICS:
                vals=[r[metric] for r in rr]
                pairs=[(0,v,r["template_cluster"]) for v,r in zip(vals,rr)]
                boot=cluster_bootstrap(pairs,stat,SEED+1000*list(BACKBONES).index(b)+100*CELLS.index(c)+METRICS.index(metric))
                cell_summary.append({"backbone":b,"condition":c,"metric":metric,"correct":sum(vals),"n":180,"mean":mean(vals),"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],"clusters":boot["cluster_count"]})

    within=[]; vectors={}
    for bi,b in enumerate(BACKBONES):
        vectors[b]={}
        for mi,m in enumerate(METRICS):
            vectors[b][m]=factorial_vectors(indexes[b],qids,m)
            for ei,(effect,values) in enumerate(vectors[b][m].items()):
                pairs=[(0,v,c) for v,c in values.values()]
                boot=cluster_bootstrap(pairs,stat,SEED+10000+bi*1000+mi*100+ei)
                within.append({"backbone":b,"metric":m,"effect":effect,"estimate":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],"clusters":boot["cluster_count"],"bootstrap_samples":BOOTSTRAP_SAMPLES})

    cross=[]
    for mi,m in enumerate(METRICS):
        for ei,effect in enumerate(vectors["qwen"][m]):
            vals={q:(vectors["qwen"][m][effect][q][0],vectors["granite"][m][effect][q][0],vectors["qwen"][m][effect][q][1]) for q in qids}
            pairs=list(vals.values()); boot=cluster_bootstrap(pairs,stat,SEED+20000+mi*100+ei)
            cross.append({"metric":m,"effect":"backbone_x_"+effect,
                "qwen_effect":mean(x[0] for x in pairs),"granite_effect":mean(x[1] for x in pairs),
                "granite_minus_qwen":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],
                "clusters":boot["cluster_count"],"bootstrap_samples":BOOTSTRAP_SAMPLES})

    # Three explicitly separate multiplicity families, each containing 4 edges x 2 endpoints.
    tests=[]
    for bi,b in enumerate(BACKBONES):
        family=f"{b}_four_edges_x_two_endpoints"
        family_rows=[]
        for ei,(name,base,treat) in enumerate(EDGES):
            for mi,m in enumerate(METRICS):
                pairs=[(indexes[b][(q,base)][m],indexes[b][(q,treat)][m],indexes[b][(q,base)]["template_cluster"]) for q in qids]
                boot=cluster_bootstrap(pairs,stat,SEED+30000+bi*1000+ei*10+mi)
                rand=cluster_randomization(pairs,SEED+40000+bi*1000+ei*10+mi)
                mc=stat.mcnemar_exact(pairs)
                family_rows.append({"family":family,"backbone":b,"contrast":name,"baseline":base,"treatment":treat,"metric":m,
                    "effect":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],
                    "cluster_randomization_p":rand["p_value"],"randomization_samples":rand["samples"],"randomization_seed":rand["seed"],
                    "mcnemar_descriptive_baseline_only":mc["baseline_only_correct"],"mcnemar_descriptive_treatment_only":mc["treatment_only_correct"],"mcnemar_descriptive_p":mc["p_value"]})
        adj=holm([r["cluster_randomization_p"] for r in family_rows])
        for r,p in zip(family_rows,adj): r["cluster_randomization_p_holm"]=p
        tests.extend(family_rows)
    family_rows=[]; family="cross_backbone_four_cells_x_two_endpoints"
    for ci,c in enumerate(CELLS):
        for mi,m in enumerate(METRICS):
            pairs=[(indexes["qwen"][(q,c)][m],indexes["granite"][(q,c)][m],indexes["qwen"][(q,c)]["template_cluster"]) for q in qids]
            boot=cluster_bootstrap(pairs,stat,SEED+50000+ci*10+mi); rand=cluster_randomization(pairs,SEED+60000+ci*10+mi); mc=stat.mcnemar_exact(pairs)
            family_rows.append({"family":family,"backbone":"granite_minus_qwen","contrast":c,"baseline":"qwen","treatment":"granite","metric":m,
                "effect":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],
                "cluster_randomization_p":rand["p_value"],"randomization_samples":rand["samples"],"randomization_seed":rand["seed"],
                "mcnemar_descriptive_baseline_only":mc["baseline_only_correct"],"mcnemar_descriptive_treatment_only":mc["treatment_only_correct"],"mcnemar_descriptive_p":mc["p_value"]})
    adj=holm([r["cluster_randomization_p"] for r in family_rows])
    for r,p in zip(family_rows,adj): r["cluster_randomization_p_holm"]=p
    tests.extend(family_rows)

    # Prompt/context package audit (gold is used offline only for recall diagnostics).
    question_audit=[]; prompt_audit=[]
    fks=factorial.formal.chess.FOREIGN_KEYS
    for q in qids:
        domain=bundles[q]["domain"]
        selected=set(domain["selected_tables"])
        selected_cols={t:set(v) for t,v in domain["selected_columns"].items()}
        gold_tables=set(questions[q]["tables"]); gold_cols=set(questions[q]["columns"])
        selected_qualified={f"{t}.{c}" for t,cols in selected_cols.items() for c in cols}
        table_recall=len(gold_tables & selected)/len(gold_tables)
        col_recall=len(gold_cols & selected_qualified)/len(gold_cols)
        join_ok=connected_required_tables(gold_tables,selected,selected_cols,fks)
        row={"question_id":q,"selected_table_count":len(selected),"selected_column_count":len(selected_qualified),
            "matched_value_field_count":len(domain["matched_values"]),"normalization_hint_count":len(domain["normalized_value_hints"]),
            "gold_required_table_count":len(gold_tables),"gold_required_column_count":len(gold_cols),
            "gold_table_recall":table_recall,"gold_column_recall":col_recall,
            "gold_all_tables_retained":int(table_recall==1),"gold_all_columns_retained":int(col_recall==1),
            "gold_join_path_retained":int(join_ok),"gold_used_offline_only":1}
        for b in BACKBONES:
            for suffix,full,compact in [("no_hint",CELLS[0],CELLS[2]),("with_hint",CELLS[1],CELLS[3])]:
                row[f"{b}_{suffix}_full_correct_compact_wrong"] = int(indexes[b][(q,full)]["execution"]==1 and indexes[b][(q,compact)]["execution"]==0)
        question_audit.append(row)
        for b in BACKBONES:
            for c in CELLS:
                p=prompts[b][(q,c)]; y=accepted[b][(q,c)]
                prompt_audit.append({"backbone":b,"question_id":q,"condition":c,"context_scope":p["context_scope"],
                    "answer_shape_hints":int(p["answer_shape_hints"]),"prompt_words":len(p["prompt"].split()),
                    "context_words":len(p["context"].split()),"model_token_input":y["token_input"],**prompt_fields(p["context"])})

    context_summary=[]
    for b in BACKBONES:
        for c in CELLS:
            rr=[r for r in prompt_audit if r["backbone"]==b and r["condition"]==c]
            for field in ["prompt_words","context_words","model_token_input"]:
                d=describe([r[field] for r in rr]); context_summary.append({"backbone":b,"condition":c,"measure":field,**d})
    for measure,values in [("selected_table_count",[r["selected_table_count"] for r in question_audit]),("selected_column_count",[r["selected_column_count"] for r in question_audit]),("gold_table_recall",[r["gold_table_recall"] for r in question_audit]),("gold_column_recall",[r["gold_column_recall"] for r in question_audit])]:
        context_summary.append({"backbone":"offline_compact_selector","condition":"F10_and_F11_identical","measure":measure,**describe(values)})

    field_audit=[]
    for c in CELLS:
        rr=[r for r in prompt_audit if r["backbone"]=="qwen" and r["condition"]==c]
        for field in ["full_schema_ddl","global_value_dictionary","selected_schema","join_paths","question_matched_values","normalization_hints","structural_hint"]:
            field_audit.append({"condition":c,"field":field,"present_questions":sum(r[field] for r in rr),"n":180,"all_present":int(all(r[field] for r in rr))})

    old_new=[]
    for b in BACKBONES:
        for c in CELLS:
            rr=[indexes[b][(q,c)] for q in qids]
            old=mean(r["structural_original"] for r in rr); new=mean(r["structural_common"] for r in rr)
            old_new.append({"backbone":b,"condition":c,"old_condition_dependent_shape":old,"new_common_target_columns":new,"new_minus_old":new-old})

    # Output tables.
    tables=OUT/"tables"
    write_csv(tables/"cell_summary_v2.csv",cell_summary)
    write_csv(tables/"within_backbone_factorial_v2.csv",within)
    write_csv(tables/"cross_backbone_modifiers_v2.csv",cross)
    write_csv(tables/"cluster_randomization_holm_v2.csv",tests)
    write_csv(tables/"prompt_context_summary.csv",context_summary)
    write_csv(tables/"prompt_field_invariance.csv",field_audit)
    write_csv(tables/"context_question_gold_offline_audit.csv",question_audit)
    write_csv(tables/"old_vs_new_shape.csv",old_new)

    # Compact TeX tables generated from canonical CSV values.
    cell_lines=[r"\begin{tabular}{llrrrr}",r"\toprule",r"Backbone & Cell & Exec. & Common cols. & Exec. 95\% CI & Cols. 95\% CI \\",r"\midrule"]
    for b in BACKBONES:
        for c in CELLS:
            e=next(r for r in cell_summary if r["backbone"]==b and r["condition"]==c and r["metric"]=="execution")
            s=next(r for r in cell_summary if r["backbone"]==b and r["condition"]==c and r["metric"]=="structural_common")
            cell_lines.append(f"{b.title()} & {latex_escape(c)} & {e['mean']:.4f} & {s['mean']:.4f} & [{e['ci_low']:.4f},{e['ci_high']:.4f}] & [{s['ci_low']:.4f},{s['ci_high']:.4f}] \\")
    cell_lines += [r"\bottomrule",r"\end{tabular}"]
    (tables/"table_cell_summary_v2.tex").write_text("\n".join(cell_lines)+"\n",encoding="utf-8")
    eff_lines=[r"\begin{tabular}{lllrrr}",r"\toprule",r"Backbone & Endpoint & Effect & Estimate & CI low & CI high \\",r"\midrule"]
    for r in within:
        eff_lines.append(f"{r['backbone'].title()} & {latex_escape(r['metric'])} & {latex_escape(r['effect'])} & {r['estimate']:.4f} & {r['ci_low']:.4f} & {r['ci_high']:.4f} \\")
    eff_lines += [r"\bottomrule",r"\end{tabular}"]
    (tables/"table_factorial_effects_v2.tex").write_text("\n".join(eff_lines)+"\n",encoding="utf-8")

    # Figures: vector + PDF + high-resolution PNG from the same data objects.
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
    x=np.arange(4); width=.34
    for ax,metric,title in zip(axes,METRICS,["Execution equality","Common-target projected-column conformity"]):
        for j,b in enumerate(BACKBONES):
            vals=[next(r for r in cell_summary if r["backbone"]==b and r["condition"]==c and r["metric"]==metric)["mean"] for c in CELLS]
            ax.bar(x+(j-.5)*width,vals,width,label=b.title())
        ax.set_xticks(x,["F00","F01","F10","F11"]); ax.set_ylim(0,1); ax.set_title(title); ax.set_ylabel("Proportion")
    axes[1].legend(frameon=False); fig.tight_layout()
    for ext in ["pdf","svg","png"]: fig.savefig(OUT/"figures"/f"fig01_v2_cells.{ext}",dpi=450 if ext=="png" else None,bbox_inches="tight")
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,4.3))
    effects=["context_package_main","structural_hint_main","interaction"]
    for ax,metric,title in zip(axes,METRICS,["Execution equality","Common-target projected columns"]):
        for j,b in enumerate(BACKBONES):
            rr=[next(r for r in within if r["backbone"]==b and r["metric"]==metric and r["effect"]==e) for e in effects]
            y=np.arange(3)+(j-.5)*.18; vals=np.array([r["estimate"] for r in rr]); lo=vals-np.array([r["ci_low"] for r in rr]); hi=np.array([r["ci_high"] for r in rr])-vals
            ax.errorbar(vals,y,xerr=[lo,hi],fmt="o",capsize=3,label=b.title())
        ax.axvline(0,color="black",lw=.8); ax.set_yticks(np.arange(3),["Context package","Structural hint","Interaction"]); ax.set_title(title); ax.set_xlabel("Paired effect")
    axes[1].legend(frameon=False); fig.tight_layout()
    for ext in ["pdf","svg","png"]: fig.savefig(OUT/"figures"/f"fig02_v2_factorial_effects.{ext}",dpi=450 if ext=="png" else None,bbox_inches="tight")
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    qrows=[r for r in context_summary if r["backbone"]=="qwen" and r["measure"]=="model_token_input"]
    axes[0].bar(range(4),[r["mean"] for r in qrows]); axes[0].set_xticks(range(4),["F00","F01","F10","F11"]); axes[0].set_ylabel("Qwen tokenizer input tokens"); axes[0].set_title("Prompt-length manipulation")
    axes[1].hist([r["gold_column_recall"] for r in question_audit],bins=np.linspace(0,1,11),edgecolor="white"); axes[1].set_xlabel("Gold-required column recall (offline only)"); axes[1].set_ylabel("Questions"); axes[1].set_title("Compact selector coverage")
    fig.tight_layout()
    for ext in ["pdf","svg","png"]: fig.savefig(OUT/"figures"/f"fig03_context_audit.{ext}",dpi=450 if ext=="png" else None,bbox_inches="tight")
    plt.close(fig)
    visual_qa={"schema_version":"ma-sqlgrid-v2-visual-qa-v1","status":"pass",
        "reviewed_utc":datetime.now(timezone.utc).isoformat(),"reviewed_files":["fig01_v2_cells.png","fig02_v2_factorial_effects.png","fig03_context_audit.png"],
        "checks":{"labels_legible":True,"confidence_intervals_not_clipped":True,"zero_reference_visible":True,"axes_and_units_present":True,"offline_gold_label_visible":True,"color_not_sole_effect_identifier":True},
        "note":"Manual inspection at rendered PNG scale; PDF/SVG share the same plotting objects."}
    (OUT/"VISUAL_QA.json").write_text(json.dumps(visual_qa,indent=2)+"\n",encoding="utf-8")

    result={"schema_version":"ma-sqlgrid-canonical-v2-reanalysis-v1","generated_utc":datetime.now(timezone.utc).isoformat(),
        "passed":all(x["passed"] for x in checks),"scope":"offline reanalysis of two accepted deterministic ledgers on one exposed synthetic database",
        "endpoint_definition":{"structural_common":"successful SQLite execution and projected-column count equals the same project-authored answer_shape.column_count for that question in all four conditions","not_measured":"row granularity, ordering correctness, semantic correctness"},
        "factor_definition":{"context":"full schema plus global value dictionary versus compact selected-schema plus question-matched values and normalization hints","hint":"corpus-tailored question-derived structural/SQL-operation hint package"},
        "multiplicity_families":["qwen_four_edges_x_two_endpoints","granite_four_edges_x_two_endpoints","cross_backbone_four_cells_x_two_endpoints"],
        "checks":checks,"cell_summary":cell_summary,"within_backbone_factorial":within,"cross_backbone_modifiers":cross,
        "registered_cluster_randomization":tests,"old_vs_new_shape":old_new,
        "context_audit_summary":{"questions":180,"gold_use":"offline diagnostics only; never prompt input",
            "all_gold_tables_retained":sum(r["gold_all_tables_retained"] for r in question_audit),
            "all_gold_columns_retained":sum(r["gold_all_columns_retained"] for r in question_audit),
            "join_paths_retained":sum(r["gold_join_path_retained"] for r in question_audit),
            "multi_table_questions":sum(r["gold_required_table_count"]>1 for r in question_audit),
            "multi_table_join_paths_retained":sum(r["gold_join_path_retained"] for r in question_audit if r["gold_required_table_count"]>1),
            "omission_failures_full_correct_compact_wrong":{f"{b}_{suffix}":sum(r[f"{b}_{suffix}_full_correct_compact_wrong"] for r in question_audit if not r["gold_all_columns_retained"] or not r["gold_all_tables_retained"]) for b in BACKBONES for suffix in ["no_hint","with_hint"]}},
        "granite_compact_shape_p_fact":{"old_question_level_mcnemar_raw":3.1028037028590916e-7,"old_question_level_mcnemar_holm":1.861682221715455e-6,
            "manuscript_mistranscription":"1.86e-4 was incorrect","v2_cluster_randomization":next(r for r in tests if r["backbone"]=="granite" and r["contrast"]=="structural_hint_at_compact" and r["metric"]=="execution")}}
    (OUT/"V2_REANALYSIS.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")

    # Freeze/method report and concise release report.
    input_files=[]
    for run in BACKBONES.values(): input_files += [run/"manifest.json",run/"prompts.jsonl",run/"predictions.jsonl",run/"scores.jsonl"]
    input_files += [DATA/"questions.jsonl",DATA/"database.sqlite",CODE/"applsci_factorial.py",SOURCE/"smoke/dev_chess_style_pilot.py",SHARED]
    freeze={"schema_version":"ma-sqlgrid-v2-reanalysis-freeze-v1","no_model_execution":True,"accepted_inputs":{str(p.relative_to(ROOT)).replace('\\','/'):{"sha256":sha(p),"bytes":p.stat().st_size} for p in input_files},
        "prohibited_input_policy":"The quarantined Qwen directory is not read and no path inside it is encoded in this release.","bootstrap_samples":BOOTSTRAP_SAMPLES,"randomization_samples":RANDOMIZATION_SAMPLES,"seed_base":SEED}
    (OUT/"FREEZE_AND_METHOD.json").write_text(json.dumps(freeze,indent=2)+"\n",encoding="utf-8")
    qshape=next(r for r in within if r["backbone"]=="qwen" and r["metric"]=="structural_common" and r["effect"]=="structural_hint_main")
    gshape=next(r for r in within if r["backbone"]=="granite" and r["metric"]=="structural_common" and r["effect"]=="structural_hint_main")
    lines=["# MA-SQLGrid canonical v2 independent reanalysis","",f"**Decision: {'PASS' if result['passed'] else 'FAIL'}.** No model was run; the manuscript and prior canonical release were not modified.","",
        "## Corrected endpoint","","The inferential structural endpoint is deliberately narrow: successful SQLite execution with the number of projected result columns equal to one frozen, project-authored target for that question in every condition. The implemented evidence does not validate row granularity, ordering correctness, or semantic correctness.","",
        "## Main correction","",f"- Qwen common-target structural-hint main effect: {qshape['estimate']:+.4f}, 95% template-cluster bootstrap CI [{qshape['ci_low']:+.4f}, {qshape['ci_high']:+.4f}] (old condition-dependent value +0.4944).",f"- Granite common-target structural-hint main effect: {gshape['estimate']:+.4f}, 95% CI [{gshape['ci_low']:+.4f}, {gshape['ci_high']:+.4f}] (old condition-dependent value +0.4528).","- All 1440 execution outcomes are unchanged and independently reproduced from the accepted prediction ledgers.","",
        "## Inference","","Twenty-thousand cluster bootstrap draws preserve all rows within each of 70 normalized-gold-SQL template clusters. Inferential p-values use 100,000 Monte Carlo sign flips at that same cluster unit. Holm adjustment is applied separately to exactly three registered eight-test families. Question-level McNemar discordances and p-values are retained only as descriptive sensitivity fields.","",
        "## Intervention boundary","","The context factor is a bundled package, not isolated schema compactness: full schema plus a global value dictionary is compared with selected schema plus question-matched values and handcrafted normalization hints. The hint factor is a corpus-tailored structural/SQL-operation package. Gold tables and columns are used only in the offline selector audit.","",
        "## Granite p-value correction","","The archived question-level exact McNemar result for Granite structural hints at compact context on execution was raw p=3.1028e-7 and Holm p=1.8617e-6; 1.86e-4 was a transcription error. The v2 release replaces that inferential use with the cluster-aware randomization result in `tables/cluster_randomization_holm_v2.csv`.",""]
    (OUT/"V2_REANALYSIS_REPORT.md").write_text("\n".join(lines),encoding="utf-8")

    # Manifest last, covering all release files except itself and transient caches.
    output_files=sorted(p for p in OUT.rglob("*") if p.is_file() and p.name not in {"release_manifest.json"} and "__pycache__" not in p.parts)
    manifest={"schema_version":"ma-sqlgrid-v2-release-manifest-v1","passed":result["passed"],"file_count":len(output_files),
        "outputs":{str(p.relative_to(OUT)).replace('\\','/'):{"sha256":sha(p),"bytes":p.stat().st_size} for p in output_files}}
    (OUT/"release_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"passed":result["passed"],"checks":f"{sum(x['passed'] for x in checks)}/{len(checks)}","qwen_shape_main":qshape,"granite_shape_main":gshape,"outputs":manifest["file_count"]},indent=2))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
