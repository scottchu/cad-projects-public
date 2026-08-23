"""CAD entry generator for the B5A center-service exploded assembly."""

import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_geometry as geometry


def gen_step():
    return geometry.exploded_shape()
