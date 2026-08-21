"""Remove only validated Python cache files below this final-candidate tree."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    targets = sorted(path for path in ROOT.rglob("__pycache__") if path.is_dir())
    for target in targets:
        target.resolve().relative_to(ROOT.resolve())
        if target.is_symlink():
            raise RuntimeError(f"refused symlink: {target}")
        descendants = list(target.rglob("*"))
        if any(path.is_symlink() for path in descendants):
            raise RuntimeError(f"refused nested symlink: {target}")
        unexpected = [path for path in descendants if path.is_file() and path.suffix != ".pyc"]
        if unexpected:
            raise RuntimeError(f"refused non-pyc cache content: {unexpected}")
    for target in targets:
        shutil.rmtree(target)
    print(f"removed_validated_python_cache_directories={len(targets)}")


if __name__ == "__main__":
    main()
