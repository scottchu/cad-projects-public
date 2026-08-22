"""Assembled Q3 base with three identical four-hole flat clamps."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp_geometry import assembled_shape


def gen_step():
    return assembled_shape()


if __name__ == "__main__":
    from build123d import export_step

    export_step(gen_step(), str(Path(__file__).with_suffix("")))
