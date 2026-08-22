# KAGE P3 V0 — motor outer-ring physical gate

This isolated prototype proves one final-radius, motor-driven **second** shadow fin. It does not replace P2R2/P2R3, and it does not yet integrate the LED, ESP32, driver board, hour ring, or minute ring.

## Assembly intent

1. Join the three 120° carrier segments with three top dogbone keys.
2. Insert the carrier before closing the four frame quadrants.
3. Join frame seams with four rear splice plates and eight M3 fasteners.
4. Install two Ø8 mm passive idlers at 1 and 5 o'clock (30° and 150° in the CAD coordinate system), starting at r143.80.
5. Mount the provisional NEMA-8 cradle at 6 o'clock (270°) and start the effective Ø12 mm tire at r145.80.
6. Mount the Hall bracket at 12 o'clock; begin at a 3 mm magnet-to-sensor-face gap.

The three friction contacts are exactly 120° apart and retain the carrier radially. Four outer-sided 45° guide lips provide axial capture and emergency radial clearance while keeping the entire radius below 130 mm empty. Do not infer equal contact force from this geometry; tune all three contacts physically.

## Pass before another ring is added

- 100 manual revolutions without a bind or visible shaving.
- Radial runout at the carrier OD no more than 0.5 mm.
- Tangential step at each dogbone seam no more than 0.2 mm.
- Working compression at drive and both idlers between 0.15 and 0.25 mm; record all three values.
- Carrier cannot translate enough to unload the drive without increasing compression at an opposing idler.
- Breakaway torque no more than 0.010 N·m.
- 24-hour driven run without a skipped revolution or joint separation.
- Home repeatability no worse than 1° after power-up.
- Bidirectional repeatability no worse than 2° after 100 reversals.
- Hall detection 100/100 passes at the chosen gap.
- Record motor/guide noise at 1 m and PETG temperature near the motor cradle.

Friction coefficient, tire material, dynamic torque, noise, Hall threshold, and purchased-part fit are physical-test results. CAD math does not prove them.

## Purchased-part hold points

- Motor reference is StepperOnline `8HS15-0604S`; measure the delivered pilot, shaft flat, face, and wire exit before final-fit CAD.
- The DRV5032 PCB is a provisional 15 × 10 × 5 mm envelope. Measure the real module and the sensor die location before freezing holes.
- The Ø3 × 2 mm Hall magnet pocket is rear-open and leaves 0.85 mm of solid PETG in front.
