# P20 R2 fixed-rod curved-rail correction brief

Status: **FIXED-ROD/RAIL ASSEMBLY PRESENCE USER-APPROVED; FROZEN AGAINST THE
NEXT WIRE TASK**

## Required outcome

Correct only the rejected P20 R1 fixed-rod guide interpretation. Use exact P19
product geometry and topology as the baseline, remove the six white-rod outer
rails, preserve the six inner-plate rail cuts, keep the outer plates rotating
about P19 virtual center `C=(0,0)`, and cut one true curved stationary-axle
rotation rail into each outer plate for full physical left `+45 deg` / right
`-45 deg` travel about `C`.

## Coordinate frame and kinematic invariant

- Units are millimetres and degrees.
- Physical FRONT is world YZ: `+Z` is mating-head/up; `+Y` is short-tail,
  tool-approach, right/outward.
- The purple stepped axle lies along X and is fixed in world at
  `A=(-15,-11)` unless the design gate falsifies that witness.
- Both inner plates remain fixed and keep the P19 white-rod rail paths.
- P19 virtual outer-plate rotation center remains `C=(0,0)`.
- One normalized state `u in [0,1]` gives physical outer-plate rotations
  `alpha_left(u)=+45u deg` and `alpha_right(u)=-45u deg`.
- The required local fixed-axle locus for side `s` is the P19 inverse-frame
  relation
  `q_s(u)=C + R(-alpha_s(u)) * (A-C)`.
- Reconstruction must satisfy
  `C + R(alpha_s(u)) * (q_s(u)-C) = A`
  for both sides at every sampled state within the declared tolerance.
- Because `A != C` and `alpha_s` varies, each `q_s` is a curved arc. A
  constant circle/journal at `A`, a plate rotating about `A`, or a translated
  P19 arc fails this contract.

## Requirements

- `P20R2-REQ-01`: Baseline is exact P19 R1 commit
  `b69b6ad12af611644987f026eef4940db9c7bb34`; P20 R1 is rejected evidence,
  not source authority.
- `P20R2-REQ-02`: Delete exactly three white-rod outer rails per outer plate,
  six total; add no substitute white-rod hole, window, bore, pocket, or slot.
- `P20R2-REQ-03`: Preserve all three P19 white-rod inner rails in each inner
  plate, their identities, geometry, and world paths.
- `P20R2-REQ-04`: Use fixed axle `A=(-15,-11)` unless the pre-BREP analytic
  gate proves it invalid; any different datum requires a new confirmed gate.
- `P20R2-REQ-05`: Preserve `C=(0,0)` as the only physical outer rotation
  center, fixed axle/inner plates, shared state, and exact physical left/right
  `+45/-45 deg` travel.
- `P20R2-REQ-06`: One deterministic pure-math function must derive both
  side-local curved fixed-axle loci using the inverse-frame equation above.
- `P20R2-REQ-07`: Each outer plate contains exactly one curved fixed-axle
  rotation rail that covers its complete side-specific locus and reconstructs
  stationary world `A` throughout motion.
- `P20R2-REQ-08`: Review media must expose both curved fixed-rod rails clearly;
  an opaque face view that hides or makes the rails indistinguishable fails.
- `P20R2-REQ-09`: Preserve P19 orientation, three rod identities, OPEN/END
  world paths, three uncut `OD4 x 50 mm` rods, six caps, four plates, stepped
  axle/keepers, workpiece, wire/cup/tool service, and all unlisted geometry.
- `P20R2-REQ-10`: Preserve and report the six expected rod/solid-outer-plate
  collisions as the known non-product boundary; no other unintended collision
  is allowed.
- `P20R2-REQ-11`: Stop after source, focused tests, STEP, visible snapshots,
  independent critique, validation, and formal review. No white-rod outer
  rail sequencing, mesh, 3MF, slicing, printing, or physical claim.

## Per-object delta mask

| Object | Authorized change | Frozen / forbidden |
|---|---|---|
| Left outer plate | Remove its three white-rod rails; replace rejected round fixed-axle journal with the left inverse-frame curved fixed-axle rail. | Body, OD, thickness, X placement, grip identity, rotation center, new white-rod apertures, or any other cut. |
| Right outer plate | Remove its three white-rod rails; replace rejected round fixed-axle journal with the right inverse-frame curved fixed-axle rail. | Body, OD, thickness, X placement, force-side identity, rotation center, new white-rod apertures, or any other cut. |
| Inner plates | Move only their keyed fixed-axle bore/seat to accepted `A` if required from P19. | Three white-rod inner rail paths, bodies, roles, X positions, or rotation. |
| Purple axle/keepers | Move complete occurrence from P19 `(-13,-9)` to accepted `(-15,-11)`. | Geometry, dimensions, X-axis role, fixed-world state, or conversion to a white rod. |
| White rods/caps | No change. | Rail addition, substitute clearance, reassignment, shortening, relocation, mirroring, or hiding known collisions. |
| Motion law | Endpoint change from P19 to physical left `+45 deg` / right `-45 deg`; local axle locus is the opposite-sign inverse motion about fixed `C`. | Rotation about `A`, independent side states, same-direction motion, moving inner plates/axle, or travel beyond `90 deg` relative. |
| Workpiece/service | No change. | Moving, trimming, or weakening service geometry to clear the corrected rail. |

## 2D intent and analytic gate

Before BREP or STEP work, the design owner must provide a phone-readable FRONT
YZ gate showing `C`, `A`, outer plate boundary, OPEN/mid/END positions of both
side-local curved fixed-axle loci, motion arrows, and a small axial-stack view.
The gate must label the white-rod outer rail count as zero, the retained inner
rail count, and the six known rod/outer-plate collisions. Analytic checks must
cover locus endpoints, determinism, left/right symmetry, inverse
reconstruction, rail sweep width, plate containment/minimum web, and whether
`A=(-15,-11)` remains feasible.

A failed cheap math, web, topology, or required-presence gate stops before
BREP. It does not authorize a journal, changed center, substitute hole, or
white-rod rail.

The user-approved corrected phone gate is
`/tmp/p20_r2_corrected_twist_center_gate.png`, SHA-256
`e2d05a852889bef2e9c97a2e18878b475aef39b690fa884d6db6a1054d1da8d7`.
It supersedes every earlier P20 R2 sign assumption.

## Evidence and acceptance layers

Implementation must separately prove pure math, source geometry, actual-solid
collision census, constraints/web, user-required presence/absence, written
STEP validity and source/export parity, and visible snapshots. Independent
critic, validator, and formal reviewer must use the same frozen candidate.
Digital acceptance cannot promote this known-collision intermediate to a
movable, manufacturable, printable, or physically accepted product.

## Post-implementation user acceptance and immutable next-task boundary

The user explicitly approved the complete P19-based P20 R2 assembly's fixed
purple rod and both curved fixed-rod rails. That approval is limited to their
presence, position, path, and visible assembly relationship; it does not accept
the inherited wire shape or promote the assembly to manufacturing, print, or
physical acceptance.

The following is immutable input to the next wire-only correction and must
never be touched by that task:

- authoritative source:
  `src/xt60_bend_jig/p20_r2_fixed_rod_arc_rail.py`, SHA-256
  `1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73`;
- focused fixed-rail STEP:
  `cad/p20_r2_fixed_rod_arc_rail/p20_r2_fixed_rail_review.step`, SHA-256
  `07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c`;
- complete P19-based assembly STEP:
  `cad/p20_r2_fixed_rod_arc_rail/p20_r2_full_motion.step`, SHA-256
  `715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca`;
- virtual outer center `C=(0,0)` and world-fixed purple axle
  `A=(-15,-11)`;
- physical outer motion: left `+45 deg`, right `-45 deg`;
- OPEN local fixed-axle point on both sides: `q(0)=(-15,-11)`;
- left local END point:
  `qL(1)=(-18.384776310850235,+2.828427124746188)`;
- right local END point:
  `qR(1)=(-2.828427124746192,-18.384776310850235)`;
- exactly two curved `7.90 mm` fixed-axle rails, one in each outer plate; and
- exactly zero white-rod outer rails or substitute apertures.

The inherited P19 diagonal wire reference is separately **USER-REJECTED**.
The next bounded task may correct only the two wire references to the already
established exact 90-degree topology: an exactly vertical leg tangent to an
`R6` quarter-circle arc tangent to an exactly horizontal leg. It may not move,
resize, regenerate differently, or otherwise alter the frozen purple fixed
rod, either fixed-rod rail centerline or cutter, `C`, `A`, outer motion, plate
geometry, or rail count.

This defect escaped earlier review because P19
`build_workpiece_reference()` and its focused tests encoded and asserted an
END-derived diagonal line as the wire reference. Those mutually reinforcing
source/test assumptions contradicted the higher-level functional authority in
`REQ-002` and `REQ-017`, which require a fixed 90-degree wire bend, so passing
the P19 tests did not prove the required wire topology.
