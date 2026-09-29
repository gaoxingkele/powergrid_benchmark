"""One-shot stdio client for the C2GES synthetic MCP server."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SERVER = Path(__file__).resolve().parent / "server.py"
PY = sys.executable


class McpClient:
    def __init__(self, proc: subprocess.Popen) -> None:
        self.proc = proc
        self._id = 0

    def call(self, method: str, params: dict | None = None, notify: bool = False) -> dict | None:
        self._id += 1
        payload: dict = {"jsonrpc": "2.0", "method": method}
        if not notify:
            payload["id"] = self._id
        if params is not None:
            payload["params"] = params
        body = json.dumps(payload).encode("utf-8")
        self.proc.stdin.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
        self.proc.stdin.flush()
        if notify:
            return None
        headers = b""
        while not headers.endswith(b"\r\n\r\n"):
            chunk = self.proc.stdout.read(1)
            if not chunk:
                raise RuntimeError("MCP server closed")
            headers += chunk
        length = int(headers.decode("ascii").split("Content-Length:")[1].split("\r\n")[0].strip())
        body = self.proc.stdout.read(length)
        return json.loads(body.decode("utf-8"))


def main() -> None:
    proc = subprocess.Popen(
        [PY, "-u", str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    client = McpClient(proc)
    try:
        init = client.call(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "c2ges-call-mcp", "version": "1"},
            },
        )
        client.call("notifications/initialized", notify=True)
        listed = client.call("tools/list")
        status = client.call("tools/call", {"name": "synthetic_status", "arguments": {}})
        gates = client.call("tools/call", {"name": "evaluate_synthetic", "arguments": {}})
        ethics = client.call(
            "tools/call",
            {"name": "claim_gate", "arguments": {"action": "issue_ethics_approval"}},
        )
        expert = client.call(
            "tools/call",
            {"name": "claim_gate", "arguments": {"action": "upgrade_llm_to_expert"}},
        )
        human = client.call(
            "tools/call",
            {"name": "claim_gate", "arguments": {"action": "complete_human_annotation"}},
        )
        kappa = client.call(
            "tools/call",
            {"name": "debug_kappa", "arguments": {"a": ["y", "y", "n", "n"], "b": ["y", "y", "n", "n"]}},
        )
        report = {
            "initialize": init["result"]["serverInfo"],
            "tools": [t["name"] for t in listed["result"]["tools"]],
            "synthetic_status": json.loads(status["result"]["content"][0]["text"]),
            "evaluate_synthetic": json.loads(gates["result"]["content"][0]["text"]),
            "claim_gate": {
                "ethics": json.loads(ethics["result"]["content"][0]["text"]),
                "llm_expert": json.loads(expert["result"]["content"][0]["text"]),
                "human": json.loads(human["result"]["content"][0]["text"]),
            },
            "debug_kappa": json.loads(kappa["result"]["content"][0]["text"]),
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    finally:
        proc.kill()


if __name__ == "__main__":
    main()
