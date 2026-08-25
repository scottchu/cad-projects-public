# P17 R2 current-lock removal brief

Status: `P17-D08` design contract complete; implementation and independent
candidate gates pending. This is a bounded P17 R2 correction, not a product
version increment.

## Frozen baseline and user evidence

- Baseline commit: `ea416dc2c120f362cdf079b4b82bb8722c58682a`.
- Accepted baseline fingerprint:
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
- Design input manifest: `/tmp/p17-r2-lock-removal-design-input-manifest.txt`,
  SHA-256 `ac8f8dae624cb3291a615a4907ed5a899a35d45819f4aea02d7c93dfa4ada35d`.
- Screenshot 1 SHA-256:
  `b000798579614596fb7cd884b8b0e9ab22f0232d345e5ebb36fac135e18265af`.
- Screenshot 2 SHA-256:
  `49c22de761cad7fdc2aad93a9faea4f91ef4d06de8f1822a5aecf8409675de92`.

The first red circle identifies the orange fork-like integral nose on the
right outer plate. The second red circle instead identifies the green
`left_outer_secondary_grip_block`: an integral finger/force tab on the green
outer plate. It is not part of the lock and remains in this one-at-a-time
iteration.

Source inspection, rather than the second circle, identifies the nose's actual
lock counterpart: the right-inner ground arm, axial bridge, stop, flexure,
ramp, retaining shoulder, and release tab. The user directs that the lock be
removed now, so complete lock removal still requires removing both that
right-inner receiver system and the first screenshot's orange nose. No
replacement lock is designed in this iteration.

## Required outcome

- Remove the complete right-outer lock nose and complete right-inner receiver
  assembly from the production plate solids.
- Remove the lock-only source API, parameters, evidence, tests, manifest
  section, generator, STEP export, and lock-only review evidence. Do not leave
  dead production geometry that could be mistaken for an active lock.
- Preserve the open-to-`32 deg` counter-twist path. Its endpoint is a travel
  end only; it is not a detent, hard stop, over-center capture, or self-lock.
- Do not add a replacement catch, stop, bridge, bar, yoke, boss, linkage,
  frame, or other stability structure.
- Keep P17 R2. Removal of one rejected feature inside the same architecture is
  an iteration repair, not a product version change.

## Axle and stainless-rod clarification

The purchased stainless stock and the purple printed axle are different
members with different axial jobs:

- Physical stainless rods measured/specified by the user are `50.00 mm` long.
- The accepted baseline currently re-derives its modeled white-rod target as
  `40.60 mm`; whether to preserve uncut `50.00 mm` stock remains a separate,
  unresolved rod-length decision and is frozen out of this lock-removal task.
- The purple printed stepped axle is `34.90 mm`: `32.00 mm` principal four-
  plate stack plus `1.45 mm` beyond each outer plate for keeper running
  clearance and the retained keeper seat. It does not need to reach the
  stainless-rod caps and is not made longer by this repair.

This contract does not claim the purple axle length, keeper retention, or the
white-rod length is physically accepted. It only prevents the two dimensions
from being confused while the lock is removed.

## Frozen geometry and behavior

- purple one-piece stepped axle length, cross sections, off-center datum
  `A=(-29.00,17.00)`, keepers, and fixed-inner hex bores;
- outer rotation datum `C=(-10.60,17.00)` and `0..32 deg` travel;
- fixed inner and moving outer roles, with equal-magnitude opposite-sign
  outer rotation;
- inner and outer plate diameters, thicknesses, stack, clearances, completed-
  pigtail windows, larger right force side, and the green left-secondary
  finger/force grip tab shown in screenshot 2;
- all three stainless-rod paths, diameter, current source length decision,
  caps, follower geometry, fixed guide slots, outer cam slots, and guide
  equations;
- XT60 and wire/service reference envelopes;
- no new part and no attempt to repair physical fit, force, or constraint
  architecture.

## Acceptance boundary

This iteration may establish only that the current lock geometry and its dead
production API/evidence are gone while the frozen mechanism remains
geometrically unchanged. It cannot establish a locked state, wire-holding
force, keeper/cap fit, physical rotation constraint, PETG behavior, or safe
soldering use.
