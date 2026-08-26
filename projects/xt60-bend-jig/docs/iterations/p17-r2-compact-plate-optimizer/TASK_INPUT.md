# P17 R2 compact-plate optimizer task input

Status: user-authorized scope reopen on `2026-08-25`; this is a 2D gate only.

## Outcome

Produce a cheap user-reviewable FRONT YZ diagram and deterministic parametric
search before any 3D CAD change. The intended mechanism remains P17 R2.

## User-authorized changes

- Reduce the current P17 principal plate diameters from `80/82/85 mm` into a
  target band of approximately `50..55 mm`; `80 mm` is unacceptable. The
  earlier roughly `40 mm` size is comparison evidence only, never a geometry
  baseline.
- Move the purple fixed stepped axle `A` as needed. It must remain on the
  left/behind side of the workpiece-relative FRONT view and near the vertical
  center of the compact mechanism.
- Search outer rotation datum `C`, fixed axle `A`, a rigid common placement of
  the complete workpiece-plus-three-rod kinematic set relative to the plates,
  and twist travel. Twist may range up to `45 deg`; prefer the longest feasible
  twist, with `45 deg` as the upper limit.
- Derive every fixed-inner and outer rail from one reusable deterministic math
  function. Plate diameter must be derived from the complete feature/swept
  envelope plus required PETG web, not typed as an unrelated constant.

## Frozen invariants

- FRONT frame: `+Z` is XT60 mating head/up; `+Y` is solder tail and both wires
  outward/right.
- XT60 body, wire, bend, three rod paths, and solder/service geometry move only
  as one rigid workpiece-relative set. Never translate the rods away from the
  workpiece/contact geometry.
- The exact current P17 `GUIDES` and visible rod triangles are the baseline.
  The source's unshifted invisible XT60/wire/service references are stale: for
  this optimizer they must receive the same
  `(+16.1869657526,+10.2949747468) mm` placement already present in the P17
  guides, restoring their accepted workpiece-relative clearance/contact. This
  is a reference-alignment repair, not permission to substitute older guide
  tables or change the visible P17 rod topology.
- OPEN topology is upper-left -> upper-right -> lower-right with an exact
  right-side vertical leg. END topology is upper-left -> middle -> lower-right
  on the accepted diagonal wrap.
- Bottom, diagonal, and upright rod identities remain continuous; no swap,
  crossing, mirror, or reversal.
- Three purchased uncut stainless rods remain `OD4.00 x 50.00 mm`; six caps
  remain permanent.
- Both inner plates and the purple axle are world-fixed. Fixed-inner rod guides
  are direct stationary straight tracks.
- Outer plates counter-rotate in opposite directions by `-theta/+theta`; every
  outer rail and both fixed-axle guide rails are inverse-transform-derived.
- Four plates, one stepped fixed axle, and a slightly larger right force-input
  outer plate remain. No stability bar, yoke, linkage, gear, grip block,
  replacement lock, or self-lock claim.
- Preserve exact workpiece-relative OPEN clearance, END three-point contact,
  `0.25 mm` geometric preload proxy, solder access, and extraction direction.
- Minimum required PETG web is `2.20 mm`; rod running slots remain `4.15 mm`
  unless a later physical-fit decision explicitly changes them.

## 2D acceptance gate

The diagram must show at least OPEN and END in the same fixed FRONT frame, with
XT60 head/tail direction, wires, all three named rods, `A`, `C`, left/right
counter-rotation arrows, derived plate outlines/diameters, and the minimum-web
location. It must state the selected twist, optimizer variables, objective,
hard constraints, and any infeasibility honestly. Do not begin 3D implementation
until the user approves this gate.

## Baseline

- Exact current P17 print kit shown by the user:
  `/Users/scottchu/Downloads/p17_d13_before_option3_print_kit.3mf`.
- Exact print-kit SHA-256:
  `138ba9133df0011cf3d55386f14415ad135ebabb214d955432246bacc1602fe5`.
- Exact P17 source/artifact manifest:
  `cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`,
  SHA-256 `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.
- This exact P17 geometry is the sole optimization baseline. Older P13 and
  earlier P17 coordinate tables must not be substituted.
