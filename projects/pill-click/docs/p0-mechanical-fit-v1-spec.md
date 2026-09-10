# P0 mechanical-fit v1 keyboard prototype specification

This is a separate progressive mechanical prototype, not a mutation or export
variant of the canonical pill dispenser. It validates only keyboard-style
motion, rail durability, front captivity, rear-feed assembly, and rear-cover
retention. All dimensions are millimetres.

## Scope and artifacts

Exactly three printed parts are permitted:

1. `p0_mechanical_fit_v1_outer_housing`;
2. `p0_mechanical_fit_v1_solid_inner_button`; and
3. `p0_mechanical_fit_v1_snap_rear_cover`.

The prototype contains no loading or dispensing apertures, shutters, shutter
tracks, couplings, springs, magnets, push-push latch, medicine text, weekday
text, or other functional opening. The front running seam and rear-cover
assembly seam are permitted seams, not dispensing holes. The inner button has
no modeled cavity, void, or exterior opening.

Keep source, tests, and generated artifacts separate:

```text
src/pill_click/p0_mechanical_fit_v1/spec.py
src/pill_click/p0_mechanical_fit_v1/geometry.py
src/pill_click/p0_mechanical_fit_v1/print_exports.py
tests/test_p0_mechanical_fit_v1.py
models/p0_mechanical_fit_v1/
```

Generation and tests use the project's UV environment. Do not import a
canonical complete dispenser and subtract features from it; build these three
parts directly from the variables below.

## Coordinates and motion

- X is left/right, Y is rear negative to key/front positive, and Z is
  bottom/top.
- The fixed outer housing occupies `X,Z=[-20.00,20.00]` and
  `Y=[-18.70,20.00]`.
- The rear cover exterior is `Y=-20.00`; its interior face is `Y=-18.70`.
- Inner placement is `Y_inner(s)=4.50+s`.
- Pressed state is `s=0.00`, released state is `s=13.40`, captive maximum pull
  is `s=13.55`, and the geometry sweep also includes future inward state
  `s=-1.00`.
- Rear feed translates the complete inner button from centre `c=-34.40` to
  `c=4.50` with the rear cover absent.

Pressed assembly bounds are exactly `X,Y,Z=[-20.00,20.00]`. Released and
maximum-pull front coordinates are respectively `Y=33.40` and `Y=33.55`;
this protrusion is the intended keyboard-button travel and does not enlarge the
pressed 40 x 40 x 40 envelope.

## Shared minimal variables

| Variable | Value |
| --- | ---: |
| `housing_size` | 40.00 |
| `housing_fixed_rear_y` | -18.70 |
| `rear_channel_width` | 37.30 |
| `rear_channel_height` | 35.80 |
| `front_key_guide_width` | 35.60 |
| `front_shoulder_y` | 15.35 |
| `captive_stop_throat_width` | 34.90 |
| `key_face_size` | 35.20 |
| `key_face_thickness` | 3.00 |
| `inner_body_width_xz` | 34.20 |
| `inner_body_rear_local_y` | -13.00 |
| `inner_body_front_local_y` | 12.50 |
| `captive_tab_span` | 36.90 |
| `captive_tab_local_y` | `[-5.70,-2.70]` |
| `captive_tab_height_z` | 5.00 |
| `rail_z_centres` | +/-9.50 |
| `rail_radial_height` | 1.20 |
| `rail_tangential_width` | 2.20 |
| `rail_global_y` | `[-18.70,15.35]` |
| `rail_rear_ramp` | 0.70 |
| `nominal_groove_width` | 2.70 |
| `nominal_radial_clearance` | 0.20 |
| `land_length` | 6.80 |
| `bearing_boss_width` | 4.30 |
| `normal_lip_per_side` | 0.80 |
| `mouth_length` | 0.60 |
| `mouth_width` | 3.10 |
| `mouth_lip_per_side` | 0.60 |
| `rear_land_local_center_y` | -13.80 |
| `front_land_local_center_y` | -6.60 |
| `rear_backing_rib_radial_thickness` | 0.80 |
| `rear_backing_rib_body_overlap_y` | 0.20 |

## Part 1: plain outer housing

Begin with the fixed exterior box
`X[-20.00,20.00] x Y[-18.70,20.00] x Z[-20.00,20.00]`. Cut only the
interfaces required for the inner button and cover:

- rear channel `X[-18.65,18.65] x Y[-18.90,15.35] x
  Z[-17.90,17.90]`;
- front key guide `X[-17.80,17.80] x Y[15.35,20.20] x
  Z[-17.90,17.90]`;
- localized front stop throat `34.90` wide, using the canonical `1.20` side
  stop pads and `5.40` Z height;
- four fixed side rails at `X=+/-17.45..+/-18.65`, centred at
  `Z=+/-9.50`, width `2.20`, with rear ramp
  `Y[-18.70,-18.00]` and full section through `Y=15.35`;
- four blind C4 receiver passages and pockets using the rear-cover snap
  coordinates below.

Do not create shutter slots, top/bottom apertures, coupling channels, or
medicine openings. Apart from the front running seam and rear assembly seam,
all six exterior directions remain backed by solid housing, solid inner
button, or solid rear faceplate.

## Part 2: plain captive solid inner button

The main body is one solid CAD region over
`X,Z=[-17.10,17.10]`, local `Y[-13.00,12.50]`. Model no internal cavity,
shell subtraction, cross web, drain, or hidden void. Material usage and mass
are controlled only by slicer infill and perimeter settings; they are not CAD
geometry.

The plain key cap is `X,Z=[-17.60,17.60]`, local
`Y[12.50,15.50]`. Cosmetic edge rounding may be at most R2.00 and must not
change its bounding box, guide clearances, rear datum, or front plane. No text
or inset is modeled.

Front captivity uses two side tabs extending to `X=+/-18.45`, local
`Y[-5.70,-2.70]`, `Z[-2.50,2.50]`. At released state the tab front is
`Y=15.20`; maximum pull places it at the fixed shoulder `Y=15.35`, giving
`0.15` released endplay and preventing front extraction.

### Strengthened C1R1 rails and backing

Use eight grooves on two longitudinal lands for each of four fixed rails. The
local intervals are:

```text
rear land   [-17.20,-10.40]   mouth [-11.00,-10.40]
front land  [-10.00, -3.20]   mouth [ -3.80, -3.20]
inter-land gap = 0.40
```

Positive-X boss envelope is `X[17.10,17.90]`; negative-X is its mirror.
Primary Z boss intervals are `[-11.65,-7.35]` and `[7.35,11.65]`. Normal
grooves retain 0.80 lips per side; the unchanged widened mouth retains 0.60.

The rear lands extend 4.20 behind the main body and require four backing ribs:

- positive-X rib `X[16.45,17.25]`; negative-X is its mirror;
- local `Y[-17.20,-12.80]`;
- the matching 4.30-wide Z boss interval.

Each rib overlaps the body by `0.559000 mm^3` and its boss by
`2.838000 mm^3`. The rib stops at the groove-bottom datum `|X|=17.25`,
preserving the 0.20 radial rail clearance.

The complete inner-button local bounding box, including lands and tabs, is
`X[-18.45,18.45] x Y[-17.20,15.50] x Z[-17.60,17.60]`. The X extreme is
set by the two captivity tabs; the Z extreme is set by the 35.20 key cap.

## Part 3: blind snap rear cover

The cover is a solid exterior faceplate
`X,Z=[-20.00,20.00]`, `Y[-20.00,-18.70]`, plus an internal pilot
`X[-18.45,18.45]`, `Z[-17.65,17.65]`, `Y[-18.70,-17.10]`.
Its exterior rear face has no holes, pockets, or magnet bores.

Internal pilot reliefs may exist only where required to pass the four fixed
rails and the four snap roots. Every such relief begins at `Y=-18.70` and
extends in positive Y, so it removes zero positive volume from the 1.30 rear
faceplate.

Reuse the accepted four C4 V3.1 snaps exactly:

- snap centre X planes `+/-16.20`, width `3.60`;
- beam `1.20` thick, R0.80 concave root with 0.20 finite grip/beam overlap;
- effective length `7.50`, local hook apex `Y=8.30`, protrusion `0.55`;
- global arm rear/front `Y[-18.70,-9.85]`;
- top beam outer/apex Z `18.15/18.70`; bottom values are mirrors;
- blind pocket X width `4.00`, global `Y[-10.95,-9.85]`, radial depth
  `0.65`, exterior skin `1.20`.

The cover is installed only after the inner button has been rear-fed and
placed at `s=0`. The rear perimeter line is an assembly seam, not a loading or
dispensing path.

## Deterministic validation

### Structure and dimensions

1. Generate exactly three labeled single-solid positive-volume BREP parts.
2. Assert the housing, inner local, and cover faceplate bounding boxes stated
   above; the pressed assembly is exactly 40 x 40 x 40.
3. Assert the inner button is one connected solid region before its external
   lands, ribs, tabs, and key are fused, and remains one connected valid BREP
   solid afterward. It contains no modeled internal void, shell cavity, drain,
   cross web, or functional opening.
4. Assert no geometry or label associated with apertures, shutters, tracks,
   couplings, springs, magnets, latch, medicine, or text exists in the source
   or part tree.

### Motion, clearance, and captivity

5. Sweep `s=-1.00..13.55` at increments no larger than 0.05 and include exact
   `0.00`, `13.40`, and `13.55`. Every unintended fixed/moving BREP
   intersection is `<1e-6 mm^3`.
6. Assert the two land intervals per rail remain fully within full-depth rail
   `Y[-18.00,15.35]`; total engagement is exactly `13.60` at every state.
7. Probe every groove and mouth from real BREP sections: rail width `2.20`,
   groove `2.70`, tangential clearance `0.25` per side, radial clearance
   `0.20`, normal lips `0.80`, mouth lips `0.60`, and positive-Y mouths.
8. Assert every backing rib has the stated bbox, `0.559000` body overlap, and
   `2.838000` boss overlap. Face-only attachment fails.
9. At `s=13.40`, tab front is `15.20`, endplay is `0.15`, and tab/stop overlap
   is `1.00` per side. At `s=13.55`, tabs contact the shoulder without
   positive-volume penetration. A rigid pull beyond this state is rejected.
10. With the cover absent, sweep rear-feed centre `-34.40..4.50` at 0.10.
    Mouth-first rail entries occur at `c=-15.50` and `c=-8.30`; all other
    unintended intersections are `<1e-6 mm^3`.

### Cover and exterior closure

11. Inverse-transform all four snap roots, beams, and hooks to the C4 coupon
    frame. Symmetric-difference volume is `<1e-6 mm^3`; root/grip and
    root/beam overlaps are respectively `0.720000` and `0.576000 mm^3`.
12. Run the full snap insertion/deflection-envelope checks, require the hooks
    wholly inside their blind pockets when seated, and repeat all inner/cover
    collision checks over the motion range.
13. A 0.50-pitch rear grid over X,Z `-19.75..19.75` contains 6400 probes;
    every rear-directed probe first intersects solid faceplate.
14. Ray and connectivity tests must find no modeled functional port through
    the housing, button, or rear faceplate in pressed, released, or
    maximum-pull state. Only the front running seam and rear assembly seam may
    be classified as seams.

### Mesh

15. Export each STL at production chord/angular tolerances, weld vertices
    within `1e-6`, and discard zero-area triangles. Each file must contain one
    connected closed shell, zero boundary or non-manifold edges, and incidence
    exactly two for every undirected edge.
16. Re-import each STL and require positive, consistently oriented volume.
    Meshing does not waive the BREP, sweep, or no-internal-void assertion.

## Print and physical acceptance

- Print the inner button with its key face on the build plate and Y vertical.
  Use slicer infill to control mass; do not add a CAD or slicer-generated
  exterior drain or support hole.
- Print the rear cover on its exterior `Y=-20.00` face so all four snap arms
  build upward. No support or sanding may touch a snap, hook, rail, groove,
  retaining lip, or running surface.
- Print the housing on its `X=-20.00` exterior side with a brim if needed.
  Review the sliced rail ramps and reject supports on functional rail faces.
- Use the same 0.40 nozzle, material, layer height, wall count, cooling, and
  orientation intended for later prototypes. Scaling is disabled.
- Measure all eight normal and mouth lips before assembly. Normal lips must be
  at least 0.70 and mouth lips at least 0.50 as printed.
- Rear-feed the inner button by hand, install the cover, and complete 100 full
  manual cycles from pressed `s=0` to released `s=13.40`. This prototype has
  no return force or latch; the operator positions it manually.
- Breakaway and steady sliding force must be at most 8 N, with no local spike
  above 12 N. Record force at cycles 1, 25, 50, 75, and 100.
- At cycles 0 and 100, apply a measured 10 N front pull for 10 seconds at
  pressed, mid-travel, and released positions. The button remains captive and
  no lip, backing rib, tab, stop, snap, or cover shows cracking, whitening,
  delamination, derailment, or permanent set.
- Complete 30 cover insertion/removal cycles separately. All four hooks seat,
  the cover remains flush, and the rear face remains blind.
- Measure total lateral and vertical key play at mid-travel; each must be at
  most 0.50. Record rather than infer snap extraction force.

Passing this prototype approves only the simplified mechanical interfaces. It
does not validate medicine use, dispensing, magnetic return, spring return,
or push-push behavior.
