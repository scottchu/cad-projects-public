# P20 rod-cap and clear plate-gap constraint

Date: `2026-08-27`

Status: **USER-DIRECTED CONSTRAINT RECORDED; NO GEOMETRY CHANGE AUTHORIZED**

## Scope and user intent

This record adds a future full-P20 product constraint while leaving both the
current P20 R3 CAD and the separate Blue-Orange web coupon unchanged.

The three purchased stainless rods remain only `50.00 mm` long. Their six
permanent caps must therefore be as axially short as can be shown to print and
retain safely, so the clear space between the two inner plate faces is kept as
wide as possible. The assembled XT60 body and its exact 90-degree wire bend
must not be trapped or snagged by the plates, rods, caps, keepers, or axle at
any motion or service state.

In this record, "gap between plates" means the axial `X` clear span between
the two opposing inner faces of the fixed inner plates, because that is the
space occupied by the XT60 body. FRONT geometry and motion remain in world
`YZ`: `+Z` is the XT60 mating head/up and `+Y` is the wire tail/outward-right.
If the user later means a different plate pair, that interpretation must be
confirmed before any dimension changes.

## Stable requirements

- `P20-R3-AXIAL-REQ-001`: All three white rods remain purchased, uncut
  `OD4.00 x 50.00 mm` stainless stock.
- `P20-R3-AXIAL-REQ-002`: All six rod-end caps remain permanent retainers.
  Each cap's axial head length and rod engagement must be minimized together,
  subject to source-derived closed-end wall, printable wall, installation,
  retention, cracking, wear, and heat gates. No target cap length or engagement
  is selected by this record.
- `P20-R3-AXIAL-REQ-003`: Within the fixed `50.00 mm` rod length, maximize the
  clear axial span between the inward-facing surfaces of the two fixed inner
  plates. A candidate must report that span and every term consuming rod
  length; maximizing the nominal value may not bypass fit or retention gates.
- `P20-R3-AXIAL-REQ-004`: The exact XT60 body envelope and exact P20 R3
  90-degree two-wire envelope must remain free of unintended solid
  intersection throughout the complete motion. Intended rod-to-wire forming
  contact must be separately named and must not be mistaken for trapping.
- `P20-R3-AXIAL-REQ-005`: The completed XT60 plus 90-degree pigtail must have a
  continuous collision-free loading and removal path. A static open or end
  pose alone is insufficient to claim that the workpiece is not trapped.
- `P20-R3-AXIAL-REQ-006`: Digital clearance is not physical acceptance. Final
  cap retention, cap height, plate spacing, snag-free loading/removal, and
  soldering access require a PETG assembly trial with the actual rods and an
  actual XT60 pigtail.

## Current inherited dimensions and exact relationship

P20 R2 inherits the following axial dimensions unchanged from P19; P20 R3
replaces only the workpiece reference and therefore inherits them too:

| Quantity | Symbol | Current value |
|---|---:|---:|
| rod length | `L_rod` | `50.00 mm` |
| clear inner-face span | `G_inner` | `18.40 mm` |
| inner plate thickness, each | `t_inner` | `3.20 mm` |
| inner-to-outer running gap, each side | `g_io` | `0.40 mm` |
| outer plate thickness, each | `t_outer` | `3.20 mm` |
| cap-to-outer running gap, each side | `g_cap` | `0.30 mm` |
| cap engagement on rod, each side | `e_cap` | `8.70 mm` |
| cap axial head length | `h_cap` | `9.05 mm` |
| cap closed-end wall | `w_end` | `0.35 mm` |
| XT60 body width across `X` | `W_XT60` | `15.90 mm` |
| nominal XT60 side clearance | `(G_inner-W_XT60)/2` | `1.25 mm` each |

The controlling stack equation is:

```text
L_rod = G_inner
      + 2*t_inner + 2*g_io + 2*t_outer
      + 2*g_cap + 2*e_cap

G_inner = L_rod
        - 2*(t_inner + g_io + t_outer + g_cap + e_cap)
```

The current values close exactly at `50.00 mm`. The current cap also has no
unused axial allowance: `h_cap = e_cap + w_end = 9.05 mm`. Consequently:

- reducing only the cap's external head length while retaining `8.70 mm`
  engagement cannot increase `G_inner` and would cut into the `0.35 mm`
  closed end;
- reducing engagement by `1.00 mm` on both ends would, all other terms held
  fixed, increase `G_inner` by exactly `2.00 mm`;
- that sensitivity is geometry only, not evidence that any shorter engagement
  will print, install, retain, or survive use.

The current cap inner face is `0.30 mm` outside the adjacent outer-plate outer
face. It does not directly project into the central XT60 span; its engagement
consumes the finite rod length and thereby limits how wide that span can be.

## Invariants for the later bounded design

- Keep P20 R3's accepted workpiece orientation and exact vertical leg,
  tangent R6 quarter-circle, and horizontal `+Y` tail.
- Keep the user-approved fixed purple axle and its two invariant curved rails
  unchanged unless a separate explicit contract reopens them.
- Keep rod diameter `4.00 mm`, rod length `50.00 mm`, three rod identities,
  four-plate architecture, and six permanent caps.
- Cap optimization is axial-stack work. It may not silently change YZ rod
  paths, inner or outer rail paths, outer rotation signs, workpiece placement,
  plate diameters, or the current sequential outer-rail design boundary.
- Cap/rod retention and printed fit remain physical unknowns; analytic closure
  or a valid STEP cannot approve them.

## Measurement and validation gates for a future candidate

1. **Axial equation gate** — emit `L_rod`, `G_inner`, both plate thicknesses,
   both running gaps, `e_cap`, `h_cap`, and `w_end` from authoritative source.
   Reconstruct both sides of the stack equation within `0.01 mm`, prove left
   and right cap engagement are equal, and show the rod remains exactly
   `50.00 mm`.
2. **Cap geometry gate** — for every proposed cap, prove
   `h_cap >= e_cap + w_end`, report minimum radial and closed-end walls from
   the actual solid, and prove zero cap intersection with its adjacent outer
   plate and keeper at all prescribed motion states.
3. **Cap physical coupon gate** — print the exact proposed stepped socket in
   the intended PETG process and test it on the actual `OD4.00 mm` stock.
   Record measured cap dimensions, installation behavior, pull-off/retention,
   cracking, and repeated removal/cycling observations. The retention target
   and cycle count are unresolved and must be set before calling this gate a
   pass.
4. **Full-motion solid gate** — after the sequential white-rod outer rails are
   complete, sweep at least `65` states across the entire prescribed motion
   using actual plate, rod, cap, keeper, axle, XT60, and P20 R3 90-degree wire
   solids. Report minimum clearances and all intersection volumes. Only named
   rod-to-wire forming contact may be allow-listed; any XT60-body or
   unintended wire intersection fails.
5. **Not-trapped service-path gate** — verify a continuous rigid loading and
   removal path for the completed XT60 plus both bent wires against all
   production solids, with both analytic sampling and actual-solid BREP
   checks. Use the current `0.75 mm` service-clearance requirement as the
   minimum unless a later explicit decision raises it. Report the limiting
   pair and pose; zero intersection at only the endpoints does not pass.
6. **Physical assembly gate** — assemble all four printed plates, six caps,
   three stock rods, keepers, and axle. With the actual XT60 pigtail, exercise
   loading, full motion, solder pose, cooling, and removal. Pass only if the
   user confirms that no cap/plate geometry traps or snags the XT60/wires and
   the plate gap is practically adequate.

## Open questions and physical unknowns

- Minimum cap engagement that provides reliable permanent retention in the
  selected PETG process.
- Minimum closed-end and radial wall that prints without cracking or heat
  damage in this exact cap orientation.
- Whether the user's phrase "cap ... too tall" identifies axial head length,
  radial head diameter, or both. Axial length is the controlling interpretation
  here; radial diameter must still be checked for snagging in the actual-solid
  and physical service gates.
- Whether `0.75 mm` is enough practical service margin for the real insulated
  90-degree pigtail, or only a digital lower bound.
- Soldering-iron access, hand force, friction, wear, springback, and heat remain
  separate physical gates.

## Non-authorization and stop boundary

This document does **not** authorize changing any parameter, source, test,
STEP, mesh, slicer project, print artifact, simulator profile, cap, plate,
rod, rail, axle, keeper, XT60, or wire geometry. It does not approve the
current P20 R3 assembly for printing and does not alter the separate temporary
approval to print the Blue-Orange `1.72 mm` web coupon. A later full-P20 axial
optimization must open its own bounded contract and freeze a candidate before
implementation.
