# P19 R1 repair-1 independent service and kinematic recheck

Decision: **ACCEPT FOR USER 2D REVIEW ONLY.** The repaired candidate closes
the prior 2D blockers. This decision does not authorize P19 3D implementation,
STEP, slicing, printing, force/fit claims or physical acceptance; those remain
blocked until the user accepts this direction and a later frozen 3D contract
passes its own independent gates.

## Exact candidate

- Baseline Git commit:
  `bcc16305ff112ba814bdf19ad544a5819127e902`.
- Seven-entry design-input manifest SHA-256:
  `133ddcafbb153a33ad07be50ad9f3dda3a31d0df82d1446a00865ef7f64b404b`;
  all entries previously verified from repository root.
- Final repaired `DESIGN.md` SHA-256:
  `169583198638b23201b5c47835a66537551f87a837e78c21bb519161e3704fb7`.
- Repaired PNG SHA-256:
  `b2597076bc821aec78cc3557c24edd9bf77f5c720a48a0975e56c5c6dbd8e675`.
- Review artifact:
  `docs/review/p19-r1-front-edge-short-tail/design-repair1-b2597076bc82.png`.

## Prior-blocker disposition

| Prior finding | Recheck result |
|---|---|
| Missing user-review image | **CLOSED.** The fingerprinted phone-format PNG exists and was inspected at original resolution. |
| Four equal OD55 plates | **CLOSED.** Fixed inner `OD54.40`, left outer `OD54.70`, right force outer `OD55.00`; the required hierarchy and force-side identity are visible. |
| Tool corridor was centreline-only | **CLOSED for 2D direction.** The complete `8 x 8 mm` keepout is shown at `Y=32.25`; its left edge `Y=28.25` is exactly `0.75 mm` beyond the largest plate tangent `Y=27.50`. The cup envelope starts at `Y=29.25`. |
| OD4.30 rod rails contradicted wobble evidence | **CLOSED.** Every OD4 rod path/rail is restored to the physically supported `OD4.15 mm`; the separate axle guide remains `OD7.90` around `OD7.60`. |
| No actual cup/wire/contact model | **CLOSED for 2D direction.** The gate shows the P18 `OD4.30` wire envelope, two X-separated cup occurrences represented by their coincident FRONT envelope, XT60 head/up, short tail/right, OPEN surface clearances, first-contact progress and named END `0.25 mm` geometric preload targets. |
| Force direction not visible | **CLOSED for user review.** Both hand-rotation arrows, world rod-travel direction and local rail-tangent arrows are shown. The shallowest crossings are reported as `2.752 deg` left and `3.101 deg` right, with rank 3 throughout the 2D probe. |
| Fixed axle appeared as a YZ point | **CLOSED.** `A=(-13,-9)` is visibly left/behind and a separate inset shows one physical `34.90 mm` X-axis stepped member through both keyed inner plates and both journalled outer plates. |

## Direction, topology and web recheck

- PASS — physical FRONT remains `+Y` right/short-tail/tool approach and `+Z`
  mating-head/up. The XT60, cup and tail are not mirrored.
- PASS — OPEN remains the ordered exact right angle
  `(5,10) -> (20.4,10) -> (20.4,-5)` and END remains the ordered exact
  diagonal `(8,9) -> (14.25,3.25) -> (20.5,-2.5)`. Bottom, diagonal and
  upright identities do not cross or swap.
- PASS — complete fixed-inner world paths and both side-specific inverse rail
  families are shown. The equations remain
  `q_s,i(u)=R(-alpha_s(u))p_i(u)` and `qA_s(u)=R(-alpha_s(u))A`; no hand-drawn
  outer rail is introduced.
- PASS — all diameters remain within the user-authorized `50-55 mm` envelope.
  Recomputed 2D minimum is the fixed-inner rim web `2.405845 mm`, above the
  `2.20 mm` requirement. The remaining `0.205845 mm` margin is explicitly
  labelled marginal and does not substitute for later exact-solid evidence.
- PASS — the short wire reaches the cup outside the largest rim, while the
  three-rod clamp stays near the front edge rather than being translated far
  behind the connector.

## Nonblocking risks that must remain visible

- The repaired image has minor overlapping header/footer annotations, but the
  OPEN/END geometry, service keepout, rail panels and axle inset remain
  readable. This is a presentation defect, not a direction ambiguity.
- First contacts are deliberately progressive (`u≈0.1185`, `0.8296`,
  `0.8717`) rather than simultaneous. The 2D gate describes that sequence but
  does not prove real flexible-wire deformation, rod force, insulation safety
  or final bend angle.
- The right-side worst normalized condition `10.1768` and the shallow crossing
  angles remain meaningful friction, clearance-amplification, wedging and
  back-drive risks. They do not invalidate the user-facing topology/service
  direction, but they require later 3D and physical treatment.
- The exact BREP rim web, actual X-separated cup/tool cone, cap/keeper
  clearance, single-solid support, heat, fit, torque and retention remain
  unvalidated.

## Gate conclusion

The exact repaired pair may now be shown to the user to answer one bounded
question: **is this the correct front-edge short-tail layout and twist
direction to freeze before 3D?** No broader acceptance follows from a positive
answer, and no P19 3D work should begin until that explicit user decision is
recorded.
