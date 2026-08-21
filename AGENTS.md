# Power Grid Benchmark Workspace Instructions

These instructions apply to all AI coding agents operating in this repository (Kimi Code, Cursor, Codex, Claude, etc.).

## Default Download Tool

Use **aria2c** as the default download tool whenever files, datasets, archives, or remote assets are fetched.

### Why
- Multi-connection segmented downloads (`--split=16`, `--max-connection-per-server=16`)
- Resume support (`--continue=true`)
- Proxy support for this network environment (`--all-proxy=http://127.0.0.1:17890`)

### Preferred workflow

1. For datasets already registered in this project, use the existing script:
   ```bash
   python scripts/data_acquisition/download_zenodo_aria2.py
   ```

2. For ad-hoc downloads, prefer the global download helper so other agents and projects use the same flags and fallback chain:
   ```bash
   python -m download_tools <URL> <output-path>
   # or
   python D:\aicoding\Lib\download_tools\download.py <URL> <output-path>
   ```
   If the helper is unavailable, use aria2c directly:
   ```bash
   aria2c --all-proxy=http://127.0.0.1:17890 \
          --split=16 \
          --max-connection-per-server=16 \
          --min-split-size=1M \
          --continue=true \
          --file-allocation=none \
          --max-tries=0 \
          --retry-wait=5 \
          --timeout=60 \
          --connect-timeout=30 \
          --auto-file-renaming=false \
          --allow-overwrite=true \
          -d <output-dir> \
          -o <output-name> \
          <URL>
   ```

3. Only fall back to `curl`, `wget`, or Python `urllib.request` when aria2c is unavailable or the target explicitly requires a simple single-stream download.

### Global reusable library

Cross-project download helpers live in `D:\aicoding\Lib\download_tools`:
- `download(url, dest)` — unified API, aria2c first, then curl/wget/urllib
- `download_many(items)` — batch downloads
- `find_aria2()` — locate aria2c on this machine

See `D:\aicoding\Lib\download_tools\README.md` for usage examples.

### Locate aria2c

If `aria2c` is not on `PATH`, check the known locations in this environment:
- `C:\Users\10175\AppData\Local\aria2\aria2-1.37.0-win-64bit-build1\aria2c.exe`
- `C:\Users\10175\AppData\Local\aria2c.exe`
- `C:\Program Files\Netease\GameViewer\bin\aria2c.exe`

## Academic research collaboration (Codex / Cursor / Claude)

Shared knowledge lives in `D:/aicoding/lib/Codex-Academic-Research/` (DIGEST + playbooks).
Installed suite: `$academic-research-suite` (ARS-Codex single skill — do **not** expect four split Claude-layout skills).

### Role
You are an academic research collaborator. Do not invent facts or citations. Do not make final scientific judgments for the author.

### Boundaries
- Ground literature claims in `papers/literature/`, `D:/aicoding/lib/powergrid_paper/`, or files the user points to.
- Never fabricate papers, authors, DOIs, venues, page numbers, or numeric results.
- Mark insufficient evidence as「待核实」; do not upgrade guesses into conclusions.
- Prefer a short plan before rewriting a whole manuscript.
- Speak like a reviewer when asked to critique: direct, no fluff.

### Capability routing
- Research / writing / review pipeline → `academic-research-suite` (aliases: `ars-plan`, `ars-lit-review`, `ars-citation-check`, `ars-full`, …)
- Journal fit / APC / house style → `Paper_CCF` (`D:/aicoding/lib/Paper_CCF` or `~/.claude/skills/Paper_CCF`)
- Local acceptance-pattern distill → IdeaSpark / RepLLM under `powergrid_paper/metadata/`
- Citation / figure-table / de-AIGC gates → `aers-powergrid-bridge`
- Task playbooks → `D:/aicoding/lib/Codex-Academic-Research/playbooks.md`

### Task framing (Goal / Context / Constraints / Done when)
State the goal, relevant paths, hard constraints (e.g. no new fabricated cites), and done criteria for each academic request.
