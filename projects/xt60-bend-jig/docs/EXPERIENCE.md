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
