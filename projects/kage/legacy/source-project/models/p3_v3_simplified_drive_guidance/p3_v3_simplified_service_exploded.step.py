"""CAD skill entry point for the simplified P3 V3 service exploded view."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_simplified_drive_guidance_geometry import make_service_exploded


def gen_step():
    return make_service_exploded()
