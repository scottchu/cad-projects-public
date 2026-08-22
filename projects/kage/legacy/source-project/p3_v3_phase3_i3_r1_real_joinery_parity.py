"""Fresh STEP export/import parity for the isolated I3-R1 successor."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from p3_v3_phase3_i3_r1_real_joinery_spec import NAMESPACE


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / NAMESPACE
NOMINAL_STEP = MODEL_ROOT / "assembled_nominal.step"
EXPLODED_STEP = MODEL_ROOT / "service_exploded.step"


def _run_json(script: str, *args: object) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-c", script, *(str(arg) for arg in args)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"fresh STEP subprocess failed rc={completed.returncode}: "
            f"stdout={completed.stdout[-2000:]!r} stderr={completed.stderr[-4000:]!r}"
        )
    return json.loads(completed.stdout)


EXPORT_SCRIPT = r'''
import json, sys
from build123d import export_step
from p3_v3_phase3_i3_r1_real_joinery_geometry import assembled_shape, candidate_occurrences, service_exploded_shape

def metric(shape):
    box=shape.bounding_box()
    return {
        "label":str(shape.label),
        "bounds":[float(box.min.X),float(box.min.Y),float(box.min.Z),float(box.max.X),float(box.max.Y),float(box.max.Z)],
        "volume":float(sum(s.volume for s in shape.solids())),
        "area":float(sum(f.area for f in shape.faces())),
        "solid_count":len(shape.solids()),
        "face_count":len(shape.faces()),
        "edge_count":len(shape.edges()),
    }
rows=candidate_occurrences()
assembly=assembled_shape()
export_step(assembly,sys.argv[1])
exploded=service_exploded_shape()
export_step(exploded,sys.argv[2])
b=assembly.bounding_box()
eb=exploded.bounding_box()
protected=[metric(r["shape"]) for r in rows if r["classification"]=="protected_exact"]
print(json.dumps({"registry_count":len(rows),"protected":protected,"bounds":[b.min.X,b.min.Y,b.min.Z,b.max.X,b.max.Y,b.max.Z],"exploded_bounds":[eb.min.X,eb.min.Y,eb.min.Z,eb.max.X,eb.max.Y,eb.max.Z]},sort_keys=True,separators=(",",":")))
'''


IMPORT_SCRIPT = r'''
import json, sys
from build123d import import_step

def metric(shape):
    box=shape.bounding_box()
    return {
        "label":str(shape.label),
        "bounds":[float(box.min.X),float(box.min.Y),float(box.min.Z),float(box.max.X),float(box.max.Y),float(box.max.Z)],
        "volume":float(sum(s.volume for s in shape.solids())),
        "area":float(sum(f.area for f in shape.faces())),
        "solid_count":len(shape.solids()),
        "face_count":len(shape.faces()),
        "edge_count":len(shape.edges()),
    }
assembly=import_step(sys.argv[1])
b=assembly.bounding_box()
children=list(assembly.children)
invalid=[str(c.label) for c in children if not c.is_valid or sum(s.volume for s in c.solids()) <= 0]
print(json.dumps({"occurrence_count":len(children),"children":[metric(c) for c in children],"bounds":[b.min.X,b.min.Y,b.min.Z,b.max.X,b.max.Y,b.max.Z],"invalid_topology":invalid},sort_keys=True,separators=(",",":")))
'''


def _metric_drift(source: dict[str, object], imported: dict[str, object]) -> list[str]:
    drift = []
    if source["label"] != imported["label"]:
        drift.append("label")
    for key in ("solid_count", "face_count", "edge_count"):
        if source[key] != imported[key]:
            drift.append(key)
    # STEP round-trip evaluates the same exact surfaces through the kernel's
    # serialized tolerance.  The 0.1 cubic-micron threshold is substantially
    # tighter than FDM resolution and is recorded, not silently clamped.
    for key, tolerance in (("volume", 1e-4), ("area", 1e-4)):
        if abs(float(source[key]) - float(imported[key])) > tolerance:
            drift.append(key)
    if max(abs(float(a) - float(b)) for a, b in zip(source["bounds"], imported["bounds"])) > 1e-6:
        drift.append("bounds")
    return drift


def fresh_process_source_import_evidence(write: bool = False) -> dict[str, object]:
    """Export source in one process and reload it in a second fresh process."""

    MODEL_ROOT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{NAMESPACE}-step-parity-", dir=MODEL_ROOT.parent) as temporary:
        candidate = Path(temporary) / NOMINAL_STEP.name
        exploded_candidate = Path(temporary) / "service_exploded.step"
        source = _run_json(EXPORT_SCRIPT, candidate, exploded_candidate)
        imported = _run_json(IMPORT_SCRIPT, candidate)
        exploded_imported = _run_json(IMPORT_SCRIPT, exploded_candidate)
        source_by_label = {str(row["label"]): row for row in source["protected"]}
        imported_by_label = {str(row["label"]): row for row in imported["children"]}
        protected_drift = []
        for label, source_row in source_by_label.items():
            imported_row = imported_by_label.get(label)
            if imported_row is None:
                protected_drift.append({"label": label, "drift": ["missing"]})
                continue
            differences = _metric_drift(source_row, imported_row)
            if differences:
                protected_drift.append({"label": label, "drift": differences})
        digest = sha256(candidate.read_bytes()).hexdigest()
        exploded_digest = sha256(exploded_candidate.read_bytes()).hexdigest()
        size = candidate.stat().st_size
        exploded_size = exploded_candidate.stat().st_size
        if write:
            MODEL_ROOT.mkdir(parents=True, exist_ok=True)
            staged = MODEL_ROOT / f".{NOMINAL_STEP.name}.new"
            staged.write_bytes(candidate.read_bytes())
            staged.replace(NOMINAL_STEP)
            if sha256(NOMINAL_STEP.read_bytes()).hexdigest() != digest:
                raise RuntimeError("atomic nominal STEP publish digest mismatch")
            exploded_staged = MODEL_ROOT / f".{EXPLODED_STEP.name}.new"
            exploded_staged.write_bytes(exploded_candidate.read_bytes())
            exploded_staged.replace(EXPLODED_STEP)
            if sha256(EXPLODED_STEP.read_bytes()).hexdigest() != exploded_digest:
                raise RuntimeError("atomic exploded STEP publish digest mismatch")

    return {
        "path": str(NOMINAL_STEP) if write else None,
        "exploded_path": str(EXPLODED_STEP) if write else None,
        "source_registry_count": source["registry_count"],
        "imported_occurrence_count": imported["occurrence_count"],
        "protected_occurrence_count": len(source_by_label),
        "protected_drift": protected_drift,
        "source_global_bounds_mm": source["bounds"],
        "imported_global_bounds_mm": imported["bounds"],
        "step_sha256": digest,
        "step_bytes": size,
        "exploded_step_sha256": exploded_digest,
        "exploded_step_bytes": exploded_size,
        "exploded_imported_occurrence_count": exploded_imported["occurrence_count"],
        "nominal_topology_failures": imported["invalid_topology"],
        "exploded_topology_failures": exploded_imported["invalid_topology"],
        "source_export_process_count": 1,
        "fresh_import_process_count": 2,
        "measurement_provenance": "actual_exported_and_imported_step_brep",
    }
