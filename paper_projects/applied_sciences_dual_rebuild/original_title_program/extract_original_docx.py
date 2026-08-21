"""Deterministically extract the two author-supplied original-title DOCX files.

The extractor uses only the Python standard library.  It preserves paragraph
order, paragraph style identifiers, tables, package media inventory, and the
SHA-256 of the source DOCX.  It does not alter the source documents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def element_text(element: ET.Element) -> str:
    return "".join((node.text or "") for node in element.iter(W + "t")).strip()


def paragraph_style(element: ET.Element) -> str:
    node = element.find("./" + W + "pPr/" + W + "pStyle")
    return node.get(W + "val", "") if node is not None else ""


def extract(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        body = root.find(W + "body")
        if body is None:
            raise ValueError(f"missing document body: {path}")

        blocks: list[dict] = []
        headings: list[dict] = []
        table_number = 0
        paragraph_number = 0
        for position, element in enumerate(list(body)):
            if element.tag == W + "p":
                text = element_text(element)
                style = paragraph_style(element)
                if not text:
                    continue
                paragraph_number += 1
                record = {
                    "kind": "paragraph",
                    "position": position,
                    "paragraph_number": paragraph_number,
                    "style": style,
                    "text": text,
                }
                blocks.append(record)
                if (
                    style.lower().startswith("heading")
                    or style in {"2", "3", "4", "5"}
                    or re.match(r"^\d+(?:\.\d+)*[.\s]+[A-Z]", text)
                    or text in {"Abstract", "References", "Appendix"}
                ):
                    headings.append(record.copy())
            elif element.tag == W + "tbl":
                table_number += 1
                rows: list[list[str]] = []
                for row in element.findall("./" + W + "tr"):
                    rows.append([element_text(cell) for cell in row.findall("./" + W + "tc")])
                blocks.append(
                    {
                        "kind": "table",
                        "position": position,
                        "table_number": table_number,
                        "rows": rows,
                    }
                )

        media = []
        for name in sorted(archive.namelist()):
            if name.startswith("word/media/") and not name.endswith("/"):
                payload = archive.read(name)
                media.append(
                    {
                        "name": name,
                        "bytes": len(payload),
                        "sha256": hashlib.sha256(payload).hexdigest(),
                    }
                )

    return {
        "schema_version": "original-title-docx-extract-v1",
        "source": str(path.resolve()),
        "source_bytes": path.stat().st_size,
        "source_sha256": sha256(path),
        "headings": headings,
        "blocks": blocks,
        "media": media,
    }


def render_markdown(data: dict) -> str:
    lines = [
        f"# Extracted source: {Path(data['source']).name}",
        "",
        f"- Source SHA-256: `{data['source_sha256']}`",
        f"- Source bytes: {data['source_bytes']}",
        "- Status: deterministic text/table extraction; not a visual-layout verification.",
        "",
    ]
    for block in data["blocks"]:
        if block["kind"] == "paragraph":
            text = block["text"]
            style = block["style"]
            if block in data["headings"] or style in {"2", "3", "4", "5"}:
                level = {"2": 1, "3": 2, "4": 3, "5": 4}.get(style, 3)
                lines.extend(["#" * level + " " + text, ""])
            else:
                lines.extend([text, ""])
        else:
            lines.extend([f"**Table {block['table_number']} (source order)**", ""])
            rows = block["rows"]
            if rows:
                width = max(len(row) for row in rows)
                normalized = [row + [""] * (width - len(row)) for row in rows]
                lines.append("| " + " | ".join(normalized[0]) + " |")
                lines.append("| " + " | ".join(["---"] * width) + " |")
                for row in normalized[1:]:
                    lines.append("| " + " | ".join(row) + " |")
                lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    sources = sorted(args.input_dir.glob("*.docx"))
    if len(sources) != 2:
        raise SystemExit(f"expected exactly two DOCX files, found {len(sources)}")
    manifest = []
    for index, source in enumerate(sources, start=1):
        data = extract(source)
        slug = "c2ges" if "Causal" in source.name else "ma_sqlgrid"
        json_path = args.output_dir / f"{slug}_source_extract.json"
        md_path = args.output_dir / f"{slug}_source_extract.md"
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(render_markdown(data), encoding="utf-8")
        manifest.append(
            {
                "index": index,
                "slug": slug,
                "source": data["source"],
                "source_sha256": data["source_sha256"],
                "json": str(json_path.resolve()),
                "markdown": str(md_path.resolve()),
            }
        )
    (args.output_dir / "SOURCE_MANIFEST.json").write_text(
        json.dumps({"schema_version": "original-title-source-manifest-v1", "items": manifest}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
