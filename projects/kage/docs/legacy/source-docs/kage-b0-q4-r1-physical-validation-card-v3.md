# KAGE B0 Q4-R1 physical validation card — v3

Status: revision candidate; requires independent acceptance  
Article: `p3_v3_mvp_base_q4_r1`  
Gate: four printed quadrants become one usable 300 mm base  
Rule: any RED stops B1; unresolved BORDERLINE is not a PASS

## CAD-passed facts versus physical unknowns

The focused CAD suite passed `13/13`. It established exactly four one-solid
quadrants and four one-solid bridges, nominal 300 mm OD and 0.10 mm seams,
coplanar nominal datums, 260 mm bed containment with a 5 mm brim, modeled
hardware/access features, upward S4 insertion after S1–S3, and an untouched
R118..150 support annulus.

CAD did **not** establish printed shrinkage, first-layer warp, hardware fit,
false screw preload, last-bridge insertion by hand, full-loop closure,
free-state flatness, service damage, clamp retention, or vertical behavior.
Only this physical run can decide those items.

## Bring

Printed from one material/profile:

- Q1–Q4, supplied `*_front_down.step`, front face on bed, 5 mm brim, no support;
- S1–S4, supplied `*_bottom_down.step`, pockets/blind bores upward, no support
  in those openings.

Hardware:

- 8 x M3x6 ISO 7380-1 button-head screws;
- 8 x ISO 4032 M3 hex nuts;
- 8 x D4x6 steel dowel pins.

Tools:

- matching hex key, phone camera, 300 mm straightedge, known-flat reference
  plane, and four equal-height supports; if the plane is not certified, verify
  it by the method below before measuring the base;
- long caliper, beam caliper, or an equivalent two-block measurement setup
  verified to resolve `<=0.25 mm` across 300 mm; record the tool and resolution;
- calibrated feeler gauges for final gap, step, and flatness decisions;
- printer/receipt paper strips may be used for quick screening only.

Do not use a household ruler or paper stack as final evidence for a numeric
limit. Borrow the required measuring tool if necessary.

## Reference-plane verification

Use a certified flat plate if available. Otherwise clean the candidate
table/counter and the 300 mm straightedge. Place the straightedge at
0/45/90/135 degrees across the intended test area, then flip it end-for-end and
repeat all four orientations. A calibrated 0.25 mm feeler must not enter
anywhere under the straightedge in any pass. Record the worst location, result,
and one photo. If it enters, the plane is not qualified; find another surface
before applying the base's 0.50 mm flatness limit.

## Initial hardware-fit gate

Complete this before arranging the quadrants. Any rejection is RED; stop and
do not compensate by tightening harder.

1. Press two D4x6 pins straight into each bridge, at R78 and R108, using steady
   non-impact pressure. Measure while pressing and stop only when the calibrated
   tool reads the target exposure of exactly `2.50 mm`; record all eight
   readings. There is no `2.40..2.60` passing band.
2. Reject a pin/bore if the pin free-drops, requires impact, or produces a
   crack, whitening, bulge, or separated layer. After reaching 2.50 mm, record
   the exposure, invert the bridge over a folded towel for 10 seconds, then
   apply a gentle three-second fingertip tug to the pin without tools. Measure
   exposure again. Any release, visible motion, or measurable before/after
   change is RED.
3. Load two nuts into every bridge from the open top. Each nut must sit flat,
   below the bridge seat, and remain nonspinning when its screw is turned.
   Reject a cocked, freely spinning, or forced nut.
4. At each seam, with the bridge seated against both quadrants, lightly test
   both screws and then loosen them for assembly. Reject any screw that becomes
   hard before its head contacts the quadrant, or appears tight while the
   bridge can still move or a paper strip remains between bridge and quadrant.
   Either symptom is false preload from bottoming, cross-threading, or a
   mis-seated nut—not usable clamping.

## Exact assembly sequence — initial assembly is Cycle 1

1. Mark Q1–Q4 and S1–S4. Photograph the eight clean printed parts, 24 hardware
   pieces, and completed initial hardware-fit record.
2. Arrange all four quadrants front-face up in final XY position on four
   equal-height supports, leaving every seam accessible from below. Keep all
   four quadrants supported through step 4.
3. Insert S1, S2, then S3 upward from below. Guide both pins into their split
   features, seat the bridge against both undersides, add two screws from
   above, and leave them loose.
4. Insert S4 **upward from below as the last bridge** while all four quadrants
   remain in final XY position. Do not attach S4 to Q4 and lower Q4. Photograph
   S4 halfway inserted and fully seated.
5. Confirm all eight screws are present and loose. Put all four bridge bottoms
   on the verified plane. Tighten finger-snug S1, S3, S2, S4; repeat that order
   until uniformly snug. Never use torque to pull a visible seam closed.
6. Remove the base, leave it unconstrained for one hour, and run Checks 1–3.
   This completed build is **Cycle 1**.
7. For Check 4, fully disassemble and repeat steps 2–6 only twice more. Those
   are Cycles 2 and 3; do not add three more assemblies.

## Six checks

1. **Last bridge and full-loop closure.** S4 seats with hand pressure; no part
   is bent, lifted, filed, heated, or forced. No seam overlaps or bows. With the
   required `<=0.25 mm`-resolution setup, record raw diameters `D0`, `D45`,
   `D90`, and `D135`, then calculate `max(D)-min(D)`. PASS limits are each
   `299.50..300.50 mm` and range `<=0.50 mm`.

2. **Seam gap and step.** Measure each seam at inner, middle, and outer radius
   with calibrated feelers; record all 12 gaps. PASS gap is `0.05..0.30 mm`
   with no overlap/forced closure. Measure step on both sides of each seam and
   record the worst location/value; PASS is `<=0.25 mm`.

3. **One-hour free-state flatness.** On the verified plane, press each quadrant
   lightly in turn; no rocking. Sweep the straightedge across both diameters
   and both diagonals. Measure and record the worst calibrated gap and its
   location; PASS is `<=0.50 mm`.

4. **Three total service cycles.** Cycle 1 is the initial assembly above;
   perform only Cycles 2 and 3 as repeats. Record S4 insertion as
   `free/light/firm/forced` each cycle and all hardware damage. PASS requires no
   force escalation, crack/whitening, loose/pulled pin, spinning nut, stripped
   screw, enlarged hole, false preload, or permanent seam opening.

5. **Vertical self-weight retention.** After Cycle 3, orient the assembly with
   **Q1 down**. A folded towel may contact only the Q1 outer rim; no other
   quadrant or seam may touch the towel, wall, or a load-bearing prop. A loose
   safety tether may prevent a fall but must carry no weight. Photograph and
   record `down quadrant = Q1`, start time, and end time after 60 minutes. No
   seam/hardware may move or disengage. Return horizontal and repeat full
   Checks 1–3, preserving all raw measurements.

6. **Ten lift/place cycles.** Over a soft surface, lift about 50 mm by one
   quadrant's outer rim, hold three seconds, then place flat. Use
   `Q1,Q2,Q3,Q4,Q1,Q2,Q3,Q4,Q1,Q3`. No seam may click, disengage, grow, or
   change step, and no hardware may move. Then repeat full Checks 1–3 again,
   preserving all raw measurements.

Paper stacks are screening-only. A paper screen suggesting a limit, any value
read exactly at a numeric boundary, or any reading whose uncertainty crosses a
boundary is `BORDERLINE` until repeated with the calibrated tool. After
calibrated measurement, PASS is within the inclusive numeric limit and RED is
only outside it. Never round a BORDERLINE result into PASS or RED.

## Required photos

1. Eight printed parts, all hardware, the hardware-fit setup, and reference-
   plane verification.
2. All quadrants supported with S1–S3 installed.
3. S4 halfway inserted upward and fully seated.
4. Cycle-1 finished front and underside views with labels.
5. Caliper/equivalent setup showing one diameter; worst seam and flatness gauges.
6. Q1-down vertical setup at start and end of the 60-minute dwell.
7. Final front and underside views after lift/place and repeated Checks 1–3.

## Results record

Print: material `______` printer `______` nozzle `____` layer `____`  
profile `________________` date `______`  
OD tool/setup `________________` resolution `____ mm` verified by `________`  
feeler set/tool `________________` calibration/check `________________`  
reference plane `________________` 0.25 mm verification/result `________`

Initial pin exposure, mm:

| Stage | S1-R78 | S1-R108 | S2-R78 | S2-R108 | S3-R78 | S3-R108 | S4-R78 | S4-R108 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| At 2.50 target before inversion | `__` | `__` | `__` | `__` | `__` | `__` | `__` | `__` |
| After inversion and fingertip tug | `__` | `__` | `__` | `__` | `__` | `__` | `__` | `__` |
| Before/after change | `__` | `__` | `__` | `__` | `__` | `__` | `__` | `__` |

Hardware fit: pins free-drop/move/damage `________`; nuts flat/nonspinning
`________`; screws clamp without false preload `________`; photo `________`.

Checks 1–3 raw data at each required checkpoint:

| Checkpoint | D0 | D45 | D90 | D135 | D max-min | Gap S1 I/M/O | Gap S2 I/M/O | Gap S3 I/M/O | Gap S4 I/M/O | Worst step + location | Worst flatness + location | Status |
|---|---:|---:|---:|---:|---:|---|---|---|---|---|---|---|
| Cycle 1, one-hour free state | `__` | `__` | `__` | `__` | `__` | `__/__/__` | `__/__/__` | `__/__/__` | `__/__/__` | `________` | `________` | `____` |
| After Q1-down vertical dwell | `__` | `__` | `__` | `__` | `__` | `__/__/__` | `__/__/__` | `__/__/__` | `__/__/__` | `________` | `________` | `____` |
| After ten lift/place cycles | `__` | `__` | `__` | `__` | `__` | `__/__/__` | `__/__/__` | `__/__/__` | `__/__/__` | `________` | `________` | `____` |

| Check | Required observation | Raw / worst-case result | Photo(s) | PASS / BORDERLINE / RED |
|---|---|---|---|---|
| 1 | S4 insertion; loop closure; four OD values/range | `________________` | `___` | `___` |
| 2 | 12 gaps; worst step/location | `________________` | `___` | `___` |
| 3 | Rocking; worst flatness/location | `________________` | `___` | `___` |
| 4 | S4 force C1/C2/C3; damage/fit changes | `________________` | `___` | `___` |
| 5 | Q1-down times; pre/post changes | `________________` | `___` | `___` |
| 6 | Ten-cycle observations; post-check changes | `________________` | `___` | `___` |

Overall B0 result: `PASS / BORDERLINE / RED`  
Failure or unresolved boundary: `________________________________________`

