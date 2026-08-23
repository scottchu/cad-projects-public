"""Fresh-process STEP parity checks for the MR84 tower handoff."""

from __future__ import annotations

from pathlib import Path

import pytest
from build123d import import_step

import p3_v3_mr84_spool_tower_export as exporter
import p3_v3_mr84_spool_tower_geometry as g


MODEL_ROOT = Path(__file__).resolve().parents[1] / "models" / "p3_v3_mr84_spool_tower_fix"


def _bounds(shape) -> tuple[float, ...]:
    bb = shape.bounding_box()
    return (bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z)


@pytest.mark.parametrize("kind", ("assembled", "service"))
def test_staged_exports_match_source_occurrences_labels_and_bounds(kind: str):
    factories = [
        g.make_stationary_module if kind == "assembled" else g.make_stationary_service_module,
        *[
            (lambda role=role: g.make_role_module(role))
            if kind == "assembled"
            else (lambda role=role: g.make_role_service_module(role))
            for role in range(3)
        ],
    ]
    roles = (None, 0, 1, 2)
    for role, factory in zip(roles, factories):
        source = factory()
        artifact = import_step(exporter.stage_path(kind, role))
        assert len(artifact.children) == len(source.children)
        assert len(artifact.solids()) == len(source.solids())
        assert [child.label for child in artifact.children] == [child.label for child in source.children]
        assert _bounds(artifact) == pytest.approx(_bounds(source), abs=1e-5)
        assert all(solid.is_valid and solid.volume > 0 for solid in artifact.solids())


@pytest.mark.parametrize(
    ("filename", "expected_bounds"),
    (
        ("p3_v3_mr84_spool_tower_assembled.step", (-150, 150, -150, 150, -29.8, 24.251)),
        ("p3_v3_mr84_spool_tower_service.step", (-150, 155.3, -150, 150, -53.0, 75.8)),
    ),
)
def test_final_steps_are_four_module_171_solid_handoffs(filename, expected_bounds):
    artifact = import_step(MODEL_ROOT / filename)
    assert len(artifact.children) == 4
    assert len(artifact.solids()) == 171
    assert _bounds(artifact) == pytest.approx(expected_bounds, abs=1e-3)
    assert all(solid.is_valid and solid.volume > 0 for solid in artifact.solids())

