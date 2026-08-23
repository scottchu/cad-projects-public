from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_mvp_ring_seam_c_interlock_m2_r1_geometry import make_hour_coupon


def gen_step():
    return make_hour_coupon()
