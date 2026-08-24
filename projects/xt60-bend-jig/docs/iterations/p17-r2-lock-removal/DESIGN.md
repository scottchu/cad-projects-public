# P17-D08 complete current-lock removal contract

Status: selected bounded design contract. No source, test, STEP, motion, or
candidate acceptance is claimed by this role.

## Selected design

Subtract nothing new and add nothing new. Restore the two affected plates to
their ordinary guide/cam geometry by removing these authored additions:

1. From `right_outer_primary_actuator`, remove the integral round/fork-like
   lock nose produced by `_lock_nose_local`.
2. From `right_inner_fixed_guide`, remove the complete receiver produced by
   `_lock_receiver_local`, including its ground arm, axial bridge, hard stop,
   stop rib, flexure beam, lead-in ramp, retaining shoulder, and thumb-release
   tab.

No fragment of either feature may remain. Plate solids must still contain all
pre-existing guide slots, axle-guide slots, fixed-inner hex bores, and service
windows. The left outer grip block is not part of the rejected lock and remains
frozen.

## Source and artifact retirement

The implementation must remove, rather than merely stop calling, the obsolete
production lock surface:

- all `lock_nose_*`, `lock_receiver_*`, `lock_contact_*`,
  `lock_over_center_*`, `lock_flexure_*`, `lock_lead_in_*`,
  `lock_thumb_*`, and lock hard-stop parameter fields and validation branches;
- `_lock_*` geometry helpers, `build_lock_nose`, `build_lock_receiver`,
  `build_lock_receiver_component`, `lock_contact_gap_y`,
  `lock_backdrive_evidence`, and their public exports;
- the manifest `lock` object and per-state lock-contact values;
- lock-only assertions/evidence in the focused P17 R2 test file;
- `lock_closeup` from `ArtifactName`, `build_lock_closeup`, and the artifact
  builder map;
- tracked `p17_r2_lock_closeup.step.py` and
  `p17_r2_lock_closeup.step`, plus lock-only review snapshots/provenance
  entries. Viewer/cache derivatives for that retired artifact must not be used
  as current evidence.

The ordinary open, mid, end-of-travel, exploded, print-kit, coupon, focused-
motion, and full-motion outputs remain and must be regenerated from the
changed source. Candidate manifests, fingerprints, provenance, snapshots, and
GIFs must be regenerated rather than patched.

## Endpoint naming decision

Geometry removal and a wholesale source-state rename are separate risks. Keep
the existing Python compatibility keys and filenames `locked`,
`theta_lock_deg`, `GuidePath.locked`, and `p17_r2_locked.step` for this bounded
repair so downstream generation does not acquire an unrelated refactor.

However, the Viewer-facing normalized parameter must be presented as
`open_to_end`, not `open_to_lock`, and labels/manifests/review docs must call
`32 deg` **end-of-travel**. A compatibility alias may parse the old
`open_to_lock` input only if it is not displayed as the active control and
does not create duplicate controls. Existing internal names are legacy
identifiers, not a lock claim.

## Frozen equations and dimensions

The following values and their dependent geometry must be bitwise or
numerically identical to the accepted baseline except where removal of the
lock changes plate volume, bounds, labels, hashes, and connected topology:

```text
inner_clear_span = 18.40 mm
principal_stack_width = 32.00 mm
current modeled rod_length_target = 40.60 mm
center_axle_total_length = 34.90 mm
per_side_center_axle_length = 8.25 mm
C = (-10.60, 17.00) mm
A = (-29.00, 17.00) mm
fixed_axle_eccentricity = 18.40 mm
theta_end = 32.00 deg
alpha_left = -theta
alpha_right = +theta
```

The purple axle length derivation remains:

```text
34.90 = 18.40 + 2 * (3.20 + 0.40 + 3.20 + 0.25 + 1.20)
      = 32.00 + 2 * 1.45
```

The separate current white-rod derivation remains:

```text
40.60 = 32.00 + 2 * 0.30 + 2 * 4.00
```

Physical `50.00 mm` stainless stock is recorded but is not substituted by
this implementation. Doing so would add `4.70 mm` per side relative to the
current centered `40.60 mm` model and requires a later explicit rod/cap-stack
decision.

## Focused acceptance checks

### Object and collision

- Right-inner and right-outer local solids are valid, positive-volume single
  solids after removal.
- All open/mid/end full assemblies have zero unintended intersections at the
  same gates as the baseline.
- At 33 motion samples, axle/outer, keeper/outer, axle/white-rod, keeper/cap,
  and XT60/service intersections remain zero.
- A negative-presence test proves the removed receiver and nose builders,
  labels, manifest data, and artifact cannot be produced.
- Removal must not fill, relocate, or reshape any rod slot, axle guide, hex
  bore, completed-pigtail window, or left grip.

### Math

- Recompute and assert the two derivations above: purple `34.90 mm` and current
  modeled white rod `40.60 mm`; never report either as the other.
- All `GUIDES`, rod reconstruction rows, `A`, `C`, eccentricity, mirror
  relations, and `0..32 deg` trajectory match the accepted baseline within
  `0.05 mm` or the stricter existing tolerance.
- Fixed-axle reconstruction and opposite outer angles remain unchanged.

### Constraints and scope

- Semantic tuples/hashes for axle, keepers, plate dimensions, stack, rod/cap
  parameters, `GUIDES`, service windows, and motion transforms match baseline.
- The only intended production-solid delta is removal of the current right-
  outer nose and right-inner receiver. Volume decreases must be reported for
  those two local plates; left plate volumes must match baseline.
- No new component occurrence or geometry helper replaces the lock.
- The lock-closeup artifact count decreases by one; no stale lock-only output
  is listed in the new provenance.
- Internal compatibility names must be documented as legacy endpoint names;
  the visible motion control is singular and says `open_to_end`.

### User and visual

- New focused and full snapshots must show no orange fork/nose and no inner
  receiver/bridge/catch from the same two review viewpoints or clearer
  equivalents.
- Inspect open, mid, and end-of-travel views plus focused/full motion; neither
  removed feature may reappear at any state.
- The purple axle, both keepers, both inner plates, all three white rods, both
  outer plates, and XT60 reference remain visible in the appropriate full or
  exploded evidence.
- Motion still shows fixed inner plates/axle and counter-rotating outer plates;
  animation is pose evidence only.

## STOP conditions

Stop and return to design if removing the current lock requires any axle,
keeper, plate-diameter, plate-thickness, rod, cap, guide, cam, XT60, service-
window, stack, or motion-path change; if any surviving plate becomes invalid;
if the mechanism needs a replacement hard stop to generate the existing
motion; or if the implementation proposes claiming self-lock after removal.

## Acceptance states

- Design contract: complete.
- CAD/source and written artifacts: pending implementation.
- Independent critique, validation, and formal review: pending.
- Mesh, DfAM, slicer, 3MF, PETG, force, retention, self-lock, heat, wear, and
  physical assembly: not accepted.
