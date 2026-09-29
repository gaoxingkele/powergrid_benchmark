from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from call_mcp import McpClient, SERVER, PY


class C2gesMcpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.proc = subprocess.Popen(
            [PY, "-u", str(SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.client = McpClient(self.proc)
        self.client.call(
            "initialize",
            {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}},
        )
        self.client.call("notifications/initialized", notify=True)

    def tearDown(self) -> None:
        self.proc.kill()
        self.proc.wait(timeout=5)

    def test_lists_synthetic_tools(self) -> None:
        listed = self.client.call("tools/list")
        names = {t["name"] for t in listed["result"]["tools"]}
        self.assertEqual(
            names,
            {"synthetic_status", "evaluate_synthetic", "build_synthetic_heldout", "claim_gate", "debug_kappa"},
        )

    def test_evaluate_existing_v8(self) -> None:
        result = self.client.call("tools/call", {"name": "evaluate_synthetic", "arguments": {}})
        payload = json.loads(result["result"]["content"][0]["text"])
        self.assertTrue(payload["deterministic_gate_pass"])
        self.assertFalse(payload["confirmatory_claims_allowed"])

    def test_claim_gate_refuses_ethics_and_expert_upgrade(self) -> None:
        for action in ("issue_ethics_approval", "upgrade_llm_to_expert", "complete_human_annotation"):
            result = self.client.call("tools/call", {"name": "claim_gate", "arguments": {"action": action}})
            payload = json.loads(result["result"]["content"][0]["text"])
            self.assertFalse(payload["allowed"])
            self.assertFalse(payload["confirmatory_claims_allowed"])


if __name__ == "__main__":
    unittest.main()
