# P20 Blue-Orange web coupon independent critique

Date: `2026-08-27`

Task: `P20-WEB-CRITIC-01`

Status: **CONDITIONAL PASS TO SLICING; NOT A PRINT, PHYSICAL, OR PRODUCT
ACCEPTANCE**

The exact coupon may advance to slicing. No finding blocks slicing this
fingerprint. Print start should wait for a layer-level toolpath check at the
named witness and an unambiguous external witness locator. This verdict does
not approve the full simulator profile, P20 mechanism, or any product web
below the ordinary `2.20 mm` rule.

## Frozen candidate verified

- Candidate fingerprint:
  `07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be`.
- The fingerprint string agrees between `IMPLEMENTATION.md` and the exact
  provenance JSON.
- All nine implementation-listed source, test, generator, STEP, 3MF, STL,
  and provenance SHA-256 values were independently recomputed and matched.
- The focused suite independently passed `6/6` on the frozen files.
- The three exact `1600 x 1200` snapshots were visually inspected. They show
  one rectangular coupon, two distinct complete through-slots, a continuous
  narrow ligament, and no visible third cut or fused opening. These are
  source-coordinate review views, not evidence of slicer toolpaths.

## DfAM evidence on the exact print-oriented STL

Target process assumptions are FDM/FFF, PETG, `0.4 mm` nozzle. The comparison
source is the installed DfAM `references/process-limits.md`, FDM/FFF column:
`1.2 mm` minimum supported wall, `1.6 mm` minimum unsupported wall, `45 deg`
self-supporting angle, `0.8 mm` minimum positive feature, and `10 mm` maximum
unsupported bridge.

`dfam_tool.py measure ...stl --angle-limit 45` measured:

- ✅ **PASS — slicing topology:** `mesh.watertight=true`, `body_count=1`,
  `volume_mm3=2009.7`, and millimetre scale was not suspect. This removes the
  universal watertightness blocker.
- ✅ **PASS — selected flat orientation:** bounding box is
  `29.03 x 28.09 x 3.20 mm`; `overhangs.down_facing_area_below_limit_mm2=0.0`
  and estimated support volume is `0.0 mm3` at the cited `45 deg` threshold.
  The broad-face-down orientation is appropriate for this extrusion/handling
  coupon and does not require supports.
- ❓ **NEED MORE INFO — sampled wall thickness:** the tool returned
  `wall_thickness.error = ModuleNotFoundError: No module named 'rtree'` in the
  repository environment, so neither `min_mm` nor `p05_mm` exists for a
  standards-style wall verdict. The independently measured BREP cutter
  distance is `1.715042423717553 mm` through the full `3.20 mm` thickness,
  which is nominally `0.515 mm` above the cited `1.2 mm` supported-wall limit,
  but this supporting fact is not substituted for the missing sampler result.
- ❓ **NEED MORE INFO — bead realization and unmeasured feature rules:** the
  DfAM tool does not measure minimum positive feature or bridge length. The
  `0.8 mm` and `10 mm` table rows therefore receive no fabricated PASS. The
  slicer must supply the relevant next evidence by showing continuous lines,
  not a void or accidental bridge, at the witness.

The print-oriented 3MF could not be measured by `dfam_tool.py` because its
loader lacked `networkx`. A separate read-only lib3mf recheck found one
millimetre-unit build item and one mesh with `IsValid=true`,
`IsManifoldAndOriented=true`, `8876` vertices, and `17756` triangles. The STL
is therefore the exact geometry used for the DfAM facts above; 3MF packaging
validity is recorded separately and is not called a DfAM measurement.

## Findings

### MAJOR — the physical witness is not visibly marked

The contract's physical question says “at the marked minimum-web witness,”
but the artifact intentionally contains no engraved mark and the current
snapshots contain no overlay locating it. Provenance names the source witness
midpoint as `YZ=(7.963860139702033, 0.9389413002297666)`; after the frozen
print transform its midpoint is approximately build
`XY=(-0.938941, 7.963860) mm`, at mid-thickness `Z=1.60 mm`.

This does not require or justify changing the CAD. Before print observation,
create an external annotated slicer screenshot or photo guide using that
coordinate and require top, bottom, and oblique close-up photos. Otherwise a
human can inspect the wrong part of the curved gap and still report “PASS.”
This finding does **not** block slicing, but it blocks an unambiguous physical
verdict until the locator exists.

### MAJOR — slicer quantization is the actual unresolved manufacturing gate

The `1.715 mm` ligament is only about `4.29` nominal nozzle diameters across;
actual extrusion width, perimeter strategy, gap fill, first-layer expansion,
and line placement can change how many continuous beads realize it. The brief
correctly leaves these settings open, so CAD/DfAM cannot infer the outcome.

Before upload or print start, inspect the exact sliced G-code at first layer,
one representative middle layer, and top layer around build
`XY=(-0.939, 7.964) mm`. Require continuous material from both adjacent fields
through the witness, both slots still open, support disabled, and no slicer
warning or omitted region. Record layer height, line width/wall strategy,
infill, first-layer settings, cooling, speed, and PETG temperatures. This is a
release condition for the G-code, not a request to alter the coupon geometry.

### MODERATE — the coupon tests extrusion and gentle handling, not plate strength

The rectangular crop preserves both complete cutter curves, the actual gap,
the `3.20 mm` thickness, and `2.20 mm` outer boundary webs, so it is a sound
minimal test for slot openness and whether the ligament survives ordinary
bed removal/finger handling. Its rectangular boundary and omission of the
circular rim, Green/other rails, fixed axle, neighboring stress raisers,
assembly loads, cyclic twist, heat, and creep can make its stiffness and load
path differ materially from the final plate.

No redesign is needed for the stated coupon question. A physical PASS must
remain scoped exactly as written in `BRIEF.md`; it cannot establish product
strength, motion, fatigue, or acceptance of the `1.72 mm` web in the complete
plate.

### LOW — visual evidence identifies continuity but not the exact minimum

Front, opposed-face, and oblique snapshots visibly show two open through-slots
and continuous material. Because the witness overlay is absent and both broad
face views are labelled `ISO`, they are inadequate for a feature-specific
claim about the exact `1.715042 mm` location. Numeric BREP evidence supplies
that geometry fact; the external locator above supplies the human-review
bridge.

## Exact commands and results

```text
shasum -a 256 <nine candidate files>
# all nine values match IMPLEMENTATION.md

uv run pytest -q projects/xt60-bend-jig/tests/test_p20_blue_orange_web_coupon.py
...... [100%]
# 6 passed

uv run python .../dfam-check/scripts/dfam_tool.py measure \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.stl \
  --angle-limit 45
# watertight=true; body_count=1; support area=0; support volume=0;
# wall sampler unavailable because rtree is missing

uv run python .../dfam-check/scripts/dfam_tool.py measure \
  projects/xt60-bend-jig/cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.3mf \
  --angle-limit 45
# loader unavailable because networkx is missing

uv run python -c '<lib3mf read-only validity check>'
# one build item; one valid manifold-and-oriented mesh; 8876 vertices;
# 17756 triangles
```

## Critic disposition

**Advance this exact coupon to slicing.** No geometry change is recommended.
The slicer role must resolve the toolpath-continuity gate, and the handoff must
add a non-geometric witness locator before a physical PASS/FAIL is recorded.
Any candidate geometry or artifact change invalidates this critique's frozen
fingerprint.
