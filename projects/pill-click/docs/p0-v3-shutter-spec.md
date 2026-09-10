# P0 v3 printable solid-shutter and lost-motion specification

This document freezes the design interface for the next P0 implementation.
It replaces the apertured exterior shutters and unprintable opaque skins from
P0 v2. It is a design contract only: no CAD implementation is approved by
this document.

P0 v3 remains a manual geometry, fit, closure, rail, and captivity prototype.
Return springs, return magnets, pill-transfer timing, and the push-push latch
are later stages.

## Coordinate and state contract

- Units are millimetres.
- X is left/right.
- Y is rear (`-`) to key/front (`+`).
- Z is bottom (`-`) to top (`+`).
- Shuttle world center is `Y(s) = Y0 + s`, with `Y0 = 4.50`.
- `s=0.00` is the pressed/latched aperture-aligned state.
- `s=13.40` is the released state.
- `s=13.55` is the maximum-pull captivity test state.
- Future P2 may add shuttle-only inward overtravel to `s=-1.00`.
- `q` is shutter travel from its pressed hard stop.

The nominal lost-motion relationship is:

```text
q(s) = 0       for -1.00 <= s <= 0.00
q(s) = s       for  0.00 <= s <= 13.55

relative_lost_motion(s) = s - q(s)
```

P0 operates only over `s=q=0.00..13.40`. The `-1.00 mm` branch reserves
future latch overtravel without forcing either shutter into the rear cover.

## Frozen named variables

### Housing and motion

| Source name | Value | Purpose |
|---|---:|---|
| `housing_size` | 40.00 | Fixed X/Y/Z exterior |
| `latched_center_y` / `Y0` | 4.50 | Shuttle center at `s=0` |
| `shuttle_inward_state` | -1.00 | Future P2 overtravel |
| `pressed_state` | 0.00 | Full aperture alignment |
| `released_state` | 13.40 | Nominal released position |
| `maximum_pull_state` | 13.55 | Captivity test limit |
| `normal_coupling_backlash` | 0.10 max | Allowed `abs(q-s)` while coupled |

### Printable shutter and track cross-section

| Source name | Value |
|---|---:|
| `shutter_web_width` | 25.00 |
| `shutter_web_thickness` | 0.80 |
| `shutter_flange_width` | 27.40 |
| `shutter_flange_thickness` | 0.80 |
| `track_web_width` | 25.40 |
| `track_flange_width` | 27.80 |
| `track_lateral_clearance_per_side` | 0.20 |
| `track_vertical_clearance` | 0.20 |
| `track_floor_clearance` | 0.20 |
| `track_capture_overlap_per_side` | 1.00 |
| `shutter_exterior_recess` | 0.20 |
| `opaque_shroud_thickness` | 0.80 |
| `opaque_shroud_width_x` | 25.40 |
| `shutter_lead_in_length` | 0.80 |
| `track_mouth_extra_width` | 0.40 |
| `track_mouth_extra_height` | 0.20 |

The cross-section equations are:

```text
lateral_clearance = (track_flange_width - shutter_flange_width)/2
                  = (27.80 - 27.40)/2
                  = 0.20 per side

capture_overlap = (shutter_flange_width - track_web_width)/2
                = (27.40 - 25.40)/2
                = 1.00 per side
```

Top Z section:

```text
fixed exterior plane       Z = 20.00
shutter exterior surface   Z = 19.80
shutter web                Z = 19.00 .. 19.80
shutter flange             Z = 18.20 .. 19.00
track floor                Z = 18.00
capture-lip underside      Z = 19.20
fixed opaque shroud        Z = 19.20 .. 20.00
```

The bottom section is the exact mirror:

```text
fixed exterior plane       Z = -20.00
shutter exterior surface   Z = -19.80
shutter web                Z = -19.80 .. -19.00
shutter flange             Z = -19.00 .. -18.20
track floor                Z = -18.00
capture-lip inner face     Z = -19.20
fixed opaque shroud        Z = -20.00 .. -19.20
```

The web, flange, and opaque shroud are each four 0.20 mm layers. All intended
external steps and running clearances are integer multiples of a 0.20 mm
layer height.

Both fixed opaque shrouds span `X=[-12.70, 12.70]`. The released top medicine
opening spans `X=[-11.50, 11.50]`, leaving `1.20 mm/side`. The released bottom
medicine opening spans `X=[-11.00, 11.00]`, leaving `1.70 mm/side`.

## Solid-shutter architecture

The exterior shutters contain no aperture. Each shutter is a solid edge plate:

- At `q=0`, its front edge is behind the corresponding fixed housing port,
  leaving the entire port open.
- As `q` increases, the shutter moves forward.
- At `q=13.4`, solid shutter material covers the fixed port.
- The medicine-container opening has translated forward beneath a separate
  fixed 0.80 mm opaque housing shroud.

This removes the P0 v2 dependency on a 0.05 mm roof/floor skin and removes the
fragile 0.40 mm shutter flange.

### Top fill geometry

| Source name | Value |
|---|---:|
| `fixed_fill_center_y` | 0.50 |
| `fixed_fill_width` | 23.00 |
| `fixed_fill_length` | 10.00 |
| `moving_fill_local_center_y` | -4.00 |
| `moving_fill_width` | 23.00 |
| `moving_fill_length` | 10.00 |
| `top_shutter_local_rear_y` | -22.90 |
| `top_shutter_local_front_y` | -9.60 |
| `top_opaque_shroud_rear_y` | 8.70 |
| `top_opaque_shroud_front_y` | 20.00 |

```text
fixed_fill_interval = [-4.50, 5.50]

top_shutter(q) = [Y0 + q - 22.90,
                  Y0 + q -  9.60]

moving_fill(s) = interval(Y0 + s - 4.00, 10.00)
```

Frozen top intervals:

| State | Shutter world Y | Moving fill world Y |
|---|---|---|
| `s=-1, q=0` | `[-18.40, -5.10]` | `[-5.50, 4.50]` |
| `s=0, q=0` | `[-18.40, -5.10]` | `[-4.50, 5.50]` |
| `s=13.4, q=13.4` | `[-5.00, 8.30]` | `[8.90, 18.90]` |
| `s=13.55, q=13.55` | `[-4.85, 8.45]` | `[9.05, 19.05]` |

Nominal margins:

```text
pressed port gap              = -4.50 - (-5.10) = 0.60
released rear backing margin  = -4.50 - (-5.00) = 0.50
released front backing margin =  8.30 - 5.50    = 2.80
released shroud rear margin   =  8.90 - 8.70    = 0.20
released shroud front margin  = 20.00 - 18.90   = 1.10
maximum-pull shutter gap      =  8.70 - 8.45    = 0.25
```

### Bottom outlet geometry

| Source name | Value |
|---|---:|
| `fixed_outlet_center_y` | 3.20 |
| `fixed_outlet_width` | 22.00 |
| `fixed_outlet_length` | 4.80 |
| `moving_outlet_local_center_y` | -1.30 |
| `moving_outlet_width` | 22.00 |
| `moving_outlet_length` | 4.80 |
| `bottom_shutter_local_rear_y` | -22.90 |
| `bottom_shutter_local_front_y` | -4.30 |
| `bottom_opaque_shroud_rear_y` | 14.00 |
| `bottom_opaque_shroud_front_y` | 20.00 |

The bottom rear edge is deliberately extended to `-22.90`. Both shutters
therefore share the same pressed rear datum and the same short cover stops.

```text
fixed_outlet_interval = [0.80, 5.60]

bottom_shutter(q) = [Y0 + q - 22.90,
                     Y0 + q -  4.30]

moving_outlet(s) = interval(Y0 + s - 1.30, 4.80)
```

Frozen bottom intervals:

| State | Shutter world Y | Moving outlet world Y |
|---|---|---|
| `s=-1, q=0` | `[-18.40, 0.20]` | `[-0.20, 4.60]` |
| `s=0, q=0` | `[-18.40, 0.20]` | `[0.80, 5.60]` |
| `s=13.4, q=13.4` | `[-5.00, 13.60]` | `[14.20, 19.00]` |
| `s=13.55, q=13.55` | `[-4.85, 13.75]` | `[14.35, 19.15]` |

Nominal margins:

```text
pressed port gap              = 0.80 - 0.20     = 0.60
released rear backing margin  = 0.80 - (-5.00)  = 5.80
released front backing margin = 13.60 - 5.60    = 8.00
released shroud rear margin   = 14.20 - 14.00   = 0.20
released shroud front margin  = 20.00 - 19.00   = 1.00
maximum-pull shutter gap      = 14.00 - 13.75   = 0.25
```

## Rear blind-cover and shutter-stop interface

| Source name | Value |
|---|---:|
| `rear_cover_back_y` | -20.00 |
| `rear_cover_front_y` | -18.70 |
| `rear_cover_blind_wall_thickness` | 1.30 |
| `pressed_shutter_rear_y` | -18.40 |
| `rear_cover_general_clearance` | 0.30 |
| `stop_nib_count_per_shutter` | 2 |
| `stop_nib_center_x` | +/-11.00 |
| `stop_nib_width_x` | 2.00 |
| `stop_nib_height_z` | 0.80 |
| `stop_nib_projection_y` | 0.30 |
| `stop_nib_contact_y` | -18.40 |

The cover is installed last. Its continuous blind wall closes both rear-fed
track entries. The wall is `1.30 mm` thick and remains `0.30 mm` clear of both
pressed shutter rear edges except at four intentional compressive stop faces.
The stop nibs project from `Y=-18.70` to `Y=-18.40` and prevent `q<0`.

The stop nibs sit within the flange tracks with `0.20 mm` X/Z running
clearance. They must not reduce the continuous rear ray barrier. No rear tool
hole is permitted in the exterior-review cover.

## Lost-motion dog, socket, and detent

Ownership is frozen: each **shutter owns its solid lug**; the medicine
**shuttle owns the boss, socket, compliant finger, relief, and detent nub**.
Each shutter/shuttle pair uses one preloaded lost-motion coupling:

| Source name | Value |
|---|---:|
| `coupling_lug_length_y` | 1.20 |
| `coupling_socket_length_y` | 2.40 |
| `coupling_lost_motion` | 1.00 |
| `coupling_end_clearance` | 0.10 each end |
| `coupling_transverse_clearance` | 0.20 per side |
| `coupling_lug_width_x` | 3.00 |
| `coupling_lug_height_z` | 0.80 |
| `coupling_socket_width_x` | 3.40 |
| `coupling_socket_height_z` | 1.20 |
| `coupling_boss_width_x` | 5.00 |
| `detent_finger_free_length` | 8.00 |
| `detent_finger_width` | 3.00 |
| `detent_finger_thickness` | 0.80 |
| `detent_root_fillet` | 0.80 |
| `detent_entry_chamfer` | 0.60 |
| `detent_relief` | 1.20 minimum |
| `detent_maximum_deflection` | 0.50 |

```text
socket_length = lug_length + lost_motion + 2*end_clearance
              = 1.20 + 1.00 + 2(0.10)
              = 2.40
```

Using a normalized rear-to-front socket interval `[0.00, 2.40]`:

```text
normal seated lug interval = [0.10, 1.30]
full-inward lug interval    = [1.10, 2.30]
```

The interval direction follows ownership: when the shuttle moves from `s=0`
to `s=-1` while the shutter remains at `q=0`, its socket moves rearward and
the fixed shutter lug appears to advance by `+1.00` inside the socket.

### Lug and socket placement at `s=q=0`

All local Y coordinates below use the shuttle/shutter center datum. World Y
at `s=q=0` is local Y plus `Y0=4.50`. The complete top and bottom coupling
assemblies use a common `coupling_rearward_shift_y=-9.00` relative to the
superseded P0 v2 placement. X and Z coordinates are unchanged.

Top coupling:

```text
shutter lug local XYZ:
  X = [-1.50, 1.50]
  Y = [-20.60, -19.40]
  Z = [17.40, 18.20]

shutter lug world XYZ at q=0:
  X = [-1.50, 1.50]
  Y = [-16.10, -14.90]
  Z = [17.40, 18.20]

shuttle socket local XYZ:
  X = [-1.70, 1.70]
  Y = [-20.70, -18.30]
  Z = [17.20, 18.40]  # open toward the top shutter

shuttle socket world XYZ at s=0:
  X = [-1.70, 1.70]
  Y = [-16.20, -13.80]
  Z = [17.20, 18.40]
```

Bottom coupling is independently located, not merely a Z mirror:

```text
shutter lug local XYZ:
  X = [-1.50, 1.50]
  Y = [-14.60, -13.40]
  Z = [-18.20, -17.40]

shutter lug world XYZ at q=0:
  X = [-1.50, 1.50]
  Y = [-10.10, -8.90]
  Z = [-18.20, -17.40]

shuttle socket local XYZ:
  X = [-1.70, 1.70]
  Y = [-14.70, -12.30]
  Z = [-18.40, -17.20]  # open toward the bottom shutter

shuttle socket world XYZ at s=0:
  X = [-1.70, 1.70]
  Y = [-10.20, -7.80]
  Z = [-18.40, -17.20]
```

The top shuttle-owned boss/keep-out envelope is local
`X=[-2.50,2.50], Y=[-21.30,-10.60], Z=[15.60,18.40]`. At `s=0` its world Y
is `[-16.80,-6.10]`. The bottom boss/keep-out envelope is local
`X=[-2.50,2.50], Y=[-15.30,-4.60], Z=[-18.40,-15.60]`; its `s=0` world Y is
`[-10.80,-0.10]`. The rear-feed housing coupling channels are:

```text
top channel    X=[-2.70,2.70] Y=[-18.70,7.65]  Z=[15.40,18.60]
bottom channel X=[-2.70,2.70] Y=[-18.70,13.65] Z=[-18.60,-15.40]
```

They give `0.20 mm/side` around the boss/keep-out envelope. Every coupling
and track feature remains within `abs(X)<=14.10`; rear-cover snap centers at
`X=+/-16.20` are outside this keep-out. At future `s=-1,q=0`, the top boss
world rear is `Y=-17.80`, retaining `0.90 mm` clearance from the rear cover's
`Y=-18.70` front plane.

The coupling envelopes are separated from the corresponding medicine-opening
ray footprints on Y for every coupled state because both translate by the
same state value:

```text
top moving fill local Y       = [-9.00, 1.00]
top complete boss local Y     = [-21.30, -10.60]
top minimum Y separation      = -9.00 - (-10.60) = 1.60

bottom moving outlet local Y  = [-3.70, 1.10]
bottom complete boss local Y  = [-15.30, -4.60]
bottom minimum Y separation   = -3.70 - (-4.60) = 0.90
```

The X projections intentionally overlap; Y is the positive separating axis.
Therefore dense aperture rays cannot encounter lug, socket, boss, finger,
nub, or relief geometry before reaching the medicine cavity. Minimum required
Y separation is `0.60 mm`; the frozen top/bottom values are `1.60/0.90 mm`.

### Compliant finger definition

The top finger is a shuttle-roof cantilever running toward `-Y`. Its root is
forward, its free tip is rearward, it bends in Z, and its bend axis is X:

```text
top root block local XYZ       = X[-2.30,2.30] Y[-11.80,-10.60] Z[15.60,17.10]
top free beam local XYZ        = X[-1.50,1.50] Y[-19.80,-11.80] Z[16.30,17.10]
top bend axis                  = X through (Y=-11.80, Z=16.70)
top tip datum                  = Y=-19.80
top nub local XYZ              = X[-1.50,1.50] Y[-20.60,-19.80] Z[17.10,17.60]
top relief local XYZ           = X[-1.70,1.70] Y[-20.80,-11.80] Z[15.60,17.30]
top maximum-deflected envelope = X[-1.50,1.50] Y[-20.60,-11.80] Z[15.80,17.10]
```

The bottom finger is the Z-mirrored cantilever with its independent Y
placement:

```text
bottom root block local XYZ       = X[-2.30,2.30] Y[-5.80,-4.60] Z[-17.10,-15.60]
bottom free beam local XYZ        = X[-1.50,1.50] Y[-13.80,-5.80] Z[-17.10,-16.30]
bottom bend axis                  = X through (Y=-5.80, Z=-16.70)
bottom tip datum                  = Y=-13.80
bottom nub local XYZ              = X[-1.50,1.50] Y[-14.60,-13.80] Z[-17.60,-17.10]
bottom relief local XYZ           = X[-1.70,1.70] Y[-14.80,-5.80] Z[-17.30,-15.60]
bottom maximum-deflected envelope = X[-1.50,1.50] Y[-14.60,-5.80] Z[-17.10,-15.80]
```

The nominal finger-to-relief lateral clearance is `0.20 mm/side`; maximum Z
deflection is `0.50 mm`. The `0.60 mm` entry chamfer is on the lug/nub contact
edge. The nub engages a matching underside detent land in the shutter lug.
The `0.80 mm` root fillet is tangent to both the root block and free beam.

The compliant detent holds the shutter lug in the normal seated position so
the coupling drives in both directions with no 1 mm reverse backlash. When a
shutter reaches its `q=0` cover stop and the shuttle continues toward `s=-1`,
the lug cams the shuttle-owned finger into its relief while traversing the
socket. During release, the shutter remains stopped; the lug returns to the
normal interval and must reseat by `s=0`. Further travel produces `q=s`.

The simple maximum surface-strain estimate is:

```text
strain = 3*t*d / (2*L^2)
       = 3*0.80*0.50 / (2*8.00^2)
       = 0.009375
       = 0.94 percent
```

This is below the provisional 3 percent general-FDM limit, but the detent is
not approved without a physical cycling coupon.

## Rear-to-front assembly and lead-ins

The shutters and shuttle are coupled **outside the housing** at `s=q=0`, then
rear-fed as one stack. Let `c` be the common temporary stack-center world Y.
During insertion:

```text
-34.40 <= c <= 4.50

top shutter world Y    = [c - 22.90, c - 9.60]
bottom shutter world Y = [c - 22.90, c - 4.30]

top shutter lug Y      = [c - 20.60, c - 19.40]
top shuttle socket Y   = [c - 20.70, c - 18.30]

bottom shutter lug Y   = [c - 14.60, c - 13.40]
bottom shuttle socket Y= [c - 14.70, c - 12.30]
```

These equations preserve the normal seated lug/socket relationship for the
entire rear-feed sweep. Assembly proceeds from rear `-Y` toward front `+Y`:

1. Outside the housing, set the shuttle and both shutters to `s=q=0` and seat
   both shutter-owned lugs in the shuttle-owned socket/detent assemblies.
2. Treat the three coupled moving parts as one rear-feed stack. The shutter
   `+Y` edge is the insertion-leading edge.
3. Taper only the flange over the first `0.80 mm`: width `25.0 -> 27.4` and
   thickness `0.4 -> 0.8`. Keep the solid closure web at full `0.80 mm`.
4. Flare each fixed track at its `-Y` entrance by `+0.40 mm` width and
   `+0.20 mm` height over `0.80 mm`.
5. Sweep `c=-34.40..4.50` while feeding the coupled stack through the shutter
   tracks, key-face reliefs, four rails, and coupling channels.
6. Install the continuous blind rear cover. The cover supplies the final four
   shutter stop nibs and closes both rear track entrances.
7. Only after cover installation, verify that both shutters contact their
   cover-supplied stops at `q=0`, then verify manual `s=q=0..13.4` motion.

Any moving-land groove-mouth chamfer belongs on the moving land's `+Y` edge,
because that edge leads during rear-to-front insertion.

## Backlash tolerance at release

While coupled, allow `q=s+/-0.10`. At `s=13.40`, this gives
`q=13.30..13.50`.

```text
top shutter rear  = -5.10 .. -4.90
top shutter front =  8.20 ..  8.40

bottom shutter rear  = -5.10 .. -4.90
bottom shutter front = 13.50 .. 13.70
```

The worst acceptable margins remain:

```text
top fixed-port rear backing >= 0.40
top shutter-to-shroud gap    >= 0.30
bottom shutter-to-shroud gap >= 0.30
```

## Executable expected-value assertions

The implementation must encode equivalent assertions rather than copying
unexplained numeric results.

```python
assert Y0 == approx(4.50)

assert shutter_q(-1.00) == approx(0.00)
assert shutter_q(0.00) == approx(0.00)
assert shutter_q(13.40) == approx(13.40)
assert shutter_q(13.55) == approx(13.55)
assert relative_lost_motion(-1.00) == approx(-1.00)
assert relative_lost_motion(0.00) == approx(0.00)

assert coupling_socket_length_y == approx(
    coupling_lug_length_y
    + coupling_lost_motion
    + 2 * coupling_end_clearance
)
assert normal_coupling_backlash <= 0.10
assert top_shroud_x_interval == approx((-12.70, 12.70))
assert bottom_shroud_x_interval == approx((-12.70, 12.70))
assert top_shroud_x_margin_per_side == approx(1.20)
assert bottom_shroud_x_margin_per_side == approx(1.70)

assert coupling_rearward_shift_y == approx(-9.00)
assert top_lug_local_y == approx((-20.60, -19.40))
assert top_socket_local_y == approx((-20.70, -18.30))
assert bottom_lug_local_y == approx((-14.60, -13.40))
assert bottom_socket_local_y == approx((-14.70, -12.30))
assert top_complete_coupling_local_y == approx((-21.30, -10.60))
assert bottom_complete_coupling_local_y == approx((-15.30, -4.60))
assert coupling_socket_length_y == approx(2.40)
assert coupling_socket_width_x - coupling_lug_width_x == approx(0.40)
assert maximum_abs_coupling_x <= 2.70
assert maximum_abs_track_x <= 14.10
assert top_coupling_aperture_y_clearance == approx(1.60)
assert bottom_coupling_aperture_y_clearance == approx(0.90)
assert min(
    top_coupling_aperture_y_clearance,
    bottom_coupling_aperture_y_clearance,
) >= 0.60
assert top_boss_world_y(-1.00)[0] - rear_cover_front_y >= 0.90

assert shutter_web_thickness >= 0.80
assert shutter_flange_thickness >= 0.80
assert opaque_shroud_thickness >= 0.80
assert shutter_exterior_recess == approx(0.20)
assert track_lateral_clearance_per_side == approx(0.20)
assert track_vertical_clearance == approx(0.20)
assert track_floor_clearance == approx(0.20)
assert track_capture_overlap_per_side == approx(1.00)

assert fixed_fill_interval == approx((-4.50, 5.50))
assert top_shutter_interval(0.00) == approx((-18.40, -5.10))
assert top_shutter_interval(13.40) == approx((-5.00, 8.30))
assert top_shutter_interval(13.55) == approx((-4.85, 8.45))
assert moving_fill_interval(0.00) == approx((-4.50, 5.50))
assert moving_fill_interval(13.40) == approx((8.90, 18.90))
assert fixed_fill_interval[0] - top_shutter_interval(0.00)[1] >= 0.60
assert fixed_fill_interval[0] - top_shutter_interval(13.40)[0] >= 0.50
assert top_opaque_shroud_rear_y - top_shutter_interval(13.55)[1] >= 0.25
assert moving_fill_interval(13.40)[0] - top_opaque_shroud_rear_y >= 0.20
assert housing_size / 2 - moving_fill_interval(13.40)[1] >= 1.00

assert fixed_outlet_interval == approx((0.80, 5.60))
assert bottom_shutter_interval(0.00) == approx((-18.40, 0.20))
assert bottom_shutter_interval(13.40) == approx((-5.00, 13.60))
assert bottom_shutter_interval(13.55) == approx((-4.85, 13.75))
assert moving_outlet_interval(0.00) == approx((0.80, 5.60))
assert moving_outlet_interval(13.40) == approx((14.20, 19.00))
assert fixed_outlet_interval[0] - bottom_shutter_interval(0.00)[1] >= 0.60
assert bottom_opaque_shroud_rear_y - bottom_shutter_interval(13.55)[1] >= 0.25
assert moving_outlet_interval(13.40)[0] - bottom_opaque_shroud_rear_y >= 0.20
assert housing_size / 2 - moving_outlet_interval(13.40)[1] >= 1.00

assert rear_cover_front_y - rear_cover_back_y == approx(1.30)
assert pressed_shutter_rear_y - rear_cover_front_y == approx(0.30)
assert stop_nib_contact_y == approx(pressed_shutter_rear_y)
assert estimated_detent_strain <= 0.03

for c in sample(-34.40, 4.50, step=0.10):
    assert top_shutter_feed_interval(c) == approx((c - 22.90, c - 9.60))
    assert bottom_shutter_feed_interval(c) == approx((c - 22.90, c - 4.30))
    assert top_lug_feed_interval(c) == approx((c - 20.60, c - 19.40))
    assert top_socket_feed_interval(c) == approx((c - 20.70, c - 18.30))
    assert bottom_lug_feed_interval(c) == approx((c - 14.60, c - 13.40))
    assert bottom_socket_feed_interval(c) == approx((c - 14.70, c - 12.30))

for q in (13.30, 13.40, 13.50):
    assert fixed_fill_interval[0] - top_shutter_interval(q)[0] >= 0.40
    assert top_opaque_shroud_rear_y - top_shutter_interval(q)[1] >= 0.30
    assert bottom_opaque_shroud_rear_y - bottom_shutter_interval(q)[1] >= 0.30
```

## Required geometry and ray tests

1. Measure actual BREP section thicknesses for both webs, both flanges, both
   fixed opaque shrouds, the rear blind wall, and the four stop nibs.
2. Sample the coupled operational stroke at no more than `0.10 mm` increments
   from `s=q=0.00` through `13.40`, plus exact `13.55` captivity geometry.
3. Sample future lost motion from `s=-1.00..0.00` with `q=0.00` and confirm
   that only the intended dog/socket relative motion occurs.
4. Exclude the four intentional stop contacts from positive-volume collision
   checks; all other fixed/moving intersections must remain below
   `1e-6 mm^3`.
5. At `s=q=0`, dense normal rays across the complete `23x10` fill footprint
   and `22x4.8` outlet footprint must reach the medicine cavity. Repeat the
   full-footprint aperture-ray test at every sampled coupled state in the
   moving medicine-opening frame. The complete top and bottom coupling
   keep-outs must remain Y-disjoint from those footprints by at least
   `1.60 mm` and `0.90 mm`, respectively; minimum permitted is `0.60 mm`.
6. At `s=q=13.4`, rays across both fixed-port footprints must first hit solid
   0.80 mm shutter material at `Z=+/-19.80`.
7. At `s=q=13.4`, rays across both translated medicine-opening footprints
   must first hit the corresponding fixed 0.80 mm opaque housing shroud.
8. Rear rays must cover the complete `40x40` projected rear face. Use an
   `0.50 mm` global cell-center pitch (`80x80 = 6400` rays over
   `X,Z=-19.75..19.75`) plus `0.20 mm` feature-focused pitches over both track
   entries (`X=[-13.90,13.90]`, top `Z=[18.00,20.00]`, bottom
   `Z=[-20.00,-18.00]`) and all coupling-channel projections. Required
   projected solid coverage is `100 percent`; every ray must first hit housing
   or continuous blind-cover material.
9. The only intentional cover/shutter contacts are four zero-volume stop-face
   regions on `Y=-18.40`: top pairs at `X=[-12,-10]` and `[10,12]`,
   `Z=[18.20,19.00]`; bottom pairs at the same X intervals and
   `Z=[-19.00,-18.20]`. Each face is `2.0x0.8=1.6 mm^2`; total intentional
   projected contact area is `6.4 mm^2`. All other cover/shutter intersection
   volumes must be below `1e-6 mm^3`.
10. A dense rear-feed insertion sweep over `c=-34.40..4.50` at no more than
   `0.10 mm` increments must verify shutters, shuttle, key face,
   rail reliefs, coupling features, and cover installation in assembly order.

## Physical validation and caveats

- Print a faithful shutter-track strip before a complete dispenser. The
  recommended coupon is a 32 mm track with a 12 mm slider, 13.4 mm usable
  stroke, and 3.3 mm end margins. A 20 mm body cannot contain a stable 12 mm
  slider over the complete stroke.
- Test both nominal and loose rail coupons independently of the shutter
  coupon.
- Perform repeated full-stroke cycles and normal pull-out retention tests on
  the shutter coupon. Geometry tests do not establish sliding force, bridge
  quality, wear, or flange fatigue.
- Print and cycle the compliant detent separately. Its estimated 0.94 percent
  strain is a screening calculation, not a material-life guarantee.
- The 0.80 mm opaque regions span roughly 25 mm and require sliced-preview and
  physical bridge/opacity review for the selected material and orientation.
- A rigid sliding shutter necessarily leaves a narrow track seam. Acceptance
  means no open path or deep recess, exterior step no greater than 0.20 mm,
  and seams no greater than the specified 0.20 mm running clearance. Literal
  zero-seam closure would require a flexible, rolling, or telescoping cover.
- The sealed exterior configuration uses the blind rear cover. A detachable
  setup wand may be used only while that cover is removed. A rigid 13.4 mm
  through-plunger cannot stay inside the pressed 40 mm envelope and also
  close the released rear face flush.
- P0 v3 does not validate return force, magnet feasibility, push-push latch
  reliability, pill-transfer timing, food-contact suitability, or medical
  performance.
