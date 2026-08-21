#!/usr/bin/env python3
"""Compatibility stand-in for the original ``researchclaw.llm.client``.

The original researchclaw package (the LLM client used for the archived
gpt-5.4-mini/krill formal run) is STILL MISSING from the supplement drop of
2026-07-20. This module exists so that the received support modules
(``minimal_text2sql_smoke``, ``dev_chess_style_pilot``, ...) and ``main.py``
can be imported and re-driven against any OpenAI-compatible
chat-completions endpoint.

Interface reproduced from the call sites in the received modules:

* ``LLMConfig(base_url, api_key, primary_model, fallback_models, max_tokens,
  temperature, timeout_sec, wire_api)``
* ``LLMClient(config).chat(messages, max_tokens=..., temperature=...)`` ->
  response object with ``.content``, ``.model``, ``.prompt_tokens``,
  ``.completion_tokens``

Fidelity notes:

* ``wire_api="chat"`` uses the standard OpenAI ``/chat/completions`` wire
  (stdlib urllib, mirroring ``run_second_model.ChatClient``).
* ``wire_api="responses"`` (the krill codex wire used by the archived run)
  is NOT reimplemented; calling it raises, because guessing the proprietary
  wire format would silently diverge from the archived behaviour. Import-time
  resolution works either way.
"""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMConfig:
    base_url: str
    api_key: str
    primary_model: str
    fallback_models: list[str] = field(default_factory=list)
    max_tokens: int = 700
    temperature: float = 0.0
    timeout_sec: int = 90
    wire_api: str = "chat"


@dataclass
class LLMResponse:
    content: str
    model: str
    prompt_tokens: int
    completion_tokens: int


class LLMClient:
    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> LLMResponse:
        cfg = self.config
        if cfg.wire_api not in {"chat", "chat_completions", "openai"}:
            raise NotImplementedError(
                f"wire_api={cfg.wire_api!r} requires the original researchclaw client, "
                "which is still missing from the supplement; this compatibility client "
                "only implements the OpenAI chat-completions wire."
            )
        payload = {
            "model": cfg.primary_model,
            "messages": messages,
            "temperature": cfg.temperature if temperature is None else temperature,
            "max_tokens": cfg.max_tokens if max_tokens is None else max_tokens,
        }
        req = urllib.request.Request(
            f"{cfg.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cfg.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=cfg.timeout_sec) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        usage = body.get("usage") or {}
        return LLMResponse(
            content=body["choices"][0]["message"]["content"] or "",
            model=body.get("model") or cfg.primary_model,
            prompt_tokens=int(usage.get("prompt_tokens") or 0),
            completion_tokens=int(usage.get("completion_tokens") or 0),
        )
