from __future__ import annotations

import json
from copy import deepcopy
from math import cos, radians, sin
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Axis, Compound, Cylinder, Location, RegularPolygon, extrude, import_step

from p3_v3_direct_gear_race_guidance_geometry import make_fin_360_sweep, make_full_role_ring_reference
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import local_point, named_sector
from p3_v3_mvp_free_roller_r0_three_station_geometry import (
    intersection_volume_mm3,
    make_spacer_print as make_r0_spacer,
    make_spool_print as make_r0_spool,
    make_upper_bridge_print as make_r0_bridge,
)
from p3_v3_mvp_free_roller_r1_retrofit_geometry import (
    make_assembled_spool,
    make_print_station_kit,
    make_spacer_print,
    make_spool_print,
    make_station_assembly,
    make_station_frame_print,
    make_three_station_context,
    make_upper_bridge_print,
)
from p3_v3_mvp_free_roller_r1_retrofit_spec import MODEL_ROOT, SPEC


ROOT = Path(__file__).resolve().parents[1]


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids())


def _planar_face_area_at_z(shape, z_mm: float) -> float:
    return sum(
        face.area
        for face in shape.faces()
        if face.bounding_box().min.Z == pytest.approx(z_mm, abs=1e-7)
        and face.bounding_box().max.Z == pytest.approx(z_mm, abs=1e-7)
    )


def _ordinary_m3_nut(radius_mm: float, tangent_mm: float):
    return extrude(
        RegularPolygon(SPEC.nut_nominal_across_flats_mm / 2, 6, major_radius=False),
        amount=SPEC.nut_nominal_thickness_mm,
    ).moved(Location((radius_mm, tangent_mm, SPEC.nut_front_skin_mm)))


def _children_matching(assembly, *tokens: str):
    return [child for child in assembly.children if any(token in child.label for token in tokens)]


def _radial_shift(shape, station_angle_deg: float, inward_mm: float):
    angle = radians(station_angle_deg)
    return deepcopy(shape).moved(
        Location((-inward_mm * cos(angle), -inward_mm * sin(angle), 0))
    )


def test_exact_existing_mount_axes_and_post_print_countersink_contract():
    assert SPEC.station_angles_deg == (60.0, 180.0, 300.0)
    assert SPEC.outer_mount_radius_mm == pytest.approx(118.0)
    assert SPEC.outer_mount_tangent_mm == pytest.approx((-7.0, 7.0))
    assert SPEC.base_hole_diameter_mm == pytest.approx(3.3)
    assert SPEC.mount_slot_width_mm == pytest.approx(3.6)
    assert SPEC.mount_slot_length_mm == pytest.approx(4.1)
    assert SPEC.mount_slot_center_travel_mm == pytest.approx(0.5)

    assert SPEC.countersink_major_diameter_mm == pytest.approx(6.0)
    assert SPEC.countersink_included_angle_deg == pytest.approx(90.0)
    assert SPEC.countersink_target_depth_mm == pytest.approx(1.45)
    assert SPEC.countersink_depth_tolerance_mm == pytest.approx(0.10)
    assert SPEC.rear_datum_z_mm == pytest.approx(-31.5)
    assert SPEC.countersink_apex_z_mm == pytest.approx(-30.05)
    assert SPEC.station_screw_length_mm == pytest.approx(10.0)
    assert SPEC.station_screw_tip_z_mm == pytest.approx(-21.5)

    axes = {
        tuple(round(value, 6) for value in local_point(angle, 118.0, tangent))
        for angle in SPEC.station_angles_deg
        for tangent in SPEC.outer_mount_tangent_mm
    }
    assert len(axes) == 6


def test_existing_canonical_base_is_reused_unmodified_and_keeps_flat_rear_datum():
    context = make_three_station_context()
    base_parts = [child for child in context.children if "EXISTING_CANONICAL_Q3_R0" in child.label]
    assert len(base_parts) == 3
    canonical = named_sector(1)
    for sector in base_parts:
        assert sector.bounding_box().min.Z == pytest.approx(SPEC.rear_datum_z_mm)
        assert _planar_face_area_at_z(sector, SPEC.rear_datum_z_mm) == pytest.approx(
            _planar_face_area_at_z(canonical, SPEC.rear_datum_z_mm),
            abs=1e-6,
        )
    assert not any(
        token in path.name.lower()
        for path in MODEL_ROOT.glob("*")
        for token in ("base", "sector", "derivative")
    )


def test_existing_six_base_bores_and_r1_slots_share_the_exact_axes():
    sectors = [named_sector(1).rotate(Axis.Z, angle) for angle in (0.0, 120.0, 240.0)]
    local_frame = make_station_frame_print()
    for angle in SPEC.station_angles_deg:
        frame = local_frame.moved(Location((0, 0, SPEC.station_foot_z_mm[0]))).rotate(Axis.Z, angle)
        for tangent in SPEC.outer_mount_tangent_mm:
            x, y = local_point(angle, SPEC.outer_mount_radius_mm, tangent)
            base_probe = Cylinder(
                SPEC.base_hole_diameter_mm / 2 - 0.05,
                SPEC.base_plate_z_mm[1] - SPEC.base_plate_z_mm[0] + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, SPEC.base_plate_z_mm[0] - 0.2)))
            slot_probe = Cylinder(
                SPEC.mount_slot_width_mm / 2 - 0.05,
                SPEC.station_foot_z_mm[1] - SPEC.station_foot_z_mm[0] + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, SPEC.station_foot_z_mm[0] - 0.2)))
            assert sum(intersection_volume_mm3(base_probe, sector) for sector in sectors) == pytest.approx(0, abs=1e-7)
            assert intersection_volume_mm3(slot_probe, frame) == pytest.approx(0, abs=1e-7)


def test_lower_d4p20_socket_clears_unchanged_d6_post_top_by_point_one():
    assert SPEC.axle_finished_diameter_mm == pytest.approx(3.99)
    assert SPEC.axle_clearance_diameter_mm == pytest.approx(4.20)
    assert SPEC.lower_post_od_mm == pytest.approx(6.0)
    assert SPEC.axle_z_mm[0] == pytest.approx(-5.0)
    assert SPEC.lower_post_top_z_mm == pytest.approx(-2.45)
    assert SPEC.lower_socket_top_clearance_mm == pytest.approx(0.10)
    assert SPEC.lower_socket_depth_mm == pytest.approx(2.65)
    assert SPEC.lower_socket_top_z_mm == pytest.approx(-2.35)
    assert SPEC.lower_socket_top_z_mm - SPEC.lower_post_top_z_mm == pytest.approx(0.10)

    frame = make_station_frame_print().moved(Location((0, 0, SPEC.station_foot_z_mm[0])))
    socket_probe = Cylinder(
        SPEC.axle_clearance_diameter_mm / 2 - 0.01,
        SPEC.lower_socket_depth_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.roller_axis_radius_mm, 0, SPEC.axle_z_mm[0])))
    assert intersection_volume_mm3(socket_probe, frame) == pytest.approx(0.0, abs=1e-7)


def test_open_top_m3_nut_captures_fit_and_keep_a_half_millimeter_floor():
    assert SPEC.nut_across_flats_mm == pytest.approx(5.8)
    assert SPEC.nut_pocket_depth_mm == pytest.approx(2.5)
    assert SPEC.nut_pocket_radial_elongation_mm == pytest.approx(0.6)
    assert SPEC.nut_front_skin_mm == pytest.approx(0.5)
    assert SPEC.station_nut_pocket_z_mm == pytest.approx((-25.0, -22.5))
    assert SPEC.station_nut_engagement_mm == pytest.approx(2.4)
    assert SPEC.station_nut_engagement_mm >= 1.0

    frame = make_station_frame_print()
    for tangent in SPEC.outer_mount_tangent_mm:
        for radial_offset in (-0.30, 0.0, 0.30):
            nut = _ordinary_m3_nut(SPEC.outer_mount_radius_mm + radial_offset, tangent)
            assert intersection_volume_mm3(nut, frame) == pytest.approx(0.0, abs=1e-7)

        # Probe intact material beside the through-slot, directly below the
        # open-top hex pocket.  This is an actual-solid assertion of the
        # specified 0.50 mm pocket floor rather than parameter math alone.
        for side in (-1.0, 1.0):
            floor_probe = Cylinder(
                0.20,
                SPEC.nut_front_skin_mm - 0.10,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((SPEC.outer_mount_radius_mm, tangent + side * 2.30, 0.05)))
            assert intersection_volume_mm3(floor_probe, frame) == pytest.approx(_volume(floor_probe), abs=1e-6)


def test_roller_spool_spacer_bridge_and_fin_geometry_is_preserved_from_r0():
    for r1, r0 in (
        (make_spool_print(), make_r0_spool()),
        (make_spacer_print(), make_r0_spacer()),
        (make_upper_bridge_print(), make_r0_bridge()),
    ):
        assert _volume(r1) == pytest.approx(_volume(r0), abs=1e-7)
        assert r1.bounding_box().size == pytest.approx(r0.bounding_box().size, abs=1e-7)

    rings = [make_full_role_ring_reference(index) for index in range(3)]
    fins = [make_fin_360_sweep(index) for index in range(3)]
    for role in range(3):
        spool = make_assembled_spool(role, 60.0)
        assert [intersection_volume_mm3(spool, ring) for ring in rings] == pytest.approx([0, 0, 0], abs=1e-7)
    stationary = [
        part
        for part in make_station_assembly(60.0, include_hardware=False).children
        if "spool" not in part.label and "spacer" not in part.label
    ]
    for part in stationary:
        for obstacle in rings + fins:
            assert intersection_volume_mm3(part, obstacle) == pytest.approx(0.0, abs=1e-7)
            assert part.distance_to(obstacle) >= SPEC.minimum_fin_clearance_mm


def test_all_nine_spool_ring_pairs_have_actual_solid_axial_flange_capture():
    """Both flange escape directions must strike the corresponding carrier.

    Nominal contact remains volume-clear; moving the spool one face clearance
    plus 0.05 mm in either axial direction must create positive solid overlap.
    This is deliberately checked for every station, not inferred from one
    symmetric parameter calculation.
    """

    escape_mm = SPEC.spool_face_clearance_mm + 0.05
    rings = [make_full_role_ring_reference(role) for role in range(3)]
    for angle in SPEC.station_angles_deg:
        for role, ring in enumerate(rings):
            spool = make_assembled_spool(role, angle)
            assert intersection_volume_mm3(spool, ring) == pytest.approx(0.0, abs=1e-7)
            assert intersection_volume_mm3(spool.moved(Location((0, 0, escape_mm))), ring) > 1e-3
            assert intersection_volume_mm3(spool.moved(Location((0, 0, -escape_mm))), ring) > 1e-3


def test_hardware_inclusive_stations_clear_every_full_360_degree_fin_sweep():
    """Purchased hardware is part of the keep-out gate, not hidden from it."""

    fin_sweeps = [make_fin_360_sweep(role) for role in range(3)]
    for angle in SPEC.station_angles_deg:
        station = make_station_assembly(angle, include_hardware=True)
        for fin in fin_sweeps:
            assert intersection_volume_mm3(station, fin) == pytest.approx(0.0, abs=1e-7)
            assert station.distance_to(fin) >= SPEC.minimum_fin_clearance_mm


def test_sampled_complete_ring_and_station_service_paths_are_volume_clear():
    """Exercise the actual assembly order with a small meaningful path sample.

    Rings descend before bridges are fitted.  The spool/washer/spacer stack is
    then withdrawn toward the open centre; the bridge and axle use vertical
    service paths.  All checks use the complete solids rather than envelopes.
    """

    rings = [make_full_role_ring_reference(role) for role in range(3)]
    for angle in SPEC.station_angles_deg:
        station = make_station_assembly(angle, include_hardware=True)
        frame = _children_matching(station, "station_frame")[0]

        # Complete rings are installed vertically with the bridge absent.
        for ring in rings:
            for lift_mm in (18.0, 9.0, 3.0, 0.0):
                assert intersection_volume_mm3(
                    ring.moved(Location((0, 0, lift_mm))), frame
                ) == pytest.approx(0.0, abs=1e-7)

        # The complete eleven-piece thrust stack shares one radial service
        # path.  Checking it as a compound covers 3 spools, 6 washers and 2
        # spacers without multiplying equivalent low-value assertions.
        stack = Compound(
            children=_children_matching(
                station, "spool_station", "spacer_station", "thrust_washer"
            )
        )
        radial_obstacles = Compound(children=[frame, *rings])
        for inward_mm in (30.0, 20.0, 10.0, 4.0, 0.0):
            assert intersection_volume_mm3(
                _radial_shift(stack, angle, inward_mm), radial_obstacles
            ) == pytest.approx(0.0, abs=1e-7)

        bridge = _children_matching(station, "upper_bridge")[0]
        bridge_obstacles = Compound(children=[frame, stack, *rings])
        for lift_mm in (12.0, 6.0, 2.0, 0.0):
            assert intersection_volume_mm3(
                bridge.moved(Location((0, 0, lift_mm))), bridge_obstacles
            ) == pytest.approx(0.0, abs=1e-7)

        axle = _children_matching(station, "polished_axle")[0]
        axle_obstacles = Compound(children=[frame, bridge, stack, *rings])
        for lift_mm in (30.0, 20.0, 10.0, 3.0, 0.0):
            assert intersection_volume_mm3(
                axle.moved(Location((0, 0, lift_mm))), axle_obstacles
            ) == pytest.approx(0.0, abs=1e-7)


def test_station_and_bridge_use_only_declared_m3_hardware():
    labels = [child.label for child in make_station_assembly(60.0, include_hardware=True).children]
    assert sum("M3x10_flat_head" in label for label in labels) == 2
    assert sum("ordinary_M3_station_nut" in label for label in labels) == 2
    assert sum("M3x6_bridge_screw" in label for label in labels) == 2
    assert sum("ordinary_M3_bridge_nut" in label for label in labels) == 2
    assert not any("printed_thread" in label.lower() or "dowel" in label.lower() for label in labels)

    flat_heads = [child for child in make_station_assembly(60.0, include_hardware=True).children if "M3x10_flat_head" in child.label]
    assert len(flat_heads) == 2
    assert all(head.bounding_box().min.Z == pytest.approx(SPEC.rear_datum_z_mm) for head in flat_heads)


def test_r1_printed_parts_are_positive_single_solids_and_fit_u1():
    for part in (make_station_frame_print(), make_upper_bridge_print(), make_spool_print(), make_spacer_print()):
        assert len(list(part.solids())) == 1
        assert _volume(part) > 0
    kit = make_print_station_kit()
    assert len(kit.children) == 7
    assert kit.bounding_box().size.X <= SPEC.u1_usable_xy_mm
    assert kit.bounding_box().size.Y <= SPEC.u1_usable_xy_mm


def test_written_r1_step_files_are_importable_positive_and_no_base_replacement_exists():
    paths = (
        MODEL_ROOT / "station_frame_print_qty3.step",
        MODEL_ROOT / "upper_bridge_print_qty3.step",
        MODEL_ROOT / "flanged_spool_print_qty9.step",
        MODEL_ROOT / "spacer_print_qty6.step",
        MODEL_ROOT / "one_station_retrofit_kit_qty3.step",
        MODEL_ROOT / "three_station_retrofit_context.step",
        MODEL_ROOT / "service_exploded.step",
    )
    for path in paths:
        assert path.is_file() and path.stat().st_size > 1000
        assert _volume(import_step(str(path))) > 0
    assert not any(
        token in path.name.lower()
        for path in MODEL_ROOT.glob("*.step")
        for token in ("base", "sector", "derivative")
    )


def test_written_3mf_and_manifest_define_retrofit_only():
    path = MODEL_ROOT / "one_station_retrofit_kit_print_qty3.3mf"
    assert path.is_file() and path.stat().st_size > 1000
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    assert not any(any(token in name.lower() for token in ("project_settings", "model_settings", "slice_info")) for name in names)
    assert len(root.findall(".//m:resources/m:object", ns)) == 7
    assert len(root.findall(".//m:build/m:item", ns)) == 7

    manifest = json.loads((MODEL_ROOT / "print_manifest.json").read_text())
    assert manifest["existing_base_policy"]["replacement_base_exported"] is False
    assert manifest["existing_base_policy"]["base_reprint_required"] is False
    assert manifest["lower_axle_socket"] == {
        "depth_mm": 2.65,
        "diameter_mm": 4.2,
        "finished_axle_diameter_mm": 3.99,
        "post_outer_diameter_mm": 6.0,
        "post_top_z_mm": -2.45,
        "socket_overrun_above_post_mm": 0.1,
        "z_mm": [-5.0, -2.35],
    }
    assert manifest["effective_print_totals"] == {
        "station_frame": 3,
        "upper_bridge": 3,
        "flanged_spool": 9,
        "spacer": 6,
    }
    assert manifest["purchased_hardware"]["station"] == "M3x10 90-degree flat-head screw x6; ordinary M3 nut x6"
    assert manifest["purchased_hardware"]["bridge"] == "M3x6 screw x6; ordinary M3 nut x6"
