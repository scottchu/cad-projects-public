"""BREP and contract tests for the directly-authored build123d geometry."""

from __future__ import annotations

from dataclasses import replace

import pytest
from build123d import Align, Box, Cylinder, Pos

from xt60_bend_jig.assembly import build_closed_assembly, build_open_assembly, build_print_kit
from xt60_bend_jig.geometry import (
    ADJUSTMENT_PITCH,
    FIT_SIZES,
    FORMING_SLOT_WIDTH,
    FRAME_CLEAR_SPAN,
    FRAME_OUTER_SPAN,
    FRAME_THICKNESS,
    NUT_TRAP_AF,
    MOVING_CLAMP_PASSAGE_DIAMETER,
    MOVING_INSERT_BOSS_DIAMETER,
    MOVING_INSERT_POCKET_DEPTH,
    MOVING_INSERT_POCKET_DIAMETER,
    REACTION_INSERT_POCKET_DEPTH,
    REACTION_INSERT_POCKET_DIAMETER,
    REACTION_LOCK_BOSS_DIAMETER,
    REACTION_LOCK_OFFSET,
    REACTION_ROD_BOSS_DIAMETER,
    ROD_BORE_DIAMETER,
    SLIDER_COLLAR_DIAMETER,
    XT60_ENVELOPE,
    XT60_SIDE_CLEARANCE,
    WIRE_BEND_RADIUS,
    WIRE_HORIZONTAL_Z,
    WIRE_TANGENT_START_Y,
    WIRE_VERTICAL_TANGENT_Y,
    build_end_cap,
    build_fit_coupon,
    build_knob,
    build_left_drive_support,
    build_left_frame,
    build_left_frame_with_drive_support,
    build_left_slider,
    build_reaction_carrier,
    build_reference_rod,
    build_right_frame,
    build_right_slider,
    build_wire_centerline,
    build_wire_reference,
    build_xt60_bridge,
    build_xt60_reference,
)
from xt60_bend_jig.mechanism import solve_mechanism
from xt60_bend_jig.parameters import DEFAULT_PARAMETERS


PART_BUILDERS = (
    build_left_frame,
    build_right_frame,
    build_left_slider,
    build_right_slider,
    build_xt60_bridge,
    build_knob,
    build_end_cap,
    build_fit_coupon,
    build_left_frame_with_drive_support,
)


@pytest.mark.parametrize("builder", PART_BUILDERS)
def test_printable_parts_are_valid_positive_volume(builder):
    part = builder()
    assert part.is_valid
    assert part.volume > 0.0
    assert len(part.solids()) == 1


@pytest.mark.parametrize("side", ("left", "right"))
@pytest.mark.parametrize("kind", ("upper", "lower"))
def test_reaction_carriers_are_single_valid_positive_solids(side, kind):
    carrier = build_reaction_carrier(side, kind)
    assert carrier.is_valid and carrier.volume > 0
    assert len(carrier.solids()) == 1


def test_side_frames_have_mirrored_x_bounds_and_four_mm_thickness():
    left = build_left_frame().bounding_box()
    right = build_right_frame().bounding_box()
    assert left.min.X == pytest.approx(-right.max.X)
    assert left.max.X == pytest.approx(-right.min.X)
    assert left.size.X == pytest.approx(FRAME_THICKNESS)
    assert right.size.X == pytest.approx(FRAME_THICKNESS)
    assert right.max.X - left.min.X == pytest.approx(FRAME_OUTER_SPAN)
    assert right.min.X - left.max.X == pytest.approx(FRAME_CLEAR_SPAN)
    assert (50.0 - FRAME_OUTER_SPAN) / 2.0 == pytest.approx(2.0)


def test_key_dimensions_match_the_frozen_mechanical_contract():
    assert ROD_BORE_DIAMETER == pytest.approx(4.3)
    assert FORMING_SLOT_WIDTH == pytest.approx(4.6)
    assert ADJUSTMENT_PITCH >= 6.5
    assert NUT_TRAP_AF == pytest.approx(7.2)
    assert XT60_ENVELOPE == pytest.approx((15.9, 8.1))
    assert XT60_SIDE_CLEARANCE == pytest.approx(0.4)
    assert FIT_SIZES == pytest.approx((4.2, 4.3, 4.4, 4.5))
    assert MOVING_CLAMP_PASSAGE_DIAMETER == pytest.approx(3.4)
    assert MOVING_INSERT_POCKET_DIAMETER == pytest.approx(4.6)
    assert MOVING_INSERT_POCKET_DEPTH == pytest.approx(5.0)
    assert MOVING_INSERT_BOSS_DIAMETER == pytest.approx(8.6)
    assert (MOVING_INSERT_BOSS_DIAMETER - MOVING_INSERT_POCKET_DIAMETER) / 2.0 >= 2.0
    assert SLIDER_COLLAR_DIAMETER == pytest.approx(10.0)
    assert REACTION_ROD_BOSS_DIAMETER == pytest.approx(9.0)
    assert REACTION_LOCK_BOSS_DIAMETER == pytest.approx(7.0)
    assert REACTION_INSERT_POCKET_DIAMETER == pytest.approx(4.6)
    assert REACTION_INSERT_POCKET_DEPTH == pytest.approx(3.5)
    assert REACTION_LOCK_OFFSET - (
        ROD_BORE_DIAMETER + REACTION_INSERT_POCKET_DIAMETER
    ) / 2.0 == pytest.approx(2.55)


@pytest.mark.parametrize(
    ("side", "builder"), (("left", build_left_slider), ("right", build_right_slider))
)
def test_slider_axial_insert_seats_and_rod_end_passages_are_exact_and_connected(side, builder):
    slider = builder()
    solved = solve_mechanism(closure=1.0)
    outward = -1.0 if side == "left" else 1.0
    plate_x = outward * (DEFAULT_PARAMETERS.outer_span / 2.0 + 1.0)
    axis_y = solved.moving_closed_center.y
    socket_z = solved.moving_closed_center.z

    # The exact insert gauge reaches 0.5 mm beyond the outer boss end, proving
    # unobstructed axial access, while the continuation reaches the rod socket.
    insert_gauge = Pos(outward * 29.75, axis_y, socket_z) * Cylinder(
        MOVING_INSERT_POCKET_DIAMETER / 2.0,
        MOVING_INSERT_POCKET_DEPTH + 0.5,
        rotation=(0, 90, 0),
    )
    clamp_gauge = Pos(outward * 26.0, axis_y, socket_z) * Cylinder(
        MOVING_CLAMP_PASSAGE_DIAMETER / 2.0, 2.2, rotation=(0, 90, 0)
    )
    assert (slider & insert_gauge).volume == pytest.approx(0.0, abs=1e-7)
    assert (slider & clamp_gauge).volume == pytest.approx(0.0, abs=1e-7)

    insert_oversize = Pos(outward * 29.5, axis_y, socket_z) * Cylinder(
        (MOVING_INSERT_POCKET_DIAMETER + 0.02) / 2.0, 4.6, rotation=(0, 90, 0)
    )
    clamp_oversize = Pos(outward * 26.0, axis_y, socket_z) * Cylinder(
        (MOVING_CLAMP_PASSAGE_DIAMETER + 0.02) / 2.0, 1.4, rotation=(0, 90, 0)
    )
    assert (slider & insert_oversize).volume > 0.0
    assert (slider & clamp_oversize).volume > 0.0

    rod_socket = Pos(plate_x, axis_y, socket_z) * Cylinder(
        ROD_BORE_DIAMETER / 2.0, 2.4, rotation=(0, 90, 0)
    )
    connected_void = rod_socket + clamp_gauge + insert_gauge
    assert len(connected_void.solids()) == 1
    assert (slider & connected_void).volume == pytest.approx(0.0, abs=1e-7)
    assert slider.is_valid and len(slider.solids()) == 1


def test_frame_has_two_reaction_tracks_three_index_datums_each_and_moving_slot():
    frame = build_left_frame()
    cylindrical_faces = [face for face in frame.faces() if face.geom_type.name == "CYLINDER"]
    assert len(cylindrical_faces) >= 12
    for index in range(3):
        solution = solve_mechanism(upper_index=index, lower_index=index)
        for point in (solution.upper_rod_center, solution.lower_rod_center):
            probe = build_reference_rod(point.y, point.z)
            assert (frame & probe).volume == pytest.approx(0.0, abs=1e-7)
    closed = solve_mechanism(closure=1.0)
    opened = solve_mechanism(closure=0.0)
    for point in (closed.moving_rod_center, opened.moving_rod_center):
        probe = build_reference_rod(point.y, point.z)
        assert (frame & probe).volume == pytest.approx(0.0, abs=1e-7)
    assert closed.moving_rod_center.distance_to(opened.moving_rod_center) == pytest.approx(
        DEFAULT_PARAMETERS.moving_stroke
    )


def _x_centered_cylinder(diameter, length, x, y, z):
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


@pytest.mark.parametrize(("side", "builder"), (("left", build_left_frame), ("right", build_right_frame)))
@pytest.mark.parametrize("wire_gauge", (12, 14))
def test_each_frame_has_six_exact_outer_insert_seats_and_inner_m3_continuations(side, builder, wire_gauge):
    frame = builder(wire_gauge=wire_gauge)
    outward = -1.0 if side == "left" else 1.0
    center_x = outward * (DEFAULT_PARAMETERS.outer_span - FRAME_THICKNESS) / 2.0
    outer_face_x = center_x + outward * FRAME_THICKNESS / 2.0
    inner_face_x = center_x - outward * FRAME_THICKNESS / 2.0
    exact_pocket_x = outer_face_x - outward * REACTION_INSERT_POCKET_DEPTH / 2.0
    floor_x = inner_face_x + outward * 0.25

    datums = []
    for index in range(DEFAULT_PARAMETERS.reaction_position_count):
        solution = solve_mechanism(wire_gauge=wire_gauge, upper_index=index, lower_index=index)
        datums.extend(
            (
                (solution.upper_rod_center.y - REACTION_LOCK_OFFSET, solution.upper_rod_center.z),
                (solution.lower_rod_center.y, solution.lower_rod_center.z + REACTION_LOCK_OFFSET),
            )
        )

    assert len(datums) == 6
    for lock_y, lock_z in datums:
        exact_pocket = _x_centered_cylinder(
            REACTION_INSERT_POCKET_DIAMETER,
            REACTION_INSERT_POCKET_DEPTH,
            exact_pocket_x,
            lock_y,
            lock_z,
        )
        oversize_pocket = _x_centered_cylinder(
            REACTION_INSERT_POCKET_DIAMETER + 0.02,
            REACTION_INSERT_POCKET_DEPTH - 0.2,
            exact_pocket_x,
            lock_y,
            lock_z,
        )
        exact_continuation = _x_centered_cylinder(3.4, 0.4, floor_x, lock_y, lock_z)
        oversize_continuation = _x_centered_cylinder(3.42, 0.3, floor_x, lock_y, lock_z)
        assert (frame & exact_pocket).volume == pytest.approx(0.0, abs=1e-7)
        assert (frame & oversize_pocket).volume > 0.0
        assert (frame & exact_continuation).volume == pytest.approx(0.0, abs=1e-7)
        assert (frame & oversize_continuation).volume > 0.0


@pytest.mark.parametrize(("side", "builder"), (("left", build_left_frame), ("right", build_right_frame)))
@pytest.mark.parametrize("wire_gauge", (12, 14))
def test_actual_frame_brep_has_minimum_structural_wall_at_every_lock_seat(side, builder, wire_gauge):
    frame = builder(wire_gauge=wire_gauge)
    assert frame.is_valid and len(frame.solids()) == 1
    outward = -1.0 if side == "left" else 1.0
    center_x = outward * (DEFAULT_PARAMETERS.outer_span - FRAME_THICKNESS) / 2.0
    outer_face_x = center_x + outward * FRAME_THICKNESS / 2.0
    # Probe within the outer 3.5 mm pocket-depth zone, where both the reaction
    # track and insert seat are present and the ligament is most critical.
    probe_x = outer_face_x - outward * 1.75
    minimum_wall = 2.4

    for index in range(DEFAULT_PARAMETERS.reaction_position_count):
        solution = solve_mechanism(
            wire_gauge=wire_gauge, upper_index=index, lower_index=index
        )
        upper = solution.upper_rod_center
        upper_lock_y = upper.y - REACTION_LOCK_OFFSET
        upper_gap_low = upper_lock_y + REACTION_INSERT_POCKET_DIAMETER / 2.0
        upper_gap_high = upper.y - ROD_BORE_DIAMETER / 2.0
        assert upper_gap_high - upper_gap_low >= minimum_wall
        upper_ligament = Pos(
            probe_x,
            (upper_gap_low + upper_gap_high) / 2.0,
            upper.z,
        ) * Box(
            REACTION_INSERT_POCKET_DEPTH - 0.2,
            minimum_wall,
            0.2,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        upper_exterior = Pos(
            probe_x,
            upper_lock_y - REACTION_INSERT_POCKET_DIAMETER / 2.0 - minimum_wall / 2.0,
            upper.z,
        ) * Box(
            REACTION_INSERT_POCKET_DEPTH - 0.2,
            minimum_wall,
            0.2,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )

        lower = solution.lower_rod_center
        lower_lock_z = lower.z + REACTION_LOCK_OFFSET
        lower_gap_low = lower.z + ROD_BORE_DIAMETER / 2.0
        lower_gap_high = lower_lock_z - REACTION_INSERT_POCKET_DIAMETER / 2.0
        assert lower_gap_high - lower_gap_low >= minimum_wall
        lower_ligament = Pos(
            probe_x,
            lower.y,
            (lower_gap_low + lower_gap_high) / 2.0,
        ) * Box(
            REACTION_INSERT_POCKET_DEPTH - 0.2,
            0.2,
            minimum_wall,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        lower_exterior = Pos(
            probe_x,
            lower.y,
            lower_lock_z + REACTION_INSERT_POCKET_DIAMETER / 2.0 + minimum_wall / 2.0,
        ) * Box(
            REACTION_INSERT_POCKET_DEPTH - 0.2,
            0.2,
            minimum_wall,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )

        for probe in (upper_ligament, upper_exterior, lower_ligament, lower_exterior):
            assert (frame & probe).volume == pytest.approx(probe.volume, rel=1e-6, abs=1e-7)


@pytest.mark.parametrize("side", ("left", "right"))
@pytest.mark.parametrize("kind", ("upper", "lower"))
def test_compact_carrier_has_exact_rod_and_m3_bores_but_no_insert_pocket(side, kind):
    carrier = build_reaction_carrier(side, kind)
    solution = solve_mechanism()
    point = solution.upper_rod_center if kind == "upper" else solution.lower_rod_center
    lock_y, lock_z = (
        (point.y - REACTION_LOCK_OFFSET, point.z)
        if kind == "upper"
        else (point.y, point.z + REACTION_LOCK_OFFSET)
    )
    outward = -1.0 if side == "left" else 1.0
    x = outward * (DEFAULT_PARAMETERS.outer_span / 2.0 + 1.0)
    rod_exact = _x_centered_cylinder(ROD_BORE_DIAMETER, 2.2, x, point.y, point.z)
    rod_oversize = _x_centered_cylinder(ROD_BORE_DIAMETER + 0.02, 1.8, x, point.y, point.z)
    lock_exact = _x_centered_cylinder(3.4, 2.2, x, lock_y, lock_z)
    lock_oversize = _x_centered_cylinder(3.42, 1.8, x, lock_y, lock_z)
    bogus_insert_gauge = _x_centered_cylinder(REACTION_INSERT_POCKET_DIAMETER, 1.8, x, lock_y, lock_z)
    assert (carrier & rod_exact).volume == pytest.approx(0.0, abs=1e-7)
    assert (carrier & rod_oversize).volume > 0.0
    assert (carrier & lock_exact).volume == pytest.approx(0.0, abs=1e-7)
    assert (carrier & lock_oversize).volume > 0.0
    # A Ø4.6 gauge must hit the carrier: the insert seat lives in the frame.
    assert (carrier & bogus_insert_gauge).volume > 0.0
    bounds = carrier.bounding_box()
    assert bounds.size.X == pytest.approx(2.0)
    if kind == "upper":
        assert bounds.size.Y == pytest.approx(REACTION_LOCK_OFFSET + REACTION_LOCK_BOSS_DIAMETER / 2.0 + REACTION_ROD_BOSS_DIAMETER / 2.0)
        assert bounds.size.Z == pytest.approx(REACTION_ROD_BOSS_DIAMETER)
    else:
        assert bounds.size.Y == pytest.approx(REACTION_ROD_BOSS_DIAMETER)
        assert bounds.size.Z == pytest.approx(REACTION_LOCK_OFFSET + REACTION_LOCK_BOSS_DIAMETER / 2.0 + REACTION_ROD_BOSS_DIAMETER / 2.0)


def test_bridge_pocket_includes_connector_envelope_and_side_clearance():
    pocket_width = XT60_ENVELOPE[0] + 2 * XT60_SIDE_CLEARANCE
    pocket_depth = XT60_ENVELOPE[1] + 2 * XT60_SIDE_CLEARANCE
    assert pocket_width == pytest.approx(16.7)
    assert pocket_depth == pytest.approx(8.9)
    bridge = build_xt60_bridge()
    assert bridge.bounding_box().size.X == pytest.approx(
        FRAME_CLEAR_SPAN - 2.0 * DEFAULT_PARAMETERS.running_clearance_per_side
    )
    connector = Pos(0, 0, -3.0) * build_xt60_reference()
    assert (bridge & connector).volume == pytest.approx(0.0, abs=1e-7)
    # Six cylindrical surfaces are the three height holes at both end cheeks.
    assert sum(face.geom_type.name == "CYLINDER" for face in bridge.faces()) >= 6
    assert (FRAME_CLEAR_SPAN - bridge.bounding_box().size.X) / 2.0 == pytest.approx(
        DEFAULT_PARAMETERS.running_clearance_per_side
    )
    for x in (-4.0, 4.0):
        wire_keepout = Pos(x, 0.0, -3.0) * Cylinder(2.4, 10.0)
        assert (bridge & wire_keepout).volume == pytest.approx(0.0, abs=1e-7)


def test_wire_is_swept_on_the_actual_horizontal_r6_vertical_centerline():
    centerline = build_wire_centerline()
    edges = centerline.edges()
    assert [edge.geom_type.name for edge in edges] == ["LINE", "CIRCLE", "LINE"]
    arc = edges[1]
    assert arc.radius == pytest.approx(WIRE_BEND_RADIUS)
    assert arc.arc_center.Y == pytest.approx(WIRE_TANGENT_START_Y)
    assert arc.arc_center.Z == pytest.approx(WIRE_HORIZONTAL_Z + WIRE_BEND_RADIUS)
    assert edges[0].bounding_box().max.Y == pytest.approx(WIRE_TANGENT_START_Y)
    assert edges[0].bounding_box().min.Z == pytest.approx(WIRE_HORIZONTAL_Z)
    assert edges[2].bounding_box().min.Y == pytest.approx(WIRE_VERTICAL_TANGENT_Y)
    wire = build_wire_reference(4.0)
    assert wire.is_valid and wire.volume > 0
    assert any(face.geom_type.name in ("TORUS", "REVOLUTION") for face in wire.faces())
    solution = solve_mechanism()
    assert centerline.length == pytest.approx(solution.path_length)
    assert edges[-1].position_at(1).Z == pytest.approx(solution.wire_endpoint.z)
    assert solution.wire_endpoint.z == pytest.approx(28.5752220392)
    open_path = build_wire_centerline(closure=0.0)
    assert len(open_path.edges()) == 1
    assert open_path.edges()[0].geom_type.name == "LINE"


def test_rod_capture_parts_fit_within_fifty_mm_span_and_clear_actual_rods():
    solution = solve_mechanism()
    rod = build_reference_rod(solution.upper_rod_center.y, solution.upper_rod_center.z)
    assert rod.bounding_box().min.X == pytest.approx(-25.0)
    assert rod.bounding_box().max.X == pytest.approx(25.0)
    for side in ("left", "right"):
        carrier = build_reaction_carrier(side, "upper")
        assert carrier.bounding_box().min.X >= -25.0
        assert carrier.bounding_box().max.X <= 25.0
        assert (carrier & rod).volume == pytest.approx(0.0, abs=1e-7)


def test_diagonal_drive_bore_is_collinear_and_support_is_fused_to_left_frame():
    support = build_left_drive_support()
    bore_face = min(
        (face for face in support.faces() if face.geom_type.name == "CYLINDER"),
        key=lambda face: face.radius,
    )
    axis = bore_face.axis_of_rotation.direction
    solved = solve_mechanism()
    cross = axis.Y * solved.screw_axis_direction.z - axis.Z * solved.screw_axis_direction.y
    assert abs(cross) <= 1e-9
    combined = build_left_frame_with_drive_support()
    assert combined.is_valid and len(combined.solids()) == 1
    assert (build_left_frame() & support).volume > 0.0


def _walk_labels(shape):
    labels = [shape.label]
    for child in getattr(shape, "children", ()):
        labels.extend(_walk_labels(child))
    return labels


def _positive_pairwise_intersections(compound):
    children = list(compound.children)
    return [
        (left.label, right.label, (left & right).volume)
        for index, left in enumerate(children)
        for right in children[index + 1 :]
        if (left & right).volume > 1e-7
    ]


def test_open_and_closed_assemblies_are_labeled_positive_compounds():
    closed = build_closed_assembly()
    opened = build_open_assembly()
    assert isinstance(closed, type(opened))
    assert closed.label == "xt60_bend_jig_closed"
    assert opened.label == "xt60_bend_jig_open"
    assert closed.is_valid and opened.is_valid
    assert closed.volume > 0 and opened.volume > 0
    labels = " ".join(_walk_labels(closed)).lower()
    for required in ("left_upper_reaction_carrier", "right_upper_reaction_carrier", "left_lower_reaction_carrier", "right_lower_reaction_carrier"):
        assert required in labels
    with pytest.raises(ValueError, match="upper-contact-unreachable"):
        build_closed_assembly(upper_index=2)
    assert _positive_pairwise_intersections(closed) == []
    assert _positive_pairwise_intersections(opened) == []
    closed_labels = " ".join(_walk_labels(closed)).lower()
    opened_labels = " ".join(_walk_labels(opened)).lower()
    assert "cold_soldering_iron_keepout" in closed_labels
    for unloaded in ("xt60_envelope", "90_degree_wire", "36x36_esc", "flight_controller", "iron_keepout"):
        assert unloaded not in opened_labels


MATRIX_PARAMETERS = replace(DEFAULT_PARAMETERS, available_lead_length=60.0)


@pytest.mark.parametrize("wire_gauge", (12, 14))
@pytest.mark.parametrize("upper_index", range(3))
@pytest.mark.parametrize("lower_index", range(3))
@pytest.mark.parametrize(("closure", "builder"), ((1.0, build_closed_assembly), (0.0, build_open_assembly)))
def test_full_three_by_three_matrix_is_valid_and_has_zero_unintended_overlap(
    wire_gauge, upper_index, lower_index, closure, builder
):
    assembly = builder(MATRIX_PARAMETERS, wire_gauge, upper_index, lower_index)
    assert assembly.is_valid and assembly.volume > 0.0
    # ``usable`` describes the closed tangency/contact state; an intentionally
    # retracted open state reports open-contact gaps by design.
    closed_solution = solve_mechanism(
        MATRIX_PARAMETERS, wire_gauge, 1.0, upper_index, lower_index
    )
    assert closed_solution.usable
    assert _positive_pairwise_intersections(assembly) == []


def _bounds_overlap(left, right, tolerance=1e-8):
    a, b = left.bounding_box(), right.bounding_box()
    return all(
        low < high - tolerance
        for low, high in (
            (max(a.min.X, b.min.X), min(a.max.X, b.max.X)),
            (max(a.min.Y, b.min.Y), min(a.max.Y, b.max.Y)),
            (max(a.min.Z, b.min.Z), min(a.max.Z, b.max.Z)),
        )
    )


def test_101_point_moving_stroke_clears_every_extreme_reaction_carrier():
    for wire_gauge in (12, 14):
        left_closed = build_left_slider(MATRIX_PARAMETERS, wire_gauge)
        right_closed = build_right_slider(MATRIX_PARAMETERS, wire_gauge)
        closed = solve_mechanism(MATRIX_PARAMETERS, wire_gauge, 1.0)
        for upper_index in (0, 2):
            for lower_index in (0, 2):
                carriers = [
                    build_reaction_carrier(
                        side,
                        kind,
                        MATRIX_PARAMETERS,
                        wire_gauge,
                        upper_index if kind == "upper" else lower_index,
                    )
                    for side in ("left", "right")
                    for kind in ("upper", "lower")
                ]
                for step in range(101):
                    closure = step / 100.0
                    solution = solve_mechanism(
                        MATRIX_PARAMETERS,
                        wire_gauge,
                        closure,
                        upper_index,
                        lower_index,
                    )
                    dy = solution.moving_rod_center.y - closed.moving_rod_center.y
                    dz = solution.moving_rod_center.z - closed.moving_rod_center.z
                    sliders = [
                        Pos(0, dy, dz) * left_closed,
                        Pos(0, dy, dz) * right_closed,
                    ]
                    for slider in sliders:
                        for carrier in carriers:
                            if _bounds_overlap(slider, carrier):
                                assert (slider & carrier).volume <= 1e-7


def test_xt60_reference_distinguishes_exact_body_from_five_mm_solder_cups():
    connector = build_xt60_reference()
    bounds = connector.bounding_box()
    assert connector.label == "reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups"
    assert bounds.size.X == pytest.approx(15.9)
    assert bounds.size.Y == pytest.approx(8.1)
    assert bounds.min.Z == pytest.approx(0.0)
    assert bounds.max.Z == pytest.approx(5.0 + DEFAULT_PARAMETERS.xt60_length)
    exact_body = Pos(0, 0, 5.0) * Box(
        15.9,
        8.1,
        20.5,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    assert (connector & exact_body).volume == pytest.approx(exact_body.volume)
    closed_labels = _walk_labels(build_closed_assembly())
    assert "reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups" in closed_labels
    assert "reference_xt60_envelope" not in closed_labels


def test_print_kit_excludes_all_reference_only_components():
    kit = build_print_kit()
    labels = " ".join(_walk_labels(kit)).lower()
    assert kit.label == "xt60_bend_jig_print_only_kit"
    for excluded in ("reference", "esc", "flight_controller", "wire", "xt60_envelope", "rod_set"):
        assert excluded not in labels
    assert "side_frame" in labels
    assert "bridge_cradle" in labels
    assert "fit_coupon" in labels
    assert labels.count("reaction_carrier") == 4
    assert all("end_cap" not in label for label in _walk_labels(kit))
    assert _positive_pairwise_intersections(kit) == []
