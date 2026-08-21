"""Generate the installed output-relevant dependency closure for v0.3.1."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
from collections import deque

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


ROOTS = (
    "networkx",
    "numpy",
    "rouge-score",
    "sentence-transformers",
    "torch",
)


def installed_closure() -> dict[str, str]:
    queue = deque(ROOTS)
    found: dict[str, str] = {}
    while queue:
        requested = queue.popleft()
        normalized = canonicalize_name(requested)
        if normalized in found:
            continue
        distribution = importlib.metadata.distribution(requested)
        canonical = canonicalize_name(distribution.metadata["Name"])
        found[canonical] = distribution.version
        for raw in distribution.requires or ():
            requirement = Requirement(raw)
            if requirement.marker is not None and not requirement.marker.evaluate({"extra": ""}):
                continue
            dependency = canonicalize_name(requirement.name)
            try:
                importlib.metadata.distribution(dependency)
            except importlib.metadata.PackageNotFoundError:
                continue
            queue.append(dependency)
    return dict(sorted(found.items()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    payload = {
        "schema": "C2GES-output-dependency-lock-v1",
        "python": platform.python_version(),
        "roots": list(ROOTS),
        "resolution": "recursive installed Requires-Dist closure with environment markers evaluated and extras disabled",
        "packages": installed_closure(),
    }
    with open(args.output, "w", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


if __name__ == "__main__":
    main()
