# C2GES synthetic MCP

Local stdio MCP server wrapping fictional synthetic-stress tools.

Registered in repo `.grok/config.toml` as `c2ges_synthetic`. Restart Grok to load it in a new session, or call:

```text
python call_mcp.py
```

## Tools

- `synthetic_status` — list synthetic runs
- `evaluate_synthetic` — frozen distribution gates
- `build_synthetic_heldout` — new fictional set; refuses overwrite
- `debug_kappa` — Cohen’s κ on debug label lists
- `claim_gate` — **refuses** human annotation, ethics approval, LLM-as-expert, and promoting synthetic to real

These fixtures are not expert gold and cannot support confirmatory claims.
