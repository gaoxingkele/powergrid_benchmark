#!/usr/bin/env python3
"""Read-only fail-closed verifier for the hand-frozen v3 input contract."""
import hashlib, json, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=HERE/"EXPECTED_INPUT_HASHES.json"
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def main():
    try: c=json.loads(CONTRACT.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL-CLOSED: unreadable contract: {exc}",file=sys.stderr); return 2
    checked=0
    for section in ("v2_accepted_upstream_inputs","v2_products_consumed"):
        if section not in c or not isinstance(c[section],dict) or not c[section]:
            print(f"FAIL-CLOSED: missing/empty contract section {section}",file=sys.stderr); return 2
        for rel,expected in c[section].items():
            p=ROOT/rel
            if not p.is_file(): print(f"FAIL-CLOSED: missing {rel}",file=sys.stderr); return 2
            actual=sha(p)
            if actual != expected: print(f"FAIL-CLOSED: hash mismatch {rel}\nexpected {expected}\nactual   {actual}",file=sys.stderr); return 2
            checked+=1
    print(f"PASS: {checked} immutable upstream/v2 inputs match the expected hash contract")
    return 0
if __name__=="__main__": raise SystemExit(main())
