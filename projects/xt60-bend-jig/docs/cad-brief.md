# P0 three-rod XT60 bend jig — CAD brief

## Goal and scope

- Model a STEP-first, parametric P0 fixture for holding two short 12/14 AWG power leads at a repeatable 90-degree bend while they are soldered and cooled.
- Keep the CAD reproducible through the project's `uv` environment. Python/build123d source is authoritative; STEP and 3MF files are generated outputs.
- P0 is a physical architecture experiment. One M4 dial acts at the left side, while the continuous forming rod spans the fixture and is the only member that carries that motion to the right-side moving carrier. CAD can constrain both carrier paths, but it cannot prove that this one-sided force path will resist racking; the physical test plan decides whether that architecture survives.
- The downloaded AMASS XT60 model is a **PCB-vertical connector envelope only**. It is a keep-out/reference body, not a dimensional claim for the wire-side XT60 pigtail connector that the jig will actually hold.

All dimensions are millimetres.

## Coordinate convention

- The model datum is `(X, Y, Z) = (0, 0, 0)`. `X = 0` is the midspan plane between the two side frames; `Y = 0` is the first lower-reaction setting plane; `Z = 0` is the common height datum beneath the wire path. The origin is a construction datum, not the pad exit.
- `+X`: along the three rod axes, from the left side plate toward the right side plate.
- `+Y`: along the horizontal lead, away from the board and toward the bend/connector.
- `+Z`: upward from the work surface.
- The modeled pad exit is at `Y = -6`, `Z = 10`. The nominal horizontal wire centerline remains at `Z = 10`; its straight-to-arc transition is at `Y = 16`.
- The 90-degree centerline arc has `R = 6`; it ends on a vertical centerline at `Y = 22` (`16 + 6`).
- Open/closed motion of the forming rod follows one straight 45-degree side-view path in the YZ plane. The open stroke is 11.
- The available lead length is a conserved centerline-arclength parameter. Its P0 default is 44, measured from the pad exit at `Y = -6` to the retained lead end.

## Frozen dimensions and assumptions

| Item | P0 value | Status |
| --- | ---: | --- |
| Stainless reaction/forming rods | 3 × diameter 4 × 50 long | User-supplied hardware |
| Clear working span between inner side-plate faces | 38 | Assumes the real board/workpiece is no more than 36 wide, leaving at least 0.5 clearance per side |
| Side-plate thickness | 4 each | Printed |
| Overall frame width across plate outer faces | 46 | `38 + 2 × 4`; rods protrude nominally 2 per side |
| Nominal horizontal wire height | `Z = 10` | Assembly datum |
| Bend start | `Y = 16` | Wire centerline datum |
| Bend radius | 6 | Centerline radius |
| Vertical lead centerline | `Y = 22` | `16 + 6` |
| Moving-rod slot | 11 travel at 45 degrees in YZ | Straight and parallel at both rod ends |
| Reaction-rod settings | 3 upper × 3 lower | Mirrored upper vertical and lower horizontal indexed tracks; three datums per track at 6.5 pitch |
| Upper reaction-rod center heights | `Z = 22`, `28.5`, `35` | Indexed settings 0, 1, and 2 |
| Conserved available lead length | 44 default | Centerline arclength from `pad_exit_y = -6`; parameter, not a stretched route |
| Minimum lead to upper settings | 37.425, 43.925, 50.425 | For `R = 6`, `bend_start_y = 16`, and upper settings 0, 1, 2 respectively |
| Reaction-rod retention | 4 compact external carriers, 2 thick | Each has a diameter-9 rod boss, diameter-7 lock boss, 5-wide connecting web, diameter-4.3 rod bore, and diameter-3.4 M3 clearance; no insert is installed in a carrier |
| Reaction-carrier locks | 4 reusable M3 screws + 12 frame inserts | Six frame datums per side: 3 upper + 3 lower; the four screws move with the carriers to the selected positions |
| Frame reaction-lock seats | 12 × diameter 4.6 × 3.5 | Heat-set insert seats in the frames, each with a diameter-3.4 continuation; 7 lock offset, nominal ligament 2.55, actual-solid wall at least 2.4 |
| Experimental drive | One M4 × 40 screw/dial, left side only | Drives both moving carriers through the single spanning forming rod; synchronization remains unaccepted |
| Captured nut envelope | 7.2 across flats | Clearance allowance for an M4 hex nut |
| Moving sliders | 2 compact diameter-10 collars | Replace the collision-prone large plate while retaining the symmetric axial rod-end bosses |
| XT60 reference | Body 15.9 × 8.1 × 20.5 + 5 solder cups | Overall axial extent 25.5; exact label `reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups` |
| XT60 collar height selection | 3 positions per side, 4 pitch | Use one matched left/right pair at a time: 2 installed M3 mounting screws, not 6 |
| Forming-rod retention | 2 symmetric axial M3 end retainers | Outward bosses span `X = -32..-25` and `X = 25..32`; each has an 8.6 outer diameter, 4.6 diameter × 5.2 heat-set insert seat, and 3.4 continuation bore |
| Rod-bore fit coupon | 4.2, 4.3, 4.4, and 4.5 bores | Print before committing the full kit |

Meaningful assumptions that must be checked physically:

- The real board, solder joints, insulation, and nearby components fit within the 36-wide workpiece assumption.
- A 38 clear span gives at least 0.5 lateral frame clearance at both sides of a 36-wide board.
- The selected fit-coupon bore produces a sliding rod fit without perceptible rock after printing in the intended material/orientation.
- M4 × 40 provides adequate engagement through the printed drive features and captured 7.2-AF nut; washers, head style, and final knob geometry remain implementation choices.
- Twelve diameter-4.6 × 3.5 heat-set inserts fit the modeled side-frame seats: three upper and three lower per frame. Four M3 lock screws are reused at the four currently selected carrier positions. The carriers themselves have only diameter-3.4 clearances and no insert pockets.
- The 7 lock offset provides a nominal 2.55 ligament between the diameter-4.3 reaction-rod bore and diameter-4.6 insert seat. Actual-solid validation must retain at least 2.4 of continuous material at every upper/lower datum for both supported gauges.
- Two selected M3 collar fasteners pass through one matching height hole on each frame/collar cheek. Three holes exist per side, but only one left/right pair is populated for a chosen height. Their length, washers, and nut style must be selected against the print because the collar mount has no modeled nut trap.
- Each moving slider has an outward axial retainer boss. A heat-set insert seats in the 4.6-diameter × 5.2 pocket and an M3 screw passes through the 3.4 continuation to bear on that end of the forming rod. The 8.6 boss leaves a 2.0 radial wall around the insert seat, and the rod seats 2.2 into each slider. Verify the actual inserts and screw engagement without axially preloading or bowing the rod.
- The default 44 lead can reach upper settings 0 and 1 only. Upper setting 2 requires a specimen with at least 50.425 available centerline length; CAD must mark configurations beyond the selected lead length unusable rather than stretching the wire path.
- The source reference models the 15.9 × 8.1 × 20.5 insulating body plus two simplified 5-long solder cups, for 25.5 overall axial extent. The 0.4-per-side collar allowance is exploratory; confirm the real wire-side connector and cup geometry before relying on it for fit.
- Printed material, layer orientation, and heat exposure are not certified by CAD.

## Parts and assembly intent

Printed P0 parts:

- Left and right side frames/plates, each 4 thick, carrying mirrored upper vertical and lower horizontal reaction-rod tracks plus parallel 45-degree forming-rod guides.
- Four compact 2-thick reaction-rod carriers: upper-left, upper-right, lower-left, and lower-right. Each consists of a diameter-9 rod boss and diameter-7 lock boss joined by a 5-wide web. A diameter-4.3 rod bore and diameter-3.4 M3 clearance are the only carrier holes; heat-set inserts belong in the frames, not the carriers.
- Each side frame carries six diameter-4.6 × 3.5 heat-set insert seats—three upper and three lower—with diameter-3.4 continuations at a 7 offset from the reaction track. Install all twelve inserts, then reuse four M3 screws at the four selected carrier datums.
- Moving-rod guide/drive features required to carry both ends of the forming rod through the same 11 stroke. Each slider is a compact diameter-10 collar and includes a symmetric outward-X axial retainer boss: left `X = -32..-25`, right `X = 25..32`, diameter 8.6, with a 4.6 diameter × 5.2 heat-set insert seat and 3.4 continuation bore. An M3 screw at each end bears on the rod end; the boss has 2.0 radial wall and the rod has 2.2 seating in each slider.
- One-sided M4 drive features, including a 7.2-AF nut trap and hand-operated dial/knob interface as represented by the source. The dial acts on the left moving carrier; the continuously spanned and axially retained forming rod connects and drives the right moving carrier.
- One removable upper XT60 collar. It has three height holes at each end on 4 pitch; install one M3 fastener per side through the selected matching pair. The collar remains installed in both modeled mechanism states.
- Fit coupon containing labeled 4.2, 4.3, 4.4, and 4.5 rod bores.

Reference/non-printed items:

- Three 304 stainless rods, diameter 4 × 50.
- One M4 × 40 screw and compatible M4 nut for the experimental drive.
- Four M3 reaction-carrier lock screws, reused at the four selected upper/lower positions.
- Twelve diameter-4.6 × 3.5-compatible heat-set inserts for the side-frame reaction-lock seats, six per frame. There are no carrier inserts.
- Two M3 XT60-collar mounting screws with compatible nuts/washers, installed at one selected matching height pair.
- Two M3 forming-rod axial-retainer screws and two matching 4.6-diameter heat-set inserts, one set at each moving slider. Select screw length to engage the insert and bear on the rod end without excessive axial preload.
- Board/workpiece envelope, wire centerlines, cold soldering-iron access envelope, and XT60 keep-out reference.

The left/right moving guides must be geometrically parallel and share the same closed and open rod-axis endpoints. The reaction tracks and their 6.5-spaced index datums must be mirrored across the assembly center plane. CAD equality does not prove that the physical one-sided screw and spanning rod will avoid racking, nor that the M3 locks will prevent carrier slip, so neither synchronization nor lock capacity is accepted until physical testing passes.

Assembly-state meaning:

- **Closed** is the loaded soldering state. It includes the fixture/hardware plus bottom ESC, upper flight controller, two formed wires, the labeled XT60 body-and-5-mm-cup reference, and cold-iron keep-out references.
- **Open** is mechanism-open and workpiece-unloaded. It omits the ESC, flight controller, wire, XT60, and iron references, but retains the frames, reaction carriers/rods, forming rod/sliders, M4 drive references, and upper XT60 collar.

## Source and outputs

Build entry points:

- `cad/p0_three_rod_clamp/p0_closed_assembly.step.py`
- `cad/p0_three_rod_clamp/p0_open_assembly.step.py`
- `cad/p0_three_rod_clamp/p0_print_kit.step.py`
- `cad/p0_three_rod_clamp/p0_fit_coupon.step.py`

Expected generated primary outputs:

- `cad/p0_three_rod_clamp/p0_closed_assembly.step`
- `cad/p0_three_rod_clamp/p0_open_assembly.step`
- `cad/p0_three_rod_clamp/p0_print_kit.step`
- `cad/p0_three_rod_clamp/p0_fit_coupon.step`

The print kit and fit coupon may also be exported as 3MF from the same source geometry. STEP remains primary. Generated STEP/3MF files must not be edited by hand.

Reproducible commands from the project root:

```bash
uv sync --frozen
uv run --frozen pytest -q

CAD_SCRIPTS=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.15/skills/cad/scripts
uv run --frozen python "$CAD_SCRIPTS/gen" --write \
  cad/p0_three_rod_clamp/p0_closed_assembly.step.py \
  cad/p0_three_rod_clamp/p0_open_assembly.step.py \
  cad/p0_three_rod_clamp/p0_print_kit.step.py \
  cad/p0_three_rod_clamp/p0_fit_coupon.step.py
uv run --frozen python "$CAD_SCRIPTS/export" \
  cad/p0_three_rod_clamp/p0_print_kit.step.py --3mf
uv run --frozen python "$CAD_SCRIPTS/export" \
  cad/p0_three_rod_clamp/p0_fit_coupon.step.py --3mf
```

The absolute `CAD_SCRIPTS` value names the currently installed CAD plugin. If that version moves, point the variable to the installed plugin's `skills/cad/scripts` directory while keeping every invocation inside `uv run --frozen`.

## CAD validation contract

Before CAD handoff:

- Run entry generation through the locked `uv` environment and confirm repeatability in a fresh process.
- Validate all returned bodies as closed, positive-volume BREP solids and confirm source-to-export parity.
- Confirm named/labeled occurrences for printed parts and reference hardware/envelopes.
- Confirm the print kit includes exactly four separately labeled reaction-rod carriers in addition to the two side frames and moving-drive parts.
- Measure the 38 clear span, 4 plate thicknesses, 46 outer frame width, and 50 rod length. Confirm nominal 2 rod protrusion at each side.
- Confirm the nominal wire datums: `Z = 10`, bend start `Y = 16`, centerline radius 6, and vertical leg at `Y = 22`.
- Confirm an 11 straight 45-degree forming-rod stroke, with coincident left/right rod-axis endpoints in both open and closed assemblies.
- Confirm mirrored upper vertical and lower horizontal tracks, with three discrete datums per track at exactly 6.5 pitch. Verify the external carriers engage every datum and retain the 4-diameter rod axes without carrier/frame or rod/frame interference.
- Validate all four compact carrier bodies as separate 2-thick positive-volume BREP occurrences. Measure diameter-9 rod bosses, diameter-7 lock bosses, 5-wide webs, diameter-4.3 rod bores, and diameter-3.4 M3 clearances; confirm a diameter-4.6 insert gauge collides because carriers contain no insert seats.
- Confirm each frame has exactly six outer-accessible diameter-4.6 × 3.5 heat-set insert seats at the three upper and three lower lock datums, each continuing through diameter 3.4. Confirm the 7 lock offset, nominal 2.55 ligament, and at least 2.4 actual-solid wall at every seat for both 12 and 14 AWG geometry.
- Confirm the 7.2-AF nut trap and M4 × 40 drive envelope, while labeling the one-sided drive experimental. Confirm one continuous 50-long forming rod engages both moving carriers throughout the 11 stroke.
- Confirm two symmetric axial forming-rod retainers: outward boss ranges `X = -32..-25` and `X = 25..32`; 8.6 boss diameter; 4.6 diameter × 5.2 insert seats; 3.4 continuation bores; 2.0 radial wall; and 2.2 rod seating at each slider. Confirm both M3 screws can bear on the rod ends without collision, loss of guide travel, or modeled rod preload.
- Confirm `available_lead_length = 44` is a named conserved parameter. From `pad_exit_y = -6`, `bend_start_y = 16`, and `R = 6`, verify minimum lead lengths of approximately 37.425, 43.925, and 50.425 for upper settings at `Z = 22`, `28.5`, and `35`. Mark upper setting 2 unusable at the default rather than altering arclength.
- Validate all 36 static assembly cases with a lead long enough to reach every setting: 2 wire gauges × 3 upper indices × 3 lower indices × 2 states (open and closed). Every assembly must be valid, positive-volume, correctly labeled, and free of unintended positive-volume overlap.
- Sweep the moving sliders through 101 evenly spaced closure positions from 0.00 through 1.00 for both wire gauges and every extreme reaction pair (`upper = 0/2`, `lower = 0/2`). At every point, verify both compact sliders clear all four carriers with no unintended positive-volume overlap.
- Confirm at least 0.5 frame clearance per side around a centered 36-wide board envelope.
- Confirm the cold-iron access envelope is not intersected by the frame or drive in the soldering state.
- Confirm the XT60 reference contains the exact 15.9 × 8.1 × 20.5 body above 5-long solder cups, spans 25.5 overall axially, and carries the exact label `reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups`. Keep the downloaded PCB-vertical vendor part identified separately as an envelope source, not the wire-side pigtail.
- Confirm the fit coupon contains distinct 4.2, 4.3, 4.4, and 4.5 bores.
- Inspect open and closed STEP assemblies visually from side, end, and isometric views. Check part separation and print-kit orientation before 3MF export.

CAD passing is necessary but not sufficient. Skew, rod flex, frame spread, soldering access, fit, and thermal behavior remain governed by `docs/p0-physical-test-plan.md`.
