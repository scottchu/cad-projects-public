# KAGE P3 V3 Phase-3 I3.4 — rejection closure and executable handoff

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation**

Date: **2026-08-19**

Supersedes: `p3-v3-phase3-i3-3-design-amendment.md` wherever this document is
more specific or conflicting.

Normative predecessors and immutable SHA-256 values:

```text
I3.1  abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77
I3.2  9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3
I3.3  4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

I3.4 closes both independent rejection reviews. It does not authorize changes
to the functional 300 mm clock, protected geometry, active teeth, R131.60
races, ring Z datums, occurrence classes, or accepted hardware quantities.
All earlier values not expressly superseded remain active.

## 1. Frame/front receiver-family supersession

I3.4 explicitly supersedes the inherited requirement that every stationary
M2 nut be captive in its bridge before quadrant closure for these two receiver
families only:

```text
stationary_frame_open_jig_captured_M2
outer_front_ring_open_jig_captured_M2
```

Their dimensions remain the I3.3 radially open slots:

```text
R=[145.70,150.20], tangent width=4.20 at t=+/-5.00, depth=1.70
inner ligament=1.20, tangential end ligament=0.90, hour-fin clearance=0.60
```

No friction-fit mouth lip is added. A thin positive mouth feature would either
block the required +Z square-nut loading envelope or introduce a subminimum
printable lip; the controlled jig/closure sequence is the safer receiver
contract. Final installed nuts are positively captured by the closed quadrant
and screw, but the bridge alone is not a captive-nut carrier.

The only authorized sequence is:

1. Clamp the bridge on the flat datum jig, whose R150 fence positively closes
   both radial mouths.
2. Load height-qualified, deburred nuts from the +Z approach side.
3. Keep the jig fence engaged while placing and clamping the quadrant.
4. Install both screws and verify thread engagement.
5. Remove the closed, screwed subassembly from the jig.

There is no transport, inversion, release, or handoff state containing an open
bridge and loose nuts. `assembly_state_manifest.json` must model the jig as an
assembly fixture and prove that every transition from nut loading through
screw engagement retains either the jig fence or the closed quadrant. Rear
chassis and moving-lap captive-pocket rules are not superseded. Treating the
frame/front bridge alone as captive, omitting the jig, closing one mouth while
the other is free, or permitting a loose-nut handling state is RED.

## 2. Moving pin and tool-vector contract

For all six moving seams, coordinates are local `zeta=Z-z0_r`. The pin axis is
at R=136.75, tangent=0. The exact final stack is:

```text
D3.00 x3.00 pin final interval       zeta=[0.00,3.00]
Half A D2.95 press interval          zeta=[0.00,2.00]  length 2.00
open lap gap                         zeta=(2.00,2.08)  length 0.08
Half B D3.10 slip interval           zeta=[2.08,3.00]  length 0.92
Half B front recess                  zeta=(3.00,3.08]  length 0.08
front recess cylindrical envelope    D3.10, coaxial with the pin
```

The front recess is the final 0.08 of one continuous D3.10 Half B through
access envelope from `zeta=2.08` through `zeta=3.08`. It may not taper below
D3.10 or contain a chamfer whose inscribed diameter is below D3.10. This
freezes a D3.10 x1.00 total Half B passage and makes D3.00 pin insertion
geometrically possible while leaving the final pin 0.08 recessed.

The assembly fixture supports the rear stop at `zeta=0`. The approach side is
**+Z**, while the insertion tool and pin travel vector is **-Z**. The tool
enters through the D3.10 front recess/slip passage and drives the pin until its
rear end contacts the stop. Any statement that the pin moves +Z during this
operation is superseded and RED.

The moving press-pair expected IV remains:

`pi/4*(3.00^2-2.95^2)*2.00 = 0.4673119072 mm3`.

The lap gap, Half B slip passage, and front recess permit no positive IV.

## 3. Moving screw-driver direction

Every moving M2 button head remains D3.50 x1.20 at
`zeta=[3.08,4.28]`. The D4.50 x8.00 driver envelope begins at
`zeta=4.28`. The driver approach side is **+Z** and its engagement sweep vector
is **-Z**. It retracts along +Z. The previous phrase “+Z approach” never means
+Z insertion motion.

Actual adjacent-role head clearance remains expected 1.27 and must be at least
1.25. Driver sweeps require IV<=`1e-7 mm3` against every non-target solid in
the modeled assembly order.

## 4. Correct camera-vector semantics

I3.3's numeric camera position, target, up, frustum, padding, near/far,
renderer, DPR, and antialias values remain unchanged. Its positive vector was
labeled ambiguously. The exact semantics are now:

```text
camera backward / local +Z / target-to-position
  [ +0.6154574548966637,-0.6154574548966637,+0.4923659639173310 ]

camera forward / local -Z / position-to-target
  [ -0.6154574548966637,+0.6154574548966637,-0.4923659639173310 ]
```

The camera looks along the second vector. A test that calls the first vector
“forward,” reverses ray direction, or swaps target and position is RED.

## 5. Accepted mesh and exact color/ID raster contract

The authoritative accepted render package is:

`models/p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention/__cadgen__/models/p3_v3_r1_i1_fixed_tower_retention_assembled.step/assembly.json`

Its SHA-256 is
`2c25e2ae0db56cd24837c62f01764756752d421f79b2dafe4d36d67d8c907762`.
It is package schema 3; component identity is the complete component map and
each component `contentHash` recorded by that exact file. Rendering from a
regenerated package, a different assembly JSON, or a component whose bytes do
not match its recorded content hash is RED.

### 5.1 Color-pass foreground predicate

The accepted reference is 1800 x1200 RGBA8 with top-left background
`(240,244,249,255)`. After the accepted antialiased color render and PNG
readback, a pixel is foreground iff at least one of its RGB bytes differs
exactly from `(240,244,249)`; alpha is ignored for this predicate. No threshold,
color distance, premultiplication adjustment, or background re-estimation is
allowed.

For all PNG reports, pixel `(0,0)` is the top-left, +x is right, and +y is
down. WebGL framebuffer readback has bottom-left origin and must be vertically
flipped exactly once before PNG encoding, mask construction, ROI coordinates,
or hashing. A zero flip or double flip is RED.

### 5.2 Triangle sidedness

Both color and ID solid passes use CCW front faces, `FrontSide` material, and
back-face culling enabled. The ID pass must use the exact accepted visible
triangle positions and occurrence transforms. Edge lines do not write ID or
depth. Two-pixel Chebyshev dilation remains responsible for the antialiased
visible edge allowance.

### 5.3 Protected occlusion and ID 0

Clear color is ID 0 `(0,0,0,0)` and clear depth is 1. Render all 275 assembled
occurrences into one shared 24-bit depth buffer with `LEQUAL`, depth test on,
and depth write on:

- all 131 `protected_exact` occurrences are depth-only occluders and retain
  color ID 0;
- the 18 `authorized_replacement` followed by 126 `new_authorized`
  occurrences receive IDs 1..144 in exact registry order and write both depth
  and encoded ID;
- an authorized surface hidden by a protected surface remains ID 0;
- an authorized surface in front of a protected surface writes its nonzero ID;
- removed legacy occurrences and non-solid references render neither depth nor
  ID.

ID 0 therefore means background **or visible protected surface**, never
“ignore depth.” The rest of the I3.3 ID encoding, disabled AA/blending/sRGB/
tone-mapping/dither rules, fixed camera, top-left output convention, dilation,
and inherited fixed-tower ROI union remain unchanged.

## 6. Exact 22-label press-IV maps

`i3_contact_whitelist_report.json` contains two JSON objects named
`expected_press_iv_by_label_mm3` and `observed_press_iv_by_label_mm3`. Each
must contain exactly the following 22 keys, in this order, with no wildcard or
summary substitution:

| label | exact expected IV mm3 |
|---|---:|
| `i3_hour_seam_1_dowel` | 0.4673119072 |
| `i3_hour_seam_2_dowel` | 0.4673119072 |
| `i3_minute_seam_1_dowel` | 0.4673119072 |
| `i3_minute_seam_2_dowel` | 0.4673119072 |
| `i3_second_seam_1_dowel` | 0.4673119072 |
| `i3_second_seam_2_dowel` | 0.4673119072 |
| `i3_chassis_seam_01_bridge_R085_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_01_bridge_R120_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_02_bridge_R085_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_02_bridge_R120_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_03_bridge_R085_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_03_bridge_R120_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_04_bridge_R085_D4x6_dowel` | 1.2487830798 |
| `i3_chassis_seam_04_bridge_R120_D4x6_dowel` | 1.2487830798 |
| `i3_frame_seam_01_D3x5_dowel` | 0.6075054794 |
| `i3_frame_seam_02_D3x5_dowel` | 0.6075054794 |
| `i3_frame_seam_03_D3x5_dowel` | 0.6075054794 |
| `i3_frame_seam_04_D3x5_dowel` | 0.6075054794 |
| `i3_front_ring_seam_01_D2x4_dowel` | 0.4653484118 |
| `i3_front_ring_seam_02_D2x4_dowel` | 0.4653484118 |
| `i3_front_ring_seam_03_D2x4_dowel` | 0.4653484118 |
| `i3_front_ring_seam_04_D2x4_dowel` | 0.4653484118 |

The values are respectively:

```text
moving  pi/4*(3.00^2-2.95^2)*2.00 = 0.4673119072
chassis pi/4*(4.00^2-3.95^2)*4.00 = 1.2487830798
frame   pi/4*(3.00^2-2.95^2)*2.60 = 0.6075054794
front   pi/4*(2.00^2-1.95^2)*3.00 = 0.4653484118
```

The observed map must have the identical ordered key set and one actual-solid
numeric result per key. Every observed value must equal its expected value
within `1e-7 mm3`. The whitelist contains exactly these 22 pin/own-press-bore
pairs; every other pair requires IV<=`1e-7 mm3`.

## 7. Feasible moving-half print placement

I3.4 preserves the I3.2 +30.000-degree rotation, source geometry, assembly
transform, functional R140 envelope, and 300 mm clock size. It supersedes only
the moving-half fallback-bed assignment and stale 238.99 footprint claim.

The reviewed worst-axis raw actual-solid footprint is **244.864483 mm**. With
the required 3.50 brim on each side:

```text
packed footprint = 244.864483 + 2*3.50 = 251.864483 mm
```

Therefore every moving half is assigned only to the 270 mm bed with 5.00 edge
keepout, whose usable square is `[5.00,265.00]^2`, exactly 260.00 x260.00. The
source-to-print transform remains:

1. rotate +30.000 degrees about source global +Z through the clock origin;
2. translate Z by `-bbox_min_Z`;
3. translate the rotated actual-solid AABB centre to `(135.00,135.00)`.

Reserve a centred 244.864483-square raw XY envelope. Its exact bounds are:

```text
raw reserved XY       [12.5677585,257.4322415]^2
3.50-brim packed XY   [ 9.0677585,260.9322415]^2
usable-bed XY         [ 5.0000000,265.0000000]^2
per-edge packed slack 4.0677585 mm
total-axis slack      8.1355170 mm
```

The implementation must report each rotated actual-solid bbox; both actual
spans must be <=244.864483 and the full support/skirt/purge envelope must stay
inside the packed reserved square and usable bed. A larger measured result is
RED and cannot be waived by clipping adhesion geometry.

For moving-half plates the packed-square calculation is closed by setting
external skirt loops to 0, support XY expansion outside the raw silhouette to
0, and object-attached purge geometry to none. Required support may exist only
inside the raw XY projection. The printer's independent startup purge line is
recorded as a separate plate-service envelope inside `[5.00,265.00]^2`; it may
not intersect the packed square. Thus the 3.50 brim is the sole object-envelope
XY expansion and 251.864483 is the exact full packed width, not a lower bound.
The startup purge-line reserved rectangle is exactly
`X=[5.50,8.50], Y=[10.00,260.00]`; it is inside the usable bed and clears the
packed square by `9.0677585-8.50=0.5677585 mm`.

The 260 mm physical fallback has only `[5.00,255.00]^2`, or 250.00 usable.
It is short by `251.864483-250.00=1.864483 mm` and is forbidden for all six
moving halves. Stationary bodies may still use it when their independently
measured full envelopes pass. No ring scaling, seam movement, tooth removal,
geometry shrink, brim clipping, diagonal bed overhang, or protected change is
authorized.

## 8. Acyclic manifest and exact artifact contract

The evidence root remains
`models/p3_v3_phase3_i3_u1_segmentation_joinery/`. The exact required primary
artifacts are:

```text
assembled_nominal.step
service_exploded.step
print_components.3mf
source_import_parity_manifest.json
purchased_hardware_bom.json
assembly_state_manifest.json
plate_manifest.json
i3_validation_manifest.json
i3_validation_manifest.sha256
snapshots/i3_matched_candidate.png
snapshots/i3_authorized_id.png
snapshots/i3_authorized_roi_mask.png
```

The exact subsidiary report filenames remain:

```text
i3_serializer_calibration.json
i3_authorized_roi_report.json
i3_nut_loading_report.json
i3_q_motion_report.json
i3_contact_whitelist_report.json
i3_fastener_access_report.json
i3_printable_body_manifest.json
i3_locked_copy_preservation_report.json
```

I3.3's self-hash cycle is superseded. `i3_validation_manifest.json` must never
contain its own SHA-256 or the SHA-256 of its detached checksum file. Its
`reports` object contains path/SHA entries for exactly the eight subsidiary
reports. Its `artifacts` object contains path/SHA entries for the three export
files, the four named non-validation JSON manifests/BOM, and the three PNGs.
After the manifest bytes are final, write
`i3_validation_manifest.sha256` as one lowercase line:

`<64 lowercase hex><two spaces>i3_validation_manifest.json`.

That detached file is not referenced from inside the manifest. Verification
recomputes the manifest hash and compares it with the detached line, so the
graph is acyclic.

The main manifest must contain `i3_1_spec_sha256`,
`i3_2_amendment_sha256`, `i3_3_amendment_sha256`, and
`i3_4_amendment_sha256`. The first three equal the constants at the top of
this document. The I3.4 value is the externally published SHA-256 of this
final immutable file; it is deliberately not embedded in itself. The RED
suite and `i3_locked_copy_preservation_report.json` must freeze that published
value before implementation acceptance.

The locked-copy report must include pre/post byte hashes and `byte_identical`
for the frozen STEP, accepted reference PNG, I3.1, I3.2, I3.3, and I3.4. Its
I3.4 pre-hash is taken before implementation source work, not before drafting
this amendment. Any mismatch is RED.

## 9. RED-suite correction matrix

The implementation may amend the RED suite only to encode this accepted
contract. The required assertions are exact:

| assertion | required value |
|---|---:|
| registry count | 275 |
| `protected_exact` | 131, never 136 |
| `authorized_replacement` | 18 |
| `new_authorized` | 126 |
| printable bodies | 34 |
| moving adjacent-role clearance gate | >=1.25, not 1.35 |
| moving adjacent-role expected clearance | 1.27 |
| q states | 189540 |
| positive press-pair labels | exactly 22 |
| M3 actual minimum wall | >=0.60 |
| frame M2 actual under-head length | >=3.80 |
| frame M2 actual thread engagement | >=1.40 |

The suite must also assert the two open receiver-family names and mouth
dimensions; jig-retained assembly states; moving pin final/press/gap/slip/
recess intervals `3.00/2.00/0.08/0.92/0.08`; +Z approach with -Z pin and
driver sweeps; corrected camera forward/backward vectors; accepted package
path/hash; protected ID-0 depth occlusion; top-left readback; exact report and
artifact filenames; acyclic detached manifest hashing; the moving-half
251.864483-on-260 packing gate and fallback prohibition; all four published
spec hashes; empty violation arrays; and locked-copy preservation.

Tests may not change a design value merely to turn RED green. Missing schema
keys, a wildcard press map, a stale 136 count, stale 1.35 clearance, fewer than
189540 states, hidden open mouths, any incorrect tool vector, 250-bed moving
half placement, registry/class drift, or altered predecessor hash is RED.

## 10. Preserved acceptance boundaries

The occurrence registry remains exactly
`131 protected_exact + 18 authorized_replacement + 126 new_authorized = 275`.
The 3MF remains exactly 34 printable bodies: 12 stationary quadrants, 6 moving
halves, and 16 stationary bridges. Purchased quantities remain 44 screws, 44
DIN 562 nuts, and 22 pins/dowels. M3 actual wall remains at least 0.60; frame
M2 actual under-head length remains at least 3.80 with at least 1.40 thread
engagement. All physical print-fit, warp, TIR, wear, strength, optical, noise,
and full-rotation proof remains outside CAD acceptance and must be reported
separately.
