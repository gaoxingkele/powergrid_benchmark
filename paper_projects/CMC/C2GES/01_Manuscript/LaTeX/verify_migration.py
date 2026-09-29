"""Verify the Applied Sciences -> Information migration changed format only."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE / "paper_applsci.tex.ORIG"
B = HERE / "paper_information.tex"

a = A.read_text(encoding="utf-8")
b = B.read_text(encoding="utf-8")

fails = 0

print("=== numeric multiset ===")
na, nb = sorted(re.findall(r"\d+\.?\d*", a)), sorted(re.findall(r"\d+\.?\d*", b))
same = na == nb
fails += not same
print(f"  orig={len(na)} now={len(nb)}  {'IDENTICAL' if same else 'DIFFER'}")
if not same:
    import collections
    print("   only-orig:", dict((collections.Counter(na) - collections.Counter(nb)).most_common(8)))
    print("   only-now :", dict((collections.Counter(nb) - collections.Counter(na)).most_common(8)))

print("\n=== key sets ===")
for label, pat in {
    "cite": r"\\cite\{([^}]*)\}",
    "ref": r"\\ref\{([^}]*)\}",
    "label": r"\\label\{([^}]*)\}",
}.items():
    x, y = re.findall(pat, a), re.findall(pat, b)
    ok = x == y
    fails += not ok
    print(f"  {label:6s} orig={len(x):3d} now={len(y):3d}  {'IDENTICAL' if ok else 'DIFFER'}")

print("\n=== line-level diff (format lines only?) ===")
la, lb = a.split("\n"), b.split("\n")
import difflib
changed = [l for l in difflib.unified_diff(la, lb, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
print(f"  changed lines: {len(changed)}")
for l in changed[:12]:
    print("   ", l[:120])

print(f"\nRESULT: {'FORMAT-ONLY MIGRATION CONFIRMED' if fails == 0 else f'{fails} CHECK(S) FAILED'}")
sys.exit(1 if fails else 0)
