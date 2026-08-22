from xt60_bend_jig.p13_four_plate_three_rod import build_artifact, parameters_from_env


def gen_step():
    return build_artifact("fit_coupons", parameters_from_env())
