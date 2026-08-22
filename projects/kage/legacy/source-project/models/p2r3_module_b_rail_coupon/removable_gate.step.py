from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p2r3_module_b_rail_coupon_geometry import make_removable_gate
def gen_step(): return make_removable_gate()
