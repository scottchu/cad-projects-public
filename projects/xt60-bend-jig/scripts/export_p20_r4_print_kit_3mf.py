"""Export the P21 R1 axial-width/cap-fit correction as a model-only 3MF."""

from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path

import lib3mf
from build123d import Shape

import xt60_bend_jig.p20_r4_blocked_test_print_3mf as p20


ROOT = Path(__file__).parents[1]
CAD_DIR = ROOT / "cad/p20_r4_custom_profile_full_cad"
STEP_PATH = CAD_DIR / "p20_r4_print_kit.step"
THREEMF_PATH = CAD_DIR / "p20_r4_print_kit.3mf"
PROVENANCE_PATH = CAD_DIR / "p20-r4-3mf-provenance.json"
BRIEF_PATH = ROOT / "docs/iterations/p21-r1-axial-width-cap-fit/BRIEF.md"
PARENT_MANIFEST_PATH = ROOT / "src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py"

PARENT_CANDIDATE_FINGERPRINT = "3eb9187ec7ad9205a2a1ced5e15e5a87a2a5a24e6c76282193ed086fb776d5b8"
EXPECTED_BRIEF_SHA256 = "b7f4a308b8f248041a54a9a075211c07a4dae844da82540d1ccdbd96308dddf8"
TESS_LINEAR_TOLERANCE_MM = 0.02
TESS_ANGULAR_TOLERANCE_RAD = 0.05
VERTEX_WELD_TOLERANCE_MM = 1.0e-6
BED_Z_TOLERANCE_MM = 1.0e-6
LAYOUT_OVERLAP_TOLERANCE_MM = 1.0e-7
VOLUME_TOLERANCE_MM3 = 1.0e-6
METADATA_NAMESPACE = "https://openai.com/codex/xt60-bend-jig/p21-r1"
EXCLUDED_OBJECTS = (
    "three required OD4 x 60 mm stainless rods",
    "XT60 reference body",
    "exact 90-degree two-conductor workpiece/wire",
    "all reference, collision, motion, tool, and coupon geometry",
)
KNOWN_PARENT_BLOCKERS = (
    "Blue rod / XT60 intersection 186.980487 mm3 at OPEN",
    "Blue rod / XT60 intersection 63.593308 mm3 at MID",
    "fixed-axle hex / inner-rim web 1.152 mm",
    "left outer Blue-Orange rail web 1.715 mm",
    "rod/workpiece contacts require functional disposition",
    "ID4.10 caps and 28.40 mm inner clear span require physical acceptance",
)


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _verify_frozen_inputs() -> dict[str, str]:
    values = {
        "parentCandidateFingerprint": _sha(PARENT_MANIFEST_PATH),
        "briefSha256": _sha(BRIEF_PATH),
        "sourceSha256": p20.source_revision_sha256(),
        "exporterSha256": _sha(Path(__file__)),
    }
    if values["parentCandidateFingerprint"] != PARENT_CANDIDATE_FINGERPRINT:
        raise ValueError("parent P21 R1 source fingerprint changed")
    if values["briefSha256"] != EXPECTED_BRIEF_SHA256:
        raise ValueError("blocked-test 3MF BRIEF fingerprint changed")
    return values


def _welded_triangles(
    shape: Shape,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    raw_vertices, raw_triangles = shape.tessellate(
        TESS_LINEAR_TOLERANCE_MM,
        TESS_ANGULAR_TOLERANCE_RAD,
    )
    vertex_by_key: dict[tuple[int, int, int], int] = {}
    vertices: list[tuple[float, float, float]] = []
    remap: list[int] = []
    for vertex in raw_vertices:
        point = (float(vertex.X), float(vertex.Y), float(vertex.Z))
        key = tuple(int(round(value / VERTEX_WELD_TOLERANCE_MM)) for value in point)
        if key not in vertex_by_key:
            vertex_by_key[key] = len(vertices)
            vertices.append(point)
        remap.append(vertex_by_key[key])
    triangles = []
    for first, second, third in raw_triangles:
        triangle = (remap[first], remap[second], remap[third])
        if len(set(triangle)) == 3:
            triangles.append(triangle)
    edges: Counter[tuple[int, int]] = Counter()
    directed: Counter[tuple[int, int]] = Counter()
    for first, second, third in triangles:
        for start, end in ((first, second), (second, third), (third, first)):
            edges[tuple(sorted((start, end)))] += 1
            directed[(start, end)] += 1
    if any(count != 2 for count in edges.values()):
        raise ValueError(f"{shape.label}: welded mesh has an open/non-manifold edge")
    if any(
        directed[(first, second)] != 1 or directed[(second, first)] != 1
        for first, second in edges
    ):
        raise ValueError(f"{shape.label}: welded mesh has inconsistent orientation")
    return vertices, triangles


def _signed_volume(
    vertices: list[tuple[float, float, float]],
    triangles: list[tuple[int, int, int]],
) -> float:
    total = 0.0
    for first, second, third in triangles:
        ax, ay, az = vertices[first]
        bx, by, bz = vertices[second]
        cx, cy, cz = vertices[third]
        total += (
            ax * (by * cz - bz * cy)
            + ay * (bz * cx - bx * cz)
            + az * (bx * cy - by * cx)
        ) / 6.0
    return total


def _bounds_from_vertices(
    vertices: list[tuple[float, float, float]],
) -> list[float]:
    return [
        min(v[0] for v in vertices),
        min(v[1] for v in vertices),
        min(v[2] for v in vertices),
        max(v[0] for v in vertices),
        max(v[1] for v in vertices),
        max(v[2] for v in vertices),
    ]


def _bounds(shape: Shape) -> list[float]:
    box = shape.bounding_box()
    return [
        float(box.min.X),
        float(box.min.Y),
        float(box.min.Z),
        float(box.max.X),
        float(box.max.Y),
        float(box.max.Z),
    ]


def _validate_layout(bounds_by_label: dict[str, list[float]]) -> dict[str, object]:
    overlaps = []
    for first, second in combinations(bounds_by_label, 2):
        a = bounds_by_label[first]
        b = bounds_by_label[second]
        overlap_x = min(a[3], b[3]) - max(a[0], b[0])
        overlap_y = min(a[4], b[4]) - max(a[1], b[1])
        if overlap_x > LAYOUT_OVERLAP_TOLERANCE_MM and overlap_y > LAYOUT_OVERLAP_TOLERANCE_MM:
            overlaps.append({"first": first, "second": second, "overlapX": overlap_x, "overlapY": overlap_y})
    if overlaps:
        raise ValueError(f"bed-layout bounding boxes overlap: {overlaps}")
    if any(abs(row[2]) > BED_Z_TOLERANCE_MM or row[2] < -BED_Z_TOLERANCE_MM for row in bounds_by_label.values()):
        raise ValueError("one or more objects do not contact Z=0 bed")
    minimum_x = min(row[0] for row in bounds_by_label.values())
    minimum_y = min(row[1] for row in bounds_by_label.values())
    maximum_x = max(row[3] for row in bounds_by_label.values())
    maximum_y = max(row[4] for row in bounds_by_label.values())
    return {
        "boundsXYMm": [minimum_x, minimum_y, maximum_x, maximum_y],
        "footprintXYMm": [maximum_x - minimum_x, maximum_y - minimum_y],
        "pairwiseBoundingBoxOverlapCount": 0,
        "allMinimumZOnBed": True,
    }


def _transform_rows(transform: object) -> list[list[float]]:
    return [[float(value) for value in row] for row in transform.Fields]  # type: ignore[attr-defined]


def export() -> dict[str, object]:
    frozen = _verify_frozen_inputs()
    if not STEP_PATH.exists():
        raise FileNotFoundError(f"generate STEP before 3MF: {STEP_PATH}")
    parts = list(p20.build_print_parts())
    source_parts = [row[0] for row in p20.build_print_source_parts()]
    labels = tuple(part.label for part in parts)
    if labels != p20.PRINT_OBJECT_LABELS or len(set(labels)) != 13:
        raise ValueError(f"source object census mismatch: {labels}")
    rows = []
    bounds_by_label = {part.label: _bounds(part) for part in parts}
    source_layout = _validate_layout(bounds_by_label)

    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.SetUnit(lib3mf.ModelUnit.MilliMeter)
    metadata = model.GetMetaDataGroup()
    embedded = {
        "parentCandidateFingerprint": frozen["parentCandidateFingerprint"],
        "sourceSha256": frozen["sourceSha256"],
        "parentSourceSha256": p20.PARENT_SOURCE_SHA256,
        "briefSha256": frozen["briefSha256"],
        "exporterSha256": frozen["exporterSha256"],
        "artifactRole": "blocked-test-model-only-13-printable-objects",
        "manufacturingAccepted": "false",
        "printingInitiated": "false",
    }
    for key, value in embedded.items():
        metadata.AddMetaData(METADATA_NAMESPACE, key, value, "xs:string", True)

    for part, source in zip(parts, source_parts, strict=True):
        if len(part.solids()) != 1 or not part.is_valid or float(part.volume) <= 0.0:
            raise ValueError(f"{part.label}: source part is not one valid positive solid")
        volume_delta = abs(float(part.volume) - float(source.volume))
        if volume_delta > VOLUME_TOLERANCE_MM3:
            raise ValueError(f"{part.label}: rigid-transform source volume changed by {volume_delta}")
        vertices, triangles = _welded_triangles(part)
        signed_volume = _signed_volume(vertices, triangles)
        if signed_volume <= 0.0:
            raise ValueError(f"{part.label}: mesh signed volume is not positive")
        mesh = model.AddMeshObject()
        mesh.SetName(part.label)
        mesh.SetGeometry(
            [lib3mf.Position(vertex) for vertex in vertices],
            [lib3mf.Triangle(triangle) for triangle in triangles],
        )
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError(f"{part.label}: lib3mf rejected source-derived mesh")
        model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
        rows.append(
            {
                "label": part.label,
                "sourceBREPVolumeMm3": float(source.volume),
                "placedBREPVolumeMm3": float(part.volume),
                "sourceToPlacedVolumeDeltaMm3": volume_delta,
                "meshSignedVolumeMm3": signed_volume,
                "vertexCount": len(vertices),
                "triangleCount": len(triangles),
                "boundsMm": bounds_by_label[part.label],
                "minimumZMm": bounds_by_label[part.label][2],
            }
        )

    CAD_DIR.mkdir(parents=True, exist_ok=True)
    model.QueryWriter("3mf").WriteToFile(str(THREEMF_PATH))

    check = wrapper.CreateModel()
    check.QueryReader("3mf").ReadFromFile(str(THREEMF_PATH))
    if check.GetUnit() != lib3mf.ModelUnit.MilliMeter:
        raise ValueError("round-trip 3MF unit is not millimetres")
    mesh_iterator = check.GetMeshObjects()
    roundtrip_labels = []
    roundtrip_bounds: dict[str, list[float]] = {}
    while mesh_iterator.MoveNext():
        mesh = mesh_iterator.GetCurrentMeshObject()
        label = mesh.GetName()
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError(f"{label}: round-trip mesh invalid")
        vertices = [tuple(float(value) for value in vertex.Coordinates) for vertex in mesh.GetVertices()]
        triangles = [tuple(int(value) for value in triangle.Indices) for triangle in mesh.GetTriangleIndices()]
        if not vertices or not triangles or _signed_volume(vertices, triangles) <= 0.0:
            raise ValueError(f"{label}: round-trip mesh empty or non-positive")
        roundtrip_labels.append(label)
        roundtrip_bounds[label] = _bounds_from_vertices(vertices)
    if tuple(roundtrip_labels) != p20.PRINT_OBJECT_LABELS:
        raise ValueError(f"round-trip mesh order mismatch: {roundtrip_labels}")
    roundtrip_layout = _validate_layout(roundtrip_bounds)

    build_iterator = check.GetBuildItems()
    build_labels = []
    identity = _transform_rows(wrapper.GetIdentityTransform())
    while build_iterator.MoveNext():
        item = build_iterator.GetCurrent()
        build_labels.append(item.GetObjectResource().GetName())
        if _transform_rows(item.GetObjectTransform()) != identity:
            raise ValueError(f"{build_labels[-1]}: build transform is not identity")
    if tuple(build_labels) != p20.PRINT_OBJECT_LABELS:
        raise ValueError(f"round-trip build-item order mismatch: {build_labels}")

    metadata_check = check.GetMetaDataGroup()
    checked_metadata = {
        key: metadata_check.GetMetaDataByKey(METADATA_NAMESPACE, key).GetValue()
        for key in embedded
    }
    if checked_metadata != embedded:
        raise ValueError("embedded metadata failed round-trip")

    payload = {
        "schema": "P21R1AxialWidthCapFitThreeMFProvenance/v1",
        "artifact": {
            "path": str(THREEMF_PATH.relative_to(ROOT)),
            "sha256": _sha(THREEMF_PATH),
            "role": embedded["artifactRole"],
            "modelOnly": True,
            "objectCount": 13,
            "meshObjectCount": len(roundtrip_labels),
            "buildItemCount": len(build_labels),
            "unit": "millimetre",
            "labels": list(roundtrip_labels),
            "objects": rows,
            "layout": roundtrip_layout,
            "lib3mfRoundTripValid": True,
            "allMeshesManifoldAndOriented": True,
            "allBuildTransformsIdentity": True,
        },
        "step": {"path": str(STEP_PATH.relative_to(ROOT)), "sha256": _sha(STEP_PATH)},
        "sourceLayout": source_layout,
        "parentCandidateFingerprint": frozen["parentCandidateFingerprint"],
        "sourceSha256": frozen["sourceSha256"],
        "parentSourceSha256": p20.PARENT_SOURCE_SHA256,
        "briefSha256": frozen["briefSha256"],
        "exporterSha256": frozen["exporterSha256"],
        "embeddedMetadata": checked_metadata,
        "excluded": list(EXCLUDED_OBJECTS),
        "knownParentBlockers": list(KNOWN_PARENT_BLOCKERS),
        "geometryChangedForThreeMF": False,
        "manufacturingAccepted": False,
        "printingInitiated": False,
        "sliced": False,
        "uploaded": False,
    }
    PROVENANCE_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main() -> int:
    print(json.dumps(export(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
