import hashlib,json,os,platform,subprocess,sys,time
from pathlib import Path
import psutil
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[3]
runner=REPO/"paper_projects/2026_c2ges_engineeringletters/source/code/run_fever_crossencoder_baseline.py"; data=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped"
model=Path.home()/".cache/huggingface/hub/models--cross-encoder--ms-marco-MiniLM-L-6-v2/snapshots/c5ee24cb16019beea0893ab7796b1df96625c6b8"; out=HERE/"runs/cross_encoder_prospective"; logs=HERE/"runs/cross_encoder_prospective_logs"
if out.exists(): raise SystemExit("fresh output required")
logs.mkdir(parents=True,exist_ok=False); cmd=[sys.executable,str(runner),"--data",str(data),"--out",str(out),"--model-path",str(model),"--batch-size","64","--max-length","512","--cutoffs","1,3,5,10"]
env=os.environ.copy(); env.update({"HF_HUB_OFFLINE":"1","TRANSFORMERS_OFFLINE":"1","TOKENIZERS_PARALLELISM":"false","OMP_NUM_THREADS":"2","MKL_NUM_THREADS":"2"})
t=time.perf_counter(); peak=0
with (logs/"process_stdout.log").open("w") as so,(logs/"process_stderr.log").open("w") as se:
 p=subprocess.Popen(cmd,cwd=REPO,env=env,stdout=so,stderr=se); pp=psutil.Process(p.pid)
 while p.poll() is None:
  try: peak=max(peak,pp.memory_info().rss+sum(x.memory_info().rss for x in pp.children(recursive=True)))
  except psutil.Error: pass
  time.sleep(.25)
wall=time.perf_counter()-t; rec={"name":"cross_encoder","status":"success" if p.returncode==0 else "failed","returncode":p.returncode,"wall_seconds":wall,"sampled_peak_rss_bytes":peak,"boundary":"model load plus complete test scoring and all-K extraction","command":cmd,"python":sys.version,"platform":platform.platform(),"runner_sha256":hashlib.sha256(runner.read_bytes()).hexdigest(),"protocol_sha256":hashlib.sha256((HERE/"ADDON_PROTOCOL_FREEZE.md").read_bytes()).hexdigest()}
target=out if out.exists() else logs; (target/"resource_usage.json").write_text(json.dumps(rec,indent=2)+"\n")
if p.returncode: raise SystemExit(p.returncode)
