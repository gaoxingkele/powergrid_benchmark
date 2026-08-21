#!/usr/bin/env python3
"""Frozen atomic-to-suite/statistics/table/figure analysis for v3."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,random
from collections import defaultdict
from pathlib import Path
from typing import Any

BACKBONES=["qwen","granite"];CELLS=["F00_Full_NoShape","F01_Full_WithShape","F10_Compact_NoShape","F11_Compact_WithShape"]
EXPECTED_ATOMIC=25920;EXPECTED_PRIMARY_STATE_ROWS=7920;EXPECTED_HOLD_ROWS=16416;EXPECTED_SUITE=1440;EXPECTED_PRIMARY_PREDICTIONS=528;SEED=20260805;RANDOMIZATION_SAMPLES=100000;BOOTSTRAP_SAMPLES=20000
def sha(p:Path):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def load_jsonl(p):return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
def write_jsonl(p,rows):
 with Path(p).open("w",encoding="utf-8",newline="\n") as f:
  for r in rows:f.write(json.dumps(r,sort_keys=True,ensure_ascii=False)+"\n")
def write_csv(p,rows):
 with Path(p).open("w",encoding="utf-8-sig",newline="") as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def holm(pvals):
 order=sorted(range(len(pvals)),key=lambda i:pvals[i]);out=[0.0]*len(pvals);running=0.0;m=len(pvals)
 for rank,i in enumerate(order):running=max(running,min(1.0,(m-rank)*pvals[i]));out[i]=running
 return out
def validate_atomic(rows,state_partition):
 semantic=set(state_partition["semantic_suite_states"]);physical=set(state_partition["physical_order_diagnostic_states"]);allstates=semantic|physical
 if len(semantic)!=15 or len(physical)!=3 or semantic&physical:raise ValueError("state partition must be disjoint 15+3")
 if len(rows)!=EXPECTED_ATOMIC:raise ValueError(f"atomic rows {len(rows)} != {EXPECTED_ATOMIC}")
 keys={(r["backbone"],r["condition"],r["question_id"],r["state"]) for r in rows}
 if len(keys)!=EXPECTED_ATOMIC:raise ValueError("atomic keys not unique")
 if {r["state"] for r in rows}!=allstates:raise ValueError("state set mismatch")
 primary=[r for r in rows if r["automatic_primary_eligible"] and r["state"] in semantic]
 holds=[r for r in rows if not r["automatic_primary_eligible"]]
 if len(primary)!=EXPECTED_PRIMARY_STATE_ROWS:raise ValueError(f"primary semantic rows {len(primary)}")
 if len(holds)!=EXPECTED_HOLD_ROWS:raise ValueError(f"order-hold rows {len(holds)}")
 if any(r["automatic_primary_eligible"] and r["state"] in physical and r.get("primary_semantic_state",False) for r in rows):raise ValueError("physical state entered primary")
 return semantic,physical
def aggregate_suite(rows,state_partition,canonical_execution):
 semantic,physical=validate_atomic(rows,state_partition);groups=defaultdict(list)
 for r in rows:groups[(r["backbone"],r["condition"],r["question_id"])].append(r)
 if len(groups)!=EXPECTED_SUITE:raise ValueError("suite group count")
 out=[]
 for key,rr in sorted(groups.items()):
  elig=bool(rr[0]["automatic_primary_eligible"]);sem=[r for r in rr if r["state"] in semantic];phy=[r for r in rr if r["state"] in physical];snap=[r for r in rr if r["state"]=="T0_snapshot"]
  if len(sem)!=15 or len(phy)!=3 or len(snap)!=1:raise ValueError(f"state denominator {key}")
  ckey="|".join(key);snapshot=bool(snap[0]["tolerant_denotation_agreement"])
  if snapshot!=bool(canonical_execution[ckey]):raise ValueError(f"snapshot inconsistency {ckey}")
  out.append({"backbone":key[0],"condition":key[1],"question_id":key[2],"automatic_primary_eligible":elig,"order_hold":not elig,"snapshot_agreement":snapshot,"semantic_state_n":15,"physical_diagnostic_state_n":3,"suite_15state_and":bool(all(r["tolerant_denotation_agreement"] for r in sem)) if elig else None,"strict_suite_15state_and":bool(all(r["strict_denotation_agreement"] for r in sem)) if elig else None,"order_hold_all18_diagnostic":bool(all(r["tolerant_denotation_agreement"] for r in rr)) if not elig else None,"execution_error_any":any(not r["prediction_ok"] for r in rr)})
 if sum(r["automatic_primary_eligible"] for r in out)!=EXPECTED_PRIMARY_PREDICTIONS:raise ValueError("primary prediction denominator")
 return out
def effect_vectors(index):
 out={}
 for b in BACKBONES:
  by={c:{q:index[(b,c,q)] for q in {k[2] for k in index if k[0]==b}} for c in CELLS}
  out[(b,"hint")]=[(q,((by[CELLS[1]][q]-by[CELLS[0]][q])+(by[CELLS[3]][q]-by[CELLS[2]][q]))/2) for q in by[CELLS[0]]]
  out[(b,"compact")]=[(q,((by[CELLS[2]][q]-by[CELLS[0]][q])+(by[CELLS[3]][q]-by[CELLS[1]][q]))/2) for q in by[CELLS[0]]]
  out[(b,"interaction")]=[(q,(by[CELLS[3]][q]-by[CELLS[2]][q])-(by[CELLS[1]][q]-by[CELLS[0]][q])) for q in by[CELLS[0]]]
 for effect in ["hint","compact","interaction"]:
  qv={q:v for q,v in out[("qwen",effect)]};gv={q:v for q,v in out[("granite",effect)]};out[("granite_minus_qwen",effect)]=[(q,gv[q]-qv[q]) for q in sorted(qv)]
 return out
def randomization(values,clusters,seed):
 grouped=defaultdict(list)
 for q,v in values:grouped[clusters[q]].append(v)
 est=sum(v for _,v in values)/len(values);rng=random.Random(seed);extreme=0;keys=sorted(grouped)
 for _ in range(RANDOMIZATION_SAMPLES):
  signs={k:(1 if rng.getrandbits(1) else -1) for k in keys};stat=sum(signs[clusters[q]]*v for q,v in values)/len(values);extreme+=abs(stat)>=abs(est)-1e-15
 return est,(extreme+1)/(RANDOMIZATION_SAMPLES+1)
def bootstrap(values,clusters,seed):
 grouped=defaultdict(list)
 for q,v in values:grouped[clusters[q]].append(v)
 keys=sorted(grouped);rng=random.Random(seed);draw=[]
 for _ in range(BOOTSTRAP_SAMPLES):
  vals=[]
  for _j in keys:vals.extend(grouped[rng.choice(keys)])
  draw.append(sum(vals)/len(vals))
 draw.sort();return draw[int(.025*len(draw))],draw[min(len(draw)-1,int(.975*len(draw)))]
def analyze(atom_path,freeze_path,cluster_path,canonical_path,outdir):
 outdir.mkdir(parents=True,exist_ok=True);freeze=json.loads(freeze_path.read_text());clusters=json.loads(cluster_path.read_text())["mapping"];canonical_rows=load_jsonl(canonical_path);canonical={f'{r["backbone"]}|{r["condition"]}|{r["question_id"]}':bool(r["execution"]) for r in canonical_rows}
 atom=load_jsonl(atom_path);suite=aggregate_suite(atom,freeze["stage_a"],canonical);suite_path=outdir/"suite_outcomes.jsonl";write_jsonl(suite_path,suite);suite_csv=outdir/"suite_outcomes.csv";write_csv(suite_csv,suite)
 primary=[r for r in suite if r["automatic_primary_eligible"]];index={(r["backbone"],r["condition"],r["question_id"]):int(r["suite_15state_and"]) for r in primary};vectors=effect_vectors(index);stats=[]
 for i,key in enumerate([(b,e) for b in BACKBONES for e in ["hint","compact","interaction"]]+[("granite_minus_qwen",e) for e in ["hint","compact","interaction"]]):
  est,p=randomization(vectors[key],clusters,SEED+1000+i);lo,hi=bootstrap(vectors[key],clusters,SEED+10000+i);stats.append({"family_index":i+1,"backbone_or_modifier":key[0],"effect":key[1],"estimate":est,"composition_sensitivity_low":lo,"composition_sensitivity_high":hi,"cluster_randomization_p_raw":p,"cluster_n":len({clusters[q] for q,_ in vectors[key]}),"question_n":66,"randomization_samples":RANDOMIZATION_SAMPLES,"bootstrap_samples":BOOTSTRAP_SAMPLES,"seed":SEED})
 adjusted=holm([r["cluster_randomization_p_raw"] for r in stats])
 for r,p in zip(stats,adjusted):r["holm_family_size"]=9;r["cluster_randomization_p_holm"]=p
 stats_path=outdir/"clustered_contrasts.csv";write_csv(stats_path,stats)
 tex=outdir/"clustered_contrasts.tex";tex.write_text("% source_sha256="+sha(stats_path)+"\n\\begin{tabular}{llrrr}\nBackbone & Effect & Estimate & Raw $p$ & Holm $p$ \\\\\n\\hline\n"+"\n".join(f'{r["backbone_or_modifier"]} & {r["effect"]} & {r["estimate"]:.4f} & {r["cluster_randomization_p_raw"]:.4f} & {r["cluster_randomization_p_holm"]:.4f} \\\\' for r in stats)+"\n\\end{tabular}\n",encoding="utf-8")
 svg=outdir/"semantic_suite_effects.svg";svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420"><metadata>source_sha256={sha(stats_path)}</metadata><rect width="100%" height="100%" fill="white"/><text x="30" y="35" font-family="sans-serif" font-size="20">15-state suite effects (66-question finite corpus)</text>'+''.join(f'<text x="40" y="{70+i*35}" font-family="sans-serif" font-size="15">{r["backbone_or_modifier"]} {r["effect"]}: {r["estimate"]:.3f} (Holm p={r["cluster_randomization_p_holm"]:.3f})</text>' for i,r in enumerate(stats))+'</svg>',encoding="utf-8")
 summary={"schema_version":"ma-sqlgrid-semantic-analysis-v3","freeze_content_sha256":freeze["freeze_content_sha256"],"atomic_rows":len(atom),"suite_rows":len(suite),"primary_predictions":len(primary),"order_hold_predictions":sum(r["order_hold"] for r in suite),"primary_semantic_state_rows":EXPECTED_PRIMARY_STATE_ROWS,"order_hold_diagnostic_rows":EXPECTED_HOLD_ROWS,"semantic_state_and":15,"physical_order_states_diagnostic":3,"contrast_family_n":9,"holm_family_n":9,"finite_corpus_question_n":66,"randomization_samples":RANDOMIZATION_SAMPLES,"bootstrap_samples":BOOTSTRAP_SAMPLES,"seed_base":SEED,"lineage":{"atomic_scores_sha256":sha(atom_path),"suite_outcomes_sha256":sha(suite_path),"suite_outcomes_csv_sha256":sha(suite_csv),"clustered_contrasts_sha256":sha(stats_path),"table_tex_source_sha256":sha(stats_path),"figure_svg_source_sha256":sha(stats_path)}};(outdir/"ANALYSIS_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8");print("ANALYSIS_V3_COMPLETE",len(atom),len(primary))
def main():
 p=argparse.ArgumentParser();p.add_argument("--atomic",type=Path,required=True);p.add_argument("--freeze",type=Path,required=True);p.add_argument("--cluster-map",type=Path,required=True);p.add_argument("--canonical-rows",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args();analyze(a.atomic,a.freeze,a.cluster_map,a.canonical_rows,a.out)
if __name__=="__main__":main()
