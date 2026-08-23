"""CAD entry generator for the assembled B6-R0 electronics backbone MVP."""

import p3_v3_mvp_electronics_b6_r0_universal_backbone_geometry as geometry


def gen_step():
    return geometry.assembled_shape()
