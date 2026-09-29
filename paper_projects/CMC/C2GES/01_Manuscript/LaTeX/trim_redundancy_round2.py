"""Remove four repeats of claims already made in adjacent text (length control, no content loss)."""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EDITS = (
    (
        " None of these sensitivities is a fresh confirmatory test.",
        "",
    ),
    (
        "A separate post-run word-cap sensitivity, defined after the primary result was visible, is described "
        "below and remains outside the confirmatory family.",
        "A post-run word-cap sensitivity, defined after the primary result was visible, remains outside the "
        "confirmatory family.",
    ),
    (
        "that unrenormalized contrast is a scale-coupled historical diagnostic, not the component estimand.",
        "that unrenormalized contrast is scale-coupled.",
    ),
    (
        "The extension is reported as a sensitivity rather than as a pre-registered test: on this corpus the "
        "sign direction is stable while mean-based inference is not.",
        "The extension is a sensitivity rather than a pre-registered test: the sign direction is stable while "
        "mean-based inference is not.",
    ),
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:60]!r}")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print("round-2 trims applied")


if __name__ == "__main__":
    main()
