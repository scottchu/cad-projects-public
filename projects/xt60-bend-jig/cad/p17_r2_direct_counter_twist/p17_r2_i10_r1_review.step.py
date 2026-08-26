"""Frozen interactive review entry for the user-approved P17 I10-R1 checkpoint."""

from copy import copy

from xt60_bend_jig.p17_r2_direct_counter_twist import (
    P17_R2_DEFAULTS,
    build_full_motion_open,
)


def gen_step():
    parameters = copy(P17_R2_DEFAULTS)
    object.__setattr__(parameters, "working_set_translation_y", -16.735)
    object.__setattr__(parameters, "working_set_translation_z", -14.935)
    object.__setattr__(parameters, "fixed_axle_center_y", -29.0)
    object.__setattr__(parameters, "fixed_axle_center_z", 17.0)
    return {
        "shape": build_full_motion_open(parameters),
        "params": "p17_r2_i10_r1_review.params.js",
    }
