from __future__ import annotations

from itertools import combinations
from math import cos, hypot, pi, radians, sin, sqrt
from pathlib import Path

import pytest
from build123d import Vector, import_step

import xt60_bend_jig.p11_asymmetric_three_rod_solder_jig as p11


def intersection_volume(first, second) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return common.volume
    return sum(item.volume for item in common)


def compound_intersection_volume(shape, compound) -> float:
    return sum(intersection_volume(shape, child) for child in compound.children)


def shape_bounds(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return (*box.min, *box.max)


def leaf_shapes(shape):
    if not shape.children:
        return [shape]
    leaves = []
    for child in shape.children:
        leaves.extend(leaf_shapes(child))
    return leaves


def bottom_planar_area(shape, tolerance: float = 1e-6) -> float:
    """Area of all horizontal faces lying exactly on the Z=0 print bed."""
    return sum(
        face.area
        for face in shape.faces()
        if face.bounding_box().size.Z <= tolerance
        and abs(face.bounding_box().min.Z) <= tolerance
    )


def test_default_contract_and_exact_compact_axial_stack() -> None:
    p = p11.P11_DEFAULTS
    assert (p.rod_diameter, p.rod_length) == (4.0, 50.0)
    assert p.d1 == 7.0
    assert p.bend_radius == 6.0
    assert p.wire_entry_z == 43.0
    assert p.body_bottom_z == 48.0
    assert p.axial_body == pytest.approx(37.2)
    assert p.rod_projection == pytest.approx(6.4)
    assert (p.left_fixed_x, p.left_cam_x, p.right_fixed_x, p.right_cam_x) == pytest.approx(
        (-14.4, -17.35, 14.4, 17.35)
    )


@pytest.mark.parametrize("radius", (5.0, 6.0, 7.0))
def test_radius_derived_contacts_are_exact_tangencies(radius: float) -> None:
    p = p11.P11Parameters(bend_radius=radius)
    rho = (p.wire_diameter + p.rod_diameter) / 2.0
    upright = p11.closed_rod_center("upright", p)
    bottom = p11.closed_rod_center("bottom", p)
    diagonal = p11.closed_rod_center("diagonal", p)
    assert upright == p11.PointYZ(-rho, p.horizontal_z + 2.0 * radius)
    assert bottom == p11.PointYZ(2.0 * radius, p.horizontal_z - rho)
    arc_center = p11.PointYZ(radius, p.horizontal_z + radius)
    assert diagonal.distance_to(arc_center) == pytest.approx(radius - rho, abs=1e-9)
    if radius == 6.0:
        assert (upright.y, upright.z) == pytest.approx((-4.15, 42.0), abs=1e-9)
        assert (bottom.y, bottom.z) == pytest.approx((12.0, 25.85), abs=1e-9)
        assert (diagonal.y, diagonal.z) == pytest.approx(
            (4.691852455, 34.691852455), abs=1e-9
        )


@pytest.mark.parametrize("radius", (5.0, 6.0, 7.0))
@pytest.mark.parametrize("d1", (6.0, 7.0, 8.0))
def test_wire_cup_body_chain_has_exact_face_continuity(radius: float, d1: float) -> None:
    p = p11.P11Parameters(bend_radius=radius, d1=d1)
    assert p.vertical_tangent_z == p.horizontal_z + radius
    assert p.wire_entry_z == p.vertical_tangent_z + d1
    assert p.body_bottom_z == p.wire_entry_z + 5.0
    assert p.body_bottom_z - p.wire_entry_z == p.cup_height


def test_invalid_parameter_ranges_fail_closed() -> None:
    with pytest.raises(ValueError):
        p11.P11Parameters(bend_radius=4.99)
    with pytest.raises(ValueError):
        p11.P11Parameters(d1=8.01)
    with pytest.raises(ValueError):
        p11.P11Parameters(rod_length=49.0)


def test_role_specific_motion_is_monotonic_ordered_and_has_true_dwell() -> None:
    samples = [i / 10.0 for i in range(351)]
    for name in p11.ROD_NAMES:
        fractions = [p11.travel_fraction(name, angle) for angle in samples]
        assert all(b >= a - 1e-12 for a, b in zip(fractions, fractions[1:]))
    assert p11.travel_fraction("upright", 20.0) == 1.0
    assert p11.travel_fraction("bottom", 20.0) < 1.0
    assert p11.travel_fraction("bottom", 27.0) == 1.0
    assert p11.travel_fraction("diagonal", 27.0) < 1.0
    assert p11.travel_fraction("diagonal", 32.0) == 1.0
    for name in p11.ROD_NAMES:
        frozen = p11.rod_center(name, 32.0)
        for angle in (32.1, 33.0, 34.99, 35.0):
            assert p11.rod_center(name, angle) == frozen
    diagonal_27 = p11.rod_center("diagonal", 27.0)
    assert diagonal_27.distance_to(p11.closed_rod_center("diagonal")) == pytest.approx(
        0.72174072265625, abs=1e-9
    )


def test_inverse_slots_reconstruct_each_independent_law() -> None:
    p = p11.P11_DEFAULTS
    for side in ("left", "right"):
        assert side in ("left", "right")
        for name in p11.ROD_NAMES:
            for i in range(141):
                angle = p.end_angle * i / 140.0
                q = p11.inverse_slot_point(name, angle, p)
                a = radians(angle)
                dy, dz = q.y - p.shaft_y, q.z - p.shaft_z
                reconstructed = p11.PointYZ(
                    p.shaft_y + cos(a) * dy - sin(a) * dz,
                    p.shaft_z + sin(a) * dy + cos(a) * dz,
                )
                assert reconstructed.distance_to(p11.rod_center(name, angle, p)) <= 1e-9


def test_slot_edge_and_inter_slot_webs_across_radius_variants() -> None:
    for radius in (5.0, 6.0, 7.0):
        p = p11.P11Parameters(bend_radius=radius)
        worst_edge = 999.0
        worst_pair = 999.0
        for i in range(141):
            angle = p.end_angle * i / 140.0
            points = {name: p11.inverse_slot_point(name, angle, p) for name in p11.ROD_NAMES}
            for point in points.values():
                radial = point.distance_to(p.shaft_center)
                worst_edge = min(worst_edge, p.plate_diameter / 2.0 - radial - p.follower_cam_lane / 2.0)
            names = list(p11.ROD_NAMES)
            for a, b in ((names[0], names[1]), (names[0], names[2]), (names[1], names[2])):
                worst_pair = min(worst_pair, points[a].distance_to(points[b]) - p.follower_cam_lane)
        # Locked load paths remain above 3.0; the R7 open diagonal endpoint is
        # the documented low-load exception and stays above 2.4 with error.
        assert worst_edge - sqrt(2.0) * p.construction_offset >= 2.4
        assert worst_pair >= 3.0


def test_static_cam_slot_web_uses_independent_theta_phi_minimum() -> None:
    angles = [index * 0.5 for index in range(71)]
    for radius in (5.0, 6.0, 7.0):
        p = p11.P11Parameters(bend_radius=radius)
        worst = min(
            p11.inverse_slot_point(first, theta, p).distance_to(
                p11.inverse_slot_point(second, phi, p)
            ) - p.follower_cam_lane
            for first, second in combinations(p11.ROD_NAMES, 2)
            for theta in angles
            for phi in angles
        )
        assert worst >= 3.0


def test_left_terminal_pockets_measure_4p4_normal_to_path() -> None:
    p = p11.P11_DEFAULTS
    cam = p11.build_cam_plate("left", p)
    for name in p11.ROD_NAMES:
        q = p11.inverse_slot_point(name, p.end_angle, p)
        # STEP-safe cam paths use 0.25-degree terminal facets; measure normal
        # to the actual final segment rather than an analytic spline tangent.
        before = p11.inverse_slot_point(name, p.end_angle - 0.25, p)
        ty, tz = q.y - before.y, q.z - before.z
        length = hypot(ty, tz)
        dy, dz = -tz / length, ty / length

        def material_at(distance: float) -> bool:
            return cam.is_inside(Vector(p.left_cam_x, q.y + dy * distance, q.z + dz * distance))

        boundaries: list[float] = []
        for sign in (-1.0, 1.0):
            low, high = 0.0, 3.0
            for _ in range(12):
                middle = (low + high) / 2.0
                if material_at(sign * middle):
                    high = middle
                else:
                    low = middle
            boundaries.append(sign * (low + high) / 2.0)
        assert boundaries[1] - boundaries[0] == pytest.approx(4.4, abs=0.01)


def test_exactly_four_full_56mm_principal_discs_and_three_rods() -> None:
    p = p11.P11_DEFAULTS
    plates = p11.build_principal_plates(35.0, p)
    rods = p11.build_rods(35.0, p)
    assert len(plates.children) == 4
    assert len(rods.children) == 3
    for plate in plates.children:
        box = plate.bounding_box()
        assert box.size.Y <= 56.0 + 1e-6
        assert box.size.Z <= 61.0 + 1e-7  # Ø56 blank plus the compact 5 mm base tongue
    for rod in rods.children:
        box = rod.bounding_box()
        assert box.size.X == pytest.approx(50.0)
        assert box.size.Y == pytest.approx(4.0)
        assert box.size.Z == pytest.approx(4.0)


def test_closed_rods_touch_without_positive_workpiece_overlap() -> None:
    p = p11.P11_DEFAULTS
    workpiece = p11.build_workpiece(p)
    for angle in (0.0, 20.0, 27.0, 32.0, 35.0):
        rods = p11.build_rods(angle, p)
        assert compound_intersection_volume(workpiece, rods) <= 1e-6


def test_open_body_and_cups_vertical_sweep_has_clearance_and_zero_brep_overlap() -> None:
    p = p11.P11_DEFAULTS
    open_centers = [p11.rod_center(name, 0.0, p) for name in p11.ROD_NAMES]

    def point_rect_distance(point: p11.PointYZ, half_y: float, z_min: float) -> float:
        dy = max(abs(point.y) - half_y, 0.0)
        dz = max(z_min - point.z, 0.0)
        return hypot(dy, dz)

    for point in open_centers:
        body_gap = point_rect_distance(point, p.xt60_y / 2.0, p.body_bottom_z) - p.rod_diameter / 2.0
        cup_gap = point_rect_distance(point, p.cup_diameter / 2.0, p.wire_entry_z) - p.rod_diameter / 2.0
        assert min(body_gap, cup_gap) >= p.load_clearance

    sweep = p11.build_loading_sweep(p)
    obstacles = [p11.build_base(p), p11.build_shaft(0.0, p),
                 *p11.build_principal_plates(0.0, p).children,
                 *p11.build_rods(0.0, p).children]
    for swept_part in sweep.children:
        for obstacle in obstacles:
            assert intersection_volume(swept_part, obstacle) <= 1e-7
    assert "flexible_wire" in p11.build_loaded_open(p).label


def test_relieved_follower_accepts_construction_error_and_height_delta() -> None:
    p = p11.P11_DEFAULTS
    assert p.follower_guide_width - p.rod_diameter >= 2.0 * p.construction_offset
    assert p.follower_cam_lane - p.rod_diameter >= 2.0 * p.construction_offset
    assert p11.construction_height_delta(p) == pytest.approx(0.1388888889)
    assert p11.construction_height_delta(p) <= 0.20


def test_actual_offset_follower_cutters_accept_rods_through_full_stroke() -> None:
    p = p11.P11_DEFAULTS
    nominal_fixed_box = shape_bounds(p11.build_fixed_plate("right", p))
    nominal_cam_box = shape_bounds(p11.build_cam_plate("right", p))
    for offset in p11.FOLLOWER_ERROR_OFFSETS:
        fixed = p11.build_fixed_plate("right", p, offset)
        cam = p11.build_cam_plate("right", p, offset)
        assert shape_bounds(fixed) == pytest.approx(nominal_fixed_box, abs=1e-7)
        assert shape_bounds(cam) == pytest.approx(nominal_cam_box, abs=1e-7)
        for step in range(141):
            angle = step / 4.0
            rotated_cam = p11._rotate_about_shaft(cam, angle, p)
            for name in p11.ROD_NAMES:
                rod = p11.build_rod(name, angle, p)
                assert intersection_volume(rod, fixed) <= 1e-7
                assert intersection_volume(rod, rotated_cam) <= 1e-7


def test_three_station_solder_sweeps_pass_strict_obstacles() -> None:
    p = p11.P11_DEFAULTS
    plates = p11.build_principal_plates(p.end_angle, p)
    rods = p11.build_rods(p.end_angle, p)
    xt60 = p11.build_xt60(p)
    wires = p11.build_wires(p)
    electronics = p11.build_electronics_reference(p)
    retainers = list(p11.build_retainers(p.end_angle, p).children)
    printed = [p11.build_base(p), p11.build_shaft(p.end_angle, p),
               p11.build_shaft_keeper(p), *plates.children, *retainers]
    for index, x in enumerate((-p.wire_x, p.wire_x)):
        tool = p11.build_solder_tool_sweep(x, p)
        for obstacle in [*printed, *rods.children, *xt60.children,
                         electronics.children[0], electronics.children[1],
                         electronics.children[2 + 2 * (1 - index)],
                         electronics.children[3 + 2 * (1 - index)],
                         wires.children[1 - index]]:
            assert intersection_volume(tool, obstacle) <= 1e-7
        assert intersection_volume(tool, wires.children[index]) > 0.20
        intended_solder = electronics.children[3 + 2 * index]
        assert intersection_volume(tool, intended_solder) > 0.15


def test_detent_indexes_open_and_lock_and_hard_stop_is_exact() -> None:
    p = p11.P11_DEFAULTS
    fixed = p11.build_fixed_plate("right", p)
    cam = p11.build_cam_plate("right", p)
    for angle in (0.0, p.end_angle):
        rotated = p11._rotate_about_shaft(cam, angle, p)
        assert intersection_volume(fixed, rotated) <= 1e-7
    assert intersection_volume(fixed, p11._rotate_about_shaft(cam, 17.5, p)) > 0.1

    clearances = [p11.stop_signed_clearance(angle, p) for angle in (34.99, 35.0, 35.01, 36.0)]
    assert clearances[0] > 0.0
    assert clearances[1] == pytest.approx(0.0, abs=1e-12)
    assert clearances[2] < 0.0
    assert clearances[3] < 0.0
    pin = p11.build_stop_pin(p)
    for angle, should_overlap in ((34.99, False), (35.0, False), (35.01, True), (36.0, True)):
        rotated = p11._rotate_about_shaft(cam, angle, p)
        volume = intersection_volume(pin, rotated)
        assert (volume > 1e-6) is should_overlap


def test_relocated_stop_clears_every_R5_R6_R7_rod_pose() -> None:
    for radius in (5.0, 6.0, 7.0):
        p = p11.P11Parameters(bend_radius=radius)
        pin = p11.build_stop_pin(p)
        for index in range(71):
            angle = index / 2.0
            for name in p11.ROD_NAMES:
                assert intersection_volume(pin, p11.build_rod(name, angle, p)) <= 1e-7


def test_seated_base_mortises_fix_guides_without_squeezing_cams() -> None:
    p = p11.P11_DEFAULTS
    base = p11.build_base(p)
    for side in ("left", "right"):
        assert intersection_volume(base, p11.build_fixed_plate(side, p)) <= 1e-7
        assert intersection_volume(base, p11.build_cam_plate(side, p)) <= 1e-7


def test_raw_crush_ribs_interfere_but_seated_envelope_is_clear() -> None:
    p = p11.P11_DEFAULTS
    base = p11.build_base(p)
    for side in ("left", "right"):
        raw = p11.build_fixed_plate(side, p, seated=False)
        seated = p11.build_fixed_plate(side, p, seated=True)
        assert intersection_volume(base, raw) > 1.0
        assert intersection_volume(base, seated) <= 1e-7
        assert "raw_integral_crush_ribs" in raw.label
        assert "seated_zero_overlap_crush_rib_envelope" in seated.label


def test_right_inserted_shaft_and_separate_keeper_have_continuous_clear_paths() -> None:
    p = p11.P11_DEFAULTS
    sweep = p11.build_shaft_insertion_sweep(p)
    obstacles = [p11.build_base(p), *p11.build_principal_plates(0.0, p).children]
    for swept_part in sweep.children:
        for obstacle in obstacles:
            assert intersection_volume(swept_part, obstacle) <= 1e-7
    shaft = p11.build_shaft(0.0, p)
    keeper = p11.build_shaft_keeper(p)
    assert intersection_volume(shaft, keeper) <= 1e-7
    assert all(intersection_volume(keeper, plate) <= 1e-7
               for plate in p11.build_principal_plates(0.0, p).children)
    assert intersection_volume(p11.build_shaft_keeper_escape_sweep(p), shaft) <= 1e-7
    assert "integral_right_head_passable_left_neck" in shaft.label


def test_fallback_rod_withdrawal_and_core_removal_sweeps_are_clear() -> None:
    p = p11.P11_DEFAULTS
    plates = p11.build_principal_plates(0.0, p)
    shaft = p11.build_shaft(0.0, p)
    for name in p11.ROD_NAMES:
        swept = p11.build_rod_withdraw_sweep(name, p)
        for obstacle in [*plates.children, shaft]:
            assert intersection_volume(swept, obstacle) <= 1e-6
    core_sweep = p11.build_core_remove_sweep(p)
    electronics = p11.build_electronics_reference(p)
    workpiece = p11.build_workpiece(p)
    for obstacle in [*electronics.children, *workpiece.children]:
        assert intersection_volume(core_sweep, obstacle) <= 1e-6
    final_keeper = p11.build_shaft_keeper(p, p.core_remove_y)
    assert intersection_volume(core_sweep, final_keeper) == pytest.approx(
        final_keeper.volume, abs=1e-6
    )


def test_intact_open_removal_is_explicitly_blocked_before_fallback() -> None:
    failed_sweep = p11.build_intact_open_removal_failure_sweep()
    assert "first_blocker_diagonal_rod" in failed_sweep.label
    assert intersection_volume(failed_sweep, p11.build_workpiece()) > 1.0


def test_all_right_keepers_escape_minusY_without_crossing_their_own_rods() -> None:
    p = p11.P11_DEFAULTS
    assert p.keeper_remove_y < 0.0
    for name in p11.ROD_NAMES:
        sweep = p11.build_right_keeper_escape_sweep(name, p)
        rod = p11.build_rod(name, 0.0, p)
        assert intersection_volume(sweep, rod) <= 1e-7
        assert "minusY_escape" in sweep.label


def test_required_generators_exist_without_touching_p10_namespace() -> None:
    root = Path(__file__).parents[1]
    folder = root / "cad" / "p11_asymmetric_three_rod_solder_jig"
    expected = {
        "p11_loaded_open.step.py", "p11_loaded_closed.step.py",
        "p11_solder_access.step.py", "p11_rods_withdrawn.step.py",
        "p11_removal_clear.step.py", "p11_exploded.step.py",
        "p11_print_kit.step.py", "p11_fit_coupon.step.py",
    }
    assert {path.name for path in folder.glob("*.step.py")} == expected


def test_print_kit_is_non_overlapping_and_fits_180mm_square_bed() -> None:
    kit = p11.build_print_kit()
    box = kit.bounding_box()
    assert box.size.X <= 180.0
    assert box.size.Y <= 180.0
    for index, first in enumerate(kit.children):
        for second in kit.children[index + 1:]:
            assert intersection_volume(first, second) <= 1e-7


def test_print_kit_small_retainers_lie_flat_and_cap_sockets_open_up() -> None:
    kit = p11.build_print_kit()
    by_label = {}
    for child in kit.children:
        by_label.setdefault(child.label, []).append(child)

    shaft_keeper, = by_label["separate_left_shaft_C_keeper_removable_minusY"]
    shaft_box = shaft_keeper.bounding_box()
    assert shaft_box.min.Z == pytest.approx(0.0, abs=1e-7)
    assert shaft_box.size.Z == pytest.approx(1.8, abs=1e-7)
    assert bottom_planar_area(shaft_keeper) == pytest.approx(
        shaft_keeper.volume / 1.8, abs=1e-6
    )

    rod_keepers = by_label["right_circular_C_keeper_4p10_plusY_open_remove_minusY"]
    assert len(rod_keepers) == 3
    for keeper in rod_keepers:
        box = keeper.bounding_box()
        assert box.min.Z == pytest.approx(0.0, abs=1e-7)
        assert box.size.Z == pytest.approx(2.9, abs=1e-7)
        assert bottom_planar_area(keeper) == pytest.approx(
            keeper.volume / 2.9, abs=1e-6
        )

    caps = by_label["left_rod_cap_3p90_tight_trial"]
    assert len(caps) == 3
    for cap in caps:
        box = cap.bounding_box()
        center = Vector(
            (box.min.X + box.max.X) / 2.0,
            (box.min.Y + box.max.Y) / 2.0,
            0.0,
        )
        assert box.min.Z == pytest.approx(0.0, abs=1e-7)
        assert box.size.Z == pytest.approx(3.7, abs=1e-7)
        assert bottom_planar_area(cap) == pytest.approx(pi * 3.5**2, abs=1e-6)
        # Closed disk at the bed, socket void at the top: the blind socket's
        # axis and opening both point +Z.
        assert cap.is_inside(center + Vector(0.0, 0.0, 0.1))
        assert not cap.is_inside(center + Vector(0.0, 0.0, box.max.Z - 0.1))


def test_right_rod_keeper_has_circular_outer_profile_and_open_throat() -> None:
    p = p11.P11_DEFAULTS
    point = p11.rod_center("upright", p.end_angle, p)
    keeper = p11.build_right_keeper(point, p)
    box = keeper.bounding_box()
    x = (box.min.X + box.max.X) / 2.0

    assert box.size.X == pytest.approx(p.rod_keeper_thickness, abs=1e-7)
    assert box.size.Z == pytest.approx(p.rod_keeper_outer, abs=1e-7)
    assert box.min.Y == pytest.approx(point.y - p.rod_keeper_outer / 2.0, abs=1e-7)
    assert box.max.Y < point.y + p.rod_keeper_outer / 2.0
    assert all(
        ((vertex.Y - point.y) ** 2 + (vertex.Z - point.z) ** 2) ** 0.5
        <= p.rod_keeper_outer / 2.0 + 1e-7
        for vertex in keeper.vertices()
    )
    # The -Y bridge remains solid while the +Y throat is open.
    assert keeper.is_inside(Vector(x, point.y - 3.0, point.z))
    assert not keeper.is_inside(Vector(x, point.y + 3.0, point.z))


def test_all_generated_steps_match_source_leaf_geometry_when_present() -> None:
    root = Path(__file__).parents[1]
    folder = root / "cad" / "p11_asymmetric_three_rod_solder_jig"
    cases = (
        ("p11_loaded_open.step", p11.build_loaded_open()),
        ("p11_loaded_closed.step", p11.build_loaded_closed()),
        ("p11_solder_access.step", p11.build_solder_access()),
        ("p11_rods_withdrawn.step", p11.build_rods_withdrawn()),
        ("p11_removal_clear.step", p11.build_removal_clear()),
        ("p11_exploded.step", p11.build_exploded()),
        ("p11_print_kit.step", p11.build_print_kit()),
        ("p11_fit_coupon.step", p11.build_fit_coupon()),
    )
    if not all((folder / filename).exists() for filename, _ in cases):
        pytest.skip("P11 STEP artifacts not generated yet")

    for filename, source in cases:
        imported = import_step(folder / filename)
        assert imported.is_valid
        assert imported.label == source.label
        assert shape_bounds(imported) == pytest.approx(shape_bounds(source), abs=2e-6)
        imported_leaves = leaf_shapes(imported)
        source_leaves = leaf_shapes(source)
        assert [leaf.label for leaf in imported_leaves] == [leaf.label for leaf in source_leaves]
        assert len(imported_leaves) == len(source_leaves)
        for imported_leaf, source_leaf in zip(imported_leaves, source_leaves):
            assert shape_bounds(imported_leaf) == pytest.approx(
                shape_bounds(source_leaf), abs=2e-6
            )
            assert len(imported_leaf.solids()) == len(source_leaf.solids())
            assert len(imported_leaf.faces()) == len(source_leaf.faces())
            assert imported_leaf.volume == pytest.approx(
                source_leaf.volume, rel=1e-8, abs=1e-6
            )
