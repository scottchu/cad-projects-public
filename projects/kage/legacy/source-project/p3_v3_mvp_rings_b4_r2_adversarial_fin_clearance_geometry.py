"""B4-R2 is evidence-only and returns accepted B4-R1 geometry verbatim."""

import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_geometry as accepted


def assembled_shape():
    return accepted.assembled_shape()


def exploded_shape():
    return accepted.exploded_shape()


def printable_occurrences():
    return accepted.printable_occurrences()
