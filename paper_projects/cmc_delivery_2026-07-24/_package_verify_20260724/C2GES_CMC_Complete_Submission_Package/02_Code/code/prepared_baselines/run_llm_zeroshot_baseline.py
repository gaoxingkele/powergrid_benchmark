#!/usr/bin/env python3
"""Prepared zero-shot LLM evidence-selection baseline for the C2GES benchmark.

Asks an OpenAI-compatible chat-completions endpoint to select the top-K
evidence sentence IDs for each of the 200 role-conditioned questions, under the
paper's protocol (same data, K=3 budget, metrics, and document-cluster
bootstrap). Uses only the Python standard library for HTTP, so it has no extra
dependencies beyond the code package's requirements.

The endpoint is fully parameterized, so this works with OpenAI, vLLM, Ollama
(with --base-url http://localhost:11434/v1), or any compatible gateway.
Responses are cached to <out-dir>/llm_response_cache.jsonl so interrupted runs
resume without re-billing.

Example (once the workspace data is supplied; see MISSING_ARTIFACTS.md):
    export OPENAI_API_KEY=...
    python run_llm_zeroshot_baseline.py \
        --model gpt-4o-mini \
        --base-url https://api.openai.com/v1 \
        --data-dir /path/to/verification_pilot/agent_audit_40doc \
        --out-dir  ./outputs/llm_zeroshot_gpt4omini \
        --reference-details /path/to/c2ges_role_selective_graph/details.jsonl
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from common import build_arg_parser, run_and_write

SYSTEM_PROMPT = (
    "You select evidence sentences from public NERC power-grid reliability reports. "
    "You answer with sentence IDs only, in the exact JSON format requested."
)

USER_PROMPT_TEMPLATE = """Report sentences (one per line, format `sid: text`):
{sentence_block}

Causal role: {role}
Question: {question}

Select exactly {k} sentence IDs from the list above that best answer the question
for this causal role. Reply with ONLY a JSON array of sentence IDs, most relevant
first, for example: ["s003", "s017", "s042"]."""


def chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    timeout: float,
    max_retries: int,
    retry_wait: float,
) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            return str(body["choices"][0]["message"]["content"])
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(retry_wait * (2**attempt))
    raise RuntimeError(f"LLM request failed after {max_retries + 1} attempts: {last_error}")


def parse_sentence_ids(response_text: str, valid_sids: list[str], k: int) -> list[str]:
    """Extract up to k valid sentence IDs from the model response, order-preserving.

    Prefers the first JSON array in the response; falls back to scanning for
    known sentence IDs anywhere in the text. Never invents IDs and never pads.
    """
    valid = set(valid_sids)
    candidates: list[str] = []
    array_match = re.search(r"\[[^\[\]]*\]", response_text, flags=re.DOTALL)
    if array_match:
        try:
            parsed = json.loads(array_match.group(0))
            if isinstance(parsed, list):
                candidates = [str(item).strip() for item in parsed]
        except json.JSONDecodeError:
            candidates = []
    if not candidates:
        # Fallback: scan for any token that is a known sid (e.g. s003).
        pattern = re.compile(r"\b(" + "|".join(re.escape(sid) for sid in valid_sids) + r")\b")
        candidates = pattern.findall(response_text)
    selected: list[str] = []
    for sid in candidates:
        if sid in valid and sid not in selected:
            selected.append(sid)
        if len(selected) == k:
            break
    return selected


class ResponseCache:
    """Append-only jsonl cache so interrupted runs resume without re-billing."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.entries: dict[str, str] = {}
        if path.is_file():
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    self.entries[str(record["key"])] = str(record["response"])

    def get(self, key: str) -> str | None:
        return self.entries.get(key)

    def put(self, key: str, response: str) -> None:
        self.entries[key] = response
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"key": key, "response": response}) + "\n")


def main() -> None:
    parser = build_arg_parser(__doc__)
    parser.add_argument("--model", type=str, required=True, help="Model name, e.g. gpt-4o-mini.")
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://api.openai.com/v1",
        help="OpenAI-compatible API base URL (e.g. a vLLM or Ollama /v1 endpoint).",
    )
    parser.add_argument(
        "--api-key-env",
        type=str,
        default="OPENAI_API_KEY",
        help="Name of the environment variable holding the API key (may be unset for local endpoints).",
    )
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--request-timeout", type=float, default=120.0)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-wait", type=float, default=2.0, help="Base seconds for exponential backoff.")
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env, "")
    if not api_key:
        print(
            f"WARNING: environment variable {args.api_key_env} is empty; "
            "proceeding without Authorization header (fine for local endpoints)."
        )

    out_dir = Path(args.out_dir).expanduser().resolve()
    cache = ResponseCache(out_dir / "llm_response_cache.jsonl")

    def rank_fn(doc_id: str, qid: str, question: str, role: str, sids: list[str], texts: list[str]) -> list[str]:
        sentence_block = "\n".join(f"{sid}: {text}" for sid, text in zip(sids, texts, strict=True))
        prompt = USER_PROMPT_TEMPLATE.format(
            sentence_block=sentence_block,
            role=role.replace("_", " "),
            question=question,
            k=int(args.k),
        )
        cache_key = f"{args.model}::{doc_id}::{qid}::k={int(args.k)}"
        response_text = cache.get(cache_key)
        if response_text is None:
            response_text = chat_completion(
                base_url=str(args.base_url),
                api_key=api_key,
                model=str(args.model),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=float(args.temperature),
                max_tokens=int(args.max_tokens),
                timeout=float(args.request_timeout),
                max_retries=int(args.max_retries),
                retry_wait=float(args.retry_wait),
            )
            cache.put(cache_key, response_text)
        selected = parse_sentence_ids(response_text, sids, int(args.k))
        if not selected:
            raise ValueError(f"Could not parse any valid sentence IDs from model response: {response_text[:200]!r}")
        return selected

    extra_metadata: dict[str, Any] = {
        "model": str(args.model),
        "base_url": str(args.base_url),
        "api_key_env": str(args.api_key_env),
        "temperature": float(args.temperature),
        "max_tokens": int(args.max_tokens),
        "system_prompt": SYSTEM_PROMPT,
        "user_prompt_template": USER_PROMPT_TEMPLATE,
        "response_cache": str(out_dir / "llm_response_cache.jsonl"),
        "selection_policy": "parse JSON array of sids; never invent or pad IDs; unparseable responses are recorded as failed questions",
    }
    run_and_write(
        condition=f"llm_zeroshot::{args.model}",
        rank_fn=rank_fn,
        args=args,
        extra_metadata=extra_metadata,
    )


if __name__ == "__main__":
    main()
