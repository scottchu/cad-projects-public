"""BREP fit, insertion, and dimensional tests for P0 v3 C1-C4 coupons."""

import math

import pytest
from build123d import Align, Box, Location, Vector

from pill_click.p0_v3 import (
    C1R1,
    C1R1B,
    C2_LEGACY,
    P0V3,
    make_c4_snap_arm,
    make_c4_snap_coupon,
    make_c4_snap_receiver,
    make_c1r1_rail_coupon,
    make_c2_legacy_rail_coupon,
    make_shutter_track_coupon,
)
from pill_click.p0_v3.coupons import _make_c4_snap_arm_rootless
from pill_click.p0_v3.geometry import _box_bounds, _make_snap_root_prism


BREP_TOLERANCE = 1e-6


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    center: tuple[float, float, float],
):
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(center))


def _spec_bbox(shape) -> tuple[float, float, float, float, float, float]:
    """Return min-X, min-Y, min-Z, max-X, max-Y, max-Z."""

    bbox = shape.bounding_box()
    return (bbox.min.X, bbox.min.Y, bbox.min.Z, bbox.max.X, bbox.max.Y, bbox.max.Z)


def _intersection_volume(first, second) -> float:
    return (first & second).volume


def _rail_coupon_parts(*, variant: str):
    if variant == "c1r1":
        children = make_c1r1_rail_coupon().children
    elif variant == "c1r1b":
        children = make_c1r1_rail_coupon(thick_lip=True).children
    elif variant == "c2":
        children = make_c2_legacy_rail_coupon().children
    else:
        raise ValueError(variant)
    rail = next(child for child in children if "rail_carrier" in child.label)
    receiver = next(child for child in children if "receiver" in child.label)
    return rail, receiver


@pytest.mark.parametrize(
    ("variant", "rail_bbox", "receiver_bbox"),
    [
        ("c1r1", (-1.2, 0.0, -3.5, 2.0, 22.4, 3.5), (-3.4, -3.4, -3.5, -0.75, 3.4, 3.5)),
        ("c1r1b", (-1.2, 0.0, -3.5, 2.0, 22.4, 3.5), (-3.4, -3.4, -3.5, -0.75, 3.4, 3.5)),
        ("c2", (-1.2, 0.0, -3.5, 2.0, 19.0, 3.5), (-3.4, -1.7, -3.5, -0.75, 1.7, 3.5)),
    ],
)
def test_rail_coupons_are_two_valid_single_solid_parts_with_exact_bboxes(
    variant: str,
    rail_bbox,
    receiver_bbox,
) -> None:
    rail, receiver = _rail_coupon_parts(variant=variant)
    assert rail.is_valid and receiver.is_valid
    assert len(rail.solids()) == len(receiver.solids()) == 1
    assert _spec_bbox(rail) == pytest.approx(rail_bbox)
    assert _spec_bbox(receiver) == pytest.approx(receiver_bbox)


def test_c1r1_c1r1b_and_c2_actual_sections_and_positive_y_mouths() -> None:
    p = P0V3
    nominal_rail, nominal_receiver = _rail_coupon_parts(variant="c1r1")
    thick_rail, thick_receiver = _rail_coupon_parts(variant="c1r1b")
    loose_rail, loose_receiver = _rail_coupon_parts(variant="c2")
    assert nominal_rail.volume == pytest.approx(thick_rail.volume)
    assert nominal_rail.volume > loose_rail.volume
    assert thick_receiver.volume > nominal_receiver.volume > loose_receiver.volume

    # A section just after the ramp has the exact 1.20 radial projection and
    # 2.20 tangential width; a section near Y=0 still has almost zero projection.
    full_section = nominal_rail & _box(4.0, 0.02, 7.0, (0.0, 0.71, 0.0))
    early_section = nominal_rail & _box(4.0, 0.02, 7.0, (0.0, 0.05, 0.0))
    assert full_section.bounding_box().min.X == pytest.approx(-p.rail_radial_height)
    assert (full_section & _box(1.2, 0.02, 2.2, (-0.6, 0.71, 0.0))).volume == pytest.approx(
        1.2 * 0.02 * p.rail_tangential_width, rel=1e-6
    )
    assert early_section.bounding_box().min.X > -0.20

    variants = (
        (nominal_receiver, C1R1),
        (thick_receiver, C1R1B),
        (loose_receiver, C2_LEGACY),
    )
    for receiver, variant in variants:
        groove_width = variant.groove_width
        groove_bottom = variant.groove_bottom_x
        mouth_bottom = variant.mouth_bottom_x
        groove_void = _box(
            -0.75 - groove_bottom - 0.02,
            0.40,
            groove_width - 0.02,
            ((groove_bottom - 0.75) / 2, 0.0, 0.0),
        )
        mouth_void = _box(
            -0.75 - mouth_bottom - 0.02,
            p.groove_mouth_length - 0.02,
            groove_width + p.groove_mouth_extra_width - 0.02,
            ((mouth_bottom - 0.75) / 2, variant.land_length / 2 - 0.30, 0.0),
        )
        assert _intersection_volume(receiver, groove_void) < BREP_TOLERANCE
        assert _intersection_volume(receiver, mouth_void) < BREP_TOLERANCE
        # The same deep/wide probe is solid at the negative-Y end, proving the
        # 0.60 mouth belongs only to the positive-Y leading edge.
        negative_y_probe = mouth_void.moved(Location((0.0, -variant.land_length + 0.60, 0.0)))
        assert _intersection_volume(receiver, negative_y_probe) > BREP_TOLERANCE


@pytest.mark.parametrize(
    ("variant_name", "variant", "normal_lip", "mouth_lip"),
    [
        ("c1r1", C1R1, 0.80, 0.60),
        ("c1r1b", C1R1B, 1.20, 1.00),
    ],
)
def test_strengthened_coupon_brep_probes_measure_both_lips_independently(
    variant_name: str,
    variant,
    normal_lip: float,
    mouth_lip: float,
) -> None:
    p = P0V3
    _, receiver = _rail_coupon_parts(variant=variant_name)
    half_boss = variant.bearing_boss_width / 2
    half_groove = variant.groove_width / 2
    half_mouth = (variant.groove_width + p.groove_mouth_extra_width) / 2

    for side in (-1.0, 1.0):
        normal_z = side * (half_groove + normal_lip / 2)
        normal_probe = _box(
            0.64,
            0.10,
            normal_lip - 0.02,
            (-1.075, 0.0, normal_z),
        )
        assert _intersection_volume(receiver, normal_probe) == pytest.approx(
            normal_probe.volume, rel=1e-6
        )

        mouth_z = side * (half_mouth + mouth_lip / 2)
        mouth_probe = _box(
            0.94,
            0.10,
            mouth_lip - 0.02,
            (-1.225, half_boss * 0 + variant.land_length / 2 - 0.30, mouth_z),
        )
        assert _intersection_volume(receiver, mouth_probe) == pytest.approx(
            mouth_probe.volume, rel=1e-6
        )

    assert half_boss - half_groove == pytest.approx(normal_lip)
    assert half_boss - half_mouth == pytest.approx(mouth_lip)


@pytest.mark.parametrize(
    ("variant", "insertion_start", "inward_center", "center_offset"),
    [
        ("c1r1", -3.40, 4.30, 5.30),
        ("c1r1b", -3.40, 4.30, 5.30),
        ("c2", -1.70, 2.60, 3.60),
    ],
)
def test_rail_coupon_insertion_and_full_hard_range_sweeps_are_collision_free(
    variant: str,
    insertion_start: float,
    inward_center: float,
    center_offset: float,
) -> None:
    p = P0V3
    rail, receiver = _rail_coupon_parts(variant=variant)
    count = int(round((inward_center - insertion_start) / 0.05)) + 1
    insertion_centers = [insertion_start + 0.05 * index for index in range(count)]
    hard_range_states = [-1.0 + 0.05 * index for index in range(292)]
    hard_range_states.append(p.maximum_pull_state)
    assert insertion_centers[-1] == pytest.approx(inward_center)
    assert hard_range_states[-1] == pytest.approx(13.55)

    for center_y in insertion_centers:
        assert _intersection_volume(rail, Location((0.0, center_y, 0.0)) * receiver) < BREP_TOLERANCE
    for state in hard_range_states:
        center_y = center_offset + state
        assert _intersection_volume(rail, Location((0.0, center_y, 0.0)) * receiver) < BREP_TOLERANCE


def _c3_parts():
    children = make_shutter_track_coupon().children
    receiver = next(child for child in children if "receiver" in child.label)
    slider = next(child for child in children if "slider" in child.label)
    return receiver, slider


def test_c3_parts_are_valid_single_solids_with_exact_bboxes() -> None:
    receiver, slider = _c3_parts()
    assert receiver.is_valid and slider.is_valid
    assert len(receiver.solids()) == len(slider.solids()) == 1
    assert _spec_bbox(receiver) == pytest.approx((-15.9, 0.0, -2.0, 15.9, 32.0, 2.0))
    assert _spec_bbox(slider) == pytest.approx((-13.7, -6.0, 0.2, 13.7, 6.0, 1.8))


def test_c3_actual_section_clearances_capture_and_opposed_lead_directions() -> None:
    p = P0V3
    receiver, slider = _c3_parts()
    combined = slider & _box(0.1, 2.0, 2.0, (12.40, 0.0, 1.0))
    flange = slider & _box(0.1, 2.0, 2.0, (12.60, 0.0, 1.0))
    web_plan = slider & _box(25.0, 2.0, 0.78, (0.0, 0.0, 1.40))
    flange_plan = slider & _box(27.4, 2.0, 0.78, (0.0, 0.0, 0.60))
    assert flange.bounding_box().size.Z == pytest.approx(p.shutter_flange_thickness)
    assert combined.bounding_box().size.Z - flange.bounding_box().size.Z == pytest.approx(
        p.shutter_web_thickness
    )
    assert web_plan.bounding_box().size.X == pytest.approx(p.shutter_web_width)
    assert flange_plan.bounding_box().size.X == pytest.approx(p.shutter_flange_width)

    assembled = Location((0.0, 9.30, 0.0)) * slider
    assert _intersection_volume(receiver, assembled) < BREP_TOLERANCE
    assert (p.track_flange_width - p.shutter_flange_width) / 2 == pytest.approx(0.20)
    assert (p.track_web_width - p.shutter_web_width) / 2 == pytest.approx(0.20)
    assert 0.20 - 0.00 == pytest.approx(p.track_floor_clearance)
    assert 1.20 - 1.00 == pytest.approx(p.track_vertical_clearance)
    assert (p.shutter_flange_width - p.track_web_width) / 2 == pytest.approx(1.00)

    # Receiver mouth is negative-Y; a widened slot probe fits only Y=0..0.8.
    receiver_mouth = _box(28.18, 0.78, 1.18, (0.0, 0.40, 0.60))
    receiver_normal = receiver_mouth.moved(Location((0.0, 1.0, 0.0)))
    assert _intersection_volume(receiver, receiver_mouth) < BREP_TOLERANCE
    assert _intersection_volume(receiver, receiver_normal) > BREP_TOLERANCE

    # Slider taper is positive-Y and remains a solid 25x0.8 web throughout.
    lead_crop = slider & _box(28.0, 0.80, 2.0, (0.0, 5.60, 1.0))
    rear_crop = slider & _box(28.0, 0.80, 2.0, (0.0, -5.60, 1.0))
    assert lead_crop.volume < rear_crop.volume
    assert (slider & _box(24.9, 0.78, 0.78, (0.0, 5.60, 1.40))).volume == pytest.approx(
        24.9 * 0.78 * 0.78, rel=1e-6
    )


def test_c3_insertion_and_operational_sweeps_are_collision_free() -> None:
    receiver, slider = _c3_parts()
    insertion_centers = [-6.0 + 0.05 * index for index in range(307)]
    operational_centers = [9.30 + 0.05 * index for index in range(269)]
    assert insertion_centers[-1] == pytest.approx(9.30)
    assert operational_centers[-1] == pytest.approx(22.70)
    for center_y in [*insertion_centers, *operational_centers]:
        assert _intersection_volume(receiver, Location((0.0, center_y, 0.0)) * slider) < BREP_TOLERANCE


def test_c4_parts_are_valid_single_solids_with_exact_bboxes() -> None:
    arm = make_c4_snap_arm()
    receiver = make_c4_snap_receiver()
    coupon = make_c4_snap_coupon()
    assert arm.is_valid and receiver.is_valid and coupon.is_valid
    assert len(arm.solids()) == len(receiver.solids()) == 1
    assert _spec_bbox(arm) == pytest.approx((-2.0, -3.0, -6.0, 1.75, 8.85, 6.0))
    assert _spec_bbox(receiver) == pytest.approx((1.2, 0.0, -6.0, 3.05, 10.5, 6.0))
    assert _intersection_volume(arm, receiver) < BREP_TOLERANCE


def test_c4_v31_exact_root_prism_overlap_and_arm_volume_accounting() -> None:
    p = P0V3
    root = _make_snap_root_prism(p)
    grip = _box_bounds((-2.0, 1.2), (-3.0, 0.0), (-6.0, 6.0))
    beam = _box_bounds((0.0, 1.2), (0.0, 8.85), (-1.8, 1.8))
    rootless = _make_c4_snap_arm_rootless(p)
    arm = make_c4_snap_arm(p)
    expected_relief_area = p.rear_snap_root_fillet**2 * (1.0 - math.pi / 4.0)
    expected_profile_area = (
        p.rear_snap_root_overlap
        * (p.rear_snap_root_fillet + p.rear_snap_root_overlap)
        + p.rear_snap_root_overlap * p.rear_snap_root_tangent_y
        + expected_relief_area
    )
    expected_gross_volume = expected_profile_area * p.rear_snap_width
    expected_net_addition = expected_gross_volume - 0.720000 - 0.576000

    assert root.is_valid and len(root.solids()) == 1
    assert _spec_bbox(root) == pytest.approx((-0.8, -0.2, -1.8, 0.2, 0.8, 1.8))
    assert root.volume / p.rear_snap_width == pytest.approx(
        0.497345175425633, abs=1e-12
    )
    assert expected_relief_area == pytest.approx(0.137345175425633, abs=1e-12)
    assert root.volume == pytest.approx(1.790442631532279, abs=1e-12)
    assert root.volume == pytest.approx(expected_gross_volume, abs=1e-12)
    assert _intersection_volume(root, grip) == pytest.approx(0.720000, abs=1e-9)
    assert _intersection_volume(root, beam) == pytest.approx(0.576000, abs=1e-9)
    assert expected_net_addition == pytest.approx(0.494442631532279, abs=1e-12)
    assert rootless.volume == pytest.approx(154.521000000000, abs=1e-9)
    assert arm.volume - rootless.volume == pytest.approx(
        expected_net_addition, abs=1e-9
    )
    assert arm.volume == pytest.approx(155.015442631532, abs=1e-9)
    assert arm.volume - 155.194104837031 == pytest.approx(
        -0.178662205499, abs=1e-9
    )


def test_c4_actual_beam_hook_pocket_outer_skin_and_root_fillet() -> None:
    p = P0V3
    arm = make_c4_snap_arm()
    receiver = make_c4_snap_receiver()
    beam_probe = _box(1.2, 6.0, 3.6, (0.60, 4.0, 0.0))
    assert _intersection_volume(arm, beam_probe) == pytest.approx(beam_probe.volume, rel=1e-6)
    assert arm.bounding_box().max.X - p.rear_snap_bending_thickness == pytest.approx(0.55)
    assert p.rear_snap_hook_apex_y - p.rear_snap_hook_base_rear_y == pytest.approx(0.55)
    assert p.rear_snap_hook_base_front_y - p.rear_snap_hook_apex_y == pytest.approx(0.55)

    pocket_probe = _box(0.64, 1.08, 3.98, (1.52, 8.30, 0.0))
    outer_skin_probe = _box(1.19, 1.0, 3.0, (2.45, 8.30, 0.0))
    assert _intersection_volume(receiver, pocket_probe) < BREP_TOLERANCE
    assert _intersection_volume(receiver, outer_skin_probe) == pytest.approx(
        outer_skin_probe.volume, rel=1e-6
    )

    # The exact R0.80 boundary and finite 0.20 overlaps retain the intended
    # concave stress relief without an endpoint-only or epsilon connection.
    assert arm.is_inside(Vector(-0.10, 0.20, 0.0), tolerance=1e-7)
    assert not arm.is_inside(Vector(-0.80, 0.80, 0.0), tolerance=1e-7)


def test_c4_deflected_envelope_clears_receiver_during_full_insertion() -> None:
    p = P0V3
    arm = make_c4_snap_arm()
    receiver = make_c4_snap_receiver()
    # Worst rigid envelope of the flexed arm: move the entire arm away from
    # the wall by the hook protrusion. This proves the non-hook remainder clears;
    # strain is checked separately rather than pretending the undeflected arm
    # is collision-free during snap-through.
    deflected = Location((-p.rear_snap_nominal_deflection, 0.0, 0.0)) * arm
    insertion_offsets = [-8.85 + 0.05 * index for index in range(178)]
    insertion_offsets.append(0.0)
    for offset_y in insertion_offsets:
        assert _intersection_volume(
            Location((0.0, offset_y, 0.0)) * deflected,
            receiver,
        ) < BREP_TOLERANCE


def test_c4_named_strain_clearance_and_packaging_equations() -> None:
    p = P0V3
    effective_length = p.rear_snap_hook_apex_y - 0.80
    nominal_strain = (
        1.5
        * p.rear_snap_bending_thickness
        * p.rear_snap_nominal_deflection
        / effective_length**2
    )
    worst_strain = (
        1.5
        * p.rear_snap_bending_thickness
        * p.rear_snap_worst_deflection
        / effective_length**2
    )
    arm_front_world_y = p.rear_faceplate_interior_y + p.rear_snap_local_front_y
    future_inward_shuttle_rear_y = p.latched_center_y + p.shuttle_inward_state + p.shuttle_rear_local_y
    assert effective_length == pytest.approx(p.rear_snap_effective_length)
    assert nominal_strain == pytest.approx(0.0176, abs=1e-4)
    assert worst_strain == pytest.approx(0.0208, abs=1e-4)
    assert worst_strain < 0.03
    assert (4.0 - p.rear_snap_width) / 2 == pytest.approx(0.20)
    assert 3.05 - 1.85 == pytest.approx(1.20)
    assert future_inward_shuttle_rear_y - arm_front_world_y == pytest.approx(0.35)
    assert (-p.rear_snap_center_x, p.rear_snap_center_x) == pytest.approx((-16.2, 16.2))
