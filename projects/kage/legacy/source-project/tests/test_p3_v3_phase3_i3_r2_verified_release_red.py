"""Exhaustive RED inventory for KAGE I3-R2 verified release.

The file deliberately imports only the isolated R2 evaluator.  Until that
evaluator exists and supplies measured, source-bound evidence, every inventory
item is RED.  R1 modules are never accepted as a fallback.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "tests" / "r2_verified_release_gate_inventory.json"
NS = "p3_v3_phase3_i3_r2_verified_release"
EXPECTED_GATE_COUNT = 101

GATES = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
assert len(GATES) == EXPECTED_GATE_COUNT
assert [gate["id"] for gate in GATES] == [f"R2-{index:03d}" for index in range(1, 102)]
assert {gate["checkpoint"] for gate in GATES} == {
    "geometry_parameters",
    "motion_mechanical",
    "manifold_freshness",
    "two_build_release",
}
assert all(gate["requirement"] and gate["sections"] for gate in GATES)


def _load_evaluator():
    name = f"{NS}.gate_evaluator"
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(f"RED: isolated R2 evaluator {name!r} is absent", pytrace=False)
        raise


@pytest.mark.parametrize("gate", GATES, ids=[gate["id"] for gate in GATES])
def test_r2_verified_release_gate(gate: dict[str, object]) -> None:
    result = _load_evaluator().evaluate_gate(str(gate["id"]))
    assert result["gate_id"] == gate["id"]
    assert result["passed"] is True
    assert result["provenance"] in {
        "actual_brep",
        "fresh_import",
        "fresh_process",
        "archive_bytes",
        "ast_closure",
        "filesystem_failpoint",
    }
    assert result["source_digests"]
    assert result["evidence_digests"]
    assert result["measured_witnesses"]
    assert result["rejection_codes"] == []

