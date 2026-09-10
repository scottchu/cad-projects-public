# P20 R4 blocked test-print 3MF independent validation

Date: `2026-08-27`

Task: `P20R4-3MF-VALIDATE-01`

Owner/role: `/root/p20_3mf_validator`, independent validator. This role did
not edit source, STEP, 3MF, tests, provenance, snapshots, or continuity files.

Candidate manifest fingerprint:
`e11c3f94b1d4081a4e58db0ec74c76651f234ce97f2e8faa06f59600dc2be871`.

## Decision

**PASS for handoff only as the exact model-only blocked-test 3MF.**

**FAIL for manufacturing, slicing, upload, or print authorization.** The
validated mesh does not waive the parent P20 R4 blockers: Blue rod / XT60
solid intersections (`186.980487 mm3` OPEN and `63.593308 mm3` MID), the
`1.152 mm` inner-rim web, the `1.715 mm` left Blue-Orange rail web, unresolved
rod/workpiece contacts, and missing physical acceptance of the unchanged
`9.05 mm` caps and `18.40 mm` inner clear span.

The artifact is therefore suitable only to show and identify to the user as
a blocked test artifact. It has not been sliced, uploaded, or printed.

## Immutable candidate and provenance

- The parent full-CAD manifest retains fingerprint
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`,
  and all `30/30` of its rows pass `sha256sum --check` against the current
  worktree.
- The repaired child candidate manifest matches the assigned fingerprint and
  all `14/14` rows pass `sha256sum --check`.
- STEP SHA-256:
  `fb1188097e74752522e90dac96996b98c3d1379d42432d09607e62eea47b39e3`.
- 3MF SHA-256:
  `cd90dc1afa0c0658981b75a040daa2a8cc91d9addf362ae3bd09420ea4b05135`.
- Provenance SHA-256:
  `2f21bcbe1bb614555e62a99c67764580f8f1f3c2e13ab9dca7e5f1129f781327`.
- Frozen parent CAD source SHA-256:
  `38ed907ea1ec0e22ff8c42c2c03e047049b65ea9962b2fe7e58ea914aecac93e`.
- Isolated print-kit composition source SHA-256:
  `b850d90c26b7326a885c028978f029d414814050cf9fc1b08d25c6c9c85f04cf`.
- Exporter SHA-256:
  `a4c0dad6522e163613dfb755678225567928abb28f5be9ee8fedfa2e310b4a87`.
- Frozen BRIEF SHA-256:
  `56956b9d43ae8b3f17622e2384c3d3f5c22f86c2c60aa571b6c41941120080b0`.
- Parent manifest file SHA-256 matches the embedded parent fingerprint:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.

The prior provenance caveat is repaired. Print-kit-only constants and helpers
now live in `p20_r4_blocked_test_print_3mf.py`; the parent CAD source was
restored byte-for-byte, so both parent and child manifests are independently
self-verifying. The isolated module also performs a runtime guard before
building source parts. An independent negative test replaced the parent hash
function with a mismatching value in memory and confirmed that the helper
raises `ValueError("parent P20 R4 source fingerprint changed")` before
constructing the kit.

## Exact object census and source/STEP parity

Independent source construction, written STEP import, and lib3mf round-trip
all returned exactly these `13` distinct objects in the frozen order:

1. `print_fixed_left_inner_R20_blue_orange_rails_green_round_bore`
2. `print_fixed_right_inner_R20_blue_orange_rails_green_round_bore`
3. `print_rotating_left_outer_R22p5_three_inverse_rails_fixed_axle_arc`
4. `print_rotating_right_outer_R22p5_three_inverse_rails_fixed_axle_arc`
5. `print_fixed_stepped_axle_A_y-10_z-10_L34p90`
6. `print_fixed_left_permanent_outer_keeper`
7. `print_fixed_right_permanent_outer_keeper`
8. `print_left_bottom_permanent_cap_H9p05`
9. `print_right_bottom_permanent_cap_H9p05`
10. `print_left_diagonal_permanent_cap_H9p05`
11. `print_right_diagonal_permanent_cap_H9p05`
12. `print_left_upright_permanent_cap_H9p05`
13. `print_right_upright_permanent_cap_H9p05`

- Every source and STEP child is one valid closed positive-volume solid.
- Maximum source-to-rigidly-placed volume delta:
  `6.366462912410498e-12 mm3`, passing the `1e-6 mm3` limit.
- Maximum placed-source-to-written-STEP volume delta:
  `1.8276296032126993e-09 mm3`, passing the `1e-6 mm3` limit.
- Source and STEP layouts have zero pairwise positive XY bounding-box
  overlaps.
- Source maximum absolute minimum-Z error is
  `1.7763568394002505e-15 mm`; STEP is
  `1.7748696890133535e-13 mm`. Both pass the `1e-6 mm` bed tolerance.
- Source and STEP footprint: `228.5 x 145.8 mm`.

Repository CAD inspection independently reported:

- `inspect validate`: `13` occurrences, `failureCount=0`;
- `refs --facts --planes --positioning`: `13` leaf occurrences, `13`
  shapes, bounds `[-98,-81.3,0]` to `[130.5,64.5,10] mm`;
- source `.step.py` versus written `.step` diff: no topology, geometry,
  bounding-box, count, size, center, or major-plane change.

## 3MF round-trip and model-only boundary

The written artifact was reopened independently with lib3mf:

- unit: millimetres;
- `13` mesh objects and `13` build items in the frozen order;
- all build-item transforms equal the lib3mf identity transform;
- total mesh census: `23,384` vertices and `46,788` triangles;
- every mesh is non-empty, `IsValid()`,
  `IsManifoldAndOriented()`, and has positive signed volume;
- minimum per-object signed volume: `40.51999423300509 mm3`;
- zero pairwise positive XY bounding-box overlaps;
- maximum absolute minimum-Z error: `0.0 mm`;
- round-trip footprint: `228.5 x 145.8000030517578 mm`.

Embedded metadata round-trips and matches the actual parent-manifest, frozen
parent source, isolated composition source, BRIEF, and exporter hashes. It
also states:

- `artifactRole=blocked-test-model-only-13-printable-objects`;
- `manufacturingAccepted=false`;
- `printingInitiated=false`.

The external provenance JSON matches the actual STEP and 3MF hashes, object
order/count, layouts, metadata, and explicit
`geometryChangedForThreeMF=false`, `manufacturingAccepted=false`,
`printingInitiated=false`, `sliced=false`, and `uploaded=false` state.

The 3MF ZIP passes `unzip -t` and contains only:

```text
3D/3dmodel.model
[Content_Types].xml
_rels/.rels
```

No G-code, slicer profile, process/material preset, support, brim, plate
assignment, or printer-control payload is present.

## Visual review

I inspected both pinned snapshots at original resolution:

- `p20-r4-print-kit-step-repair1_20260827T213237Z.png`: four separated plates, one
  axle, two keepers, and six caps are all visible; no object is hidden or
  visually overlapping.
- `p20-r4-print-kit-3mf-repair1_20260827T213239Z.png`: the same complete 13-object
  layout is visible as the actual 3MF mesh surface; all objects are separated.
  The uniform white rendering contains no material/painting claim.

The snapshots support object presence and separation only. They do not prove
feature manufacturability or physical fit.

## Commands and results

```text
sha256sum IMPLEMENTATION_CANDIDATE.sha256
# e11c3f94b1d4081a4e58db0ec74c76651f234ce97f2e8faa06f59600dc2be871

sha256sum --check IMPLEMENTATION_CANDIDATE.sha256
# child 14/14 OK; parent 30/30 OK

uv run python <cad-skill>/scripts/inspect validate \
  .../p20_r4_print_kit.step --skip-self-intersection
# ok=true, occurrenceCount=13, failureCount=0

uv run python <cad-skill>/scripts/inspect refs \
  .../p20_r4_print_kit.step --facts --planes --positioning
# 13 leaf occurrences, 13 shapes, 228.5 x 145.8 x 10.0 mm

uv run python <cad-skill>/scripts/inspect diff \
  .../p20_r4_print_kit.step.py .../p20_r4_print_kit.step --planes
# no topology/geometry/bounds/count/size/center/plane delta

uv run pytest -q \
  projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py \
  projects/xt60-bend-jig/tests/test_p20_r4_print_kit_3mf.py
# 9 passed

uv run python <runtime-guard negative probe>
# runtime_guard=PASS expected_mismatch_rejected

unzip -t .../p20_r4_print_kit.3mf
# no errors
```

An additional read-only Python/lib3mf audit independently recomputed the
source/STEP/3MF labels, solid and mesh validity, source/STEP volume parity,
signed mesh volumes, build transforms, Z contact, pairwise XY separation,
footprint, metadata, archive payload boundary, and provenance hashes; all
child-candidate assertions passed.

## Required handoff wording

> P20 R4 model-only 3MF prepared as a blocked test artifact. It contains 13
> printable plastic objects and no rods, XT60, or wire. Mesh/STEP validation
> does not waive the XT60 collision or thin-web failures. It has not been
> sliced, uploaded, or printed.
