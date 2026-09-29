"""Qualify the "provisional default" claim in the Conclusions after the external run."""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

OLD = (
    "No-path \\cges{} is the provisional default. System superiority, semantic validity of the "
    "structural proxies, and operational benefit are not established by this study."
)
NEW = (
    "No-path \\cges{} remains the provisional default within the internal evidence, and the external "
    "run qualifies that choice rather than confirming it: on the new corpus an untyped graph baseline "
    "exceeded no-path at 260 words while the typed path channel fell below it, so neither the framework "
    "nor its simpler configuration carries a demonstrated accuracy advantage. System superiority, "
    "semantic validity of the structural proxies, and operational benefit are not established by this study."
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise AssertionError(f"anchor occurs {count} times")
    TEX.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print("conclusions qualified")


if __name__ == "__main__":
    main()
