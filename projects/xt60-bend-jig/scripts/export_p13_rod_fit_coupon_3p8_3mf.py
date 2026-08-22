"""Export the standalone measured-rod coupon as one valid model-only 3MF."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import lib3mf

import xt60_bend_jig.p13_rod_fit_coupon_3p8 as coupon


ROOT = Path(__file__).parents[1]
OUT = ROOT / "cad" / "p13_rod_fit_coupon_3p8"
THREEMF = OUT / "p13_rod_fit_coupon_3p8.3mf"
PROVENANCE = OUT / "p13_rod_fit_coupon_3p8.provenance.json"
LINEAR_TOLERANCE_MM = 0.02
ANGULAR_TOLERANCE_RAD = 0.05
WELD_TOLERANCE_MM = 1.0e-6


def _welded_mesh(shape):
    raw_vertices, raw_triangles = shape.tessellate(
        LINEAR_TOLERANCE_MM, ANGULAR_TOLERANCE_RAD
    )
    vertex_by_key: dict[tuple[int, int, int], int] = {}
    vertices: list[tuple[float, float, float]] = []
    remap: list[int] = []
    for vertex in raw_vertices:
        point = (float(vertex.X), float(vertex.Y), float(vertex.Z))
        key = tuple(int(round(value / WELD_TOLERANCE_MM)) for value in point)
        if key not in vertex_by_key:
            vertex_by_key[key] = len(vertices)
            vertices.append(point)
        remap.append(vertex_by_key[key])

    triangles = []
    for first, second, third in raw_triangles:
        triangle = (remap[first], remap[second], remap[third])
        if len(set(triangle)) == 3:
            triangles.append(triangle)

    undirected: Counter[tuple[int, int]] = Counter()
    directed: Counter[tuple[int, int]] = Counter()
    for first, second, third in triangles:
        for start, end in ((first, second), (second, third), (third, first)):
            undirected[tuple(sorted((start, end)))] += 1
            directed[(start, end)] += 1
    if any(count != 2 for count in undirected.values()):
        raise ValueError("coupon mesh has an open or non-manifold edge")
    if any(
        directed[(first, second)] != 1 or directed[(second, first)] != 1
        for first, second in undirected
    ):
        raise ValueError("coupon mesh has inconsistent triangle orientation")
    if min(vertex[2] for vertex in vertices) < -1.0e-6:
        raise ValueError("coupon mesh is below the print bed")
    return vertices, triangles


def _signed_volume(vertices, triangles) -> float:
    result = 0.0
    for first, second, third in triangles:
        ax, ay, az = vertices[first]
        bx, by, bz = vertices[second]
        cx, cy, cz = vertices[third]
        result += (
            ax * (by * cz - bz * cy)
            + ay * (bz * cx - bx * cz)
            + az * (bx * cy - by * cx)
        ) / 6.0
    return result


def main() -> int:
    shape = coupon.build_coupon()
    if not shape.is_valid or len(shape.solids()) != 1 or float(shape.volume) <= 0.0:
        raise ValueError("source coupon must be one valid positive-volume solid")
    vertices, triangles = _welded_mesh(shape)
    signed_volume = _signed_volume(vertices, triangles)
    if signed_volume <= 0.0:
        raise ValueError("coupon mesh signed volume must be positive")

    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.SetUnit(lib3mf.ModelUnit.MilliMeter)
    namespace = "https://openai.com/codex/xt60-bend-jig/p13-rod-fit-coupon-3p8"
    metadata = model.GetMetaDataGroup()
    embedded = {
        "sourceRevisionSha256": coupon.source_revision_sha256(),
        "parameterManifestSha256": coupon.parameter_manifest_sha256(),
        "artifactRole": "standalone-measured-3p80-rod-fit-coupon-exactly-7-holes",
    }
    for key, value in embedded.items():
        metadata.AddMetaData(namespace, key, value, "xs:string", True)

    mesh = model.AddMeshObject()
    mesh.SetName(coupon.PART_LABEL)
    mesh.SetGeometry(
        [lib3mf.Position(vertex) for vertex in vertices],
        [lib3mf.Triangle(triangle) for triangle in triangles],
    )
    if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
        raise ValueError("lib3mf rejected the source-derived coupon mesh")
    model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
    OUT.mkdir(parents=True, exist_ok=True)
    model.QueryWriter("3mf").WriteToFile(str(THREEMF))

    check = wrapper.CreateModel()
    check.QueryReader("3mf").ReadFromFile(str(THREEMF))
    meshes = check.GetMeshObjects()
    names: list[str] = []
    while meshes.MoveNext():
        item = meshes.GetCurrentMeshObject()
        names.append(item.GetName())
        if not item.IsValid() or not item.IsManifoldAndOriented():
            raise ValueError("round-trip 3MF coupon mesh is invalid")
    if names != [coupon.PART_LABEL] or check.GetBuildItems().Count() != 1:
        raise ValueError("3MF must contain exactly one named coupon object")
    if check.GetUnit() != lib3mf.ModelUnit.MilliMeter:
        raise ValueError("3MF unit must be millimetres")

    box = shape.bounding_box()
    payload = {
        "schema": "P13RodFitCoupon3p8Provenance/v2",
        "step": "cad/p13_rod_fit_coupon_3p8/p13_rod_fit_coupon_3p8.step",
        "threeMf": "cad/p13_rod_fit_coupon_3p8/p13_rod_fit_coupon_3p8.3mf",
        "threeMfSha256": sha256(THREEMF.read_bytes()).hexdigest(),
        "sourceRevisionSha256": embedded["sourceRevisionSha256"],
        "parameterManifestSha256": embedded["parameterManifestSha256"],
        "objectCount": 1,
        "objectLabel": coupon.PART_LABEL,
        "unit": "millimeter",
        "boundsMm": [box.size.X, box.size.Y, box.size.Z],
        "minimumZMm": box.min.Z,
        "sourceBrepVolumeMm3": float(shape.volume),
        "meshSignedVolumeMm3": signed_volume,
        "vertexCount": len(vertices),
        "triangleCount": len(triangles),
        "lib3mfRoundTripValid": True,
        "meshManifoldAndOriented": True,
        "parameterManifest": coupon.parameter_manifest(),
    }
    PROVENANCE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
