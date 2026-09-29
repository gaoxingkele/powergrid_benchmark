"""Repair two overreaching claims and one stale layer map in the Results narrative."""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EDITS = [
    # 1. The layer map must name the two bounded layers added after the reduction.
    (
        "The evidence is presented in four explicitly separated layers (Table~\\ref{tab:evidence-layers}).",
        "The internal evidence is presented in four explicitly separated layers (Table~\\ref{tab:evidence-layers}), followed by two bounded layers that are not pooled with them: an adjacent-corpus construct audit of the role and edge cues (Section~4.10) and a prospective frozen external evaluation on a new report family (Section~4.11).",
    ),
    # 2. Scope the external claim: corrected contrasts also exist in the historical layer.
    (
        "These are the only contrasts in this study that survive family-wise correction, and they favour the simpler untyped ranking over the typed path channel rather than supporting it.",
        "Within the external corpus these are the only two contrasts that survive family-wise correction, and they favour the simpler untyped ranking over the typed path channel rather than supporting it. The historical equal-unit layer contains corrected wins for Full against both baselines at the smaller budget, which the length diagnostic below qualifies; the correction-carrying evidence therefore points in different directions across layers.",
    ),
    # 3. Same correction in the Discussion.
    (
        "so the only corrected system-level evidence in this study favours the untyped ranking over the typed path.",
        "so the corrected external contrasts favour the untyped ranking over the typed path, while the historical equal-unit layer still contains corrected wins for Full against both baselines at the smaller budget. Correction-carrying system evidence therefore points in different directions across layers instead of supporting one method.",
    ),
]


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:70]!r}")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print(f"applied {len(EDITS)} narrative repairs")


if __name__ == "__main__":
    main()
