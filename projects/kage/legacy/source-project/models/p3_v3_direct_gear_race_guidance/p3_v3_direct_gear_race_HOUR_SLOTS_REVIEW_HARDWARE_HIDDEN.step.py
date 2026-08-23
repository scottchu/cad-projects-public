"""Review-only isolated hour yoke with the clamp hardware hidden.

The production assembly is unchanged.  This view omits only the four hour
station screw/washer/nut stacks and isolates the connected yoke so the four
radial adjustment slots can be inspected directly in CAD Viewer.
"""

from pathlib import Path
import sys

from build123d import Compound

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from p3_v3_direct_gear_race_guidance_geometry import make_unibody_drive_yoke


def gen_step():
    yoke = make_unibody_drive_yoke(0)
    return Compound(
        children=[yoke],
        label="p3_v3_direct_race_REVIEW_ISOLATED_hour_four_radial_slots_clamp_hardware_hidden",
    )
