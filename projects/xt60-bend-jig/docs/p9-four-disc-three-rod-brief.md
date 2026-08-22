# P9 — minimal four-disc / three-rod proof

P9 replaces the rejected P7/P8 structures. It is intentionally a bare motion
proof, not a styled enclosure.

## Architecture contract

- Exactly three purchased 304 stainless rods: `4.0 mm × 50.0 mm`.
- Exactly four principal printed plates:
  - left fixed guide disc;
  - left rotating cam disc;
  - right fixed guide disc;
  - right rotating cam disc.
- Each side therefore contains one fixed disc and one rotating disc.
- The two rotating discs share one keyed shaft and move together.
- No L-frame, cage, tower, large wall, skeletal spider, handle frame, gear,
  linkage, or cosmetic body.
- A small integral flat clamp tab on each fixed disc is allowed. It is not a
  separate part and must not obstruct the work corridor.
- One simple indexed lock hole may align at the closed position. A removable
  3 mm pin is allowed and is the only positive closed-position lock; do not add
  another stop or lock mechanism.

## Motion

- Preserve the accepted P7 three-rod endpoints and common `11.0 mm` travel.
- Use three straight `4.4 mm` guide slots in each fixed disc.
- Use three calculated `4.4 mm` inverse cam slots in each rotating disc.
- Closing motion is `0°..70°`; `70°..80°` is a true dwell.
- The `80°` indexed lock position must retain the exact final `90°` wire path.
- The rod center positions at open and closed remain the P7 values.
- Shaft datum: `Y=-7.500, Z=32.500 mm`. The more central candidate blocks the
  XT60 removal corridor and does not leave enough slot web.
- Disc outside diameter: `64.0 mm`. Dense path sampling must reproduce maximum
  follower radius `26.301568 mm`, at least `2.0 mm` inter-slot web, and about
  `3.498 mm` edge material before solid-level validation. The extra 0.5 mm
  radial margin is intentional print robustness, not added mechanism complexity.

## Plate construction

- Plain circular plates, no full-face visual decoration.
- Fixed guide disc thickness: `3.0 mm`.
- Rotating cam disc thickness: `2.5 mm`.
- Axial running clearance between paired discs: `0.30 mm`.
- Guide and cam slot width: `4.4 mm` for the purchased 4 mm rods.
- Minimum material from every slot edge to the outside edge: `2.5 mm` for this
  first proof; target `3.0 mm` where it does not enlarge the disc.
- Minimum web between slots: `2.0 mm`.
- All four plates must be single connected solids.

## Rod retention and assembly

- Left rod ends use the existing `3.90 mm` press-fit trial retainers.
- Right rod ends use removable `4.10 mm` keepers with a `3.60 mm` snap throat.
- The rods pass through both plate pairs and are the only work-contact members.
- The keyed shaft synchronizes the two outer cam discs.
- Model an exploded assembly proving the order: left retainers, left cam, left
  fixed disc, three rods, right fixed disc, right cam, right keepers, shaft,
  and the single optional lock pin.

## Work and removal clearance

- Clear span between the inside faces of the fixed discs: `32.0 mm` minimum.
- The open rod triangle must leave a vertical removal corridor for the XT60:
  `|X| <= 8.25 mm`, `|Y| <= 4.25 mm`, `Z >= 34.0 mm`.
- No printed solid, shaft, or purchased rod may enter that corridor in the open
  state. This represents the `15.9 × 8.1 mm` XT60 body plus clearance.
- In the closed state, show the bottom ESC, copper pads, horizontal solder legs,
  R6 bend, vertical leads, and XT60 only as reference geometry.
- ESC remains below the FC. The copper-pad top datum is `Z=27.85 mm`.
- No printed solid may intersect the closed solder-access volume:
  `|X| <= 10.0 mm`, `Y=24.0..70.0 mm`, `Z=27.85..38.0 mm`. Electronics,
  solder, and wire references are intentionally excluded from this check.
- Open and closed workpiece states may be physical references. Any intermediate
  wire interpolation is construction-only and must be labeled
  `nonphysical_mid_deformation_reference`.

## Required artifacts

- Source: `src/xt60_bend_jig/p9_four_disc_three_rod.py`
- Tests: `tests/test_p9_four_disc_three_rod.py`
- STEP Python entrypoints and generated STEP files under
  `cad/p9_four_disc_three_rod/`:
  - `p9_loaded_open`
  - `p9_loaded_closed`
  - `p9_exploded`
  - `p9_print_kit`

## Acceptance tests

- Exactly three rod solids and exactly four principal plate solids.
- Rod diameter/length are `4.0 × 50.0 mm`.
- Common rod travel is `11.0 mm` and final wire angle is exactly `90°`.
- Closed and `80°` dwell rod centers are identical.
- Both cam discs have identical slot geometry and keyed angular pose.
- Every plate is one connected solid.
- Slot widths and plate thicknesses match this brief.
- Minimum edge/web material passes the stated limits.
- Open XT60 removal corridor has zero BREP intersection with plates, shaft,
  rods, and keepers.
- Closed solder-access corridor has zero intersection with printed parts.
- Source/export label parity and fresh-process repeatability pass.
- Print kit contains no purchased rods or electronics.

Passing CAD tests proves only nominal geometry. Press fit, snap retention,
friction, heat response, stiffness, soldering access, and real XT60 removal
still require printing and bench testing.
