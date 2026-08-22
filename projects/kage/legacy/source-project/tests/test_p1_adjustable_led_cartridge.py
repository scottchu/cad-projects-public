from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest
from build123d import Align, Box, Compound, Cylinder, Location, import_step

from p1_adjustable_led_cartridge_geometry import (
    PRINTABLE_FACTORIES,
    make_assembly,
    make_axial_xz_section_review,
    make_emitter_reference,
    make_fixed_references,
    make_free_air_envelope,
    make_heatsink_reference,
    make_integration_reference_assembly,
    make_mcpcb_reference,
    make_moving_carriage,
    make_rail_frame,
    make_rear_service_bridge,
    make_review_assembly,
    make_service_exploded,
    make_stack_references,
    placed_carriage,
    placed_strain_relief,
    service_bridge_transform,
    service_carriage_transform,
    wire_u_loop_metrics,
)
from p1_adjustable_led_cartridge_spec import P1, validate_spec


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p1_adjustable_led_cartridge"


def intersection_volume(a, b) -> float:
    """Robust collision volume for solids or positioned Compounds.

    build123d Compound.intersect can silently return None for overlapping child
    solids, so every collision contract explicitly evaluates every solid pair.
    """
    total = 0.0
    for solid_a in a.solids():
        for solid_b in b.solids():
            overlap = solid_a.intersect(solid_b)
            if overlap is not None:
                total += sum(float(solid.volume) for solid in overlap.solids())
    return total


def test_compound_collision_helper_detects_known_child_overlap():
    a = Compound(children=[Box(2, 2, 2).moved(Location((-5, 0, 0))), Box(2, 2, 2)])
    b = Compound(children=[Box(2, 2, 2).moved(Location((5, 0, 0))), Box(1, 1, 1)])
    assert intersection_volume(a, b) == pytest.approx(1.0)


def all_labels(shape) -> list[str]:
    labels = [shape.label or ""]
    for child in getattr(shape, "children", ()) or ():
        labels.extend(all_labels(child))
    return labels


def test_frozen_spec_positions_distances_axis_and_travel():
    validate_spec()
    assert P1.travel == pytest.approx(50.0)
    assert P1.source_positions == pytest.approx((36.0, 40.0, 86.0))
    assert P1.mask_distances == pytest.approx((30.0, 34.0, 80.0))
    for source_z in P1.source_positions:
        emitter = make_emitter_reference(source_z)
        bbox = emitter.bounding_box()
        assert (bbox.center().X, bbox.center().Y, bbox.max.Z) == pytest.approx((0, 0, source_z))


def test_metal_stack_rigid_offsets_follow_source_plane():
    for source_z in range(36, 87, 2):
        mcpcb = make_mcpcb_reference(source_z)
        heatsink = make_heatsink_reference(source_z)
        assert mcpcb.bounding_box().min.Z == pytest.approx(source_z)
        assert mcpcb.bounding_box().max.Z == pytest.approx(source_z + P1.mcpcb_thickness)
        assert heatsink.bounding_box().min.Z == pytest.approx(source_z + P1.heatsink_front_offset)
        assert heatsink.bounding_box().max.Z == pytest.approx(source_z + P1.heatsink_rear_offset)
        assert heatsink.bounding_box().center().X == pytest.approx(0)
        assert heatsink.bounding_box().center().Y == pytest.approx(0)


def test_petg_never_occupies_mcpcb_disk_or_central_hot_base_footprint():
    carriage = make_moving_carriage()
    mcpcb_zone = Cylinder(
        P1.mcpcb_diameter / 2,
        P1.mcpcb_thickness + 0.02,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, -0.01)))
    hot_zone = Box(
        P1.hot_base_footprint,
        P1.hot_base_footprint,
        P1.heatsink_base,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, P1.mcpcb_thickness)))
    assert intersection_volume(carriage, mcpcb_zone) < 1e-8
    assert intersection_volume(carriage, hot_zone) < 1e-8


def test_rail_clearance_engagement_and_frame_envelope():
    frame = make_rail_frame()
    bbox = frame.bounding_box()
    assert bbox.size.X <= P1.frame_max_x
    assert bbox.size.Y <= P1.frame_max_y
    assert (bbox.min.Z, bbox.max.Z) == pytest.approx((28.0, 96.0))
    assert P1.rail_clearance_size - P1.rail_y_size == pytest.approx(0.60)
    assert P1.rail_x_clearance_size - P1.rail_x_size == pytest.approx(0.60)
    assert P1.bearing_land >= 12.0
    for source_z in range(36, 87):
        # Rail containment is intentional, but the 0.30 mm per-side channel
        # means the two actual solids remain collision-free over the full sweep.
        assert intersection_volume(frame, placed_carriage(source_z)) < 1e-7


def test_hard_stops_are_exact_source_planes():
    assert P1.front_stop_top_z + P1.carriage_stop_tab_half_height == P1.source_z_min
    assert P1.rear_stop_bottom_z - P1.carriage_stop_tab_half_height == P1.source_z_max
    for source_z in (P1.source_z_min, P1.source_z_max):
        assert intersection_volume(make_rail_frame(), placed_carriage(source_z)) < 1e-7
    assert intersection_volume(make_rear_service_bridge(), placed_carriage(P1.source_z_max)) < 1e-7
    assert intersection_volume(make_rail_frame(), placed_carriage(P1.source_z_min - 0.1)) > 5.0
    assert intersection_volume(make_rear_service_bridge(), placed_carriage(P1.source_z_max + 0.1)) > 5.0


def test_dense_swept_collision_checks_excluding_guide_containment_contact():
    frame = make_rail_frame()
    bridge = make_rear_service_bridge()
    for index in range(201):
        source_z = P1.source_z_min + P1.travel * index / 200
        carriage = placed_carriage(source_z)
        assert intersection_volume(frame, carriage) < 1e-7
        assert intersection_volume(bridge, carriage) < 1e-7


def test_required_free_air_volume_has_zero_fixed_printable_brep_intersection_at_201_states():
    frame = make_rail_frame()
    bridge = make_rear_service_bridge()
    for index in range(201):
        source_z = P1.source_z_min + P1.travel * index / 200
        free_air = make_free_air_envelope(source_z)
        assert intersection_volume(frame, free_air) < 1e-7
        assert intersection_volume(bridge, free_air) < 1e-7


def test_only_four_quantified_cool_edge_clips_interrupt_moving_air_envelope():
    expected = 4 * P1.edge_clip_depth * P1.edge_clip_width * P1.edge_clip_height
    for source_z in P1.source_positions:
        interruption = intersection_volume(placed_carriage(source_z), make_free_air_envelope(source_z))
        assert interruption == pytest.approx(expected, abs=1e-6)
        assert interruption == pytest.approx(288.0)
        assert intersection_volume(placed_carriage(source_z), make_heatsink_reference(source_z)) < 1e-7


def test_free_air_pla_and_driver_keepout_math():
    assert P1.free_air_half_x - P1.heatsink_x / 2 >= 5.0
    assert P1.decorative_keepout_half_x - P1.heatsink_x / 2 >= 10.0
    assert P1.heatsink_depth + P1.free_air_rear == pytest.approx(35.0)
    driver_nearest_x = 75.0 - 10.0
    assert driver_nearest_x - P1.heatsink_x / 2 >= P1.driver_clearance


def test_wire_u_loop_slack_anchor_and_minimum_bend_radius():
    metrics = wire_u_loop_metrics()
    assert metrics == {
        "nominal_length": 80.0,
        "travel": 50.0,
        "slack_after_travel": 30.0,
        "minimum_bend_radius": 15.0,
        "moving_anchor_offset": 12.0,
    }
    assert metrics["slack_after_travel"] >= 2 * metrics["minimum_bend_radius"]


def test_service_bridge_removal_transform_and_path_are_clear():
    frame = make_rail_frame()
    bridge = make_rear_service_bridge()
    for index in range(1, 81):
        moved = bridge.moved(service_bridge_transform(index / 80))
        assert intersection_volume(frame, moved) < 1e-7
    removed = bridge.moved(service_bridge_transform(1.0))
    assert removed.bounding_box().min.Z > frame.bounding_box().max.Z
    carriage = placed_carriage(P1.source_z_default)
    stack = make_stack_references(P1.source_z_default)
    for index in range(81):
        transform = service_carriage_transform(index / 80)
        assert intersection_volume(frame, carriage.moved(transform)) < 1e-7
        assert intersection_volume(frame, stack.moved(transform)) < 1e-7
    assert carriage.moved(service_carriage_transform(1)).bounding_box().min.Z > frame.bounding_box().max.Z
    assert make_service_exploded().is_valid


def test_strain_relief_clip_has_clearanced_retained_slide_interface_and_moves_with_carriage():
    local_carriage = make_moving_carriage()
    local_clip = placed_strain_relief(0)
    assert intersection_volume(local_carriage, local_clip) < 1e-7
    assert P1.clip_mount_clearance == pytest.approx(0.30)
    mount_center = (32.0, 16.0)
    assert local_carriage.bounding_box().min.X < mount_center[0] < local_carriage.bounding_box().max.X
    for index in range(201):
        source_z = P1.source_z_min + P1.travel * index / 200
        clip = placed_strain_relief(source_z)
        carriage = placed_carriage(source_z)
        assert intersection_volume(clip, carriage) < 1e-7
        assert clip.bounding_box().min.Z == pytest.approx(source_z - 4.5)


def test_no_unrequested_light_control_part_symbols():
    banned = ("diffuser", "lens", "reflector", "secondary_optic")
    labels = [label.lower() for label in all_labels(make_assembly())]
    assert not any(token in label for token in banned for label in labels)


def test_all_printable_and_reference_shapes_are_valid_positive_volume_solids():
    shapes = [factory() for _, factory in PRINTABLE_FACTORIES]
    shapes.extend(
        [
            make_stack_references(P1.source_z_default),
            make_fixed_references(P1.source_z_default),
            make_assembly(P1.source_z_min),
            make_assembly(P1.source_z_default),
            make_assembly(P1.source_z_max),
            make_service_exploded(),
            make_review_assembly(),
            make_axial_xz_section_review(),
        ]
    )
    for shape in shapes:
        assert shape.is_valid
        solids = list(shape.solids())
        assert solids
        assert all(solid.is_valid and solid.volume > 0 for solid in solids)
    assert len(make_rail_frame().solids()) == 1
    assert len(make_moving_carriage().solids()) == 1


def test_nonprintable_integration_story_preserves_v0r2_and_stationary_support_clearance():
    integration = make_integration_reference_assembly()
    labels = [label.lower() for label in all_labels(integration)]
    assert any("wall_z0" in label for label in labels)
    assert any("standalone_v0r2_quartz_and_moving_carriers" in label for label in labels)
    assert any("stationary_kage_bridge" in label for label in labels)
    assert any("glare_shield_mounting_datum_only_no_dome" in label for label in labels)
    assert any("room_side_viewer_datum" in label for label in labels)
    assert any("wall_facing_led_optical_axis_open_path" in label for label in labels)
    assert P1.rail_z_min - P1.v0r2_keepout_z_max == pytest.approx(2.154)
    assert integration.is_valid


def test_generator_entries_and_expected_primary_steps_exist_after_build():
    stems = (
        "rail_frame",
        "moving_carriage",
        "rear_service_bridge",
        "strain_relief_clip",
        "p1_assembled_min",
        "p1_assembled_default",
        "p1_assembled_max",
        "p1_service_exploded",
    )
    for stem in stems:
        assert (MODEL_ROOT / f"{stem}.step.py").exists()
        assert (MODEL_ROOT / f"{stem}.step").exists()


def test_generated_part_breps_enforce_sweep_air_hot_zone_and_real_stops():
    frame = import_step(MODEL_ROOT / "rail_frame.step")
    bridge = import_step(MODEL_ROOT / "rear_service_bridge.step")
    carriage_local = import_step(MODEL_ROOT / "moving_carriage.step")
    assert len(carriage_local.solids()) == 1

    mcpcb_zone = Cylinder(
        P1.mcpcb_diameter / 2,
        P1.mcpcb_thickness + 0.02,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, -0.01)))
    hot_zone = Box(
        P1.hot_base_footprint,
        P1.hot_base_footprint,
        P1.heatsink_base,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, P1.mcpcb_thickness)))
    assert intersection_volume(carriage_local, mcpcb_zone) < 1e-7
    assert intersection_volume(carriage_local, hot_zone) < 1e-7

    for index in range(201):
        source_z = P1.source_z_min + P1.travel * index / 200
        carriage = carriage_local.moved(Location((0, 0, source_z)))
        free_air = make_free_air_envelope(source_z)
        assert intersection_volume(frame, carriage) < 1e-7
        assert intersection_volume(bridge, carriage) < 1e-7
        assert intersection_volume(frame, free_air) < 1e-7
        assert intersection_volume(bridge, free_air) < 1e-7

    min_interference = intersection_volume(
        frame, carriage_local.moved(Location((0, 0, P1.source_z_min - 0.1)))
    )
    max_interference = intersection_volume(
        bridge, carriage_local.moved(Location((0, 0, P1.source_z_max + 0.1)))
    )
    assert min_interference > 5.0
    assert max_interference == pytest.approx(6.4, abs=0.05)


def test_p1_is_isolated_from_frozen_v0r2_source_generators_and_print_bundle():
    v0r2_paths = [
        ROOT / "v0r2_identifiable_fin_fixture_spec.py",
        ROOT / "v0r2_identifiable_fin_fixture_geometry.py",
        ROOT / "v0r2_identifiable_fin_fixture_export.py",
        *sorted((ROOT / "models" / "v0r2_identifiable_fin_fixture").glob("*.step.py")),
        ROOT / "models" / "v0r2_identifiable_fin_fixture" / "print" / "v0r2_manifest.json",
    ]
    for path in v0r2_paths:
        assert path.exists()
        text = path.read_text(errors="ignore").lower()
        assert "p1_adjustable_led_cartridge" not in text
        assert "adjustable_led_cartridge" not in text
    bundle = (
        ROOT
        / "models"
        / "v0r2_identifiable_fin_fixture"
        / "print"
        / "v0r2_four_part_identifiable_fin_test.3mf"
    )
    assert bundle.exists()
    with ZipFile(bundle) as package:
        contents = b"".join(package.read(name) for name in package.namelist()).lower()
    assert b"p1_adjustable_led_cartridge" not in contents
    assert b"adjustable_led_cartridge" not in contents
    keepout_labels = [
        label.lower()
        for label in all_labels(make_fixed_references(P1.source_z_default))
    ]
    assert "reference_v0r2_keepout_r40p3_zminus16_to_27p846_nonprintable" in keepout_labels
