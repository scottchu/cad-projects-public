from xt60_bend_jig.p20_r4_custom_profile_full_cad import build_full_motion_open


def gen_step():
    return {
        "shape": build_full_motion_open(),
        "params": "p20_r4_full_motion.params.js",
    }
