# P17 R2 outer-rail force-balance defect input

Status: frozen user defect and coordination input for `P17-D11`.
Baseline commit: `8adfb20f352e36cede54a3414307ced3de81c2b8`.
Version disposition: focused P17 R2 rail-geometry refinement; no P/R increment.

## User observation

Review is limited to the outer plates and their three rod rails. The user
identified the two end rods as unbalanced: one side presents a long/shallow
rail while the opposite side is short, raising concern that the hand force
will be either ineffective or excessive. The unlabelled middle rod appears
most balanced and is the qualitative reference.

Reference images:

- `/Users/scottchu/.codex/attachments/210908bc-9de2-4c43-aedb-8a18d5f90b6a/codex-clipboard-7eb2821f-aa8a-4869-aee0-cbd022b72eac.png`
- `/Users/scottchu/.codex/attachments/e18aec55-2c27-4dce-b652-517697dc7c13/Screenshot 2026-08-25 at 9.57.36 AM.png`

## Rod identity mapping

- User Rod 1: source role `bottom`, OPEN upper-left -> END upper-left.
- User middle/reference rod: source role `diagonal`, OPEN upper-right -> END middle.
- User Rod 2: source role `upright`, OPEN lower-right -> END lower-right.

## Reproduced analytic evidence at first contact / END

The crossing angle is between the outer-slot centerline tangent and the fixed
inner straight-track direction. Ignoring friction and compliance, the useful
normal component along the rod direction is `sin(phi)`, so `1/sin(phi)` is a
diagnostic ideal contact-load multiplier, not a measured hand-force claim.

| rod | outer side | rail length (mm) | END crossing angle | diagnostic multiplier |
|---|---|---:|---:|---:|
| Rod 1 / bottom | right blue | `15.866822` | `5.05 deg` | `11.4x` |
| Rod 1 / bottom | left opposite | `5.582780` | `14.56 deg` | `4.0x` |
| middle / diagonal | right blue | `14.536168` | `21.43 deg` | `2.7x` |
| middle / diagonal | left opposite | `11.213927` | `29.99 deg` | `2.0x` |
| Rod 2 / upright | right blue | `4.519826` | `29.86 deg` | `2.0x` |
| Rod 2 / upright | left opposite | `19.041356` | `4.45 deg` | `12.9x` |

Thus the previous coupled-rank acceptance did not prove useful force
transmission. The defect is rail direction/path asymmetry, not nominal slot
width.

## Preserved invariants and non-goals

- Preserve exact OPEN, first-contact, and END world rod triangles and continuous
  rod identities unless the design role proves mathematically impossible and
  stops for explicit reopening.
- Preserve workpiece frame: XT60 mating head `+Z`/up; tails and wires `+Y`/right.
- Preserve fixed inner plates and their direct stationary straight tracks.
- Preserve opposite outer rotation, four plates, larger right force plate,
  three `OD4 x 50 mm` rods, six permanent caps, fixed purple axle
  `A=(-29,17)`, and no added part or mechanism.
- Preserve `4.15 mm` rod-slot width. Do not treat visual path length as bore
  looseness and do not widen the rails.
- No bar, yoke, link, gear, grip block, lock, self-lock claim, 3MF, slicer, or
  physical-force claim.
- Force quality is a new geometric diagnostic/gate; real friction, PETG
  compliance/wear, wire stiffness, and hand torque remain physical unknowns.

## Design objective

Find the smallest parametric outer-motion/rail refinement that makes Rod 1 and
Rod 2 comparable to the current middle rod at contact-to-END, while keeping
the frozen architecture and user-visible rod states. The designer must derive
and justify quantitative pass thresholds for minimum force angle and
left/right path balance, then prove actual-solid feasibility before handing a
contract to implementation.
