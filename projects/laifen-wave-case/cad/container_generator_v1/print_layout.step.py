"""Standalone P1 R7 two-object openings-up print-layout target."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from container_generator_v1 import derive, preset
from container_generator_v1.assembly import print_layout


def gen_step():
    return print_layout(derive(preset()))
