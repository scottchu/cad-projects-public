"""Zero-geometry-change Stage A print exports from the immutable locked STEP.

The locked STEP is imported directly.  This adapter may translate whole
occurrences for print layout, but never rebuilds, scales, fuses, cuts, or
otherwise edits a source solid.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from html import escape
import json
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import Compound, Location, export_step, import_step


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_locked_stage_a_print_exports"
MODEL_ROOT = ROOT / "models" / NAMESPACE
LOCKED_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
LOCKED_STEP = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step"
PARITY_JSON = ROOT / "models" / "p3_v3_locked_parametric_repair_r1" / "p3_v3_locked_parametric_repair_r1_zero_delta_parity.json"
LOCKED_STEP_SHA256 = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"
BUILD_VOLUME_MM = (260.0, 260.0, 260.0)
BED_MARGIN_MM = 5.0
MIN_OBJECT_GAP_MM = 3.0


PACKS: dict[str, dict[str, Any]] = {
    "base_joinery": {
        "status": "STAGE_A_TEST_PACK",
        "description": "Minimum adjacent rear-chassis Q1/Q2 pair for the frozen flat seam.",
        "indices": (0, 1),
        "factories": ("make_chassis_segments()[0]", "make_chassis_segments()[1]"),
        "xy": ((5.0, 5.0), (110.0, 110.0)),
    },
    "roller_tower": {
        "status": "STAGE_A_TEST_PACK",
        "description": "One frozen tower-1 printable yoke, spacers, washers, and three role rollers.",
        "indices": tuple(range(18, 26)),
        "factories": (
            "make_roller_tower_yoke(0)",
            "make_tower_spacers(0)[0]", "make_tower_spacers(0)[1]",
            "make_tower_thrust_washers(0)[0]", "make_tower_thrust_washers(0)[1]",
            "make_roller(0, 0)", "make_roller(1, 0)", "make_roller(2, 0)",
        ),
    },
    "motor_station": {
        "status": "STAGE_A_TEST_PACK",
        "description": "Frozen hour-station printable subset; purchased/reference solids excluded.",
        "indices": (69, 130, 131, 135, 136),
        "factories": (
            "make_unibody_drive_yoke(0)",
            "make_motor_station_parts(0)[2]", "make_motor_station_parts(0)[3]",
            "make_motor_station_parts(0)[7]", "make_motor_station_parts(0)[8]",
        ),
    },
    "ring_seam_review_only": {
        "status": "REVIEW_ONLY_DO_NOT_PRINT",
        "description": "Exact frozen hour Q1/Q2 seam-2 occurrence set.",
        "warning": (
            "Contains the frozen 3 mm alignment dowel contrary to the current user preference. "
            "A later intentional, versioned screw-only redesign is required before printing."
        ),
        "indices": (108, 109, 116, 117),
        "factories": (
            "make_ring_quadrant(0, 0)", "make_ring_quadrant(0, 1)",
            "make_seam_hardware(0)[4]", "make_seam_hardware(0)[5]",
        ),
        "xy": ((5.0, 5.0), (110.0, 110.0), (230.0, 10.0), (245.0, 10.0)),
    },
}


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _aabb(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return tuple(round(float(v), 9) for v in (
        box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z,
    ))


def _dimensions(shape) -> tuple[float, float, float]:
    box = shape.bounding_box()
    return tuple(round(float(v), 9) for v in (box.size.X, box.size.Y, box.size.Z))


def _topology(shape) -> dict[str, int]:
    return {
        "solids": len(shape.solids()), "shells": len(shape.shells()),
        "faces": len(shape.faces()), "edges": len(shape.edges()),
        "vertices": len(shape.vertices()),
    }


def brep_fingerprint(shape) -> dict[str, Any]:
    """Match the canonical fingerprint stored in the frozen parity manifest."""
    topology = _topology(shape)
    vertices = sorted(tuple(round(float(v), 9) for v in (p.X, p.Y, p.Z)) for p in shape.vertices())
    edges = sorted((str(e.geom_type), round(float(e.length), 9), tuple(round(float(v), 9) for v in e.center())) for e in shape.edges())
    faces = sorted((str(f.geom_type), round(float(f.area), 9), tuple(round(float(v), 9) for v in f.center())) for f in shape.faces())
    canonical = json.dumps(
        {"topology": topology, "vertices": vertices, "edges": edges, "faces": faces, "aabb": _aabb(shape)},
        sort_keys=True, separators=(",", ":"),
    ).encode()
    return {
        "brep_sha256": sha256(canonical).hexdigest(),
        "topology": topology,
        "volume_mm3": round(float(sum(s.volume for s in shape.solids())), 9),
        "area_mm2": round(float(sum(f.area for f in shape.faces())), 9),
        "aabb_mm": _aabb(shape),
    }


def _normalized_fingerprint(shape) -> dict[str, Any]:
    box = shape.bounding_box()
    normalized = deepcopy(shape).moved(Location((-box.min.X, -box.min.Y, -box.min.Z)))
    return brep_fingerprint(normalized)


@lru_cache(maxsize=1)
def authority() -> tuple[dict[str, Any], tuple[Any, ...]]:
    if _sha(LOCKED_STEP) != LOCKED_STEP_SHA256:
        raise RuntimeError("immutable locked assembled STEP hash drift")
    manifest = json.loads(PARITY_JSON.read_text())
    if manifest["locked_step_sha256"] != LOCKED_STEP_SHA256:
        raise RuntimeError("parity manifest names a different locked STEP")
    if any(manifest[key] for key in (
        "unknown_occurrence_names", "unclassified_occurrence_names", "protected_drift_occurrence_names",
    )):
        raise RuntimeError("parity manifest is not zero-delta clean")
    assembly = import_step(LOCKED_STEP)
    children = tuple(assembly.children)
    if len(children) != 201 or len(manifest["occurrences"]) != 201:
        raise RuntimeError("locked occurrence count drift")
    return manifest, children


def source_rows(pack_name: str) -> list[dict[str, Any]]:
    manifest, children = authority()
    spec = PACKS[pack_name]
    rows = []
    for index, factory in zip(spec["indices"], spec["factories"], strict=True):
        source = children[index]
        frozen = manifest["occurrences"][index]
        facts = brep_fingerprint(source)
        if source.label != frozen["label"] or facts["brep_sha256"] != frozen["brep_fingerprint"]["brep_sha256"]:
            raise RuntimeError(f"frozen occurrence extraction mismatch: occurrence_{index:03d}")
        rows.append({
            "occurrence_index": index,
            "occurrence_name": f"occurrence_{index:03d}",
            "frozen_generator_function": factory,
            "frozen_label": source.label,
            "frozen_owner_group": frozen["owner_group"],
            "frozen_brep_sha256": facts["brep_sha256"],
            "frozen_aabb_mm": facts["aabb_mm"],
            "frozen_dimensions_mm": _dimensions(source),
            "frozen_topology": facts["topology"],
            "frozen_volume_mm3": facts["volume_mm3"],
            "shape": source,
        })
    return rows


def _shelf_xy(rows: list[dict[str, Any]]) -> tuple[tuple[float, float], ...]:
    x = y = BED_MARGIN_MM
    row_height = 0.0
    result = []
    for row in rows:
        w, h, _ = row["frozen_dimensions_mm"]
        if x + w > BUILD_VOLUME_MM[0] - BED_MARGIN_MM:
            x = BED_MARGIN_MM
            y += row_height + MIN_OBJECT_GAP_MM
            row_height = 0.0
        result.append((x, y))
        x += w + MIN_OBJECT_GAP_MM
        row_height = max(row_height, h)
    return tuple(result)


def layout_rows(pack_name: str) -> list[dict[str, Any]]:
    rows = source_rows(pack_name)
    xy = PACKS[pack_name].get("xy") or _shelf_xy(rows)
    output = []
    for row, (target_x, target_y) in zip(rows, xy, strict=True):
        box = row["shape"].bounding_box()
        translation = (target_x - box.min.X, target_y - box.min.Y, -box.min.Z)
        placed = deepcopy(row["shape"]).moved(Location(translation))
        placed.label = row["frozen_label"]
        output.append({**row, "print_translation_mm": translation, "print_aabb_mm": _aabb(placed), "shape": placed})
    return output


def pack_shape(pack_name: str):
    # STEP stays in the exact locked assembly frame so its per-occurrence
    # canonical BREP hashes remain byte-for-byte comparable to the authority.
    # Translation-only print placement belongs exclusively to the 3MF.
    return Compound(
        children=[row["shape"] for row in source_rows(pack_name)],
        label=f"{NAMESPACE}_{pack_name}",
    )


def artifact_paths(pack_name: str) -> tuple[Path, Path]:
    return MODEL_ROOT / f"{pack_name}.step", MODEL_ROOT / f"{pack_name}.3mf"


def _mesh(shape):
    vertices, triangles = shape.tessellate(0.05, 0.15)
    return (
        [(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        [(int(a), int(b), int(c)) for a, b, c in triangles],
    )


def _write_3mf(pack_name: str, path: Path) -> None:
    resources, items = [], []
    for object_id, row in enumerate(layout_rows(pack_name), start=1):
        vertices, triangles = _mesh(row["shape"])
        vertex_xml = "".join(f'<vertex x="{x:.12g}" y="{y:.12g}" z="{z:.12g}"/>' for x, y, z in vertices)
        triangle_xml = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles)
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(row["frozen_label"])}">'
            f'<metadata name="kage:frozenOccurrence">{row["occurrence_name"]}</metadata>'
            f'<mesh><vertices>{vertex_xml}</vertices><triangles>{triangle_xml}</triangles></mesh></object>'
        )
        items.append(f'<item objectid="{object_id}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        f'<metadata name="Title">{escape(NAMESPACE + " " + pack_name)}</metadata>'
        f'<resources>{"".join(resources)}</resources><build>{"".join(items)}</build></model>'
    ).encode()
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        '</Types>'
    ).encode()
    rels = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        '</Relationships>'
    ).encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", content_types)
        package.writestr("_rels/.rels", rels)
        package.writestr("3D/3dmodel.model", model)


def read_3mf_objects(path: Path) -> list[dict[str, Any]]:
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(path) as package:
        if package.testzip() is not None:
            raise RuntimeError(f"3MF CRC failure: {path}")
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    rows = []
    for obj in root.findall("m:resources/m:object", ns):
        vertices = [tuple(float(v.attrib[a]) for a in ("x", "y", "z")) for v in obj.findall("m:mesh/m:vertices/m:vertex", ns)]
        triangles = [tuple(int(t.attrib[a]) for a in ("v1", "v2", "v3")) for t in obj.findall("m:mesh/m:triangles/m:triangle", ns)]
        rows.append({"name": obj.attrib["name"], "vertices": vertices, "triangles": triangles})
    return rows


def _clean(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "shape"}


def export_all(*, include_review_only: bool = True) -> tuple[Path, ...]:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    names = ["base_joinery", "roller_tower", "motor_station"]
    if include_review_only:
        names.append("ring_seam_review_only")
    outputs: list[Path] = []
    pack_records = []
    for name in names:
        step_path, mf_path = artifact_paths(name)
        export_step(pack_shape(name), step_path)
        _write_3mf(name, mf_path)
        source = source_rows(name)
        placed = layout_rows(name)
        imported = tuple(import_step(step_path).children)
        mesh_objects = read_3mf_objects(mf_path)
        objects = []
        for src, out, step_obj, mesh in zip(source, placed, imported, mesh_objects, strict=True):
            objects.append({
                **_clean(src),
                "print_translation_mm": out["print_translation_mm"],
                "print_aabb_mm": out["print_aabb_mm"],
                "step_reimport_label": step_obj.label,
                "step_reimport_dimensions_mm": _dimensions(step_obj),
                "step_reimport_brep_sha256": brep_fingerprint(step_obj)["brep_sha256"],
                "three_mf_object_name": mesh["name"],
                "three_mf_vertex_count": len(mesh["vertices"]),
                "three_mf_triangle_count": len(mesh["triangles"]),
            })
        pack_records.append({
            "name": name,
            "status": PACKS[name]["status"],
            "description": PACKS[name]["description"],
            "warning": PACKS[name].get("warning"),
            "step": {"path": str(step_path.relative_to(ROOT)), "sha256": _sha(step_path)},
            "three_mf": {"path": str(mf_path.relative_to(ROOT)), "sha256": _sha(mf_path)},
            "objects": objects,
        })
        outputs.extend((step_path, mf_path))
    authority_manifest, _ = authority()
    manifest_path = MODEL_ROOT / "stage_a_print_export_manifest.json"
    manifest_path.write_text(json.dumps({
        "schema": "kage.p3-v3.locked-stage-a-print-exports.v1",
        "namespace": NAMESPACE,
        "geometry_policy": "exact locked STEP occurrences; translation-only print layout",
        "authority": {
            "locked_step_path": str(LOCKED_STEP.relative_to(ROOT)),
            "locked_step_sha256": LOCKED_STEP_SHA256,
            "parity_manifest_path": str(PARITY_JSON.relative_to(ROOT)),
            "parity_manifest_sha256": _sha(PARITY_JSON),
            "locked_generator_sha256": authority_manifest["locked_generator_sha256"],
        },
        "build_volume_mm": BUILD_VOLUME_MM,
        "bed_margin_mm": BED_MARGIN_MM,
        "packs": pack_records,
    }, indent=2, sort_keys=True) + "\n")
    outputs.append(manifest_path)
    return tuple(outputs)


def write_existing_manifest(*, include_review_only: bool = False) -> Path:
    """Write traceability for already-exported packs without rebuilding geometry."""
    parity = json.loads(PARITY_JSON.read_text())
    names = ["base_joinery", "roller_tower", "motor_station"]
    if include_review_only:
        names.append("ring_seam_review_only")
    packs = []
    for name in names:
        step_path, mf_path = artifact_paths(name)
        if not step_path.is_file() or not mf_path.is_file():
            raise FileNotFoundError(f"missing Stage A artifact for {name}")
        spec = PACKS[name]
        frozen = [parity["occurrences"][i] for i in spec["indices"]]
        sizing_rows = [{"frozen_dimensions_mm": (
            row["aabb_mm"][3] - row["aabb_mm"][0],
            row["aabb_mm"][4] - row["aabb_mm"][1],
            row["aabb_mm"][5] - row["aabb_mm"][2],
        )} for row in frozen]
        xy = spec.get("xy") or _shelf_xy(sizing_rows)
        mesh = read_3mf_objects(mf_path)
        objects = []
        for index, factory, row, target, mesh_row in zip(
            spec["indices"], spec["factories"], frozen, xy, mesh, strict=True,
        ):
            aabb = row["aabb_mm"]
            dx, dy, dz = target[0] - aabb[0], target[1] - aabb[1], -aabb[2]
            objects.append({
                "occurrence_name": f"occurrence_{index:03d}",
                "frozen_generator_function": factory,
                "frozen_label": row["label"],
                "frozen_owner_group": row["owner_group"],
                "frozen_brep_sha256": row["brep_fingerprint"]["brep_sha256"],
                "frozen_aabb_mm": aabb,
                "frozen_dimensions_mm": sizing_rows[len(objects)]["frozen_dimensions_mm"],
                "frozen_topology": row["topology"],
                "frozen_volume_mm3": row["volume_mm3"],
                "step_object_name": row["label"],
                "three_mf_object_name": mesh_row["name"],
                "three_mf_vertex_count": len(mesh_row["vertices"]),
                "three_mf_triangle_count": len(mesh_row["triangles"]),
                "print_translation_mm": (dx, dy, dz),
                "print_aabb_mm": (
                    aabb[0] + dx, aabb[1] + dy, aabb[2] + dz,
                    aabb[3] + dx, aabb[4] + dy, aabb[5] + dz,
                ),
            })
        packs.append({
            "name": name, "status": spec["status"],
            "description": spec["description"], "warning": spec.get("warning"),
            "step": {"path": str(step_path.relative_to(ROOT)), "sha256": _sha(step_path)},
            "three_mf": {"path": str(mf_path.relative_to(ROOT)), "sha256": _sha(mf_path)},
            "objects": objects,
        })
    path = MODEL_ROOT / "stage_a_print_export_manifest.json"
    path.write_text(json.dumps({
        "schema": "kage.p3-v3.locked-stage-a-print-exports.v1",
        "namespace": NAMESPACE,
        "geometry_policy": "STEP exact assembly-frame occurrences; 3MF translation-only print layout",
        "authority": {
            "locked_step_path": str(LOCKED_STEP.relative_to(ROOT)),
            "locked_step_sha256": LOCKED_STEP_SHA256,
            "parity_manifest_path": str(PARITY_JSON.relative_to(ROOT)),
            "parity_manifest_sha256": _sha(PARITY_JSON),
            "locked_generator_sha256": parity["locked_generator_sha256"],
        },
        "build_volume_mm": BUILD_VOLUME_MM,
        "bed_margin_mm": BED_MARGIN_MM,
        "packs": packs,
        "deferred_review_only_pack": None if include_review_only else {
            "name": "ring_seam_review_only",
            "reason": PACKS["ring_seam_review_only"]["warning"],
        },
    }, indent=2, sort_keys=True) + "\n")
    return path


if __name__ == "__main__":
    for output in export_all():
        print(output)
