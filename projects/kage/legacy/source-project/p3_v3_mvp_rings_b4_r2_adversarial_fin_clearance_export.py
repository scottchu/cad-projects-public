"""Byte-identical B4-R1 artifact handoff for evidence-only B4-R2."""

from hashlib import sha256

import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_export as accepted
from p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance_spec import MODEL_ROOT, NAMESPACE


ASSEMBLED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembled.step"
EXPLODED_STEP = MODEL_ROOT / f"{NAMESPACE}_assembly_order_exploded.step"
MODEL_ONLY_3MF = MODEL_ROOT / f"{NAMESPACE}_nine_ring_segments_unchanged_model_only.3mf"
README = MODEL_ROOT / "README.md"

ARTIFACT_PAIRS = (
    (accepted.ASSEMBLED_STEP, ASSEMBLED_STEP),
    (accepted.EXPLODED_STEP, EXPLODED_STEP),
    (accepted.MODEL_ONLY_3MF, MODEL_ONLY_3MF),
)


def export_all():
    """Copy accepted artifacts byte-for-byte; never regenerate geometry."""
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    for source, target in ARTIFACT_PAIRS:
        target.write_bytes(source.read_bytes())
    README.write_text(
        "# B4-R2 adversarial fin-clearance evidence\n\n"
        "Evidence-only correction over accepted B4-R1. STEP and 3MF artifacts "
        "are byte-identical copies; no geometry and no B5 were added.\n"
    )
    return ASSEMBLED_STEP, EXPLODED_STEP, MODEL_ONLY_3MF, README


def artifact_identity_evidence():
    rows = []
    for source, target in ARTIFACT_PAIRS:
        source_bytes = source.read_bytes()
        target_bytes = target.read_bytes()
        rows.append(
            {
                "accepted_path": str(source),
                "b4_r2_path": str(target),
                "accepted_sha256": sha256(source_bytes).hexdigest(),
                "b4_r2_sha256": sha256(target_bytes).hexdigest(),
                "byte_count": len(target_bytes),
                "byte_identical": source_bytes == target_bytes,
            }
        )
    return {"rows": tuple(rows), "all_byte_identical": all(row["byte_identical"] for row in rows)}


if __name__ == "__main__":
    print(export_all())
