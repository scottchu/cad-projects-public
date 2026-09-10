# P0 Mechanical Fit V2.2 — Planar Rear Latch

## CAD brief

- Model: source modification and three-part assembly derivative of V2.1.
- Units: millimetres.
- Failure evidence: both old rear-cover cantilevers are printed upward when the
  cover face is on the bed; one root fractured after roughly 5–10 removals.
- Manufacturing assumption: 0.40 mm nozzle, nominal 0.20 mm layers.
- Preserve: four accepted rails, four front rail stops and exact 13.40 mm
  working travel.
- Improve: widen the key skirt to 37.60 mm and retain the shallow spherical
  finger dish so the released button reads as a large mechanical key.
- Replace: both forward, layer-rooted cantilevers with side paddles supported by
  dual beams that flex inside the rear-cover XZ print plane.
- Output: V2.2 inner, rear cover, pressed assembly and released assembly STEP.
- Validation: one solid per part, three assembly solids, nozzle-width feature
  checks, hook engagement/release math, flexure strain, full-travel collision
  tests, STEP inspection and multi-view snapshots.

## Print-driven dimensions

| Feature | Value | 0.40 mm nozzle equivalent |
|---|---:|---:|
| Rear face thickness | 2.40 | 6 diameters |
| Each planar beam | 1.20 | 3 diameters |
| Inner relief slot | 1.20 | 3 diameters |
| Lock tower thickness | 2.40 | 6 diameters |
| Lock tower height | 10.00 | 25 diameters |
| Hook axial length | 1.60 | 4 diameters |
| Hook engagement | 0.60 | 1.5 diameters |
| Housing outer skin | 1.20 | 3 diameters |

The paddle projects 2.40 mm beyond each 40 mm housing side and is 10.00 mm tall
for deliberate two-finger access. Each side uses two 13.50 mm beams. A fixed
0.40 mm nub inside each inner slot creates a real 0.80 mm squeeze stop. The
conservative fixed-guided
surface-strain estimate is:

`strain = 3 × beam_thickness × lateral_travel / beam_length²`

- 0.70 mm release: 1.38%.
- 0.80 mm physical hard stop: 1.58%.
- Resting hook overlap: 0.60 mm.
- Hook clearance at release: 0.10 mm.
- Axial seating clearance: 0.20 mm.
- Receiver retention wall: 0.40 mm.

The key transitions from the 34.20 mm inner body to a 37.60 mm skirt over
0.50 mm, then tapers to a 29.00 mm face across the remaining 7.50 mm height.
The housing opening is 38.00 mm, leaving 0.20 mm radial running clearance and a
nominal 1.00 mm bezel per side at its rear edge.

## Physical acceptance gate

This is geometrically plausible, not a fatigue certification. Before the latch
is accepted for the dispenser, print the cover exterior-face-down with four
walls and verify:

1. Print the rear cover with its exterior face on the bed. Both 1.20 mm slots
   must print open without knife cleanup.
2. 100 simultaneous squeeze cycles show no crack, whitening or more than
   0.15 mm permanent set.
3. 25 complete install/removal cycles do not damage a beam, tower or hook.
4. The seated cover survives a 10 N axial hand-pull and ten upside-down shakes.
5. With both paddles squeezed, the cover can still be removed without a tool.
