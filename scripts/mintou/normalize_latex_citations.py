"""Convert Pandoc-style static numeric citations to LaTeX citation commands.

Only bracket groups that consist entirely of positive reference numbers,
commas, and ``--`` ranges are touched.  Author-input markers, confidence
intervals, units, and other bracketed prose remain unchanged.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEX_FILES = tuple(
    sorted(
        (ROOT / "paper_projects").glob(
            "mintou_*/manuscript/journal_submission/paper.tex"
        )
    )
)
STATIC_CITATION = re.compile(
    r"\{\[\}(\d+(?:(?:\s*,\s*|\s*--\s*)\d+)*)\{\]\}"
)


def citation_keys(value: str) -> list[str]:
    numbers: list[int] = []
    for part in re.split(r"\s*,\s*", value):
        range_match = re.fullmatch(r"(\d+)\s*--\s*(\d+)", part)
        if range_match:
            start, end = map(int, range_match.groups())
            if start > end or end - start > 100:
                raise ValueError(f"unsafe citation range: {part}")
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(part))
    unique = list(dict.fromkeys(numbers))
    return [f"ref{number}" for number in unique]


def normalize(path: Path, check_only: bool) -> int:
    text = path.read_text(encoding="utf-8")
    bibliography = set(re.findall(r"\\bibitem\{([^}]+)\}", text))

    def replace(match: re.Match[str]) -> str:
        keys = citation_keys(match.group(1))
        missing = [key for key in keys if key not in bibliography]
        if missing:
            raise ValueError(
                f"{path.relative_to(ROOT)} cites keys absent from its bibliography: {missing}"
            )
        return r"\cite{" + ",".join(keys) + "}"

    updated, count = STATIC_CITATION.subn(replace, text)
    if STATIC_CITATION.search(updated):
        raise RuntimeError(f"numeric static citation remains: {path.relative_to(ROOT)}")
    if not check_only and updated != text:
        path.write_text(updated, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    if len(TEX_FILES) != 6:
        raise SystemExit(f"expected six Mintou TeX files, found {len(TEX_FILES)}")
    total = 0
    for path in TEX_FILES:
        count = normalize(path, check_only=args.check)
        total += count
        print(f"{path.relative_to(ROOT)}: {count} citation groups")
    print(f"total={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
