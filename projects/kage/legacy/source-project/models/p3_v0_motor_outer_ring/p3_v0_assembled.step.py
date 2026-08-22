from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v0_motor_outer_ring_geometry import make_assembled
def gen_step(): return make_assembled()
