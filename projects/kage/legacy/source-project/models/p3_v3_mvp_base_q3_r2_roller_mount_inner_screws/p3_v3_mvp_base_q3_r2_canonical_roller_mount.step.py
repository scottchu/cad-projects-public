"""Canonical seated two-hole free-roller mount base in print orientation; print x3."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_geometry import printable_roller_mount_shape


def gen_step():
    return printable_roller_mount_shape()
