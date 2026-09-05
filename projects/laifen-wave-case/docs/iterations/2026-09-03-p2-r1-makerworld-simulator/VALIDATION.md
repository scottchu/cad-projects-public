# VAL-MW-01 independent validation history

**Current verdict: repair 1 HOLD.** Repair 1 closes the attempt-1 slider, dynamic-bound, z-fighting, and accessibility failures, but its assembled view completely occludes the full/effective thread bands. The repair-1 candidate cannot advance to formal review, private delivery, or the user intent gate until that assembled-view blocker is repaired and independently rerun. Attempt 1 remains preserved below.

## Attempt 1 — HOLD

**Owner:** `/root/mw_sim_validate`, independent validation role.  
**Attempt:** 1, exact original candidate manifest below.  
**Status:** **FAIL / HOLD for repair.** Pure math, global-Z phase, static loading, nonblank rendering, and responsive flow pass, but the exact attempt-1 candidate has three blocking UI/render defects and two material accessibility/intent-clarity findings. It must not advance to private delivery or the user intent gate until a new implementation candidate is frozen and this independent gate is rerun. This attempt-1 receipt remains historical evidence and must not be read as a result for any repaired source.

## Frozen provenance and scope

- Supplied implementation candidate manifest SHA-256: `26e5717885bfd4dcc6a473f455a405767011cca3f94a4ec1cd47ee5fda4fcb6d`.
- All five candidate entries verified before and after validation. No candidate source, dedicated candidate test, R7 CAD, route, index, service configuration, or printer/slicer state was changed.
- Supplied design baseline manifest SHA-256: `b060787132e71d20b995624e7deced8403d3c76c61507f2287170f28d0dc29b6`.
- Validator input manifest SHA-256: `09b9ffb1f73ae8457b20d906adc13974212d77417e59f1a8e1c80193cbf776f0`. It binds the candidate, BRIEF/DESIGN/implementation receipt, Python/UV dependency inputs, and the four independent validation helpers.
- Runtime: root UV workspace, Python `3.12.13`, project `cad-preview` Playwright `1.62.0`, installed Chromium, Node for the ES-module math checks, and a temporary Python loopback server at `127.0.0.1:8993`.
- Evidence is under `projects/laifen-wave-case/scratch/makerworld-simulator-validation/`; `inputs/validation-evidence.sha256` freezes this receipt and the exact evidence files.

## Findings

### V-MW-01 — P1 blocker — both range sliders ignore their own value

The millimetre slider was changed from 84 to 120 through a real `input` event. The page immediately restored it to 84 because `sync("mm")` reads `#split-mm-number`, not the range that emitted the event. The percentage slider behaved the same way: setting it to 50 read the still-visible rounded percentage number (`38.356`) and produced `S=83.99964`, then snapped back to `38.356%`. This reproduces at both `1024x900` and `390x844`.

Number fields do work: entering 50/169 mm updates seam/readouts and entering 50% gives `S=109.5`. The prominent range controls nevertheless fail MW-REQ-02 and the stated use sequence. Evidence: `ui-evidence.json` keys `afterMmRange120` and `afterPercentRange50`; responsible source is `app.js` lines 43–48.

### V-MW-02 — P1 blocker — the 9 mm overlap co-renders two near/coincident outer shells

`lowerInterval=[0,seam+P]` and `upperInterval=[seam,H]`; `build()` renders both full-radius patterned shells. Their common `[seam,seam+9]` outer surface is therefore represented twice, with different materials and near/coincident tessellation. Chromium screenshots show severe alternating cyan/orange striping in the full thread band for the default, both split boundaries, and all four patterns on desktop and phone. The striping is present even for `smooth`, so it is not the selected texture.

This is the expected visual signature of depth conflict at the overlap and makes the full/effective thread overlays difficult to read. It fails the visual target for MW-REQ-01 and MW-REQ-07. Evidence: both contact sheets and every `*-canvas.png`; responsible source is `app.js` lines 11–24 and 29–36.

### V-MW-03 — P1 blocker — percentage control bounds become invalid after H changes

The candidate exposes editable device length and preserves canonical `S` as promised, but the percent range/number keep hard-coded R7 bounds `22.83..77.17`. At device length 300, `H=311`; the bounds that map to legal `S=50..169` are approximately `16.077..54.341%`. The UI still permits 77.17%, which produces `S=239.9987` and a red out-of-range error. Thus the percentage adapter does not map its allowed input domain into the canonical S domain after an H edit. This fails MW-REQ-02. Evidence: `ui-evidence.json` keys `afterDeviceLength300` and `afterPercentOldMaxAtH311`; hard-coded bounds are in `index.html` line 11.

### V-MW-04 — P2 — the four split inputs have no accessible names

The ARIA snapshot exposes the two split sliders as unnamed `slider` nodes and their numeric adapters as unnamed `spinbutton` nodes. Each wrapping label contains two labelable controls, so the visible label is not assigned as an accessible name to either input. Pattern/display/device-length controls are named. This fails the planned semantic DOM/accessibility check for the primary interaction. Evidence: `aria-snapshot.txt`.

### V-MW-05 — P2 — the visual gate weakens top-datum and pattern recognition

The model is side-wall-only geometry and fills almost the entire canvas. Pixel evidence places colored geometry at desktop y=0..584 of 586 and phone y=1..489 of 491, so closed-end datums are not visibly distinguished from the canvas crop. At the 50 mm boundary the short orange region reads visually like a top cap even though text calls it the upper piece. The default does read as a mid split and the 169 mm boundary remains two pieces, but the lower allowed boundary does not reliably preserve the intended “mid split, not a small top cap” reading.

The current blunt-diamond render also appears as diagonal moire/ridges rather than blunt diamond cells. The mesh samples 33 circumferential repeats with only 96 radial segments (~2.9 samples/repeat), and about 4.8 mm axial pitch with ~2 mm ring spacing (~2.4 samples/repeat), which is insufficient to resolve the field shape. The four select values execute and their canvases differ, but MW-REQ-06 is not visually demonstrated for the current diamond. Evidence: desktop/phone contact sheets, `image-analysis.json`, and `app.js` lines 11–22.

## Passing evidence

- Candidate's Node test exits 0: `makerworld simulator math and semantic-source checks passed`.
- Independent math exits 0. Defaults exactly reproduce `C=213`, `H=219`, `S=84`, `U=81`, `B=137`, `P=9`, seam `135`, lower/upper outer `144/84`, full band `135..144`, and effective band `136.5..142.5`.
- Twenty length/split cases pass closure, seam, band-width, and exact percent-to-mm round trips. Boundary/warning/error cases behave as designed.
- `smooth`, `blunt-diamond`, `shallow-helix`, and `wave-flutes` stay within their declared relief bounds. Sixty seam/overlap probes and a dense field grid prove the mathematical field uses the same assembled global Z regardless of split.
- Exact static HTML returns HTTP 200 and the served body hash equals candidate `index.html` SHA-256 `aeaaf2d11e143fde7e505a2710840195e3b9650cdb8078de0055b42a398fd489`.
- Pinned Three.js `0.160.1` and matching OrbitControls load at both viewports. Each run has one nonblank canvas, both upper/lower colors, updated numeric readouts from the working number adapters, and no console/page errors.
- Responsive document width equals viewport width (`1024/1024`, `390/390`), with no horizontal overflow or panel overlap. Phone panels stack viewer, controls, then readouts with 16 px separation. Exploded display leaves all numeric state unchanged.
- Warnings and non-CAD/non-printability language are visible as text. The default legend and readouts identify upper/lower pieces, seam, full/effective bands, both global-Z datums, pitch, engagement, gaps, and wall/thread assumptions.

## Requirement disposition

| Requirement | Result | Evidence |
| --- | --- | --- |
| MW-REQ-01 two mid-split pieces | **HOLD** | Default labels/colors and boundary movement render, but overlap depth conflict obscures the joint and S=50 risks a top-cap reading. |
| MW-REQ-02 canonical mm / percent adapter | **FAIL** | Pure math/number adapters pass; both sliders fail and percent bounds go stale when H changes. |
| MW-REQ-03 top/global-Z datum | **PARTIAL** | Text and math pass; closed ends are not visually distinguished in the canvas. |
| MW-REQ-04 R7 defaults | **PASS** | Independent default tuple and UI readouts match. |
| MW-REQ-05 global-Z phase | **PASS (math)** | Dense grid and 60 seam/overlap probes pass; visual overlap is independently blocked by V-MW-02. |
| MW-REQ-06 four patterns | **HOLD** | All options execute and bounded laws pass; blunt diamond is under-resolved visually. |
| MW-REQ-07 thread/readouts/warnings | **HOLD** | Text coverage passes; overlap conflict obscures band legibility. |
| MW-REQ-08 private static route | **DEFERRED** | Only exact temporary loopback HTTP was in validator scope; delivery must wait for repaired candidate and formal review. |

## Commands and method note

Final executions, all from the repository root:

```sh
node projects/laifen-wave-case/tests/test_makerworld_simulator.mjs
node projects/laifen-wave-case/scratch/makerworld-simulator-validation/validate_math.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/makerworld-simulator-validation/validate_ui.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/makerworld-simulator-validation/capture_aria.py
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/makerworld-simulator-validation/analyze_images.py
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r1-makerworld-simulator/inputs/validation-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r1-makerworld-simulator/inputs/implementation-candidate.sha256
```

All final commands exited 0. One validator-method repair occurred before evidence collection: Playwright `fill()` rejected a decimal range value as malformed, so the helper changed only its range-driving method to set the actual range DOM value and dispatch the same bubbling `input` event a user gesture emits. No candidate code or acceptance threshold changed.

## Next action and acceptance boundary

Return to IMP-MW-01 for a new candidate that reads the emitting range control, derives percent control bounds from current H, gives each input its own accessible label, and renders the thread overlap without co-planar competing shells. The visual sampling/framing should also make the blunt diamonds and closed top datum recognizable and keep the lower split boundary from reading as a tiny cap. Freeze a new implementation manifest, then rerun VAL-MW-01 and CRIT-MW-01 before formal review or static delivery.

This receipt validates only a visual intent simulator. It provides no CAD, STEP, slicer, printability, fit, thread-strength, retention, or physical acceptance.

## Repair 1 — HOLD

### Frozen provenance

- Exact repair-1 implementation-candidate manifest SHA-256: `3951e89f0fefe28f86e5d5eb470610c11cb54c6a39439fa96c33e29f1d712daa`; all five entries verified before and after the final rerun.
- Repair-1 validator input manifest SHA-256: `538dab725281749f2ef4eccf6d1ad8fdc586ebbac73b9690c346bbf93c077038`. It binds the current candidate, BRIEF/DESIGN/implementation receipt, attempt-1 evidence manifest, runtime dependency files, and repair-1 helpers.
- Repair-1 raw evidence is isolated under `scratch/makerworld-simulator-validation/repair1/`. Attempt-1 scratch evidence and `inputs/validation-{inputs,evidence}.sha256` were not overwritten.
- Runtime remained root UV Python `3.12.13`, Playwright `1.62.0`, installed Chromium, Node, and temporary loopback HTTP at `127.0.0.1:8994`.

### Repair disposition

| Attempt-1 finding | Repair-1 result | Evidence |
| --- | --- | --- |
| V-MW-01 sliders ignored their own values | **CLOSED** | On both viewports, mm slider 120 yields range/number/readout 120 and seam Z99; percent slider 50 yields S109.5 and 50.000%. |
| V-MW-02 competing outer shells/z-fighting | **CLOSED, with regression below** | Upper/lower exterior meshes now meet only at the seam. All assembled screenshots are free of the cyan/orange depth-conflict striping. |
| V-MW-03 stale percent bounds after H edit | **CLOSED** | At H311 both percent controls derive `16.077170418..54.340836013`; driving the slider to its exact maximum yields S168.9999999999999, no red error. |
| V-MW-04 unnamed primary inputs | **CLOSED** | Desktop and phone ARIA snapshots name both sliders and both exact numeric adapters and expose the live axial/pattern/display summary. |
| V-MW-05 top datum/pattern clarity | **PARTIAL / user gate remains** | Patterns are distinct and the diamond law passes, but the diamond still reads as a coarse herringbone field; S50 still presents a visually short upper piece and neither closed end is given a distinct rendered face. |

### R1-MW-01 — P1 blocker — assembled view hides both thread-band overlays

Repair 1 moves the full/effective bands to radii 19.05 and 18.82 while the opaque upper exterior spans from the seam to H at radius 19.5 plus relief. In assembled mode the upper exterior therefore depth-occludes the entire nominal thread interval `seam..seam+9`. Desktop and phone screenshots show only the thin yellow seam; neither the purple full band nor white effective band is visible even though the legend promises both.

Pixel classification corroborates the visual review: every assembled image has zero white-band pixels and only 26–42 purple-like antialias/background pixels. The same bands become clearly visible in exploded mode with 3,042 white/1,188 purple pixels on desktop and 2,125 white/840 purple pixels on phone. This fails the DESIGN visual gate and MW-REQ-07 in the primary assembled view. Responsible source: repair-1 `app.js` lines 24 and 35–39.

The exploded overlay behavior itself passes. The upper piece and seam move +7; the lower piece and both bands move −7; numeric readouts remain identical and the live summary changes only display mode. The gap clearly shows full and effective bands without z-fighting.

### Essential regression results

- Candidate Node test exits 0.
- Independent math exits 0: exact default tuple/closure/thread bands, S50/S84/S169 boundaries, five H-domain percent-bound and round-trip groups, four declared relief ranges, and 510,996 global-Z split-independence comparisons pass.
- Static candidate returns HTTP 200 and the served index is byte-identical to the candidate index.
- Desktop `1024x900` and phone `390x844` load pinned Three.js, render one nonblank canvas with both piece colors, and report no console/page errors or horizontal overflow.
- Slider, number, percent, device-length, boundary, pattern, and display controls were exercised through browser events. Default/min/max and all four assembled patterns plus default exploded mode were captured at both viewports.
- Semantic regions, warnings, non-CAD language, global-Z readouts, pitch/engagement text, and the pass/fail intent question remain present.

One validator-method repair occurred before evidence collection: the first helper relied on nonstandard element-ID globals (`splitMm`) and stopped at its initial page-state read. The corrected helper uses explicit `document.querySelector()` calls only. `validate_repair1.method0.py` and the first traceback are retained; no candidate code, browser state, or acceptance threshold changed.

### Repair-1 requirement disposition and next action

| Requirement | Current result |
| --- | --- |
| MW-REQ-01 | **PASS for default topology and z-fighting removal; user topology confirmation remains external.** |
| MW-REQ-02 | **PASS.** Both adapters and dynamic domains work at desktop and phone sizes. |
| MW-REQ-03 | **PARTIAL.** Text/math pass; the closed-end visual treatment remains weak. |
| MW-REQ-04 | **PASS.** |
| MW-REQ-05 | **PASS (math/render phase contract).** |
| MW-REQ-06 | **PASS for controls/laws/distinct renders; visual taste remains for the user.** |
| MW-REQ-07 | **FAIL.** Assembled full/effective bands are not visible. |
| MW-REQ-08 | **DEFERRED.** No private route work is allowed while repair 1 is on HOLD. |

The smallest next correction must keep the repaired non-overlapping exterior shells while making the full and effective band positions readable in the assembled view without introducing a competing co-planar outer shell. Freeze a new candidate and rerun the assembled/exploded band, slider, accessibility, and essential math/global-Z gates. CDN availability and the user's actual desktop/phone rendering remain external risks even after a deterministic PASS.
