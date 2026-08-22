from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_mvp_ring_seam_screw_only_r1_geometry import make_hour_coupon

result = make_hour_coupon()
