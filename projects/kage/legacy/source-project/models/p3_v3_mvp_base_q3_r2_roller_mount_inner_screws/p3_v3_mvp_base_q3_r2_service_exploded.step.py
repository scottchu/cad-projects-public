"""R2 service view with sectors, mounts, screws, and nuts separated for review."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_geometry import service_exploded_shape


def gen_step():
    return service_exploded_shape()
