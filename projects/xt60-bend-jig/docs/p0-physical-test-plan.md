# P0 three-rod XT60 bend jig — physical test plan

## Decision being tested

Determine whether the printed two-frame, three-rod fixture can form and hold short power leads at 90 degrees without unacceptable racking, rod flex, frame spread, access loss, or thermal damage.

The one-sided M4 × 40 drive is explicitly an experiment. One dial drives the left moving carrier, and the single continuous forming rod spans the fixture to carry that motion to the right moving carrier. CAD-constrained endpoints do not establish physical synchronization. If the moving rod exceeds the skew limits below, the one-sided-drive architecture is a **NO-GO**; do not tune around the failure with looser acceptance limits.

The two reaction rods are not permanently fixed. Their ends sit in four external clamp-cap/carriers: mirrored upper carriers move on vertical tracks and mirrored lower carriers move on horizontal tracks. Each track has three index datums at 6.5 spacing. These rods are set manually at matching left/right indices and locked with M3 hardware before the M4 dial is operated.

The modeled **closed** state is loaded for soldering. The modeled **open** state is mechanism-open and workpiece-unloaded, so its ESC, flight-controller, wire, XT60, and iron references are deliberately absent; the fixed upper XT60 collar remains installed. Do not interpret that simplified open assembly as the actual loading sequence until the workflow gate below has been performed with real parts.

The vendor XT60 STEP is a PCB-vertical connector envelope only. Use the actual wire-side connector during fit and process trials.

CAD preflight is required before printing. The frozen test suite must pass all 36 static assembly cases—12/14 AWG × three upper indices × three lower indices × open/closed—and the 101-position motion sweep for both gauges at all four extreme reaction pairs. These checks establish modeled BREP clearance only; the physical matrix below remains mandatory.

## Equipment and samples

- P0 fit coupon and full print kit, printed PETG-first with the intended orientation, layer height, and wall/infill settings. Record the exact filament and profile; PETG is an experiment near soldering heat, not an approval.
- Three straight 304 stainless rods, diameter 4 × 50.
- M4 × 40 screw, M4 nut, intended washers/knob, and normal assembly tools.
- Four M3 reaction-carrier lock screws, reused at the four selected carrier positions, plus twelve matching heat-set inserts for the side-frame datum seats (six per frame). No insert is installed in a carrier.
- Two M3 XT60-collar mounting screws with selected nuts/washers. The collar provides three height holes on each side, but one matched left/right pair is used at a time.
- Two M3 axial forming-rod retainer screws and two matching heat-set inserts for the symmetric left/right slider bosses. Each modeled insert seat is 4.6 diameter × 5.2; select screw length so it engages the insert and bears on the rod end without excessive axial preload.
- Actual target board(s), all verified at no more than 36 wide, plus a 36-wide gauge block if available.
- Actual XT60 pigtail connector, representative 12 AWG and 14 AWG insulated wire, and representative solder joints. The source reference separates a 15.9 × 8.1 × 20.5 body from 5-long solder cups, totaling 25.5 axially; verify all dimensions against the real connector.
- Lead specimens with measured available centerline length. Include the default 44 specimen and at least one specimen of 50.425 or longer for the complete mechanical matrix.
- Calipers, feeler gauges, machinist square or angle gauge, and a dial indicator or fixed scale suitable for measuring end position/skew to 0.05 or better.
- Cold soldering iron for the access trial; temperature-controlled hot iron and normal PPE/extraction for the supervised thermal rehearsal.

Record printer, material, slicer profile, measured rod diameters, board width, wire type, available lead length, ambient conditions, selected coupon bore, exact four reaction-lock screws and twelve frame inserts, selected collar height and hardware, and the two axial-retainer screws/inserts.

## 1. Fit coupon gate

1. Measure each rod at several positions and record the largest diameter.
2. Print the coupon with 4.2, 4.3, 4.4, and 4.5 bores using the full-kit process settings.
3. Test all three rods in every bore. Select the smallest bore that permits smooth full-length insertion and sliding without binding, while rejecting a bore with perceptible lateral rock.
4. Repeat after the coupon has rested at room conditions for at least one hour.

Pass: one bore size works for all three rods with smooth motion and no visible cracking, layer separation, or meaningful rock. Record the chosen source parameter before printing the full kit.

Fail: no common bore works. Adjust the parameter/process and reprint the coupon; do not proceed by drilling only the full-size parts without updating the CAD/process record.

## 2. Assembly, board fit, and clearance

1. Heat-set all twelve reaction-lock inserts into the frame seats: three upper and three lower per side. Confirm no insert is fitted to a carrier.
2. Assemble the frames, four compact reaction carriers, three rods, one-sided M4 drive, nut, four reusable M3 reaction-lock screws, two symmetric M3 axial forming-rod retainers, and any specified washers/knob.
3. Verify rods seat through both frames without forcing and remain removable.
4. Move all four reaction carriers through their full tracks. At each setting, pass the same four lock screws through the carriers' diameter-3.4 clearances into the selected frame inserts. Confirm all twelve positions accept hardware and opposing carriers lock at matching indices without cracking, insert pullout, or track slip.
5. Set the removable XT60 collar to one height by installing exactly one M3 fastener at each side through the matching hole pair. Check all three paired heights in turn; reject crossed left/right heights.
6. Heat-set one forming-rod insert in each outward slider boss, then install the two axial M3 screws against the rod ends. Confirm the inserts remain fully seated; the rod engages 2.2 into each slider; and the screws retain it without axial preload, bowing, boss cracking, or loss of free guide motion.
7. Measure the real board width. This P0 assumes `board width <= 36`.
8. Center the board/workpiece in the 38 clear span and measure clearance to both inner frame faces.
9. Check the actual wire-side XT60 body and 5-long solder-cup region at each relevant collar height; do not use fit to the PCB-vertical vendor model as evidence of pigtail compatibility.

Pass: every compact reaction carrier locates and locks at all three datums using the four reused screws; all twelve frame inserts remain seated; no carrier shows cracking around its diameter-9 rod boss, diameter-7 lock boss, or 5-wide web; the collar mounts squarely at each matched height with only one installed screw per side; both axial retainers capture the forming rod without preload, damage, or drag; real board width is no more than 36; each side has at least 0.5 frame clearance; and the actual connector/lead can be loaded and removed without scraping or forced frame deflection.

## 3. Cold-iron access gate

With the iron unpowered, load representative board, wires, and connector. Exercise all intended approach angles to both solder joints in the closed/soldering state and repeat at the most obstructive upper/lower reaction settings.

Pass: the cold iron can reach and dwell on each joint without touching the printed frame, drive, rods, adjacent insulation, or connector body, and the operator can see both joint and tip.

Fail: any required joint or approach is blocked. Treat this as a geometry change, not an operator-workaround item.

## 4. Reaction-setting matrix and conserved lead length

Available lead length is the conserved wire-centerline arclength from the pad exit at `Y = -6` to the retained lead end. Do not pull, stretch, or silently lengthen a short specimen to make a setting appear usable. With `bend_start_y = 16` and `R = 6`, the minimum available lengths to upper settings at `Z = 22`, `28.5`, and `35` are approximately 37.425, 43.925, and 50.425 respectively. Therefore a 44 specimen supports upper settings 0 and 1, but not upper setting 2.

First test every combination usable by the default 44 specimen: upper indices 0 and 1 crossed with lower indices 0, 1, and 2. Then use a separately measured specimen at least 50.425 long to validate the full 3 × 3 mechanical matrix. For each applicable combination:

1. Set the left and right carriers for each reaction rod to matching index datums and lock all four M3 fasteners.
2. Run the forming rod from fully open to fully closed and back without wire, checking for binding, collision, or slot escape.
3. Load representative wire and close only with normal hand force.
4. Confirm the wire remains captured without changing its measured available length, the rods do not touch each other, the reaction carriers do not move from their index marks, and the board/connector can be inserted and removed.
5. Verify cold-iron access where the reaction setting changes the access envelope.
6. After release, check each compact carrier, reused M3 screw, selected frame insert, track, rod boss, lock boss, and connecting web for slip, witness marks, cracking, insert movement, or permanent deformation.

Pass: every combination usable by the 44 specimen operates without interference, unintended release, carrier slip, damage, lead-length change, or loss of required access; the specimen at least 50.425 long also completes all nine settings as a mechanical matrix. A short specimen's intentionally unusable setting is recorded as out of range, not as a fixture failure and not as a waived test of the full matrix.

## 5. Dial endurance and skew

Mark or instrument the left and right forming-rod ends at equivalent frame datums. End skew is the absolute difference between their progress along the 45-degree guide direction.

1. With no workpiece loaded, perform 25 complete dial cycles from fully open to fully closed and back. Do not manually help the undriven end.
2. At each closed state, observe binding and record skew; record measured skew at minimum on cycles 1, 5, 10, 15, 20, and 25.
3. Repeat representative closes with the intended wire load, including the stiffest planned wire and worst usable reaction setting. Use the 50.425-or-longer specimen when the worst mechanical setting includes upper index 2.
4. Inspect the M4 screw/nut trap, guide surfaces, spanning forming rod, compact diameter-10 sliders, both axial M3 retainer screws/inserts and 8.6 bosses, reaction-carrier tracks, four reused carrier-lock screws, twelve frame inserts, compact carrier bosses/webs, collar mounts, and rod bores for wear, cracking, loosening, slip, or progressive bias.

Pass:

- Unloaded end skew is no more than 0.25 at every measured cycle.
- Loaded end skew is no more than 0.50.
- All 25 cycles complete without binding, manual correction, reaction-carrier slip, loosening, damage, or worsening trend.

Architecture gate: either skew limit failing makes the one-sided M4 architecture a **NO-GO**. Move to a mechanically synchronized/two-sided drive concept before further P0 refinement.

## 6. Formed-angle and surface-quality checks

Form at least three representative samples for each intended wire gauge and include the worst usable reaction combination identified above. Record the conserved available lead length for every specimen. Measure after normal cooling and release, using a defined straight length on both sides of the bend.

Pass:

- Released centerline bend angle is `90° ± 3°`.
- No flat spot, kink, indentation, or local departure from the intended bend envelope exceeds 0.25.
- Insulation has no cut, split, whitening, or conductor exposure.

Record springback separately; do not hide systematic springback by measuring while the wire remains clamped.

## 7. Deflection and frame-separation checks

At the worst loaded condition:

1. Measure the forming rod's unloaded reference position and its loaded position at midspan. Rod deflection is the load-direction displacement after subtracting rigid frame motion.
2. Measure the clear distance between inner frame faces at the same fixed datums before loading and at peak load. Frame separation is the absolute increase from the unloaded value.

Pass:

- Rod deflection is less than 0.25.
- Frame separation increase is less than 0.5.

Also reject visible permanent set, cracking, nut-trap damage, or a rod that does not return to its unloaded reference after release.

## 8. Thermal rehearsal

Only after the cold-iron gate passes, perform a supervised solder-and-cool rehearsal with the actual temperature-controlled iron, representative board/pads, flux/solder, wire, and XT60 pigtail. Use normal extraction and PPE.

1. Record baseline dimensions and smoothness of the nearby guide/drive features.
2. Complete the intended solder dwell on both joints while the jig holds the leads.
3. Keep the lead constrained for the intended cooling period, then release and remove it normally.
4. Repeat enough times to expose the frame to a realistic work session, including the longest expected dwell once; do not intentionally overheat the board or printed jig.
5. Recheck fit, stroke, skew, angle, rod deflection, and frame separation after cooling to room temperature.

Pass: no softening, glossing, scorching, odor beyond the chosen material's normal process behavior, warping, delamination, fused motion, loss of clamp force, or measurable acceptance-limit regression.

Stop immediately if the iron or hot joint contacts printed material, insulation chars, the frame softens, or the workpiece becomes unsafe to handle.

## Release decision and record

P0 passes only if every gate passes: the 36-case CAD matrix and 101-position extreme-setting sweep; coupon fit; all four compact reaction carriers, four reused lock screws, and twelve frame inserts; real board width and frame clearance; cold-iron access; every reaction combination usable at the measured lead length; the full 3 × 3 mechanical matrix with a specimen at least 50.425 long; 25 dial cycles; skew; `90° ± 3°` angle; no flat spot over 0.25; rod deflection under 0.25; frame separation under 0.5; and thermal rehearsal.

The collar-height pair and both symmetric axial forming-rod retainers are also release gates. Their fastener selections must be recorded; both heat-set inserts and 2.0 walls must remain intact through endurance and thermal tests; and the retainers must hold 2.2 rod seating without axial preload, drag, or obstruction of the XT60 load/unload and iron-access paths.

For each specimen/configuration, record measured values rather than pass/fail alone, plus photos of setup, both forming-rod ends, the released bend, and any wear or thermal marks. A CAD pass does not substitute for this physical record.
