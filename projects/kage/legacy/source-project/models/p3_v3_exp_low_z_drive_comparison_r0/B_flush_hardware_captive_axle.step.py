import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_exp_low_z_drive_comparison_r0_geometry import make_flush_hardware_B


def gen_step():
    return make_flush_hardware_B()
