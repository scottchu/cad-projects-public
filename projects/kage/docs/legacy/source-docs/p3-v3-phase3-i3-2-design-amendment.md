# KAGE P3 V3 Phase-3 I3.2 — deterministic implementation amendment

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation**  
Date: **2026-08-19**  
Parent specification: `p3-v3-phase3-i3-u1-segmentation-joinery-accepted-spec.md`  
Parent specification SHA-256:
`abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77`  
Frozen Phase-2A STEP SHA-256:
`8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724`

This addendum closes eight implementation holes without changing the accepted
I3 architecture. It is normative where more specific than I3.1. All other
I3.1 requirements remain active.

## 1. Exact moving half-lap ownership and Z intervals

For role `r`, let the frozen carrier interval be `[z0_r,z1_r]`:

| Role | `z0_r` | `z1_r` |
|---|---:|---:|
| hour | -1.50 | 1.50 |
| minute | 4.05 | 7.05 |
| second | 9.60 | 12.60 |

Define local axial coordinate `zeta=Z-z0_r`, so every carrier occupies
`zeta=[0.00,3.00]`.

At both moving seams:

- `half_A_130T_beta15p230769` owns the lower/rear male lap;
- `half_B_130T_beta195p230769` owns the upper/front receiving lap;
- Half A nominal lower solid interval is `zeta=[0.00,2.00]`;
- Half B finished upper solid interval is `zeta=[2.08,3.08]`;
- the open axial fit interval `zeta=(2.00,2.08)` is the complete 0.08 Z
  clearance;
- Half A owns the nominal tangential/radial male envelope
  `R=[133.50,140.00]`, `tangent=[-8.00,+8.00]`;
- Half B alone owns the XY fit removal. Its receiving relief is the Half A
  nominal male envelope offset outward by 0.10 on every non-seam radial and
  tangential boundary;
- Half A is never undersized to create XY or Z fit clearance;
- outside the overlapping lap band, both halves own 0.025 retreat from the
  ideal radial cut face. The two retreats create the 0.050 assembled butt-face
  gap;
- no 0.025 face retreat is applied to the Half A male-lap boundary. Applying
  both face relief and receiving clearance to the same lap face is forbidden.

Absolute finished lap intervals are therefore:

| Role | Half A lower lap | Half B upper lap | axial fit gap |
|---|---|---|---|
| hour | `[-1.50,0.50]` | `[0.58,1.58]` | `(0.50,0.58)` |
| minute | `[4.05,6.05]` | `[6.13,7.13]` | `(6.05,6.13)` |
| second | `[9.60,11.60]` | `[11.68,12.68]` | `(11.60,11.68)` |

Half B retains its full 1.00 thickness. Its Z=3.08 face is an authorized 0.08
front protrusion relative to the nominal Z=3.00 carrier front and is legal only
inside the named seam ROI. Relative to the frozen local seam comparison datum
Z=2.65, the maximum authorized protrusion is 0.43. Neither value authorizes a
global fin, tooth, race, or silhouette change.

The exact M2x3 stack is:

`3.00 = 1.00 upper tongue + 0.08 gap + 1.60 nut engagement + 0.32 tip space`.

The DIN 562 pocket occupies local Z=`[0.30,2.00]`; its upper face seats against
the Z=2.00 lap roof. The upper tongue alone owns the 0.10-per-side XY removal.
The separate 0.025 butt-face relief remains outside the overlap as defined
above.

RED conditions include clearance split between both solids, Half A shrink,
double-applied face relief, an axial interval other than 0.08, or any clearance
cut reaching an active tooth/race surface.

## 2. Exact stationary dowel axes and engagement

All stationary seams use:

`theta_k = 37.5 + 90*k degrees`, for `k=0,1,2,3`.

For a local radial coordinate `R` and tangential coordinate `t`, the global
axis point is:

```text
X = R*cos(theta_k) - t*sin(theta_k)
Y = R*sin(theta_k) + t*cos(theta_k)
axis direction = +Z
```

### 2.1 Chassis dowels

Each chassis seam has dowels at `(R,t)=(85.00,0.00)` and
`(120.00,0.00)`.

- pin: D4.00 x6.00 steel;
- chassis Z: `[-28.00,-25.50]`;
- bridge Z: `[-32.00,-28.00]`;
- pin installed Z: `[-32.00,-26.00]`;
- bridge D3.95 press engagement: `[-32.00,-28.00]`, exactly 4.00;
- chassis D4.10 blind slip engagement: `[-28.00,-26.00]`, exactly 2.00;
- chassis blind roof: `[-26.00,-25.50]`, exactly 0.50;
- assembly direction: press the pin fully into the bridge first; then lower the
  chassis slip bore over the projecting 2.00 pin. Through-insertion from the
  visible +Z chassis face is forbidden.

### 2.2 Frame dowels

Each frame seam has one axis at `(R,t)=(147.80,0.00)`.

- pin: D3.00 x5.00;
- frame Z: `[-6.45,-4.05]`, D3.10 slip engagement 2.40;
- bridge Z: `[-9.45,-6.45]`;
- pin installed Z: `[-9.05,-4.05]`;
- bridge D2.95 press engagement 2.60;
- rear skin 0.40;
- insertion from +Z to a flush front face at Z=-4.05.

### 2.3 Front-ring dowels

Each front-ring seam has one axis at `(R,t)=(147.80,0.00)`.

- pin: D2.00 x4.00;
- front ring Z: `[12.80,13.80]`, D2.10 slip engagement 1.00;
- bridge Z: `[9.80,12.80]`, D1.95 press engagement 3.00;
- pin installed Z: `[9.80,13.80]`, flush at both ends;
- insertion from +Z.

Every press/slip pair remains a physical coupon gate. A pin may not be forced
through the slip member to compensate for an undersized bore.

## 3. Front-ring DIN 562 M2 incoming inspection

Every production and spare front-ring DIN 562 M2 nut is measured individually
at three evenly spaced points after deburring.

Incoming height gate:

`measured maximum height <= 1.60`.

The 1.70 pocket therefore provides at least 0.10 axial loading clearance. A
nut above 1.60 is rejected because it can prevent bridge closure. Thread
engagement is measured independently from the installed actual screw/nut
pair; no unreviewed lower height limit is inferred. Sorting or sanding an
over-height nut into compliance is not an authorized production operation.

## 4. Exact stationary hardware label schema

Indices are one-based and zero-padded. `seam` is `01..04`. Only the labels
generated by the following finite schema are authorized.

### 4.1 Chassis

For each seam and `radius in {R085,R120}`:

```text
i3_chassis_seam_{seam}_bridge_{radius}
i3_chassis_seam_{seam}_bridge_{radius}_DIN562_M3_nut_tneg
i3_chassis_seam_{seam}_bridge_{radius}_DIN562_M3_nut_tpos
i3_chassis_seam_{seam}_bridge_{radius}_M3x5_button_screw_tneg
i3_chassis_seam_{seam}_bridge_{radius}_M3x5_button_screw_tpos
i3_chassis_seam_{seam}_bridge_{radius}_D4x6_dowel
```

Expansion yields exactly 8 bridge, 16 nut, 16 screw, and 8 dowel labels.

### 4.2 Stationary frame

For each seam:

```text
i3_frame_seam_{seam}_bridge_R144p50_R150p00
i3_frame_seam_{seam}_DIN562_M2_nut_tneg
i3_frame_seam_{seam}_DIN562_M2_nut_tpos
i3_frame_seam_{seam}_M2x4_button_screw_tneg
i3_frame_seam_{seam}_M2x4_button_screw_tpos
i3_frame_seam_{seam}_D3x5_dowel
```

Expansion yields exactly 4 bridge, 8 nut, 8 screw, and 4 dowel labels.

### 4.3 Outer front ring

For each seam:

```text
i3_front_ring_seam_{seam}_bridge_R144p50_R150p00
i3_front_ring_seam_{seam}_DIN562_M2_nut_tneg
i3_front_ring_seam_{seam}_DIN562_M2_nut_tpos
i3_front_ring_seam_{seam}_M2x3_button_screw_tneg
i3_front_ring_seam_{seam}_M2x3_button_screw_tpos
i3_front_ring_seam_{seam}_D2x4_dowel
```

Expansion yields exactly 4 bridge, 8 nut, 8 screw, and 4 dowel labels.

Any spelling variant, missing index, unexpanded wildcard, or generic
`hardware_REFERENCE` label is RED.

## 5. Motion coordinates and contact whitelist

### 5.1 Ring rotation

Positive `phi` is positive rotation about +Z under the existing source
convention. Ring centres and Z datums remain fixed.

### 5.2 Motor q

For role motor angle `alpha_r`:

| Role | `alpha_r` |
|---|---:|
| hour | 0 |
| minute | 120 |
| second | 240 |

Positive `q_motor` moves the complete rigid motor station radially outward:

```text
dX = q_motor*cos(alpha_r)
dY = q_motor*sin(alpha_r)
dZ = 0
```

The motor, yoke, miter gears, bearings, shafts, collars, and output pinion move
as one rigid transform. Powered samples are `q_motor={-0.35,0,+0.10}`. Service
positions are not powered motion samples.

### 5.3 Adjustable tower q

The adjustable tower is at `alpha_t=300 degrees`. Positive `q_tower` moves the
complete tower-3 module radially outward:

```text
dX = q_tower*cos(300 degrees)
dY = q_tower*sin(300 degrees)
dZ = 0
roller axis radius = 125.50 + q_tower
```

Samples are `q_tower={-0.25,0,+0.25}`. Fixed towers at 60 and 180 degrees have
q=0 and never move.

### 5.4 Contact tests and the finite IV whitelist

The positive-intersection whitelist contains only each exact dowel/pin paired
with its own named press-side bore. The allowed press IV must equal the
analytical nominal interference volume within `1e-7 mm3`. No other pair is
allowed positive-volume intersection.

Gear mesh, race/roller behavior, screw/nut fastening, lap bearing, and bridge
bearing are tested as gap, contact, containment, or engagement relationships,
not placed on the IV whitelist:

1. Each role ring's active internal teeth versus its own output pinion must
   satisfy the accepted tooth-distance/backlash test and IV<=`1e-7 mm3`.
2. Each R131.60 race versus its own three running lands must satisfy the
   accepted contact/gap test and IV<=`1e-7 mm3`.
3. Screw/nut thread engagement is measured by named axial interval and
   containment using thread void/envelope solids; screw and nut material IV is
   <=`1e-7 mm3`.
4. Slip-side dowel bores, mating laps, bridges, axles, flanges, heads, fins,
   chassis, frame, and front ring all require IV<=`1e-7 mm3`.

No ring may use another role's pinion or roller as a contact pair.

## 6. Serializer calibration and matched-camera evidence

### 6.1 Expected registry classes

The I3 assembled registry has exactly 275 occurrences:

```text
203 baseline
- 6 moving quadrant count reduction
- 48 removed legacy seam-hardware occurrences
+ 30 new moving joint hardware
+ 96 new stationary joint hardware
= 275
```

Classification is exactly:

- 131 `protected_exact` occurrences;
- 18 `authorized_replacement` occurrences: 12 stationary quadrants and 6
  moving halves;
- 126 `new_authorized` hardware occurrences.

### 6.2 Serializer policy

Protected occurrences retain the Phase-1/I1 floors and are never recalibrated:

```text
transform <= 1e-12
AABB      <= 1e-12 mm
area      <= 1e-12 mm2
volume    <= 1.999978849198669e-09 mm3
```

Authorized replacement/new occurrences require three fresh-process
build-export-import runs. For each metric `m`, the I3 STEP-representation
tolerance is:

```text
T_transform = max(2*observed_max_transform, 1.4011902749189176e-11)
T_AABB      = max(2*observed_max_AABB,      1e-12)
T_area      = max(2*observed_max_area,      1e-12)
T_volume    = max(2*observed_max_volume,    2.3096000006717076e-05)
```

Calibration applies only to source-versus-import STEP representation. It may
not be used for source rebuild drift, protected occurrences, Boolean
reconstruction, tooth phase, or collision tests. All three runs must have the
same 275-label order and the same maximum-occurrence identity per metric. A
single outlier, topology change, or tolerance over 10 times the I1 floor needs
independent review and cannot self-authorize.

### 6.3 Exact camera and reference images

The mandatory matched camera is:

- camera `iso`;
- orthographic projection;
- display `solid`;
- theme `snapshot`;
- resolution 1800 x1200 pixels;
- locked reference
  `models/p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention/snapshots/i1_matched_final.png`;
- reference SHA-256
  `25a8365c020c026d2ff5098fad8eba6d632c7913e64321a2b248a7ef208c9f7e`.

The earlier locked pre-I1 reference remains audit evidence only:

- `locked_matched_final.png`;
- SHA-256
  `09c6e7bb07be379b819126b0f731ff6cf00a81224b3284741f7268593c313d84`.

The inherited fixed-tower ROIs remain exactly:

`(370,205,438,380)` and `(1495,390,1522,414)` in `(xmin,ymin,xmax,ymax)`.

I3 does not authorize a broad rectangular or annular pixel ROI. Its authorized
pixel set is generated deterministically by an ID-buffer render using the same
camera: render only the 18 authorized replacement solids and 126 new hardware
solids, mark every non-background pixel, and apply a two-pixel Chebyshev
dilation. Store the resulting binary mask as
`snapshots/i3_authorized_roi_mask.png` and record its SHA-256 in the validation
manifest. This exact mask, unioned with the two inherited fixed-tower ROIs, is
the only foreground-difference authorization.

Run exact border-background flood fill using both four- and eight-connectivity.
Both exterior-mask XOR counts must be zero. Candidate/reference foreground XOR
outside the exact authorized mask must be zero. The global outer-contour XOR
must remain zero.

## 7. Exact moving-half print transform

Source half geometry and assembly transforms remain unchanged. Plate placement
uses this deterministic transform, in this order:

1. Rotate every moving half `+30.000 degrees` about global +Z through the
   source clock origin.
2. Measure the rotated actual-solid AABB, including integral fin and lap.
3. Translate in Z by `-bbox_min_Z`, placing the frozen rear planar datum at
   plate Z=0.
4. For the nominal 270 bed, translate XY by:

   ```text
   dX = 135.00 - (bbox_min_X+bbox_max_X)/2
   dY = 135.00 - (bbox_min_Y+bbox_max_Y)/2
   ```

5. For the fallback 260 bed, replace 135.00 with 130.00.

No mirror, XY scale, elephant-foot compensation transform, or role-specific
rotation is permitted. Half A and Half B of every role use the same +30-degree
rotation rule. Bed fit is evaluated after the translation with the full
brim/support/skirt envelope; raw actual-solid max XY remains at most 238.99.

The plate manifest stores the 4x4 `T_print_from_source` matrix and its exact
inverse `T_source_from_print`. Applying the inverse to the imported 3MF
occurrence must restore the source AABB and transform within the I3 serializer
policy.

## 8. Stationary head and driver envelopes

All stationary screws approach along -Z tool motion from the viewer/front;
their driver cylinders extend in +Z from the installed head top and are swept
downward coaxially to full socket engagement.

### 8.1 Chassis M3

- screw axis: the Section 2 transform with bridge R85 or R120 and
  `t=+/-5.50`;
- bearing surface Z=-25.50;
- ISO 7380-1 M3 head envelope D5.70 x1.65,
  Z=`[-25.50,-23.85]`;
- driver envelope D6.50 x12.00,
  Z=`[-23.85,-11.85]` before downward engagement;
- required free radial clearance around the head: 0.40.

### 8.2 Frame M2

- screw axis: `R=147.80`, `t=+/-5.00`, `theta_k` from Section 2;
- bearing surface Z=-4.05;
- button-head envelope D3.50 x1.20,
  Z=`[-4.05,-2.85]`;
- driver envelope D4.50 x8.00,
  Z=`[-2.85,5.15]` before downward engagement;
- accepted hour-ring lower datum Z=-1.50 leaves 1.35 axial clearance above
  the maximum head.

### 8.3 Outer front-ring M2

- screw axis: `R=147.80`, `t=+/-5.00`, `theta_k` from Section 2;
- bearing surface Z=13.80;
- button-head envelope D3.50 x1.20,
  Z=`[13.80,15.00]`;
- driver envelope D4.50 x8.00,
  Z=`[15.00,23.00]` before downward engagement.

At every assembly stage, actual driver sweeps must have IV<=`1e-7 mm3`
against non-target protected solids. Driver clearance is tested before motors,
towers, rings, or the next front assembly stage can conceal an axis. A screw
that is geometrically reachable only in the exploded viewer but not in the
specified assembly order is RED.

## 9. Amendment artifact and RED inventory

Implementation evidence must add:

- an I3.2 parameter table containing every interval and transform above;
- expanded exact stationary label list and 275-occurrence classification;
- three-run serializer calibration JSON;
- matched-camera candidate PNG, ID-buffer ROI PNG, ROI SHA-256, four/eight
  exterior masks, and pixel counts;
- per-half print matrices and inverse-restoration evidence;
- driver/head, nut-loading, dowel, q-motion, and whitelist pair reports.

All I3.1 RED tests remain active. This amendment adds RED status for any
ambiguous fit ownership, wrong Z interval, non-Cartesian q interpretation,
contact pair outside the finite whitelist, protected-tolerance recalibration,
camera mismatch, hand-drawn ROI, non-invertible print transform, or driver
envelope that is not clear in the authoritative assembly order.
