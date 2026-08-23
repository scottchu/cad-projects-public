"""Actual-BREP geometry for the one-solid B6-R0 electronics backbone MVP."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as r4_geometry
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1_geometry
import p3_v3_mvp_drive_b2_r2_outward_face_plate_role_stations_geometry as b2_geometry
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3_geometry
import p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_geometry as b5a_geometry
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_geometry as b4_geometry
import p3_v3_mvp_rings_b4_r0_segmented_fins_magnets_spec as b4_spec
import p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance_geometry as b4r2_geometry
from p3_v3_mvp_electronics_b6_r0_universal_backbone_spec import NAMESPACE, SPEC


def _one(shape, label: str):
    solids = [] if shape is None else list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be exactly one solid, got {len(solids)}")
    result = solids[0]
    if not result.is_valid or result.volume <= 0.0:
        raise RuntimeError(f"{label} must be valid with positive volume")
    result.label = label
    return result


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    if left is None or right is None:
        return 0.0
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def polar(angle_deg: float, radius_mm: float, tangent_mm: float = 0.0) -> tuple[float, float]:
    angle = radians(angle_deg)
    return (
        radius_mm * cos(angle) - tangent_mm * sin(angle),
        radius_mm * sin(angle) + tangent_mm * cos(angle),
    )


def local_box(
    angle_deg: float,
    radial_min_mm: float,
    radial_max_mm: float,
    tangent_min_mm: float,
    tangent_max_mm: float,
    z0_mm: float,
    height_mm: float,
):
    return Box(
        radial_max_mm - radial_min_mm,
        tangent_max_mm - tangent_min_mm,
        height_mm,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((radial_min_mm, tangent_min_mm, z0_mm))).rotate(Axis.Z, angle_deg)


def vertical_cylinder(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    diameter_mm: float,
    z0_mm: float,
    height_mm: float,
):
    x, y = polar(angle_deg, radius_mm, tangent_mm)
    return Cylinder(
        diameter_mm / 2.0,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0_mm)))


def annulus(radial_min_mm: float, radial_max_mm: float, z0_mm: float, height_mm: float):
    outer = Cylinder(radial_max_mm, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0_mm))
    )
    inner = Cylinder(radial_min_mm, height_mm + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0_mm - 0.1))
    )
    return outer.cut(inner)


def radial_capsule(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    width_mm: float,
    overall_length_mm: float,
    z0_mm: float,
    height_mm: float,
):
    center_spacing = overall_length_mm - width_mm
    bar = local_box(
        angle_deg,
        radius_mm - center_spacing / 2.0,
        radius_mm + center_spacing / 2.0,
        tangent_mm - width_mm / 2.0,
        tangent_mm + width_mm / 2.0,
        z0_mm,
        height_mm,
    )
    ends = tuple(
        vertical_cylinder(
            angle_deg,
            radius_mm + offset,
            tangent_mm,
            width_mm,
            z0_mm,
            height_mm,
        )
        for offset in (-center_spacing / 2.0, center_spacing / 2.0)
    )
    return bar.fuse(*ends)


def _hex_prism(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    across_flats_mm: float,
    z0_mm: float,
    height_mm: float,
):
    circumradius = across_flats_mm / (2.0 * cos(radians(30.0)))
    points = tuple(
        (
            radius_mm + circumradius * cos(radians(30.0 + 60.0 * vertex)),
            tangent_mm + circumradius * sin(radians(30.0 + 60.0 * vertex)),
        )
        for vertex in range(6)
    )
    return extrude(Polygon(*points), amount=height_mm).moved(Location((0.0, 0.0, z0_mm))).rotate(
        Axis.Z, angle_deg
    )


def seam_axes() -> tuple[dict[str, float], ...]:
    return tuple(
        {
            "angle_deg": angle,
            "radius_mm": radius,
            "tangent_mm": 0.0,
            "name": f"A{angle:03.0f}_R{radius:03.0f}",
        }
        for angle in SPEC.r4_seam_angles_deg
        for radius in SPEC.r4_seam_axis_radii_mm
    )


def component_layout() -> tuple[dict[str, object], ...]:
    """Replaceable envelopes; XYZ means tangential, radial, installed height."""
    return (
        {"name": "esp32_c6_touch_lcd", "angle_deg": 60.0, "radius_mm": 88.0, "tangent_mm": 0.0, "env_xyz": SPEC.esp_env_xyz, "tangent_size_mm": 50.0, "radial_size_mm": 40.0},
        {"name": "logic_buck", "angle_deg": 180.0, "radius_mm": 82.0, "tangent_mm": -25.0, "env_xyz": SPEC.logic_buck_env_xyz, "tangent_size_mm": 45.0, "radial_size_mm": 25.0},
        {"name": "led_cc_driver", "angle_deg": 180.0, "radius_mm": 82.0, "tangent_mm": 25.0, "env_xyz": SPEC.led_cc_driver_env_xyz, "tangent_size_mm": 45.0, "radial_size_mm": 25.0},
        # Rotate each 22 x 18 carrier 90 degrees in plan: 18 tangent, 22 radial.
        {"name": "tmc2209_H", "angle_deg": 300.0, "radius_mm": 79.0, "tangent_mm": -23.0, "env_xyz": SPEC.tmc_env_xyz, "tangent_size_mm": 18.0, "radial_size_mm": 22.0},
        {"name": "tmc2209_M", "angle_deg": 300.0, "radius_mm": 79.0, "tangent_mm": 0.0, "env_xyz": SPEC.tmc_env_xyz, "tangent_size_mm": 18.0, "radial_size_mm": 22.0},
        {"name": "tmc2209_S", "angle_deg": 300.0, "radius_mm": 79.0, "tangent_mm": 23.0, "env_xyz": SPEC.tmc_env_xyz, "tangent_size_mm": 18.0, "radial_size_mm": 22.0},
        {"name": "usb_c_pd_trigger", "angle_deg": 270.0, "radius_mm": 79.0, "tangent_mm": 0.0, "env_xyz": SPEC.pd_trigger_env_xyz, "tangent_size_mm": 30.0, "radial_size_mm": 20.0},
    )


def board_slot_layout() -> tuple[dict[str, object], ...]:
    rows = []
    offsets = {
        "esp32_c6_touch_lcd": (-17.5, 17.5),
        "logic_buck": (-15.0, 15.0),
        "led_cc_driver": (-15.0, 15.0),
        "tmc2209_H": (-5.0, 5.0),
        "tmc2209_M": (-5.0, 5.0),
        "tmc2209_S": (-5.0, 5.0),
        "usb_c_pd_trigger": (-10.0, 10.0),
    }
    for component in component_layout():
        tangent_width = float(component["tangent_size_mm"])
        for slot_index, offset in enumerate(offsets[str(component["name"])]):
            tangent = float(component["tangent_mm"]) + offset
            side = -1.0 if offset < 0.0 else 1.0
            rows.append(
                {
                    "name": f"{component['name']}_universal_slot_{slot_index + 1}",
                    "component": component["name"],
                    "angle_deg": component["angle_deg"],
                    "radius_mm": component["radius_mm"],
                    "tangent_mm": tangent,
                    "channel_exit_tangent_mm": float(component["tangent_mm"]) + side * (tangent_width / 2.0 + 1.0),
                }
            )
    return tuple(rows)


@lru_cache(maxsize=1)
def backbone_shape():
    z0 = SPEC.printed_underside_z_mm
    web_h = SPEC.web_thickness_mm
    pad_h = SPEC.pad_thickness_mm
    pieces = [annulus(*SPEC.inner_web_radii_mm, z0, web_h)]

    for angle, radii, tangents in (
        (SPEC.control_lobe_angle_deg, SPEC.control_lobe_radii_mm, SPEC.control_lobe_tangent_mm),
        (SPEC.power_lobe_angle_deg, SPEC.power_lobe_radii_mm, SPEC.power_lobe_tangent_mm),
        (SPEC.motion_lobe_angle_deg, SPEC.motion_lobe_radii_mm, SPEC.motion_lobe_tangent_mm),
        (SPEC.pd_input_lobe_angle_deg, SPEC.pd_input_lobe_radii_mm, SPEC.pd_input_lobe_tangent_mm),
        (SPEC.cable_arm_angle_deg, SPEC.cable_arm_radii_mm, SPEC.cable_arm_tangent_mm),
    ):
        pieces.append(local_box(angle, *radii, *tangents, z0, web_h))

    # Narrow spokes make both seam radii structural members of the same solid.
    for axis in seam_axes():
        pieces.append(
            local_box(
                float(axis["angle_deg"]),
                SPEC.inner_web_radii_mm[1] - 2.0,
                max(SPEC.r4_seam_axis_radii_mm) + SPEC.mount_pad_diameter_mm / 2.0,
                -SPEC.mount_arm_tangent_width_mm / 2.0,
                SPEC.mount_arm_tangent_width_mm / 2.0,
                z0,
                web_h,
            )
        )
        pieces.append(
            vertical_cylinder(
                float(axis["angle_deg"]),
                float(axis["radius_mm"]),
                0.0,
                SPEC.mount_pad_diameter_mm,
                z0,
                pad_h,
            )
        )

    # Four equal pips support the otherwise flat underside at the R4 top plane.
    for angle in (0.0, 90.0, 180.0, 270.0):
        pieces.append(
            vertical_cylinder(
                angle,
                74.0,
                0.0,
                SPEC.landing_pip_diameter_mm,
                SPEC.r4_plate_top_z_mm,
                SPEC.landing_pip_height_mm + 0.02,
            )
        )

    # Each universal slot has a 4 mm local pad, independent of board hole pitch.
    for slot in board_slot_layout():
        pieces.append(
            local_box(
                float(slot["angle_deg"]),
                float(slot["radius_mm"]) - SPEC.board_slot_pad_radial_mm / 2.0,
                float(slot["radius_mm"]) + SPEC.board_slot_pad_radial_mm / 2.0,
                float(slot["tangent_mm"]) - SPEC.board_slot_pad_tangent_mm / 2.0,
                float(slot["tangent_mm"]) + SPEC.board_slot_pad_tangent_mm / 2.0,
                z0,
                pad_h,
            )
        )

    # Open-top 6 x 3 mm cable-arm channel: no roof and no enclosure.
    half_gap = SPEC.open_channel_width_mm / 2.0
    rail_w = SPEC.open_channel_rail_width_mm
    for t0, t1 in ((-half_gap - rail_w, -half_gap), (half_gap, half_gap + rail_w)):
        pieces.append(
            local_box(
                SPEC.cable_arm_angle_deg,
                SPEC.cable_arm_radii_mm[0],
                SPEC.cable_arm_radii_mm[1],
                t0,
                t1,
                SPEC.printed_top_z_mm,
                SPEC.open_channel_height_mm,
            )
        )

    # Open strain-relief cheeks at the cable exit; cable ties pass through slots.
    pieces.extend(
        (
            local_box(270.0, 136.0, 143.0, -7.0, -4.5, SPEC.printed_top_z_mm, 4.0),
            local_box(270.0, 136.0, 143.0, 4.5, 7.0, SPEC.printed_top_z_mm, 4.0),
        )
    )

    body = pieces[0].fuse(*pieces[1:])

    cuts = []
    for axis in seam_axes():
        angle = float(axis["angle_deg"])
        radius = float(axis["radius_mm"])
        cuts.append(vertical_cylinder(angle, radius, 0.0, SPEC.m3_clearance_diameter_mm, z0 - 0.5, pad_h + 1.0))
        cuts.append(
            vertical_cylinder(
                angle,
                radius,
                0.0,
                SPEC.seam_counterbore_diameter_mm,
                SPEC.seam_counterbore_floor_z_mm,
                SPEC.pad_top_z_mm - SPEC.seam_counterbore_floor_z_mm + 0.5,
            )
        )

    nut_z0 = z0 + SPEC.nut_channel_bottom_floor_mm
    for slot in board_slot_layout():
        angle = float(slot["angle_deg"])
        radius = float(slot["radius_mm"])
        tangent = float(slot["tangent_mm"])
        exit_t = float(slot["channel_exit_tangent_mm"])
        cuts.append(
            radial_capsule(
                angle,
                radius,
                tangent,
                SPEC.board_slot_width_mm,
                SPEC.board_slot_overall_length_mm,
                z0 - 0.5,
                pad_h + 1.0,
            )
        )
        cuts.append(
            _hex_prism(
                angle,
                radius,
                tangent,
                SPEC.side_load_nut_channel_af_mm,
                nut_z0,
                SPEC.side_load_nut_channel_depth_mm,
            )
        )
        cuts.append(
            local_box(
                angle,
                radius - SPEC.side_load_nut_channel_af_mm / 2.0,
                radius + SPEC.side_load_nut_channel_af_mm / 2.0,
                min(tangent, exit_t),
                max(tangent, exit_t),
                nut_z0,
                SPEC.side_load_nut_channel_depth_mm,
            )
        )

    # Two open cable-tie slots leave the side rails continuous.
    for radius in (137.0, 141.0):
        cuts.append(local_box(270.0, radius - 1.0, radius + 1.0, -4.0, 4.0, z0 - 0.5, pad_h + 1.0))

    # B6-only top-edge reliefs preserve the shared A135/A225 R82 axes while
    # clearing the accepted B2 station sleds at the q=-2.5 service extreme.
    # They begin outside the R3.5 washer footprint and do not alter R4/B2.
    cuts.extend(
        (
            local_box(135.0, 77.5, 86.5, -6.0, -3.55, -22.65, 2.2),
            local_box(225.0, 77.5, 86.5, 3.55, 6.0, -22.65, 2.2),
        )
    )

    return _one(body.cut(*cuts), f"{NAMESPACE}_one_solid_PETG_backbone")


def printable_shape():
    source = deepcopy(backbone_shape())
    source = source.moved(Location((0.0, 0.0, -source.bounding_box().min.Z)))
    source.label = f"{NAMESPACE}_one_solid_flat_underside_print_orientation"
    return source


def seam_hardware_witnesses() -> tuple:
    children = []
    for axis in seam_axes():
        angle, radius = float(axis["angle_deg"]), float(axis["radius_mm"])
        shaft = vertical_cylinder(
            angle,
            radius,
            0.0,
            SPEC.seam_screw_diameter_mm,
            SPEC.seam_screw_tip_z_mm,
            SPEC.seam_screw_length_mm,
        )
        head = vertical_cylinder(
            angle,
            radius,
            0.0,
            SPEC.seam_screw_head_diameter_mm,
            SPEC.seam_screw_under_head_z_mm,
            SPEC.seam_screw_head_height_mm,
        )
        screw = _one(shaft.fuse(head), f"{NAMESPACE}_shared_M3x8_{axis['name']}")
        washer_outer = vertical_cylinder(
            angle, radius, 0.0, SPEC.seam_washer_od_mm, SPEC.seam_counterbore_floor_z_mm, SPEC.seam_washer_thickness_mm
        )
        washer_inner = vertical_cylinder(
            angle, radius, 0.0, SPEC.m3_clearance_diameter_mm, SPEC.seam_counterbore_floor_z_mm - 0.05, SPEC.seam_washer_thickness_mm + 0.1
        )
        washer = _one(washer_outer.cut(washer_inner), f"{NAMESPACE}_washer_{axis['name']}")
        children.extend((screw, washer))
    return tuple(children)


def side_load_nut_witnesses() -> tuple:
    z0 = SPEC.printed_underside_z_mm + SPEC.nut_channel_bottom_floor_mm + 0.1
    children = []
    for slot in board_slot_layout():
        nut = _one(
            _hex_prism(
                float(slot["angle_deg"]),
                float(slot["radius_mm"]),
                float(slot["tangent_mm"]),
                SPEC.ordinary_m3_nut_af_mm,
                z0,
                SPEC.ordinary_m3_nut_thickness_mm,
            ),
            f"{NAMESPACE}_ordinary_M3_side_load_nut_{slot['name']}",
        )
        children.append(nut)
    return tuple(children)


def component_envelope_witnesses() -> tuple:
    children = []
    for row in component_layout():
        height = float(row["env_xyz"][2])
        tangent = float(row["tangent_size_mm"])
        radial = float(row["radial_size_mm"])
        shape = _one(
            local_box(
                float(row["angle_deg"]),
                float(row["radius_mm"]) - radial / 2.0,
                float(row["radius_mm"]) + radial / 2.0,
                float(row["tangent_mm"]) - tangent / 2.0,
                float(row["tangent_mm"]) + tangent / 2.0,
                SPEC.pad_top_z_mm,
                height,
            ),
            f"{NAMESPACE}_REPLACEABLE_{row['name']}_envelope_heatsink_up",
        )
        children.append(shape)
    return tuple(children)


def keepout_witnesses() -> tuple:
    antenna = _one(
        local_box(60.0, 78.0, 98.0, 25.0, 25.0 + SPEC.esp_antenna_keepout_mm, SPEC.pad_top_z_mm, SPEC.installed_height_max),
        f"{NAMESPACE}_ESP_antenna_keepout_10mm",
    )
    led_x, led_y = polar(270.0, 170.0)
    heatsink = Cylinder(
        SPEC.led_heatsink_reference_diameter_mm / 2.0,
        10.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((led_x, led_y, SPEC.pad_top_z_mm)))
    heatsink = _one(heatsink, f"{NAMESPACE}_nonprint_LED_40mm_heatsink_reference")
    return antenna, heatsink


def wiring_witnesses() -> tuple:
    z0 = SPEC.printed_top_z_mm
    h = 6.0
    high_current = _one(local_box(270.0, 90.0, 143.0, -3.0, 3.0, z0, h), f"{NAMESPACE}_high_current_open_trunk")
    logic = _one(local_box(60.0, 70.0, 100.0, -3.0, 3.0, z0, h), f"{NAMESPACE}_logic_open_trunk")
    motor = _one(local_box(300.0, 70.0, 89.5, -3.0, 3.0, z0, h), f"{NAMESPACE}_motor_branch_service_loop_25mm")
    return high_current, logic, motor


def b6_assembled_occurrences() -> tuple:
    return (
        deepcopy(backbone_shape()),
        *seam_hardware_witnesses(),
        *side_load_nut_witnesses(),
        *component_envelope_witnesses(),
        *wiring_witnesses(),
        *keepout_witnesses(),
    )


def model_only_shape():
    return Compound(children=[printable_shape()], label=f"{NAMESPACE}_model_only_exactly_one_printed_object")


def _accepted_mechanism_without_r4_m3x6():
    """Compose frozen generated sources while replacing only seam screw witnesses."""
    accepted = b4r2_geometry.assembled_shape()
    return tuple(
        child
        for child in accepted.children
        if "M3x6_" not in str(child.label or "")
    )


def assembled_shape():
    children = list(_accepted_mechanism_without_r4_m3x6())
    children.extend(b5a_geometry.b5a_assembled_occurrences())
    children.extend(b6_assembled_occurrences())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_frozen_predecessors_plus_B6")


def _moved_labeled(shape, dz_mm: float, label: str):
    moved = deepcopy(shape).moved(Location((0.0, 0.0, dz_mm)))
    moved.label = f"{NAMESPACE}_{label}"
    return moved


def exploded_shape():
    """Exact requested B6-first service order; hardware/envelopes are witnesses."""
    children = []
    # 01: the unchanged R4 plate is the fixed root datum.
    for index in range(1, 5):
        children.append(_moved_labeled(r4_geometry.named_quadrant(index), -60.0, f"step_01_R4_quadrant_Q{index}"))

    # 02: backbone and the eight shared M3x8 seam screws/washers.
    children.append(_moved_labeled(backbone_shape(), -45.0, "step_02_B6_backbone_on_eight_R4_axes"))
    for index, hardware in enumerate(seam_hardware_witnesses(), 1):
        children.append(_moved_labeled(hardware, -45.0, f"step_02_shared_seam_hardware_{index:02d}"))

    # 03: ordinary M3 side-load nuts before any board/adaptor.
    for index, nut in enumerate(side_load_nut_witnesses(), 1):
        children.append(_moved_labeled(nut, -30.0, f"step_03_side_load_ordinary_M3_nut_{index:02d}"))

    # 04: replaceable board envelopes/adapters; no board-specific holes.
    for index, envelope in enumerate(component_envelope_witnesses(), 1):
        children.append(_moved_labeled(envelope, -15.0, f"step_04_replaceable_board_or_adapter_{index:02d}"))

    # 05: open wiring, strain relief, service loops, then low-voltage tests.
    for index, wire in enumerate(wiring_witnesses(), 1):
        children.append(_moved_labeled(wire, 0.0, f"step_05_open_wiring_and_low_voltage_test_{index:02d}"))

    # 06: accepted B1 removable mount pieces after B6 wiring.
    for index, part in enumerate((b1_geometry.motor_sled_shape(), b1_geometry.fixed_riser_shape(60.0), b1_geometry.spine_riser_shape()), 1):
        children.append(_moved_labeled(part, 20.0 + index * 5.0, f"step_06_B1_mount_piece_{index:02d}"))

    # 07: accepted B2 role sleds and their service-loop witnesses.
    for role, angle in zip(b2_geometry.SPEC.station_roles, b2_geometry.SPEC.station_angles_deg):
        children.append(_moved_labeled(b2_geometry.printed_station_sled(role, 0.0, angle), 45.0, f"step_07_B2_{role}_sled_and_service_loop"))

    # 08: accepted B3 fixed support and C-bar/roller additions.
    fixed_180 = b1_geometry.fixed_riser_shape(180.0)
    children.append(_moved_labeled(fixed_180, 68.0, "step_08_B3_reused_fixed_riser_A180"))
    for index, part in enumerate(b3_geometry.printed_additions_shape().children, 1):
        children.append(_moved_labeled(part, 75.0, f"step_08_B3_tower_or_roller_{index:02d}"))

    # 09: frozen B5A passive bridge/receiver layer.
    for index, part in enumerate(b5a_geometry.b5a_assembled_occurrences(), 1):
        children.append(_moved_labeled(part, 105.0, f"step_09_B5A_passive_receiver_{index:02d}"))

    # 10: explicit no-ring power-test witness before moving rings are installed.
    children.append(_moved_labeled(wiring_witnesses()[0], 125.0, "step_10_NO_RING_power_test_witness"))

    # 11: B4 rings are last. Exact accepted segments, magnets, and seam screws.
    for role_index, role in enumerate(b4_spec.SPEC.ring.roles):
        dz = 145.0 + role_index * 24.0
        for segment_index in range(3):
            children.append(
                _moved_labeled(
                    b4_geometry.segment_shape(role_index, segment_index),
                    dz + segment_index * 3.0,
                    f"step_11_B4_LAST_{role}_segment_{segment_index + 1}",
                )
            )
        children.append(_moved_labeled(b4_geometry.magnet_witness(role_index), dz + 11.0, f"step_11_B4_LAST_{role}_magnet"))
        for seam_index in range(3):
            children.append(
                _moved_labeled(
                    b4_geometry.screw_witness(role_index, seam_index),
                    dz + 15.0 + seam_index * 3.0,
                    f"step_11_B4_LAST_{role}_seam_screw_{seam_index + 1}",
                )
            )
    return Compound(children=children, label=f"{NAMESPACE}_exact_assembly_order_exploded")
