# P20 R4 independent validation

Date: `2026-08-27`

Task: `P20R4-VALIDATE-01`

Owner/role: `/root/p20_final_validator`, independent validator. This role did
not implement or repair the candidate.

Candidate-manifest SHA-256:
`e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.

## Verdict

- **Full-assembly geometry and STEP occurrence identities pass for an
  explicitly non-manufacturing user preview.** The OPEN/MID/END, exploded and
  full-motion geometry is complete and visually reviewable. All five written
  STEP files now retain distinct left-inner and right-inner identities.
- **Manufacturing, slicing and printing acceptance: FAIL / NOT AUTHORIZED.**
  The known `1.152 mm` inner-rim and `1.715 mm` left Blue-Orange web failures
  remain, and the Blue rod passes through the XT60 reference solid at OPEN
  and MID.

## Fingerprint and focused test evidence

`sha256sum -c IMPLEMENTATION_CANDIDATE.sha256` verified all `30/30` rows.
The exact profile JSON hash independently recomputed to
`7a8013c935c74df865b3bd861ec163a00725e86f0e27415489babd26cd85eeb0`.

```text
uv run pytest -q projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py
......                                                                   [100%]
```

## Independent math recomputation

The validator parsed the frozen compact JSON, independently rebuilt START
points from each polar angle/radius, added the frozen shared offset to the
three P19 base END points, sampled each world path at all `361` values, and
then applied independent left/right inverse rotations.

- Source path authority versus direct profile recomputation:
  `4.974e-10 mm` maximum difference. This is within the frozen `1e-9 mm`
  coordinate tolerance and comes from the explicit nine-decimal source
  coordinates.
- Rod inverse round-trip maximum residual: `4.441e-15 mm`.
- Fixed-axle inverse round-trip maximum residual: `3.972e-15 mm`.
- Green START-to-END travel: numerically zero; its inner feature is correctly
  a round bore while both outer Green paths remain complete 45-degree arcs.
- Independent exact-path-to-33-point-BREP-polyline deviations:

| rail | maximum deviation (mm) |
|---|---:|
| left Blue | `0.003049` |
| left Orange | `0.003066` |
| left Green | `0.001204` |
| right Blue | `0.002169` |
| right Orange | `0.001682` |
| right Green | `0.001204` |

Overall maximum is `0.003066 mm`, below the frozen `0.01 mm` BREP preview
limit.

## Assembly census and constraints

For OPEN, MID and END, source assemblies each contain exactly `18` valid,
positive-volume leaf occurrences: four plates, three OD4 x 50 rods, six caps,
one stepped fixed axle, two keepers, one XT60 reference and one exact
90-degree two-conductor workpiece. The exploded and full-motion artifacts
also contain `18` leaves.

The checked source parameters retain:

- inner/outer radii `20.0/22.5 mm`;
- plate thickness `3.20 mm` and X centers `-14.4, -10.8, +10.8, +14.4 mm`;
- inner clear span `18.40 mm`, rod length `50.00 mm`;
- cap head length `9.05 mm`, engagement `8.70 mm`;
- fixed axle length `34.90 mm` and location `A=(-10,-10)`;
- minimum cap-to-own-outer axial clearance `0.300000 mm`.

The source constructs Blue/Orange complete inner capsules, Green's round
inner bore, all three complete inverse rails on each outer plate, and both
fixed-axle inverse arcs. No coupon-only object replaces the full assembly.

## Actual-solid collision evidence

Independent all-pairs BREP checks were run over the `18` source occurrences
at OPEN/MID/END. Focused mechanism results are:

- maximum rod/any-plate intersection: `0.0 mm3`;
- maximum fixed-axle/outer-plate intersection: `0.0 mm3`;
- maximum cap/any-plate intersection: `0.0 mm3`;
- the axle touches the two inner guide bores without positive-volume
  intersection;
- each rod/cap interface is clear/tangent without positive-volume
  intersection;
- the fixed axle overlaps each keeper by `0.713927 mm3`, an intended
  retention interference;
- XT60/workpiece overlap is `297.701247 mm3` at every state, the intended
  reference termination connection.

Rod/reference intersections requiring explicit review are:

| pair | OPEN (mm3) | MID (mm3) | END (mm3) | classification |
|---|---:|---:|---:|---|
| Blue rod / XT60 body | `186.980487` | `63.593308` | `0.0` | unexpected blocker |
| Blue rod / workpiece | `27.847560` | `32.469756` | `0.0` | bend-contact evidence |
| Green rod / workpiece | `1.558785` | `1.558785` | `1.558785` | bend/contact, review physically |
| Orange rod / workpiece | `0.0` | `0.0` | `0.294329` | bend-contact evidence |

The Blue rod/XT60 solid intersection is not an allowed rod-in-own-cut or
axle-in-own-guide contact. It blocks product acceptance and must remain
visible to the user; this validation does not redesign the frozen profile.

## Written STEP validation and parity

For each of `open`, `mid`, `end`, `exploded`, and `full_motion`, the validator
ran:

```text
scripts/inspect validate <artifact.step>
scripts/inspect refs <artifact.step> --facts --planes --positioning --format text
scripts/inspect diff <artifact.step.py> <artifact.step> --planes
```

All five written STEP files report `18` valid leaf occurrences and
`failureCount=0`. Source versus exported geometry has zero topology, geometry,
bounds and count delta according to `inspect diff`. An independent import
comparison found maximum bounds delta `7.11e-15 mm` and maximum corresponding
child-volume delta `1.83e-9 mm3`.

Independent source/import label comparison now finds no missing or extra
labels in any artifact. OPEN/MID/END/EXPLODED each retain:

```text
fixed_left_inner_R20_blue_orange_rails_green_round_bore
fixed_right_inner_R20_blue_orange_rails_green_round_bore
```

The full-motion STEP likewise retains distinct
`motion_full_fixed_left_inner` and `motion_full_fixed_right_inner` labels.
Geometry and exact occurrence-label parity both pass.

## Snapshot review

All five frozen snapshots exist, match the candidate manifest, and were
visually inspected:

- `p20-r4-open-front-labelrepair_20260827T210320Z.png`;
- `p20-r4-mid-front-labelrepair_20260827T210321Z.png`;
- `p20-r4-end-front-labelrepair_20260827T210318Z.png`;
- `p20-r4-exploded-axial-labelrepair_20260827T210323Z.png`;
- `p20-r4-open-axial-stack-labelrepair_20260827T210316Z.png`.

The FRONT state snapshots correctly show the rotating outer face and its
complete cut paths, but that opaque face naturally occludes the inner plate,
rear caps and deeper stack. The exploded ISO snapshot visibly exposes all
four plates, all three rods, all six caps, both keepers, the fixed axle, XT60
and the 90-degree workpiece. The TOP axial snapshot exposes the unchanged
cap height, four-plate stack, inner clear span and `0.30 mm` cap/outer gap.

## Remaining boundary

This candidate may be shown as a **complete geometry intent preview** so the
user can accept or reject topology and orientation. Its STEP geometry and
occurrence identities are clean for that preview purpose, but it must not be
called manufacturing-ready. No mesh, slicer, upload, print, force, friction,
wear or physical-fit claim follows from this validation.
