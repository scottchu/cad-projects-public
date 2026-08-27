from xt60_bend_jig.p20_r2_fixed_rod_arc_rail import build_artifact, parameters_from_env


def gen_step():
    return build_artifact("fixed_rail_review", parameters_from_env())
