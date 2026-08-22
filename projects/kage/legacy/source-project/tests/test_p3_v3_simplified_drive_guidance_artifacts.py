"""Written-STEP validity and source/export parity for simplified V3."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from build123d import import_step
import pytest

from p3_v3_simplified_drive_guidance_geometry import make_assembled, make_service_exploded


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_simplified_drive_guidance"
SOURCE_FILES = (
    ROOT / "p3_v3_simplified_drive_guidance_spec.py",
    ROOT / "p3_v3_simplified_drive_guidance_geometry.py",
    ROOT / "p3_v3_simplified_drive_guidance_export.py",
)
# OpenCascade STEP round-tripping is expected to preserve these millimetre
# bounds to 1 micrometre. Labels and their occurrence-order hash are exact.
STEP_BOUND_TOLERANCE_MM = 0.001


def _labels(shape) -> list[str]:
    return [child.label for child in shape.children]


def _label_hash(shape) -> str:
    return sha256(json.dumps(_labels(shape), separators=(",", ":")).encode()).hexdigest()


def _bounds(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z


@pytest.mark.parametrize(
    "filename,factory",
    (
        ("p3_v3_simplified_assembled.step", make_assembled),
        ("p3_v3_simplified_service_exploded.step", make_service_exploded),
    ),
)
def test_written_step_has_exact_occurrence_name_hash_and_bounded_geometry_parity(filename, factory):
    path = MODEL_ROOT / filename
    newest_source = max(source.stat().st_mtime for source in SOURCE_FILES)
    assert path.is_file() and path.stat().st_mtime >= newest_source
    source, written = factory(), import_step(path)
    assert written.is_valid
    assert len(written.children) == len(source.children) == 165
    assert len(written.solids()) == len(source.solids()) == 165
    assert _labels(written) == _labels(source)
    assert _label_hash(written) == _label_hash(source)
    assert _bounds(written) == pytest.approx(_bounds(source), abs=STEP_BOUND_TOLERANCE_MM)
    for source_child, written_child in zip(source.children, written.children):
        assert _bounds(written_child) == pytest.approx(
            _bounds(source_child), abs=STEP_BOUND_TOLERANCE_MM
        )
        assert written_child.is_valid
        assert written_child.volume > 0.0
