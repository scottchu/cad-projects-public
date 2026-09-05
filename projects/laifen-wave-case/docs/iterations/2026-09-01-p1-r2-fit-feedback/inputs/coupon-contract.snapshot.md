CDE-01; owner `/root/case_coupon_design`; design only. Baseline repository `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`, project `projects/laifen-wave-case`, iteration `2026-09-01-p1-r2-fit-feedback`. Verified input manifest `inputs/coupon-design-inputs.sha256`, fingerprint `ecaeb5478c7fe92dcc09baa7b5381c2ffb0b0c464cfd1214ef95e2e074cd3305`. Source geometry does not yet exist.

## Experiment authority and boundary

User explicitly offered a short test cap after supplying a pyramidal/diamond grip image. This contract authorizes an original short-cap experiment independent of unmeasured toothbrush L. It does not resolve the full case's actual L/D, end contact, retention, length, or physical acceptance, and does not authorize printer start. The current measurement-preview contract remains separate. Image inspected: raised faceted grip intent only; no geometry, branding, or dimensions are copied.

Deliver one common male open ring and three otherwise identical closed-end caps, with nominal radial thread clearance c = 0.20, 0.25, 0.30 mm. This minimizes material and isolates female-clearance changes against the same printed male. Alternate testing order and record wear/order; use an additional male only if damage/wear confounds comparison. Every later full-case generator must call the same thread/collar construction and preserve the tested zones before coupon evidence can transfer.

Use sequence: identify c, align starts, turn by hand to the external shoulder, inspect grip/fit/rocking, unscrew, repeat five empty cycles. No toothbrush is needed in this experiment. Do not force a binding pair.

## Numeric choices and bounds

All units mm. Fixed experiment parameters: pitch p=2; one-start right-hand thread; lower bore30; cap main bore31; nominal main wall2.4; male thread root radius16.8; radial tooth height h=0.6; male crest radius17.4; female collar outer radius19.5; cap closed floor3. Variable c is restricted to the three values above; arbitrary dimension edits require a new contract.

Derived budget: male root wall16.8-15=1.8. Female cavity root radius17.4+c =17.60/17.65/17.70; remaining smooth collar wall19.5-(17.4+c)=1.90/1.85/1.80. Female cavity crest radius16.8+c. Thus worst collar OD39 and minimum1.8 coexist; this needs a smooth enlarged collar. The cap main shell OD is31+2(2.4)=35.8. Raised grip height <=0.6 gives main grip OD<=37.0, below the collar OD39. Never apply raised grip on the OD39 collar or cut texture into the thread root wall.

The minimum1.8 at roots is an explicit experiment design assumption; nominal wall2.4 applies to the unthreaded shells. It is not a strength or perimeter-path proof.

## Exact original screw profile

Let theta be the right-handed angle about assembly +Z, viewed from +Z counterclockwise positive. Let q be z-p*theta/(2*pi), wrapped to [-p/2,p/2], and a=abs(q). The common infinite male outer profile M is:

- a<=0.15: radius17.4 (crest flat width0.30).
- 0.15<a<0.85: radius17.4-(0.6/0.7)*(a-0.15).
- 0.85<=a<=1: radius16.8 (root flat total width0.30).

The matching female inner profile is exactly M+c, not an unrelated thread standard. c is a radial offset at identical theta/z; it is not diametral, normal, or axial clearance. Diameter difference is2c. Flank-section normal gap is approximately c/sqrt(1+(6/7)^2)=0.152/0.190/0.228; helix adds a small angular term. Approximate free axial travel to either flank from the centered position is c/(6/7), not c. Physical backlash and fit remain unknown.

Exposed flank radial/axial slope6/7 gives atan(6/7)=40.60 degrees from build vertical in a meridian section. Helix angle at the root is atan(2/(2*pi*16.8))=1.09 degrees. The true helical normal must be checked, not replaced by the meridian number. With r=M(q), |n_z|/sqrt(n_r^2+n_theta^2) = |M'|/sqrt(1+(p*M'/(2*pi*r))^2) <=6/7; this bounds the downward-facing helical surfaces within the intended45-degree overhang limit in either upright print orientation. This is geometric intent only; slices/print remain unverified.

Own build123d Helix/profile construction is required; no downloaded mesh or copied thread mesh. The mathematical profile above is authoritative even if a sweep's moving frame changes the generated section. Verify actual meridian sections. If an additive ridge embeds epsilon=0.05 into the root cylinder for reliable union, extend each outer flank along the SAME slope to axial half-width0.85+epsilon/(6/7)=0.908333333 at radius16.75; crest remains +/-0.15 at17.4. Do not merely drop the same-width profile deeper and thereby steepen the exposed flank. Overbuild and trim tools outside functional bounds; tool-extension turns never count as engagement.

## Assembly coordinates and end treatments

Fixed male: external shoulder plane z=0; body/ring spans z=-8..0; neck spans0..9. Female cap at closed pose: mouth/shoulder z=0; exterior closed end z=25; inner floor z=22. Both axes coincide and phase is q=0 at theta=0,z=0. These define reusable mating datums, not the future case length.

Male base cylinder: bore radius15 throughout; OD radius17.4 from z=-8..-4.1, then conical flare to19.5 atz=-2 (radial rise2.1 / axial2.1), flange19.5 from-2..0. Above shoulder the radius obeys the finite thread rule below. Overall ring height17. No closed floor or cap-like obstruction in the ring.

Define male amplitude ceiling e_m(z): 0 on0..1; 0.6*(z-1) on1..2; 0.6 on2..8; 0.6*(9-z) on8..9. Male outer radius is min(M,16.8+e_m). This is a geometric envelope intersection, NOT multiplication of thread height by a fade; multiplication can steepen the lead flank. It provides a1mm free shank,1mm bottom runout,6mm full-form zone,1mm top lead.

Female collar inner radius is max(M+c,16.8+c+e_f(z)), where e_f=0.6 on0..1, 0.6*(2-z) on1..2, 0 on2..8, and0.6*(z-8) on8..9. From9..10.2 inner radius is17.4+c. Outer collar radius19.5 on0..10.2. The female entry/runout likewise uses max envelopes rather than multiplicative fades. No annular undercut with an unsupported horizontal ceiling is introduced.

Fromz=10.2..12.4, linearly reduce female inner radius17.4+c to15.5 and outer radius19.5 to17.9. From12.4..22 main bore is15.5; exterior radius17.9 continues through the closed end25. Taper wall is linear from at least1.8 to2.4. Largest taper radial change is2.2 over2.2, and outer build-up is1.6 over2.2. In the cap print direction the inner cavity widens toward the opening while the exterior expands at slope1.6/2.2. Male tipz9 has1.2 axial margin to the first internal bore reduction at10.2 and13 to the inner floor22 at full shoulder closure. Thus the shoulder, not the male tip/floor or an internal ledge, is the intended positive stop.

Effective engagement is the axial intersection length of BOTH full-form intervals, each[2,8], at the centered closed phase:6mm =3 pitch lengths. It excludes the entry/runout/free-shank zones and does not mean nine millimeters of neck overlap or five millimeters of old-case overlap. Overall penetration is9mm. These coupon numbers do not silently change the full-case schematic overlap5; future full-case design must reconcile that stack explicitly.

Shoulder contact is the planar annulus z=0, r in[17.4+c,19.5]. Keep it smooth and unchamfered. It is the only intended closed-state interpart contact. Do not enlarge female entry radius beyond17.4+c, which would break the worst-case1.8 wall budget.

## Printing, labels and grip binding

Male print transform: translate assembly z by+8, opening up; bed is original z=-8. Cap print transform: rotate180 degrees about X and translate+25 inZ, opening up; bed is original z=25. Reversing cap axis is a proper rotation, not a mirror of thread handedness. Provide named bed, screw-axis, shoulder, tip, full-thread-start/end, inner-floor and grip-phase datums plus native part labels and a source-level cylindrical/rigid relationship for generated closed and service poses.

Male bed rim inner and outer chamfers0.30x0.30 leave first-layer ring wall2.4-0.6=1.8; their inclines are45 degrees. Cap exterior bed edge chamfer0.30x0.30. Functional threads are above these bed zones. Lead envelopes relieve the starts; do not add arbitrary chamfers into the minimal female collar wall. No drainage holes in this first coupon: avoiding extra floor variables isolates thread/grip testing. Closed floor remains3 throughout except permitted label recesses below.

Cap labels `20`, `25`, `30` are raised0.2 on the INTERIOR floor (print-up face, assembly z21.8..22), stroke width>=0.6, glyph height>=3, inset>=2 from the bore. This preserves minimum floor3 and leaves12.8 minimum male-tip clearance. Labels remain clear of threads, shoulder, grip and opening zones. Name the common ring `M` in the source/export manifest; no tiny physical ring label is required.

Grip geometry is a dependency on PAT-01's independently frozen original pattern contract; until bound, no textured CAD implementation is ready. Available cap texture region is assembly z14.4..20.0 on main radius17.9, with>=2mm from taper and inner-floor junction. Full fixed-pitch repeats must fit within5.6mm; choose repeat count by floor, center whole repeats, never Z-scale them. Height<=0.6, blunt tips, lower facets rising no faster than1 radial per1 axial; constant axial pitch and circumferential seam closure need explicit PAT-01 values. Shared closed-assembly angular/axial phase is retained for future paired shells; this ring coupon does not prove future full-case phase continuity.

## Required evidence before a print candidate

1. Math/parameter bounds: reject c outside the declared set and invalid fixed dimensions; independently verify radial budgets at all c,6mm effective full-form overlap, profile slope including embedded root, lead envelope slopes, taper and first-layer widths. Failure caught: apparently compatible nominal threads consuming all collar wall or possessing steeper real starts.
2. Actual solids/constraint: one connected positive-volume solid per part; bore30 throughout ring except the declared0.3mm bed-edge relief, cap main bore31; minimum walls in full thread and taper sampled at crest/root/flank phases and CAD boundaries; outer envelope<=39; cap height25/ring17; named datums; correct handedness; floor/label clearance; smooth shoulder and texture exclusion. Phase-sampled sections must match M+c and the min/max envelopes, includingtheta0,90,180,270 at axial feature boundaries. Toolpath/sweep approximations require declared geometric tolerance<=0.01mm; never erase the0.05 clearance differences through meshing tolerance.
3. Motion/collision: drive cap rotation beta about world+Z and gap g=p*beta/(2*pi), with beta0..9*pi radians (0..1620 degrees); closed beta0/g0. Because q is invariant under this screw transform, M phase remains matched wherever finite domains overlap; male<=M and female>=M+c prove radial separation in the screw band. Independently test actual solids at beta0,15,45,90,180,360,720,1080,1440,1620 degrees for every c, including lead/taper/shoulder zones. Allowed interpart intersection volume<=1e-6mm3 numerical tolerance, no positive-volume contact. Atbeta0 shoulder separation0; atbeta15 it is1/12mm; full-form intersection length=max(0,6-g). Atg9 domains just separate; test straight axial removal fromg9 to11 and reverse entry. Test a small negative closure g=-0.02 with corresponding rotation to require shoulder collision, proving the positive stop precedes internal abutment. No collision-free claim follows from final pose alone.
4. Requirement/visual: four fabricated parts and three matched assembly variants; original source; actual short cap with closed floor and matching open ring; raised grip checked against reference intent; section, assembled, exploded and print-pose STEP snapshots. Validate actual written STEP geometry and source/export placement parity before meshes. Fabrication mesh tolerance must be sufficiently below the0.05 gap increment (target0.01 or better), manifold with matching quantities/units. Only a later real slicer inspection can establish support-free paths and distinguish printable grip flats/labels at0.4 nozzle,0.2 layer PLA.

Physical results remain pending: grip comfort, visible point quality, entry without cross-threading, shoulder seating, rocking/backlash, relative clearance preference, five-cycle wear, and actual support-free print quality. Root/layer strength and full-case length/brush fit/texture registration remain outside coupon acceptance. Record chosen c, exact source/artifact hashes, process/profile, test order and observations before transferring the interface.

Expected later source namespace `projects/laifen-wave-case/cad/p1_r2_coupons/`, with an original shared helper and explicit male, c20/c25/c30 cap and assembly `.step.py` entrypoints; primary STEP siblings and later secondary fabrication meshes. This contract creates no CAD/export artifact and requires no snapshot yet.
