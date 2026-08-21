#!/usr/bin/env python3
"""Extract only frozen question-to-cluster membership from canonical v2 rows."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;SRC=HERE.parent/"canonical_v2_reanalysis/canonical_rows_v2.jsonl"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows=[json.loads(x) for x in SRC.read_text(encoding="utf-8").splitlines() if x.strip()]
mapping={}
for r in rows:
 q=r["question_id"];c=r["template_cluster"]
 if q in mapping and mapping[q]!=c:raise RuntimeError("cluster conflict")
 mapping[q]=c
if len(mapping)!=180:raise RuntimeError("expected 180 questions")
out={"schema_version":"ma-sqlgrid-semantic-cluster-map-v3","source":{"path":SRC.relative_to(HERE.parents[3]).as_posix(),"sha256":sha(SRC),"bytes":SRC.stat().st_size},"questions":180,"clusters":len(set(mapping.values())),"mapping":dict(sorted(mapping.items()))}
raw=json.dumps(out,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode();out["content_sha256"]=hashlib.sha256(raw).hexdigest();(HERE/"CLUSTER_MAP_V3.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(len(mapping),out["clusters"],out["content_sha256"])
