"""Freshness and source-to-STEP parity for the V3 roller correction."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from build123d import import_step

from p3_v3_roller_tower_geometry import (
    make_role_module,
    make_role_service_module,
    make_stationary_module,
    make_stationary_service_module,
)


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_roller_tower_fix"
SOURCE_FILES = (
    ROOT / "p3_v3_roller_tower_spec.py",
    ROOT / "p3_v3_roller_tower_geometry.py",
    ROOT / "p3_v3_roller_tower_export.py",
)


def _facts(shape):
    facts = []
    for child in shape.children:
        box = child.bounding_box()
        facts.append(
            (
                child.label,
                round(child.volume, 4),
                tuple(round(value, 4) for value in (box.min.X, box.min.Y, box.min.Z)),
                tuple(round(value, 4) for value in (box.max.X, box.max.Y, box.max.Z)),
            )
        )
    return facts


def _digest(shape):
    return sha256(json.dumps(_facts(shape), separators=(",", ":")).encode()).hexdigest()


def _occurrence_facts(shape, path=()):
    facts = []
    for index, child in enumerate(shape.children):
        child_path = (*path, f"{index}:{child.label}")
        box = child.bounding_box()
        facts.append(
            (
                child_path,
                round(child.volume, 4),
                tuple(round(value, 4) for value in (box.min.X, box.min.Y, box.min.Z)),
                tuple(round(value, 4) for value in (box.max.X, box.max.Y, box.max.Z)),
                len(child.children),
            )
        )
        facts.extend(_occurrence_facts(child, child_path))
    return facts


def _occurrence_digest(shape):
    return sha256(
        json.dumps(_occurrence_facts(shape), separators=(",", ":")).encode()
    ).hexdigest()


def _source_module(kind, role):
    if kind == "assembled":
        return make_stationary_module() if role is None else make_role_module(role)
    return make_stationary_service_module() if role is None else make_role_service_module(role)


def _source_final(kind):
    modules = [_source_module(kind, None)]
    modules.extend(_source_module(kind, role) for role in range(3))
    label = (
        "p3_v3_roller_tower_COMPLETE_assembly"
        if kind == "assembled"
        else "p3_v3_roller_tower_COMPLETE_service_exploded"
    )
    from build123d import Compound

    return Compound(children=modules, label=label)


def _stage_path(kind, role):
    suffix = "stationary" if role is None else ("hour", "minute", "second")[role]
    return MODEL_ROOT / "staged" / f"p3_v3_roller_tower_{kind}_{suffix}_module.step"


def test_final_exports_are_fresh_complete_and_valid():
    newest_source = max(path.stat().st_mtime for path in SOURCE_FILES)
    for kind in ("assembled", "service"):
        path = MODEL_ROOT / f"p3_v3_roller_tower_{kind}.step"
        assert path.exists() and path.stat().st_mtime >= newest_source
        exported = import_step(path)
        assert exported.is_valid and len(exported.children) == 4
        staged_count = sum(len(import_step(_stage_path(kind, role)).solids()) for role in (None, 0, 1, 2))
        assert len(exported.solids()) == staged_count
        assert all(child.volume > 0.0 for child in exported.solids())


def test_all_eight_staged_modules_have_occurrence_bounds_and_hash_parity():
    for kind in ("assembled", "service"):
        for role in (None, 0, 1, 2):
            source = _source_module(kind, role)
            exported = import_step(_stage_path(kind, role))
            assert len(source.children) == len(exported.children)
            assert len(source.solids()) == len(exported.solids())
            assert [child.label for child in source.children] == [child.label for child in exported.children]
            assert _facts(exported) == _facts(source)
            assert _digest(exported) == _digest(source)


def test_final_steps_have_strict_recursive_occurrence_name_bounds_volume_and_hash_parity():
    for kind in ("assembled", "service"):
        source = _source_final(kind)
        exported = import_step(MODEL_ROOT / f"p3_v3_roller_tower_{kind}.step")
        assert exported.label == source.label
        assert _occurrence_facts(exported) == _occurrence_facts(source)
        assert _occurrence_digest(exported) == _occurrence_digest(source)
