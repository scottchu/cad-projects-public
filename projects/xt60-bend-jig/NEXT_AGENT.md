# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p18-r1-compact-counter-twist`.
- Active baseline: P18 R1 compact 45-degree counter-twist.
- Candidate manifest SHA-256:
  `fb0755a0d448ee000dde4bd63eacca7fbaf6e55abeb16312a7f39c5ccfc5d1d5`.
- Source: `src/xt60_bend_jig/p18_r1_compact_counter_twist.py`.
- Tests: `tests/test_p18_r1_compact_counter_twist.py`.
- Full motion:
  `cad/p18_r1_compact_counter_twist/p18_r1_full_motion.step.py`.

## Frozen mechanism

- FRONT is world YZ: `+Z` XT60 head/up; `+Y` solder tail/wires right.
- OPEN is upper-left -> upper-right -> lower-right with an exact right vertical
  leg. END is upper-left -> middle -> lower-right on the accepted diagonal.
- Rod identities never swap, cross, mirror or reverse.
- Three rods are `OD4 x 50 mm`; six caps are permanent.
- Fixed: both inner plates, both keepers and purple stepped axle
  `A=(-9.5,-9.5)`.
- Rotating: left/right outer plates at `-theta/+theta` around virtual
  `C=(0,0)`, END `45 deg`; right force outer is slightly larger.
- Plates are `OD52.933/53.933/54.933 mm`; all outer rails and axle rails are
  inverse-transform-derived. There is no physical centered pivot at C.
- Forbidden: stability bar, yoke, linkage, gear, grip block, replacement lock
  or self-lock claim.

## Accepted evidence

- Focused tests `10 passed`.
- Rail reconstruction residual `3.97e-15 mm`; minimum web
  `2.200398673579 mm`.
- Four-contact closure rank `3`; maximum normalized condition
  `3.750295905779`.
- 65-state actual-BREP and full two-sided support passed with zero unintended
  intersections.
- Completed-pigtail service clearance `0.933815921231 mm` analytic and
  `1.25 mm` BREP against the `0.75 mm` gate.
- Six STEP artifacts validate and exactly match source bounds/topology/counts.
- Four snapshots were independently reviewed.
- Formal review accepts CAD, STEP and Viewer handoff only.

## Next smallest action

Obtain user review of the persistent P18 full-motion Viewer. Do not change CAD
from visual feedback until the exact requested change is stated. Do not slice
or print unless explicitly requested.

If the user approves the 3D geometry for a first print, keep these physical
gates explicit: near-tangent hand force/friction/wedging/backlash, complete
soldering-iron access, cap/keeper retention, axle/hex fit, limiting-web PETG
outcome, right-side grip usefulness, heat and wear. END is not self-locking.

Use only Python 3.12 through the repository root `uv` workspace and the
persistent singleton Viewer managed by `~/.local/bin/cad-viewer`.
