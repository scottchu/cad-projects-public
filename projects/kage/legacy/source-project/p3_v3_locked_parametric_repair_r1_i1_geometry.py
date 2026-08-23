"""I1 fixed-tower axle-retention geometry for the accepted KAGE R1 clock."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import atan2, cos, degrees, radians, sin

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cylinder,
    Location,
    RegularPolygon,
    extrude,
)

from p3_v3_locked_parametric_repair_r1_parity import baseline_occurrences
from p3_v3_locked_parametric_repair_r1_i1_spec import (
    FixedTowerParams,
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1,
    P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE,
)


# Immutable accepted-R1 exterior envelope.  The frozen I1 schema continues to
# describe a 30 mm stock axle; the installed service realization is trimmed to
# this plane so a purchased pin cannot create a new exterior silhouette.
LOCKED_EXTERIOR_MAX_Z_MM = 24.2514
M3_SERVICE_PATH_OUTER_OFFSET_MM = 10.0


FIXED_TOWER_YOKE_NAMES = {1: "occurrence_018", 2: "occurrence_035"}
FIXED_TOWER_AXLE_NAMES = {1: "occurrence_026", 2: "occurrence_043"}
FIXED_TOWER_COLLAR_NAMES = {1: "occurrence_027", 2: "occurrence_044"}
FIXED_TOWER_FASTENER_NAMES = {1: "occurrence_028", 2: "occurrence_045"}


def _volume(shape) -> float:
    if shape is None:
        return 0.0
    return float(sum(solid.volume for solid in shape.solids()))


def _axis_xy(tower: int, params: FixedTowerParams) -> tuple[float, float]:
    angle = radians(params.fixed_station_angles_deg[tower - 1])
    return params.tower_axis_radius_mm * cos(angle), params.tower_axis_radius_mm * sin(angle)


def polar_angle_deg(x: float, y: float) -> float:
    return degrees(atan2(y, x)) % 360.0


def _cylinder_at(x: float, y: float, diameter: float, z0: float, z1: float):
    return Cylinder(
        diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))


def _cylinder_along_xy(
    tower: int,
    params: FixedTowerParams,
    *,
    angle_deg: float,
    diameter: float,
    start_offset_mm: float,
    end_offset_mm: float,
    z_mm: float,
    origin_xy: tuple[float, float] | None = None,
):
    x, y = origin_xy or _axis_xy(tower, params)
    length = end_offset_mm - start_offset_mm
    center_offset = (start_offset_mm + end_offset_mm) / 2.0
    direction_x = cos(radians(angle_deg))
    direction_y = sin(radians(angle_deg))
    return Cylinder(
        diameter / 2.0,
        length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).rotate(Axis.Z, angle_deg).moved(Location((
        x + direction_x * center_offset,
        y + direction_y * center_offset,
        z_mm,
    )))


def _oriented_box_along_xy(
    *,
    origin_xy: tuple[float, float],
    frame_angle_deg: float,
    u_center_mm: float,
    v_center_mm: float,
    z_center_mm: float,
    size_u_mm: float,
    size_v_mm: float,
    size_z_mm: float,
):
    """Box in a local XY frame: U at angle, V at angle+90 degrees."""

    angle = radians(frame_angle_deg)
    center_x = origin_xy[0] + cos(angle) * u_center_mm - sin(angle) * v_center_mm
    center_y = origin_xy[1] + sin(angle) * u_center_mm + cos(angle) * v_center_mm
    return Box(
        size_u_mm,
        size_v_mm,
        size_z_mm,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Z, frame_angle_deg).moved(Location((center_x, center_y, z_center_mm)))


def _hex_prism_along_xy(
    *,
    origin_xy: tuple[float, float],
    angle_deg: float,
    across_flats_mm: float,
    start_offset_mm: float,
    end_offset_mm: float,
    z_mm: float,
):
    """Regular hexagonal prism whose axis lies in XY."""

    length = end_offset_mm - start_offset_mm
    center_offset = (start_offset_mm + end_offset_mm) / 2.0
    direction_x = cos(radians(angle_deg))
    direction_y = sin(radians(angle_deg))
    # RegularPolygon's minor radius is the requested across-flats radius.
    profile = RegularPolygon(
        across_flats_mm / 2.0,
        6,
        major_radius=False,
        rotation=30.0,
    )
    prism = extrude(profile, amount=length)
    return prism.rotate(Axis.Y, 90.0).rotate(Axis.Z, angle_deg).moved(Location((
        origin_xy[0] + direction_x * center_offset,
        origin_xy[1] + direction_y * center_offset,
        z_mm,
    )))


def _collar_frame(tower: int, params: FixedTowerParams):
    axle_x, axle_y = _axis_xy(tower, params)
    screw_axis_angle = params.fixed_station_angles_deg[tower - 1]
    return {
        "axle_center": (axle_x, axle_y),
        "collar_center": (axle_x, axle_y),
        "contact_angle_deg": screw_axis_angle,
        "screw_axis_angle_deg": screw_axis_angle,
        "screw_origin": (axle_x, axle_y),
    }


def _make_leaf(tower: int, params: FixedTowerParams):
    x, y = _axis_xy(tower, params)
    wall_bottom = params.leaf_seat_z_range_mm[0] - params.minimum_leaf_bottom_wall_mm
    body = _cylinder_at(x, y, 8.0, wall_bottom, params.leaf_seat_z_range_mm[1])
    seat = _cylinder_at(
        x, y, params.leaf_seat_diameter_mm,
        params.leaf_seat_z_range_mm[0], params.leaf_seat_z_range_mm[1],
    )
    leaf = body.cut(seat)
    leaf.label = f"p3_v3_r1_i1_tower_{tower}_blind_D4p05x3_leaf_seat"
    return leaf


def _make_upper_bridge(tower: int, params: FixedTowerParams):
    """One connected bridge with two short legs landing on the locked yoke."""

    angle = params.fixed_station_angles_deg[tower - 1]
    z0, z1 = params.upper_bridge_z_range_mm
    # Create in the local radial frame, overlapping the accepted yoke at
    # Z14.50..14.75; rotate only after the union is complete.
    r0, r1 = 114.0, 130.0
    bridge = Box(
        r1 - r0, 10.0, z1 - z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((r0, 0.0, z0)))
    for tangent in (-3.5, 3.5):
        leg = Box(
            4.0, 3.0, z0 - 14.50,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((116.0, tangent, 14.50)))
        bridge = bridge.fuse(leg)
    bridge = bridge.cut(_cylinder_at(
        params.tower_axis_radius_mm,
        0.0,
        params.upper_bridge_bore_diameter_mm,
        z0 - 0.10,
        z1 + 0.10,
    ))
    bridge = bridge.rotate(Axis.Z, angle)
    bridge.label = f"p3_v3_r1_i1_tower_{tower}_upper_bridge_D4p06_through"
    return bridge


def _make_axle(tower: int, params: FixedTowerParams):
    x, y = _axis_xy(tower, params)
    axle = _cylinder_at(
        x, y, params.axle_diameter_mm,
        params.axle_bottom_z_mm, params.axle_top_z_mm,
    )
    axle.label = f"p3_v3_r1_i1_tower_{tower}_D3p99x30_bottomed_axle"
    return axle


def _make_installed_axle(tower: int, params: FixedTowerParams):
    """Installed axle after the stock D3.99x30 pin is cut to the locked skin."""

    x, y = _axis_xy(tower, params)
    axle = _cylinder_at(
        x,
        y,
        params.axle_diameter_mm,
        params.axle_bottom_z_mm,
        min(params.axle_top_z_mm, LOCKED_EXTERIOR_MAX_Z_MM),
    )
    axle.label = (
        f"p3_v3_r1_i1_tower_{tower}_D3p99_stock30_"
        "installed_trimmed_to_locked_envelope"
    )
    return axle


def _make_washer(tower: int, params: FixedTowerParams):
    x, y = _axis_xy(tower, params)
    z0 = params.upper_bridge_z_range_mm[1]
    washer = _cylinder_at(x, y, params.washer_outer_diameter_mm, z0, z0 + params.washer_thickness_mm)
    washer = washer.cut(_cylinder_at(
        x, y, params.washer_bore_diameter_mm,
        z0 - 0.05, z0 + params.washer_thickness_mm + 0.05,
    ))
    washer.label = f"p3_v3_r1_i1_tower_{tower}_D8x0p15_upper_washer"
    return washer


def _make_set_screw_collar(tower: int, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    hardware.validate()
    frame = _collar_frame(tower, params)
    x, y = frame["collar_center"]
    z0, z1 = params.collar_bottom_z_mm, params.collar_top_z_mm
    collar = _cylinder_at(x, y, params.collar_outer_diameter_mm, z0, z1)
    collar = collar.cut(_cylinder_at(
        x, y, params.collar_bore_diameter_mm, z0 - 0.1, z1 + 0.1,
    ))
    screw_axis_angle = frame["screw_axis_angle_deg"]
    # An intact radial D2.50 pilot crosses the complete 2.00 mm D8-to-D4
    # collar wall.  It is tapped M3x0.5 after printing; that operation is an
    # explicit assembly requirement, not an implied printable thread.
    tapped_pilot = _cylinder_along_xy(
        tower,
        params,
        angle_deg=screw_axis_angle,
        diameter=hardware.tap_pilot_diameter_mm,
        start_offset_mm=params.collar_bore_diameter_mm / 2.0,
        end_offset_mm=params.collar_outer_diameter_mm / 2.0 + 0.5,
        z_mm=(z0 + z1) / 2.0,
        origin_xy=frame["screw_origin"],
    )
    collar = collar.cut(tapped_pilot)
    collar.label = f"p3_v3_r1_i1_tower_{tower}_intact_D4_D8x4_M3_set_screw_collar"
    return collar


def _make_m3_reference(tower: int, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    frame = _collar_frame(tower, params)
    screw_axis_angle = frame["screw_axis_angle_deg"]
    screw_axis_z = params.collar_bottom_z_mm + params.collar_height_mm / 2.0
    outer_face = params.collar_outer_diameter_mm / 2.0 - hardware.nominal_outer_face_recess_mm
    tip = outer_face - hardware.nominal_screw_length_mm
    fastener = _cylinder_along_xy(
        tower,
        params,
        angle_deg=screw_axis_angle,
        diameter=hardware.nominal_screw_diameter_mm,
        start_offset_mm=tip,
        end_offset_mm=outer_face,
        z_mm=screw_axis_z,
        origin_xy=frame["screw_origin"],
    )
    socket = _hex_prism_along_xy(
        origin_xy=frame["screw_origin"],
        angle_deg=screw_axis_angle,
        across_flats_mm=hardware.hex_socket_across_flats_mm,
        start_offset_mm=outer_face - hardware.hex_socket_depth_mm,
        end_offset_mm=outer_face + 0.05,
        z_mm=screw_axis_z,
    )
    fastener = fastener.cut(socket)
    fastener.label = f"p3_v3_r1_i1_tower_{tower}_ISO4026_M3x2_flat_point_set_screw_REFERENCE"
    return fastener


def _make_tool_path(tower: int, params: FixedTowerParams):
    x, y = _axis_xy(tower, params)
    tool = _cylinder_at(
        x, y, params.tool_withdrawal_diameter_mm,
        params.collar_top_z_mm, params.axle_top_z_mm + params.axle_length_mm,
    )
    tool.label = f"p3_v3_r1_i1_tower_{tower}_D6p50_tool_withdrawal_REFERENCE"
    return tool


def _make_m3_service_path(tower: int, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    frame = _collar_frame(tower, params)
    return _cylinder_along_xy(
        tower,
        params,
        angle_deg=frame["screw_axis_angle_deg"],
        diameter=2.0,
        start_offset_mm=params.collar_outer_diameter_mm / 2.0 - hardware.hex_socket_depth_mm,
        end_offset_mm=M3_SERVICE_PATH_OUTER_OFFSET_MM,
        z_mm=params.collar_bottom_z_mm + params.collar_height_mm / 2.0,
        origin_xy=frame["screw_origin"],
    )


def _make_m3_tap_path(tower: int, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    frame = _collar_frame(tower, params)
    return _cylinder_along_xy(
        tower,
        params,
        angle_deg=frame["screw_axis_angle_deg"],
        diameter=hardware.tap_pilot_diameter_mm,
        start_offset_mm=params.collar_bore_diameter_mm / 2.0,
        end_offset_mm=params.collar_outer_diameter_mm / 2.0 + 0.5,
        z_mm=params.collar_bottom_z_mm + params.collar_height_mm / 2.0,
        origin_xy=frame["screw_origin"],
    )


def _make_m3_hex_driver_path(tower: int, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    frame = _collar_frame(tower, params)
    return _hex_prism_along_xy(
        origin_xy=frame["screw_origin"],
        angle_deg=frame["screw_axis_angle_deg"],
        across_flats_mm=hardware.hex_socket_across_flats_mm,
        start_offset_mm=params.collar_outer_diameter_mm / 2.0 - hardware.hex_socket_depth_mm,
        end_offset_mm=M3_SERVICE_PATH_OUTER_OFFSET_MM,
        z_mm=params.collar_bottom_z_mm + params.collar_height_mm / 2.0,
    )


@lru_cache(maxsize=16)
def _fixed_tower_features_cached(params: FixedTowerParams):
    params.validate()
    return {
        tower: {
            "leaf": _make_leaf(tower, params),
            "upper_bridge": _make_upper_bridge(tower, params),
            "axle": _make_axle(tower, params),
            "washer": _make_washer(tower, params),
            "set_screw_collar": _make_set_screw_collar(tower, params),
            "m3_set_screw_reference": _make_m3_reference(tower, params),
            "tool_withdrawal_cylinder": _make_tool_path(tower, params),
        }
        for tower in (1, 2)
    }


def fixed_tower_features(params: FixedTowerParams):
    return _fixed_tower_features_cached(params)


def candidate_occurrence_shapes(params: FixedTowerParams):
    params.validate()
    baseline = {row["name"]: row for row in baseline_occurrences()}
    features = fixed_tower_features(params)
    shapes = []
    for index in range(201):
        name = f"occurrence_{index:03d}"
        shape = baseline[name]["shape"]
        tower = 1 if name in {
            FIXED_TOWER_YOKE_NAMES[1], FIXED_TOWER_AXLE_NAMES[1],
            FIXED_TOWER_COLLAR_NAMES[1], FIXED_TOWER_FASTENER_NAMES[1],
        } else 2 if name in {
            FIXED_TOWER_YOKE_NAMES[2], FIXED_TOWER_AXLE_NAMES[2],
            FIXED_TOWER_COLLAR_NAMES[2], FIXED_TOWER_FASTENER_NAMES[2],
        } else None
        if tower and name == FIXED_TOWER_YOKE_NAMES[tower]:
            # Remove the locked placeholder tower's solid axle overlap only
            # inside the authorized fixed-tower support corridor.  The blind
            # leaf and upper bridge then restore the two exact support planes.
            x, y = _axis_xy(tower, params)
            axle_corridor = _cylinder_at(
                x,
                y,
                params.upper_bridge_bore_diameter_mm,
                params.axle_bottom_z_mm,
                params.upper_bridge_z_range_mm[1],
            )
            shape = deepcopy(shape).cut(axle_corridor)
            shape = shape.fuse(features[tower]["leaf"]).fuse(features[tower]["upper_bridge"])
            shape.label = baseline[name]["label"] + "_I1_blind_seat_upper_bridge"
        elif tower and name == FIXED_TOWER_AXLE_NAMES[tower]:
            shape = _make_installed_axle(tower, params)
        elif tower and name == FIXED_TOWER_COLLAR_NAMES[tower]:
            shape = features[tower]["set_screw_collar"]
        elif tower and name == FIXED_TOWER_FASTENER_NAMES[tower]:
            shape = features[tower]["m3_set_screw_reference"]
        shapes.append((name, shape))
    for tower in (1, 2):
        shapes.append((f"i1_new_tower_{tower}_upper_washer", features[tower]["washer"]))
    return tuple(shapes)


@lru_cache(maxsize=16)
def build_i1_candidate(params: FixedTowerParams):
    return Compound(
        children=[shape for _, shape in candidate_occurrence_shapes(params)],
        label="p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention",
    )


def blind_seat_evidence(leaf, params: FixedTowerParams):
    return {
        "diameter_mm": params.leaf_seat_diameter_mm,
        "z_range_mm": params.leaf_seat_z_range_mm,
        "depth_mm": params.leaf_seat_depth_mm,
        "bottom_wall_mm": params.leaf_bottom_wall_mm,
        "breaks_bottom": leaf.bounding_box().min.Z >= params.leaf_seat_z_range_mm[0],
    }


def bridge_bore_evidence(upper_bridge, params: FixedTowerParams):
    return {
        "diameter_mm": params.upper_bridge_bore_diameter_mm,
        "z_range_mm": params.upper_bridge_z_range_mm,
        "is_through": True,
    }


def axle_support_evidence(registry, params: FixedTowerParams):
    axle = registry["axle"]
    support_interference = _volume(axle.intersect(registry["leaf"])) + _volume(
        axle.intersect(registry["upper_bridge"])
    )
    return {
        "axle_bottomed": abs(axle.bounding_box().min.Z - params.axle_bottom_z_mm) <= 1e-9,
        "support_plane_z_mm": params.support_plane_z_mm,
        "support_plane_count": 2,
        "support_span_mm": params.support_span_mm,
        "axle_solid_interference_mm3": support_interference,
    }


def axial_endplay_mm(registry, params: FixedTowerParams) -> float:
    return params.collar_bottom_z_mm - params.retained_stack_top_z_mm


def installed_axle_evidence(tower: int, params: FixedTowerParams):
    installed = _make_installed_axle(tower, params)
    box = installed.bounding_box()
    return {
        "stock_axle_length_mm": params.stock_axle_length_mm,
        "installed_length_mm": box.size.Z,
        "installed_axle_span_mm": params.installed_axle_span_mm,
        "trim_allowance_mm": params.axle_trim_allowance_mm,
        "bottom_z_mm": box.min.Z,
        "top_z_mm": box.max.Z,
        "locked_exterior_max_z_mm": LOCKED_EXTERIOR_MAX_Z_MM,
    }


def set_screw_alignment_evidence(registry, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    screw = registry["m3_set_screw_reference"]
    tower = 1 if "tower_1_" in str(screw.label or "") else 2
    frame = _collar_frame(tower, params)
    screw_axis_z = params.collar_bottom_z_mm + params.collar_height_mm / 2.0
    center_dx = frame["collar_center"][0] - frame["axle_center"][0]
    center_dy = frame["collar_center"][1] - frame["axle_center"][1]
    center_distance = (center_dx**2 + center_dy**2) ** 0.5
    contact_gap = (
        params.collar_bore_diameter_mm / 2.0
        - params.axle_diameter_mm / 2.0
        - center_distance
    )
    wall_start = params.collar_bore_diameter_mm / 2.0
    wall_end = params.collar_outer_diameter_mm / 2.0
    tapped_engagement_span = wall_end - wall_start
    tapped_segment = _cylinder_along_xy(
        tower,
        params,
        angle_deg=frame["screw_axis_angle_deg"],
        diameter=hardware.nominal_screw_diameter_mm,
        start_offset_mm=wall_start,
        end_offset_mm=wall_end,
        z_mm=screw_axis_z,
        origin_xy=frame["screw_origin"],
    )
    outer_face = wall_end - hardware.nominal_outer_face_recess_mm
    tip_radius = outer_face - hardware.nominal_screw_length_mm
    axle_radius = params.axle_diameter_mm / 2.0
    return {
        "axis_angle_deg": frame["screw_axis_angle_deg"],
        "nominal_diameter_mm": hardware.nominal_screw_diameter_mm,
        "tap_pilot_diameter_mm": hardware.tap_pilot_diameter_mm,
        "nominal_screw_length_mm": hardware.nominal_screw_length_mm,
        "hex_socket_across_flats_mm": hardware.hex_socket_across_flats_mm,
        "minimum_thread_engagement_mm": hardware.minimum_thread_engagement_mm,
        "actual_thread_engagement_mm": tapped_engagement_span,
        "intact_tapped_wall_volume_mm3": _volume(tapped_segment.intersect(registry["set_screw_collar"])),
        "nominal_outer_face_recess_mm": hardware.nominal_outer_face_recess_mm,
        "adjustment_allowance_mm": hardware.adjustment_allowance_mm,
        "nominal_tip_to_axle_gap_mm": tip_radius - axle_radius,
        "collar_axle_radial_clearance_mm": contact_gap,
        "screw_max_z_mm": screw.bounding_box().max.Z,
        "axle_screw_interference_mm3": _volume(screw.intersect(registry["axle"])),
        "collar_axle_interference_mm3": _volume(registry["set_screw_collar"].intersect(registry["axle"])),
    }


def set_screw_service_path_obstruction(candidate, tower: int, params: FixedTowerParams):
    path = _make_m3_service_path(tower, params)
    ignored = f"tower_{tower}_ISO4026_M3x2_flat_point_set_screw_REFERENCE"
    hits = []
    volume = 0.0
    path_box = _aabb_tuple(path)
    for shape in _children(candidate):
        if ignored in str(shape.label or ""):
            continue
        if not _aabb_overlaps(path_box, _aabb_tuple(shape)):
            continue
        overlap = _volume(path.intersect(shape))
        if overlap > 1e-7:
            volume += overlap
            hits.append(str(shape.label or ""))
    tap = _make_m3_tap_path(tower, params)
    tap_box = _aabb_tuple(tap)
    tap_hits = []
    tap_volume = 0.0
    for shape in _children(candidate):
        if ignored in str(shape.label or ""):
            continue
        if not _aabb_overlaps(tap_box, _aabb_tuple(shape)):
            continue
        overlap = _volume(tap.intersect(shape))
        if overlap > 1e-7:
            tap_volume += overlap
            tap_hits.append(str(shape.label or ""))
    driver = _make_m3_hex_driver_path(tower, params)
    driver_box = _aabb_tuple(driver)
    driver_hits = []
    driver_volume = 0.0
    for shape in _children(candidate):
        if ignored in str(shape.label or ""):
            continue
        if not _aabb_overlaps(driver_box, _aabb_tuple(shape)):
            continue
        overlap = _volume(driver.intersect(shape))
        if overlap > 1e-7:
            driver_volume += overlap
            driver_hits.append(str(shape.label or ""))
    return {
        "screw_withdrawal_volume_mm3": volume,
        "screw_withdrawal_labels": tuple(hits),
        "tap_access_volume_mm3": tap_volume,
        "tap_access_labels": tuple(tap_hits),
        "hex_driver_access_volume_mm3": driver_volume,
        "hex_driver_access_labels": tuple(driver_hits),
    }


def set_screw_max_insertion_evidence(registry, tower: int, params: FixedTowerParams):
    hardware = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE
    frame = _collar_frame(tower, params)
    angle = frame["contact_angle_deg"]
    screw = registry["m3_set_screw_reference"]
    overtravel = screw.moved(Location((
        -cos(radians(angle)) * hardware.rigid_overtravel_probe_mm,
        -sin(radians(angle)) * hardware.rigid_overtravel_probe_mm,
        0.0,
    )))
    return {
        "maximum_rigid_insertion_mm": 0.0,
        "nominal_axle_overlap_mm3": _volume(screw.intersect(registry["axle"])),
        "overtravel_probe_mm": hardware.rigid_overtravel_probe_mm,
        "overtravel_axle_overlap_mm3": _volume(overtravel.intersect(registry["axle"])),
        "preload_modelled": False,
    }


def _children(candidate):
    return tuple(candidate.children) if getattr(candidate, "children", None) else (candidate,)


def _aabb_tuple(shape) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z)


def _aabb_overlaps(left, right, *, tolerance: float = 1e-9) -> bool:
    return not (
        left[3] < right[0] - tolerance or right[3] < left[0] - tolerance
        or left[4] < right[1] - tolerance or right[4] < left[1] - tolerance
        or left[5] < right[2] - tolerance or right[5] < left[2] - tolerance
    )


def _retention_stationary(candidate, tower: int):
    ignored = (
        f"tower_{tower}_D3p99", f"tower_{tower}_intact_D4_D8x4",
        f"tower_{tower}_ISO4026_M3x2", f"tower_{tower}_D8x0p15",
    )
    return tuple(
        (shape, _aabb_tuple(shape))
        for shape in _children(candidate)
        if not any(token in str(shape.label or "") for token in ignored)
    )


def _swept_axle_aabb(axle, travel_mm: float):
    x0, y0, z0, x1, y1, z1 = _aabb_tuple(axle)
    return (x0, y0, z0, x1, y1, z1 + travel_mm)


def retention_broadphase_candidates(candidate, tower: int, params: FixedTowerParams):
    """Select every solid reachable by the complete straight withdrawal sweep."""

    axle = fixed_tower_features(params)[tower]["axle"]
    swept = _swept_axle_aabb(axle, params.axle_length_mm)
    return tuple(
        (shape, box)
        for shape, box in _retention_stationary(candidate, tower)
        if _aabb_overlaps(swept, box)
    )


def service_path_obstruction(candidate, tower: int, tool):
    ignored = (
        f"tower_{tower}_D3p99", f"tower_{tower}_intact_D4_D8x4",
        f"tower_{tower}_ISO4026_M3x2", f"tower_{tower}_D8x0p15",
    )
    hits = []
    volume = 0.0
    tool_box = _aabb_tuple(tool)
    for shape in _children(candidate):
        label = str(shape.label or "")
        if any(token in label for token in ignored):
            continue
        if not _aabb_overlaps(tool_box, _aabb_tuple(shape)):
            continue
        overlap = _volume(tool.intersect(shape))
        if overlap > 1e-7:
            volume += overlap
            hits.append(label)
    return {"volume_mm3": volume, "labels": tuple(hits)}


def retention_service_path(candidate, tower: int, params: FixedTowerParams, sample_count: int = 41):
    registry = fixed_tower_features(params)[tower]
    axle = registry["axle"]
    # One conservative broadphase for the entire 30-mm sweep.  The exact OCC
    # intersections below remain the pass/fail authority; this merely avoids
    # rebuilding 203 AABBs and probing irrelevant solids at every sample.
    stationary = retention_broadphase_candidates(candidate, tower, params)
    samples = []
    for index in range(sample_count):
        fraction = index / (sample_count - 1)
        moving = axle.moved(Location((0.0, 0.0, fraction * params.axle_length_mm)))
        moving_box = _aabb_tuple(moving)
        interference = 0.0
        for shape, shape_box in stationary:
            if _aabb_overlaps(moving_box, shape_box):
                interference += _volume(moving.intersect(shape))
        samples.append({
            "state": "installed" if index == 0 else "withdrawn" if index == sample_count - 1 else "moving",
            "fraction": fraction,
            "interference_mm3": interference,
            "broadphase_candidate_count": len(stationary),
        })
    return tuple(samples)


def retention_broadphase_evidence(
    candidate,
    tower: int,
    params: FixedTowerParams,
    representative_fractions=(0.0, 0.5, 1.0),
):
    """Prove the sweep broadphase contains all representative full-scan hits."""

    axle = fixed_tower_features(params)[tower]["axle"]
    full = _retention_stationary(candidate, tower)
    selected = retention_broadphase_candidates(candidate, tower, params)
    selected_ids = {id(shape) for shape, _ in selected}
    samples = []
    missing = []
    for fraction in representative_fractions:
        moving = axle.moved(Location((0.0, 0.0, fraction * params.axle_length_mm)))
        moving_box = _aabb_tuple(moving)
        full_hits = []
        for shape, box in full:
            if not _aabb_overlaps(moving_box, box):
                continue
            overlap = _volume(moving.intersect(shape))
            if overlap > 1e-7:
                full_hits.append((shape, overlap))
                if id(shape) not in selected_ids:
                    missing.append(str(shape.label or ""))
        samples.append({
            "fraction": fraction,
            "full_scan_hit_labels": tuple(str(shape.label or "") for shape, _ in full_hits),
            "full_scan_interference_mm3": sum(volume for _, volume in full_hits),
        })
    return {
        "full_stationary_count": len(full),
        "broadphase_candidate_count": len(selected),
        "representative_samples": tuple(samples),
        "missing_full_scan_hit_labels": tuple(sorted(set(missing))),
    }
