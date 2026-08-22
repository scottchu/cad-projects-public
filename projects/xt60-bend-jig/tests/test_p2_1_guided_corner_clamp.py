"""Analytic and actual-BREP acceptance checks for P2.1."""

from __future__ import annotations

from math import sqrt
from pathlib import Path

import pytest
from build123d import Align, Cylinder, Pos, RegularPolygon, Rot, extrude, import_step
import lib3mf

from xt60_bend_jig.p2_corner_clamp import (
    build_esc,
    build_fc,
    build_reference_rod,
    build_wire,
    build_wires,
    build_xt60,
    contact_points,
    rod_centers,
)
from xt60_bend_jig.p2_1_guided_corner_clamp import (
    CLEAR_SPAN,
    DRIVE_CONTACT_CLOSED,
    KEEPER_SNAP_ARM_THICKNESS,
    KEEPER_SNAP_DEFLECTION,
    KEEPER_SNAP_ROOF_GAP,
    GUIDE_CLEARANCE,
    LEFT_FIXED_BORE,
    MOVING_ROD_KEEPER_GAP,
    OPEN_STROKE,
    OUTER_SPAN,
    PLATE_THICKNESS,
    RIGHT_FIXED_BORE,
    ROD_PROJECTION,
    TONGUE_ROOT_DEPTH,
    _axis_cylinder,
    _axis_hex_prism,
    _axis_point,
    M6_CLEARANCE_DIAMETER,
    M6_NUT_ACROSS_CORNERS,
    M6_NUT_THICKNESS,
    NUT_AXIS_DISTANCE,
    SCREW_AXIS_ANGLE_DEG,
    SCREW_LENGTH,
    THRUST_TIP_THICKNESS,
    build_fixed_rod_caps,
    build_frame,
    build_exploded,
    build_knob,
    build_loaded_closed,
    build_loaded_open,
    build_pusher,
    build_m6_nut,
    build_moving_rod_keepers,
    build_nut_keeper,
    build_print_kit,
    build_rods,
    build_screw,
    moving_center,
)


def test_frozen_p2_contact_math_and_exact_three_4x50_rods():
    rods = rod_centers()
    for name, contact in contact_points().items():
        assert rods[name].distance_to(contact) == pytest.approx(4.15)
    assembly = build_rods()
    assert len(assembly.children) == 3
    for rod in assembly.children:
        b = rod.bounding_box()
        assert (b.size.X, b.size.Y, b.size.Z) == pytest.approx((50.0, 4.0, 4.0))


@pytest.mark.parametrize("wire_x", (-4.0, 4.0))
def test_closed_rods_make_tangent_zero_overlap_wire_contacts(wire_x):
    wire = build_wire(wire_x, "#FFFFFF")
    for rod in build_rods().children:
        assert rod.distance_to(wire) == pytest.approx(0.0, abs=1.1e-7)
        assert (rod & wire).volume == pytest.approx(0.0, abs=1e-7)


def test_t3_frame_span_and_real_4x50_projection_are_frozen():
    assert PLATE_THICKNESS == 3.0
    assert CLEAR_SPAN == 38.0
    assert OUTER_SPAN == 44.0
    assert ROD_PROJECTION == 3.0
    assert LEFT_FIXED_BORE == 3.90
    assert RIGHT_FIXED_BORE == 4.20


def test_frame_and_pusher_are_each_one_valid_printed_solid():
    for shape in (build_frame(), build_pusher()):
        assert shape.is_valid
        assert len(shape.solids()) == 1
    assert GUIDE_CLEARANCE >= 0.30
    assert TONGUE_ROOT_DEPTH >= 1.20


def test_actual_frame_gap_is_at_least_0p30_through_the_sweep():
    frame, pusher = build_frame(), build_pusher()
    for index in range(101):
        travel = OPEN_STROKE * index / 100.0
        d = travel / sqrt(2.0)
        assert (Pos(0.0, d, d) * pusher).distance_to(frame) >= 0.299999


def test_full_101_pose_actual_brep_frame_pusher_and_moving_rod_sweep_is_clear():
    frame = build_frame()
    pusher = build_pusher()
    for index in range(101):
        travel = OPEN_STROKE * index / 100.0
        d = travel / sqrt(2.0)
        moved_pusher = Pos(0.0, d, d) * pusher
        moving_rod = build_reference_rod("moving", moving_center(travel))
        assert (moved_pusher & frame).volume == pytest.approx(0.0, abs=1e-6)
        assert (moving_rod & frame).volume == pytest.approx(0.0, abs=1e-6)


def test_full_101_pose_pusher_and_moving_rod_clear_fixed_rods_and_workpiece_references():
    pusher = build_pusher()
    centers = rod_centers()
    fixed_rods = build_reference_rod("left", centers["left"]) + build_reference_rod("bottom", centers["bottom"])
    references = build_wires() + build_esc() + build_fc() + build_xt60()
    for index in range(101):
        travel = OPEN_STROKE * index / 100.0
        d = travel / sqrt(2.0)
        moved_pusher = Pos(0.0, d, d) * pusher
        moving_rod = build_reference_rod("moving", moving_center(travel))
        assert (moved_pusher & fixed_rods).volume == pytest.approx(0.0, abs=1e-6)
        assert (moved_pusher & references).volume == pytest.approx(0.0, abs=1e-6)
        assert (moving_rod & fixed_rods).volume == pytest.approx(0.0, abs=1e-6)
        assert (moving_rod & references).volume == pytest.approx(0.0, abs=1e-6)


def test_moving_rod_retention_has_positive_endplay():
    assert MOVING_ROD_KEEPER_GAP >= 0.30
    frame = build_frame()
    rod = build_rods().children[2]
    for keeper in build_moving_rod_keepers().children:
        assert (keeper & rod).volume == pytest.approx(0.0, abs=1e-7)
        assert keeper.distance_to(frame) == pytest.approx(MOVING_ROD_KEEPER_GAP)


def test_open_guide_throat_accepts_pusher_before_moving_rod_is_inserted():
    frame, pusher = build_frame(), build_pusher()
    for extra in range(7):
        d = (OPEN_STROKE + extra) / sqrt(2.0)
        assert (frame & (Pos(0.0, d, d) * pusher)).volume == pytest.approx(0.0, abs=1e-6)


def test_top_loaded_nut_and_drive_hardware_have_real_clear_paths():
    frame = build_frame()
    nut = build_m6_nut()
    for step in range(41):
        assert (frame & (Pos(0.0, 0.0, step * 0.5) * nut)).volume == pytest.approx(0.0, abs=1e-6)
    references = build_wires() + build_esc() + build_fc() + build_xt60()
    for travel in (0.0, OPEN_STROKE / 2.0, OPEN_STROKE):
        screw, knob = build_screw(travel), build_knob(travel)
        assert (screw & frame).volume == pytest.approx(0.0, abs=1e-6)
        assert (knob & frame).volume == pytest.approx(0.0, abs=1e-6)
        assert (screw & references).volume == pytest.approx(0.0, abs=1e-6)
        assert (knob & references).volume == pytest.approx(0.0, abs=1e-6)


def test_external_thrust_tip_is_tangent_and_drive_clears_iron_corridors_for_101_poses():
    pusher = build_pusher()
    frame = build_frame()
    for index in range(101):
        travel = OPEN_STROKE * index / 100.0
        d = travel / sqrt(2.0)
        moved = Pos(0.0, d, d) * pusher
        screw = build_screw(travel)
        assert (moved & screw).volume == pytest.approx(0.0, abs=1e-7)
        assert moved.distance_to(screw) == pytest.approx(0.0, abs=1e-7)
    for x in (-4.0, 4.0):
        corridor = Pos(x, 28.0, 50.0) * Cylinder(
            3.0, 40.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )
        assert (corridor & frame).volume == pytest.approx(0.0, abs=1e-7)
        assert (corridor & build_screw()).volume == pytest.approx(0.0, abs=1e-7)
        assert (corridor & build_knob()).volume == pytest.approx(0.0, abs=1e-7)


def test_hex_head_socket_and_keyed_keeper_provide_positive_rotational_engagement():
    # The aligned head fits its true hex socket; a 5-degree rotated head
    # interferes, proving the knob is not a cosmetic cylindrical recess.
    screw = build_screw()
    head = screw.children[2]
    knob = build_knob()
    assert (head & knob).volume == pytest.approx(0.0, abs=1e-7)
    tip_center = _axis_point(DRIVE_CONTACT_CLOSED, THRUST_TIP_THICKNESS / 2.0)
    head_center = _axis_point(tip_center, SCREW_LENGTH + 2.0)
    rotated_head_face = RegularPolygon(11.0 / 2.0, 6, rotation=5.0)
    rotated_head = Pos(0.0, head_center.y, head_center.z) * Rot(SCREW_AXIS_ANGLE_DEG, 0.0, 0.0) * extrude(
        rotated_head_face, 2.0, both=True
    )
    assert (rotated_head & knob).volume > 0.1
    # Nut is independently keyed by both lower frame and installed keeper.
    center = _axis_point(DRIVE_CONTACT_CLOSED, NUT_AXIS_DISTANCE)
    face = RegularPolygon(M6_NUT_ACROSS_CORNERS / 2.0, 6, rotation=5.0)
    rotated = Pos(0.0, center.y, center.z) * Rot(SCREW_AXIS_ANGLE_DEG, 0.0, 0.0) * extrude(
        face, M6_NUT_THICKNESS / 2.0, both=True
    )
    rotated -= _axis_cylinder(M6_CLEARANCE_DIAMETER, M6_NUT_THICKNESS + 2.0, center)
    assert (rotated & build_nut_keeper()).volume > 0.1


def test_keeper_snap_hooks_prevent_positive_z_ejection_but_are_intentionally_flexible():
    frame, keeper = build_frame(), build_nut_keeper()
    assert KEEPER_SNAP_ARM_THICKNESS >= 1.2
    assert KEEPER_SNAP_DEFLECTION == pytest.approx(0.30)
    assert KEEPER_SNAP_ROOF_GAP == pytest.approx(0.20)
    assert (frame & keeper).volume == pytest.approx(0.0, abs=1e-7)
    assert keeper.distance_to(frame) == pytest.approx(KEEPER_SNAP_ROOF_GAP)
    # A rigid +Z extraction encounters both hook roofs immediately after the
    # designed free gap. Assembly/removal instead flexes each 1.2 mm arm
    # outward by the explicit 0.30 mm hook overlap.
    assert (frame & (Pos(0.0, 0.0, KEEPER_SNAP_ROOF_GAP + 0.01) * keeper)).volume > 0.0
    assert (frame & (Pos(0.0, 0.0, 0.50) * keeper)).volume > 1.0


def test_printed_volume_is_materially_below_the_rejected_cage():
    from xt60_bend_jig.p5_simple_slider import build_fixed_plate as build_p5_plate
    from xt60_bend_jig.p5_simple_slider import build_pusher as build_p5_pusher

    p5_volume = build_p5_plate("left").volume + build_p5_plate("right").volume + build_p5_pusher().volume
    printed = (
        build_frame().volume
        + build_pusher().volume
        + build_knob().volume
        + build_nut_keeper().volume
        + build_moving_rod_keepers().volume
        + build_fixed_rod_caps().volume
    )
    assert printed < 1.5 * p5_volume


def test_exploded_assembly_packet_is_valid():
    exploded = build_exploded()
    assert exploded.is_valid
    assert len(exploded.solids()) >= 10
    for index, first in enumerate(exploded.children):
        for second in exploded.children[index + 1 :]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7), (
                first.label,
                second.label,
            )


def test_print_kit_has_eight_positive_nonoverlapping_printed_solids():
    kit = build_print_kit()
    assert kit.is_valid and len(kit.solids()) == 8
    assert all(solid.volume > 0.0 for solid in kit.solids())
    for index, first in enumerate(kit.children):
        for second in kit.children[index + 1 :]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)


def test_closed_and_open_assemblies_are_valid_and_keep_one_piece_frame():
    for assembly in (build_loaded_closed(), build_loaded_open()):
        assert assembly.is_valid
        labels = {child.label for child in assembly.children}
        assert "one_piece_green_rigid_frame_t3_38mm_clear_span_flat_clamp_bridges" in labels
        assert "reference_exactly_three_user_4x50_rods" in labels
        assert "reference_standard_M6_hex_nut_fixed_in_green_pocket" in labels


def test_generated_closed_open_steps_match_source_counts_and_bounds_when_present():
    project = Path(__file__).resolve().parents[1]
    export_dir = project / "cad" / "p2_1_guided_corner_clamp"
    for filename, source in (
        ("p2_1_loaded_closed.step", build_loaded_closed()),
        ("p2_1_loaded_open.step", build_loaded_open()),
    ):
        path = export_dir / filename
        if not path.exists():
            pytest.skip(f"generate {filename} before source/export parity")
        imported = import_step(path)
        assert len(imported.solids()) == len(source.solids())
        sb, ib = source.bounding_box(), imported.bounding_box()
        assert (*ib.min, *ib.max) == pytest.approx((*sb.min, *sb.max), abs=1e-5)


def test_generated_3mf_has_eight_lib3mf_valid_manifold_oriented_meshes():
    project = Path(__file__).resolve().parents[1]
    path = project / "cad" / "p2_1_guided_corner_clamp" / "p2_1_print_kit.3mf"
    if not path.exists():
        pytest.skip("generate the source-derived welded print-kit 3MF first")
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.QueryReader("3mf").ReadFromFile(str(path))
    meshes = model.GetMeshObjects()
    names: list[str] = []
    while meshes.MoveNext():
        mesh = meshes.GetCurrentMeshObject()
        names.append(mesh.GetName())
        assert mesh.IsValid(), mesh.GetName()
        assert mesh.IsManifoldAndOriented(), mesh.GetName()
        assert mesh.GetVertexCount() > 0
        assert mesh.GetTriangleCount() > 0
    assert len(names) == 8
    assert len(set(names)) == 8
