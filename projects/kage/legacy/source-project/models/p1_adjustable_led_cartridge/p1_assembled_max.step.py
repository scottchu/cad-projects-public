from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p1_adjustable_led_cartridge_geometry import make_assembly
from p1_adjustable_led_cartridge_spec import P1


def gen_step():
    return make_assembly(P1.source_z_max)
