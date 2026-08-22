"""STEP entry point for the P0 rod-bore fit coupon."""

from xt60_bend_jig.geometry import build_fit_coupon


def gen_step():
    return build_fit_coupon()
