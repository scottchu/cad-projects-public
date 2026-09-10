"""Mesh-only generator applying the frozen rigid print-orientation transform."""

from xt60_bend_jig.p20_blue_orange_web_coupon import build_print_coupon


def gen_step():
    return build_print_coupon()

