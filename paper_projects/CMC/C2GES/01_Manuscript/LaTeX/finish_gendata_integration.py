"""Final manuscript touches for the GenData synthetic-fixture integration."""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EDITS = (
    (
        "A fourth layer scores a four-series synthetic stress set, which exercises software and endpoint "
        "alignment on fictional fixtures rather than real-report validity.",
        "A fourth layer scores a parent--held-out synthetic stress pair, which exercises software and "
        "endpoint alignment on fictional fixtures rather than real-report validity.",
    ),
    (
        "the dataset card for the incident family, and the derived tables behind Supplementary Tables~S14--S19 "
        "and Figure~S5.",
        "the dataset card for the incident family, and the derived tables behind Supplementary Tables~S14--S20 "
        "and Figure~S5. The frozen parent--held-out synthetic stress fixtures are distributed as "
        "\\nolinkurl{03_Reproducibility/Data/synthetic_stress_v1/run_20260927_gendata_parent_v3r1/} and "
        "\\nolinkurl{03_Reproducibility/Data/synthetic_stress_v1/run_20260927_gendata_heldout_v2r3/}: the "
        "sixteen fictional reports, their semantic cores, the nineteen-gate ledgers, the component-factorial "
        "records, the frozen generation protocol, its freeze record and the dataset card (all synthetic, "
        "author-generated, and non-confirmatory).",
    ),
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:70]!r}")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print("gendata integration edits applied")


if __name__ == "__main__":
    main()
