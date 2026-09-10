# P0 v3 rear-feed, rear-cover, and retention specification

All dimensions are millimetres. X is left/right, Y is rear (-) to
key/front (+), and Z is bottom/top. This document freezes only the rear-feed
assembly path, guide and captive-stop interfaces, rear-open coupling channels,
blind rear closeout, shutter lost motion, and rear-cover retention.

## Motion states

| Variable | Value | Meaning |
| --- | ---: | --- |
| `s_pressed` | 0.00 | P0 pressed/open state |
| `s_released` | 13.40 | P0 released/closed state |
| `s_pull_max` | 13.55 | captive maximum pull |
| `s_future_overtravel` | -1.00 | future shuttle-only latch overtravel |
| `shuttle_center_y_at_pressed` | 4.50 | moving-part center at `s=0` |
| `shuttle_rear_local_y` | -13.00 | shuttle rear face in shuttle coordinates |
| `key_front_local_y` | 15.50 | key front face in shuttle coordinates |

- P0 operational sweep: `0.00 <= s <= 13.55`.
- Future overtravel: the shuttle alone moves to `s=-1.00`; both shutters
  remain at their `s=0` hard stops.
- Moving center: `Y(s) = 4.50 + s`.
- Pressed shuttle rear: `4.50 - 13.00 = -8.50`.
- Future-overtravel shuttle rear: `3.50 - 13.00 = -9.50`.
- Pressed key front: `4.50 + 15.50 = 20.00`.

## Guide and rear-feed section

| Variable | Value |
| --- | ---: |
| `housing_size` | 40.00 |
| `housing_fixed_rear_y` | -18.70 |
| `rear_channel_width` | 37.30 |
| `rear_channel_height` | 35.80 |
| `front_key_guide_width` | 35.60 |
| `captive_stop_throat_width` | 34.90 |
| `key_face_size` | 35.20 |
| `captive_tab_span` | 36.90 |
| `captive_tab_depth` | 3.00 |
| `captive_tab_height` | 5.00 |
| `captive_stop_pad_height` | 5.40 |

Derived clearances and overlaps:

- Rear-channel wall: `(40.00 - 37.30)/2 = 1.35`.
- Key/main-guide clearance: `(35.60 - 35.20)/2 = 0.20` per side.
- Key/rear-channel X clearance: `(37.30 - 35.20)/2 = 1.05` per side.
- Key/rear-channel Z clearance: `(35.80 - 35.20)/2 = 0.30` per side.
- Tab/rear-channel clearance: `(37.30 - 36.90)/2 = 0.20` per side.
- Tab/stop-throat overlap: `(36.90 - 34.90)/2 = 1.00` per side.
- Stop-pad radial width: `(37.30 - 34.90)/2 = 1.20` per side.
- Tab/stop-pad Z overlap margin: `(5.40 - 5.00)/2 = 0.20` per edge.

A globally widened `35.60` guide plus rigid `1.00`-per-side captive tabs is
not geometrically feasible while preserving `1.20` exterior walls and a
positive rear-feed clearance:

```text
required_tab_span >= 35.60 + 2(1.00) = 37.60
required_rear_channel > 37.60
maximum_rear_channel_with_1.20_walls = 40.00 - 2(1.20) = 37.60
```

The frozen solution is therefore a `35.60` main guide with localized `34.90`
captive-stop pads.

## Key-face rail and stop-pad reliefs

Four rail reliefs:

| Variable | Value |
| --- | ---: |
| `key_rail_relief_count` | 4 |
| `rail_z_offset` | +/-9.50 |
| `key_rail_relief_width` | 2.80 |
| `key_rail_relief_depth` | 0.35 |
| `key_rail_relief_rear_y` | 12.30 local |
| `key_rail_relief_front_y` | 15.70 local |
| `rail_tangential_width` | 2.20 |
| `rail_inner_tip_x` | +/-17.45 |

- Tangential clearance: `(2.80 - 2.20)/2 = 0.30` per side.
- Relieved key half-width: `35.20/2 - 0.35 = 17.25`.
- Radial clearance: `17.45 - 17.25 = 0.20`.

Two additional stop-pad passage reliefs:

| Variable | Value |
| --- | ---: |
| `key_stop_relief_count` | 2 |
| `key_stop_relief_edge` | `+X` and `-X` key edges |
| `key_stop_relief_rear_y` | 12.30 local |
| `key_stop_relief_front_y` | 15.70 local |
| `key_stop_relief_min_z` | -2.70 |
| `key_stop_relief_max_z` | 2.70 |
| `key_stop_relief_depth` | 0.35 |

- Stop-pad inner face: `X=+/-17.45`.
- Stop-pad passage clearance: `17.45 - 17.25 = 0.20`.
- Each stop relief is an edge pocket over local
  `Y[12.30,15.70] x Z[-2.70,2.70]`, cut inward `0.35` from its respective
  `+X` or `-X` key edge.
- The key reliefs pass the fixed pads; the unrelieved captive tabs behind the
  key face contact those pads at maximum pull.

## C1R1 strengthened moving rail lands

Physical C1 evidence showed lip fracture and derailment after only a few
slides. The integrated nominal rail interface therefore adopts the C1R1
geometry. C3 and C4 are independent shutter and cover coupons, not later rail
versions. The original C2 remains an independent loose-clearance diagnostic;
it does not replace this strength revision.

| Variable | C1R1 integrated value |
| --- | ---: |
| `rail_tangential_width` | 2.20 |
| `groove_width_nominal` | 2.70 |
| `groove_radial_clearance` | 0.20 |
| `groove_mouth_length` | 0.60 |
| `groove_mouth_extra_width` | 0.40 total |
| `groove_mouth_extra_depth` | 0.30 |
| `land_length` | 6.80 |
| `bearing_boss_width` | 4.30 |
| `normal_lip_per_side` | 0.80 |
| `mouth_lip_per_side` | 0.60 |
| `rear_land_local_center_y` | -13.80 |
| `front_land_local_center_y` | -6.60 |
| `land_center_spacing` | 7.20 |
| `longitudinal_land_gap` | 0.40 |
| `rear_land_backing_radial_thickness` | 0.80 |
| `rear_land_backing_body_overlap_y` | 0.20 |

The primary physical coupon is
`P0_V3_C1R1_nominal_L6p80_lip0p80`. Also print
`P0_V3_C1R1B_nominal_L6p80_lip1p20`, with boss width `5.10`, normal lip
`1.20`, and mouth lip `1.00`. C1R1B is not integrated unless its physical
result is needed; all groove, clearance, mouth, rail, travel, and centre
coordinates remain identical.

The two C1R1 local land intervals are:

```text
rear_land_local_Y  = [-17.20,-10.40]
front_land_local_Y = [-10.00,-3.20]
rear_mouth_local_Y = [-11.00,-10.40]
front_mouth_local_Y= [ -3.80, -3.20]
gap                = -10.00 - (-10.40) = 0.40
```

The shifted centres preserve the two old positive-Y land edges and mouth
locations while adding all new length rearward.

At shuttle state `s`, with center `4.50+s`:

| State | Rear land Y | Front land Y | Total rail engagement |
| --- | --- | --- | ---: |
| `s=-1.00` | `[-13.70,-6.90]` | `[-6.50,0.30]` | 13.60 |
| `s=0.00` | `[-12.70,-5.90]` | `[-5.50,1.30]` | 13.60 |
| `s=13.40` | `[0.70,7.50]` | `[7.90,14.70]` | 13.60 |
| `s=13.55` | `[0.85,7.65]` | `[8.05,14.85]` | 13.60 |

The fixed rail full-depth interval is `Y[-18.00,15.35]`; its rear ramp is
`[-18.70,-18.00]`. Both lands remain fully supported throughout the complete
hard range. At maximum pull, the front edge is `15.35-14.85=0.50` behind the
rail end. At inward overtravel, the rear edge is
`-13.70-(-18.70)=5.00` ahead of the rail entrance, or `4.30` ahead of the
full-depth ramp exit. Total engagement is the complete `2(6.80)=13.60` at
every state, exactly twice the original two-land length. No front overhang is
permitted.

For rear feed at translated shuttle centre `c`:

```text
rear_land_Y(c)  = [c-17.20,c-10.40]
front_land_Y(c) = [c-10.00,c-3.20]
```

At `c=-34.40`, both lands are behind the housing. The front and rear positive-Y
mouths first reach the fixed rail entrance at `c=-15.50` and `c=-8.30`,
respectively. At seated `c=4.50`, their intervals are `[-12.70,-5.90]` and
`[-5.50,1.30]`. The existing rear-feed sweep therefore remains feasible, but
must be rerun against the longer real BREP lands.

The shifted rear land extends `4.20` behind the main shuttle rear
`Y=-13.00`, versus `0.80` in failed C1. Do not leave that length supported
only by the groove-bottom web. Add four rear-land backing ribs:

- positive-X rib `X[16.45,17.25]`; negative-X rib is its mirror;
- local `Y[-17.20,-12.80]`, giving `0.20` finite overlap into the main body;
- primary Z intervals `[-11.65,-7.35]` and `[7.35,11.65]`;
- the rib stops at the groove-bottom radial datum `|X|=17.25` and therefore
  does not reduce the frozen 0.20 rail clearance.

Each primary rib overlaps the main body by
`0.65(0.20)(4.30)=0.559000 mm^3` and its rear bearing boss by
`0.15(4.40)(4.30)=2.838000 mm^3`. Face-, edge-, or point-only attachment is a
failure. If C1R1B is selected, widen the rib with the boss to `5.10`; the
corresponding overlaps are `0.663000` and `3.366000 mm^3`.

Primary C1R1 boss placement:

- positive-X boss radial envelope `X[17.10,17.90]`; negative-X is its mirror;
- Z intervals `[-11.65,-7.35]` and `[7.35,11.65]` at each X side;
- same-side tangential gap between the two bosses: `14.70`;
- outer margin to the 40 mm Z envelope: `20.00-11.65=8.35`;
- clearance to the nearest coupling-channel Z boundary: `15.40-11.65=3.75`;
- clearance to the nearest shutter-track floor: `18.00-11.65=6.35`;
- shutter X half-width is at most `13.70`, leaving
  `17.10-13.70=3.40` X separation from either side boss.
- at future `s=-1.00`, the rear land begins at `Y=-13.70`, still `4.20`
  forward of the cover-root front `Y=-17.90`; at installed `s=0` the gap is
  `5.20`.

For the unselected C1R1B trial, the Z intervals become
`[-12.05,-6.95]` and `[6.95,12.05]`; the corresponding same-side gap is
`13.90`, coupling-channel Z clearance is `3.35`, and shutter-track-floor
clearance is `5.95`. Thus either candidate fits the frozen neighboring
envelopes. The fixed key relief remains `2.80` wide because only the unchanged
`2.20` fixed rail passes through it; the moving boss never uses that relief.

### C1R1 executable assembly assertions

- All eight integrated bearing lands are valid material in one shuttle solid.
  Their rigidly back-transformed normal and mouth sections must match the
  C1R1 coupon with symmetric-difference volume `<1e-6 mm^3`.
- BREP probes must measure `6.80` land length, `4.30` boss width, `2.70`
  groove width, `0.80` normal lips, `3.10` mouth width, `0.60` mouth lips,
  the frozen radial depths, and the positive-Y mouth position on every land.
- Assert the four state intervals and `0.40` inter-land gaps above. Intersect
  each land interval with `Y[-18.00,15.35]` and require total engagement per
  rail `==13.60` throughout `s=-1.00..13.55`.
- Every rear backing rib must have the exact bbox and positive body/boss
  overlap volumes stated above. The fused shuttle remains one connected valid
  BREP solid; no rib may touch its body or boss only at a face.
- Repeat the operational/hard-range sweep at increments no larger than `0.05`
  and the 390-sample rear-feed sweep with the longer lands. Unintended
  rail/land, land/housing, land/key, land/stop, land/coupling, land/shutter,
  land/cover, and land/snap intersection volume is `<1e-6 mm^3` after
  excluding each land's intended fusion to the shuttle.
- At rear-feed entry, first contact must occur only at the widened/deepened
  positive-Y mouth. Probe both entry events at `c=-15.50` and `c=-8.30` and
  reject any back-edge or lip collision.
- Export the strengthened shuttle STL, weld vertices within `1e-6`, discard
  zero-area triangles, and require one connected closed shell, zero boundary
  or non-manifold edges, and incidence two for every undirected edge.
- The complete moving and fixed assembly bounding boxes remain within
  `X,Z=[-20.00,20.00]`; the motion values `13.40` and `13.55` and every key,
  coupling, shutter, cover, and snap datum remain unchanged.
- After the coupon selection, print one strengthened shuttle with all four
  backing ribs. Repeat the 100-cycle and three-position 10 N normal-pull test;
  a coupon result alone cannot approve the 4.20 rear extension.

## Captive-stop coordinates

| Variable | Value |
| --- | ---: |
| `front_shoulder_y` | 15.35 |
| `tab_local_front_y` | -2.70 |
| `tab_local_rear_y` | -5.70 |

Equations:

- `tab_local_front_y = 15.35 - (4.50 + 13.55) = -2.70`.
- `tab_local_rear_y = -2.70 - 3.00 = -5.70`.
- Released tab front: `4.50 + 13.40 - 2.70 = 15.20`.
- Released endplay: `15.35 - 15.20 = 0.15`.
- Maximum-pull tab front: `4.50 + 13.55 - 2.70 = 15.35`.

## Rear-open coupling channels

Both shutters are coupled to the shuttle outside the housing. The complete
three-part moving stack is rear-fed as one unit.

| Variable | Value |
| --- | ---: |
| `coupling_boss_width` | 5.00 |
| `coupling_boss_keepout_height` | 2.80 |
| `coupling_channel_width` | 5.40 |
| `coupling_channel_height` | 3.20 |
| `coupling_channel_clearance` | 0.20 per side |
| `coupling_common_rearward_shift_y` | -9.00 |
| `rear_feed_interface_y` | -18.70 |
| `top_coupling_channel_front_y` | 7.65 |
| `bottom_coupling_channel_front_y` | 13.65 |
| `coupling_channel_rear_lead_in` | 0.40 |

- Top channel section:
  `X[-2.70,2.70] x Z[15.40,18.60]`, or `5.40 x 3.20`.
- Bottom channel section:
  `X[-2.70,2.70] x Z[-18.60,-15.40]`, or `5.40 x 3.20`.
- Top channel interval: `Y[-18.70,7.65]`.
- Bottom channel interval: `Y[-18.70,13.65]`.
- Top front equation:
  `maximum_pull_center + top_boss_local_front + clearance`
  `= 18.05 + (-10.60) + 0.20 = 7.65`.
- Bottom front equation:
  `maximum_pull_center + bottom_boss_local_front + clearance`
  `= 18.05 + (-4.60) + 0.20 = 13.65`.
- Both channels open only at the rear assembly interface and are closed by the
  final blind cover.

## Shutter closure and lost-motion interface

Both shutters use the same rear envelope so the rear cover can use identical
short stop nibs.

| Variable | Value |
| --- | ---: |
| `shutter_local_rear_y` | -22.90 |
| `shutter_pressed_rear_y` | -18.40 |
| `shutter_web_width` | 25.00 |
| `shutter_web_thickness` | 0.80 |
| `shutter_flange_width` | 27.40 |
| `shutter_flange_thickness` | 0.80 |
| `track_web_width` | 25.40 |
| `track_flange_width` | 27.80 |
| `shutter_track_clearance` | 0.20 per side |

Lost-motion coupling:

| Variable | Value |
| --- | ---: |
| `coupling_lug_length_y` | 1.20 |
| `coupling_overtravel` | 1.00 |
| `coupling_end_clearance` | 0.10 at each end |
| `coupling_socket_length_y` | 2.40 |
| `coupling_transverse_clearance` | 0.20 per side |
| `coupling_preload_finger_length` | 8.00 |
| `coupling_preload_finger_width` | 3.00 |
| `coupling_preload_finger_thickness` | 0.80 |
| `coupling_preload_root_fillet` | R0.80 |
| `coupling_preload_entry_chamfer` | 0.60 |
| `coupling_preload_relief` | >=1.20 |
| `coupling_preload_max_deflection` | 0.50 |
| `normal_coupling_backlash` | <=0.10 |

- Socket equation: `1.20 + 1.00 + 2(0.10) = 2.40`.
- For future overtravel, `s_shutter = 0` while
  `-1.00 <= s_shuttle <= 0`.
- For normal operation, `abs(s_shutter - s_shuttle) <= 0.10` for
  `0 < s_shuttle <= 13.40`.
- A plain elongated socket without the preload finger is rejected because it
  creates approximately `1.00` reverse backlash and loses aperture timing.

Exact `q=0` seated world envelopes:

| Feature | X interval | Y interval | Z interval |
| --- | --- | --- | --- |
| top shutter lug | `[-1.50,1.50]` | `[-16.10,-14.90]` | `[17.40,18.20]` |
| top shuttle socket | `[-1.70,1.70]` | `[-16.20,-13.80]` | `[17.20,18.40]` |
| bottom shutter lug | `[-1.50,1.50]` | `[-10.10,-8.90]` | `[-18.20,-17.40]` |
| bottom shuttle socket | `[-1.70,1.70]` | `[-10.20,-7.80]` | `[-18.40,-17.20]` |

The socket/lug transverse clearance is `0.20` on every X and Z side. At
`q=0`, each lug has `0.10` rear Y clearance and `1.10` forward Y reserve for
the `1.00` shutter-stopped overtravel plus `0.10` end clearance.

Corresponding shuttle/shutter-local Y intervals after the common `-9.00`
relocation are:

```text
top_lug_local_Y = [-20.60,-19.40]
top_socket_local_Y = [-20.70,-18.30]
bottom_lug_local_Y = [-14.60,-13.40]
bottom_socket_local_Y = [-14.70,-12.30]
```

Complete shuttle-local boss/keepout envelopes:

| Feature | X interval | Y interval | Z interval |
| --- | --- | --- | --- |
| top boss/finger keepout | `[-2.50,2.50]` | `[-21.30,-10.60]` | `[15.60,18.40]` |
| bottom boss/finger keepout | `[-2.50,2.50]` | `[-15.30,-4.60]` | `[-18.40,-15.60]` |

The housing channels expand each X and Z keepout by `0.20`; the Y limits are
the swept keepout limits clipped only where the moving feature has exited the
fixed housing.

Top preload finger, shuttle-local coordinates:

| Feature | X interval | Y interval | Z interval |
| --- | --- | --- | --- |
| root | `[-2.30,2.30]` | `[-11.80,-10.60]` | `[15.60,17.10]` |
| beam | `[-1.50,1.50]` | `[-19.80,-11.80]` | `[16.30,17.10]` |
| nub | `[-1.50,1.50]` | `[-20.60,-19.80]` | `[17.10,17.60]` |
| relief | `[-1.70,1.70]` | `[-20.80,-11.80]` | `[15.60,17.30]` |
| maximum-deflected finger | `[-1.50,1.50]` | `[-20.60,-11.80]` | `[15.80,17.10]` |

- Top bend axis: X-directed at `Y=-11.80, Z=16.70`.

Bottom preload finger, shuttle-local coordinates:

| Feature | X interval | Y interval | Z interval |
| --- | --- | --- | --- |
| root | `[-2.30,2.30]` | `[-5.80,-4.60]` | `[-17.10,-15.60]` |
| beam | `[-1.50,1.50]` | `[-13.80,-5.80]` | `[-17.10,-16.30]` |
| nub | `[-1.50,1.50]` | `[-14.60,-13.80]` | `[-17.60,-17.10]` |
| relief | `[-1.70,1.70]` | `[-14.80,-5.80]` | `[-17.30,-15.60]` |
| maximum-deflected finger | `[-1.50,1.50]` | `[-14.60,-5.80]` | `[-17.10,-15.80]` |

- Bottom bend axis: X-directed at `Y=-5.80, Z=-16.70`.

### Coupling-to-aperture keepouts

The coupling X projections overlap the port X projections intentionally. Y is
the required separating axis.

| Keepout | Rear boundary | Coupling front | Y separation |
| --- | ---: | ---: | ---: |
| top moving fill, shuttle-local | -9.00 | -10.60 | 1.60 |
| bottom moving outlet, shuttle-local | -3.70 | -4.60 | 0.90 |
| top fixed fill at `s=q=0`, world | -4.50 | -6.10 | 1.60 |
| bottom fixed outlet at `s=q=0`, world | 0.80 | -0.10 | 0.90 |

- The local top separation is `-9.00 - (-10.60) = 1.60` and remains
  invariant whenever `s=q`.
- The local bottom separation is `-3.70 - (-4.60) = 0.90` and remains
  invariant whenever `s=q`.
- At future `s=-1, q=0`, the sockets/fingers move rearward with the shuttle;
  both aperture separations increase by `1.00` while the shutters remain at
  their pressed stops.
- The top and bottom complete coupling keepouts must have intersection volume
  `<1e-6 mm^3` with their full pressed fill/outlet ray prisms.

## Blind rear cover and stepped closeout

| Variable | Value |
| --- | ---: |
| `rear_faceplate_width` | 40.00 |
| `rear_faceplate_height` | 40.00 |
| `rear_faceplate_thickness` | 1.30 |
| `rear_faceplate_exterior_y` | -20.00 |
| `rear_faceplate_interior_y` | -18.70 |
| `housing_fixed_rear_y` | -18.70 |
| `rear_cover_pilot_width` | 36.90 |
| `rear_cover_pilot_height` | 35.30 |
| `rear_cover_pilot_depth` | 1.60 |
| `rear_cover_pilot_front_y` | -17.10 |
| `rear_cover_top_coupling_relief_x` | `[-2.70,2.70]` |
| `rear_cover_top_coupling_relief_y` | `[-18.70,-17.10]` |
| `rear_cover_top_coupling_relief_z` | `[15.40,18.60]` |
| `rear_cover_edge_chamfer` | 0.30 |
| `rear_cover_through_hole_count` | 0 |

- Blind exterior thickness: `1.30 >= 1.20`.
- The fixed housing has no material at `Y < -18.70`; the full faceplate
  replaces the complete envelope slab `Y[-20.00,-18.70]`.
- Pilot X clearance: `(37.30 - 36.90)/2 = 0.20` per side.
- Pilot Z clearance: `(35.80 - 35.30)/2 = 0.25` per side.
- General cover-to-shutter clearance:
  `-18.40 - (-18.70) = 0.30`.
- The full `40.00 x 40.00` faceplate closes the rear ends of both shutter
  tracks and both coupling channels.
- The faceplate has no tool hole, coupling opening, magnet escape path, or
  through-path into the medicine cavity.
- The top coupling relief cuts only the forward pilot, not the `1.30` blind
  faceplate. At future `s=-1`, the top coupling keepout is world
  `X[-2.50,2.50] x Y[-17.80,-7.10] x Z[15.60,18.40]`; the relief provides
  `0.20` X/Z clearance through the pilot and the solid faceplate remains
  `0.90` behind its rear edge: `-17.80 - (-18.70) = 0.90`.
- The fixed housing and faceplate have zero volumetric overlap:
  `volume(housing & faceplate) < 1e-6 mm^3`.
- Their intended interface is the shared plane `Y=-18.70`; the two uninterrupted
  side support strips contribute at least
  `2(1.35)(40.00) = 108.00 mm^2` projected perimeter support before counting
  the remaining top/bottom lands and pilot bearing surfaces.

Intentional shutter hard stops:

| Variable | Value |
| --- | ---: |
| `shutter_stop_nibs_per_shutter` | 2 |
| `shutter_stop_nib_center_x` | +/-11.00 |
| `shutter_stop_nib_width_x` | 2.00 |
| `shutter_stop_nib_thickness_z` | 0.80 |
| `shutter_stop_nib_rear_y` | -18.70 |
| `shutter_stop_nib_front_y` | -18.40 |
| `top_shutter_stop_nib_z` | `[18.20,19.00]` |
| `bottom_shutter_stop_nib_z` | `[-19.00,-18.20]` |

- Only the four nib end faces are intentional shutter contacts.
- All other faceplate and pilot surfaces preserve at least `0.20` shutter
  clearance; the main rear wall provides `0.30`.

## Rear-cover retention

The cover is retained by four long, reversible snap arms. A sliding dovetail
or transverse printed pin is not used because the axial stepped closeout must
enter both shutter tracks straight in `+Y`; a side insertion would conflict
with those closeout interfaces, and transverse pins would add visible side or
bottom access holes.

| Variable | Value |
| --- | ---: |
| `rear_snap_count` | 4 |
| `rear_snap_center_x` | +/-16.20 |
| `rear_snap_effective_length` | 7.50 |
| `rear_snap_width` | 3.60 |
| `rear_snap_bending_thickness` | 1.20 |
| `rear_snap_root_fillet` | R0.80 |
| `rear_snap_root_overlap` | 0.20 |
| `rear_snap_root_relief_cutter_rear_y` | -18.70 |
| `rear_snap_local_rear_y` | 0.00 |
| `rear_snap_local_front_y` | 8.85 |
| `rear_snap_global_rear_y` | -18.70 |
| `rear_snap_global_front_y` | -9.85 |
| `rear_snap_hook_base_rear_y` | 7.75 local |
| `rear_snap_hook_base_front_y` | 8.85 local |
| `rear_snap_hook_apex_y` | 8.30 local |
| `rear_snap_top_beam_outer_z` | 18.15 |
| `rear_snap_bottom_beam_outer_z` | -18.15 |
| `rear_snap_top_hook_apex_z` | 18.70 |
| `rear_snap_bottom_hook_apex_z` | -18.70 |
| `rear_channel_boundary_z` | +/-17.90 |
| `rear_snap_top_receiver_inner_z` | 18.15 |
| `rear_snap_bottom_receiver_inner_z` | -18.15 |
| `rear_snap_nominal_deflection` | 0.55 |
| `rear_snap_worst_deflection` | 0.65 |
| `rear_snap_pocket_outer_z` | +/-18.80 |
| `rear_snap_pocket_width_x` | 4.00 |
| `rear_snap_pocket_rear_y` | -10.95 |
| `rear_snap_pocket_front_y` | -9.85 |
| `rear_snap_pocket_radial_depth` | 0.65 |
| `flared_track_mouth_half_width` | 14.10 |
| `rear_snap_apex_track_clearance_x` | 0.10 |
| `rear_snap_insertion_ramp` | 45 degrees |
| `rear_snap_extraction_ramp` | 45 degrees |

Derived checks:

- Exterior pocket skin: `20.00 - 18.80 = 1.20`.
- Arm/pocket lateral clearance: `(4.00 - 3.60)/2 = 0.20`.
- Positive-X arm interval: `X[14.40,18.00]`.
- Negative-X arm interval: `X[-18.00,-14.40]`.
- Positive-X pocket interval: `X[14.20,18.20]`.
- Negative-X pocket interval: `X[-18.20,-14.20]`.
- Top pocket radial interval: `Z[18.15,18.80]`.
- Bottom pocket radial interval: `Z[-18.80,-18.15]`.
- Top straight beam radial interval: `Z[16.95,18.15]`.
- Bottom straight beam radial interval: `Z[-18.15,-16.95]`.
- The exact V3.1 coupon-local root prism is
  `X[-0.80,0.20] x Y[-0.20,0.80] x Z[-1.80,1.80]`, where local X is the
  radial bending coordinate and local Z is the arm-width coordinate.
- After rigid mapping, the four root-prism bounding boxes are:

  | Root | Assembly bounding box |
  | --- | --- |
  | top, +X | `X[14.40,18.00]`, `Y[-18.90,-17.90]`, `Z[16.15,17.15]` |
  | top, -X | `X[-18.00,-14.40]`, `Y[-18.90,-17.90]`, `Z[16.15,17.15]` |
  | bottom, +X | `X[14.40,18.00]`, `Y[-18.90,-17.90]`, `Z[-17.15,-16.15]` |
  | bottom, -X | `X[-18.00,-14.40]`, `Y[-18.90,-17.90]`, `Z[-17.15,-16.15]` |

- Every root has `0.720000 mm^3` finite overlap with its mapped cover grip and
  `0.576000 mm^3` finite overlap with its mapped straight beam. The exposed
  R0.80 stress relief adds `0.494443 mm^3` to the fused union. The root source
  prism gross volume is `1.790443 mm^3`.
- The pilot cutter that clears each root/beam region begins exactly at
  `rear_faceplate_interior_y=-18.70`, not `-18.71`, and extends only in the
  positive-Y direction. It must remove zero positive volume from the hidden
  root/grip overlap at `Y[-18.90,-18.70]`. This preserves the complete
  `0.20` hidden overlap and the exact `0.720000 mm^3` root/grip intersection.
  Its exact per-root bounds are the relevant arm X interval, global
  `Y[-18.70,-17.09]`, and top radial `Z[16.15,18.15]` or bottom radial
  `Z[-18.15,-16.15]`; `-17.09` is
  `rear_cover_pilot_front_y+0.01`.
- Volume accounting uses distinct baselines:

  ```text
  measured V3 full-cover BREP             = 4230.288099348127 mm^3
  measured V3.1 rootless-cover BREP       = 4227.880800000004 mm^3
  V3.1 addition to its rootless cover     =    1.977770526128 mm^3
  measured V3.1 full-cover BREP            = 4229.858570536589 mm^3
  V3 -> V3.1 full-cover delta              =   -0.429528811538 mm^3
  ```

  The measured full-minus-rootless result is `1.977770536586 mm^3`; its
  `0.000000010458 mm^3` kernel deviation from the analytic value is below the
  `1e-6 mm^3` BREP tolerance. Do not infer the full-cover result from four
  coupon-arm deltas or add `1.977770526128` to the old V3 cover volume.
- Top hook apex/pocket outer clearance: `18.80 - 18.70 = 0.10`.
- Bottom hook apex/pocket outer clearance:
  `(-18.70) - (-18.80) = 0.10`.
- The fixed rear-channel boundary `Z=+/-17.90` is a separate housing datum;
  it is not the C4 receiver inner face.
- Flared shutter-track mouth half-width: `14.10`.
- Arm-to-track X clearance: `14.40 - 14.10 = 0.30`.
- Hook/pocket-to-track X clearance: `14.20 - 14.10 = 0.10`.
- Each blind pocket occupies global `Y[-10.95,-9.85]`, has radial depth
  `0.65`, and preserves the `1.20` exterior skin.
- Nominal insertion deflection maps C4 exactly:
  `18.70 - 18.15 = 0.55` top and
  `(-18.15) - (-18.70) = 0.55` bottom.
- Arm clearance to future-overtravel shuttle:
  `-9.50 - (-9.85) = 0.35`.
- Nominal cantilever surface strain:
  `1.5(1.20)(0.55)/(7.50^2) = 1.76%`.
- Worst-case cantilever surface strain:
  `1.5(1.20)(0.65)/(7.50^2) = 2.08% < 3.00%`.

Retention targets:

- Single-arm and four-arm extraction forces: establish by V3.1 coupon and
  full-cover measurement; geometric strain is not a force guarantee.
- Installation/removal cycle target: `30`.
- Permanent set after cycling: `<=0.20`.

Load path:

```text
rear faceplate -> four arm roots -> four reversible hooks
-> blind pockets in top/bottom housing walls -> 40 mm housing
```

The snap pockets load the `2.10` top/bottom housing walls, not the thinner
`1.35` side walls.

## Assembly order

1. Couple both shutters to the shuttle outside the housing.
2. Seat both shutter lugs in their shuttle sockets at the common stack
   coordinate `q=0`; set the shutters and shuttle to `s=0`.
3. Rear-feed the complete three-part moving stack through `Y=-18.70`.
4. Pass the four fixed rails through the four `2.80 x 0.35` key reliefs.
5. Pass the localized stop pads through the two `5.40 x 0.35` key reliefs.
6. Push the moving stack to `shuttle_center_y=4.50`.
7. Verify `0.15` tab endplay at `s=13.40` and positive retention at
   `s=13.55`.
8. Insert the blind rear cover axially in `+Y` and seat all four reversible
   hooks in their blind top/bottom pockets.
9. Only after the cover is seated, press the stack to the limit and verify both
   shutter rear edges contact only their four designated stop nibs.
10. Recheck pressed aperture alignment, released aperture closure, `0.15`
    captive endplay, and rear blindness.

## Dense rear-feed insertion sweep

| Variable | Value |
| --- | ---: |
| `feed_start_center_y` | -34.40 |
| `feed_end_center_y` | 4.50 |
| `feed_travel` | 38.90 |
| `feed_step` | 0.10 |
| `feed_sample_count` | 390 |
| `feed_shutter_coordinate_q` | 0.00 |
| `feed_translation_at_start` | -38.90 |
| `feed_translation_at_end` | 0.00 |

Equations:

```text
feed_start_center_y = -18.70 - 15.50 - 0.20 = -34.40
feed_travel = 4.50 - (-34.40) = 38.90
c_i = -34.40 + 0.10*i, i = 0..389
q_feed = 0.00
feed_translation(c_i) = c_i - 4.50
```

The rear cover is absent during this sweep. The shuttle and both shutters are
treated as one preassembled moving stack. The shutter mechanism remains built
at its seated operational coordinate `q=0` throughout rear feed. `c` is the
translated world center of that complete stack and
`feed_translation(c)=c-4.50`; at the final `c=4.50`, feed translation is zero.
The coupling lugs remain seated in their sockets for the entire feed.

For every feed coordinate `c`:

```text
shuttle_body_Y(c) = [c - 13.00, c + 12.50]
key_face_Y(c) = [c + 12.50, c + 15.50]
top_shutter_Y(c, q=0) = [c - 22.90, c - 9.60]
bottom_shutter_Y(c, q=0) = [c - 22.90, c - 4.30]
top_lug_Y(c) = [c - 20.60, c - 19.40]
bottom_lug_Y(c) = [c - 14.60, c - 13.40]
top_socket_Y(c) = [c - 20.70, c - 18.30]
bottom_socket_Y(c) = [c - 14.70, c - 12.30]
top_complete_coupling_Y(c) = [c - 21.30, c - 10.60]
bottom_complete_coupling_Y(c) = [c - 15.30, c - 4.60]
```

At `c=-34.40`, `feed_translation=-38.90`; the key front is `-18.90`, which is
`0.20` behind the fixed housing rear plane. The top shutter occupies
`Y[-57.30,-44.00]` and the bottom shutter occupies `Y[-57.30,-38.70]`, so
both remain entirely behind the housing. At `c=4.50`,
`feed_translation=0.00`; the top shutter occupies `Y[-18.40,-5.10]`, the
bottom shutter occupies `Y[-18.40,0.20]`, the key occupies
`Y[17.00,20.00]`, and both couplings are seated at their `q=0` interfaces.
At every `c`, each lug translates with its matching socket, preserving the
same `0.10` rear and `1.10` forward socket allowances during rear feed.
At `c=-34.40`, the top complete coupling is `Y[-55.70,-45.00]` and the
bottom is `Y[-49.70,-39.00]`; both are behind the fixed housing. At `c=4.50`,
they are respectively `Y[-16.80,-6.10]` and `Y[-10.80,-0.10]`, matching the
seated `q=0` world keepouts.

## Executable dimensional and geometry assertions

1. `housing_size == 40.00` in X and Z.
2. `housing_fixed_rear_y == -18.70`; the fixed housing contains no positive
   volume at `Y < -18.70`.
3. Pressed assembly Y envelope is exactly `[-20.00, 20.00]` with the rear
   cover installed.
4. `volume(fixed_housing & rear_faceplate) < 1e-6 mm^3` and their support
   faces are coplanar at `Y=-18.70`.
5. Projected faceplate/housing perimeter support is at least `108.00 mm^2`.
6. `key_face_size <= front_key_guide_width`.
7. Key/main-guide clearance is `0.20` per side.
8. Rail/key-relief radial clearance is `0.20`.
9. Rail/key-relief tangential clearance is `0.30` per side.
10. Each `+X/-X` stop-relief insertion probe over local
    `Y[12.30,15.70] x Z[-2.70,2.70]` clears its fixed stop pad by `0.20` and
    has intersection volume `<1e-6 mm^3` through the rear-feed sweep.
11. Tab/rear-channel clearance is `0.20` per side.
12. Tab/stop-pad overlap is `1.00` per side.
13. Released captive endplay is `0.15`.
14. Maximum-pull tab front equals `front_shoulder_y=15.35`.
15. Coupling bosses clear rear-open channels by `0.20` on every transverse
    side.
16. Both coupling channels begin at `rear_feed_interface_y=-18.70`. The top
    and bottom channel fronts are respectively `7.65` and `13.65`, exactly
    `0.20` beyond their maximum-pull complete boss/finger fronts.
17. At `s=q=0`, the complete top coupling world Y interval is
    `[-16.80,-6.10]` and remains `1.60` behind the fixed fill ray footprint;
    the bottom interval is `[-10.80,-0.10]` and remains `0.90` behind the
    fixed outlet ray footprint.
18. For all coupled states `s=q`, the top and bottom coupling-to-moving-port
    Y separations remain respectively `1.60` and `0.90`.
19. Dense pressed rays over the full `23.00 x 10.00` fill footprint and
    `22.00 x 4.80` outlet footprint reach the medicine cavity without
    intersecting any lug, socket, boss, finger, nub, or finger relief. Each
    coupling/ray-prism intersection volume is `<1e-6 mm^3`.
20. At future `s=-1,q=0`, the top complete coupling world Y interval is
    `[-17.80,-7.10]`; it clears the solid rear faceplate by `0.90` and clears
    the pilot through `X[-2.70,2.70] x Y[-18.70,-17.10] x Z[15.40,18.60]`.
    The bottom complete interval is `[-11.80,-1.10]` and is `5.30` forward of
    the pilot front.
21. Both shutters have pressed rear edge `Y=-18.40`.
22. Main rear wall/shutter clearance is `0.30`.
23. Rear faceplate thickness is `1.30 >= 1.20`.
24. Snap centers are `X=+/-16.20`; arm/track and pocket/track X clearances are
    respectively `0.30` and `0.10`.
25. The coupling-channel outer X datum `2.70` clears the inner snap arm and
    pocket X datums by `14.40-2.70=11.70` and `14.20-2.70=11.50`.
26. C4 maps exactly: top beam outer and receiver inner are `Z=18.15`, top
    apex is `Z=18.70`, and top pocket is `Z[18.15,18.80]`; bottom values are
    their Z mirrors. Pocket depth is `0.65`, apex clearance is `0.10`, nominal
    deflection is `0.55`, and `Z=+/-17.90` remains a separate channel datum.
    Pocket global Y is `[-10.95,-9.85]`, X width is `4.00`, and exterior skin
    is `1.20`.
    The mapped V3.1 roots have the four exact bounding boxes listed in the
    retention section and preserve `root_tangent_y=0.80`.
27. In the coupon-local frame, each of the four root prisms has bbox
    `(-0.80,-0.20,-1.80,0.20,0.80,1.80)`, gross volume
    `1.7904426315`, exposed-relief volume `0.4944426315`, grip-overlap volume
    `0.720000`, and beam-overlap volume `0.576000`, all in mm-based units.
    The root-relief cutter rear boundary is exactly `Y=-18.70`; its
    intersection with the hidden overlap `Y[-18.90,-18.70]` has volume
    `<1e-6 mm^3`.
28. Each cover arm, after all fusions, is one valid connected
    positive-volume BREP solid. Root/grip and root/beam connectivity must be
    volumetric; shared faces, edges, or points alone fail.
29. Inverse-transform all four root/beam/grip regions into the coupon-local
    frame. Pairwise symmetric-difference volume against the C4 coupon region
    is `<1e-6 mm^3`; no root may be independently approximated or repaired.
30. The corrected roots do not change the full arm bbox, `7.50` effective
    length, `3.60` width, `1.20` bending thickness, hook/pocket dimensions, or
    the `1.76%` nominal and `2.08%` worst geometric strain values.
31. Repeat every operational, future-overtravel, and rear-feed unintended-
    intersection test with the corrected roots present. Every newly possible
    root/shuttle, root/shutter, root/track, root/housing, and root/coupling
    intersection outside its intended cover fusion is `<1e-6 mm^3`.
32. Export the fused full cover STL at production chord/angular tolerances.
    After a `1e-6` vertex weld and removal of zero-area triangles, require one
    connected closed shell, zero boundary edges, zero non-manifold edges, and
    incidence exactly two for every undirected edge. Re-imported mesh volume
    is positive and consistently oriented.
    Separately generate the cutter-corrected rootless cover, assert that the
    fused full-cover volume exceeds it by `1.977770526128 mm^3`, then record
    and assert the actual V3.1 full-cover volume and its delta from the measured
    V3 reference `4230.288099348127 mm^3`.
33. Worst-case snap strain is `2.08% < 3.00%`.
34. Snap-arm front-to-future-overtravel-shuttle clearance is `0.35`.
35. At every operational and future-overtravel state, unintended
    arm/shuttle, hook/shuttle, pocket/shuttle, arm/shutter, hook/shutter,
    pocket/shutter, arm/track, hook/track, and pocket/track intersection volume
    is `<1e-6 mm^3`.
36. The rear-feed sweep contains exactly `390` samples.
37. At every rear-feed sample, both lug intervals remain within their seated
    socket envelopes. Every portion of a complete coupling keepout that
    overlaps fixed-housing Y is contained by its rear-open channel with
    `0.20` X/Z clearance, and unintended housing/moving-stack BREP
    intersection volume is `<1e-6 mm^3`.
38. At every operational sample from `s=0.00` through `13.50` in `0.10`
    increments, plus `s=13.55`, unintended pairwise BREP intersection volume
    is `<1e-6 mm^3`.
39. At `s=0`, the load and dispense apertures are fully aligned.
40. At `s=13.40`, both fixed apertures are fully backed by shutter material,
    both moving apertures are under opaque housing, and no load or dispense
    hole is visible. First-hit ray classification over each fixed port must be
    shutter material, never coupling material; over each translated moving
    port it must be the corresponding opaque housing shroud.
41. Rear projected coverage is exactly `40.00 x 40.00 = 1600.00 mm^2`.
42. A `0.50`-pitch rear probe grid at
    `X,Z = -19.75,-19.25,...,19.75` contains `80 x 80 = 6400` probes; every
    `0.10 x 1.50 x 0.10` Y-directed probe intersects solid faceplate.
43. No rear ray reaches a shutter channel, coupling channel, or medicine
    cavity after cover installation.
44. The only intentional cover/shutter contact regions are four rectangles on
    `Y=-18.40`: X intervals `[-12.00,-10.00]` and `[10.00,12.00]`, paired
    with top Z interval `[18.20,19.00]` and bottom Z interval
    `[-19.00,-18.20]`. Each projected
    contact area is `2.00(0.80)=1.60 mm^2`.
45. Excluding those four zero-volume nib face contacts, every
    cover/shutter intersection volume is `<1e-6 mm^3` through the complete
    motion sweep.
46. For future `-1.00` overtravel, shutters remain at `s=0`, the preload
    fingers deflect without exceeding their relief, and the shuttle remains
    collision-free.
47. Every principal printed part is a valid positive-volume single solid.

## Physical acceptance and caveats

- Print a one-arm retention coupon before the full rear cover using the exact
  `7.50 x 3.60 x 1.20`, `R0.80`, `0.55`-engagement section.
- Coupon acceptance: record initial, median, and final extraction force over
  30 complete cycles, with no crack and permanent set `<=0.20`; final force is
  at least 80 percent of initial force.
- Full-cover acceptance: all four hooks audibly or visibly seat, measured
  extraction force is recorded, and the cover remains flush after 30 cycles.
  Production force limits are set only after same-material/process coupon and
  cover data are reviewed.
- The strain equations are geometric beam estimates, not material
  certification. PLA, PETG, layer orientation, moisture, nozzle width, and
  print temperature can materially change retention force and fatigue life.
- The cover snap arms should be printed and coupon-tested in the same material,
  layer orientation, nozzle, layer height, and perimeter count intended for
  the final cover.
- The `0.20` running clearances assume a calibrated FDM printer. C1R1 and
  C1R1B preserve the nominal `2.70` groove; the original `2.80` C2 remains a
  clearance diagnostic only. If nominal clearance is too tight, specify and
  test a long-land C2R1 instead of integrating the weak original C2 geometry.
- The `1.30` blind rear plate is a P0 fit/closure wall, not an impact-rated or
  child-resistant barrier.
- The compliant lost-motion preload finger requires its own cycle coupon
  before it is relied on for future push-push overtravel.
- The common `-9.00` coupling relocation creates rearward shuttle-owned
  cantilevers beyond the main medicine-box rear wall. Their root stiffness,
  print orientation, and accidental assembly loads require a physical coupon;
  the aperture clearances above validate geometry only.
- P0 validates manual pressed/released motion only. Springs, return magnets,
  push-push latch forces, and medicine-use suitability are later-stage tests.
