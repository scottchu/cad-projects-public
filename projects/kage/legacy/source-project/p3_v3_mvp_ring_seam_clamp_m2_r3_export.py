"""Export KAGE r3 full-radial U-clamp review and print artifacts."""

from __future__ import annotations

from hashlib import sha256
from html import escape
import json
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import export_step

from p3_v3_mvp_ring_seam_clamp_m2_r3_geometry import (
    authority,
    make_hour_coupon,
    make_three_ring_stack,
    print_layout_rows,
)
from p3_v3_mvp_ring_seam_clamp_m2_r3_spec import (
    LOCKED_STEP,
    LOCKED_STEP_SHA256,
    MODEL_ROOT,
    NAMESPACE,
    ROOT,
    SPEC,
)


COUPON_STEP = MODEL_ROOT / "hour_q1_q2_full_radial_u_clamp_m2_coupon.step"
STACK_STEP = MODEL_ROOT / "three_ring_full_radial_u_clamp_m2_review.step"
PRINT_3MF = MODEL_ROOT / "hour_q1_q2_full_radial_u_clamp_m2_print_layout.3mf"
MANIFEST = MODEL_ROOT / "p3_v3_mvp_ring_seam_clamp_m2_r3_manifest.json"


def _sha(path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _aabb(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return tuple(round(float(value), 9) for value in (
        box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z,
    ))


def _mesh(shape):
    vertices, triangles = shape.tessellate(0.05, 0.15)
    return (
        [(float(v.X), float(v.Y), float(v.Z)) for v in vertices],
        [(int(a), int(b), int(c)) for a, b, c in triangles],
    )


def write_3mf(path=PRINT_3MF) -> None:
    resources, items = [], []
    for object_id, row in enumerate(print_layout_rows(), start=1):
        vertices, triangles = _mesh(row["shape"])
        vertex_xml = "".join(f'<vertex x="{x:.12g}" y="{y:.12g}" z="{z:.12g}"/>' for x, y, z in vertices)
        triangle_xml = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles)
        resources.append(
            f'<object id="{object_id}" type="model" name="{escape(row["shape"].label)}">'
            f'<mesh><vertices>{vertex_xml}</vertices><triangles>{triangle_xml}</triangles></mesh></object>'
        )
        items.append(f'<item objectid="{object_id}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        f'<metadata name="Title">{escape(NAMESPACE)}</metadata>'
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


def read_3mf_names(path=PRINT_3MF) -> list[str]:
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(path) as package:
        if package.testzip() is not None:
            raise RuntimeError("3MF CRC failure")
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    return [obj.attrib["name"] for obj in root.findall("m:resources/m:object", ns)]


def export_all() -> tuple:
    SPEC.validate()
    authority()
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    export_step(make_hour_coupon(), COUPON_STEP)
    export_step(make_three_ring_stack(include_hardware=True), STACK_STEP)
    write_3mf()
    payload = {
        "schema": "kage.p3-v3.mvp-ring-seam-clamp-m2-r3.v1",
        "namespace": NAMESPACE,
        "status": "REVIEW_PENDING_NOT_PRINT_READY",
        "scope": "isolated full-radial seam-clamp branch; locked baseline and r2 unchanged",
        "authority": {
            "locked_step_path": str(LOCKED_STEP.relative_to(ROOT)),
            "locked_step_sha256": LOCKED_STEP_SHA256,
        },
        "radial_coverage_mm": {
            "tooth_tip_radius": SPEC.tooth_tip_radius_mm,
            "tooth_root_radius": SPEC.tooth_root_radius_mm,
            "ring_outer_smooth_radius": SPEC.carrier_outer_radius_mm,
            "r2_covered_width": SPEC.r2_ring_body_coverage_mm,
            "r2_coverage_percent": 100.0 * SPEC.r2_ring_body_coverage_fraction,
            "r3_covered_width": SPEC.full_ring_body_coverage_mm,
            "r3_coverage_percent": 100.0 * SPEC.full_ring_body_coverage_fraction,
            "exposed_tooth_profile_width": SPEC.tooth_profile_exposed_radial_width_mm,
        },
        "stack_math_mm": {
            "ring_layer_pitch": SPEC.carrier_layer_pitch_mm,
            "clamp_total_height": SPEC.clamp_total_height_mm,
            "worst_case_adjacent_clamp_clearance": SPEC.worst_case_adjacent_clamp_clearance_mm,
        },
        "fastener": {
            "screw": "M2x4 90-degree flat head; nominal length includes head",
            "inner_radial_edge_distance_mm": SPEC.clamp_inner_radial_screw_edge_distance_mm,
            "outer_radial_edge_distance_mm": SPEC.clamp_outer_radial_screw_edge_distance_mm,
            "nut": "side-loaded AF4 M2 hex nut captured in 3 mm ring-end land",
        },
        "artifacts": {
            "coupon_step": {"path": str(COUPON_STEP.relative_to(ROOT)), "sha256": _sha(COUPON_STEP)},
            "stack_step": {"path": str(STACK_STEP.relative_to(ROOT)), "sha256": _sha(STACK_STEP)},
            "three_mf": {"path": str(PRINT_3MF.relative_to(ROOT)), "sha256": _sha(PRINT_3MF), "objects": read_3mf_names()},
        },
        "print_layout": [
            {"label": row["shape"].label, "translation_mm": row["translation_mm"], "aabb_mm": _aabb(row["shape"])}
            for row in print_layout_rows()
        ],
        "physical_validation_required": [
            "M2 flat-head and side-loaded nut fit",
            "printed lateral U-clamp slide fit",
            "loaded seam rigidity",
            "full three-ring rotation through pinion and roller stations",
        ],
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return COUPON_STEP, STACK_STEP, PRINT_3MF, MANIFEST


if __name__ == "__main__":
    for output in export_all():
        print(output.relative_to(ROOT))
