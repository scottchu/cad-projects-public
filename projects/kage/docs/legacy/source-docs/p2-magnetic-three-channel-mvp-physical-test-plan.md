# P2 magnetic three-channel MVP physical test plan

This is a mechanism test, not an approved clock. Use six Ø6 x 3 mm neodymium
magnets. Keep magnets away from children, pets, implanted medical devices, and
magnet-sensitive items. Verify polarity before seating them.

## Sequence

1. Print and assemble the t1p5 bundle first.
   Confirm all six M3 bolts pass freely through R3, the separator, the integral
   4.0 mm spacer columns, and the base ring before adding rear washers/nuts.
2. Rotate H through 360° while M/S remain parked. Repeat M and S.
3. Set all three to arbitrary angles and sweep each channel again.
4. Command each driver by 90° in both directions and measure follower response.
5. Repeat 100 manual cycles per channel.
6. Repeat the same measurements with t1p0 and t2p0.

## Pass gates

- Selected driver moves only its matching follower through 360°.
- No stall, jump, lift, derailment, or printed-part collision.
- Non-commanded follower motion is less than 2° per commanded 90°.
- Reversal lag is at most 5°.
- No visible damage or retention loss after 100 cycles per channel.
- The follower never leaves its mechanically captured annular track.

Record separator thickness, filament, layer height, magnet source/polarity,
commanded angle, follower angle, lag, unintended follower motion, and failure
notes. CAD clearance tests cannot determine magnetic force or printed friction.
