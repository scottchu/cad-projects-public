from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_stacked_three_motor_90deg_geometry import make_axial_side_section
def gen_step(): return make_axial_side_section()
