"""Review-only complete assembly at the inward powered tuning limit."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_direct_gear_race_guidance_geometry import make_powered_min


def gen_step():
    return make_powered_min()
