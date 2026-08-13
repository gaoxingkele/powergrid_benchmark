"""Distance-only subset of :mod:`scipy.spatial`."""

from . import distance
from .distance import cdist, pdist, squareform

__all__ = ["distance", "cdist", "pdist", "squareform"]

