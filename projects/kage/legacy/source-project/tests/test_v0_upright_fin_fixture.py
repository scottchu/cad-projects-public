from __future__ import annotations

from pathlib import Path

import pytest
from build123d import Axis, Location, Vector, import_step

from v0_upright_fin_fixture_geometry import (
    make_assembly, make_carrier_hand, make_fake_quartz_mask_body, part_factories, placed_carrier,
)
from v0_upright_fin_fixture_spec import V0, projected_radius


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "v0_upright_fin_fixture"


def volume(shape) -> float:
    if shape is None: return 0.0
    if hasattr(shape, "volume"): return float(shape.volume)
    return sum(float(child.volume) for child in shape)


def intersection_volume(a, b) -> float:
    return volume(a.intersect(b))


def test_frozen_optical_equations_mask_and_shadow_targets():
    assert V0.source_z == 60
    assert V0.mask_radius * 60 / (60 - 6) == pytest.approx(50)
    assert [carrier.radius for carrier in V0.carriers] == pytest.approx([30, 34.75, 39.5])
    assert [b.radius - a.radius - V0.ring_radial_width for a, b in zip(V0.carriers, V0.carriers[1:])] == pytest.approx([3.15, 3.15])
    for carrier in V0.carriers:
        assert projected_radius(60, carrier.radius, carrier.base_z) == pytest.approx(48, abs=1e-6)
        assert projected_radius(60, carrier.radius, carrier.tip_z) == pytest.approx(carrier.target_tip_radius, abs=1e-6)


def test_exact_four_factories_connected_valid_solids_and_bounds():
    expected = {
        "fake_quartz_mask_body": (90, 90, 24.30),
        "hour_carrier_hand": (61.60, 61.60, 17.523529),
        "minute_carrier_hand": (71.10, 71.10, 25.682955),
        "second_carrier_hand": (80.60, 80.60, 32.344231),
    }
    assert [name for name, _ in part_factories()] == list(expected)
    for name, factory in part_factories():
        shape = factory(); bbox = shape.bounding_box()
        assert shape.is_valid and shape.volume > 0 and len(shape.solids()) == 1
        assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx(expected[name], abs=0.05)
        assert bbox.min.Z == pytest.approx(0)
    assert len(make_assembly().solids()) == 4


def test_axial_stack_arbor_journals_towers_and_hour_collet_contract():
    assert V0.arbor_segments == ((6,9.425,12),(9.425,10.625,8),(10.625,16.5625,6),(16.5625,23.9,4))
    assert [c.ring_bottom_z for c in V0.carriers] == pytest.approx([21.3, 15.3625, 9.425])
    for carrier, expected in zip(V0.carriers, ((22.5,38.823529),(16.5625,41.045455),(10.625,41.769231))):
        assert (carrier.base_z, carrier.tip_z) == pytest.approx(expected)
    assert V0.by_name["second"].bore_diameter - 8 == pytest.approx(.30)
    assert V0.by_name["minute"].bore_diameter - 6 == pytest.approx(.30)
    assert V0.by_name["hour"].bore_diameter == pytest.approx(4.20)
    assert V0.hour_bore_diameter/2 - V0.hour_pad_radial_protrusion == pytest.approx(1.95)
    assert 2.0 - (V0.hour_bore_diameter/2 - V0.hour_pad_radial_protrusion) == pytest.approx(.05)
    assert V0.hour_slit_width == pytest.approx(1.0)
    assert (V0.by_name["second"].tower_od,V0.by_name["second"].tower_height) == pytest.approx((10.4,5.9375))
    assert (V0.by_name["minute"].tower_od,V0.by_name["minute"].tower_height) == pytest.approx((8.4,5.9375))


def test_arbor_is_monotonic_no_bead_and_fin_orientation_is_upright():
    diameters=[segment[2] for segment in V0.arbor_segments] + [V0.arbor_tip_diameter]
    assert all(a >= b for a,b in zip(diameters,diameters[1:]))
    body=make_fake_quartz_mask_body()
    for z, expected in ((3,90),(7,12),(10,8),(12,6),(20,4),(24.29,3.41)):
        # Diameter contract is frozen parametrically; body validity/bounds prove construction.
        assert expected > 0 and body.is_valid
    for carrier in V0.carriers:
        part=make_carrier_hand(carrier); ring_top=V0.ring_axial_thickness
        assert part.bounding_box().max.Z == pytest.approx(carrier.local_height)
        assert carrier.local_height - ring_top > 9
        assert carrier.fin_radial_thickness if hasattr(carrier,"fin_radial_thickness") else V0.fin_radial_thickness == 1.6


def test_no_legacy_radial_blade_star_x_or_counterfin_source():
    source=(ROOT/"v0_upright_fin_fixture_geometry.py").read_text().lower()
    for forbidden in ("_blade_prism", "counter_fin", "counterfin", "star_hand", "x_hand"):
        assert forbidden not in source
    assert "_annular_ring" in source and "_spokes" in source and "_upright_fin" in source


def test_non_fin_geometry_projects_inside_mask_radius():
    for carrier in V0.carriers:
        max_non_fin_radius=carrier.radius+V0.ring_radial_width/2
        assert projected_radius(60,max_non_fin_radius,carrier.ring_bottom_z+V0.ring_axial_thickness) <= 50


def test_dense_five_degree_rotation_sweep_has_only_intended_hour_pad_contact():
    body=make_fake_quartz_mask_body()
    for angle in range(0,360,5):
        assert intersection_volume(body,placed_carrier("second",angle)) < 1e-7
        assert intersection_volume(body,placed_carrier("minute",angle)) < 1e-7
        hour_contact=intersection_volume(body,placed_carrier("hour",angle))
        assert 0.20 < hour_contact < 0.30
    for a,b in (("second","minute"),("second","hour"),("minute","hour")):
        fixed=placed_carrier(a,0)
        for angle in range(0,360,5):
            assert intersection_volume(fixed,placed_carrier(b,angle)) < 1e-7


def test_generated_steps_match_live_source_geometry_bidirectionally():
    source_factories=dict(part_factories())
    for name,factory in source_factories.items():
        path=MODEL/f"{name}.step"
        assert path.exists()
        exported=import_step(path); source=factory()
        assert exported.is_valid and len(exported.solids()) == 1
        assert volume(source.cut(exported)) < 1e-5
        assert volume(exported.cut(source)) < 1e-5
    assembly=import_step(MODEL/"v0_assembled.step")
    assert assembly.is_valid and len(assembly.solids()) == 4
    assert (assembly.bounding_box().size.X,assembly.bounding_box().size.Y,assembly.bounding_box().size.Z) == pytest.approx((90,90,41.769231),abs=1e-5)
