#!/usr/bin/env python3
"""Path-compatibility re-export of the packaged evaluator.

`main.py` and the received smoke modules import a top-level ``evaluator``
module via sys.path entries (``WORKSPACE/evaluator`` and
``STAGE10_DIR/agent_reference``) that do not contain the packaged evaluator,
which lives at ``code/evaluator/evaluator.py``. This shim loads the canonical
file and re-exports its public names so the original import statements
resolve without duplicating evaluator code.
"""

from __future__ import annotations

import importlib.util as _ilu
import sys as _sys
from pathlib import Path as _Path

_CANONICAL = _Path(__file__).resolve().parents[1] / "evaluator" / "evaluator.py"
_spec = _ilu.spec_from_file_location("_ma_sqlgrid_canonical_evaluator", _CANONICAL)
_mod = _ilu.module_from_spec(_spec)
_sys.modules[_spec.name] = _mod  # dataclasses requires the module in sys.modules
_spec.loader.exec_module(_mod)

globals().update({_k: _v for _k, _v in vars(_mod).items() if not _k.startswith("__")})
