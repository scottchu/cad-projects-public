# P20 Blue-Orange web coupon formal independent review

Date: `2026-08-27`

Task: `P20-WEB-REVIEW-01`

Status: **ACCEPT EXACT DIGITAL COUPON FOR SLICING ONLY; G-CODE, PRINTER,
PHYSICAL, AND PRODUCT ACCEPTANCE REMAIN OPEN**

The joined critic and validator evidence supports advancing the exact frozen
coupon to slicer preparation. This is not permission to upload or start a
print. Printer start is blocked until the exact generated G-code passes the
first/middle/top-layer witness inspection below and an external witness locator
exists. This disposition does not accept the complete simulator profile, any
P20 mechanism or plate, or a product web below the ordinary `2.20 mm` rule.

## Frozen review inputs

- Candidate fingerprint:
  `07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be`.
- `BRIEF.md`:
  `388c27a9af1c8c6dffe0a809f057428e986d246d099b55617a74de8752ac2081`.
- `DESIGN.md`:
  `c8920c6014bfbdfe3904ae09975b7446fbc92d2e115a051556279c0d992034f9`.
- `IMPLEMENTATION.md`:
  `cd97de7edeb1d4d5f12c01f5a562c934d2a180e4d4a022c815ffcf4623d56307`.
- `CRITIQUE.md`:
  `0a50c5036585c5d61fb61cb353a20ef610ee254fa9e6e281865f72cbc1eeee6e`.
- `VALIDATION.md`:
  `2becf1c712cc7e40b16cb47fd681ae8a2dc8ec346ffa1dc36add62e2a9fadd46`.

All six decision-bearing input hashes in `BRIEF.md` were recomputed and
matched. The eight-field canonical fingerprint was independently reconstructed
from current file hashes and matched both provenance and the value above.

The current candidate bytes are bound as follows:

| Evidence | SHA-256 |
|---|---|
| authoritative coupon source | `07755b38ec2b008a19ba556cd18d5cd84e3ebb47b62c995571783480bab5c917` |
| focused test | `38f4deb59e40c0a056bde45ea650fb058dc79db9f491180c5abe8758eb3e4147` |
| STEP generator | `b803696277c1edf831002a5b3809e68ee22cf612a853437e6b9d9fc2f852856d` |
| print generator | `f51ae3105300bd80d1f16736c104525282c9b8d0a87c4518afe90c04ddf4a3c7` |
| provenance generator | `3f19531dda721df7d1e52e223195afd1d17d657275e41d57b8e4cc059330da81` |
| STEP | `14716d85365645ead4774ea03cc5d93fb330b807f902d067ee8c09f2abbef085` |
| print 3MF | `07810673e418315fb6c782a1799f65fe15d9f5390db9390a6f8420c139245ce2` |
| print STL | `6181d4ae4c9e5a396c1cc425826464cb00074fbb618be9d67630ee12d92529b0` |
| provenance JSON | `db8fe0be3b2513846be1d268fe8a547cb922d99a6811a0e686fcc7c3ef9f5be7` |
| front snapshot | `76e7e649f8bc4140b2b44f7ff41d0b72b1bc92bf76e861bc7770c3b2b887d36d` |
| oblique snapshot | `874ad187ef563d9e6ca8600e7cb85a4ea761f25ab998dbbed1fa51ff16096430` |
| opposed snapshot | `44df6aad14e5228c5880d247770701ff706fb4a15f534bae1ec428053f4ca7e3` |

Any change to a bound candidate file invalidates this slicing disposition.
Changes only to downstream slicer evidence require a new G-code review, not a
coupon redesign.

## Joined evidence and requirement coverage

- Independent critique and validation used the same exact candidate
  fingerprint and did not identify a geometry blocker to slicing.
- The focused suite was rerun by this reviewer and passed `6/6`.
- STEP validation was rerun and returned `ok=true`, one occurrence, and zero
  failures. Source-generator versus written-STEP diff reported no topology,
  geometry, bounds, plane, or count change.
- The actual Blue-Orange cutter gap is `1.715042423717553 mm`, the cutters do
  not intersect, both slots pass through the full `3.20 mm` thickness, and
  the ordinary exterior boundary web remains `2.20 mm`.
- The 3MF/STL evidence establishes one print-oriented, positive-volume,
  manifold coupon on a broad face at build `Z=0`; no support geometry is
  required by the exact extrusion.
- All three saved snapshots were inspected at original resolution. They show
  one rectangular coupon, two distinct complete through-slots, continuous
  material between them, and no Green/fixed-axle/other product geometry. The
  exact minimum point is not identifiable from the unannotated images.

The evidence is sufficient for the deliberately narrow question: prepare a
flat PETG coupon to learn whether this exact ligament can be realized and
survive ordinary bed removal and finger handling. It does not predict the
full plate's stiffness, rail loading, heat, wear, motion, or assembly behavior.

## Finding dispositions and release conditions

### Candidate digest omits separately listed evidence — accepted and bound here

The canonical eight-field digest omits the focused test, provenance generator,
provenance JSON, and snapshots. That omission is a provenance weakness, not a
geometry defect. This formal review binds their exact hashes in the table
above, so it does not block this one slicing handoff. A future candidate
manifest should include every decision-bearing file in one canonical digest.

### Visible witness marker absent — no CAD change; external locator required

Do not engrave or otherwise modify the coupon. Before printer upload/start,
create and retain an external annotated slicer screenshot or equivalent
non-geometric guide pointing to the witness at print build
`XY=(-0.938941, +7.963860) mm`. The physical record must use this locator for
top, bottom, and oblique close-up observations. Without it, the physical
PASS/FAIL is ambiguous and must not be recorded as accepted.

### DfAM wall sampler unavailable — not a slicing blocker, no fabricated PASS

The installed DfAM wall-thickness sampler could not run because `rtree` is
absent. The exact BREP distance and support-free orientation are adequate to
advance to slicing, but no sampled-wall DfAM PASS is claimed. Slicer toolpath
evidence and the physical coupon remain the controlling manufacturing gates;
installing `rtree` is optional and would not replace either gate.

### Mandatory exact-G-code toolpath gate — blocks upload/start

After slicing the exact `3MF` or `STL` above, inspect the exact G-code at:

1. the first material layer at the witness;
2. one representative middle layer through the `3.20 mm` thickness; and
3. the top material layer.

At each layer, at build `XY` approximately `(-0.939,+7.964) mm`, require a
continuous material toolpath across the ligament, both neighboring slots still
open, no omitted island, no accidental bridge/fusion, supports disabled, and
no unresolved slicer warning. Record exact G-code hash, printer/profile,
material/tool mapping, layer and first-layer heights, extrusion/line-width and
wall strategy, infill, first-layer expansion or compensation, temperatures,
cooling, and speed. Failure of any condition rejects that G-code for print;
it does not silently authorize a coupon geometry change.

## New cap and plate-gap requirement is outside this coupon

The later requirement that rod caps stay short and that the axial gap between
plates remain as wide as possible is not represented here: this coupon contains
no rods, caps, XT60 envelope, or plate stack. It neither conflicts with nor is
validated by this slicing acceptance. It must be carried into the next product
CAD contract and checked against the real XT60 insertion/service envelope
before any complete P20 print.

## Acceptance labels

- **Digital coupon CAD/mesh:** accepted for slicing on the exact fingerprint.
- **Slicer/G-code:** pending the exact first/middle/top toolpath gate and
  external witness locator.
- **Printer upload/start:** not authorized by this review.
- **Physical coupon:** pending PETG print, bed removal, handling, and the exact
  `BRIEF.md` observation question.
- **P20 product/profile:** not accepted; ordinary `>=2.20 mm` web rule remains.

## Commands rerun by formal reviewer

```text
sha256sum <six frozen inputs, five joined review inputs, and all bound evidence>
  -> every declared hash matched

uv run python - <<'PY'
  # reconstruct sorted compact eight-field candidate digest
PY
  -> 07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be

uv run pytest -q projects/xt60-bend-jig/tests/test_p20_blue_orange_web_coupon.py
  -> 6 passed

uv run python <cad-skill>/scripts/inspect validate \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step
  -> ok=true; occurrenceCount=1; failureCount=0

uv run python <cad-skill>/scripts/inspect diff \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step.py \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step --planes
  -> topologyChanged=false; geometryChanged=false; bboxChanged=false; all deltas zero
```

Next action: create the exact slicer/G-code candidate, external witness locator,
and layer-level toolpath record. Only then may a separate printer-start gate be
considered.
