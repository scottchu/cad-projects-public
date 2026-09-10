# P20 R4 custom-profile full-CAD implementation receipt

Date: `2026-08-27`

Task: `P20R4-IMPL-01`

Owner/role: `/root/p20_final_impl`, implementation only. This receipt does
not approve the candidate.

Status: **IMPLEMENTED AS A NON-MANUFACTURING FULL-ASSEMBLY PREVIEW; LIKELY
PRODUCT BLOCKER FOUND AT THE XT60 REFERENCE**

## Verified inputs and candidate

- Frozen BRIEF SHA-256: `295c414a6f4a4f657e3bb6d0a76686baef38c413f1f3c015f79293bcd0b7f64a`.
- Frozen DESIGN SHA-256: `04915102cebf3891a47202bfa69843d317bdf58e1bfdf9aa22673efde3af3a06`.
- Frozen TASK_DAG SHA-256: `eb29cbf6fd8c8ec5f675b57684a46a9d08fb04f7a6e4e75c3a7dd7c631cbc498`.
- Frozen input-manifest SHA-256: `4286336b7709980f7d9ec4d22bb3f54f262639b88d3b3a7a1dba36b9e48b0691`.
- Exact compact-profile SHA-256:
  `7a8013c935c74df865b3bd861ec163a00725e86f0e27415489babd26cd85eeb0`.
- Candidate manifest:
  `IMPLEMENTATION_CANDIDATE.sha256`, `30/30` rows verified.
- Candidate-manifest SHA-256:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.

Focused repair cycle 1 corrected export identity labels only. The left and
right inner plates previously shared one cached BREP identity, so the STEP
exporter's later right-side label replaced both occurrences. The cache now
owns one independent BREP per side. Geometry, profile, dimensions, motion and
all known blockers are unchanged. A focused regression imports every written
STEP and requires exactly one left-inner and one right-inner occurrence.

## Implemented geometry

- One pure, deterministic 361-point world-path authority drives all three
  rods, the fixed-inner features and both inverse outer-plate rail sets.
- The exact 361 samples remain the analytic authority. For practical BREP
  generation, each curved outer rail uses 33 verified polyline centers. The
  maximum distance from any of the 361 exact centers to its BREP polyline is
  `0.003066465573 mm`, below the frozen `0.01 mm` limit. Per-rail maxima are:
  left Blue `0.003049`, left Orange `0.003066`, left Green `0.001204`,
  right Blue `0.002169`, right Orange `0.001681`, right Green `0.001204 mm`.
- Blue and Orange inner rails are exact straight capsules. Green inner travel
  is exactly `0.0 mm`, so it is a round `4.15 mm` bore.
- Both fixed-axle rails are true circular `R=sqrt(200)` arcs, not sampled
  polylines. Round-trip residuals are `<=3.973e-15 mm`.
- Four plates are `R20 x 3.20 mm` inner and equal `R22.5 x 3.20 mm` outer.
  Every outer plate has all three complete white-rod rails and one `7.90 mm`
  fixed-axle arc.
- The fixed stepped axle is world-stationary at `A=(-10,-10)` with inherited
  `34.90 mm` X length and two keepers.
- The full assembly has exactly 18 leaf occurrences: four plates, three
  `OD4 x 50 mm` rods, six unchanged `9.05 mm` caps, axle, two keepers, XT60
  and P20 R3's exact two-conductor 90-degree workpiece.
- The inherited axial stack remains unchanged: inner plate centers
  `X=-10.8/+10.8`, outer centers `X=-14.4/+14.4`, inner clear span `18.4 mm`,
  and cap-to-outer axial clearance `0.30 mm`.

## Paths and generated artifacts

- Source:
  `src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py`.
- Focused tests:
  `tests/test_p20_r4_custom_profile_full_cad.py`.
- CAD directory:
  `cad/p20_r4_custom_profile_full_cad/`.
- Written STEP targets:
  `p20_r4_open.step`, `p20_r4_mid.step`, `p20_r4_end.step`,
  `p20_r4_exploded.step`, and `p20_r4_full_motion.step`.
- Viewer sidecar: `p20_r4_full_motion.params.js`; OPEN geometry is the source
  pose, left/right outer rotations are `+45u/-45u`, and every rod/cap follows
  the same world path.

STEP SHA-256 values:

| artifact | SHA-256 |
|---|---|
| OPEN | `6905e17adaffe7a63af88eeaf5c33e7a0fa9de391d93183751fa147a1d853a9b` |
| MID | `f272df4329aef4f2beaab0afe43268242408c6ee5e0a32a7bc43afbab56e643b` |
| END | `c9b96d4c2b2f8526d0ad5201d0dc08f8f416518542bbd6f34f916d10980dd513` |
| EXPLODED | `0fd93dfe0aa1765fdb94aa6e68868c959ae07f5c7449b5413b7ce6bb5f937d9b` |
| FULL MOTION | `5d64f0849225383809ee493678418ed37a80820b4ea93f043d97f68ef39e41e1` |

## Commands and results

Focused tests:

```text
uv run pytest -q projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py
......                                                                   [100%]
```

Generation used one explicit `scripts/gen ... --write` call over the five
named `.step.py` targets. Result: five render packages built and five STEP
files written.

For every written STEP, these were run:

```text
scripts/inspect validate <target.step>
scripts/inspect refs <target.step> --facts --planes --positioning --format text
scripts/inspect diff <target.step.py> <target.step> --planes
```

Results:

- OPEN/MID/END/EXPLODED/FULL MOTION each report `18` valid occurrences and
  `failureCount=0`.
- Imported identity census passes for every written STEP: exactly one
  left-inner and exactly one right-inner occurrence.
- Source-to-written-STEP diff is zero for every target: no topology, geometry,
  bounding-box, count, size or center delta.
- OPEN and FULL MOTION bounds are `50.7 x 44.87417 x 53.25 mm`.
- MID bounds are `50.7 x 58.679082 x 60.12359 mm`.
- END bounds are `50.7 x 63.550636 x 63.550636 mm`.
- EXPLODED bounds are `147.2 x 137.811545 x 59.4 mm`.

Focused actual-solid evidence at OPEN/MID/END:

- maximum rod/any-plate intersection: `0.0 mm3`;
- maximum fixed-axle/outer-plate intersection: `0.0 mm3`;
- maximum cap/plate intersection: `0.0 mm3`;
- minimum cap/own-outer axial clearance: `0.29999999999999 mm`.

The known analytic failures are unchanged and are not waived:

- fixed-axle hex to inner rim web: `1.152 mm`;
- left outer Blue-Orange web: `1.715 mm`.

## XT60/workpiece trapping finding

An additional actual-BREP probe checked every plate and rod against the exact
P20 R3 XT60 and 90-degree workpiece references at OPEN/MID/END.

- All four plates are clear of XT60 and workpiece at all three states.
- The Blue/bottom rod intersects the XT60 reference body by
  `186.980487 mm3` at OPEN and `63.593308 mm3` at MID; it clears at END.
- Rod/workpiece intersections are Blue `27.847560/32.469756/0.0 mm3`,
  Green `1.558785 mm3` at all states, and Orange `0.294329 mm3` at END.

Some rod/workpiece contact is the bending function, but a rod passing through
the XT60 solid envelope is a likely product blocker. It is deliberately not
repaired here because the profile is frozen and this task authorizes preview,
not design drift. Independent critique/validation must classify it before any
manufacturing step.

## Mandatory visual review

The CAD snapshot tool generated and this implementation role inspected:

- `p20-r4-open-front-labelrepair_20260827T210320Z.png`;
- `p20-r4-mid-front-labelrepair_20260827T210321Z.png`;
- `p20-r4-end-front-labelrepair_20260827T210318Z.png`;
- `p20-r4-exploded-axial-labelrepair_20260827T210323Z.png`;
- `p20-r4-open-axial-stack-labelrepair_20260827T210316Z.png`.

The state snapshots use the CAD `RIGHT` camera because looking along X exposes
the physical FRONT-YZ mechanism plane. The solid right outer plate naturally
occludes deeper occurrences, while the exploded ISO view exposes all four
plates, all three rods, all six caps, both keepers, the axle, XT60 and 90-degree
workpiece. The additional TOP snapshot exposes the assembled X stack, the
unchanged `9.05 mm` cap heads, `18.4 mm` inner clear span and `0.30 mm`
cap-to-outer gaps for the user's cap-height/plate-gap review.

## Boundary and next action

This implementation is suitable only for independent critique, validation and
formal review of a user-facing full-assembly preview. It is not a product,
manufacturing, mesh, slice, print, force, friction, wear or physical acceptance
claim. Do not proceed to manufacturing from this fingerprint. The next action
is independent review of exact candidate manifest
`e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`.
