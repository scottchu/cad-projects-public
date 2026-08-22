"""STEP entry point for the P0 printable-parts kit."""

from xt60_bend_jig.assembly import build_print_kit


def gen_step():
    return build_print_kit()
