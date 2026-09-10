# P0 mechanical-fit v2 keyboard prototype with inverted rails

This is a separate three-part progressive prototype. It supersedes
`p0_mechanical_fit_v1` for the next print, but V1 source and artifacts remain
unchanged for comparison. All dimensions are millimetres.

V2 evaluates a genuinely keyboard-like exterior and an inverted guide system:
the solid inner button carries four continuous male rails, while the outer
housing contains four rear-open blind female channels. It deliberately removes
the V1 blocky grooved bearing bosses, separate captive tabs, raised stop pads,
and key relief pockets.

## Scope, parts, and separation

Exactly three printed parts are permitted:

1. `p0_mechanical_fit_v2_outer_female_guide_housing`;
2. `p0_mechanical_fit_v2_solid_keyboard_button_male_rails`; and
3. `p0_mechanical_fit_v2_blind_two_side_latch_rear_cover`.

There are no loading or dispensing apertures, shutters, shutter tracks,
couplings, springs, magnets, push-push latch, medicine features, or text. The
front running seam and rear-cover assembly seam are the only permitted seams;
neither is a functional hole.

Use separate implementation paths:

```text
src/pill_click/p0_mechanical_fit_v2_keyboard_inverted_rails/spec.py
src/pill_click/p0_mechanical_fit_v2_keyboard_inverted_rails/geometry.py
src/pill_click/p0_mechanical_fit_v2_keyboard_inverted_rails/print_exports.py
tests/test_p0_mechanical_fit_v2_keyboard_inverted_rails.py
models/p0_mechanical_fit_v2_keyboard_inverted_rails/
```

Do not derive V2 by destructively editing V1 or the canonical dispenser.

## Coordinates, motion, and envelopes

- X is left/right, Y is rear negative to key/front positive, and Z is
  bottom/top.
- Inner placement is `Y_inner(s)=4.50+s`.
- Pressed `s=0.00`; released `s=13.40`; maximum pull `s=13.55`; geometry-only
  inward state `s=-1.00`.
- Rear feed occurs with the cover absent from centre `c=-34.40` through
  `c=4.50`.
- Pressed assembly bounding box is at most
  `X,Y,Z=[-20.00,20.00]` and is exactly 40.00 in each principal dimension.
- Released and maximum front coordinates are `Y=33.40` and `Y=33.55`.

## Why the guide is rectangular

Use a plain rectangular rail/channel section. A T section or dovetail would
reintroduce thin retaining lips, unsupported down-facing ledges, and tighter
FDM sensitivity—the failure mode this revision is intended to remove.

Four opposed rectangular rails provide capture by engagement depth and the
body's limited transverse clearance:

```text
male external radial height       = 1.20
housing/body straight clearance   = 0.20 per side
female channel radial depth       = 1.20
male depth inside channel         = 1.00
maximum total side-to-side shift  = 0.40
minimum opposite-rail engagement  = 1.00 - 0.20 = 0.80
```

With four rails at two Z levels, derailment would require more than 1.00
radial displacement on a side, while the body permits only 0.40 total. These
are geometric capture margins, not a material-strength certification.

## Minimal frozen variables

| Variable | Value |
| --- | ---: |
| `housing_size` | 40.00 |
| `housing_outer_corner_radius_xz` | 4.00 |
| `housing_rear_y` | -18.70 |
| `housing_front_y` | 20.00 |
| `main_guide_size_xz` | 34.60 |
| `main_guide_corner_radius_xz` | 3.20 |
| `front_guide_size_xz` | 35.60 |
| `front_guide_corner_radius_xz` | 4.20 |
| `front_guide_rear_y` | 16.05 |
| `inner_body_size_xz` | 34.20 |
| `inner_body_corner_radius_xz` | 3.00 |
| `inner_body_local_y` | `[-13.00,12.50]` |
| `male_rail_centres_z` | +/-9.50 |
| `male_rail_width_z` | 2.20 |
| `male_rail_external_height_x` | 1.20 |
| `male_rail_local_y` | `[-17.20,-3.20]` |
| `male_rail_source_embed_x` | 0.20 |
| `female_channel_width_z` | 2.60 |
| `female_channel_depth_x` | 1.20 |
| `female_channel_rear_y` | -18.70 |
| `female_channel_blind_front_y` | 14.85 |
| `female_mouth_length_y` | 0.80 |
| `female_mouth_extra_width_z` | 0.40 total |
| `female_mouth_extra_depth_x` | 0.40 |
| `blind_stop_wall_axial_thickness` | 1.20 |
| `key_skirt_size_xz` | 34.20 |
| `key_skirt_corner_radius_xz` | 4.00 |
| `key_face_size_xz` | 32.80 |
| `key_face_corner_radius_xz` | 5.00 |
| `key_local_y` | `[12.50,15.50]` |
| `front_bezel_chamfer` | 1.00 x 45 degrees |
| `side_latch_count` | 2, one per +/-X side |
| `side_latch_width_z` | 6.00 |
| `side_latch_beam_thickness_x` | 1.00 |
| `side_latch_effective_length_y` | 7.50 |
| `side_latch_root_faceplate_overlap_y` | 0.20 |
| `side_latch_beam_radial_x` | `[16.95,17.95]` on +X; mirrored on -X |
| `side_latch_hook_apex_abs_x` | 18.60 |
| `side_latch_hook_protrusion_x` | 0.65 from beam outer face |
| `side_latch_direct_insertion_travel_x` | 0.55 inward |
| `side_latch_required_hook_release_x` | 0.55 +/-0.05 inward |
| `side_latch_pad_release_travel_x` | 0.40 inward |
| `side_latch_pad_squeeze_stop_x` | 0.50 inward |
| `side_latch_pad_load_distance_a` | 6.00 from root tangent |
| `side_latch_pocket_width_z` | 6.40 |
| `side_latch_pocket_depth_x` | 0.55 |
| `side_latch_pocket_y` | `[-10.45,-9.85]` |
| `side_latch_outer_skin_x` | 1.30 |
| `side_latch_pad_size_yz` | 1.70 x 10.00 |
| `side_latch_connector_size_xyz` | 1.05 x 1.70 x 6.00 |
| `side_latch_broad_notch_radial_x` | `[18.10,20.20]` |
| `side_latch_rear_connector_slot_x` | `[16.90,19.00]` |
| `side_latch_rear_connector_slot_y` | `[-18.70,-10.85]` |
| `side_latch_forward_beam_passage_x` | `[16.75,18.15]` |
| `side_latch_forward_beam_passage_y` | `[-11.60,-9.65]` |

## Part 1: rounded outer housing with female channels

The exterior is a rounded-square XZ profile, 40.00 x 40.00 with R4.00
corners, extruded over `Y[-18.70,20.00]`. Add a 1.00 x 45-degree chamfer to
the front exterior perimeter and front guide rim without changing the 40.00
bounding box.

The rear/main guide is a rounded-square opening 34.60 x 34.60, R3.20, from
`Y=-18.90` through `Y=16.05`. This gives the 34.20 rounded inner body 0.20
clearance on every straight side and follows it around the corners as a 0.20
profile offset. The widened front guide is 35.60 x 35.60, R4.20, over
`Y[16.05,20.20]`; it clears the maximum 34.20 key skirt by 0.70 per straight
side. The extra front clearance is cosmetic bezel space, not guide capture.

Four female channels are cut into the +/-X main-guide walls at Z centres
+/-9.50:

- positive-X normal channel `X[17.30,18.50]`; negative-X is mirrored;
- Z intervals `[-10.80,-8.20]` and `[8.20,10.80]`;
- usable Y interval `[-18.70,14.85]`, rear-open and front-blind;
- rear mouth over `Y[-18.70,-17.90]`, widened to 3.00 and deepened to
  `|X|=18.90`.

Normal channel clearance is 0.20 on both Z sides and 0.20 at the male rail
tip. Normal outer wall residual is `20.00-18.50=1.50`. At the short rear mouth
it is `20.00-18.90=1.10`.

The front end of every normal channel is a flat wall at `Y=14.85`. The front
guide does not begin until `Y=16.05`, preserving an exact 1.20 axial stop wall.
Per-channel stop-wall bounding volume is at least
`1.20(1.20)(2.60)=3.744 mm^3`, before union with surrounding housing.

No separate captive throat, side tabs, raised stop pads, or key-face reliefs
are present. The four channel end walls are the only forward captivity stops.

The +/-X housing sides also contain the two rear-cover latch passages, blind
pockets, and rear-open squeeze notches specified under Part 3. These are
mechanical release features at the rear seam, not medicine apertures. The top
and bottom housing walls contain no latch pocket, latch passage, squeeze notch,
or snap access feature.

The outer housing BREP bounding box is
`X[-20.00,20.00] x Y[-18.70,20.00] x Z[-20.00,20.00]`.

## Part 2: solid sculpted keyboard button with male rails

The main inner body is a solid rounded-square 34.20 x 34.20 R3.00 profile over
local `Y[-13.00,12.50]`. It has no modeled cavity, hole, or internal void;
slicer infill controls material use.

The keycap is a centered rounded-square loft:

- rear skirt at local `Y=12.50`: 34.20 x 34.20, R4.00, matching the main
  body's XZ envelope;
- front key face at local `Y=15.50`: 32.80 x 32.80, R5.00;
- inward taper per side: `(34.20-32.80)/2=0.70` over 3.00 Y;
- taper angle from the Y axis: `atan(0.70/3.00)=13.13 degrees`;
- front perimeter blend/chamfer no larger than 1.00, tangent to the loft and
  contained inside the stated bounding box.

This produces a visibly narrower, more rounded key face and a sculpted skirt
while remaining support-friendly when printed on the key face. The full key
loft is contained inside the 34.20 skirt envelope, so it passes through the
34.60 rear/main guide with at least 0.20 straight-side clearance. No key relief
cut is permitted.

### Continuous male rails

Use four clean continuous rail prisms, not separated lands or grooved bosses:

- positive-X source rail `X[16.90,18.30]`; negative-X is mirrored;
- the functional external projection is `X[17.10,18.30]`, exactly 1.20;
- Z intervals `[-10.60,-8.40]` and `[8.40,10.60]`;
- local Y interval `[-17.20,-3.20]`, length 14.00;
- the 0.20 source embed into the rounded body/root region is intentional and
  must survive the final union as positive-volume connectivity.

Do not taper the male rail's positive-Y end: it is the full-area axial stop
face. Entry guidance is provided by the female rear mouth. Cosmetic rail-edge
chamfers may be at most 0.20 and must leave a centered end-contact rectangle at
least 1.00 radial by 1.80 tangential.

The rear 4.20 of each rail extends behind the body. Support it with an integral
spine:

- positive-X spine `X[16.30,17.10]`; negative-X is mirrored;
- local `Y[-17.20,-12.80]`, giving 0.20 body overlap;
- the matching rail Z interval, width 2.20.

The source rail/spine overlap is `0.20(4.40)(2.20)=1.936 mm^3`; the spine/body
overlap is `0.80(0.20)(2.20)=0.352 mm^3`. Face-only attachment fails.

The complete inner local BREP bounding box is
`X[-18.30,18.30] x Y[-17.20,15.50] x Z[-17.10,17.10]`.

## Rail-end captivity equations

The male rail world interval is:

```text
rail_Y(s) = [4.50+s-17.20, 4.50+s-3.20]
          = [s-12.70, s+1.30]
```

| State | Rail Y | Front gap to stop |
| --- | --- | ---: |
| `s=-1.00` | `[-13.70,0.30]` | 14.55 |
| `s=0.00` | `[-12.70,1.30]` | 13.55 |
| `s=13.40` | `[0.70,14.70]` | 0.15 |
| `s=13.55` | `[0.85,14.85]` | 0.00 face contact |

At maximum pull, each rail presents `1.00 x 2.20=2.20 mm^2` of channel-engaged
flat end area. Four rails provide 8.80 total. A distributed 10 N pull therefore
has average contact-stress proxy `10/8.80=1.136 MPa`; even a conservative
two-rail load share gives `10/4.40=2.273 MPa`. These values compare geometry
and load distribution only; they do not certify printed material strength.

The old separate vertical tabs and raised stop guards are explicitly removed.
They may be restored only if physical pull testing shows rail-end wall damage,
unequal load sharing, or front extraction.

## Part 3: rounded blind two-side-latch cover

The rear cover has a 40.00 x 40.00 R4.00 faceplate over
`Y[-20.00,-18.70]` and a rounded-square 34.20 x 34.20 R3.00 internal pilot
over `Y[-18.70,-17.10]`. Pilot/main-guide clearance is 0.20 per straight side.
The rear exterior face is uninterrupted and contains no hole or magnet bore.

No rail relief is needed in the pilot: at installed `s=0`, the male rail rear
is `Y=-12.70`, 4.40 ahead of the pilot front. The pilot remains plain except
where the two side-latch roots require internal relief.

Exactly two reversible cantilever latches retain the cover, one on each X
side and both centred at `Z=0`. Top and bottom have no arm, hook, pocket, or
release feature.

For latch dimensions only, `local_y=global_y-(-18.70)`, so latch local Y=0 is
the housing rear plane and positive local Y points into the housing.

### Side arm, hook, and pocket

The +X arm is:

- straight beam `X[16.95,17.95]`, `Z[-3.00,3.00]`, global
  `Y[-18.70,-9.85]`; the -X arm is mirrored;
- exact R0.80 concave root whose untrimmed source includes the +X overlap
  prism `X[16.95,17.95]`, `Y[-18.90,-17.90]`, Z `[-3.00,3.00]`. Its rear
  `Y[-18.90,-18.70]` strip overlaps the faceplate by exactly 0.20 and
  `1.00(0.20)(6.00)=1.20 mm^3`; its forward
  `Y[-18.70,-17.90]` strip overlaps the straight beam by 0.80 and
  `1.00(0.80)(6.00)=4.80 mm^3`. Apply the R0.80 concave transition without
  trimming either mandatory overlap strip to zero volume;
- root tangent local `Y=0.80`, hook apex local `Y=8.30`, effective length
  `8.30-0.80=7.50`;
- hook polygon in the +X/local-Y plane, extruded over `Z[-3.00,3.00]`, with
  ordered vertices `(17.75,7.85)`, `(18.15,8.25)`, `(18.60,8.25)`,
  `(18.60,8.30)`, and `(17.75,8.75)`; the segment from local Y 8.75 to 8.30
  is the insertion ramp and the local-Y 8.25 face over X `[18.15,18.60]` is
  the positive retention shoulder. Its X `[17.75,17.95]` region overlaps the
  beam by 0.20 and must survive as positive-volume union material;
- hook apex radial coordinate `|X|=18.60`, protruding 0.65 from the beam outer
  face. The -X hook is the exact radial mirror;
- housing pocket radial interval `|X|=[18.15,18.70]`, global
  `Y[-10.45,-9.85]`, and Z `[-3.20,3.20]`.

The pocket supplies 0.20 Z clearance per side, 0.10 radial clearance beyond
the hook apex, 0.10 forward clearance beyond the insertion-ramp tip, and
`20.00-18.70=1.30` remaining exterior side skin. In the seated position, the
pocket rear wall at global `Y=-10.45` contacts the hook's local-Y 8.25
retention face over a projected `0.45(6.00)=2.70 mm^2` per side. This is a
positive axial shoulder rather than a cam-only detent. The two arms are the
complete retention system and engage simultaneously.

Insertion cams the hook directly at distance `L=7.50`; its geometric
surface-strain estimate is:

```text
direct insertion strain = 1.5(1.00)(0.55)/(7.50^2) = 1.47%
```

Manual squeeze acts at the relocated pad centre. Its global Y is -11.90,
local Y is 6.80, and distance from the root tangent is
`a=6.80-0.80=6.00`. Under the conservative point-load-at-pad approximation,
hook/pad displacement amplification and root-strain proxies are:

```text
hook/pad amplification = (3L-a)/(2a)
                       = (3(7.50)-6.00)/(2(6.00)) = 1.375
predicted hook travel at pad release = 1.375(0.40) = 0.550
predicted hook travel at pad stop    = 1.375(0.50) = 0.688
pad-release root strain = 1.5(1.00)(0.40)/(6.00^2) = 1.67%
pad-stop root strain    = 1.5(1.00)(0.50)/(6.00^2) = 2.08%
```

These values correct the invalid assumption that pad travel equals hook
travel. They compare geometry only and do not predict insertion, holding,
pinch, or extraction force. The C5 coupon must measure direct hook-apex travel;
the amplification estimate is not an acceptance substitute.

### Rear-open pinch access and over-deflection stop

Each cover arm carries an exterior finger pad:

- pad global Y `[-12.75,-11.05]`, Z `[-5.00,5.00]`, and radial thickness
  1.00 over `|X|=[18.60,19.60]`;
- the +X connector is exactly `X[17.75,18.80]`,
  `Y[-12.75,-11.05]`, Z `[-3.00,3.00]`; the -X connector is mirrored;
- connector/beam radial overlap is `17.95-17.75=0.20`, while connector/pad
  radial overlap is `18.80-18.60=0.20`; both must remain positive-volume
  unions after final healing;
- the +X housing pad-notch cutter is `X[18.10,20.20]`,
  `Y[-18.70,-10.85]`, Z `[-5.20,5.20]`; the -X cutter is mirrored and the
  0.20 overshoot beyond the exterior guarantees a rear- and side-open notch;
- the +X rear connector-clearance cutter is `X[16.90,19.00]`,
  `Y[-18.70,-10.85]`, Z `[-3.20,3.20]`; the -X cutter is mirrored;
- the +X forward beam-passage cutter is `X[16.75,18.15]`,
  `Y[-11.60,-9.65]`, Z `[-3.20,3.20]`; the -X cutter is mirrored. This gives
  the nominal beam 0.20 radial clearance on both sides and 0.20 forward
  clearance past its end. It ends exactly at the pocket inner plane and does
  not consume any positive volume of the pocket.

The broad notch has a fixed inner stop ledge at `|X|=18.10`. The pad inner
face begins at `|X|=18.60`, so inward pad travel is exactly
`18.60-18.10=0.50`. The rear connector slot supplies flex clearance below the
pad; it may not remove the ledge outside Z `[-3.20,3.20]`. At the commanded
0.40 pad release, direct hook travel must measure 0.55 +/-0.05. The nominal
0.55 result places the hook apex at `|X|=18.05`, giving 0.10 running clearance
inside the pocket/passage inner face. A further 0.10 pad motion reaches the
ledge and prevents over-deflection; its estimated direct hook travel is 0.688.

At the hard stop, each pad retains two ledge-contact wings. Their combined Z
width is `10.00-6.40=3.60`, so the projected stop area is at least
`1.70(3.60)=6.12 mm^2` per side. This area is geometric only; coupon testing
sets the permitted squeeze force.

Because +Y is the cover print-up direction, the radial and Z expansion into
the connector/pad begins on a down-facing surface at `Y=-12.75`. Controlled
support is permitted only on the negative-Y undersides of the connector and
pad. A support blocker must maintain at least 0.50 clearance from the beam,
R0.80 root, hook, pad radial stop faces, housing ledge, and pocket. Support may
not bridge the flex gap or join the pad to the receiver. After removal, no
sanding or knife work may touch any functional flex, latch, or stop surface.

Each notch is open to its X-side exterior and to the rear assembly seam, but
not to the front, top, or bottom exterior. Its remaining fixed inner side
ligament outside the rear connector slot is
`18.10-17.30=0.80`; forward of `Y=-10.85` the normal side wall and 1.30 pocket
skin are uninterrupted outside the narrow Z-localized latch passage. The 0.40
axial wall from the rear-slot front at -10.85 to the pocket rear at -10.45
preserves the positive retention shoulder. The
passage reaches only guide-clearance space behind the solid inner body's rear
plane; this prototype has no medicine void. The cover-owned pad fills the
visible recess when assembled. This localized access is accepted for a
mechanical prototype but is not a sealed or child-resistant feature.

To remove the cover, pinch both pads inward to their release positions, then
push or pull the cover in negative Y. Releasing only one side must not free the
opposite hook.

The cover is installed after rear feeding the button to `s=0`. The rear seam
is an assembly seam, not a functional opening.

The complete cover BREP bounding box, including arms, hooks, connectors, and
pads, is `X[-20.00,20.00] x Y[-20.00,-9.85] x Z[-20.00,20.00]`.
At pressed `s=0`, the solid inner body rear is `Y=4.50-13.00=-8.50`, leaving
`-8.50-(-9.85)=1.35` axial clearance ahead of the cover-arm envelope even
while the arms deflect inward.

### Side-latch force variables and coupon gate

The following full-cover values are measured outputs, not analytic guarantees:

| Measurement | Prototype acceptance gate |
| --- | ---: |
| `F_insert_total` | record; target <=15 N |
| `F_hold_unsqueezed` | withstand 10 N axial pull for 10 seconds |
| `F_pinch_both_total` | record; target <=20 N total |
| `F_extract_squeezed` | record; target <=5 N |
| `permanent_hook_set_after_30` | <=0.20 |

The one-side C5 coupon has stronger explicit gates:

| One-side C5 measurement | Acceptance gate |
| --- | ---: |
| `F_insert_one` | <=7.5 N |
| `F_pinch_one` | <=10 N |
| `F_hold_one_unsqueezed` | one engaged hook withstands 10 N axial pull for 10 seconds |
| `F_extract_one_squeezed` | <=5 N |
| `F_squeeze_at_stop_one` | withstand 10 N inward for 10 seconds with no damage |
| `hook_apex_travel_at_pad_0p40` | 0.55 +/-0.05 |
| `permanent_hook_set_after_30` | <=0.20 |

Before printing the full cover, generate the separate labeled two-part coupon
assembly `C5_V2_one_side_latch_pad_notch_coupon`:

1. `C5_V2_side_latch_arm_cover_specimen`, containing one exact
   arm/root/hook/connector/pad attached only to a reduced cover-side carrier;
2. `C5_V2_side_latch_housing_receiver_specimen`, containing one exact rear
   notch, connector slot, forward beam passage, stop ledge, and blind pocket
   attached only to a reduced housing-side carrier.

The two specimens must be independently moving solids. They may not share a
fused base, bridge, membrane, print-in-place sprue, or common carrier. Reduced
carriers must remain outside the swept functional geometry and may only supply
hand grips or stable print surfaces. This validation assembly does not change
the dispenser's assembled part count of exactly three. Print a second mirrored
two-part coupon assembly if printer orientation is not symmetrical.

Required C5 artifacts are:

```text
models/p0_mechanical_fit_v2_keyboard_inverted_rails/coupons/
  C5_V2_side_latch_arm_cover_specimen.stl
  C5_V2_side_latch_housing_receiver_specimen.stl
  C5_V2_one_side_latch_pad_notch_coupon_assembly.step
```

An optional
`C5_V2_one_side_latch_pad_notch_coupon_two_component.3mf` may package the two
specimens, but it must contain exactly two independently selectable components.

The coupon must complete 30 insertion, latch, squeeze-to-stop, and extraction
cycles. Measure every one-side gate above, directly measure 0.55 +/-0.05 hook
travel at 0.40 pad travel, and verify the 0.50 hard stop. Hold a measured 10 N
inward squeeze against that stop for 10 seconds. Reject cracking, whitening,
delamination, pad/connector damage, pocket breakout, stop damage, or permanent
set above 0.20. Final insertion and pinch forces must remain within 20 percent
of their initial values. Full-cover force limits are set only after coupon
data; the numeric gates are measured usability requirements, not predicted
performance.

### Reviewer reconciliation

The pad-motion critique was valid for the earlier pad centre at `a=4.60` with
0.55/0.65 pad travel: the same point-load approximation would have produced
about 1.95 hook amplification and 3.90/4.61 percent root-strain proxies. That
geometry is removed. The pad is now at `a=6.00`, release/stop pad travel is
0.40/0.50, and direct hook travel is a measured coupon gate.

Critiques that the beam has no corridor clearance, that the pocket has no
positive shoulder, or that C5 is one fused solid refer to superseded geometry.
This frozen revision has 0.20 nominal beam clearance, a 0.40-thick axial web
and 2.70 mm^2 shoulder per side, and two independently moving C5 specimens.

## Deterministic validation

### BREP and dimensions

1. Generate exactly three labeled valid positive-volume single solids.
2. Assert the three stated bounding boxes and pressed 40 x 40 x 40 envelope.
3. Probe rounded-square sizes/radii, front bezel chamfer, key skirt/face loft,
   0.70-per-side taper, 13.13-degree angle, and front/rear planes from real
   BREP geometry. Intersect every sampled key-loft XZ section with the 34.20
   skirt envelope and require zero positive-volume excess.
4. Assert the inner has one connected material region, no modeled void, and no
   forbidden feature or label from the scope exclusion list.
5. Probe all four rail and channel sections independently. Require exact
   width/depth, 0.20 side/tip clearances, 1.50 normal outer wall, 1.10 mouth
   outer wall, 1.20 axial blind wall, and the stated spine overlap volumes.

### Motion and capture

6. Run 292 non-penetrating positions
   `s_i=-1.00+0.05i`, `i=0..291`, including exact pressed, released, and
   maximum-pull states. Unintended fixed/moving intersection volume is
   `<1e-6 mm^3`; at maximum pull the four rail/front-wall intersections are
   zero-volume face contacts. At `s=-1.00`, the skirt rear plane is
   `Y=4.50-1.00+12.50=16.00`, so its first 0.05 lies in the rear/main guide;
   explicitly require at least 0.20 straight-side skirt clearance there and
   zero skirt/guide intersection.
7. Add a 293rd rejection probe at `s=13.60`. It must produce positive-volume
   intersection only at the four rail-end walls and nowhere else. This probe
   proves the stop direction and is not an allowed operating state.
8. At every allowed state, compute each rail's radial and tangential overlap
   with its channel. Minimum radial engagement is at least 0.80 under the full
   permitted transverse body shift. No rigid transform within the guide
   clearance may extract or derail the button.
9. Apply virtual distributed +Y loads at the rail end faces and verify four
   nonzero contact regions totaling at least 8.80 mm^2. Also pass the
   conservative two-contact 4.40 mm^2 case without a geometric bypass path.
10. Remove the rear cover and run exactly 390 rear-feed states
    `c_i=-34.40+0.10i`, `i=0..389`. The rail front faces first enter the
    flared female mouths at `c=-15.50`; unintended intersection is
    `<1e-6 mm^3` at every sample. Independently section the complete body and
    key loft wherever each sample crosses the 34.60 rear/main guide. Require
    maximum key section size 34.20, minimum straight-side clearance 0.20, and
    no need for a key relief cut.
11. Prove by BREP absence tests that no captive tab, stop pad, throat guard, or
    key relief exists. Captivity is supplied only by opposed channel
    engagement and the four blind rail-end walls.

### Cover, exterior, and mesh

12. Back-transform both side latches to their respective C5 arm and receiver
    specimen frames and require symmetric-difference volume `<1e-6 mm^3` for
    every functional feature. Probe exact R0.80 roots, finite
    overlaps, beam/hook/pocket/pad dimensions, 0.55 direct insertion travel,
    0.40 pad release, 0.50 pad stop, 1.30 pocket skin, and all notch residuals.
    Require the root/faceplate and root/beam positive-volume intersections to
    be at least 1.20 and 4.80 mm^3 respectively. Require the
    forward beam-passage/pocket positive-volume intersection to be
    `<1e-9 mm^3` while their X=18.15 boundary faces coincide. Require the
    untouched source pocket volume to be `0.55(0.60)(6.40)=2.112 mm^3` and
    each seated retention-shoulder contact area to be at least 2.70 mm^2.
    Probe the intact 0.40 axial web between rear clearance and pocket.
13. Sweep cover insertion with both undeflected hooks, then their 0.55
    inward-deflection envelopes. In the seated state both hooks are wholly
    inside their pockets and both positive shoulders contact. With one arm
    released and the other engaged, axial removal remains geometrically
    blocked. Drive both pads 0.40 inward, directly measure each hook apex at
    0.55 +/-0.05 inward, and require extraction without unintended
    intersection. Drive both pads to the 0.50 stops and require no geometric
    bypass or over-travel. Assert at least 1.35 axial
    clearance to the pressed solid inner throughout the latch deflection sweep.
14. A deterministic 0.50-pitch rear grid contains 6400 cell-centre probes at
    `x_i=z_i=-19.75+0.50i`, `i=0..79`. Classify each point analytically against
    the exact 40.00 x 40.00 R4.00 footprint using
    `dx=max(|x|-16.00,0)`, `dz=max(|z|-16.00,0)`, and
    `dx^2+dz^2<=4.00^2`. Exactly 6352 probes are in/on the rounded footprint;
    rays cast from behind the rear face in +Y at all 6352 must first intersect
    solid faceplate at `Y=-20.00`. Exactly 48 probes are outside the footprint
    in the four rounded-corner cutaways and must miss the cover by design.
    Require `6352+48=6400` and reject any unclassified point. Blindness is
    evaluated only by the 6352 intended-footprint rays in pressed, released,
    and maximum-pull states; none may pass through the faceplate. The front and
    rear seams are classified separately; the two rear/side-open squeeze
    notches are classified only as mechanical seam access and may reach only
    the guide-clearance space behind the solid button, never a modeled medicine
    void.
15. Assert by BREP absence that the top and bottom contain no latch arm,
    pocket, passage, notch, or release pad. Exactly two hooks and two pockets
    exist, both on +/-X.
16. Export the three dispenser-part STLs and the two separately named C5
    specimen STLs at production tolerances. After a `1e-6` vertex weld and
    removal of zero-area triangles, each of the five STL files has exactly one
    connected closed shell, zero boundary/non-manifold edges, and edge
    incidence exactly two. The two C5 STL triangle sets must be disjoint and
    neither file may contain geometry from the other specimen.
17. Export the C5 STEP assembly with exactly two labeled positive-volume solids:
    `C5_V2_side_latch_arm_cover_specimen` and
    `C5_V2_side_latch_housing_receiver_specimen`. Their functional features
    must mate through relative rigid motion and have no common positive-volume
    carrier intersection. If the optional 3MF is emitted, re-import it and
    require exactly two independently selectable components with the same two
    labels. A fused common-base pseudo-coupon fails.
18. Re-import every mesh, require positive consistently oriented volume, and
    repeat applicable bounding-box, rail/channel, and C5 functional-section
    checks.

## Required visual review packet

Generate snapshots from the viewpoints most useful for the user's marked-up
review:

1. front-right three-quarter, pressed;
2. the identical camera, released;
3. rear-right exploded view with cover removed, showing female mouths and
   continuous male rails;
4. right-side longitudinal section through `Z=+9.50`, released with 0.15 stop
   gap annotated;
5. the same section at maximum pull, showing four flat stop contacts;
6. front orthographic comparison of 40.00 R4.00 bezel, 34.20 skirt, and 32.80
   key face;
7. underside/side close-up proving the old tabs, guards, and block bosses are
   absent;
8. rear-left view of both squeeze pads and rear-open access notches;
9. side section through `Z=0` showing engaged hook, 0.40 pad-release position
   with directly measured 0.55 hook travel, 0.50 pad stop, pocket skin, and
   simple top/bottom walls;
10. rear orthographic footprint audit with the 6352 intended face hits and 48
    deliberate R4 corner misses shown in distinct colours.

## Print and physical acceptance

- Print the housing rear-opening-down with +Y vertical. Use a brim if needed;
  female channels must remain support-free. The 1.20 blind end wall bridges
  only the 2.60 x 1.20 channel section.
- Print the inner on its 32.80 key face with -Y upward. The 13.13-degree taper
  expands gradually, and continuous rails/spines build in the layer plane.
- Print both independently moving C5 specimens first and assemble them only
  after printing. Print the dispenser cover on its exterior rear face with
  both side latches upward in Y. Controlled support may touch only the
  designated negative-Y connector/pad undersides. No support or sanding may
  touch rails, channels, rail stop faces, latch beams, roots, hooks, pad radial
  stop faces, housing ledges, or pockets.
- Use a 0.40 nozzle and the same material, layer height, perimeter count,
  cooling, and slicer infill intended for later prototypes. Scaling is off.
- Measure rail width/height, channel width/depth, all straight-side body gaps,
  stop-wall thickness, and key skirt/face sizes before assembly.
- Rear-feed by hand, install the cover, and complete 100 full manual cycles
  from `s=0` to `s=13.40`. There is no return force or latch.
- Sliding force is at most 8 N, with no spike above 12 N. Record cycles 1, 25,
  50, 75, and 100.
- At cycles 0 and 100, apply a measured 10 N +Y pull for 10 seconds at pressed,
  mid-travel, and released states, then pull gently to the maximum stop. The
  button must remain captive; all four stop faces must show contact witness or
  gauge evidence without crack, whitening, wall breakout, derailment, or
  permanent set.
- Measure total X and Z key play at mid-travel; each is at most 0.50. Verify no
  rail can leave its channel under combined corner pull and 10 N axial load.
- Complete 30 rear-cover cycles after C5 passes. Both hooks seat and withstand
  the unsqueezed 10 N hold. Pinching both pads releases the cover within the
  measured usability gates; pinching only one does not. The cover remains
  flush, the rear stays blind, and top/bottom remain visually simple.

Passing V2 approves only keyboard feel, inverted-guide fit, rail-end
captivity, rear-feed assembly, and cover retention. It does not approve a
medicine path or future return/latch mechanism.
