# P20 R4 blocked test-print 3MF formal review

Date: `2026-08-27`

Task: `P20R4-3MF-REVIEW-01`

Owner/role: `/root/p20_3mf_reviewer`, independent formal reviewer. This role
did not edit source, tests, STEP, 3MF, provenance, snapshots, or continuity
records.

## Candidate identity

- Reviewed implementation-candidate fingerprint:
  `e11c3f94b1d4081a4e58db0ec74c76651f234ce97f2e8faa06f59600dc2be871`.
- Child candidate manifest: all `14/14` rows pass SHA-256 verification.
- Parent full-CAD candidate fingerprint:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`;
  all `30/30` parent rows pass SHA-256 verification.
- Frozen parent CAD source is restored byte-for-byte at
  `38ed907ea1ec0e22ff8c42c2c03e047049b65ea9962b2fe7e58ea914aecac93e`.
- Isolated child print-kit source is pinned at
  `b850d90c26b7326a885c028978f029d414814050cf9fc1b08d25c6c9c85f04cf`.
- Reviewed STEP SHA-256:
  `fb1188097e74752522e90dac96996b98c3d1379d42432d09607e62eea47b39e3`.
- Reviewed 3MF SHA-256:
  `cd90dc1afa0c0658981b75a040daa2a8cc91d9addf362ae3bd09420ea4b05135`.
- Reviewed provenance SHA-256:
  `2f21bcbe1bb614555e62a99c67764580f8f1f3c2e13ab9dca7e5f1129f781327`.

The repaired child candidate is internally clean: every file pinned by its
manifest matches, the parent manifest is independently restored and clean,
and the print-kit composition is isolated behind a runtime parent-source hash
guard. The expected work remains uncommitted in the worktree; Git cleanliness
is not used as artifact evidence.

## Independent evidence synthesis

The implementation receipt, independent critique, and independent validation
all address the exact fingerprint above and agree on the following facts:

- source composition, written STEP, and lib3mf round-trip each contain exactly
  `13` distinct named printable plastic objects in the frozen order;
- the census is four plates, one stepped axle, two keepers, and six unchanged
  `H9.05 mm` caps;
- purchased rods, XT60, wire/workpiece, motion/reference objects, tools, and
  coupon geometry are excluded;
- every mesh is non-empty, positive-volume, valid, manifold, and oriented;
- all build-item transforms are identity, unit is millimetres, all objects
  contact `Z=0`, pairwise XY bounding-box overlap count is zero, and the
  footprint is approximately `228.5 x 145.8 mm`;
- the archive contains only the standard 3MF model, content-types, and
  relationship entries, with no slicer profile, G-code, supports, material or
  printer-control payload;
- embedded and external provenance preserve
  `manufacturingAccepted=false`, `printingInitiated=false`, `sliced=false`,
  and `uploaded=false`.

I independently recomputed both manifest fingerprints and verified all rows,
listed the 3MF archive entries, inspected the exact repaired STEP and 3MF TOP
snapshots at original resolution, and counted the same thirteen separated
objects. The source-colored STEP view and white 3MF view both show four
plates, one axle, two keepers, and six caps without a hidden or visibly
overlapping object. These snapshots support presence and separation only.

The exact 3MF also resolves through CAD Viewer at the repository-root URL.
Both the local Viewer and the tailnet-only Tailscale `:8446` delivery surface
returned HTTP `200`, so a Tailscale Viewer handoff is allowed for this exact
artifact. This is delivery-surface evidence, not manufacturing evidence.

## Formal disposition

| Gate | Decision | Reason |
|---|---|---|
| User handoff as exact model-only blocked test artifact | **PASS** | Candidate identity, 13-object census, source/STEP/3MF parity, provenance, snapshots, and Viewer surface are coherent. |
| STEP and 3MF artifact integrity | **PASS** | Manifests, written STEP checks, lib3mf round-trip, positive volumes, manifold/oriented meshes, object separation, and archive boundary pass. |
| Slicing | **REJECT / NOT AUTHORIZED** | No printer, material, process, support, or plate-fit decision has been made; parent geometry blockers remain. |
| Upload | **REJECT / NOT AUTHORIZED** | The user authorized 3MF preparation only, not printer handoff. |
| Print start | **REJECT / NOT AUTHORIZED** | No sliced G-code or printer preflight exists, and parent failures remain unresolved. |
| Manufacturing or physical acceptance | **REJECT** | Mesh validity does not waive assembled collisions, thin webs, unresolved contacts, or unverified cap/plate-gap behavior. |

The exact model-only 3MF may therefore be shown and delivered to the user,
but it must not be described as print-ready. No downstream slicer or printer
action may start from this review.

## Blockers that must remain adjacent to the handoff

- Blue rod / XT60 intersections: `186.980487 mm3` at OPEN and
  `63.593308 mm3` at MID;
- fixed-axle hex / inner-rim web: `1.152 mm`;
- left outer Blue-Orange rail web: `1.715 mm`;
- unresolved rod/workpiece functional contacts;
- no physical acceptance for the unchanged `9.05 mm` caps and `18.40 mm`
  inner clear span.

The required adjacent handoff wording is:

> P20 R4 model-only 3MF prepared as a blocked test artifact. It contains 13
> printable plastic objects and no rods, XT60, or wire. Mesh/STEP validation
> does not waive the XT60 collision or thin-web failures. It has not been
> sliced, uploaded, or printed.

## Next action

The root orchestrator may update continuity and hand off the exact 3MF, its
two repaired snapshots, and the tailnet-only Viewer link with the warning
above. Stop after artifact delivery. Any slicing, upload, or print request
requires a separate workflow and cannot treat this review as manufacturing
acceptance.
