# P3 V3 MR84 profiled-spool tower successor

This is an isolated successor to the accepted `p3_v3_keeper_fix` assembly. It
reuses the keeper-fix ring geometry unchanged and replaces ring radial support
with three serviceable roller towers at 60, 180, and 300 degrees. The motor
stations remain at 0, 120, and 240 degrees and transmit torque only.

## Handoff files

- `p3_v3_mr84_spool_tower_assembled.step` - complete working-position assembly
- `p3_v3_mr84_spool_tower_service.step` - exploded service-position assembly
- `staged/` - separately generated stationary/hour/minute/second modules used
  to compose both complete STEP files in fresh Python processes

Regenerate with:

```sh
uv run python p3_v3_mr84_spool_tower_export.py all
```

## Tower architecture

Each of the three towers carries three independent MR84ZZ bearings and three
free-running profiled spools at Z = -2.90, 2.65, and 8.20 mm. Two towers use
round fixed datums. The 300-degree tower has 0.10 mm total radial adjustment
(axle radius 126.35-126.45 mm). Each 3.985 mm shoulder axle is supported at
both ends, with a removable upper yoke and an M3 threaded retainer.

The spool groove gives the accepted ring flange 0.15 mm axial float in either
direction. A 12.6 mm belt land establishes a 0.05-0.15 mm radial running gap;
14.4 mm lips provide at least 0.75 mm nominal radial capture.

## Assembly order for one tower

1. Fasten the printed lower tower to the chassis with two M3x10 screws. Leave
   only the adjustable tower loose enough for its final radial setting.
2. Seat the lower 0.20 mm shim and lower 6/4.1 x 2.55 mm spacer on the axle.
3. Install, bottom to top, the hour, minute, and second MR84ZZ/spool pairs. The
   bearings remain separate from the spools; do not glue the bearing races.
4. Add the upper 0.20 mm shim and upper spacer, then seat the 6 mm axle shoulder.
5. Install the removable upper yoke with two M3x8 screws.
6. Install the M3 threaded retainer without clamping the rotating stack.
7. Set the adjustable tower so all three spools freewheel with no detectable
   ring lift, then tighten its two M3x10 base screws.

## Per-clock bill of materials

- 9 x MR84ZZ bearings, 4 x 8 x 3 mm
- 9 x printed or low-friction machined profiled spools
- 3 x 3.985 mm two-end-supported shoulder axles with M3 internal thread
- 6 x spacers, 6 mm OD / 4.1 mm ID / 2.55 mm long
- 6 x 0.20 mm inner-race shims
- 6 x M3x10 base screws
- 6 x M3x8 yoke screws
- 3 x M3 threaded retainers
- 3 x printed lower towers and 3 x printed removable upper yokes

## Required physical gates

CAD checks cannot validate printed fit, noise, wear, or debris behavior. Before
release, print an 8 mm bore coupon (recommended 7.90/8.00/8.10 mm variants),
verify each spool freewheels after installation, check axle deflection and ring
retention under a 5 N pull, confirm seam crossing without lift or sag, and run a
long-duration drive test while monitoring noise, temperature, dust, and wear.

One numerical conflict remains explicit: at the specified outward axle radius
of 126.45 mm, the specified 14.4 mm lip overlaps the unchanged keeper neck by
about 0.0349 mm3 per spool. The inward 126.35 mm position is clear. Resolve this
before treating the outward slot limit as a usable running position.
