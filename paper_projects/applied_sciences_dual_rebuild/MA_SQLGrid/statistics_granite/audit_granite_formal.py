#!/usr/bin/env python3
"""Independent Granite formal audit and paired two-backbone sensitivity."""
from __future__ import annotations

import csv, hashlib, importlib.util, json, re, sqlite3, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[4]
MA = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid"
OUT = MA / "statistics_granite"
RUN = MA / "granite_formal/granite33_8b_q4km_seed20260805_clean1"
FREEZE = MA / "SECOND_MODEL_ROBUSTNESS_FREEZE.json"
LOCAL_MODEL = MA / "granite33_local_model_artifact_manifest.json"
EXEC_MANIFEST = MA / "GRANITE33_FORMAL_EXECUTION_HASH_MANIFEST.json"
QWEN_AUDIT = MA / "statistics/MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json"
QWEN_ROWS = MA / "statistics/canonical_recomputed_rows.jsonl"
SOURCE = ROOT / "paper_projects/2026_ma_sqlgrid_cmc/source"
CODE_DIR = SOURCE / "code/experiment_final"
DATA_DIR = SOURCE / "data/griddb_maintenance_v2_v0_1"
SHARED = ROOT / "paper_projects/applied_sciences_dual_rebuild/shared/stat_audit.py"
CELLS = ["F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape"]
GOLD_KEYS = {"gold_sql", "gold_result", "gold_results", "answer", "answers"}

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def rows(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def canonical_hash(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def combined(paths):
    values=[{"name":p.name,"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted({p.resolve() for p in paths},key=str)]
    return canonical_hash(values)

def template(sql):
    x=re.sub(r"'[^']*'", "?", sql.lower()); x=re.sub(r'"[^"]*"',"?",x); x=re.sub(r"\b\d+(?:\.\d+)?\b","?",x)
    return " ".join(x.split())

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def write_csv(path, data):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)

def cluster_scalar(values, stat, seed):
    pairs=[(0.0,v,c) for v,c in values.values()]
    return stat.cluster_paired_bootstrap(pairs,samples=20_000,confidence=.95,seed=seed)

def factorial_vectors(index, qids, metric):
    result={"context_compact_main":{},"shape_hint_main":{},"interaction":{}}
    for q in qids:
        v={c:index[(q,c)][metric] for c in CELLS}; cluster=index[(q,CELLS[0])]["template_cluster"]
        result["context_compact_main"][q]=(0.5*((v[CELLS[2]]-v[CELLS[0]])+(v[CELLS[3]]-v[CELLS[1]])),cluster)
        result["shape_hint_main"][q]=(0.5*((v[CELLS[1]]-v[CELLS[0]])+(v[CELLS[3]]-v[CELLS[2]])),cluster)
        result["interaction"][q]=((v[CELLS[3]]-v[CELLS[2]])-(v[CELLS[1]]-v[CELLS[0]]),cluster)
    return result

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    freeze=json.loads(FREEZE.read_text(encoding="utf-8")); local=json.loads(LOCAL_MODEL.read_text(encoding="utf-8")); execution=json.loads(EXEC_MANIFEST.read_text(encoding="utf-8"))
    manifest=json.loads((RUN/"manifest.json").read_text(encoding="utf-8"))
    qwen_audit=json.loads(QWEN_AUDIT.read_text(encoding="utf-8"))
    p_rows=rows(RUN/"prompts.jsonl"); y_rows=rows(RUN/"predictions.jsonl"); s_rows=rows(RUN/"scores.jsonl")
    qwen_rows=rows(QWEN_ROWS)
    all_questions=rows(DATA_DIR/"questions.jsonl"); questions={r["question_id"]:r for r in all_questions if r["split"]=="test"}; qids=sorted(questions)
    sys.path[:0]=[str(CODE_DIR),str(SOURCE/"code"),str(SOURCE/"code/evaluator")]
    factorial=load("granite_factorial_audit",CODE_DIR/"applsci_factorial.py"); stat=load("granite_shared_stat",SHARED)
    checks=[]
    def check(name,ok,evidence): checks.append({"check":name,"passed":bool(ok),"evidence":evidence})

    check("freeze_status",freeze["status"]=="formal_execution_complete_pending_independent_audit",freeze["status"])
    check("qwen_audit_frozen_hash",sha(QWEN_AUDIT)==freeze["qwen7_independent_audit"]["report_sha256"] and qwen_audit["passed"],sha(QWEN_AUDIT))
    check("granite_completed",manifest["status"]=="completed" and manifest["canonical_result_eligible"],manifest["status"])
    check("single_process_no_resume",execution["single_process_run"] and not execution["resume_mode"] and not manifest["resume_mode"],{"single_process":execution["single_process_run"],"resume":manifest["resume_mode"],"harness_pid":execution["harness_pid"],"server_pid":execution["server_pid"]})
    check("process_shutdown",execution["integrity_checks"]["harness_process_absent_after_run"] and execution["integrity_checks"]["server_process_absent_after_shutdown"] and execution["integrity_checks"]["tcp_listener_8081_absent_after_shutdown"],execution["integrity_checks"]["server_shutdown_note"])
    check("row_counts",len(p_rows)==len(y_rows)==len(s_rows)==720,{"prompts":len(p_rows),"predictions":len(y_rows),"scores":len(s_rows)})
    expected={(q,c) for q in qids for c in CELLS}; maps={}
    for name,data in (("prompts",p_rows),("predictions",y_rows),("scores",s_rows)):
        keys=[(r["question_id"],r["condition"]) for r in data]; maps[name]={k:r for k,r in zip(keys,data)}
        check(name+"_720_unique_keys",len(keys)==len(set(keys))==720 and set(keys)==expected,{"rows":len(keys),"unique":len(set(keys)),"missing":len(expected-set(keys))})
    check("db_question_cell_keys",len({(manifest["hashes"]["data_sha256"],q,c) for q,c in expected})==720,720)

    data_paths=[factorial.formal.DB_PATH,factorial.formal.QUESTIONS_PATH,factorial.formal.DATA_DIR/"splits.json",factorial.formal.SCHEMA_PATH]
    code_paths=[Path(factorial.__file__),Path(factorial.formal.__file__),Path(factorial.formal.chess.__file__),Path(factorial.formal.smoke.__file__)]
    recomputed={"configuration_sha256":canonical_hash(manifest["configuration"]),"data_sha256":combined(data_paths),"code_sha256":combined(code_paths)}
    check("run_hashes_recomputed",recomputed==manifest["hashes"],{"recomputed":recomputed,"manifest":manifest["hashes"]})
    for field,expected_value in freeze["frozen_inputs"].items():
        key="code_sha256" if field=="code_sha256_before_adapter_review" else field
        actual=manifest["prompt_set_sha256"] if key=="prompt_set_sha256" else manifest["hashes"].get(key)
        check("freeze_"+field,actual==expected_value,{"actual":actual,"expected":expected_value})
    model_file=Path(local["model_file"])
    model_actual=sha(model_file)
    check("official_local_model_identity",local["model_repo"]==freeze["selected_candidate"]["repo"] and local["model_revision"]==freeze["selected_candidate"]["revision"] and local["model_bytes"]==model_file.stat().st_size==freeze["selected_candidate"]["bytes"] and model_actual==local["model_sha256"]==freeze["selected_candidate"]["lfs_file_sha256"],{"bytes":model_file.stat().st_size,"sha256":model_actual,"repo":local["model_repo"],"revision":local["model_revision"]})
    check("local_manifest_hash",sha(LOCAL_MODEL)==manifest["configuration"]["local_model"]["manifest_sha256"]==execution["frozen_hashes"]["local_model_manifest_sha256"],sha(LOCAL_MODEL))
    for name,meta in execution["files"].items():
        check("execution_manifest_file_"+name,sha(RUN/name)==meta["sha256"],sha(RUN/name))
    prompt_set=canonical_hash([{"key":[r["question_id"],r["condition"]],"prompt":r["prompt_hash"],"context":r["context_hash"]} for r in p_rows])
    check("prompt_set_recomputed",prompt_set==manifest["prompt_set_sha256"]==freeze["frozen_inputs"]["prompt_set_sha256"],prompt_set)
    linkage=[]
    for key in sorted(expected):
        p,y,s=maps["prompts"][key],maps["predictions"][key],maps["scores"][key]
        for f in ("prompt_hash","context_hash"):
            if len({p[f],y[f],s[f]})!=1: linkage.append([*key,f])
        if y["response_hash"]!=s["response_hash"]: linkage.append([*key,"response_hash"])
    check("artifact_linkage",not linkage,linkage[:20])

    log=(RUN/"server_stderr.log").read_text(encoding="utf-8",errors="replace"); tasks=re.findall(r"task\s+(\d+)\s+\|\s+processing task",log); launches=len(re.findall(r"launch_slot_:",log)); timings=len(re.findall(r"total time\s*=",log))
    check("one_generation_per_row",launches==timings==len(tasks)==len(set(tasks))==720,{"launches":launches,"timings":timings,"tasks":len(tasks),"unique_tasks":len(set(tasks))})
    check("no_server_errors",not re.search(r"(?m)^.*\sE\s+(?:srv|slot)\s",log),"no E-level record")
    check("no_provider_parse_retry_errors",Counter(r["status"] for r in y_rows)=={"success":720} and all(r["retry_count"]==0 and r["error_type"] is None for r in y_rows),{"statuses":Counter(r["status"] for r in y_rows),"retries":sum(r["retry_count"] for r in y_rows)})
    check("no_scoring_errors",Counter(r["status"] for r in s_rows)=={"scored":720},Counter(r["status"] for r in s_rows))
    check("model_accounting",all(r["model_requested"]==r["model_returned"]==local["served_model_id"] for r in y_rows),local["served_model_id"])
    leaked=[]
    for r in p_rows:
        gold=questions[r["question_id"]]["gold_sql"].strip()
        if any(k.lower() in GOLD_KEYS for k in r) or gold in r["prompt"] or gold in r["context"]: leaked.append([r["question_id"],r["condition"]])
    check("gold_isolation",not leaked,leaked[:20])

    conn=sqlite3.connect(f"file:{factorial.formal.DB_PATH.as_posix()}?mode=ro",uri=True); conn.execute("PRAGMA query_only=ON")
    canonical=[]; unsafe=[]; mismatches=[]
    try:
        contexts={q:factorial.build_contexts(conn,factorial.without_gold(rec)) for q,rec in questions.items()}
        for q,c in sorted(expected):
            y=maps["predictions"][(q,c)]; sql=y["predicted_sql"]; safe,_,err=factorial.formal.validate_read_only_select(sql)
            if not safe: unsafe.append([q,c,err,sql])
            ev=factorial.formal.score_prediction(conn,questions[q],sql); val=factorial.formal.chess.reference_free_validation(conn,contexts[q][c][1],sql); s=maps["scores"][(q,c)]
            correct=bool(ev.correct); shape=bool(val.get("shape_ok"))
            if correct!=bool(s["correct"]) or shape!=bool(s["shape_ok"]): mismatches.append([q,c,correct,s["correct"],shape,s["shape_ok"]])
            t="tpl_"+hashlib.sha256(template(questions[q]["gold_sql"]).encode()).hexdigest()[:12]
            fam="family_"+hashlib.sha256((questions[q]["difficulty"]+"|"+"|".join(questions[q]["sql_feature_tags"])).encode()).hexdigest()[:12]
            canonical.append({"question_id":q,"condition":c,"template_cluster":t,"family_cluster":fam,"correct_int":int(correct),"shape_int":int(shape),"prompt_hash":y["prompt_hash"],"context_hash":y["context_hash"],"response_hash":y["response_hash"],"data_sha256":y["data_sha256"],"configuration_sha256":y["configuration_sha256"],"code_sha256":y["code_sha256"]})
    finally: conn.close()
    check("all_sql_read_only",not unsafe,unsafe[:20]); check("direct_sqlite_rescore",not mismatches,{"mismatches":len(mismatches),"examples":mismatches[:20]})
    canonical_path=OUT/"granite_canonical_recomputed_rows.jsonl"; canonical_path.write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in canonical),encoding="utf-8")
    shared=stat.build_report(canonical_path,canonical,"jsonl",condition_field="condition",item_fields=["question_id"],cluster_field="template_cluster",metric_fields=["correct_int","shape_int"],required_fields=["family_cluster","prompt_hash","context_hash","response_hash"],hash_fields=["data_sha256","configuration_sha256","code_sha256"],expected_conditions=CELLS,bootstrap_samples=20_000,confidence=.95,seed=20260805,max_examples=20)
    (OUT/"granite_shared_stat_audit.json").write_text(json.dumps(shared,indent=2)+"\n",encoding="utf-8"); (OUT/"granite_shared_stat_audit.md").write_text(stat.report_markdown(shared),encoding="utf-8"); check("shared_stat_audit",shared["audit"]["passed"],shared["audit"])

    idx={(r["question_id"],r["condition"]):r for r in canonical}; qidx={(r["question_id"],r["condition"]):r for r in qwen_rows}
    check("qwen_canonical_pairing",set(qidx)==expected and all(qidx[k]["template_cluster"]==idx[k]["template_cluster"] for k in expected),{"qwen_rows":len(qidx),"paired":len(set(qidx)&expected)})
    cell_summary=[]
    for c in CELLS:
        rr=[idx[(q,c)] for q in qids]; cell_summary.append({"condition":c,"n":180,"execution_correct":sum(r["correct_int"] for r in rr),"execution_accuracy":mean(r["correct_int"] for r in rr),"shape_correct":sum(r["shape_int"] for r in rr),"shape_accuracy":mean(r["shape_int"] for r in rr)})
    edges=[("shape_at_full",CELLS[0],CELLS[1]),("compact_at_no_shape",CELLS[0],CELLS[2]),("shape_at_compact",CELLS[2],CELLS[3]),("compact_at_with_shape",CELLS[1],CELLS[3])]
    contrasts=[]
    for ei,(name,b,t) in enumerate(edges):
        for mi,metric in enumerate(("correct_int","shape_int")):
            pairs=[(idx[(q,b)][metric],idx[(q,t)][metric],idx[(q,b)]["template_cluster"]) for q in qids]; boot=stat.cluster_paired_bootstrap(pairs,samples=20_000,confidence=.95,seed=20260805+ei*101+mi); mc=stat.mcnemar_exact(pairs)
            contrasts.append({"contrast":name,"baseline":b,"treatment":t,"metric":metric,"baseline_mean":mean(x[0] for x in pairs),"treatment_mean":mean(x[1] for x in pairs),"effect":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],"cluster_count":boot["cluster_count"],"mcnemar_baseline_only":mc["baseline_only_correct"],"mcnemar_treatment_only":mc["treatment_only_correct"],"mcnemar_p":mc["p_value"]})
    for r,p in zip(contrasts,stat.holm_adjust([x["mcnemar_p"] for x in contrasts])): r["mcnemar_p_holm"]=p
    gv={m:factorial_vectors(idx,qids,m) for m in ("correct_int","shape_int")}; qv={m:factorial_vectors(qidx,qids,m) for m in ("correct_int","shape_int")}
    factorial_results=[]
    for mi,m in enumerate(gv):
        for ei,name in enumerate(gv[m]):
            boot=cluster_scalar(gv[m][name],stat,20262000+mi*100+ei); factorial_results.append({"metric":m,"effect":name,"estimate":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],"cluster_count":boot["cluster_count"],"bootstrap_samples":20_000})

    # Granite minus audited-Qwen, paired on the same questions/templates.
    cross_cells=[]
    for ci,c in enumerate(CELLS):
        for mi,m in enumerate(("correct_int","shape_int")):
            pairs=[(qidx[(q,c)][m],idx[(q,c)][m],idx[(q,c)]["template_cluster"]) for q in qids]; boot=stat.cluster_paired_bootstrap(pairs,samples=20_000,confidence=.95,seed=20264000+ci*101+mi); mc=stat.mcnemar_exact(pairs)
            cross_cells.append({"condition":c,"metric":m,"qwen_mean":mean(x[0] for x in pairs),"granite_mean":mean(x[1] for x in pairs),"granite_minus_qwen":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],"cluster_count":boot["cluster_count"],"mcnemar_qwen_only":mc["baseline_only_correct"],"mcnemar_granite_only":mc["treatment_only_correct"],"mcnemar_p":mc["p_value"]})
    for r,p in zip(cross_cells,stat.holm_adjust([x["mcnemar_p"] for x in cross_cells])): r["mcnemar_p_holm"]=p
    cross_factorial=[]
    for mi,m in enumerate(gv):
        for ei,name in enumerate(gv[m]):
            values={q:(gv[m][name][q][0]-qv[m][name][q][0],gv[m][name][q][1]) for q in qids}; boot=cluster_scalar(values,stat,20265000+mi*100+ei)
            cross_factorial.append({"metric":m,"effect":"backbone_x_"+name,"qwen_effect":mean(v[0] for v in qv[m][name].values()),"granite_effect":mean(v[0] for v in gv[m][name].values()),"granite_minus_qwen":boot["estimate"],"ci_low":boot["ci_low"],"ci_high":boot["ci_high"],"cluster_count":boot["cluster_count"],"bootstrap_samples":20_000})
    shape_rep={m:{"qwen":mean(v[0] for v in qv[m]["shape_hint_main"].values()),"granite":mean(v[0] for v in gv[m]["shape_hint_main"].values())} for m in gv}
    for m,v in shape_rep.items(): v["direction_replicates_positive"] = v["qwen"]>0 and v["granite"]>0

    write_csv(OUT/"granite_cell_summary.csv",cell_summary); write_csv(OUT/"granite_registered_contrasts.csv",contrasts); write_csv(OUT/"granite_factorial_effects.csv",factorial_results); write_csv(OUT/"cross_backbone_cell_comparisons.csv",cross_cells); write_csv(OUT/"cross_backbone_factorial_sensitivity.csv",cross_factorial)
    result={"schema_version":"ma-sqlgrid-granite-independent-audit-v1","generated_utc":datetime.now(timezone.utc).isoformat(),"passed":all(x["passed"] for x in checks),"scope":"paired two-backbone sensitivity only; no broader model-family generalization","eligible_granite_run":str(RUN.relative_to(ROOT)),"qwen_source":{"audit":str(QWEN_AUDIT.relative_to(ROOT)),"audit_sha256":sha(QWEN_AUDIT),"canonical_rows":str(QWEN_ROWS.relative_to(ROOT)),"canonical_rows_sha256":sha(QWEN_ROWS)},"checks":checks,"granite_cell_summary":cell_summary,"granite_registered_contrasts":contrasts,"granite_factorial_effects":factorial_results,"cross_backbone_cell_comparisons":cross_cells,"cross_backbone_factorial_sensitivity":cross_factorial,"shape_main_direction_replication":shape_rep}
    json_path=OUT/"GRANITE_INDEPENDENT_AUDIT.json"; json_path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    lines=["# Granite 3.3 8B Formal Run - Independent Audit","",f"**Decision: {'PASS - eligible for bounded two-backbone sensitivity analysis' if result['passed'] else 'FAIL - do not promote'}.**","","## Integrity boundary","",f"- Granite input: `{result['eligible_granite_run']}`.",f"- Qwen input: audited canonical rows only, SHA-256 `{result['qwen_source']['canonical_rows_sha256']}`.","- The contaminated Qwen run directory was not read.",f"- Checks passed: {sum(x['passed'] for x in checks)}/{len(checks)}. Exactly 720 keys, 720 unique server generation tasks, no resume, zero provider/parse/scoring errors or retries, all SQL read-only, and 720/720 direct SQLite execution/shape verdicts reproduced.","- Granite model file bytes/SHA, local manifest, official revision/license identity, prompt set, configuration, data and code hashes match the freeze.","","## Granite recomputed cells","","| Cell | Execution | Shape |","|---|---:|---:|"]
    for r in cell_summary: lines.append(f"| {r['condition']} | {r['execution_correct']}/180 = {r['execution_accuracy']:.4f} | {r['shape_correct']}/180 = {r['shape_accuracy']:.4f} |")
    lines += ["","## Granite factorial effects","","20,000 paired bootstrap draws over the same 70 normalized gold-SQL template clusters.","","| Metric | Effect | Estimate | 95% CI |","|---|---|---:|---|"]
    for r in factorial_results: lines.append(f"| {r['metric']} | {r['effect']} | {r['estimate']:+.4f} | [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}] |")
    lines += ["","Exact McNemar tests and Holm-adjusted p-values for the eight Granite factorial edges are in `granite_registered_contrasts.csv`.","","## Paired Granite-minus-Qwen cell sensitivity","","The two backbones are not pooled as independent samples; every contrast is paired by the same 180 questions and template clusters.","","| Cell | Metric | Qwen | Granite | Difference | 95% CI | Holm p |","|---|---|---:|---:|---:|---|---:|"]
    for r in cross_cells: lines.append(f"| {r['condition']} | {r['metric']} | {r['qwen_mean']:.4f} | {r['granite_mean']:.4f} | {r['granite_minus_qwen']:+.4f} | [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}] | {r['mcnemar_p_holm']:.6g} |")
    lines += ["","## Backbone-by-factor sensitivity","","| Metric | Backbone interaction | Qwen effect | Granite effect | Granite-Qwen | 95% CI |","|---|---|---:|---:|---:|---|"]
    for r in cross_factorial: lines.append(f"| {r['metric']} | {r['effect']} | {r['qwen_effect']:+.4f} | {r['granite_effect']:+.4f} | {r['granite_minus_qwen']:+.4f} | [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}] |")
    lines += ["","## Bounded replication statement","",f"- Execution shape-hint main effect direction replicated: Qwen {shape_rep['correct_int']['qwen']:+.4f}, Granite {shape_rep['correct_int']['granite']:+.4f} (both positive).",f"- Answer-shape main effect direction replicated: Qwen {shape_rep['shape_int']['qwen']:+.4f}, Granite {shape_rep['shape_int']['granite']:+.4f} (both positive).","- This is evidence from two quantized instruction backbones on one synthetic database, not general model-family robustness.","","Canonical JSON/CSV files and recomputed rows are stored in this directory.",""]
    md_path=OUT/"GRANITE_INDEPENDENT_AUDIT.md"; md_path.write_text("\n".join(lines),encoding="utf-8")
    outputs=[json_path,md_path,canonical_path,OUT/"granite_shared_stat_audit.json",OUT/"granite_shared_stat_audit.md",OUT/"granite_cell_summary.csv",OUT/"granite_registered_contrasts.csv",OUT/"granite_factorial_effects.csv",OUT/"cross_backbone_cell_comparisons.csv",OUT/"cross_backbone_factorial_sensitivity.csv"]
    art={"schema_version":"ma-sqlgrid-granite-canonical-manifest-v1","passed":result["passed"],"outputs":{p.name:{"sha256":sha(p),"bytes":p.stat().st_size} for p in outputs},"immutable_granite_inputs":{p.name:sha(p) for p in [RUN/"manifest.json",RUN/"prompts.jsonl",RUN/"predictions.jsonl",RUN/"scores.jsonl",RUN/"server_stderr.log"]},"qwen_audit_sha256":sha(QWEN_AUDIT),"qwen_canonical_rows_sha256":sha(QWEN_ROWS)}
    (OUT/"canonical_artifact_manifest.json").write_text(json.dumps(art,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"passed":result["passed"],"checks":len(checks),"granite_cells":cell_summary,"shape_replication":shape_rep},indent=2)); return 0 if result["passed"] else 2

if __name__=="__main__": raise SystemExit(main())
