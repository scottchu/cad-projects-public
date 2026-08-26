# P17 compact plate optimizer 2D gate

Status: numeric design candidate frozen for 2D implementation only. No 3D
authorization.

## Outcome

Starting only from the exact current P17 print kit and current P17 guide
geometry, derive compact circular plates in the `50..55 mm` range, retain a
left/behind fixed axle, and lengthen counter-twist travel to `45 deg` while
preserving every invariant in `TASK_INPUT.md`.

## Frozen candidate

- Twist: `45 deg`, left/right outer angles `-45u/+45u deg`.
- Outer rotation datum gauge: `C=(0,0) mm`.
- Rigid placement of the complete current P17 rod plus aligned workpiece set:
  `S=(-14.6869657526,-12.2949747468) mm`.
- Fixed purple axle: `A=(-9.5,-9.5) mm`.
- Analytic minimum envelope for both fixed inner plates: `52.932203 mm`;
  implementation uses the upward-rounded `52.933 mm`.
- Left outer plate diameter: `53.932203 mm`; implementation uses the
  upward-rounded `53.933 mm`.
- Right force-input outer plate diameter: `54.932203 mm`; implementation uses
  the upward-rounded `54.933 mm`.
- The explicit `inner < left outer < right force outer` hierarchy preserves
  canonical `REQ-012`; the two outer increments are design clearance and force-
  side hierarchy, not a change to the analytic inner envelope.
- Minimum internal feature web: `2.59773248 mm`.
- Boundary web: exactly `2.20 mm` at the analytic inner envelope before upward
  rounding; both outer plates exceed the same gate.

This candidate was computed by design owner
`/root/compact_optimizer_design_recovery` against design-input manifest
`293a0b4cc271e3db9ec1596ffa6f8edaf026897976c65d51fc1bef5decb6e135`.

## Position check

After the authorized workpiece-reference alignment and rigid placement, XT60
body center is `Y=-5.0 mm`. Fixed axle `A_y=-9.5 mm` is therefore `4.5 mm`
left/behind it. Rod endpoint Z span is `-18.9853..+7.5 mm`, midpoint
`-5.7426 mm`; `A_z=-9.5 mm` is within the compact central band.

## Gate

The next artifact is a deterministic 2D FRONT OPEN/END diagram only. It must
show the exact candidate and frozen topology clearly enough for user approval.
Do not alter or generate 3D CAD before that approval.
