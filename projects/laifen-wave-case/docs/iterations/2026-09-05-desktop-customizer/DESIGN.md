# CC-DES-01 — implementable option 2

## Selection and limits

Use the selected light, quiet two-pane workspace: expansive canvas left,
approximately 360–400 px settings right; four vertically consistent label/input/
unit rows; local panel scrolling only if options need it; persistent action
footer. Browser title: **Cylindrical Container Customizer**. View controls sit
on canvas. No development subtitle or page header. On narrow screens keep the
viewer and actions reachable without horizontal overflow.

Option 2's short lid and idealized cut material are illustrations, not approved
mechanics. Preserve the actual tall screw cap. Use real compiled STL clipping
with double-sided materials; label Cutaway as a viewing mode. A clipped mesh
need not have artificial section caps. Do not fake threads, fill a cavity with
an invented solid, alter STL bytes, or promise exact raster fidelity.

## Numeric adapter

New pure adapter wraps immutable `schema.mjs`; start from BROWSER_PRESET and
change only the mappings below. Hidden legacy source knobs stay internal.

| Input | Default | Mapping and plain explanation |
|---|---:|---|
| Inside diameter D | 30 | `body_bore=D; cap_bore=D+1`. Width inside body; lid is 1 mm wider. |
| Inside height H | 213 | `device_length=H-5`, retain `axial_allowance=5`. Floor to underside of fully closed lid. |
| Wall thickness W | 4.5 | `outer_diameter=D+2W`. Body sides; lid sides are 0.5 mm thinner for clearance. This is not `minimum_wall`. |
| Top & bottom thickness T | 3 | `floor_thickness=T`. Both closed ends, excluding drain holes. |

Default adapter snapshot must exactly equal BROWSER_PRESET (all keys), not
merely produce similar dimensions. Retain smooth, minimum_wall 2.4, thread
pitch 2, turns 3, clearance .25, depth .5, root wall 1.4, chamfer 1.2 and all
inactive values. Cap-side/thread-wall differences are visible helper text,
not a claim of uniform wall thickness everywhere.

Directly beneath the four dimension inputs, always show **Drain holes** as a
labeled Off/Top/Bottom selector. Map these to none/top/bottom; default Bottom
preserves the preset. Keep 3 mm holes; set internal ring radius `min(9,D/2-2)`
to retain baseline 9 and avoid small-diameter failures even when source asserts
drainage bounds with holes off. No unsupported Both option.

Container options (collapsed):

- **Lid height**: default **Auto**, outer top-to-seam distance
  `L=(H+2T)*(84/219)`. Default exact 84 mm. H=60,T=3 gives approximately
  25.315 mm without user calculation. An explicit numeric override disables
  Auto; an Auto action restores proportional sizing. Set source distance
  mode and distance L; retain inactive percentage value 38.356. No rounding
  before compilation. This preserves a substantial cap, not a shallow lid.
- **Export shape**: Closed container/Body/Lid/Print layout → existing
  assembled/body/cap/print_layout. Changing this requires Generate and clearly
  changes the selected downloadable geometry; never present assembled STL as
  a proven slicer-ready print layout. Keep Diamond unavailable.

Validate raw input strings before Number conversion: blank, nonfinite and
out-of-range input is invalid, never zero/default. D in [10,69], H in [6,305],
T in [2,8], W in [3.95,35]; require OD in [20,80]. L in [20,250],
`H >= 2T+9`, `L > T+11`, and `L < H+T-2`. Run original snapshot validation
after adapter checks. Ranges are mathematical/source limits, not a physical
printability guarantee. Do not clamp any entered value. Auto lid outside its
feasible domain yields a friendly height error, not a silent changed target.

Why W≥3.95: female thread residual is
`OD/2-(D/2+1.4+.5+.25)=W-2.15`; source requires ≥1.8. At floating-point
boundary do not silently perturb W; use equivalent stable adapter inequality
and verify original schema accepts the mapped snapshot. If exact 3.95 fails
floating evaluation, report the failed constraint or use a documented slightly
higher advertised floor rather than secretly adjust geometry. D39/W3 must
show **This screw lid needs walls of at least 3.95 mm.** This iteration cannot
fulfil that thinner-wall example without a separate mechanics change.

Derived draft summary: **Outside diameter D+2W**, **Outside height H+2T**.
These are design results, not measurements of an old displayed mesh. Canvas
dimension overlays always use successful generated snapshot values and source
coordinates: inner height z=T…H+T, body bore away from thread and floor,
wall away from chamfer/thread. Focus selects the corresponding generated
dimension; if dirty, label preview **Previous generation**. Suppress irrelevant
whole-container annotations for body/lid/print-layout outputs rather than draw
misleading full-height arrows. Closed container supports all four dimensions.

## Actions and lifecycle

First open may Generate the default once, displaying real loading/compiling
stages. Subsequent edits use explicit Generate. Reset restores the complete
adapter defaults (including options/Auto) and invalidates output; it does not
silently compile. Reset view changes camera framing only.

| State | Generate | Cancel | Download | Canvas/status |
|---|---|---|---|---|
| Initial/valid edited | Enabled | Disabled | Disabled | Empty or previous generation; Generate to update |
| Invalid edited | Disabled | Disabled | Disabled | Associated inline field error; previous generation if any |
| Loading/compiling | Disabled | Enabled | Disabled | Current stage, no invented progress percentage |
| Verified current result | Enabled | Disabled | Enabled | Actual STL and its own dimensions |
| Error/cancel/timeout | Enabled if valid | Disabled | Disabled | Reason; previous generation explicitly stale |
| Reset | Enabled | Disabled | Disabled | Default inputs, old mesh cleared |

Editing during work cancels the active request and invalidates it, retaining
only explicitly stale prior preview. Every Generate synchronously reserves a
monotonic epoch **before any await**. Check that epoch after identity/hash
awaits and inside every worker callback and timeout, alongside event job ID,
identity/source/lock checks. Cancel, Reset, edit and superseding request all
increment epoch; terminate old worker, clear timeout and revoke download URL.
Queued old results/logs/errors cannot mutate mesh, status or download. Start
the 180-second timeout directly in the owned request, not click polling.
Only a nonempty, verified current result may install a download; exactly its
returned bytes enter Blob. Preview parse/WebGL failure remains visible but
does not change verified downloadable bytes. User errors are inline; compiler
details remain collapsed. Preserve accessible status and focus without forcing
a modal for normal edits. Download label **Download STL**; fixed footer includes
Generate, Cancel and Reset with readable labels.

## Minimal acceptance evidence

1. Pure adapter: exact baseline snapshot; H60 automatic lid; D39/W4/T4 valid;
   D39/W3 rejection; blank/NaN, too-short height, manual lid outside bounds,
   max OD and drainage near minimum D. Covers hidden algebra/topology mistakes.
2. Deterministic delayed async worker harness: Cancel/Reset/edit during identity
   await and queued late result; superseding generation; timeout; mismatched
   identity; exact Blob bytes. Covers known resurrected-output race.
3. Actual browser WASM run: default assembled then edited valid model;
   independent body/lid/print-layout outputs, successful nonempty parses and
   model bounds matching generated dimensions. Clipping toggle/Reset view must
   leave download hash unchanged. No new CAD/physical acceptance inferred.
4. Desktop screenshots and keyboard checks at required viewports, plus mobile
   reachability. Inspect actual tall-cap section, dimension placement, footer,
   stale error state and focus. Do not count source-string CSS assertions as
   interaction evidence. Retain useful old provenance/engine tests; replace
   brittle assertions that merely lock obsolete layout strings.

## Frozen path/content inputs

Paths below are relative to `projects/laifen-wave-case/`; SHA-256:

```text
0367b4aff210f4638e5f6f0c599ad3e640738de7d09325b551a80344d01aee19 docs/REQUIREMENTS.md
98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353 preview/openscad-wasm-simulator/src/main.mjs
894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0 preview/openscad-wasm-simulator/src/schema.mjs
fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845 preview/openscad-wasm-simulator/workers/openscad.worker.js
b530ae8870b5b2c0eb9548192edeb96fb122860ead203eb1295bd9ebb3893114 preview/openscad-wasm-simulator/style.css
997c2fbc80f453911c3ba68fed55ab17b3c9d2d56d7bb99ceee43a9e0ee82d6f preview/openscad-wasm-simulator/index.html
6d4a6b007f96b00752efd33cf1cf9e4eff5daaf82f011edd0655ea68c20e09b8 preview/openscad-wasm-simulator/dependency-lock.json
ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841 openscad/laifen_case_customizer_v1.scad
bf9ee06d1d3648f9d0fcec27c626f50a8d501db0395d9f071d86a1808b28a79c tests/test_openscad_wasm_simulator.py
903859b70da4f86308170f846ddecbad688b53bd0a3eba211d988dfc8f98659f tests/test_openscad_customizer.py
a7297933430d0e2f2135ff8c5a3ecde2fd573cff1ae90ef042d140bb66f96fa6 tests/test_vfr08_functional_repair.py
```

Image root `/Users/scottchu/.codex/generated_images/01a0731b-e2fe-7c90-98fa-f65de85371f3/`:
selected `exec-f4ef6da2-cf85-4cc0-a5f0-d8fe7190a888.png`, SHA-256
`4cf9b86ddca46524bd4278159b59342e7c7a734da83454b808de813dde7169c1`;
revised action/default visual `exec-eb2f8e66-78c5-4bd9-8acb-69316c8e2a12.png`,
SHA-256 `f4a915c98ad96009436e170d7b65521d32c4735f8887f51d11c1b36172092267`.
Source semantics above supersede illustrated geometry.

CC-DES-01 verified HEAD and source hashes with `git rev-parse HEAD` and
`shasum -a 256`; read source/schema/worker and existing tests; inspected selected
image. No generation, browser, CAD, slicing or physical tests run by designer.
Next: root freezes BRIEF+DESIGN with this manifest and assigns CC-IMP-01.

## CC-DES-01 amendment 1 — drainage visibility

Independent critique identified that hiding the default Bottom drains inside
collapsed options misleads everyday storage users. The correction above moves
the existing Off/Top/Bottom selector directly below the four dimensions, always
visible in both initial and edited states. This adds no parameter or geometry
change and retains the exact default snapshot. Keep lid height and export shape
collapsed. Validate that initial Bottom is readable without expanding options,
Off updates the draft visibly, and the normal stale/Generate contract still
applies. All other requirements and scope remain unchanged.
