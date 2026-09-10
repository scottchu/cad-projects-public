# P0 manual-slider specification

P0 is a geometry and fit coupon. It deliberately contains no printed return
spring, return magnet, push-push cam, follower, or pill-transfer gate. It is
not a pill-functional dispenser.

## Coordinate and state contract

- Units: millimetres.
- X: left/right; Y: rear (-) to key/front (+); Z: bottom (-) to top (+).
- Shuttle world center: `Y(s) = Y0 + s`, where `Y0 = 4.50`.
- `s=-1.00`: inward hard-stop contact.
- `s=0.00`: pressed aperture-aligned position.
- `s=13.40`: released design position.
- `s=13.55`: captive-tab maximum pull; 0.15 mm beyond released.

## Frozen named variables

| Intent | Symbol/source name | Value |
|---|---|---:|
| Housing cube | `housing_size` | 40.00 |
| Rear tab channel width | `rear_channel_width` | 37.30 |
| Front guide width | `front_guide_width` | 34.90 |
| Interior height | `interior_height` | 35.20 |
| Front shoulder plane | `front_shoulder_y` | 15.35 |
| Inward key stop plane | `inward_stop_plane_y` | 16.00 |
| Shuttle width/height | `shuttle_width`, `shuttle_height` | 34.20 |
| Medicine wall | `medicine_wall` | 2.00 |
| Fill fixed/moving Y centers | `fill_fixed_center_y`, `fill_moving_local_center_y` | -1.50 / -6.00 |
| Fill Y length | `fill_length` | 10.00 |
| Outlet fixed/moving Y centers | `outlet_fixed_center_y`, `outlet_moving_local_center_y` | 11.50 / 7.00 |
| Outlet Y length | `outlet_length` | 4.80 |
| Ready roof closure zone | `roof_closure_local_*` | -25.40 .. -13.40 |
| Ready floor closure zone | `floor_closure_local_*` | -9.80 .. -3.00 |
| Housing rail count | `rail_count` | 4 |
| Rail Z centers | `rail_z_offset` | +/-9.50 |
| Rail cross-section | `rail_tangential_width` x `rail_radial_height` | 2.20 x 1.20 |
| Nominal groove | `groove_width` x `groove_radial_depth` | 2.70 x 0.65 |
| Loose coupon groove | `groove_width_coupon_loose` | 2.80 |
| Nominal radial clearance | `radial_running_clearance` | 0.20 |
| Tangential clearance | `tangential_clearance_per_side` | 0.25/side |
| Land length | `land_length` | 3.40 |
| Rear/front land local centers | `rear_land_local_y`, `front_land_local_y` | -12.10 / -4.90 |
| Full rail Y interval | `rail_start_y` .. `rail_end_y` | -15.70 .. 15.35 |
| Captive-tab overall width | `captive_tab_overall_width` | 36.90 |
| Tab channel side clearance | derived `tab_side_clearance` | 0.20/side |
| Tab shoulder overlap | derived `tab_shoulder_overlap` | 1.00/side |

The executable source of truth is
`src/pill_click/p0/spec.py`; tests assert every value and equation below.

## Derived equations

```text
Y0 = housing_front - (shuttle_front_local + key_face_thickness)
   = 20.00 - (12.50 + 3.00)
   = 4.50

moving_aperture_world(s) = Y0 + s + moving_aperture_local

overlap(A, B) = max(0, min(Amax, Bmax) - max(Amin, Bmin))

rail_tip_x = groove_bottom_x + radial_running_clearance
           = 17.25 + 0.20 = 17.45

rail_root_x = rail_tip_x + rail_radial_height
            = 17.45 + 1.20 = 18.65

bearing_center_spacing = -4.90 - (-12.10) = 7.20
bearing_end_to_end_span = 7.20 + 3.40 = 10.60

land_interval(s, local_y) =
  [Y0 + s + local_y - land_length/2,
   Y0 + s + local_y + land_length/2]

tab_local_front_y = shoulder_y - (Y0 + maximum_pull)
                  = 15.35 - (4.50 + 13.55) = -2.70
ready_endplay = 15.35 - (4.50 + 13.40 - 2.70) = 0.15
```

## Acceptance checks

1. At `s=0`, both fixed and moving apertures have full 10.0/4.8 mm Y overlap.
2. At `s=13.4`, both overlaps are zero; the fixed top and bottom intervals map
   completely inside their named solid moving-skin closure zones.
3. At `s=-1`, the key rear face contacts the independent Y=16.0 hard stop.
4. Four fixed rails remain inside all eight C-section lands from `s=-1` through
   `s=13.4`; the maximum-pull front-land rail margin is 0.50 mm.
5. Captive tabs have 0.20 mm side clearance, 1.00 mm shoulder overlap, and
   0.15 mm released-state endplay.
6. Housing, rear insert, and shuttle are valid single solids. Sampled static
   poses across the stroke have no positive-volume fixed/moving collision.
7. The shuttle is inserted through the open rear channel before the separate
   rear insert is installed.

STL and 3MF exports are deferred until independent review accepts P0.
