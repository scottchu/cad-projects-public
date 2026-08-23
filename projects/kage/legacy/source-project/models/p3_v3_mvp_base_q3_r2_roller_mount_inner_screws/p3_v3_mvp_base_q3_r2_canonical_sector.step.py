"""Accepted r0 canonical 120 degree sector in U1 print orientation; print x3."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_geometry import canonical_printable_sector_shape


def gen_step():
    return canonical_printable_sector_shape()
