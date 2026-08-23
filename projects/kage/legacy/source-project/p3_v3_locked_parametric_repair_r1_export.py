"""Generate the reviewed Phase-1 WIP STEP and occurrence parity manifest."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import shutil
from typing import Any

from p3_v3_locked_parametric_repair_r1_geometry import LOCKED_INPUTS, MODEL_ROOT, ROOT
from p3_v3_locked_parametric_repair_r1_parity import brep_fingerprint, hash_file, parity_manifest
from p3_v3_locked_parametric_repair_r1_spec import P3_V3_LOCKED_PARAMETRIC_REPAIR_R1


WIP_STEP = MODEL_ROOT / "p3_v3_locked_parametric_repair_r1_zero_delta_wip.step"
PARITY_JSON = MODEL_ROOT / "p3_v3_locked_parametric_repair_r1_zero_delta_parity.json"


def _jsonable_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    output = dict(manifest)
    output["occurrences"] = []
    for row in manifest["occurrences"]:
        clean = {key: value for key, value in row.items() if key != "shape"}
        clean["brep_fingerprint"] = brep_fingerprint(row["shape"])
        output["occurrences"].append(clean)
    return output


def export_wip() -> tuple[Path, Path]:
    params = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1
    params.validate()
    raw_manifest = parity_manifest(params)
    manifest = _jsonable_manifest(raw_manifest)
    if manifest["unknown_occurrence_names"] or manifest["unclassified_occurrence_names"] or manifest["protected_drift_occurrence_names"]:
        raise ValueError("zero-delta parity manifest is not clean; refusing WIP export")
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    # Publish the exact candidate STEP bytes that crossed the parity evidence
    # boundary.  Re-exporting its imported children here would create an
    # unnecessary second serializer round trip.
    shutil.copyfile(raw_manifest["candidate_temporary_step_evidence_path"], WIP_STEP)
    manifest["candidate_permanent_step_evidence_path"] = str(WIP_STEP)
    manifest["wip_step_sha256"] = sha256(WIP_STEP.read_bytes()).hexdigest()
    manifest["source_locked_hashes"] = {
        str(path.relative_to(ROOT)): hash_file(path)
        for path in LOCKED_INPUTS
    }
    PARITY_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return WIP_STEP, PARITY_JSON


if __name__ == "__main__":
    for path in export_wip():
        print(path)
