"""Non-powered outward service endpoint with every moving ring removed."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_direct_gear_race_guidance_geometry import make_service_outward_rings_removed


def gen_step():
    return make_service_outward_rings_removed()
