"""Materialize immutable v1.0 code snapshots without altering live files.

Concurrent workspace work added the authorized v1.1 warning guard directly to
two live v1.0 files.  This script reverses only those exact additive hunks into
new snapshot files and refuses output unless the historical frozen hashes match.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_exact(source: str, target: str, replacements: list[tuple[str, str]], expected: str) -> None:
    text = (ROOT / source).read_text(encoding="utf-8")
    for old, new in replacements:
        if text.count(old) != 1:
            raise SystemExit(f"Expected exactly one authorized drift hunk in {source}: {old!r}")
        text = text.replace(old, new)
    data = text.encode("utf-8")
    actual = sha_bytes(data)
    if actual != expected:
        raise SystemExit(f"Recovered snapshot hash mismatch for {source}: {actual} != {expected}")
    (ROOT / target).write_bytes(data)


def main() -> None:
    write_exact(
        "freeze_public_baseline.py",
        "freeze_public_baseline_v1_0_snapshot.py",
        [(
            "    except (sqlite3.Error, sqlite3.Warning) as exc:\n"
            "        # sqlite3.Warning is NOT a subclass of sqlite3.Error; multi-statement\n"
            "        # model outputs raise it (\"You can only execute one statement at a\n"
            "        # time\") and must be classified, not crash the run.\n",
            "    except sqlite3.Error as exc:\n",
        )],
        "d715d17f3d220fa5d17667ec2603c5290c0b2131ede8fc4ab674776455289d23",
    )
    write_exact(
        "test_public_baseline_freeze.py",
        "test_public_baseline_freeze_v1_0_snapshot.py",
        [(
            "\n    def test_multi_statement_output_is_classified(self):\n"
            "        # sqlite3.Warning (not an sqlite3.Error subclass) must classify, not raise.\n"
            "        status, rows = f.safe_execute(\"SELECT x FROM a; SELECT x FROM a\", self.db)\n"
            "        self.assertEqual(status, \"OTHER_EXECUTION_ERROR\")\n"
            "        self.assertIsNone(rows)\n"
            "        self.assertIn(status, f.FEEDBACK)\n",
            "",
        )],
        "ffc00d3cd004fd4f1f09de7b598c481b9eba366ac8edd33f4e70b67c39f91a01",
    )
    print("v1.0 snapshot hashes recovered exactly")


if __name__ == "__main__":
    main()
