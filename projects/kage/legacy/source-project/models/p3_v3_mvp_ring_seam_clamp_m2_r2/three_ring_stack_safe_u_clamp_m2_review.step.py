from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_mvp_ring_seam_clamp_m2_r2_geometry import make_three_ring_stack


def gen_step():
    return make_three_ring_stack(include_hardware=True)
