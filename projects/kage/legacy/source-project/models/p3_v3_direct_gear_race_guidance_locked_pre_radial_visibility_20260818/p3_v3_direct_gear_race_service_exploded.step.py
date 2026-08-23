"""CAD skill entry point for the isolated direct gear-race exploded view."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_direct_gear_race_guidance_geometry import make_service_exploded


def gen_step():
    return make_service_exploded()
