"""Execute the frozen Round-3 add-on runs with bounded parallelism and resource logs."""
from __future__ import annotations
import concurrent.futures, hashlib, json, os, platform, subprocess, sys, threading, time
from pathlib import Path
import psutil

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[3]
CORE=REPO/"paper_projects/2026_c2ges_engineeringletters/source/code/c2ges_learnable.py"
DATA=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped"
CE=REPO/"paper_projects/2026_c2ges_engineeringletters/source/code/run_fever_crossencoder_baseline.py"
MODEL=Path.home()/".cache/huggingface/hub/models--cross-encoder--ms-marco-MiniLM-L-6-v2/snapshots/c5ee24cb16019beea0893ab7796b1df96625c6b8"
RUNS=HERE/"runs"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def execute(name, cmd, out):
    out.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy(); env.update({"OMP_NUM_THREADS":"2","MKL_NUM_THREADS":"2","TOKENIZERS_PARALLELISM":"false","HF_HUB_OFFLINE":"1","TRANSFORMERS_OFFLINE":"1"})
    t0=time.perf_counter(); peak=0; stop=threading.Event()
    with (out/"process_stdout.log").open("w",encoding="utf-8") as so,(out/"process_stderr.log").open("w",encoding="utf-8") as se:
        proc=subprocess.Popen(cmd,stdout=so,stderr=se,env=env,cwd=REPO)
        pp=psutil.Process(proc.pid)
        while proc.poll() is None:
            try: peak=max(peak,pp.memory_info().rss+sum(x.memory_info().rss for x in pp.children(recursive=True)))
            except (psutil.NoSuchProcess,psutil.AccessDenied): pass
            time.sleep(.25)
    wall=time.perf_counter()-t0
    record={"name":name,"status":"success" if proc.returncode==0 else "failed","returncode":proc.returncode,"wall_seconds":wall,"sampled_peak_rss_bytes":peak,"command":cmd,"python":sys.version,"platform":platform.platform(),"core_sha256":sha(CORE),"protocol_sha256":sha(HERE/"ADDON_PROTOCOL_FREEZE.md")}
    (out/"resource_usage.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    if proc.returncode: raise RuntimeError(f"{name} failed; see {out}")
    return record

def learned(arch,seed):
    out=RUNS/arch/f"seed_{seed}"
    cmd=[sys.executable,str(CORE),"--data",str(DATA),"--out",str(out),"--train-limit","8000","--dev-limit","1500","--test-limit","1500","--epochs","4","--lr","0.001","--seed",str(seed),"--device","cpu","--train-k","3","--eval-k","1,3,5,10","--bootstrap-samples","2000","--protocol","label-blind","--architecture",arch]
    return execute(f"{arch}:{seed}",cmd,out)

def main():
    if RUNS.exists() and any(RUNS.rglob("resource_usage.json")): raise SystemExit("fresh output required: add-on run records already exist")
    jobs=[(a,s) for a in ("true_no_floor","true_no_role") for s in (2026,2027,2028,2029,2030)]
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        future={pool.submit(learned,*j):j for j in jobs}
        for f in concurrent.futures.as_completed(future): records.append(f.result()); print(records[-1]["name"],records[-1]["wall_seconds"],flush=True)
    out=RUNS/"cross_encoder"
    cmd=[sys.executable,str(CE),"--data",str(DATA),"--out",str(out),"--model-path",str(MODEL),"--batch-size","64","--max-length","512","--cutoffs","1,3,5,10"]
    records.append(execute("cross_encoder",cmd,out))
    (HERE/"execution_summary.json").write_text(json.dumps({"protocol_sha256":sha(HERE/"ADDON_PROTOCOL_FREEZE.md"),"runs":records},indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
