# P2R3 Module B — r135 inset-rail coupon

This isolated coupon answers one question before the 300 mm cassette is
redesigned: can the P2R2-sized second follower run, remain captured, and be
removed through a screwed service gate in a one-piece printed C-slot?

## Exactly three printable parts

1. `main_rail_coupon`: 110° r135 PETG rail, integral rear web/lips, loading
   window, two M2 pilot ears.
2. `second_follower_fin`: 9 mm shoe, two 4.2 mm yaw lands, pointed 50 mm fin,
   Ø6.15 × 3.10 mm post-breakout magnet pocket with a true 0.40 mm roof.
3. `removable_gate`: 12° exact-profile rail insert with two Ø2.2 M2 holes.

The main rail fits a 256 mm bed: 76.81 × 237.56 mm before brim and less than
248 mm on its long axis with a 5 mm brim. Print the main rail and follower rear
faces on the bed. The exported gate is deliberately rotated onto one radial
seam face: this turns the former 6.7 mm tab cantilevers into continuous vertical
walls. Its maximum curvature drift is under 0.05 mm per 0.20 mm layer; the only
horizontal bridge is the 2.2 mm M2 hole. Print in PETG with a 0.4 mm nozzle,
0.2 mm layers, four walls, and no supports. Do not auto-orient the supplied 3MF.

## Assembly

1. Punch out the 0.2 mm sacrificial magnet membrane from the follower rear.
2. Install one Ø6 × 3 mm magnet into the Ø6.15 × 3.10 mm pocket.
3. Remove the gate and insert the follower through the r128..142 loading window.
4. Rotate the follower away from the window.
5. Install the gate with two M2 screws into the Ø1.6 × 4 mm pilots. Do not
   overtighten printed pilots.

## Physical pass/fail plan

- Hand-slide the follower through at least 98° without a hard spot.
- With the gate installed, pull the fin forward at the loading position; the
  shoe must remain captured.
- Remove the gate; the follower must lift out without flexing the rail.
- Run 100 full sweeps and reject visible shaving, cracks, or a seam catch.
- Test driver-to-follower magnetic gaps of 1.7, 2.0, and 2.4 mm.
- At each gap, record angular lag, unintended motion, and whether the follower
  can reverse direction without sticking.

CAD validates only geometry, capture, and nominal clearances. It does not prove
printed friction, M2 pilot life, magnetic coupling, or clock-movement torque.
