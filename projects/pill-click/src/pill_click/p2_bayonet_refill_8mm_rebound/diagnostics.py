"""P2 review geometry."""

from build123d import Align, Box, Compound, Part

from .assembly import placed_bayonet_cap, placed_hollow_keyboard_container
from .geometry import make_magnetic_rear_cover, make_ported_outer_housing
from .spec import P2_BAYONET_REFILL_8MM_REBOUND


def make_hopper_cutaway(p=P2_BAYONET_REFILL_8MM_REBOUND):
    state = p.released_state
    parts = [make_ported_outer_housing(p), placed_hollow_keyboard_container(state, p), make_magnetic_rear_cover(p), placed_bayonet_cap(state, True, 0, p)]
    # Remove the viewer-facing (-X) half so the hopper, outlet throat, refill
    # bore, magnet bosses, and cap engagement remain visible in one ISO view.
    cutter = Box(40, 160, 80, align=(Align.MAX, Align.CENTER, Align.CENTER))
    # Re-wrap each result before assembling the diagnostic compound.  Keeping
    # the original parented part here causes STEP export to serialize the
    # untouched source occurrences instead of these sectioned solids.
    cut = []
    for part in parts:
        sectioned = (part - cutter).clean()
        detached = Part(sectioned.wrapped)
        detached.label = sectioned.label
        cut.append(detached)
    return Compound(children=cut, label="p2_hopper_and_refill_cutaway")


__all__ = ["make_hopper_cutaway"]
