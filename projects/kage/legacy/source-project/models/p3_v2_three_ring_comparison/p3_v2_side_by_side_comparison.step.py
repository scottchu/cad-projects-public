from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v2_three_ring_comparison_geometry import make_side_by_side_comparison
def gen_step(): return make_side_by_side_comparison()
