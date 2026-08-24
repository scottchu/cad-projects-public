# P17 R1 counter-twist permanent-caps design record

## Selected smallest falsifiable simulator architecture

Select a four-plate counter-twist simulator with:

- two fixed inner guide plates, grounded to a visible rigid inner frame, that never rotate;
- two larger outer plates that the user grips and counter-rotates;
- one relative twist input, `theta_rel`, with a required physical 1:1 opposite-rotation relationship between the outer plates;
- three straight `OD4.00 x 50.00 mm` rods, each carrying permanent caps on both ends;
- complementary left/right outer cam tracks generated from the actual signed plate rotations, not by sign-flipping an animation of identical geometry;
- a visible grounded detent/hard-stop lock concept that holds the primary outer plate and, through the 1:1 relationship, the secondary outer plate.

This is the smallest simulator change that can falsify the reported architecture failure before any CAD work: if either outer plate rotates the same direction, either inner plate rotates, either rod end no longer coincides with the other end, or the lock/ground path is missing, the simulator is wrong.

## Coordinate and handedness contract

Use the existing simulator's mechanism plane convention: rods run along world `X`; the mechanism cross-section is world `Y/Z`; outer plates rotate about the shared world `X` axis.

Define positive rotation by the right-hand rule about `+X`. Define closing relative twist:

- `theta_rel >= 0` is the user's closing input.
- Left outer plate global rotation: `alpha_left(theta_rel) = -theta_rel / 2`.
- Right outer plate global rotation: `alpha_right(theta_rel) = +theta_rel / 2`.
- Therefore `alpha_right - alpha_left = theta_rel`.
- Looking inward from each exterior face, the two gripped plates visibly counter-twist toward each other; global signs differ because the exterior viewpoints are opposite.

For a simulator readout, show one `theta_rel` control rather than independent left/right sliders. Independent phase error may be exposed only as a validation/debug mode and must default to zero.

## Provisional digital choices

These numbers are simulator design choices only. They are not CAD acceptance, print acceptance, or physical force proof.

| Choice | Value | Rationale |
|---|---:|---|
| Open relative twist | `0 deg` | Rods retracted/open. |
| First-contact relative twist | `44 deg` | Corresponds to about `22 deg` on each outer plate, preserving the prior P13 contact intuition while changing the architecture. |
| Closed/lock relative twist | `54 deg` | Corresponds to about `27 deg` on each outer plate, matching the prior P13 locked-pose angle per side without claiming P13 locking proof. |
| Secondary outer plate diameter | `60 mm` | Larger than fixed inner plates and easy to grip visually. |
| Primary force/actuator outer plate diameter | `64 mm` | Slightly larger than the other outer plate and visually obvious. |
| Fixed inner plate diameter | `50 mm` | Smaller than both outer plates while still large enough to show straight guide tracks. |
| Provisional inner clear span | `18.5 mm` | Reduces P13's `26.2 mm` inner span surplus around the `15.9 mm` XT60 body to a visible simulator target of `2.6 mm` total clearance. |
| Provisional principal stack | about `35 mm` | Leaves visible rod protrusion from `50 mm` rods for permanent caps while reducing the P13 `37.4 mm` stack. |

The implementation may adjust purely visual dimensions if browser layout requires it, but it must preserve the hierarchy `primary outer > secondary outer > inner` and keep the inner-span surplus visibly reduced from P13.

## Complementary slot math and invariants

For each rod `i`, define a world straight-guide path on the fixed inner plates:

```text
p_i(theta_rel) = p_open_i + s(theta_rel) * d_i
```

where `d_i` is the rod's fixed guide direction in the `Y/Z` plane and `s(theta_rel)` is the shared monotonic scalar travel. The two inner plates carry identical grounded straight slots on those world lines.

Let `C` be the common plate-axis center in the `Y/Z` plane. Let `R(a)` rotate a `Y/Z` vector by angle `a` about world `X`. For side `sigma`, with `sigma = -1` for left and `sigma = +1` for right:

```text
alpha_sigma(theta_rel) = sigma * theta_rel / 2
q_i_sigma(theta_rel) = R(-alpha_sigma(theta_rel)) * (p_i(theta_rel) - C)
```

`q_i_sigma` is the local slot centerline to draw in the corresponding outer plate. Reconstruction must satisfy:

```text
C + R(alpha_left(theta_rel)) * q_i_left(theta_rel)  == p_i(theta_rel)
C + R(alpha_right(theta_rel)) * q_i_right(theta_rel) == p_i(theta_rel)
left_rod_end_i(theta_rel) == right_rod_end_i(theta_rel) == p_i(theta_rel)
rod_skew_i(theta_rel) == 0
```

This means the left and right cam tracks are complementary. They may look mirrored, but they are generated from their own signed plate rotations. Reusing one slot path and merely rotating a visual copy with the opposite sign is forbidden unless the math above independently proves both side reconstructions.

Required simulator invariants:

- two inner plates have `rotation = 0` for every state;
- left and right outer rotations are equal magnitude and opposite sign for every normal state;
- every rod remains straight, with equal left and right `Y/Z` positions and no modeled skew;
- every rod pose lies on its fixed inner guide line;
- common travel is monotonic from open to closed;
- contact and closed states preserve the intended 90-degree wire path as a kinematic target;
- any shown lock freezes `theta_rel` and the two outer rotations without moving the inner plates.

## Ground, reaction, and lock concept

P17 requires a visible ground path. The simulator should show the two inner plates tied by a fixed frame/yoke or equivalent grounded bridge. The reaction path is:

```text
wire load -> three rods -> fixed inner straight slots -> fixed inner plates -> grounded frame/yoke -> user's stationary reaction or bench/fixture
```

The outer plates apply drive forces through their cam tracks into the rod-end followers/caps. The two outer plates must have a stated 1:1 opposite-rotation relationship, shown as a timing link, crossed belt, opposed gear/idler pair, or equivalent future mechanism. The simulator may render this as a schematic timing bridge, but tests must enforce the relationship numerically.

The selected lock concept is a grounded detent plus hard stop on the primary larger outer plate:

- at `theta_rel = 54 deg`, a detent tooth/pawl or notch engages the primary outer plate relative to the grounded inner frame;
- a hard stop defines the end angle and prevents over-travel;
- the 1:1 opposite-rotation relationship transfers that held state to the secondary outer plate;
- unlocking retracts the detent before reopening.

This is a lock concept only. The simulator may demonstrate frozen kinematics and a visible ground path; it cannot prove force capacity, vibration resistance, creep, wear, self-locking, or release effort. A later CAD/physical iteration must provide geometry, actual contact normals, material margins, and print/cycle evidence before claiming a physical lock.

## Permanent cap strategy and fit uncertainty

All six caps are permanent. The simulator and UI must not use "removable right cap", "service cap", or cap removal language.

P13 physical evidence is mixed: four physical caps fit on nominal rods, and two were too tight to push onto the same nominal rods. The current P13 left cap socket was nominally `3.90 mm` on an `OD4.00 mm` rod, or `0.10 mm` diametral interference. That value is not physically proven as a universal permanent-cap fit.

For P17 simulator purposes:

- render six permanent rod-end caps outside the outer plates;
- treat caps as captured/pressed permanent elements, not service elements;
- keep cap fit as a physical unknown;
- require the later CAD design to use a focused cap-fit coupon or parameter ladder before selecting final cap socket, lead-in, split relief, chamfer, or retention features;
- do not prescribe a single rigid interference as accepted.

## Visual affordances

The simulator should make these relationships obvious without explanatory text overlays:

- fixed inner plates use a grounded/frame color and never animate;
- outer plates are visibly larger than the inner plates;
- the primary force/actuator outer plate is slightly larger than the secondary outer plate;
- each outer plate has a grip rim or handhold affordance;
- permanent caps are visible at all six rod ends;
- a timing/opposition indicator connects the two outer plates so the opposite rotation is not perceived as arbitrary animation;
- the lock/detent is visibly grounded to the inner frame, not floating on an outer plate;
- the middle spacing around the XT60 envelope is visibly reduced from P13.

## Focused tests that must fail on wrong implementations

Implementation should add focused tests or assertions with names tied to these defects:

| Failure to catch | Required check |
|---|---|
| Same-direction outer rotation | For sampled `theta_rel`, assert `alpha_left + alpha_right == 0` and `alpha_right - alpha_left == theta_rel`; reject any shared same-direction shaft angle. |
| Inner plate rotation | Assert both inner plate objects are named fixed/grounded and have zero rotation for all rendered states. |
| Rod-end mismatch or skew | For every rod and sampled state, reconstruct both side followers from their side-local slot math and assert equal world `Y/Z` positions and `skew == 0`. |
| Mere animation sign flip | Assert left and right local slot samples are generated from `q_i_sigma(theta_rel)` with opposite signed `alpha`, and reconstruct both side followers through world transforms. |
| Absent ground/reaction path | Static source/browser checks must find a grounded inner frame/yoke, fixed inner guide names, and a lock/detent anchored to ground, not only to rotating geometry. |
| Absent or overclaimed lock | State reducer must freeze `theta_rel` only when locked; UI/readout/docs must state lock concept or pending proof, not physical self-lock acceptance. |
| Wrong diameter hierarchy | Assert `primaryOuterDiameter > secondaryOuterDiameter > innerDiameter`. |
| Removable cap wording | Static checks reject `removable`, `right removable cap`, and cap service wording in P17 simulator UI/source/docs except historical notes. |
| Cap-count regression | Assert exactly six permanent cap visuals attached to rod ends. |
| Excess P13 inner spacing retained | Assert provisional simulator inner clear span is closer to the `15.9 mm` XT60 body than P13's `26.2 mm` span; target surplus `<= 4.0 mm` unless the design contract is reopened. |

## Alternatives considered and rejected

1. Preserve P13 shared D-shaft and flip only the visible right plate animation. Rejected: the user requires real opposite-direction outer plate rotation and forbids mere animation sign flip. P13's same-direction keyed shaft is a conflicting assumption.
2. Keep inner plates visually moving with the cams. Rejected: the user explicitly states the two inner plates are fixed/grounded and do not rotate.
3. Treat one cap socket interference as solved. Rejected: physical P13 evidence has four fitting caps and two too-tight caps on nominal rods; cap fit remains process-variable.
4. Continue with CAD before simulator review. Rejected: user requires simulator-first delivery and no new STEP/3MF until simulator motion is reviewed.
5. Use lock-anywhere shaft brake copy from P13 simulator. Rejected: P17 has no shared same-direction shaft; the lock concept must ground a counter-twist relationship.
6. Make the outer plates equal diameter. Rejected: the primary force/actuator outer plate must be slightly larger and visually obvious.

## Decision promoted to ADR

`ADR-0003` records that P17 supersedes the conflicting P13 assumptions in `ADR-0001`: same-direction synchronized cams, one shared rotary shaft input, removable cap/service wording, and P13 locked-pose sufficiency. P13 remains historical evidence and may remain digitally accepted for its own iteration, but it is not the current architecture for P17.
