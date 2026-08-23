"""R2 assembled view with three mounts and simplified M3 hardware envelopes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_geometry import assembled_shape


def gen_step():
    return assembled_shape()
