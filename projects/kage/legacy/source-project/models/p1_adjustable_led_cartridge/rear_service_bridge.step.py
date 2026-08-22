from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from p1_adjustable_led_cartridge_geometry import make_rear_service_bridge


def gen_step():
    return make_rear_service_bridge()
