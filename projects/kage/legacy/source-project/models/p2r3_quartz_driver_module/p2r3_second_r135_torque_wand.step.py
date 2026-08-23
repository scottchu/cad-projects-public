from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p2r3_quartz_driver_module_geometry import make_full_radius_second_torque_wand_reference


def gen_step():
    return make_full_radius_second_torque_wand_reference()
