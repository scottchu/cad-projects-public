"""Project-local compatibility surface for legacy KAGE color-only imports.

The locked KAGE geometry used only ``cadgen.srgb``.  Keeping this tiny helper
inside the uv project makes the historical source reproducible without adding
the external CAD-skill runtime as an undeclared dependency.
"""

from p3_v3_locked_parametric_repair_r1_color import srgb

__all__ = ["srgb"]

