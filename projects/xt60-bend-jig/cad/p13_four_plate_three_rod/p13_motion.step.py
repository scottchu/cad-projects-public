"""Review-only OPEN-pose P13 assembly for CAD Viewer motion playback.

The solids are the current production P13 solids at OPEN.  This entry changes
only occurrence labels and grouping so the viewer can apply exact rigid motion
to sixteen independent occurrences.  It is intentionally excluded from the
production P13 artifact/evidence and print-3MF census.
"""

from build123d import Compound, Shape

from xt60_bend_jig.p13_four_plate_three_rod import (
    P13_DEFAULTS,
    ROD_NAMES,
    build_actuator_shaft,
    build_fixed_plate,
    build_left_cam,
    build_left_cap,
    build_right_actuator,
    build_right_cap,
    build_rod,
    build_shaft_keeper,
    build_workpiece,
    provenance_token,
)


def _motion_occurrence(shape: Shape, label: str) -> Shape:
    """Relabel an exact P13 solid for stable name-based viewer targeting."""

    shape.label = label
    return shape


def build_motion_open() -> Compound:
    """Return exactly sixteen separate P13 occurrences in the OPEN pose."""

    p = P13_DEFAULTS
    theta = p.open_angle_deg
    fixed_workpiece = list(build_workpiece(p).children)
    if len(fixed_workpiece) != 1:
        raise ValueError("P13 motion workpiece must remain one fused occurrence")

    children: list[Shape] = [
        _motion_occurrence(build_fixed_plate("left", p), "motion_fixed_left_plate"),
        _motion_occurrence(build_fixed_plate("right", p), "motion_fixed_right_plate"),
        _motion_occurrence(build_shaft_keeper(p), "motion_fixed_shaft_keeper"),
        _motion_occurrence(fixed_workpiece[0], "motion_fixed_workpiece"),
        _motion_occurrence(build_left_cam(theta, p), "motion_rotating_left_cam"),
        _motion_occurrence(
            build_right_actuator(theta, p), "motion_rotating_right_actuator"
        ),
        _motion_occurrence(build_actuator_shaft(theta, p), "motion_rotating_shaft"),
    ]

    for name in ROD_NAMES:
        children.extend(
            [
                _motion_occurrence(build_rod(name, theta, p), f"motion_{name}_rod"),
                _motion_occurrence(
                    build_left_cap(name, theta, p), f"motion_{name}_left_cap"
                ),
                _motion_occurrence(
                    build_right_cap(name, theta, p), f"motion_{name}_right_cap"
                ),
            ]
        )

    if len(children) != 16:
        raise ValueError(f"P13 motion entry requires 16 occurrences, got {len(children)}")
    return Compound(
        children=children,
        label=f"P13_ARTIFACT_motion__{provenance_token(p)}",
    )


def gen_step():
    return {"shape": build_motion_open(), "params": "p13_motion.params.js"}
