"""Export the isolated hour seam with one removable C-channel M2 clamp."""

from __future__ import annotations

from hashlib import sha256
from html import escape
import json
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from build123d import export_step, import_step

from p3_v3_mvp_ring_seam_clamp_m2_r1_geometry import (
    authority, capture_clearance_report, make_hour_coupon, print_layout_rows,
)
from p3_v3_mvp_ring_seam_clamp_m2_r1_spec import (
    LOCKED_STEP, LOCKED_STEP_SHA256, MODEL_ROOT, NAMESPACE, PARITY_JSON, ROOT, SPEC,
)


COUPON_STEP = MODEL_ROOT / "hour_q1_q2_c_channel_clamp_m2_coupon.step"
PRINT_3MF = MODEL_ROOT / "hour_q1_q2_c_channel_clamp_m2_print_layout.3mf"
MANIFEST = MODEL_ROOT / "p3_v3_mvp_ring_seam_clamp_m2_r1_manifest.json"


def _sha(path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _aabb(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return tuple(round(float(v), 9) for v in (
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
        vertex_xml = "".join(
            f'<vertex x="{x:.12g}" y="{y:.12g}" z="{z:.12g}"/>' for x, y, z in vertices
        )
        triangle_xml = "".join(
            f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in triangles
        )
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
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    export_step(make_hour_coupon(), COUPON_STEP)
    write_3mf()
    parity, _ = authority()
    source_records = []
    for index in SPEC.quadrant_occurrence_indices[0]:
        row = parity["occurrences"][index]
        source_records.append({
            "occurrence_index": index,
            "label": row["label"],
            "brep_sha256": row["brep_fingerprint"]["brep_sha256"],
        })
    layout = []
    for row in print_layout_rows():
        layout.append({
            "label": row["shape"].label,
            "translation_mm": row["translation_mm"],
            "print_aabb_mm": _aabb(row["shape"]),
        })
    step_children = tuple(import_step(COUPON_STEP).children)
    payload = {
        "schema": "kage.p3-v3.mvp-ring-seam-clamp-m2-r1.v1",
        "namespace": NAMESPACE,
        "status": "REVIEW_PENDING_NOT_PRINT_READY",
        "scope": "isolated production hour Q1/Q2 seam coupon; locked baseline and M3 r1 unchanged",
        "authority": {
            "locked_step_path": str(LOCKED_STEP.relative_to(ROOT)),
            "locked_step_sha256": LOCKED_STEP_SHA256,
            "parity_manifest_path": str(PARITY_JSON.relative_to(ROOT)),
            "parity_manifest_sha256": _sha(PARITY_JSON),
            "source_occurrences": source_records,
        },
        "phase_contract": {
            "ring_teeth": SPEC.ring_teeth,
            "quadrant_teeth": SPEC.quadrant_teeth,
            "locked_global_tooth_phase_deg": SPEC.locked_global_tooth_phase_deg,
            "seam_angle_deg": SPEC.seam_angle_deg,
            "pinion_geometry_in_coupon": False,
            "carrier_layers_mm": SPEC.carrier_layers,
            "carrier_race_radius_mm": SPEC.carrier_race_radius_mm,
            "display_fin_angles_deg": SPEC.display_fin_angles_deg,
        },
        "design": {
            "alignment_interlock": {
                "type": "full-thickness XY planar complementary jigsaw",
                "engagement_mm": SPEC.interlock_engagement_mm,
                "neck_width_mm": SPEC.interlock_neck_width_mm,
                "xy_clearance_per_side_mm": SPEC.interlock_xy_clearance_per_side_mm,
                "axial_allowance_mm": SPEC.interlock_axial_allowance_mm,
                "root_fillet_mm": SPEC.interlock_root_fillet_mm,
                "protected_inner_radius_mm": SPEC.protected_radius_mm,
            },
            "retention": {
                "type": "one removable three-sided C-channel clamp",
                "top_flange_thickness_mm": SPEC.clamp_top_flange_thickness_mm,
                "bottom_flange_thickness_mm": SPEC.clamp_bottom_flange_thickness_mm,
                "side_wall_inner_radius_mm": SPEC.clamp_side_wall_inner_radius_mm,
                "tangential_width_mm": SPEC.clamp_tangential_width_mm,
                "screws": "two M2x8 socket-cap screws, one through each ring half",
                "capture_method": SPEC.capture_method,
            },
            "screw_tangential_offsets_mm": SPEC.screw_tangential_offsets_mm,
            "capture_clearance": capture_clearance_report(),
        },
        "artifacts": {
            "step": {"path": str(COUPON_STEP.relative_to(ROOT)), "sha256": _sha(COUPON_STEP), "objects": [part.label for part in step_children]},
            "three_mf": {"path": str(PRINT_3MF.relative_to(ROOT)), "sha256": _sha(PRINT_3MF), "objects": read_3mf_names()},
        },
        "print_layout": layout,
        "physical_validation_required": [
            "independent reviewer acceptance", "printed interlock fit", "M2 screw and nut insertion",
            "loaded seam rigidity", "full three-ring rotation in frozen capture",
        ],
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return COUPON_STEP, PRINT_3MF, MANIFEST


if __name__ == "__main__":
    for output in export_all():
        print(output.relative_to(ROOT))
