# P20 Blue-Orange web coupon implementation receipt

Date: `2026-08-27`

Task: `P20-WEB-IMPLEMENT-01`

Status: **IMPLEMENTED; DIGITAL EVIDENCE COMPLETE; INDEPENDENT CRITIQUE,
VALIDATION, FORMAL REVIEW, SLICING, AND PHYSICAL TEST PENDING**

This is a test-only non-product coupon. It does not approve the simulator
profile, the P20 assembly, any product web below `2.20 mm`, or physical
survival.

## Verified frozen input

- Baseline HEAD: `9698cf30e9ddb3e576c08179bfdd067446514c67`.
- `BRIEF.md` SHA-256:
  `388c27a9af1c8c6dffe0a809f057428e986d246d099b55617a74de8752ac2081`.
- `DESIGN.md` SHA-256:
  `c8920c6014bfbdfe3904ae09975b7446fbc92d2e115a051556279c0d992034f9`.
- Both hashes were rechecked before source edits and did not drift.

## Implementation

- The pure function `trajectory_point()` is the sole geometry authority for
  both rails. `sampled_trajectory()` evaluates exactly `i=0..360` at
  `u=i/360`.
- Each cutter starts from one open wire containing exactly `360` straight
  edges. A `2.075 mm` round 2D offset supplies the straight-segment swept
  capsule and round joins/endpoints; no spline, resampling, or curve fitting
  is used. The planar cutter is extruded `5.20 mm` through the `3.20 mm`
  coupon.
- The primary STEP remains in source FRONT-YZ coordinates with X thickness.
  The secondary print generator applies only the frozen rigid
  `(0,-90,0) deg` rotation and `+1.60 mm` build-Z translation.
- The ordinary CAD mesh exporter initially emitted a visually correct but
  lib3mf-invalid 3MF because OCC face-boundary vertices were duplicated. The
  final 3MF is regenerated from the same print-oriented BREP with deterministic
  `1e-6 mm` vertex welding and is round-trip valid, manifold, and consistently
  oriented. No source geometry changed to repair the mesh topology.

## Focused evidence

The focused suite collected `6` tests and passed all `6`:

```text
uv run pytest -q projects/xt60-bend-jig/tests/test_p20_blue_orange_web_coupon.py
......  [100%]
```

Risk-driven results:

- Math: both trajectories contain exactly `361` deterministic points;
  endpoints and sampled extrema match the frozen contract within `1e-12 mm`.
- Named discrete witness: Blue index `360`, Orange index `209`, center
  distance `5.8650733085690888 mm`, boundary gap
  `1.7150733085690888 mm`, displayed as `1.72 mm`.
- Actual cutter BREP distance: `1.715042423717553 mm`; cutter intersection
  volume `0.0 mm3`.
- Coupon: one valid positive-volume solid, volume
  `2009.7053159375214 mm3`, exact source bounds
  `X=[-1.6,1.6]`, `Y=[-11.786545004574247,16.308446371474318]`,
  `Z=[-10.624660298830026,18.402161485742834]`.
- Both disjoint cutters overrun both X faces, proving two distinct through
  slots; the minimum blank-boundary web is `2.20 mm`.
- STEP inspection: one valid closed positive-volume occurrence; bounds
  `3.20 x 28.094991 x 29.026821 mm`.
- Print STL: one watertight, winding-consistent volume/body; build bounds
  approximately `29.026821 x 28.094992 x 3.200000 mm`, with minimum build Z
  numerically zero.
- Print 3MF: millimeter unit, one build item, one named mesh, `8876` vertices,
  `17756` triangles; `IsValid=true` and
  `IsManifoldAndOriented=true` after write/read round trip.
- Provenance asserts both physical and product acceptance as `false`.

Exact validation/generation commands:

```text
uv run python .../cad/skills/cad/scripts/gen \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step.py \
  --write --force --json
uv run python .../cad/skills/cad/scripts/inspect refs \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step \
  --facts --planes --positioning
uv run python .../cad/skills/cad/scripts/inspect validate \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step
uv run python .../cad/skills/cad/scripts/export \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon_print.step.py \
  --stl p20_blue_orange_web_coupon.stl \
  --mesh-tolerance 0.01 --mesh-angular-tolerance 0.03 --json
uv run python -c "from xt60_bend_jig.p20_blue_orange_web_coupon import export_print_coupon_3mf; export_print_coupon_3mf('projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.3mf')"
uv run python projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/generate_provenance.py
uv run python .../cad/skills/cad/scripts/snapshot \
  --job projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/snapshot_job.json --json
```

## Snapshot review and Viewer handoff

All three `1600 x 1200` snapshots were generated and inspected:

- `snapshots/front_20260827T194252Z.png`
- `snapshots/oblique_20260827T194252Z.png`
- `snapshots/bottom_20260827T194252Z.png`

The opposed broad-face views show two separate complete openings and a visibly
continuous ligament. The oblique view shows both openings pass through the
full thickness. No fusion, missing slot, or unintended geometry is visible.
The frozen witness is identified non-geometrically in provenance at
`YZ=(7.963860139702033,0.9389413002297666)`; it is not engraved or added as a
third solid. The snapshot renderer labels the custom views `ISO` even though
the saved images do contain the requested distinct front/oblique/opposed
camera directions.

The already-running CAD Viewer returned HTTP `200` for the exact generator:

`http://127.0.0.1:3245/Users/scottchu/Projects/personal/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp20_blue_orange_web_coupon%2Fp20_blue_orange_web_coupon.step.py`

## Candidate fingerprint and artifacts

Candidate fingerprint SHA-256:
`07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be`.

| File | SHA-256 |
|---|---|
| source | `07755b38ec2b008a19ba556cd18d5cd84e3ebb47b62c995571783480bab5c917` |
| focused test | `38f4deb59e40c0a056bde45ea650fb058dc79db9f491180c5abe8758eb3e4147` |
| STEP generator | `b803696277c1edf831002a5b3809e68ee22cf612a853437e6b9d9fc2f852856d` |
| print generator | `f51ae3105300bd80d1f16736c104525282c9b8d0a87c4518afe90c04ddf4a3c7` |
| provenance generator | `3f19531dda721df7d1e52e223195afd1d17d657275e41d57b8e4cc059330da81` |
| STEP | `14716d85365645ead4774ea03cc5d93fb330b807f902d067ee8c09f2abbef085` |
| 3MF | `07810673e418315fb6c782a1799f65fe15d9f5390db9390a6f8420c139245ce2` |
| STL | `6181d4ae4c9e5a396c1cc425826464cb00074fbb618be9d67630ee12d92529b0` |
| provenance JSON | `db8fe0be3b2513846be1d268fe8a547cb922d99a6811a0e686fcc7c3ef9f5be7` |

## Requirement coverage and unresolved risks

- Implemented: exact Blue/Orange identities and paths, exact `4.15 mm`
  cutters, `3.20 mm` blank, `1.72 mm` witness, two through-slots, ordinary
  boundary webs, one source STEP, one source-oriented manifold print mesh,
  provenance, focused tests, and three snapshots.
- Excluded as required: Green, fixed axle, all other rails, product plates,
  assembly, motion, wire, labels/engraving, and simulator changes.
- Not yet established: independent critique/validation/formal acceptance,
  slicer settings or G-code, printer/bed readiness, real extrusion behavior,
  bed removal survival, handling survival, strength, heat, wear, fit, motion,
  or product acceptance.

Next action: independent critic and validator must verify this exact candidate
fingerprint before any slicer or printer handoff.
