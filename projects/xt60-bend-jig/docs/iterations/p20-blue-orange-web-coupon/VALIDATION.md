# P20 Blue-Orange web coupon independent validation

Date: `2026-08-27`

Task: `P20-WEB-VALIDATE-01`

Status: **PASS FOR FORMAL DIGITAL REVIEW on exact candidate fingerprint
`07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be`; two
non-geometric minor findings require formal disposition.**

This verdict is limited to the test-only coupon's math, CAD, STEP, print mesh,
and saved review media. It does not approve slicing, printer upload/start,
physical survival, the simulator profile, any P20 assembly, or a product web
below the normal `2.20 mm` rule.

## Frozen inputs and fingerprint

All six decision-bearing input hashes in `BRIEF.md` independently rechecked
without drift: the immutable simulator, P20 R3 brief, requirements, experience,
P20 R2 source, and P19 R1 source. `BRIEF.md` and `DESIGN.md` rechecked as
`388c27a...2081` and `c8920c6...34f9` respectively.

The candidate fingerprint was independently reconstructed as SHA-256 of the
canonical sorted compact JSON object containing the eight declared fields
`briefSha256`, `designSha256`, `sourceSha256`, `generatorSha256`,
`printGeneratorSha256`, `stepSha256`, `threeMfSha256`, and `stlSha256`. It is
exactly:

```text
07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be
```

Every field matched the current file bytes and the provenance JSON. The
canonical parameter-manifest SHA-256 independently reproduced as
`e669a3a745505458ff9afe01fa3889e9913f28663345e15ce0a4f09f7ffedcad`.
The separately declared focused-test, provenance-generator, provenance-JSON,
and three snapshot hashes also matched:

| Evidence | SHA-256 |
|---|---|
| focused test | `38f4deb59e40c0a056bde45ea650fb058dc79db9f491180c5abe8758eb3e4147` |
| provenance generator | `3f19531dda721df7d1e52e223195afd1d17d657275e41d57b8e4cc059330da81` |
| provenance JSON | `db8fe0be3b2513846be1d268fe8a547cb922d99a6811a0e686fcc7c3ef9f5be7` |
| front snapshot | `76e7e649f8bc4140b2b44f7ff41d0b72b1bc92bf76e861bc7770c3b2b887d36d` |
| oblique snapshot | `874ad187ef563d9e6ca8600e7cb85a4ea761f25ab998dbbed1fa51ff16096430` |
| opposed snapshot | `44df6aad14e5228c5880d247770701ff706fb4a15f534bae1ec428053f4ca7e3` |

## Independent math and constraint checks

An independent equation implementation, not calling the production
`trajectory_point()`, recomputed all `361` points per rail from the frozen
angles, radius, endpoints, offset, and `-45u deg` transform. Its maximum delta
from every production point was `0.0 mm`.

- Blue START/END: `(-7.511545004574255, 14.127161485742830)` to
  `(5.286598713468044, 2.135621075408544) mm`.
- Orange START/END: `(11.313708498984761, 11.313708498984760)` to
  `(5.640152104061318, -6.349660298830027) mm`.
- Named Blue `360` / Orange `209` witness: center distance
  `5.865073308569088 mm`; boundary gap `1.715073308569088 mm`, which rounds to
  `1.72 mm`.
- Exhaustive `360 x 360` segment-pair search: the true sampled-polyline minimum
  is Blue endpoint `360` to Orange segment `209..210` at segment fraction
  `0.3529123105635372`; center distance `5.865042423717555 mm` and boundary
  gap `1.715042423717555 mm`.
- The independent polyline result agrees with the BREP cutter distance
  `1.715042423717553 mm`; cutter intersection volume is `0.0 mm3`.
- Minimum ordinary cutter-to-coupon boundary web is
  `2.199999999999992 mm` (floating-point representation of the frozen
  `2.20 mm`). All other exterior webs are greater. Only the named internal
  Blue-Orange ligament is below the ordinary rule.

The source includes only Blue and Orange rail specifications and fails closed
for Green. The immutable simulator and both referenced product-source hashes
were unchanged. The repository already contains unrelated dirty P20 R3 and
continuity paths, so this validation does not claim the whole worktree is
clean; no candidate dependency on those unrelated paths was found.

## Actual-solid and STEP checks

- Source BREP: one valid positive-volume solid,
  `2009.7053159375214 mm3`.
- Written STEP: one valid solid in one closed shell,
  `2009.7053159379707 mm3`; source-to-STEP volume delta is
  `4.49e-10 mm3`.
- Exact STEP bounds are `X=[-1.6,1.6]`,
  `Y=[-11.78654500457,16.308446371474]`, and
  `Z=[-10.62466029883,18.402161485743] mm`, giving thickness `3.20 mm`.
- Each of the two broad `X=+-1.6 mm` faces has one outer wire and exactly two
  inner wires. Together with the positive `1.715042 mm` cutter separation,
  zero cutter intersection, and both cutter overruns, this verifies two
  distinct complete through-slots rather than one fused opening.
- CAD `inspect validate` reports `ok=true`, one occurrence, zero failures.
- CAD source-generator versus written-STEP `inspect diff` reports no topology,
  geometry, bounds, size, center, plane, or count change.

## 3MF/STL parity and print orientation

The print transform is rigid only. Both meshes place the broad coupon face at
build `Z=0` with thickness along `+Z` and bounds approximately
`29.026821 x 28.094992 x 3.200000 mm`.

- 3MF: millimeter unit, one named mesh, one identity-transformed build item,
  `8876` vertices and `17756` triangles; lib3mf reports valid, manifold, and
  oriented. Independent mesh inspection reports one watertight,
  winding-consistent body and volume `2009.7084542923421 mm3`.
- STL: after normal STL vertex merging, one watertight,
  winding-consistent body, `8876` vertices and `17756` triangles, volume
  `2009.7085485866664 mm3`. Its unmerged raw triangle soup duplicates vertices
  per facet, which is normal STL serialization and not a topology failure.
- 3MF-to-STL maximum bounds delta is `9.54e-7 mm`; volume delta is
  `9.43e-5 mm3`. Mesh-to-source volume error is about `0.0032 mm3`
  (`~1.6e-6` relative), consistent with the frozen tessellation.
- Every mesh triangle is either horizontal or vertical with respect to build
  Z; there are zero sloped/unsupported transition faces. The part is the
  constant `3.20 mm` extrusion of a planar profile and is geometrically
  support-free in the declared orientation. This is not a slicer or process
  acceptance claim.

## Snapshot review

All three saved `1600 x 1200` PNGs were inspected at original resolution:

- FRONT/opposed broad-face views visibly show two separate complete openings
  and continuous material between them.
- The oblique view visibly shows both slots passing through the full coupon
  thickness and no extra hole, engraving, Green rail, or fixed-axle feature.
- The files contain the requested distinct camera directions even though the
  renderer labels both broad-face images `ISO`.

Visual review found no shape defect. Deterministic topology and distance
checks above support the visible conclusion; the images alone are not used as
proof.

## Findings

### `MINOR` — candidate digest does not bind every separately listed evidence file

The exact digest is reproducible and binds the physical 3MF/STL plus their
authoritative source and generators. It does not itself include the focused
test, provenance generator, provenance JSON, or snapshots, although their
hashes are listed in `IMPLEMENTATION.md` and rechecked above. This does not
change the exact printable bytes or digital geometry verdict, but formal review
should bind these separate hashes in its joined receipt; a future candidate
manifest should include every decision-bearing path in one manifest.

### `MINOR` — minimum-web witness is not visibly marked in the snapshots

The design visual gate asks for a marked witness, while the snapshots show the
ligament without an overlay marker. The location is unambiguously recorded in
provenance as `YZ=(7.963860139702033,0.9389413002297666)` and is independently
verified above. No engraving should be added. Formal review may accept an
annotation-only review image or explicitly disposition this as non-blocking to
the exact print artifact.

## Commands and results

```text
shasum -a 256 <six frozen inputs and all declared candidate/evidence files>
  -> every hash matched

uv run pytest -q projects/xt60-bend-jig/tests/test_p20_blue_orange_web_coupon.py
  -> 6 passed

uv run python <cad-skill>/scripts/inspect refs \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step \
  --facts --planes --positioning
  -> bounds 3.2 x 28.094991 x 29.026821 mm; one leaf shape

uv run python <cad-skill>/scripts/inspect validate \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step
  -> ok=true; occurrenceCount=1; failureCount=0

uv run python <cad-skill>/scripts/inspect diff \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step.py \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step --planes
  -> topologyChanged=false; geometryChanged=false; bboxChanged=false; all deltas zero

uv run python - <<'PY'
  # independent frozen-equation/segment-distance, STEP inner-wire and volume,
  # lib3mf round-trip, trimesh manifold/parity, and orientation checks
PY
  -> results recorded in the sections above
```

## Verdict and remaining physical gate

**ACCEPT the exact digital coupon for `P20-WEB-REVIEW-01`.** The two minor
findings are provenance/review-media issues, not geometry blockers, and require
formal disposition before release. Formal acceptance, slicing, printer
readiness, PETG extrusion, bed removal, finger handling, crack/fusion outcome,
strength, heat, wear, fit, motion, and all product acceptance remain open.
