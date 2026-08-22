# KAGE continuation and clean-restart summary

Date: 2026-08-22  
Repository: `/Users/scottchu/Projects/personal/3d-print`  
Project: `/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator`  
Branch observed while writing this document: `main`

## 0. Restart directive

The current KAGE data set is not trustworthy enough to continue incrementally.
This document is the restart boundary.

- Do not continue the Half-Z experimental CAD.
- Do not treat historical test counts as proof that a mechanism works.
- Do not select a newer-looking folder merely because its timestamp or version
  number is higher.
- Do not modify the locked reference in place.
- Do not delete old work yet. It is historical evidence, not a current design.
- Begin the next implementation from a new, explicitly named restart version.
- Every later change must state its intention, name its parent baseline, and
  regenerate its artifacts from parametric source.

No CAD was modified while preparing this summary.

## 1. Goal state

KAGE is a roughly 300 mm wall-mounted, 3D-printed kinetic shadow clock and home
decor object.

The intended functional chain is:

```text
time controller
    -> three independent motors
    -> three independent rotating ring gears
    -> hour / minute / second upright fins
    -> central point LED illuminates the fins
    -> wall receives a halo and three readable clock-hand shadows
```

The final object should remain visually intentional during daylight, not only
when the LED is on. Mechanics may be visible as part of the art, but every
visible part must have a real structural, optical, or service purpose.

### Hard product constraints

1. Three independently controlled hour, minute, and second shadow fins.
2. The center remains optically clear for the LED.
3. Positive, tunable ring drive is preferred for the MVP.
4. Motors and drive hardware stay inside the ring system; fins project toward
   the useful outer/light region.
5. The 300 mm design must be printable on the Snapmaker U1 270 x 270 x 270 mm
   build volume by intentional segmentation.
6. The base must lie flat for assembly and bench testing.
7. Mechanical parts are validated before electronics packaging and decoration.
8. PETG is the primary structural/internal material.
9. CAD acceptance and physical print acceptance are always reported separately.

## 2. Frozen reference, not a finished product

The only accepted visual/mechanical reference for restarting is:

```text
models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/
  p3_v3_direct_gear_race_assembled.step
```

Absolute path:

```text
/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/p3_v3_direct_gear_race_assembled.step
```

Verified SHA-256 on 2026-08-22:

```text
dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7
```

Review URL:

```text
https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/models?file=p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818%2Fp3_v3_direct_gear_race_assembled.step
```

### What “locked” means

Locked means the file is a frozen reference and must not be silently changed.
It does **not** mean the clock is physically proven or production-ready.

The next version may intentionally change it, but only by:

1. copying the relevant source into a new restart namespace;
2. declaring the exact intended change;
3. preserving an immutable parent hash;
4. regenerating STEP/3MF from source;
5. running meaningful checks for that change;
6. obtaining a separate review verdict;
7. keeping physical proof open until printed and assembled.

### Useful locked-reference contents

- `p3_v3_direct_gear_race_assembled.step`
- `p3_v3_direct_gear_race_service_exploded.step`
- `p3_v3_direct_gear_race_powered_min_q-0p35.step`
- `p3_v3_direct_gear_race_powered_max_q+0p10.step`
- `p3_v3_direct_gear_race_SERVICE_outward_q+2p50_RINGS_REMOVED.step.py`
- `source_snapshot/p3_v3_direct_gear_race_guidance_spec.py`
- `source_snapshot/p3_v3_direct_gear_race_guidance_geometry.py`
- `source_snapshot/p3_v3_direct_gear_race_guidance_export.py`
- three frozen test snapshots under `tests_snapshot/`
- locked review snapshots under `snapshots/`

The locked reference contains the direct gear/race concept, three ring roles,
roller guidance, and radial motor-mount adjustment. These are reference ideas;
their tiny nominal clearances must not be copied into the restart without new
PETG tolerance decisions.

## 3. Explicitly rejected or untrusted work

### Half-Z experiment

The following namespace is rejected as a continuation source:

```text
p3_v3_exp_half_z_architecture_r1*
models/p3_v3_exp_half_z_architecture_r1/
tests/test_p3_v3_exp_half_z_architecture_r1.py
```

It may remain on disk for forensic comparison, but no dimensions, manifests,
test counts, or geometry from it are accepted.

The reported `11/11` test result is invalid as a release claim because critical
physical pairs were omitted. Later actual-solid inspection found, among other
problems:

- adjacent H/M and M/S spools overlapping by about 37.107 mm^3 per tower;
- an hour spool intersecting a chassis boss by about 22.766 mm^3;
- output pinions without shaft bores, leaving about 33.301 mm^3 shaft/hub
  intersection;
- cradle/chassis intersection around 1.200 mm^3;
- a referenced keeper set screw without a matching cap tunnel;
- approximately 0.05 mm ring-to-spool race clearance;
- approximately 0.20 mm diametral spool/post clearance;
- approximately 0.15 mm axial flange clearance;
- approximately 0.35 mm ring-to-ring axial gap;
- approximately 0.20 mm gear backlash;
- no complete U1 segmentation plan for the approximately 300 mm parts.

This failure is why the restart must use actual-solid checks and physical
coupons rather than symbolic clearance assertions alone.

### Historical generated folders

The project contains many earlier P0/P1/P2/P3, ring-seam, electronics, roller,
base, and production folders. They are not current merely because they exist.
In particular:

- `p3_v3_direct_gear_race_guidance_r2/production/plate_*.3mf`
- `p3_v3_locked_stage_a_print_exports/`
- old Q4 base variants
- old ring seam clamp variants
- old electronics backbone variants
- old roller tower and retrofit variants
- old complete-mechanics releases

must be treated as historical until a restart decision explicitly adopts one.

## 4. Decisions that survive the restart

### Clock architecture

- Do not use a commodity quartz movement.
- Use three independently controlled motors, one per ring.
- The center stays free for the optical source.
- Use software to derive hour, minute, and second angles.
- Provide a homing reference because open-loop steppers do not know absolute
  position after power loss.
- Keep the MVP mechanically simple and serviceable.

### Ring and fin intent

- Three rotating ring gears carry three vertical fins.
- The fins are shadow blockers, not traditional flat clock hands.
- Fin length can remain short because projection magnifies the shadow.
- Exact fin height, thickness, and H/M/S visual differentiation are not frozen.
- Fins should have a clear path through all stationary guidance and drive
  stations for a full revolution.

### Drive intent

- Keep the positive gear-drive MVP first.
- Do not introduce TPU, belts, friction drive, or extra optical mechanisms yet.
- Each motor station needs radial mesh adjustment; the locked reference models
  a physical range of approximately +/-2.50 mm and a much smaller powered
  window.
- Motor, pinion, and station dimensions remain provisional until the real NEMA
  8 motors arrive and are measured.

### Guidance intent

- Avoid continuous rails under the rings when point guidance can retain them.
- The accepted concept direction is a small number of free-rolling guidance
  stations that capture all three rings while leaving fin travel unobstructed.
- Exact roller/spool topology and tolerances are **not frozen** by this restart.
- Do not reuse the 0.05/0.15/0.20 mm experimental clearances without a PETG
  coupon.

### Base and segmentation intent

- Keep the overall design at 300 mm for now.
- Snapmaker U1 volume is 270 x 270 x 270 mm, so segmentation is required.
- Prefer one canonical 120-degree base sector printed three times, if its
  mechanical interfaces can truly be identical.
- The back of the assembled base must remain flat.
- The base must retain functional mounting reservations for motors, guidance,
  and later sensors; segmentation must not erase those interfaces.
- Seam clamping must spread load radially rather than concentrating all screws
  near the middle.
- The last explored three-sector contract used four M3 seam holes per seam: two
  may share the roller-mount region and two are placed toward the inner radius.
  This is a **candidate to revalidate**, not an automatic source of truth.

### Fasteners and materials

- Use real metal screws and nuts for the MVP; do not print screws or dowel pins.
- User-owned screw assortment includes M3 x 6, 8, 10, and 12 mm socket-head
  screws.
- Ordinary captive/replaceable M3 nuts are preferred for the MVP.
- Heat-set inserts are a later production option.
- Exact screw length is joint-specific and must be checked from stack thickness
  and thread engagement.
- PETG is used for structural/internal parts.
- PLA, PLA+, or wood PLA may be used for later decoration, away from LED heat.

## 5. Electronics and optical decisions retained as future requirements

These parts are not to be packaged into the restart mechanics until the hard
mechanics work.

### Intended clock electronics BOM

| Item | Qty | Status |
|---|---:|---|
| StepperOnline NEMA 8, 4 N cm class | 3 | selected, physical dimensions must be measured |
| TMC2209 stepper driver | 3 + 1 spare | selected |
| Waveshare ESP32-C6 Touch LCD | 1 | selected |
| DRV5032 Hall module | 3 + spares | selected, exact PCB and sensor suffix must be verified |
| 3 x 2 or 4 x 2 mm magnets | test stock | owned candidates; final size not frozen |
| 12 V / 4 A supply | 1 | selected |
| 12 V to 5 V / 3 A USB-C buck | 2 | selected; final load split unresolved |

### Homing reservation, not implementation

- One Hall channel per ring.
- Home one ring at a time and park the other rings away from the active sensor.
- Angular separation alone does not prevent cross-triggering.
- Reserve different radial sensor/magnet lanes; a starting target near 8 mm
  lane-center separation should be bench-tested, not assumed.
- The actual DRV5032 suffix matters because unipolar/omnipolar behavior differs.
- The seller's generic `30 kHz` description is not sufficient specification.
- No homing pocket should be frozen before testing the actual module, magnet,
  polarity, and trigger air gap.

### LED optical/thermal subsystem

Current target:

- Cree XHP35.2 HI, warm white 3000 K;
- nominal 12 V class;
- 20 mm copper MCPCB;
- typical operating power around 3-5 W;
- optional limited 8-10 W daytime boost;
- do not assume continuous 13 W operation.

Required thermal path:

```text
LED
  -> 20 mm copper MCPCB
  -> thermal paste or thin pad
  -> aluminum heatsink
  -> open air gap / ventilation
  -> PETG mechanical carrier at cooler edges
```

The LED and heatsink must move as one serviceable optical cartridge. The future
cartridge should support about 30-80 mm LED-to-mask adjustment. Do not add a
diffuser. Do not assume a secondary optic in the first optical test.

## 6. Existing files and how to treat them

### Project environment

- `pyproject.toml`: present
- `uv.lock`: present
- use the project-local uv environment; do not install CAD dependencies
  globally

### Authoritative frozen reference

```text
models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/
```

Read-only use: visual comparison, intent recovery, and parent hash.

### Candidate base-sector artifacts

```text
models/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview/
  p3_v3_mvp_base_q3_identical_sector_print_qty3.3mf
  p3_v3_mvp_base_q3_r0_identical_sector_qty3.step
  p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_assembled.step
  p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_u1_diagonal_beds.step
```

These were previously reported as fitting the U1 and using an identical sector
three times. Because the data set is being restarted, they are reference
candidates only. Their exported placement, seam-hole count, and physical fit
must be rechecked before printing.

### Candidate later base revisions

`p3_v3_mvp_base_q3_r1_*` and `p3_v3_mvp_base_q3_r2_*` contain later clamp and
roller-mount explorations. They are not automatically preferred over r0.

### Working inventory

`docs/KAGE_PARTS_AND_BOM.md` is useful as an inventory, but some text describes
old four-part base and electronics work. Treat it as a parts ledger, not the
restart mechanical specification.

## 7. Test state

### What has evidence

1. The locked STEP hash listed above was verified while writing this document.
2. The locked folder contains frozen source and test snapshots.
3. Frozen locked tests include checks for:
   - radial motor adjustment geometry;
   - fixed versus slotted mount behavior;
   - ring/pinion collision matrices;
   - actual STEP/source occurrence parity;
   - roller/ring contact bands;
   - fin and seam-hardware clearance;
   - segmented ring validity.
4. The earlier identical-sector handoff reported 9 focused tests and independent
   CAD/artifact review. This remains CAD evidence only and must be refreshed in
   the restart namespace before relying on it.

### What is invalid

- Half-Z `11/11` is not accepted because the test matrix omitted real
  collisions and missing bores/service features.
- Any test that validates only named parameters, labels, or interval math is
  insufficient for a moving assembly.
- A generated STEP, a passing import, or an Orca-load check does not prove
  mechanical motion or printed fit.
- Old large aggregate test counts do not prove the restart version.

### Meaningful restart test gates

Only add tests that close a real failure mode:

1. **Parent hash guard** — proves the locked reference was not silently changed.
2. **Source/export parity** — every promised part occurs in the written STEP/3MF.
3. **Actual-solid collisions** — all moving/contact pairs, not selected pairs.
4. **Full 360-degree sweep** — each ring and fin through every stationary
   station, seam, roller, and motor envelope.
5. **Gear mesh** — center distance, backlash, axial overlap, seam phase, and
   radial adjustment at min/nominal/max.
6. **Guidance/capture** — no ring escape, no tooth contact by guide rollers, and
   printable PETG running clearances.
7. **Assembly path** — the mechanism can be assembled flat, with real tools and
   hardware, in a documented order.
8. **Service path** — motor, pinion, roller, or ring can be removed without
   destroying the base.
9. **U1 envelope** — measure written artifact footprints plus brim, not only
   source bounding boxes.
10. **Physical coupons** — PETG seam, free roller, ring mesh, and motor station
    must pass before building the full clock.

CAD results must be labeled `CAD accepted`, `CAD rejected`, or `not run`.
Physical results must be labeled separately.

## 8. Current agent/task status

At the time this document was prepared:

| Task | Status | Action |
|---|---|---|
| `/root` | active | writing this restart summary only |
| `/root/q3_seam_critic` | `pending_init` stale entry | interrupt/cancel requested; no continuation work accepted |

No important design, implementation, review, or validation agent is currently
running. No new handoff was created.

The UI displayed `128 active agents`, but that number did not match the current
collaboration tree. Two attempts to list app-wide historical tasks timed out,
and local process inspection did not show 128 CAD agents. Treat `128` as a
stale/historical UI count, not as 128 active KAGE workers.

Historical agent work should be treated as completed, cancelled, or untrusted
unless a result is explicitly listed in this restart document.

## 9. Clean restart sequence

The restart should proceed bottom-up and stop at each physical gate.

### R0 — restart manifest and reference guard

- Create a new namespace such as `kage_restart_r0`.
- Record this document and the locked STEP hash.
- Copy only the smallest required parametric concepts; do not copy generated
  assemblies wholesale.
- Define coordinate system, ring roles, material/tolerance policy, and
  printer envelope in one spec module.

Deliverable: spec and tests only; no large assembly.

### R1 — base-sector coupon and flat assembly

- Decide the final MVP segmentation: preferred candidate is one 120-degree
  sector printed quantity three.
- Confirm one sector plus brim fits the U1 in the intended orientation.
- Use four load-spread M3 holes per seam if that remains the chosen contract.
- Preserve a flat back and practical nut/tool access.
- Print one seam coupon before the full three-sector base.

Deliverable: one canonical sector, seam coupon, and assembly card.

### R2 — one guidance station and one ring coupon

- Design one free-rolling guide station around measured PETG tolerances.
- Test one ring/race coupon, not all three rings.
- Verify free rotation, capture, fin passage, and disassembly.

Deliverable: one small print kit.

### R3 — one motor and gear-mesh station

- Wait for and measure the actual NEMA 8 motor.
- Design one motor station with radial adjustment.
- Test pinion/ring mesh at low speed.
- Do not model all three stations until this one works physically.

Deliverable: one motor station, mesh coupon, and measured results.

### R4 — three mechanical rings

- Apply proven tolerances and interfaces to H/M/S rings.
- Run full-sweep collision tests.
- Print/assemble only after R1-R3 pass.

Deliverable: hard-mechanics MVP without electronics packaging.

### R5 — homing experiment

- Bench one DRV5032 module and both magnet candidates.
- Determine real trigger gap, polarity, hysteresis, and cross-trigger spacing.
- Add sensor/magnet reservations only from measurements.

### R6 — LED cartridge

- Bench LED, MCPCB, driver, and heatsink outside printed plastic.
- Validate thermal behavior at 3 W and 5 W before limited boost testing.
- Then create the removable 30-80 mm optical cartridge.

### R7 — electronics packaging and aesthetics

- Add controller, drivers, buck converters, wiring, covers, and decorative
  parts only after the mechanics and optics have physical evidence.

## 10. Immediate next work after this summary

Do not resume from Half-Z. The next task should be only:

1. create the restart namespace and locked-parent hash guard;
2. recover the minimum 300 mm / 120-degree base-sector geometry;
3. define four properly spread M3 seam holes and flat-back assembly access;
4. produce a small seam coupon before another full 3MF;
5. run actual-solid and U1 footprint checks;
6. request physical observations before adding rollers, gears, or electronics.

No additional agent should be started until the restart scope is explicitly
approved. If staged agents are used later, the intended order remains design,
implementation, critic, review, and validation by separate roles, but only one
bounded stage at a time and always against the explicit restart namespace.

## 11. Known unknowns to resolve with real hardware or prints

- actual NEMA 8 dimensions, shaft, mounting screws, and connector clearance;
- actual pinion choice and gear module;
- PETG guide clearance and long-term ring sag;
- seam strength and flatness of the 300 mm segmented base;
- actual DRV5032 PCB/sensor position and suffix;
- 3 x 2 versus 4 x 2 mm homing magnet behavior;
- fin height/thickness required for readable H/M/S shadows;
- bare LED angular distribution and useful halo size;
- selected heatsink thermal performance;
- one-supply versus split-supply power architecture;
- acceptable acoustic noise at clock speeds.

These unknowns are physical test items, not gaps to hide with more CAD detail.
