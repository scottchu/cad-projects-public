"""Progressive P0 manual-slider geometry and frozen interface contract."""

from .assembly import make_p0_assembly, placed_shuttle
from .geometry import make_back_insert, make_housing, make_shuttle
from .spec import P0, P0Spec

__all__ = [
    "P0",
    "P0Spec",
    "make_back_insert",
    "make_housing",
    "make_p0_assembly",
    "make_shuttle",
    "placed_shuttle",
]
