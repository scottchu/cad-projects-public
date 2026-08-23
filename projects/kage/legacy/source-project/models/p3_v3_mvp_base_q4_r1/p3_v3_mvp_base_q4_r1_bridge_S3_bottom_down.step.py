import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p3_v3_mvp_base_q4_r1_geometry import printable_bridge_shape


def gen_step():
    return printable_bridge_shape(3)
