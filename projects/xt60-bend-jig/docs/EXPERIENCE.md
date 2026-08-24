# XT60 bend jig experience and physical observations

Entries preserve observed evidence separately from CAD inference. Legacy source records remain under `docs/legacy/`.

## `2026-08-21` — PETG rod-hole coupon

- Context: printed rod-hole calibration coupon, PETG, `0.4 mm` nozzle, actual `OD4.00 mm` rods.
- Observations:
  - `4.05 mm`: very tight; the coupon had to be used to push the rod back out.
  - `4.10 mm`: tight; hand push and pull were possible.
  - `4.15 mm`: best sliding fit with slight friction.
  - `4.20 mm`: similar but looser.
  - `4.25 mm`: loose with wobble.
- Limitation: this evidence applies to the sliding rod-hole role and this print process, not every functional bore.
- Design implication: preserve `4.15 mm` as the sliding-fit reference until a new measured coupon supersedes it.

## `2026-08-21` — cap/throat coupons

- Context: upright-printed P16 removable right-cap throat specimens.
- Observation: all three latest specimens were usable; the two left specimens felt nearly identical.
- Limitation: this is initial hand-fit evidence for the exact removable right-cap `4.10` functional core. It does not prove the unslit permanent left `ID3.90` cap, cycling, wear, heat, or retention.
- Design implication: do not declare a universal throat winner or transfer the result to another cap role without a focused physical check.

## `2026-08-22` — missing-half and floating early-layer print preview

- Context: Snapmaker U1 preview of the earlier P13 3MF using PETG, `0.25 mm` first layer, and `0.20 mm` later layers.
- Observation: large plate faces were above the bed, producing incomplete or floating first layers; the shared `0.10 + 0.10 mm` thrust-land arrangement was not faithful to the first-layer process.
- Source repair: fixed thrust land `0.20 mm`, cam thrust land `0.00 mm`, `main_face_gap = 0.30 mm`, fixed-land shaft clearance `ID5.70`, and source-authored bed orientations for all plates and caps.
- Design implication: preserve source-defined orientation. Do not repair the artifact with slicer flipping, negative Z, or `Lay on face`.

## `2026-08-22` — latest print center-hole fit failure

- Context: user printed the latest available version.
- User observation: the "middle stick" is too thick for the "center hole".
- Confidence and limitation: this is a concrete physical assembly failure, but the user-facing names do not yet identify whether the interface is the printed D shaft, round journal, keeper, or another central feature.
- Design implication: before changing CAD, identify the exact printed parts and functional fit, add a regression representing the failed insertion/clearance, then enlarge only the responsible source-controlled hole. Regenerate dependent STEP/3MF/provenance and provide a Tailscale CAD Viewer URL for review.

## Pending complete P13 observation

- The latest print has not passed assembly because of the center-hole fit failure.
- After repair, record actual wire OD, dry `0..27 deg` motion, first contact, locked preload, binding, cap retention/removal, insulation condition, XT60 body loading, soldering access, PETG heat response, completed-part removal, cooled angle, and springback.

## `2026-08-23` — P13 physical assembly and counter-twist requirements

- Context: user supplied three photos after handling the printed P13 assembly.
- Photo references and SHA-256:
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/1-Photo-1.jpg`: `8604131d1b6ba3e636492a964d0c3d92811041bbf93696afefe0a8a20a976f93`.
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/2-Photo-2.jpg`: `d740f4e252e0bd1636dd674480c865949c3dbde21c6c6e2522d3a4e602c362ec`.
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B931B501-4470-4E89-82E8-BD46F0E51353/3-Photo-3.jpg`: `8d12c39427823ff36c4205e70716db6df1f166aab87d113b7a0a767bb7f079fe`.
- User observations and requirements:
  - Six rod-end caps are permanent; none are removable/service caps.
  - Four physical P13 caps fit the nominal rods; two were too tight to push onto the same nominal rods.
  - Two inner plates are fixed/grounded and do not rotate.
  - Two outer plates are the user-gripped rotating elements and rotate in opposite directions as a relative twist.
  - Outer plates must be larger than inner plates. The primary force/actuator outer plate should be slightly larger or provide a quantitatively larger grip/lever affordance.
  - P13's prescribed `LOCKED` pose is not proof of locking; a new design needs an explicit ground/reaction path and lock concept.
- Photo observations:
  - Photos 1 and 2 show CAD Viewer states with central shaft/keeper and colored slot/plate geometry that can read as moving holes or slots.
  - Photo 3 shows the physical P13 assembly with rods protruding, caps on rod ends, and a large middle spacing between the principal plates.
- Verified P13 nominal context supplied for P17 R2:
  - inner clear span `26.2 mm` vs XT60 body width `15.9 mm`;
  - rod length `50.0 mm`;
  - printed D-shaft total `45.275 mm`;
  - principal plate stack `37.4 mm`;
  - left cap `ID3.90` on `OD4.00` rod equals `0.10 mm` diametral interference.
- Limitation: the photos and hand observations do not prove cap retention, final cap interference, lock force, wire holding force, heat response, cycling durability, or springback.
- Design implication: P17 R2 must re-derive inner spacing, stack, rod length, cap engagement, fixed/moving roles, and lock path together. Do not preserve the `50.0 mm` rod freeze or `ID3.90` cap interference as accepted.

## `2026-08-24` — P17 simulator rejected; simulation skipped

- Context: the user reviewed the live P17 simulator over Tailscale.
- User observation: the simulator was unacceptable because the visible holes or slots appeared to move with the animation.
- User decision: skip simulation rather than repair or iterate it.
- Disposition: P17 R1 simulator evidence is rejected for product-direction approval even though its deterministic tests had passed. It must not be used as motion, architecture, CAD, or physical acceptance evidence.
- Version implication: this rejects the P17 R1 simulator artifact and its evidence, not the P17 counter-twist design version. Direct CAD, fit, lock, yoke, hub, rod, and cap refinements continue as P17 R2.
- Next-direction implication: preserve the physical mechanism requirements: fixed inner plates, opposite-rotating outer plates, a slightly larger primary force-side outer plate or quantified larger primary grip, six permanent caps, re-derived rod/stack/cap geometry, and real lock/reaction architecture. Do not copy the rejected simulator geometry or its provisional `18.5/64/60/50 mm` choices into P17 R2 CAD as accepted dimensions.

## `2026-08-24` — P17-D02 center-bar architecture correction

- Context: user clarified that P17 R2 should not add three yoke/stability bars
  and should instead use the original good four-plate plus one center-bar
  architecture.
- User decision: this is a refinement based on the prior version, not a
  redesign and not a new `P` number.
- Architecture direction:
  - one-piece stepped center axle;
  - larger central hex spacer section sets the fixed-inner clear span and
    provides axial shoulders;
  - smaller hex key sections pass through matching inner-plate hex bores so
    both inner plates are rotationally fixed and seated against the shoulders;
  - outer round journal sections support independent opposite rotation of the
    two outer plates;
  - thin outer keepers retain the axial stack;
  - no shared same-direction actuator coupling through the axle.
- Design implication: remove yoke/stability bars and yoke socket/tenon
  requirements from P17 R2 docs. Re-derive stack, rod, journal, keeper, and
  collision/service gates around the stepped center axle, especially because it
  crosses the XT60/wire span.

## `2026-08-24` — P17-D03 center-axle numeric/assembly correction

- Context: a read-only audit of the first center-axle implementation attempt
  exposed an impossible assembly path in the P17-D02 provisional defaults.
- Observation: an inner hex key/bore around `AF6` cannot slide over a round
  journal around `OD8`, contradicting the intended assembly sequence where the
  fixed inner plate is pushed over the outer round section before seating on
  the inner hex key.
- User decision: this is a focused P17 R2 refinement, not a new `P` version.
- Corrected design implication:
  - the round journal OD must be smaller than the fixed-inner hex bore
    inscribed diameter, which is the across-flats dimension for a regular hex
    bore;
  - coherent provisional defaults are central spacer hex `AF10`, inner key
    `AF8`, fixed-inner hex bore about `AF8.15`, round journal about `OD7.60`,
    and outer bearing bore about `7.90`;
  - the per-side axle segment must run from central spacer shoulder through
    full inner hex key engagement, running gap, full outer plate thickness,
    keeper clearance, and an actual retained keeper seat;
  - the axle solid must extend under the keeper, and a keeper must be retained
    by modeled press fit, seat/groove, split keeper, or equivalent actual
    geometry rather than represented as a floating ring.
- Limitation: these are CAD defaults and assembly invariants. Print fit,
  keeper installation/retention, PETG wear, and real force behavior remain
  physical gates.

## `2026-08-24` — P17-I04 visual rejection and fixed-axle identity correction

- Context: the user reviewed the live P17-I04 locked/exploded Viewer artifact
  on a phone and supplied four screenshots.
- Screenshot references and SHA-256:
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/53219609-F596-40A5-8E14-0867D84C2208/1-Pasted-Image-1.jpg`: `71d4c407ae645a32cf616c6fc7f0e34f2c8c5ac1bd47e77ec8fec2a445a280e8`.
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/53219609-F596-40A5-8E14-0867D84C2208/2-Pasted-Image-2.jpg`: `6064cb5005bfb50f92c61ae9b48fd201efc6a8e898b875650a217c912e7b5bbb`.
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/53219609-F596-40A5-8E14-0867D84C2208/3-Pasted-Image-3.jpg`: `d2e59057a67dc348708812adb33e0ef47b7912faff50c6484974a5b58f2d06b1`.
  - `/tmp/codex-remote-attachments/01a02c54-c344-75f0-a983-e2e2dd8162a7/B55E60F8-583B-4FAB-B574-A448109DDDBE/1-Pasted-Image-1.jpg`: `2a0b9383f9cbc990b78aadefdaac9daaf5f4b443c6a68fdbee05f4d977f4779d`.
- Observed visual failures: the purple printed stepped axle still read as a
  large centered axle through the outer plates; the lower white stainless rod
  appeared floating; and the static locked entry did not show motion.
- User identity correction: the fixed member is the purple printed stepped
  axle shown in the exploded screenshot. It is fixed to both inner plates.
  White stainless rods remain moving forming/locking rods and are not the
  fixed reaction rod.
- User motion correction: move the purple axle farther behind/off the outer
  plate center. Give each outer plate its own axle guide rail, mirrored so one
  permits clockwise and the other counter-clockwise travel. Inner plates and
  axle stay fixed; outer plates move.
- Rejected interpretation: the initial D06 reading that proposed fixing the
  lower white stainless rod was wrong and was stopped before source or
  artifact implementation.
- Mechanical limitation: one fixed pin in one arcuate slot does not alone
  reduce a free planar plate to one rotational degree of freedom. The smallest
  no-new-part closure is to retain the existing rod/slot contact network; a
  focused motion preview may prescribe the intended rigid transforms but must
  not call the rail alone a complete physical constraint.
- Version implication: this is a focused P17 R2 repair, not a P or R bump.
  Viewer/simulation quality and a bounded geometry correction are evidence and
  implementation changes, not new product-version identities.

## `2026-08-24` — P17-D07 provisional axle-datum failure and repair

- Context: the first D06 implementation probe kept the outer rotation center,
  all white-rod paths, and all plate dimensions frozen while moving the purple
  axle to the provisional `A=(-18.00,17.00) mm`.
- Actual-solid failure evidence at that datum:
  - inner hex-bore cutter vs frozen upright fixed-guide cutter:
    `68.3212367 mm^3` intersection;
  - left outer axle-guide cutter vs frozen upright cam cutter:
    `34.0035540 mm^3` intersection;
  - right outer axle-guide cutter vs frozen upright cam cutter:
    `128.9744351 mm^3` intersection;
  - analytic signed webs: inner `-3.915 mm`, left outer `-2.195 mm`, right
    outer `-5.042 mm`, against required `+2.20 mm`.
- Scope disposition: this invalidates only D06's provisional axle location.
  It does not invalidate the purple-fixed/white-moving identity, off-center
  axle architecture, mirrored guide equations, opposite outer motion, or P17
  R2 version.
- Feasible-region evidence with `C=(-10.60,17.00)` and frozen features:
  a same-Z analytic scan found `>=2.20 mm` minimum web from approximately
  `A_y=-27.5` through `-30.5 mm`; `A=(-29.00,17.00)` maximized the sampled
  minimum near `3.849 mm` while moving the axle farther behind.
- Independent exact BREP evidence at `A=(-29.00,17.00)`:
  - all inner hex-to-guide/window/receiver and outer guide-to-cam/grip/lock-
    nose cutter intersections were zero;
  - minimum exact frozen-feature distance was `3.650 mm`;
  - all four local plate results were valid single solids;
  - over 33 motion samples, axle/outer, keeper/outer, axle/rod, and keeper/cap
    unintended intersections were zero;
  - minimum axle-to-outer guide clearance was `0.150 mm`; keeper radial
    capture was `1.050 mm`;
  - sampled XT60/service minimum clearance was `19.1764973 mm`, with zero
    intersection;
  - fixed-axle reconstruction error was `7.11e-15 mm` and mirror error zero.
- Limitation: these are design-search and source-BREP results from a WIP
  implementation, not independent candidate validation or physical proof.

## `2026-08-24` — Current lock rejected for removal and rod/axle identity clarified

- The user marked two Viewer regions. Full-resolution correction identifies
  the first as the orange fork-like right-outer lock nose and the second as the
  green `left_outer_secondary_grip_block`, an integral finger/force tab on the
  green outer plate. The second circle is not the receiver or lock geometry.
- Source inspection independently identifies the nose's actual grounded lock
  counterpart as the right-inner receiver/bridge/catch assembly.
- User direction: remove the complete mechanism first and add no replacement
  lock in this bounded iteration. Therefore remove the first screenshot's
  nose and its source-identified receiver, but retain the green grip tab.
- Design consequence: retain `0..32 deg` counter-twist motion as travel only;
  do not claim a hard stop, detent, over-center capture, or self-lock.
- Dimension clarification: the user's stainless rods are `50.00 mm` physical
  stock. The accepted P17 source currently models a re-derived `40.60 mm` rod
  target. The purple printed axle is independently derived as `34.90 mm` to
  span the `32.00 mm` four-plate stack plus `1.45 mm` keeper clearance/seat per
  side. The axle is not supposed to reach the rod caps.
- Boundary: deciding whether P17 must return to uncut `50.00 mm` stainless
  rods is a separate rod/cap-stack decision. The lock-removal iteration must
  not silently change either rod length or axle length.
