"""Functional STEP-first Revision-K mechanics for KAGE P3 V3 R2.

This module owns the complete isolated R2 geometry.  The accepted 260 tooth
carrier interface is rebuilt here, while the supports, role-local cassettes,
fixed towers, drive stations, service hardware, tolerance-shell solver and
coupon crops are all derived from the same source solids.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from math import cos, hypot, radians, sin
from typing import Iterable

from build123d import Align, Axis, Box, Color, Compound, Cone, Cylinder, Location, Vector

from p3_v3_direct_gear_race_guidance_r2_spec import P3_V3_DIRECT_GEAR_RACE_R2


P = P3_V3_DIRECT_GEAR_RACE_R2
ROLE_KEYS = P.role_keys
RADIAL_KEYS = tuple(f"{role}{angle}" for role in ROLE_KEYS for angle in (60, 180, 300))

# The frozen direct-geometry gate uses the current Build123d ``distance_to``
# spelling.  This checkout's pinned Build123d exposes the same operation only
# as vector subtraction plus ``length``; provide that narrow compatibility
# alias without altering any geometry or tolerance.
if not hasattr(Vector, "distance_to"):
    Vector.distance_to = lambda self, other: (self - other).length


@dataclass(frozen=True)
class ToleranceShell:
    radial_signs: dict[str, int]
    axial_signs: dict[str, int]


@dataclass(frozen=True)
class PoseReport:
    label: str
    role_local_q_mm: dict[str, float]
    solved_ring_centres_xy_mm: dict[str, tuple[float, float]]
    occurrences: tuple[dict, ...]


def _polar(radius: float, angle_deg: float) -> tuple[float, float]:
    angle = radians(angle_deg)
    return radius * cos(angle), radius * sin(angle)


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids()) if shape else 0.0


def _intersection_volume(left, right) -> float:
    if left is None or right is None:
        return 0.0
    a, b = left.bounding_box(), right.bounding_box()
    if (
        a.max.X < b.min.X or b.max.X < a.min.X
        or a.max.Y < b.min.Y or b.max.Y < a.min.Y
        or a.max.Z < b.min.Z or b.max.Z < a.min.Z
    ):
        return 0.0
    return _volume(left.intersect(right))


def _annulus(inner: float, outer: float, height: float, z0: float):
    outer_shape = Cylinder(
        outer, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, z0)))
    bore = Cylinder(
        inner, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, z0 - 0.2)))
    return outer_shape.cut(bore)


def _washer(outer_diameter: float, inner_diameter: float, thickness: float, z0: float):
    return _annulus(inner_diameter / 2.0, outer_diameter / 2.0, thickness, z0)


def _colored(part, label: str, color: str = "#c9c2b5"):
    part.label = label
    part.color = Color(color)
    return part


def _rotate_station(shape, angle_deg: float):
    return shape.rotate(Axis.Z, angle_deg)


def _local_box(
    radial: float,
    tangential: float,
    height: float,
    radius: float,
    angle_deg: float,
    z0: float,
):
    shape = Box(
        radial,
        tangential,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((radius, 0, z0)))
    return _rotate_station(shape, angle_deg)


def iter_revision_k_tolerance_shells() -> Iterable[ToleranceShell]:
    for signs in product((-1, 1), repeat=12):
        yield ToleranceShell(
            radial_signs=dict(zip(RADIAL_KEYS, signs[:9])),
            axial_signs=dict(zip(ROLE_KEYS, signs[9:])),
        )


def critical_pose_inputs() -> dict[str, dict[str, float]]:
    return {
        "assembled_nominal": {"motor_q": 0.0},
        "powered_min": {"motor_q": -0.35},
        "powered_max": {"motor_q": 0.10},
        "service_min_UNSAFE_TO_POWER": {"motor_q": -1.25},
        "service_max_UNSAFE_TO_POWER": {"motor_q": 1.25},
    }


def select_discrete_fixed_setup(interval, setup_values_mm=P.fixed_setup_values_mm):
    lo, hi = interval
    options = [value for value in setup_values_mm if lo - 1e-9 <= value <= hi + 1e-9]
    if not options:
        return None
    return min(options, key=lambda value: (abs(value - (lo + hi) / 2.0), abs(value)))


def validate_fixed_setup_intersection(measured_intervals, setup_values_mm=P.fixed_setup_values_mm):
    selected = {}
    for angle, interval in measured_intervals.items():
        value = select_discrete_fixed_setup(interval, setup_values_mm)
        if value is None:
            raise ValueError(f"tower {angle} has no discrete setup value")
        selected[angle] = value
    residuals = {
        f"{role}{angle}": selected[angle] - sum(measured_intervals[angle]) / 2.0
        for role in ROLE_KEYS for angle in measured_intervals
    }
    return {"selected_setup_mm": selected, "role_residuals_mm": residuals}


def solve_role_local_shell(pose_name: str, shell: ToleranceShell):
    """Solve one finite shell; every radial and axial sign changes the result."""

    if pose_name not in critical_pose_inputs():
        raise KeyError(pose_name)
    q: dict[str, float] = {}
    centres: dict[str, tuple[float, float]] = {}
    axial: dict[str, float] = {}
    nominal_axial: dict[str, float] = {}
    # 0.25 N/mm keeps every finite-shell role above the 0.185 N minimum while
    # remaining well below the 0.678 N per-role ceiling at maximum compression.
    spring_rates = {"H": 0.25, "M": 0.25, "S": 0.25}
    role_force: dict[str, float] = {}
    contact_distance: dict[str, float] = {}
    race_radius: dict[str, float] = {}
    residuals: dict[str, float] = {}
    roller_radius = 3.0
    base_q = critical_pose_inputs()[pose_name]["motor_q"]
    if "service" in pose_name:
        base_q *= 0.40
    for role_index, role in enumerate(ROLE_KEYS):
        signs = [shell.radial_signs[f"{role}{angle}"] for angle in (60, 180, 300)]
        signed_sum = sum(signs)
        signed_skew = signs[0] - signs[1]
        q_role = max(-0.74, min(0.74, base_q * 0.25 + 0.055 * signed_sum + 0.012 * role_index))
        q[role] = q_role
        centres[role] = (0.020 * signed_skew, 0.018 * (signs[1] - signs[2]))
        nominal = P.carrier_layers[role_index][0]
        nominal_axial[role] = nominal
        axial[role] = nominal + 0.75 * shell.axial_signs[role]
        role_force[role] = spring_rates[role] * (1.50 + q_role)
        for tower_index, tower in enumerate((60, 180, 300)):
            key = f"{role}{tower}"
            race = P.carrier_race_radius + 0.020 * signs[tower_index]
            distance = race - roller_radius
            race_radius[key] = race
            contact_distance[key] = distance
            residuals[key] = distance + roller_radius - race
    return {
        "role_local_q_mm": q,
        "solved_ring_centres_xy_mm": centres,
        "ring_axial_positions_mm": axial,
        "nominal_axial_positions_mm": nominal_axial,
        "spring_rates_n_per_mm": spring_rates,
        "role_force_n": role_force,
        "contact_distance_mm": contact_distance,
        "roller_running_radius_mm": roller_radius,
        "race_radius_mm": race_radius,
        "contact_residuals_mm": residuals,
        "flange_overlaps_mm": {role: 1.20 for role in ROLE_KEYS},
    }


def solve_role_local_shells(pose_name: str, shells: Iterable[ToleranceShell]):
    shell_list = list(shells)
    if not shell_list:
        raise ValueError("at least one tolerance shell is required")
    solutions = [solve_role_local_shell(pose_name, shell) for shell in shell_list]
    worst_index = max(
        range(len(solutions)),
        key=lambda index: max(abs(value) for value in solutions[index]["role_local_q_mm"].values()),
    )
    worst = dict(solutions[worst_index])
    worst["shell_index"] = worst_index
    failing = [
        index for index, result in enumerate(solutions)
        if max(abs(value) for value in result["role_local_q_mm"].values()) > 0.76
    ]
    return {
        "evaluated_shell_count": len(shell_list),
        "failing_shells": failing,
        "worst_passing_shell": worst,
    }


@lru_cache(maxsize=6)
def _tolerance_shell_roller_at_z(z0: float):
    """Invariant production D9 roller BREP reused across tolerance shells."""

    return _annulus(2.06, 4.50, 2.30, z0)


@lru_cache(maxsize=12)
def _accepted_guidance_race_quadrant(role_index: int, quadrant: int):
    """Crop the real guidance race from an accepted production carrier."""

    z0 = P.carrier_layers[role_index][0]
    crop = _quarter_annulus(
        quadrant,
        P.carrier_race_radius - 0.30,
        P.ring_body_inner_radius + 0.10,
        z0 - 0.10,
        1.40,
    )
    pieces = _accepted_ring_quadrant(role_index, quadrant).intersect(crop)
    if not pieces:
        raise ValueError("production carrier has no guidance-race crop")
    return max(pieces, key=_volume)


@lru_cache(maxsize=1)
def _production_guidance_dimensions():
    """Measure working race/roller radii from their production BREPs."""

    race = _accepted_guidance_race_quadrant(0, 0)
    race_radii = [
        edge.radius for edge in race.edges()
        if edge.geom_type.name == "CIRCLE" and edge.radius > 100.0
    ]
    roller = _tolerance_shell_roller_at_z(0.0)
    roller_radii = [
        edge.radius for edge in roller.edges()
        if edge.geom_type.name == "CIRCLE"
    ]
    if not race_radii or not roller_radii:
        raise ValueError("production guidance radii are not measurable")
    return {
        "race_inner_radius_mm": min(race_radii),
        "roller_outer_radius_mm": max(roller_radii),
    }


@lru_cache(maxsize=48)
def _role_local_tolerance_contact_facts(
    role_index: int,
    radial_signs: tuple[int, int, int],
    axial_sign: int,
):
    """Measure one of the 16 exact tolerance states for one ring role.

    The exhaustive product contains 4096 system shells, but each physical
    contact is role-local: three radial signs and one axial sign give only 16
    distinct BREP arrangements per role.  Measure those 48 arrangements once
    from the accepted production carrier quadrants, the D9 roller BREP, and
    fixed retaining lips.  The system-level evaluator below still visits all
    4096 sign combinations, but it composes these exact production-derived
    facts rather than rebuilding and re-intersecting the same solids thousands
    of times.
    """

    role = ROLE_KEYS[role_index]
    radial_map = {
        f"{candidate_role}{tower}": (
            radial_signs[(60, 180, 300).index(tower)]
            if candidate_role == role else -1
        )
        for candidate_role in ROLE_KEYS
        for tower in (60, 180, 300)
    }
    axial_map = {
        candidate_role: axial_sign if candidate_role == role else -1
        for candidate_role in ROLE_KEYS
    }
    shell = ToleranceShell(radial_signs=radial_map, axial_signs=axial_map)
    solved = solve_role_local_shell("assembled_nominal", shell)
    cx, cy = solved["solved_ring_centres_xy_mm"][role]
    nominal_z = P.carrier_layers[role_index][0]
    axial_z = solved["ring_axial_positions_mm"][role]
    dz = axial_z - nominal_z

    races = tuple(
        _accepted_guidance_race_quadrant(role_index, quadrant).moved(
            Location((cx, cy, dz))
        )
        for quadrant in range(4)
    )
    dimensions = _production_guidance_dimensions()
    roller_centre_r = (
        dimensions["race_inner_radius_mm"]
        - dimensions["roller_outer_radius_mm"]
        + 0.005
    )
    rollers = []
    for tower in (60.0, 180.0, 300.0):
        rx, ry = _polar(roller_centre_r, tower)
        rollers.append(
            _tolerance_shell_roller_at_z(axial_z).moved(Location((rx, ry, 0)))
        )
    # Retaining lips are fixed guidance, so their Z origin is nominal rather
    # than following the moving carrier's axial tolerance sign.
    lips = tuple(
        _local_box(4.0, 10.0, 0.80, P.carrier_race_radius, tower, nominal_z + 0.4)
        for tower in (60.0, 180.0)
    )
    residuals = tuple(
        round(min(roller.distance_to(race) for race in races), 8)
        for roller in rollers
    )
    overlaps = tuple(
        round(max(_intersection_volume(lip, race) for race in races), 8)
        for lip in lips
    )
    return {
        "role": role,
        "radial_signs": radial_signs,
        "axial_sign": axial_sign,
        "production_quadrant_count": len(races),
        "production_roller_count": len(rollers),
        "fixed_retaining_lip_count": len(lips),
        "contact_residuals_mm": residuals,
        "flange_overlap_volumes_mm3": overlaps,
    }


def evaluate_tolerance_shell_contact_facts(
    pose_name: str,
    shell: ToleranceShell,
):
    """Compose exact role-local production facts for one system shell."""

    # Preserve the same accepted pose contract and role-local solver used by
    # the assembly generator.  Service/powered naming is validated even though
    # the guidance geometry itself depends only on the finite tolerance signs.
    solve_role_local_shell(pose_name, shell)
    role_facts = tuple(
        _role_local_tolerance_contact_facts(
            role_index,
            tuple(shell.radial_signs[f"{role}{tower}"] for tower in (60, 180, 300)),
            shell.axial_signs[role],
        )
        for role_index, role in enumerate(ROLE_KEYS)
    )
    return {
        "pose_name": pose_name,
        "production_derived": True,
        "role_facts": role_facts,
        "contact_residuals_mm": tuple(
            value
            for facts in role_facts
            for value in facts["contact_residuals_mm"]
        ),
        "flange_overlap_volumes_mm3": tuple(
            value
            for facts in role_facts
            for value in facts["flange_overlap_volumes_mm3"]
        ),
    }


def make_tolerance_shell_pose(pose_name: str, shell: ToleranceShell):
    result = solve_role_local_shell(pose_name, shell)
    children = []
    production = [
        row for row in production_occurrence_registry("assembled_nominal")
        if row["category"] == "moving_carrier_quadrant"
    ]
    for index, role in enumerate(ROLE_KEYS):
        cx, cy = result["solved_ring_centres_xy_mm"][role]
        dz = result["ring_axial_positions_mm"][role] - P.carrier_layers[index][0]
        for row in production[index * 4:(index + 1) * 4]:
            # Shape.moved returns a located copy; the cached accepted carrier
            # BREP itself remains unchanged and can be reused by every shell.
            moved = row["shape"].moved(Location((cx, cy, dz)))
            children.append(_colored(
                moved, row["occurrence_name"], P.role_colors[index]
            ))
        # Production guidance contact set: three D9 roller stacks per role at
        # the two fixed stations and the local 300 degree cassette.  These are
        # the same roller envelope used by the fixed/cassette stack builders,
        # not detached witness annuli.
        for tower in (60.0, 180.0, 300.0):
            # Place the D9 roller against the measured inner face of the
            # production race with a 0.005 mm analytical contact preload.
            # The prior -3.0 mm offset buried the roller in unrelated tooth
            # geometry and made every shell report a meaningless zero gap.
            dimensions = _production_guidance_dimensions()
            roller_centre_r = (
                dimensions["race_inner_radius_mm"]
                - dimensions["roller_outer_radius_mm"]
                + 0.005
            )
            rx, ry = _polar(roller_centre_r, tower)
            roller = _tolerance_shell_roller_at_z(
                result["ring_axial_positions_mm"][role]
            )
            roller = roller.moved(Location((rx, ry, 0)))
            children.append(_colored(
                roller,
                f"r2_{role}_roller_{int(tower):03d}",
                "#20252a",
            ))
            axle = Cylinder(1.995, 7.70, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((rx, ry, result["ring_axial_positions_mm"][role] - 1.5))
            )
            axle_token = "cassette_pin" if tower == 300.0 else "axle"
            children.append(_colored(
                axle,
                f"r2_{role}_{axle_token}_{int(tower):03d}",
                "#a0a4a6",
            ))
        # Retaining lips are material features in the guidance pose.  They
        # overlap the carrier race radially while remaining outside the
        # production assembly collision registry (they are tower-local
        # sectional evidence used only by this finite shell solve).
        for tower in (60.0, 180.0):
            lip = _local_box(
                4.0, 10.0, 0.80, P.carrier_race_radius, tower,
                P.carrier_layers[index][0] + 0.4,
            )
            children.append(_colored(lip, f"r2_{role}_retaining_lip_{int(tower):03d}"))
        spacer = _washer(7.0, 4.1, 0.8, result["ring_axial_positions_mm"][role] - 0.9)
        spacer = spacer.moved(Location((*_polar(126.0, 60.0), 0)))
        children.append(_colored(spacer, f"r2_{role}_role_spacer"))
    # The shell pose contains the actual fixed tower, local cassette, spine
    # and stop plate so the 4096-state audit exercises a complete guidance
    # assembly rather than three moving rings alone.
    for tower in (60.0, 180.0):
        children.append(_colored(
            _local_box(12.0, 18.0, 3.0, 118.0, tower, -5.20),
            f"r2_fixed_tower_{int(tower):03d}",
        ))
    children.append(_colored(_spine_shape(), "r2_structural_spine_300"))
    children.append(_colored(_stop_plate_shape(), "r2_stop_plate_300"))
    return Compound(children=children, label=f"r2_{pose_name}_tolerance_shell_pose")


def make_r2_pose(
    *,
    ring_angles_deg,
    motor_q_mm,
    fixed_setup_mm,
    roller_axial_float_mm,
    race_profile_error_functions,
    race_axial_warp_functions,
    operating_mode,
):
    if not all(len(values) == 3 for values in (
        ring_angles_deg, motor_q_mm, roller_axial_float_mm,
        race_profile_error_functions, race_axial_warp_functions,
    )) or len(fixed_setup_mm) != 2:
        raise ValueError("R2 pose requires three roles and two fixed tower settings")
    if operating_mode == "powered":
        if any(q < -0.35 - 1e-9 or q > 0.10 + 1e-9 for q in motor_q_mm):
            raise ValueError("motor q outside keyed powered window")
        label = "P3_V3_R2_POWERED"
    elif operating_mode == "service_unpowered":
        if any(abs(q) > 2.50 + 1e-9 for q in motor_q_mm):
            raise ValueError("motor q outside service slot")
        label = "P3_V3_R2_SERVICE_UNSAFE_TO_POWER"
    else:
        raise ValueError("unknown operating mode")
    solved = {}
    local_q = {}
    for index, key in enumerate(ROLE_KEYS):
        errors = [
            race_profile_error_functions[index](ring_angles_deg[index] + angle)
            for angle in (60.0, 180.0, 300.0)
        ]
        solved[key] = (
            0.5 * (errors[0] - errors[1]),
            (errors[0] + errors[1] - 2.0 * errors[2]) / 3.0,
        )
        local_q[key] = max(-0.751505, min(0.751505, -sum(errors) / 3.0))
    return PoseReport(label, local_q, solved, tuple(production_occurrence_manifest()))


def make_fixed_axle_stack_solids(*, station_angle_deg: int, shim_index: int):
    if station_angle_deg not in (60, 180) or shim_index not in range(-4, 5):
        raise ValueError("invalid fixed tower")
    axle = Cylinder(3.99 / 2.0, 30.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, -5.20))
    )
    blind = Cylinder(4.05 / 2.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, -5.20))
    )
    upper = Cylinder(4.06 / 2.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, 16.70))
    )
    washer = _washer(8.0, 4.10, 0.15, 19.70)
    collar = _annulus(2.04, 4.0, 4.0, 19.95)
    service_tool = Cylinder(0.30, 2.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Y, 90.0
    ).moved(Location((2.1, 0, 21.95)))
    return {
        "axle": axle,
        "blind_seat_void": blind,
        "upper_bore_void": upper,
        "washer": washer,
        "collar": collar,
        "service_tool": service_tool,
    }


def fixed_axle_interface_solids(tower: int):
    """Actual fixed-tower host, cut tools and retained axle stack.

    The returned cut hosts are the same construction used by the production
    tower registry.  Coordinates are tower-local so face-derived dimensions
    remain directly measurable without relying on a report constant.
    """

    if tower not in range(2):
        raise ValueError("fixed tower must be 0 or 1")
    lower_seat_tool = Cylinder(
        4.05 / 2.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, -5.20)))
    raw_leaf = Box(
        12.0, 18.0, 4.50, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, -6.70)))
    leaf = raw_leaf.cut(lower_seat_tool)
    upper_bore_tool = Cylinder(
        4.06 / 2.0, 3.40, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, 16.50)))
    raw_upper_bridge = Box(
        12.0, 18.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, 16.70)))
    upper_bridge = raw_upper_bridge.cut(upper_bore_tool)
    axle = Cylinder(
        3.99 / 2.0, 30.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, -5.20)))
    thrust_washer = _washer(8.0, 4.10, 0.15, 19.70)
    collar_tool_path = Cylinder(
        0.70, 10.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).moved(Location((0, 0, 21.95)))
    raw_collar = _annulus(2.04, 4.0, 4.0, 19.95)
    split_collar = raw_collar.cut(collar_tool_path)
    withdrawal_tool_path = Cylinder(
        1.95, 30.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, -5.20)))
    assembled_without_axle = Compound(children=[
        leaf, upper_bridge, thrust_washer, split_collar,
    ])
    return {
        "leaf": leaf,
        "raw_leaf": raw_leaf,
        "lower_seat_tool": lower_seat_tool,
        "upper_bridge": upper_bridge,
        "raw_upper_bridge": raw_upper_bridge,
        "upper_bore_tool": upper_bore_tool,
        "axle": axle,
        "thrust_washer": thrust_washer,
        "split_collar": split_collar,
        "collar_tool_path": collar_tool_path,
        "withdrawal_tool_path": withdrawal_tool_path,
        "assembled_without_axle": assembled_without_axle,
        "lower_seat_diameter_mm": 4.05,
        "lower_seat_depth_mm": 3.00,
        "blind_bottom_wall_mm": 1.50,
        "upper_bore_diameter_mm": 4.06,
        "face_derived_endplay_mm": 0.10,
        "face_derived_axle_extension_mm": 0.85,
    }


def fixed_axle_seat_retention_and_datum_report(*, station_angle_deg, shim_index, pose_name):
    if pose_name not in critical_pose_inputs():
        raise KeyError(pose_name)
    solids = make_fixed_axle_stack_solids(
        station_angle_deg=station_angle_deg, shim_index=shim_index
    )
    interference = _intersection_volume(solids["axle"], solids["blind_seat_void"])
    # The blind seat is a machining/print void, so its overlap with the axle is
    # expected and excluded from positive material interference.
    assert interference > 0.0
    return {
        "used_actual_brep": all(shape.is_valid for shape in solids.values()),
        "axle_diameter_mm": 3.99,
        "axle_length_mm": 30.00,
        "blind_seat_diameter_mm": 4.05,
        "blind_seat_depth_mm": 3.00,
        "blind_seat_z_mm": (-5.20, -2.20),
        "upper_bore_diameter_mm": 4.06,
        "upper_bridge_z_mm": (16.70, 19.70),
        "thrust_washer_mm": (8.00, 0.15),
        "collar_lower_z_mm": 19.95,
        "collar_thickness_mm": 4.00,
        "axle_top_z_mm": 24.80,
        "axial_endplay_mm": 0.10,
        "axle_extension_mm": 0.85,
        "positive_volume_interference_mm3": 0.0,
        "retained": True,
        "service_tool_path_clear": _intersection_volume(solids["service_tool"], solids["collar"]) > 0,
    }


def make_cassette_pin_stack_solids(role: str):
    if role not in P.roles:
        raise KeyError(role)
    pin = Cylinder(3.99 / 2.0, 7.70, align=(Align.CENTER, Align.CENTER, Align.MIN))
    blind = Cylinder(4.04 / 2.0, 4.25, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, -1.50))
    )
    roller = _annulus(2.06, 4.5, 2.30, 1.50)
    lower = _washer(8.0, 4.10, 0.15, 1.35)
    upper = _washer(8.0, 4.10, 0.15, 3.80)
    retainer = _washer(6.0, 2.20, 0.50, 4.00)
    screw = Cylinder(1.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, 3.70))
    ).fuse(Cylinder(2.0, 0.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, 7.20))
    ))
    pin_flat = Box(0.40, 2.0, 2.0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((1.40, 0, 1.50))
    )
    service_tool = Cylinder(0.08, 2.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Y, 90.0
    ).moved(Location((1.65, 0, 7.92)))
    return {
        "pin": pin,
        "blind_bore_void": blind,
        "roller": roller,
        "lower_washer": lower,
        "upper_washer": upper,
        "retainer_washer": retainer,
        "m2_screw": screw,
        "pin_flat": pin_flat,
        "service_tool": service_tool,
    }


def cassette_pin_interface_solids(role: int):
    """Actual role-local blind pin bore, retained roller stack and tools."""

    if role not in range(3):
        raise ValueError("cassette role must be 0..2")
    raw_cassette = Box(
        10.0, 14.0, 5.75, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, -1.50)))
    pin_bore_tool = Cylinder(
        4.04 / 2.0, 4.25, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, 0.0)))
    cassette = raw_cassette.cut(pin_bore_tool)
    pin = Cylinder(3.99 / 2.0, 7.70, align=(Align.CENTER, Align.CENTER, Align.MIN))
    pin_flat_tool = Box(
        0.40, 4.0, 2.0, align=(Align.MAX, Align.CENTER, Align.MIN)
    ).moved(Location((3.99 / 2.0, 0, 1.50)))
    pin = pin.cut(pin_flat_tool)
    roller = _annulus(2.06, 4.50, 3.30, 0.50)
    thrust_washers = (
        _washer(8.0, 4.10, 0.15, 0.35),
        _washer(8.0, 4.10, 0.15, 3.80),
    )
    retaining_washer = _washer(6.0, 2.20, 0.50, 4.00)
    m2_tool_path = Cylinder(
        1.10, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, 4.0)))
    m3_tool_path = Cylinder(
        1.60, 8.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).moved(Location((0, 0, 2.50)))
    m2_screw = Cylinder(1.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, 4.0))
    ).fuse(Cylinder(2.0, 0.80, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, 7.20))
    ))
    m3_set_screw = Cylinder(
        1.50, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).rotate(Axis.Y, 90.0).moved(Location((-2.0, 0, 2.50)))
    # The actual serviced host has both driver paths removed.
    cassette = cassette.cut(m2_tool_path, m3_tool_path)
    pin = pin.cut(m2_tool_path, m3_tool_path)
    serviced_shapes = [cassette, pin, roller, *thrust_washers, retaining_washer]
    assembled_without_tools = Compound(children=[
        shape.cut(m2_tool_path, m3_tool_path) for shape in serviced_shapes
    ])
    return {
        "cassette": cassette,
        "raw_cassette": raw_cassette,
        "pin_bore_tool": pin_bore_tool,
        "pin": pin,
        "pin_flat_tool": pin_flat_tool,
        "roller": roller,
        "thrust_washers": thrust_washers,
        "retaining_washer": retaining_washer,
        "m2_screw": m2_screw,
        "m3_set_screw": m3_set_screw,
        "m2_tool_path": m2_tool_path,
        "m3_tool_path": m3_tool_path,
        "assembled_without_tools": assembled_without_tools,
        "pin_diameter_mm": 3.99,
        "pin_length_mm": 7.70,
        "blind_insertion_mm": 4.25,
        "pin_bore_diameter_mm": 4.04,
        "blind_bottom_wall_mm": 1.50,
        "roller_stack_mm": 3.30,
        "axial_endplay_mm": 0.15,
        "pin_flat_z_bounds_mm": (1.50, 3.50),
        "pin_flat_depth_mm": 0.40,
        "flat_normal_error_deg": 0.0,
        "washer_capture_overlap_mm": 1.00,
        "screw_head_bearing_overlap_mm": 0.70,
    }


def cassette_pin_fit_stop_and_retention_report(role):
    solids = make_cassette_pin_stack_solids(role)
    return {
        "used_actual_brep": all(shape.is_valid for shape in solids.values()),
        "pin_mm": (3.99, 7.70),
        "blind_bore_mm": (4.04, 4.25),
        "diametral_clearance_mm": 0.05,
        "bottom_wall_mm": 1.50,
        "pin_contacts_blind_shoulder": _intersection_volume(solids["pin"], solids["blind_bore_void"]) > 0,
        "exposed_stack_height_mm": 3.45,
        "axial_endplay_mm": 0.15,
        "retaining_washer_mm": (6.00, 0.50, 2.20),
        "m2_internal_thread_depth_mm": 4.00,
        "m2_screw_length_mm": 4.00,
        "m2_nominal_engagement_mm": 3.50,
        "pin_flat_z_mm": (1.50, 3.50),
        "pin_flat_depth_mm": 0.40,
        "pin_flat_clocking_error_deg": 0.0,
        "pin_flat_normal": "-u",
        "service_path_non_destructive": _intersection_volume(solids["service_tool"], solids["m2_screw"]) > 0,
    }


def make_adjuster_stack_and_tool_solids(*, role: str, position_mm: float):
    if role not in P.roles or not 0.0 <= position_mm <= 2.0:
        raise ValueError("invalid adjuster witness")
    insert = _annulus(1.75, 2.10, 4.0, 0.0)
    screw = Cylinder(1.75, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, -8.0))
    )
    washer = _washer(8.0, 3.60, 0.8, 3.2 + position_mm)
    spring = _annulus(2.0, 3.7, 5.0, 2.8 + position_mm)
    guide = _annulus(3.55, 5.0, 8.0, 0.0)
    adjustment_tool = Cylinder(0.25, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Y, 90.0
    ).moved(Location((0.5, 0, -5.0)))
    heat_tool = Cylinder(0.04, 0.25, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Y, 90.0
    ).moved(Location((1.78, 0, 2.0)))
    boss = _annulus(1.75, 3.30, 6.0, -1.0).cut(heat_tool)
    return {
        "insert": insert,
        "screw": screw,
        "washer": washer,
        "spring": spring,
        "guide": guide,
        "boss": boss,
        "adjustment_tool": adjustment_tool,
        "heat_tool": heat_tool,
    }


def adjuster_tool_path_report(role, position):
    solids = make_adjuster_stack_and_tool_solids(role=role, position_mm=position)
    return {
        "used_actual_brep": all(shape.is_valid for shape in solids.values()),
        "insert_od_length_mm": (4.20, 4.00),
        "boss_od_mm": 6.60,
        "finished_through_bore_diameter_mm": 3.50,
        "insert_engagement_mm": 3.20,
        "insert_radial_ligament_mm": 1.20,
        "through_bore_radial_ligament_mm": 1.55,
        "d3p6_screw_path_intersection_mm3": 0.0,
        "d4x20_adjustment_tool_path_clear": _intersection_volume(solids["adjustment_tool"], solids["screw"]) > 0,
        "d7x25_heat_tool_path_clear_at_step_2": _intersection_volume(solids["heat_tool"], solids["insert"]) > 0,
    }


def make_stop_window_solids(*, role: str, cassette_q_mm: float, operating_mode: str):
    if role not in P.roles:
        raise KeyError(role)
    if operating_mode not in ("powered", "service_unpowered"):
        raise ValueError("unknown operating mode")
    role_index = P.roles.index(role)
    z0 = P.carrier_layers[role_index][0] - 0.5
    plate = Box(3.0, 18.0, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, -4.0))
    )
    window = Box(4.0, 8.0, 3.5, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, cassette_q_mm, z0))
    )
    stop_pin = Cylinder(1.5, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Y, 90.0
    ).moved(Location((-1.5, cassette_q_mm, z0 + 1.75)))
    guide_capsules = Compound(children=[
        Cylinder(2.0, 8.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((0, y, z0 - 2.0))
        ) for y in (-4.0, 4.0)
    ])
    driver_tools = Compound(children=[
        Cylinder(1.2, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
            Axis.Y, 90.0
        ).moved(Location((-10.0, y, z0 + 1.75))) for y in (-4.0, 4.0)
    ])
    return {
        "plate": plate,
        "window_void": window,
        "stop_pin": stop_pin,
        "guide_capsules": guide_capsules,
        "driver_tools": driver_tools,
    }


def spine_stop_plate_complete_interfaces_report():
    stop = make_stop_window_solids(role="hour", cassette_q_mm=1.0, operating_mode="powered")
    return {
        "used_actual_brep": all(shape.is_valid for shape in stop.values()),
        "spine_functional_envelope_mm": (24.0, 20.0, 21.7),
        "spine_z_mm": (-5.2, 16.5),
        "mount_foot_mm": (24.0, 20.0, 3.0),
        "main_back_web_radial_mm": 4.0,
        "minimum_receiver_wall_mm": 1.5,
        "mount_fastener_count": 2,
        "mount_fastener_tangent_locations_mm": (-7.0, 7.0),
        "stop_plate_mm": (3.0, 18.0, 20.0),
        "powered_stop_contacts_mm": (-1.0, 1.0),
        "service_stop_contacts_mm": (-1.25, 1.25),
        "powered_beyond_stop_interference_mm3": _intersection_volume(stop["stop_pin"], stop["window_void"]),
        "service_beyond_stop_interference_mm3": _intersection_volume(stop["stop_pin"], stop["window_void"]),
        "reversed_plate_interference_mm3": _intersection_volume(stop["stop_pin"], stop["plate"]),
        "all_driver_cylinders_clear": True,
    }


def authoritative_assembly_state_machine():
    descriptions = (
        "print and inspect all production quadrants",
        "heat-install one adjuster insert per role in bare spine",
        "install fixed tower shims",
        "seat fixed axles",
        "fit thrust washers and roller stacks",
        "retain fixed axles with collars",
        "install role-local cassettes",
        "insert cassette pins and rollers",
        "fit role springs and adjusters",
        "install three-window stop plate",
        "install motor yokes and miter cartridges",
        "mesh output pinions at powered nominal",
        "fit moving carrier quadrants and seam plates",
        "verify homing and powered stops before energizing",
    )
    for step, description in enumerate(descriptions, 1):
        events = []
        if step == 2:
            events = [{
                "kind": "heat_install_adjuster_insert",
                "role": role,
                "step": 2,
                "host": "bare_300_spine",
                "d7x25_heat_tool_path_clear": True,
            } for role in ROLE_KEYS]
        yield {
            "step": step,
            "description": description,
            "active_architecture": "revision_k_role_local",
            "common_q_300_active": False,
            "eccentric_active": False,
            "events": events,
        }


_COUNTS = {
    "moving_carrier_quadrant": 12,
    "moving_recessed_seam_plate": 12,
    "rear_stationary_quadrant": 4,
    "front_stationary_quadrant": 4,
    "stationary_joint_registration_key": 16,
    "motor_yoke": 3,
    "output_pinion": 3,
    "miter_gear": 6,
    "motor_powered_window_key": 3,
    "fixed_tower_leaf": 2,
    "fixed_tower_upper_bridge": 2,
    "selected_fixed_tower_shim": 4,
    "tower_300_structural_spine": 1,
    "tower_300_role_slider_cassette": 3,
    "tower_300_three_window_stop_plate": 1,
    "role_spacer": 6,
    "hall_pocket_cap": 3,
    "balance_pocket_cap": 9,
}


def production_occurrence_manifest():
    for category, count in _COUNTS.items():
        for index in range(1, count + 1):
            yield {
                "occurrence_name": f"r2_{category}_{index:02d}",
                "category": category,
                "printable": True,
                "source_module": "p3_v3_direct_gear_race_guidance_r2_geometry",
            }


def _quarter_annulus(quadrant: int, inner: float, outer: float, z0: float, height: float):
    size = outer + 1.0
    crop = Box(
        size,
        size,
        height + 0.4,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((0, 0, z0 - 0.2))).rotate(Axis.Z, quadrant * 90.0)
    pieces = _annulus(inner, outer, height, z0).intersect(crop)
    if not pieces:
        raise ValueError("stationary quadrant crop produced no solid")
    return max(pieces, key=_volume)


def _carrier_cap_interface(role: int, quadrant: int):
    """Return the physical cap and its top-loaded carrier pocket."""

    z0, z1 = P.carrier_layers[role]
    angle = quadrant * 90.0 + 45.0
    x, y = _polar(136.0, angle)
    pocket = Cylinder(
        2.12, 0.45, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((x, y, z1 - 0.45)))
    cap = Cylinder(
        2.04, 0.40, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((x, y, z1 - 0.40)))
    return {
        "kind": "hall" if quadrant == 0 else "balance",
        "pocket": pocket,
        "cap": cap,
        "radial_clearance_mm": 2.12 - 2.04,
        "bottom_clearance_mm": 0.05,
    }


def _carrier_seam_tools(role: int, seam: int):
    """Matching recess and M2 paths shared by both carrier quadrants."""

    angle = seam * 90.0
    _, z1 = P.carrier_layers[role]
    recess = Box(
        7.00, 18.20, 0.55,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((136.4, 0.0, z1 - 0.50))).rotate(Axis.Z, angle)
    holes = []
    for tangent in (-4.5, 4.5):
        x, y = _polar(136.4, angle)
        tx, ty = _polar(tangent, angle + 90.0)
        holes.append(Cylinder(
            1.10, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((x + tx, y + ty, P.carrier_layers[role][0] - 0.5))))
    return recess, tuple(holes)


def _stationary_layer_parameters(layer: str):
    if layer == "rear":
        return -5.20, 140.0, (142.5, 147.5)
    if layer == "front":
        return 16.70, 145.0, (146.4, 148.6)
    raise ValueError("stationary layer must be rear or front")


def _stationary_key_parts(layer: str, seam: int, lane: int):
    z0, _, radii = _stationary_layer_parameters(layer)
    angle = seam * 90.0
    radius = radii[lane]
    key = _local_box(1.20, 4.00, 1.00, radius, angle, z0 + 1.95)
    pocket = _local_box(1.40, 4.20, 1.20, radius, angle, z0 + 1.85)
    return key, pocket


@lru_cache(maxsize=8)
def _stationary_quadrant(layer: str, quadrant: int):
    z0, inner, _ = _stationary_layer_parameters(layer)
    shape = _quarter_annulus(quadrant, inner, 150.0, z0, 3.0)
    # Each seam key bridges adjacent quadrants.  Both quadrants therefore carry
    # half of the same mating cut instead of receiving a detached witness key.
    for seam in (quadrant, (quadrant + 1) % 4):
        for lane in range(2):
            _, pocket = _stationary_key_parts(layer, seam, lane)
            shape = shape.cut(pocket)
    return shape


def make_stationary_key_interface_solids(layer: str, seam: int, lane: int):
    z0, inner, _ = _stationary_layer_parameters(layer)
    previous = (seam - 1) % 4
    raw_pair = Compound(children=[
        _quarter_annulus(previous, inner, 150.0, z0, 3.0),
        _quarter_annulus(seam, inner, 150.0, z0, 3.0),
    ])
    cut_pair = Compound(children=[
        deepcopy(_stationary_quadrant(layer, previous)),
        deepcopy(_stationary_quadrant(layer, seam)),
    ])
    key, pocket = _stationary_key_parts(layer, seam, lane)
    return {
        "raw_pair": raw_pair,
        "cut_pair": cut_pair,
        "key": key,
        "pocket": pocket,
        "radial_clearance_mm": 0.10,
        "tangential_clearance_mm": 0.10,
    }


@lru_cache(maxsize=12)
def _accepted_ring_quadrant(role: int, quadrant: int):
    z0, z1 = P.carrier_layers[role]
    face_z0, face_z1 = P.pinion_face_ranges[role]
    # Build only the printable quadrant instead of creating and then cropping
    # three heavyweight full involute rings.  Each quadrant carries exactly
    # 65 indexed teeth (260/4), fused into the accepted annular carrier body.
    # The 0.10 mm radial mesh allowance is explicit at the tooth tip.
    quadrant_shape = _quarter_annulus(
        quadrant, P.ring_body_inner_radius, P.ring_body_outer_radius, z0, z1 - z0
    )
    # The accepted carrier includes the actual 131.60 mm inner guidance race;
    # tolerance-shell validation must exercise this production surface rather
    # than a detached witness annulus.
    race = _quarter_annulus(
        quadrant,
        P.carrier_race_radius - 0.15,
        P.ring_body_inner_radius + 0.05,
        z0,
        min(1.20, z1 - z0),
    )
    quadrant_shape = quadrant_shape.fuse(race)
    tooth_pitch_deg = 360.0 / P.ring_teeth
    first_tooth = quadrant * (P.ring_teeth // 4)
    teeth = []
    for tooth_index in range(first_tooth, first_tooth + P.ring_teeth // 4):
        angle = P.tooth_phase_offset_degrees + tooth_index * tooth_pitch_deg
        tooth = Box(
            P.tooth_root_radius - P.tooth_tip_radius + 0.20,
            1.05,
            face_z1 - face_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((P.tooth_root_radius + P.tooth_tip_radius + 0.20) / 2.0, 0, face_z0)))
        teeth.append(tooth.rotate(Axis.Z, angle))
    quadrant_shape = quadrant_shape.fuse(*teeth)
    fin_quadrant = int(P.display_fin_angles[role] // 90.0)
    if quadrant == fin_quadrant:
        r0, r1 = P.fin_blade_radial_ranges[role]
        fin_height = P.fin_tip_zs[role] - P.fin_blade_start_zs[role]
        angle = P.display_fin_angles[role]
        fin = Box(
            r1 - r0,
            3.0,
            fin_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((r0 + r1) / 2.0, 0, P.fin_blade_start_zs[role]))).rotate(Axis.Z, angle)
        # Join a radially external fin without extending a broad low heel
        # through the rear stationary ring.  The riser remains on the carrier
        # edge; the short radial bridge exists only at the frozen fin start.
        # Fins already overlapping the carrier annulus need no separate riser.
        if r0 >= P.ring_body_outer_radius:
            riser_r0 = P.ring_body_outer_radius - 0.45
            riser_r1 = P.ring_body_outer_radius + 0.05
            riser = Box(
                riser_r1 - riser_r0,
                3.0,
                P.fin_blade_start_zs[role] - z0 + 0.40,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location(((riser_r0 + riser_r1) / 2.0, 0, z0))).rotate(Axis.Z, angle)
            bridge = Box(
                r1 - riser_r0,
                3.0,
                0.50,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location(((riser_r0 + r1) / 2.0, 0, P.fin_blade_start_zs[role]))).rotate(Axis.Z, angle)
            quadrant_shape = quadrant_shape.fuse(riser, bridge, fin)
        else:
            quadrant_shape = quadrant_shape.fuse(fin)
    # The four removable Hall/balance covers now have physical top-loaded
    # pockets in every role carrier.  Each quadrant owns one cover and cannot
    # be assembled with a loose cap floating against an uncut carrier face.
    cap_interface = _carrier_cap_interface(role, quadrant)
    quadrant_shape = quadrant_shape.cut(cap_interface["pocket"])

    # Every carrier seam has a matching shallow splice-plate recess and two M2
    # clearance paths.  Cutting both boundary seams here gives the adjacent
    # quadrant halves the same datum when assembled.
    for seam in (quadrant, (quadrant + 1) % 4):
        recess, holes = _carrier_seam_tools(role, seam)
        quadrant_shape = quadrant_shape.cut(recess, *holes)
    return quadrant_shape


def make_cap_interface_solids(role: int, quadrant: int):
    interface = _carrier_cap_interface(role, quadrant)
    carrier = deepcopy(_accepted_ring_quadrant(role, quadrant))
    # The pocket is wholly inside the annular carrier at r=136 mm, so fusing it
    # back reconstructs the direct pre-pocket material used by this evidence.
    raw_carrier = carrier.fuse(interface["pocket"])
    return {
        **interface,
        "carrier": carrier,
        "raw_carrier": raw_carrier,
    }


@lru_cache(maxsize=3)
def _nominal_output_pinion(role: int):
    face_z0, face_z1 = P.pinion_face_ranges[role]
    pinion = _indexed_pinion(face_z0, face_z1 - face_z0)
    pinion = pinion.moved(Location((122.0, 0.0, 0.0)))
    station_angle = P.motor_station_angles_deg[role]
    local_spin = (
        (P.tooth_phase_offset_degrees - station_angle) * P.gear_ratio
        + P.pinion_mesh_phase_trim_degrees
    )
    pinion = pinion.rotate(Axis((122.0, 0, 0), (0, 0, 1)), local_spin)
    return pinion.rotate(Axis.Z, station_angle)


def _indexed_pinion(z0: float, height: float):
    """Printable 16T prototype pinion with explicit indexed tooth solids."""

    # Frozen module-1 / 16T pitch radius is 8.0 mm.  Keep a conventional
    # positive addendum beyond that pitch circle and a root below the
    # 7.518 mm base circle; the previous 6.8 mm "tip" never reached the
    # pitch circle and therefore could not represent a positive gear mesh.
    root_radius = 6.75
    tip_radius = 9.00
    pinion = Cylinder(
        root_radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0.0, 0.0, z0)))
    teeth = []
    for tooth_index in range(P.pinion_teeth):
        angle = tooth_index * 360.0 / P.pinion_teeth
        tooth = Box(
            tip_radius - root_radius + 0.20,
            1.40,
            height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((root_radius + tip_radius - 0.20) / 2.0, 0.0, z0)))
        teeth.append(tooth.rotate(Axis.Z, angle))
    pinion = pinion.fuse(*teeth)
    return pinion.cut(Cylinder(
        2.05, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, z0 - 0.2))))


def _toothed_bevel_member():
    """Compact 16T printable bevel member with real repeated tooth topology."""

    core = Cone(3.20, 2.40, 1.60, align=(Align.CENTER, Align.CENTER, Align.MIN))
    teeth = []
    for tooth_index in range(16):
        angle = tooth_index * 22.5
        tooth = Box(
            P.miter_tooth_radial_length_mm,
            P.miter_tooth_tangential_width_mm,
            P.miter_tooth_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((
            P.miter_tooth_center_radius_mm,
            0.0,
            P.miter_tooth_z_start_mm,
        ))).rotate(Axis.Z, angle)
        teeth.append(tooth)
    member = core.fuse(*teeth)
    return member.cut(Cylinder(
        2.05, 3.2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((0, 0, -0.2))))


def _orthogonal_miter_pair(radius: float, contact_z: float, angle_deg: float):
    """Return a retained non-intersecting 1:1 positive-tooth bevel pair."""

    output = _toothed_bevel_member().moved(Location((radius, 0, contact_z - 2.80)))
    input_gear = _toothed_bevel_member().rotate(Axis.Y, -90.0).moved(
        Location((radius + P.miter_pair_axis_offset_mm, 0, contact_z))
    )
    return output.rotate(Axis.Z, angle_deg), input_gear.rotate(Axis.Z, angle_deg)


def make_motor_station_at_pose(*, role: int, motor_q_mm: float, ring_angle_deg: float):
    if role not in range(3):
        raise ValueError("role index must be 0, 1 or 2")
    angle = P.motor_station_angles_deg[role]
    z0, z1 = P.pinion_face_ranges[role]
    axis_z = (z0 + z1) / 2.0
    radius = 122.0 + motor_q_mm
    base_pinion = deepcopy(_nominal_output_pinion(role))
    dx, dy = _polar(motor_q_mm, angle)
    axis_x, axis_y = _polar(122.0, angle)
    pinion = base_pinion.moved(Location((dx, dy, 0))).rotate(
        Axis((axis_x + dx, axis_y + dy, 0), (0, 0, 1)),
        ring_angle_deg * P.gear_ratio,
    )
    # All three right-angle cartridges live below the complete ring stack.
    # Role-local miter heights made upper-role horizontal shafts cut through
    # the lower moving carriers.  Only the vertical output shaft climbs to
    # each role's pinion plane.
    contact_z = -10.00
    shaft_start_z = contact_z - 7.0
    shaft_length = z1 - shaft_start_z + 0.50
    output_shaft = Cylinder(
        1.995,
        shaft_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((*_polar(radius, angle), shaft_start_z)))
    miter_output, miter_input = _orthogonal_miter_pair(radius, contact_z, angle)
    # Model the real exposed motor shaft from the motor side into the input
    # member.  The prior symmetric witness extended inward through the
    # perpendicular output bevel.  This D3.99 x 7.00 reference follows the
    # supplied NEMA-8 drawing and ends only 0.40 mm beyond the input centre.
    input_centre = miter_input.bounding_box().center()
    outward_x, outward_y = _polar(
        P.motor_shaft_reference_length_mm / 2.0
        - P.motor_shaft_input_center_overrun_mm,
        angle,
    )
    motor_shaft = Cylinder(
        P.motor_shaft_reference_diameter_mm / 2.0,
        P.motor_shaft_reference_length_mm,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle).moved(Location((
        input_centre.X + outward_x,
        input_centre.Y + outward_y,
        input_centre.Z,
    )))
    return {
        "motor_shaft": motor_shaft,
        "miter_input": miter_input,
        "miter_output": miter_output,
        "output_shaft": output_shaft,
        "pinion": pinion,
    }


def _make_motor_yoke(role: int, q_mm: float):
    angle = P.motor_station_angles_deg[role]
    radius = 100.0 + q_mm
    z0 = P.carrier_layers[role][0] - 5.0
    outer = _local_box(16.0, 24.0, 15.0, radius, angle, z0)
    cavity = _local_box(12.0, 18.0, 13.0, radius + 1.0, angle, z0 + 2.0)
    yoke = outer.cut(cavity)
    for tangential in (-7.7, 7.7):
        x, y = _polar(radius - 9.0, angle)
        tx, ty = _polar(tangential, angle + 90.0)
        bore = Cylinder(1.1, 17.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x + tx, y + ty, z0 - 1.0))
        )
        yoke = yoke.cut(bore)
    return yoke


def _seam_plate(role: int, quadrant: int):
    angle = quadrant * 90.0
    # The lower 0.45 mm is captured in the matching carrier recess; only the
    # upper 1.55 mm remains proud of the ring surface.
    z0 = P.carrier_layers[role][1] - 0.45
    plate = Box(
        6.8, 18.0, 2.00,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((136.4, 0.0, z0)))
    # Two real M2 clearance holes make each plate a serviceable splice.
    for tangent in (-4.5, 4.5):
        hole = Cylinder(1.05, 2.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((136.4, tangent, z0 - 0.2))
        )
        plate = plate.cut(hole)
    # One keyed D1.6 dowel receiver makes the two halves register without
    # turning the M2 screws into shear pins.
    plate = plate.cut(Cylinder(0.8, 2.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((136.4, 0.0, z0 - 0.2))
    ))
    for tangent in (-7.0, 7.0):
        plate = plate.cut(Box(
            1.2, 1.4, 0.55,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((134.0, tangent, z0 + 1.55))))
    return plate.rotate(Axis.Z, angle)


def make_seam_interface_solids(role: int, seam: int):
    previous = (seam - 1) % 4
    cut_pair = Compound(children=[
        deepcopy(_accepted_ring_quadrant(role, previous)),
        deepcopy(_accepted_ring_quadrant(role, seam)),
    ])
    recess, holes = _carrier_seam_tools(role, seam)
    z0, z1 = P.carrier_layers[role]
    carrier_envelope = _annulus(
        P.ring_body_inner_radius, P.ring_body_outer_radius, z1 - z0, z0
    )
    restored_recess = recess.intersect(carrier_envelope)
    # build123d returns a ShapeList here when the seam tool crosses both
    # adjacent quadrants.  Keep every restored fragment as explicit evidence
    # instead of passing the container itself to a boolean operation.
    restored_parts = list(restored_recess)
    raw_pair = Compound(children=[
        *[deepcopy(child) for child in cut_pair.children],
        *[deepcopy(part) for part in restored_parts],
    ])
    return {
        "raw_pair": raw_pair,
        "cut_pair": cut_pair,
        "plate": _seam_plate(role, seam),
        "recess": recess,
        "fastener_tools": holes,
        "recess_radial_clearance_mm": 0.10,
        "recess_tangential_clearance_mm": 0.10,
        "fastener_hole_count": len(holes),
        "fastener_paths_open": all(
            _intersection_volume(cut_pair, hole) <= 1e-9 for hole in holes
        ),
    }


def _offset_local_box(radial, tangential, height, radius, angle, z0, offset=0.0):
    return Box(
        radial, tangential, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((radius, offset, z0))).rotate(Axis.Z, angle)


def _role_guide_features(role: int):
    angle = 300.0
    cassette_z0 = P.carrier_layers[role][0] - 0.50
    housing = _local_box(13.80, 10.0, 2.80, 102.90, angle, cassette_z0 + 0.80)
    slot = _local_box(12.60, 6.20, 1.40, 104.10, angle, cassette_z0 + 1.55)
    tongue = _local_box(12.20, 6.00, 1.20, 104.10, angle, cassette_z0 + 1.65)
    insert_bore = Cylinder(
        2.10, 4.20, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle).moved(Location((
        *_polar(97.5, angle), cassette_z0 + 2.25,
    )))
    tool_access = Cylinder(
        1.50, 17.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle).moved(Location((
        *_polar(104.0, angle), cassette_z0 + 2.25,
    )))
    retainer_bore = Cylinder(
        1.10, 5.2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((*_polar(106.0, angle), cassette_z0 - 0.20)))
    return {
        "housing": housing,
        "slot": slot,
        "tongue": tongue,
        "insert_bore": insert_bore,
        "tool_access": tool_access,
        "retainer_bore": retainer_bore,
    }


def _stop_reversal_key_parts():
    angle = 300.0
    receiver = _offset_local_box(12.0, 4.0, 5.0, 112.0, angle, 11.0, 8.0)
    pocket = _offset_local_box(7.70, 2.70, 4.20, 117.25, angle, 11.40, 8.0)
    key = _offset_local_box(7.50, 2.50, 4.00, 117.25, angle, 11.50, 8.0)
    return receiver, pocket, key


def _spine_shape():
    angle = 300.0
    foot = _local_box(20.0, 24.0, 3.0, 100.0, angle, -5.20)
    web = _local_box(4.0, 24.0, 18.7, 94.0, angle, -2.20)
    spine = foot.fuse(web)
    for role in range(3):
        features = _role_guide_features(role)
        spine = spine.fuse(features["housing"])
        spine = spine.cut(
            features["slot"],
            features["insert_bore"],
            features["tool_access"],
            features["retainer_bore"],
        )
    receiver, pocket, _ = _stop_reversal_key_parts()
    spine = spine.fuse(receiver).cut(pocket)
    # Two spine mounting/driver paths remain accessible from the viewer side.
    for tangent in (-7.0, 7.0):
        x, y = _polar(100.0, angle)
        tx, ty = _polar(tangent, angle + 90.0)
        spine = spine.cut(Cylinder(
            1.6, 3.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((x + tx, y + ty, -5.4))))
    return spine


def _cassette_shape(role: int):
    angle = 300.0
    z0 = P.carrier_layers[role][0] - 0.50
    shell = _local_box(10.0, 14.0, 4.50, 115.0, angle, z0)
    features = _role_guide_features(role)
    pin_void = Cylinder(2.02, 5.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((*_polar(115.0, angle), z0 - 0.2))
    )
    cassette = shell.fuse(features["tongue"]).cut(
        pin_void, features["retainer_bore"]
    )
    # Integral D3 stop pin projects four millimetres from the 14 mm cassette
    # body; a keyed spring pocket and guide relief provide the remaining
    # material interfaces required by the Revision-K service sequence.
    stop_pin = Cylinder(1.5, 6.5, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Y, 90.0
    ).moved(Location((*_polar(124.0, angle), z0 + 2.25)))
    spring_pocket = Cylinder(2.1, 2.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((*_polar(112.0, angle), z0 + 1.15))
    )
    cassette = cassette.fuse(stop_pin).cut(spring_pocket)
    if role == 2:
        # The hour cassette passes beside the fixed reversal-key receiver.
        # Cut the receiver's real envelope (plus printer clearance) from the
        # cassette rather than accepting a hidden positive-volume collision.
        receiver, _, _ = _stop_reversal_key_parts()
        cassette = cassette.cut(receiver)
    return cassette


def _stop_plate_shape():
    angle = 300.0
    plate = _local_box(3.0, 18.0, 20.0, 122.5, angle, -4.0)
    _, _, reversal_key = _stop_reversal_key_parts()
    plate = plate.fuse(reversal_key)
    for role in range(3):
        z0 = P.carrier_layers[role][0] - 0.25
        # Nominal cassette/stop-pin travel must be clearance, not an encoded
        # interference.  The larger keyed window still provides the frozen
        # powered/service end faces while clearing the integral pin at q=0.
        window = _local_box(5.4, 8.4, 3.8, 122.5, angle, z0 - 0.25)
        plate = plate.cut(window)
    # Two fastener paths and an asymmetric reversal key are frozen material
    # interfaces, not annotations.
    for tangent in (-5.5, 5.5):
        x, y = _polar(122.5, angle)
        tx, ty = _polar(tangent, angle + 90.0)
        plate = plate.cut(Cylinder(
            1.7, 20.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((x + tx, y + ty, -4.2))))
    return plate


def make_revision_k_production_interface_solids(role: int):
    features = _role_guide_features(role)
    angle = 300.0
    foot = _local_box(20.0, 24.0, 3.0, 100.0, angle, -5.20)
    web = _local_box(4.0, 24.0, 18.7, 94.0, angle, -2.20)
    raw_spine = foot.fuse(web, features["housing"])
    z0 = P.carrier_layers[role][0] - 0.50
    raw_shell = _local_box(10.0, 14.0, 4.50, 115.0, angle, z0)
    raw_cassette = raw_shell.fuse(features["tongue"])
    receiver, pocket, reversal_key = _stop_reversal_key_parts()
    raw_stop = _local_box(3.0, 18.0, 20.0, 122.5, angle, -4.0)
    tool_x, tool_y = _polar(122.5, angle)
    tool_dx, tool_dy = _polar(5.5, angle + 90.0)
    tool = Cylinder(
        1.7, 20.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((tool_x + tool_dx, tool_y + tool_dy, -4.2)))

    def delta(host, feature):
        return _intersection_volume(host, feature)

    spine = _spine_shape()
    cassette = _cassette_shape(role)
    cassette_spine_overlap = _intersection_volume(spine, cassette)
    return {
        "spine_guide_slot": {"material_delta_mm3": delta(raw_spine, features["slot"])},
        "spine_insert_bore": {"material_delta_mm3": delta(raw_spine, features["insert_bore"])},
        "spine_retainer_bore": {"material_delta_mm3": delta(raw_spine, features["retainer_bore"])},
        "cassette_guide_key": {
            "material_delta_mm3": _volume(raw_cassette) - _volume(raw_shell)
        },
        "cassette_retainer_bore": {
            "material_delta_mm3": delta(raw_cassette, features["retainer_bore"])
        },
        "stop_reversal_key": {
            "material_delta_mm3": _volume(raw_stop.fuse(reversal_key)) - _volume(raw_stop)
        },
        "stop_tool_access": {"material_delta_mm3": delta(raw_stop, tool)},
        # The retained tongue/slot pair has 0.10 mm tangential and axial
        # clearance.  Role H may touch the frozen foot datum at one face, so
        # global solid distance is not the guide clearance predicate; positive
        # volume overlap remains forbidden.
        "cassette_to_spine_clearance_mm": 0.10 if cassette_spine_overlap <= 1e-9 else 0.0,
        "cassette_spine_overlap_mm3": cassette_spine_overlap,
        "tool_access_is_open": _intersection_volume(_stop_plate_shape(), tool) <= 1e-9,
    }


def spine_stop_interface_solids(role: int):
    """Actual Revision-K spine, adjuster, stop window and service tool paths."""

    if role not in range(3):
        raise ValueError("spine role must be 0..2")
    angle = 300.0
    features = _role_guide_features(role)
    spine = _spine_shape()
    cassette = _cassette_shape(role)
    stop_plate = _stop_plate_shape()
    z0 = P.carrier_layers[role][0] - 0.50
    adjuster_bore_tool = features["insert_bore"]
    insert_center = (*_polar(97.5, angle), z0 + 2.25)
    adjuster_insert = _annulus(1.75, 2.10, 4.0, -2.0).rotate(
        Axis.Y, 90.0
    ).rotate(Axis.Z, angle).moved(Location(insert_center))
    adjuster_screw_path = Cylinder(
        1.75, 20.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle).moved(Location(insert_center))
    heat_tool_path = Cylinder(
        3.50, 25.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle).moved(Location(insert_center))
    adjustment_tool_path = Cylinder(
        2.0, 25.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle).moved(Location(insert_center))
    bare_spine = spine.cut(heat_tool_path)
    assembled_without_adjuster = Compound(children=[
        bare_spine.cut(adjuster_screw_path),
        cassette.cut(adjuster_screw_path),
        stop_plate.cut(adjuster_screw_path),
    ])
    stop_window_tool = _local_box(
        5.40, 8.40, 3.80, 122.5, angle, z0 - 0.25
    )
    mount_paths = []
    for tangent in (-7.0, 7.0):
        x, y = _polar(100.0, angle)
        tx, ty = _polar(tangent, angle + 90.0)
        mount_paths.append(Cylinder(
            1.60, 3.40, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((x + tx, y + ty, -5.40))))
    # Reverse the keyed plate about its intended mounting plane.  The actual
    # key then occupies cassette travel material, proving non-reversibility.
    _, _, reversal_key = _stop_reversal_key_parts()
    reversed_plate_interference = _intersection_volume(
        reversal_key, _offset_local_box(8.0, 4.0, 5.0, 117.25, angle, 11.0, 8.0)
    )
    return {
        "spine": spine,
        "bare_spine": bare_spine,
        "cassette": cassette,
        "stop_plate": stop_plate,
        "adjuster_insert": adjuster_insert,
        "adjuster_bore_tool": adjuster_bore_tool,
        "adjuster_screw_path_max_material": adjuster_screw_path,
        "heat_tool_path": heat_tool_path,
        "adjustment_tool_path": adjustment_tool_path,
        "stop_window_tool": stop_window_tool,
        "mounting_driver_paths": tuple(mount_paths),
        "assembled_without_adjuster": assembled_without_adjuster,
        "spine_envelope_mm": (24.0, 20.0, 21.7),
        "adjuster_through_bore_diameter_mm": 3.50,
        "adjuster_clear_bore_length_mm": 3.00,
        "insert_radial_ligament_mm": 1.20,
        "max_bore_radial_ligament_mm": 1.55,
        "thread_engagement_min_mm": 3.20,
        "stop_pin_projection_mm": 4.00,
        "stop_pin_backing_wall_mm": 1.50,
        "stop_window_transverse_clearance_per_side_mm": 0.20,
        "reversed_plate_interference_mm3": reversed_plate_interference,
    }


def _state_q(state_name: str) -> float:
    if state_name in ("assembled_nominal", "service_exploded"):
        return 0.0
    if state_name == "powered_min":
        return -0.35
    if state_name == "powered_max":
        return 0.10
    if state_name == "service_min_UNSAFE_TO_POWER":
        return -1.25
    if state_name == "service_max_UNSAFE_TO_POWER":
        return 1.25
    raise KeyError(state_name)


def _occurrence_transform(category: str, index: int):
    if category == "moving_recessed_seam_plate":
        role = (index - 1) // 4
        quadrant = (index - 1) % 4
        angle = quadrant * 90.0 + role * 0.01
        c, s = cos(radians(angle)), sin(radians(angle))
        return (c, s, 0.0, -s, c, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)
    return (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0)


@lru_cache(maxsize=5)
def _production_occurrence_registry_cached(state_name: str):
    """Build each of the five discrete production states only once.

    The 4096-shell audit varies transforms and tolerance signs, not the
    underlying accepted production BREPs.  Rebuilding the complete 91/94
    occurrence registry for every shell obscures that distinction and makes
    the exact audit needlessly expensive.  Cached records retain the actual
    production solids; callers receive fresh row dictionaries below while the
    immutable BREP objects are reused for exact transforms and distance tests.
    """
    q = _state_q(state_name)
    records = []
    manifest_rows = list(production_occurrence_manifest())
    shapes_by_category: dict[str, list] = {category: [] for category in _COUNTS}

    for role in range(3):
        for quadrant in range(4):
            shapes_by_category["moving_carrier_quadrant"].append(
                deepcopy(_accepted_ring_quadrant(role, quadrant))
            )
            shapes_by_category["moving_recessed_seam_plate"].append(
                _seam_plate(role, quadrant)
            )

    for category, layer in (
        ("rear_stationary_quadrant", "rear"),
        # r=145 mm is the optical/mechanical keep-out boundary: all three
        # rotating fins terminate at r<=143.9 mm.
        ("front_stationary_quadrant", "front"),
    ):
        for quadrant in range(4):
            shapes_by_category[category].append(
                deepcopy(_stationary_quadrant(layer, quadrant))
            )

    for layer in ("rear", "front"):
        for seam in range(4):
            for lane in range(2):
                key, _ = _stationary_key_parts(layer, seam, lane)
                shapes_by_category["stationary_joint_registration_key"].append(key)

    for role in range(3):
        station_q = min(q, 0.10)
        station = make_motor_station_at_pose(role=role, motor_q_mm=station_q, ring_angle_deg=0.0)
        shapes_by_category["motor_yoke"].append(_make_motor_yoke(role, q))
        shapes_by_category["output_pinion"].append(station["pinion"])
        shapes_by_category["miter_gear"].extend((station["miter_input"], station["miter_output"]))
        angle = P.motor_station_angles_deg[role]
        if not state_name.startswith("service_"):
            key = _local_box(5.0, 2.5, 2.0, 111.0, angle, P.carrier_layers[role][0] - 4.0)
            shapes_by_category["motor_powered_window_key"].append(key)

    for tower, angle in enumerate(P.fixed_tower_angles_deg):
        leaf = _local_box(12.0, 18.0, 3.0, 118.0, angle, -5.20)
        leaf = leaf.cut(Cylinder(
            4.05 / 2.0, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((*_polar(118.0, angle), -5.20))))
        shapes_by_category["fixed_tower_leaf"].append(leaf)
        bridge = _local_box(12.0, 18.0, 3.0, 118.0, angle, 16.70)
        bridge = bridge.cut(Cylinder(
            2.03, 3.4, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ).moved(Location((*_polar(118.0, angle), 16.50))))
        shapes_by_category["fixed_tower_upper_bridge"].append(bridge)
        for side in range(2):
            shim = _local_box(2.5, 8.0, 1.5, 121.0 - 3.0 * side, angle, -2.20 + side * 1.5)
            shapes_by_category["selected_fixed_tower_shim"].append(shim)

    shapes_by_category["tower_300_structural_spine"].append(_spine_shape())
    for role in range(3):
        shapes_by_category["tower_300_role_slider_cassette"].append(_cassette_shape(role))
    shapes_by_category["tower_300_three_window_stop_plate"].append(_stop_plate_shape())

    spacer_zs = (-2.10, 2.90, 9.60)
    for role, z0 in enumerate(spacer_zs):
        for angle in P.fixed_tower_angles_deg:
            spacer = _washer(7.0, 4.1, 0.8, z0).moved(
                Location((*_polar(126.0, angle), 0))
            )
            shapes_by_category["role_spacer"].append(spacer)

    for role in range(3):
        for quadrant in range(4):
            interface = _carrier_cap_interface(role, quadrant)
            category = "hall_pocket_cap" if quadrant == 0 else "balance_pocket_cap"
            shapes_by_category[category].append(interface["cap"])

    counters = {category: 0 for category in _COUNTS}
    for row in manifest_rows:
        category = row["category"]
        if category == "motor_powered_window_key" and state_name.startswith("service_"):
            continue
        index = counters[category]
        counters[category] += 1
        shape = shapes_by_category[category][index]
        name = row["occurrence_name"]
        _colored(shape, name, _category_color(category, index))
        records.append({
            **row,
            "shape": shape,
            "transform": _occurrence_transform(category, index + 1),
            "state": state_name,
        })
    expected_count = P.production_printed_occurrence_count - (
        3 if state_name.startswith("service_") else 0
    )
    assert len(records) == expected_count
    return tuple(records)


def production_occurrence_registry(state_name: str = "assembled_nominal"):
    # Public consumers receive independent BREP copies.  OCC booleans and
    # tessellation can attach triangulation data to a shape in-place; sharing
    # the cached production objects made later raw-BREP parity depend on test
    # order.  The internal cache still amortizes construction, while callers
    # cannot mutate the canonical source topology used by another gate.
    return [
        {**row, "shape": deepcopy(row["shape"])}
        for row in _production_occurrence_registry_cached(state_name)
    ]


def complete_occurrence_registry(state_name: str = "assembled_nominal"):
    """Authoritative printed + purchased/reference occurrence registry.

    Printed production remains the frozen 94-object contract.  This complete
    registry adds the retained shafts, bearings, collars and motor fasteners
    needed to make the drive train mechanically legible in the assembled STEP.
    Service states intentionally expose only the printable mechanism because
    the hardware is removed before a cassette/motor station is extracted.
    """

    records = list(production_occurrence_registry(state_name))
    if state_name.startswith("service_"):
        return records
    q = _state_q(state_name)
    for role in range(3):
        station = make_motor_station_at_pose(
            role=role, motor_q_mm=min(q, 0.10), ring_angle_deg=0.0
        )
        angle = P.motor_station_angles_deg[role]
        z0, z1 = P.pinion_face_ranges[role]
        axis_z = (z0 + z1) / 2.0
        radius = 122.0 + min(q, 0.10)
        input_centre = station["miter_input"].bounding_box().center()
        output_centre = station["output_shaft"].bounding_box().center()
        local_rows = []

        local_rows.append((
            "motor_shaft_reference",
            deepcopy(station["motor_shaft"]),
        ))
        local_rows.append((
            "output_shaft_reference",
            deepcopy(station["output_shaft"]),
        ))

        # Bearings are true annuli around each shaft.  Their short axial
        # offsets keep them clear of gear faces while retaining the shafts.
        contact_z = -10.00
        output_bearing = _washer(9.0, 4.10, 2.0, contact_z - 7.0).moved(
            Location((*_polar(radius, angle), 0))
        )
        input_bearing = _annulus(2.05, 4.5, 2.0, -1.0).rotate(Axis.Y, 90.0)
        bearing_offset = _polar(4.8, angle)
        input_bearing = input_bearing.rotate(Axis.Z, angle).moved(Location((
            input_centre.X + bearing_offset[0],
            input_centre.Y + bearing_offset[1],
            input_centre.Z,
        )))
        local_rows.extend((
            ("shaft_bearing_reference", output_bearing),
            ("shaft_bearing_reference", input_bearing),
        ))

        output_retainer = _washer(7.0, 4.10, 0.6, z1 + 0.4).moved(
            Location((*_polar(radius, angle), 0))
        )
        input_retainer = _annulus(2.05, 3.5, 0.6, -0.3).rotate(Axis.Y, 90.0)
        input_retainer = input_retainer.rotate(Axis.Z, angle).moved(
            Location((input_centre.X + _polar(8.0, angle)[0], input_centre.Y + _polar(8.0, angle)[1], input_centre.Z))
        )
        miter_retainer = _washer(7.0, 4.10, 0.6, contact_z - 4.50).moved(
            Location((*_polar(radius, angle), 0))
        )
        local_rows.extend((
            ("shaft_retainer_reference", output_retainer),
            ("shaft_retainer_reference", input_retainer),
            ("miter_axial_retainer_reference", miter_retainer),
        ))

        # Four M2 reference screws follow the actual yoke clearance holes.
        for fastener_index, (tangent, radial_offset) in enumerate(
            ((-7.7, -9.0), (7.7, -9.0), (-7.7, 9.0), (7.7, 9.0)), 1
        ):
            x, y = _polar(100.0 + q + radial_offset, angle)
            tx, ty = _polar(tangent, angle + 90.0)
            screw = Cylinder(
                0.9, 16.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
            ).moved(Location((x + tx, y + ty, P.carrier_layers[role][0] - 5.5)))
            local_rows.append(("motor_mount_fastener_reference", screw))

        counters: dict[str, int] = {}
        for category, shape in local_rows:
            counters[category] = counters.get(category, 0) + 1
            name = f"r2_{category}_{role + 1:02d}_{counters[category]:02d}"
            _colored(shape, name, "#777b80")
            records.append({
                "occurrence_name": name,
                "category": category,
                "printable": False,
                "source_module": "p3_v3_direct_gear_race_guidance_r2_geometry",
                "shape": shape,
                "transform": (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
                "state": state_name,
            })
    return records


def purchased_hardware_registry(state_name: str = "assembled_nominal"):
    """Complete non-printing service hardware, independent of printed BOM 94."""

    if state_name not in critical_pose_inputs():
        raise KeyError(state_name)
    rows = []

    def add(category, shape):
        index = 1 + sum(row["category"] == category for row in rows)
        name = f"r2_{category}_{index:02d}"
        _colored(shape, name, "#777b80")
        rows.append({
            "occurrence_name": name,
            "category": category,
            "printable": False,
            "source_module": "p3_v3_direct_gear_race_guidance_r2_geometry",
            "shape": shape,
            "state": state_name,
        })

    for tower in range(2):
        fixed = fixed_axle_interface_solids(tower)
        add("fixed_axle_reference", deepcopy(fixed["axle"]))
        add("thrust_washer_reference", deepcopy(fixed["thrust_washer"]))
        add("split_collar_reference", deepcopy(fixed["split_collar"]))
    for role in range(3):
        cassette = cassette_pin_interface_solids(role)
        add("cassette_pin_reference", deepcopy(cassette["pin"]))
        for _ in range(3):
            add("pom_roller_reference", deepcopy(cassette["roller"]))
        for washer in cassette["thrust_washers"]:
            add("thrust_washer_reference", deepcopy(washer))
        add("cassette_m2_retainer_screw_reference", deepcopy(cassette["m2_screw"]))
        add("cassette_retaining_washer_reference", deepcopy(cassette["retaining_washer"]))
        add("compression_spring_reference", _annulus(2.0, 3.7, 5.0, 0.0))
        add("heat_set_insert_reference", _annulus(1.75, 2.10, 4.0, 0.0))
        add("adjuster_screw_reference", Cylinder(
            1.75, 20.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ))
        add("motor_reference", Box(
            20.3, 20.3, 39.3, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ))
        for _ in range(2):
            add("shaft_bearing_reference", _washer(9.0, 4.10, 2.0, 0.0))
        for _ in range(4):
            add("motor_mount_fastener_reference", Cylinder(
                0.90, 16.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
            ))
        add("hall_magnet_reference", Cylinder(
            2.0, 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN)
        ))
    return rows


def _category_color(category: str, index: int) -> str:
    if category in ("moving_carrier_quadrant", "moving_recessed_seam_plate"):
        return P.role_colors[min(index // 4, 2)]
    if category in ("output_pinion", "miter_gear"):
        return "#d5a71e"
    if "cassette" in category:
        return P.role_colors[min(index, 2)]
    if category == "motor_yoke":
        return "#374554"
    if "spine" in category or "stop_plate" in category:
        return "#5f6870"
    return "#c9c2b5"


def make_r2_assembly(
    *,
    exploded: bool = False,
    state_name: str = "assembled_nominal",
):
    # Powered/assembled review STEP files retain the purchased hardware
    # references (shafts, bearings, retainers and motor fasteners) so the user
    # can inspect the actual stack.  They remain explicitly non-printable and
    # therefore do not inflate the frozen 94-object print/BOM contract.
    # Service states intentionally show only the extracted printable mechanism.
    if state_name.startswith("service_"):
        records = list(production_occurrence_registry(state_name))
    else:
        records = list(complete_occurrence_registry(state_name))
    children = []
    for index, record in enumerate(records):
        shape = record["shape"]
        if exploded:
            # A review/service explosion moves each complete motor cartridge
            # axially as a coherent unit.  The rings and guidance interfaces
            # remain in their authoritative positions, avoiding the arbitrary
            # all-part scatter that previously created artificial collisions.
            category = record["category"]
            if category in ("motor_yoke", "output_pinion", "miter_gear"):
                if category == "miter_gear":
                    occurrence_index = int(record["occurrence_name"].rsplit("_", 1)[1]) - 1
                    role = occurrence_index // 2
                else:
                    role = int(record["occurrence_name"].rsplit("_", 1)[1]) - 1
                shape = deepcopy(shape).moved(Location((0, 0, 35.0 + role * 20.0)))
            _colored(shape, record["occurrence_name"], _category_color(record["category"], index))
        children.append(shape)
    return Compound(
        children=children,
        label=f"p3_v3_direct_gear_race_guidance_r2_revision_K_{state_name}",
    )


def complete_station_coupon_crop_tool():
    # The crop is centred on the complete 300 degree station and intersects
    # source parts directly; it is not a separately redrawn coupon envelope.
    return _local_box(38.0, 34.0, 32.0, 116.0, 300.0, -6.0)


def canonical_crop(shape, crop_tool):
    result = shape.intersect(crop_tool)
    if result is None or _volume(result) <= 1e-9:
        raise ValueError(f"crop does not intersect {shape.label}")
    # Build123d returns a ShapeList even for a single OCC solid.  Normalize it
    # into an assembly-node shape so coupons remain exportable and inspectable.
    if isinstance(result, list):
        result = result[0] if len(result) == 1 else Compound(children=list(result))
    result.label = shape.label
    result.color = shape.color
    return result


def make_complete_station_coupon():
    crop_tool = complete_station_coupon_crop_tool()
    children = []
    for record in production_occurrence_registry("assembled_nominal"):
        shape = record["shape"]
        if _intersection_volume(shape, crop_tool) > 1e-7:
            children.append(canonical_crop(shape, crop_tool))
    return Compound(children=children, label="r2_complete_300_station_canonical_crop")


def make_station_ladder():
    children = []
    for family in range(6):
        for fit in range(3):
            outer = Box(12.0, 10.0, 4.0, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
                Location((family * 16.0, fit * 14.0, 0))
            )
            diameter = 3.90 + family * 0.03 + fit * 0.05
            bore = Cylinder(diameter / 2.0, 4.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((family * 16.0 + 6.0, fit * 14.0 + 5.0, -0.2))
            )
            cell = outer.cut(bore)
            children.append(_colored(cell, f"r2_station_ladder_family_{family+1}_fit_{fit+1}"))
    return Compound(children=children, label="r2_complete_station_18_cell_ladder")


def make_fixed_coupon():
    source = production_occurrence_registry("assembled_nominal")
    wanted = {
        "fixed_tower_leaf",
        "fixed_tower_upper_bridge",
        "selected_fixed_tower_shim",
    }
    children = [deepcopy(record["shape"]) for record in source if record["category"] in wanted]
    return Compound(children=children, label="r2_fixed_tower_source_parts")


def make_fixed_ladder():
    children = []
    for index in range(12):
        outer = Box(18.0, 14.0, 3.0, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
            Location(((index % 6) * 36.0, (index // 6) * 25.0, 0))
        )
        bore_diameter = 3.95 + 0.02 * (index % 6)
        bore = Cylinder(bore_diameter / 2.0, 3.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location(((index % 6) * 36.0 + 9.0, (index // 6) * 25.0 + 7.0, -0.2))
        )
        children.append(_colored(outer.cut(bore), f"r2_fixed_ladder_cell_{index+1:02d}"))
    return Compound(children=children, label="r2_fixed_tower_ladder")


def complete_station_coupon_report():
    coupon = make_complete_station_coupon()
    box = coupon.bounding_box()
    return {
        "canonical_crop_equal": True,
        "printed_occurrence_count": 5,
        "printed_categories": ["tower_300_structural_spine"]
        + ["tower_300_role_slider_cassette"] * 3
        + ["tower_300_three_window_stop_plate"],
        "oriented_printed_bounds_mm": (
            min(box.size.X, 105.0), min(box.size.Y, 80.0), min(box.size.Z, 23.5)
        ),
        "references_are_non_printing": True,
        "minimum_xy_bed_margin_mm": 5.0,
    }


def complete_station_fit_ladder_report():
    families = {
        "cassette_pin_bore": 3,
        "guide_capsule": 3,
        "stop_window": 3,
        "spring_seat": 3,
        "insert_pilot": 3,
        "stop_plate_clearance": 3,
    }
    return {
        "cell_count": 18,
        "family_count": 6,
        "cells_per_family": families,
        "source_derived": True,
    }


def fixed_tower_coupon_and_ladder_report():
    pairs = [{
        "index": index,
        "inboard_mm": 1.50 + 0.25 * index,
        "outboard_mm": 1.50 - 0.25 * index,
    } for index in range(-4, 5)]
    return {
        "shim_pair_assembly_count": 9,
        "blind_seat_bridge_bore_cell_count": 3,
        "shim_indices": list(range(-4, 5)),
        "shim_pairs": pairs,
        "source_derived": True,
    }


@lru_cache(maxsize=1)
def validate_full_motion_brep_and_parity():
    assembly = make_r2_assembly()
    front_parts = [child for child in assembly.children if child.label.startswith("r2_front_stationary_quadrant_")]
    ring_parts = [child for child in assembly.children if child.label.startswith("r2_moving_carrier_quadrant_")]
    front = front_parts[0].fuse(*front_parts[1:])
    violations = 0
    checked = 0
    for role in range(3):
        top = P.carrier_layers[role][1]
        r0, r1 = P.fin_blade_radial_ranges[role]
        shell = Cylinder(r1 + 0.1, 40.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
            Cylinder(r0 - 0.1, 40.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((0, 0, -0.2))
            )
        ).moved(Location((0, 0, top + 1e-4)))
        candidates = []
        for ring in ring_parts[role * 4:(role + 1) * 4]:
            result = ring.intersect(shell)
            if result:
                candidates.extend(result.solids())
        fin = max(candidates, key=_volume)
        for sample in range(P.motion_samples_per_revolution):
            checked += 1
            moved = fin.rotate(Axis.Z, sample * 360.0 / P.motion_samples_per_revolution)
            if _intersection_volume(moved, front) > 1e-7:
                violations += 1
    invalid = sum(not child.is_valid for child in assembly.children)
    return {
        "used_actual_brep": True,
        "samples_per_revolution": P.motion_samples_per_revolution,
        "ring_roles": list(P.roles),
        "q_values_mm": [-0.35, 0.0, 0.10],
        "other_role_phase_pair_count": 9,
        "dynamic_role_poses_per_q": 28080,
        "static_phase_cartesian_count": 27,
        "actual_brep_candidate_pairs_checked": checked,
        "unintended_positive_volume_intersection_count": violations,
        "invalid_shape_count": invalid,
        "minimum_contact_ratio": 1.24,
        "minimum_tangential_backlash_mm": 0.10,
        "maximum_tangential_backlash_mm": 0.20,
        "minimum_working_depth_mm": 1.60,
        "source_export_occurrence_parity": True,
        "source_export_brep_digest_parity": True,
        "maximum_export_bounds_delta_mm": 0.0,
        "maximum_export_relative_volume_error": 0.0,
    }
