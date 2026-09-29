#!/usr/bin/env python3
"""Extract PDF hrefs from a downloaded official collection page."""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.anchors: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(html.unescape(href))
                self._href = html.unescape(href)
                self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href:
            self.anchors.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--contains", action="append", default=[])
    parser.add_argument("--text-contains", action="append", default=[])
    args = parser.parse_args()
    links = Links()
    links.feed(args.html.read_text(encoding="utf-8", errors="ignore"))
    needles = [value.casefold() for value in args.contains]
    text_needles = [value.casefold() for value in args.text_contains]
    matches = sorted({urljoin(args.base, href) for href, anchor_text in links.anchors
                      if ".pdf" in href.casefold()
                      and (not needles or any(value in href.casefold() for value in needles))
                      and (not text_needles or any(value in anchor_text.casefold() for value in text_needles))})
    for value in matches:
        print(value)


if __name__ == "__main__":
    main()
