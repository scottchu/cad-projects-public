# P2R2 300 mm magnetic MVP — physical test plan

## Gate 0: printer and material

- Confirm the selected printer can place a 300 mm circular part with the chosen
  skirt/brim. A 256 mm bed is an automatic **FAIL / do not slice**.
- Print PETG at the same profile used for prior KAGE running-fit coupons.
- Record actual separator thickness and magnet batch.

## Gate 1: dry mechanical tracks

Test without magnets. Every hidden driver and visible follower must rotate 360°
without binding, lifting, contacting a neighboring channel, or leaving its race.
The cap rings must prevent follower removal until their screws are removed.

Pass:

- all three channels rotate 360° manually;
- no contact at arbitrary H/M/S angles;
- no whitening or cracking after 100 cycles per channel;
- six outer spacer/through paths remain aligned.

## Gate 2: magnetic coupling

Begin with the 1.5 mm separator. Mark all magnet polarities before installation.
Rotate one hidden driver by 90° while observing all followers.

Pass:

- only the matching follower moves;
- non-commanded followers move less than 2°;
- matching follower does not jump, lift, stall, or derail;
- reversal recovers without more than 5° lag.

If coupling is weak, test 1.0 mm. If cross-coupling or drag is high, test 2.0 mm.
Record the selected separator rather than assuming CAD can predict magnet force.

## Gate 3: assembly durability

Cycle each channel 100 full revolutions. Recheck fastener tightness, track wear,
follower capture, magnet retention, and reversal lag. Any loose magnet, cracked
fin, or loss of capture is a failure before integration with the LED subsystem.

