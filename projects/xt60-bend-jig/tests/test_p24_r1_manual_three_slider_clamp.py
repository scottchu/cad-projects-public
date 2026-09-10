from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

import pytest

from xt60_bend_jig import p20_r4_custom_profile_full_cad as p20
from xt60_bend_jig import p24_r1_manual_three_slider_clamp as p24


ROOT = Path(__file__).resolve().parents[3]
CAD_DIR = ROOT / "projects/xt60-bend-jig/cad/p24_r1_manual_three_slider_clamp"


def _load_entry(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_inherited_centers_delegate_exactly_and_clamp_never_changes_yz() -> None:
    for role, name in p24.ROLE_TO_P20_NAME.items():
        for mechanism_progress in (0.0, 0.125, 0.5, 0.875, 1.0):
            inherited = p20.world_rod_center(name, mechanism_progress)
            assert p24.inherited_rod_center(role, mechanism_progress).as_tuple() == pytest.approx(
                inherited.as_tuple(), abs=1.0e-12
            )
            centers = {
                p24.shoe_center(role, mechanism_progress, clamp).as_tuple()
                for clamp in (0.0, 0.25, 0.5, 0.75, 1.0)
            }
            assert centers == {inherited.as_tuple()}


def test_exact_axial_stack_pressure_travel_and_x_mirror() -> None:
    p = p24.P24_R1_DEFAULTS
    assert p.rod_diameter == 4.00
    assert p.rod_length == 50.00
    assert p.socket_depth == 4.00
    assert p.shoe_engagement == 3.70
    assert p.blind_end_clearance == 0.30
    assert p.shoe_socket_id == 4.20
    assert p.frame_thickness == p.pressure_plate_thickness == 3.00
    assert p24.clamp_gap(0.0) == pytest.approx(0.60)
    assert p24.clamp_gap(1.0) == pytest.approx(0.00)

    for clamp in (0.0, 0.4, 1.0):
        left = p24.cassette_x_layout("left", clamp)
        right = p24.cassette_x_layout("right", clamp)
        for field in left.__dataclass_fields__:
            assert getattr(left, field) == pytest.approx(-getattr(right, field), abs=1.0e-12)
        assert abs(right.rod_end_x) == pytest.approx(25.00)
        assert abs(right.rod_end_x - right.socket_open_x) == pytest.approx(3.70)
        assert abs(right.socket_blind_x - right.rod_end_x) == pytest.approx(0.30)
    released = p24.cassette_x_layout("right", 0.0)
    clamped = p24.cassette_x_layout("right", 1.0)
    assert released.pressure_center_x - clamped.pressure_center_x == pytest.approx(0.60)


def test_path_derived_slots_clear_necks_and_capture_flanges() -> None:
    p = p24.P24_R1_DEFAULTS
    evidence = p24.slot_clearance_evidence(p)
    assert evidence["slotOverNeckRadialClearanceMm"] == pytest.approx(0.50)
    assert evidence["flangeOverSlotCaptureMarginMm"] == pytest.approx(0.50)
    assert evidence["minimumScrewAxisToPathCenterMm"] > evidence["requiredScrewAxisToSlotCenterMm"]
    for role in p24.ROLES:
        locus = p24.slot_locus(role, p)
        assert len(locus) == p.relief_sample_count
        for index, point in enumerate(locus):
            u = index / (p.relief_sample_count - 1)
            assert point.as_tuple() == pytest.approx(
                p20.world_rod_center(p24.ROLE_TO_P20_NAME[role], u).as_tuple(), abs=1.0e-12
            )


@pytest.mark.parametrize("state", ("RELEASED_OPEN", "CLAMPED_END"))
def test_required_counts_labels_rods_and_no_caps(state: p24.State) -> None:
    assembly = p24.build_preview(state)
    census = p24.occurrence_census(assembly)
    assert census["rodCount"] == 3
    assert census["capCount"] == 0
    assert census["shoeCount"] == 6
    assert census["frameCount"] == 2
    assert census["pressurePlateCount"] == 2
    assert census["screwEnvelopeCount"] == 2
    assert census["leafCount"] == 24
    assert sum("CONCEPTUAL_THREAD_REACTION_NOT_HELICAL" in label for label in census["labels"]) == 2
    assert sum("CONCEPTUAL_THREAD_NOT_HELICAL_head_knob" in label for label in census["labels"]) == 2

    rods = [leaf for leaf in p24.iter_leaf_shapes(assembly) if "_OD4_rod_L50.00" in leaf.label]
    assert len(rods) == 3
    for rod in rods:
        size = rod.bounding_box().size
        assert size.X == pytest.approx(50.00, abs=1.0e-7)
        assert sorted((size.Y, size.Z)) == pytest.approx([4.00, 4.00], abs=1.0e-7)


@pytest.mark.parametrize("state", ("RELEASED_OPEN", "CLAMPED_END"))
def test_all_leaf_parts_are_single_closed_positive_solids(state: p24.State) -> None:
    leaves = tuple(p24.iter_leaf_shapes(p24.build_preview(state)))
    assert leaves
    for leaf in leaves:
        assert leaf.is_valid, leaf.label
        assert leaf.volume > 0.0, leaf.label
        solids = tuple(leaf.solids())
        assert solids, leaf.label
        assert all(solid.is_valid and solid.volume > 0.0 for solid in solids), leaf.label
        if "workpiece" not in leaf.label:
            assert len(solids) == 1, leaf.label


@pytest.mark.parametrize("state", ("RELEASED_OPEN", "CLAMPED_END"))
def test_no_p24_only_positive_volume_collision_and_named_contacts(state: p24.State) -> None:
    intersections = p24.p24_pairwise_intersections(state)
    assert max(volume for _, _, volume in intersections) <= 1.0e-7

    mechanism, clamp = p24.STATE_COORDINATES[state]
    parts = {
        part.label: part
        for side in p24.SIDES
        for part in p24.module_parts(side, mechanism, clamp)
    }
    for first, second in p24.named_zero_penetration_contacts(state):
        assert float(parts[first].distance(parts[second])) <= 1.0e-7, (first, second)

    if state == "RELEASED_OPEN":
        for side in p24.SIDES:
            plate = parts[f"{side}_common_pressure_plate_T3_clamp_0.00"]
            for role in p24.ROLES:
                shoe = parts[f"{side}_{role}_floating_shoe_socket_ID4p20_flange_D8p20"]
                assert float(plate.distance(shoe)) > 0.0
            layout = p24.cassette_x_layout(side, 0.0)
            assert abs(layout.pressure_inner_x - layout.flange_back_x) == pytest.approx(0.60)


def test_screw_reaction_head_retainer_and_controlled_plate_travel() -> None:
    p = p24.P24_R1_DEFAULTS
    assert p24.screw_backoff(1.0, p) == pytest.approx(0.0)
    assert p.plate_capture_endplay == pytest.approx(0.30)
    assert p24.screw_backoff(0.0, p) == pytest.approx(0.90)
    assert p24.screw_contact_gaps(1.0, p) == pytest.approx(
        {
            "outboardHeadToPlateMm": 0.0,
            "inboardRetainerToPlateMm": 0.30,
            "frameThreadRadialClearanceMm": 0.0,
        }
    )
    assert p24.screw_contact_gaps(0.0, p) == pytest.approx(
        {
            "outboardHeadToPlateMm": 0.30,
            "inboardRetainerToPlateMm": 0.0,
            "frameThreadRadialClearanceMm": 0.0,
        }
    )

    for side in p24.SIDES:
        released_plate = p24.cassette_x_layout(side, 0.0)
        clamped_plate = p24.cassette_x_layout(side, 1.0)
        assert abs(released_plate.pressure_center_x - clamped_plate.pressure_center_x) == pytest.approx(0.60)

        for clamp in (0.0, 1.0):
            frame = p24.build_side_frame(side)
            plate = p24.build_pressure_plate(side, clamp)
            shaft, head, retainer = p24.build_screw_components(side, clamp)
            assert float(frame.distance(shaft)) <= 1.0e-7
            assert p20.p19._intersection_volume(frame, shaft) <= 1.0e-7
            assert p20.p19._intersection_volume(plate, head) <= 1.0e-7
            assert p20.p19._intersection_volume(plate, retainer) <= 1.0e-7
            if clamp == 1.0:
                assert float(plate.distance(head)) <= 1.0e-7
                assert float(plate.distance(retainer)) == pytest.approx(0.30, abs=1.0e-7)
            else:
                assert float(plate.distance(head)) == pytest.approx(0.30, abs=1.0e-7)
                assert float(plate.distance(retainer)) <= 1.0e-7


def test_three_finger_stems_protrude_at_least_five_mm_in_both_states() -> None:
    for side in p24.SIDES:
        for clamp in (0.0, 1.0):
            assert p24.finger_protrusion(side, clamp) >= 5.0
            for role in p24.ROLES:
                shoe = p24.build_shoe(side, role, clamp, clamp)
                pressure = p24.build_pressure_plate(side, clamp)
                if side == "right":
                    actual = shoe.bounding_box().max.X - pressure.bounding_box().max.X
                else:
                    actual = pressure.bounding_box().min.X - shoe.bounding_box().min.X
                assert actual >= 5.0


def test_inherited_xt60_blue_overlap_is_reported_separately() -> None:
    blue = p20.build_rod("bottom", 0.0)
    xt60 = p20.build_xt60_reference()
    assert p20.p19._intersection_volume(blue, xt60) > 0.0


def test_explicit_entry_generators_match_required_states() -> None:
    expected = {
        "p24_r1_released_open.step.py": "RELEASED_OPEN",
        "p24_r1_clamped_end.step.py": "CLAMPED_END",
    }
    for filename, state in expected.items():
        module = _load_entry(CAD_DIR / filename)
        generated = module.gen_step()
        assert generated.label.startswith(f"P24_R1_{state}_")
        assert p24.occurrence_census(generated)["leafCount"] == 24
