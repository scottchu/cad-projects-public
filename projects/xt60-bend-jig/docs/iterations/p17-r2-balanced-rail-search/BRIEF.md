# P17-D14 balanced rail search

Status: **BLOCKED by frozen geometry; no implementation candidate.** This remains P17 R2.

## Intent

The user selected a joint deterministic search over outer-plate datum `C=(Cy,Cz)` and one common world translation `D=(Dy,Dz)` of all three stainless rods. The goal was to retain the exact I10 workpiece and three-point END contact while reducing left/right outer-rail imbalance. D13 is retained as rejected evidence.

## Frozen product contract

- FRONT uses `+Z` up and `+Y` right; XT60 head is up and tail/wires exit right.
- The I10 XT60 body, finite wire bend, service/extraction interface, rod identities, OPEN and END topology are fixed.
- Three `OD4 x 50 mm` rods follow equal `10.5852813742 mm` straight world strokes; six permanent caps remain.
- `A=(-29,12)` is fixed. Inner plates are fixed. Outer plates counter-rotate by `-24u/+24u deg`.
- Four plates, one stepped fixed axle, larger right force side, no new part, link, yoke, gear or lock.
- Every outer rail must use the existing inverse-frame equation; no hand-drawn rail is allowed.

## Result

The feasible set is empty before outer-rail optimization:

1. Exact END contact against the fixed I10 vertical wire forces `Dy=0` from the bottom rod.
2. Exact END contact against the fixed I10 horizontal wire forces `Dz=0` from the upright rod.
3. Therefore `D=(0,0)`; the diagonal rod then retains the I10 bend contact automatically.
4. At `D=(0,0)`, the fixed axle/hex guide to bottom inner straight slot web is only `1.615172 mm`, below the hard `2.20 mm` gate. This distance is world-fixed and independent of `C`.

Changing `C` can rebalance outer rails, but cannot repair that inner-plate web. No D14 candidate is dependency-ready.

Review diagram: [p17-d14-bounded-infeasibility.svg](../../review/p17-r2-balanced-rail-search/p17-d14-bounded-infeasibility.svg).
