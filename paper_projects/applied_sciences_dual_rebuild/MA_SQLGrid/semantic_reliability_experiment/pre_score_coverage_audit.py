#!/usr/bin/env python3
"""Gold-only Stage-B pre-score coverage and order/tie inventory."""

from __future__ import annotations

import argparse, csv, hashlib, json, re, sqlite3
from pathlib import Path
from typing import Any
from comparison_v2 import rows_equal

ORDER_RE = re.compile(r"\border\s+by\s+(.*?)(?:\blimit\b|;|$)", re.I | re.S)
SELECT_RE = re.compile(r"^\s*select\s+(.*?)\s+from\s", re.I | re.S)
LIMIT_RE = re.compile(r"\blimit\s+(\d+)", re.I)

def load_jsonl(p: Path): return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def sha(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(obj: Any): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def split_exprs(text: str) -> list[str]:
    out=[]; buf=[]; depth=0
    for ch in text:
        if ch=="(": depth+=1
        elif ch==")": depth-=1
        if ch=="," and depth==0: out.append("".join(buf).strip()); buf=[]
        else: buf.append(ch)
    if buf: out.append("".join(buf).strip())
    return out
def norm_expr(x: str) -> str:
    x=re.sub(r"\s+(asc|desc)\b.*$","",x.strip(),flags=re.I)
    x=re.sub(r"\s+as\s+\w+$","",x,flags=re.I)
    return re.sub(r"\s+","",x).lower()
def order_record(q: dict[str,Any]) -> dict[str,Any]:
    sql=q["gold_sql"]; om=ORDER_RE.search(sql); sm=SELECT_RE.search(sql); lm=LIMIT_RE.search(sql)
    order=split_exprs(om.group(1)) if om else []; projections=split_exprs(sm.group(1)) if sm else []
    aliases={}
    for p in projections:
        am=re.search(r"\s+as\s+(\w+)\s*$",p,re.I)
        if am: aliases[am.group(1).lower()]=norm_expr(p)
    order_norm=[aliases.get(norm_expr(x),norm_expr(x)) for x in order]; projection_norm=[norm_expr(x) for x in projections]
    all_projection_ordered=bool(order_norm) and set(projection_norm).issubset(set(order_norm))
    if not om: klass="AMBIGUOUS_ORDER_HOLD"; rationale="metadata says order-sensitive but SQL has no ORDER BY"
    elif all_projection_ordered: klass="TIE_OUTPUT_EQUIVALENT_MACHINE"; rationale="ORDER BY covers every projected expression; tied rows are output-identical"
    else: klass="AMBIGUOUS_ORDER_HOLD"; rationale="schema does not prove total order and ORDER BY does not cover every projected expression"
    if lm and klass != "TIE_OUTPUT_EQUIVALENT_MACHINE": klass="TOPK_TIE_POLICY_HOLD"; rationale="LIMIT cutoff can select among non-output-identical ties; independent adjudication required"
    return {"question_id":q["question_id"],"order_sensitive":q["order_sensitive"],"top_k":bool(lm),"limit":int(lm.group(1)) if lm else "","order_by_clause":om.group(1).strip() if om else "","projection_count":len(projections),"order_term_count":len(order),"machine_class":klass,"automatic_primary_eligible":klass=="TIE_OUTPUT_EQUIVALENT_MACHINE","rationale":rationale}
def execute(db: Path, sql: str):
    c=sqlite3.connect(db.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
    try:
        cur=c.execute(sql); return [d[0] for d in cur.description or []],[tuple(r) for r in cur.fetchall()]
    finally: c.close()
def write_csv(p:Path,rows:list[dict[str,Any]]):
    with p.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--questions",type=Path,required=True);ap.add_argument("--states",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    qs=[q for q in load_jsonl(a.questions) if q["split"]=="test"]
    manifest=json.loads((a.states/"STAGE_A_STATE_MANIFEST.json").read_text(encoding="utf-8"));states=manifest["states"]
    base={}; atomic=[]; state_rows=[]
    for si,s in enumerate(states):
        changed=0; errors=0
        for q in qs:
            error=None
            try: cols,rows=execute(a.states/s["state_path"],q["gold_sql"])
            except sqlite3.Error as e: cols=[];rows=[];errors+=1;error=str(e)
            key=q["question_id"]
            if si==0: base[key]=(cols,rows)
            different = si>0 and not rows_equal(rows,base[key][1],ordered=bool(q["order_sensitive"]),strict_numeric=False)
            changed+=different
            atomic.append({"state":s["state"],"question_id":key,"gold_ok":error is None,"gold_error":error,"gold_row_count":len(rows),"gold_column_count":len(cols),"changed_from_snapshot":different,"snapshot_empty":len(base.get(key,(None,rows))[1])==0,"became_nonempty":si>0 and len(base[key][1])==0 and len(rows)>0})
        state_rows.append({"state":s["state"],"gold_executions":len(qs),"gold_errors":errors,"changed_gold_denotations":changed,"unchanged_gold_denotations":len(qs)-changed})
    changed_union={r["question_id"] for r in atomic if r["changed_from_snapshot"]}
    empty_ids=sorted(k for k,v in base.items() if not v[1]); empty_counts={k:sum(r["became_nonempty"] for r in atomic if r["question_id"]==k) for k in empty_ids}
    order=[order_record(q) for q in qs if q["order_sensitive"]]; top=[r for r in order if r["top_k"]]
    write_csv(a.out/"gold_state_coverage_atomic.csv",atomic);write_csv(a.out/"state_gold_coverage.csv",state_rows);write_csv(a.out/"ORDER_TIE_MACHINE_CHECKLIST.csv",order);write_csv(a.out/"TOPK_TIE_MACHINE_CHECKLIST.csv",top)
    with (a.out/"ORDER_TIE_MACHINE_CHECKLIST.jsonl").open("w",encoding="utf-8",newline="\n") as f:
        for r in order:f.write(json.dumps(r,sort_keys=True)+"\n")
    uncovered=sorted(set(base)-changed_union);holds=sorted(r["question_id"] for r in order if not r["automatic_primary_eligible"])
    result={"schema_version":"ma-sqlgrid-pre-score-gold-coverage-v2","prediction_or_score_inputs_accessed":False,"inputs":{"questions_sha256":sha(a.questions),"stage_a_manifest_content_sha256":manifest["manifest_content_sha256"]},"denominators":{"questions":len(qs),"states":len(states),"gold_executions":len(qs)*len(states),"order_sensitive":len(order),"top_k":len(top)},"coverage":{"changed_union_n":len(changed_union),"unchanged_union_n":len(uncovered),"uncovered_question_ids":uncovered,"snapshot_empty_ids":empty_ids,"snapshot_empty_became_nonempty_state_counts":empty_counts,"all_empty_nonempty_in_at_least_two_states":all(v>=2 for v in empty_counts.values())},"order_tie":{"machine_eligible_n":sum(r["automatic_primary_eligible"] for r in order),"hold_n":len(holds),"hold_question_ids":holds,"policy":"holds are not automatically scored as wrong; independent adjudication is required"},"state_coverage":state_rows}
    result["content_sha256"]=canon(result);(a.out/"PRE_SCORE_GOLD_COVERAGE.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"GOLD_ONLY_COVERAGE changed={len(changed_union)}/180 empty2={result['coverage']['all_empty_nonempty_in_at_least_two_states']} order={len(order)} topk={len(top)} holds={len(holds)}")
if __name__=="__main__":main()
