"""Export and validate source-derived P13 production and coupon 3MF files."""

from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import sqrt
from pathlib import Path

import lib3mf
from build123d import Shape

import xt60_bend_jig.p13_four_plate_three_rod as p13


ROOT = Path(__file__).parents[1]
OUT = ROOT / "cad" / "p13_four_plate_three_rod"
PRODUCTION_3MF = OUT / "p13_print_kit.3mf"
COUPON_3MF = OUT / "p13_fit_coupons.3mf"
PROVENANCE = OUT / "p13-3mf-provenance.json"
PRODUCTION_LABELS = (
    "left_D_bore_cam_OD40p50_theta_0p00",
    "left_fixed_OD40p50_integral_upward_C_journal_ID4p80",
    "right_fixed_OD40p50_integral_upward_C_journal_ID4p80",
    "right_D_bore_cam_actuator_OD40p50_theta_0p00",
    "separate_printed_D_shaft_OD5p60_AF5p15_theta_0p00",
    "round_C_shaft_keeper_OD9p60_ID4p80",
    "print_permanent_left_cap_1",
    "print_permanent_left_cap_2",
    "print_permanent_left_cap_3",
    "print_removable_right_cap_1",
    "print_removable_right_cap_2",
    "print_removable_right_cap_3",
)
COUPON_LABELS = (
    "diagnostic_lane_width_coupon_role",
    "diagnostic_D_bore_and_round_journal_coupon_role",
)
PRINCIPAL_LABELS = PRODUCTION_LABELS[:4]
TESS_LINEAR_TOLERANCE_MM = 0.02
TESS_ANGULAR_TOLERANCE_RAD = 0.05
VERTEX_WELD_TOLERANCE_MM = 1.0e-6
LAYOUT_OVERLAP_TOLERANCE_MM = 1.0e-7
BED_Z_TOLERANCE_MM = 1.0e-6
PRINCIPAL_MINIMUM_BED_AREA_MM2 = 1000.0


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
        key = tuple(
            int(round(value / VERTEX_WELD_TOLERANCE_MM)) for value in point
        )
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


def _mesh_signed_volume(
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


def _mesh_bed_metrics(
    vertices: list[tuple[float, float, float]],
    triangles: list[tuple[int, int, int]],
) -> dict[str, object]:
    minimum_z = min(vertex[2] for vertex in vertices)
    maximum_z = max(vertex[2] for vertex in vertices)
    bed_area = 0.0
    bed_triangle_count = 0
    for first, second, third in triangles:
        a = vertices[first]
        b = vertices[second]
        c = vertices[third]
        if not all(abs(point[2]) <= BED_Z_TOLERANCE_MM for point in (a, b, c)):
            continue
        ab = tuple(b[index] - a[index] for index in range(3))
        ac = tuple(c[index] - a[index] for index in range(3))
        cross = (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0],
        )
        bed_area += 0.5 * sqrt(sum(value * value for value in cross))
        bed_triangle_count += 1
    return {
        "boundsZMm": [minimum_z, maximum_z],
        "minimumZMm": minimum_z,
        "maximumZMm": maximum_z,
        "coplanarZ0TriangleAreaMm2": bed_area,
        "coplanarZ0TriangleCount": bed_triangle_count,
    }


def _require_principal_bed_contact(label: str, metrics: dict[str, object]) -> None:
    minimum_z = float(metrics["minimumZMm"])
    bed_area = float(metrics["coplanarZ0TriangleAreaMm2"])
    if minimum_z < -BED_Z_TOLERANCE_MM:
        raise ValueError(f"{label}: principal mesh has negative Z={minimum_z}")
    if abs(minimum_z) > BED_Z_TOLERANCE_MM:
        raise ValueError(f"{label}: principal mesh minimum Z is not zero: {minimum_z}")
    if bed_area <= PRINCIPAL_MINIMUM_BED_AREA_MM2:
        raise ValueError(
            f"{label}: principal mesh Z=0 coplanar triangle area {bed_area} "
            f"does not exceed {PRINCIPAL_MINIMUM_BED_AREA_MM2} mm^2"
        )


def _xy_bbox(shape: Shape) -> tuple[float, float, float, float]:
    box = shape.bounding_box()
    return float(box.min.X), float(box.min.Y), float(box.max.X), float(box.max.Y)


def _validate_bed_layout(parts: list[Shape]) -> dict[str, object]:
    boxes = {part.label: _xy_bbox(part) for part in parts}
    overlaps = []
    for first, second in combinations(parts, 2):
        a = boxes[first.label]
        b = boxes[second.label]
        overlap_x = min(a[2], b[2]) - max(a[0], b[0])
        overlap_y = min(a[3], b[3]) - max(a[1], b[1])
        if (
            overlap_x > LAYOUT_OVERLAP_TOLERANCE_MM
            and overlap_y > LAYOUT_OVERLAP_TOLERANCE_MM
        ):
            overlaps.append(
                {
                    "first": first.label,
                    "second": second.label,
                    "overlapX": overlap_x,
                    "overlapY": overlap_y,
                }
            )
    if overlaps:
        raise ValueError(f"bed-layout bounding boxes overlap: {overlaps}")
    minimum_x = min(row[0] for row in boxes.values())
    minimum_y = min(row[1] for row in boxes.values())
    maximum_x = max(row[2] for row in boxes.values())
    maximum_y = max(row[3] for row in boxes.values())
    return {
        "boundsXY": [minimum_x, minimum_y, maximum_x, maximum_y],
        "footprintXY": [maximum_x - minimum_x, maximum_y - minimum_y],
        "pairwiseBoundingBoxOverlapCount": 0,
    }


def _export_one(
    output: Path,
    parts: list[Shape],
    expected_labels: tuple[str, ...],
    role: str,
) -> dict[str, object]:
    labels = tuple(part.label for part in parts)
    if labels != expected_labels or len(set(labels)) != len(labels):
        raise ValueError(f"{role}: source object census mismatch: {labels}")
    if any(len(part.solids()) != 1 or float(part.volume) <= 0.0 for part in parts):
        raise ValueError(f"{role}: every source object must be one positive-volume solid")
    layout = _validate_bed_layout(parts)
    source_hash = p13.source_revision_sha256()
    manifest_hash = p13.parameter_manifest_sha256()
    brief_hash = p13.P13_GATE0_BRIEF_SHA256
    amendment_hash = p13.P13_DOMAIN_AMENDMENT_SHA256
    exporter_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.SetUnit(lib3mf.ModelUnit.MilliMeter)
    metadata = model.GetMetaDataGroup()
    namespace = "https://openai.com/codex/xt60-bend-jig/p13"
    metadata.AddMetaData(namespace, "sourceRevisionSha256", source_hash, "xs:string", True)
    metadata.AddMetaData(namespace, "parameterManifestSha256", manifest_hash, "xs:string", True)
    metadata.AddMetaData(namespace, "parentBriefSha256", brief_hash, "xs:string", True)
    metadata.AddMetaData(
        namespace,
        "controllingAmendmentSha256",
        amendment_hash,
        "xs:string",
        True,
    )
    metadata.AddMetaData(namespace, "artifactRole", role, "xs:string", True)
    metadata.AddMetaData(namespace, "exporterSha256", exporter_hash, "xs:string", True)
    rows = []
    for part in parts:
        vertices, triangles = _welded_triangles(part)
        signed_volume = _mesh_signed_volume(vertices, triangles)
        if signed_volume <= 0.0:
            raise ValueError(f"{part.label}: mesh signed volume is not positive")
        source_bed_metrics = _mesh_bed_metrics(vertices, triangles)
        if part.label in PRINCIPAL_LABELS:
            _require_principal_bed_contact(part.label, source_bed_metrics)
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
                "sourceBREPVolume": float(part.volume),
                "meshSignedVolume": signed_volume,
                "vertexCount": len(vertices),
                "triangleCount": len(triangles),
                "boundsXY": list(_xy_bbox(part)),
                "sourceMeshBedContact": source_bed_metrics,
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    model.QueryWriter("3mf").WriteToFile(str(output))

    check_model = wrapper.CreateModel()
    check_model.QueryReader("3mf").ReadFromFile(str(output))
    iterator = check_model.GetMeshObjects()
    roundtrip_labels = []
    rows_by_label = {row["label"]: row for row in rows}
    while iterator.MoveNext():
        mesh = iterator.GetCurrentMeshObject()
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError(f"{mesh.GetName()}: round-trip 3MF mesh invalid")
        if mesh.GetVertexCount() <= 0 or mesh.GetTriangleCount() <= 0:
            raise ValueError(f"{mesh.GetName()}: round-trip 3MF mesh is empty")
        label = mesh.GetName()
        roundtrip_labels.append(label)
        roundtrip_vertices = [
            tuple(float(value) for value in vertex.Coordinates)
            for vertex in mesh.GetVertices()
        ]
        roundtrip_triangles = [
            tuple(int(value) for value in triangle.Indices)
            for triangle in mesh.GetTriangleIndices()
        ]
        roundtrip_bed_metrics = _mesh_bed_metrics(
            roundtrip_vertices,
            roundtrip_triangles,
        )
        if label in PRINCIPAL_LABELS:
            _require_principal_bed_contact(label, roundtrip_bed_metrics)
        rows_by_label[label]["writtenRoundTripBedContact"] = roundtrip_bed_metrics
    if tuple(roundtrip_labels) != expected_labels:
        raise ValueError(f"{role}: round-trip object census mismatch")
    metadata_check = check_model.GetMetaDataGroup()
    embedded = {
        "sourceRevisionSha256": metadata_check.GetMetaDataByKey(
            namespace, "sourceRevisionSha256"
        ).GetValue(),
        "parameterManifestSha256": metadata_check.GetMetaDataByKey(
            namespace, "parameterManifestSha256"
        ).GetValue(),
        "parentBriefSha256": metadata_check.GetMetaDataByKey(
            namespace, "parentBriefSha256"
        ).GetValue(),
        "controllingAmendmentSha256": metadata_check.GetMetaDataByKey(
            namespace, "controllingAmendmentSha256"
        ).GetValue(),
        "artifactRole": metadata_check.GetMetaDataByKey(
            namespace, "artifactRole"
        ).GetValue(),
        "exporterSha256": metadata_check.GetMetaDataByKey(
            namespace, "exporterSha256"
        ).GetValue(),
    }
    expected_metadata = {
        "sourceRevisionSha256": source_hash,
        "parameterManifestSha256": manifest_hash,
        "parentBriefSha256": brief_hash,
        "controllingAmendmentSha256": amendment_hash,
        "artifactRole": role,
        "exporterSha256": exporter_hash,
    }
    if embedded != expected_metadata:
        raise ValueError(f"{role}: embedded provenance metadata mismatch")
    return {
        "path": str(output.relative_to(ROOT)),
        "sha256": sha256(output.read_bytes()).hexdigest(),
        "sourceRevisionSha256": source_hash,
        "parameterManifestSha256": manifest_hash,
        "parentBriefSha256": brief_hash,
        "controllingAmendmentSha256": amendment_hash,
        "exporterSha256": exporter_hash,
        "objectCount": len(rows),
        "objectLabels": list(expected_labels),
        "objects": rows,
        "layout": layout,
        "principalBedContact": {
            "labels": [label for label in expected_labels if label in PRINCIPAL_LABELS],
            "minimumRequiredCoplanarZ0TriangleAreaMm2": PRINCIPAL_MINIMUM_BED_AREA_MM2,
            "zToleranceMm": BED_Z_TOLERANCE_MM,
            "writtenRoundTripValidated": all(
                "writtenRoundTripBedContact" in rows_by_label[label]
                for label in expected_labels
                if label in PRINCIPAL_LABELS
            ),
        },
        "embeddedMetadata": embedded,
        "lib3mfRoundTripValid": True,
        "allMeshesManifoldAndOriented": True,
    }


def main() -> int:
    source_children = list(p13.build_print_kit().children)
    by_label = {part.label: part for part in source_children}
    if set(by_label) != set((*PRODUCTION_LABELS, *COUPON_LABELS)):
        raise ValueError("P13 STEP print-kit source must contain exactly 12 parts plus 2 coupons")
    production = [by_label[label] for label in PRODUCTION_LABELS]
    coupons = [by_label[label] for label in COUPON_LABELS]
    payload = {
        "schema": "P13ThreeMFProvenance/v2",
        "production": _export_one(
            PRODUCTION_3MF,
            production,
            PRODUCTION_LABELS,
            "production-print-kit-12-objects-no-forming-rods-no-hardware-no-references",
        ),
        "coupons": _export_one(
            COUPON_3MF,
            coupons,
            COUPON_LABELS,
            "diagnostic-fit-coupons-2-objects",
        ),
        "stepPrintKitCensus": {
            "path": "cad/p13_four_plate_three_rod/p13_print_kit.step",
            "objectCount": 14,
            "meaning": "12 production printable parts plus 2 diagnostic coupons",
        },
        "excludedFromProduction3MF": [
            "three purchased uncut OD4x50 rods",
            "XT60 and completed workpiece",
            "ESC/electronics references",
            "soldering iron/tool envelopes",
            "all motion/removal proof envelopes",
        ],
        "geometryChangedForThreeMF": False,
        "printingInitiated": False,
    }
    PROVENANCE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
