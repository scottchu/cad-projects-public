# P0 v3 faithful physical-coupon specification

This document freezes the physical fit coupons that must be printed before the
P0 mechanism is integrated. All dimensions are millimetres. This is a design
contract only: the implementation agent owns CAD/source generation and the
review agent must independently inspect the resulting BREP geometry.

## Coordinate and assembly convention

- X is radial: negative X points inward toward the medicine cavity and positive
  X points outward toward the housing wall.
- Y is motion: rear is negative Y and the key/front is positive Y.
- Z is tangential across the rail or shutter.
- Rear insertion moves from negative Y toward positive Y.
- The **positive-Y edge of every moving land or shutter is the
  insertion-leading edge**.
- Fixed track mouths are at their negative-Y entrances.
- Moving-land groove mouths and shutter lead-ins are at their positive-Y
  leading edges.
- Boolean interference acceptance is less than `1e-6 mm^3` unless explicitly
  noted for the intentionally deflecting snap hook.

## Audit of the rejected P0 v2 rail coupons

The current P0 v2 nominal and loose rail artifacts are valid solids and their
existing sixteen tests pass, but they are not faithful interface coupons:

- the fixed rail is a straight box and omits the 0.70 lead-in;
- the receiver groove is uniform and omits the 0.60 mouth;
- the receiver is 12.00 long instead of the actual 3.40 bearing land;
- the source places the land mouth on the negative-Y edge even though the
  positive-Y edge leads during rear-to-front insertion; and
- current tests prove only that the two artifacts are valid and distinct, not
  that they reproduce the real interface.

P0 v3 replaces those artifacts with the coupons below.

## C1R1 strengthened nominal rail-fit coupon and preserved C2 fallback

The first printed C1 receiver failed after only a few slides: the short
receiver derailed and the two groove-retaining lips fractured. C1R1 is the
strengthened nominal revision. C2 remains the original loose-clearance coupon
for printer-fit diagnosis only; it is not evidence that the original short,
thin-lip geometry is durable.

### Shared rail, groove, and mouth variables

| Variable | Value | Intent |
| --- | ---: | --- |
| `rail_radial_height` | 1.20 | Root-to-tip rail projection |
| `rail_tangential_width` | 2.20 | Rail width in Z |
| `rail_rear_lead_in` | 0.70 | Fixed-rail ramp at the negative-Y entrance |
| `groove_mouth_length` | 0.60 | Widened/deepened leading mouth length |
| `groove_mouth_extra_width` | 0.40 | Total mouth widening in Z |
| `groove_mouth_extra_depth` | 0.30 | Mouth deepening in X |
| `inward_state` | -1.00 | Future shuttle inward hard stop |
| `released_state` | 13.40 | Normal released state |
| `maximum_pull_state` | 13.55 | Captive maximum pull state |

The coupon models the positive-X housing side. The rail root is `X=0.00` and
the rail projects inward to `X=-1.20`. The moving-land groove opens toward
positive X, away from the medicine cavity. The receiver's handling wings may
occupy `|Z|=1.75..3.50` only behind `X<=-1.55`; they must not change the
contacting boss, groove, or mouth geometry.

### Versioned variants and derived clearances

| Variable | C1R1 primary | C1R1B thick-lip trial | Preserved C2 |
| --- | ---: | ---: | ---: |
| Coupon name | `P0_V3_C1R1_nominal_L6p80_lip0p80` | `P0_V3_C1R1B_nominal_L6p80_lip1p20` | `P0_V3_C2_loose_original` |
| `rail_coupon_length` | 22.40 | 22.40 | 19.00 |
| `land_length` | 6.80 | 6.80 | 3.40 |
| `bearing_boss_width` | 4.30 | 5.10 | 3.50 |
| `groove_width` | 2.70 | 2.70 | 2.80 |
| Normal retaining lip per side | 0.80 | 1.20 | 0.35 |
| Mouth retaining lip per side | 0.60 | 1.00 | 0.15 |
| `radial_running_clearance` | 0.20 | 0.20 | 0.30 |
| Tangential clearance per side | 0.25 | 0.25 | 0.30 |
| Normal groove bottom X | -1.40 | -1.40 | -1.50 |
| Normal groove radial depth to `X=-0.75` | 0.65 | 0.65 | 0.75 |
| Mouth width | 3.10 | 3.10 | 3.20 |
| Mouth bottom X | -1.70 | -1.70 | -1.80 |

The rejected C1 baseline used `land_length=3.40`,
`bearing_boss_width=3.50`, and nominal `groove_width=2.70`, leaving only
`(3.50-2.70)/2=0.40` per normal lip and
`(3.50-3.10)/2=0.20` per mouth lip. C1R1 doubles the land length and the
normal lip. Because the frozen mouth remains 0.40 wider than the normal
groove, its minimum C1R1 lip is 0.60, not 0.80.

The equations are:

```text
radial_clearance = rail_tip_x - groove_bottom_x
tangential_clearance_per_side =
    (groove_width - rail_tangential_width) / 2
mouth_width = groove_width + groove_mouth_extra_width
mouth_bottom_x = groove_bottom_x - groove_mouth_extra_depth
```

The C1R1/C1R1B 0.60 mouth occupies moving-land local
`Y=[+2.80,+3.40]`, at the positive-Y insertion-leading edge. The C2 mouth
remains at local `Y=[+1.10,+1.70]`. The fixed rail ramps from zero projection
at `Y=0.00` to its full `1.20` projection at `Y=0.70`, then remains constant
through the variant's stated coupon length.

### Section improvement without a strength claim

At a normal groove section, one lip is a `lip_width x 0.65` rectangle. At the
deepened mouth it is `mouth_lip_width x 0.95`. Relative to failed C1:

| Metric per lip | Failed C1 | C1R1 | Ratio | C1R1B | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Normal area, mm^2 | 0.2600 | 0.5200 | 2.0x | 0.7800 | 3.0x |
| Normal `S` about tangential axis, mm^3 | 0.028167 | 0.056333 | 2.0x | 0.084500 | 3.0x |
| Normal `S` about radial axis, mm^3 | 0.017333 | 0.069333 | 4.0x | 0.156000 | 9.0x |
| Mouth area, mm^2 | 0.1900 | 0.5700 | 3.0x | 0.9500 | 5.0x |
| Mouth `S` about tangential axis, mm^3 | 0.030083 | 0.090250 | 3.0x | 0.150417 | 5.0x |
| Mouth `S` about radial axis, mm^3 | 0.006333 | 0.057000 | 9.0x | 0.158333 | 25.0x |

These use `S=b*h^2/6` for the two orthogonal rectangular-section axes. They
quantify geometry only; layer adhesion, notch effects, print orientation,
material, and load sharing prevent them from certifying strength. The 0.80
normal lip is only two nominal 0.40-nozzle widths, while its 0.60 mouth lip is
only 1.5 nozzle widths. Print C1R1B in the same batch rather than assuming
C1R1 is sufficient.

### Exact part bounding boxes

| Part | Bounding box | Size |
| --- | --- | --- |
| C1R1/C1R1B fixed rail carrier | `X[-1.20,2.00]`, `Y[0.00,22.40]`, `Z[-3.50,3.50]` | 3.20 x 22.40 x 7.00 |
| C1R1/C1R1B receiver | `X[-3.40,-0.75]`, `Y[-3.40,3.40]`, `Z[-3.50,3.50]` | 2.65 x 6.80 x 7.00 |
| Preserved C2 fixed rail carrier | `X[-1.20,2.00]`, `Y[0.00,19.00]`, `Z[-3.50,3.50]` | 3.20 x 19.00 x 7.00 |
| Preserved C2 receiver | `X[-3.40,-0.75]`, `Y[-1.70,1.70]`, `Z[-3.50,3.50]` | 2.65 x 3.40 x 7.00 |

### Insertion and motion equations

The C1R1/C1R1B receiver centre during the full shuttle hard range is:

```text
receiver_center_y(s) = 5.30 + s
land_interval(s) = [receiver_center_y(s)-3.40,
                    receiver_center_y(s)+3.40]
s in [-1.00, 13.55]
```

Therefore:

```text
land_interval(-1.00)  = [0.90, 7.70]
land_interval(13.40)  = [15.30, 22.10]
land_interval(13.55)  = [15.45, 22.25]
lead-in exit margin   = 0.90 - 0.70 = 0.20
maximum-pull margin   = 22.40 - 22.25 = 0.15
full guide travel     = 13.55 - (-1.00) = 14.55
```

The C1R1 insertion sweep moves its receiver centre from `Y=-3.40` (leading
edge first touches the fixed entrance) to `Y=4.30` (the `s=-1.00` position).
The preserved C2 retains its original `receiver_center_y(s)=3.60+s`, original
intervals, and insertion-centre sweep `-1.70..2.60`.

### Executable geometry assertions

The implementation tests must assert all of the following against real BREP
geometry:

```python
assert c1r1_rail_bbox == approx((-1.20, 0.00, -3.50, 2.00, 22.40, 3.50))
assert c1r1_receiver_bbox == approx((-3.40, -3.40, -3.50, -0.75, 3.40, 3.50))
assert c2_rail_bbox == approx((-1.20, 0.00, -3.50, 2.00, 19.00, 3.50))
assert c2_receiver_bbox == approx((-3.40, -1.70, -3.50, -0.75, 1.70, 3.50))
assert rail_radial_height == approx(1.20)
assert rail_tangential_width == approx(2.20)
assert rail_rear_lead_in == approx(0.70)
assert groove_mouth_length == approx(0.60)
assert mouth_is_on_positive_y_leading_edge

assert nominal_radial_clearance == approx(0.20)
assert nominal_tangential_clearance_per_side == approx(0.25)
assert nominal_groove_width == approx(2.70)
assert nominal_mouth_width == approx(3.10)
assert c1r1_land_length == approx(6.80)
assert c1r1_bearing_boss_width == approx(4.30)
assert c1r1_normal_lip_per_side == approx(0.80)
assert c1r1_mouth_lip_per_side == approx(0.60)
assert c1r1b_bearing_boss_width == approx(5.10)
assert c1r1b_normal_lip_per_side == approx(1.20)
assert c1r1b_mouth_lip_per_side == approx(1.00)

assert loose_radial_clearance == approx(0.30)
assert loose_tangential_clearance_per_side == approx(0.30)
assert loose_groove_width == approx(2.80)
assert loose_mouth_width == approx(3.20)
assert c2_land_length == approx(3.40)
assert c2_bearing_boss_width == approx(3.50)
assert c2_normal_lip_per_side == approx(0.35)
assert c2_mouth_lip_per_side == approx(0.15)

assert c1r1_land_interval(-1.00) == approx((0.90, 7.70))
assert c1r1_land_interval(13.40) == approx((15.30, 22.10))
assert c1r1_land_interval(13.55) == approx((15.45, 22.25))
assert lead_in_exit_margin == approx(0.20)
assert maximum_pull_margin == approx(0.15)
```

- Every manufactured part is one valid positive-volume solid.
- The rail has zero projection at `Y=0.00`, reaches 1.20 projection at
  `Y=0.70`, and is constant afterward.
- Real BREP volumes must satisfy
  `volume(C1R1B receiver) > volume(C1R1 receiver) > volume(C2 receiver)`;
  do not use source parameters as a proxy.
- Sweep the C1R1/C1R1B insertion centre from `-3.40` to `4.30` and the
  preserved C2 insertion centre from `-1.70` to `2.60`, at increments no
  larger than 0.05, and assert fixed/moving intersection volume
  `<1e-6 mm^3`.
- Sweep `s=-1.00..13.55` at increments no larger than 0.05, including exact
  endpoints, for all three variants and assert intersection volume
  `<1e-6 mm^3`.
- Tests must measure the actual groove section, mouth section, lead-in profile,
  and open-positive-X side from BREP probes; parameter-only checks do not pass.
- At normal and mouth sections, probe both retaining lips independently and
  assert the exact widths and radial depths stated above.
- Export each receiver STL, weld vertices within `1e-6`, remove zero-area
  triangles, and require one connected closed shell, zero boundary and
  non-manifold edges, and incidence two for every undirected edge.

### Print orientation and physical acceptance

- Print C1R1 and C1R1B in the same batch and process. Preserve C2 as the
  original loose-clearance comparison. Use the same material, layer height,
  wall count, and cooling profile, with scaling disabled.
- Print the receiver with its positive-X open groove facing upward.
- Print the fixed carrier with its negative-X rail tip facing upward.
- No supports may touch a functional surface. Remove only loose strings or a
  brim outside the interface; sanding the rail or groove invalidates the test.
- Measure and record as-printed rail width, groove width, groove depth, and
  mouth dimensions with callipers before assembly.
- All pairs must insert without a tool and complete 100 full 14.55 travel
  cycles without binding, gouging, cracking, stress whitening, or delamination.
- Initial insertion force must be at most 15 N.
- Breakaway and steady sliding force must be at most 8 N, with no local spike
  above 12 N.
- At cycles 0 and 100, apply a measured 10 N normal pull for 10 seconds at the
  inward, mid-travel, and released positions. The receiver must remain
  captured with no lip crack, whitening, delamination, or permanent set.
- Record the as-printed normal and mouth lip widths for both strengthened
  variants. Do not select C1R1 merely from nominal dimensions if the slicer or
  print produces a single-line mouth lip.
- Before cycling, both C1R1 normal lips must measure at least `0.70` and both
  mouth lips at least `0.50`. C1R1B limits are `1.10` and `0.90`. A specimen
  outside those limits is a print-process failure and cannot establish the
  design's capture durability.
- Prefer C1R1 if it passes capture, force, and cycling. Select C1R1B if C1R1
  shows lip damage or insufficient printed wall count. C2 remains a clearance
  fallback and cannot overrule a durability failure; a loose long-land
  revision would require a separately specified C2R1.

## C3: revised captured shutter-track strip

This coupon uses the revised printable solid shutter. It tests the captured
track interface only; it does not contain a medicine opening or exterior port.
The shutter operational range is `s=0.00..13.40`. Future 1.00 shuttle-only
inward overtravel is excluded and will be handled by lost motion in a later
mechanism phase.

### Variables and derived section

| Variable | Value |
| --- | ---: |
| `shutter_web_width` | 25.00 |
| `shutter_web_thickness` | 0.80 |
| `shutter_flange_width` | 27.40 |
| `shutter_flange_thickness` | 0.80 |
| `track_web_width` | 25.40 |
| `track_flange_width` | 27.80 |
| `lateral_clearance_per_side` | 0.20 |
| `track_floor_clearance` | 0.20 |
| `vertical_lip_clearance` | 0.20 |
| `capture_overlap_per_side` | 1.00 |
| `exterior_recess` | 0.20 |
| `track_mouth_length` | 0.80 |
| `track_mouth_extra_width` | 0.40 total |
| `track_mouth_extra_height` | 0.20 |
| `shutter_lead_in` | 0.80 |
| `track_length` | 32.00 |
| `slider_length` | 12.00 |
| `operational_stroke` | 13.40 |

The normalized top-track section is:

```text
receiver backing             Z=-2.00..0.00
track floor                  Z=0.00
assembled flange             Z=0.20..1.00
assembled web                Z=1.00..1.80
capture-lip underside        Z=1.20
receiver exterior            Z=2.00
```

The derived clearances are:

```text
flange lateral clearance = (27.80 - 27.40)/2 = 0.20/side
web lateral clearance    = (25.40 - 25.00)/2 = 0.20/side
floor clearance          = 0.20
lip clearance            = 1.20 - 1.00 = 0.20
capture overlap          = (27.40 - 25.40)/2 = 1.00/side
```

The receiver track mouth is at its fixed negative-Y entrance, `Y=[0.00,0.80]`,
and flares the web and flange slots by 0.40 total width and 0.20 height. The
slider's positive-Y insertion-leading edge occupies local `Y=[5.20,6.00]`.
Across that edge the flange tapers from 25.00 wide and 0.40 thick at the tip to
27.40 wide and 0.80 thick at the full section. The solid closure web remains
the full 25.00 wide by 0.80 thick throughout.

### Exact part bounding boxes

| Part | Bounding box | Size |
| --- | --- | --- |
| Track receiver | `X[-15.90,15.90]`, `Y[0.00,32.00]`, `Z[-2.00,2.00]` | 31.80 x 32.00 x 4.00 |
| Slider, assembly coordinates | `X[-13.70,13.70]`, `Y[-6.00,6.00]`, `Z[0.20,1.80]` | 27.40 x 12.00 x 1.60 |

For build-plate layout only, the slider may be translated so its bounding box
is `Z=[0.00,1.60]`; its section must not be scaled or otherwise transformed.

### Motion equations

```text
pressed_slider_center_y  = 9.30
released_slider_center_y = 22.70

slider_interval_pressed  = [3.30, 15.30]
slider_interval_released = [16.70, 28.70]
operational_stroke       = 22.70 - 9.30 = 13.40
rear_end_margin          = 3.30
front_end_margin         = 32.00 - 28.70 = 3.30
```

The insertion sweep moves the slider centre from `Y=-6.00`, when its positive-Y
leading tip first meets the receiver entrance, to `Y=9.30`. The operational
sweep is `Y=9.30..22.70`.

### Executable geometry assertions

```python
assert receiver_bbox == approx((-15.90, 0.00, -2.00, 15.90, 32.00, 2.00))
assert slider_bbox == approx((-13.70, -6.00, 0.20, 13.70, 6.00, 1.80))
assert flange_lateral_clearance == approx(0.20)
assert web_lateral_clearance == approx(0.20)
assert track_floor_clearance == approx(0.20)
assert vertical_lip_clearance == approx(0.20)
assert capture_overlap_per_side == approx(1.00)
assert track_mouth_is_on_negative_y_receiver_entrance
assert slider_lead_is_on_positive_y_leading_edge
assert slider_interval_pressed == approx((3.30, 15.30))
assert slider_interval_released == approx((16.70, 28.70))
assert operational_stroke == approx(13.40)
assert rear_end_margin == approx(3.30)
assert front_end_margin == approx(3.30)
```

- Both parts must be valid single positive-volume solids.
- BREP probes must measure the real 0.80 web, 0.80 flange, 0.80 lead-in length,
  0.80 track mouth, all four 0.20 clearances, and 1.00 capture overlap.
- Sweep insertion centre `-6.00..9.30` and operational centre `9.30..22.70`
  at increments no larger than 0.05 and assert intersection volume
  `<1e-6 mm^3`.
- At every operational sample the two lips must overlap the flange by at least
  1.00 on each side.
- Section probes must verify that the receiver remains one continuous solid
  and that its backing is at least 2.00 thick below the track floor.

### Print orientation and physical acceptance

- Print the receiver on its `Z=-2.00` backing face with the track slot upward.
- Print the slider with its flange bottom on the build plate.
- Use no support on any sliding or capture surface and do not sand those
  surfaces after printing.
- The slider must insert by hand and complete 100 full 13.40 travel cycles.
- Breakaway and steady sliding force must be at most 8 N, with no spike above
  12 N.
- Measured total lateral play must be at most 0.50 and total vertical play at
  most 0.50.
- Apply 10 N normal pull for 10 seconds at mid-stroke. The slider must remain
  captured with no crack, lip damage, stress whitening, or permanent set.

## C4: one-arm reversible rear-cover snap coupon (P0 V3.1 root correction)

The chosen rear retention is an axial positive-Y blind cover with four long
reversible snap arms in the full assembly. The coupon tests one exact arm and
one matching receiver pocket. C4 is a **standalone, rotated manufacturing
coupon**: its X/Y/Z values below are coupon-local coordinates chosen for a
support-free print and direct force test, not the world coordinates of a snap
inside the 40 mm housing.

The full assembly relocates copies of this same local snap section and pocket
to snap centre planes `X=-16.20` and `X=+16.20`. That placement may translate,
rotate, and mirror a copy for the opposite side, but it must not scale, shear,
or change the beam, hook, pocket, clearance, effective length, or strain
geometry frozen by C4.

### Variables and exact geometry

| Variable | Value |
| --- | ---: |
| `beam_width` | 3.60 |
| `bending_thickness` | 1.20 |
| `root_fillet_radius` | 0.80 |
| `root_overlap` | 0.20 |
| `root_tangent_y` | 0.80 |
| `hook_apex_y` | 8.30 |
| `effective_beam_length` | 7.50 |
| `hook_base_rear_y` | 7.75 |
| `hook_base_front_y` | 8.85 |
| `hook_protrusion` | 0.55 |
| `hook_apex_x` | 1.75 |
| `hook_ramp_angle` | 45 degrees |
| `arm_total_length` | 8.85 |
| `pocket_width` | 4.00 |
| `pocket_side_clearance` | 0.20 per side |
| `pocket_depth` | 0.65 |
| `receiver_outer_skin` | 1.20 |
| `relative_insertion_stroke` | 8.85 |

The straight beam occupies `X=[0.00,1.20]`, `Y=[0.00,8.85]`, and
`Z=[-1.80,1.80]`. Its root relief reaches its tangent at `Y=0.80`. The
symmetric reversible hook rises 0.55 over 0.55 axial travel and falls 0.55
over 0.55 axial travel, giving the 45-degree base `Y=[7.75,8.85]` and apex
`(X,Y)=(1.75,8.30)`.

P0 V3.1 replaces the non-manifold, endpoint-only circular-segment root with
one exact, closed root prism. In coupon-local XY, route its outer profile
through these points and arc, in order:

```text
(-0.80,-0.20)
( 0.20,-0.20)
( 0.20, 0.80)
( 0.00, 0.80)
exact R0.80 quarter arc, centre (-0.80,0.80),
    from (0.00,0.80) to (-0.80,0.00)
close to (-0.80,-0.20)
```

Extrude that profile over `Z=[-1.80,1.80]`. Its exact root-prism bounding box
is therefore `X[-0.80,0.20]`, `Y[-0.20,0.80]`, `Z[-1.80,1.80]`. The
`0.20` extensions are intentional hidden overlaps, not running clearances:

- root/grip overlap is `X[-0.80,0.20] x Y[-0.20,0.00] x
  Z[-1.80,1.80]`, volume `0.720000 mm^3`;
- root/beam overlap is `X[0.00,0.20] x Y[0.00,0.80] x
  Z[-1.80,1.80]`, volume `0.576000 mm^3`.

The exposed concave stress-relief area is
`R^2(1-pi/4)=0.137345 mm^2`, so its net union-added volume is
`0.494443 mm^3`. Including the two overlap regions, the source root prism has
profile area `0.497345 mm^2` and gross volume `1.790443 mm^3`. Fuse the grip,
root prism, straight beam, and hook into one BREP before any mesh export. Do
not restore the legacy `0.02` tangent bridge or use an epsilon-only overlap.

Keep root-vs-rootless additions separate from V3-to-V3.1 part deltas. For the
coupon arm, the corrected accounting is:

```text
V3.1 rootless arm baseline       = 154.521000000000 mm^3
V3.1 root addition to baseline  =  +0.494442631532 mm^3
V3.1 expected fused arm         = 155.015442631532 mm^3

measured V3 arm BREP            = 155.194104837031 mm^3
V3 -> V3.1 arm delta            =  -0.178662205499 mm^3
```

The old V3 BREP volume is a valid measured reference even though its root did
not satisfy the required fused-manifold STL behavior. The positive
`0.494442631532 mm^3` is not the old/new arm delta; it is only the material
that the V3.1 root contributes to its own rootless-arm baseline. Likewise,
`4(0.494442631532)=1.977770526128 mm^3` is the four-root addition to a V3.1
rootless-cover baseline, not the V3-to-V3.1 full-cover delta.

A topology probe also tested a local-axis band over `X[-0.80,0.00] x
Y[-0.01,0.01] x Z[-1.80,1.80]`. It produced a valence-two coupon and changed
the V3 arm by `+0.026792429 mm^3`, but its `0.02` thickness is rejected as
non-robust FDM manufacturing geometry. That experimental V3 delta must not be
compared directly with the V3.1 root-vs-rootless addition.

The receiver pocket occupies `X=[1.20,1.85]`, `Y=[7.75,8.85]`, and
`Z=[-2.00,2.00]`. Its 4.00 width supplies 0.20 clearance on each side of the
3.60 arm. The receiver ends at `X=3.05`, leaving `3.05-1.85=1.20` outer skin
and 0.10 radial clearance beyond the latched hook apex.

### Exact part bounding boxes

| Part | Bounding box | Size |
| --- | --- | --- |
| Snap arm plus grip | `X[-2.00,1.75]`, `Y[-3.00,8.85]`, `Z[-6.00,6.00]` | 3.75 x 11.85 x 12.00 |
| Receiver wall | `X[1.20,3.05]`, `Y[0.00,10.50]`, `Z[-6.00,6.00]` | 1.85 x 10.50 x 12.00 |

The grip alone occupies `X=[-2.00,1.20]`, `Y=[-3.00,0.00]`, and
`Z=[-6.00,6.00]`. The receiver pocket values above are cuts within the stated
receiver-wall bounding box.

### Deflection, strain, and packaging equations

```text
effective_length = hook_apex_y - root_tangent_y
                 = 8.30 - 0.80 = 7.50

nominal_deflection = 0.55
worst_case_deflection = 0.65

cantilever_surface_strain = 1.5 * thickness * deflection / length^2
nominal_strain = 1.5 * 1.20 * 0.55 / 7.50^2 = 0.0176 = 1.76%
worst_strain   = 1.5 * 1.20 * 0.65 / 7.50^2 = 0.0208 = 2.08%
strain_limit   = 3.00%

cover_front_world_y = -18.70
arm_front_world_y = -18.70 + 8.85 = -9.85
future_inward_shuttle_rear_y = -9.50
axial_packaging_gap = -9.50 - (-9.85) = 0.35
```

The relative insertion motion begins with the leading arm tip at the receiver
entrance and advances 8.85 in positive Y to the latched pocket pose.

The V3.1 overlap lies behind the `Y=0.80` root tangent and does not shorten the
straight-beam lever. Therefore the first-order beam strain values remain
unchanged. The corrected finite root removes the line-contact stress
singularity, but it also changes local root stiffness and peak-stress
distribution relative to the invalid predecessor; no extraction-force value
may be inferred from the geometric strain equation alone.

The coupon-local X direction is the cantilever bending direction. When C4 is
mapped into the full cover, that local bending axis is rotated to the relevant
housing radial direction and the local snap datum is placed at assembly
`X=-16.20` or `X=+16.20`. The motion remains axial positive Y. Placement is
therefore independent of the section calculations: rigid rotation, mirroring,
and translation preserve the 7.50 effective length and the 1.76/2.08 percent
nominal/worst-case strain values.

### Executable geometry assertions

```python
assert snap_bbox == approx((-2.00, -3.00, -6.00, 1.75, 8.85, 6.00))
assert receiver_bbox == approx((1.20, 0.00, -6.00, 3.05, 10.50, 6.00))
assert root_bbox == approx((-0.80, -0.20, -1.80, 0.20, 0.80, 1.80))
assert root_profile_area == approx(0.4973451754, abs=1e-9)
assert root_gross_volume == approx(1.7904426315, abs=1e-9)
assert root_exposed_relief_area == approx(0.1373451754, abs=1e-9)
assert root_net_union_added_volume == approx(0.4944426315, abs=1e-9)
assert volume(root_prism & grip) == approx(0.720000, abs=1e-6)
assert volume(root_prism & straight_beam) == approx(0.576000, abs=1e-6)
assert v31_rootless_arm_volume == approx(154.521000000000, abs=1e-9)
assert v3_arm_brep_volume == approx(155.194104837031, abs=1e-9)
assert v31_expected_arm_volume == approx(155.015442631532, abs=1e-9)
assert v31_expected_arm_volume == approx(
    v31_rootless_arm_volume + root_net_union_added_volume,
    abs=1e-9,
)
assert v31_expected_arm_volume - v3_arm_brep_volume == approx(
    -0.178662205499,
    abs=1e-9,
)
assert effective_beam_length == approx(7.50)
assert hook_apex_y - root_tangent_y == approx(7.50)
assert hook_apex_x - bending_thickness == approx(0.55)
assert hook_apex_y - hook_base_rear_y == approx(0.55)
assert hook_base_front_y - hook_apex_y == approx(0.55)
assert pocket_side_clearance == approx(0.20)
assert receiver_outer_skin == approx(1.20)
assert nominal_strain == approx(0.0176, abs=1e-4)
assert worst_strain == approx(0.0208, abs=1e-4)
assert worst_strain < 0.03
assert axial_packaging_gap == approx(0.35)
assert assembly_snap_center_x == approx((-16.20, 16.20))
assert assembly_arm_local_section_at_each_center == coupon_arm_local_section
assert assembly_pocket_local_section_at_each_center == coupon_pocket_local_section
assert assembly_arm_effective_length_at_each_center == approx(7.50)
assert assembly_arm_worst_strain_at_each_center == approx(0.0208, abs=1e-4)
```

- Both parts must be valid single positive-volume solids.
- The fused arm must contain exactly one connected BREP solid. Root/grip and
  root/beam intersections must each have the positive volumes stated above;
  face-, edge-, or point-only connectivity is a failure.
- BREP probes must verify beam thickness, beam width, exact root profile, hook
  rise/run, pocket width/depth, and remaining outer skin.
- In the final latched pose the rigid arm and receiver must have no
  positive-volume intersection; the hook must be wholly inside the pocket.
- During insertion the undeflected hook intentionally overlaps the receiver
  wall by 0.55. A deflected-envelope sweep must place the hook at `X<=1.20`
  while passing the wall and prove that the remainder of the arm clears.
- The implementation must not incorrectly use a rigid no-intersection sweep
  as a substitute for the cantilever deflection and strain checks.
- For both assembly centre planes, transform the arm and pocket back into the
  C4 coupon-local frame and compare the actual BREP sections to the coupon.
  Translation, rotation, or mirroring is allowed; any dimensional mismatch is
  a failure.
- Export the coupon arm STL at the production chord/angular tolerances. Weld
  mesh vertices within `1e-6`, discard zero-area triangles, and require one
  connected closed shell, zero boundary edges, zero non-manifold edges, and
  incidence exactly two for every undirected edge.
- Re-import the welded STL and require a positive volume with the same
  orientation as the BREP. Meshing success alone does not waive the BREP
  single-solid and finite-overlap assertions.

### Print orientation and physical acceptance

- Print the snap part with its broad YZ arm face on the bed and positive X
  upward. This keeps the beam length in the layer plane and prints the two
  hook ramps at no more than 45 degrees.
- Print the receiver with its `X=3.05` outer-skin face on the bed so the pocket
  opens upward.
- No support or sanding is allowed on the arm, hook, channel, or pocket.
- The arm must insert without a tool.
- Measure axial extraction with a 0-20 N force gauge and record the initial,
  median, and final values. V3.1 uses this coupon to establish the one-arm
  force empirically; the geometric model does not guarantee `2-5 N` or a
  four-arm multiple.
- Complete 30 full insert/remove cycles. There must be no crack, whitening,
  delamination, hook damage, or receiver-wall damage.
- After one minute of relaxation, permanent hook set must be at most 0.20.
- Final extraction force must remain at least 80 percent of the initial
  measured extraction force. Set production force limits only after the
  material/process coupon data are reviewed.

## Implementation and independent-review gate

The implementation agent must generate five separately identifiable outputs:

1. C1R1 nominal long-land 0.80-lip rail-fit pair;
2. C1R1B nominal long-land 1.20-lip comparison pair;
3. preserved C2 original loose rail-fit pair;
4. C3 shutter-track strip; and
5. C4 one-arm rear-snap strip.

The review agent must independently inspect real exported geometry, repeat the
named measurements and sweep assertions, inspect section snapshots, and reject
any artifact whose tests merely compare derived values to the same source
parameters. Passing deterministic geometry tests does not replace the physical
force, fit, wear, and cycling trials in this specification.

C1R1 supersedes the failed C1 nominal rail geometry. C2, C3, and C4 remain
independent coupons with their previously frozen functions and geometry.
