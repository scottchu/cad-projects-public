"""Measured R2 gate evaluation, implemented only through Checkpoint A."""

from __future__ import annotations

import ast
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .frozen import (
    accepted_r1_fact_evidence,
    artifact_rejection_evidence,
    file_sha256,
    frozen_hash_evidence,
)
from .geometry import actual_geometry_evidence
from .probes import (
    ast_parameter_consumption_evidence,
    immutability_evidence,
    run_fresh_process_probe,
)
from .spec import DEFAULT_OWNERS, NAMESPACE, R2_ARTIFACT_ROOT, adjustable_field_specs


PACKAGE_ROOT = Path(__file__).resolve().parent


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=list).encode()
    ).hexdigest()


def _source_digests() -> dict[str, str]:
    return {
        path.name: file_sha256(path)
        for path in sorted(PACKAGE_ROOT.glob("*.py"))
    }


def _namespace_evidence() -> dict[str, object]:
    forbidden_imports = []
    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                if (
                    name.startswith("p3_v3_phase3_i3_r1_real_joinery")
                    and path.name != "predecessor.py"
                ):
                    forbidden_imports.append({"path": str(path), "module": name})
    mutable_root_payloads = sorted(
        str(path)
        for path in R2_ARTIFACT_ROOT.iterdir()
        if path.is_file() and path.suffix.lower() in {".step", ".stp", ".3mf", ".json"}
    )
    return {
        "namespace": NAMESPACE,
        "package_path": str(PACKAGE_ROOT),
        "artifact_path": str(R2_ARTIFACT_ROOT),
        "forbidden_r1_fallback_imports": forbidden_imports,
        "mutable_root_payloads": mutable_root_payloads,
        "passed": (
            PACKAGE_ROOT.name == NAMESPACE
            and R2_ARTIFACT_ROOT.name == NAMESPACE
            and not forbidden_imports
            and not mutable_root_payloads
        ),
    }


def _range_matches(bounds: list[float], expected: float, tolerance: float = 1e-7) -> bool:
    return all(abs(float(value) - expected) <= tolerance for value in bounds)


@lru_cache(maxsize=1)
def checkpoint_a_evidence() -> dict[str, Any]:
    frozen = frozen_hash_evidence()
    r1_facts = accepted_r1_fact_evidence()
    namespace = _namespace_evidence()
    artifact_rejection = artifact_rejection_evidence()
    geometry = actual_geometry_evidence(DEFAULT_OWNERS)
    ast_consumption = ast_parameter_consumption_evidence()
    immutability = immutability_evidence()
    probes = {
        row["field"]: run_fresh_process_probe(str(row["field"]))
        for row in adjustable_field_specs()
    }
    return {
        "frozen": frozen,
        "r1_facts": r1_facts,
        "namespace": namespace,
        "artifact_rejection": artifact_rejection,
        "geometry": geometry,
        "ast": ast_consumption,
        "immutability": immutability,
        "probes": probes,
        "source_digests": _source_digests(),
    }


def _gate_predicate(gate_id: str, evidence: dict[str, Any]) -> tuple[bool, object, str]:
    geometry = evidence["geometry"]
    probes = evidence["probes"]
    receive = probes["receive_xy_clearance_mm"]
    relief = probes["butt_face_relief_mm"]
    predicates: dict[str, tuple[bool, object, str]] = {
        "R2-001": (
            evidence["frozen"]["all_match"],
            evidence["frozen"],
            "fresh_process",
        ),
        "R2-002": (
            evidence["r1_facts"]["all_match"],
            evidence["r1_facts"],
            "fresh_import",
        ),
        "R2-003": (
            evidence["namespace"]["passed"],
            evidence["namespace"],
            "ast_closure",
        ),
        "R2-004": (
            evidence["artifact_rejection"]["passed"],
            evidence["artifact_rejection"],
            "fresh_process",
        ),
        "R2-005": (
            geometry["seam_count"] == 6
            and _range_matches(geometry["radial_clearance_range_mm"], 0.10)
            and _range_matches(geometry["tangential_clearance_range_mm"], 0.10),
            geometry["seams"],
            "actual_brep",
        ),
        "R2-006": (
            geometry["seam_count"] == 6
            and _range_matches(geometry["half_a_butt_relief_range_mm"], 0.025)
            and _range_matches(geometry["half_b_butt_relief_range_mm"], 0.025)
            and _range_matches(geometry["butt_gap_range_mm"], 0.050),
            geometry["seams"],
            "actual_brep",
        ),
        "R2-007": (
            geometry["seam_count"] == 6
            and _range_matches(geometry["axial_gap_range_mm"], 0.080),
            geometry["seams"],
            "actual_brep",
        ),
        "R2-008": (
            evidence["r1_facts"]["registry"]["passed"]
            and receive["passed"]
            and relief["passed"]
            and not receive["protected_drift"]
            and not relief["protected_drift"],
            {"registry": evidence["r1_facts"]["registry"], "receive": receive, "relief": relief},
            "actual_brep",
        ),
        "R2-009": (
            evidence["immutability"]["passed"]
            and evidence["immutability"]["required_owner_names"]
            == evidence["immutability"]["actual_owner_names"],
            evidence["immutability"],
            "fresh_process",
        ),
        "R2-010": (
            evidence["ast"]["all_adjustable_fields_consumed"]
            and evidence["ast"]["no_duplicated_geometry_literals"],
            evidence["ast"],
            "ast_closure",
        ),
        "R2-011": (
            len(probes) == len(adjustable_field_specs())
            and all(probe["passed"] for probe in probes.values()),
            probes,
            "fresh_process",
        ),
        "R2-012": (receive["passed"], receive, "actual_brep"),
        "R2-013": (relief["passed"], relief, "actual_brep"),
        "R2-014": (
            all(
                probe["passed"]
                and probe["protected_count"] == 131
                and not probe["protected_drift"]
                and all(value <= 1e-7 for value in probe["unchanged_witness_drift_mm"].values())
                for probe in probes.values()
            ),
            probes,
            "actual_brep",
        ),
    }
    if gate_id not in predicates:
        raise NotImplementedError(f"{gate_id} is outside bounded Checkpoint A")
    return predicates[gate_id]


def evaluate_gate(gate_id: str) -> dict[str, object]:
    try:
        gate_number = int(gate_id.rsplit("-", 1)[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"invalid R2 gate ID {gate_id!r}") from exc
    if gate_number > 14:
        raise NotImplementedError(f"{gate_id} is outside bounded Checkpoint A")
    evidence = checkpoint_a_evidence()
    passed, witnesses, provenance = _gate_predicate(gate_id, evidence)
    evidence_digest = _digest(witnesses)
    return {
        "gate_id": gate_id,
        "passed": bool(passed),
        "provenance": provenance,
        "source_digests": evidence["source_digests"],
        "evidence_digests": {gate_id: evidence_digest},
        "measured_witnesses": witnesses,
        "rejection_codes": [] if passed else [f"{gate_id}_FAILED"],
    }
