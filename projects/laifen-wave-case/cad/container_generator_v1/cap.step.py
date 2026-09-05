"""Standalone P1 R7 cap target at the default 0.25 mm radial clearance."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from container_generator_v1 import derive, preset
from container_generator_v1.parts import build_cap


def gen_step():
    return build_cap(derive(preset()))
