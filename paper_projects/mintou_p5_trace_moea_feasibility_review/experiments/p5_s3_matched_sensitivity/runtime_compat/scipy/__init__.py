"""Minimal SciPy compatibility surface for the prespecified optimizer rerun.

The execution host has a NumPy-compatible CPython interpreter but its installed
SciPy extension modules target the free-threaded ABI.  Pymoo 0.6.2 only needs
Euclidean distance helpers and ``special.binom`` for the methods used here.
Statistical functions are intentionally unavailable so this shim cannot emit
inferential results.
"""

from . import spatial, special, stats

__all__ = ["spatial", "special", "stats"]
__version__ = "compat-p5-s3"

