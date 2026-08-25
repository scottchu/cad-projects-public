# P17 R2 head-up / tail-right orientation repair brief

Status: `P17-D10-R2` frozen for implementation. This is a focused orientation
repair inside P17 R2, not a P/R version increment.

`P17-D10-R1` corrects two inherited acceptance contradictions without changing
the selected geometry. Exact corresponding-vertex END displacement is at most
`0.657823586728 mm`, so the six-decimal safe ceiling is `0.657824 mm`.
Individual fixed-line/outer-rail crossing sine is retained as a diagnostic,
not a pass threshold, because this coupled three-rod mechanism is accepted by
regular rail loci, monotonic travel, branch continuity, and the full combined
constraint Jacobian. No coordinate, path, part, or user-visible gate changes.

`P17-D10-R2` changes only the virtual outer-rotation datum from
`C=(1.75,6.25)` to actual-solid-verified `C=(3.00,12.00)`. The former inverse
rails curled back inside their own `4.15 mm` swept cavities and removed one
side of local outer-plate reaction material. The new datum restores the
unchanged two-sided support gate while preserving every rod coordinate,
workpiece feature, angle, plate envelope, fixed axle, and part count.

## Frozen input and defect

- Design input manifest:
  `/tmp/p17-r2-orientation-design-input-manifest.txt`, SHA-256
  `8314f6fb1e7777d535f3d96b2d8549cc8e6ad4118e1aa3e01e5f743f27d569ea`.
- Baseline commit: `2b82131973d395e917e4471914584bcef1734fc3`.
- Authoritative source:
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- The accepted P17-I07-R1 mechanism used the wrong front-view workpiece
  orientation and therefore the wrong OPEN triangle. Its digital acceptance
  does not make that user-visible orientation correct.

## User-fixed outcome

- Workpiece-relative front view is world `YZ`: `+Z` is mating-head/up and
  `+Y` is solder-tail/both-wires/right, independent of Viewer camera pose.
- The completed workpiece is `└`: XT60 mating head and short vertical wire
  leg point up; the horizontal solder-tail/wire leg exits right.
- The corrected OPEN triangle has one rod at upper-left and two rods on a
  common right vertical leg: upper-right and lower-right.
- Preserve the accepted END upper-left-to-lower-right diagonal topology with
  only the supplied small orientation correction.
- Rod identity is continuous: OPEN upper-left -> END upper-left, OPEN
  upper-right -> END middle, OPEN lower-right -> END lower-right.
- All three rods move together on direct straight fixed-inner tracks. The two
  outer plates counter-rotate and their rod rails are derived by exact inverse
  transform, never drawn by eye.

## Durable orientation and topology rationale

- `REQ-027`: the front frame is workpiece-relative, not camera-relative:
  `+Z=head/up`, `+Y=tail and wires/right`.
- `REQ-028`: OPEN is UL-UR-LR with UR/LR on the exact right vertical leg
  because these are outward/retracted positions of the same rods on direct
  contact-normal paths. Rod identities cannot swap or cross and fixed-inner
  motion remains direct and stationary.
- `REQ-029`: CLAMPED/END converges UL -> middle -> LR on the diagonal. The
  middle rod addresses the bend arc; the two end rods address the vertical and
  horizontal straight-leg features. Together they form three-point wire wrap
  without using XT60 plastic as a reaction path.
- `REQ-030`: “locked” means only colloquial CLAMPED/END, not retention or
  self-lock. These invariants survive numeric refinements and cannot be
  mirrored or reversed without reopening design.

## Invariants

- Four principal plates: two fixed inner plates and two independently rotating
  outer plates; right outer remains the larger force side.
- Three moving `OD4.00 x 50.00 mm` stainless rods and six permanent caps.
- Purple stepped axle remains fixed at `A=(-29.00,17.00) mm`.
- Sliding rod slots remain `4.15 mm`; geometric motion remains linear in
  angle with `theta_end=24 deg`. Animation time alone may ease.
- No bar, yoke, linkage, gear, stabilizer, new lock, centered support, or new
  printed part.
- No XT60-body load path and no physical force, self-lock, cap-retention,
  PETG, heat, wear, or springback claim.

## Acceptance boundary

Implementation must reproduce the exact tables and equations in `DESIGN.md`,
validate actual solids through OPEN/contact/END and motion, and revalidate
loading, reverse opening, and completed-workpiece removal. CAD may prove
geometry and collision clearance only. Printed fit, holding force, insulation
response, cap retention, and cooled 90-degree result remain physical gates.
