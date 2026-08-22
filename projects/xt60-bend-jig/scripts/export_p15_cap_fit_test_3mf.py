"""Export the three P15 cap specimens as separate named 3MF objects."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import lib3mf

import xt60_bend_jig.p15_cap_fit_test as caps


ROOT = Path(__file__).parents[1]
OUT = ROOT / "cad" / "p15_cap_fit_test"
STEP = OUT / "p15_cap_fit_test.step"
GENERATOR = OUT / "p15_cap_fit_test.step.py"
THREEMF = OUT / "p15_cap_fit_test.3mf"
PROVENANCE = OUT / "p15_cap_fit_test.provenance.json"
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
        raise ValueError("cap mesh has an open or non-manifold edge")
    if any(
        directed[(first, second)] != 1 or directed[(second, first)] != 1
        for first, second in undirected
    ):
        raise ValueError("cap mesh has inconsistent triangle orientation")
    if min(vertex[2] for vertex in vertices) < -1.0e-6:
        raise ValueError("cap mesh is below the print bed")
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
    if not STEP.is_file() or STEP.stat().st_size == 0:
        raise ValueError("generate the primary STEP before exporting the 3MF")
    specimens = caps.build_caps()
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.SetUnit(lib3mf.ModelUnit.MilliMeter)
    namespace = "https://openai.com/codex/xt60-bend-jig/p15-cap-fit-test"
    metadata = model.GetMetaDataGroup()
    metadata.AddMetaData(
        namespace, "sourceRevisionSha256", caps.source_revision_sha256(), "xs:string", True
    )
    metadata.AddMetaData(
        namespace,
        "parameterManifestSha256",
        caps.parameter_manifest_sha256(),
        "xs:string",
        True,
    )

    object_records = []
    for specimen in specimens:
        if not specimen.is_valid or len(specimen.solids()) != 1 or float(specimen.volume) <= 0.0:
            raise ValueError("every cap specimen must be one valid positive solid")
        vertices, triangles = _welded_mesh(specimen)
        signed_volume = _signed_volume(vertices, triangles)
        if signed_volume <= 0.0:
            raise ValueError("cap mesh signed volume must be positive")
        mesh = model.AddMeshObject()
        mesh.SetName(specimen.label)
        mesh.SetGeometry(
            [lib3mf.Position(vertex) for vertex in vertices],
            [lib3mf.Triangle(triangle) for triangle in triangles],
        )
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError("lib3mf rejected a cap specimen")
        model.AddBuildItem(mesh, wrapper.GetIdentityTransform())
        object_records.append(
            {
                "name": specimen.label,
                "sourceBrepVolumeMm3": float(specimen.volume),
                "meshSignedVolumeMm3": signed_volume,
                "vertexCount": len(vertices),
                "triangleCount": len(triangles),
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    model.QueryWriter("3mf").WriteToFile(str(THREEMF))
    check = wrapper.CreateModel()
    check.QueryReader("3mf").ReadFromFile(str(THREEMF))
    names: list[str] = []
    meshes = check.GetMeshObjects()
    while meshes.MoveNext():
        mesh = meshes.GetCurrentMeshObject()
        names.append(mesh.GetName())
        if not mesh.IsValid() or not mesh.IsManifoldAndOriented():
            raise ValueError("round-trip 3MF cap mesh is invalid")
    if names != [specimen.label for specimen in specimens]:
        raise ValueError("3MF cap object names or order changed")
    if check.GetBuildItems().Count() != 3:
        raise ValueError("3MF must contain exactly three cap build items")

    shape = caps.build_cap_fit_test()
    box = shape.bounding_box()
    payload = {
        "schema": "P15CapFitTestProvenance/v1",
        "step": "cad/p15_cap_fit_test/p15_cap_fit_test.step",
        "threeMf": "cad/p15_cap_fit_test/p15_cap_fit_test.3mf",
        "stepSha256": sha256(STEP.read_bytes()).hexdigest(),
        "threeMfSha256": sha256(THREEMF.read_bytes()).hexdigest(),
        "generatorSha256": sha256(GENERATOR.read_bytes()).hexdigest(),
        "sourceRevisionSha256": caps.source_revision_sha256(),
        "parameterManifestSha256": caps.parameter_manifest_sha256(),
        "objectCount": 3,
        "unit": "millimeter",
        "boundsMm": [box.size.X, box.size.Y, box.size.Z],
        "minimumZMm": box.min.Z,
        "lib3mfRoundTripValid": True,
        "meshManifoldAndOriented": True,
        "objects": object_records,
        "parameterManifest": caps.parameter_manifest(),
    }
    PROVENANCE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
