"""STEP entry point for the P0 open assembly."""

from xt60_bend_jig.assembly import build_open_assembly


def gen_step():
    return build_open_assembly()
