# P17 compact plate optimizer numeric contract

## Variables and transform

For progress `u in [0,1]`, preserve the exact current P17 rod paths and apply
the same rigid placement `S` to rods, XT60, wire, bend, solder and service
references. Outer plates use `alpha_left=-theta*u` and
`alpha_right=+theta*u`. Every side-local rail is generated only by the existing
inverse-frame transform; no rail may be hand drawn.

Search variables are `(S_y,S_z)`, `A_y,A_z`, `C_y,C_z`, and
`theta in [24,45] deg`. `C=(0,0)` is a coordinate gauge for the selected
candidate, not a requirement that the physical axle be centered.

## Objective order

1. Reject any violation of TASK_INPUT invariants, contact, collision, service,
   topology, identity, web, or plate upper bound.
2. Prefer the longest feasible twist, capped at `45 deg`.
3. Minimize the inner circular envelope.
4. Preserve canonical `REQ-012` with strict diameter hierarchy:
   `left outer = inner + 1.0 mm` and
   `right force outer = inner + 2.0 mm`.
5. Prefer `A` left/behind the aligned XT60 and near the compact Z center.
6. Use rail balance/crossing as conditioning diagnostics, never as physical
   force proof.

## Selected values

| Quantity | Value |
|---|---:|
| `theta` | `45 deg` |
| `C` | `(0,0) mm` |
| rigid set placement `S` | `(-14.6869657526,-12.2949747468) mm` |
| fixed axle `A` | `(-9.5,-9.5) mm` |
| inner plate diameter | `52.933 mm` |
| left outer diameter | `53.933 mm` |
| right outer diameter | `54.933 mm` |
| minimum internal web | `2.59773248 mm` |
| required boundary web | `2.20 mm` |

The analytic unrounded inner envelope is `52.93220265 mm`; rounding down to
`52.932 mm` would undershoot the boundary construction by about `0.000101 mm`,
so the implementation value is rounded upward. The unrounded left and right
outer diameters are respectively `53.932203 mm` and `54.932203 mm`; their
`+1.0/+2.0 mm` increments are the explicit design hierarchy required by
`REQ-012`, while the inner envelope remains the mathematical size driver.

## Required 2D evidence

Render OPEN and END in the same workpiece-relative FRONT frame. Show XT60 head
up, tail/wires right, the three named rods, unchanged rod identities and
triangles, straight inner tracks, both derived counter-rotating outer rail
sets, `A`, `C`, plate circles and diameters, 45-degree arrows, and the limiting
web location. Include a compact invariant checklist and clearly label this as
a 2D proposal, not 3D/print/physical acceptance.
