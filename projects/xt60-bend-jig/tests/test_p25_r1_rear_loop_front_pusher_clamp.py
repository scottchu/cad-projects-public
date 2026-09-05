from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path

import pytest

from xt60_bend_jig import p20_r4_custom_profile_full_cad as p20
from xt60_bend_jig import p25_r1_rear_loop_front_pusher_clamp as p25


ROOT = Path(__file__).resolve().parents[3]
CAD_DIR = ROOT / "projects/xt60-bend-jig/cad/p25_r1_rear_loop_front_pusher_clamp"


def _load_entry(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_design_dimensions_and_exact_x_stack() -> None:
    p = p25.P25_R1_DEFAULTS
    assert p.rod_od == 4.00
    assert p.rod_length == 50.00
    assert p.rod_end_abs_x == 25.00
    assert p.module_axial_thickness == 3.20
    assert p.hinge_pin_diameter == 2.00
    assert p.released_open_angle == 60.00
    assert p.layer_sum == pytest.approx(3.20)
    for side in p25.SIDES:
        x = p25.axial_layout(side)
        assert x.inboard_abs_x == pytest.approx(21.30)
        assert x.outboard_abs_x == pytest.approx(24.50)
        assert x.rod_end_abs_x - x.outboard_abs_x == pytest.approx(0.50)


def test_inherited_centres_are_exact_and_clamp_state_is_inert() -> None:
    for role, name in p25.ROLE_TO_P20_NAME.items():
        for u in (0.0, 0.25, 0.5, 0.75, 1.0):
            assert p25.inherited_rod_center(role, u).as_tuple() == pytest.approx(
                p20.world_rod_center(name, u).as_tuple(), abs=1.0e-12
            )
        end = p20.world_rod_center(name, 1.0).as_tuple()
        for c in (0.0, 0.25, 0.5, 0.75, 1.0):
            assert p25.clamp_state_rod_center(role, c).as_tuple() == pytest.approx(end, abs=1.0e-12)


@pytest.mark.parametrize("state", p25.STATES)
def test_required_occurrences_rods_and_zero_forbidden_parts(state: p25.State) -> None:
    assembly = p25.build_preview(state)
    census = p25.occurrence_census(assembly)
    assert census["rodCount"] == 3
    assert census["capCount"] == 0
    assert census["rearYokeCount"] == 2
    assert census["frontBarCount"] == 2
    assert census["hingeEnvelopeCount"] == 2
    assert census["springEnvelopeCount"] == 2
    labels = " ".join(census["labels"])
    for forbidden in ("screw", "pressure_plate", "floating_shoe"):
        assert forbidden not in labels.lower()
    rods = [leaf for leaf in p25.iter_leaf_shapes(assembly) if "_OD4_rod_L50.00" in leaf.label]
    for rod in rods:
        size = rod.bounding_box().size
        assert size.X == pytest.approx(50.00, abs=1.0e-7)
        assert sorted((size.Y, size.Z)) == pytest.approx([4.00, 4.00], abs=1.0e-7)


@pytest.mark.parametrize("state", p25.STATES)
def test_left_right_modules_are_x_mirrored_with_same_yz_bounds(state: p25.State) -> None:
    left = p25.module_parts("left", state)
    right = p25.module_parts("right", state)
    for a, b in zip(left, right, strict=True):
        ba, bb = a.bounding_box(), b.bounding_box()
        assert ba.min.X == pytest.approx(-bb.max.X, abs=1.0e-7)
        assert ba.max.X == pytest.approx(-bb.min.X, abs=1.0e-7)
        assert ba.min.Y == pytest.approx(bb.min.Y, abs=1.0e-7)
        assert ba.max.Y == pytest.approx(bb.max.Y, abs=1.0e-7)
        assert ba.min.Z == pytest.approx(bb.min.Z, abs=1.0e-7)
        assert ba.max.Z == pytest.approx(bb.max.Z, abs=1.0e-7)


@pytest.mark.parametrize("state", p25.STATES)
def test_every_p25_part_is_one_valid_positive_closed_solid(state: p25.State) -> None:
    for side in p25.SIDES:
        for part in p25.module_parts(side, state):
            assert part.is_valid, part.label
            assert part.volume > 0.0, part.label
            solids = tuple(part.solids())
            assert len(solids) == 1, part.label
            assert solids[0].is_valid and solids[0].volume > 0.0


def test_latched_named_contacts_are_tangent_and_only_target_intended_rods() -> None:
    for side in p25.SIDES:
        table = p25.rod_contact_table(side, "LATCHED_END")
        for name in ("rearYokeBlue", "rearYokeGreen", "frontBarOrange"):
            assert table[name]["distance"] <= 1.0e-7, name
            assert table[name]["intersection"] <= 1.0e-7, name
        for name in ("frontBarBlue", "frontBarGreen", "rearYokeOrange"):
            assert table[name]["distance"] > 0.0, name
            assert table[name]["intersection"] <= 1.0e-7, name


@pytest.mark.parametrize("state", p25.STATES)
def test_no_new_positive_volume_collision_within_p25_or_context(state: p25.State) -> None:
    assert max((v for _, _, v in p25.p25_pairwise_intersections(state)), default=0.0) <= 1.0e-7
    new_parts = [part for side in p25.SIDES for part in p25.module_parts(side, state)]
    for new_part, context in combinations(new_parts + p25._context(p20.P20_R4_DEFAULTS), 2):
        if new_part not in new_parts and context not in new_parts:
            continue
        assert p20.p19._intersection_volume(new_part, context) <= 1.0e-7, (
            new_part.label,
            context.label,
        )


def test_open_states_and_60_degree_sweep_clear_orange_without_gravity() -> None:
    p = p25.P25_R1_DEFAULTS
    for side in p25.SIDES:
        for state in ("PRECLAMP_END", "RELEASED_CLEAR"):
            table = p25.rod_contact_table(side, state)
            assert table["frontBarOrange"]["distance"] >= p.released_orange_clearance
        sweep = p25.sweep_clearances(side)
        assert set(sweep) == {0.0, 10.0, 30.0, 60.0}
        assert sweep[0.0]["orange"] <= 1.0e-7
        for angle in (10.0, 30.0, 60.0):
            assert min(sweep[angle].values()) > 0.0
        assert sweep[60.0]["orange"] >= p.released_orange_clearance
    assert p25.state_angle("RELEASED_CLEAR") == pytest.approx(60.0)
    assert p25.latch_release_gap() >= 0.60


def test_spring_envelope_is_isolated_and_remains_an_unverified_envelope() -> None:
    for side in p25.SIDES:
        spring = p25.build_opening_spring_envelope(side)
        assert "UNVERIFIED" in spring.label
        for state in p25.STATES:
            for part in p25.module_parts(side, state):
                if part.label == spring.label:
                    continue
                assert p20.p19._intersection_volume(spring, part) <= 1.0e-7
        for name in p20.ROD_NAMES:
            assert p20.p19._intersection_volume(spring, p20.build_rod(name, 1.0)) <= 1.0e-7


def test_inherited_open_blue_xt60_collision_is_reported_separately() -> None:
    assert p25.inherited_baseline_collision_mm3() > 0.0


def test_explicit_entry_generators_cover_three_states_and_exploded() -> None:
    expected = {
        "p25_r1_preclamp_end.step.py": "PRECLAMP_END",
        "p25_r1_latched_end.step.py": "LATCHED_END",
        "p25_r1_released_clear.step.py": "RELEASED_CLEAR",
    }
    for filename, state in expected.items():
        generated = _load_entry(CAD_DIR / filename).gen_step()
        assert generated.label.startswith(f"P25_R1_{state}_")
    exploded = _load_entry(CAD_DIR / "p25_r1_modules_exploded.step.py").gen_step()
    assert exploded.label == "P25_R1_LEFT_RIGHT_MODULES_EXPLODED"
