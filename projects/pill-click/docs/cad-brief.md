# Frozen v0 CAD brief: Pill Click single-key prototype

- Model: one rear-installed captive pill key in two strictly separate return
  variants: `pill_click_spring_v0` and `pill_click_magnet_v0_gap_1.2mm`.
- Geometry provenance: independently authored from the agreed behavior and
  dimensions; supplied/reference models are functional inspiration only.
- Units and axes: millimetres; X width, Y rear-to-front actuation, Z up;
  pressing moves the shuttle toward negative Y.
- Fixed body: 40 x 40 x 40 mm housing, rear-open for assembly.
- Shuttle states: `s=0` latched, `s=+13.4` ready, and `s=-1.0` inward hard
  stop. The full ready-to-stop press is 14.4 mm.
- Independent stops:
  - ready tabs are inserted through a 37.3 mm rear channel; their front edge is
    Y=15.4 at ready and is retained behind the Y=15.8 shoulder;
  - the blank keycap rear face meets a separate Y=16.0 counterbore plane at
    `s=-1.0`; neither stop relies on the cam or follower.
- Guide/key: 34.9 mm square front guide; 34.2 x 25 x 34.2 mm medicine shuttle;
  2.0 mm medicine walls; blank 35.2 x 3.0 mm R3.6 key face.
- Transfer sequence:
  - fixed and shuttle outlets are 22 x 4.8 mm, with the shuttle outlet at local
    Y=+7; overlap becomes zero at `s=4.8`;
  - the fixed gate remains closed through `s=5.8`, giving a 4.8..5.8 mm
    both-closed deadband before transfer opens;
  - blade is 22 x 1.9 mm, moving dam is 22.8 x 2.0 mm, vertical overlap is
    0.9 mm, and X edges carry 0.6 mm anti-shear chamfers;
  - 23 x 10 mm top fill apertures align only at `s=0`; at ready the shuttle
    roof covers the housing port with at least 1.0 mm rear overlap.
- Latch: shared external shuttle-mounted heart cam, outside the medicine
  cavity; 3.2 mm plate, 3.0 x 1.7 mm blind groove, 2.2 mm pin, approximately
  4.2 mm branch spacing, state-referenced 13.4 mm stable span plus 1.0 mm
  overtravel. A separate compliant follower selects the asymmetric branches.
- Spring variant: exactly two symmetric replaceable printed serpentine
  springs and no return magnets.
- Magnet-return variant: exactly one centered repelling pair (two 6 x 2 mm
  magnets total), no springs, rear-loaded 6.1 x 2.1 mm pockets, solid caps,
  default minimum hard-stop gap 1.2 mm; source supports 0.8/1.2/1.6 mm shims.
- Fridge mounting in both variants: two independent rear-loaded 6.1 x 2.1 mm
  pockets at X=+/-11.5, Z=0. A solid 0.8 mm rear trap plate captures them and
  the cover preserves an intact front wall toward the medicine mechanism.
- Manufacturing assumptions: FDM prototype, 0.4 mm nozzle, 0.2 mm layers;
  0.35 mm nominal sliding clearance per side. Functional clearances and magnet
  pockets must not be changed by uniform slicer scaling.
- Source: `src/pill_click/`; generators and primary artifacts: `models/`.
- Review targets: labeled positive-volume parts; state/stop/deadband tests;
  STEP facts/planes/positioning; opposed ISO, top/front, and internal section
  snapshots. Physical cycling is still required for follower branch choice,
  spring force, magnet force, pill flow, and wear.

## Deferred from v0

- Weekday text and seven-key rail/backplate customization.
- Print-plate polish and slicer-specific part arrangement.
- Child resistance, moisture seal, dose certification, and medical-device
  claims.
