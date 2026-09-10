# P20 R4 custom-profile full-CAD handoff

Date: `2026-08-27`

## Current authority

- Candidate fingerprint:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`
  (`30/30`).
- Focused tests: `6/6` passed.
- Formal review SHA-256:
  `96935afda438dc487b1ed68e48140a3364ca1a96a3de10ff2ba93a78610477de`.
- Full-motion source:
  `cad/p20_r4_custom_profile_full_cad/p20_r4_full_motion.step.py`.

## Disposition

Conditional pass for user-facing complete-assembly intent preview only.
Manufacturing and printing fail. Do not generate mesh, slice, upload, or
print from this candidate.

## Open blockers

- Blue rod / XT60 intersection: `186.980487 mm3` OPEN,
  `63.593308 mm3` MID.
- Fixed-axle hex / inner-rim web: `1.152 mm`.
- Left outer Blue-Orange web: `1.715 mm`.
- Rod/workpiece contacts need physical-function classification.
- Caps are unchanged at `9.05 mm`; the `18.40 mm` inner clear span is visible
  but not physically accepted.

## Next action

Wait for the user to inspect the exact full-motion Viewer, exploded view, and
axial-stack snapshot. If the user rejects the Blue/XT60 relationship, open a
new bounded delta mask for that correction only; preserve the exact P20 R4
profile until the user explicitly changes it.
