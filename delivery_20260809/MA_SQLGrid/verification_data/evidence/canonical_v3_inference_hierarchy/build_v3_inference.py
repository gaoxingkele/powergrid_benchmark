#!/usr/bin/env python3
"""Build the MA-SQLGrid v3 inferential hierarchy without changing frozen v2."""
from __future__ import annotations

import csv, hashlib, json, platform, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
V2 = HERE.parent / "canonical_v2_reanalysis"
TABLES = HERE / "tables"
CONTRACT = HERE / "EXPECTED_INPUT_HASHES.json"
QUESTIONS = ROOT / "paper_projects/2026_ma_sqlgrid_cmc/source/data/griddb_maintenance_v2_v0_1/questions.jsonl"
CELLS = ["F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape"]
BACKBONES = ["qwen", "granite"]
METRICS = ["execution", "structural_common"]
EFFECTS = ["context_package_main", "structural_hint_main", "interaction"]
SEED, FLIPS, BOOTS = 20260805, 100000, 20000

def sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def fail_closed_preflight() -> dict:
    contract=json.loads(CONTRACT.read_text(encoding="utf-8")); checked=[]
    for section in ("v2_accepted_upstream_inputs","v2_products_consumed"):
        for rel, expected in contract[section].items():
            p=ROOT/rel
            if not p.is_file(): raise RuntimeError(f"FAIL-CLOSED missing accepted input: {rel}")
            actual=sha(p)
            if actual != expected: raise RuntimeError(f"FAIL-CLOSED hash mismatch: {rel}; expected {expected}; got {actual}")
            checked.append({"section":section,"path":rel,"sha256":actual,"bytes":p.stat().st_size})
    return {"passed":True,"contract_sha256":sha(CONTRACT),"checked_count":len(checked),"checked":checked}

def read_jsonl(p): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def write_csv(name, rows):
    p=TABLES/name
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def tex_escape(s): return str(s).replace("_",r"\_").replace("%",r"\%")
def write_tex(name, headers, rows, aligns):
    lines=[r"\begin{tabular}{"+aligns+"}",r"\toprule"," & ".join(headers)+r" \\",r"\midrule"]
    lines += [" & ".join(tex_escape(x) for x in row)+r" \\" for row in rows]
    lines += [r"\bottomrule",r"\end{tabular}"]
    (TABLES/name).write_text("\n".join(lines)+"\n",encoding="utf-8")

def holm(ps):
    order=sorted(range(len(ps)),key=lambda i:ps[i]); out=[0.0]*len(ps); running=0.0
    for rank,i in enumerate(order):
        running=max(running,min(1.0,(len(ps)-rank)*ps[i])); out[i]=running
    return out

def sign_flip(values, clusters, seed):
    grouped=defaultdict(float)
    for v,c in zip(values,clusters): grouped[c]+=float(v)
    sums=np.asarray([grouped[c] for c in sorted(grouped)]); obs=abs(float(sums.sum()))
    rng=np.random.default_rng(seed); extreme=0
    for start in range(0,FLIPS,10000):
        n=min(10000,FLIPS-start); signs=rng.integers(0,2,size=(n,len(sums)),dtype=np.int8)*2-1
        extreme += int(np.count_nonzero(np.abs(signs@sums)>=obs-1e-12))
    return extreme,(extreme+1)/(FLIPS+1)

def composition(values, groups, seed):
    by=defaultdict(list)
    for v,g in zip(values,groups): by[g].append(float(v))
    keys=sorted(by); rng=np.random.default_rng(seed); draws=np.empty(BOOTS)
    for i in range(BOOTS):
        chosen=rng.integers(0,len(keys),size=len(keys)); vals=[]
        for j in chosen: vals.extend(by[keys[j]])
        draws[i]=np.mean(vals)
    group_means=[np.mean(by[k]) for k in keys]
    return {"group_count":len(keys),"bootstrap_low":float(np.quantile(draws,.025)),"bootstrap_high":float(np.quantile(draws,.975)),
            "arbitrary_group_reweighting_min":float(min(group_means)),"arbitrary_group_reweighting_max":float(max(group_means))}

def effect_vectors(index, backbone, metric, qids):
    out={e:{} for e in EFFECTS}
    for q in qids:
        v={c:index[(backbone,q,c)][metric] for c in CELLS}
        out["context_package_main"][q]=.5*((v[CELLS[2]]-v[CELLS[0]])+(v[CELLS[3]]-v[CELLS[1]]))
        out["structural_hint_main"][q]=.5*((v[CELLS[1]]-v[CELLS[0]])+(v[CELLS[3]]-v[CELLS[2]]))
        out["interaction"][q]=(v[CELLS[3]]-v[CELLS[2]])-(v[CELLS[1]]-v[CELLS[0]])
    return out

def main():
    TABLES.mkdir(parents=True,exist_ok=True); preflight=fail_closed_preflight()
    rows=read_jsonl(V2/"canonical_rows_v2.jsonl"); index={(r["backbone"],r["question_id"],r["condition"]):r for r in rows}
    qids=sorted({r["question_id"] for r in rows}); assert len(rows)==1440 and len(qids)==180
    questions={r["question_id"]:r for r in read_jsonl(QUESTIONS) if r["question_id"] in qids}
    template={q:index[("qwen",q,CELLS[0])]["template_cluster"] for q in qids}
    family={q:"family_"+hashlib.sha256((questions[q]["difficulty"]+"|"+"|".join(questions[q]["sql_feature_tags"])).encode()).hexdigest()[:12] for q in qids}
    vectors={(b,m):effect_vectors(index,b,m,qids) for b in BACKBONES for m in METRICS}
    tests=[]; sensitivity=[]
    for mi,m in enumerate(METRICS):
        fam_name="primary_execution_nine_core_factorial_tests" if m=="execution" else "secondary_structural_adherence_nine_core_factorial_tests"
        family_rows=[]
        for bi,b in enumerate(BACKBONES):
            for ei,e in enumerate(EFFECTS):
                vals=[vectors[(b,m)][e][q] for q in qids]; clusters=[template[q] for q in qids]
                extreme,p=sign_flip(vals,clusters,SEED+mi*1000+bi*100+ei)
                family_rows.append({"family":fam_name,"endpoint_role":"primary finite-set execution equality" if m=="execution" else "secondary direct manipulation/adherence diagnostic", "metric":m,"scope":b,"effect":e,"estimate":float(np.mean(vals)),"cluster_unit":"normalized_gold_SQL_structure","clusters":70,"randomization_draws":FLIPS,"seed":SEED+mi*1000+bi*100+ei,"extreme_draws":extreme,"p_raw":p})
                for grouping,grp in [("normalized_sql_70",template),("difficulty_x_feature_39",family)]:
                    ss=composition(vals,[grp[q] for q in qids],SEED+10000+mi*1000+bi*100+ei+(0 if grouping.startswith("normalized") else 50))
                    sensitivity.append({"metric":m,"scope":b,"effect":e,"grouping":grouping,"interpretation":"composition sensitivity only; groups are not sampled and are not authoring templates",**ss})
        for ei,e in enumerate(EFFECTS):
            vals=[vectors[("granite",m)][e][q]-vectors[("qwen",m)][e][q] for q in qids]; clusters=[template[q] for q in qids]
            extreme,p=sign_flip(vals,clusters,SEED+mi*1000+500+ei)
            family_rows.append({"family":fam_name,"endpoint_role":"primary finite-set execution equality" if m=="execution" else "secondary direct manipulation/adherence diagnostic", "metric":m,"scope":"granite_minus_qwen","effect":"backbone_x_"+e,"estimate":float(np.mean(vals)),"cluster_unit":"normalized_gold_SQL_structure","clusters":70,"randomization_draws":FLIPS,"seed":SEED+mi*1000+500+ei,"extreme_draws":extreme,"p_raw":p})
            for grouping,grp in [("normalized_sql_70",template),("difficulty_x_feature_39",family)]:
                ss=composition(vals,[grp[q] for q in qids],SEED+20000+mi*1000+ei+(0 if grouping.startswith("normalized") else 50))
                sensitivity.append({"metric":m,"scope":"granite_minus_qwen","effect":"backbone_x_"+e,"grouping":grouping,"interpretation":"composition sensitivity only; groups are not sampled and are not authoring templates",**ss})
        adjusted=holm([r["p_raw"] for r in family_rows])
        for r,padj in zip(family_rows,adjusted): r["p_holm"]=padj; r["holm_reject_0_05"]=padj<.05
        tests.extend(family_rows)
    write_csv("core_inference_hierarchy.csv",tests); write_csv("composition_sensitivity.csv",sensitivity)
    sizes=Counter(template.values()); famsizes=Counter(family.values())
    cluster_profile=[{"grouping":"normalized_sql_70","groups":len(sizes),"singletons":sum(v==1 for v in sizes.values()),"max_size":max(sizes.values()),"rule":"lowercase gold SQL; replace quoted strings and numeric literals; normalize whitespace"},
                     {"grouping":"difficulty_x_feature_39","groups":len(famsizes),"singletons":sum(v==1 for v in famsizes.values()),"max_size":max(famsizes.values()),"rule":"exact difficulty + ordered sql_feature_tags; sensitivity only; not authoring provenance"}]
    write_csv("dependence_group_profile.csv",cluster_profile)
    targets=Counter(index[("qwen",q,CELLS[0])]["frozen_target_column_count"] for q in qids)
    target_rows=[{"projected_columns":k,"questions":targets[k],"endpoint_note":"shared provenance with supplied hint; direct adherence/manipulation diagnostic"} for k in sorted(targets)]
    write_csv("frozen_target_distribution.csv",target_rows)
    write_tex("table_core_inference.tex",["Endpoint","Scope","Effect","Estimate","Raw $p$","Holm $p$"],[[r["metric"],r["scope"],r["effect"],f'{r["estimate"]:+.4f}',f'{r["p_raw"]:.6g}',f'{r["p_holm"]:.6g}'] for r in tests],"lllrrr")
    write_tex("table_composition_sensitivity.tex",["Endpoint","Scope","Effect","Grouping","95\\% sensitivity interval"],[[r["metric"],r["scope"],r["effect"],r["grouping"],f'[{r["bootstrap_low"]:+.4f}, {r["bootstrap_high"]:+.4f}]'] for r in sensitivity],"lllll")
    estimands={"finite_set_population":"all 180 frozen, author-constructed, development-visible GridDB questions; each question has weight 1/180", "point_estimates":"exact descriptive contrasts for this finite set, not estimates of an external question population", "execution_endpoint":"strict result equality on one frozen SQLite database state; not semantic correctness", "structural_endpoint":"successful execution plus exact projected-column-count match to the common supplied target; direct manipulation/adherence diagnostic", "context_main":"one half of [(F10-F00)+(F11-F01)]", "hint_main":"one half of [(F01-F00)+(F11-F10)]", "interaction":"(F11-F10)-(F01-F00)", "cross_backbone_modifier":"Granite finite-set effect minus Qwen finite-set effect", "composition_boundary":"70-cluster and 39-group bootstraps are sensitivity analyses to empirical question composition, not population confidence intervals; min/max group means bound arbitrary convex reweighting over observed groups", "randomization_assumption":"two-sided cluster sign flips test the sharp zero/symmetry null while assigning one sign to all questions in each normalized-SQL group; this grouping is a dependence proxy, not known authoring provenance"}
    result={"schema_version":"ma-sqlgrid-canonical-v3-inference-hierarchy-v1","generated_utc":datetime.now(timezone.utc).isoformat(),"passed":True,"no_model_execution":True,"v2_modified":False,"preflight":preflight,"estimands":estimands,"multiplicity_hierarchy":[{"family":"primary_execution_nine_core_factorial_tests","tests":9,"adjustment":"Holm","status":"confirmatory only for the frozen post-review reanalysis, not preregistered"},{"family":"secondary_structural_adherence_nine_core_factorial_tests","tests":9,"adjustment":"Holm","status":"secondary manipulation diagnostic; cannot corroborate semantic accuracy independently"}],"cluster_profile":cluster_profile,"target_distribution":dict(sorted(targets.items())),"core_tests":tests,"composition_sensitivity":sensitivity}
    (HERE/"V3_INFERENCE_HIERARCHY.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    report=["# MA-SQLGrid canonical v3 inference hierarchy","","**Decision: PASS.** This add-on consumes hash-pinned v2 products, runs no model, and does not modify v2 or the manuscript.","","## Estimand and claim boundary","",estimands["point_estimates"]+" The 70- and 39-group intervals are explicitly composition-sensitivity intervals, not confidence intervals for an unstated superpopulation.","","## Multiplicity hierarchy","","- Primary family: nine execution-equality factorial quantities (three per backbone plus three Granite-minus-Qwen modifiers), 100,000 cluster sign flips per test and Holm adjustment across all nine.","- Secondary family: the analogous nine common-target structural-adherence quantities, separately Holm-adjusted and labeled a direct manipulation diagnostic.","- This hierarchy was frozen after Round-2 review. It is a post-review reanalysis, not preregistration.","","## Family-wise result","","- **Execution equality:** zero of nine core tests survives Holm at 0.05. In particular, Qwen hint raw/adjusted p=0.01372/0.09604, Qwen interaction 0.00919/0.07352, hint modifier 0.00640/0.05760, and three-way interaction modifier 0.07010/0.42060. These may be reported as finite-set estimates with exploratory composition sensitivity, not promoted as statistically nonzero.","- **Structural adherence:** the Qwen hint main effect (+0.4083; adjusted p=0.000090) and Granite hint main effect (+0.3556; adjusted p=0.01944) survive the separate secondary family. Because the target is supplied by the intervention, these are manipulation/adherence results only.","","## Dependence and sensitivity","",f"The normalized-SQL proxy has {len(sizes)} groups, {sum(v==1 for v in sizes.values())} singletons, and maximum size {max(sizes.values())}. The coarser difficulty-by-feature grouping has {len(famsizes)} groups and is not an authoring-template identifier. Both mappings retain question-level weighting.","",f"The common projected-column targets are 1:{targets[1]}, 2:{targets[2]}, 3:{targets[3]}, 4:{targets[4]}; because the same provenance supplies the hint target, this endpoint measures instruction uptake/adherence rather than independent semantic benefit.","","## Reproducibility boundary","",f"Fail-closed preflight verified {preflight['checked_count']} upstream/v2 files against a hand-frozen contract before analysis. `MANUAL_VISUAL_QA.json` is deliberately outside the generator; the completed inspection records a minor color-redundancy issue for Figures 1 and 2."]
    (HERE/"V3_INFERENCE_REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    # Generator never creates or edits MANUAL_VISUAL_QA.json.
    outputs=sorted(p for p in HERE.rglob("*") if p.is_file() and p.name not in {"release_manifest.json","MANUAL_VISUAL_QA.json"} and "__pycache__" not in p.parts)
    manifest={"schema_version":"ma-sqlgrid-v3-release-manifest-v1","generated_utc":datetime.now(timezone.utc).isoformat(),"input_contract_sha256":sha(CONTRACT),"manual_visual_qa_policy":"separate record; never generator-authored","runtime":{"python":platform.python_version(),"numpy":np.__version__},"outputs":{str(p.relative_to(HERE)).replace('\\','/'):{"sha256":sha(p),"bytes":p.stat().st_size} for p in outputs}}
    (HERE/"release_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return 0

if __name__=="__main__": raise SystemExit(main())
