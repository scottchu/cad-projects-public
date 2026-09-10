"""Write reproducible provenance for the P20 test-only web coupon exports."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from build123d import import_stl

import xt60_bend_jig.p20_blue_orange_web_coupon as coupon


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = PROJECT / "src/xt60_bend_jig/p20_blue_orange_web_coupon.py"
    generator = HERE / "p20_blue_orange_web_coupon.step.py"
    print_generator = HERE / "p20_blue_orange_web_coupon_print.step.py"
    step = HERE / "p20_blue_orange_web_coupon.step"
    three_mf = HERE / "p20_blue_orange_web_coupon.3mf"
    stl = HERE / "p20_blue_orange_web_coupon.stl"
    print_mesh = import_stl(stl)
    print_bounds = print_mesh.bounding_box()

    fingerprints = {
        "briefSha256": coupon.BRIEF_SHA256,
        "designSha256": coupon.DESIGN_SHA256,
        "sourceSha256": _sha(source),
        "generatorSha256": _sha(generator),
        "printGeneratorSha256": _sha(print_generator),
        "stepSha256": _sha(step),
        "threeMfSha256": _sha(three_mf),
        "stlSha256": _sha(stl),
    }
    candidate_fingerprint = sha256(
        json.dumps(fingerprints, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    record = {
        "schema": "P20BlueOrangeWebCouponProvenance/v1",
        "candidateStatus": "test_only_non_product_coupon",
        "baselineHead": coupon.BASELINE_HEAD,
        **fingerprints,
        "candidateFingerprintSha256": candidate_fingerprint,
        "parameterManifestSha256": coupon.parameter_manifest_sha256(),
        "parameterManifest": coupon.parameter_manifest(),
        "actualSolidEvidence": coupon.actual_solid_evidence(),
        "printMeshBounds": {
            "min": [print_bounds.min.X, print_bounds.min.Y, print_bounds.min.Z],
            "max": [print_bounds.max.X, print_bounds.max.Y, print_bounds.max.Z],
            "size": [print_bounds.size.X, print_bounds.size.Y, print_bounds.size.Z],
        },
        "meshExport": {
            "linearDeflectionMm": 0.01,
            "angularDeflection": 0.03,
            "orientation": "rigid source transform; broad face at build Z=0",
        },
        "physicalAcceptanceClaimed": False,
        "productAcceptanceClaimed": False,
    }
    (HERE / "p20_blue_orange_web_coupon.provenance.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
