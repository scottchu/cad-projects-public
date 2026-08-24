# P17-D07 fixed stepped-axle datum repair contract

Status: selected focused datum repair contract; no source, tests, STEP, or
motion artifact has been accepted by this role. D07 supersedes only D06's
provisional `A=(-18.00,17.00) mm`.

## Selected interpretation

Keep the intended outer rotation center and all existing white-rod kinematics
at the current world datum

```text
C = outer_rotation_center_yz = (-10.60, 17.00) mm
```

Move the fixed purple stepped axle farther behind the XT60 to

```text
A = fixed_stepped_axle_yz = (-29.00, 17.00) mm
d = A - C = (-18.40, 0.00) mm
e = |d| = 18.40 mm
```

The inner plate outlines remain centered at `C`, but their hex axle bores move
to `A`; axle, hex bores, inner plates, and keepers are fixed in world. Outer
plate outlines remain centered and rotate about `C`. This makes the axle
visibly eccentric without moving the already-derived white-rod cam system or
lock datum.

`C` and all frozen features remain unchanged. D06's provisional `A` failed
actual-solid collision and web checks. The D07 `A` is a design default selected
from the feasible region below and remains subject to independent candidate
validation.

## D07 datum search and selection

At D06 `A=(-18.00,17.00)`, the inner hex cutter intersected the frozen upright
guide by `68.3212367 mm^3`; left/right outer axle guides intersected the frozen
upright cams by `34.0035540/128.9744351 mm^3`. Signed webs were
`-3.915/-2.195/-5.042 mm` against `+2.20 mm` required. This is a local datum
failure, not a mechanism-identity failure.

With `C`, plate sizes, and every frozen feature held fixed, a numeric scan over
`A_y=-26..-32 mm` at `A_z=16,17,18 mm` found the strongest same-Z region near
`A_y=-29 mm`. At `A_z=17`, sampled minimum analytic web values were:

```text
A_y:  -27.0  -27.5  -28.0  -28.5  -29.0  -29.5  -30.0  -30.5  -31.0
web:   1.935   2.410   2.887   3.367   3.849   3.395   2.895   2.395   1.895
```

Select `A=(-29.00,17.00)`. Exact source-BREP probing gives:

- zero intersection between the inner hex cutter and every frozen guide,
  service window, and receiver; nearest gap `4.1378 mm`;
- zero intersection between either axle-guide cutter and every frozen cam,
  left grip, and right lock nose; global nearest feature gap `3.6500 mm`;
- inner/left-outer/right-outer boundary webs
  `3.8946/7.650/9.150 mm`;
- valid, positive-volume single solids for both inner and both outer local
  plates;
- zero axle/outer, keeper/outer, axle/rod, and keeper/cap intersection across
  33 states;
- `0.150 mm` minimum radial axle/guide clearance, `1.050 mm` keeper radial
  capture, and `19.1764973 mm` sampled minimum XT60/service clearance;
- fixed-axle reconstruction error `<=7.11e-15 mm`, mirror error zero.

## Outer axle-guide loci

For `theta in [0,32 deg]`:

```text
alpha_left(theta)  = -theta
alpha_right(theta) = +theta

q_left(theta)  = R(-alpha_left(theta))  * d = R(+theta) * d
q_right(theta) = R(-alpha_right(theta)) * d = R(-theta) * d
```

At open, both local slots start at `(-18.40, 0.00)`. At locked `32 deg`:

```text
q_left(32)  ~= (-15.604, -9.751) mm
q_right(32) ~= (-15.604, +9.751) mm
```

The two centerlines are mirrors about the local radial `Y` axis. Each is cut
as a continuous capsule-ended sweep with at least 33 samples and width

```text
fixed_axle_guide_slot_width
  = outer_journal_diameter + outer_journal_clearance_diametral
  = 7.60 + 0.30
  = 7.90 mm
```

No endpoint margin is added beyond the capsule radius. The open end blocks
motion in the opposite direction; the locked end is an axle-guide endpoint,
not a replacement for the existing lock.

For every sample and side, validate

```text
reconstructed_A = C + R(alpha_side(theta)) * q_side(theta)
|reconstructed_A - A| <= 0.05 mm
```

and left/right slot-radius error `abs(|q|-18.40) <= 0.05 mm`.

## Part-local geometry changes

`left_inner_fixed_guide` and `right_inner_fixed_guide`:

- keep world transform and outline center at `C`;
- move only the hex bore center from local `(0,0)` to `d=(-18.40,0)`;
- do not move or edit white-rod fixed-guide slots, service windows, or right
  lock receiver.

`stepped_center_axle` and keepers:

- retain all axial segment dimensions and cross sections;
- translate their world `YZ` center from `C` to `A`;
- remain world-invariant in every state.

`left_outer_secondary_cam` and `right_outer_primary_actuator`:

- retain outline centers and rigid-body rotation center at `C`;
- remove the old circular outer-bearing bore at local `(0,0)`;
- cut the side-specific `7.90 mm` axle-guide locus above;
- do not move or regenerate the three existing white-rod cam centerlines;
- preserve the right lock nose and left/right outer sizes unchanged.

No empty central hole at `C` is allowed in the focused D07 artifact. An
integral boss/bore pivot at `C` is not selected by D07 and would require a
later explicit design decision.

## Constraint-closure statement

Planar rigid-body configuration has three degrees of freedom. A fixed circular
pin constrained to the centerline of one slot provides one scalar constraint;
the outer plate still has two free instantaneous degrees of freedom. Therefore:

- the purple axle guide is necessary for the requested eccentric fixed-bar
  interface;
- it is not, by itself, a revolute joint about `C`;
- no drawing, animation, endpoint, or close slot clearance may be used to
  claim otherwise.

The selected smallest closure uses no new part: retain the existing three
white rods, the fixed-inner guide contacts, and the outer cam contacts. Their
geometry/path coordinates are frozen. The full candidate must demonstrate
that these existing contacts and the new axle guide have one mutually
compatible outer pose at each sampled `theta`. At minimum:

1. both outer occurrences use only the prescribed rotation about `C`;
2. every white-rod outer-cam reconstruction remains identical to the P17-I04
   baseline within `0.05 mm`;
3. every fixed-axle guide reconstruction maps to `A` within `0.05 mm`;
4. solving the combined contact residuals from perturbed trial poses returns
   the prescribed pose uniquely within numeric tolerance, or the validator
   records the assembly as underconstrained and blocks acceptance.

The design does not authorize changing white-rod paths to make this proof pass.
If closure fails, return to design before adding a pivot, boss, linkage, or bar.

## Motion-review contract

Create a generated entry `p17_r2_fixed_axle_motion.step.py` whose `gen_step()`
returns the focused open-pose assembly plus a relative path to one self-
contained JS sidecar. The sidecar must not import sibling modules.

One normalized parameter:

| id | min | max | default | meaning |
|---|---:|---:|---:|---|
| `open_to_lock` | `0` | `1` | `0` | `theta = 32 deg * value` |

Viewer update behavior:

- rotate left outer by `-theta` about world X through `C`;
- rotate right outer by `+theta` about world X through `C`;
- do not transform axle, keepers, inner plates, their holes/slots, or XT60
  reference;
- provide play/pause, scrub, reset, loop/ping-pong, and speed controls;
- loop endpoints must not jump.

The focused entry deliberately omits white rods, caps, and lock detail for
visual clarity. It is not collision or closure evidence. A separate full-
assembly open/mid/locked sampled check and at least one full-assembly motion
review must prove the isolation did not hide interference.

## Focused acceptance checks

Object/actual-solid:

- axle and keepers intersect neither outer plate solid outside the intentional
  guide volume nor XT60/service envelopes at open, mid, locked;
- keeper remains axially captured over the entire guide, with minimum radial
  overlap reported; no physical retention claim;
- full assembly has no new unintended intersections caused by moving axle/
  inner bores or cutting the outer guide.

Math:

- `A`, `C`, `e`, slot endpoints, mirror relation, constant radius, and world
  reconstruction meet the equations above;
- axle/inner transforms are bitwise or numerically identical across states;
- left/right outer angles are equal magnitude and opposite sign.

Constraints/scope:

- minimum plate web from guide envelope to outer edge and neighboring frozen
  features is at least `2.20 mm`;
- inner hex-bore minimum web is at least `2.20 mm`;
- exactly one stepped axle, two inner plates, two outer plates, and two keepers
  appear in the focused entry;
- hashes or semantic tuples for `GUIDES`, rod/cap parameters, lock parameters,
  axial stack, and plate dimensions match the P17-I04 baseline;
- no new part, stability bar, yoke, pivot boss, linkage, or frame.

User requirements/visual:

- purple axle is visibly eccentric and farther behind;
- left and right outer axle guides visibly mirror one another;
- motion visibly keeps the axle/inner pair fixed and rotates only the outers in
  opposite directions;
- holes/slots remain part-local and do not slide across their owning plate;
- focused PNGs at `t=0,0.5,1`, one motion GIF, and a full-assembly review are
  inspected after deterministic checks.

## Acceptance boundaries

- Design contract: complete.
- CAD/source: pending `P17-I05` and independent gates.
- Viewer motion: pending; when present it proves only the prescribed poses.
- Mesh/DfAM/slicer/3MF: out of scope.
- Physical fit, friction, keeper retention, force, wear, heat, and self-lock:
  pending and not inferable from D07.
