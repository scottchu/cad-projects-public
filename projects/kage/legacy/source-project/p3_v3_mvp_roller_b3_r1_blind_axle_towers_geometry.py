"""BREP geometry for B3-R1 C-bar towers, rollers, rings, and hardware witnesses."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location

import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1
import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as b2
from p3_v3_mvp_roller_b3_r1_blind_axle_towers_spec import NAMESPACE, SPEC


P = SPEC.purchased
R = SPEC.ring


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    if left is None or right is None:
        return 0.0
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def _one(shape, label: str):
    solids = list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    if not result.is_valid or result.volume <= 0:
        raise RuntimeError(f"{label} must be a valid positive-volume solid")
    result.label = label
    return result


def local_point(angle_deg: float, radius_mm: float, tangent_mm: float = 0.0) -> tuple[float, float]:
    a = radians(angle_deg)
    return (
        radius_mm*cos(a)-tangent_mm*sin(a),
        radius_mm*sin(a)+tangent_mm*cos(a),
    )


def local_box(angle: float, r0: float, r1: float, t0: float, t1: float, z0: float, height: float):
    return Box(r1-r0, t1-t0, height, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((r0, t0, z0))
    ).rotate(Axis.Z, angle)


def vertical_cylinder(angle: float, radius: float, tangent: float, diameter: float, z0: float, height: float):
    x, y = local_point(angle, radius, tangent)
    return Cylinder(diameter/2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))


def annulus(radius_outer: float, radius_inner: float, z0: float, height: float):
    return _one(
        Cylinder(radius_outer, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0))).cut(
            Cylinder(radius_inner, height+0.1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0-0.05)))
        ),
        f"{NAMESPACE}_annulus",
    )


def role_index(role: str) -> int:
    if role not in R.role_names:
        raise ValueError(f"unknown role {role!r}")
    return R.role_names.index(role)


def landing_radius(angle: float) -> float:
    return SPEC.spine_landing_radius_mm if abs(angle-300.0) <= 1e-9 else SPEC.axle_radius_mm


@lru_cache(maxsize=None)
def tower_shape(angle_deg: float):
    if angle_deg not in SPEC.tower_angles_deg:
        raise ValueError("tower angle must be 60, 180, or 300 degrees")
    bottom_z0, bottom_z1 = SPEC.bottom_arm_z_mm
    top_z0, top_z1 = SPEC.top_arm_z_mm
    r0, r1 = SPEC.cbar_radial_mm
    if angle_deg == 300.0:
        bottom_r0 = SPEC.spine_landing_radius_mm-4.0
    else:
        bottom_r0 = r0-2.0
    bottom = local_box(
        0.0, bottom_r0, r1,
        SPEC.cbar_tangential_mm[0], SPEC.cbar_tangential_mm[1],
        bottom_z0, bottom_z1-bottom_z0,
    )
    top = local_box(
        0.0, r0, r1,
        SPEC.cbar_tangential_mm[0], SPEC.cbar_tangential_mm[1],
        top_z0, top_z1-top_z0,
    )
    side = local_box(
        0.0, r0, r1,
        SPEC.side_web_tangential_mm[0], SPEC.side_web_tangential_mm[1],
        bottom_z1-0.1, top_z0-bottom_z1+0.2,
    )
    axle_pocket = vertical_cylinder(
        0.0, SPEC.axle_radius_mm, 0.0,
        SPEC.blind_axle_pocket_diameter_mm,
        SPEC.blind_axle_pocket_z_mm[0],
        SPEC.blind_axle_pocket_z_mm[1]-SPEC.blind_axle_pocket_z_mm[0]+0.05,
    )
    top_bore = vertical_cylinder(
        0.0, SPEC.axle_radius_mm, 0.0,
        SPEC.top_axle_bore_diameter_mm,
        top_z0-0.05, top_z1-top_z0+0.1,
    )
    nut_pocket = b1._hex_prism(
        0.0, SPEC.axle_radius_mm, 0.0,
        P.top_nut_pocket_af_mm,
        SPEC.top_nut_pocket_z_mm[0],
        SPEC.top_nut_pocket_z_mm[1]-SPEC.top_nut_pocket_z_mm[0],
        30.0,
    )
    nut_slot = local_box(
        0.0,
        SPEC.axle_radius_mm-P.top_nut_pocket_af_mm/2.0-0.1,
        SPEC.axle_radius_mm+P.top_nut_pocket_af_mm/2.0+0.1,
        SPEC.cbar_tangential_mm[0]-0.1,
        0.0,
        SPEC.top_nut_pocket_z_mm[0],
        SPEC.top_nut_pocket_z_mm[1]-SPEC.top_nut_pocket_z_mm[0],
    )
    mount_radius = landing_radius(angle_deg)
    mount_bores = tuple(
        vertical_cylinder(
            0.0, mount_radius, tangent,
            SPEC.lower_mount_bore_diameter_mm,
            bottom_z0-0.05, bottom_z1-bottom_z0+0.1,
        )
        for tangent in SPEC.mount_axis_tangent_mm
    )
    radial_overflow = Cylinder(
        SPEC.tower_max_radius_mm+100.0,
        top_z1-bottom_z0+2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).cut(
        Cylinder(
            SPEC.tower_max_radius_mm,
            top_z1-bottom_z0+2.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((0, 0, -0.1)))
    ).moved(Location((0, 0, bottom_z0-1.0)))
    tower = _one(
        bottom.fuse(top, side).cut(
            radial_overflow, axle_pocket, top_bore, nut_pocket, nut_slot, *mount_bores
        ),
        f"{NAMESPACE}_printed_C_bar_A{angle_deg:03.0f}",
    ).rotate(Axis.Z, angle_deg)
    tower.label = f"{NAMESPACE}_printed_C_bar_A{angle_deg:03.0f}"
    return tower


def _roller_local(role: str):
    index = role_index(role)
    center = R.role_centers_z_mm[index]
    roller_z0, roller_z1 = SPEC.roller_z_mm[index]
    carrier_z0, carrier_z1 = R.complete_carrier_z_mm[index]
    tooth_z0, tooth_z1 = R.tooth_face_z_mm[index]
    groove_z0 = center-SPEC.roller_groove_width_mm/2.0
    groove_z1 = center+SPEC.roller_groove_width_mm/2.0
    pieces = (
        Cylinder(SPEC.roller_outer_diameter_mm/2.0, SPEC.roller_flange_thickness_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,roller_z0))),
        Cylinder(SPEC.roller_guide_radius_mm, tooth_z0-groove_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,groove_z0))),
        Cylinder(SPEC.roller_tooth_relief_radius_mm, tooth_z1-tooth_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,tooth_z0))),
        Cylinder(SPEC.roller_guide_radius_mm, groove_z1-tooth_z1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,tooth_z1))),
        Cylinder(SPEC.roller_outer_diameter_mm/2.0, SPEC.roller_flange_thickness_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,groove_z1))),
    )
    roller = pieces[0].fuse(*pieces[1:])
    pocket = Cylinder(
        P.bearing_pocket_diameter_mm/2.0,
        P.bearing_pocket_depth_mm+0.02,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0,0,roller_z0-0.01)))
    bore = Cylinder(
        SPEC.roller_axle_bore_diameter_mm/2.0,
        roller_z1-roller_z0+0.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0,0,roller_z0-0.1)))
    return _one(roller.cut(pocket, bore), f"{NAMESPACE}_{role}_printed_roller")


def roller_shape(role: str, angle_deg: float, radius_mm: float = SPEC.axle_radius_mm):
    shape = deepcopy(_roller_local(role)).moved(Location((radius_mm, 0.0, 0.0))).rotate(Axis.Z, angle_deg)
    shape.label = f"{NAMESPACE}_{role}_printed_roller_A{angle_deg:03.0f}_R{radius_mm:.2f}"
    return shape


def bearing_witness(role: str, angle_deg: float, radius_mm: float = SPEC.axle_radius_mm):
    index = role_index(role)
    z0 = SPEC.roller_z_mm[index][0]+0.05
    outer = vertical_cylinder(angle_deg, radius_mm, 0.0, P.bearing_od_mm, z0, P.bearing_width_mm)
    bore = vertical_cylinder(angle_deg, radius_mm, 0.0, P.bearing_bore_mm, z0-0.05, P.bearing_width_mm+0.1)
    shape = _one(outer.cut(bore), f"{NAMESPACE}_{role}_purchased_623ZZ_A{angle_deg:03.0f}")
    return shape


def washer_witness(index: int, angle_deg: float):
    z0, z1 = SPEC.washer_z_mm[index]
    outer = vertical_cylinder(angle_deg, SPEC.axle_radius_mm, 0.0, P.washer_od_mm, z0, z1-z0)
    bore = vertical_cylinder(angle_deg, SPEC.axle_radius_mm, 0.0, P.washer_id_mm, z0-0.05, z1-z0+0.1)
    return _one(outer.cut(bore), f"{NAMESPACE}_purchased_M3_washer_{index+1}_A{angle_deg:03.0f}")


def axle_witness(angle_deg: float):
    shaft = vertical_cylinder(
        angle_deg, SPEC.axle_radius_mm, 0.0,
        P.axle_diameter_mm, SPEC.axle_tip_z_mm, P.axle_length_mm,
    )
    head = vertical_cylinder(
        angle_deg, SPEC.axle_radius_mm, 0.0,
        P.axle_head_diameter_mm, SPEC.axle_under_head_z_mm, P.axle_head_height_mm,
    )
    return _one(shaft.fuse(head), f"{NAMESPACE}_purchased_M3x25_blind_axle_A{angle_deg:03.0f}")


def top_nut_witness(angle_deg: float):
    shape = b1._hex_prism(
        angle_deg, SPEC.axle_radius_mm, 0.0,
        P.top_nut_af_mm,
        SPEC.top_nut_pocket_z_mm[1]-P.top_nut_thickness_mm,
        P.top_nut_thickness_mm,
        30.0,
    )
    return _one(shape, f"{NAMESPACE}_purchased_top_AF5p5_nut_A{angle_deg:03.0f}")


def ring_witness(role: str):
    index = role_index(role)
    z0, z1 = R.complete_carrier_z_mm[index]
    tooth_z0, tooth_z1 = R.tooth_face_z_mm[index]
    body = annulus(R.body_outer_radius_mm, R.race_radius_mm, z0, z1-z0)
    tooth_band = annulus(R.race_radius_mm, R.tooth_tip_radius_mm, tooth_z0, tooth_z1-tooth_z0)
    shape = _one(body.fuse(tooth_band), f"{NAMESPACE}_{role}_nonprint_ring_witness")
    return shape


def fin_sweep_witness(role: str):
    index = role_index(role)
    z0, z1 = R.complete_carrier_z_mm[index]
    shape = annulus(R.fin_sweep_radius_mm[1], R.fin_sweep_radius_mm[0], z0, z1-z0)
    shape.label = f"{NAMESPACE}_{role}_nonprint_360_fin_sweep"
    return shape


def hall_keepout_witness(angle_deg: float):
    r0, r1 = SPEC.hall_keepout_radial_mm
    tangent = r1*sin(radians(SPEC.hall_keepout_half_angle_deg))
    z0, z1 = SPEC.hall_keepout_z_mm
    shape = local_box(angle_deg, r0, r1, -tangent, tangent, z0, z1-z0)
    shape.label = f"{NAMESPACE}_Hall_keepout_REFERENCE_A{angle_deg:03.0f}"
    return shape


def topology_clean_b2_input_bevel_witness(angle_deg: float, q_mm: float):
    """Rebuild the inherited purchased bevel without its tangent boolean seam.

    B2 subtracts the bore before fusing the tooth lug.  The lug starts exactly
    on the bore radius, so the rotated 240-degree occurrence can acquire a
    self-intersection when exported again inside B3.  Fusing the unchanged
    outer envelopes first and subtracting the unchanged bore last is the same
    intended solid with stable STEP topology.
    """
    hub_length = 2.50
    outer = b2.radial_cylinder(
        angle_deg,
        b2.SPEC.input_bevel_rear_radius_nominal_mm+q_mm,
        0.0,
        b2.SPEC.motor_input_axis_z_mm,
        6.0,
        hub_length,
    )
    bore = b2.radial_cylinder(
        angle_deg,
        b2.SPEC.input_bevel_rear_radius_nominal_mm+q_mm-0.05,
        0.0,
        b2.SPEC.motor_input_axis_z_mm,
        b2.P.spur_bore_diameter_mm,
        hub_length+0.1,
    )
    tooth_lug = b2.local_box(
        angle_deg,
        b2.SPEC.input_bevel_rear_radius_nominal_mm+q_mm+hub_length-0.1,
        b2.SPEC.input_bevel_front_radius_nominal_mm+q_mm,
        2.05,
        2.50,
        b2.SPEC.motor_input_axis_z_mm-0.4,
        0.8,
    )
    return _one(
        outer.fuse(tooth_lug).cut(bore),
        f"{b2.NAMESPACE}_purchased_input_bevel_1to1",
    )


def inherited_b2_children_with_clean_input_bevels(q_mm: float = 0.0) -> tuple:
    """Copy B2 verbatim except for its three topology-clean bevel witnesses."""
    children = []
    bevel_angles = iter(b2.SPEC.station_angles_deg)
    replacement_count = 0
    bevel_label = f"{b2.NAMESPACE}_purchased_input_bevel_1to1"
    for child in b2.assembled_shape(q_mm).children:
        if child.label == bevel_label:
            children.append(
                topology_clean_b2_input_bevel_witness(next(bevel_angles), q_mm)
            )
            replacement_count += 1
        else:
            children.append(deepcopy(child))
    if replacement_count != len(b2.SPEC.station_angles_deg):
        raise RuntimeError(
            f"expected {len(b2.SPEC.station_angles_deg)} inherited input bevels, "
            f"replaced {replacement_count}"
        )
    return tuple(children)


def mount_hardware_witnesses(angle_deg: float) -> tuple:
    radius = landing_radius(angle_deg)
    rows = []
    for tangent in SPEC.mount_axis_tangent_mm:
        shaft = vertical_cylinder(
            angle_deg, radius, tangent,
            P.tower_mount_screw_diameter_mm,
            SPEC.bottom_arm_z_mm[0]-P.tower_mount_screw_length_mm+SPEC.bottom_arm_z_mm[1]-SPEC.bottom_arm_z_mm[0],
            P.tower_mount_screw_length_mm,
        )
        shaft.label = f"{NAMESPACE}_purchased_M3x8_tower_mount_A{angle_deg:03.0f}_T{tangent:+.0f}"
        rows.append(shaft)
    return tuple(rows)


def tower_station_children(angle_deg: float) -> tuple:
    rows = [tower_shape(angle_deg)]
    for role in R.role_names:
        rows.extend((roller_shape(role, angle_deg), bearing_witness(role, angle_deg)))
    rows.extend(washer_witness(index, angle_deg) for index in range(len(SPEC.washer_z_mm)))
    rows.extend((axle_witness(angle_deg), top_nut_witness(angle_deg)))
    rows.extend(mount_hardware_witnesses(angle_deg))
    return tuple(rows)


def assembled_shape(q_mm: float = 0.0):
    children = list(inherited_b2_children_with_clean_input_bevels(q_mm))
    fixed_180 = b1.fixed_riser_shape(180.0)
    fixed_180.label = f"{NAMESPACE}_reused_B1_fixed_riser_A180"
    children.append(fixed_180)
    for angle in SPEC.tower_angles_deg:
        children.extend(tower_station_children(angle))
    children.extend(ring_witness(role) for role in R.role_names)
    return Compound(children=children, label=f"{NAMESPACE}_assembled_q{q_mm:+.2f}")


def exploded_assembly_order_shape():
    children = [
        child.moved(Location((0,0,-20)))
        for child in inherited_b2_children_with_clean_input_bevels()
    ]
    fixed_180 = b1.fixed_riser_shape(180.0).moved(Location((0,0,20)))
    fixed_180.label = f"{NAMESPACE}_step_01_reuse_fixed_riser_A180"
    children.append(fixed_180)
    for tower_index, angle in enumerate(SPEC.tower_angles_deg):
        dx, dy = local_point(angle, 30.0)
        tower = tower_shape(angle).moved(Location((dx,dy,25+tower_index*8)))
        tower.label = f"{NAMESPACE}_step_02_mount_empty_C_bar_A{angle:03.0f}"
        children.append(tower)
        for role_index_value, role in enumerate(R.role_names):
            ring = ring_witness(role).moved(Location((0,0,12+role_index_value*5)))
            ring.label = f"{NAMESPACE}_step_03_lower_{role}_ring_witness"
            children.append(ring)
            roller = roller_shape(role, angle, SPEC.axle_radius_mm-24.0).moved(Location((dx,dy,34+tower_index*8)))
            roller.label = f"{NAMESPACE}_step_04_insert_{role}_roller_center_outward_A{angle:03.0f}"
            children.append(roller)
        for washer_index in range(len(SPEC.washer_z_mm)):
            washer = washer_witness(washer_index, angle).moved(Location((dx,dy,52+washer_index*3+tower_index*8)))
            washer.label = f"{NAMESPACE}_step_05_washer_{washer_index+1}_A{angle:03.0f}"
            children.append(washer)
        axle = axle_witness(angle).moved(Location((dx,dy,72+tower_index*8)))
        axle.label = f"{NAMESPACE}_step_06_axle_top_down_A{angle:03.0f}"
        children.append(axle)
    return Compound(children=children, label=f"{NAMESPACE}_exploded_assembly_order")


def printable_occurrences() -> tuple[dict[str, object], ...]:
    rows = [dict(row) for row in b2.printable_occurrences()]
    duplicate = b1.fixed_riser_shape()
    duplicate.label = f"{NAMESPACE}_second_reusable_fixed_riser_print_orientation"
    rows.append({"name":"second_reusable_fixed_riser", "shape":duplicate.moved(Location((0,0,-duplicate.bounding_box().min.Z))), "orientation":"minimum_z_on_bed", "label":duplicate.label})
    for angle in SPEC.tower_angles_deg:
        shape = tower_shape(angle).moved(Location((0,0,-tower_shape(angle).bounding_box().min.Z)))
        shape.label = f"{NAMESPACE}_C_bar_A{angle:03.0f}_print_orientation"
        rows.append({"name":f"C_bar_A{angle:03.0f}", "shape":shape, "orientation":"minimum_z_on_bed", "label":shape.label})
    for angle in SPEC.tower_angles_deg:
        for role in R.role_names:
            shape = roller_shape(role, angle)
            shape = shape.moved(Location((0,0,-shape.bounding_box().min.Z)))
            shape.label = f"{NAMESPACE}_{role}_roller_A{angle:03.0f}_print_orientation"
            rows.append({"name":f"{role}_roller_A{angle:03.0f}", "shape":shape, "orientation":"minimum_z_on_bed", "label":shape.label})
    return tuple(rows)


def printed_additions_shape():
    children = [tower_shape(angle) for angle in SPEC.tower_angles_deg]
    children.extend(roller_shape(role, angle) for angle in SPEC.tower_angles_deg for role in R.role_names)
    return Compound(children=children, label=f"{NAMESPACE}_printed_additions")
