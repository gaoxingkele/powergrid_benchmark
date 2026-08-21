#!/usr/bin/env python3
"""Locked Stage B scorer. Formal execution requires an independent v2 re-audit."""

from __future__ import annotations
import argparse, csv, hashlib, json, sqlite3, time, re
from pathlib import Path
from comparison_v2 import rows_equal, header_diagnostics, COLUMN_POLICY, ABS_TOL, REL_TOL

CELLS=["F00_Full_NoShape","F01_Full_WithShape","F10_Compact_NoShape","F11_Compact_WithShape"]
FORBIDDEN=re.compile(r"\b(insert|update|delete|drop|alter|create|attach|detach|vacuum|pragma|reindex|analyze|begin|commit|rollback)\b",re.I)
REPLACE_INTO=re.compile(r"\breplace\s+into\b",re.I)
def sha(p:Path):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def load(p:Path):return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
def canonical_hash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def verify_ledger(label:str,pred:Path,manifest_path:Path,questions:set[str],canonical:dict):
 accepted=canonical["accepted_inputs"]; rel_pred=pred.as_posix().split("powergrid_benchmark/")[-1] if "powergrid_benchmark/" in pred.as_posix() else None
 # Match by immutable basename suffix, then require physical hash/bytes.
 pred_entry=next(v for k,v in accepted.items() if k.endswith(str(pred).replace("\\","/").split("paper_projects/")[-1]) or (k.endswith("predictions.jsonl") and v["sha256"]==sha(pred)))
 man_entry=next(v for k,v in accepted.items() if k.endswith(str(manifest_path).replace("\\","/").split("paper_projects/")[-1]) or (k.endswith("manifest.json") and v["sha256"]==sha(manifest_path)))
 assert sha(pred)==pred_entry["sha256"] and pred.stat().st_size==pred_entry["bytes"]
 assert sha(manifest_path)==man_entry["sha256"] and manifest_path.stat().st_size==man_entry["bytes"]
 m=json.loads(manifest_path.read_text(encoding="utf-8"));rows=load(pred);expected={(q,c) for q in questions for c in CELLS};keys=[(r["question_id"],r["condition"]) for r in rows]
 assert len(rows)==720 and len(set(keys))==720 and set(keys)==expected and all(r["status"]=="success" for r in rows)
 assert m["status"]=="completed" and m["canonical_result_eligible"] and m["prediction_count"]==720
 for field,mkey in [("data_sha256","data_sha256"),("code_sha256","code_sha256"),("configuration_sha256","configuration_sha256")]: assert {r[field] for r in rows}=={m["hashes"][mkey]}
 return rows
def clean_sql(sql:str):
 text=sql.strip();parts=[x.strip() for x in text.split(";") if x.strip()]
 if len(parts)!=1:return False,text,"multiple_statement"
 text=parts[0]
 if not re.match(r"^(select|with)\b",text,re.I) or FORBIDDEN.search(text) or REPLACE_INTO.search(text):return False,text,"not_read_only_select"
 return True,text,None
def ro_conn(path:Path):
 c=sqlite3.connect(path.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
 allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION}
 if hasattr(sqlite3,"SQLITE_RECURSIVE"):allowed.add(sqlite3.SQLITE_RECURSIVE)
 c.set_authorizer(lambda action,_a,_b,_db,_src:sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY);return c
def execute(c,sql,timeout=3.0,row_cap=100000,byte_cap=10_000_000):
 ok,stmt,error=clean_sql(sql)
 if not ok:return {"ok":False,"error_type":"safety_rejection","error":error,"columns":[],"rows":[]}
 deadline=time.monotonic()+timeout;c.set_progress_handler(lambda:1 if time.monotonic()>deadline else 0,1000)
 try:
  cur=c.execute(stmt);cols=[d[0] for d in cur.description or []];rows=[];size=0
  while True:
   batch=cur.fetchmany(1000)
   if not batch:break
   rows.extend(tuple(x) for x in batch);size+=sum(len(repr(x).encode("utf-8")) for x in batch)
   if len(rows)>row_cap:return {"ok":False,"error_type":"row_cap","error":str(row_cap),"columns":cols,"rows":[]}
   if size>byte_cap:return {"ok":False,"error_type":"byte_cap","error":str(byte_cap),"columns":cols,"rows":[]}
  return {"ok":True,"error_type":None,"error":None,"columns":cols,"rows":rows}
 except sqlite3.Error as e:return {"ok":False,"error_type":"execution_error","error":str(e),"columns":[],"rows":[]}
 finally:c.set_progress_handler(None,0)
def write_jsonl(path,rows):
 with path.open("w",encoding="utf-8",newline="\n") as f:
  for r in rows:f.write(json.dumps(r,sort_keys=True,ensure_ascii=False)+"\n")
def main():
 p=argparse.ArgumentParser();p.add_argument("--freeze",type=Path,required=True);p.add_argument("--reaudit",type=Path,required=True);p.add_argument("--approval",type=Path,required=True);p.add_argument("--out",type=Path,required=True);m=p.add_mutually_exclusive_group();m.add_argument("--preflight-only",action="store_true");m.add_argument("--canonical-snapshot-preflight",action="store_true");a=p.parse_args();freeze=json.loads(a.freeze.read_text(encoding="utf-8"));audit=json.loads(a.reaudit.read_text(encoding="utf-8"));approval=json.loads(a.approval.read_text(encoding="utf-8"))
 expected=freeze.pop("freeze_content_sha256");assert canonical_hash(freeze)==expected,"freeze content hash mismatch";freeze["freeze_content_sha256"]=expected
 root=Path(__file__).resolve().parents[4]
 # Exact-freeze live closure: code/protocol/tests, immutable data, policy, and Stage-A manifest.
 for item in freeze["frozen_files"]:
  path=root/item["path"];assert sha(path)==item["sha256"] and path.stat().st_size==item["bytes"],f"frozen file identity changed: {item['path']}"
 for name,item in freeze["immutable_inputs"].items():
  path=root/item["path"];assert sha(path)==item["sha256"] and path.stat().st_size==item["bytes"],f"immutable input changed: {name}"
 policy_binding=freeze["authorization_contract"]["policy"];policy_path=root/policy_binding["path"];assert sha(policy_path)==policy_binding["sha256"] and policy_path.stat().st_size==policy_binding["bytes"],"launch approval policy identity changed";policy=json.loads(policy_path.read_text(encoding="utf-8"));required=set(policy["required_reaudit_gate_ids"])
 assert approval.get("schema_version")==policy["required_launch_companion_schema_version"] and approval.get("decision")==policy["required_launch_companion_decision"],"invalid launch companion"
 assert approval.get("freeze_content_sha256")==expected and approval.get("reaudit_sha256")==sha(a.reaudit) and approval.get("reaudit_bytes")==a.reaudit.stat().st_size and Path(approval.get("reaudit_path","")).name==a.reaudit.name,"launch companion does not bind exact freeze/audit"
 assert audit.get("schema_version")==policy["required_reaudit_schema_version"] and audit.get("decision")==policy["required_reaudit_decision"] and audit.get("freeze_content_sha256")==expected,"formal scoring locked pending PASS_AUTHORIZE_FORMAL_SCORE for exact freeze"
 assert audit.get("required_gates_all_pass") is True and audit.get("authorizes_formal_score") is True
 gates={g["id"]:g["status"] for g in audit.get("gates",[])};assert required.issubset(gates) and all(gates[x]=="PASS" for x in required),"required re-audit gates not all PASS"
 qpath=root/"paper_projects/2026_ma_sqlgrid_cmc/source/data/griddb_maintenance_v2_v0_1/questions.jsonl";qs={r["question_id"] for r in load(qpath) if r["split"]=="test"}
 canonical_path=root/"paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/canonical_v2_reanalysis/FREEZE_AND_METHOD.json";binding=freeze["canonical_v2_binding"]["freeze_and_method"];assert sha(canonical_path)==binding["sha256"] and canonical_path.stat().st_size==binding["bytes"],"canonical-v2 freeze physical identity changed";canonical=json.loads(canonical_path.read_text(encoding="utf-8"))
 # Bind the two blind reviews and adjudication as one immutable chain.
 order_chain=freeze["order_adjudication"]
 loaded={}
 for name,item in order_chain["artifacts"].items():
  path=root/item["path"];assert sha(path)==item["sha256"] and path.stat().st_size==item["bytes"];loaded[name]=json.loads(path.read_text(encoding="utf-8"))
 assert loaded["adjudication"]["inputs"]["reviewer_a_json_sha256"]==order_chain["artifacts"]["reviewer_a"]["sha256"] and loaded["adjudication"]["inputs"]["reviewer_b_json_sha256"]==order_chain["artifacts"]["reviewer_b"]["sha256"]
 assert loaded["adjudication"]["agreement"]["held_ids"]==114 and loaded["adjudication"]["final_policy"]["order_insensitive_candidate_questions"]==66
 ledgers={label:verify_ledger(label,root/d["predictions"],root/d["manifest"],qs,canonical) for label,d in freeze["prediction_bindings"].items()}
 questions={r["question_id"]:r for r in load(qpath) if r["split"]=="test"}
 exp=a.freeze.parent;state_dir=exp/freeze["stage_a"]["state_directory"];manifest_path=state_dir/"STAGE_A_STATE_MANIFEST.json";manifest_binding=freeze["stage_a"]["manifest"];assert sha(manifest_path)==manifest_binding["sha256"] and manifest_path.stat().st_size==manifest_binding["bytes"],"Stage-A manifest physical identity changed";state_manifest=json.loads(manifest_path.read_text())
 assert state_manifest["manifest_content_sha256"]==freeze["stage_a"]["manifest_content_sha256"]
 assert sqlite3.sqlite_version==state_manifest["sqlite"]["version"]
 runtime_options=[r[0] for r in sqlite3.connect(":memory:").execute("PRAGMA compile_options")];assert runtime_options==state_manifest["sqlite"]["compile_options"]
 for s in state_manifest["states"]:assert sha(state_dir/s["state_path"])==s["state_sha256"]
 order={r["question_id"]:r for r in load(exp/freeze["pre_score"]["order_checklist_jsonl"])}
 crow_path=root/freeze["canonical_v2_binding"]["canonical_rows_v2"]["path"];cb=freeze["canonical_v2_binding"]["canonical_rows_v2"];assert sha(crow_path)==cb["sha256"] and crow_path.stat().st_size==cb["bytes"],"canonical-v2 rows physical identity changed"
 if a.preflight_only:
  assert len(ledgers)==2 and all(len(x)==720 for x in ledgers.values()) and len(state_manifest["states"])==18 and len(order)==114
  print("STAGE_B_V4_PREFLIGHT_PASS authorization=1 canonical=1 ledgers=1440 states=18 order=114 sql_executions=0 output_written=0")
  return
 if a.canonical_snapshot_preflight:
  t0=next(s for s in state_manifest["states"] if s["state"]=="T0_snapshot");c=ro_conn(state_dir/t0["state_path"]);executions=0;mismatches=[]
  try:
   gold={}
   for qid,q in questions.items():gold[qid]=execute(c,q["gold_sql"]);executions+=1
   crow_path=root/freeze["canonical_v2_binding"]["canonical_rows_v2"]["path"];canonical_snapshot={(r["backbone"],r["condition"],r["question_id"]):bool(r["execution"]) for r in load(crow_path)}
   for backbone,rows in ledgers.items():
    for pred in rows:
     q=questions[pred["question_id"]];g=gold[pred["question_id"]];r=execute(c,pred["predicted_sql"]);executions+=1;shape=bool(r["ok"] and len(r["columns"])==q["answer_shape"]["column_count"]);got=bool(g["ok"] and shape and rows_equal(r["rows"],g["rows"],ordered=q["order_sensitive"],strict_numeric=False));key=(backbone,pred["condition"],pred["question_id"])
     if got!=canonical_snapshot[key]:mismatches.append({"backbone":backbone,"condition":pred["condition"],"question_id":pred["question_id"]})
  finally:c.close()
  assert executions==1620 and not mismatches,f"canonical T0 mismatch count={len(mismatches)} ids={mismatches[:10]}"
  print("STAGE_B_V5_CANONICAL_SNAPSHOT_PREFLIGHT_PASS ledgers=1440 gold=180 sql_executions=1620 canonical_mismatches=0 output_written=0")
  return
 atom=[]
 for s in state_manifest["states"]:
  c=ro_conn(state_dir/s["state_path"])
  try:
   gold={qid:execute(c,q["gold_sql"]) for qid,q in questions.items()}
   for backbone,rows in ledgers.items():
    for pred in rows:
     q=questions[pred["question_id"]];g=gold[pred["question_id"]];r=execute(c,pred["predicted_sql"]);shape=bool(r["ok"] and len(r["columns"])==q["answer_shape"]["column_count"])
     tolerant=bool(g["ok"] and shape and rows_equal(r["rows"],g["rows"],ordered=q["order_sensitive"],strict_numeric=False));strict=bool(g["ok"] and shape and rows_equal(r["rows"],g["rows"],ordered=q["order_sensitive"],strict_numeric=True))
     ordrec=order.get(pred["question_id"]);hold=bool(q["order_sensitive"])
     headers=header_diagnostics(r["columns"],g["columns"],q["answer_shape"]["columns"]) if r["ok"] and g["ok"] else {"prediction_vs_gold_header_match":False,"prediction_vs_metadata_header_match":False,"gold_vs_metadata_header_match":False}
     semantic=s["state"] in set(freeze["stage_a"]["semantic_suite_states"]);physical=s["state"] in set(freeze["stage_a"]["physical_order_diagnostic_states"])
     atom.append({"backbone":backbone,"question_id":pred["question_id"],"condition":pred["condition"],"state":s["state"],"state_operator":s["operator"],"semantic_suite_state":semantic,"physical_order_diagnostic_state":physical,"primary_semantic_state":bool(semantic and not hold),"automatic_primary_eligible":not hold,"adjudication_class":"order_hold_two_reviewer_consensus" if hold else ("execution_error_hold" if not r["ok"] else "automatic"),"machine_order_class":ordrec["machine_class"] if ordrec else "ORDER_INSENSITIVE","tolerant_denotation_agreement":tolerant,"strict_denotation_agreement":strict,"prediction_ok":r["ok"],"prediction_error_type":r["error_type"],"gold_ok":g["ok"],"shape_ok":shape,**headers})
  finally:c.close()
 assert len(atom)==25920 and len({(r["backbone"],r["condition"],r["question_id"],r["state"]) for r in atom})==25920
 assert sum(r["primary_semantic_state"] for r in atom)==7920 and sum(not r["automatic_primary_eligible"] for r in atom)==16416
 # Reproduce the canonical snapshot before any output is committed.
 cmap={(r["backbone"],r["condition"],r["question_id"]):bool(r["execution"]) for r in load(crow_path)};snapshot={(r["backbone"],r["condition"],r["question_id"]):bool(r["tolerant_denotation_agreement"]) for r in atom if r["state"]=="T0_snapshot"};assert snapshot==cmap,"T0 snapshot outcomes differ from canonical v2"
 a.out.mkdir(parents=True,exist_ok=True);write_jsonl(a.out/"atomic_scores.jsonl",atom)
 result={"schema_version":"ma-sqlgrid-semantic-reliability-atomic-v2","freeze_content_sha256":freeze["freeze_content_sha256"],"column_policy":COLUMN_POLICY,"abs_tol":ABS_TOL,"rel_tol":REL_TOL,"prediction_state_rows":len(atom),"expected_prediction_state_rows":1440*len(state_manifest["states"]),"automatic_primary_question_n":66,"order_hold_question_n":114,"automatic_eligible_rows":sum(r["automatic_primary_eligible"] for r in atom),"order_hold_rows":sum(r["adjudication_class"]=="order_hold_two_reviewer_consensus" for r in atom)}
 (a.out/"RUN_SUMMARY.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(f"STAGE_B_COMPLETE rows={len(atom)}")
if __name__=="__main__":main()
