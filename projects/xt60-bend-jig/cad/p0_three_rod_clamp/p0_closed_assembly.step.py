"""STEP entry point for the P0 closed assembly."""

from xt60_bend_jig.assembly import build_closed_assembly


def gen_step():
    return build_closed_assembly()
