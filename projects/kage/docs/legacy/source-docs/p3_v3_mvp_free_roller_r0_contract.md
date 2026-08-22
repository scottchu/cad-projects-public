# P3 V3 MVP free-roller R0 contract

Status: **critic-corrected design contract; implementation may proceed**. No CAD, STEP, 3MF, simulator, or locked-baseline file is changed by this document.

Independent mechanical-critic disposition: the prior drafts were **REJECTED** because they either tapped M4 directly into the accepted printed base or added an underside captive-nut bar that destroyed the required flat rear datum. They also allowed neighboring spools to bear on one shared spacer without isolating thrust washers and treated the upper bridge as optional even though a fixed bridge obstructs complete-ring installation. The corrected contract below uses top-entering `M3 x 8` screws and ordinary M3 nuts captured wholly inside the existing step-lap interface at only the outer hole pair, six independent thrust washers per station, and a mandatory removable upper bridge. Remaining friction, wear, stiffness, and printed-thread behavior are physical prototype gates rather than CAD claims.

## 1. Decision and scope

Create one passive free-roller station and place three rotationally identical instances at `60 deg`, `180 deg`, and `300 deg`. Each station bolts only to the existing **outer** Q3 seam-hole pair at `R118.00, T +/-7.00`; the existing **inner** pair at `R76.00, T +/-7.00` remains a plain base-seam screw pair and may not be used by the station.

Each station carries three mechanically independent, free-spinning flanged spools on one common vertical axle: one spool for each of the locked hour, minute, and second carrier layers. The ring's existing smooth inner carrier root land is the running surface. There is no continuous or segmented stationary guide rail beneath any ring, no driven roller, and no motor, pinion, gear train, sensor, PCB, wiring, battery, or other electronics in this branch.

The following are immutable inputs:

- `models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/`, including its source and tests snapshots;
- `p3_v3_direct_gear_race_guidance_spec.py` and `p3_v3_direct_gear_race_guidance_geometry.py`, which are currently byte-identical to that locked source snapshot;
- the accepted Q3 r0 base-sector source/export and its four-hole seam pattern, retained unchanged as the locked reference.

Implementation must be a new branch/namespace. It may import or copy numeric intent from the locked sources, but it must not edit or regenerate the locked directory or overwrite the accepted Q3 r0 sector. The branch-owned derivative sector may add only the two internal M3-nut pockets described below at each seam; its front face, rear face, outer envelope, step-lap seating faces, and all four existing D3.30 through-hole axes remain unchanged.

Units are millimetres. The clock plane is XY, `+Z` faces the viewer, and seam-local coordinates are radial `R`, tangential `T`, and axial `Z`. Station geometry is authored once at the zero-degree local seam and placed only by exact Z-axis rotations.

## 2. Frozen interfaces and named parameters

### Base and station placement

| Parameter | Value | Contract meaning |
|---|---:|---|
| `station_angles_deg` | `(60, 180, 300)` | Exactly three passive station instances |
| `base_outer_radius_mm` | `150.00` | Accepted Q3 base envelope |
| `base_plate_z_mm` | `(-31.50, -25.50)` | Accepted 6 mm base plate |
| `station_seat_z_mm` | `-25.50` | Station sits directly on the base top face |
| `outer_mount_radius_mm` | `118.00` | Existing outer Q3 seam-hole row |
| `outer_mount_tangent_mm` | `(-7.00, +7.00)` | Both outer holes used by every station |
| `base_outer_hole_diameter_mm` | `3.30` | Existing geometry; do not remodel or relocate |
| `inner_seam_radius_mm` | `76.00` | Plain base-seam screw row only |
| `inner_seam_tangent_mm` | `(-7.00, +7.00)` | Two plain seam screws per seam |
| `station_mount_slot_width_mm` | `3.60` | M3 clearance in the new station foot only |
| `station_mount_slot_length_mm` | `4.10` | Radial capsule length; gives 0.50 mm center travel |
| `station_mount_slot_center_travel_mm` | `0.50` | Common setup range, `+/-0.25` radial |
| `station_foot_z_mm` | `(-25.50, -22.50)` | 3 mm integral foot; no separate flat strap below it |
| `station_foot_r_mm` | `(112.50, 130.00)` | Covers both mount axes and supports the axle column |
| `station_foot_t_mm` | `(-12.50, +17.20)` | Bridges and face-contacts both seam owners |

All three stations have the same two radial slots. There is no special “adjustable third station.” Adjustment is a setup allowance only; the clamped operating position must satisfy the measured ring-clearance gates below.

The outer D3.30 holes remain untapped M3 clearance holes on their existing axes. Each station uses two top-entering `M3 x 8` socket screws and `D7` washers through the radial slots and the upper step-lap leaf into two ordinary M3 nuts. Each nut is captured in an individual blind hex pocket opened only to the internal step-lap mating face. The mating lower leaf closes the pocket when the sectors are assembled. No nut, bar, screw head, pocket, or plug may break or stand proud of the base rear plane at `Z=-31.50`; the assembled rear datum remains one uninterrupted planar support surface.

The two outer nut pockets are branch-owned derivative features, not edits to the locked Q3 r0 artifact. Size each pocket from the measured nuts, nominally `5.70 mm` across flats and `2.50 mm` deep, with the nut axis coincident with the existing D3.30 bore. Preserve at least `0.50 mm` closed front skin above each pocket and verify that the selected `M3 x 8` screw achieves at least `2.0 mm` thread engagement without contacting the lower leaf. The pockets capture only the **outer** R118 pair and may not connect to, touch, or bridge either inner R76 hole. The outer screws and nuts may assist local seam clamp-up, but the inner pair remains the sole plain base-join screw pair. Production may replace each ordinary nut pocket with a separately approved heat-set-insert interface, but that is outside R0.

The six inner holes remain ordinary D3.30 clearance holes with M3 screw, washer, and nut stacks. They close the base seams before the base is placed flat on its assembly datum. They do not pass through the station foot.

### Locked ring and running geometry

| Parameter | Value | Contract meaning |
|---|---:|---|
| `carrier_layers_z_mm` | `((-1.50,1.50),(4.05,7.05),(9.60,12.60))` | Locked H/M/S carrier layers |
| `carrier_race_radius_mm` | `131.60` | Smooth inner cylinder; only allowed running surface |
| `race_land_depth_mm` | `0.80` | Lower tooth-free land on each carrier |
| `contact_land_width_mm` | `0.60` | Spool running-band axial width |
| `tooth_tip_radius_mm` | `129.00` | Forbidden tooth-tip envelope boundary |
| `roller_axis_radius_nominal_mm` | `125.50` | Common axle centerline at each station |
| `roller_axis_setup_mm` | `+/-0.25` | Slot capacity, not an automatically accepted operating range |
| `roller_axis_operating_tolerance_mm` | `+/-0.05` | Maximum locked deviation after setup |
| `spool_bore_diameter_mm` | `4.06` | Finished free-running bore |
| `axle_finished_diameter_mm` | `3.99` | Polished axle diameter |
| `spool_hub_od_mm` | `6.00` | Clears the tooth-tip envelope |
| `spool_running_od_mm` | `12.10` | Gives `0.05` nominal radial running gap |
| `spool_flange_od_mm` | `13.80` | Gives `0.80` nominal radial capture overlap |
| `spool_flange_thickness_mm` | `0.50` | Lower and upper flange thickness |
| `spool_face_clearance_mm` | `0.15` | Clearance from each carrier axial face |
| `spool_step_fillet_mm` | `0.30` | Maximum step fillet |
| `spool_edge_chamfer_mm` | `0.20` | Edge break |

The three spools are geometrically identical and differ only by their Z placement. Their ranges are:

| Role | Carrier race/contact Z | Complete spool Z | Lower/upper flange Z |
|---|---|---|---|
| Hour | `-1.40 .. -0.80` | `-2.15 .. 2.15` | `-2.15 .. -1.65` / `1.65 .. 2.15` |
| Minute | `4.15 .. 4.75` | `3.40 .. 7.70` | `3.40 .. 3.90` / `7.20 .. 7.70` |
| Second | `9.70 .. 10.30` | `8.95 .. 13.25` | `8.95 .. 9.45` / `12.75 .. 13.25` |

Nominal radial running gap is `131.60 - (125.50 + 12.10/2) = 0.05`. Nominal flange overlap is `(125.50 + 13.80/2) - 131.60 = 0.80`. At the accepted `+/-0.05` operating tolerance, running gap must remain in `0.00 .. 0.10` and flange overlap in `0.75 .. 0.85`. The D6 hub retains at least `0.45` clearance to the R129 tooth tip at the worst accepted outward position. Tooth flanks and tooth tips are not rolling surfaces.

### Axle stack, frame, and fin corridor

| Parameter | Value | Contract meaning |
|---|---:|---|
| `axle_nominal_mm` | `D4 x 25` | Polished straight pin/shaft, finished D3.99 running surface |
| `axle_z_mm` | `(-5.00, 20.00)` | One common axle through all three spools |
| `lower_socket_depth_mm` | `1.10` | Blind lower locator; axle is not a base fastener |
| `spacer_qty_per_station` | `2` | Independent D6 spacers between spools |
| `spacer_length_mm` | `(0.80, 0.80)` | Fixed tube between two 0.20 mm thrust washers; leaves 0.05 mm residual axial play in each 1.25 mm inter-spool gap |
| `spacer_bore_mm` | `4.20` | Must not drag on axle |
| `thrust_washer_qty_per_station` | `6` | One on each axial face of every spool; neighboring spools never share a dry printed thrust face |
| `thrust_washer_mm` | `D6 x D4.2 x 0.20` | Low-friction thrust washers |
| `lower_post_top_z_mm` | `-2.45` | Fixed lower post ends 0.10 mm below the lower thrust washer |
| `upper_bushing_z_mm` | `(13.55, 14.85)` | Mandatory removable bridge/bushing; 0.10 mm above the upper thrust washer |
| `retainer_collar_mm` | `D4 bore, D10 OD x 4` | Purchased metal split/set-screw shaft collar |
| `retainer_collar_z_mm` | `(15.00, 19.00)` | Top-accessible axle retention; verify set-screw tool access with all rings installed |
| `stationary_radius_limit_mm` | `134.70` | Absolute stationary limit in every swept fin Z band |
| `minimum_fin_clearance_mm` | `0.80` | Required actual-solid clearance to every 360-degree fin sweep |

The frame is an open, two-sided tower with an integral flat foot, lower axle socket/post, two inboard backbones, and a **mandatory removable** upper axle bridge/bushing. No frame member may form an arcuate rail beneath a ring. The implementation keeps the legacy backbone centers at `R110.20, T +/-5.50`, a `2.50 x 2.50` backbone section, and the upper bridge inside `R107.80 .. 131.10`, `T +/-7.70`, `Z13.55 .. 14.85`. The bridge-only critic repair preserves the screw axes at `R111.00, T +/-4.50` and the D3.40 clearance bores, producing `1.50 mm` minimum solid ligament at both the inboard radial edge and tangential edges. The bridge positively re-registers to the identical station body and is retained by two top-accessible `M3 x 6` screws into replaceable printed M3 nut pockets in the backbones. Production heat-set inserts are a later substitution. The bridge, nut pockets, screw heads, and tool envelopes must remain inside the same stationary envelope and must pass the fin-sweep test.

The locked fin sweep envelopes are actual acceptance geometry, not visual references: hour root/blade `R135.50 .. 143.90`, minute root/blade `R135.50 .. 141.95`, and second blade `R137.20 .. 138.40`, over their locked Z ranges. Every stationary printed part, axle, collar, mounting head, and service-fastener envelope must have zero BREP intersection with all three complete 360-degree sweeps. The nominal spool-flange outer radius is `132.40`, leaving `3.10` to the governing R135.50 fin root.

## 3. Parts and quantities

One canonical geometry is repeated; no angle-specific printable variants are allowed. The derivative-sector 3MF intentionally contains exactly **one object and one build item** with manifest `print_quantity = 3`. It is one canonical sector file to print three times, not a three-sector plate: three copies do not fit together on the Snapmaker U1 bed.

| Item | Per station | Total | Source |
|---|---:|---:|---|
| Identical branch-derivative Q3 base sector | - | 3 | Locked r0 geometry plus the two permitted internal outer-nut pockets |
| Identical station frame/yoke | 1 | 3 | New print part |
| Identical removable upper bridge | 1 | 3 | New print part; mandatory for complete-ring installation/service |
| Identical flanged spool | 3 | 9 | POM preferred; low-friction print permitted for prototype |
| D6 x D4.2 x 0.80 spacer | 2 | 6 | Printed or purchased fixed separator tube |
| D6 x D4.2 x 0.20 thrust washer | 6 | 18 | Purchased low-friction washer; one on each spool face |
| Polished D4 x 25 axle | 1 | 3 | Purchased |
| D4 x D10 x 4 shaft collar and matching set screw | 1 | 3 | Purchased metal hardware |
| M3 x 8 socket station screw | 2 | 6 | Existing hardware; top-side into an internally captured nut |
| M3 D7 washer | 2 | 6 | Under station screw heads; must fully cover the adjustment slots |
| M3 nut for station mount | 2 | 6 | Purchased; captured inside the step-lap at the outer R118 pair |
| M3 x 6 removable-bridge screw | 2 | 6 | Existing hardware; top-side service |
| Replaceable printed bridge nut | 2 | 6 | Prototype-only; production heat-set insert later |
| M3 plain inner seam screw | 2 | 6 | Purchased, length selected from measured base stack |
| M3 washer | 4 | 12 | Purchased, one under head and nut |
| M3 nut | 2 | 6 | Purchased |

No printed axle, printed shaft collar, bearing substituted for a spool, or shared three-ring roller is allowed. Each spool must rotate without transmitting torque to either neighboring spool.

## 4. Print and assembly contract

- Base: derive one sector from the locked r0 source, add only the two permitted internal outer-nut pockets, and print the one-object canonical file three separate times in the accepted diagonal flat orientation. Do not duplicate three sectors into the 3MF, because that is not a valid U1 single-bed layout. Do not add station geometry to the sector export and do not overwrite the locked r0 artifact.
- Station frame: print quantity three from one canonical file. The plate-contact face is the datum and preferred bed face. The upper bridge is always a separate identical part; do not accept support scars on axle, spool, fastener, or registration surfaces.
- Station nuts: load two ordinary M3 nuts into the outer blind pockets from the internal step-lap mating face before joining the sectors. No separate underside print part is permitted.
- Spools: print quantity nine flat with axle axis vertical; use concentric walls and ream every bore to `4.06`. POM is preferred where available. A printed low-friction material is prototype-only until wear testing passes.
- Spacers: print quantity six flat with axis vertical, or buy dimensioned D6/D4.2 spacers.
- Do not print shaft collars, thrust washers, axles, or screw/nut hardware.

Assembly/service sequence:

1. Before closing each step lap, load the two outer M3 nuts into their internal pockets at R118. Keep the inner R76 hardware independent. Join the three branch-derivative Q3 sectors on a flat R150 datum jig and tighten the six plain inner seam screws. Verify seam closure, the unmarked rear datum, and free-state base flatness.
2. Seat the three identical station frames on the base top face with their upper bridges removed. Install six `M3 x 8` station screws plus D7 washers from above into the captured nuts. Set each axle datum initially at R125.50 and lock only after the measured running-gap test passes.
3. Install the three complete bare rings in their locked Z order while every axle, spool, and removable upper bridge is absent. The stationary foot, lower post, and two inboard backbones must clear the complete axial insertion path. A segmented-ring-only workaround is not accepted.
4. At each station, load the stack radially from the clock center in this order: lower washer, hour spool, washer, 0.80 spacer, washer, minute spool, washer, 0.80 spacer, washer, second spool, upper washer. Use a removable alignment mandrel/comb if needed; it is tooling, not retained geometry. The 0.05 mm residual in each inter-spool gap is intentional and must remain measurable after export.
5. Register and fasten the removable upper bridge using its two `M3 x 6` screws and replaceable printed nuts. Insert the polished axle from the top through the bridge/bushing and loose stack into the blind lower socket. Fit the purchased collar at `Z15.00 .. 19.00` and tighten its set screw. Confirm collar set-screw tool access and all three spools' independent spin before moving to the next station.
6. Rotate each ring independently and then all three together through at least 360 degrees. Any fin contact, tooth contact, spool binding, or neighbor-spool coupling is a failure.
7. For spool service, remove collar and axle from the top, then withdraw the spool/washer/spacer stack radially toward the center; the bridge may remain installed if the verified path clears. For complete-ring removal, remove the upper bridges first. The base and all inner seam screws remain installed. Ring removal must not require removing a base sector.

## 5. Conflict with the current flat Q3 r2 roller strap

The r2 part in `p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_*` is a flat `R113.35 .. 122.65`, `T-11.65 .. +17.20`, `Z-25.50 .. -22.50` two-hole strap. It is **not** a usable station frame for this contract and must not be stacked with the new station.

Specific conflicts:

1. Its full Z band is the proposed integral station-foot band, so a coplanar station foot intersects it; placing the station on top instead shifts every axle/spool datum by +3 mm and misaligns all three locked carrier layers.
2. It ends at R122.65, 2.85 mm inboard of the required R125.50 axle, so it provides no lower axle socket or column support.
3. It has no upper bushing/bridge, axle retention, independent spacers, thrust washers, or spool-support geometry.
4. Its loose M3 nut envelope requires repeated underside nut access. R0 instead captures the nuts inside the closed step-lap interface and provides routine top-side station service while preserving the flat rear datum.
5. The legacy tower source uses mount axes `R119.50, T +/-4.50`; those do not align with the Q3 outer holes at `R118.00, T +/-7.00`. Reusing the old tower unchanged is therefore also forbidden.
6. Its broad ring keep-out begins at the base top plane and treats the intentional roller interaction region as forbidden. The new branch must replace that proxy with actual locked ring, tooth, fin-sweep, and station solids.

Accordingly, r2 remains historical/reference evidence only. The R0 station integrates the outer-pair mounting foot and supersedes the separate r2 strap as a print part. The new branch derives its sector from accepted r0 and adds only the internal outer-nut pockets; the locked r0 source/export itself remains unchanged.

## 6. Acceptance tests

### Source and deterministic CAD gates

1. Hash every file in the locked baseline directory before and after generation; require exact equality. Require the accepted Q3 r0 sector BREP/export to remain byte-identical.
2. Assert exactly three station occurrences at `(60,180,300)` and nine spool occurrences. Rotate every station back to zero degrees and require source-solid identity within `1e-6 mm3` volume and `1e-6 mm` bounds.
3. Assert each station foot has exactly two `3.60 x 4.10` radial slots centered on the existing outer axes `R118,T+/-7`; assert zero station geometry or station hardware on either inner R76 axis. On the actual assembled step-lap solids and measured nuts, assert each `M3 x 8` screw has at least 2.0 mm nut engagement, does not contact the lower leaf, and has zero intersection with the pocket's closed front skin.
4. Assert each foot face-contacts both neighboring sector owners at Z-25.50, has no positive-volume base intersection, and has at least 3.0 mm bore-edge ligament around the complete slot envelope.
5. Validate every printed part as one positive-volume watertight solid. Validate named children and exact print quantities in STEP and fresh-process 3MF imports; measure written files, not source shapes only.
   For the derivative-sector 3MF, require exactly one mesh object, one build item, and manifest quantity three. Verify its complete written rear bed-contact plane corresponds to the accepted design rear plane at `Z=-31.50`: no geometry may extend behind it and the two blind nut pockets may not open or recess that support face.
6. On actual ring and spool BREPs, require running gap `0.00 .. 0.10`, flange overlap `0.75 .. 0.85`, axial face clearance at least `0.15` on both faces of every carrier, hub-to-tooth-tip clearance at least `0.45`, and zero spool/tooth intersection.
7. Sweep each actual fin solid through 360 degrees against every stationary solid and hardware envelope. Require zero intersection and minimum distance at least `0.80` mm. A cylinder-only proxy is insufficient.
8. Require zero forbidden intersection among each spool, its two thrust washers, neighboring fixed spacers, axle, frame, and the other two rings. Verify 0.05 mm residual axial play in both inter-spool gaps and rotate each spool independently through 360 degrees in the solid model. No spool may bear directly on a shared printed spacer face.
9. With complete rings already installed, sweep the radial insertion/removal path for all nine spools, eighteen washers, and six spacers, plus the axial insertion/removal path for all three axles and collars. Require zero stationary/ring intersection at sampled and endpoint states. Separately sweep complete-ring axial installation with bridges, axles, and spool stacks absent; require clearance from foot, lower post, and backbones.
10. Assert there is no continuous rail, guide bead/head/neck, motor, gear/pinion, electronics, wiring, or battery solid or BOM line in the branch.
11. Verify every printed file in its declared orientation, with brim/support envelope, fits the U1 usable `260 x 260` mm area. Support material may not touch an axle bore, spool bore, running land, flange capture face, or station registration face.

### Physical gates (CAD cannot satisfy these)

1. Service-cycle one branch-derivative outer captive-nut pocket and one removable-bridge printed-nut coupon ten times using the specified M3 screws. The metal station nut may not rotate, pull out, crush the closed pocket skin, or mark the flat rear datum; the printed bridge-nut interface may not strip, crack, or gain more than 0.10 mm screw-axis looseness. Record the qualified torque. Pocket failure requires revising only the branch-owned derivative sector; the locked Q3 r0 source/export remains untouched.
2. With the station tightened at that qualified torque, each of the nine spools must start and coast independently by hand; rotating one spool may not visibly drive either neighbor.
3. Measure base free-state flatness after inner seam closure and after all three stations are torqued. Maximum gap is `0.50` mm and no rocking is allowed.
4. Rotate each ring alone and the full stack at least ten complete revolutions in both directions. There must be no fin strike, tooth-tip rub, axial escape, binding, screw loosening, or permanent ring mark.
5. Repeat axle/collar/spool removal and reassembly for ten cycles at one station, then repeat the rotation test. Reject bore galling, collar migration, cracked foot threads, or loss of independent spin.
6. Run a minimum one-hour continuous manual or external-fixture rotation trial. No drive hardware is part of this branch; any temporary test drive must remain outside the delivered assembly and may not mask a stationary collision.

Passing the CAD gates accepts only the geometric contract. Print fit, tapped-thread life, friction, noise, wear, ring runout, stiffness, and long-duration usability remain physical evidence requirements.
