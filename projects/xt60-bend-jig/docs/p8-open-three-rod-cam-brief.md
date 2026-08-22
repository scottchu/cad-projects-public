# P8 open three-rod cam bender — corrective CAD brief

- Status: corrective architecture after the user rejected P7. Preserve P7 as a rejected kinematic proof; do not overwrite P0-P7.
- Model: simple, open, two-sided corner-clamp mechanism for holding two 12 AWG XT60 leads at a 90 degree bend above the bottom ESC.
- Units: millimetres.
- Coordinate convention: the three purchased rods run on X; the bend lies in YZ; +Y points from the bend toward the ESC stack and +Z is up.

## Preserve from P7

- Exactly three purchased 304 stainless rods, diameter 4.0 mm and length 50.0 mm.
- Closed rod centers:
  - upright: Y=-4.15, Z=42.00;
  - bottom: Y=12.00, Z=25.85;
  - diagonal former: Y=4.691852455, Z=34.691852455.
- All three rods move together through a common 11.0 mm stroke:
  - upright along +Y;
  - bottom along +Z;
  - diagonal along (-Y,-Z)/sqrt(2).
- One shared X shaft drives mirrored outside cam layers.
- Rotation 0-70 degrees closes the rods; 70-80 degrees is a true constant-radius dwell; a positive stop and removable lock define the exact 80 degree end pose.
- Freeze the review mid pose at shaft angle 35 degrees. Because smoothstep(0.5)=0.5, this is an exact 45 degree partial bend.
- Closed workpiece: two 4.3 mm nominal 12 AWG leads, 44 mm available arclength, R6 centerline bend, horizontal solder leg and exactly vertical XT60 leg.
- Shaft/track math may reuse the audited P7 inverse paths and shaft datum Y=-7.5, Z=32.5. Handedness must not be mirrored.

## Reject from P7

- No full rectangular side panels.
- No full or mostly-solid 64 mm scroll discs.
- No upper cage, overhead bridge, or tall remote lock tower.
- The wire, all three rods, R6 bend, and XT60 must not require hiding most of the mechanism to become understandable.
- Open and mid assemblies must not reuse the already-closed wire and vertical XT60.

## Corrected architecture

- Two mirrored OPEN stationary L-shaped guide cheeks, one at each rod end. Their side profile contains only:
  - a narrow vertical guide rail around the upright straight slot;
  - a narrow horizontal guide rail around the bottom straight slot;
  - a narrow diagonal guide rail around the former slot;
  - a compact round shaft bearing boss;
  - only the short ribs required to make each cheek one connected solid.
- The paired cheeks are joined by one low/rear cross-member and one broad flat bench-clamp foot. Nothing crosses above the bend or XT60.
- Two mirrored thin OPEN cam spiders sit outside the guide cheeks and key to the same shaft. Each spider contains:
  - one compact hex-keyed hub;
  - three curved slot rails generated from the P7 inverse kinematics;
  - minimal spokes and, only if needed, a narrow outer connecting arc/ring.
- Cam spiders must be predominantly open. Design target is <=42% projected solid area and hard acceptance is <=45% of a full circle using the same outer envelope; the open window must expose the rod ends and bend. Do not use a full outer ring; if an outer connector is required, limit it to a narrow arc no greater than 150 degrees.
- Each stationary cheek must also be demonstrably open: its projected YZ material area divided by its YZ bounding rectangle must be <=55%, with at least one exterior-connected central window. Labels alone are not evidence of an L profile.
- Keep one right-side dial. Put the 80 degree stop/detent immediately beside the shaft/dial on the right L cheek; no member may rise into the XT60 region.
- Retention remains prototype-oriented: left rod caps may use the 3.90 mm press trial; right retainers remain removable snap-friction trials and must be labelled as requiring print validation. The grooved shared shaft keeper remains true axial capture.

## Workpiece states and simulation boundary

- Add explicit bottom ESC copper pad references at X=+/-4 near Y=28. Their top datum must contact the lead start with zero modeled gap; add small solder-reference solids if needed for a readable connection.
- The ESC remains below the FC. Electronics and XT60 are reference geometry only and never appear in the print kit.
- The open and closed workpiece poses are physical CAD acceptance states. A true intermediate deformation requires elastic/contact analysis and is not proven by this mechanism CAD.
- For a readable mid-state construction reference only, let `g(theta)=smoothstep(clamp(theta/70,0,1))` and `alpha=90deg*g(theta)`.
- For alpha in radians, preserve 44 mm lead arclength with:
  - partial-arc endpoint `A=(6-6*sin(alpha), 36-6*cos(alpha))`;
  - terminal tangent `t=(-cos(alpha), sin(alpha))`;
  - remaining tail `Ltail=44-22-6*alpha`;
  - lead endpoint `E=A+Ltail*t`.
- At 0 degrees the physical loading reference is straight and the XT60 axis follows -Y. At 70-80 degrees the physical closed reference is unchanged and exactly vertical.
- A 35 degree mid entry may show the alpha=45 construction ghost for communication, but it must be labelled `nonphysical_mid_deformation_reference` and excluded from collision/physical-path claims. The inherited common rod trajectories intersect this simple interpolated wire around the upright rod, so it is not an elastic simulation.
- Frozen numeric state checks:
  - 0 degrees: endpoint E=(-16,30), tangent=(-1,0), tail=22;
  - 35 degrees: alpha=45 degrees, A=(1.757359313,31.757359313), tangent=(-0.707106781,0.707106781), tail=17.287611020, endpoint E=(-10.466827670,43.981546295);
  - 70 and 80 degrees: A=(0,36), tangent=(0,1), tail=12.575222039, endpoint E=(0,48.575222039).

## Protected access and visibility

- Within the 32 mm clear X span, no printed solid is allowed in the work zone; only the three stainless rods and reference workpiece/electronics may occupy it.
- Keep clear approach corridors to the ESC pads from +Y and to the XT60 from +Z.
- External cam tracks may extend above the final wire endpoint when required by the preserved inverse path; they remain outside the work span. Do not apply a global-height ban that makes the track geometry impossible.
- Protect the actual work/access volume instead:
  - central bend box: `|X|<=16`, `Y=-8..30`, `Z=24..55` contains no printed solid;
  - XT60 top-insertion prism: `|X|<=10`, `|Y|<=6`, `Z=48.575222..90` contains no printed solid;
  - solder approach prism: `|X|<=10`, `Y=24..70`, `Z=27.85..38` contains no printed solid.
- Purchased rods and workpiece/electronics references may enter those volumes where intended; the zero-printed-solid rule applies to printable structure only.
- In the normal closed ISO/slight-yaw review, both leads, all three rods, copper pads, horizontal legs, R6 bend, vertical legs, and XT60 must be simultaneously readable.
- A side diagnostic may ghost the nearest cam spider, but the physical open structure itself must retain a clear central window.

## Simplicity gates

- At most four principal side plates: two L guide cheeks and two cam spiders.
- Exactly one low fixed cross-member plus the clamp foot.
- No full disc, full rectangular wall, top cage, or remote lock tower.
- The three rods must be the visually dominant moving members.
- Print kit separates every printed part, places every part on the bed, and excludes all purchased rods/electronics.

## Source and artifacts

- Helper: `src/xt60_bend_jig/p8_open_three_rod_cam.py`.
- Entries under `cad/p8_open_three_rod_cam/`:
  - `p8_loaded_open.step.py`;
  - `p8_loaded_mid.step.py`;
  - `p8_loaded_closed.step.py`;
  - `p8_exploded.step.py`;
  - `p8_print_kit.step.py`.
- Generate matching STEP files after source tests pass.

## Required deterministic validation

- Preserve the P7 401-pose common-travel/dwell contract and <=0.02 mm inverse-slot reconstruction residual.
- Preserve exact final wire arclength 44 mm, R6 bend, perpendicular final tangents, and three closed rod tangencies with zero positive overlap.
- Verify the physical open and closed lead endpoints/XT60 axes against the equations and verify both endpoint workpieces clear or contact the intended rods correctly.
- If the mid construction ghost is included, verify its endpoint/arclength equation and label, but do not require or claim rod clearance. Tests and reports must state that it is not a physical deformation solution.
- Verify wire-to-copper-pad distance is zero and the solder reference does not intersect the printed jig.
- Verify both guide cheeks and both cam spiders are individual connected, closed, positive-volume solids.
- Verify cam-spider projected solid-area fraction <=45% and no full rectangular guide wall exists.
- Verify each L-cheek projected material-area ratio <=55% and its central opening connects to the exterior.
- Sweep moving BREP geometry through at least 201 poses for guide/cam/rod clearance, synchronized left/right placement, stop contact, and overtravel interference.
- Verify one-piece fixed frame, low bridge, and clamp foot do not intersect the protected work/approach corridors.
- Validate every generated STEP and source/export parity.

## Mandatory visual acceptance

- Slight-yaw closed ISO: both leads, all three rods, pads, horizontal-to-vertical bend, and XT60 visible without hiding the fixed structure.
- Pure side profile with only the nearest cam spider ghosted/hidden.
- Top view proving the 32 mm clear work span.
- Open loading pose with straight lead and horizontal XT60.
- Mid pose with partially bent lead.
- Exploded assembly and top print-kit view.

## Physical-proof boundary

- CAD can prove geometry, motion, nominal clearances, openness, and assembly order only.
- Printing must prove PETG stiffness at the skeletal track rails, rod/cap fits, right-retainer holding force, guide friction, backlash, lock-pin fit, heat exposure, soldering access, and compatibility with the actual FPV stack.
