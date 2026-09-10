# P20 R4 custom-profile full CAD design contract

Status: **FROZEN ANALYTIC CONTRACT; EVIDENCE-ONLY FULL CAD PREVIEW MAY PROCEED**

## Pure path authority

For rod `r`, with START polar point `S_r`, the P19 base END `E0_r`, common
offset `D`, inner arch `a_r=0`, and `u in [0,1]`:

```text
E_r = E0_r + D
P_r(u) = (1-u) S_r + u E_r
L_r(u) = R(-45u) P_r(u)
R_r(u) = R(+45u) P_r(u)
```

`L_r` and `R_r` are the complete left/right outer-plate local inverse rails.
Forward physical plate rotations `+45u/-45u` reconstruct `P_r(u)` exactly.
The implementation must expose one deterministic reusable function for this
math; inner and both outer rail builders must delegate to it. BREP and export
logic must not duplicate the equations.

For the fixed axle `A=(-10,-10)`:

```text
F_L(u) = R(-45u) A
F_R(u) = R(+45u) A
R(+45u) F_L(u) = A
R(-45u) F_R(u) = A
```

Both fixed guides use a `7.90 mm` cutter. White-rod cutters are `4.15 mm`.
`PATH_STEPS=360`, `arch_peak=0.5`, and `curve_bias=0` are frozen.

## Exact OPEN/MID/END coordinates

Coordinates are `(Y,Z)` in millimetres.

| rod | OPEN/world | MID/world | END/world |
|---|---:|---:|---:|
| Blue / bottom | `(-7.511545005,14.127161486)` | `(-2.641733675,9.687731715)` | `(2.228077655,5.248301944)` |
| Orange / diagonal | `(11.313708499,11.313708499)` | `(9.895893077,5.406005222)` | `(8.478077655,-0.501698056)` |
| Green / upright | `(14.728077655,-6.251698056)` | `(14.728077655,-6.251698056)` | `(14.728077655,-6.251698056)` |

The Green path is therefore a round inner bore, not an elongated inner slot.
Its outer local path is still a full 45-degree arc because the outer plates
rotate around a world-stationary Green rod.

| feature | OPEN local | MID local | END local |
|---|---:|---:|---:|
| fixed axle, left outer | `(-10,-10)` | `(-13.065629649,-5.411961001)` | `(-14.142135624,0)` |
| fixed axle, right outer | `(-10,-10)` | `(-5.411961001,-13.065629649)` | `(0,-14.142135624)` |

## Plate and part contract

- Inner plates: both `R20.0 / Ø40.0 x 3.20 mm`, fixed in world, same YZ cuts.
- Outer plates: both `R22.5 / Ø45.0 x 3.20 mm`, independently rotating.
- Fixed axle: preserve P19 stepped axle construction and keepers, translated
  as a complete functional occurrence to `A=(-10,-10)`.
- Rods/caps: preserve the existing P19/P20 R3 X geometry, six caps, occurrence
  identities, rod OD and length.
- Workpiece: delegate to P20 R3's exact vertical leg + tangent `R6`
  quarter-circle + horizontal `+Y` tail; do not reuse P19's diagonal wire.
- XT60 reference: preserve P20 R3/P18 coordinates and orientation.

## Per-object delta mask

| object | may change | frozen/forbidden |
|---|---|---|
| inner plate bodies | radius to `20.0`; cuts from exact profile | thickness/X placement; Green elongated rail; omitted Blue/Orange rail |
| outer plate bodies | both radii to `22.5`; exact inverse rod and axle cuts | thickness/X placement; any missing/endpoint-only rod rail; rotation about `A` |
| three rods | YZ trajectories from profile | OD, `50 mm` X length, identity or count |
| fixed axle/keepers | complete YZ move to `(-10,-10)`; exact inverse axle rails | stepped geometry, X stack, keeper geometry/count, world-fixed role |
| caps | follow each rod trajectory | geometry, `9.05 mm` height, engagement, count, hidden caps |
| workpiece/XT60 | use exact P20 R3 90-degree reference | diagonal wire, move, resize or reorientation |
| motion | left/right `+45/-45`, common `u` | same-direction motion, independent timing, moving inner plates |

## Analytic preview warnings

The exact simulator reports these sampled geometric margins:

- inner feature gap `3.269 mm`;
- inner rim web `1.152 mm` at the fixed-axle hex: below the existing
  `2.20 mm` prototype design threshold;
- left outer minimum rail-to-rail web `1.715 mm`, Blue–Orange: user granted
  temporary test-only interest, not full-product physical acceptance;
- right outer minimum rail-to-rail web `2.230 mm`;
- both outer rim webs `4.408 mm`.

The inner-rim and left-web failures prohibit manufacturing acceptance. The
user explicitly requested the full geometry as an intent/preview artifact, so
implementation may continue only as a visibly labeled **non-manufacturing
preview candidate**. These failures must remain visible in validation and may
not be hidden by a snapshot angle.

## Required implementation and review paths

- Source: `projects/xt60-bend-jig/src/xt60_bend_jig/p20_r4_custom_profile_full_cad.py`
- Focused tests: `projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py`
- Primary full-motion generator/artifact:
  `projects/xt60-bend-jig/cad/p20_r4_custom_profile_full_cad/p20_r4_full_motion.step.py`
  and matching `.step`
- Static generators/artifacts: matching `p20_r4_open`, `p20_r4_mid`,
  `p20_r4_end`, and `p20_r4_exploded` `.step.py/.step` files
- Viewer sidecar: `p20_r4_full_motion.params.js`
- Snapshots:
  `projects/xt60-bend-jig/docs/review/p20-r4-custom-profile-full-cad/`
  with OPEN front, MID front, END front, and exploded/axial images.

## Validation gates

1. **Math:** exact profile JSON hash; path endpoints; Green travel `<=1e-9`;
   inverse round-trip residual `<=1e-10`; deterministic 361-point paths;
   left/right sign and fixed-axle reconstruction.
2. **User requirements:** 18 occurrence census; four plates, three rods, six
   caps, axle, two keepers, XT60 and 90-degree workpiece; complete rail
   presence/absence; no coupon-only artifact.
3. **Constraints:** exact radii/thickness/X stack/rod dimensions; report the
   known `1.152/1.715 mm` failures rather than accepting them; measure written
   STEP occurrences and bounds.
4. **Actual-solid collision:** OPEN/MID/END plus meaningful closest-approach
   samples; explicitly allow intended rod-in-own-cut and axle-in-own-guide
   contacts only; list every unexpected intersection by pair and state.
5. **Motion/service:** rods remain supported by both inner and outer plate
   features through `u=0..1`; fixed axle remains world invariant; exact P20 R3
   XT60/wire envelope is checked for trapping; cap/plate axial clearance is
   reported without optimization.
6. **STEP parity:** source and STEP have equal occurrence census, labels,
   bounds and valid closed positive-volume solids; no double transforms.
7. **Visual:** mandatory snapshots show the complete assembly and clearly
   expose caps, plate spacing, fixed axle, all rod rails and 90-degree wire.
   Exact Viewer page and artifact readiness must both succeed before handing
   the preview to the user.

No gate may call this physically accepted. The final independent review can
approve only delivery of the full intent preview for user confirmation.

