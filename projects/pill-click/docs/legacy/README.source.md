# Pill Click

Parametric pill click model for 3D printing, built with Python and
[`build123d`](https://build123d.readthedocs.io/).

## Progressive workflow

- **P0 mechanical-fit V2 — physically tested baseline:** its four rails and
  rail-based front stop passed the first complete physical print. The rear
  side-squeeze cover works but is too easy to pull off, so its retention is not
  accepted unchanged. It has exactly three
  dispenser parts, 13.40 mm manual travel, a solid rounded/tapered key, four
  continuous male rails in housing-side female channels, and a blind rear
  cover released by squeezing two side pads. Print the two-piece C5 latch
  coupon first. It deliberately has no medicine openings, return force,
  push-push mechanism, magnet, spring, or text.
- **P0 mechanical-fit V2.1 — next keyboard-identity test:** preserves the
  successful V2 rails and front stop, increases rear-clamp beam thickness and
  hook engagement, and gives the button an 8 mm-tall straight keycap taper,
  1 mm face-rim fillet, and shallow 0.55 mm finger dish.
- **P0 mechanical-fit V2.2 — layer-aware rear latch test:** rejects the V2/V2.1
  upright latch after a printed root fractured in roughly 5–10 removals. It
  preserves the V2.1 key, accepted rails, stops and 13.40 mm travel, but moves
  flexing into two long beams per side in the flat rear-cover print plane. All
  critical latch dimensions are based on a 0.40 mm nozzle. Physical acceptance
  requires 100 squeeze cycles and 25 complete cover-removal cycles.
- **P0 mechanical-fit V2.3 — current print candidate:** preserves the accepted
  V2 rail cross-sections and front stops while using states 3.40 to 13.40 for
  10.00 mm physical travel. It has one uninterrupted keyboard-key taper with a
  flat, R0.90 edge-filleted face. The thin retaining ridge is replaced by a
  full-height hook: 1.20 mm axial shelf, 0.80 mm radial engagement, 10.00 mm
  height, and a 2.00 mm (five-nozzle) supporting tower. The rear pilot is
  3.20 mm deep with a 0.40 mm 45-degree entry. Four broad rail-aligned bosses
  provide a verified inward stop at state 3.40. Its 10 mm-tall side squeeze
  surfaces remain flush with the 40 mm cover envelope, and both compliant side
  strips remain 2.00 mm wide. CAD checks pass, but physical fatigue remains
  gated by 100 squeeze cycles and 25 install/removal cycles.
- **P0 mechanical-fit V1 — preserved baseline:** the earlier three-part
  implementation remains available for comparison but is no longer the next
  print candidate.
- **P0 V3.1 C1R1 — manual slider:** CAD implementation awaiting independent
  review. It strengthens the failed short rail lands with 6.80 mm lands,
  0.80/0.60 mm normal/mouth lips, and four backing ribs. It otherwise preserves
  the captive
  shuttle, aligned/hidden medicine ports, solid shutters, blind rear cover,
  rear-feed assembly, and C1-C4 fit coupons. CAD acceptance does not approve
  physical force, fit, fatigue, food-contact suitability, or child resistance.
- **P1 — return force:** the current `pill_click_spring` and
  `pill_click_magnet` files are exploratory WIP only. They are not accepted
  extensions of P0 V3.1 and should not be printed as a validated mechanism.
- **P2 — push-push latch:** pending. It will add first-press latch/open and
  second-press release/close behavior after P0 coupons and P1 force experiments.

## Setup and checks

```sh
uv sync
uv run pytest
uv run pytest -q tests/test_p0_mechanical_fit_v2_keyboard_inverted_rails.py tests/test_p0_mechanical_fit_v2_keyboard_inverted_rails_artifacts.py
uv run pytest -q tests/test_p0_v3_spec.py tests/test_p0_v3_geometry.py tests/test_p0_v3_coupons.py tests/test_p0_v3_print_exports.py
uv run pytest -q tests/test_p0_mechanical_fit_v1.py tests/test_p0_mechanical_fit_v1_artifacts.py
```

## P0 mechanical-fit V2 generation

V2 lives in its own source package and does not modify V1. Generate its STEP,
STL, and 3MF artifacts from this directory:

```sh
CADPY=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/packages/cadpy
CAD_STEP=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/step

uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/p0_mechanical_fit_v2_pressed.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/p0_mechanical_fit_v2_released.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/p0_mechanical_fit_v2_maximum_pull.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/print/p0_mechanical_fit_v2_outer_female_guide_housing.py --stl p0_mechanical_fit_v2_outer_female_guide_housing.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/print/p0_mechanical_fit_v2_solid_keyboard_button_male_rails.py --stl p0_mechanical_fit_v2_solid_keyboard_button_male_rails.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/print/p0_mechanical_fit_v2_blind_two_side_latch_rear_cover.py --stl p0_mechanical_fit_v2_blind_two_side_latch_rear_cover.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/print/p0_mechanical_fit_v2_three_part_bundle.py --3mf p0_mechanical_fit_v2_three_part_bundle.3mf
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/coupons/C5_V2_side_latch_arm_cover_specimen.py --stl C5_V2_side_latch_arm_cover_specimen.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/coupons/C5_V2_side_latch_housing_receiver_specimen.py --stl C5_V2_side_latch_housing_receiver_specimen.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v2_keyboard_inverted_rails/coupons/C5_V2_one_side_latch_pad_notch_coupon_assembly.py --3mf C5_V2_one_side_latch_pad_notch_coupon_assembly.3mf
uv run python -m pill_click.threemf_compat \
  models/p0_mechanical_fit_v2_keyboard_inverted_rails/print/p0_mechanical_fit_v2_three_part_bundle.3mf \
  models/p0_mechanical_fit_v2_keyboard_inverted_rails/coupons/C5_V2_one_side_latch_pad_notch_coupon_assembly.3mf
```

The final command rewrites only the two OPC wrapper XML files that strict
slicers such as OrcaSlicer require to use default namespaces. The 3D model XML
and component geometry are left byte-for-byte unchanged.

The frozen dimensions and proofs are in
`docs/p0-mechanical-fit-v2-keyboard-inverted-rails-spec.md`. Print order and
physical acceptance are in
`docs/p0-mechanical-fit-v2-keyboard-inverted-rails-test-plan.md`. Generated
hashes, mesh facts, and reviewed snapshots are recorded in
`models/p0_mechanical_fit_v2_keyboard_inverted_rails/p0_mechanical_fit_v2_manifest.json`.
The manifest is `accepted_for_C5_first_physical_print`. Independent CAD review
passed, but CAD validation does not replace the C5 physical test; do not print
the complete three-part dispenser until the two-piece C5 coupon passes.

## P0 mechanical-fit V2.1 keyboard-identity generation

V2.1 is a separate source package; the physically tested V2 files remain
unchanged. Generate the current STEP review set with:

```sh
CADPY=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/packages/cadpy
CAD_STEP=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/step

uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v21_keyboard_identity/p0_mechanical_fit_v21_inner.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v21_keyboard_identity/p0_mechanical_fit_v21_pressed.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v21_keyboard_identity/p0_mechanical_fit_v21_released.py
uv run pytest -q tests/test_p0_mechanical_fit_v21_keyboard_identity.py
```

The frozen parameters, physical-test evidence, and validation contract are in
`docs/p0-mechanical-fit-v2.1-keyboard-identity-spec.md`.

## P0 mechanical-fit V2.2 planar-latch generation

V2.2 is a separate durability experiment. Generate its STEP review set with:

```sh
CADPY=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/packages/cadpy
CAD_STEP=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/step

uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v22_planar_latch/p0_mechanical_fit_v22_inner.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v22_planar_latch/p0_mechanical_fit_v22_rear_cover.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v22_planar_latch/p0_mechanical_fit_v22_pressed.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v22_planar_latch/p0_mechanical_fit_v22_released.py
uv run pytest -q tests/test_p0_mechanical_fit_v22_planar_latch.py
```

The print-driven dimensions, strain equations and physical cycle gate are in
`docs/p0-mechanical-fit-v2.2-planar-latch-spec.md`.

## P0 mechanical-fit V2.3 keyboard/durable-latch generation

V2.3 is a separate correction; the rejected V2.2 artifacts remain unchanged.
Generate the STEP review set with:

```sh
CADPY=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/packages/cadpy
CAD_STEP=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/step

uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v23_keyboard_durable_latch/p0_mechanical_fit_v23_inner.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v23_keyboard_durable_latch/p0_mechanical_fit_v23_rear_cover.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v23_keyboard_durable_latch/p0_mechanical_fit_v23_pressed.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v23_keyboard_durable_latch/p0_mechanical_fit_v23_released.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v23_keyboard_durable_latch/print/p0_mechanical_fit_v23_three_part_test_bundle.py --3mf p0_mechanical_fit_v23_three_part_test_bundle.3mf
uv run python -m pill_click.threemf_compat models/p0_mechanical_fit_v23_keyboard_durable_latch/print/p0_mechanical_fit_v23_three_part_test_bundle.3mf
uv run pytest -q tests/test_p0_mechanical_fit_v23_keyboard_durable_latch.py
```

The frozen dimensions, collision sweeps, nozzle/layer interpretation, print
orientation, and physical fatigue gate are in
`docs/p0-mechanical-fit-v2.3-keyboard-durable-latch-spec.md`.

## P0 mechanical-fit v1 generation

This prototype is a separate source package and exactly three printed parts.
Its inner button is solid CAD geometry; choose material usage with slicer
infill rather than a modeled cavity.

```sh
CADPY=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/packages/cadpy
CAD_STEP=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/step

uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v1/p0_mechanical_fit_v1_pressed.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v1/p0_mechanical_fit_v1_released.py
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v1/print/p0_mechanical_fit_v1_outer_housing.py --stl p0_mechanical_fit_v1_outer_housing.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v1/print/p0_mechanical_fit_v1_solid_inner_button.py --stl p0_mechanical_fit_v1_solid_inner_button.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v1/print/p0_mechanical_fit_v1_snap_rear_cover.py --stl p0_mechanical_fit_v1_snap_rear_cover.stl
uv run --with "$CADPY" python "$CAD_STEP" models/p0_mechanical_fit_v1/print/p0_mechanical_fit_v1_three_part_bundle.py --3mf p0_mechanical_fit_v1_three_part_bundle.3mf
```

See `docs/p0-mechanical-fit-v1-test-plan.md` for print orientation, assembly,
cycle, force, and pull-test recording. Generated hashes and mesh facts are in
`models/p0_mechanical_fit_v1/p0_mechanical_fit_v1_manifest.json`; review status
remains `pending_independent_review`.

## Accepted P0 V3.1 STEP generation

The generated STEP files are derived artifacts; edit only the Python source.
Run from this directory:

```sh
CADPY=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/packages/cadpy
CAD_STEP=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/step

uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_pressed.py
uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_released.py
uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_c1r1_nominal_L6p80_lip0p80.py
uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_c1r1b_nominal_L6p80_lip1p20.py
uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_c2_rail_loose.py
uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_c3_shutter_track.py
uv run --with "$CADPY" python "$CAD_STEP" models/pill_click_p0_v3_c4_rear_snap.py
```

## Print-pose STL and 3MF exports

The prototype has five true printed pieces: housing, inner medicine shuttle,
top shutter, bottom shutter, and blind rear cover. The four coupon files may
contain multiple disconnected coupon halves by design.

```sh
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_housing.py --stl p0_v3_housing.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_inner_medicine_shuttle.py --stl p0_v3_inner_medicine_shuttle.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_top_shutter.py --stl p0_v3_top_shutter.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_bottom_shutter.py --stl p0_v3_bottom_shutter.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_rear_cover.py --stl p0_v3_rear_cover.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_c1r1_nominal_L6p80_lip0p80_coupon.py --stl p0_v3_c1r1_nominal_L6p80_lip0p80_coupon.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_c1r1b_nominal_L6p80_lip1p20_coupon.py --stl p0_v3_c1r1b_nominal_L6p80_lip1p20_coupon.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_c2_loose_rail_coupon.py --stl p0_v3_c2_loose_rail_coupon.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_c3_shutter_track_coupon.py --stl p0_v3_c3_shutter_track_coupon.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_c4_rear_snap_coupon.py --stl p0_v3_c4_rear_snap_coupon.stl
uv run --with "$CADPY" python "$CAD_STEP" models/print/p0_v3_test_bundle.py --3mf p0_v3_test_bundle.3mf
```

The test bundle uses a 220 x 220 mm layout with ten named groups and fifteen
solids. `C1R1` and `C1R1B` are coupon revision IDs, not product design-version
numbers. Print both strengthened nominal coupons in one batch; preserve C2 as
the original clearance-only diagnostic; then print C3, C4, and only then the
five-part P0 prototype. The former `p0_v3_c1_nominal_rail_coupon` filename is a
deprecated compatibility alias. Its checked-in STEP/STL now resolve exactly to
strengthened C1R1 geometry, and the alias identity/hashes are locked in the
manifest; use the explicit C1R1 name when recording physical results. Physical
force, fit, fatigue, snap life, and
printer/material calibration remain mandatory gates. See
`models/print/p0_v3_print_manifest.json` for hashes, dimensions, print poses,
the C1R1 artifact hashes and mesh metrics. The manifest deliberately remains
`pending_independent_review`; implementation does not self-approve. V3.1 also
retains the corrected snap root, which replaces the former
endpoint-only root with an exact R0.80 prism having 0.20 mm finite overlaps;
the C4 and rear-cover STLs now pass the strict 1e-6 coordinate-welded
valence-two manifold gate without slicer repair. Physical coupons remain the
authority for force, fit, fatigue, and snap life.

## CAD Viewer

Start or reuse the viewer and open any explicit artifact:

```sh
CAD_VIEWER=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.3.13/skills/cad/scripts/viewer
npm --prefix "$CAD_VIEWER" run serve -- --host 127.0.0.1 --dir "$(pwd)/models" --shutdown-after 12h --json
```

Link pattern:

```text
http://127.0.0.1:4178/?dir=/absolute/path/to/pill-click/models&file=print/p0_v3_test_bundle.3mf
```
