# P20 R4 blocked test-print 3MF brief

Date: `2026-08-27`

Status: **FROZEN FOR MODEL-ONLY 3MF PREPARATION; NOT MANUFACTURING-ACCEPTED**

Owner/role: `/root/p20_3mf_design`, print-kit design/contract owner. This
role does not implement, validate, approve, slice, upload, or start a print.

## User authorization and safety boundary

The user explicitly requested: **prepare the P20 print 3MF** after inspecting
the full P20 R4 CAD preview. This authorizes one source-derived, model-only
3MF containing the printable plastic parts of the exact P20 R4 candidate. It
does not authorize geometry redesign, slicer settings, G-code, upload, printer
control, or print start.

The parent P20 R4 candidate is still blocked for manufacturing acceptance:

- Blue rod / XT60 solid intersection: `186.980487 mm3` at OPEN and
  `63.593308 mm3` at MID;
- fixed-axle hex / inner-rim web: `1.152 mm`;
- left outer Blue-Orange rail web: `1.715 mm`;
- rod/workpiece contacts still require functional disposition;
- unchanged `9.05 mm` caps and `18.40 mm` inner clear span are not physically
  accepted.

The requested 3MF is therefore an **evidence-only blocked test artifact**. Its
existence, mesh validity, or successful import must never be reported as proof
that the product is safe, manufacturable, printable, or physically accepted.

## Frozen baseline and immutable inputs

Baseline Git HEAD: `9698cf30e9ddb3e576c08179bfdd067446514c67`.

Parent P20 R4 candidate-manifest fingerprint:
`e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`
(`30/30` rows previously verified).

The 3MF implementation must verify these exact inputs before writing derived
artifacts:

```text
e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db  projects/xt60-bend-jig/docs/iterations/p20-r4-custom-profile-full-cad/IMPLEMENTATION_CANDIDATE.sha256
7979c6ebbacde425c47e4ac96f6e5287e064c09452b84ec771aa841f7a13e971  projects/xt60-bend-jig/docs/iterations/p20-r4-custom-profile-full-cad/HANDOFF.md
96935afda438dc487b1ed68e48140a3364ca1a96a3de10ff2ba93a78610477de  projects/xt60-bend-jig/docs/iterations/p20-r4-custom-profile-full-cad/REVIEW.md
7e44623cb2a515ac763454a253b705c5010842dba8e0825d8eee38156add40ba  projects/xt60-bend-jig/docs/iterations/p20-r4-custom-profile-full-cad/VALIDATION.md
38ed907ea1ec0e22ff8c42c2c03e047049b65ea9962b2fe7e58ea914aecac93e  projects/xt60-bend-jig/src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py
41c06b8536fbf4e1bb2e9979d74de299232379b4b0ebf87ee81e93c63f581017  projects/xt60-bend-jig/src/xt60_bend_jig/p19_r1_front_edge_short_tail.py
a6f69d3e1a0283fae382a0d31b608b1fad3e03805010da211c1df1c00f67b32c  projects/xt60-bend-jig/scripts/export_p13_3mf.py
```

The P19 source is precedent only for the print-bed transforms and layout. The
P13 exporter is precedent only for welded source tessellation, lib3mf writing,
round-trip validation, metadata, and provenance. Neither is geometry authority
for P20 R4.

## Delta mask

Allowed:

- add a `build_print_kit()` composition that copies the frozen P20 R4
  printable solids, or an equivalently named pure composition helper;
- rotate and translate copied occurrences onto the bed;
- prefix stable print-object labels;
- tessellate the unchanged source-derived solids and package them as a
  model-only 3MF;
- write provenance, focused tests, STEP/3MF artifacts, and review snapshots.

Forbidden:

- changing any plate, rail, bore, fixed axle, keeper, cap, radius, thickness,
  fit, clearance, stack, or profile geometry;
- shortening the caps or widening the plate stack;
- including purchased rods, XT60, wire/workpiece, tools, or motion envelopes;
- merging printable parts into one mesh;
- adding slicer settings, process/material profiles, support decisions, G-code,
  upload metadata, or printer-start instructions;
- calling the 3MF production-ready or using it to waive any parent blocker.

## Exact printable object census

The STEP print kit and model-only 3MF must each contain exactly `13` distinct,
named, positive-volume printable objects:

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

Explicitly excluded:

- three purchased `OD4 x 50 mm` stainless rods;
- XT60 reference body;
- exact 90-degree two-conductor workpiece/wire;
- all reference, collision, motion, tool, and coupon geometry.

Every 3MF object remains a separate mesh and build item so the user or slicer
can identify and arrange parts individually.

## Frozen bed orientation and layout

Use the proven P19 transform convention without changing geometry:

- each X-axis plate and each keeper is rotated `Rot(0,-90,0)` so a broad flat
  face rests at `Z=0`;
- the stepped axle remains horizontal as built and is translated so its
  minimum Z is `0`;
- every cap is rotated with its X axis into the bed plane using
  `Rot(0,-90,0)` and translated so its minimum Z is `0`;
- after orientation, every object is centered on its declared XY placement by
  its source BREP bounds and translated by `-bounds.min.Z` onto the bed.

Freeze these placement centers in millimetres, inherited from the P19
print-kit layout:

| object | X | Y |
|---|---:|---:|
| left inner plate | `-78` | `42` |
| right inner plate | `-22` | `42` |
| left outer plate | `42` | `42` |
| right outer plate | `108` | `42` |
| stepped axle | `-56` | `-28` |
| left keeper | `10` | `-28` |
| right keeper | `26` | `-28` |
| left Blue cap | `-34` | `-78` |
| right Blue cap | `48` | `-78` |
| left Orange cap | `-20` | `-78` |
| right Orange cap | `62` | `-78` |
| left Green cap | `-6` | `-78` |
| right Green cap | `76` | `-78` |

This is a deterministic source layout, not a printer-profile claim. Validate
pairwise XY bounding-box separation after placement; any positive overlap over
`1e-7 mm` fails. Require every object minimum Z within `1e-6 mm` of zero and
no negative-Z vertex beyond that tolerance. Record the overall XY footprint;
do not claim it fits a particular printer until a later slicer/profile stage.

## Required source and artifacts

- Authoritative geometry remains:
  `src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py`.
- Source-derived print-kit STEP generator/artifact:
  `cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.step.py` and
  `p20_r4_print_kit.step`.
- Model-only export helper:
  `scripts/export_p20_r4_print_kit_3mf.py`.
- Model-only 3MF:
  `cad/p20_r4_custom_profile_full_cad/p20_r4_print_kit.3mf`.
- Provenance:
  `cad/p20_r4_custom_profile_full_cad/p20-r4-3mf-provenance.json`.
- Focused tests:
  `tests/test_p20_r4_print_kit_3mf.py`.
- Review evidence:
  `docs/review/p20-r4-blocked-test-print-3mf/` containing one STEP bed-layout
  snapshot and one 3MF snapshot that visibly show all 13 separate objects.

## STEP and 3MF validation contract

### Source and STEP

- `build_print_kit()` returns exactly the 13 labels above, in that order, with
  no duplicates; every child is one valid closed positive-volume solid.
- The print-kit composition may transform copies only; source volume for each
  printed occurrence must match the corresponding frozen P20 R4 source solid
  within `1e-6 mm3` absolute tolerance.
- The source layout passes bed-Z and pairwise XY-box checks.
- Generate the STEP through the repository CAD workflow; run `inspect
  validate`, `inspect refs --facts --planes --positioning`, and `inspect diff`
  between the `.step.py` source and written `.step`.
- Written STEP must preserve all 13 distinct labels, occurrence count, bounds,
  volumes, bed layout, and source-to-export parity.

### Model-only 3MF

- Tessellate each STEP-print-kit source child directly; do not re-model from
  screenshots or hand-edit the archive.
- Use the P13 proven mesh defaults unless an independently validated reason is
  recorded: linear tolerance `0.02 mm`, angular tolerance `0.05 rad`, vertex
  weld tolerance `1e-6 mm`.
- Each of the 13 meshes must have positive signed volume, non-empty vertices
  and triangles, and pass `lib3mf` `IsValid()` plus
  `IsManifoldAndOriented()` before and after round-trip.
- Unit must be millimetres. The 3MF must contain exactly 13 mesh objects and
  13 identity-transform build items in the frozen order and labels.
- It must be model-only: no slicer profile, material/process preset, G-code,
  support, brim, plate assignment, or printer-control payload.
- Re-open the written 3MF with lib3mf and independently verify unit, mesh/build
  census, labels/order, manifold/oriented state, positive volume, bed Z,
  pairwise XY bounds, and metadata.
- Embed and round-trip verify provenance metadata for parent candidate SHA,
  source SHA, this BRIEF SHA, exporter SHA, artifact role, and explicit
  `manufacturingAccepted=false` / `printingInitiated=false` state.
- The JSON provenance records artifact SHA-256, STEP SHA-256, source and
  exporter SHA-256 values, frozen object labels, exclusion list, mesh counts,
  source/mesh volumes, per-object bounds and bed contact, overall footprint,
  lib3mf round-trip result, and all known parent blockers.

## Visual and handoff gate

Both STEP and 3MF snapshots must show the complete 13-object layout with no
hidden or overlapping part. Validate the actual 3MF review surface before
handing it to the user; a file hash or successful lib3mf import alone is not
visual proof.

The handoff wording must say:

> P20 R4 model-only 3MF prepared as a blocked test artifact. It contains 13
> printable plastic objects and no rods, XT60, or wire. Mesh/STEP validation
> does not waive the XT60 collision or thin-web failures. It has not been
> sliced, uploaded, or printed.

No downstream slicing or printer action may begin without a separate user
request after this exact 3MF has been shown and identified.
