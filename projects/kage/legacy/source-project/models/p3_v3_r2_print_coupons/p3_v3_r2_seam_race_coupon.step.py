"""CAD Viewer entry point for coupon A."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_r2_print_coupon_geometry import make_seam_coupon_assembly


def gen_step():
    return make_seam_coupon_assembly()

