from dataclasses import replace
from pathlib import Path

import pytest

from halo_experiment_spec import DEFAULT_PHONE_HALO, PhoneHaloExperiment


ROOT = Path(__file__).resolve().parents[1]


def test_starting_geometry_is_internally_consistent():
    h = DEFAULT_PHONE_HALO
    h.validate()
    assert h.magnification == pytest.approx(47 / 35)
    assert h.projected_inner_diameter_mm == pytest.approx(87.2857, abs=0.001)
    assert h.projected_outer_diameter_mm == pytest.approx(141.0)
    assert h.projected_ring_width_mm == pytest.approx(26.8571, abs=0.001)
    assert h.first_order_edge_transition_mm == pytest.approx(12 / 7)


def test_diffuser_changes_edge_model_not_mask_geometry():
    bare = DEFAULT_PHONE_HALO
    diffuse = replace(bare, effective_source_diameter_mm=20.0)
    assert diffuse.projected_inner_diameter_mm == bare.projected_inner_diameter_mm
    assert diffuse.projected_outer_diameter_mm == bare.projected_outer_diameter_mm
    assert diffuse.first_order_edge_transition_mm == pytest.approx(
        4 * bare.first_order_edge_transition_mm
    )


def test_scale_to_260mm_preserves_body_relative_geometry_only():
    h = DEFAULT_PHONE_HALO
    assert h.final_scale == pytest.approx(4.0)
    assert h.scaled_wall_gap_mm == pytest.approx(48.0)
    assert h.scaled_halo_outer_diameter_mm == pytest.approx(564.0)


@pytest.mark.parametrize(
    "candidate",
    [
        PhoneHaloExperiment(body_mask_diameter_mm=0),
        PhoneHaloExperiment(outer_aperture_diameter_mm=65),
        PhoneHaloExperiment(source_to_mask_mm=0),
        PhoneHaloExperiment(mask_to_wall_mm=-1),
        PhoneHaloExperiment(effective_source_diameter_mm=0),
    ],
)
def test_invalid_physical_configs_are_rejected(candidate):
    with pytest.raises(ValueError):
        candidate.validate()


def test_research_page_is_the_concise_upright_fin_reference():
    html = (ROOT / "research.html").read_text()
    assert "Axial height becomes a radial shadow" in html
    assert "does not use long flat hands" in html
    assert "HIDDEN CARRIERS + UPRIGHT RIM FINS" in html
    assert "fin r30" in html and "fin r34.75" in html and "fin r39.5" in html
    assert "phone flash" in html.lower()


def test_wired_point_led_purchase_chain_is_explicit_and_current_limited():
    html = (ROOT / "research.html").read_text()
    for token in (
        "Cree XQ-E",
        "350 mA constant-current driver",
        "regulated supply",
        "aluminum heatsink",
        "never hot-plug the LED output",
    ):
        assert token in html
