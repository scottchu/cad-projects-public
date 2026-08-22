# KAGE P3 V3 direct gear-race guidance R2 revision K — frozen numeric handoff

Status: **revision K design handoff, frozen for implementation**  
Target implementation slug: `p3_v3_direct_gear_race_guidance_r2`  
Units: millimetres, degrees, newtons, and seconds unless stated otherwise.  
Coordinates: XY is the wall/clock plane; +Z faces the viewer; positive ring
rotation follows the existing P3 V3 source convention.

This document is the authoritative design input for the R2 implementation.
The implementation agent may reject an impossible interface with measured
evidence, but must not silently tune these values around generated geometry.

## Revision table

| Revision | Status | Mechanical decision |
|---|---|---|
| A | Superseded | Initial numerical handoff; identified architecture and validation envelopes |
| B | Superseded | Recessed serviceable seams, printable stationary quadrants, back-side clamps, specified roller towers, physical unsafe-q key, deterministic motion model, Hall keep-outs, print/3MF manifest and transitive parity |
| C | Superseded | Contact-solved flange overlap, finite tolerance-shell equilibrium, canonical crop identity, non-overlapping counterweights, provisional optical cone, complete stationary/key/service interfaces and production POM rollers |
| D | Superseded | Correct pin-contact capsule travel, raw combined contact-datum shell, optical ADR deferral, contained counterweights, all-occurrence parity, M3×7 stationary joints and exact production cap manifest |
| E | Superseded | Two-stage fixed-tower setup calibration and post-calibration shell; did not yet couple the three roles on each common physical axle and allowed zero-thickness endpoint shims |
| F | Superseded | Shared H/M/S settings and matched-ring intervals, but its 64-shell proof under-enumerated nine independently bounded role×tower residuals |
| G | Superseded | Correct 4096-shell enumeration exposed that one compliant q cannot satisfy opposed accepted H/M/S residuals |
| H | Superseded | Accepted role-local compliant architecture and math, but left seven axle, spine, assembly, manifest, coupon and purchased-spring manufacturing interfaces open |
| I | Superseded | Manufacturing-complete interfaces, but four exact manufacturing contradictions remained in axle endplay, cassette-pin retention, adjuster insertion and production count |
| J | Superseded | Corrected axle, pin-retainer, adjuster and manifest concepts, but left the adjuster screw blocked by a closed wall, duplicated its insert-install stage and omitted pin drawing datums |
| K | Current | Through-bored insert adjuster, one explicit heat-install stage and a fully dimensioned/clocked M2 cassette-pin retainer |

Revision K supersedes only the conflicting J2 pin-retainer drawing omissions,
J3 adjuster closed-end wall, I4 duplicate adjuster-insert installation wording
and the affected I6/I8 validation references. Revision J's 94-occurrence
manifest and every other accepted mechanical clause remain normative.

Revision J supersedes only the conflicting I1 fixed-axle collar/endplay values,
I2 cassette-pin retention, I4 affected assembly/service words, I5 production
count, I6 affected references, I7 adjuster capture and I8 affected tests.
All accepted Revision I mechanics, architecture and interfaces not explicitly
changed below remain normative.

Revision I supersedes only the incomplete manufacturing interfaces and relative
manifest/assembly language in Revision H. Revision H's role-local compliance,
discrete setup, force/contact equations and 4096-shell proof remain normative.
Revision H supersedes Revision F's common 300° axle/displacement/force clauses,
adds discrete fixed-tower setup acceptance, and updates the active assembly and
coupon manifest. Revision G's full 4096-shell enumeration remains normative,
with its common-q requirement replaced by the three role-local solutions below.
All other Revision F clauses remain frozen and normative.
Revision F supersedes the setup/equilibrium and shim equations in Revision E
section E1 only. All other Revision E and Revision D clauses remain frozen and
normative. Revision D in turn supersedes any conflicting numeric value or
interface in revisions A, B or C later in this document. Non-conflicting
architecture and acceptance language remains active.

## Revision K normative amendments

### K1. The M3 adjuster has a continuous screw path

The three role adjusters retain the J3 OD4.20×4.00 heat-set insert and 6.60
minimum boss. The former closed-end wall is deleted. In insert-axis coordinate
`x`, positive from clock interior toward the spring, the installed insert
occupies `x=0.00…4.00`; a concentric finished M3 clearance bore occupies
`x=4.00…7.00`; and the moving spring-seat washer datum occupies
`x=7.00…9.00` over the frozen 2.00 adjustment travel.

| Adjuster through-interface | Frozen value |
|---|---:|
| finished through-bore diameter | D3.50 +0.10/-0.00 |
| clear-bore length beyond insert | 3.00 |
| minimum ligament around insert OD4.20 | 1.20 radial |
| minimum ligament around maximum D3.60 bore | 1.50 radial |
| M3×12 tip coordinate over adjustment | x=7.00…9.00 |
| socket-end coordinate over adjustment | x=-5.00…-3.00 |
| minimum measured insert thread engagement | 3.00 |

The D3.50 bore is clearance only and contains no printed thread. Actual-solid
tests must pass a D3.60 maximum-material screw-path cylinder continuously from
the insert exit through the entire washer travel, prove zero positive-volume
intersection with the boss, and measure both annular ligaments at every role.
The M3 screw must remain tool-accessible at both travel stops.

### K2. Adjuster inserts are heat-installed exactly once

All three adjuster inserts are heat-installed in the bare printed 300° spine
during authoritative assembly step 2. At that state, before the spine, rings,
cassettes, springs or stop plate are mounted, each insert must admit its complete
D7.00×25.00 heat-tool cylinder from the clock-interior side, coaxial with the
insert pocket. No later assembly or service step repeats heat installation.
Step 6 only introduces the three washers, M3×12 set screws, springs, guide pins
and cassettes into the already-inserted spine.

### K3. Complete custom cassette-pin and M2-retainer drawing

The J2 D3.99×7.70 pin and ISO 4762 M2×4 screw remain. The retaining washer is
D6.00×0.50 with a finished concentric bore D2.20 +0.10/-0.00. Every retained
roller/thrust-washer centre bore is at most D4.10, so the D6 washer provides at
least `(6.00-4.10)/2 = 0.95` radial capture overlap. With the ISO 4762 M2 head
minimum D3.62 and washer bore maximum D2.30, screw-head bearing overlap is at
least `(3.62-2.30)/2 = 0.66` radial. Actual purchased washer and screw-head
diameters replace nominal values in production acceptance.

Pin coordinate `z_p=0.00` is the blind-seat end and `z_p=7.70` is the viewer
end. The existing 2.00-long ×0.40-deep retention flat occupies
`z_p=1.50…3.50`; its centre at `z_p=2.50` is coaxial with the cassette M3×4
set-screw axis. In cassette coordinates the set screw advances in +u from the
radial interior, so the flat outward normal is -u and antiparallel to the screw
advance vector, angular error ≤2°. The flat remains entirely inside the 4.25
blind insertion span, leaving 1.50 pin material below it and 0.75 before the
cassette mouth.

Reference/actual-solid tests must instantiate the purchased screw and measured
washer, prove both minimum annular overlaps, the 0.15 roller endplay, the flat's
axial bounds/depth, screw-axis coincidence, -u orientation and unobstructed M2
and M3 tool paths in all three role cassettes.

## Revision J normative amendments

### J1. Fixed-axle endplay datums are arithmetically closed

The fixed upper bridge remains at Z=16.70…19.70 and its D8.00×0.15 thrust
washer therefore ends at Z=19.85. The split collar lower face is corrected to
Z=19.95±0.05. Consequently the physical endplay is
`collar_lower_Z - 19.85 = 0.05…0.15`, inclusive. The seated axle top remains
Z=24.80; with a 4.00-thick collar, its exposed extension above the collar is
therefore 0.80…0.90. Any former Z=19.90±0.05 collar datum or 0.85…0.95
extension is superseded.

The implementation must derive all four values from actual faces: bridge top,
washer top, collar lower face and collar upper face. It may not assert endplay
from nominal labels. Both tolerance endpoints and the nominal 0.10 endplay
state must pass without washer/collar contact.

### J2. Cassette roller uses positive screw retention, not a nonstandard groove

The D3.99×7.70 polished cassette pin remains, but its blind insertion depth is
4.25 rather than 3.50. The pin has a concentric axial M2×0.40 internal thread,
4.00 full tapped depth, in its viewer end. One ISO 4762 M2×4 socket-head screw
and one D6.00×0.50 stainless retaining washer with finished
D2.20 +0.10/-0.00 bore replace the E-clip and groove.
The screw engages 3.50 nominal thread after the washer and is tightened to
0.12 N·m with low-strength removable threadlocker. The retaining washer seats
on the pin end, not on the running thrust washer.

The closed stack is exactly:

```text
4.25 pin insertion
+ 0.15 lower POM thrust washer
+ 0.50 lower roller flange
+ 2.00 POM running band
+ 0.50 upper roller flange
+ 0.15 upper POM thrust washer
+ 0.15 roller axial endplay
= 7.70 pin length
```

The existing radial M3×4 set screw and K3-clocked pin flat remain as secondary
pin retention while the M2 screw/washer is serviced. No groove is cut in the
D3.99 pin. The M2 washer is the positive roller retainer. Actual solids must
prove the 4.25 insertion, 1.50 minimum blind-bottom wall, 3.30 roller/washer
stack, 0.15 endplay, M2 engagement, washer overlap and both tool paths.

### J3. Spring adjusters use heat-set inserts; the impossible nut mouth is gone

Each role uses the same M3×12 cup-point adjuster and D4.00×0.50 stainless
spring-seat washer, but its standard hex nut, AF pocket, side-loading mouth and
snap lip are deleted. The thread receiver is one M3 heat-set insert,
OD4.20×4.00, installed from the clock interior on the radial adjuster axis.
Its printed boss is at least 6.60 across every section, giving at least 1.20
wall around the insert. The concentric D3.50 +0.10/-0.00 through-bore and its
3.00 length are defined by K1; no closed-end wall exists. The insertion lead
is 0.40×45°. A D7.00×25.00 heat-install tool cylinder and the existing
D4.00×20.00 adjustment-tool cylinder must both remain clear of rings, motors,
springs, adjacent lanes and stationary joints.

The insert provides at least 3.00 measured full-thread engagement throughout
the frozen 0.00…2.00 screw adjustment travel. At both stops at least 2.00 of
screw remains behind the insert and the tip remains captured in the spring-seat
washer. The nominal setup remains 1.00. No printed thread or friction-captured
nut is accepted.

### J4. Exact production occurrence count is 94

Only the two fixed common axles use inter-role spacers: Hour-to-Minute and
Minute-to-Second on each axle, giving four installed spacers. The three
role-local 300° cassette pins have no inter-role spacer. With two printed
spares, the production quantity is six role spacers, not eight.

The authoritative total is exactly:

`94 = 12+12+4+4+16+3+3+6+3+2+2+4+1+3+1+6+3+9`.

Every former production occurrence total is superseded. Coupons, ladders and
purchased/non-printing references remain outside this count.

## Revision I normative amendments

### I1. Fixed-tower D4 axle seat and retention after eccentric removal

The fixed 60° and 180° towers contain no eccentric bushing. Each uses one
straight polished D3.99×30.00 axle at the common H/M/S radial datum selected by
its locked shim pair.

| Fixed-axle interface | Frozen value |
|---|---:|
| lower blind seat finished diameter/depth | D4.05 × 3.00 |
| lower seat bottom datum | Z=-5.20 |
| lower seat mouth datum | Z=-2.20 |
| minimum wall below blind seat | 1.50 |
| upper bridge finished through-bore | D4.06 |
| upper bridge Z | 16.70–19.70 |
| upper thrust washer | D8.00 × 0.15 |
| axial endplay above washer | 0.05–0.15 |
| split top collar | D4 bore, D8 OD × 4.00, M3 clamp |
| collar lower-face setup datum | Z=19.95±0.05 |
| axle top after seating | Z=24.80 |
| axle extension above collar | 0.80–0.90 |

The axle bottoms on the flat blind-seat shoulder and is radially supported by
both the 3.00-deep lower seat and the 3.00-thick removable upper bridge. The
collar is tightened only after the 0.15 washer and 0.05–0.15 endplay gauge are
installed. Its M3 clamp has a D6.50 radial tool cylinder to the clock exterior.
Actual solids must prove the blind bottom, two bearing spans, washer/collar
datum, axle extension, endplay, D4 roller/spacer stack and service withdrawal
path. No friction-only press fit is credited as axial retention.

### I2. Role-local D3.99 cassette pin interface

Each 300° cassette uses one D3.99×7.70 polished pin inserted from the viewer
side into a D4.04×4.25 flat-bottom blind bore. Diametral running clearance is
0.05. The bore has 1.50 minimum wall beneath its bottom shoulder. The pin end
must contact that shoulder; pin height may not be set by the roller or M2
retainer.

The exposed stack is:

```text
cassette top datum
-> 0.15 POM thrust washer
-> 0.50 lower roller flange
-> 2.00 POM running band
-> 0.50 upper roller flange
-> 0.15 POM thrust washer
-> 0.15 axial endplay to the pin end
-> D6.00×0.50 retaining washer and ISO 4762 M2×4 screw
```

The pin contains no retaining-ring groove. Its viewer end has a concentric
M2×0.40 internal thread with 4.00 full tapped depth. A radial M3×4 cup-point
set screw in the cassette acts on a
2.00-long ×0.40-deep pin flat and prevents pin rotation/withdrawal during
M2-retainer service. It passes through one M3 heat-set insert, OD4.20×3.00,
and has
3.00 full-thread engagement before its final 1.00 reaches the pin flat. Insert
wall is ≥1.20 around the pocket and its D4.00×12.00 tool path is clear from the
radial interior.
The M2 screw and D6 washer are roller retention; the blind shoulder plus set
screw is pin retention. All fits are serviceable without cutting a cassette.

### I3. Complete shared 300° spine and three-window stop plate

Local station coordinates are `u` radial outward, `v` tangential positive and
`w=Z` toward the viewer. The one printed PETG spine has these frozen interfaces:

| Spine interface | Frozen value |
|---|---:|
| overall functional envelope | 24.00 u × 20.00 v × 21.70 w |
| envelope Z | -5.20…16.50 |
| stationary mounting foot | 24.00 × 20.00 × 3.00 |
| main back web | 4.00 radial × 20.00 tangential |
| minimum wall around guide receiver | 1.50 |
| mounting fasteners | 2 × M3×8 socket head |
| mounting washer | 2 × D7.00×1.00 |
| mounting inserts | 2 × M3 heat-set, 4.00 long |
| mounting fastener tangential spacing | ±7.00 |
| insert closed-end wall | 1.00 minimum |
| mounting driver cylinders | D6.50 from viewer side |

Each role lane is centred at its running-band Z centre (-1.10, 5.60, 12.30),
is engraved H/M/S, and derives both D3 guide receivers and spring/adjuster axis
from that datum. Six D3 shoulder screws engage ≥4.00 in spine receivers and
retain ≥1.50 wall around every receiver at every cassette position.

The stop plate is one 3.00-thick PETG plate on the +v exterior face, 18.00
radial ×20.00 axial. It contains three radial 3.20×5.00 capsules centred at the
three role Z datums. Each cassette has one D3.00 tangential stop pin projecting
through its own window with 0.10 transverse clearance per side. Plate fasteners
are two M3×8 socket-head screws through D7×1 washers and the 3.00 plate into
4.00-long M3 heat-set inserts, with 1.00 closed-end wall and zero protrusion.
Their axes are tangential; D6.50×25.00 tool cylinders approach from +v and do
not cross any ring, spring, cassette or motor envelope.

Each stop pin is integral PETG geometry on its labelled cassette, projects
4.00 from the +v cassette face, and has a 1.00 root fillet plus 1.50 minimum
backing wall. It is printed in the cassette's source-derived orientation and
must survive a 10 N tangential proof load with permanent tip displacement
≤0.10. A separately glued pin or unreceived screw is forbidden.

The anti-reversal key is a 4.00 radial ×3.00 axial ×2.00 tangential tongue at
the H end, offset 3.50 radially from plate centre. Its spine receiver is
4.40×3.40×2.20. At the S end a continuous 3.00 wall occupies the mirrored key
volume, so a reversed plate has positive-volume interference before either
screw can enter an insert. Minimum wall around each stop window, screw and key
receiver is 1.50. The red `SERVICE / DO NOT POWER` field is on the spine face
covered by the correctly installed plate and exposed only after plate removal.

### I4. One authoritative assembly and service sequence

Revision C section C8 and the older section 8 assembly/service sequence are
entirely superseded. The only active sequence is:

1. Print and measure the fixed-tower and complete 300° station coupons. Ream/
   finish only the source-designated bores, choose production ladder values,
   measure all three rings and select discrete `A_60,A_180` from `S_A`.
2. Heat-install all rear/front stationary, motor-yoke, fixed-tower, spine and
   stop-plate inserts, including exactly three role-adjuster inserts in the
   bare spine. Prove each K2 D7 heat-tool cylinder, then gauge every insert
   depth and every applicable closed-end wall. No later step heat-installs an
   adjuster insert.
3. Assemble four rear stationary quadrants using four joints, eight
   registration keys and eight frozen wall-side M3×7 stationary screws.
4. Install three motor yokes loosely, then their motor/miter/output-shaft
   cartridges. Set every shaft endplay to 0.05–0.15; leave powered keys off.
5. At each fixed tower, install its selected indexed inboard/outboard shim pair,
   tower leaf, two D7×1 washers and two M3×8 clamps. Match all witness indices,
   tighten both clamps, install the bare D3.99×30 axle to its blind stop, and
   leave the upper bridge, washer and collar off.
6. Mount the one 300° spine with its two complete M3×8 mounting stacks. Install
   the three adjuster washers, set screws, springs and guide pins, then three
   labelled cassettes with six shoulder screws. Leave the stop plate off.
7. Install the Hour roller on both fixed axles and the H cassette pin. Assemble
   the four Hour carrier quadrants around all three roller flanges; install its
   seam hardware, Hall magnet/cap and selected balance slugs/caps.
8. Add the fixed-axle Hour-to-Minute spacers and repeat step 7 for Minute; add
   Minute-to-Second spacers and repeat for Second.
9. Install both fixed upper bridges, D8×0.15 washers and split D4 collars at
   Z=19.95±0.05. Verify 0.05–0.15 endplay and collar tool access.
10. Install the three-window stop plate, both complete M3×8 stacks and its
    reversal key. Prove all three powered ±1.00 contacts and inaccessible
    ±1.01 positions before applying spring preload.
11. Set H/M/S spring compression to 1.50 independently. Measure each force,
    total force and all three `q_r` while rotating each ring through 360°.
12. Tune motor-yoke q only inside its frozen powered window, lock all yokes,
    install the three powered-window keys, and repeat three independent 360°
    rotations plus the complete homing, Hall, COM, mesh and clearance checks.
13. Assemble the four front stationary quadrants with four joints, eight
    registration keys and eight frozen viewer-side M3×7 screws. Install the
    registered front structure only after all internal service checks pass.
14. Run all-state parity and safety checks off-wall; only then mount the clock.

Service starts off-wall and unpowered. Remove the front structure, stop plate
only when cassette service travel is needed, fixed collars/bridges, then rings
in Second/Minute/Hour order. A role cassette can be removed after its ring and
M2 retainer clear; release its pin set screw before withdrawing the pin. Fixed
tower
leaves/shims and the 300° spine are serviced last. Reassembly follows steps
5–14 and always repeats discrete witnesses, endplay, preload and 360° checks.

### I5. Authoritative production object manifest

The production print-project 3MF contains exactly these printed occurrences:

| Printed production object | Count |
|---|---:|
| moving carrier quadrants, four per role | 12 |
| moving recessed seam plates, four per role | 12 |
| rear stationary quadrants | 4 |
| front stationary quadrants | 4 |
| stationary-joint registration keys, eight rear + eight front | 16 |
| motor yokes | 3 |
| output pinions | 3 |
| miter gears | 6 |
| motor powered-window keys | 3 |
| fixed tower leaves | 2 |
| fixed tower upper bridges | 2 |
| selected indexed fixed-tower shims, two per tower | 4 |
| 300° structural spine | 1 |
| 300° role slider cassettes H/M/S | 3 |
| 300° three-window stop plate | 1 |
| role spacers, four installed + two spares | 6 |
| Hall pocket caps | 3 |
| balance-pocket caps | 9 |
| **total printed production occurrences** | **94** |

Fins, teeth, Hall pockets and balance pockets are integral to their carrier
quadrants and are not separate objects. Production contains zero printed POM
rollers, roller spools, generic compliant carriages, compliant upper bridges,
eccentric bushings, eccentric locks, fixed eccentric tower bars, old common
300° axles, old single-spring parts, coupons or fit ladders. Purchased axles,
pins, POM rollers, M2 roller-retainer screws, collars, washers, springs, inserts, screws,
magnets, slugs, motors, bearings and electronics are BOM references, not print
objects. This table supersedes every earlier relative manifest/count statement.

### I6. Source-derived complete-station coupons and exact U1 ladders

The complete 300° coupon is a canonical source crop containing the full spine,
all three production cassettes, all six guide interfaces, three stop pins, the
complete stop plate/key/fastener receivers, three spring/adjuster lanes and all
three production pin bores. Purchased springs, pins, rollers, screws, inserts
and washers appear as non-printing reference occurrences. Crop
stops may be added only outside the canonical interfaces. Its oriented printed
bounds must be ≤110.00×85.00×24.00.

The coupon 3MF has exactly five printing occurrences: one spine, three labelled
cassettes and one stop plate. Its reference-only occurrences are six D3 guide
shoulder screws, three springs, three M3×12 adjusters/inserts/seat washers,
three D3.99 cassette pins, three POM rollers, six 0.15 thrust washers, three
M2×4 roller-retainer screws, three D6.00×0.50 retaining washers,
three pin-retention M3×4 screws/inserts, two stop-plate screw/washer/insert
stacks and two spine-mount screw/washer/insert stacks. Missing references or a
reference incorrectly flagged for printing fails the coupon manifest.

The 300° fit-ladder plate contains exactly 18 individually labelled cells:

| Cell family | Three values |
|---|---|
| cassette D3.99 pin finished bore | 4.00 / 4.04 / 4.08 |
| D3 shoulder-guide capsule width, length 5.50 | 3.35 / 3.40 / 3.45 |
| D3 stop-window width, length 5.00 | 3.15 / 3.20 / 3.25 |
| spring seat diameter, depth 1.50 | 4.15 / 4.20 / 4.25 |
| M3 adjuster heat-set-insert pilot, depth 4.20 | 3.90 / 4.00 / 4.10 |
| stop-plate/key running clearance per side | 0.15 / 0.20 / 0.25 |

The fixed-tower ladder retains the nine complete keyed shim pairs from H6 and
adds exactly three blind-seat/bridge-bore paired cells at D4.02/D4.05,
D4.05/D4.06 and D4.08/D4.10. Each includes the full blind bottom, upper bridge,
washer/collar reference and tool cylinder. Its bounds are ≤240×180×12.

Coupon and ladder 3MFs use the U1 conservative 260×260×260 volume, 5.00 minimum
XY bed margin and zero out-of-bed/support-on-interface objects. Exact oriented
bounds, object counts, canonical crop digests and reference/non-printing flags
are asserted after Orca/Snapmaker Orca reload. The complete 300° coupon, its
18-cell ladder, fixed coupon and fixed ladder are separate from the 94-object
production 3MF.

### I7. Purchasable spring and adjuster constraints

Each of the three springs must be a catalogued closed-and-ground compression
spring meeting all of:

| Purchased spring constraint | Value |
|---|---:|
| free length | 10.00±0.30 |
| outside diameter | 4.00±0.10 |
| wire diameter | 0.35±0.03 |
| minimum inside diameter | 3.18 |
| active/total coil guidance | 11–13 / 13–15 |
| measured rate | 0.25–0.30 N/mm |
| measured solid height | ≤6.50 |
| material | stainless spring wire or music wire |

Catalog dimensions do not replace rate and solid-height measurement on three
production samples. The D1.80 guide leaves ≥0.69 radial clearance at minimum
ID; the D4.20 seat leaves ≥0.05 radial clearance at maximum OD. At nominal
free length and 2.75 maximum service compression, spring length is 7.25. At
the minimum allowed 9.70 free length it is 6.95 and still retains ≥0.45
solid-height margin over the allowed 6.50 maximum.

Each role adjuster is one M3×12 cup-point socket set screw, one M3 heat-set
insert OD4.20×4.00 and one D4.00×0.50 stainless spring-seat washer. The insert
boss, K1 through-bore and K2 installation access are normative. Measured
full-thread engagement is 3.00 minimum throughout the 2.00 adjustment travel.
The screw position is mechanically limited to 0.00–2.00 from its setup datum;
nominal is 1.00. At either stop, ≥2.00 screw length remains behind the insert and
the tip stays captured in the D4 washer pocket. A D4.00×20.00 radial tool
cylinder reaches the 1.5-mm hex socket from the clock interior without crossing
a ring, motor, adjacent spring lane or stationary joint.

### I8. Mandatory Revision K tests

1. `fixed_axle_seat_retention_and_datum`: both towers, every discrete shim
   index and all critical poses prove I1 bore fits, blind stop, two bearing
   spans, actual-face equation `19.90…20.00 - 19.85 = 0.05…0.15`,
   0.80…0.90 axle extension, retention and tool path.
2. `cassette_pin_fit_stop_and_retention`: all three cassettes and ladder bores
   prove pin clearance, 4.25 insertion, 1.50 bottom wall, set-screw flat/thread
   engagement, K3 flat location/orientation, M2 internal thread, measured
   washer/screw references, both annular overlaps, axial stack and
   non-destructive service path.
3. `spine_stop_plate_complete_interfaces`: actual solids prove spine envelope,
   receiver walls, every fastener stack, three windows, powered/service stops,
   reversal collision, correct key fit and all driver cylinders.
4. `authoritative_assembly_state_machine`: generate and validate every I4 step
   and reverse-service state; no C8/eccentric/common-q state may be active.
5. `authoritative_production_manifest_94`: exact names/counts total 94, zero
   obsolete objects, and source/all-state STEP/3MF occurrence parity.
6. `complete_station_coupon_and_ladders`: source-crop equality, 18-cell 300°
   ladder, nine fixed shim-pair assemblies plus three fixed bore cells, bounds,
   bed margins, non-printing refs and slicer reload all pass.
7. `purchased_spring_adjuster_envelope`: measured spring samples and all three
   adjuster stacks satisfy I7 rate, ID/OD/wire/solid-height, capture, travel,
   insert engagement, K1 through-bore/ligaments/screw path and adjustment-tool
   gates.
8. `single_adjuster_insert_installation_stage`: the generated assembly state
   machine contains exactly one heat-install event for each of the three
   adjuster inserts, all at step 2 on the bare spine; actual solids prove all
   three K2 D7×25 heat-tool cylinders at that state and no duplicate event.

Revision K changes no accepted Revision H optical, balance, Hall, gear, ring,
force, displacement, uncertainty-shell or fixed discrete-index mathematics.

## Revision H normative amendments

### H1. Smallest honest remedy: three local cassettes in one 300° tower

The 60° and 180° towers remain one structural tower and one common D4 axle per
station carrying H/M/S rollers. The 300° station remains one structural tower
spine, but the impossible common roller axle is replaced by three independent
radial roller cassettes, one each for H, M and S. This is the only added motion;
there are no role-local adjustments at the fixed towers and no fourth tower.

The role-local variables are:

```text
q_H, q_M, q_S = powered radial displacement of each 300° roller cassette
|q_r| <= 0.76 acceptance bound
powered mechanical window = [-1.00,+1.00]
service hard stops = [-1.25,+1.25]
minimum powered travel margin = 1.00-|q_r| >= 0.24
```

Each cassette uses the already accepted D3 guide interface: two D3.00 shoulder
screws at tangent ±5.00 through 3.40×5.50 radial capsules. This gives exactly
±1.25 pin-contact hard-stop travel. One removable three-window stop plate on
the common spine has three independent 3.20×5.00 capsules around D3.00 stop
pins, giving exactly ±1.00 powered travel for each cassette. Removing that one
plate exposes the existing red `SERVICE / DO NOT POWER` field and unlocks all
three ±1.25 service ranges. The plate is retained by two M3×8 screws and cannot
be installed reversed.

The single structural spine fixes the three role Z datums. Each cassette axle
is a separate polished D3.99 pin and its roller running band is centred on the
existing frozen role band: Hour -2.10…-0.10, Minute 4.60…6.60, Second
11.30…13.30. The existing POM roller OD, flange geometry, 0.15 axial clearance
per side, role spacers and flange-overlap gates are unchanged. Splitting the
axle may not move a role's axial plane or introduce an extra ring guide.

The local axle stack, wall side to viewer side, is the existing lower capture
collar, 0.15 running clearance, 0.50 lower roller flange, 2.00 running band,
0.50 upper flange, 0.15 running clearance and existing upper capture collar.
The short D3.99 pin is cut from the accepted axle stock to leave 1.00–2.00
beyond the purchased upper collar. Axle-stock, collar and spacer fit ladders
remain mandatory; only the one long common 300° axle becomes three short pins.

### H2. Role-local spring stack and force equations

Each cassette has its own purchased metal compression spring; PETG is not the
preload source. The three stacks are identical and independently adjustable:

| Role-local compliance variable | Frozen value |
|---|---:|
| spring quantity | 3 total, one per role |
| spring OD / free length | 4.00 / 10.00 |
| maximum spring solid height | 6.50 |
| spring-rate accepted range `k_r` | 0.25–0.30 N/mm |
| nominal compression `c0_r` | 1.50 |
| powered compression at `q_r=±0.76` | 0.74–2.26 |
| service-stop compression at `q_r=±1.25` | 0.25–2.75 |
| fixed/slider spring seats | D4.20×1.50 deep |
| spring guide pin | D1.80×4.50 |
| seat retention lip | 0.60 minimum |
| preload adjuster | 3 × M3×12 set screw with captive M3 nut |

Positive `q_r` is defined as motion that increases spring compression:

```text
c_r(q_r) = 1.50 + q_r
F_r(q_r) = k_r*c_r(q_r)
F_total = F_H + F_M + F_S
```

Across the powered acceptance range, every contact remains positively loaded:

```text
F_r,min = 0.25*(1.50-0.76) = 0.185 N
F_r,max = 0.30*(1.50+0.76) = 0.678 N
F_total guaranteed envelope = 0.555–2.034 N
```

The inherited outer acceptance `0.20<=F_total<=2.10 N` remains active, and in
addition each `F_r` must remain 0.185–0.678 N. Spring/guide-pin capture is
proved through the complete ±1.25 service travel, where compression remains
positive; at maximum compression the spring length is `10.00-2.75=7.25`, at
least 0.75 above maximum solid height. Spring axes are at the three running-band
centres Z=-1.10, 5.60 and 12.30. Adjacent separation is 6.70, so two D4.00
spring envelopes retain 2.70 axial clearance. One role may not borrow preload
or displacement from another.

### H3. Contact solve under all 4096 independent shells

The measured errors and 4096-shell sign order remain exactly as Revision G.
For each role independently, the two common fixed tower locations solve that
role's XY ring centre; its local 300° cassette then solves `q_r`:

```text
delta[r,t] = d[r,t] + R_run - R_race[r,t]
|delta[r,60]| <= 0.05
|delta[r,180]| <= 0.05
|delta[r,300]| <= 0.05
F_r = k_r*(1.50+q_r)
```

One shell is accepted only when all three role solves simultaneously satisfy
`|q_r|<=0.76`, travel margin ≥0.24, each positive force, total force, and
per-role flange overlap ≥1.05 using the same locked `A_60,A_180`. The original
~0.751505 worst scalar result remains a regression target for each role-local
solver. The implementation must still compute and report the actual worst
role, shell and exact displacement over all 4096 cases; it may not infer H/M/S
success from one role.

This physically realizes every opposed residual corner admitted by Revision
G: H, M and S can occupy different `q_r` values while sharing the same tower
spine. No uncertainty shell is excluded or correlated by assertion.

### H4. Discrete fixed-tower setup and complete clamp stack

The available fixed-tower setup indices are exactly:

```text
S_A = {-1.00,-0.75,-0.50,-0.25,0.00,+0.25,+0.50,+0.75,+1.00}
```

For each fixed tower, matched-ring acceptance now requires both
`spread_t<=0.50` and `I_t intersect S_A` nonempty. Choose the single common
`A_t` only from that discrete intersection. A continuous point in `I_t` that
contains no member of `S_A` is not manufacturable and rejects/rematches the
ring set.

For example, a continuous intersection `[+0.10,+0.20]` passes the older
nonempty-interval rule but contains no discrete setup index and must now fail.
The executable test includes this witness plus both accepted endpoint indices.

The paired shim geometry remains `t_in=1.50+A_t`,
`t_out=1.50-A_t`, total 3.00 and individual thickness 0.50–2.50. Exactly two
indexed, keyed and retained shims are installed at each fixed tower: four
production shims total. The -4…+4 witness index on both shims, tower leaf and
stationary cheek must match. Both 0.60 retaining lips engage before tightening.

Each fixed tower has two identical clamp stacks at tangent ±7.00:

```text
M3x8 socket-head screw
-> D7.00x1.00 stainless washer
-> 3.00 tower leaf with 3.40x5.00 radial capsule
-> 4.00-long M3 heat-set insert in stationary carrier
```

The under-head stack is `1.00+3.00+4.00=8.00`, giving 4.00 insert engagement
and zero nominal protrusion. Each insert has 1.00 closed-end carrier wall.
All four clamps are inserted from the viewer side. Each has an unobstructed
D6.50 driver cylinder from Z=30.00 to its socket at every setup index, and the
D7 washer must overlap the complete slot by ≥1.00 tangentially/radially. The
old active eccentric bushings, eccentric locks and their lock screws are
removed from the R2 assembly, BOM, print manifest and all-state exports.

### H5. Assembly and production-manifest changes — superseded by I4/I5

The active 300° station assembly order is:

1. Fasten the one structural tower spine to the stationary carrier.
2. Install the H, M and S springs, guide pins and preload adjusters in their
   labelled spine lanes.
3. Install three labelled slider cassettes with six D3 shoulder guide screws.
4. Install one short D3.99 axle, one POM roller and the unchanged axial
   spacer/collar stack in each cassette at its derived role Z plane.
5. Install the common three-window powered stop plate and its two M3×8 screws;
   verify each role contacts ±1.00 and cannot reach ±1.01.
6. Set each nominal spring compression to 1.50, then verify individual and
   total preload before powering any motor.

Relative to the prior active manifest, remove two printed eccentric-bushing
sets and their four eccentric bushings; replace the one compliant carriage by
three labelled role cassettes; replace one compliant spring/axle stack by three
springs and three short axle stacks; and add one three-window stop plate. The
one compliant base becomes the one structural tower spine. Purchased POM
roller count remains unchanged.

### H6. Production-derived fixed-tower coupon and fit ladder — superseded by I6

The fixed-tower coupon is a canonical source crop of one complete fixed tower,
including stationary cheeks, tower leaf, both capsules, both insert bosses,
retaining lips, witness windows and driver keep-out cylinders. Coupon geometry
may add only outer crop stops; it may not redraw these interfaces.

Its fit-ladder plate contains all nine keyed shim pairs (18 separate shims),
labelled -4…+4, plus two M3×8 screws, two D7×1 washers and two production insert
reference solids. For each index the test assembles the source-derived coupon
with that exact pair and proves: expected `A_t`, 3.00 total shim stack, each
shim 0.50–2.50, both bearing faces, both 0.60 lips, matching witnesses, full
washer support, 4.00 insert engagement, zero protrusion and clear D6.50 driver
access. The -4 and +4 endpoint assemblies are mandatory exported coupon states.

The production 3MF contains only the four selected fixed-tower shims for the
measured accepted ring set. The fit-ladder 3MF contains the 18 labelled ladder
shims and one source-derived coupon station. Mixing ladder shims into the
production object manifest or omitting a selected production pair fails parity.

### H7. Mandatory Revision H tests

1. `role_local_compliant_solves_4096`: run all 4096 Revision G shells at every
   critical pose and solve `q_H,q_M,q_S` independently on one tower spine;
   prove all contact, travel, force and overlap gates and report the exact worst.
2. `three_window_powered_and_service_stops`: actual-solid contact at ±1.00 and
   ±1.25 for all three cassettes; ±1.01 and ±1.26 are impossible in the
   corresponding assembled states.
3. `three_spring_capture_and_force`: sweep each cassette across service travel,
   prove spring/guide capture, then prove powered individual force
   0.185–0.678 N and total force 0.555–2.034 N.
4. `discrete_fixed_setup_intersection`: require a member of `S_A` in each
   measured `I_60,I_180`; reject continuous-only or empty intersections and
   prove every role residual is within ±0.25 at the chosen common indices.
5. `fixed_clamp_stack_and_access`: all 18 fixed-tower index/station combinations
   prove the complete M3×8 stack, lips, witnesses, insert wall and driver paths.
6. `fixed_setup_coupon_source_parity`: canonical crop digest and actual-solid
   equality hold for the coupon, nine shim pairs and both endpoint exports.
7. `active_manifest_has_no_eccentrics`: production source, all-state STEP, BOM
   and 3MF contain zero eccentric bushings/locks and exact new H5/H6 counts.

Revision H changes no optical, counterweight, Hall, balance-cap, stationary
quadrant, ring-seam, motor-yoke, gear-mesh or all-occurrence parity clause.

## Revision G normative amendment — enumeration retained; common q superseded by H

### G1. Full independent role×tower residual proof — use H role-local q

Revision F defines nine independently bounded post-calibration residuals,
one for every role×tower pair. Therefore three shared radial signs do not
enclose the accepted tolerance space. R2 uses the direct corner proof; it does
not introduce a correlated-error shortcut.

For each named critical pose, enumerate the complete radial sign vector:

```text
sigma[r,t] in {-1,+1}
r in {H,M,S}
t in {60,180,300}
e[r,t] = 0.25*sigma[r,t]
radial corners = 2^(3 roles * 3 towers) = 2^9 = 512
```

For every radial corner, enumerate the complete role axial sign vector:

```text
zeta[r] in {-1,+1}
z[r] = 0.75*zeta[r]
axial corners = 2^3 = 8
total shells per critical pose = 512*8 = 4096
```

Each shell uses the already locked common `A_60` and `A_180`, one shared axle
transform at each tower, and one exact common compliant solution `q_300` for
H/M/S. It is forbidden to select role-specific tower positions or three
different compliant displacements. The solver must simultaneously evaluate
all nine residual values, all three axial values, all three role centres, all
contact residuals, each flange overlap and the summed spring reaction.

The corner set exactly includes the allowed matched-set extrema:

```text
max_r(e[r,t]) - min_r(e[r,t]) <= (+0.25)-(-0.25) = 0.50
max for each role of |sum_t e[r,t]| = 3*0.25 = 0.75
```

Thus the 512 radial corners include same-sign, opposed-role and opposed-tower
cases that Revision F's eight shared-datum corners omitted. The existing
matched-ring interval acceptance remains the prerequisite for entering this
proof.

At every one of the 4096 shells, the exact solver must prove one simultaneous
solution with:

- common `|q_300|<=0.76` and remaining ±1.00 travel margin ≥0.24;
- fixed-contact residual within ±0.05 for every role/contact;
- common total spring force/preload 0.20–2.10 N;
- flange overlap ≥1.05 for H, M and S;
- no role-specific tower transform, setup value or compliant displacement.

The earlier ~0.751505 result remains a regression value for its original
three-correlated-sign subset only; it is not the asserted maximum of the new
independent 4096-shell space. The implementation must compute and report the
actual worst shell, exact `q_300`, travel margin, total force, residual and
overlap across all 4096 cases. R2 passes only if that computed maximum remains
within 0.76 and every other gate above passes. Any infeasible shell rejects
the measured ring set or the implementation; it may not be deleted or mapped
onto a correlated sign case.

### G2. Corrected executable test

Revision F test 6 is replaced by:

`exact_common_equilibrium_4096_shells`: at every named critical pose, generate
all nine named residual signs in deterministic order
`H60,H180,H300,M60,M180,M300,S60,S180,S300`, cross them with axial signs
`H,M,S`, assert 512 unique radial corners, eight unique axial corners and 4096
unique combined shells, then run the simultaneous common-setting acceptance
checks from G1. The report records the worst passing shell and every failing
shell without deduplication.

The design-level enumeration result is exactly `2^9*2^3=4096` shells per
critical pose. This arithmetic result is frozen; equilibrium pass/fail and its
actual worst displacement remain implementation outputs because no CAD/contact
solver is changed by this design-only revision.

## Revision F normative amendments — common 300° axle/q superseded by H

### F1. Every tower position and axle is common to all three roles

Each station is one physical tower with one common axle carrying the H, M and
S rollers. It is forbidden to solve or export separate tower positions for
the three roles. The only setup variables at the fixed towers are the common
`A_60` and `A_180`; the only operational radial variable at the compliant
tower is one common displacement `q_300`. These settings apply simultaneously
to H, M and S.

Measured raw radial error is indexed by role and tower:

```text
r in {H, M, S}
t in {60, 180, 300}
E[r,t] = measured ring mean-radius/local-race error at role r, tower t
```

For each tower, the three rings are an acceptable matched set only if:

```text
spread_t = max_r(E[r,t]) - min_r(E[r,t]) <= 0.50
I_t = intersection over r of [E[r,t]-0.25, E[r,t]+0.25]
I_t is nonempty
```

The setup datum has the same sign as measured error; the physical tower shift
is `-A_t`. At each fixed tower, choose one common value:

```text
A_t in I_t intersect [-1.00,+1.00], t in {60,180}
e[r,t] = E[r,t] - A_t
|e[r,t]| <= 0.25 for every role on that shared axle
```

The raw absolute acceptance remains `|E[r,t]|<=0.85`. Therefore any accepted
matched set has a setup intersection inside the frozen ±1.00 range. If either
the ±0.85 raw bound, the 0.50 role spread or the common setup intersection
fails, the complete H/M/S ring set is rejected or rematched; an implementation
may not tune one roller on the common axle independently.

At the 300° compliant tower, the exact solver uses the same measured
`E[r,300]` set and must find one `q_300` that simultaneously satisfies all
three roles' contact, force and flange constraints. Each role may retain its
own solved ring XY centre, but the tower axle position and `q_300` are common.
The spring reaction is the sum over all three roller contacts:

```text
F_total(q_300) = F_H(q_300) + F_M(q_300) + F_S(q_300)
0.20 <= F_total <= 2.10 N
```

The minimum total installed preload is 0.20 N; it is not 0.20 N per roller.
The exact solver must report `F_H`, `F_M`, `F_S`, `F_total`, common `q_300`,
each role centre, contact residual and flange overlap. A matched set that
passes the 0.50 spread screen but has no common compliant solution is rejected.

### F2. Common-setting finite proof — shell count superseded by G1

Post-calibration residual uncertainty is indexed by role and tower,
`e[r,t]`, and bounded by ±0.25. The proof must not independently choose a
tower adjustment or compliant displacement for each role. For every named
critical pose it uses one physical tuple `(A_60,A_180,q_300)` and evaluates:

- all eight radial corner sign patterns over the three shared tower datums;
- all eight H/M/S axial sign patterns at
  `±(0.60 warp+0.15 roller float)=±0.75`;
- all nine measured role×tower residual intervals against those same common
  physical settings.

This is exactly `2^3*2^3=64` physical shells per critical pose, not 64 shells
per role. An executable interval proof may replace explicit corner evaluation
only if it encloses every corner and returns the same common physical settings.
No free ring-set XY input or role-specific tower adjustment is permitted.

For 120° tower spacing, the exact conservative common compliant displacement
is approximately 0.751505 mm at the worst accepted corner. The frozen bound is:

```text
q_worst_exact ~= 0.751505
exact remaining margin ~= 1.00 - 0.751505 = 0.248495
|q_300| <= 0.76
remaining travel margin = 1.00 - |q_300| >= 0.24
```

The rounded 0.75 value from Revision E is superseded. Exact evaluation must
use unrounded values and prove both `|q_300|<=0.76` and margin ≥0.24 at all 64
shells, together with fixed-contact residual ±0.05, total force 0.20–2.10 N
and flange overlap ≥1.05 for every role.

### F3. Always-solid paired setup shims

The fixed-tower shim cassette preserves a constant 3.00 total bearing stack:

```text
t_in  = 1.50 + A_t
t_out = 1.50 - A_t
t_in + t_out = 3.00
A_t in [-1.00,+1.00]
0.50 <= t_in,t_out <= 2.50
```

Both shims therefore remain physical, load-bearing and captured even at either
setup endpoint. The nine 0.25-indexed settings, paired witness index, 0.60
retaining lips and two M3 clamp screws remain as frozen in Revision E. Any
zero-thickness, absent, one-sided or mismatched shim pair fails production
assembly and all-state STEP parity.

### F4. Mandatory Revision F tests

1. `shared_axle_coupling`: actual solids and pose data prove one axle/tower
   transform serves H/M/S at each of 60°, 180° and 300°, with no role-specific
   tower transform or hidden adjustment.
2. `matched_ring_interval_overlap`: for measured `E[r,t]`, prove raw ±0.85,
   role spread ≤0.50 and nonempty `I_t`; reject/rematch the complete ring set
   if any tower fails.
3. `common_fixed_tower_settings`: choose one `A_60` and one `A_180` from their
   intersections and ±1.00 range, then prove all six fixed-tower residuals are
   within ±0.25 using those same two values.
4. `common_compliant_setting_and_total_force`: solve one `q_300` for all three
   roles, prove the three contacts simultaneously, and prove summed preload/
   spring force `F_total` is 0.20–2.10 N.
5. `paired_shim_solidity`: enumerate all nine setup indices at both fixed
   towers and prove each shim is 0.50–2.50 thick, the pair totals 3.00, both
   bearing faces engage and both retaining lips capture actual solids.
6. `exact_common_equilibrium_64_shells`: at every named critical pose, prove
   all 64 common-setting shells with exact unrounded arithmetic,
   `|q_300|<=0.76`, travel margin ≥0.24, fixed residual ±0.05, total force and
   per-role flange overlap. Record the worst shell and its ~0.751505 result.

Revision F changes no optical, counterweight, cap, fastener, parity, service,
print-manifest or assembly requirement accepted in Revision D.

## Revision E normative amendment — partially superseded by Revision F

### E1. Two-stage setup calibration and operating tolerance shell

Revision D section D2 is infeasible because it applies the complete raw
manufacturing error directly to two towers that are described as fixed during
operation. R2 instead separates one-time assembly calibration from the locked
operating tolerance proof.

#### Stage 1 — raw-error setup calibration

Before either fixed tower is locked, its raw ring mean-radius plus tower-seat
error may be anywhere in the interval:

```text
E_raw_i = E_ring_mean_i + E_seat_i
|E_raw_i| <= 0.75 + 0.10 = 0.85, i in {60°, 180°}
```

The nominally fixed towers at 60° and 180° each have an independent radial
setup adjustment `A_i` of at least -1.00 to +1.00. Adjustment exists only for
assembly and calibration; it is not an operational degree of freedom. The
setup range exceeds the complete raw bound by `1.00-0.85=0.15` at both ends.

Each fixed-tower foot uses a radial 3.40×5.00 capsule around each of two D3.00
clamp screws. The resulting screw-centre travel is `5.00-3.00=2.00`, exactly
±1.00 about nominal. The two screws are separated tangentially by 14.00 and
clamp a 3.00-thick tower leaf to the stationary carrier.

The frozen setup locator is a paired inboard/outboard shim cassette captured
between parallel stationary cheeks. Its measured shim pair always totals 2.00
and selects `A_i` at 0.25 increments from -1.00 through +1.00:

```text
t_in  = 1.00 + A_i
t_out = 1.00 - A_i
t_in + t_out = 2.00
```

There are nine keyed shim-pair settings per fixed tower. Each pair carries its
offset index (-4 through +4); matching index windows in the stationary cheek
and tower leaf are the setup witness geometry. At the selected setup, both
shim faces bear against their cheeks, both M3 clamps are tightened, and a
0.60-deep retaining lip captures each shim from the wall side. The bearing
shim faces, retaining lips and two-screw clamp are the frozen lock geometry;
no spring, loose unindexed shim, eccentric motion or free radial slide remains
in service.

The setup solver chooses the nearest indexed compensation
`A_i=quantize_0.25(-E_raw_i)` in the closed ±1.00 range. For any raw value
within ±0.85, the selected 0.25 increment leaves at most 0.125 uncompensated
error, below the frozen ±0.25 post-calibration limit. A setup test applies raw
endpoints -0.85 and +0.85 independently to
both towers and proves a valid indexed adjustment exists without exceeding
either ±1.00 setup stop. The test reports chosen adjustment, ≥0.15 raw-range
capacity margin, post-calibration residual and locked witness index. A raw
error outside ±0.85 or adjustment demand outside ±1.00 is a setup failure, not
an operating shell.

#### Stage 2 — locked operating shell

Once calibrated and locked, the two fixed towers are rigid operational
contacts. The only independent radial perturbation is residual local race
error at each of the three tower contact angles:

```text
E_residual_i in {-0.25, +0.25}, i in {60°, 180°, 300°}
```

No free XY offset, setup-adjustment motion or second seat-error term is added
to an operating pose. For every named critical pose, the solver enumerates all
`2^3=8` residual radial signs and all `2^3=8` role axial signs at
`±(0.60 warp+0.15 roller float)=±0.75`, exactly 64 shells.

For contacts separated by 120°, the frozen conservative compliant-equilibrium
bound is:

```text
|E_residual_60 + E_residual_180 + E_residual_300|
    <= 3*0.25
    = 0.75
```

This is inside the compliant tower's frozen ±1.00 operational travel with
`1.00-0.75=0.25` minimum travel margin. At all 64 shells the exact contact
solver must return finite ring centres, fixed-contact residuals within ±0.05,
compliant displacement within ±0.75, compliant travel margin ≥0.25, force
0.20–2.10 N and flange overlap ≥1.05. Any shell that cannot reach equilibrium
fails R2.

#### Mandatory Revision E tests

1. `raw_setup_calibration_range`: independently enumerate both raw fixed-tower
   endpoints, prove `A_60,A_180` stay inside ±1.00 and retain ≥0.15 margin.
2. `post_calibration_residual_bound`: derive measured post-lock residuals and
   reject any fixed or compliant contact with `|E_residual_i|>0.25`.
3. `fixed_tower_setup_lock`: actual solids prove ±1.00 setup travel while loose,
   paired-shim bearing/capture and two-screw clamp seating at every selected
   witness index, then zero radial operational freedom in the locked assembly.
4. `compliant_equilibrium_64_shells`: at every named critical pose, enumerate
   all 64 residual-radial/axial shells and prove the equilibrium, contact,
   force, flange-overlap and ≥0.25 compliant-travel-margin requirements above.

The implementation report must keep Stage 1 setup cases separate from Stage 2
operating shells. Passing a raw setup case does not count as one of the 64
operating shells, and an unlocked fixed tower is forbidden in every production
assembly occurrence and all-state STEP.

## Revision D normative amendments

### D1. Capsule travel is derived from the actual pin diameter

The compliant guide capsule is 3.40 wide ×5.50 overall around a D3.00 shoulder.
The allowed shoulder-centre travel is `5.50-3.00=2.50`, exactly ±1.25 about
nominal. The 0.40 width difference gives 0.20 tangential running clearance per
side. Exact BREP accepts free poses through ±1.25 with end contact at ±1.25;
±1.26 is impossible and must produce positive-volume shoulder/stop contact.
Revision C's 5.90 slot is superseded.

The powered-window key capsule is 3.20 wide ×3.45 overall around its D3.00 pin.
Pin-centre travel is `3.45-3.00=0.45`. Centred at q=-0.125, its endpoints are
`-0.125±0.225`, exactly q=-0.35 and +0.10. Exact solids are free inside the
window, contact both endpoint stops, and are impossible at -0.36/+0.11.
Revision C's 3.65 overall window is superseded.

### D2. Conservative finite tolerance shell — superseded by E1

R2 uses one combined net contact-datum radial error per tower:

```text
E_tower = race_profile_error + tower_seat_error
|E_tower| <= 0.75 + 0.10 = 0.85
```

No independent free ring-centre offset exists. At each named critical pose,
the equilibrium solver enumerates all `2^3=8` radial tower sign combinations
at ±0.85 and all `2^3=8` role axial signs at
`±(0.60 warp+0.15 roller float)=±0.75`, for exactly 64 adversarial shells.
This shell conservatively contains every same-direction sum of the frozen
race and seat tolerances. The canonical pose returns the solved ring centres,
compliant displacement, contact residuals and forces or fails if no finite
equilibrium satisfies fixed residual ±0.05, compliant travel ±1.00, force
0.20–2.10 N and flange overlap ≥1.05.

### D3. Optical acceptance is deferred

The provisional cone in Revision C is removed from mandatory R2 acceptance.
R2 makes no halo, shadow, occlusion or optical-clearance claim. The next
optical ADR must freeze:

- mechanical-to-optical rigid transform `T_mech_to_optical`;
- wall plane and wall normal;
- LED point/source-area position and emission full angle;
- mask and fin optical surfaces;
- target halo diameter range 500–1000.

For source-to-wall distance `L`, a provisional cone relation is
`D_halo=2*L*tan(alpha_half)` and
`alpha_half=atan(D_halo/(2*L))`. Perspective projection of a blocker uses
`M=(source_to_wall)/(source_to_blocker)`. These equations are ADR inputs only,
not R2 mechanical pass/fail gates. Hall keep-outs remain mechanical solids.

### D4. Counterweight containment

Each balance pocket is D4.10×3.40 from the wall side. Its wall-to-viewer stack
is a 0.40 inward PETG cap, a D4×3.00 304-stainless slug, then 1.00 continuous
viewer-side PETG wall: `0.40+3.00+1.00=4.40` carrier thickness. The cap is a
D4.08×0.40 disk with two 0.15 radial retention nubs engaging a D4.30×0.20
annular pocket-mouth groove. Nine separate balance caps exist, three per role.

BREP tests prove every cap and slug is fully contained by its host carrier,
has zero intersection with race, teeth, seams, Hall pocket and non-host ring,
retains ≥1.00 viewer wall, and cannot translate out through the mouth without
crossing the retention groove. COM includes all caps, selected slugs and empty
pockets.

### D5. All-production-occurrence parity

Every production occurrence in every all-state STEP must be valid and match
its canonical source occurrence by name, transform, face count and canonical
BREP digest. Relative volume error is
`abs(V_step-V_source)/max(V_source,1e-9) <= 1e-5`; bounds remain within 0.02.
This applies transitively to stationary hardware, references, keep-out solids,
caps and fasteners, not only primary printed bodies. All 1040 motion poses stay
in memory; only the named critical states from Revision C are exported.

### D6. Stationary joint screw convention

Rear and front stationary joints use M3×7 90° flat-head screws, where 7.00 is
total under-head length. Each passes through a 3.00 clearance leaf and engages
exactly 4.00 in the receiving heat-set insert: `7.00-3.00=4.00`; nominal
protrusion is 0.00. Rear screws insert from the wall side and front screws from
the viewer side. Actual-solid tests measure length, countersink seating,
engagement, closed-end wall, protrusion and driver path. Revision C's M3×8
stationary-joint screw is superseded.

### D7. Hall caps and production 3MF counts

Each D4.10 Hall magnet pocket is 2.50 deep from the wall side and contains a
D4×2 magnet plus one D4.08×0.40 PETG Hall cap and 0.10 seating allowance. The
cap uses the same two 0.15 retention nubs and D4.30×0.20 mouth groove as the
balance cap. Remaining viewer wall is `4.40-2.50=1.90`. Three separate Hall
caps exist, one per role. Tests prove containment, retention, host-pair air-gap
semantics and non-host clearance.

Production 3MF contains exactly nine balance caps and three Hall caps. It
contains zero production roller spools because rollers are purchased POM.
Assembly steps 5 and 6 install each Hall magnet and Hall cap before checking
that role's balance, then install zero to three steel slugs and all three
balance caps. Missing, duplicate or unretained caps fail the object manifest
and assembly-state parity.

## Revision C normative amendments

### C1. Compliant guide travel and spring capture

The compliant carriage uses two D3.00 shoulder screws. Each capsule guide slot
is 3.40 wide × 5.90 overall radial. Its end-centre travel is
`5.90-3.40=2.50`, providing exactly ±1.25 hard-stop travel. Diametral running
clearance is `3.40-3.00=0.40`, or 0.20 per side. Shoulder length is 5.10 for a
5.00 carriage, leaving 0.10 axial running clearance beneath the screw head.

Exact-BREP tests translate the complete carriage to -1.25, -1.00, 0, +1.00,
and +1.25. The shoulder/slot intersection is zero at legal poses; a ±0.01 move
beyond either hard stop produces positive-volume stop contact. At all five
poses the D6×12 spring intersects both D6.20×2.00 seats by at least 1.00 axial,
remains around its D2.80 guide pin, and cannot pass the 0.80 retention lips.

### C2. Solved-contact race model and finite adversarial shell

The only flange-overlap equation is the solved-contact equation. With running
radius `R_run=6.05`, flange radius `R_flange=7.15`, and contact residual
`delta=d+R_run-R_race`, overlap is:

```text
O = d + R_flange - R_race
  = R_flange - R_run + delta
```

Every accepted intended roller contact has `delta>=-0.05`; therefore
`O_min=7.15-6.05-0.05=1.05`. The older free-centre/profile-only 0.35 result is
superseded and must not appear in implementation assertions.

There is no free `ring_radial_offsets_xy_mm` input in the canonical pose.
Instead, each role is solved at each angle from:

- measured race profile samples `e(theta)` bounded ±0.75;
- fixed-tower seat error ±0.10 at 60° and 180°;
- compliant-tower seat error ±0.10 at 300°;
- two fixed tangent constraints with residual ±0.05;
- compliant spring equilibrium, 0.20–2.10 N, within ±1.00 running travel.

Adversarial enumeration includes all `2^3=8` tower-error sign combinations.
For axial checks, each role uses total displacement
`±(0.60 warp + 0.15 roller float)=±0.75`; all `2^3=8` role sign combinations
are tested. The 64 radial-error/axial-sign shells are applied to every named
critical pose. A pose fails if no finite equilibrium exists, fixed-contact
residual exceeds 0.05, compliant travel/force escapes its interval, or flange
overlap falls below 1.05.

The canonical pose API removes `ring_radial_offsets_xy_mm`; it returns solved
ring XY centres, compliant displacement, contact residuals, forces and axial
positions. `roller_axial_float_mm` remains explicit and bounded ±0.15.

### C3. Hall and provisional optical keep-outs

Generic Hall clearance applies only to non-host/non-intended pairs. A role's
own magnet and own Hall sensing envelope are an intended pair and are checked
for 1.50–3.00 air gap and trigger alignment, not 0.50 generic clearance. Every
magnet versus either non-host sensor envelope and every sensor envelope versus
non-host moving ring must maintain ≥0.50 through the 64 tolerance shells.

R2 freezes a provisional optical cone consistent with `optical_spec.py`:

| Variable | Value |
|---|---:|
| wall plane | Z=0.00 |
| point-source plane | Z=40.00 |
| clear full angle | 150.00° |
| clear half angle | 75.00° |
| cone radius | `(40-Z)*tan(75°)` for `0<=Z<=40` |
| wall radius | `40*tan(75°)=149.282` |

The cone is a validation solid. Fins and the intentional mask are named
optical blockers. Hall envelopes, wires, counterweights, joints, towers and
motor hardware are non-optical solids and may not intersect it unless a later
optical ADR explicitly accepts the resulting permanent shadow.

### C4. Canonical coupon crop and parity

Coupon production geometry is exactly:

```python
canonical_crop(full_pose, sector_tool)
```

for the selected role, tower variant and pose. Coupon-only motion stops are
unioned after the crop and excluded from equality. Equality compares the
canonical cropped production occurrences only: transitive dependency digest,
occurrence names, transforms, validity, volume within 1e-5, bounds within
0.02, face count, and canonicalized BREP digest must match the same subset of
the full pose. No coupon helper may redraw teeth, race, seam, yoke, roller,
Hall keep-out or fastener interfaces.

All 1040 motion poses per revolution are evaluated in memory. Only named
critical states are exported: assembled nominal, exploded, powered minimum,
powered maximum, service minimum/maximum `UNSAFE_TO_POWER`, each exact fin/
seam/station/tower/Hall alignment, and each tolerance-shell failure witness.

### C5. Non-overlapping rotating balance hardware

Counterweight is dense material inside the existing carrier cross-section,
not an axial or radial boss. Each role has three wall-side pockets centred at
R136.00, at the angle opposite its fin, with tangential offsets -6.00, 0,
+6.00. Each pocket is D4.10×3.10 and retains a removable D4×3 304-stainless
slug behind a 0.40 PETG snap cap; minimum remaining viewer-side wall is 0.90.
Pocket radial minimum is `136-4.10/2=133.95`, outside tooth root R132.50 and
race R131.60. Pockets are forbidden within 8.00 tangential of a seam receiver
or Hall magnet pocket; the opposite-fin angle may clock ±10° solely to satisfy
those keep-outs.

Material densities and rotating reference masses are frozen:

| Item | Density / mass |
|---|---:|
| solid PETG ring/fin/cap | 1.27 g/cm³ |
| 304 stainless slug | 8.00 g/cm³; 0.302 g each |
| M2×5 low-head screw | 0.22 g |
| captive M2 nut | 0.14 g |
| D2.90×6 dowel | 0.31 g |
| D4×2 NdFeB Hall magnet | 0.189 g |

Zero to three slugs are selected per role from actual solid mass properties.
The complete rotating role, including seam hardware, dowels, Hall magnet,
snap caps and selected slugs, must have XY COM eccentricity ≤0.50. Empty
pockets and caps are included in the calculation. No balance feature may
extend beyond the existing ring axial/radial envelope.

### C6. Complete stationary quadrant joint stacks

There are exactly 16 separate registration keys: two at each of four rear
joints and two at each of four front joints. Integral keys are prohibited in
Revision C.

Each rear joint uses two M3×8 90° flat-head screws inserted from the wall side
through D3.40 clearance leaves 3.00 thick into two M3 heat-set inserts, OD4.60
×4.00, in the receiving leaf. Each front joint is identical but screws insert
from the viewer side. Both sides use D6.00×1.70 countersinks; insert pockets are
D4.50 pilot with 4.20 heated depth and 1.00 closed-end wall. Engagement is
4.00; screw protrusion beyond the receiving leaf is 1.00 maximum. Driver paths
are D6.50 from the stated side and must clear the complete assembled clock
after removal of only its decorative cover.

Each joint's two separate keys remain 4.00 radial ×6.00 tangential ×2.50
axial with 0.20 per-side pocket clearance. Actual BREP tests verify sixteen
keys, sixteen pockets, sixteen M3 screws, sixteen inserts, correct side,
countersink support, engagement/protrusion and positive registration.

### C7. Powered-window key solid

Each motor station has one 20.00 radial ×10.00 tangential ×2.00-thick keyed
stop plate on the viewer side of the yoke-foot datum. The yoke carries a D3.00
stop pin. The plate window is a 3.20-wide capsule with end-centre travel 0.45
and overall radial length 3.65; this gives 0.10 running clearance per side.
The window centre datum is q=-0.125, so hard-stop centre coordinates are
q=-0.35 and q=+0.10 exactly.

An off-centre 4.00×3.00 anti-reversal tongue at tangential +3.50 mates only to
the matching chassis pocket. Two M3×8 screws and captive M3 inserts retain the
plate. With the plate installed, exact solids are free at q=-0.35 and +0.10
but have positive-volume pin/end contact at q=-0.36 and +0.11. Removing the
plate is the only mechanical path to ±2.50 service travel and exposes the red
`SERVICE / DO NOT POWER` field.

### C8. Revision C assembly and service order — wholly superseded by I4

1. Heat-install rear/front stationary-joint inserts; assemble four rear
   quadrants with eight keys and eight wall-side screws. Verify ≤0.10 joint
   steps and mount the rear chassis off the wall.
2. Install motor yokes loosely with back-side M3×10 clamps and captive
   viewer-side nyloc nuts; keep powered-window keys off.
3. Install fixed-tower bases, eccentric bushings and bare D4 axles. Install
   compliant base, guided carriage, spring, guide pin, adjuster and bare axle.
   Do not preload or install upper bridges yet.
4. Install the complete motor/miter/output-shaft cartridges, bearings and
   pinions. Set shaft endplay 0.05–0.15.
5. Install hour rollers. Assemble hour quadrants in place around flanges; add
   recessed plates, dowels, nuts, M2×5 screws, Hall reference magnet/cap and
   selected balance slugs/caps.
6. Add the first spacers; repeat for minute. Add second spacers; repeat for
   second.
7. Install all tower bridges with M2.5×8 fasteners and top collars. Confirm
   spring/roller capture before applying preload.
8. Clock and lock both fixed eccentric towers to residual ±0.05. Adjust the
   compliant spring to 1.00 compression and verify 0.80–1.20 N nominal force.
9. Assemble four front stationary quadrants with eight keys and eight
   viewer-side screws; install as one registered front structure.
10. With the clock off-wall and every ring installed, tune each q through the
    back-side clamps while hand-rotating its ring. Tighten clamps, then install
    all three powered-window keys and prove physical stops.
11. Verify three independent 360° rotations, equilibrium, axial capture, COM,
    mesh and tool access. Only then mount the clock to the wall.

Service begins by removing the clock from the wall. Remove decorative cover,
front stationary structure, powered-window keys only if service travel is
needed, tower bridges/collars, then second/minute/hour rings in that order.
Motor cartridges may be removed after the relevant ring clears. Rear joints,
fixed eccentric locks and compliant spring are serviced last. No destructive
snap, glue joint, or cutting is allowed.

### C9. Production rollers, ladders, and 3MF

Production rollers are purchased/machined POM, OD12.10 running land, OD14.30
flanges, D4.06 finished bore. Nine production rollers plus three spares belong
to the purchased BOM and are excluded from every production 3MF. Printed
low-friction rollers are prototype-only fit-ladder objects, visibly named
`PROTOTYPE_ONLY_NOT_FOR_CLOCK`, and never satisfy production endurance.

Revision C ladders add D2.90/D3.00/D3.10 dowel holes and
D7.90/D8.00/D8.10 eccentric-bushing seats. The backlash ladder is
0.10/0.18/0.25; an optional 0.08 cell is a deliberately tight fail-control and
is not a production candidate. Revision B's printed roller production count
is superseded: production 3MF object/instance assertions must contain zero
roller spools and retain the rest of the manifest.

## Revision B normative amendments

### B1. Moving-ring seam is recessed and replaceable

Each of the four seams in each moving ring uses a 2.00-thick underside splice
plate seated in a 2.10-deep recess. With the carrier underside as Z=0, the
plate occupies Z=0.10–2.10: its exposed underside is recessed 0.10 from flush.
The recess and plate radial range is R132.00–138.80; neither may enter the
R131.60 running race.

| Variable | Frozen value |
|---|---:|
| `seam_plate_radial_range` | 132.00–138.80 |
| `seam_plate_tangential_length` | 18.00 |
| `seam_plate_thickness` | 2.00 |
| `seam_recess_depth` | 2.10 |
| `seam_plate_below_flush` | 0.10 |
| `seam_fastener` | M2 × 5 low-head socket screw |
| `seam_fastener_head_height_max` | 1.50 |
| `seam_fastener_count` | 2 per seam |
| `seam_fastener_centres` | R135.40, tangent ±4.00 |
| `seam_clearance_hole_diameter` | 2.20 |
| `seam_captive_nut_af` | 4.10 |
| `seam_captive_nut_thickness` | 1.70 |
| `seam_registration_dowel/hole` | D2.90 / D3.00 |

The captive nut's two flats run radially. For a regular hex with AF=4.10,
point-to-point size is `4.10 / cos(30°) = 4.734`; the minimum tangential
ligament is `18/2 - 4.00 - 4.734/2 = 2.633`, exceeding 2.00. Radial ligament
around the radially oriented flats is
`min(135.40-4.10/2-132.00, 138.80-135.40-4.10/2) = 1.35`, exceeding 1.00.
The plate begins 0.40 outside the race and has zero positive-volume
intersection with the race cylinder. The M2×5 screw is accepted only if the
actual assembled STEP proves thread engagement ≥1.50 and protrusion beyond the
recessed underside ≤1.00; no nominal fastener label may substitute for this
measurement.

### B2. Stationary structure is four printable quadrants

The rear chassis/frame and front stationary ring each split into four 90°
quadrants with joints clocked at 45°, 135°, 225°, and 315°. Joints alternate
male/female so a quadrant cannot be installed flipped. Each joint has two
4.00-radial × 6.00-tangential × 2.50-axial positive-registration keys and two
M3×10 replaceable screws into captive M3 nyloc nuts; printed threads and
permanent glue are prohibited. Registration clearance is 0.20 per side.

Every stationary quadrant must have an actual oriented bounding box no larger
than 160.00 × 160.00 × 22.00 and therefore below the U1 260.00-mm conservative
XY print envelope. The four reassembled quadrants must reproduce the
continuous R150.00 datum with joint radial step ≤0.10 and joint axial step
≤0.10. Fastener and key solids remain outside all moving and optical keep-outs.

### B3. Installed-ring motor clamp orientation and mechanical unsafe-q stop

All four clamp screws per motor station install from the wall/back side. Each
has a 0.50 washer beneath its head, passes through the 2.50 chassis and 2.50
yoke foot, then engages a viewer-side captive anti-rotation M3 nyloc nut,
AF5.50 × 5.00 thick. The clock is removed from the wall for adjustment; the
three rings remain installed.

The frozen fastener is M3×10. Under-head stack before the nut is
`0.50+2.50+2.50=5.50`; calculated nut engagement is `10.00-5.50=4.50`, which
exceeds 3.00, and calculated protrusion is `max(0, 10.00-5.50-5.00)=0.00`,
below 1.00. CAD must measure these values from the actual screw/nut solids at
all slot positions. Back-side driver and viewer-side nut-tool cylinders must
stay clear with all rings installed.

A removable physical powered-window key is mandatory. With the keyed stop
plate installed, yoke travel is mechanically limited to q=-0.35…+0.10. Two
M3×8 screws retain the stop plate. Its asymmetric tongue is 4.00 × 3.00 and
cannot be installed reversed. Removing the plate with a 2.5-mm hex key unlocks
the ±2.50 service range and exposes a red recessed `SERVICE / DO NOT POWER`
witness field. Firmware validation remains secondary; service geometry cannot
be exported or powered without `operating_mode="service_unpowered"`.

The 10 N clamp-slip proof is a physical gate only. CAD gates are actual washer
support, nut capture, bearing/yoke clearance, ligament, slot, and complete tool
path checks.

### B4. Fixed eccentric towers and compliant tower

The 60° and 180° towers are fixed after setup. Each D4 axle is located by two
replaceable eccentric bushings:

| Fixed-tower variable | Frozen value |
|---|---:|
| bushing OD | 8.00 |
| bushing thickness | 4.00 |
| axle bore | 4.05 |
| eccentricity | 0.50 |
| setup authority | ±0.50 radial |
| lock screw | M3×8 socket, brass tip or polymer pad |
| lock-screw tool path | D6.00 clear cylinder |

Both bushings share an engraved index and are clocked together. After setup,
the running-axis target is R125.55±0.05. The lock screw acts on the bushing OD,
not the polished axle.

The 300° tower is a guided spring carriage:

| Compliant-tower variable | Frozen value |
|---|---:|
| carriage body | 18.00 radial × 16.00 tangential × 5.00 axial |
| guide screws | 2 × M3 shoulder screws, tangent ±5.00 |
| guide slots | 3.40 wide × 5.40 overall radial |
| usable radial travel | -1.00…+1.00 |
| hard-stop travel | -1.25…+1.25 |
| spring type | metal compression spring |
| spring OD / free length | 6.00 / 12.00 |
| spring rate | 0.80–1.20 N/mm |
| nominal compression | 1.00 |
| fixed/slider spring seats | D6.20 × 2.00 deep |
| spring guide pin | D2.80 × 6.00 |
| seat retention lip | 0.80 minimum |
| preload adjuster | M3×12 set screw with captive M3 nut |
| upper bridge fasteners | 2 × M2.5×8 into captive M2.5 nuts |
| bridge pilot | 1.00 deep, 0.20 per-side clearance |
| bridge/adjuster tool paths | D5.00 / D6.00 clear cylinders |

The spring and guide pin remain captured at both hard stops and during bridge
removal. At the nominal 1.00 compression the force is 0.80–1.20 N. Across the
±0.75 race-profile envelope it remains 0.20–2.10 N. PETG flexure is not the
preload source.

### B5. Race geometry uses profile error and equilibrium, not a free center

The roller running OD remains 12.10, so running radius is 6.05 and nominal
contact axis is `131.60-6.05=125.55`. Flange OD increases to 14.30, flange
radius 7.15. Nominal capture overlap is:

```text
O_nom = R_axis + R_flange - R_race
      = 125.55 + 7.15 - 131.60 = 1.10
```

The ring is not assigned an impossible arbitrary XY offset. Its measured race
is `R_i(theta)=131.60+e_i(theta)` with `|e_i(theta)|<=0.75`. At each pose, ring
center translation and compliant-carriage displacement are solved from two
fixed tangent contacts plus the third-tower spring equilibrium. For each
roller `j`, contact residual is
`delta_j = d_j + 6.05 - R_i(theta_j)`. Fixed contacts require
`|delta_j|<=0.05`; the compliant contact requires spring force within
0.20–2.10 N and carriage travel within ±1.00.

Worst flange overlap at maximum outward profile error is
`O_min=125.55+7.15-(131.60+0.75)=0.35`, exceeding the frozen 0.30 minimum.
Axial race warp remains `|w_i(theta)|<=0.60` and roller axial float is
`f_i in [-0.15,+0.15]`. The front stationary ring minimum Z becomes 16.85:
`15.60+0.60+0.15+0.50=16.85`.

Roller/race tangency and pinion/ring gear mesh are named intended-contact
pairs. They are excluded from generic noncontact clearance assertions but have
their own penetration, overlap, force, backlash, contact-ratio, and working-
depth assertions. No other waiver is permitted.

The authoritative pose API adds:

```python
roller_axial_float_mm=(f_hour, f_minute, f_second)
race_profile_error_functions=(e_hour, e_minute, e_second)
race_axial_warp_functions=(w_hour, w_minute, w_second)
```

### B6. Gear engagement and deterministic full-motion validation

Pressure angle is frozen at 20°. Pitch radii are 8.00 and 130.00; internal-
gear center distance is 122.00; base radii are 7.517541 and 122.160041; addendum
radii are 9.00 and 129.00. The theoretical transverse contact ratio is:

```text
epsilon = [sqrt(9^2-7.517541^2)
           - sqrt(129^2-122.160041^2)
           + 122*sin(20deg)] / [pi*1*cos(20deg)]
        = 1.770584
```

Actual BREP mesh must have contact ratio ≥1.20, tangential backlash at the
pitch circle 0.10–0.25, working depth ≥1.60, and zero unintended positive-
volume tooth interference for every role at q=-0.35, 0.00, +0.10. Ring-angle
backlash is `b_t/130*180/pi`; at the 0.25 maximum it is 0.1102°, below the
separate 0.50° physical fin-reversal gate.

One revolution is sampled at 1040 equal poses, four per ring tooth:
`delta_theta=360/1040=0.346153846°`. For each driven role, the other two roles
take all nine deterministic phase pairs from
`P={0, 0.6923076923, 1.3846153846}`. Thus each q value has
`3*9*1040=28,080` dynamic role poses. A broad-phase may reject distant pairs,
but every candidate pair is checked with exact BREP.

Additionally evaluate exact events for every fin, seam, motor station, fixed
tower, compliant tower, Hall keep-out and stationary joint alignment. Static
all-ring phase parity uses all 27 Cartesian H/M/S combinations in `P^3`.

### B7. Frozen fin solids and static balance

All fins are integral, opaque black PETG, density 1.27 g/cm³, modeled and
printed at 100% solid. No slicer infill assumption defines their mass.

| Role | Radial range | Tangential width | Z start–tip | Root radial range | Root Z |
|---|---:|---:|---:|---:|---:|
| Hour | 142.50–143.70 | 3.00 | 2.00–17.152 | 135.50–143.70 | 2.00–3.40 |
| Minute | 139.30–140.50 | 2.00 | 8.70–21.1867 | 135.50–140.50 | 8.70–10.10 |
| Second | 136.10–137.30 | 1.20 | 15.40–24.2514 | 136.10–137.30 | 15.40–16.80 |

Blade thickness is the listed radial width; blade outer edges have R0.30 and
root transitions R0.80. Each complete rotating role, including ring quadrants,
seam hardware, Hall magnet reference and counterweight, must have XY center of
mass eccentricity ≤0.50. Counterweight volume is a source-derived parameter at
the angle opposite the fin and R135.0–138.5; it is solved from actual solid
mass properties, not slicer infill.

### B8. Hall keep-outs exist in R2 now

R2 creates validation-only solids, not sensors, for one D4.10×2.10 magnet
pocket per ring at R136.00 and a three-height 12.00×8.00×4.00 sensor-module
envelope centred at 90°. The module envelope includes a 3.00 wire-bend zone and
1.00 connector-service shell. All moving/stationary mechanics keep ≥0.50 from
these solids across the complete equilibrium/runout model. Actual Hall parts
remain staged until mechanics passes, but later implementation may not claim
space that violates these keep-outs.

### B9. Coupon variants and crop identity

The API is frozen as:

```python
make_r2_sector_coupon(role, tower_variant="fixed" | "compliant", q_mm=0.0,
                      include_hall_keepout=True)
```

Both variants use the production motor station, 80° production ring crop,
production seam, and selected production tower. The oriented printed bounding
box, including hard stops, must be measured from each actual artifact and fit
within 205.00×190.00×60.00; no dimension may be reported from the arc alone.
Each coupon stores a crop digest over source dependency hashes, occurrence
names, transforms and local bounds. The digest must equal the corresponding
subset digest from the full assembly for the same role/state.

### B10. Print orientation, fit ladders, manifest, and U1 3MF gate — counts superseded by I5/I6

Production ring and stationary quadrants print flat with gear teeth upward;
seam plates and keys print broad-face down; yokes print wall-side foot down;
tower bridges and compliant carriage print on their largest flat face. Support
is prohibited on gear teeth, races, nut pockets, roller bores and registration
faces.

Before production parts, print source-derived ladders for: roller bore
4.00/4.06/4.12; M3 slot 3.50/3.60/3.70; M2 nut AF 4.00/4.10/4.20; M3 nyloc
pocket AF 5.40/5.50/5.60; D4 magnet pocket 4.00/4.10/4.20; stationary-joint
clearance 0.15/0.20/0.25; and gear backlash 0.08/0.10/0.12. Production values
change only through a documented revision after measuring these ladders.

The printable manifest is: 12 moving carrier quadrants, 12 moving seam plates,
4 rear stationary quadrants, 4 front stationary quadrants, 8 stationary-joint
registration keys, 3 motor yokes, 3 output pinions, 6 miter gears, 2 fixed
tower bars, 4 eccentric bushings, 1 compliant base, 1 compliant carriage,
3 tower bridges, 9 roller spools plus 3 spares, 6 spacers plus 2 spares,
3 powered-window keys, and the fit-ladder plate. Purchased fasteners, axles,
collars, springs, motors, bearings and electronics are BOM references, not
print objects.

The U1 project 3MF must contain every manifest object exactly once unless the
listed quantity is encoded as instances, use a 260×260×260 conservative build
volume, preserve per-object names/material/orientation, contain no out-of-bed
object, load in Orca/Snapmaker Orca without repair, and produce zero support on
the prohibited surfaces. Plate/object counts and source artifact SHA256 values
are asserted by tests.

### B11. Transitive source and all-state parity

The R2 manifest records SHA256 for every transitive Python source dependency,
not only the leaf generator. Assembled, exploded, powered-min, nominal,
powered-max, service-min, service-max, all 1040-sample critical snapshots,
Hall-keep-out and coupon states use one occurrence registry. Each exported
state must match source occurrence names, transforms and bounds within 0.02;
the only allowed differences are state transforms explicitly returned by the
pose API. Stale export timestamps or a mismatched dependency hash fail parity.

## 1. Frozen architecture

R2 preserves:

- 300.00 overall clock diameter;
- three independently rotating stacked carrier planes: hour, minute, second;
- 260-tooth internal ring gears;
- 16-tooth output pinions;
- module 1.00 positive gear drive;
- one independent motor station per ring at 0°, 120°, and 240°;
- three guide towers at 60°, 180°, and 300°;
- direct use of the carrier's smooth inner root land as the roller race;
- complete 360° rings assembled from four quadrants;
- no continuous T-rail, guide bead, TPU drive, belt, friction drive, quartz
  movement, or center shaft.

The rollback baseline must remain untouched at:

- `models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/`

R2 is a new source/export namespace. It must not overwrite that directory or
the current `p3_v3_direct_gear_race_guidance` outputs.

## 2. Frozen global variables and equations

| Variable | Value | Contract |
|---|---:|---|
| `clock_outer_diameter` | 300.00 | Absolute maximum stationary envelope |
| `ring_teeth` | 260 | Unchanged |
| `pinion_teeth` | 16 | Unchanged |
| `gear_module` | 1.00 | Unchanged |
| `gear_ratio` | 16.25 | `ring_teeth / pinion_teeth` |
| `ring_tooth_pitch_deg` | 1.3846153846° | `360 / ring_teeth` |
| `half_tooth_phase_deg` | 0.6923076923° | `ring_tooth_pitch_deg / 2` |
| `carrier_race_radius` | 131.60 | Smooth inner race datum |
| `tooth_tip_radius` | 129.00 | Moving tooth-tip sweep datum |
| `tooth_root_radius` | 132.50 | Moving tooth-root datum |
| `ring_body_outer_radius` | 138.90 | Unchanged carrier outer datum |
| `stationary_outer_radius` | 150.00 | `clock_outer_diameter / 2` |

For a ring pose `theta_ring_deg`, the output-pinion pose is:

```text
theta_pinion_deg = gear_ratio * theta_ring_deg + mesh_phase_offset_deg[role]
```

The implementation must use the existing positive-sign convention rather
than introducing a second sign convention in export or simulation code.

## 3. Authoritative pose API and unsafe-q interlock

All source assemblies, exported review poses, collision tests, and the sector
coupon must call one pose constructor with this logical signature:

```python
make_r2_pose(
    ring_angles_deg=(hour, minute, second),
    motor_q_mm=(q_hour, q_minute, q_second),
    roller_radial_offsets_mm=(fixed_60, fixed_180, compliant_300),
    ring_radial_offsets_xy_mm=((hx, hy), (mx, my), (sx, sy)),
    ring_axial_offsets_z_mm=(hz, mz, sz),
    operating_mode="powered" | "service_unpowered",
)
```

No exporter may place components by duplicating transforms outside this API.

### Motor adjustment `q`

The whole motor/yoke/miter/shaft/pinion cartridge translates rigidly along its
station radial unit vector:

```text
C_role(q) = C_role(0) + q * e_radial(role)
```

| Variable | Value |
|---|---:|
| `motor_q_physical_min` | -2.50 |
| `motor_q_physical_max` | +2.50 |
| `motor_q_powered_min` | -0.35 |
| `motor_q_powered_max` | +0.10 |
| `motor_q_nominal` | 0.00 |

Rules:

1. `operating_mode="powered"` must raise `ValueError` if any `q` is outside
   `[-0.35, +0.10]`.
2. `service_unpowered` may use `[-2.50, +2.50]`, but the assembly label must
   contain `UNSAFE_TO_POWER` when any `q` is outside the powered interval.
3. Generated firmware constants must clamp or reject unsafe `q`; they must not
   silently saturate to a valid value.
4. CAD acceptance retains the known tooth facts: at `q=+0.20` the mesh has no
   clearance reserve; at `q=+0.25` the present 260T/16T BREPs collide.

## 4. Installed-ring-accessible motor clamp

The current top access that requires removing the moving rings is rejected.
R2 uses wall-side/underside access for all four clamps at every station.

| Variable | Value |
|---|---:|
| `motor_mount_service_adjustment` | ±2.50 |
| `motor_mount_slot_width` | 3.60 |
| `motor_mount_slot_overall_length` | 8.60 |
| `motor_clamp_count_per_station` | 4 |
| `motor_clamp_screw` | M3 × 10 socket head |
| `motor_clamp_chassis_hole_diameter` | 3.40 |
| `motor_clamp_washer_od` | 7.00 |
| `motor_clamp_washer_thickness` | 0.50 |
| `motor_clamp_nut_af` | 5.50 |
| `motor_clamp_nut_thickness` | 2.40 |
| `underside_driver_clear_diameter` | 6.00 minimum |
| `underside_nut_tool_clear_diameter` | 8.00 minimum |
| `tool_path_clearance_to_moving_solid` | 0.50 minimum |

Clamp axes remain at local station coordinates:

```text
radial x = (88.00, 126.00)
tangential y = (-12.00, +12.00)
```

The screw head or a captive anti-rotation feature must be reachable from the
wall side. The nut/driver pairing must allow loosening, sliding, measuring
mesh, and retightening while all three rings, rollers, fins, and the outer
frame are installed. A test cylinder along every tool path must have zero
positive-volume intersection with the complete assembly at `q=-0.35, 0.00,
+0.10` and at all three stations.

Clamp acceptance:

- washer tangential ligament ≥ 1.00;
- worst service-end radial ligament ≥ 2.00;
- slot radial clearance per side ≥ 0.30;
- tightened yoke slip under 10 N radial proof load ≤ 0.10;
- no powered adjustment outside the interlocked interval.

## 5. Roller guidance: two fixed towers plus one compliant tower

Tower roles are frozen:

- 60°: fixed datum tower;
- 180°: fixed datum tower;
- 300°: compliant setup/runout tower.

Each tower remains one bar carrying three independently rotating flanged
rollers on one polished D4 axle. Motor pinions provide torque only and must not
be counted as ring-location supports.

### Roller interface

| Variable | Value |
|---|---:|
| `roller_axle_finished_diameter` | 3.99 |
| `roller_bore_finished_diameter` | 4.06 |
| `roller_running_od` | 12.10 |
| `roller_flange_od` | 13.80 |
| `roller_flange_thickness` | 0.50 |
| `roller_flange_axial_clearance_per_side` | 0.15 |
| `roller_capture_radial_overlap_nominal` | 0.80 |
| `roller_min_capture_overlap_worst_case` | 0.30 |
| `roller_running_band_height` | 2.00 minimum |
| `roller_material_primary` | POM |
| `roller_material_fallback` | low-friction printed coupon only |
| `roller_spacer_lengths` | 1.00, 1.00 |

The R2 axial planes are frozen below. They provide the 2.00 running band while
retaining a 2.10 tooth face and 2.30 nominal clear space between carriers.

| Role | Carrier Z | Smooth running band Z | Tooth/pinion face Z |
|---|---:|---:|---:|
| Hour | -2.20–2.20 | -2.10–-0.10 | 0.00–2.10 |
| Minute | 4.50–8.90 | 4.60–6.60 | 6.70–8.80 |
| Second | 11.20–15.60 | 11.30–13.30 | 13.40–15.50 |

Carrier thickness is 4.40. The motor output pinion, its axial collar stack,
role spacers, fin roots, roller flanges, tower bridges, front stationary ring,
and exported reference hardware must follow these datums through shared
derived properties; no role-specific literal Z values may be duplicated in
geometry code. The front stationary ring occupies Z=16.70–17.70, leaving
`16.70 - (15.60 + 0.60) = 0.50` at worst second-ring axial warp. Tower upper
bridges must remain at or above Z=16.70 and outside the moving radial sweep;
the D4 tower axle grows to 30.00 nominal length and is cut/selected to leave
1.00–2.00 above the purchased top collar after final assembly.

For a roller with running radius `r_run = roller_running_od / 2`, nominal
contact occurs at:

```text
R_axis_contact = carrier_race_radius - r_run = 131.60 - 6.05 = 125.55
```

The two fixed towers use an eccentric D4 bushing with ±0.50 radial setup
authority, then lock at `R_axis_contact ± 0.05`. They do not move during use.

The 300° tower uses a metal compression spring and guided radial carriage:

| Variable | Value |
|---|---:|
| `compliant_axis_nominal_radius` | 125.55 |
| `compliant_radial_travel` | -1.00 to +1.00 |
| `compliant_nominal_spring_compression` | 1.00 |
| `compliant_spring_rate_range` | 0.80–1.20 N/mm |
| `compliant_force_at_nominal` | 0.80–1.20 N |
| `compliant_force_min_over_envelope` | 0.20 N |
| `compliant_force_max_over_envelope` | 2.10 N |
| `compliant_hard_stop_margin` | 0.25 beyond runout envelope |

Printed PETG flexure creep is not accepted as the sole preload source.

## 6. Runout, warp, clearances, and fin envelopes

The CAD must pass the complete mechanism under this deliberately conservative
printed-part envelope:

| Variable | Value |
|---|---:|
| `ring_radial_runout_allowance` | ±0.75 per ring |
| `ring_radial_TIR` | 1.50 maximum |
| `ring_axial_warp_allowance` | ±0.60 per ring |
| `ring_axial_TIR` | 1.20 maximum |
| `roller_axial_float` | ±0.15 per ring |
| `min_moving_to_stationary_clearance` | 0.50 |
| `min_moving_to_moving_clearance` | 0.50 |
| `min_remaining_interplane_gap` | 0.80 |

Worst-case adjacent-fin nominal radial separation is:

```text
G_fin_nominal >= 2 * ring_radial_runout_allowance
                 + min_moving_to_moving_clearance
              >= 2.00
```

Freeze the fin blade radial bands to:

| Role | Blade radial range |
|---|---:|
| Hour | 142.50–143.70 |
| Minute | 139.30–140.50 |
| Second | 136.10–137.30 |

This leaves 2.00 nominal between adjacent blade sweeps. The hour blade also
retains `145.00 - (143.70 + 0.75) = 0.55` to the stationary outer ring at its
worst outward runout.

All clearance tests must include the complete carrier quadrants, gear teeth,
fins, seam plates, dowels, screws, washers, motor stations, roller towers,
outer frame, posts, and future reserved Hall envelopes—not bounding boxes
alone.

## 7. Complete quadrant seam receiver and tool interface

Each ring remains four quadrants and four seams. Every seam uses:

- one underside splice plate;
- one D2.90 registration dowel in a D3.00 channel;
- two M2 × 8 socket screws from the viewer side;
- two captive M2 hex nuts in the splice plate.

| Variable | Value |
|---|---:|
| `seam_plate_radial_range` | 133.50–138.50 |
| `seam_plate_tangential_length` | 12.00 |
| `seam_plate_thickness` | 2.00 |
| `seam_screw_pitch_from_joint` | ±4.00 tangential |
| `seam_ring_clearance_hole_diameter` | 2.20 |
| `seam_screw_head_counterbore_diameter` | 4.00 |
| `seam_screw_head_counterbore_depth` | 1.50 |
| `seam_captive_nut_af` | 4.10 |
| `seam_captive_nut_thickness` | 1.70 |
| `seam_driver_clear_diameter` | 5.00 |
| `seam_min_edge_ligament` | 2.00 |

Bare printed M2 threads and an unreceived screw in a 2.20 clearance hole are
not acceptable. The nut pocket must positively prevent nut rotation and allow
replacement during service.

## 8. Required assembly and service order — wholly superseded by I4

The implementation must render and test these ordered states:

1. Install chassis/frame segments and the three motor-yoke cartridges.
2. Install all motor/miter/output shafts and set axial endplay to 0.05–0.15.
3. Install fixed/compliant tower bases and bare D4 axles; leave upper bridges
   and collars off.
4. Install hour rollers, thrust washer, and spacers.
5. Assemble the four hour quadrants in place around the flanged rollers; add
   all four seam plates, dowels, captive nuts, and eight screws.
6. Repeat the roller/ring/seam sequence for minute, then second.
7. Install upper thrust washers, tower bridges, and purchased D4 collars.
8. With all rings installed, loosen each motor station from the wall side,
   tune `q` only within the powered band, rotate the corresponding ring 360°
   by hand, and tighten the four clamps.
9. Verify all three rings rotate independently through 360° before installing
   any decorative cover or LED cartridge.

Service removal is the exact reverse order. No ring may require cutting,
destructive snap removal, or removal of another motor station.

## 9. Complete motion and mesh acceptance

### CAD/BREP gates

For each role independently:

1. Sweep its complete moving module through `theta=0..359°` in 1° steps.
2. At each step, test `q=-0.35, 0.00, +0.10`.
3. Test the other two rings at relative phases `0`, `half_tooth_phase_deg`,
   and `ring_tooth_pitch_deg`.
4. Test radial offsets `(±0.75, 0)`, `(0, ±0.75)` and axial offsets `±0.60`.
5. Require zero unintended positive-volume intersection and the numeric
   clearances in section 6.
6. Treat only the intended pinion/ring tooth relationship as a contact pair;
   no motor, roller flange, seam, fin, or frame contact may be waived.

The source assembly and exported STEP must have identical named-occurrence
sets, occurrence bounds within 0.02, and zero invalid solids.

### Physical mechanics gate

- ring radial TIR ≤ 1.50 and axial TIR ≤ 1.20;
- no bind through 20 manual revolutions per ring;
- no other ring moves more than 0.5° while one ring is driven 360°;
- backlash at each fin after reversal ≤ 0.50°;
- startup/running torque margin ≥ 2.0 against measured worst-case drag;
- no stalls, tooth skips, flange escape, or clamp slip during a 24-hour
  seconds-speed run;
- record A-weighted dBA at 1 m; R2 makes no unmeasured “quiet” claim.

## 10. Source-derived sector coupon

The full R2 production source is authoritative. The coupon is generated by
selecting production solids; it must not redraw simplified teeth, races,
slots, fasteners, or Hall features.

API:

```python
make_r2_sector_coupon(role, q_mm=0.0, include_hall_reservation=False)
```

The coupon is an 80° sector local to each role, spanning station angle −10°
through its adjacent guide tower at +60° plus a +10° margin. At R150 its chord
is `2 * 150 * sin(40°) = 192.84`, fitting the 270 mm U1 bed.

It must contain the exact production:

- role-specific carrier/tooth/race sector;
- complete motor cartridge and four radial clamps;
- one fixed/compliant production roller-tower interface;
- one complete production seam receiver;
- hard stops limiting coupon motion without altering mesh geometry;
- optional reserved Hall interface selected from the full model.

Coupon physical acceptance:

- motor `q` can be adjusted and clamped with the sector installed;
- 100 forward/reverse cycles without tooth climb or clamp motion;
- remains free with ±0.75 radial shims and ±0.60 axial shims;
- backlash ≤ 0.50° equivalent at the role fin radius;
- source/export part names and local bounds match the corresponding full-model
  production interfaces within 0.02.

Passing the coupon permits a full-ring print; it does not prove the complete
clock's balance, runout, optics, noise, or endurance.

## 11. Staged Hall and optical gates

Hall and optical hardware are intentionally staged after the mechanical gate.
R2 reserves space but does not make them load-bearing or part of ring guidance.

### Hall reservation

| Variable | Value |
|---|---:|
| `home_magnet_nominal` | D4 × 2 |
| `home_magnet_pocket` | D4.10 × 2.10 |
| `home_magnet_min_back_wall` | 1.00 |
| `hall_target_air_gap_adjustable` | 1.50–3.00 |
| `hall_reserved_module_envelope` | 12 × 8 × 4 |
| `hall_min_mechanical_clearance` | 0.50 |

Reserve one magnet pocket per ring on radius 136.00 and one three-height sensor
bracket sector centred at 90°. Magnet pockets must be mechanically captured;
adhesive is secondary retention. No Hall solid is implemented until the full
mechanical sweep passes.

Hall gate after mechanics:

- exactly one clean transition per ring revolution;
- repeatable home angle within ±0.25° over 50 home cycles;
- no false trigger from adjacent-ring magnets or motor fields;
- sensor/magnet clearance remains 1.50–3.00 throughout the runout envelope.

### Optical gate after Hall

The LED source, heatsink cartridge, mask, and wiring remain separate work.
Before they are added, ray/swept-cone tests must show that every new fixed part
either lies outside the useful LED-to-wall cone or is explicitly accepted as
part of the permanent shadow composition. Diffusers and assumed secondary
optics remain prohibited for the point-source shadow test.

## 12. Explicit non-goals

R2 does **not**:

- redesign the LED/heatsink cartridge, decorative face, wall mount, enclosure,
  ESP32 firmware, TMC2209 electronics, power supply, or UI;
- add TPU, belts, friction drive, helical gears, motorization of adjustment, or
  a quartz movement;
- claim final quietness, optical quality, thermal safety, or 24-hour accuracy
  from CAD tests;
- optimize visual styling;
- delete or overwrite prior model versions;
- accept a disconnected coupon as evidence for the full mechanism.

## 13. Implementation handoff checklist

Implementation is complete only when it produces:

- new R2 spec and geometry source without editing rollback sources;
- named variables matching this document;
- assembled, service-exploded, powered-min, powered-max, and
  `UNSAFE_TO_POWER` STEP poses;
- role-derived sector coupons;
- exact math, BREP, source/export parity, assembly-order, and unsafe-q tests;
- screenshots/section views showing underside clamp access, three ring planes,
  roller capture, seams, and reserved Hall envelopes;
- an independent read-only review verdict.

Physical printing remains the final proof of fit, runout, backlash, drag,
noise, wear, homing repeatability, and optical shadow quality.
