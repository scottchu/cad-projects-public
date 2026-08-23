# KAGE B0 Q4-R1 physical validation card — v1

Article: `p3_v3_mvp_base_q4_r1`  
Gate: four printed quadrants become one usable 300 mm base  
Rule: any RED stops B1 ring/support work

## CAD already passed — do not retest by eye

The focused CAD suite passed `13/13` before this card was issued. It established:

- exactly four one-solid quadrants and four one-solid bridges;
- nominal 300 mm OD, 0.10 mm seams, and coplanar nominal datums;
- each quadrant fits the 260 mm usable bed with the required 5 mm brim;
- real nut, screw, round-dowel, relieved-dowel, and driver-access geometry;
- S4 has a collision-free upward insertion path after S1–S3;
- joinery stays inside R117, leaving R118..150 for later supports.

CAD did **not** establish printed shrinkage, first-layer warp, press fit, nut
capture, last-bridge insertion by hand, full-loop closure, free-state flatness,
clamp retention, damage over service cycles, or vertical behavior. This card
decides those unknowns.

## Bring

Printed, all from the same material/profile:

- Q1, Q2, Q3, Q4, front face printed on the bed;
- S1, S2, S3, S4, bottom-down with pockets/bores open upward.

Purchased hardware:

- 8 x M3x6 ISO 7380-1 button-head screws;
- 8 x ISO 4032 M3 hex nuts;
- 8 x D4x6 steel dowel pins.

Ordinary tools:

- matching hex key, phone camera, ruler/tape, and a straightedge at least
  300 mm long;
- a known-flat table/counter and four equal-height supports such as identical
  blocks or cans;
- ordinary printer paper cut into strips (about 0.10 mm per sheet) and, if
  available, thin receipt paper (about 0.05 mm);
- optional feeler gauge or long caliper for resolving borderline results.

## Contract-critical printing

- Quadrants: supplied `*_front_down.step`, front face on bed, 5 mm brim, no
  support.
- Bridges: supplied `*_bottom_down.step`, pockets and blind bores upward; no
  support inside them.
- Use one material, layer height, wall count, cooling setting, and bed setup for
  all four quadrants. Do not tune one quadrant separately.

Record material, printer, nozzle, layer height, and slicer/profile name below.
All other slicer choices are process notes, not new acceptance requirements.

## Exact assembly sequence

1. Mark Q1–Q4 and S1–S4. Photograph all eight clean printed parts and all 24
   hardware pieces before assembly.
2. Press two D4x6 pins into every bridge, one at R78 and one at R108, leaving
   2.50 mm exposed. Press straight; do not hammer against the 1 mm bottom skin.
3. Drop two M3 nuts into every bridge from its open top. Confirm each lies flat
   and cannot spin freely in its pocket.
4. Arrange all four quadrants front-face up in final XY position on four
   equal-height supports, leaving every seam open from below. Keep all four
   quadrants supported throughout steps 5–6.
5. Insert S1, then S2, then S3 upward from below. At each seam, guide both pins
   into the two split features, seat the bridge against both quadrant
   undersides, add its two M3x6 screws from above, and leave them loose.
6. Insert S4 **upward from below as the last bridge**. Do not attach S4 to Q4
   and lower Q4 into place. Both S4 pins must enter while all four quadrants
   remain in final XY position. Photograph S4 halfway inserted and fully seated.
7. Confirm eight screws are installed and loose. Move the assembly so all four
   bridge bottoms sit on the verified flat surface. Tighten only finger-snug in
   this order: S1, S3, S2, S4; repeat the order until uniformly snug. Do not use
   screw torque to pull a visibly open seam closed.
8. Remove the base from the surface, leave it unconstrained for one hour, then
   perform checks 1–3. Continue with checks 4–6 only if they pass.

## Six pass/fail checks

1. **Last bridge and full-loop closure.** S4 inserts and seats using hand
   pressure only; no quadrant is bent, lifted, filed, heated, or forced. All
   four seams close without overlap or visible bow. Measure four diameters at
   0/45/90/135 degrees with a ruler between two square reference blocks:
   `299.5..300.5 mm`, with maximum minus minimum `<=0.5 mm`.

2. **Seam gap and step.** Check each seam at inner edge, mid-radius, and outer
   edge. There must be no overlap or forced closure. A thin receipt-paper strip
   should enter a visible gap without spreading it; three stacked printer-paper
   strips (`~0.30 mm`) must not. Run the straightedge across both sides of every
   seam. If two printer-paper strips plus one receipt-paper strip (`~0.25 mm`)
   fit under it, mark RED or verify with a feeler gauge. This is only a
   household screen for the `0.05..0.30 mm` gap and `<=0.25 mm` step limits.

3. **One-hour free-state flatness.** Lay the unconstrained base front-face up
   on the verified surface and press each quadrant lightly in turn. It must not
   rock. Sweep the straightedge across both diameters and both diagonals. Five
   stacked paper strips (`~0.50 mm`) must not fit anywhere under the
   straightedge. Photograph the worst location with the attempted paper stack.

4. **Three complete service cycles.** Fully disassemble and repeat the exact
   assembly sequence three times. On every cycle S4 must insert without more
   force than cycle 1. RED for cracked/whitened plastic, loose or pulled pins,
   spinning nuts, stripped screws, enlarged holes, permanent seam opening, or
   worsening paper/straightedge results.

5. **Vertical self-weight retention.** After cycle 3, stand the base vertically
   on a folded towel and secure it loosely against falling without squeezing it
   flat. Leave it for 60 minutes. No seam may disengage, shift visibly, or shed
   hardware. Return it horizontal and repeat checks 2–3; both must still pass.

6. **Ten lift/place cycles.** Over a soft surface, lift the base about 50 mm by
   the outer rim of one quadrant, hold three seconds, and place it flat. Use
   Q1, Q2, Q3, Q4, Q1, Q2, Q3, Q4, Q1, Q3. No seam may click, disengage, grow,
   or change step; no pin, nut, or screw may move. Repeat checks 2–3 once more.

If paper thickness is unknown or a measurement sits on a limit, mark the row
`BORDERLINE`, measure with a feeler gauge/caliper, and do not round it to PASS.

## Required photos

1. Eight printed parts plus eight screws, eight nuts, and eight pins.
2. All four quadrants supported in final position with S1–S3 installed.
3. S4 halfway inserted upward, showing the last-bridge path.
4. Finished front and underside views with Q/S labels visible.
5. Worst seam/straightedge measurement and worst one-hour flatness measurement.
6. Base vertical at the start and end of the 60-minute dwell.
7. Final front and underside views after service and lift/place cycles.

## Results

Print record: material `________`  printer `________`  nozzle `____ mm`  
layer `____ mm`  slicer/profile `________________`  date `________`

| Check | Measured / observed result | Photo(s) | PASS / RED |
|---|---|---|---|
| 1. S4 insertion + loop closure + four diameters | `________________________` | `_____` | `_____` |
| 2. Seam gaps and steps | `________________________` | `_____` | `_____` |
| 3. One-hour free-state flatness | `________________________` | `_____` | `_____` |
| 4. Three assembly cycles | `________________________` | `_____` | `_____` |
| 5. 60-minute vertical retention | `________________________` | `_____` | `_____` |
| 6. Ten lift/place cycles | `________________________` | `_____` | `_____` |

Overall B0 result: `PASS / RED`  
Observed failure location or note: `________________________________________`
