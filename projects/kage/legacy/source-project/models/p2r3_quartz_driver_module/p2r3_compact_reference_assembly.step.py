from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p2r3_quartz_driver_module_geometry import make_compact_reference_assembly


def gen_step():
    return make_compact_reference_assembly()
