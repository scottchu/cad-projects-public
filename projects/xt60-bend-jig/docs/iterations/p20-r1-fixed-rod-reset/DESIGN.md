# P20 R1 fixed-rod reset analytic design gate

Date: `2026-08-26`

Status: **BLOCKED AT CHEAP TOPOLOGY/COLLISION GATE; NO IMPLEMENTATION
CANDIDATE.** The centered-equivalent transform is mathematically feasible,
but the frozen P19 axial stack makes removal of all six outer white-rod rails
physically contradictory with retaining the three uncut rods and solid outer
plates. No P20 source, tests, BREP, STEP, Viewer, mesh, slicer, or print work is
authorized by this result.

Owner/role: `/root/p20_mechanism_design`, mechanism designer and analytic
owner only. This role did not implement or approve CAD.

## Provenance and scope

- Frozen design input:
  `DESIGN_INPUT_MANIFEST.sha256`, SHA-256
  `b26fcf469f3c06c30d89896d91b262c3b0eaeb650a5c00a9d562fd4177b1633b`.
- Verification: all `14` declared path-and-content entries matched, including
  the two `git:b69b6ad...` snapshots.
- Product baseline: merged P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Coordinate convention: millimetres in physical FRONT YZ; `+Z` is
  mating-head/up, `+Y` is short-tail/tool/outward-right, and the rod/plate
  stack runs along X.
- Allowed output was analytic design evidence only. P19/P20 source, tests,
  generators, solids and exports were not edited or generated.

## Candidate datum A (design choice, not a force claim)

The old P19 datums are `C=(0,0)` and `A_old=(-13,-9)`. The user requires both
coordinates of the fixed axle to move strictly lower-left, but supplies no
measured force/torque target. Therefore force performance cannot select a
numeric optimum.

For this gate the smallest responsible displacement is declared as one P19
white-rod radius (`2.00 mm`) in **each** required direction. This avoids a
sub-feature-size/false-precision move while remaining the least displacement
on that physically named grid:

```text
r_rod = OD4.00 / 2 = 2.00 mm
A = A_old + (-r_rod, -r_rod) = (-15.00, -11.00) mm
|A_old-C| = 15.811388 mm
|A-C|     = 18.601075 mm  (+17.6435%)
```

This is a user-confirmable coordinate for the otherwise feasible transform;
it does **not** claim that hand force, torque or “rotation power” is sufficient.
The topology blocker below prevents this coordinate from becoming an
implementation candidate under the current contract.

### Boundary, bore-web and retained-inner-track checks

The inner keyed bore has AF `8.15 mm`; its conservative containing-circle
radius is `8.15/sqrt(3)=4.705405 mm`. The centered-equivalent outer guide is
one round OD `7.90 mm` bore, radius `3.95 mm`. Conservative rim web is
`plate_radius - |A-C| - cutter_radius` and is state-invariant because the bore
and plate body share the same reauthored outer frame.

| feature | conservative web | gate |
|---|---:|---:|
| OD54.40 inner plate to AF8.15 keyed bore | `3.893520 mm` | `>=2.20`, PASS |
| OD54.70 left outer to OD7.90 round guide | `4.798925 mm` | `>=2.20`, PASS |
| OD55.00 right outer to OD7.90 round guide | `4.948925 mm` | `>=2.20`, PASS |

For each retained inner OD4.15 track, the conservative clearance is the
minimum point-to-segment distance from `A`, less the keyed-bore containing
radius `4.705405` and track radius `2.075`.

| retained P19 inner track | nearest centerline distance | location | conservative clear web |
|---|---:|---|---:|
| bottom | `29.000000 mm` | OPEN endpoint `(5,10)` | `22.219595 mm` |
| diagonal | `33.539988 mm` | END endpoint `(15.802212,2.272322)` | `26.759583 mm` |
| upright | `35.447124 mm` | OPEN endpoint `(20.4,-9.172814)` | `28.666719 mm` |

Thus `A=(-15,-11)` passes the cheap datum/boundary checks. Exact polygonal
BREP web was intentionally not run because the later topology gate fails.

## Centered-equivalent fixed-axle transform

Let side sign `sigma_left=-1`, `sigma_right=+1`, normalized state
`u in [0,1]`, and

```text
alpha_s(u) = sigma_s * 45 deg * u
```

To be **identical to a center-pivot reference**, the outer-plate frame must be
reauthored with world origin at the stationary axle datum `A`. For a local
point `q` and world point `x`:

```text
T_s(q,u)     = A + R(alpha_s(u)) q
T_s^-1(x,u)  = R(-alpha_s(u)) (x-A)
```

The fixed axle world center is `x=A`, hence

```text
q_axle,s(u) = T_s^-1(A,u) = R(-alpha_s(u)) (A-A) = (0,0)
```

for both sides and all states. Therefore both guide-center loci are the same
singleton `{(0,0)}`: one constant OD7.90 round journal bore, exactly as for a
center pivot. It is not an arc and is not a translated P19 guide.

The inverse/round-trip identities hold exactly:

```text
T_s(T_s^-1(x,u),u) = A + R(alpha)R(-alpha)(x-A) = x
T_s^-1(T_s(q,u),u) = R(-alpha)R(alpha)q = q
```

World reconstruction is stationary:

```text
T_s(q_axle,s(u),u) = T_s(0,u) = A.
```

If the old `C`-origin outer frame were retained, its guide would instead be
`R(-alpha_s(u))(A-C)`, an arc of nonzero radius `|A-C|=18.601075 mm`. That
cannot be identical to a center-pivot guide unless `A=C`. Merely translating
or redrawing the P19 arc therefore fails the stated equivalence.

To preserve the physical plate body at OPEN while reauthoring its frame, its
local disk center is `C-A=(15,11)`. Its world center is

```text
D_s(u) = A + R(alpha_s(u))(C-A).
```

| side/state | alpha | world plate-body center `D_s=(Y,Z)` |
|---|---:|---:|
| both OPEN | `0 deg` | `(0.000000,0.000000)` |
| left mid | `-22.5 deg` | `(3.067711,-6.577577)` |
| left END | `-45 deg` | `(3.384776,-13.828427)` |
| right mid | `+22.5 deg` | `(-5.351325,4.902926)` |
| right END | `+45 deg` | `(-12.171573,7.384776)` |

The axle and both inner plates remain world-fixed. The left/right END angles
are `-45/+45 deg`, exactly `90 deg` relative twist.

## Removed-versus-retained topology

| object/path | P20 requested disposition |
|---|---|
| left outer bottom/diagonal/upright rod rails | remove all 3 |
| right outer bottom/diagonal/upright rod rails | remove all 3 |
| left inner bottom/diagonal/upright tracks | retain all 3 unchanged |
| right inner bottom/diagonal/upright tracks | retain all 3 unchanged |
| three white rods | retain P19 OD4.00 x 50.00 and OPEN/END world paths |
| six permanent caps | retain P19 geometry and axial positions |
| fixed axle guides in outer plates | replace P19 arcs with identical constant round journals at local `(0,0)` |

## Authoritative axial-stack collision gate

The P19 formulas give the exact principal stack below. All intervals are X in
millimetres.

| occurrence | X interval |
|---|---:|
| OD4 x 50 rod (each of 3) | `[-25.00,+25.00]` |
| left cap | `[-25.35,-16.30]` |
| left outer plate, thickness 3.20 | `[-16.00,-12.80]` |
| left 0.40 running gap | `[-12.80,-12.40]` |
| left inner plate, thickness 3.20 | `[-12.40,-9.20]` |
| XT60/central clear span | `[-9.20,+9.20]` |
| right inner plate, thickness 3.20 | `[+9.20,+12.40]` |
| right 0.40 running gap | `[+12.40,+12.80]` |
| right outer plate, thickness 3.20 | `[+12.80,+16.00]` |
| right cap | `[+16.30,+25.35]` |

Each rod spans both outer-plate slabs. At OPEN the three P19 rod centers are
inside the complete OD54.70/55.00 outer disks. After subtracting the rod
radius, the minimum full-section margin to an outer rim is still positive:

| rod at OPEN | radial distance from C | left full-section rim margin | right full-section rim margin |
|---|---:|---:|---:|
| bottom `(5,10)` | `11.180340 mm` | `14.169660 mm` | `14.319660 mm` |
| diagonal `(20.4,10)` | `22.719155 mm` | `2.630845 mm` | `2.780845 mm` |
| upright `(20.4,-9.172814)` | `22.367399 mm` | `2.982601 mm` | `3.132601 mm` |

The new axle bore is remote from these centers, and by contract there is no
other outer rod aperture. Consequently each rod/outer-plate pair contains a
full OD4 cylinder slice through `3.20 mm` thickness:

```text
V_pair = pi * (2.00 mm)^2 * 3.20 mm = 40.212386 mm^3
6 pairs = 241.274316 mm^3 at OPEN
```

This is an unavoidable actual-topology intersection, not a sampling,
tolerance or visual-interpretation issue. OPEN alone disproves the candidate;
a motion sweep cannot repair an already-invalid required state. Moving `A` in
YZ does not change the rods' overlap with the frozen X slabs.

**Collision/topology disposition: BLOCKED.** Per `P20-CON-06`, no BREP,
STEP/export, Viewer or downstream implementation evidence was produced.

## 2D user gate

- Deterministic vector authority:
  `docs/review/p20-r1-fixed-rod-reset/p20-r1-fixed-rod-reset-2d-gate.svg`.
- Rendered delivery copy:
  `docs/review/p20-r1-fixed-rod-reset/p20-r1-fixed-rod-reset-2d-gate.png`.
- The diagram shows FRONT-YZ `C`, old/new `A`, retained inner tracks, removed
  outer tracks, OPEN rods, the centered-equivalent OPEN/mid/END motion, the
  exact axial stack, and the OPEN collision blocker.

## Requirement coverage

| requirement | result | evidence / reason |
|---|---|---|
| P20-REQ-01 | PASS | exact P19 baseline pinned and 14-entry input manifest verified |
| P20-REQ-02 | BLOCKER | deleting all six rails leaves six solid-plate rod collisions at OPEN |
| P20-REQ-03 | PASS analytically | retained inner paths unchanged; candidate bore clear web `>=22.219595 mm` |
| P20-REQ-04 | PASS as design coordinate only | candidate `A=(-15,-11)` is strictly farther lower-left and passes conservative web |
| P20-REQ-05 | PASS mathematically | `alpha_left=-45u`, `alpha_right=+45u`, fixed A/inners; relative END `90 deg` |
| P20-REQ-06 | PASS mathematically | one transform and exact round-trip; both guide loci identical `{0}` |
| P20-REQ-07 | BLOCKER | uncut rods plus frozen four-plate X stack contradict solid outer plates |
| P20-REQ-08 | BLOCKER | resolving collision requires changing a currently frozen object/topology |
| P20-REQ-09 | PASS stop condition | stopped before implementation and all downstream artifacts |

`P20-CON-01/02` are defined and analytically satisfied. `P20-CON-03/04/05`
cannot advance to source, actual-solid or export evidence because the cheaper
collision gate failed. `P20-CON-06` is satisfied by stopping.

## Physical unknowns and next decision

Hand torque/force, friction, wedging, backlash, PETG fit/strength, heat, wear,
keeper/cap retention and real soldering usability remain untested physical
unknowns. The `+17.6435%` axle eccentricity increase is geometric only and is
not evidence of adequate rotation power.

Implementation remains blocked until the user explicitly reopens at least one
of these frozen constraints: allow non-guiding clearance apertures/windows in
the outer plates, shorten or axially relocate the rods/caps, move the outer
plates outside the rod span, or change the rod/plate topology. The smallest
single-object reopening to investigate first would be **non-guiding outer-plate
clearance apertures**, but that is forbidden by the present delta mask and is
not designed or authorized here.

## P20-DESIGN-01 receipt

- Status: `BLOCKED`, as required by the failed cheap gate.
- Verified fingerprint: input manifest SHA-256
  `b26fcf469f3c06c30d89896d91b262c3b0eaeb650a5c00a9d562fd4177b1633b`,
  `14/14` entries matched.
- Changed paths: this `DESIGN.md`, the iteration `HANDOFF.md` design section,
  `DESIGN_CANDIDATE.sha256`, and the SVG/PNG review image pair only.
- Deterministic checks actually run: input-manifest verification; P19 formula
  extraction; transform/inverse calculation; datum radius/web and
  point-to-segment track clearance; exact X interval overlap; OPEN full-section
  rim margins and analytic intersection volume; SVG-to-PNG render and visual
  inspection.
- Explicitly not run: P20 source/tests, BREP, STEP, Viewer, snapshot, mesh,
  3MF, slicer, print or physical validation.
- Next action: user chooses whether to keep the strict no-outer-aperture rule
  (ending P20 as infeasible) or authorizes a new topology contract.
