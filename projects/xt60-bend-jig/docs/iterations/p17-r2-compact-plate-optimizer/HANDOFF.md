# P17 R2 compact plate optimizer handoff

Status: **2D GATE READY / awaiting user approval; no 3D authorization**.

## Exact candidate

- Baseline: exact current P17 R2 print kit
  `/Users/scottchu/Downloads/p17_d13_before_option3_print_kit.3mf`, SHA-256
  `138ba9133df0011cf3d55386f14415ad135ebabb214d955432246bacc1602fe5`.
- Twist: left `-45 deg`, right `+45 deg`.
- Outer datum: `C=(0,0) mm`.
- Rigid workpiece/three-rod placement:
  `S=(-14.6869657526,-12.2949747468) mm`.
- Fixed purple axle: `A=(-9.5,-9.5) mm`, left/behind the aligned XT60.
- Geometry-derived diameters: inner `52.933 mm`, left outer `53.933 mm`,
  right force outer `54.933 mm`.
- Derived minimum internal web: `2.597732481369 mm`.
- True limiting rounded boundary web: `2.200398673579 mm` at the extended
  bottom fixed-track start.

## Evidence

- Deterministic optimizer:
  `src/xt60_bend_jig/p17_compact_plate_optimizer.py`.
- Focused tests: `tests/test_p17_compact_plate_optimizer.py`; `10 passed` via
  root `uv`.
- User gate:
  `docs/review/p17-r2-compact-plate-optimizer/p17-compact-plate-open-end.svg`
  and matching PNG.
- `xmllint --noout` passed.
- Independent numeric validation and visual critique passed for the exact
  candidate fingerprint in `CANDIDATE_MANIFEST.sha256`.
- The optimizer derives the plate envelope, hierarchy, internal web and true
  limiting boundary marker from P17 geometry; these are not supplied literals.

## Frozen boundary

This remains P17 R2. OPEN is the exact upper-left to upper-right to lower-right
right-angle topology; END is the accepted upper-left to middle to lower-right
diagonal. Rod identities, `OD4 x 50 mm` stock, exact head-up/tail-right wire
route, fixed inner plates, fixed purple axle, straight inner tracks and
inverse-derived counter-rotating outer rails remain unchanged.

No authoritative 3D source, STEP, 3MF, slicer artifact or print was changed.
Do not begin 3D implementation until the user explicitly approves this 2D
gate. The 2D result does not prove force, self-locking, printing or physical
behavior.

## Generalization note

The non-limiting AF8.15 inner hex bore uses an AF/2 radial proxy in this
candidate-only optimizer. It does not change this candidate, but replace it
with exact polygon-edge geometry before using the optimizer over arbitrary
future axle locations.
