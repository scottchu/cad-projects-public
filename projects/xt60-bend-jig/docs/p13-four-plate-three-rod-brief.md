# P13 — four circular plates / three equal-travel rods

P13 is a new mechanism-validation prototype. P1 through P12 remain unchanged.
This brief is the Gate-0 contract: implementation may begin only after an
independent intent reviewer and an independent geometry reviewer accept every
item below. A later implementation is not allowed to weaken these requirements
to make CAD pass.

## Accepted-spec provenance and supersession

The current accepted CAD-source specification is this parent brief **as
amended by** `docs/p13-cad-source-domain-amendment.md`. The amendment is the
controlling authority wherever older pass history below describes an integral
right-cam shaft, rectangular local key/rib, keyed left cam, three unique
principal printable definitions, or forbids a separate shaft. Those clauses
are retained only as design-history evidence and are not current production
requirements. Current source, manifest, STEP, and 3MF provenance records must
hash both documents and must identify the amendment as accepted and
controlling. The current production architecture is four independently
printable principal plates, one separate shallow-D actuator shaft, one shaft
keeper, and six rod caps; the production 3MF census is 12 objects and the STEP
print-kit census is those 12 objects plus two diagnostic coupons.

CAD can prove nominal part count, one-DOF kinematics, clearance and collision
envelopes, assembly reachability, and exported-solid integrity. It cannot prove
printed fit, stiffness, torque, long-term frictional retention, elastic life of
the remaining C-journals/keeper, wire deformation, springback, insulation
damage, heat resistance, or one-handed usability. The removable right-cap fit
is separately informed by the initial accepted P16 PETG hand-fit coupon gate;
shake, cycling, wear, creep, heat, and pull-off retention remain untested.

## 1. Frozen architecture (consolidated by the accepted amendment)

- Exactly four visible principal plate bodies, each independently printable:
  1. left keyed rotating circular cam plate;
  2. left fixed circular guide plate;
  3. right fixed circular guide plate;
  4. right rotating circular actuator plate with a shallow-D bore and outward
     hub.
- All four plate blanks are plain `OD 40.50 mm` circles. Slots, the centre bore,
  annular bearing lands/hubs, the two fixed-plate integral upward-opening
  C-journals, and the two matching shallow-D cam bores are the only permitted
  plate features; no
  flower lobes or structural tab may
  extend outside the circular blank. The C-journals are integral regions of the
  two fixed plates, not additional loose structural parts.
- Exactly three purchased uncut 304 stainless rods, each `Ø4.00 x 50.00 mm`.
- One user actuator input, `theta`: the user rotates the circular rim of the
  right cam. One separate printed shallow-D shaft, nominal `OD5.60 / AF5.15`,
  passes through matching `OD5.70 / AF5.25` bores in both cam plates. A round
  `OD9.60 x 2.00` head and the removable left C keeper retain it axially. There
  is no separate key occurrence or rectangular/full-length key. The same three rigid
  rods pass through both cam paths and both fixed guides. Printed key clearance
  may create bounded phase/backlash and is not assumed accurate until the
  Section 4 feasible-set audit and physical coupons pass.
  There is no second user adjustment, screw, gear, worm, translated pin,
  linkage, or independently timed rod.
- There is no separate key occurrence, rectangular keyway, local rib, or
  full-length key. Phase coupling is provided only by the bounded shallow-D
  shaft/bore interfaces documented by the accepted amendment.
- Every rod uses the same scalar travel function and the same stroke. Their
  straight guide directions differ.
- No base, spine, platform, bridge, cage, tower, wall, bench tongue, connector
  holder, electronics holder, locator, or integrated workholding.
- The locked workpiece centreline is exactly 90 degrees. Angle adjustment is
  out of scope.
- Retainers have round outside envelopes. Square/rectangular rod blocks and
  decorative handles are forbidden.

**Archived fifteenth-pass renewed-intent-review notice:** this historical repair retains four
visible circular plates and side-entry fixed journals but replaces the
separate full-length keyed-shaft concept with one simpler right-cam/round-shaft
actuator occurrence and a key rib only inside the left-cam final zone. The
left cam remains separately printable and installs from the left. There are
four visible plates but only three unique principal printable definitions. It
adds no base, spine, bridge, spacer, or hardware. The production fixed-journal
cutter remains exactly `ID4.80`; diagnostic coupon diameters are not source
alternatives. The axial cam state and full SE(2) fit model introduced here need
renewed intent approval before implementation.

**Archived twenty-first-pass renewed-architecture-review notice:** the shaft and
all four plate-local origins are no longer fixed at inherited datum `(0,30)`.
One fully derived `C_shaft=(shaft_y,shaft_z)` moves diagonally outward from the
90-degree bend by the exact Section4 formula. Every circular blank, fused
shaft, shaft groove, fixed C-journal, keeper, inverse cam lane, and
pivot-relative cutter/pose regenerates concentrically from that datum. The
three locked rod/contact centres and the complete workpiece centreline remain
task geometry in world YZ. This changes no occurrence, connectivity, rod,
actuator, or forbidden-feature census and adds no base or cheek-removal step;
it does require renewed intent and math acceptance before implementation.

### 1.1 Mandatory parametric-source contract

P13 must remain easy to modify without editing geometry code or generated
artifacts. The authoritative source exposes one central, typed, unit-bearing
`P13Params` schema. Every dimension, position, angle, fit, tolerance,
manufacturing variant, metrology input, operation state, solver tolerance,
evidence camera, and output selection is either a named field in that schema or
a named formula derived from those fields. Numeric literals are permitted only
for mathematical identities such as `0`, `1`, `2`, `pi`, and explicitly named
unit conversions; scattered geometry/placement/test magic numbers are a hard
failure.

The source must serialize a dependency graph that maps each primary parameter
to every derived datum, cutter, solid, assembly pose, test threshold, state,
and export it affects. The graph and a machine-readable default parameter
manifest are source-controlled evidence. Every formula quoted in this brief is
implemented once as a named derivation and reused by geometry, tests, reports,
and exports; duplicated arithmetic with independent literals fails parity.

Parameter classes are explicit:

- **Retunable without architecture re-Gate:** measured specimen/profile inputs
  and diagnostic manufacturing/tolerance values that remain inside their
  frozen ranges and do not alter occurrence count, connectivity, allowed
  cutters, operation sequence, 90-degree intent, or purchased-hardware class.
  Any accepted retune still requires clean regeneration, all affected tests,
  source/STEP parity, and independent math/visual re-review.
- **Requires renewed Gate-0 intent review before implementation:** any change
  to part count, connectivity, circular-plate topology, rod count or hardware
  class, actuator count, allowed/forbidden feature census, workpiece path or
  angle, operation sequence, access/removal contract, or any option that
  enables/disables a solid/cutter or changes topology. Such options must be
  named, default-frozen, and absent from accepted exports until re-Gated.

For the P21 pivot family, `c_sw` may be safely retuned only over
`0.50..0.75 mm`, and `wire_diameter_design` only over `4.20..4.30 mm` for the
same declared wire/insulation hardware class, provided every derived geometry,
continuous clearance, rim, and parity test passes. `shaft_od=5.60 mm` is the
frozen separate shallow-D actuator-shaft class and `R_bend=6.00 mm` is the
frozen task workpiece path;
changing either nominal value is a dependency/metamorphic test case only and
requires renewed Gate-0 intent approval before any resulting artifact can be
accepted.

Metamorphic parameter tests must start fresh processes from at least three
representative nondefault parameter sets within the retunable class. Each test
changes one primary parameter, regenerates STEP from source, and proves that
every declared dependent measurement changes by its documented formula while
unrelated invariants and occurrence labels remain unchanged. A second test
changes two coupled parameters and proves the dependency graph, formulas,
analytic checks, BREP checks, and STEP/source parity remain coherent. Repeated
generation with the same manifest must be deterministic. Generated STEP, STL,
3MF, GLB, snapshots, and reports are never hand-edited; every artifact records
the source revision and exact parameter-manifest hash that generated it.

## 2. Coordinates and axial stack

- Units are millimetres. Rod and shaft axes are `X`; all mechanism paths lie in
  `YZ`. `X=0` is midway between the inside faces of the fixed plates. `+Y`
  points toward the ESC pads and `+Z` upward toward the XT60. Positive `theta`
  is right-hand rotation about `+X`.
- OPEN is `theta=0`. Smooth motion is `0..22 degrees`; `22..27 degrees` is a
  true endpoint dwell; LOCKED is `theta=27 degrees`.
- Frozen left-to-right order:
  `left cam -> left fixed -> nominal 26.20 clear span -> right fixed -> right cam`;
  the permitted endplay minimum is exactly `26.00`.
- `t_fixed=2.80`, `t_cam=2.50`, and main-face running gap `g_cam=0.30`.
- Fixed centres are `X=+/-14.50`; cam centres are `X=+/-17.45`.
- Principal stack width is
  `26.20 + 2*(2.80+0.30+2.50) = 37.40 mm` at nominal fixed-plate seating.
- In the nominal unskewed `a_i=0,k_i=0` state, a 50 mm rod projects
  `50.00-37.40=12.60 mm` total, `6.30 mm` at each side before retainer bodies,
  and occupies `X=-25.00..+25.00`. Across the full physical state, Section 4
  instead uses the exact unit rod axis `n_i`, arclength endpoints
  `c_i+/-25*n_i`, and X tips `a_i+/-25*n_iX`; it never treats 50 mm as a world-X
  length when the rod is skewed. The exact bare projections are
  `(X_cam-1.25)-X_left_tip_i` on the left and
  `X_right_tip_i-18.70` on the right for the nominal core only. Every admissible
  physical specimen uses its frozen measured exact BREP extrema
  `X_left_actual_i/X_right_actual_i`; the outer audit repeats for every
  admitted `W in U_i` and must retain full
  slot-thickness coverage, exact cap/plate BREP clearance, and `>=2.50 mm`
  cap engagement measured along rod arclength.
- Each fixed disc has `0.20 mm` total axial groove endplay. Fixed-centre spacing
  is nominally `29.00`, with bounded range `28.80..29.20`; corresponding clear
  span between the 2.80-mm fixed-disc inner faces is `26.00..26.40`, nominally
  `26.20`. All four endplay corners must be tested.

## 3. Locked workpiece and exact contact geometry

The assumed workpiece remains a parameterized CAD envelope, not a catalog
claim. Two insulated leads have `Ø4.30` and X centres `-4.00,+4.00`.

In YZ, the centreline is defined exactly as:

```text
horizontal: (Y,Z)=(q,30), q >= 6
arc:        (Y,Z)=(6-6*cos(phi), 36-6*sin(phi)), 0 <= phi <= 90 deg
vertical:   (Y,Z)=(0,q), q >= 36
```

The equivalent quarter-circle has centre `(6,36)` and radius `6`. The arc is
G1 tangent to the horizontal line at `(6,30)` and to the vertical line at
`(0,36)`. Unit tangents immediately before/after each join must have dot
product `1` within `1e-9`; the horizontal and vertical endpoint tangents must
have dot product `0` and included angle `90.0 +/-0.05 degrees`.

The three frozen locked rod centres and contact-normal directions are:

| role | guide normal angle | locked centre `(Y,Z)` | contact feature |
|---|---:|---:|---|
| upright/forming | `0 deg` | `(-4.15,42.00)` | vertical lead, normal `(-1,0)` |
| bottom/support | `90 deg` | `(12.00,25.85)` | horizontal lead, normal `(0,-1)` |
| diagonal/locking | `225 deg` | `(4.691852455,34.691852455)` | 45-degree arc contact, inward normal `(1/sqrt(2),1/sqrt(2))` |

At each declared contact the distance between the Ø4 rod centre and Ø4.30 wire
centreline is `2.00+2.15=4.15 mm`. Analytic tangency residual must be
`<=0.02 mm`, contact normals must agree within `0.05 degrees`, and nominal
BREP positive-overlap volume must be `<=1e-7 mm3`.

## 4. Audited equal-travel candidate

The accepted candidate replaces all inherited P9/P11 values and the first P13
shaft guess. In particular, `C=(-7.5,32.5)`, `C=(0,30)`, `S=11`, and the old
`70/80-degree` law are forbidden. Freeze the following single-source
derivation in `P13Params`:

```text
shaft_od = 5.60
wire_diameter_design = 4.30
c_sw = 0.50
R_bend = bend_radius = 6.00
bend_center = (bend_center_y,bend_center_z) = (6.00,36.00)
horizontal_z = 30.00
r_s = shaft_od/2 = 2.80
r_w = wire_diameter_design/2 = 2.15
d_arc0 = R_bend*(sqrt(2)-1) = 2.485281374239
delta_pivot = ((r_s+r_w+c_sw)-d_arc0)/sqrt(2)
            = 2.096372644586
shaft_y = (bend_center_y-R_bend)-delta_pivot
        = -2.096372644586
shaft_z = horizontal_z-delta_pivot
        = 27.903627355414
C_shaft = (shaft_y,shaft_z)
guide normals = 0, 90, 225 degrees
common stroke S = 3.764213562 mm
E(a) = 3*a^2 - 2*a^3, a clamped to 0..1
s(theta) = S*E(theta/22)  for 0 <= theta <= 22
s(theta) = S              for 22 <= theta <= 27
P_i(theta) = P_i_locked - u_i*(S-s(theta))
Q_i(theta) = C_shaft + Rot_X(-theta)*(P_i(theta)-C_shaft)
```

`Rot_X` above means the 2D YZ rotation induced by world-X rotation, not
`R_bend`. The vector from `bend_center` to `C_shaft` is
`(-(R_bend+delta_pivot),-(R_bend+delta_pivot))`, so the exact nearest centreline distance
from the shaft datum to the quarter arc is

```text
sqrt(2)*(R_bend+delta_pivot)-R_bend = r_s+r_w+c_sw = 5.45
```

and nominal shaft-surface to Ø4.30 wire-surface clearance is exactly `c_sw`.
This analytic equality is only a default seed: acceptance uses the complete
solid and specimen-domain certificate below.

Both cam plates use the same local inverse paths `Q_i`; mirroring is permitted
only in X. In the nominal zero-clearance model their YZ slot phase may not
differ.

### 4.1 Nominal positive phase coupling and physical feasible-set audit

The free passive-cam alternative is rejected: the independent audit found an
exact `5-degree` phase continuum over the `22..27-degree` dwell and at least
`+/-1.495 degrees` nominal slot-only phase freedom. Rod paths therefore remain
the load/forming constraint but are not accepted as the sole phase coupling.

The driven right-cam angle is `theta_R=theta`. The left cam installs on the
single local rectangular rib defined in Section 7, so its nominal line-to-line
key flanks impose `theta_L=theta_R`. Across the full stroke, solve the complete
nominal BREP constraints with `theta_L` retained as a variable and prove one
connected branch:

```text
theta_L = theta_R
P_left_i(theta_L) = P_right_i(theta_R) = P_i(theta)
```

within `1e-9 degree` and `1e-9 mm`, with zero positive key-flank overlap and no
slot-only alternate phase branch accepted.

An independent tolerance audit must then solve the **feasible set**, not force
the printed key to be line-to-line or the left cam to remain coaxial. Its
left-cam cross-section pose is the full
`g_cam=(d_cam_y,d_cam_z,theta_L) in SE(2)`. A pose is feasible only when the
measured round-bore and rectangular-keyway BREP, transformed by `g_cam`, has no
positive overlap with the measured round shaft/local rib and retains legal
flank/roof contact. Nominal line-to-line CAD alone freezes
`d_cam=(0,0),theta_L=theta_R`.

For every commanded `theta_R` and each fixed specimen record `p_c` classified
in Section 4.1.1, cross the exact feasible `g_cam` set with that specimen's
measured as-printed production `ID5.70`+nominal-keyway geometry, cam/fixed lane
realization, rod diameters, production-`ID4.80` journal fits, movable fixed
guide/keeper/cap rotations and offsets, and axial states. Independent lane
variants and other tolerance realizations are
separate outer-loop specimen records, never time-varying geometry. Diagnostic
left-cam cutters may inform sensitivity only and cannot be substituted into
the production solve. Solve every
left-cam/rod pose with no rigid positive overlap. Report:

- `min/max(theta_L-theta_R)` at every pose and the global backlash interval;
- any disconnected solution branch, jump, dead zone, reversal, or key bind;
- rod translation slack and maximum rod-axis skew;
- resulting LOCKED contact residuals and both configuration-dependent reverse
  events from the exact Section-4 predicates.

Axial states are variables, not a nominal rendering assumption. Let

```text
X_keeper in [-19.50,-19.30]
X_fixed_left in [-14.60,-14.40]
X_cam in [X_keeper+1.75, X_fixed_left-2.85]
```

The lower inequality follows from keeper-right-face
`X_keeper+0.50 <= X_cam-1.25` (left-cam outer face). The upper follows from
cam-land tip `X_cam+1.35 <= X_fixed_left-1.50` (left fixed-land tip). The full
coupled domain is nonempty and its global projection is exactly
`-17.75<=X_cam<=-17.25`; physical-state views must not pin the cam at `-17.45`.
Intersecting the cam span `[X_cam-1.25,X_cam+1.25]` with local rib
`[-18.70,-16.20]` gives `2.20 mm` engagement at `X_cam=-17.75`, `2.30 mm` at
`X_cam=-17.25`, and `2.50 mm` nominally. Every feasible state must retain
`>=2.20 mm` engagement and zero positive land/keeper overlap.

Journal mobility is explicit in that same solve. From the measured as-printed
parts made with the frozen production `ID4.80` source cutter, define independent
shaft-relative-to-fixed-disc offsets

```text
p_k=max(0,(ID_k_production_measured-OD_k_groove_measured)/2)
Q_LF(p_c)=connected component containing d_left=(0,0) of
  {d_left in R2 : exact groove transverse material is contained in the
   complete measured LF C-void transverse profile}
Q_RF(p_c)=connected component containing (d_right=(0,0),theta_RF=0) of
  {(d_right,theta_RF) in R2 x S1 : exact groove transverse material is
   contained in the complete measured transformed RF C-void transverse profile}
d_left in Q_LF(p_c)
(d_right,theta_RF) in Q_RF(p_c)
```

`p_left/p_right` are only concentric circular seed radii for numerical search;
they are not the admissible domains or acceptance prefilters. The exact
configuration spaces use the full C-mouth and relief geometry, so they may be
anisotropic and, on the right, rotation-dependent. No friction, preload, or
gravity constraint may select the concentric subdisk. `Q_LF/Q_RF` are strictly
local transverse journal/groove C-spaces derived from `p_c`; rod lanes, workpiece,
caps, tools, current-X axial shoulder/capture, and other mechanism collisions
are imposed later by the full
`A_p_c(x,theta)` and may reduce its feasible branch. They may not be smuggled
into a supposedly specimen-only `Q_*` definition.

Transform the left and right fixed-guide BREP systems by `d_left` and `d_right`
respectively relative to derived `C_shaft`; all plate-local origins, central
lands, grooves, journals, and inverse paths share that same source datum. The left fixed guide is the grounded
gauge at `theta_LF=0`. The right fixed guide has no anti-rotation feature, so
its full movable `theta_RF` must be solved through all three measured lane/rod
constraints on the same connected periodic branch; never freeze it at zero or
replace both sides by one common radial allowance. Dense samples of the
diagnostic concentric seeds, full C-mouth/relief boundaries, and periodic angle
may only seed the Section-4.2 certified constrained optimizer over the exact
connected `Q_LF x Q_RF` configuration space. Cross that domain with
the fixed specimen's measured production key-flank/roof clearance, lane
realization, and rod diameters, plus full movable `g_cam`, all four fixed-disc
axial endplay corners, the full `theta_RF` branch, every coupled
`(X_keeper,X_cam)` interval endpoint and interior optimum, whole
rod/subassembly axial shift, and each removable
right-cap float interval crossed with its complete periodic roll domain, plus
the seated keeper's complete measured offset/roll domain. Permanent
left-cap internal engagements remain frozen in `p_c`. At every joint case
evaluate cam translation/angle/backlash, local
key engagement, rod axial coverage/insertion, cap float without plate squeeze,
contact residuals, rod skew, rigid binding, the complete rotated right-fixed
C-mouth/material pose, both reverse-event predicates, solder-tool sweep, and
connector removal. Boundary-only sampling without interior optimization is
insufficient.

### 4.1.1 Frozen specimen data versus movable state

The coupled audit has two nested domains and may not morph one manufactured
specimen into another during motion. Write a fully instantiated LOCKED state as
`c=(p_c,x_c)`:

- `p_c` is the immutable specimen/manufacturing record. It contains the
  measured geometry/BREP realization and registration of all four plates and
  the integral shaft/rib/grooves; the selected production bore, rectangular
  keyway, journals, guide lanes and all profile/cutter deviations; each actual
  each admitted rod's measured exact centreline/profile BREP, diameter, length,
  endpoint frames, and straightness/tangent admission bounds;
  measured groove diameters and the diagnostic concentric clearance seeds
  `p_left/p_right/p_keeper`; cap/keeper geometry and
  elastic bounds; complete workpiece/ESC/tool envelopes and measured
  `Frame_ESC_ref`; verification that every admitted insulation OD is
  `<=wire_diameter_design`; and every other as-printed or
  purchased dimensional tolerance. Each discrete minus/nominal/plus lane case
  is a different `p_c`, not a time-varying coordinate. Diagnostic coupons are
  sensitivity data and never replace the production `p_c`.
- The three permanently pressed left-cap/rod subassemblies are also part of
  `p_c`: each actual left-cap socket realization and its final seated
  `q_L in [2.50,3.00]` are frozen after the physical press. That internal
  cap-to-rod engagement does not vary during jig motion or normal disassembly.
- `x` contains only coordinates that can move without changing manufactured
  material: commanded `theta_R`; left-cam pose
  `(d_cam_y,d_cam_z,theta_L)` within the fixed key-clearance BREP; assembly
  offsets `d_left/d_right` within exact connected C-space components
  `Q_LF/Q_RF`; right fixed
  guide angle `theta_RF` on its same connected periodic branch; seated keeper
  offset `d_keeper` and roll `alpha_keeper`; axial endplay coordinates
  `X_keeper`, both fixed-disc X positions, and `X_cam`;
  each measured rod's best-fit-axis coordinates `(b_i,k_i)`, whole
  rod/left-cap-subassembly axial shift `a_i`, and periodic roll `psi_i`; and
  each removable right-cap
  engagement `q_R_i` plus roll `alpha_R_i`. There is no catch-all movable coordinate: adding one
  requires a Gate-0 amendment to the frozen `A_p` equation census. The
  manufactured centres, eccentricities, profile errors, clearance radii, and
  left-cap internal `q_L_i` are not members of `x`.
- Assembly-only snap/press coordinates `z_J`, `z_rel`, the right-cap `q`
  portions outside its retained seated subrange, and left-cap manufacturing
  `q_L`, plus operation-test perturbation angle,
  keeper snap `z_rel`, insertion/removal lambda, and tool-sweep lambda, are auxiliary path/test
  coordinates in their named procedures. They are not free reverse-branch
  coordinates unless that procedure explicitly includes them. In particular,
  the left-cap manufacturing `q_L` is frozen into `p_c` before `Gamma(c)` is
  formed; only whole-subassembly axial motion may occur afterward.

The outer tolerance audit may enumerate many admissible specimen records
`p_c`. Every kinematic/global solve is then an inner solve over `x` for one
fixed `p_c`; extrema may be aggregated across specimens only after each
specimen's continuous certificate is complete.

Call one fully instantiated LOCKED point in this coupled domain `c`. First
separate kinematic admissibility and state validity from the two event
predicates. For the frozen specimen `p_c`, define the exact admissibility
predicate

```text
A_p_c(x,theta) = theta in [0,27 degrees]
    AND every coordinate of x lies in its frozen Section-4 domain
    AND every named equality, inequality, BREP-containment residual, and
        contact-mode rule in the frozen A-p equation census below is satisfied
```

`A_p_c` is not a loose bounds check. It contains the authoritative equations
for **every** movable coordinate classified in `x`; an arbitrary translation,
rotation, endplay value, rod motion, cap float, or contact-mode trace that
breaks any one of those equations is not an admissible state and cannot belong
to `Gamma(c)`. The implementation must serialize the named equation/residual
census and fail if a classified `x` coordinate is absent from it.

#### Frozen `A_p` equation and mode census

The implementation may not invent or weaken this census. Let the exact centre
and unit axis of physical uncut rod `i` be

```text
c_i = (a_i,b_iY,b_iZ)
sigma_i = sqrt(1 + norm(k_i)^2)
n_i = (1,k_iY,k_iZ)/sigma_i
n_iX = 1/sigma_i
C_i(ell) = c_i + ell*n_i,  ell in [-25.00,25.00]
X_left_tip_i  = a_i - 25.00*n_iX
X_right_tip_i = a_i + 25.00*n_iX
r_i(X) = b_i + k_i*(X-a_i)
W_i_nom = exact right circular ØD_i cylinder about C_i(ell), retained only as
          the nominal rendering/reference core
e_straight_i = certified maximum radial centreline departure from the best-fit
               line over ell in [-25.00,25.00], frozen in p_c and <=0.05
beta_straight_i = certified maximum angle between the measured local
                  centreline tangent and n_i, frozen in p_c and <=0.05 degrees
U_i(e_straight_i,beta_straight_i) = all exact uncut ØD_i x 50.00 rod solids
                    swept on a unit-speed centreline C_W(ell), ell in [-25,25],
                    whose distance to the best-fit line is <=e_straight_i,
                    whose tangent angle to n_i is <=beta_straight_i, and whose
                    planar end faces are normal to t_W(+/-25)
W_i_env = union over W in U_i(e_straight_i,beta_straight_i) of W
        = optional conservative rejection/precheck envelope only
frame_projection_min = 0.95, a named dimensionless P13Params admission field
F_hat_i(p_c) = immutable right-handed measured rod-local frame
             (o_hat_i,eX_hat_i,eY_hat_i,eZ_hat_i): o_hat_i is the midpoint of
             the measured best-fit-axis segment between the two registered end
             planes; eX_hat_i points from the left end plane to the right;
             eY_hat_i is the normalized projection of the metrology fixture's
             frozen +Y datum onto eX_hat_i's normal plane; eZ_hat_i is
             eX_hat_i cross eY_hat_i. Admission requires the projected +Y
             datum norm >=frame_projection_min, so no fallback branch exists.
W_hat_i(p_c) = the one measured exact rod BREP selected by immutable specimen
               p_c, expressed in coordinates of F_hat_i with o_hat_i=(0,0,0),
               eX_hat_i=(1,0,0), eY_hat_i=(0,1,0), eZ_hat_i=(0,0,1), and
               including registered local centreline/end frames
eX = (1,0,0)
v_i = eX cross n_i
q_i = eX dot n_i = n_iX > 0
K_i = skew_symmetric_matrix(v_i)
R0_i = I + K_i + K_i^2/(1+q_i)
       (the unique shortest-arc rotation eX -> n_i; q_i>0 excludes the
        antipodal singularity over the complete admitted skew domain)
psi_i in S1, represented continuously modulo 2*pi
Rroll_i(psi_i) = I + sin(psi_i)*[n_i]_x
                    + (1-cos(psi_i))*[n_i]_x^2
T_rod_i(z;x) = c_i + Rroll_i(psi_i)*R0_i*z
W_i(p_c,x) = {T_rod_i(z;x) : z in W_hat_i(p_c)}, with world centreline
             C_W_i(ell), tangent t_W_i(ell), and exact end faces
X_left_actual_i  = min_X(W_i(p_c,x))
X_right_actual_i = max_X(W_i(p_c,x))
```

Thus the transverse rod coordinates are exactly `(b_i,k_i)`, not independent
per-plate points. `a_i` is the X coordinate of the rod centre, `ell` is physical
rod arclength, and neither the world-X projection nor a skew-plane section may
replace the exact 50-mm nominal cylinder. Diameter and the measured conservative
straightness/tangent bounds and the measured exact rod BREP remain frozen in
`p_c`. The incoming-stock gate
measures maximum radial centreline departure and local tangent error and
requires `e_straight_i<=e_straight_max=0.05 mm` and
`beta_straight_i<=0.05 degrees`, but admission does not erase that
uncertainty. Each `W in U_i` is a different immutable outer-loop specimen
realization; its own exact rod-local `W_hat_i(p_c)`, placed `W_i(p_c,x)`,
lane/contact modes, cap endpoint frames,
and complete `Gamma(c)` are solved before extrema are aggregated. `W_i_env` may
reject a family early for conservative clearance, but it may never define
`A_p_c`, contact modes, path branches, or prove retention. `W_i_nom` is allowed
only in explicitly labeled nominal renders. No straightness realization may be
silently combined with, omitted from, or morphed inside skew/lane tolerance.
Because a round rod, round lanes, and round caps provide no anti-roll feature,
`psi_i` is unwrapped continuously from the LOCKED representative on every
periodic branch. Every `A_p_c`, `Gamma`, lane/contact, coverage, cap, tool,
removal, binding, and retention calculation certifies the complete `psi_i in
S1` domain; friction, gravity, or a favourable bow direction may not freeze it.
The exact zero-roll convention is `psi_i=0`, for which `eY_hat_i` maps to
`R0_i*eY`; source parity must prove `R0_i*eX=n_i`, this zero-roll transverse
datum mapping, orthonormality/determinant `+1`, and exact periodic closure
`T_rod_i(z;psi_i+2*pi)=T_rod_i(z;psi_i)` with continuous one-sided limits at
the chosen `S1` seam. No implementation-selected transverse gauge is allowed.
For each
plate `j in {LC,LF,RF,RC}` and rod `i`, let `L_ji(p_c,pose_j)` be that
specimen's exact transformed production lane-void BREP over the complete plate
thickness, and `M_j` the corresponding transformed plate material BREP. The
poses are `pose_LC=(X_cam,C_shaft+d_cam,theta_L)`,
`pose_LF=(X_fixed_left,C_shaft+d_left,0)`,
`pose_RF=(X_fixed_right,C_shaft+d_right,theta_RF)`, and
`pose_RC=(+17.45,C_shaft,theta_R)`. Here each tuple is `(X,YZ-origin,roll-X)`;
no plate or lane may retain an independent world `(0,30)` translation. The right actuator's circular stock/shaft may
be rotationally symmetric, but its three lane voids rotate by exactly
`theta_R`; no fixed-lane or omitted-pose convention is permitted. The left
fixed guide is the sole grounded angular gauge. `theta_RF` lives on `S1`, is
unwrapped continuously from the LOCKED value on each branch, and is constrained
only by all three exact `RF` lane equations plus global collision/contact
validity. No hidden right-fixed anti-rotation constraint is permitted. Freeze

```text
p_keeper=max(0,(ID_keeper_measured-OD_keeper_groove_measured)/2)
phi_K_transverse(d_keeper,alpha_keeper;p_c) = signed minimum 2D BREP
    clearance between the measured groove disk and the keeper's complete
    local C-void after only YZ translation d_keeper and roll alpha_keeper
Q_K(p_c)=connected component containing ((0,0),alpha_keeper=0) of
  {(d_keeper,alpha_keeper) in R2 x S1 :
   exact transverse keeper/groove material nonoverlap holds AND
   phi_K_transverse(d_keeper,alpha_keeper;p_c)>=0}
(d_keeper,alpha_keeper) in Q_K(p_c)
pose_K=(X_keeper,C_shaft+d_keeper,alpha_keeper)
K_world=transform(K,pose_K)
F_K_world=transform(F_K,pose_K)
E_K_rigid = volume(K_world intersection M_K_rigid) = 0
phi_K_groove = signed minimum BREP clearance(K_world,G_keeper_groove) >= 0
C_K_capture = exact current-X pilot/groove shoulder capture is true
mode_K_groove = FREE iff phi_K_groove>0 and lambda_K=0
                CONTACT iff phi_K_groove=0 and lambda_K>=0
lambda_K*phi_K_groove=0
```

Here `d_keeper` is the keeper-centre YZ offset relative to derived `C_shaft` and the shaft/groove
axis, and `alpha_keeper` is roll about world X, unwrapped continuously from the
LOCKED representative on each periodic branch. The measured nominal source
pair gives `p_keeper=(4.80-4.60)/2=0.10 mm`, but that is only a concentric
search seed, not the seated domain: the C-mouth/reliefs can admit anisotropic,
roll-dependent rigid travel beyond the seed circle. Every exact keeper mouth,
deforming subset, shoulder-blocking
test, collision solid, and seated-state BREP is transformed by `pose_K`; the
centred mouth-down auxiliary snap uses its separately declared Section-7 path
transform for `F_K/O_K`. Centred mouth-down seated geometry is a nominal view
only. There is no friction,
preload, gravity, or hidden anti-roll equation. The seated operational solve
must certify the complete exact connected `Q_K` component; the auxiliary
radial snap path in Section 7 must reach the centred seated state with its
transformed `F_K/O_K` exception, after which the recovered rigid-clear sweep
must connect that state to the complete admitted seated pose domain.
`M_K_rigid` is the exact union of every rigid mechanism solid other than the
keeper and the keeper-groove shaft surface, which is reported separately by
`phi_K_groove`; no
bounding-circle substitute may replace either BREP calculation or truncate
`Q_K`. Like the journal components, `Q_K` is local to the frozen transverse
keeper/groove geometry; `E_K_rigid`, current-X shoulder/capture, and all
rod/cap/workpiece/tool collisions are full-state `A_p_c` constraints applied
after component membership.
`phi_K_transverse` contains no `X_keeper`, `pose_K`, axial face, shoulder, or
other movable-state dependency. The separate full 3D `phi_K_groove` and
`C_K_capture` remain in `A_p_c` and may further reduce a branch.

Freeze

```text
E_lane_ji = volume(W_i(p_c,x) intersection M_j) = 0
phi_lane_ji = min over X in H_j of
    signed transverse YZ clearance(
        cross_section(W_i(p_c,x),X),
        lateral_YZ_boundary(cross_section(L_ji,X))) >= 0
mode_lane_ji = FREE     iff phi_lane_ji > 0 and lambda_lane_ji = 0
               CONTACT  iff phi_lane_ji = 0 and lambda_lane_ji >= 0
lambda_lane_ji*phi_lane_ji = 0
```

This exact full-thickness containment, evaluated on the skewed straight-rod
BREP, is the cam-slot/fixed-guide equation. For nonzero `k_i`, a world-X plane
cuts even the nominal right circular rod cylinder in an oblique ellipse-like
exact BREP, not an ØD disk; the exact measured-specimen
`cross_section(W_i(p_c,x),X)` is therefore mandatory for physical clearance.
`lateral_YZ_boundary` contains only the swept in-plane lane walls and
explicitly excludes both axial entry/exit faces of plate slab `H_j`;
equivalently `phi_lane_ji` is the certified minimum transverse clearance over
all exact rod/lane X sections in that slab. Axial rod coverage is owned only by
the separate `g_cover_*` inequalities below. This definition preserves real
lane slack and replaces any invented centreline equality in the physical
model. The nominal line-to-line audit still uses the exact `P_i(theta)`
equations from Section 4.1. Every combination of the 12 named lane modes that
belongs to the same connected solution component is a branch to continue or
reject explicitly.

The commanded and fixed-journal configuration-space residuals are

```text
E_command = theta_R-theta = 0
E_JL_material = volume(Groove_L intersection M_LF(pose_LF)) = 0
E_JR_material = volume(Groove_R intersection M_RF(pose_RF)) = 0
C_JL_capture = exact axial/radial shoulder capture is true
C_JR_capture = exact axial/radial shoulder capture is true
d_left belongs to Q_LF(p_c)
(d_right,theta_RF) belongs to Q_RF(p_c)
```

For every exact lateral C-void boundary contact, signed BREP clearance has mode
`FREE` when strictly positive and `CONTACT` when zero, with its own nonnegative
multiplier and `lambda*phi=0`. Material nonoverlap, capture, connected-component
membership, and every active boundary mode are all part of `A_p_c`. These are
the only independent fixed-disc YZ offsets; the transformed lane equations
above couple them to every rod. Diameter-derived `p_left/p_right` circles may
seed the solver but may not truncate either exact component.

For the left-cam keyed SE(2) pose, define exact signed BREP gaps
`phi_round`, `phi_flank_minus`, `phi_flank_plus`, and `phi_roof` between the
measured production bore/keyway and shaft/rib. Each is `>=0`; each rigid
contact uses the same two-mode rule `FREE iff phi>0, CONTACT iff phi=0` and
`lambda>=0, lambda*phi=0`. Also freeze

```text
ell_key = length([X_cam-1.25,X_cam+1.25]
                 intersection [-18.70,-16.20]) >= 2.20
E_key = volume(left_cam(pose_LC) intersection rigid_shaft_or_rib) = 0
```

where legal zero-volume tangency is not positive overlap. These four gaps,
`ell_key`, and `E_key` are the complete key/bore pose residuals; no coaxial,
fixed-phase, or line-to-line equation may be silently added to the physical
model.

Axial/endplay equations are exactly:

```text
g_FL_minus = X_fixed_left + 14.60 >= 0
g_FL_plus  = -14.40 - X_fixed_left >= 0
g_FR_minus = X_fixed_right - 14.40 >= 0
g_FR_plus  = 14.60 - X_fixed_right >= 0
g_K_minus  = X_keeper + 19.50 >= 0
g_K_plus   = -19.30 - X_keeper >= 0
g_KC       = X_cam - X_keeper - 1.75 >= 0
g_CF       = X_fixed_left - X_cam - 2.85 >= 0
```

Each named rigid axial gap has modes `FREE iff g>0, CONTACT iff g=0` and a
nonnegative multiplier satisfying `lambda*g=0`. Simultaneous opposite contacts
are allowed only when both exact gaps are zero; otherwise their mode pair is
one of `(FREE,FREE)`, `(CONTACT,FREE)`, or `(FREE,CONTACT)`. The fixed-disc,
keeper, and cam X coordinates have no other freedom or hidden preload rule.

For each rod `i`, define plate slabs

```text
H_LC=[X_cam-1.25,X_cam+1.25]
H_LF=[X_fixed_left-1.40,X_fixed_left+1.40]
H_RF=[X_fixed_right-1.40,X_fixed_right+1.40]
H_RC=[16.20,18.70]
```

and require for every `H_j=[H_j_minus,H_j_plus]`

```text
g_cover_ji_minus = H_j_minus - X_left_actual_i >= 0
g_cover_ji_plus  = X_right_actual_i - H_j_plus >= 0
```

The expanded old `a_i+/-25.00` expressions are forbidden when `k_i!=0`.
These eight inequalities per rod are the exact full-slot-thickness coverage
rule.

Let frozen permanent engagement `q_L_i in [2.50,3.00]` belong to `p_c` and
movable removable-cap engagement `q_R_i in [2.50,3.00]` belong to `x`. Both are
measured along physical rod arclength, not world X. Freeze the cap frames and
poses as

```text
alpha_R_i in S1
for W=W_i(p_c,x):
    Pminus_W=C_W_i(-25.00);  tminus_W=t_W_i(-25.00)
    Pplus_W =C_W_i(+25.00);  tplus_W =t_W_i(+25.00)
    eZminus_W=normalize(global_eZ-dot(global_eZ,tminus_W)*tminus_W)
    eZplus0_W=normalize(global_eZ-dot(global_eZ,tplus_W)*tplus_W)
    eYplus0_W=eZplus0_W cross tplus_W
    eZplus_W(alpha)=cos(alpha)*eZplus0_W-sin(alpha)*eYplus0_W
    eYplus_W(alpha)=eZplus_W(alpha) cross tplus_W
    C_Lopen_i(W)=Pminus_W+q_L_i*tminus_W
    C_Ropen_i(W)=Pplus_W-q_R_i*tplus_W
    T_Lcap_i(W)=frame(origin=C_Lopen_i(W), local_x=-tminus_W,
                      local_z=eZminus_W,
                      local_y=eZminus_W cross (-tminus_W))
    T_Rcap_i(W,alpha_R_i)=frame(origin=C_Ropen_i(W), local_x=+tplus_W,
                      local_z=eZplus_W(alpha_R_i),
                      local_y=eYplus_W(alpha_R_i))
    Cap_L_i(W)=transform(Cap_L_local,T_Lcap_i(W))
    Cap_R_i(W)=transform(Cap_R_local,T_Rcap_i(W,alpha_R_i))
    E_Rcap_rod_i(W)=volume(Cap_R_i(W) intersection W)=0
    E_Lcap_plate_i(W)=volume(Cap_L_i(W) intersection M_LC)=0
    E_Rcap_plate_i(W)=volume(Cap_R_i(W) intersection M_RC)=0
    phi_Lcap_plate_i(W)=signed minimum BREP clearance(Cap_L_i(W),M_LC)>=0
    phi_Rcap_plate_i(W)=signed minimum BREP clearance(Cap_R_i(W),M_RC)>=0
```

`q_R_i` mode is `LOW` at `2.50`, `FLOAT` strictly inside, and `HIGH` at
`3.00`; it has no invented friction or complementarity force. Each
`phi_*cap_plate_i` uses the rigid FREE/CONTACT rule and its own
`lambda>=0,lambda*phi=0` only for cap-to-plate squeeze. The exact BREP residuals
include the complete tilted OD7 body and cap end plane; scalar open-face X gaps
are forbidden. Every residual uses the immutable measured endpoint position
and tangent of `W_i(p_c,x)`; the outer audit repeats for every admitted
`W in U_i`, while nominal `C_i(+/-25),n_i` cap placement is render-only. The
left cap remains rigidly united with its rod through fixed
`q_L_i`; there is no independent left-cap pose. Its unslitted coaxial local
BREP is exactly rotationally symmetric about each actual endpoint tangent, so
left-cap roll is a
proven geometry quotient rather than a hidden constrained coordinate. The
right-cap world pose is
determined by `T_Rcap_i`; its only additional pose freedom is the declared
`alpha_R_i`, unwrapped continuously from the LOCKED representative on each
periodic branch. Because a round rod and round cap socket provide no
anti-rotation feature, every cap-to-rod, cap-to-plate, cap-to-mechanism, tool,
and removal test must certify the complete `alpha_R_i in S1` domain.
`alpha_R_i=0` makes the slit projected-up and is a nominal view only. There is
no friction, gravity, or hidden cap-roll constraint in CAD. The exact actual
rod/cap positive intersection must remain empty in each roll state; a locally
evaluated or frozen-up slit is a hard failure.

Rigid complementarity is restricted to the lane walls, recovered seated
journal/keeper rigid contacts, shaft/bore/key contacts, axial groove/land
contacts, and cap-to-plate squeeze gaps named above. It is **not** applied to
intentional nominal-source interference. For every elastic exception
`E in {E-JL,E-JR,E-K,E-LP1..3}` with its exact Section-7/9 trajectory
coordinate `eta_E`, interval `I_E`, deforming BREP `F_E`, permitted overlap
`O_E(eta_E)`, and displacement bound `u_E`, freeze the accommodated-contact
rule

```text
eta_E in I_E:
    actual_nominal_source_intersection(E,eta_E) = O_E(eta_E)
    O_E(eta_E) subset F_E
    displacement(E) <= u_E
eta_E outside I_E:
    actual_nominal_source_intersection(E,eta_E) = empty
```

Equality/subset tests use the Section-9 `1e-7 mm3` BREP tolerance. Specifically
`I_J=[0,22.188190922871]`, `I_K=[-5.877708764000,0]`, and
`I_LP=(0,3.00]`. For the left press cap, `q_L=0`
belongs exclusively to rigid approach/tangency and has empty positive
intersection; elastic accommodation starts only at `q_L>0`. The exact `O_*`,
`F_*`, displacement components, and bounds are those already frozen in
Sections 7 and 9. In normal `Gamma(c)`
operation, auxiliary journal/keeper assembly coordinates are frozen at their
seated states, each `q_L_i` is frozen in `p_c`, and only `q_R_i` may vary.
Nominal negative gap inside an allowed `O_*` is never passed through rigid
`gap>=0` complementarity. If a future implementation uses post-deformation
contact complementarity, it must first return to Gate 0 with an exact deformed
geometry map; none is authorized here.

For any mechanism state `g=(p_c,x)`, define

```text
V(g) = A_p_c(x(g),theta_R(g))
       AND every positive overlap is either a legal rigid contact
           or contained in one named Section-9 exception BREP
       AND no rigid mechanism bind exists
       AND all declared material/collision/operation constraints are feasible
       AND g belongs to at least one connected A_p_c-feasible branch

R(g) = contact_normal_matrix_positively_spans_YZ(g)
       AND for every Section-10 linear perturbation:
             max_rod_geometric_incursion >= 0.02
       AND for every Section-10 rotational perturbation:
             (max_positive_rod_overlap > 1e-7 mm3
              OR minimum_signed_clearance <= -0.02 mm)

C(g) = theta_R(g)=0
       AND V(g)
       AND all three exact reverse right-cap removal sweeps are clear
       AND the synchronous three-rod/left-cap -X withdrawal sweep is clear
       AND after caps and rods are off,
           volume(E_remove_full(g) intersection
                  assembled_four_plate_shaft_keeper(g)) <= 1e-7 mm3
```

`R(g)` and `C(g)` are defined only on states satisfying `V(g)`. `R` is only the
frozen geometric retention predicate and contains no validity or `+Z` removal
term. `C` is only the complete Section-8 OPEN preparation plus full-workpiece
`+Z` removal-clearance/reachability predicate and contains no retention
perturbation. It is false before OPEN: cap removal or rod withdrawal before a
valid commanded `theta_R=0` is forbidden. Its cap and rod motions are named
auxiliary paths after `Gamma`; they do not alter the preceding same-branch
reverse lift or smuggle disassembly coordinates into `x`.

Because clearance/endplay variables mean one connected component need not
select one unique reverse trajectory, do not invent a deterministic
`gamma_c`. Define `Gamma(c)` as **all maximal physically admissible,
constraint-consistent reverse lifts**
`gamma:[0,T_gamma]->state`, `0<=T_gamma<=27`, satisfying:

- `gamma(0)=c` and `theta_R(gamma(tau))=27 degrees-tau`;
- `p(gamma(tau))=p_c` everywhere; only `x(gamma(tau))` may vary;
- `A_p_c(x(gamma(tau)),theta_R(gamma(tau)))` holds for every `tau` in the
  complete **closed** domain `[0,T_gamma]`, including the endpoint;
- the lift remains on the same connected `A_p_c` solution branch anchored at
  `c`; and
- it is maximal on that branch: if `T_gamma<27`, no positive-epsilon continuous
  extension exists that preserves the preceding bullets and `A_p_c`.

Branch jumps and arbitrary equation-breaking `x` traces are forbidden. A
nonmaximal prefix is not a member of `Gamma(c)`; branch termination is a
feasible branch endpoint at maximal `T_gamma<27` with no positive-epsilon
same-branch `A_p_c`-consistent extension. A non-admissible limit, if useful for
diagnostics, is reported separately and is never a point of `gamma`. Samples
cannot stand in for this quantified family of maximal lifts.

For each `gamma in Gamma(c)`, define its validity horizon and the two separate
first-event sets:

```text
h_V(gamma) = sup {h in [0,T_gamma] :
                  V(gamma(tau)) for every tau in [0,h]}

OPEN_REACHED(gamma) = (T_gamma = 27)

OPEN_VALID(c,gamma) = V(gamma(27))  if T_gamma = 27
                      false         if T_gamma < 27

PATH_VALID_THROUGH_OPEN(c,gamma) =
    OPEN_REACHED(gamma)
    AND (h_V(gamma) = 27)
    AND OPEN_VALID(c,gamma)

S_loss(c,gamma) = {tau in [0,h_V] :
                   V(gamma(tau)) AND NOT R(gamma(tau))}
S_clear(c,gamma) = {tau in [0,h_V] :
                    V(gamma(tau)) AND C(gamma(tau))}

tau_loss(c,gamma) = inf S_loss(c,gamma)
theta_loss_of_retention(c,gamma) = 27 degrees-tau_loss(c,gamma)

tau_clear(c,gamma) = inf S_clear(c,gamma)
theta_removal_clear(c,gamma) = 27 degrees-tau_clear(c,gamma)
```

Both first-event brackets include their limiting contact state only when that
state satisfies `V`. `OPEN_REACHED` is mandatory because a maximal admissible
branch may end at `T_gamma<27`. The separate Boolean `OPEN_VALID` is mandatory
because `h_V=27` can still be the supremum when every `tau<27` is valid but
OPEN itself is invalid. `PATH_VALID_THROUGH_OPEN` is an independent mandatory
path acceptance, not an event status: Gate 0 fails for every maximal lift with
`T_gamma<27`, `h_V<27`, or `NOT OPEN_VALID`, even when retention loss or
removal clearance was reached earlier on a valid prefix. A reached event never
masks later branch termination or path invalidity.

If an event set is empty and `PATH_VALID_THROUGH_OPEN` is false, return
`UNREACHED_BRANCH_INVALID`. For `T_gamma<27`, report terminal
`theta_R=27-T_gamma`, certify that the endpoint itself satisfies every
`A_p_c` equation, and provide a one-sided continuation bracket immediately
beyond it proving no same-branch `A_p_c` solution exists; name the blocking
equation, complementarity mode, or branch-existence condition. That attempted
extension is diagnostic and is not part of `gamma`. For a lift reaching
`T_gamma=27` but losing `V` earlier,
report terminal `theta_R=27-h_V`; for endpoint-only invalidity report terminal
`theta_R=0`. The latter two cases include a certified one-sided terminal
validity bracket and first named failing `V` condition. Every terminal bracket
has width `<=0.001 degree`, certifies the admissible/valid prefix through its
lower-tau side, and ends at the failing side; for endpoint-only failure its
upper-tau endpoint is exactly `tau=27`.
Return `UNREACHED_AT_OPEN` only when the event set is empty and
`PATH_VALID_THROUGH_OPEN` is true. Never evaluate beyond `T_gamma`, `tau>27`,
or `theta_R<0`. A maximal zero-length lift is
`UNREACHED_BRANCH_INVALID`, not an event.

Every disconnected LOCKED component is analyzed independently. For each `c`,
report earliest/latest event angles over **all** `gamma in Gamma(c)`, every
attaining path certificate, both unreached status sets, continuity/jumps, and
branch identity. Independently report `PATH_VALID_THROUGH_OPEN` for every path,
including its terminal invalidity certificate when false. Then report separate
global extrema over all `(c,gamma)` for retention loss and removal clearance.
Gate 0 fails if either event is unreached on any admissible path **or** any path
has `PATH_VALID_THROUGH_OPEN=false`. The two event quantities may not be merged
into one release scalar, computed from one arbitrarily selected path, or used
to waive the independent full-path validity gate.

The concentric circular seed radii provide only this diagnostic comparison:

```text
L_min = 28.80
p_left+p_right <= L_min*tan(0.05 deg)
                   = 0.025132747609 mm
```

This is a combined comparison, not `0.02513 mm` per journal, and is neither a
necessary nor sufficient acceptance rule for the full C-shaped journal
components: mouth/relief directions can extend beyond each `p_k`. The exact
`Q_LF x Q_RF` optimizer and certified rod-axis extrema alone determine
acceptance. Nominal CAD uses
`p_left=p_right=0`. The production source remains exactly `ID4.80`.
`ID4.85/4.90` coupons are diagnostic only and cannot become production from
this seed comparison; any diameter change requires source regeneration,
renewed geometry/intent review, and a new Gate-0 decision.

No `<=0.10 degree` physical cam-phase/backlash claim is active. Physical
acceptance remains blocked until the as-printed production keyway is measured,
the audit derives its bound, the full coupled optimizer accepts the measured
journal offsets, and assembled rod skew is `<=0.05 degrees`. A very
small integral preload leaf may be studied in a later prototype only; it is not
part of P13 allowed stock, cutters, BOM, or acceptance evidence.

### 4.2 Why this candidate is accepted

The exploratory design audit sampled pose at `0.1 degree`, solved path roots
initially at `0.01 degree`, then refined every root numerically. Its `813`
pose/root cases are regression seeds and visualization coordinates only, not a
global proof. Their candidate values were:

- number of valid guide/cam intersections at every case: exactly `1`;
- minimum absolute kinematic Jacobian determinant after the P21 pivot shift:
  `2.053627355414 mm`, which must remain `>=2.00 mm` under the exact nominal
  continuous solve;
- minimum guide/cam path crossing angle after the P21 pivot shift:
  `5.938027856 degrees`, which must remain `>=5.00 degrees` under the exact
  nominal continuous solve;
- minimum cam-path centre separation: `7.659821686 mm`;
- nominal right follower cam-lane web:
  `7.659821686-4.75 = 2.909821686 mm`;
- nominal left datum cam-lane web:
  `7.659821686-4.75 = 2.909821686 mm`;
- with both independently dilated lanes, tolerance-minimum inter-lane web:
  `7.659821686-4.75-2*0.353553391 = 2.202714905 mm`;
- maximum path-centre radius from derived `C_shaft`:
  `15.249753922059 mm`.

Every implementation must rerun those regression seeds from source geometry,
then replace sampling as acceptance evidence with one of these reproducible
continuous certificates over the complete `theta_R in [0,27 degrees]` and
Section-4 physical configuration domain: (a) exact continuous swept BREP for a
motion/collision claim; or (b) bracketed interval branch-and-bound/global
minimization whose reported lower and upper bounds contain the true extremum.
Samples may seed the solver and make plots, but may not close a gate.

For every length, separation, signed-clearance, web, residual, tool-access,
binding, retention, or removal-clearance extremum, terminate refinement only
when the certified global bracket width is `<=eps_global=0.005 mm`, strictly
smaller than the controlling `0.042893219-mm` eroded-lane clearance. Angular
event/root brackets must be `<=0.001 degree`; exact nominal kinematic equalities
retain their separately stated `1e-9` tolerances. Every report records the
complete domain box/branch, lower and upper bound, attaining interval, and
convergence status. Nonconvergence, an uncovered interval, or a branch found
only at a sampled point is a failure. This continuous-certificate rule applies
to every later physical-domain collision, tool, binding, retention, and both
release-event claims even when a section also names convenient sample poses.

### 4.3 Conservative centre-clearance stroke construction

The common stroke is derived from a deliberately conservative 2D centre
clearance construction, not from the exact-solid removal sweep. An uninflated
exact payload is merely tangent to a locked rod, so the infimum of a simple
"no positive intersection" solve would be zero and cannot define the required
opening stroke.

In YZ define the semi-infinite nominal passage set and its forbidden rod-centre
envelope:

```text
K = [-4.25,+4.25] x [34,+infinity)
r_rod = 2.00
m_clear = 0.75
eps_follower = sqrt(0.25^2+0.25^2) = sqrt(2)/4
             = 0.353553390593
rho = r_rod + m_clear + eps_follower
    = 3.103553390593
K_forbid = K Minkowski-summed with a closed disk of radius rho
```

For each straight guide, define the required retraction as:

```text
S_i_req = min { d >= 0 : P_i_locked-u_i*d lies on or outside
                         the exterior boundary of K_forbid }
S_req = max_i(S_i_req)
```

The boundary arithmetic from the frozen coordinates is reproducible directly:

```text
upright:
  S_u = (-4.15) - (-4.25-rho)
      = 0.10 + rho
      = 3.203553390593

bottom:
  P_bottom_locked=(12.00,25.85) is already exterior to K_forbid
  S_b = 0

diagonal:
  opening adds d/sqrt(2) to both Y and Z
  delta_Y = (4.25+rho) - 4.691852455
          = 2.661700935593
  S_d = sqrt(2)*delta_Y
      = 0.5 + 2.308147545*sqrt(2)
      = 3.764213562097

S_req = max(S_u,S_b,S_d) = 3.764213562097
S = 3.764213562 mm in the frozen parameter set
```

The diagonal rod controls the common stroke. Source tests must recompute these
values from the coordinates and named allowances; they may not compare only to
hard-coded expected decimals. Moving `C_shaft` changes inverse cam paths and
plate/rim geometry but not the task-fixed `P_i_locked`, guide directions,
workpiece envelope, or centre-clearance construction; source must nevertheless
recompute all three `S_i_req` and prove the same controlling
`S=3.764213562097` rather than copying it. The exact payload BREP and its `+Z` sweep remain
a separate continuous collision/retention/removal-clear validation in Sections
8, 10, I10, and I11. The candidate comparison is:

| candidate | C | S | rise/dwell | raw OD consequence | disposition |
|---|---:|---:|---:|---:|---|
| inherited P9/P11 | `(-7.5,32.5)` | `11.0` | `0..70 / 70..80` | `~64 mm` | rejected: oversized and not clearance-derived |
| first P13 shaft guess | `(0,30)` | `3.764213562` | `0..22 / 22..27` | `40.2067 mm` raw | rejected: insufficient task-specific shaft/workpiece derivation |
| audited P13/P21 | derived `(-2.096372645,27.903627355)` | recomputed `3.764213562` | `0..22 / 22..27` | `39.9566 mm` minimum at 2.0-mm tolerance rim; `40.50 mm` stock retained | accepted pending complete-domain certificates |

## 5. Plate diameter, webs, shaft clearance, and topology budget

All straight and inverse moving lanes are frozen at `4.75 mm`; the left datum
cam retains a `4.40 mm` endpoint pocket only through the no-motion dwell. The
right side supports but does not establish locked YZ.

The conservative isotropic profile allowance is
`eps=sqrt(0.25^2+0.25^2)=0.353553390593 mm`. The frozen tolerance-case minimum
rim is `m_rim_min=2.00`; the source derives, rather than copies, the complete
continuous maximum path-centre radius from `C_shaft`:

```text
R_path_max = max_i,theta norm(P_i(theta)-C_shaft)
           = 15.249753922059
D_required_raw = 2*(R_path_max + 4.75/2 + eps + m_rim_min)
               = 39.956614625304 mm
D_required_rounded = ceil(D_required_raw/0.5)*0.5 = 40.00 mm
D_plate     = 40.50 mm frozen stock OD
```

At OD40.50 the nominal pivot-to-lane rim web is exactly
`20.25-15.249753922059-2.375 = 2.625246077941 mm`; after the complete isotropic
profile allowance it is `2.271692687348 mm`, above `m_rim_min=2.00`. The
continuous full-domain source certificate must use actual swept lane BREPs and
prove every plate's minimum rim web `>=2.00 mm`; these decimals are regression
seeds, not sampled acceptance. With minimum centre separation
`7.659821686`, two 4.75 lanes have nominal web `2.909821686 mm`; when both
independently dilate by eps the minimum is `2.202714905 mm`, above the frozen
`2.00 mm` limit. Every plate remains one connected positive-volume solid.

### 5.1 Derived-pivot clearance and concentric-regeneration contract

All plate stock and cutters are authored in one YZ-local frame whose origin is
the shaft axis, then placed at `C_shaft`. This includes every OD40.50 circle,
central land/bore, fused shaft and its grooves/rib, both fixed C-journals,
keeper/groove, straight-guide lanes, generated inverse cam lanes `Q_i`, and
every pivot-relative path or evidence camera. Changing a primary input to the
Section4 pivot formula must translate/regenerate all of those declared
dependents concentrically. It must not translate or rotate the world-fixed
workpiece centreline, three `P_i_locked` contact centres, guide normals, ESC
joint references, or tool targets. The common stroke is independently
recomputed from those task-fixed quantities and must not be copied from a
previous manifest.

Let `M_shaft(p_c,theta)` be the exact world BREP of the complete fused shaft
material, including its actual grooves and rotating local rib but excluding
voids. Let `W_complete(p_c)` be the full connected completed workpiece from
Section8, not the former connector-only payload. Freeze these named clearance
parameters in `P13Params`:

```text
c_sw = 0.50                 shaft-to-full-workpiece minimum
c_shaft_rod_min = 0.50      shaft-to-each rod minimum
c_shaft_tool_min = 0.50     shaft-to-each non-contact iron region minimum
c_shaft_frame_min = 0.50    shaft-to-measured FPV-frame/ESC reference minimum
m_rim_min = 2.00            tolerance-case lane-to-plate-rim minimum
```

For every `theta in [0,27 degrees]`, every immutable specimen `p_c`, and the
complete admissible same-branch movable state `x`, continuously certify:

```text
phi_shaft_workpiece = clearance(M_shaft,W_complete) >= c_sw
phi_shaft_rod_i     = clearance(M_shaft,W_i(p_c,x)) >= c_shaft_rod_min
phi_shaft_tool_k    = clearance(M_shaft,Iron_k_noncontact_sweep) >=
                      c_shaft_tool_min
phi_shaft_frame     = clearance(M_shaft,Frame_ESC_ref(p_c)) >=
                      c_shaft_frame_min
g_rim_j             = minimum exact lane-wall-to-OD40.50-rim web in plate j
                      >= m_rim_min
```

`Frame_ESC_ref(p_c)` is a measured nonstructural reference BREP in the
specimen record. A bounded provisional frame envelope may be used only for an
explicitly labeled exploratory CAD run; final frame-clearance acceptance
remains blocked until the real frame/ESC envelope is measured and the full
certificate is regenerated. Intentional fused shaft/right-cam material and
declared shaft/bore/journal/keeper contacts are not misclassified as
shaft-to-frame collisions; `Frame_ESC_ref` means only the external FPV
assembly. Every clearance is an exact BREP/global certificate over the full
domain, not the nominal 2D seed. The nominal shaft/workpiece result is exactly
`c_sw`, the nominal shaft/nearest-lane rim web is
`2.625246077941 mm`, and all tolerance/coupled states must still satisfy their
frozen lower bounds.

The parameter dependency graph must include the complete chain
`shaft_od/wire_diameter_design/c_sw/R_bend/bend_center/horizontal_z ->
d_arc0/delta_pivot/C_shaft -> Q_i/plate poses/plate stock/shaft/grooves/rib/
journals/keeper/lanes/rim/tool-frame-clearance tests/evidence/exports`.
Fresh-process safe-retune metamorphic tests perturb `c_sw`,
`wire_diameter_design`, and one measured profile/tolerance input separately,
plus one coupled `c_sw+wire_diameter_design` pair, regenerate all derived
BREPs/STEP, and prove concentric dependents follow the formula while task-fixed
contacts remain invariant. Separate noncandidate dependency tests perturb
`shaft_od` and `R_bend` and prove coherent regeneration while explicitly marking the
outputs `RE-GATE REQUIRED`; those artifacts cannot enter the accepted export
set. Any stale `(0,30)` transform, independently moved
plate, hand-shifted lane, or hard-coded output coordinate fails P13.

There is no retained-area strength claim. Strength remains physical. Topology
is instead controlled by an exact allowed-stock envelope and cutter census:

```text
A_blank = pi*(40.50/2)^2 = 1288.249337513 mm2
fixed allowed stock = OD40.50 x 2.80 blank
                    union one OD10 annular thrust land x 0.20
left-cam allowed stock = OD40.50 x 2.50 blank
right-actuator allowed stock = OD40.50 x 2.50 cam blank
                              union one round OD5.60 shaft cylinder
                              from X=-21.00..+16.20
                              union one local rectangular key-rib prism
                              from X=-18.70..-16.20
```

The fixed-land inner boundary is a round `ID5.70` running clearance around the
rotating `OD5.60` shaft; the main fixed blank retains the exact upward
`ID4.80` C-journal around its dedicated `OD4.60` journal station. The cam-side
land is omitted. All protruding volumes are therefore computed from source
profiles. A C-journal lies inside the 2.80-mm blank and adds no external stock.

Exact permitted cutters are:

- each fixed plate: three straight guide-lane swept cutters and exactly one
  independently reproducible upward C-keyhole cutter in plate-local YZ:
  `D=circle(center=(0,0),r=2.40)` and
  `T=box(Y=-2.10..2.10,Z=0..20.25)`. Their exact upper intersections are
  `(Y,Z)=(+/-2.10,z_t)`, where
  `z_t=+sqrt(2.40^2-2.10^2)=+1.161895003862`. Add exactly two stress-relief
  cutter circles `R=1.00` centred at those intersection points. The final
  zero-width rim slivers are removed by the exact top-cap cutter
  `B = circle(center=(0,0),r=20.25) intersection {Z>=z_tip}`, where

  ```text
  z_tip = +sqrt(20.25^2-(2.10+2.20)^2)
        = +19.788190922871
  cap depth = 20.25-z_tip = 0.461809077129
  ```

  The final profile is
  `C_key=D union T union relief_left union relief_right union B`, extruded
  through 2.80 mm. `T` overlaps both `D` and `B`, so the cutter is connected.
  At the intentional flat edge `Z=z_tip`, the retained left and right free-tip
  intervals are exactly `[-4.30,-2.10]` and `[2.10,4.30]`, each `2.20 mm` wide.
  No vague auto-fillet, trapezoid, offset, extra relief, or zero-width material
  sliver is permitted;
- left cam: three generated inverse-lane swept cutters and exactly one keyed
  centre cutter equal to the union of a coaxial round `ID5.70` bore and the
  Section 7 nominal line-to-line rectangular keyway (`|v|<=0.75`, tangential
  width `1.50`; `2.50<=u<=3.50`, radial roof `u=3.50`) through its 2.50-mm
  thickness. This is the only production centre cutter. `ID5.60/5.80`,
  alternate keyway widths, and alternate roofs are diagnostic coupon geometry
  only; changing any nominal source dimension requires source regeneration and
  renewed Gate-0 intent/geometry review;
- right actuator: three generated inverse-lane swept cutters and one shallow-D
  centre cutter equal to the accepted-amendment `OD5.70 / AF5.25` bore. It has
  an outward `OD10 x 2.0 mm` hub and no integral shaft, rectangular key/rib,
  or full-length key;
- no other hole, pocket, lightening cut, projection, or additive body.

Tests compare each final principal solid with
`allowed_stock minus union(allowed_cutters)` using symmetric-difference volume
`<=1e-6 mm3`. Thus an extra decorative hole cannot pass by merely reducing net
area or volume.

Minimum path-centre radius occurs at the diagonal locked point:

```text
r_path_min = norm(P_diagonal_locked-C_shaft)
           = 9.600000000000
lane half-width = 2.375
common allowances:
  lane dilation eps = 0.353553390593
  path residual = 0.020000000000
  maximum 29.20-span skew translation = 0.025481813548

right actuator central shaft, radius2.80:
  nominal = 9.60-2.375-2.80 = 4.425000000000
  after common allowances = 4.025964795859

left cam round ID5.70 bore, radius2.85 (controlling production geometry):
  nominal = 9.60-2.375-2.85 = 4.375000000000
  after common allowances = 3.975964795859

fixed plate C-journal / seated groove surface, radius2.40:
  nominal = 9.60-2.375-2.40 = 4.825000000000
  after common allowances = 4.425964795859
  physical side k = 4.425964795859-p_k

diagnostic left-cam ID5.80, radius2.90:
  after common allowances = 3.925964795859
```

The nominal assembly-wide controlling central clearance is therefore the left
cam's `3.975964795859 mm`, not the right actuator's `4.025964795859 mm`.
`ID5.80` remains a diagnostic coupon because `ID5.70` is the frozen production
architecture, not because the new pivot makes it fail radial clearance; using
it in production still requires source regeneration and renewed Gate-0 intent
review. For each
fixed side, the selected measured `p_k` from Section 4 is substituted into its
own expression; no common or unmeasured radial free motion may be silently
assigned zero.

The local key is deliberately placed opposite the closest diagonal path.
Using Section 7 coordinates, the exploratory dense/refined audit produced the
candidate minimum motion-path-centre distance to the nominal keyway rectangle
`8.710988567945 mm`, hence nominal keyway-to-lane material web
`8.710988567945-2.375=6.335988567945 mm`. Even the largest declared keyway
coupon envelope (`u<=3.60`, `|v|<=0.85`) gives `6.310554149820 mm`, or
`5.957000759227 mm` after simultaneous lane dilation by `eps`. The coaxial
round-bore/shaft corridor, not the local keyway, remains the controlling radial
clearance. Source tests must recompute and continuously certify these global
values under Section 4.2 rather than trust decimals or the sampled audit.

## 6. Reproducible profile tolerance and assembly skew

Two models must not be conflated:

1. **Cutter/profile-offset model.** For each nominal YZ lane cutter `L_j`, make
   reproducible solid variants before X extrusion:
   `L_j_plus=L_j Minkowski-summed with disk(eps)` and
   `L_j_minus=L_j eroded by disk(eps)`. Each of the three lanes varies
   independently among minus/nominal/plus, giving `3^3=27` combinations per
   plate and pose. Dilation is worst for rim/web/shaft clearance; erosion is
   worst for rod fit. These offsets preserve the ideal centreline and create
   no rod skew.
2. **Assembly-skew model.** Relative right-plate centreline translation and
   rotation are tested using the exact independent Section-4 connected
   C-space components, never one scalar offset or diameter-derived disk. At
   minimum span `L_min=28.80`, the concentric-seed diagnostic is
   `p_left+p_right<=28.80*tan(0.05 deg)=0.025132747609 mm`; the complete BREP
   optimizer must demonstrate rod axes within `0.05 degrees` over all of
   `Q_LF x Q_RF`. This inequality is neither necessary nor sufficient for the
   C-shaped components and cannot replace the full optimizer. A
   `0.25 mm` centreline translation, or a nominal-diameter coupon label without
   measured `p_k`, is not claimed compatible with the physical model.

Nominal reconstruction residual is `<=0.02 mm`; nominal rod skew is zero.
Every 4.75 lane clears nominal Ø4 by `0.75 mm` diametrically. Full erosion gives
`4.75-2*eps = 4.042893219 mm`, retaining `0.042893219 mm` diametric CAD
clearance. That proves only analytic feasibility at the frozen tolerance
bound; actual rod diameter, FDM hole shrinkage, surface roughness, and sliding
fit remain physical coupon acceptance. Same-orientation coupon widths are
`4.55/4.65/4.75 mm`; changing the production lane needs renewed review because
it changes web and shaft-clearance margins. The independently varied left/right
lane cases also feed the Section 4 `theta_L` feasible-set audit. Physical
acceptance requires the selected assembled fit to measure rod-axis skew
`<=0.05 degrees`; nominal CAD alignment cannot substitute for that result.

## 7. Superseded integral-actuator design history

This section records the rejected integral-shaft design and is non-normative.
The accepted split-shaft dimensions, service sequence, and bounded mobility are
defined by `docs/p13-cad-source-domain-amendment.md`; no prohibition against
the accepted separate shallow-D shaft survives this supersession.

The text below is retained solely so historical review findings remain
traceable.

- Right actuator: circular cam plate `X=16.20..18.70` plus integral coaxial
  round `OD5.60` shaft from `X=-21.00..+16.20`, fused as one connected solid.
  The user grips and rotates the `OD40.50` cam rim. There is no input head,
  decorative handle, D-flat, D-bore, or full-length keyed envelope.
- Local positive phase key: in shaft-centred YZ coordinates define unit vectors
  `e_r=(-1/sqrt(2),-1/sqrt(2))` and
  `e_t=(+1/sqrt(2),-1/sqrt(2))`, then `u=p dot e_r`, `v=p dot e_t`. The single
  rectangular rib is exactly `2.50<=u<=3.50`, `|v|<=0.75`, and
  `X=-18.70..-16.20`; it overlaps the OD5.60 shaft and is part of the right
  actuator solid. The left cam has the union cutter `round ID5.70 bore union
  {2.50<=u<=3.50, |v|<=0.75}` through its full axial thickness. Nominal rib and
  keyway flanks are line-to-line. This local zone ends `0.20 mm` before the
  left fixed-journal groove starts at `X=-16.00`; it starts `0.10 mm` after the
  keeper groove ends at `X=-18.80`. It shares only the boundary plane
  `X=-16.20` with the left-cam inner main face and creates no positive overlap
  with either groove or keeper.
- Keyed left cam: nominal centre `X=-17.45`, thickness `2.50`; this centre is
  used only for nominal CAD. Physical states use the exact coupled
  `X_cam` interval from Section 4 and the full SE(2) cross-section pose. It
  slides from the free LEFT shaft end, passes only round shaft/keeper-groove
  sections, then its keyway engages the local rib at `X=-18.70`; it never
  traverses the rib as an undersized round bore. The production bore/keyway fit
  is the measured as-printed result of the frozen production `ID5.70`,
  width-1.50, roof-3.50 cutter; diagnostic alternatives cannot replace it.
- Two dedicated fixed-disc locating grooves are cut into the integral shaft:
  root `OD4.80`, width `3.00`, centres `X=-14.50,+14.50`. In nominal CAD the
  seated fixed-journal ID is also `4.80`, so radial free motion is zero and the
  coaxial shaft may rotate at tangency without positive BREP overlap. Radial
  shoulder capture is `(5.60-4.80)/2=0.40 mm`.
- Left keeper groove: root `OD4.60`, width `1.20`, centre `X=-19.40`, spanning
  `-20.00..-18.80`. The round C-keeper axial thickness is `1.00`; it can occupy
  `X=-20.00..-19.00` through `-19.80..-18.80`. Its exact local YZ BREP is
  frozen below. Relative to the left-cam outer face at `X=-18.70`, its
  geometric restraint gap is `0.10..0.30 mm` only at nominal
  `X_cam=-17.45`. Physical tests instead vary `X_keeper=-19.50..-19.30` and
  enforce `X_cam>=X_keeper+1.75`; they report keeper contact/noncontact and no
  assumed preload.
- Keeper local coordinates are centred on its seated shaft axis with opening
  toward `-Z`. Start with stock disk `K0=circle(R=4.80)`. Define inner cutter
  `K_D=circle(R=2.40)`, mouth
  `K_T=box(Y=-2.00..2.00,Z=-4.80..0)`, and exact inner intersections
  `(Y,Z)=(+/-2.00,-1.326649916142)`. Add exactly two relief cutters
  `circle(R=0.60)` centred at those intersections. To avoid zero-width tips,
  define `z_k_tip=-sqrt(4.80^2-(2.00+1.20)^2)=-3.577708764000` and
  `K_B=K0 intersection {Z<=z_k_tip}`. The keeper is
  `(K0 minus union(K_D,K_T,relief_left,relief_right,K_B))` extruded exactly
  `1.00` in X. Its seated ID is `4.80`, throat is `4.00`, removed cap depth is
  `1.222291236000`, and retained flat-tip intervals at `z_k_tip` are exactly
  `[-3.20,-2.00]` and `[2.00,3.20]`, width `1.20` each. This profile, not a
  generic C-ring primitive or auto-fillet, is the only keeper source.
- Let `K` be that final 3D keeper solid in local coordinates
  `X=-0.50..+0.50`. Its exact allowed deforming subset is
  `F_K=K intersection {z_k_tip<=Z<=0, |Y|>=2.00}`. In every seated operation
  state use the exact transform
  `T_K=translate(X_keeper,d_keeperY,d_keeperZ)*rotate_about_X(alpha_keeper)`
  and define `K_world=transform(K,T_K)` and
  `F_K_world=transform(F_K,T_K)`. The mouth, flat tips, and all collision and
  pilot-shoulder tests use this transformed asymmetric BREP, never a centred
  circular envelope. For seated-groove material
  at radial snap coordinate `z_rel`, define
  `G_K(z_rel)={-0.50<=X<=+0.50,
  Y^2+(Z-z_rel)^2<=2.30^2}`. The only permitted positive keeper/groove
  intersection BREP is
  `O_K(z_rel)=F_K intersection G_K(z_rel)`. Along the declared centred,
  mouth-down snap path, source tests must prove
  `K intersection G_K(z_rel)=O_K(z_rel)` within the declared BREP tolerance at
  every elastic pose; any keeper/groove intersection outside `F_K` fails.
- For the keeper radial snap, define
  `z_rel=Z_shaft_axis-Z_keeper_centre` with Y_rel=0. Rigid approach ends exactly
  at `z_rel=z_k_tip-2.30=-5.877708764000`; all earlier poses have zero positive
  overlap. The only elastic-only interval is
  `-5.877708764000<=z_rel<=0`, during which only `F_K` may deform with
  `u_X=u_Z=0` and `0<=sign(Y)*u_Y<=0.30`; only
  `O_K(z_rel)` is exempt from rigid positive-overlap rejection. Seated state is
  `z_rel=0`; removal is the exact reverse trajectory. After elastic recovery at
  that centred seated state, the operational keeper may move over the complete
  exact connected `Q_K(p_c)` offset/roll component. A
  separate continuous exact-BREP sweep must prove that every such seated pose
  lies in the same connected rigid-clear component and must transform
  `K_world`, `F_K_world`, mouth/tips, groove, outer pilot shoulder, left cam,
  and all other mechanism/workpiece/tool solids. If that connected sweep fails,
  the specimen is rejected; friction, preload, gravity, and anti-roll may not
  choose a favourable pose. `K minus F_K` and every other solid remain rigid
  and clear.
  Keeper force, recovery, fatigue, and minimum useful material width are
  physical tests. No analytic keeper C-arm material-midline/length acceptance
  metric is active; exact profile connectedness and the snap BREP trajectory
  replace that redundant ambiguous metric.
- The integral shaft retains a full round `OD5.60` outer pilot/shoulder from
  `X=-21.00..-20.00`. This 1.00-mm shoulder lies outside the keeper groove and
  geometrically blocks a seated keeper from escaping leftward; positive
  overlap under a commanded axial keeper-removal translation is required until
  the keeper is first removed radially. It is not a separate part or key.
- Each cam/fixed facing pair has one `OD10 x 0.20` annular thrust land on the
  fixed plate and no cam-side thrust land. The total projection remains `0.20`
  inside the retained `0.30` main-face gap, leaving `0.10 mm` nominal axial
  bearing gap. A zero cam-land height omits that solid rather than constructing
  degenerate geometry. At the endplay corner where
  a fixed disc moves `0.10` toward its adjacent cam, lands are tangent with
  positive overlap `<=1e-7 mm3`; at every other endplay corner their gap is
  positive. Printed axial wobble is a physical usability/binding test, not
  claimed absent. No land enters the nominal 26.20-mm central work span.

Each fixed disc uses one upward-opening (`+Z`) integral C-journal centred on
its dedicated shaft groove:

- seated circle centre is plate-local `(Y,Z)=(0,0)`, nominal `ID4.80` around
  groove `OD4.80`; this is a provisional line-to-line CAD relation, not a claim
  that a printed bearing has zero play or acceptable torque;
- throat `4.20`, requiring `0.30 mm` outward elastic displacement per arm as
  the `OD4.80` groove passes;
- access mouth is exact cutter `T` and its finite tips are created by exact
  top-cap cutter `B` from Section 5;
- the two finite free-tip intervals at `z_tip` are each exactly `2.20 mm` and
  the exact `0.461809077129-mm` bottom cap plus width-4.20 mouth are the only
  excluded outer-rim regions. Verify the fixed plate is one connected
  positive-volume solid and globally certify nonnegative Euclidean separation
  from every simultaneously dilated motion cutter. No material-midline arc,
  relief-tangent arm length, normal-width, or ligament-strength acceptance
  metric is active. C-arm stress, minimum useful wall, snap force, recovery,
  and fatigue are physical coupon tests;
- plate thickness `2.80` in groove width `3.00` gives `0.20 mm` total X
  endplay per fixed disc (`+/-0.10` about nominal) while groove shoulders bound
  further X motion without friction.

For each side `k in {JL,JR}`, let `J_k` be the final fixed-plate solid in
plate-local coordinates `X=-1.40..+1.40`. Define the exact deforming subset

```text
F_Jk = J_k intersection {0<=Z<=z_tip, |Y|>=2.10}
```

and define `z_J=Z_groove_axis-Z_journal_centre`. The groove material crossing
that plate is

```text
G_Jk(z_J) = {-1.50<=X<=+1.50, Y^2+(Z-z_J)^2<=2.40^2}
O_Jk(z_J) = F_Jk intersection G_Jk(z_J)
```

`E-JL/E-JR` permit positive journal/groove intersection only in the exact BREP
`O_Jk(z_J)`. At every elastic pose, source tests prove
`J_k intersection G_Jk(z_J)=O_Jk(z_J)` within BREP tolerance; intersection
outside `F_Jk` is a hard failure. Only `F_Jk` may deform, with
`u_X=u_Z=0` and `0<=sign(Y)*u_Y<=0.30`; `J_k minus F_Jk`, the
groove shoulders, and every other solid remain rigid.

The seated C-circle reaches world
`Z=shaft_z+2.40=30.303627355414`. No Z-only corridor shortcut is accepted:
the full workpiece includes horizontal material below `Z=34`, while the fixed
plates are separated in X. Continuous exact 3D tests over every plate pose and
specimen must prove zero C-mouth/material overlap with the complete workpiece,
nominal/dilated rod-motion cutters, iron/frame references, and the complete
release/removal sweeps, plus the exact flat-tip intervals, intended-only rim
opening, and one connected fixed-disc solid. Failure reopens Gate 0.

Assembly is radial for fixed discs and axial only for the keyed left cam:

1. Take the one-piece right-cam/shaft actuator with no keeper installed. Align
   the left-cam keyway with the 225-degree rib orientation. Slide the left cam
   from `X<-21.00` in `+X`: its ID5.70 round region first traverses the full
   OD5.60 pilot `X=-21.00..-20.00`, then clears the recessed keeper groove; at
   `X=-18.70` the through-keyway begins axial engagement with the rib; stop at
   nominal centre `X=-17.45` with full `2.50-mm` engagement for the nominal
   assembly view. Physical-state sweeps then allow the coupled
   `-17.75..-17.25` interval while enforcing `>=2.20-mm` engagement. Only then
   snap the round
   keeper radially into the `X=-19.40` groove. The keeper never passes the
   pilot shoulder or rib, and the cam never passes an installed keeper. No
   fixed journal is on the shaft during this step. Continuous insertion BREP
   must prove the ID5.70 bore clears the full pilot and the aligned keyway alone
   receives the rib.
2. Present each fixed disc below its dedicated groove with its `+Z` mouth
   facing the shaft, then translate the disc only in `+Z`. Elastic exemption
   begins when the groove first enters the retained flat opening at
   `z_J=z_tip+2.40=22.188190922871` and ends seated at `z_J=0`; throughout
   this exact interval only `F_Jk` may expand symmetrically up to `0.30 mm` and
   only `O_Jk(z_J)` is an allowed positive intersection. All prior approach is
   rigid and clear.
3. Confirm fixed-disc centres `-14.50/+14.50`; then insert the three pre-capped
   rods through left cam, left fixed, right fixed, and right cam, and install
   the three removable opposite caps.

The normal workpiece-removal sequence in Sections8/10 stops after removing the
three right caps, synchronously pulling the three rod/left-cap subassemblies
leftward clear of every plate, and lifting the complete workpiece. All four
plates, the fused actuator/shaft, keeper, and fixed guides remain assembled;
normal operation never removes an actuator/shaft cheek or fixed guide.

Full **service-only** jig disassembly starts only with the workpiece removed and
all three rod/left-cap subassemblies off the jig. Remove the keeper radially
first; then translate each upward-mouth fixed C-guide only in `-Z`, reversing
the exact seated `z_J=0` to `z_J=22.188190922871` elastic sweep until it clears
its groove. Only after both fixed guides are off may the keyed left cam and
fused actuator separate: hold the left cam and translate the one-piece right
actuator/shaft in `+X`, so the local rib exits through the aligned keyway and
the keeper groove/full left pilot pass through the left cam's `ID5.70` round
region. The `OD5.60` shaft is never commanded through either fixed guide's
production `ID4.80` C-journal. The integral shaft never separates from the
right cam. CAD proves each rigid approach/sweep, nominal tangency, shoulder
capture, and bounded endplay; fit, rotation torque, C-arm recovery, fatigue,
snap retention, and radial play are physical-only.

Mobility claims are split. In the nominal zero-clearance model, grounding the
left fixed disc and commanding the right actuator yields one connected
kinematic solution branch: line-to-line key flanks impose
`theta_L=theta_R=theta` and each rod coordinate is `s(theta)`. The
physical-clearance model is **not** strict M=1: fixed discs have bounded X
endplay, the ungrounded right fixed guide has lane-constrained `theta_RF`
mobility, and the keyed left cam has tolerance-dependent SE(2) and X intervals.
All four axial corners
`(left,right)=(-0.10,-0.10),(-0.10,+0.10),(+0.10,-0.10),(+0.10,+0.10)` and the
full Section 4 feasible set must pass binding, contact, rod-skew, tool-access,
and removal sweeps. They cover fixed-centre spacing `28.80..29.20` and clear
span `26.00..26.40`; no strict physical M=1 or unproved phase-accuracy claim is
permitted.

## 8. Exact workpiece placement and removal sweep

The former connector-only removal payload is rejected. Define one complete,
connected workpiece BREP `W_complete(p_c)` for each immutable specimen:

- two Ø4.30 insulated swept tubes over the complete Section3 90-degree path:
  horizontal `q=6..19`, the exact quarter arc, and vertical `Z=36..43`, at
  X centres `-4,+4`;
- two stripped Ø2.30 conductor cylinders over `Y=19..24,Z=30`, joined to the
  insulated horizontal tubes at `Y=19`;
- the two allowed completed solder envelopes at `J_left/J_right` from
  Section10, joined to their conductors;
- two Ø3.00 solder-cup cylinders at `X=-4,+4,Y=0,Z=43..48`;
- the XT60 body box `X=-7.95..+7.95`, `Y=-4.05..+4.05`,
  `Z=48..68.50`, joined to the cups.

The exact union must be one connected completed XT60 + horizontal + bend +
vertical workpiece assembly. Source tests reject a connector-only, vertical-
lead-only, disconnected, or long-horizontal-lead-omitted substitute. ESC pads
and `Frame_ESC_ref` remain nonstructural reference BREPs rather than jig parts;
their real attachment/handling is a physical workflow boundary, but their
collisions are not silently removed from the declared frame/tool tests.

Normal removal begins only at a valid OPEN state after the commanded reverse
lift reaches `theta_R=0`:

1. Reverse each exact right-cap installation path from its seated
   `(q_R_i,alpha_R_i)` state through `q=0..-3`, certify every declared elastic
   exception and rigid clearance, and remove all three right caps from the
   active assembly. No cap is removed before OPEN.
2. Let `H_LC_minus=X_cam-1.25` and freeze
   `c_rod_exit=0.50`. From the exact OPEN rod BREPs, derive one common
   synchronous withdrawal distance

   ```text
   L_rods = max_i(max(0,
              X_right_actual_i-(H_LC_minus-c_rod_exit)))
   a_i(lambda_r)=a_i_OPEN-lambda_r*L_rods, 0<=lambda_r<=1
   ```

   and translate all three complete rod/permanent-left-cap subassemblies
   together toward `-X`. Continuously prove exact lane/cam/journal/shaft/
   keeper/workpiece clearance for the complete three-body sweep and prove at
   `lambda_r=1` every rod's rightmost actual BREP point is at least
   `c_rod_exit` left of the left-cam slab. The three subassemblies are then off
   the jig; pulling one rod alone is not the accepted normal-removal evidence.
3. Keep the two cams, both fixed guides, fused shaft, and shaft keeper fully
   assembled. Define their exact post-rod union as
   `M_remain(p_c,x_OPEN)`. Let

   ```text
   Z_mech_top = max_Z(M_remain)
   Z_payload_min = min_Z(W_complete)
   c_remove_end = 0.50
   L_remove_required = max(0,
       Z_mech_top+c_remove_end-Z_payload_min)
   L_remove = certified global upper bound of L_remove_required over the
              complete admissible OPEN p/x domain
   T_remove(lambda)=(0,0,lambda*L_remove), 0<=lambda<=1
   E_remove_full = union_lambda(T_remove(lambda)*W_complete)
   ```

   The nominal seed is
   `L_remove_required=(shaft_z+20.25+0.50)-(30-2.15)
   =20.803627355414 mm`; the production command comes from the certified global
   upper bound, not that nominal decimal. The complete swept BREP must have
   zero positive overlap with `M_remain`, and its endpoint must clear every
   remaining mechanism solid by at least `c_remove_end`. No actuator/shaft
   cheek, fixed guide, keeper, or circular plate is removed to make this pass.

This three-stage exact reachability test is predicate `C`. It validates
normal removal after the common stroke has been selected and does not derive
that stroke. Samples or an endpoint-only lift do not prove cap release, rod
withdrawal, or full-workpiece clearance. Actual solder-joint/frame handling,
wire flexibility, and whether the user can pull three uncoupled rods together
comfortably remain physical usability tests; CAD must nevertheless prove the
specified simultaneous geometric path.

## 9. Retainers and assembly/disassembly

The current printable census is four independent principal plates, one
separate shallow-D shaft, one round shaft keeper, six round rod end caps, and
two diagnostic coupons; the three forming rods are purchased stock. The
integral-actuator census described in the archived Section 7 is forbidden in
current production artifacts.

- **Left rod cap (permanent tight/blind rod subassembly):** use cap-local
  coordinate `xi` with `xi=0` at the open face and `+xi` pointing from that
  face toward the closed floor (`+xi` maps to world `-X` when installed on a
  jig rod). The body is a round `OD7.00` cylinder over `xi=0..3.80`; its
  coaxial blind socket is exactly `Ø3.90` over `xi=0..3.00`; its closed floor
  is `xi=3.00..3.80`. It has no slit. Hold the cap fixed and define
  `q_L=xi_rod_tip`. The bounded coaxial manufacturing trajectory is exactly
  `q_L=-3.00..3.00`: rigid approach `-3.00<=q_L<=0` has zero positive overlap;
  physical-only interference insertion is `0<q_L<=3.00`. In that interval the
  only allowed deforming region is
  `F_LP=Cap_L intersection {0<=xi<=3.00}`, the cap's exact socket-wall body
  before its rigid floor; nominal `Ø3.90` over `Ø4.00` requires exactly
  `0.05 mm` radial accommodation per side. The exact permitted nominal rod/cap
  intersection is
  `O_LP(q_L)=Cap_L intersection {0<=xi<=min(q_L,3.00),
  1.95<=sqrt(Y^2+Z^2)<=2.00}`. Source tests prove the actual intersection
  equals `O_LP(q_L)` within BREP tolerance; any overlap outside that shell is a
  failure. The rod, floor, and `Cap_L minus F_LP` remain rigid.
  Accepted seated engagement is `q_L=2.50..3.00`; at `q_L=3.00` the rod tip is
  tangent to the floor boundary and may not pass it. Press force, strain,
  recovery, and retention are physical-only. This press operation creates one
  permanent left-cap/rod subassembly per rod before jig assembly. During normal
  jig operation or jig disassembly the left cap is never removed from the rod;
  cap extraction is a separate destructive/service physical test, not a
  reverse CAD motion exemption.
- **Right rod cap (removable print-fit/friction cap):** in cap-local coordinates, X is
  the rod axis, open face `X=0`, and body is the cylinder `OD7.00`,
  `X=0..3.80`. The coaxial blind cavity is `Ø4.20` over `X=0.60..3.00`; the
  entrance throat is `Ø4.10` over `X=0..0.60`; closed floor is `X=3.00..3.80`.
  The nominal one-sided radial clearances over the `Ø4.00` purchased rod are
  `0.10 mm` in the cavity and `0.05 mm` in the throat. The minimum nominal
  radial wall is `(7.00-4.20)/2=1.40 mm`.
  Exactly one `+Z` radial slit cutter matches the accepted P16 core after axis
  rotation: nominal functional material removal is
  `X=0..3.00, Y=-0.30..+0.30, Z=1.995..3.50`, with a named `0.03-mm`
  Boolean overcut only past the open face (`X=-0.03`) and past the OD
  (`Z=3.53`). It stops exactly at the floor boundary `X=3.00`. Its width is
  `0.60`, centreline throat penetration is
  `delta_slit=2.05-1.995=0.055`, and functional axial depth is `3.00`.
  At the two lower slit corners its radial penetration into
  the R2.05 throat is still positive:
  `2.05-sqrt(1.995^2+0.30^2)=0.032569703806 mm`; therefore the cutter is not
  merely tangent to the throat. It is open to the OD and throat/cavity and
  terminates on plane `X=3.00` without entering the `0.80` floor. At the slit-
  root plane `Z=1.995`, each retained side interval is
  `sqrt(3.50^2-1.995^2)-sqrt(2.05^2-1.995^2)=2.404083866319 mm` in the throat
  zone and
  `sqrt(3.50^2-1.995^2)-sqrt(2.10^2-1.995^2)=2.220031632399 mm` in the cavity
  zone. Both arms remain connected through the uncut full-annulus floor
  `X=3.00..3.80`; the final cap must be one connected positive-volume solid.
  No second slit, through-floor cut, spiral, or implicit flexible region is
  permitted. Required seated rod engagement is `2.50..3.00`.
- **Shaft keeper:** the fully dimensioned round C-keeper from Section 7:
  `OD9.60`, seated ID `4.80`, throat `4.00`, axial thickness `1.00`, in the
  `OD4.60 x 1.20` groove centred at `X=-19.40`.

CAD proves only that each closed cap floor geometrically blocks the rod end
from passing axially through the seated cap and that the removable right cap
has a rigid-clear assembly/removal path. CAD does **not** prove that the Ø3.90
left press cap stays attached or that the right cap retains load by printed
friction. The P16 PETG coupon gate established only initial acceptable hand
insertion/removal for throats `Ø4.05/4.10/4.15` with a `Ø4.20` cavity;
`Ø4.10` is the centred production default. Shake retention, cycling, wear,
creep, heat, and pull-off force have not been performed.

For each of the three identical removable caps, hold the cap fixed and define
`q=X_rod_tip-X_open_face`. The exact coaxial installation trajectory is
`q=-3.00..3.00`. The complete trajectory is rigid-clear: source tests prove
the actual `Ø4.00` rod/right-cap positive intersection is zero for every
`q` in that interval and every cap roll. There is no right-cap elastic-overlap
exception and no nominal snap-interference claim. At `q=3.00` the rod-tip
plane is tangent to the rigid floor boundary; any `q>3.00` is rejected because
it would enter the floor. Accepted seated engagement is
`q=2.50..3.00`, giving tip-to-cavity-end clearance `0.50..0.00 mm` with
zero positive-volume overlap. Disassembly is the exact reverse. Each cap's
physical engagement/float variable spans `2.50..3.00` and enters the coupled
rod-coverage/cap-squeeze optimizer. Slit force, strain, recovery, fatigue, and
retention remain physical-only. Both root-plane side intervals, retained
`0.80-mm` floor, one-solid connectedness, minimum `1.40-mm` radial wall,
zero rod/cap overlap, and complete rigid-clear `q=-3..3` sweep are mandatory
source tests.

Assembly:

1. Print and evaluate lane, cap, C-journal, round-bore, and rectangular-keyway
   fit coupons.
2. Align and slide the keyed left cam from the free LEFT end onto the one-piece
   right-cam/shaft actuator before installing the keeper; then present the two
   upward-mouth fixed discs from below and snap them in `+Z` into their
   dedicated `X=+/-14.50` grooves as Section 7 specifies.
3. Create the three permanent left-cap/rod subassemblies using the exact
   `q_L=-3..3` physical press trajectory above. Insert those subassemblies from
   `-X` to `+X` through all four aligned slot systems; the attached left caps
   remain outside the left cam.
4. Push the three round print-fit right caps onto the +X rod ends and verify
   axial float without squeezing cam/fixed bearing lands.
5. Rotate only the right circular cam rim. Verify nominal keyed equal travel;
   do not call physical left-cam phase/backlash exact until the feasible-set and
   measured-keyway gates pass.

Normal operation does not disassemble the four-plate actuator structure.
After RELEASE it removes all three right caps, withdraws all three
rod/left-cap permanent subassemblies synchronously toward `-X`, lifts the full
completed workpiece, and leaves both fixed guides, both cams, fused shaft, and
keeper assembled. Full service-only disassembly follows the separate Section7
order: rods already off; keeper radially off; both fixed guides `-Z` off their
grooves; then fused actuator/shaft `+X` through the stationary keyed left cam.
It does not reverse the left blind-cap press operation. Swept-volume tests must
prove the exact normal and service paths, and must explicitly reject any
OD5.60-shaft-through-ID4.80-fixed-journal trajectory.

The complete allowed deformation/overlap-exception census is closed and
enumerated:

| IDs | Coordinate interval | Exact deforming subset | Exact permitted intersection |
|---|---|---|---|
| `E-JL/E-JR` | `0<=z_J<=z_tip+2.40` | `F_JL/F_JR` | `O_JL(z_J)/O_JR(z_J)` |
| `E-K` | `-5.877708764000<=z_rel<=0` | `F_K` | `O_K(z_rel)` |
| `E-LP1..3` | `0<q_L<=3.00` | `F_LP` of that cap | `O_LP(q_L)` |

Every remaining subset and intersection is the coordinate/Boolean BREP defined above;
the identifier alone grants no exemption. Each source test evaluates the
actual mating-pair intersection and proves it equals the named `O_*` BREP
within tolerance, while all material outside the named `F_*` subset remains
rigid. Every rigid approach endpoint and every other part pair must have zero
positive overlap. No other deformation region or silent BREP-overlap waiver
exists.

## 10. Complete operation, solder-tool access, retention, and release

The operation contract is stateful and may not be replaced by an isolated
LOCKED rendering. The ESC references below are translucent, nonstructural test
geometry; they add no holder, base, locator, or BOM occurrence.
All three left blind caps remain permanently attached to their rods throughout
every normal `INSERT` through `REMOVE` operation and service disassembly. The
three right caps and three rod/left-cap subassemblies are the only parts
removed during normal loading/removal; the complete four-plate/shaft/keeper
structure remains assembled.

- Two explicit ESC pad/lead joint points are
  `J_left=(-4,24,30)` and `J_right=(+4,24,30)` in XYZ. Horizontal insulated
  leads follow the Section 3 centreline to `Y=19`; stripped straight lead
  segments occupy `Y=19..24` at `Z=30`, ending on the pad reference plane
  `Y=24`. The XT60 body and local leads remain vertical as Section 8 defines.
- Provisional solder-target BREP solids are independently reproducible:
  each ESC pad is a box `5.00 X x 1.50 Y x 0.50 Z`, centred at `X=-4/+4`,
  spanning `Y=24.00..25.50` and `Z=29.75..30.25`; each stripped copper lead is
  a `Ø2.30 x 5.00` Y-axis cylinder from `Y=19..24` at `X=-4/+4,Z=30`; its
  Ø4.30 insulation ends exactly at plane `Y=19`; each allowed molten-solder
  envelope is a sphere `R1.50` centred at J. Pad size, conductor OD, strip
  length, insulation end, and acceptable solder-blob envelope are provisional
  until caliper/photo measurement and must be re-frozen before physical-fit
  acceptance.
- Every physical operation test below uses the Section 4 nested domain. Its
  outer loop selects one immutable specimen record `p_c`, including the
  as-printed production `ID5.70`/width-1.50/roof-3.50 key geometry, lane and
  profile realizations, exact measured rod BREPs/endpoint frames,
  journal/groove measurements, cap
  geometry, permanent left-cap seated engagements, full workpiece/iron
  envelopes, and measured `Frame_ESC_ref`. Its inner continuous
  solve varies only movable `x`: left-cam `SE(2)` pose, `X_cam/X_keeper`,
  independent journal offsets, right-fixed `theta_RF`, fixed-disc X endplay,
  seated keeper `(d_keeper,alpha_keeper)`, exact rod
  `(b_i,k_i,a_i,psi_i)` state,
  and removable right-cap `(q_R_i,alpha_R_i)` poses. Every
  operation path satisfies `p(t)=p_c`; diagnostic key/bore coupons never
  substitute here. Collision, tool, removal, and binding sweeps transform the
  complete right-fixed plate material and upward C-mouth by `pose_RF`, the
  complete asymmetric keeper by `pose_K`, and every slitted right cap by its
  exact `T_Rcap_i`; lane constraints alone determine the right-fixed admissible
  angular branch, while no keeper/cap roll is frozen by friction or gravity.
  Nominal views at `d_cam=0,X_cam=-17.45` are reference
  views only and cannot satisfy the physical sweep requirement.
- **OPEN/INSERT:** command and validate `theta=0`, remove all three right caps,
  and synchronously withdraw all three rod/left-cap subassemblies by the exact
  Section8 paths if they are not already off. Start the complete unsoldered
  workpiece BREP (the Section8 full geometry without completed solder
  envelopes) at the certified `+Z` endpoint and apply the exact reverse lift
  into LOADED placement. Then reverse the synchronous rod withdrawal to insert
  all three rod/left-cap subassemblies together from the left, and install all
  three right caps by their exact rigid-clear print-fit paths. The four plates, fused shaft, and
  keeper remain assembled throughout. Continuous BREP overlap outside named
  elastic exceptions is zero; a connector-only insertion proof fails.
- **SET/CLOSE:** with all rods/caps installed, place both stripped lead ends on J_left/J_right, then command
  only right actuator theta from `0` to `27 degrees`; certify the complete
  continuous sweep throughout the coupled domain using Section 4.2. The
  0.1-degree poses are regression/visualization seeds only.
- **LOCKED:** at theta=27 both stripped leads are horizontal at the ESC pad
  references, the XT60/local leads are vertical, and the centreline is the
  Section 3 G1 90-degree path.
- **SOLDER:** for each joint use this exact iron BREP. Let axial coordinate `t`
  run along `a=(0,+sin(35deg),+cos(35deg))`. The centre of the terminal
  `Ø1.20` face is J. The tip is the closed frustum `0<=t<=12` with
  `r(t)=0.60+(1.75-0.60)*t/12`. The coaxial barrel is `12<=t<=47` with
  `r(t)=4.00`. At each J all cone/barrel material extends along `+a`; no apex
  primitive or implied zero-radius point exists. The approach starts
  at `final+25*a` and translates along `-a` to final. Because each J has Y=24,
  the complete final barrel has `Y >= 24-4 = 20`, while the XT60 body has
  `Y<=4.05`; nominal Y separation is therefore at least `15.95 mm` and grows
  at every outward approach pose. Thus the tool body moves analytically away
  from, never toward, the XT60. Only the terminal portion `0<=t<=1.50` may
  overlap the **target** pad box, target stripped-conductor cylinder, and target
  molten-solder sphere. Every point with `t>1.50` has axial distance greater
  than `1.50 mm` from J, so it is analytically outside the target `R1.50`
  sphere; BREP intersection tests additionally enforce the legal pad/conductor
  contact mask. The remaining frustum and entire Ø8 barrel have zero
  positive overlap with both pad boxes, both conductors, both solder spheres,
  insulation, plates, shaft, retainers, rods, and XT60. The terminal tip also
  has zero overlap with the opposite joint's pad/conductor/solder solids.
  Run left/right sweeps separately over the complete coupled domain.
- **COOL:** remove the iron while theta remains exactly 27; hold the unchanged
  LOCKED contact geometry. No springback claim is made.
- **RELEASE:** command theta from 27 back to 0 on each configuration's same
  connected feasible component. Quantify every maximal admissible,
  constraint-consistent reverse lift
  `gamma in Gamma(c)` and independently compute
  `theta_loss_of_retention(c,gamma)` from predicate `R` and
  `theta_removal_clear(c,gamma)` from predicate `C` exactly as Section 4
  defines. Report separate certified extrema, attaining paths/states,
  continuity/jumps, disconnected components, validity termination, both
  unreached statuses, `OPEN_VALID`, every terminal validity bracket/first
  failing condition, independent `PATH_VALID_THROUGH_OPEN`, and binding over
  the complete domain. Each lift reports `T_gamma`, every `A_p_c` equation and
  complementarity residual over the complete closed `[0,T_gamma]`, and
  same-branch maximality/nonextendability. A `T_gamma<27` endpoint must itself
  pass `A_p_c`; only a separately reported attempted extension may be
  infeasible. A path fails Gate 0 if `T_gamma<27`, it loses validity before
  OPEN, or it has invalid OPEN, even when either event occurred earlier.
  Workpiece removal is permitted only at a valid state where `C` is true,
  irrespective of whether geometric retention has already been lost. Each path
  certificate explicitly proves `p(gamma(tau))=p_c`; only its classified
  movable `x` trace may change and every such change must satisfy `A_p_c`.
- **REMOVE:** only after a valid commanded `theta=0`, reverse/remove all three
  right caps, synchronously pull all three rod/left-cap subassemblies leftward
  and completely off the jig, then execute the Section8 certified full
  connected-workpiece `+Z` sweep. Both cams, both fixed guides, fused shaft,
  and keeper remain assembled. Removal before OPEN, one-rod-only withdrawal,
  connector-only lifting, or actuator/shaft-cheek removal is forbidden.

Mandatory operation tests and views are named `OPEN`, `LOADED`, `SET/CLOSE`,
`LOCKED`, `SOLDER-left`, `SOLDER-right`, `COOL`, `RELEASE`, and `REMOVE`, plus
one combined tool-access swept-envelope view.

### Locked retention tests

At LOCKED, use the exact 90-degree workpiece and contacts from Section 3.

- Contact residual `<=0.02 mm`; contact-normal error `<=0.05 degrees`;
  nominal positive overlap `<=1e-7 mm3`.
- Linear retention: for rigid YZ translations of magnitude `0.10 mm` at every
  direction in `1-degree` increments, at least one rod must create positive
  geometric incursion `>=0.02 mm`. The analytical contact-normal matrix must
  positively span YZ (no nonzero translational escape vector).
- Rotational retention: rotate the rigid local workpiece about X through the
  bend centre `(Y,Z)=(6,36)` at `+/-0.25,+/-0.50,+/-1.00 degrees`; every case
  must create positive overlap with at least one rod or reduce signed clearance
  below `-0.02 mm`.
- Every maximal lift `gamma in Gamma(c)` first proves every classified movable
  coordinate satisfies its named `A_p_c` equation/complementarity over
  `[0,T_gamma]` and certifies same-branch maximality. It evaluates `R` only on
  states satisfying `V` to determine
  `theta_loss_of_retention(c,gamma)`. Independently, `C` evaluates the full
  Section-8 `+Z` swept payload only on valid states to determine
  `theta_removal_clear(c,gamma)`. Report separate global
  earliest/latest events across all paths/configurations, certified brackets
  and residuals, continuity or jumps on every connected component,
  disconnected components, `UNREACHED_BRANCH_INVALID`, and
  `UNREACHED_AT_OPEN`. Each maximal lift reports `T_gamma`, `OPEN_REACHED`, and
  `OPEN_VALID`; an empty event set is `UNREACHED_BRANCH_INVALID` whenever
  `PATH_VALID_THROUGH_OPEN` is false and includes either the certified
  closed-endpoint `A_p_c` residuals plus one-sided nonextendability condition at
  `T_gamma<27`, or the one-sided terminal bracket and first failing `V`
  condition. `UNREACHED_AT_OPEN` is permitted only when
  `PATH_VALID_THROUGH_OPEN` is true. Independently require
  `PATH_VALID_THROUGH_OPEN=(T_gamma=27 AND h_V=27 AND OPEN_VALID)` for every
  maximal lift, even after a reached event; any false result fails Gate 0.
  Never evaluate beyond `T_gamma` or below `theta=0`; at valid OPEN every
  configuration's Section-8 removal sweep must be completely clear. Event
  extrema are first certified over all admissible `x` lifts for one fixed
  `p_c`, then aggregated across separately identified specimen records; no
  path may interpolate between specimens.
- No claim of frictional holding, wire force, or springback follows from these
  geometric retention tests.

## 11. Angle command only; no stop, detent, or index geometry

P13 contains no hard-stop channel, detent pocket, orientation notch, printed
angle mark, extra solid, or associated cutter. OPEN `theta_R=0`, dwell start
`22 degrees`, and commanded LOCKED `27 degrees` are test-fixture/software
coordinates only. Documentation images may add non-BREP angle annotations,
but those annotations are excluded from source, STEP, print kit, BOM, topology
census, and collision claims. Holding/indexing feel is outside P13; adding any
physical stop/detent/index requires a new reviewed source revision.

### Alternatives rejected at Gate 0

| alternative | why it fails the frozen invariants |
|---|---|
| External cap compression of otherwise free fixed discs | Requires preload/friction to establish X, can squeeze cam bearing gaps, and cannot guarantee the `26.00` minimum work span or repeatable solder-tool access. |
| Bounded but otherwise free fixed discs | Honest clearance produces uncontrolled axial placement beyond a named journal; it cannot provide repeatable clear span, rod skew, or removal proof. |
| Separate centre spacer/sleeve | Adds a loose structural part through the central work span, behaves as a bridge, and directly reduces connector and iron access. |
| Through-insert annular snap journal | Requires an undersized journal to traverse shaft/groove features and needs a long elastic exception; the third review rejected that assembly trap. |
| Upward-mouth side-entry integral C-journal with downward service release (selected) | Adds no occurrence, seats directly into a dedicated groove, bounds X geometrically, permits the required fixed-guide `-Z` service removal after the keeper/rods are off, and localizes elasticity to one explicit radial snap sweep; exact 3D workpiece/tool clearance replaces a false Z-only corridor argument. |

## 12. Required review evidence and files

Mechanism-approval images contain no FPV frame, ESC, FC, table, base, or bench
background. ESC pads/workpiece/iron may appear only as translucent,
nonstructural operation references in explicitly labeled operation views.
Required views:

1. OPEN front/side showing both the ready state with rods/caps installed and
   the post-release caps-off/three-rods-off state with the exact full-workpiece
   removal corridor;
2. LOADED with the complete unsoldered horizontal+bend+vertical+XT60 workpiece
   lowered into the still-assembled four-plate structure while rods/caps are
   off, followed by SET/CLOSE from the same camera with all three rods inserted
   synchronously and all three right caps installed;
3. LOCKED front/side showing horizontal stripped leads at pad references,
   vertical XT60, three contacts, and the 90-degree path;
4. SOLDER-left, SOLDER-right, and combined tool-approach swept envelope;
5. COOL and RELEASE matched-camera views, including valid OPEN before any cap
   is removed;
6. final REMOVE sequence showing all three right caps reversing off, all three
   rod/left-cap subassemblies moving left together and off the jig, and the
   full connected completed workpiece lifting `+Z` while both cams, both fixed
   guides, shaft, and keeper remain assembled;
7. OPEN and LOCKED isometrics;
8. follower-side close-up showing exactly four circular plates, three rods,
   the right cam's integral round grooved shaft/local rib, keyed left-cam bore,
   upward C-mouths, and round retainers, plus matched physical-state overlays
   at global `X_cam=-17.75/-17.25` showing `2.20/2.30-mm` key engagement;
9. transparent inverse-slot overlay with equal-travel plot and the full feasible
   left-cam SE(2) pose envelope rather than a theta-only trace; plot samples are
   visibly labeled as seeds and accompanied by the continuous global bound;
10. two exploded workflow views with every occurrence and all six rod caps
    countable. Initial assembly shows the keyed left cam sliding from LEFT onto
    the one-piece right cam/shaft across the full outer pilot, keeper radial
    installation behind the `X=-21..-20` shoulder, both upward-mouth fixed
    guides entering from below in `+Z`, the three permanent left-cap/rod units,
    and three removable right caps. Service-only disassembly shows rods/caps
    already off, keeper radially off, both fixed guides moving `-Z` off their
    grooves, then the fused actuator/shaft moving `+X` through the stationary
    keyed left cam—never OD5.60 through an ID4.80 fixed journal, a false
    separate shaft, or a fixed-disc through-insert sequence;
11. print-kit top view excluding purchased rods, workpiece, ESC references,
    and iron. The right actuator appears exactly once as one fused occurrence.
    The four principal print orientations are authored explicitly: left cam
    `+90 degrees Y` with its flat inner face on the bed and hub up; left fixed
    `+90 degrees Y` with its plain face on the bed and fixed land up; right
    fixed `-90 degrees Y` with its plain face on the bed and fixed land up; and
    right actuator `-90 degrees Y` with its flat inner face on the bed and hub
    up. Each principal part must have a large planar authored footprint at
    `build Z=0` and no negative Z. The keeper, six caps, and coupons are
    separate nonstructural print-kit items.
12. sectioned shaft-keeper profile and matched snap-trajectory sequence at
    rigid first contact, maximum declared elastic opening, seated, and reverse
    release, with the exact D/T/two-R0.60/B cutter boundaries, `F_K`,
    pose-dependent `O_K(z_rel)`, and `z_rel` coordinates labeled; a matched
    section for each fixed journal similarly labels `F_Jk` and `O_Jk(z_J)`.
    A separate seated-keeper envelope plots the complete exact
    `Q_K(p_c)` offset/roll component, transformed C-mouth/tips,
    pilot-shoulder blocking and minimum clearances, and identifies the
    connected rigid-clear component reached from centred mouth-down seating;
13. sectioned removable right rod-cap profile and matched `q=-3,0,2.5,3`
    installation states, showing the one +Z slit, positive
    `delta_slit=0.055` throat penetration, both exact root-plane side intervals,
    retained rigid floor, `1.40-mm` minimum radial wall, one-solid connectedness,
    zero nominal rod/cap positive intersection throughout the rigid-clear path,
    and exact reverse release path. The seated states
    include a certified full `alpha_R_i in S1` roll envelope for each cap and
    label projected-up slit orientation as the nominal `alpha_R_i=0` view only;
14. sectioned permanent left-cap/rod subassembly at
    `q_L=-3,0,2.5,3`, showing the `Ø3.90` socket over the `Ø4.00` rod, the
    exact local annular-wall interference exception, rigid floor, and the
    exact `F_LP/O_LP(q_L)` overlays plus the completed rod/left-cap unit moving
    together during normal jig withdrawal;
    no normal-operation cap-removal arrow is permitted.
15. a validity report for `V` and two separate quantified-path reverse-event
    reports/plots: one for `theta_loss_of_retention(c,gamma)` using only `R`,
    and one for `theta_removal_clear(c,gamma)` using only `C`. Each shows
    certified lower/upper brackets across all `Gamma(c)`, attaining paths and
    configurations, connected-component IDs, discontinuities,
    `OPEN_VALID`, `UNREACHED_BRANCH_INVALID`, and `UNREACHED_AT_OPEN`. Every
    invalid-branch result shows its certified one-sided terminal validity
    bracket and first failing `V` condition, including the endpoint-only
    `tau=27` case. A third independent path-validity table reports `T_gamma`,
    `OPEN_REACHED`, `OPEN_VALID`, and
    `PATH_VALID_THROUGH_OPEN=(T_gamma=27 AND h_V=27 AND OPEN_VALID)` for every
    maximal `gamma`, plus passing `A_p_c` residuals at every closed endpoint and
    the blocking continuation equation/mode with a one-sided nonextendability
    certificate for every `T_gamma<27`; it marks Gate 0 failed whenever the
    path gate is false, regardless of either event result. The evidence also
    includes the frozen named `x`-coordinate-to-`A_p_c` formula/mode census,
    source-parity result, maximum residuals, and rigid-versus-elastic contact
    partition. The 12 `phi_lane_ji` overlays show each exact skew-rod
    `cross_section(W_i(p_c,x),X)` over complete `psi_i in S1` roll branches and
    transverse YZ clearance to lateral walls across
    the complete slab while visibly excluding axial entry/exit faces. They
    also label all four plate poses, including
    `pose_RF=(X_fixed_right,C_shaft+d_right,theta_RF)` and
    `pose_RC=(+17.45,C_shaft,theta_R)`, with both sets of rotating lanes. Keeper
    rows label `pose_K=(X_keeper,C_shaft+d_keeper,alpha_keeper)` and its complete
    transformed asymmetric BREP. Cap exception rows
    label `I_LP=(0,3.00]` and `q_L=0` as rigid tangency, and section the exact
    exact measured-endpoint `T_Lcap_i/T_Rcap_i` frames, all `alpha_R_i`, OD7 cap bodies,
    transformed cap/rod intersection residual, normal end planes, arclength engagement, and
    cap-to-plate BREP gaps. Neither event plot may be
    labeled with a generic release angle or extend below theta0. Every plot and
    path certificate labels the immutable specimen-record hash `p_c`, proves it
    is constant, and plots admissible movable `x(tau)` separately;
    cross-specimen envelopes are summaries, never a continuous path. The `C`
    report separately certifies the three right-cap reverse sweeps, synchronous
    three-rod/left-cap withdrawal, complete `W_complete` lift, and the invariant
    assembled four-plate/shaft/keeper remainder; a connector-only `E_remove`
    report fails.
16. a parametric-source evidence package containing the serialized typed
    `P13Params` default manifest, the complete primary-to-derived dependency
    graph, and a no-magic-number/static-source audit. Fresh-process metamorphic
    reports must cover at least three representative safe single-parameter
    retunes and one safe coupled two-parameter retune. For every variant they
    identify the changed primary fields, verify every declared dependent value
    against its named formula, prove unrelated occurrence labels and topology
    remain invariant, regenerate STEP, and pass source/export parity. Repeating
    an identical manifest must produce deterministic source measurements and
    export checksums. The package records the source revision and exact
    parameter-manifest hash for every artifact and verifies that no generated
    STEP, STL, 3MF, GLB, snapshot, or report was hand-edited. P21-specific rows
    show safe `c_sw`, wire-diameter, profile, and coupled pivot retunes; separate
    `shaft_od` and `R_bend` dependency runs are visibly stamped `RE-GATE REQUIRED`.
    Each proves the complete concentric dependent set moves/regenerates while
    world workpiece/contact centres and unrelated topology/labels remain fixed.

The current source/export census must report four independently printable
principal plate occurrences, separate shallow-D actuator shaft `1`, keeper
`1`, rod caps `6`, purchased rods `3`, and two diagnostic coupons only in the
STEP print kit. The production 3MF therefore contains exactly 12 objects and
the STEP print kit exactly 14 occurrences. Any integral cam/shaft, rectangular
key/rib, full-length key, or duplicate actuator is a hard failure.

The implementation source and regenerated exports must also prove that the
left-cam production cutter is exactly `ID5.70` union the width-`1.50`,
`u=2.50..3.50` nominal keyway. Source/export parity rejects every diagnostic
`ID5.60/5.80`, width-`1.60/1.70`, or roof-`3.55/3.60` alternative, and rejects
every stop, detent, orientation-index, or printed-angle solid/cutter. Any
parameter change invalidates the current exports and requires clean
regeneration/parity. A change inside the explicitly frozen safe-retune class
follows Section1.1 tests/re-review; every other dimension/topology/workflow
change returns the design to renewed Gate-0 intent/geometry review before its
artifacts may be accepted.

The source test suite must encode the exception identifiers
`E-JL,E-JR,E-K,E-LP1..3` as an allowlist containing the exact mating
part pair, trajectory coordinate interval, exact `F_*` deforming-region BREP,
pose-dependent `O_*` permitted-intersection BREP, and displacement bound for
each. At every certified pose the test compares the actual mating-pair
intersection to `O_*` by symmetric-difference volume `<=1e-7 mm3`. Tests fail
on an undeclared identifier, an overlap outside the named interval/`F_*`, an
actual intersection unequal to `O_*`, a nonzero rigid-approach overlap, a
left-cap removal motion in the normal assembly/disassembly sequence, or any
positive overlap silently omitted from the report.
For each right cap, source tests additionally prove the `1.40-mm` minimum wall,
connected solid, retained `0.80-mm` floor, and zero positive rod/cap
intersection. Those proofs transform the exact cap and rod by
`T_Rcap_i(q_R_i,alpha_R_i)` and certify the full `q_R_i` interval times
`alpha_R_i in S1`; projected-up-only testing fails.
For the keeper, source tests separately certify the centred mouth-down elastic
snap/reverse path and the complete recovered seated domain
`(d_keeper,alpha_keeper) in Q_K(p_c)` using p-only
`phi_K_transverse`, then independently apply full 3D current-X keeper gaps and
capture. They transform `K`, mouth/tips,
`F_K`, pilot shoulder and every collision pair by `pose_K`, prove that domain
is in the same connected rigid-clear component as the seated snap endpoint,
and reject any friction, preload, gravity, or anti-roll constraint.

Normal-workflow source tests start from a certified valid OPEN state
(`theta_R=0`, `OPEN_REACHED`, `OPEN_VALID`, and
`PATH_VALID_THROUGH_OPEN` all true), reverse all three exact right-cap paths,
then move all three rod/permanent-left-cap subassemblies synchronously over the
single derived `L_rods` path. With all four circular plates, both fixed
guides, the fused actuator/shaft, and keeper still assembled, they sweep the
one connected `W_complete` payload through `E_remove_full` to its certified
global `+Z` endpoint. The test fails on pre-OPEN cap release, one- or two-rod
withdrawal, cheek/fixed-guide/keeper removal, connector-only payloads, or any
endpoint command copied from the nominal seed rather than derived over the
complete admitted `p/x` domain. When `C` succeeds,
`theta_removal_clear=0`; before valid OPEN, `C` is false rather than a partial
removal result.

Service-workflow source tests begin only with `W_complete`, all six caps, and
all three rods off. They reverse the keeper radial snap, reverse each fixed
upward-mouth guide from `z_J=0` to `z_J=22.188190922871` in `-Z`, and only
then hold the keyed left cam while translating the fused actuator/shaft in
`+X`. The exact swept-BREP sequence must pass pairwise collision/exception
checks and explicitly reject every trajectory that sends the `OD5.60` shaft
through either production `ID4.80` fixed journal. No alternate service order
or hidden disassembly coordinate is accepted.

Every motion/collision/tool/binding/retention/event test report must additionally
carry the Section-4.2 continuous-certificate method, complete domain, global
lower/upper bounds, attaining bracket, and convergence status. A report that
contains only pose samples or endpoint snapshots fails source review.
Validity `V` is tested and reported independently from `R` and `C`. Before any
event result is accepted, source tests build a complete named census mapping
every classified movable `x` coordinate to its exact `A_p_c` actuation,
guide/cam-slot, key, axial/endplay, rigid-subassembly, or contact-
complementarity equation and certify every residual over the path domain.
Reverse-event tests quantify the full family `Gamma(c)` of maximal admissible
same-branch lifts, prove each lift satisfies `A_p_c` throughout its declared
closed domain including every endpoint, certify maximality/nonextendability at
every `T_gamma<27` without placing an inadmissible limit inside `gamma`, prove every
reported event state satisfies `V`, and distinguish
`UNREACHED_BRANCH_INVALID` from `UNREACHED_AT_OPEN`. Tests independently
evaluate `OPEN_REACHED=(T_gamma=27)` and `OPEN_VALID`; an empty event set returns
`UNREACHED_BRANCH_INVALID` whenever `PATH_VALID_THROUGH_OPEN` is false, with the
applicable nonextendability or one-sided terminal certificate, and may return
`UNREACHED_AT_OPEN` only when `PATH_VALID_THROUGH_OPEN` is true. Any arbitrary
equation-breaking `x` trace, nonmaximal prefix, single selected lift, silent
component jump, event evaluation at `NOT V`, omitted path/component, evaluation
beyond `T_gamma`, or endpoint validity inferred from the supremum alone fails
source review. Independently, the suite asserts
`PATH_VALID_THROUGH_OPEN=(T_gamma=27 AND h_V=27 AND OPEN_VALID)` for every
maximal `gamma` and fails Gate 0 on any false result even if `S_loss` or
`S_clear` is nonempty; event success is never accepted as a substitute for
full-path validity.
Source parity compares the implementation's equation-census identifiers and
serialized formulas exactly against the frozen census:
`shaft_od/wire_diameter_design/c_sw/R_bend/bend_center/horizontal_z/r_s/r_w/
d_arc0/delta_pivot/shaft_y/shaft_z/C_shaft`, every `P_i/s/S_i_req/Q_i`,
all four pivot-derived plate poses, stock/cutters and `g_rim_j`,
`phi_shaft_workpiece/phi_shaft_rod_i/phi_shaft_tool_k/phi_shaft_frame`,
`E_command`, `E_lane_ji`, `phi_lane_ji`,
`E_JL_material/E_JR_material`, `C_JL_capture/C_JR_capture`, `Q_LF/Q_RF`,
`phi_round`, both flank gaps, `phi_roof`, `ell_key`, `E_key`, all eight named
axial gaps, `theta_RF/pose_RF`,
`d_keeper/alpha_keeper/p_keeper/phi_K_transverse/Q_K/pose_K`,
`E_K_rigid/phi_K_groove/mode_K_groove/C_K_capture`,
`c_i/sigma_i/n_i/C_i/frame_projection_min/F_hat_i/v_i/q_i/K_i/R0_i/psi_i/Rroll_i/T_rod_i`,
`e_straight_i/beta_straight_i/U_i/W_i_nom/W_i_env`, the frozen measured
`W_hat_i(p_c)`, its placed `W_i(p_c,x)`, and endpoint
frames, every
`g_cover_ji_minus/plus`, `X_left_tip_i`, `X_right_tip_i`, and
`X_left_actual_i/X_right_actual_i`,
`C_Lopen_i(W)/C_Ropen_i(W)`, `alpha_R_i`,
`T_Lcap_i(W)/T_Rcap_i(W,alpha_R_i)`, both transformed cap
BREPs, right-cap/rod rigid-clear intersection,
`E_Lcap_plate_i/E_Rcap_plate_i`, both `phi_*cap_plate_i`, and each `q_R_i`
mode, `W_complete`, all three reverse cap paths, `c_rod_exit/L_rods`, the
synchronous `a_i(lambda_r)` rod-withdrawal path, `M_remain/Z_mech_top/
Z_payload_min/c_remove_end/L_remove_required/L_remove/E_remove_full`, and the
normal/service sequence predicates.
It fails on a missing coordinate/equation, an extra hidden motion coordinate,
an altered formula, a mode partition not declared here, or a rigid
complementarity constraint applied to any intentional `O_*` interference.
For every rod, formula-parity tests independently prove the frozen metrology
frame admission/projection rule, `R0_i*eX=n_i`, zero-roll mapping of the
registered `eY_hat_i` datum, orthonormality and determinant `+1` of `R0_i` and
`Rroll_i`, the non-antipodal bound `q_i>0`, and continuous periodic closure at
`psi_i=0/2*pi`. The exact transformed measured BREP and endpoint frames must
coincide at both periodic representatives; an implementation-defined roll
gauge or seam discontinuity is a hard failure.
For every `phi_lane_ji`, tests additionally prove the minimization spans the
complete plate slab, uses the exact `cross_section(W_i(p_c,x),X)` for the frozen
potentially skew/bowed rod specimen, and uses only transverse YZ lateral lane
walls; substituting an ØD
disk for a skew cross-section or including either axial slab end face in the
contact/clearance metric is a hard failure. Pose/source parity separately
proves the integral right-cam lanes use
`pose_RC=(+17.45,C_shaft,theta_R)` at every commanded angle rather than a fixed
or omitted pose, and proves the ungrounded right fixed guide uses
`pose_RF=(X_fixed_right,C_shaft+d_right,theta_RF)` throughout every exact material,
C-mouth, lane, and collision calculation. It likewise proves LC/LF/K use their
exact `C_shaft`-derived origins and rejects any surviving world `(0,30)` datum.
The exception suite separately checks every `E-JL/E-JR/E-K/E-LP` interval,
actual-intersection equality to `O_*`, containment in `F_*`, displacement
bound, and rigid zero-overlap outside the interval.
The source suite serializes/hash-compares `p(gamma(tau))` against `p_c` over
every certified maximal lift and fails on any changed rod, profile, bore,
keyway, journal, lane, cap, keeper, workpiece/tool envelope, clearance radius,
or permanent left-cap engagement. It separately reports the permitted movable
`x(tau)` trace and aggregates extrema across specimen records only after every
fixed-`p_c` inner solve passes.
It also verifies an incoming-stock admission record for every rod with
`e_straight_i<=0.05 mm` and `beta_straight_i<=0.05 degrees`, freezes the
measured exact `W_hat_i(p_c)`, placed `W_i(p_c,x)`, and endpoint frames, and
proves every A/contact/path
result uses that one immutable BREP. It repeats the inner solve for every
admitted outer-loop `W in U_i`; `W_i_env` is rejection/precheck-only. A
nominal-cylinder or union-envelope contact/mobility report fails. No CAD result is labeled
valid for a rod that fails the physical gate.

Source tests must also instantiate the complete typed `P13Params` default
manifest and serialize its primary-to-derived dependency graph. A static audit
rejects any geometry, placement, angle, fit, tolerance, manufacturing option,
metrology input, state, solver threshold, evidence camera, or output-selection
literal that is neither a schema field nor a named derivation, except the
mathematical identities and unit conversions permitted by Section1.1. In fresh
processes, tests perturb at least three representative safe-retune primary
fields one at a time and one safe coupled pair; each run checks declared
dependent formulas, unchanged unrelated topology and occurrence labels,
deterministic repeat generation, and source/re-imported-STEP parity. Every
generated artifact manifest must match the active source revision and exact
parameter-manifest hash. An undocumented topology-changing option, stale
derived value, duplicated formula, undeclared literal, or hand-edited derived
artifact fails source review and requires the applicable renewed Gate-0 review.

Authoritative future paths are exclusively:

- `src/xt60_bend_jig/p13_four_plate_three_rod.py`;
- `tests/test_p13_four_plate_three_rod.py`;
- `cad/p13_four_plate_three_rod/`.

P1 through P12 source, tests, documents, and generated artifacts remain
unchanged.

## 13. I01-I18 invariant traceability

| ID | Frozen invariant | Objective evidence |
|---|---|---|
| I01 | Exactly four connected circular structural occurrences, fixed+cam per side. | Role census=4; each blank OD40.50; right cam and round shaft are one fused occurrence; integral upward-mouth C-journals remain part of fixed parent plates; one connected positive-volume solid each; no undeclared stock. |
| I02 | Exactly three unmodified Ø4 x 50 rods. | Exact 50-mm nominal-core BREPs and occurrence census=3; rods excluded from print kit; each physical rod passes `e_straight<=0.05 mm` and `beta_straight<=0.05 degrees`, then freezes its exact measured local `F_hat_i`, registered `W_hat_i(p_c)`, and endpoint frames. Every `W in U_i` is a separate outer specimen; explicit shortest-arc `R0_i` plus Rodrigues `Rroll_i(psi_i)` define `T_rod_i` over complete free roll with zero-gauge/periodic parity, and `W_i_env` is precheck-only. |
| I03 | No forbidden structure/workholding/holder. | Forbidden-label/source census plus isolated visual rejection gate. |
| I04 | One right-rim actuator input, locally keyed left cam, and bounded physical pose set. | Nominal key imposes d_cam=0/theta_L=theta_R. Exact plate poses include `pose_LC=(X_cam,C_shaft+d_cam,theta_L)`, `pose_LF=(X_fixed_left,C_shaft+d_left,0)`, rotating `pose_RF=(X_fixed_right,C_shaft+d_right,theta_RF)`, and `pose_RC=(+17.45,C_shaft,theta_R)`. For each frozen specimen p, the physical x solve jointly optimizes left-cam SE(2), X_cam/X_keeper, exact anisotropic `Q_LF/Q_RF/Q_K` components, key backlash, axial endplay, each rod shift/roll `(a_i,psi_i)`, and each right-cap `q_R_i/alpha_R_i`; no stale `(0,30)`, diameter-disk truncation, or friction-selected pose is admitted. |
| I05 | Equal scalar travel with a reproducibly derived common stroke. | Recompute `rho`, all three `S_i_req`, and `max=3.764213562097` from task-fixed contacts after deriving `C_shaft`; continuously certify projection onto each guide equals common s(theta) within 1e-9 mm, orthogonal residual <=1e-9, common dwell, minimum Jacobian2.053627355 and crossing angle5.938027856; samples are seeds only. |
| I06 | Exact G1 90-degree path and three tangent contacts. | Endpoint tangent, G1 join, centre-distance, normal, residual, and zero-positive-overlap tests from Section 3. |
| I07 | Inverse slots derived from motion and uniquely constrain nominal rods/cam phase. | Nominal audit retains theta_L and proves one line-to-line branch; each physical audit freezes lane/rod/journal geometry in p and solves the full movable `(d_cam_y,d_cam_z,theta_L,theta_RF)`/X feasible set, with the left fixed guide as the sole angular ground. |
| I08 | Compact circular plates and exact permitted topology. | All plate OD40.50 concentric at derived `C_shaft`; exact stock/cutter symmetric difference<=1e-6; nominal/tolerance rim2.625246078/2.271692687 and continuous exact minimum>=2.00; no stop, detent, orientation-index, printed mark, or undeclared cutter. |
| I09 | Explicit per-part central clearances and viable analytic Ø4 lane. | Web nominal/tolerance2.909821686/2.202714905; final right-actuator/left-cam/fixed central clearances4.025964796/3.975964796/4.425964796 with each fixed value subtracting its own p_k; diagnostic ID5.80 is nonproduction despite3.925964796 clearance; eroded lane4.042893219. |
| I10 | OPEN full completed-workpiece removal is validated independently from the conservative stroke construction. | At valid OPEN, all three right caps reverse off, all three rod/left-cap subassemblies withdraw synchronously left and off the jig, then exact derived-length `+Z` continuous `W_complete` sweep clears the still-assembled four plates/shaft/keeper by `c_remove_end`; connector-only and 16-mm shortcuts fail and none of this derives S. |
| I11 | Admissibility, validity, LOCKED retention loss, and removal clearance are distinct specimen/configuration/path-dependent predicates and events. | Exact `g=(p,x)` partition with immutable `p(gamma)=p_c`; source parity to the frozen formula/mode-complete `x`-to-`A_p_c` census, including exact `C_shaft` poses/clearances, `cross_section(W_i(p_c,x),X)` over every free rod-roll branch, separate outer rod-BREP realizations, exact anisotropic C-space components, transverse-only lane-wall clearance over each complete plate slab, rotating `pose_RF/pose_RC`, seated keeper offset/roll, and all removable-cap rolls; rigid versus accommodated-elastic contact partition; all maximal same-branch admissible lifts `Gamma(c)` have closed A-feasible endpoints and certified `T_gamma`/nonextendability; Boolean `V`; independent `OPEN_REACHED`/`OPEN_VALID`; mandatory `PATH_VALID_THROUGH_OPEN=(T_gamma=27 AND h_V=27 AND OPEN_VALID)` for every maximal lift regardless of event success; valid-domain-only `R/C`, with C false before valid OPEN and then quantifying cap release, synchronous rod withdrawal, and full-workpiece lift; separate event extrema, attaining paths/configurations/specimens, continuity/jumps/termination/disconnected components, exact `UNREACHED_BRANCH_INVALID` versus `UNREACHED_AT_OPEN` truth table and terminal certificate. |
| I12 | Profile tolerance is reproducible and does not conceal skew/fit/phase. | Independent fixed-p specimen records for lanes/exact rod BREPs/keyway/journals; inner x solve uses full SE(2) cam plus exact `Q_LF x Q_RF x Q_K` continuous global optimizer, concentric `p_k` values as seeds only, `eps_global=0.005 mm` certificate, <=0.05-degree measured rod-skew acceptance, and frozen straightness/tangent metrology. |
| I13 | Only declared round retainers, one separate shallow-D shaft/head, and integral side-entry journals. | Exact keeper D/T/relief/B profile and snap sweep; matching cam D bores; no keeper arm-length claim, rectangular key/rib occurrence, or full-length key. |
| I14 | Assembly/disassembly and every retained axial state are geometrically reachable. | Exact cam/keeper X equations, key engagement, upward-mouth fixed-journal +Z assembly/-Z service snap and centred keeper snap plus connected full seated `Q_K` sweep, rigid-clear right-cap q sweep over all `alpha_R_i`, permanent left-cap q_L press subassembly, closed remaining `F_*/O_*` allowlist, measured rod/end-frame and cap transforms, and exact normal/service orders. Service is rods off -> keeper radial off -> both fixed guides -Z off -> fused actuator/shaft +X through keyed left cam; any OD5.60-through-ID4.80 trajectory fails. |
| I15 | Evidence and exports cannot hide architecture or workflow. | All 16 required mechanism/operation/profile/event/parametric-source evidence items, exact `F_*/O_*` exception report, quantified-path validity/event report, continuous certificates, STEP refs/validate/source parity, full test report, and independent zero-finding critics. |
| I16 | Complete INSERT->SET/CLOSE->LOCKED->SOLDER->COOL->RELEASE->REMOVE contract. | Full unsoldered-workpiece reverse +Z insertion with rods/caps off, synchronous rod insertion and cap installation, provisional BREP pads/conductors/solder at J_left/J_right, both outward iron sweeps and allowed-contact masks, COOL at theta27, every maximal A-consistent same-component reverse lift through valid OPEN, then caps off, three rods synchronously left/off, and full completed-workpiece +Z only at a V-and-C true state while the four-plate/shaft/keeper structure stays assembled. |
| I17 | The complete CAD is centrally parametric, source-regenerable, and safely modifiable without magic numbers or hand-edited artifacts. | Typed unit-bearing `P13Params` schema, serialized dependency graph/default manifest including the complete pivot-to-geometry/evidence chain, named single-source derivations reused by geometry/tests/reports/exports, explicit safe-retune versus renewed-Gate classes, no-magic-number audit, three safe single-parameter plus one coupled metamorphic regeneration tests, separate RE-GATE-required `shaft_od`/`R_bend` dependency tests, deterministic artifact provenance, and clean STEP/source parity. |
| I18 | The shaft/pivot is task-derived, concentric, and continuously clear without moving the task geometry. | Exact `r_s/r_w/d_arc0/delta_pivot/C_shaft` formula and default `(-2.096372645,27.903627355)`; all four circles/shaft/grooves/rib/journals/keeper/lanes/cameras regenerate concentrically while world workpiece/contact centres remain fixed; full theta and complete p/x certificates prove `phi_shaft_workpiece>=c_sw`, named shaft-to-rod/tool/frame clearances, and every `g_rim_j>=2.00`; stale `(0,30)` or independently shifted dependents fail. |

## 14. Gate-0 finding closure

The initial 17 findings, six second-pass findings, seven third-pass findings,
six fourth-pass findings, five fifth-pass findings, four sixth-pass findings,
four seventh-pass findings, eight eighth-pass findings, five ninth-pass
findings, four tenth-pass findings, two eleventh-pass findings, and one
twelfth-pass finding, one thirteenth-pass finding, and one fourteenth-pass
finding, three fifteenth-pass findings, nine sixteenth-pass findings, three
seventeenth-pass findings, two eighteenth-pass findings, one
nineteenth-pass finding, one twentieth-pass finding, and five twenty-first-pass
findings are
closed in this brief. Reviewers reopen any claim if implementation diverges.

### Intent findings (5)

| Finding | Closure |
|---|---|
| INT-01: P12 architecture survived as a skeleton rather than four simple plates. | Sections 1 and 13 freeze exactly four OD40.5 circles and forbid lobes, spine, base, bridge, holder, and workholding. |
| INT-02: Rod length/projection arithmetic was wrong. | Section 2 freezes `50.00-37.40=12.60 mm` total and `6.30 mm` per side only for nominal unskewed `a=0,k=0`; every physical specimen uses its measured exact 50-mm rod BREP/end frames, specimen-specific X projection, full slab coverage, and exact cap BREP clearance. |
| INT-03: Shaft/keeper assembly contained an impassable shoulder or ambiguous parts. | Section 7 dimensions one fused right-cam/round-OD5.60-shaft occurrence through X=-21, its full outer pilot/keeper shoulder, local key rib, locating/keeper grooves, keyed left-cam insertion from X<-21, journals, and exact elastic intervals. |
| INT-04: Retention mixed geometric blocking with unproved press/snap friction. | Section 9 uses one permanent blind-cap/rod press-fit subassembly and one removable rigid-clear print-fit cap per rod, bounds both installation paths, and separates end-floor geometry from the initial accepted PETG hand fit. Shake/cycling/wear/pull-off retention remains unproven. |
| INT-05: XT60 removal and 90-degree wire intent were under-defined. | Sections 3, 8, and 10 define exact centreline, body/cups/leads, start/end/direction, G1/tangency, no-overlap, retention, and independent removal-clear tests. |

### Math/geometry findings (12)

| Finding | Closure |
|---|---|
| MATH-01: Inherited P9 datum/stroke/angles were not re-derived. | Section4 rejects the P9 values; P21 further rejects the first `(0,30)` P13 guess and freezes derived `C_shaft=(-2.096372645,27.903627355)`, independently recomputed S=3.764213562, and 0..22 rise/22..27 dwell. |
| MATH-02: Common stroke was arbitrary, and a first attempted exact-payload intersection equation had the incorrect infimum. | Section 4.3 replaces it with the named conservative centre-clearance construction: `rho=3.103553390593`, requirements `3.203553390593/0/3.764213562097`, and their controlling maximum; exact payload BREP sweep is explicitly separate. |
| MATH-03: Slot/guide intersections could have multiple roots. | Sections 4.1/4.2 require one nominal connected phase branch and exactly one continuously certified intersection; the 813 dense/refined cases are regression seeds only and physical tolerance is reported as a feasible set. |
| MATH-04: Singular or near-tangent constraints were not bounded. | P21 recomputes the new-pivot minimum Jacobian determinant2.053627355 mm and crossing angle5.938027856 degrees and freezes >=2.00 mm/>=5.00-degree continuous nominal gates. |
| MATH-05: Inter-slot web was not calculated from path separation. | At lane width4.75, min centre separation7.659821686 gives nominal web2.909821686 and independently dilated minimum2.202714905. |
| MATH-06: Plate OD was inherited from an oversized design. | P21 derives raw minimum OD39.956614625 for the new pivot and 2.00-mm tolerance rim, while retaining the frozen OD40.50 stock for all four circles. |
| MATH-07: Worst-case profile tolerance was absent from rim sizing. | Section5 includes eps=sqrt(0.25^2+0.25^2) and proves new-pivot nominal/tolerance rims2.625246078/2.271692687 with continuous exact minimum>=2.00. |
| MATH-08: Shaft/slot corridor clearance was unproved. | P21 recomputes new-pivot right-actuator4.025964796, controlling left-cam ID5.70 clearance3.975964796, and fixed corridor4.425964796-p_k. ID5.80 remains diagnostic by frozen production topology, not a now-obsolete clearance failure. |
| MATH-09: Equal travel was checked only at endpoints. | Sections 4 and 13 require continuously certified identical s(theta), orthogonal residual, and common dwell; 0.1-degree poses are seeds/visualization only. |
| MATH-10: Follower cutter error was incorrectly treated as assembly skew. | Section 6 defines independent isotropic dilation/erosion solids (27 combinations per plate), separates assembly skew, and explicitly reports the eroded Ø4 fit failure as physical risk. |
| MATH-11: Locked escape was qualitative. | Sections4/10 freeze separate validity V, retention R, and +Z removal C predicates, quantify every admissible same-component reverse path, and report distinct certified event extrema, attaining paths/states, continuity/jumps, validity termination, OPEN-unreached status, disconnected components, and residuals. |
| MATH-12: Arbitrary 60% area and a contradictory net-volume ceiling were used. | Section 5 replaces both with an exact allowed-stock envelope, exact cutter census, and symmetric-difference topology test including thrust lands and integral journals. |

### Subsequent Gate-0 re-review findings (6)

| Finding | Closure |
|---|---|
| REVIEW-01: Both fixed plates retained uncontrolled axial X translation, so strict physical M=1 was false. | Dedicated side-entry C-journals bound each disc to its X=+/-14.50 groove with +/-0.10 endplay; only the ideal zero-clearance model claims M=1, while all four physical endplay corners are tested. |
| REVIEW-02: The volume ceiling omitted permitted additive lands/features and rewarded extra holes. | Exact allowed stock includes each thrust land and integral journals; exact allowed cutter census plus symmetric difference rejects both extra and missing topology. |
| REVIEW-03: Profile tolerance was not a reproducible solid operation or independently variable. | Section 6 defines disk dilation/erosion of each lane cutter independently, 27 combinations per plate. |
| REVIEW-04: Tolerance-minimum inter-lane web was not reported. | Width4.75 gives nominal2.909821686 and independently dilated2.202714905 mm. |
| REVIEW-05: Tolerance-minimum shaft clearance was not reported. | At new-pivot r_path_min9.600000000, the actual left-cam ID5.70 radius2.85 controls at3.975964796 after allowances; each fixed side separately reports4.425964796-p_k. |
| REVIEW-06: Narrower lanes might not accept real Ø4 rods. | Width4.75 erodes to4.042893219, analytically clearing nominal Ø4; actual sliding fit still requires measured rods/coupons. |

### Third-pass Gate-0 findings (7)

| Finding | Closure |
|---|---|
| PASS3-01: Through-insert annular journals remained an assembly trap. | Replaced with integral side-entry C-journals; P21 mirrors them to upward mouths so fixed discs assemble +Z from below and service-release -Z, while no journal traverses any groove. |
| PASS3-02: Fixed-disc axial spacing and mobility were overstated. | Groove width3.00 versus disc2.80 gives honest +/-0.10 endplay each; ideal M=1 is separated from physical bounded endplay, and all four corners cover span26.00..26.40. |
| PASS3-03: Lane tolerance simultaneously needed Ø4 fit, >=2 web, and >=1 central clearance. | Width4.75 gives eroded4.042893219, tolerance web2.202714905, and new-pivot controlling left-cam clearance3.975964796; diagnostic ID5.80 is still excluded from production by the frozen feature census. |
| PASS3-04: Keeper and left-cam axial contact were under-defined. | Keeper centre varies-19.50..-19.30 and the exact coupled constraint X_cam>=X_keeper+1.75 replaces a nominal-only0.10..0.30 gap; contact/noncontact and no preload are reported. |
| PASS3-05: C-mouth structural/access feasibility was untested. | Upward mouth, nominal ID4.80, throat4.20, exact connected mirrored `D union T union two R1.00 relief circles union B` profile, finite 2.20 tips, one-solid tests, and exact 3D workpiece/tool/removal clearance are frozen; the obsolete Z-only corridor shortcut is rejected and arm strength remains physical. |
| PASS3-06: User operation stopped at generic LOCK/REMOVE. | Section10 freezes INSERT,SET/CLOSE,LOCKED,SOLDER both joints,COOL,commanded RELEASE,and final REMOVE with explicit pad and iron envelopes. |
| PASS3-07: Simpler axial alternatives were not compared. | Section11 documents why external compression, free discs, a separate spacer, and through-insert journals fail, and why integral side-entry C-journals add no part or central obstruction. |

### Fourth-pass Gate-0 findings (6)

| Finding | Closure |
|---|---|
| PASS4-01: Solder iron body pointed toward the XT60. | Axis is flipped to `(0,+sin35,+cos35)`; final body Y>=20 while XT60 Y<=4.05, and outward-to-final sweeps run at all endplay corners. |
| PASS4-02: Opposed 0.15 lands consumed the 0.30 gap and collided under endplay. | The retained nominal pair projection is fixed0.20 plus cam0.00, leaving0.10 nominal gap; motion toward cam closes only to tangency, never positive overlap, while axial wobble remains physical. |
| PASS4-03: Journal radial play was absent from the model. | Nominal seated ID4.80/OD4.80 has zero free motion; physical sides use independent exact connected `Q_LF/Q_RF` C-space components in the full feasible solve and fixed-side clearance is evaluated from the complete transformed BREP. |
| PASS4-04: C-mouth profile was not independently reproducible. | Section5 defines exact mirrored `D`, `T`, analytic intersections, two `R1.00` circles, exact top-cap `B`, extrusion, finite tips, and connectedness; unreproducible arm-length/ligament strength claims are removed. |
| PASS4-05: Solder targets and legal tip contact were not BREP-defined. | Section10 freezes provisional pad boxes, Ø2.30 conductors, insulation plane, R1.50 solder spheres, and exact terminal-1.50-mm tip contact mask; measurement remains required. |
| PASS4-06: Historical active dimensions remained stale. | Active stack/projection values are37.40/12.60/6.30; stale-number scan is mandatory before Gate-0 acceptance. |

### Fifth-pass Gate-0 findings (5)

| Finding | Closure |
|---|---|
| PASS5-01: A separate keyed shaft/head was unnecessary, while a free passive left cam had a 5-degree dwell continuum and >=+/-1.495-degree nominal phase freedom. | Right cam and round shaft are one actuator occurrence; one short rectangular rib exists only in the left-cam zone. Matching line-to-line keyway fixes nominal phase, while coupon/feasible-set tests report physical backlash. |
| PASS5-02: C-journal free motion was assumed rather than measured. | Production CAD remains line-to-line ID4.80/OD4.80; measured as-printed complete C-void/groove BREPs define `Q_LF/Q_RF`. Diameter-derived p values are search seeds only; the full coupled optimizer decides physical acceptance. |
| PASS5-03: Parallel C-mouth arms tapered to impossible zero-width rim tips. | Exact mirrored top-cap cutter `B` stops the retained plate at z_tip=+19.788190922871 and leaves two exact 2.20-mm flat tips; CAD makes no structural ligament-strength claim. |
| PASS5-04: The iron used ambiguous apex language. | Section10 defines terminal-face centre J, frustum t=0..12 with explicit r(t), legal t=0..1.50 contact, and barrel t=12..47/r4.00. |
| PASS5-05: BOM, assembly, print orientation, and evidence still described the rejected shaft. | Archived fused-shaft closure; superseded by the accepted split-shaft amendment and retained only as review history. |

### Sixth-pass Gate-0 findings (4)

| Finding | Closure |
|---|---|
| PASS6-01: Keeper groove lacked an outer retaining shoulder. | Integral OD5.60 shaft extends to X=-21, leaving full pilot/shoulder X=-21..-20 outside the unchanged keeper groove. Cam inserts from X<-21 before radial keeper installation; axial keeper escape is BREP-blocked. |
| PASS6-02: Independent journal offsets were absent from the physical solve. | Section4 defines exact independent `Q_LF/Q_RF` connected C-space components and jointly optimizes them with cam SE(2), key/lane/rod/X/endplay cases; p-sum is diagnostic only. |
| PASS6-03: One shaft-radius clearance was incorrectly reused for every plate. | P21 Section5 reports actual central geometries: right actuator4.025964796, controlling left cam3.975964796, fixed sides4.425964796-p_k. ID5.80 remains nonproduction regardless of its now-positive clearance margin. |
| PASS6-04: Diagnostic coupon sizes could be mistaken for production approval. | Production source remains exactly ID4.80. The4.85/4.90 journal and ID5.80 bore coupons only inform a future source regeneration and renewed Gate; they cannot select the current production fit. |

### Seventh-pass Gate-0 findings (4)

| Finding | Closure |
|---|---|
| PASS7-01: Physical left-cam motion was reduced to theta_L only. | Section4 solves the exact measured-bore/keyway BREP pose `(d_cam_y,d_cam_z,theta_L)` and crosses it with exact journal C-space components, lanes, rods, axial states, operation sweeps, and both reverse-event predicates. Nominal alone is d_cam=0/theta_L=theta_R. |
| PASS7-02: Left cam and keeper were rendered at fixed nominal X. | Coupled bounds are `X_keeper=-19.50..-19.30` and `X_cam=[X_keeper+1.75,X_fixed_left-2.85]`, global `-17.75..-17.25`; key engagement is2.20/2.30 at extremes and2.50 nominal. |
| PASS7-03: The p-sum skew inequality was mislabeled necessary. | It is now a concentric-seed diagnostic only. The complete SE(2)/exact C-space/key/measured-rod optimizer determines physical acceptance. |
| PASS7-04: Diagnostic journal cutters risked changing production architecture without review. | Production source is frozen at exact ID4.80. ID4.85/4.90 coupons may only inform a future regenerated source and renewed intent/geometry Gate. |

### Eighth-pass Gate-0 findings (8)

| Finding | Closure |
|---|---|
| PASS8-01: Diagnostic left-cam cutters could be selected into production. | Production centre cutter is exactly ID5.70 union width1.50/roof3.50 nominal keyway. Every alternate bore/width/roof is diagnostic-only and any source change requires regeneration and renewed Gate-0 review. |
| PASS8-02: An unqualified key prohibition contradicted the mandatory local rib. | Architecture now forbids only a separate key occurrence and full-length key; the local integral rib/matching keyway remains mandatory. |
| PASS8-03: Stop/detent/index cutters were underdimensioned complexity. | All such solids/cutters/claims are removed. Theta values are test coordinates and documentation-only annotations, excluded from BREP/BOM/print kit. |
| PASS8-04: Shaft C-keeper lacked reproducible geometry and motion. | Section7 freezes OD/ID, exact D/T/two-R0.60/B cutter profile, 1.20 tips, X extrusion, opening direction, and rigid/elastic radial trajectory. |
| PASS8-05: Removable rod-cap slit and snap interval were undefined. | Section9 freezes cap stock, cavity/throat/floor, one width0.60/depth2.00/+Z slit with positive throat penetration and termination at X=3.00, q=-3..3 trajectory, rigid q<=0 and elastic q>=0 intervals. |
| PASS8-06: Release was still one scalar threshold. | Sections4/10 now separate valid-domain loss-of-retention and removal-clear event angles over every admissible same-component path, with independently certified extrema, attaining paths/states, continuity/jumps, termination, OPEN status, and disconnected components. |
| PASS8-07: Keeper C-arm material-midline acceptance was ambiguous. | No analytic keeper arm-length/midline metric is active; exact BREP connectedness, finite tips, and snap trajectory replace it, while force/recovery remain physical. |
| PASS8-08: Stale wording and stray text could contradict the repaired contract. | Full-brief scans reject ambiguous key prohibitions, selectable diagnostic cutters, undeclared angle-index geometry, a scalar release threshold, and stray sentence fragments. |

### Ninth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS9-01: The elastic-exception census omitted the shaft keeper and silently treated the Ø3.90 left cap over the Ø4.00 rod as rigid/reversible. | Section9 closes a named exception allowlist for both fixed journals, the exact Section7 keeper interval, and all three bounded physical-only left-cap press intervals, now with exact `F_*/O_*` BREPs. The later P16 gate reclassifies right caps as rigid-clear print-fit parts. Left caps remain permanent rod subassemblies. |
| PASS9-02: One release angle mixed loss of geometric retention with clearance for the +Z removal sweep. | Sections4/10 define separate valid-domain predicates R and C and separately certify theta_loss_of_retention(c,gamma) and theta_removal_clear(c,gamma) over every admissible same-component reverse path, including distinct invalid-branch and valid-OPEN unreached statuses. |
| PASS9-03: The right-cap slit was tangent to the throat and did not create a reproducible opening. | Section9 lowers the slit root to Z=1.50, freezes delta_slit=0.30 and positive corner penetration0.270294145923, reports exact throat/cavity side intervals and floor connectedness, and reruns the complete q sweep. |
| PASS9-04: Fixed C-journal arm-strength metrics depended on an undefined material midline and relief tangency. | Section7 retains exact BREP profile, finite tips, one-solid connectedness, and collision clearance but removes arm-length/normal-width/ligament-strength CAD claims; force, wall adequacy, recovery, and fatigue are physical tests. |
| PASS9-05: Pose sampling was being used as a global collision and release proof. | Section4.2 makes samples seeds/visualization only and requires continuous swept BREP or certified interval global optimization over theta and the complete physical domain, with eps_global0.005 mm and angular brackets<=0.001 degree. |

### Tenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS10-01: Retention and removal predicates embedded feasibility/binding, so an invalid branch state could be misreported as an event. | Section4 defines validity `V` separately, defines `R/C` only on `V` states, and returns `UNREACHED_BRANCH_INVALID` when validity ends before an event. |
| PASS10-02: The elastic allowlist named vague arms/walls but did not bound each permitted overlap BREP. | Sections7/9 freeze `F_Jk/O_Jk(z_J)`, `F_K/O_K(z_rel)`, and `F_LP/O_LP(q_L)` coordinate/Boolean BREPs, displacement bounds, exact interval census, source tests, and sectioned overlays. The later P16 right-cap contract is rigid-clear and has no overlap exception. |
| PASS10-03: One connected feasible component did not select a unique reverse path in the non-M=1 clearance model. | Section4 quantifies all maximal `A_p_c`-consistent continuous same-component lifts `Gamma(c)` over movable x while freezing immutable specimen p, and reports per-specimen/configuration plus global extrema across `(p,c,gamma)`; no arbitrary continuation, nonmaximal prefix, specimen morph, or component jump is accepted. |
| PASS10-04: Reverse-event search was unbounded and conflated branch invalidity with no event by valid OPEN. | Tau is frozen to `[0,27]`; no theta below0 is evaluated; empty event sets return `UNREACHED_BRANCH_INVALID` when the validity horizon ends early or OPEN itself is invalid, and `UNREACHED_AT_OPEN` only when a valid path including the OPEN endpoint reaches OPEN without the event. |

### Eleventh-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS11-01: `Gamma(c)` allowed immutable measured/manufactured data to morph while searching for a favorable reverse path. | Section4 partitions `g=(p,x)`, classifies every specimen and movable variable, freezes permanent left-cap engagement in p, requires `p(gamma(tau))=p_c`, solves every continuation only in x, and aggregates extrema across separately certified specimen records. Sections10/12 and I11/I16 require the same specimen hash throughout every path. |
| PASS11-02: `F_RC` included the complete cavity wall while text simultaneously called that wall rigid. | Superseded by the P16 physical-fit gate: the production `Ø4.10` throat and `Ø4.20` cavity are nominally rigid-clear over the `Ø4.00` rod, so `F_RC/R_RC/O_RC` are removed from the active contract. |

### Twelfth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS12-01: `h_V=27` did not prove that OPEN itself was valid because the supremum is still 27 when every `tau<27` is valid but `V(gamma(27))` is false. | Section4 defines and independently certifies `OPEN_REACHED=(T_gamma=27)` and `OPEN_VALID=(OPEN_REACHED AND V(gamma(27)))`. An empty event set is `UNREACHED_BRANCH_INVALID` unless the maximal lift reaches a valid OPEN through a fully valid prefix, with the applicable nonextendability or one-sided terminal certificate; `UNREACHED_AT_OPEN` is allowed only when the complete path gate is true. Sections10/12 and I11/I16 encode the same endpoint truth table. |

### Thirteenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS13-01: OPEN/path validity was checked only while classifying an empty event set, so a loss/clear event reached early could mask later branch invalidity or an invalid OPEN endpoint. | Section4 defines `PATH_VALID_THROUGH_OPEN=(T_gamma=27 AND h_V=27 AND OPEN_VALID)` as an independent mandatory acceptance for every maximal admissible lift. Gate 0 fails on any false result regardless of either event result. Sections10/12, the third evidence table, and I11/I16 preserve event reports while independently rejecting every early branch termination, pre-OPEN validity loss, or invalid OPEN endpoint. |

### Fourteenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS14-01: `Gamma(c)` constrained x only to broad domains, so arbitrary equation-breaking traces were included and the universal full-path gate became unsatisfiable. | Section4 freezes exact `A_p_c(x,theta)` equations/complementarity for every movable coordinate and defines `Gamma(c)` as all maximal continuous same-branch `A_p_c`-consistent reverse lifts on `[0,T_gamma]`. Nonmaximal prefixes and arbitrary x traces are excluded; every `T_gamma<27` requires a nonextendability certificate and makes `PATH_VALID_THROUGH_OPEN` false. Sections10/12, evidence, and I11/I16 require the same equation census, residuals, maximality, and endpoint proof. |

### Fifteenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS15-01: Rigid `gap>=0` complementarity was applied to cap and snap contacts whose nominal-source BREPs intentionally interfere, rejecting mandatory retained states before `V` could allow them. | Section4 partitions rigid unilateral contacts from accommodated elastic exceptions. Every remaining `E-JL/E-JR/E-K/E-LP` state inside its frozen interval must have actual nominal-source intersection exactly `O_*`, contained in `F_*`, within its displacement bound; outside the interval it is rigid and overlap-free. The P16 right-cap contract is rigid-clear. |
| PASS15-02: A maximal lift could include a non-admissible terminal point while later sections required `A_p_c` on the closed domain. | `Gamma(c)` now consists only of closed-domain `A_p_c`-feasible lifts. A `T_gamma<27` endpoint itself passes every residual and is maximal only when no positive-epsilon same-branch A-consistent extension exists; any non-admissible limit is a separate diagnostic, never a point of `gamma`. Operation, evidence, tests, and I11 require the same endpoint contract. |
| PASS15-03: `A_p_c` called category prose “exact” while leaving fixed-disc X, rod/cap axial coupling, cap float, lane slack, key gaps, and contact modes for implementation to invent. | Section4 freezes the authoritative formula/mode census: measured rod-local BREPs plus declared rigid poses, full-thickness lane containment and slack modes, command/journal/key residuals, eight axial gaps, plate-slab coverage, exact cap endpoint-frame/engagement coupling, rigid contact modes, and elastic exception rules. Source tests require exact identifier/formula parity and reject missing, extra, or altered coordinates/equations. |

### Sixteenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS16-01: `phi_lane_ji` measured clearance to the complete finite lane-void boundary, so a through-rod always touched the axial entry/exit faces and every lane was falsely classified CONTACT. | Section4 defines `phi_lane_ji` as the certified minimum transverse YZ clearance to exact lateral lane walls over every X cross-section of plate slab `H_j`, explicitly excluding axial end faces. Full-thickness material nonoverlap remains `E_lane_ji=0`; axial coverage is owned separately by `g_cover_*`. Source parity and I11 reject any axial-face clearance implementation. |
| PASS16-02: The frozen exception census assigned `q_L=0` to the left-cap elastic interval while Section9 assigned it to rigid approach/tangency. | `I_LP=(0,3.00]` everywhere. The `q_L=0` state belongs exclusively to rigid approach/tangency with empty positive intersection; elastic `O_LP/F_LP` accommodation begins only for `q_L>0`. |
| PASS16-03: The first transverse lane formula substituted an ØD disk for the X-plane section of a skew right circular rod, so contact/tangency was wrong whenever `k_i` was nonzero. | `phi_lane_ji` now uses the exact BREP `cross_section(W_i(p_c,x),X)` at every X in the plate slab. Evidence and source tests reject circular-disk substitution while retaining the separate full-thickness `E_lane_ji=0` test. |
| PASS16-04: The right actuator was called a fixed integral pose, leaving its asymmetric lane rotation undefined even though its round stock and shaft are rotationally symmetric. | The frozen pose census now defines `pose_RC=(+17.45,C_shaft,theta_R)`; its three lane voids rotate exactly with commanded `theta_R` about the derived axis. Evidence, source parity, I04, and I11 reject a fixed, stale, or omitted right-cam lane pose. |
| PASS16-05: A skew rod was still given world-X endpoints `a_i+/-25`, making its physical arclength exceed 50 mm; scalar cap open-face X gaps also ignored tilted OD7 cap bodies and end planes. | Section4 first corrected nominal rods to 50-mm arclength/end-plane geometry, then PASS17 froze each measured exact rod-local BREP and actual endpoint frames. Cap engagement is measured along rod arclength, and exact transformed cap-to-plate BREP gap/intersection residuals replace scalar X gaps. Section2, evidence, source parity, I14, and coverage equations use the same specimen-specific transforms; removable-cap roll is closed separately by PASS16-07. |
| PASS16-06: The right fixed guide had no anti-rotation feature, but its asymmetric lanes/C-mouth were frozen at zero angle. | Section4 adds periodic same-branch `theta_RF` to `x`, grounds only the left fixed guide, and constrains the right guide through all three exact lanes plus global collision validity. Every RF material, C-mouth, lane, tool and removal calculation uses `pose_RF=(X_fixed_right,C_shaft+d_right,theta_RF)`; operation/evidence/source parity and I04/I07/I11 reject a fixed, stale, or omitted pose. |
| PASS16-07: Each removable slitted cap sat on a round rod without anti-rotation geometry, yet its slit roll was frozen projected-up. | Section4 adds `alpha_R_i in S1` for every right cap and constructs the full measured-endpoint-frame `T_Rcap_i` from an explicit transverse basis. Projected-up is nominal `alpha=0` only; cap/rod clearance, cap/plate, mechanism, tool, and removal tests certify all roll angles without a CAD friction/gravity constraint. Evidence, source parity, I04/I11/I14 enforce the same domain. |
| PASS16-08: The specimen hash claimed to include actual rod straightness, while the rod BREP remained a perfect right circular cylinder and no residual used the measurement. | Section4 freezes measured radial/tangent bounds and the exact measured rod-local `W_hat_i(p_c)`/endpoint frames, with each `W in U_i` a separate outer specimen and only declared `T_rod_i(x)` placement. `W_i_env` is precheck-only, nominal cylinders are render-only, and source tests reject an unused bound. Section15 freezes the incoming metrology gate. |
| PASS16-09: The asymmetric seated C-keeper had nominal radial clearance and free roll, but only `X_keeper` was modeled. | Section4 adds `d_keeper/alpha_keeper` to `x`, transforms the full keeper/mouth/deforming subset by `pose_K`, and uses exact connected `Q_K` rather than a diameter disk. Section7 separates centred elastic snap from the complete recovered seated component. Evidence, source parity and I04/I11/I14 forbid friction, preload, gravity or hidden anti-roll selection. |

### Seventeenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS17-01: Diameter-derived radial disks omitted rigid-clear mouth/relief travel of the C-shaped fixed journals and keeper, including roll-dependent anisotropy. | Section4 replaces those disks with local exact connected transverse configuration spaces `Q_LF(p_c)`, `Q_RF(p_c)`, and `Q_K(p_c)` built from complete measured C-void/groove BREPs. Diameter clearances are solver seeds only. The full `A_p_c` then applies current-X shoulder/capture plus rod/lane/cap/workpiece/tool coupling without contaminating specimen-only `Q_*` definitions. Tests enumerate component boundaries and reject disk truncation or friction/preload selection. |
| PASS17-02: A nonzero straightness gate was discarded into a perfect cylinder; the first envelope repair then combined mutually exclusive bows, omitted cap endpoint/tangent motion, and could hide real contact branches. | The incoming gate now measures radial and tangent error. Each admitted exact 50-mm rod-local BREP and endpoint frame is frozen as `W_hat_i(p_c)` and placed only by declared `T_rod_i(x)`; every `W in U_i` is a separate outer specimen with its own A/contact modes, cap transforms, maximal paths, and extrema. `W_i_env` may reject conservatively but never defines A, contact, retention, or mobility. Nominal geometry is render-only. |
| PASS17-03: Axial coverage used min/max of the union envelope, which are best-case projection extremes and could pass when another admitted rod realization failed to cover a plate. | Coverage now uses `X_left_actual_i=min_X(W_i(p_c,x))` and `X_right_actual_i=max_X(W_i(p_c,x))` for each immutable rod specimen and repeats both inequalities for every outer `W in U_i`. No cross-realization extrema are combined; cap engagement and endpoint-frame feasibility are likewise specimen-specific. |

### Eighteenth-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS18-01: The measured bowed rod BREP was registered only by best-fit axis position/direction, omitting rigid roll about that axis even though round rods/lanes/caps provide no anti-roll feature. | Section4 adds periodic `psi_i` for each rod, defines deterministic registered-frame `T_rod_i(a_i,b_i,k_i,psi_i)`, and includes complete same-branch rod-roll domains in A/Gamma, lane/contact/coverage/cap endpoint frames, tool/removal, binding, and retention. Evidence/source parity and I02/I04/I11 reject friction, gravity, or favourable bow-direction freezing. |
| PASS18-02: `Q_K(p_c)` used full 3D `phi_K_groove` built from `pose_K`, silently importing movable `X_keeper` into a specimen-only local component. | Section4 defines independent p-only transverse `phi_K_transverse(d_keeper,alpha_keeper;p_c)` and builds `Q_K` only from that complete 2D C-void/groove relation. Full 3D `phi_K_groove(X_keeper,d_keeper,alpha_keeper)`, `E_K_rigid`, and `C_K_capture` remain exclusively in A after component membership. Source parity and PASS17 locality tests reject any current-X leakage. |

### Nineteenth-pass Gate-0 finding

| Finding | Closure |
|---|---|
| PASS19-01: “Parametric source” did not yet guarantee that the complete design could be modified coherently; there was no exhaustive central schema, dependency graph, no-magic-number rule, parameter-change class, or metamorphic regeneration proof. | Section1.1 now freezes the typed unit-bearing `P13Params` schema, named single-source derivations, serialized dependency graph/default manifest, safe-retune versus renewed-Gate classes, deterministic artifact provenance, and a ban on hand-edited generated files. Evidence item16, source/export parity, and I17 require three single-parameter plus one coupled fresh-process metamorphic test and reject undeclared literals, stale dependents, topology drift, or manifest/source mismatch. |

### Twentieth-pass Gate-0 finding

| Finding | Closure |
|---|---|
| PASS20-01: Rod roll `psi_i` was present, but “registered-frame transform” left an SO(2) gauge: two implementations could choose different zero-roll transverse datums and produce different bowed-rod contacts or cap frames. | Section4 now freezes measured local frame `F_hat_i`, its origin/end-direction/transverse-datum admission rule, the unique non-antipodal shortest-arc `R0_i`, Rodrigues roll `Rroll_i(psi_i)`, and explicit `T_rod_i`. Source parity proves axis and zero-roll datum mapping, SO(3) properties, `q_i>0`, and exact continuous periodic closure at 0/2pi; no implementation-selected gauge remains. |

### Twenty-first-pass Gate-0 findings

| Finding | Closure |
|---|---|
| PASS21-01: The inherited shaft datum `(0,30)` was a hand-placed pivot rather than a task-derived parameter and could not prove wire clearance. | Section4 derives `C_shaft` from `shaft_od`, `wire_diameter_design`, `c_sw`, bend radius/centre, and horizontal Z. Defaults produce `(-2.096372644586,27.903627355414)` and exact nominal shaft-to-arc surface clearance `c_sw=0.50`; I18 and source parity reject any stale independent datum. |
| PASS21-02: Moving the pivot risked stale plates/lanes and invalid old rim/Jacobian/central-clearance numbers. | Sections4/5 regenerate every circular plate, shaft feature, journal, keeper, path and lane concentrically; task contacts remain fixed. Recomputed gates are Jacobian2.053627355, crossing5.938027856, max radius15.249753922, nominal/tolerance rim2.625246078/2.271692687, and central clearances4.025964796/3.975964796/4.425964796. Complete-domain `g_rim>=2.00` and shaft-to-workpiece/rod/tool/frame certificates replace nominal-only arithmetic. |
| PASS21-03: The previous C predicate lifted only a connector/local vertical payload by 16 mm and omitted the horizontal/bend material and the mechanism-opening actions needed for removal. | Section8 defines connected `W_complete`, requires valid OPEN, reverses all three right caps, synchronously withdraws all three rod/left-cap units left/off the jig, derives the full-workpiece lift from global mechanism/payload extrema, and leaves both cams, both fixed guides, shaft and keeper assembled. Section10/evidence/I10/I11/I16 reject connector-only, one-rod-only, pre-OPEN, 16-mm, or cheek-removal shortcuts. |
| PASS21-04: Service disassembly order could imply passing OD5.60 shaft stock through production ID4.80 fixed journals and did not match the required downward fixed-guide release. | The fixed C-guide profile is mirrored to an upward mouth: assembly is +Z from below and service release is -Z. Service is rods off, keeper radial off, both guides -Z off grooves, then fused actuator/shaft +X through the stationary keyed left cam; exact sweeps explicitly reject OD5.60 through ID4.80. Normal operation never performs service disassembly. |
| PASS21-05: The new pivot and workflow could be patched numerically without propagating to tests, evidence, and exports. | The `P13Params` dependency graph now includes the entire pivot-to-pose/stock/path/C-space/clearance/removal/evidence chain, safe `c_sw`/wire retunes, RE-GATE-required `shaft_od`/`R_bend` changes, fresh-process metamorphic tests, deterministic manifest/source provenance, and STEP parity. I17/I18 and evidence item16 make any stale `(0,30)`, independently shifted dependent, or hand-edited artifact a hard failure. |

## 15. Physical acceptance boundary

- Measure the user's actual rod diameters and lengths, XT60 body/cups, stripped
  lead, and 12 AWG insulation OD before print-fit acceptance. Roll/fixture each
  full 50-mm rod against a metrology datum, fit its centreline and local
  tangent, and require maximum radial deviation `e_straight<=0.05 mm` plus
  maximum tangent error `beta_straight<=0.05 degrees` before admitting it to a
  P13 specimen. Capture/freeze the exact measured rod BREP and endpoint frames
  as `W_hat_i(p_c)`; every physical CAD proof uses its declared rigid placement
  `W_i(p_c,x)` and the
  tolerance audit repeats over admitted `U_i`. `W_i_env` is only a conservative
  rejection precheck. Because the existing analytical lane has only
  `0.0214466095 mm` radial clearance, the current design is permitted to fail
  this conservative envelope gate. That failure triggers geometry/intent
  re-Gate; it does not authorize widening a lane or dropping the uncertainty.
- Measure actual ESC pad XYZ size/location, stripped copper OD and length,
  insulation-end plane, typical solder-blob envelope, and iron tip/barrel
  geometry before solder-access acceptance; Section10 values are provisional.
- Measure and register the real FPV frame/ESC external BREP as
  `Frame_ESC_ref(p_c)` before final shaft/frame and removal acceptance. A
  provisional box is exploratory evidence only and cannot close
  `phi_shaft_frame` or real-stack removal.
- Print same-orientation lane coupons `4.55/4.65/4.75` and left blind sockets
  around `3.90`. The separate P16 PETG gate tested one fixed `Ø4.20` right-cap
  cavity with `Ø4.05/4.10/4.15` throats; all three were usable and `Ø4.10` is
  the centred production default.
- For every left blind-cap coupon, record the measured socket and rod diameters,
  insertion force over `q_L=0..3.00`, final seated engagement, OD growth,
  cracking, creep, and pull-off force. The nominal `0.05-mm` radial-per-side
  interference is a geometry input, not proof of elastic safety or retention;
  accepted production caps remain permanently paired with their rods.
- Print C-journal coupons at seated IDs `4.80/4.85/4.90` and throats
  `4.10/4.20/4.30`; radial play, snap force, arm strain, and recovery are
  physical-only. Production source remains exactly `ID4.80`; its as-printed
  dimensions feed the coupled optimizer. The `4.85/4.90` coupons are diagnostic
  only and may inform a future source regeneration/re-Gate, never selection in
  current P13. The p-sum inequality is reported only as a concentric-seed
  diagnostic, not an approval or rejection rule; exact `Q_LF/Q_RF` components
  control the audit.
- Print left-cam centre-fit coupons with round bores `5.60/5.70/5.80` and keyed
  profiles. Current production source is frozen at `ID5.70`, tangential width
  `1.50` (`|v|<=0.75`), radial interval `u=2.50..3.50`, and roof `u=3.50`.
  `ID5.60/5.80`, widths `1.60/1.70`, and roofs `3.55/3.60` are diagnostic only;
  they measure insertion force, flank gap, angular backlash, and wear but cannot
  be selected into current P13. Any nominal change requires source regeneration
  and renewed Gate-0 intent/geometry review. Under the P21 pivot ID5.80 no
  longer fails central radial clearance; its exclusion is architectural and
  may not be relaxed by that numerical result.
- Test fixed plate thicknesses `2.8/3.2/3.6 mm`; the CAD brief makes no strength
  or warping conclusion.
- Bench-test C-journal arm strain/recovery/snap life, axial endplay and bearing
  wobble from the retained 0.10 land gap,
  racking/binding, cam torque, press retention, rod-cap snap
  recovery, key insertion/removal, measured left/right cam phase/backlash,
  selected-fit rod skew `<=0.05 degrees`, PETG/ASA heat response, wire marking,
  forming force, springback, final physical angle, actual soldering access,
  simultaneous three-rod pull ergonomics, six-cap handling, completed
  horizontal+bend+vertical workpiece lift with the four-plate structure still
  assembled, service-only downward fixed-guide release, real-stack removal,
  external clamping, and one-handed operation.

Gate 0 passes only when the design and math critics independently report zero
unresolved findings against this exact brief. Implementation then follows the
separate design -> implement -> critic/review -> repair loop; passing CAD tests
never overrides a failed intent review.
