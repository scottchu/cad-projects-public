# P19 R1 repaired-candidate independent validation

Owner/role: `/root/p18_validator`, independent validator (`P19-VAL-05`)

Date: 2026-08-26

Decision: **PASS the exact repaired candidate for formal review and exact-artifact
Viewer handoff.** All assigned parametric, constraint, actual-solid, service,
written-STEP and visual-review gates pass. This is digital acceptance only;
mesh/3MF/slicing and physical print, assembly, cap fit, force and self-lock
acceptance remain unperformed.

No candidate source, tests, STEP, sidecar, snapshot or continuity file was
changed by this validation. Only this validation record was replaced.

## Frozen fingerprint

- Candidate manifest: `IMPLEMENTATION_CANDIDATE.sha256`.
- Exact manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- `sha256sum -c` result: all `20/20` declared content entries `OK`. The command
  also warns that the four leading comment lines are not checksum records;
  they are not candidate entries.
- Repaired design SHA-256 recorded by the manifest:
  `36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4`.
- Repaired source SHA-256:
  `41c06b8536fbf4e1bb2e9979d74de299232379b4b0ebf87ee81e93c63f581017`.
- The implementation receipt was context only and was not used as acceptance
  authority.

## Commands and deterministic results

All Python commands ran from repository root through the root `uv` workspace.

1. `uv run pytest -q projects/xt60-bend-jig/tests/test_p19_r1_front_edge_short_tail.py`
   - PASS, `8/8` focused tests.
2. Independent `uv run python` recomputation over `10,001` uniform shared-`u`
   states:
   - maximum equal/opposite rotation-law error: `0 deg`;
   - maximum left/right world-rod reconstruction residual:
     `7.944109290391274e-15 mm`;
   - maximum fixed-axle reconstruction residual:
     `5.0242958677880805e-15 mm`.
3. Exact inverse-derived outer-rail center travel, mm:
   - left: bottom `3.999999999999628`, diagonal `8.012433561030779`,
     upright `7.864158836933870`;
   - right: bottom `5.944910143797074`, diagonal `10.157688045825534`,
     upright `4.000000000000192`.
   - All six are at or above the declared `4.0 mm` tolerance. The active
     constraints are left/bottom and right/upright.
4. OPEN/END and conditioning:
   - OPEN ordered identity remains `bottom -> diagonal -> upright`, right-angle
     area `147.630669539430 mm2`, and the right leg has `deltaY=0`;
   - END area is `7.105427357601002e-15 mm2`, with maximum accepted endpoint
     displacement `4.440892098500626e-16 mm`;
   - four-contact closure is rank `3`; maximum condition number
     `13.007686517253434 <= 15`.
5. Rail/plate and 65-state actual-solid motion:
   - maximum inverse reconstruction residual:
     `7.105427357601002e-15 mm`;
   - all four plates are single valid solids;
   - minimum actual web `2.405845086139318 mm >= 2.20 mm`;
   - maximum unintended and pre-contact wire intersection: `0 mm3`;
   - minimum XT60 clearance: `3.955249784853697 mm`;
   - exact-contact wire clearance is numeric tangency
     `2.459882262924633e-11 mm`.
6. Two-sided support, cap/axle stack and solder-tool service:
   - 65-state support passes: every normal side supported, every slot end
     closed, every outer support strip continuous;
   - minimum endpoint material ratio `0.9999999999999982`; minimum material
     probe volume `0.100530964914873 mm3`;
   - cap stack passes with three `OD4 x 50 mm` rods, six permanent caps,
     `8.70 mm` engagement per side and `0.30 mm` cap-to-outer gap;
   - the fixed axle is one continuous `34.90 mm` member; principal stack is
     `32.00 mm`; all axle/outer, axle/rod, keeper/outer, keeper/cap and
     XT60/service intersection gates are zero;
   - fixed-axle minimum analytic web is `6.683207005262652 mm` and the rotation
     center has no decorative hole;
   - two solder-tool occurrences pass with keepout beginning `0.75 mm` outside
     the largest rim and maximum production intersection `0 mm3`.
7. Exact AF8.15 actual geometry and diameters:
   - each fixed inner bore uses `_x_hex_prism(8.15, ...)`;
     `RegularPolygon(AF/2, 6, major_radius=False)` makes `AF/2` the apothem,
     so the true across-flats value is `8.15 mm` and circumradius is
     `8.15/sqrt(3)=4.705404693895450 mm`;
   - plate ODs are inner `54.4`, left outer `54.7`, right force outer
     `55.0 mm`; inner clear span is `18.4 mm`.

## Repaired completed-pigtail removal gate

The independent check evaluates the completed pigtail as five finite features
(XT60 body, two solder joints and two bent wires) pairwise against every OPEN
production solid along the exact piecewise-linear path:

```text
(dy,dz,phiX) = (0,0,0)
             -> (-8,10,-5 deg)
             -> (-16,26,-10 deg)
             -> (-16,50,-10 deg)
required clearance >= 0.75 mm
```

- Actual BREP: `41` samples per segment, `123` recorded samples, minimum
  clearance `0.7499999999996648 mm`, maximum intersection `0 mm3`.
- Dense analytic: `1001` samples per segment, `3003` recorded samples,
  minimum clearance `0.7499999999996647 mm`.
- The limiting pair is `bentWire0 :: diagonalRod` at the seated OPEN pose.
- `zeroIntersection=true` and `passes=true`.

The previous validator defect remains an explicit regression fixture. At the
rejected historical pose `(-4,26.84,-15 deg)`, the two individual bent-wire
solids intersect the OPEN diagonal rod by respectively
`47.25940252956725 mm3` and `47.25940236750162 mm3`, with exact distance
`0 mm`. `regressionDetected=true`. This proves the repaired gate can detect
the old real collision instead of hiding it in an aggregate compound.

## Six written STEP gates

For every stem, the validator ran independently:

```text
uv run python <cad-skill>/scripts/inspect validate <written.step>
uv run python <cad-skill>/scripts/inspect refs <written.step> --facts --planes --positioning
uv run python <cad-skill>/scripts/inspect diff <generator.step.py> <written.step>
```

| artifact | valid closed positive-volume leaves | refs facts | source/export diff |
|---|---:|---:|---|
| OPEN | `22/22` | `1515 faces / 4359 edges` | unchanged |
| CONTACT | `22/22` | `1515 / 4359` | unchanged |
| END | `22/22` | `1515 / 4359` | unchanged |
| exploded | `16/16` | `1485 / 4311` | unchanged |
| print kit | `13/13` | `1476 / 4302` | unchanged |
| full motion | `18/18` | `1497 / 4329` | unchanged |

Every refs command reports no warnings/errors. Every diff reports no kind,
topology, geometry or bounding-box change and zero face/edge/shape/size/center
delta.

## Fingerprinted snapshot inspection

The exact three manifest PNGs were inspected at original resolution.

- `p19-r1-impl05-open-front_20260826T182611Z.png`: `RIGHT` view; +Z head is
  up and +Y solder tail/wires exit right. The three rods show the accepted OPEN
  right-angle topology, and the purple fixed axle stays left/behind.
- `p19-r1-impl05-end-front_20260826T182727Z.png`: `RIGHT` view; the three rod
  centers visibly reach the accepted collinear END clamp topology without an
  identity swap.
- `p19-r1-impl05-exploded-iso_20260826T182821Z.png`: one stepped purple axle,
  two inner plates, two outer plates, two keepers, three stainless rods and six
  caps are visible. There is no extra linkage, yoke, gear or stability bar.

The state images are named `front` but explicitly badge the rendered camera as
`RIGHT`. That naming mismatch is non-blocking because the badge is explicit
and the orientation/topology are independently proven; it should not be used
as evidence for a literal front-camera view.

## Acceptance boundary and remaining risks

- Parametric motion, rails, constraints and exact candidate source: **PASS**.
- Actual production solids and repaired completed-pigtail removal: **PASS**.
- Six written STEP artifacts and exact review snapshots: **PASS**.
- Formal independent review: **not performed by this validator**.
- Mesh, 3MF, slicing, printability and physical print/assembly: **not
  performed**.
- PETG rail friction, required hand torque, cap retention variance, rod wobble,
  material flex, self-lock behavior and real soldering ergonomics remain
  physical unknowns. Digital clearance at the limiting removal pair is exactly
  the required `0.75 mm`, so manufacturing/process variation is not an added
  digital margin and must be evaluated physically.
