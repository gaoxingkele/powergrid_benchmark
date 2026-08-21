# MA public baseline formal runbook

## Current boundary

The package is frozen but not run. The commands below are documentation only. Do not execute them until the root technical review is complete and a real human author creates an approval JSON binding the exact SHA-256 of `BASELINE_PROTOCOL_FREEZE.json`. No agent may invent that approval.

The run is an independent transparent BIRD comparison. It is not a DKASQL reproduction.

## Required human approval file

Create a file outside the canonical freeze directory with all four fields:

```json
{
  "approved_by_human": "REAL HUMAN NAME",
  "approval_date": "YYYY-MM-DD",
  "acknowledge_5000_generation_calls": true,
  "protocol_id": "MA-PUBLIC-BIRD-MINIDEV-v1.0",
  "freeze_sha256": "SHA256 OF BASELINE_PROTOCOL_FREEZE.json"
}
```

The runner refuses a missing/mismatched approval, any status other than `FROZEN_NOT_RUN`, an audit other than `PASS`, model-hash drift, non-loopback server failure, prompt/call-order drift, token-budget overflow, or an already existing output directory.

## Root preflight

From this directory:

```powershell
python audit_frozen_public_baseline.py --auditor /root-final-prelaunch-review
Get-FileHash -Algorithm SHA256 BASELINE_PROTOCOL_FREEZE.json
Get-Process llama-server -ErrorAction SilentlyContinue
nvidia-smi
```

Confirm no competing server/worker and that ports 8091 and 8092 are unused. The two backbones must run sequentially, never concurrently. A failed/crashed formal run is retained as an incident and is not resumed or silently overwritten.

## Qwen: 2500 calls

Start the pinned server in one foreground terminal:

```powershell
& 'D:\aicoding\models\ma_sqlgrid_local\llama.cpp-b9637-cuda13.3\bin\llama-server.exe' `
  --model 'D:\aicoding\models\ma_sqlgrid_local\Qwen2.5-Coder-7B-Instruct-GGUF-13fb94bf\qwen2.5-coder-7b-instruct-q4_k_m.gguf' `
  --alias 'qwen2.5-coder-7b-instruct-q4_k_m@13fb94bf' --host 127.0.0.1 --port 8091 `
  --ctx-size 16384 --n-gpu-layers 99 --flash-attn on --threads 12 --parallel 1 --seed 20260805
```

After `/health` reports ready, run in a second foreground terminal. Amendment v1.0.1: the runner MUST use the pinned compatibility runtime (Python 3.10.11 / SQLite 3.40.1); the embeddable distribution isolates `sys.path` via its `._pth` file, so invoke through `runpy` with the protocol directory inserted:

```powershell
runtime_compat\python31011\python.exe -c "import sys,runpy; sys.path.insert(0,'.'); runpy.run_path('run_formal_public_baseline.py', run_name='__main__')" `
  --model qwen --server-url http://127.0.0.1:8091 `
  --human-approval 'D:\ABSOLUTE\PATH\human_launch_approval.json' `
  --output-dir 'D:\ABSOLUTE\NEW\PATH\MA_PUBLIC_BIRD_v1_qwen'
```

Stop the Qwen server normally after the runner completes and the 2500-call/2000-final-row manifest is verified.

## Granite: 2500 calls

Only after Qwen has stopped, start Granite:

```powershell
& 'D:\aicoding\models\ma_sqlgrid_local\llama.cpp-b9637-cuda13.3\bin\llama-server.exe' `
  --model 'D:\aicoding\models\ma_sqlgrid_local\ibm-granite-3.3-8b-instruct-GGUF-e40e9dd\granite-3.3-8b-instruct-Q4_K_M.gguf' `
  --alias 'granite-3.3-8b-instruct-q4_k_m@e40e9dd' --host 127.0.0.1 --port 8092 `
  --ctx-size 16384 --n-gpu-layers 99 --flash-attn on --threads 12 --parallel 1 --seed 20260805
```

Then:

```powershell
runtime_compat\python31011\python.exe -c "import sys,runpy; sys.path.insert(0,'.'); runpy.run_path('run_formal_public_baseline.py', run_name='__main__')" `
  --model granite --server-url http://127.0.0.1:8092 `
  --human-approval 'D:\ABSOLUTE\PATH\human_launch_approval.json' `
  --output-dir 'D:\ABSOLUTE\NEW\PATH\MA_PUBLIC_BIRD_v1_granite'
```

## Post-run promotion gate

Do not copy scores into the manuscript directly from these ledgers. A separate auditor must re-execute all 4000 final predictions, verify 5000 unique call records, zero retries/drops, prompt/model/data/runtime hashes, official EX set semantics, and regenerate database-clustered intervals/Holm tables from the immutable ledgers.
