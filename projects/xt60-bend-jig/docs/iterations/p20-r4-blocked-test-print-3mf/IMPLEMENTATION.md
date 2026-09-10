# P20 R4 blocked test-print 3MF implementation receipt

Date: `2026-08-27`

Task: `P20R4-3MF-IMPL-01`

Owner/role: `/root/p20_3mf_impl`, implementation only. This receipt does not
approve manufacturing or printing.

Status: **IMPLEMENTED AS A MODEL-ONLY BLOCKED TEST ARTIFACT; NOT SLICED,
UPLOADED, OR PRINTED**

## Verified contract

- Parent candidate-manifest fingerprint:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.
- Corrected frozen BRIEF SHA-256:
  `56956b9d43ae8b3f17622e2384c3d3f5c22f86c2c60aa571b6c41941120080b0`.
- Frozen P20 R4 source SHA-256 before print-kit-only additions:
  `38ed907ea1ec0e22ff8c42c2c03e047049b65ea9962b2fe7e58ea914aecac93e`.
- Parent P20 R4 source remains exactly:
  `38ed907ea1ec0e22ff8c42c2c03e047049b65ea9962b2fe7e58ea914aecac93e`.
- Separate print-kit composition source SHA-256:
  `b850d90c26b7326a885c028978f029d414814050cf9fc1b08d25c6c9c85f04cf`.

The first input check stopped before editing because the BRIEF contained an
incorrect P19 precedent hash. The contract owner corrected and refroze the
BRIEF; the resumed check matched all frozen inputs. Focused repair cycle 1
then moved every print-kit-only constant and helper into the separate
`p20_r4_blocked_test_print_3mf.py` module after validation found that adding
them to the parent source invalidated its internal candidate manifest. The
parent source was restored byte-for-byte and its `30/30` manifest rows verify.
No P20 R4 plate, rail, bore, axle, keeper, cap, stack, or profile builder was
changed.

## Implemented output

- Added `p20_r4_blocked_test_print_3mf.py` with
  `build_print_source_parts()`, `build_print_parts()`, and `build_print_kit()`
  to compose rigidly transformed copies imported from the frozen P20 R4
  parent source. The helper refuses to run if the parent source hash changes.
- The kit contains exactly 13 distinct positive-volume solids: four plates,
  one stepped axle, two keepers, and six unchanged `H9.05 mm` caps.
- Purchased rods, XT60, wire/workpiece, motion/reference objects, tools and
  coupons are excluded.
- The fixed P19 layout centers and orientation convention are used exactly.
- The source and round-trip mesh footprint is `228.5 x 145.8 mm`; pairwise XY
  bounding-box overlap count is `0`, and all 13 objects contact `Z=0` within
  `1e-6 mm`.
- Maximum rigid-transform source-volume delta is
  `6.367e-12 mm3`, below the `1e-6 mm3` contract tolerance.

The primary print-kit STEP is:
`cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.step`.

The secondary model-only 3MF is:
`cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.3mf`.

The 3MF contains 13 named lib3mf mesh objects and 13 identity-transform build
items in the frozen order. It uses millimetres and contains `23,384` welded
vertices and `46,788` triangles. Every mesh is non-empty, positive-volume,
`IsValid()`, and `IsManifoldAndOriented()` before and after lib3mf round-trip.
The archive has only the standard model, content-types, and relationship
entries; it contains no slicer, process, material, support, G-code, or printer
payload.

Embedded metadata round-trips the parent candidate fingerprint, source,
BRIEF and exporter hashes, artifact role, and explicit
`manufacturingAccepted=false` / `printingInitiated=false` values. External
provenance is recorded in `p20-r4-3mf-provenance.json`.

## Artifact hashes

| artifact | SHA-256 |
|---|---|
| STEP | `fb1188097e74752522e90dac96996b98c3d1379d42432d09607e62eea47b39e3` |
| model-only 3MF | `cd90dc1afa0c0658981b75a040daa2a8cc91d9addf362ae3bd09420ea4b05135` |
| provenance JSON | `2f21bcbe1bb614555e62a99c67764580f8f1f3c2e13ab9dca7e5f1129f781327` |
| exporter | `a4c0dad6522e163613dfb755678225567928abb28f5be9ee8fedfa2e310b4a87` |

## Commands and results

Generation:

```text
uv run python <cad-skill>/scripts/gen \
  projects/xt60-bend-jig/cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.step.py \
  --write --json
```

Result: one STEP and a matching CAD render package were generated.

Export:

```text
uv run python projects/xt60-bend-jig/scripts/export_p20_r4_print_kit_3mf.py
```

Result: 13 mesh objects and 13 build items passed lib3mf pre-write and
round-trip validation; provenance was written.

STEP validation:

```text
scripts/inspect validate p20_r4_print_kit.step
scripts/inspect refs p20_r4_print_kit.step --facts --planes --positioning
scripts/inspect diff p20_r4_print_kit.step.py p20_r4_print_kit.step
```

Results: `13` leaf occurrences, `failureCount=0`, bounds
`228.5 x 145.8 x 10.0 mm`, and zero topology/geometry/bounds/count/size/center
delta between source generator and written STEP.

Before/after repair comparison also confirmed every STEP object label, bound
and volume remained identical, and every 3MF mesh label, source/placed/mesh
volume, bound, vertex count and triangle count remained identical.

Tests:

```text
uv run pytest -q \
  projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py \
  projects/xt60-bend-jig/tests/test_p20_r4_print_kit_3mf.py
.........                                                                [100%]
```

`unzip -t p20_r4_print_kit.3mf` also passed. A non-required `ruff` check was
attempted but the root workspace does not provide the `ruff` executable; no
environment or dependency change was made.

## Visual review

The CAD snapshot tool rendered and this implementer inspected both actual
artifacts from TOP:

- `p20-r4-print-kit-step-repair1_20260827T213237Z.png` — all 13 source-colored STEP
  solids are individually visible and separated;
- `p20-r4-print-kit-3mf-repair1_20260827T213239Z.png` — all 13 mesh objects are visible
  in the same bed layout, with no hidden or overlapping part.

The white 3MF rendering is expected because this model-only export carries no
slicer/material painting. The geometry and object census match the STEP.

## Blockers and handoff boundary

This preparation does not waive any parent P20 R4 blocker: Blue rod/XT60
intersections (`186.980487 mm3` OPEN, `63.593308 mm3` MID), `1.152 mm` inner
rim web, `1.715 mm` left Blue-Orange rail web, unresolved functional
rod/workpiece contacts, or missing physical acceptance for the unchanged
`9.05 mm` caps and `18.40 mm` inner clear span.

The next action is independent critique and validation against the exact
candidate manifest. Do not slice, upload, or print from this receipt.
