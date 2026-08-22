# P11 — asymmetric three-rod XT60 soldering jig

P11 is a new task-specific successor to P10. P10 remains frozen as the
validated generic four-disc motion baseline. P11 keeps the same purchased
hardware concept — four side plates, one shared rotary input, and exactly
three stainless rods — but assigns the rods different jobs and different
motion laws.

P11 is a mechanism-validation prototype. CAD may prove nominal geometry,
kinematics, access envelopes, and disassembly paths. It does not prove printed
fit, detent force, wire deformation, springback, heat resistance, or real
soldering ergonomics.

## Coordinate system and workpiece

- Units are millimetres.
- Rod axes run along X. The 90-degree wire path lies in YZ. +Y points from the
  bend toward the ESC pads and +Z is upward toward the XT60.
- Two nominal 12 AWG leads have diameter `4.30` and X centres `-4.0,+4.0`.
- Bend centreline radius `R = 6.0`, parameter range `5.0..7.0`.
- Horizontal wire centreline is `Z=30.0`; the arc ends vertical at
  `(Y,Z)=(0,36.0)` for the default R6 path.
- `D1` is defined precisely as the straight vertical centreline distance from
  the top arc tangent to the XT60 solder-cup/wire-entry plane. Default
  `D1=7.0`; supported design range `6.0..8.0`.
- Default wire entry is therefore `Z=43.0`. The assumed XT60 cup begins there
  and the plastic body begins `5.0 mm` higher. Freeze the existing assumed
  cup envelope as two `3.0 mm` diameter x `5.0 mm` cylinders at X `-4,+4`,
  Y `0`; freeze the plastic body envelope as `15.9 x 8.1 x 20.5`. The
  connector remains an adjustable assumed envelope, not an exact
  purchased-part model.
- The closed workpiece has exact horizontal and vertical tangents with included
  angle `90.0 degrees`.

## Purchased rods and role-specific closure

- Exactly three purchased 304 stainless rods, each `4.0 x 50.0`.
- Preserve the accepted default-R6 closed contact centres:
  - `upright_forming = (-4.15,42.00)` in YZ;
  - `bottom_support = (12.00,25.85)`;
  - `diagonal_locking = (4.691852455,34.691852455)`.
- For R variants, do not reuse the R6 centres. Let
  `rho=(wire_diameter+rod_diameter)/2`. Derive:
  - upright/forming `(-rho, 30+2R)`;
  - bottom/support `(2R, 30-rho)`;
  - 45-degree arc contact
    `(R-R/sqrt(2), 30+R-R/sqrt(2))`, with diagonal rod centre offset toward
    the arc centre by `(rho/sqrt(2),rho/sqrt(2))`.
  The R6 evaluation must reproduce the three frozen values above within
  `1e-9 mm`; every R variant regenerates its guide and inverse-slot geometry.
- The rods must not share one generic travel law:
  Let `E(s)=3s^2-2s^3` for `s` clamped to `0..1`.
  - upright/forming travel: `5.5 mm` along +Y with
    `fU(theta)=E(theta/20)`, complete by `20 degrees`, then dwell;
  - bottom/support travel: `5.5 mm` along +Z with
    `fB(theta)=E((theta-5)/22)`, complete by `27 degrees`, then dwell;
  - diagonal/locking travel: `11.0 mm` along `(-Y,-Z)/sqrt(2)` with
    `fD(theta)=E(theta/32)`, complete by `32 degrees`, then dwell through lock.
- Total rotary stroke is `0..35 degrees`. `32..35 degrees` is a true endpoint
  dwell with zero rod motion. The exact hard stop is `35 degrees`.
- Contact order, not necessarily motion-start order, is forming -> support ->
  locking. At no earlier stage may the diagonal rod become the workpiece datum.
- The open rod arrangement must permit a straight vertical drop/load sweep of
  the assumed XT60 plastic body and two solder cups plus `3.0 mm` side-view
  clearance. Do not claim a rigid straight-drop sweep for the complete connected
  L-shaped pigtail: its horizontal leg necessarily crosses the current open
  diagonal rod. The real leads are flexible and their one-handed routing is a
  physical loading test, not a CAD-proven rigid-body motion.

## Four compact side plates and anti-binding constraint strategy

- Exactly four principal circular plates: fixed guide plus rotating cam on the
  left, and fixed follower plus rotating follower cam on the right.
- Default plate outside diameter `56.0`; no principal plate may exceed it.
- Fixed plate thickness `2.8`; cam thickness `2.5`; axial running gap `0.30`.
- Clear central X span `26.0`; complete four-plate axial body must be
  `<=38.0` and remain inside the `50 mm` rod ends.
- Shared shaft default datum `(Y,Z)=(-5.0,29.0)`, nominal diameter `6.0` in a
  printable fit-coupon-selected bore. Source must recompute slot paths about
  this shaft; it must not reuse P10's inverse-slot coordinates.
- Each fixed plate has three straight, role-specific guide slots. Each cam has
  three independently calculated inverse slots from the P11 motion laws.
- Left/datum-side guide nominal width `4.4`. Left cam motion lane nominal width
  `4.8` in the open/mid region, tapering to a `4.4` locked lane by shaft angle
  `24 degrees`; the final lane remains `4.4` through the 32..35-degree dwell so
  a wider overlapping cutter cannot swallow the locked endpoint datum.
- Right/follower guide nominal width `4.9`; right cam lane nominal width `5.0`.
  Right slots support the rod but do not establish the locked YZ datum.
- Fit coupon trials must include datum widths `4.3,4.4,4.5` and follower widths
  `4.8,5.0` before the full mechanism is printed.
- Model left/right construction offset of at least `+/-0.25 mm`; rods must
  remain assemblable without solid overlap, and worst-case locked contact-height
  difference across the two 8 mm-spaced wires must be `<=0.20 mm`.
- Interpret this as right/follower slot-path construction error while the shaft
  bore and plate body datums remain fixed. Instantiate actual right guide/cam
  cutter variants at all `(+/-0.25,0)`, `(0,+/-0.25)`, and diagonal
  `(+/-0.25,+/-0.25)` YZ offsets. At dense full-stroke poses, nominal straight
  rods must have zero BREP overlap with every offset follower plate. Scalar
  clearance arithmetic alone is insufficient.
- Minimum material web in locked load paths is `3.0`. Low-load open slot ends
  may reduce to `2.4` only when explicitly measured and tested.
- Static cam-slot web is the minimum over independent path parameters
  `min(theta,phi)`, not only centres evaluated at the same shaft angle.
- Full circular blanks are acceptable for this prototype; do not add decorative
  windows, gears, worm screws, towers, cages, or an enclosure. Compactness comes
  first from the smaller OD, thinner stack, and removal of unrelated features.

## One-action OPEN / LOCK interface

- No separate screw adjustment and no translated lock pin.
- The right fixed/cam pair carries one integral printed leaf detent with two
  indexed states: OPEN at `0 degrees` and LOCK at `35 degrees`.
- An integral hard stop must be clear at `34.99 degrees`, tangent at exactly
  `35.00`, and positively overlap at `35.01` and `36.0` degrees.
- The `32..35 degree` dwell prevents the detent from changing rod position.
- Model geometry must prevent more than `1 degree` closed overtravel. Detent
  force, tactile quality, and 100-cycle fatigue are physical tests.
- The operating tab stays below/outside the XT60 and solder-access envelopes.
- Hard-stop pins/tabs must have zero intersection with every rod for R5, R6,
  and R7 over the complete 0..35-degree stroke, including the R7 OPEN pose.

## Base, soldering access, and operation

- Use one compact base with a flat external bench-clamp land. The base fixes
  both guide plates and must not squeeze either cam.
- Guide tongues use minimal integral crush ribs for a selected removable
  interference fit. Tests must distinguish raw/as-printed interference from a
  zero-overlap seated envelope and document a physical pull-out-force gate.
- The shared keyed shaft inserts from the right through all four plates. Its
  right head is integral; its left end remains small enough to pass every bore
  and receives a separate removable C-keeper after insertion. A rigid oversized
  feature is not allowed at both shaft ends. Prove the complete insertion sweep.
- Do not carry P10's tall removable locator into P11. The mechanism prototype
  is loaded directly against the ESC/pad references: place stripped ends on the
  pads, seat the pigtail into the open rod triangle, then rotate once to LOCK.
- Required nominal UX after the base is bench-clamped:
  `OPEN -> drop pigtail -> rotate to LOCK -> solder -> cool -> rotate OPEN`.
- Model the bottom ESC and the upper FC; do not omit or relocate the FC merely
  to make an access test pass.
- Model two separate solder-tip approach envelopes aimed at the pad centres.
  Each is a `55 mm` long tapered tool sweep entering from the +Y side at a
  shallow `10 degrees` downward toward the pad. Use a physical three-station
  profile: radius `0.75` at the solder target, radius `2.75` at `8 mm` behind
  the target, and hand-side radius `11.0` at `55 mm`. Small target-specific X
  convergence is allowed so both far handles centre inside the clear plate
  span. Do not substitute a 2.75 mm-radius blunt face at the target.
- The approach sweeps may intersect only their intended pad/solder/conductor
  target. They must have zero intersection with every printed part, all three
  rods, all six rod caps/keepers, the shaft keeper, the XT60 body/cups, the
  opposite insulated wire, and non-target electronics reference bodies.

## Loading and post-solder removal

- Prove the straight vertical XT60 body-and-cups loading sweep in the OPEN pose.
  Explicitly label the flexible-wire loading route as physically unproven.
- First attempt a preferred intact-jig removal after reopening. If the soldered
  ESC attachment makes that impossible, retain an explicit fallback sequence:
  remove the three right keepers, withdraw all rods toward -X with left caps,
  and translate the base/four-plate/shaft core toward -Y.
- Continuous swept BREP volumes, not pose samples alone, must prove every rigid
  removal phase. Sampled intermediate poses remain regression evidence.
- If intact OPEN removal fails, preserve an explicit swept BREP that intersects
  the fixed pigtail and labels the first blocking member. This is a documented
  failed attempt, not an omitted path.
- Right rod keepers are compact `Ø7.0 x 2.9 mm` circular C-clips with a
  `4.10 mm` bore and +Y-open throat; the round outside removes the previous
  square visual/material envelope while retaining side removal. They therefore
  remove toward `-Y`.
  Their own-rod snap/escape sweeps must be checked; a +Y removal pose is invalid.

## Source and outputs

- Authoritative source:
  `src/xt60_bend_jig/p11_asymmetric_three_rod_solder_jig.py`.
- Tests:
  `tests/test_p11_asymmetric_three_rod_solder_jig.py`.
- Generated outputs live only under
  `cad/p11_asymmetric_three_rod_solder_jig/` and must include:
  - `p11_loaded_open.step`;
  - `p11_loaded_closed.step`;
  - `p11_solder_access.step`;
  - `p11_rods_withdrawn.step`;
  - `p11_removal_clear.step`;
  - `p11_exploded.step`;
  - `p11_print_kit.step`;
  - `p11_fit_coupon.step`.
- Preserve every P10 source, test, document, and artifact unchanged.
- Use the project uv environment. Python/build123d source is authoritative;
  generated STEP files are derived artifacts.

## CAD acceptance

- Exactly three `4 x 50` rod solids and four principal circular plates.
- `D1=7.0` by default and parameter checks over `6..8`; R6 default and checks
  over `5..7`; connected wire/cup geometry has no gap or positive overlap.
- Exact 90-degree closed tangent relationship, endpoint residual `<=0.05 mm`,
  and zero rod/workpiece positive overlap at all accepted poses.
- Dense kinematic sampling proves monotonic role-specific travel, ordered
  completion, and exact `32..35 degree` dwell.
- Inverse-slot reconstruction residual `<=0.02 mm` on both sides.
- Open XT60 body-and-cups loading sweep clearance `>=3.0 mm` in side view and
  zero BREP intersection in the full assembly. No equivalent claim is allowed
  for a rigid connected L-wire sweep.
- Locked datum/follower misalignment test passes `+/-0.25 mm`; contact-height
  delta across the wire pair remains `<=0.20 mm`.
- Actual BREP rod/plate checks pass every frozen follower-slot offset variant;
  nominal static slot web uses the independent-parameter minimum.
- Two solder tool sweeps pass the strict obstacle list.
- Detent/stop endpoint tests cover `34.99,35.00,35.01,36.0 degrees`.
- Stop hardware remains clear of all R5/R6/R7 rod sweeps.
- Shaft insertion and left C-keeper installation are geometrically possible;
  no shaft has two rigid oversized ends.
- Complete axial body `<=38.0`; all printed geometry remains inside the rod-end
  planes except intentionally removable external caps/keepers/operating tab.
- All eight STEP outputs pass `inspect refs --facts --planes --positioning` and
  `inspect validate`, plus source/export label, bounding-box, volume, and BREP
  parity for functional children.
- Mandatory multi-view snapshots include open loading, closed, solder approach,
  follower-side detail, exploded, removal-clear, print kit, and fit coupon.
- Independent review must report no remaining actionable CAD/proof finding.

## Physical acceptance boundary

Print the fit coupon first. Physical tests must then establish:

- selected slot widths on the actual printer/material and no four-plane bind;
- open/lock torque, detent holding force, tactile release, and 100 cycles;
- rod/cap/keeper retention and endplay;
- loaded connector/pad repeatability and resistance to light iron contact;
- real iron access with the actual frame and ESC stack;
- PETG/ASA stiffness and local heat response;
- 12/14 AWG bend formation, springback, insulation damage, and final angle;
- complete post-solder removal without stressing pads or solder joints.
