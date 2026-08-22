# P13 CAD-source-domain certificate amendment

Status: accepted, controlling superseding contract for the current P13 CAD
source. The parent brief retains historical review material; this amendment
controls every conflicting integral-shaft/key-rib clause.

Parent Gate-0 brief: `docs/p13-four-plate-three-rod-brief.md`, SHA256
`9c2102114cbf87ccabaa4388ed3814b91cdf3f8f654c775f5ddd8a5d05272322`.

This amendment explicitly supersedes the parent brief only where the parent
required an integral actuator shaft/local rectangular key. That printable
architecture was rejected because a plate-flat print put the integral shaft
root across layer lines. All four principal plate locations, three forming-rod
paths, workpiece geometry, and OPEN/Rise/LOCK kinematics remain unchanged. It
also separates two claims which the earlier evidence incorrectly allowed to
blur:

- `CAD_SOURCE_DOMAIN_CERTIFIED`: the parametric source geometry and its
  explicitly bounded configuration domain have a complete continuous removal
  certificate.
- `PHYSICAL_RECORD_NOT_INSTANTIATED`: no measured printed/purchased specimen
  record has been supplied, so the parent brief's physical `p_c` acceptance is
  not claimed.
- `MEASURED_SPECIMEN_GEOMETRY_CERTIFIED`: reserved for a future strict
  per-specimen certificate whose complete measured record passes the schema and
  exact-BREP interface. This status is impossible when any required measured
  field or BREP is absent.

## Superseding split-shaft print architecture

- The production mechanism has exactly four circular principal plates, one
  separate printed shallow-D actuator shaft, one removable left C keeper, and
  six rod caps. The three uncut `OD4 x 50 mm` stainless forming rods remain
  purchased parts and are excluded from the production 3MF.
- Both cam plates have matching shallow-D bores and `OD10 x 2.0 mm` outward
  hubs. Each D engagement is `4.50 mm`; the fixed guide stations remain round
  upward-C journals and therefore do not carry a D profile.
- The nominal shaft is `OD5.60 / AF5.15 mm`; both cam bores are
  `OD5.70 / AF5.25 mm`; the reduced fixed-guide journal lands are `OD4.60 mm`
  in `ID4.80 mm` upward-C journals. The hub radial wall is `2.15 mm`.
- A low-profile `OD9.60 x 2.00 mm` stop head retains the right end. The
  existing removable C keeper retains the left. The keeper centre, groove,
  shaft left tip, hubs, and head are derived from named parameters; nominal
  axial endplay is `0.275 mm`.
- The exact D endpoint-to-female-flat contact equation certifies
  `1.9325113632826 deg` one-sided angular lash (`3.8650227265652 deg` total),
  below the active `3 deg` one-sided CAD limit. Actual-solid containment below
  and escape above that contact are regression tested. No physical lash claim
  exists until the PETG coupons are measured.
- Service disassembly is staged and is the only claimed shaft-removal path:
  remove the keeper radially, release both upward-C fixed guides in `-Z`, then
  extract the separate D shaft in `+X` through the two stationary cams. Direct
  `+X` extraction with the fixed guides installed is explicitly inadmissible
  and is retained as a negative actual-solid test.
- The current printability repair keeps `main_face_gap=0.30 mm`, uses fixed
  `OD10 x 0.20 mm` thrust lands, omits zero-height cam lands, and therefore
  preserves exact nominal facing clearance `0.10 mm` on both sides.
- Principal print orientations are exact: left cam `+90 deg Y` with flat inner
  face on the bed/hub up; left fixed `+90 deg Y` with plain face on the bed/land
  up; right fixed `-90 deg Y` with plain face on the bed/land up; right actuator
  `-90 deg Y` with flat inner face on the bed/hub up. Every principal part has
  a large authored planar footprint at `Z=0` and no negative Z. The separate
  shaft prints with its axis parallel to the bed and its D flat down.
  All six rod caps print closed-end-down/socket-up; this preserves the exact
  right-cap P16 4.10 functional core while making no physical-fit claim for the
  unslit left `ID3.90` socket.
  Production 3MF census is exactly 12 objects; the STEP print kit adds two
  diagnostic coupons for exactly 14 occurrences.

## Domain A: exact CAD-source allowance domain

Every variable below is mandatory machine-readable evidence with unit, closed
bounds, correlation/component rule, and provenance.

- `c_sw` is `[0.50,0.75] mm` and `wire_diameter_design` is `[4.20,4.30] mm`.
- normal removal begins at `theta_R=0 deg`.
- `X_fixed_left=[-14.60,-14.40] mm`,
  `X_fixed_right=[14.40,14.60] mm`, and
  `X_keeper=[-21.575,-21.375] mm` for the current derived split-shaft datum.
- `X_cam` is not an independent box: it satisfies
  `X_keeper+1.75 <= X_cam <= X_fixed_left-2.85`, with global projection
  `[-17.75,-17.25] mm`.
- the exact-source left-cam transverse connected component is conservatively
  enclosed by the D-bore circular radial clearance
  `max(0,(cam_d_bore_od-shaft_od)/2)`; D-flat constraints may reduce it but may
  not enlarge it.
- the exact-source fixed-guide transverse components are conservatively
  enclosed by `max(0,(fixed_groove_od-fixed_groove_od)/2)=0`. The projection
  (union across admissible stages) of right-fixed roll is the complete
  periodic `S1`, but its admissibility is stage-correlated and is never an
  independent Cartesian `S1` while any rod journal relation remains true.
- the exact-source keeper connected component is enclosed by
  `max(0,(keeper_id-keeper_groove_od)/2)` and complete keeper roll is retained.
- rod roll, right-cap roll, keeper roll, and right-fixed roll each cover the
  complete `S1=[0,360] deg`. Right-cap geometry is explicitly non-roll-invariant;
  it is removed before the workpiece lift and remains a mandatory Stage-1
  domain/procedure item.
- permanent left-cap engagement and removable right-cap engagement each cover
  `[2.50,3.00] mm`; the former is frozen per specimen and the latter is movable
  before cap removal.
- the source-domain workpiece is the maximum declared insulation envelope;
  smaller admitted wire OD cannot lower its minimum Z.
- source profile/BREP deviation is exactly zero. This is a CAD-source statement,
  not a manufactured-tolerance statement.

### Staged right-fixed-roll union

`alpha_RF=0 deg` is the upward-mouth assembly datum and `u` is synchronous rod
withdrawal in `-X`. The final right-fixed source BREP has inner face
`X=13.10 mm`; the uncut rod tip begins at `X=25.00 mm`. Therefore the exact
support guard is `u_clear=11.90 mm`. Full withdrawal is `44.20 mm` and leaves
`32.30 mm` axial gap.

- D0 operates over `theta=[0,27] deg`, `u=0`, caps installed, all three `J_i`
  true, and `alpha_RF` in the exact-lane-valid component connected to
  `alpha_RF=0`.
- D1 removes the right caps with the same engaged roll constraint.
- D2 covers `0<u<u_clear`, all `J_i` true, continuing the same connected
  component without a component jump.
- D3 begins at `u=u_clear`, where all `J_i` are false, and permits complete
  `alpha_RF in S1` through full withdrawal.
- D4 certifies complete-workpiece `+Z` lift for every `alpha_RF in S1` using
  the full-roll right-fixed swept envelope and the global workpiece proof.
- D5 permits empty/service prealignment over full `S1`.
- D6 removes the keeper and releases the right fixed plate in `-Z` only at
  `alpha_RF=0`, mouth up.

The engaged component is globally enumerated on `S1` by an endpoint-convex
reduction over the continuous OPEN..LOCKED lane traversal and a Lipschitz
interval branch-and-bound classifier. The `0=360 deg` seam is explicit;
samples are diagnostic only. After the rod-clear guard, a conservative coaxial
annular swept BREP covers every right-fixed rotation and is checked against all
remaining structure occurrences and the complete workpiece.

The global workpiece-removal command is an outward-rounded upper bound on

`max(0,Z_mech_top+c_remove_end-Z_payload_min)`

over the complete Domain A. The report contains directed lower/upper bounds,
the attaining parameter corner, a bound width no greater than
`eps_global=0.005 mm`, convergence and domain-coverage flags, and positive
endpoint/continuous-sweep margins. Every REMOVE/sweep artifact and label uses
this same global command; the nominal `P13Parameters.removal_lift` remains only
a regression seed and is forbidden as an acceptance command.

## Domain B: future measured specimen interface

One immutable physical record must identify every printed/purchased exact BREP,
its registration and measurement provenance, production lane/bore/key/journal/
keeper/cap geometry, three exact rod BREPs/end frames/straightness admissions,
completed workpiece and external frame/tool envelopes, fixed left-cap seated
engagements, and every bounded movable-domain component required by the parent
brief. Domain B validation is strict: missing keys, missing BREP paths/hashes,
unbounded intervals, or an uninstantiated connected component fail. A future
per-specimen certificate may report `MEASURED_SPECIMEN_GEOMETRY_CERTIFIED` only
after the complete physical record and exact-BREP global solves pass.

## Dependency evidence

The dependency graph is cross-checked against an AST-derived direct-read and
transitive helper/property call graph. Dynamic `getattr` access to parameters is
forbidden. Independent typed terminal descriptors cover every certificate,
state builder, and STEP export. Removing any actual consumer or typed terminal
effect is a hard failure.
