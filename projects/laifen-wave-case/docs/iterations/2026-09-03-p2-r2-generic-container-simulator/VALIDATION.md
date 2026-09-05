# VAL-GCS-01 independent validation history

**Current status:** **REPAIR 1 FAIL / HOLD.** Repair 1 closes strict numeric-domain rejection and replaces the incorrectly oriented marker hoops, but the actual desktop and phone page still hides the Laifen upper piece, clips wide custom geometry, exposes false derived dimensions and an active magnifier in invalid states, and provides no visible chamfer/drain change or field-level error association. It must not advance to formal review or delivery.

## Attempt 1 — HOLD

**Owner:** `/root/mw_sim_validate`, independent validation role.  
**Status:** **FAIL / HOLD for repair.** Preset arithmetic, canonical split conversion, dynamic bounds, thread-turn scaling, global-Z phase, two-shell source intervals, accessible control names, true-scale detail disclosure and responsive document flow pass. The exact candidate has three blocking contract/render failures: incomplete numeric-domain rejection, incorrectly oriented seam/thread markers, and a fixed camera which hides or clips required pieces for supported dimensions. It must not advance to formal review or delivery.

## Frozen provenance and scope

- Verified design baseline fingerprint: `aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df`.
- Verified implementation-candidate manifest-file SHA-256: `4acefaf383cd7b0e0425f5da23e5ca19612920ede43df469db3f1ac16cbf228d`; all five entries passed before and after final execution.
- Validator input manifest SHA-256: `7504f77d7ec67356c8a9b1296f9e54156ed5a73978681fa327c5dfd0e11bd392`. It binds BRIEF/DESIGN/implementation receipt, candidate source/test, root UV inputs and validator helpers.
- Runtime: root UV Python `3.12.13`, project Playwright `1.62.0`, installed Chromium, Node, and temporary loopback HTTP `127.0.0.1:8995`.
- Candidate source/tests/routes/services/CAD/slicer/printer state were read-only. Validator writes are limited to this receipt, `inputs/validation-*.sha256`, and `scratch/generic-container-validation/`.

## Findings

### GCS-V01 — P1 blocker — required numeric domains are accepted as valid

Independent pure-model checks found 15 prohibited inputs which return `valid=true` with no error: negative floor, thread pitch, lead/runout, keepout, axial pitch, arc pitch, pattern depth, chamfer, clearance, bore and drain count; fractional drain count; `thread_turns=4`; infinite OD; and NaN depth. These violate the schema constraints and GCS-05/GCS-09 warning contract. Some produce reversed thread bands, invalid counts or non-finite render coordinates while the live state says valid.

The candidate does reject infeasible height with the exact formula, S outside a feasible dynamic range, OD at/below twice wall, bore above OD, and pattern depth above a wall readout. Negative wall is rejected only indirectly as “bore exceeds OD” after the auto-bore calculation, not as a named negative-input failure. Evidence: `math-evidence.json`; responsible implementation is the compact validation logic in `math.js` line 9.

### GCS-V02 — P1 blocker — axial markers render as large vertical hoops

`ring()` creates `THREE.TorusGeometry` but never rotates the torus from its default XY plane into the container's XZ section. Each supposed axial-plane tick is therefore a large vertical hoop centered at its Z/Y value. The jar and custom screenshots show purple/yellow arches rising above and passing through the vessel rather than two labelled axial ticks plus a bracket. Exploded mode adds more overlapping arches. This fails GCS-06 and GCS-09's assembled/exploded marker contract and makes the wide-short form resemble an open bowl.

No third thread-tube mesh exists, and the two shell intervals meet at one seam mathematically. The failure is the actual marker orientation/presentation. Evidence: every jar/custom screenshot and contact sheet; responsible implementation is `app.js` lines 5–6.

### GCS-V03 — P1 blocker — fixed framing does not support the declared generic dimension range

The camera and target are fixed at `(150,130,160)` and global Y60. No preset or H/OD edit refits them. At both desktop and 390/412 phone sizes, the Laifen H219 preset shows only the teal lower exterior; the orange upper piece, seam and thread markers are entirely outside the canvas. Pixel evidence records zero orange/yellow/purple pixels for all three Laifen assembled captures. Exploded Laifen is similarly incomplete.

The OD120/H88 custom form clips across both horizontal canvas edges, while the H55/OD80 jar is framed near the bottom and its visible shell ratio is roughly square rather than clearly 80:55 wide-short. This fails GCS-01, GCS-06 and the true-geometry intent gate. Evidence: `image-analysis.json`, desktop/phone contact sheets, and preset viewport screenshots; fixed camera source is `app.js` line 10.

### GCS-V04 — P2 — rendered pieces do not show closed ends, chamfer or drain indicators

`shell()` builds only the lateral surface; it has no closed-end face. The supported jar consequently reads as an open bowl from the camera angle, conflicting with the brief's two closed-end pieces and the global closed-end datums. Chamfer and drain controls update text, but neither is consumed by `shell()` or another scene object, so changing them has no visual effect despite the design describing an end-treatment reference and visual open-hole indicator. Evidence: `app.js` lines 4 and 6–9 plus jar/custom screenshots.

### GCS-V05 — P2 — live errors are not related to the responsible controls

All controls have accessible names, the status uses `role=status`/`aria-live`, and the detail canvas receives an honest dynamic accessible label. However, inputs have no `aria-describedby`, `aria-errormessage`, or invalid state linking the shared message to the field which caused it. This falls short of the DESIGN requirement for error/help relationships and makes multi-field infeasibility harder to diagnose with assistive technology. The readout also says “1 turns”; this is minor copy quality.

## Passing evidence

- Both required presets derive valid inputs: Laifen `E=6`, `P=9`, `K=2.4`, bounds `14.4..204.6`, bores `30/31`; jar `E=3`, `P=7.5`, `K=4`, bounds `14.5..40.5`, auto bore `74`.
- Browser controls for 1/2/3 turns give `E=2/4/6`, `P=5/7/9` at pitch2 and recompute bounds. Pitch3.5 with three turns gives `E=10.5`, `P=15.75`, bounds `21.15..98.85`.
- H261 and H311 percent endpoints convert exactly to current raw-mm S bounds and remain valid. S is preserved across H edits until the user changes percent.
- Null bores resolve to `OD-2*wall`; positive lower/upper overrides update independent wall readouts.
- The H20 jar becomes infeasible, clears the false assembled split and states `Required H >= 2*(F+P+K) = 29.00 mm; received H = 20 mm.`
- Four pattern laws stay in `0..depth`, derive physical circumference count/actual arc pitch at four diameters, and pass 349,932 fixed-global-Z split/explosion independence comparisons.
- Full-model relief remains at requested depth. At depth0.20 the detail view and accessible label explicitly say `4× radial display`, requested relief `0.2 mm`, and full model true scale. Detail screenshots clearly distinguish smooth, blunt diamond, helix and wave/flutes at all three viewports.
- Exactly two exterior shell calls use `[0,z0]` and `[z0,H]`; no exterior overlap or thread-tube mesh is present in source.
- Desktop `1024x900`, phone `390x844`, and phone `412x915` return HTTP 200, load the pinned Three.js module, render nonblank canvases, have no console/page errors, horizontal overflow or panel overlap, and expose named semantic controls/readouts/status.
- Served `index.html` SHA-256 `912218aadad88a29c00bfbb70bf976b30946689ead539d808daee9956c779267` exactly equals the frozen candidate index.

## Requirement disposition

| Requirement | Result |
| --- | --- |
| GCS-01 generic presets | **FAIL visual / PASS math.** Laifen is not fully visible and jar geometry is misleading. |
| GCS-02 canonical S adapter | **PASS.** |
| GCS-03 global closed-end frame | **PARTIAL.** Math/text pass; rendered closed ends are absent. |
| GCS-04 1/2/3 turns | **PASS.** |
| GCS-05 dynamic bounds/infeasibility | **FAIL domain / PASS formula.** Dynamic S math works, but many prohibited parameters remain accepted. |
| GCS-06 two exteriors/no tube/markers | **FAIL visual / PASS shell intervals.** Marker orientation and camera hide the intended relationship. |
| GCS-07 patterns/global Z/count | **PASS.** |
| GCS-08 true scale/magnifier | **PASS.** |
| GCS-09 text/accessibility/markers | **FAIL.** Text and names pass; marker geometry and field-level error relationships do not. |
| GCS-10 route isolation | **DEFERRED.** No route work is allowed while deterministic validation is on HOLD. |

## Commands, method repairs and next action

Final checks from repository root:

```sh
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
node projects/laifen-wave-case/scratch/generic-container-validation/validate_math.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/validate_ui.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/analyze_images.py
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/validation-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/implementation-candidate.sha256
```

Candidate test and browser execution exit 0; the independent math runner exits 0 as an evidence collector and records the 15 failed rejection assertions explicitly. Two method-only helper repairs were used: one corrected a validator JavaScript-expression closing token before state collection, and one added per-pattern detail-canvas captures. `validate_ui.method0.py` and `validate_ui.method1.py` preserve both earlier helper states. No candidate or acceptance threshold changed.

Return to implementation for the smallest repair which validates every schema type/domain before derivation/render, rotates or replaces the axial marker geometry, and refits the camera to current H/OD in assembled and exploded states. The next candidate should also render unambiguous closed ends and the promised chamfer/drain indicators, and relate invalid controls to their messages. Freeze a new manifest and rerun the failed deterministic/browser gates before critique/review/delivery.

CDN availability and comprehension on the user's actual desktop/phone remain external risks. This simulator supplies no CAD, thread-solid, mesh, slicer, printability, fit, drainage, strength or physical acceptance.

## Repair 1 — FAIL / HOLD

### Frozen provenance and scope

- Verified design baseline fingerprint: `aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df`.
- Verified repair-1 implementation-candidate manifest-file SHA-256: `8e3d7cd62d4c46c80a0d11865bc8fc39a36e1f943920e3051e130f948ec29e81`; all five declared entries passed before and after the rerun.
- Repair-1 validator input manifest SHA-256: `d9921c293a2a44751d4af53fbdf87843d11234c51c87be1db1c24fc9bf8cebf7`. It binds the exact repair-1 candidate, design/implementation records, root UV inputs, attempt-1 evidence manifest, and preserved repair-1 validator helpers.
- Runtime: root UV Python `3.12.13`, project Playwright `1.62.0`, installed Chromium, Node, and temporary loopback HTTP `127.0.0.1:8996`.
- Candidate source, candidate tests, CAD, routes, indexes and services remained read-only. Repair-1 writes are limited to this receipt, `inputs/validation-repair1-*.sha256`, and `scratch/generic-container-validation/repair1/`.

### Repair dispositions

#### Closed — strict numeric/type domains

Independent math now rejects all 21 exercised bad inputs, including non-finite dimensions, non-positive floor/pitch/lead/runout/keepout/pattern pitches, negative depth/chamfer/clearance, invalid bore overrides, non-integer/negative drain counts, invalid turn and pattern enums, and non-boolean flags. The runner completed 280,571 assertions with zero failures. Exact preset arithmetic, dynamic S bounds, percent endpoints, round trips, null/override bores, 1/2/3 turns, infeasibility and 280,524 global-Z phase comparisons also pass.

#### Closed in orientation, still weak in presentation — axial marker bracket

The large vertical torus hoops are gone. The actual scene now uses a vertical purple bracket with horizontal end ticks at the thread-band interval. It no longer intersects the whole vessel like a tube. In the jar screenshots it remains very small and sits at the right edge: the detected purple region is only 61–77 pixels on desktop and 40–57 pixels on phones. The wide custom desktop capture has no detected purple pixels and the vessel itself reaches both canvas edges. The marker relationship is therefore directionally corrected but not reliably legible across supported geometry.

#### Partially closed — closed-end indication

The jar and wide-custom assembled screenshots now show an orange outer-end disc at global `z=H`. In exploded jar views the lower piece also exposes a teal oval from the lower outer-end disc through the open interface. Because the camera crops the Laifen preset and the bottom of the jar/wide views, both global closed ends cannot be reviewed together. The exploded lower-piece oval can also be mistaken for a cap at the split interface, the exact semantic the user rejected. Closed-end geometry is present, but the delivered view does not communicate the two mid-split pieces unambiguously.

### Remaining findings

#### GCS-R1-V01 — P1 blocker — fixed camera still hides and clips supported geometry

The actual Laifen preset at desktop `1024x900`, phone `390x844`, and phone `412x915` shows only the teal lower exterior in both assembled and exploded modes. Every one of those six captures has zero orange, yellow and purple pixels. The desktop assembled teal box is `[61,1,235,532]`; phone boxes start at y=1 as well, confirming the upper assembly lies beyond the canvas rather than merely blending into the background.

The H88/OD120 custom case reaches both horizontal edges and the bottom of the canvas: colored bounds are `[0,133,295,560]` of 296×561 on desktop, `[0,93,335,390]` of 336×391 at 390px, and `[0,93,357,390]` of 358×391 at 412px. The required geometry and marker interval are clipped. This fails GCS-01/GCS-06 and the requested camera auto-fit gate.

#### GCS-R1-V02 — P1 blocker — invalid states retain false derived dimensions and active detail

Both strict-domain and infeasible inputs correctly clear the full-model canvas and expose an error in the live status. However, they do not suppress the derived readout, live derived announcement, or detail magnifier.

For the infeasible jar H20 case, the status correctly states `Required H >= 2*(F+P+K) = 29.00 mm; received H = 20 mm.`, while the live announcement still claims split 27.5 mm with upper span `-7.5 to 20`, the readout reports `137.50000%`, negative thread intervals, and reversed split range `14.50–5.50 mm`; the 1× detail magnifier remains active. With floor `-1`, the error is correct but valid-looking split/thread/readout values and the detail magnifier likewise remain. This is materially misleading state, not merely stale copy, and fails the invalid/infeasible suppression gate.

#### GCS-R1-V03 — P2 — chamfer and drains remain text-only controls

Changing the wide-short jar from chamfer 1 mm/drains off to chamfer 5 mm/drains on/count 5 changes its readout but not the rendered vessel. Desktop A/B canvas files are pixel-identical. On both phone sizes, the only pixel difference is the one-pixel canvas top border; all model pixels, color counts and bounds are identical. No chamfer reference or drain-hole indicator is visible. This fails the promised end-treatment/drain visualization and prevents the user from validating those relationships.

#### GCS-R1-V04 — P2 — field-level error relationships remain absent

Accessible names and a live status region are present, but every tested control still has null `aria-invalid`, `aria-describedby`, and `aria-errormessage`, including floor while it holds `-1`. The shared error is not programmatically related to its responsible field. On 390/412px layouts the three panels stack without horizontal overflow or overlap, and the controls remain grouped under the named parameters form, so responsive grouping otherwise passes.

### Essential passing evidence

- Candidate test exits 0. Independent math records `total=280571`, `phase=280524`, `failures=0`; all four pattern ranges remain bounded (`smooth 0..0`, others `0..0.45`).
- Both required presets and the custom case update the visible status/readout. Canonical raw-mm S, H-dependent bounds, percent endpoints, bore null/override behavior, turn/pitch scaling and fixed-global-Z pattern behavior remain correct.
- Invalid and infeasible inputs clear the full-model canvas at all three viewports. Valid canvases are nonblank; the pinned Three.js dependency loads; no console or page errors occur.
- The depth0.20 magnifier states `4× radial display`, requested relief `0.2 mm`, and full model true scale. The four detail patterns remain visually distinguishable.
- Source/equation evidence still establishes two exterior shell intervals `[0,z0]` and `[z0,H]` with no overlapping exterior shell or third thread-tube mesh. This does not override the camera and closed-end presentation failures above.
- Desktop and phone document widths equal viewport widths. Desktop panels are disjoint columns; phone panels are disjoint stacked blocks with no horizontal clipping.
- Served `index.html` matches the exact repair-1 candidate entry.

### Repair-1 requirement disposition

| Requirement | Repair-1 result |
| --- | --- |
| GCS-01 generic presets | **FAIL visual / PASS math.** Fixed framing hides the Laifen upper piece and clips wide custom geometry. |
| GCS-02 canonical S adapter | **PASS.** |
| GCS-03 global closed-end frame | **PARTIAL.** Discs exist, but both datums are not reviewable and exploded presentation can read as a split cap. |
| GCS-04 1/2/3 turns | **PASS.** |
| GCS-05 dynamic bounds/infeasibility | **FAIL UI / PASS math.** Strict rejection is fixed; invalid derived/detail output remains. |
| GCS-06 two exteriors/no tube/markers | **FAIL visual / PASS intervals.** Bracket orientation is fixed, but framing/legibility is not. |
| GCS-07 patterns/global Z/count | **PASS.** |
| GCS-08 true scale/magnifier | **PASS valid states; FAIL invalid-state suppression.** |
| GCS-09 text/accessibility/markers | **FAIL.** Live invalid details, missing field relationships, and marginal marker legibility remain. |
| GCS-10 route isolation | **DEFERRED.** Candidate remains on HOLD. |

### Commands, method history and next action

Repair-1 checks from the repository root:

```sh
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
node projects/laifen-wave-case/scratch/generic-container-validation/repair1/validate_math.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/repair1/validate_ui.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/generic-container-validation/repair1/analyze_images.py
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/validation-repair1-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/implementation-candidate.sha256
```

One method-only repair was used after the first UI helper stopped before screenshots on a `PosixPath + str` path-construction error. `validate_ui.method0.py` preserves that state; the current helper changes only evidence capture. No candidate, acceptance threshold or test was changed.

Repair the camera around the current assembled/exploded object bounds; suppress all derived/detail output when invalid; make both outer closed ends and the split interface visually unambiguous; render a visible chamfer/drain reference; and relate the responsible control to its error. Freeze another candidate before rerunning these exact failed gates.

CDN availability and comprehension on the user's actual desktop/phone remain external risks. This simulator supplies no CAD, thread-solid, mesh, slicer, printability, fit, drainage, strength or physical acceptance.
