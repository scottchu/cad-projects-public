"""Standalone P1 R7 closed assembly target."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from container_generator_v1 import derive, preset
from container_generator_v1.assembly import build_assembly


def gen_step():
    return {
        "shape": build_assembly(derive(preset())),
        "params": "closed.params.js",
    }
