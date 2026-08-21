# MA-SQLGrid Local Model Execution Plan

## Status and hard boundary

Status at 2026-08-05: **exact artifacts downloaded, execution halted before extraction because the initial plan confused a Hugging Face Xet hash with the file SHA-256; no runtime installed and no model output produced**. The official tree API subsequently confirmed the downloaded file's SHA-256, but the stop gate remains in force for this run. This path is for noncanonical development smoke tests first. It does not change `CLAIM_LEDGER.md`, populate the registered factorial result table, or establish any MA-SQLGrid accuracy claim. Promotion to a formal run requires an independently reviewed model/runtime freeze and the existing full evidence audit.

No paid or cloud inference endpoint is used. The server must bind to loopback only, and the harness rejects a `local-openai-compatible` base URL whose host is not `localhost`, `127.0.0.1`, or `::1`.

## Observed machine state

| Item | Observed value |
|---|---|
| OS | Windows 11, build 26100 |
| GPU | NVIDIA GeForce RTX 3090, 24,576 MiB |
| NVIDIA driver / CUDA UMD | 610.62 / 13.3 |
| Free GPU memory at audit | approximately 23.4 GiB |
| Python | 3.12.10 |
| PyTorch | 2.13.0+cpu; `torch.cuda.is_available() == False` |
| Existing local servers | no Ollama, llama.cpp server, LM Studio CLI, or vLLM executable found |
| Python inference packages | `transformers` 5.14.1 installed; no `accelerate`, `bitsandbytes`, or `llama_cpp` |
| Existing Hugging Face cache | embedding/reranker models only; no generative instruction model |
| Free storage | approximately 656.8 GB on `D:` |

The preferred path is a standalone prebuilt llama.cpp CUDA server. It avoids replacing the current CPU-only PyTorch environment and exposes the OpenAI-compatible `/v1/chat/completions` interface already used by `applsci_factorial.py`.

## Frozen primary model proposal

| Field | Frozen proposal |
|---|---|
| Model | `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF` |
| Quantization/file | `qwen2.5-coder-7b-instruct-q4_k_m.gguf` |
| Hugging Face revision | `13fb94bfda8c8cf22497dc57b78f391a9acb426a` |
| File size | 4,683,073,536 bytes (4.36 GiB / 4.68 GB decimal) |
| File SHA-256 (official LFS OID) | `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c` |
| Hugging Face Xet hash (not the file SHA-256) | `fa9e1815472201e7dea978475c1f3ca7bc7df773eaeb3b3a383258c25b052f6f` |
| Parameters | 7.61B |
| License | Apache-2.0 |
| Reason | SQL/code instruction tuning, official Qwen GGUF, comfortably bounded on a 24 GiB RTX 3090 |
| Expected local footprint | model 4.68 GB; llama.cpp archives about 550 MB compressed; allow 8 GB total working storage |
| Expected VRAM envelope | approximately 6–10 GiB for Q4 weights plus a 16k context and runtime buffers; verify empirically with `nvidia-smi` |

Model metadata is taken from the [official Qwen GGUF repository](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF) and its pinned Hugging Face tree API revision. The tree entry distinguishes LFS OID `509287...94d3c` from Xet hash `fa9e18...52f6f`; only the LFS OID is the downloaded file SHA-256. The model card identifies Apache-2.0, 7.61B parameters, a 32,768-token native GGUF context, and a 4.68 GB Q4_K_M artifact. The execution context is deliberately capped at 16,384 tokens for the first smoke.

## Frozen runtime proposal

| Field | Frozen proposal |
|---|---|
| Runtime | `ggml-org/llama.cpp` Windows CUDA 13.3 prebuilt release |
| Release | `b9637` |
| Commit | `aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3` |
| Binary archive | `llama-b9637-bin-win-cuda-13.3-x64.zip`, 159,029,255 bytes, SHA-256 `8667e76077b40db57fc680577c6d8b48b8aa3f58e34fc23a70bcc668a69c97e9` |
| CUDA archive | `cudart-llama-bin-win-cuda-13.3-x64.zip`, 390,970,417 bytes, SHA-256 `1462a050eb4c684921ba51dcc4cc488a036674c3e73e9945ee705b854808d03e` |

The official [llama.cpp release page](https://github.com/ggml-org/llama.cpp/releases/tag/b9637) provides separate Windows CUDA 13.3 binary and runtime archives. Both must be verified before extraction. If the exact release asset is no longer accessible, stop; do not silently substitute a newer runtime.

## Exact download commands (not executed)

Target root: `D:\aicoding\models\ma_sqlgrid_local\`. Downloads must use the workspace-standard aria2-first helper.

```powershell
$runtimeRoot = 'D:\aicoding\models\ma_sqlgrid_local\llama.cpp-b9637-cuda13.3'
$modelRoot = 'D:\aicoding\models\ma_sqlgrid_local\Qwen2.5-Coder-7B-Instruct-GGUF-13fb94bf'
New-Item -ItemType Directory -Path $runtimeRoot,$modelRoot -Force

python -m download_tools `
  'https://github.com/ggml-org/llama.cpp/releases/download/b9637/llama-b9637-bin-win-cuda-13.3-x64.zip' `
  "$runtimeRoot\llama-b9637-bin-win-cuda-13.3-x64.zip"

python -m download_tools `
  'https://github.com/ggml-org/llama.cpp/releases/download/b9637/cudart-llama-bin-win-cuda-13.3-x64.zip' `
  "$runtimeRoot\cudart-llama-bin-win-cuda-13.3-x64.zip"

python -m download_tools `
  'https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/13fb94bfda8c8cf22497dc57b78f391a9acb426a/qwen2.5-coder-7b-instruct-q4_k_m.gguf' `
  "$modelRoot\qwen2.5-coder-7b-instruct-q4_k_m.gguf"
```

Before extraction, re-query release and Hugging Face tree metadata and verify all three exact file SHA-256 values. A mismatch stops the workflow. Do not use `-Force` to overwrite an existing verified model.

## Server command after checksum verification

```powershell
$runtimeRoot = 'D:\aicoding\models\ma_sqlgrid_local\llama.cpp-b9637-cuda13.3'
$modelFile = 'D:\aicoding\models\ma_sqlgrid_local\Qwen2.5-Coder-7B-Instruct-GGUF-13fb94bf\qwen2.5-coder-7b-instruct-q4_k_m.gguf'

& "$runtimeRoot\llama-server.exe" `
  --model $modelFile `
  --alias 'qwen2.5-coder-7b-instruct-q4_k_m@13fb94bf' `
  --host 127.0.0.1 `
  --port 8080 `
  --ctx-size 16384 `
  --n-gpu-layers 99 `
  --flash-attn on `
  --threads 12 `
  --parallel 1 `
  --seed 20260805
```

The console log must show that CUDA found the RTX 3090 and that model layers were offloaded. Capture the complete startup log, `nvidia-smi`, `/v1/models`, runtime archive hashes, model hash, and the server command. Bind only to `127.0.0.1`; do not expose port 8080 to the LAN.

## Noncanonical real-output smoke command

Create `local_model_artifact_manifest.json` from the template installed with the adapter, filling only verified values. Then run one development question through four factorial cells. Development prompts remove all gold fields, and the smoke records reference-free syntax/safety/execution diagnostics only; it does not compute gold accuracy.

```powershell
$env:MA_SQLGRID_LOCAL_KEY = 'local-no-auth'
python paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/applsci_factorial.py `
  --out paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/local_smoke/qwen25coder7b_q4km_seed20260805 `
  --execute `
  --provider local-openai-compatible `
  --base-url http://127.0.0.1:8080/v1 `
  --model 'qwen2.5-coder-7b-instruct-q4_k_m@13fb94bf' `
  --local-model-manifest paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/local_model_artifact_manifest.json `
  --split dev-smoke `
  --max-questions 1 `
  --seed 20260805 `
  --temperature 0 `
  --max-tokens 256 `
  --timeout 180 `
  --retries 0
```

Acceptance requires four real provider responses, non-null response hashes, no `provider_error`, no gold material in prompts, an endpoint restricted to loopback, and at least one safely extracted read-only SQL statement. A zero-correct or parse-failure smoke is still honest evidence of model behaviour; it is not repaired or replaced manually.

## Promotion gates

1. Independently re-query and verify both runtime asset checksums and the model LFS OID before download.
2. Download and hash the exact pinned runtime/model artifacts.
3. Demonstrate GPU offload and retain the startup log.
4. Pass unit tests and the one-development-question real-output smoke.
5. Review prompt length against the 16k context cap; truncation is prohibited unless a deterministic registered policy is added.
6. Run a larger development-only pilot and inspect SQL safety/error modes.
7. Freeze the final model/runtime manifest before any canonical 180-question execution.
8. Keep all smoke and future local-model results out of canonical claims until the registered E4 audit is complete.

## Current blockers

- The generative model and runtime archives are downloaded, but the runtime is deliberately not extracted or installed after the initial hash-gate stop.
- Current PyTorch is CPU-only, so direct Transformers GPU inference is not presently viable without a separate environment.
- No real-output smoke can run until an independent reviewer accepts the corrected LFS SHA-256 and explicitly resumes after the recorded stop.
- Runtime and model checksums must be re-queried and independently verified again before extraction.

## Recorded preparation stop

At `2026-08-05T07:00:24Z`, both runtime archives matched their GitHub release SHA-256 values. The model download had the expected 4,683,073,536-byte length and local SHA-256 `509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c`, but the initial plan expected Xet hash `fa9e1815...52f6f`. Execution stopped before extraction. A read-only query to the official Hugging Face tree API for revision `13fb94bf...b426a` then returned `lfs.oid=509287...94d3c`, `xetHash=fa9e18...52f6f`, and the same byte count. The plan and manifest template are corrected, but no continuation occurs in this stopped run.
