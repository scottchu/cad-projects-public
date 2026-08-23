"""CAD entry generator for the exact B6-R1 assembly-order exploded view."""

import p3_v3_mvp_electronics_b6_r1_coplanar_broad_underside_geometry as geometry


def gen_step():
    return geometry.exploded_shape()
