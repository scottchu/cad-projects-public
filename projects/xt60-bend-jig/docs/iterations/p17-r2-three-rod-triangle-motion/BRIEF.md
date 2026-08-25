# P17 R2 three-rod triangle motion brief

Status: frozen design input for implementation. This is a focused P17 R2
repair, not a new product or revision version.

## Exact baseline

- Task input manifest: `/tmp/p17-r2-three-rod-design-input-manifest.txt`,
  SHA-256 `a753e37f408aa4dfaa04159e41c71f1b692fa9f36b01587d46ccb244d92f51c2`;
  every listed entry matched before design.
- Baseline commit at task freeze:
  `df9af826385db3f625917eca15a6d64273d8fd5f`.
- Accepted predecessor fingerprint:
  `20fc5068814e5c3f5d9c58fdaff98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
- Authoritative source remains
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- A concurrent Viewer-service-only commit advanced repository HEAD after the
  freeze; none of the frozen XT60 project inputs changed.

## User outcome and sequence

1. Use all three physical `OD4.00 x 50.00 mm` stainless rods as one coupled
   mechanism, not one rod at a time.
2. At OPEN, the three rod centers form a real, large insertion triangle.
3. Counter-twist the two outer plates in opposite directions. The fixed inner
   plates and purple printed axle remain world-invariant.
4. Each rod moves on one direct straight world `YZ` line through both fixed
   inner plates. Each rotating outer plate uses its own derived curved rail.
5. At first contact, the rods are tangent to the nominal two-wire 90-degree
   bend envelope. At END, each rod adds the same `0.25 mm` geometric preload
   displacement proxy without contacting or loading the XT60 plastic.
6. Solder, cool, reverse to OPEN, and remove the completed pigtail through the
   central clear span. No removable rod cap is used.

The user called END the “locked triangle.” That name identifies endpoint
geometry only. This iteration adds no hard stop, detent, over-center feature,
or self-lock and makes no lock claim.

## Requirements

- `TRI-REQ-01`: exactly three moving stainless rods, all `OD4.00 x 50.00 mm`.
- `TRI-REQ-02`: exactly four principal plates; both inner plates fixed; left
  and right outer plates counter-rotate `-theta/+theta`.
- `TRI-REQ-03`: the purple stepped axle stays fixed at world
  `A=(-29.00,17.00) mm` and is not a stainless forming rod.
- `TRI-REQ-04`: define numeric OPEN, first-contact, and END triangles and
  derive every fixed and rotating rail from them.
- `TRI-REQ-05`: rods contact only insulated wires; XT60 body is never a load
  path and has at least `0.75 mm` nominal actual-solid clearance.
- `TRI-REQ-06`: both wires use the same world `YZ` bend geometry and are
  separated only in `X`; every X-spanning rod therefore acts on both wires.
- `TRI-REQ-07`: all six caps are permanent and use a coupon-gated stepped
  socket; inconsistent P13 cap interference is not inherited.
- `TRI-REQ-08`: no new bar, stability member, yoke, linkage, gear, centered
  support, or decorative hole is added.
- `TRI-REQ-09`: remove the redundant green left outer grip block; retain a
  larger right force-side outer plate.
- `TRI-REQ-10`: a rod is supported on both sides of every guide normal in both
  fixed inner plates and both outer plates; no floating/open-sided guide is
  accepted.

## Explicit non-goals

- No new lock or self-lock claim.
- No simulator repair and no simulation-only geometry authority.
- No change to the fixed purple axle geometry or world position.
- No new support hardware or stability structure.
- No claim of physical force, insulation safety, springback, cap retention,
  PETG heat behavior, wear, or stiffness from CAD.

## Supplied physical evidence

- The P13 photo shows real rods protruding and inconsistent cap installation.
  It confirms a product geometry problem, not a print-only tolerance problem.
- Four caps fit while two were too tight on nominal rods. The production cap
  needs a separate permanent-retention coupon ladder.
- The physical rods are `50.00 mm`; the accepted predecessor modeled
  `40.60 mm`. This iteration intentionally returns all three rods to the real
  `50.00 mm` stock and re-derives the cap stack.
- The `4.15 mm` PETG coupon was the best observed sliding fit with slight
  friction; it applies to moving rod guides, not permanent cap retention.

## Done gate

Implementation is ready for independent critique/validation only when the
selected numeric contract in `DESIGN.md` is source-derived, the current invalid
guide table and smoothstep law are gone, actual solids satisfy the collision,
math, constraint, support, motion/service, and user-requirement gates, written
STEP states validate, and the exact artifact is visually reviewed. Physical
acceptance remains pending.
