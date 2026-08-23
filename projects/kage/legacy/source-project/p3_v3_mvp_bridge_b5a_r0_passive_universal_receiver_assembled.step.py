"""CAD entry generator for the assembled B5A passive bridge/receiver MVP."""

import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_geometry as geometry


def gen_step():
    return geometry.assembled_shape()
