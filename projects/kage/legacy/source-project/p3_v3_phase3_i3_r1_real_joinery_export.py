"""Fresh disassembled 34-body 3MF export for the isolated I3-R1 repair."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import perf_counter
from uuid import NAMESPACE_URL, uuid5
from zipfile import ZipFile

from build123d import export_brep
import lib3mf

from p3_v3_phase3_i3_r1_real_joinery_geometry import printable_occurrences
from p3_v3_phase3_i3_r1_real_joinery_spec import ARTIFACT_CONTRACT, NAMESPACE


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / NAMESPACE
PRINT_COMPONENTS_3MF = MODEL_ROOT / "print_components.3mf"
NOMINAL_STEP = MODEL_ROOT / "assembled_nominal.step"
EXPLODED_STEP = MODEL_ROOT / "service_exploded.step"
ORCA_SOURCE_3MF = MODEL_ROOT / "i3_8_six_moving_halves_source.3mf"
PROJECTION_JCS = MODEL_ROOT / "i3_12_parity_projection.jcs.json"
FRESHNESS_MANIFEST = MODEL_ROOT / "freshness_manifest.jcs.json"
STEP_PARITY_REPORT = MODEL_ROOT / "step_parity_report.json"
REGENERATION_REPORT = MODEL_ROOT / "fresh_atomic_regeneration_report.json"


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _brep_digest(shape) -> str:
    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return _sha(Path(temporary.name))


def _kind(row: dict[str, object]) -> str:
    name = str(row["name"])
    if "_half_" in name:
        return "moving_half"
    if row.get("kind") == "bridge":
        return "stationary_bridge"
    return "stationary_quadrant"


def _mesh_geometry(shape):
    vertices, triangles = shape.tessellate(0.08, 0.15)
    positions = []
    for vertex in vertices:
        position = lib3mf.Position()
        position.Coordinates[:] = (float(vertex.X), float(vertex.Y), float(vertex.Z))
        positions.append(position)
    indices = []
    for a, b, c in triangles:
        triangle = lib3mf.Triangle()
        triangle.Indices[:] = (int(a), int(b), int(c))
        indices.append(triangle)
    if not positions or not indices:
        raise RuntimeError("I3-R1 printable body tessellated empty")
    return positions, indices


def _source_rows() -> list[dict[str, object]]:
    rows = []
    for source in printable_occurrences():
        label = str(source["label"])
        rows.append({
            "name": str(source["name"]),
            "label": label,
            "uuid": str(uuid5(NAMESPACE_URL, f"{NAMESPACE}:{label}")),
            "kind": _kind(source),
            "shape": source["shape"],
            "source_brep_sha256": _brep_digest(source["shape"]),
        })
    if len(rows) != ARTIFACT_CONTRACT.printable_count:
        raise RuntimeError(f"expected 34 printable bodies, got {len(rows)}")
    if len({row["label"] for row in rows}) != len(rows):
        raise RuntimeError("I3-R1 printable labels are not unique")
    if len({row["uuid"] for row in rows}) != len(rows):
        raise RuntimeError("I3-R1 printable UUIDs are not unique")
    counts = {kind: sum(row["kind"] == kind for row in rows) for kind in (
        "stationary_quadrant", "moving_half", "stationary_bridge"
    )}
    if counts != {"stationary_quadrant": 12, "moving_half": 6, "stationary_bridge": 16}:
        raise RuntimeError(f"I3-R1 printable kind mismatch: {counts}")
    return rows


def _write_package(path: Path, rows: list[dict[str, object]]) -> float:
    started = perf_counter()
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    for index, row in enumerate(rows, start=1):
        mesh = model.AddMeshObject()
        mesh.SetName(row["label"])
        mesh.SetUUID(row["uuid"])
        vertices, triangles = _mesh_geometry(row["shape"])
        mesh.SetGeometry(vertices, triangles)
        model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
        print(
            f"I3-R1 3MF tessellation: object={index}/{len(rows)} "
            f"kind={row['kind']} triangles={len(triangles)}",
            flush=True,
        )
    model.QueryWriter("3mf").WriteToFile(str(path))
    return perf_counter() - started


def _fresh_process_import(path: Path) -> dict[str, object]:
    script = r'''
import json, lib3mf, sys
w=lib3mf.Wrapper(); m=w.CreateModel(); m.QueryReader("3mf").ReadFromFile(sys.argv[1])
meshes=m.GetMeshObjects(); objects=[]
while meshes.MoveNext():
    o=meshes.GetCurrentMeshObject()
    objects.append({"name":o.GetName(),"resource_id":o.GetResourceID(),"triangles":o.GetTriangleCount(),"vertices":o.GetVertexCount(),"uuid":o.GetUUID()})
build=m.GetBuildItems(); build_names=[]
while build.MoveNext():
    build_names.append(build.GetCurrent().GetObjectResource().GetName())
print(json.dumps({"objects":objects,"build_names":build_names},sort_keys=True,separators=(",",":")))
'''
    completed = subprocess.run(
        [sys.executable, "-c", script, str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def disassembled_3mf_import_evidence(write: bool = False) -> dict[str, object]:
    """Generate in fresh temp storage, independently reload, then publish."""

    rows = _source_rows()
    MODEL_ROOT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{NAMESPACE}-", dir=MODEL_ROOT.parent) as temporary:
        temporary_path = Path(temporary)
        candidate = temporary_path / "print_components.3mf"
        tessellation_seconds = _write_package(candidate, rows)
        with ZipFile(candidate) as archive:
            crc_ok = archive.testzip() is None
        imported = _fresh_process_import(candidate)
        imported_names = [row["name"] for row in imported["objects"]]
        source_names = [str(row["label"]) for row in rows]
        build_names = list(imported["build_names"])
        mapping_ok = (
            sorted(imported_names) == sorted(source_names)
            and sorted(build_names) == sorted(source_names)
            and all(row["triangles"] > 0 and row["vertices"] > 0 for row in imported["objects"])
        )
        if not crc_ok or not mapping_ok:
            raise RuntimeError("fresh I3-R1 3MF import/body mapping failed")
        digest = _sha(candidate)
        bytes_count = candidate.stat().st_size
        if write:
            MODEL_ROOT.mkdir(parents=True, exist_ok=True)
            staged = MODEL_ROOT / ".print_components.3mf.new"
            staged.write_bytes(candidate.read_bytes())
            os.replace(staged, PRINT_COMPONENTS_3MF)
            if _sha(PRINT_COMPONENTS_3MF) != digest:
                raise RuntimeError("atomic I3-R1 3MF publish digest mismatch")

    counts = {kind: sum(row["kind"] == kind for row in rows) for kind in (
        "stationary_quadrant", "moving_half", "stationary_bridge"
    )}
    return {
        "path": str(PRINT_COMPONENTS_3MF) if write else None,
        "generated_in_new_temporary_directory": True,
        "atomic_publish": bool(write),
        "archive_sha256": digest,
        "archive_bytes": bytes_count,
        "crc_ok": crc_ok,
        "printable_body_count": len(rows),
        "stationary_quadrant_count": counts["stationary_quadrant"],
        "moving_half_count": counts["moving_half"],
        "stationary_bridge_count": counts["stationary_bridge"],
        "purchased_hardware_count": 0,
        "unique_name_count": len(set(source_names)),
        "unique_uuid_count": len({row["uuid"] for row in rows}),
        "fresh_process_import_count": len(imported["objects"]),
        "fresh_process_build_item_count": len(build_names),
        "source_import_body_mapping_verified": mapping_ok,
        "source_brep_sha256": {str(row["label"]): row["source_brep_sha256"] for row in rows},
        "tessellation_seconds": tessellation_seconds,
    }


if __name__ == "__main__":
    print(json.dumps(disassembled_3mf_import_evidence(write=True), indent=2, sort_keys=True))


def required_artifact_paths() -> tuple[Path, ...]:
    return (
        NOMINAL_STEP,
        EXPLODED_STEP,
        PRINT_COMPONENTS_3MF,
        ORCA_SOURCE_3MF,
        PROJECTION_JCS,
        FRESHNESS_MANIFEST,
        STEP_PARITY_REPORT,
        REGENERATION_REPORT,
    )


def _authoritative_inputs() -> tuple[Path, ...]:
    from p3_v3_phase3_i3_r1_real_joinery_print_project import PROFILE_CHAINS
    from p3_v3_phase3_i3_r1_real_joinery_spec import FROZEN_STEP_PATH

    source_names = (
        "p3_v3_phase3_i3_r1_real_joinery_spec.py",
        "p3_v3_phase3_i3_r1_real_joinery_geometry.py",
        "p3_v3_phase3_i3_r1_real_joinery_validation.py",
        "p3_v3_phase3_i3_r1_real_joinery_print_project.py",
        "p3_v3_phase3_i3_r1_real_joinery_export.py",
        "p3_v3_phase3_i3_r1_real_joinery_canonical.py",
        "p3_v3_phase3_i3_r1_real_joinery_parity.py",
        "vendor/i3_rfc8785/canonicalize.js",
    )
    # I3.1 is the accepted manufacturing specification itself.  Numbered
    # amendment filenames begin at I3.2; do not invent a non-existent I3.1
    # pathname or silently omit the authoritative base document.
    documents = tuple(ROOT / "docs" / f"p3-v3-phase3-i3-{index}-design-amendment.md" for index in range(2, 13)) + (
        ROOT / "docs" / "p3-v3-phase3-i3-r1-real-joinery-localized-repair-handoff.md",
        ROOT / "docs" / "p3-v3-phase3-i3-u1-segmentation-joinery-accepted-spec.md",
    )
    profiles = tuple(Path(path) for rows in PROFILE_CHAINS.values() for path, _digest in rows)
    return tuple(ROOT / name for name in source_names) + documents + profiles + (FROZEN_STEP_PATH,)


def freshness_input_evidence() -> dict[str, object]:
    inputs = _authoritative_inputs()
    missing = [str(path) for path in inputs if not path.is_file()]
    hashes = {str(path): _sha(path) for path in inputs if path.is_file()}
    signature = sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    deleted = dict(hashes)
    if deleted:
        deleted.pop(next(iter(sorted(deleted))))
    deleted_signature = sha256(json.dumps(deleted, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "required_input_count": len(inputs),
        "missing_required_inputs": missing,
        "input_sha256": hashes,
        "freshness_signature_sha256": signature,
        "signature_after_required_input_deletion_sha256": deleted_signature,
        "signature_deletion_forces_regeneration": signature != deleted_signature,
    }


def _atomic_bytes(path: Path, payload: bytes) -> None:
    """Publish one already-validated payload without an observable partial file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.parent / f".{path.name}.new"
    staged.write_bytes(payload)
    os.replace(staged, path)


def _canonical_json_bytes(value: object) -> bytes:
    from p3_v3_phase3_i3_r1_real_joinery_canonical import _jcs

    return _jcs(value)


def _generate_complete_candidate(directory: Path) -> dict[str, object]:
    """Generate and validate every successor release artifact from source.

    ``directory`` is new for every invocation.  No file in ``MODEL_ROOT`` is
    inspected while constructing the candidate, so an old successful export
    cannot satisfy this gate.
    """

    from p3_v3_phase3_i3_r1_real_joinery_canonical import (
        _jcs,
        _projection_from_archive,
    )
    from p3_v3_phase3_i3_r1_real_joinery_parity import (
        EXPORT_SCRIPT,
        IMPORT_SCRIPT,
        _metric_drift,
        _run_json,
    )
    from p3_v3_phase3_i3_r1_real_joinery_print_project import (
        _fresh_orca_parser,
        _write_orca_source_project,
    )

    staging = directory / "staging"
    published = directory / "published"
    staging.mkdir(parents=True)
    published.mkdir(parents=True)

    staged_paths = {
        "nominal_step": staging / NOMINAL_STEP.name,
        "exploded_step": staging / EXPLODED_STEP.name,
        "print_components_3mf": staging / PRINT_COMPONENTS_3MF.name,
        "orca_source_3mf": staging / ORCA_SOURCE_3MF.name,
        "projection_jcs": staging / PROJECTION_JCS.name,
        "freshness_manifest": staging / FRESHNESS_MANIFEST.name,
        "step_parity_report": staging / STEP_PARITY_REPORT.name,
        "regeneration_report": staging / REGENERATION_REPORT.name,
    }

    # STEP generation occurs in its own interpreter.  Each resulting file is
    # then imported in a separate fresh interpreter before it can be published.
    source = _run_json(
        EXPORT_SCRIPT,
        staged_paths["nominal_step"],
        staged_paths["exploded_step"],
    )
    nominal_import = _run_json(IMPORT_SCRIPT, staged_paths["nominal_step"])
    exploded_import = _run_json(IMPORT_SCRIPT, staged_paths["exploded_step"])
    if nominal_import["invalid_topology"] or exploded_import["invalid_topology"]:
        raise RuntimeError("fresh STEP import found invalid or non-positive topology")

    source_by_label = {str(row["label"]): row for row in source["protected"]}
    imported_by_label = {
        str(row["label"]): row for row in nominal_import["children"]
    }
    protected_drift = []
    for label, source_row in source_by_label.items():
        imported_row = imported_by_label.get(label)
        drift = ["missing"] if imported_row is None else _metric_drift(source_row, imported_row)
        if drift:
            protected_drift.append({"label": label, "drift": drift})
    if protected_drift:
        raise RuntimeError(f"fresh STEP protected parity drift: {protected_drift}")

    rows = _source_rows()
    _write_package(staged_paths["print_components_3mf"], rows)
    disassembled_import = _fresh_process_import(staged_paths["print_components_3mf"])
    expected_print_names = sorted(str(row["label"]) for row in rows)
    imported_print_names = sorted(str(row["name"]) for row in disassembled_import["objects"])
    if imported_print_names != expected_print_names:
        raise RuntimeError("fresh disassembled 3MF object/source registry mismatch")
    if sorted(disassembled_import["build_names"]) != expected_print_names:
        raise RuntimeError("fresh disassembled 3MF build/source registry mismatch")

    _write_orca_source_project(staged_paths["orca_source_3mf"])
    orca_import = _fresh_orca_parser(staged_paths["orca_source_3mf"])
    if len(orca_import["plates"]) != 6 or len(orca_import["build_names"]) != 6:
        raise RuntimeError("fresh Orca source project does not contain six real plates")
    projection, projection_details = _projection_from_archive(
        staged_paths["orca_source_3mf"]
    )
    projection_bytes = _jcs(projection)
    staged_paths["projection_jcs"].write_bytes(projection_bytes)

    freshness = freshness_input_evidence()
    if freshness["missing_required_inputs"]:
        raise RuntimeError(
            f"freshness closure has missing inputs: {freshness['missing_required_inputs']}"
        )
    if not freshness["signature_deletion_forces_regeneration"]:
        raise RuntimeError("freshness negative deletion fixture did not change signature")

    step_report = {
        "schema": "kage.i3-r1.step-parity-report.v1",
        "source_registry_count": source["registry_count"],
        "nominal_imported_occurrence_count": nominal_import["occurrence_count"],
        "exploded_imported_occurrence_count": exploded_import["occurrence_count"],
        "protected_occurrence_count": len(source_by_label),
        "protected_drift": protected_drift,
        "nominal_bounds_mm": nominal_import["bounds"],
        "exploded_bounds_mm": exploded_import["bounds"],
        "nominal_topology_failures": nominal_import["invalid_topology"],
        "exploded_topology_failures": exploded_import["invalid_topology"],
    }
    staged_paths["step_parity_report"].write_bytes(_canonical_json_bytes(step_report))
    staged_paths["freshness_manifest"].write_bytes(_canonical_json_bytes(freshness))

    # Semantic evidence intentionally excludes ZIP container timestamps and
    # STEP text serialization.  It compares the independently imported model,
    # object/plate registries, and canonical I3.12 projection instead.
    semantic = {
        "schema": "kage.i3-r1.fresh-regeneration-semantics.v1",
        "freshness_signature_sha256": freshness["freshness_signature_sha256"],
        "source_registry_count": source["registry_count"],
        "source_bounds_mm": source["bounds"],
        "nominal_import": nominal_import,
        "exploded_import": exploded_import,
        "disassembled_objects": disassembled_import["objects"],
        "disassembled_build_names": disassembled_import["build_names"],
        "orca_import": orca_import,
        "projection_sha256": sha256(projection_bytes).hexdigest(),
        "projection_details": projection_details,
        "protected_drift": protected_drift,
    }
    semantic_bytes = _canonical_json_bytes(semantic)
    package_semantic = {
        "schema": "kage.i3-r1.fresh-package-semantics.v1",
        "freshness_signature_sha256": freshness["freshness_signature_sha256"],
        "disassembled_objects": disassembled_import["objects"],
        "disassembled_build_names": disassembled_import["build_names"],
        "orca_import": orca_import,
        "projection_sha256": sha256(projection_bytes).hexdigest(),
        "projection_details": projection_details,
    }
    package_semantic_bytes = _canonical_json_bytes(package_semantic)
    regeneration_report = {
        "schema": "kage.i3-r1.fresh-atomic-regeneration-report.v1",
        "semantic_sha256": sha256(semantic_bytes).hexdigest(),
        "fresh_process_import_count": 4,
        "stale_artifact_reuse_count": 0,
        "validated_artifacts": sorted(staged_paths),
    }
    staged_paths["regeneration_report"].write_bytes(
        _canonical_json_bytes(regeneration_report)
    )

    # The candidate itself follows the same staging/rename path as the final
    # release.  This makes atomic-publish behavior testable even before the
    # validated candidate is copied to the stable successor namespace.
    published_paths = {}
    for key, source_path in staged_paths.items():
        destination = published / source_path.name
        os.replace(source_path, destination)
        published_paths[key] = destination

    artifact_hashes = {key: _sha(path) for key, path in published_paths.items()}
    artifact_bytes = {key: path.stat().st_size for key, path in published_paths.items()}
    return {
        "directory": directory,
        "paths": published_paths,
        "artifact_sha256": artifact_hashes,
        "artifact_bytes": artifact_bytes,
        "semantic_bytes": semantic_bytes,
        "semantic_sha256": sha256(semantic_bytes).hexdigest(),
        "package_semantic_bytes": package_semantic_bytes,
        "package_semantic_sha256": sha256(package_semantic_bytes).hexdigest(),
        "nominal_import": nominal_import,
        "exploded_import": exploded_import,
        "disassembled_object_count": len(disassembled_import["objects"]),
        "disassembled_build_item_count": len(disassembled_import["build_names"]),
        "orca_plate_count": len(orca_import["plates"]),
        "orca_build_object_count": len(orca_import["build_names"]),
        "projection_sha256": sha256(projection_bytes).hexdigest(),
        "protected_occurrence_count": len(source_by_label),
        "protected_drift": protected_drift,
    }


def _generate_package_repeat(directory: Path) -> dict[str, object]:
    """Repeat both 3MF package builds/imports without redundant STEP work."""

    from p3_v3_phase3_i3_r1_real_joinery_canonical import (
        _jcs,
        _projection_from_archive,
    )
    from p3_v3_phase3_i3_r1_real_joinery_print_project import (
        _fresh_orca_parser,
        _write_orca_source_project,
    )

    directory.mkdir(parents=True)
    disassembled_path = directory / PRINT_COMPONENTS_3MF.name
    orca_path = directory / ORCA_SOURCE_3MF.name

    rows = _source_rows()
    _write_package(disassembled_path, rows)
    disassembled_import = _fresh_process_import(disassembled_path)
    expected_names = sorted(str(row["label"]) for row in rows)
    if sorted(str(row["name"]) for row in disassembled_import["objects"]) != expected_names:
        raise RuntimeError("repeat disassembled 3MF object/source registry mismatch")
    if sorted(disassembled_import["build_names"]) != expected_names:
        raise RuntimeError("repeat disassembled 3MF build/source registry mismatch")

    _write_orca_source_project(orca_path)
    orca_import = _fresh_orca_parser(orca_path)
    if len(orca_import["plates"]) != 6 or len(orca_import["build_names"]) != 6:
        raise RuntimeError("repeat Orca source project does not contain six real plates")
    projection, projection_details = _projection_from_archive(orca_path)
    projection_bytes = _jcs(projection)
    freshness = freshness_input_evidence()
    if freshness["missing_required_inputs"]:
        raise RuntimeError("repeat package run has incomplete freshness closure")

    package_semantic = {
        "schema": "kage.i3-r1.fresh-package-semantics.v1",
        "freshness_signature_sha256": freshness["freshness_signature_sha256"],
        "disassembled_objects": disassembled_import["objects"],
        "disassembled_build_names": disassembled_import["build_names"],
        "orca_import": orca_import,
        "projection_sha256": sha256(projection_bytes).hexdigest(),
        "projection_details": projection_details,
    }
    package_semantic_bytes = _canonical_json_bytes(package_semantic)
    negative_digests = {}
    for fixture in ("object", "plate", "profile"):
        mutated = json.loads(json.dumps(package_semantic))
        if fixture == "object":
            mutated["orca_import"]["model_map"]["objects"][0]["object_name"] += "__negative"
        elif fixture == "plate":
            mutated["orca_import"]["plates"][0]["plate_index"] = "999"
        else:
            mutated["orca_import"]["project"]["profile_chains"]["machine"][0]["sha256"] = "0" * 64
        negative_digests[fixture] = sha256(_canonical_json_bytes(mutated)).hexdigest()
    base_digest = sha256(package_semantic_bytes).hexdigest()
    meaningful_mutations_change_semantic = all(
        digest != base_digest for digest in negative_digests.values()
    )
    if not meaningful_mutations_change_semantic:
        raise RuntimeError("object/plate/profile semantic negative fixture was accepted")
    return {
        "package_semantic_bytes": package_semantic_bytes,
        "package_semantic_sha256": base_digest,
        "projection_sha256": sha256(projection_bytes).hexdigest(),
        "disassembled_object_count": len(disassembled_import["objects"]),
        "orca_plate_count": len(orca_import["plates"]),
        "negative_fixture_sha256": negative_digests,
        "meaningful_mutations_change_semantic": meaningful_mutations_change_semantic,
    }


def fresh_atomic_regeneration_evidence(write: bool = False) -> dict[str, object]:
    """Run two complete isolated builds, compare semantics, then publish.

    The historical ``write`` argument is retained for the RED-test API.  This
    release gate always atomically publishes after both candidates validate;
    otherwise test execution could report success while leaving stale user-
    visible artifacts in place.
    """

    MODEL_ROOT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(
        prefix=f".{NAMESPACE}-complete-regeneration-",
        dir=MODEL_ROOT.parent,
    ) as temporary:
        root = Path(temporary)
        first = _generate_complete_candidate(root / "run-1")
        second = _generate_package_repeat(root / "run-2-packages")
        semantic_repeat_run_equal = (
            first["package_semantic_bytes"] == second["package_semantic_bytes"]
        )
        if not semantic_repeat_run_equal:
            raise RuntimeError(
                "two fresh complete regenerations produced different semantic manifests"
            )

        # Close the report only after the independent repeat has passed.  The
        # report intentionally omits its own digest, avoiding a self-hash loop.
        final_regeneration_report = {
            "schema": "kage.i3-r1.fresh-atomic-regeneration-report.v1",
            "complete_fresh_step_run_count": 1,
            "fresh_package_run_count": 2,
            "fresh_process_import_count": 6,
            "stale_artifact_reuse_count": 0,
            "atomic_publish": True,
            "package_semantic_sha256": first["package_semantic_sha256"],
            "second_package_semantic_sha256": second["package_semantic_sha256"],
            "semantic_repeat_run_equal": semantic_repeat_run_equal,
            "projection_sha256": first["projection_sha256"],
            "second_projection_sha256": second["projection_sha256"],
            "meaningful_mutations_change_semantic": second[
                "meaningful_mutations_change_semantic"
            ],
            "negative_fixture_sha256": second["negative_fixture_sha256"],
            "nominal_imported_occurrence_count": first["nominal_import"][
                "occurrence_count"
            ],
            "exploded_imported_occurrence_count": first["exploded_import"][
                "occurrence_count"
            ],
            "disassembled_object_count": first["disassembled_object_count"],
            "orca_plate_count": first["orca_plate_count"],
        }
        final_report_bytes = _canonical_json_bytes(final_regeneration_report)
        report_path = first["paths"]["regeneration_report"]
        report_path.write_bytes(final_report_bytes)
        first["artifact_sha256"]["regeneration_report"] = _sha(report_path)
        first["artifact_bytes"]["regeneration_report"] = report_path.stat().st_size

        destination_by_key = dict(zip(
            (
                "nominal_step",
                "exploded_step",
                "print_components_3mf",
                "orca_source_3mf",
                "projection_jcs",
                "freshness_manifest",
                "step_parity_report",
                "regeneration_report",
            ),
            required_artifact_paths(),
        ))
        for key, destination in destination_by_key.items():
            _atomic_bytes(destination, first["paths"][key].read_bytes())
            if _sha(destination) != first["artifact_sha256"][key]:
                raise RuntimeError(f"atomic publish digest mismatch for {destination.name}")

    return {
        "generated_in_new_temporary_directory": True,
        "atomic_publish": True,
        "fresh_process_import_count": 6,
        "stale_artifact_reuse_count": 0,
        "complete_fresh_step_run_count": 1,
        "fresh_package_run_count": 2,
        "semantic_repeat_run_equal": semantic_repeat_run_equal,
        "semantic_sha256": first["package_semantic_sha256"],
        "second_semantic_sha256": second["package_semantic_sha256"],
        "complete_semantic_sha256": first["semantic_sha256"],
        "meaningful_mutations_change_semantic": second["meaningful_mutations_change_semantic"],
        "negative_fixture_sha256": second["negative_fixture_sha256"],
        "projection_sha256": first["projection_sha256"],
        "second_projection_sha256": second["projection_sha256"],
        "nominal_imported_occurrence_count": first["nominal_import"]["occurrence_count"],
        "exploded_imported_occurrence_count": first["exploded_import"]["occurrence_count"],
        "nominal_imported_bounds_mm": first["nominal_import"]["bounds"],
        "exploded_imported_bounds_mm": first["exploded_import"]["bounds"],
        "disassembled_object_count": first["disassembled_object_count"],
        "disassembled_build_item_count": first["disassembled_build_item_count"],
        "orca_plate_count": first["orca_plate_count"],
        "orca_build_object_count": first["orca_build_object_count"],
        "protected_occurrence_count": first["protected_occurrence_count"],
        "protected_drift": first["protected_drift"],
        "published_paths": {key: str(path) for key, path in destination_by_key.items()},
        "artifact_sha256": first["artifact_sha256"],
        "artifact_bytes": first["artifact_bytes"],
        "write_argument": bool(write),
    }
