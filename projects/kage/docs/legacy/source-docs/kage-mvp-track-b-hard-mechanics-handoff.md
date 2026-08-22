# KAGE MVP track B — hard-mechanics handoff

Status: design-only, implementation not started.  B1 must pass physical review
before B2 CAD is released; B2 must pass before motors, electronics, LEDs,
Hall sensing, optics, or the cosmetic enclosure are added.

## Decision

Yes: validate the four-segment assembly and the passive mechanics first.

- **B1:** four base quadrants assembled into one rigid support, one four-quadrant
  ring, all four moving seams, one hand-driven pinion, and three minimal flanged
  free-roller retainers.
- **B2:** reuse the accepted B1 base/joinery and add three stacked four-quadrant
  rings, nine independent rollers, three hand-driven pinions, and short H/M/S
  clearance fins.
- A small coupon may select a bore or backlash value, but it cannot pass B1 or
  B2.  Each gate requires the complete promised assembly.

The aim is to answer the expensive questions now: can four printed quarters
become a round, guided ring; can gear teeth and rollers cross every seam without
a bump or escape; and can three rings rotate independently with usable axial
clearance?  Nothing powered is required to answer those questions.

## Inspected baseline and known contradictions

Checkout: `/Users/scottchu/Projects/personal/3d-print`  
Git HEAD: `2f5fac86a8f3f8cc23fbc5ca8ae9a37d531d607a`  
Branch: `kage/magnetic-three-channel-mvp`

| Baseline input | SHA-256 |
|---|---|
| `src/adr-direct-gear-race-guidance.js` | `a249d378b43064395d1bda287deab58b9876b0bc756edabcace3e2d60a60a863` |
| `p3_v3_direct_gear_race_guidance_r2_spec.py` | `0007955b05d68aa4b2b53926928dd142b0cd6c3412fc3a294703e7ab5d71679a` |
| `p3_v3_direct_gear_race_guidance_r2_geometry.py` | `4cac88b03c6872f032c9c7022b4192745b385b82da91b9cad323772482d5a13d` |
| `docs/p3-v3-direct-gear-race-guidance-r2-frozen-handoff.md` | `03cf057036166c9497cf37025616cdeb7bd2e582b1c5f7c464eec23ea80078cc` |
| `models/p3_v3_direct_gear_race_guidance_r2/manifest.json` | `5c62a2fc0779edfcaa0e74d95762cfdcfbe483b62fde0c4516727570d6c87f48` |

These R2 inputs are currently untracked in Git, so the hashes above, not HEAD
alone, identify the inspected geometry.

Do not inherit these claims silently:

1. The source calls the 260T carrier “full involute,” but both ring and 16T
   pinion are repeated `Box` teeth.  The ring tooth is about 3.70 radial by
   1.05 tangential; the pinion uses root R6.75, tip R9.00 and 1.40 tangential
   boxes.  The frozen 20-degree involute/contact-ratio equations therefore do
   not validate the current BREP.
2. The ADR/frozen target says roller running OD12.10 and flange OD13.80/14.30,
   while current R2 contact witnesses and cassette solids use smaller D9-class
   rollers and even a separate analytical radius.  One actual roller profile
   must own CAD, tests and printed parts.
3. Current source carrier layers/body and tooth-face ranges do not exactly
   match the older 4.40-thick frozen narrative.  B2 must derive all Z planes
   from one new parameter table.
4. Existing CAD/artifact checks do not establish printed seam bump, drag,
   runout, roller retention, backlash, or independent motion.  The manifest
   correctly leaves printed fit, torque, noise and wear pending.

## Tooth-profile freeze before B1

Choose exactly one profile and name it with `tooth_profile_kind`:

- `internal_involute_20deg_m1` (**recommended**): generate a true 20-degree,
  module-1, 260T internal ring and matching 16T pinion; keep pitch radii
  130.00/8.00 and nominal centre distance 122.00.
- `indexed_box_r2` (diagnostic only): preserve the current box teeth exactly
  and delete all involute/contact-ratio claims from its acceptance report.

Do not print a full B1 with one profile and infer results for the other.  The
seam must fall in a repeated root-space datum so each quadrant owns exactly 65
complete pitches; no truncated tooth may be repaired by a splice plate.

## Shared named parameters

All dimensions are millimetres.  Initial values are prototype targets, not
printer compensation; fit-ladder results may update only the corresponding
`*_printed` parameter.

| Parameter | Initial value / rule |
|---|---:|
| `bed_xy_limit` | 270.00 |
| `bed_keepout_margin` | 5.00 per side |
| `base_segment_count` | 4 |
| `ring_segment_count` | 4 per ring |
| `segment_angle_deg` | 90.00 |
| `ring_teeth` / `pinion_teeth` | 260 / 16 |
| `gear_module` / `pressure_angle_deg` | 1.00 / 20.00 when involute |
| `ring_pitch_radius` / `pinion_pitch_radius` | 130.00 / 8.00 |
| `pinion_nominal_center_radius` | 122.00 |
| `carrier_race_radius` | 131.60 |
| `ring_body_outer_radius` | 138.90 |
| `base_outer_radius` | 150.00 maximum |
| `seam_phase_deg` | half a 260T pitch from tooth centre |
| `seam_registration_pin_diameter` | D2.90 pin / D3.00 bore baseline |
| `seam_plate_thickness` / `seam_recess_depth` | 2.00 / 2.10 |
| `seam_fastener` | 2 × M2 per seam into replaceable nuts |
| `roller_tower_angles_deg` | 60, 180, 300 |
| `roller_running_od` | 12.10, single source of truth |
| `roller_flange_od` | 14.30, single source of truth |
| `roller_running_band_height` | 2.00 minimum |
| `roller_flange_thickness` | 0.50 |
| `roller_bore` / `roller_axle` | D4.06 / D3.99 target |
| `roller_axial_endplay` | 0.10–0.20 |
| `roller_axis_nominal_radius` | 125.55 |
| `fixed_roller_adjust_range` | ±0.50 setup, then lock |
| `third_roller_adjust_range` | ±1.00 screw/slot setup |
| `manual_pinion_adjust_range` | -1.00…+0.50 from nominal |
| `manual_pinion_lock_repeatability` | 0.10 maximum |

Printed PETG rollers are acceptable for B1/B2 geometry discovery, with three
spares.  They cannot establish final friction, wear or noise; the same roller
profile should later be made in POM without changing the mating race.

## B1 — one complete manually driven ring

### Assembly

1. Four 90-degree rear base quadrants form one R150 support.  Each joint uses
   positive keys plus replaceable screws/nuts; glue and printed threads do not
   count.  Roller and pinion datums must bridge the assembled base, not a loose
   tabletop jig.
2. Four 90-degree carrier quadrants form one 360-degree R138.90 ring.  Every
   seam uses the production recess, splice plate, registration pin and two
   fasteners.  The splice remains outside the R131.60 running race.
3. Three freely rotating flanged rollers contact only the smooth inner race.
   Two towers lock after radial setup; the third remains accessible for preload
   adjustment.  Roller flanges replace continuous keeper rails and provide
   positive axial capture on both sides.
4. One 16T pinion is mounted directly on a hand shaft with a removable crank or
   knob.  Its whole cartridge slides radially and locks; no motor, bevel pair,
   belt, spring cassette, Hall part or front cosmetic ring is present.

### B1 CAD gates

- Each base and ring quadrant has an oriented XY bound within
  `bed_xy_limit - 2*bed_keepout_margin = 260.00`; no rotated packing assumption
  may hide an oversized object.
- Reassembled base joint step and ring race/tooth seam step are measured from
  actual faces.  Nominal CAD target: ≤0.10 radial and axial at every joint.
- All four seam plates, pins, holes, nut captures and tool paths are real solids;
  the plate/race positive intersection is zero.
- Sweep one complete assembled ring 360 degrees against all three actual roller
  solids and the actual pinion.  Sample uniform poses plus exact alignment of
  each seam with each roller and with the pinion.  Only intended tooth and race
  contact pairs are waived from generic intersection.
- At nominal setting, actual gear BREPs have continuous engagement, no
  unintended positive-volume overlap, and measurable backlash.  If involute,
  compute contact ratio from the generated flank geometry; if box-profile,
  report only measured phase coverage and backlash.
- Roller flange overlap remains positive at every seam and the ring cannot be
  removed axially without removing at least one retainer.
- Deliberate CAD negatives must fail: add 0.30 seam radial step; set pinion
  `q=+0.25`; set pinion `q=-1.00`; move one roller outward 0.80; remove one
  flange.  A test that passes its negative does not count.

### B1 physical gate

- Assemble/disassemble the four-piece base and ring three times without damage;
  record joint gap/step and pinion setting each time.
- Measure ring radial and axial TIR at 12 angular positions; record, do not
  replace, the existing provisional limits of 1.50 radial and 1.20 axial.
- Hand-drive 20 full revolutions each direction.  Mark all four seams and log
  crank force immediately before/on/after every pinion-seam and roller-seam
  crossing.  Pass means no bind, tooth climb/skip, flange escape or retainer
  motion; seam peak force must be ≤1.25 × the non-seam median.
- Reverse at eight ring angles including every seam; backlash at the ring rim
  is ≤0.50 degree and the locked pinion setting moves ≤0.10.
- Deliberate physical negatives: insert a removable 0.20 seam shim and verify
  the force/step gate detects it; set pinion visibly shallow then deep and verify
  backlash then bind is observable; loosen the adjustable roller by 0.50 and
  verify capture/runout degrades.  Restore nominal before acceptance.

Passing B1 proves the four-to-one structure, seam crossing, direct tooth drive,
radial adjustment and rail-free roller capture.  It does not prove balance,
final material wear, silence, motor torque or optics.

## B2 — three stacked manually driven rings

B2 changes only the number of lanes and the axial interfaces.  Reuse B1 base
joinery, tooth profile, race, seam and radial tower geometry without redesign.

### Additional named parameters

| Parameter | Initial value / rule |
|---|---:|
| `role_keys` | H, M, S |
| `role_plane_pitch` | 6.70 |
| `carrier_body_z` | derive from one table; current-source starting points -2.75…-0.10, 3.95…6.60, 10.65…13.30 |
| `pinion_face_z` | -0.70…1.40, 4.85…6.95, 10.40…12.50 |
| `minimum_moving_axial_clearance` | 0.80 under tolerance stack |
| `fin_test_radial_bands` | H 142.50…143.70; M 139.30…140.50; S 136.10…137.30 |
| `fin_test_tangential_width` | 3.00 common, matching current source |
| `fin_test_height` | H/M/S = 8.0/10.0/12.0, deliberately short and removable |
| `initial_ring_phase_deg` | H/M/S = 0/30/60 for inspection only |

Each tower carries three independently rotating flanged rollers; no common
roller may rub two rings.  Fixed towers may share a metal axle only if spacers,
washers and collars positively locate each roller.  The adjustable tower may
use three simple role-local screws/slots; springs and the current complex
cassette/stop-plate system are deferred unless B2 shows runout demands them.

Use three manual 16T pinion cartridges at the existing 0/120/240-degree
stations, one per role.  This validates simultaneous packaging and lets each
ring be driven while the other two are observed.  Do not install dummy motors
or bevel gears.

### B2 CAD gates

- Repeat B1 actual-solid seam/mesh/roller gates for all 12 seams, nine rollers
  and three pinions.
- Sweep each complete ring 360 degrees while the other two are checked at
  phases 0, half tooth pitch and one tooth pitch.  Require zero unintended
  ring/ring, fin/fin, pinion/non-host-ring and retainer/ring intersection.
- Measure every actual axial gap at nominal and with adjacent rings shifted by
  the agreed prototype warp/float envelope; minimum moving clearance is 0.80.
- Verify every roller running band contacts only its assigned race, both flanges
  retain that ring, and adjacent roller/spacer stacks have positive clearance.
- Deliberate CAD negatives must fail: remove one 0.50 spacer; shift M axially
  0.80 toward H; shift a fin radial band 2.00 toward its neighbour; apply the
  B1 bad-seam and bad-pinion settings to each role.

### B2 physical gate

- Repeat the B1 assembly/repeatability, TIR, backlash and seam-force log for all
  three rings.
- Drive each ring 20 revolutions each way.  Neither idle ring may move more than
  0.5 degree during one driven revolution; no fin touch, tooth skip, flange
  escape, spacer migration or tower motion is allowed.
- At the 12 seam alignments and at fin-to-fin closest approach, verify the
  0.80 feeler/gauge clearance where accessible and record the minimum.
- Deliberate negatives: temporarily omit the designated removable 0.50 spacer
  and confirm axial clearance fails; add a 0.50 radial shim at one tower and
  confirm drag/runout worsens.  Restore parts and re-run one clean revolution.

Passing B2 authorizes a separate powered-drive design phase.  It still does not
authorize claims about motor margin, 24-hour timing, electronics, light/shadow
quality, heat, final noise or wear.

## Exact implementation artifact list

No artifact below exists yet.  Source is authoritative; STEP is primary and
3MF is derived.

### B1

- `p3_b1_single_ring_manual_spec.py`
- `p3_b1_single_ring_manual_geometry.py`
- `models/p3_b1_single_ring_manual/p3_b1_assembled.step`
- `models/p3_b1_single_ring_manual/p3_b1_service_exploded.step`
- `models/p3_b1_single_ring_manual/print/plate_01_base_q1.3mf`
- `models/p3_b1_single_ring_manual/print/plate_02_base_q2.3mf`
- `models/p3_b1_single_ring_manual/print/plate_03_base_q3.3mf`
- `models/p3_b1_single_ring_manual/print/plate_04_base_q4.3mf`
- `models/p3_b1_single_ring_manual/print/plate_05_ring_q1.3mf`
- `models/p3_b1_single_ring_manual/print/plate_06_ring_q2.3mf`
- `models/p3_b1_single_ring_manual/print/plate_07_ring_q3.3mf`
- `models/p3_b1_single_ring_manual/print/plate_08_ring_q4.3mf`
- `models/p3_b1_single_ring_manual/print/plate_09_joinery_drive_rollers.3mf`
- `models/p3_b1_single_ring_manual/manifest.json`
- `tests/test_p3_b1_single_ring_manual.py`
- `docs/kage-mvp-b1-physical-results.md`

### B2, only after B1 physical acceptance

- `p3_b2_three_ring_manual_spec.py`
- `p3_b2_three_ring_manual_geometry.py`
- `models/p3_b2_three_ring_manual/p3_b2_assembled.step`
- `models/p3_b2_three_ring_manual/p3_b2_service_exploded.step`
- `models/p3_b2_three_ring_manual/print/plate_01_base_q1.3mf`
- `models/p3_b2_three_ring_manual/print/plate_02_base_q2.3mf`
- `models/p3_b2_three_ring_manual/print/plate_03_base_q3.3mf`
- `models/p3_b2_three_ring_manual/print/plate_04_base_q4.3mf`
- `models/p3_b2_three_ring_manual/print/plate_05_ring_h_q1.3mf`
- `models/p3_b2_three_ring_manual/print/plate_06_ring_h_q2.3mf`
- `models/p3_b2_three_ring_manual/print/plate_07_ring_h_q3.3mf`
- `models/p3_b2_three_ring_manual/print/plate_08_ring_h_q4.3mf`
- `models/p3_b2_three_ring_manual/print/plate_09_ring_m_q1.3mf`
- `models/p3_b2_three_ring_manual/print/plate_10_ring_m_q2.3mf`
- `models/p3_b2_three_ring_manual/print/plate_11_ring_m_q3.3mf`
- `models/p3_b2_three_ring_manual/print/plate_12_ring_m_q4.3mf`
- `models/p3_b2_three_ring_manual/print/plate_13_ring_s_q1.3mf`
- `models/p3_b2_three_ring_manual/print/plate_14_ring_s_q2.3mf`
- `models/p3_b2_three_ring_manual/print/plate_15_ring_s_q3.3mf`
- `models/p3_b2_three_ring_manual/print/plate_16_ring_s_q4.3mf`
- `models/p3_b2_three_ring_manual/print/plate_17_joinery_drives_rollers_fins.3mf`
- `models/p3_b2_three_ring_manual/manifest.json`
- `tests/test_p3_b2_three_ring_manual.py`
- `docs/kage-mvp-b2-physical-results.md`

Implementation must regenerate the derived files from source, snapshot both
assembled STEP files, and independently review CAD gates.  Physical result
documents must include photos, measured values and failed negatives; a CAD
green suite cannot fill those fields.
