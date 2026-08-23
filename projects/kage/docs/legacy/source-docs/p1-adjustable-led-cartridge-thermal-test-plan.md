# P1 adjustable LED cartridge thermal test plan

## Purpose

Verify the printed PETG carriage, wiring, 40 x 40 x 30 mm heatsink, and nearby
decorative PLA remain within their actual material/component ratings throughout
the 36-86 mm source adjustment. CAD clearance is not evidence of safe operating
temperature.

## Instrumentation and setup

- Use the intended XHP35.2-class LED, 20 x 1.6 mm metal-core PCB, thermal
  interface material, heatsink, constant-current driver, leads, and connectors.
- Measure MCPCB rear contact, heatsink base, hottest fin tip, all four PETG edge clips,
  wire anchor, driver case, and the nearest planned PLA surface. Use attached
  thermocouples; confirm readings against ambient before power-on.
- Keep the modeled 5 mm free-air envelope around all four lateral heatsink sides
  and its rear, except for the four explicit 3 x 6 x 4 mm edge-retention clips
  (288 mm3 total interruption). Keep decorative PLA at least 10 mm away and the
  driver at least 30 mm from the heatsink.
- Test the source at z=36, 40, and 86 mm, plus the warmest-looking intermediate
  position. Orient the clock exactly as installed.

## Procedure

1. Inspect clamp engagement, captive nut retention, pad contact, thermal paste,
   wire bend radius (15 mm minimum), 80 mm U-loop, strain relief, and bridge
   retention. Verify the carriage moves end-to-end without pinching wires.
2. Run at 25%, 50%, 75%, then 100% intended electrical power. At each level,
   log all channels every minute until every channel changes less than 1 C over
   ten minutes, or for 60 minutes, whichever comes first.
3. Repeat at every required source position. Cycle min-to-max ten times while
   warm, then repeat the full-power max-position soak.
4. Block no vents. Separately perform a fault-oriented run with one realistic
   nearby obstruction, watched continuously, to confirm the chosen protection
   trips before any component rating is approached.
5. Power down and record cool-down for 20 minutes. Inspect PETG edge clips, rails,
   bridge, nut pocket, wire insulation, MCPCB seating, and PLA witness coupons
   for creep, gloss change, odor, discoloration, loosening, or distortion.

## Acceptance

- Every measured point remains below the lowest applicable manufacturer rating
  with an additional project safety margin agreed before the test.
- No upward temperature trend remains at the end of a full-power soak.
- No PETG creep, loss of clamp preload, rail binding, wire damage, or visible
  change to a PLA witness coupon occurs.
- Source motion, hard stops, anti-withdraw bridge, and wire bend radius remain
  functional hot and after cool-down.

If any criterion fails, stop using the assembly. Reduce drive current, improve
the heatsink/air path, increase thermal isolation, or change material; then
repeat the complete test. This plan is not a certification or substitute for
component datasheets and electrical protection.

The z=6 mask plane is conceptual, and a 500-1000 mm halo/shadow result is not a
CAD acceptance claim. Verify the actual LED, mask, wall distance, sharpness, and
contrast together during the optical bench test.
