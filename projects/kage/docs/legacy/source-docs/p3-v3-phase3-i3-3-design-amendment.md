# KAGE P3 V3 Phase-3 I3.3 — manufacturing and evidence closure

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation**

Date: **2026-08-19**

Parent amendment: `p3-v3-phase3-i3-2-design-amendment.md`

Parent amendment SHA-256:
`9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3`

I3.1 specification SHA-256:
`abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77`

Frozen Phase-2A STEP SHA-256:
`8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724`

This is a narrow normative addendum to I3.1 and I3.2. It closes the remaining
manufacturing and reproducibility gaps without authorizing a redesign. Values
not explicitly superseded below remain exactly as accepted.

## 1. Radially open frame and front-ring nut receivers

The two DIN 562 M2 receivers in every stationary-frame bridge and every outer
front-ring bridge are intentional radially open outboard slots, not closed
blind pockets. In the local seam frame, each slot is the subtraction:

```text
R                  = [145.70,150.20]
tangent width      = 4.20, centred at t=+/-5.00
Z depth            = 1.70 from the bridge +Z assembly face
outboard mouth     = continuous through the actual R=150.00 bridge edge
```

The 0.20 extension beyond R=150.00 is Boolean overtravel only and guarantees a
fully open mouth. The bridge remains R=`[144.50,150.00]`, tangent
`[-8.00,+8.00]`, and 3.00 thick. Therefore the finished nominal ligaments are:

```text
inner radial ligament = 145.70-144.50 = 1.20
end ligament          = 8.00-(5.00+2.10) = 0.90
hour-fin clearance    = 144.50-143.90 = 0.60
```

Assembly is performed on the flat R150 datum jig. With the bridge supported,
load each deburred, height-qualified nut along +Z into its slot, place the
corresponding quadrant to close the slot, insert the screw, and only then
remove the subassembly from the jig. Radial loading of a loose nut and an
unclosed transport state are forbidden. The closed quadrant and installed
screw are the capture features; friction alone is not.

The incoming M2 nut-height gate remains maximum 1.60. The finished slot depth
is 1.70, so its axial loading reserve remains at least 0.10. Any closed pocket,
blocked +Z loading path, slot mouth short of the actual outboard edge, inner
ligament below 1.20, end ligament below 0.90, or hour-fin clearance below 0.60
is RED.

## 2. Exact moving D3 x3 dowel installation

For each moving role, use I3.2 local coordinate `zeta=Z-z0_r`. The installed
D3.00 x3.00 pin and its receiving intervals are exactly:

| Feature | local Z interval | length |
|---|---:|---:|
| Half A D2.95 press bore | `[0.00,2.00]` | 2.00 |
| open axial lap gap | `(2.00,2.08)` | 0.08 |
| Half B D3.10 slip bore | `[2.08,3.00]` | 0.92 |
| front recess above pin | `(3.00,3.08]` | 0.08 |
| installed D3 pin | `[0.00,3.00]` | 3.00 |

Mate the halves, support the rear face on a hard rear-stop jig at `zeta=0`,
and insert the pin along +Z until it contacts the jig stop. The finished pin
must end 0.08 below the Half B front face; a flush or proud pin is RED.

The only authorized positive intersection for this joint is the pin versus
its own Half A press bore. Its analytical nominal value is:

```text
pi/4 * (3.00^2-2.95^2) * 2.00 = 0.4673119072 mm3
```

The comparison tolerance is `1e-7 mm3`. The 0.08 open gap and the 0.92 D3.10
slip interval have no authorized positive intersection. All six moving pins
use this same ownership; a pin forced through Half B to compensate for a bad
press bore is RED.

## 3. Cartesian motion-state ownership

Let the three independent motor coordinates be ordered `(q_H,q_M,q_S)`:

```text
(q_H,q_M,q_S) in {-0.35,0,+0.10}^3       # exactly 27 motor states
q_tower         in {-0.25,0,+0.25}        # exactly 3 tower states
```

Their Cartesian product therefore contains exactly 81 q states. The rigid
transform owned by each `q_r` and by `q_tower` remains the transform specified
in I3.2; one role's q must not move another role's station.

For target role `r`, enumerate:

```text
phi_r = j*(360/260)+delta
j in {0,...,259}
delta in {-0.05,0,+0.05} degrees
```

The two non-target ring angles remain fixed at their accepted nominal
zero-angle transforms. Thus each target role owns 780 angle samples and the
complete three-role matrix contains:

`3 roles * 780 target angles * 81 q states = 189540 states`.

All 189540 state transforms must be instantiated and reported. A broadphase
may prune pairwise exact-intersection calls only when its swept actual-AABB
candidate set is a proved superset of full-scan hits. Reusing one role's result
for another role, or reducing the state matrix by asserted symmetry, is
forbidden unless the report proves identical actual-solid candidate sets and
records full-scan agreement at every q extreme and nominal q for each role.
The role shortcut is RED without that broadphase proof.

## 4. Frozen matched-camera and raster contract

The accepted reference remains:

`models/p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention/snapshots/i1_matched_final.png`

with SHA-256
`25a8365c020c026d2ff5098fad8eba6d632c7913e64321a2b248a7ef208c9f7e`.
The following numbers are the expanded, reproducible form of the accepted
viewer package's former `iso` shorthand. Candidate renders must use these
fixed values directly and must not refit to candidate bounds:

```text
projection                 orthographic
image                      1800 x1200 RGBA8
position                   [421.5618774220361,-421.5618774220361,332.9457800403248]
target                     [0.0543702719103261,-0.0543702719103261,-4.2602256797758]
up                         [0,0,1]
view direction             [0.6154574548966637,-0.6154574548966637,0.4923659639173310]
orthographic left/right    [-163.03291470718082,+163.03291470718082]
orthographic bottom/top    [-108.68860980478722,+108.68860980478722]
orthographic full scale    326.06582941436164 x217.37721960957444
near/far                   [0.01,2568.257381947491]
fit padding                0.04 per edge
zoom                       1.0
display/theme              solid / snapshot
```

The extraction authority is the accepted Phase-2A CAD Viewer package with
bounds `[-150.0000001,-150.0000001,-32.5000001]` to
`[150.0000001,150.0000001,24.2514001]`, its visible triangle vertices, and the
accepted image whose exact non-background bounding box is inclusive
`(72,92,1727,1107)`. The renderer is CAD Viewer/cadjs `0.4.19` with Three.js
`0.161.0`; device pixel ratio/render scale is exactly 1. The color pass uses
WebGL antialiasing enabled, alpha enabled, logarithmic depth enabled,
`preserveDrawingBuffer=true`, sRGB output, and ACES filmic tone mapping. A
fallback renderer, browser DPR scaling, auto-fit, changed mesh package, or
changed antialias setting is RED.

The authorization ID pass uses the same fixed camera, frustum, viewport,
triangle sidedness, depth ordering, and visible-solid set, with these exact
raster rules:

- 1800 x1200 `RGBA8`, DPR 1, one sample per pixel; MSAA/FXAA and all
  antialiasing are disabled;
- clear ID is integer 0 encoded `(0,0,0,0)`;
- the 144 authorized solids are the 18 `authorized_replacement` followed by
  the 126 `new_authorized` occurrences in exact registry order and receive
  integer IDs 1..144;
- encode ID as `(R=id&255, G=(id>>8)&255, B=(id>>16)&255, A=255)` with no sRGB
  conversion, tone mapping, lighting, shadows, edges, floor, blending,
  transparency, dithering, or post-processing;
- depth test and depth write are enabled with the normal `LEQUAL` rule and a
  24-bit depth attachment; color sampling/readback is nearest and exact;
- a pixel is authorized iff its decoded ID is 1..144; union those pixels,
  apply exactly a two-pixel Chebyshev dilation, then union the two inherited
  fixed-tower rectangles `(370,205,438,380)` and `(1495,390,1522,414)`.

The ID mask, not an RGB color threshold or hand-drawn region, is the sole I3
foreground authorization. Four- and eight-connected exterior XOR, foreground
XOR outside the final mask, and global outer-contour XOR must each equal zero.

## 5. Moving M2 head, driver, and adjacent-role clearance

At every moving seam, relative to that role's `z0_r`:

```text
Half B front face          zeta=3.08
button head envelope       D3.50 x1.20, zeta=[3.08,4.28]
driver envelope            D4.50 x8.00, zeta=[4.28,12.28]
driver/insertion direction +Z approach, swept downward to socket engagement
```

For the hour-to-minute and minute-to-second interfaces, the expected nominal
actual-solid axial clearance is:

`2.55-0.08-1.20 = 1.27 mm`.

The measured gate is at least 1.25 for every actual head/adjacent-role pair.
The second-role head and driver are additionally tested against the radially
separate front assembly by actual-solid sweep; axial interval overlap alone
does not waive the zero-IV requirement. Every driver sweep must have
IV<=`1e-7 mm3` against non-target solids in the authoritative assembly order.

## 6. Stationary fastener tolerance gates

### 6.1 Chassis M3 bridge wall

The accepted 12 x18 bridge and 5.70-square pockets retain nominal radial wall
3.15, tangential end wall 0.65, and inter-pocket material 5.30. After all
bores, slot/pocket cuts, chamfers, and exported/imported representation, the
minimum actual-solid wall from any M3 receiver to a non-opening exterior face
must be at least **0.60 mm**. Report the measured minimum and its owning seam,
bridge radius, receiver side, and closest-point pair. A sampled or nominal-only
claim is RED.

### 6.2 Stationary-frame M2 x4 screws

Measure every production screw from under-head bearing plane to tip. Each must
satisfy both:

```text
actual under-head length L_actual >= 3.80 mm
actual thread engagement = L_actual - actual frame stack >= 1.40 mm
```

The nominal frame stack remains 2.40 and the nominal 4.00 screw therefore has
1.60 engagement; the 0.20 short-length allowance is the tolerance reserve.
The actual nut height must still pass the maximum-1.60 incoming gate, the
driver path must remain clear, and screw/nut material IV must remain
<=`1e-7 mm3`. Nominal `M2x4` labeling without the two actual measurements is
RED.

## 7. Frozen registry and exactly 34 printable bodies

The I3 assembled occurrence registry remains exactly 275:

```text
131 protected_exact
 18 authorized_replacement
126 new_authorized
275 total
```

No class, label order, or count is changed by this amendment. The disassembled
`print_components.3mf` contains exactly 34 printable bodies:

```text
12 stationary quadrants = 4 chassis + 4 frame + 4 outer front ring
 6 moving halves        = 2 hour + 2 minute + 2 second
16 stationary bridges  = 8 chassis + 4 frame + 4 outer front ring
34 total
```

These are the 18 authorized replacements plus the 16 printable bridge members
within `new_authorized`. All 44 screws, 44 DIN 562 nuts, and 22 dowels/pins are
purchased hardware and must be present in assembly/BOM evidence but absent
from the printable-body count. An assembled compound, duplicated body,
omitted bridge, purchased-hardware mesh marked printable, or count other than
34 is RED.

## 8. Exact evidence files and manifest schema

Implementation evidence is rooted at:

`models/p3_v3_phase3_i3_u1_segmentation_joinery/`

The following filenames are mandatory; aliases do not satisfy the gate:

```text
i3_validation_manifest.json
i3_serializer_calibration.json
i3_authorized_roi_report.json
i3_nut_loading_report.json
i3_q_motion_report.json
i3_contact_whitelist_report.json
i3_fastener_access_report.json
i3_printable_body_manifest.json
i3_locked_copy_preservation_report.json
snapshots/i3_matched_candidate.png
snapshots/i3_authorized_id.png
snapshots/i3_authorized_roi_mask.png
```

`i3_validation_manifest.json` must contain keys
`schema_version`, `design_id`, `parent_spec_sha256`,
`parent_amendment_sha256`, `frozen_step_sha256`, `registry_count`,
`classification_counts`, `printable_body_count`, `artifacts`, `reports`,
`red_failures`, and `physical_validation_boundary`. `reports` maps each exact
JSON filename above to its relative path and SHA-256; `artifacts` does the same
for both STEP files, the 3MF, BOM, plate manifest, and three required PNGs.

The report-specific required keys are:

- `i3_serializer_calibration.json`: `fresh_process_runs`, `label_order_sha256`,
  `classification_counts`, `observed_maxima`, `applied_tolerances`,
  `maximum_occurrence_identity`, `protected_floor`, `violations`;
- `i3_authorized_roi_report.json`: `camera_contract`,
  `reference_png_sha256`, `candidate_png_sha256`, `id_raster_contract`,
  `authorized_id_count`, `id_png_sha256`, `roi_mask_png_sha256`,
  `inherited_fixed_tower_rois`, `exterior_xor_4`, `exterior_xor_8`,
  `foreground_xor_outside_mask`, `outer_contour_xor`;
- `i3_nut_loading_report.json`: `assembly_order`, `moving_receivers`,
  `frame_receivers`, `front_ring_receivers`, `measured_nut_heights`,
  `loading_sweeps`, `capture_state`, `obstruction_max_iv_mm3`, `violations`;
- `i3_q_motion_report.json`: `motor_samples`, `motor_cartesian_state_count`,
  `tower_samples`, `q_state_count`, `target_angle_rule`,
  `target_angle_count_per_role`, `other_ring_angle_rule`, `role_state_count`,
  `total_state_count`, `broadphase_proof`, `role_shortcuts`, `violations`;
- `i3_contact_whitelist_report.json`: `allowed_positive_pairs`,
  `expected_press_iv_mm3`, `observed_press_iv_mm3`, `unexpected_positive_pairs`,
  `maximum_nonwhitelist_iv_mm3`, `violations`;
- `i3_fastener_access_report.json`: `moving_head_clearances_mm`,
  `moving_driver_sweeps`, `chassis_m3_minimum_walls_mm`,
  `frame_m2_under_head_lengths_mm`, `frame_m2_thread_engagements_mm`,
  `stationary_driver_sweeps`, `violations`;
- `i3_printable_body_manifest.json`: `body_count`, `class_counts`, `bodies`,
  `hardware_excluded_count`, `duplicate_labels`, `missing_labels`,
  `plate_occurrence_count`, `violations`;
- `i3_locked_copy_preservation_report.json`: `files`,
  `preimplementation_sha256`, `postimplementation_sha256`,
  `byte_identical`, `protected_occurrence_count`, `protected_digest_sha256`,
  `violations`.

The locked-copy report's `files` must include the frozen Phase-2A STEP, the
accepted I1 reference PNG, I3.1, and I3.2. Every corresponding pre/post hash
must match and `byte_identical` must be true. The main manifest is GREEN only
when every `violations` and `red_failures` array is empty, every referenced
file exists, and every recorded SHA-256 recomputes exactly.

## 9. Added RED inventory

All earlier RED rules remain active. I3.3 additionally makes RED: a closed or
non-loadable frame/front receiver; incorrect moving-pin interval or press IV;
a non-Cartesian or role-reused motion matrix without proof; any camera
auto-fit or raster ambiguity; moving-head clearance below 1.25; M3 actual wall
below 0.60; frame M2 under-head length below 3.80 or engagement below 1.40;
registry/classification drift; a printable-body count other than 34; a missing
required report/key/hash; or any failure of locked-copy preservation.
