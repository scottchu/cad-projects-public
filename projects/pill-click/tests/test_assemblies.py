"""Variant separation and labeled assembly checks."""

import pytest

from pill_click.assembly import make_magnet_assembly, make_spring_assembly
from pill_click.parameters import DEFAULTS


def _labels(assembly) -> set[str]:
    return {child.label for child in assembly.children}


def test_spring_assembly_has_exactly_two_returns_and_no_return_magnets() -> None:
    assembly = make_spring_assembly()
    labels = _labels(assembly)
    spring_labels = {label for label in labels if label.startswith("spring_return:")}

    assert assembly.is_valid
    assert spring_labels == {"spring_return:left", "spring_return:right"}
    assert not any(label.startswith("return_magnet_carrier:") for label in labels)


def test_magnet_assembly_has_one_pair_no_springs_and_captured_caps() -> None:
    assembly = make_magnet_assembly(minimum_gap=1.2)
    labels = _labels(assembly)

    assert assembly.is_valid
    assert not any(label.startswith("spring_return:") for label in labels)
    assert {label for label in labels if label.startswith("return_magnet_carrier:")} == {
        "return_magnet_carrier:fixed",
        "return_magnet_carrier:moving",
    }
    assert {label for label in labels if label.startswith("return_magnet_cap:")} == {
        "return_magnet_cap:fixed",
        "return_magnet_cap:moving",
    }


@pytest.mark.parametrize("minimum_gap", [0.8, 1.2, 1.6])
def test_magnet_ready_gap_includes_full_14_4_mm_span(minimum_gap: float) -> None:
    assembly = make_magnet_assembly(minimum_gap=minimum_gap)
    by_label = {child.label: child for child in assembly.children}
    fixed = by_label["return_magnet_carrier:fixed"].bounding_box()
    moving = by_label["return_magnet_carrier:moving"].bounding_box()

    assert moving.min.Y - fixed.max.Y == pytest.approx(
        minimum_gap + DEFAULTS.total_press_span
    )
