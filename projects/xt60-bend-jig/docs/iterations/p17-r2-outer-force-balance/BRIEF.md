# P17-D11 outer-rail force balance

Status: **BLOCKED — no implementation contract accepted**.

This remains P17 R2. The user-visible defect is real: Rod 1 (`bottom`) and
Rod 2 (`upright`) have strongly unequal left/right outer-rail crossing angles
and path lengths, while the middle `diagonal` rod is the qualitative balance
reference. The correction is limited to the outer-rail kinematics. The exact
OPEN/contact/END world triangles, rod identities, fixed straight inner tracks,
head-up/tail-right workpiece, `A=(-29,17)`, plate diameters `80/82/85 mm`,
`4.15 mm` slots, three `OD4 x 50 mm` rods, six permanent caps and larger right
force side are frozen.

The design task tested, in order:

1. a common outer center `C` with the existing linear `+/-24 deg` motion;
2. the smallest equal-magnitude/opposite nonlinear outer motion compatible
   with `REQ-023`, first at frozen `C`, then with a bounded common-`C` shift.

No tested candidate passed force-balance, `2.20 mm` web, two-sided support and
actual-solid collision gates together. Source, tests and CAD artifacts must not
be changed from this iteration. `IMPLEMENTATION_INPUT_MANIFEST.sha256` freezes
the blocked result for provenance; it is not permission to start P17-I09.

## P17-D11-R1 focused outer-envelope repair

R1 reopened only the two outer plate envelopes/profile and common virtual
rotation datum `C`, as authorized. The result remains **BLOCKED**. A
lower-curvature candidate passes force balance, web, collision, guide,
conditioning and service gates, but its swept rail topology removes the
required `0.30 mm` two-sided support internally. Its derived radial envelope
needs only `73.302 mm`, already smaller than the existing `82/85 mm` outer
plates. Therefore a shared or independent diameter increase cannot repair the
failure. No P17-I09 implementation contract is released.

## P17-D11-R2 final motion-law repair

R2 reopened only the physical `beta(u)` law to a two-segment, strictly
monotone `C1` spline plus bounded common `C`. The final result remains
**BLOCKED**. The bounded analytic search found force- and web-feasible laws,
but both actual-solid shortlists still lose the mandatory `0.30 mm` internal
support strip. No further design repair is authorized and no implementation
contract is released.
