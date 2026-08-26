# ADR-0004: P18 R1 compact 45-degree counter-twist baseline

- Status: accepted for digital CAD/STEP baseline
- Date: `2026-08-26`
- Supersedes: P17 R2 as the active forward product-design baseline
- Superseded by:

## Context

The user accepted the P17 compact 2D optimizer candidate and explicitly asked
to create P18. The accepted change combines a much smaller plate envelope,
moved eccentric fixed axle and longer 45-degree counter-twist. That changes the
core product geometry together and therefore qualifies as a new `P` baseline,
not a small P17 revision.

## Decision

P18 R1 uses inner/left-outer/right-outer diameters
`52.933/53.933/54.933 mm`, virtual outer datum `C=(0,0)`, fixed stepped axle
`A=(-9.5,-9.5)`, and opposite outer rotations `-45/+45 deg`. It preserves the
accepted workpiece-relative OPEN/END topology, three `OD4 x 50 mm` rods, six
permanent caps, fixed inner plates, exact stepped hex/round axle, straight
inner tracks and inverse-derived outer rails. It adds no centered pivot,
stability bar, yoke, linkage, gear, grip block or lock.

## Consequences

The compact candidate digitally passes math, constraint, actual-solid,
two-sided support, service path, STEP parity and visual gates. The near-tangent
rail interval remains a physical force/friction risk. Full soldering-iron
access, printed fit, cap/keeper retention, heat, wear and self-lock are not
accepted. Mesh, 3MF, slicing and printing remain separate evidence layers.

## Evidence

- `docs/iterations/p17-r2-compact-plate-optimizer/`
- `docs/iterations/p18-r1-compact-counter-twist/`
- `src/xt60_bend_jig/p18_r1_compact_counter_twist.py`
- `tests/test_p18_r1_compact_counter_twist.py`
