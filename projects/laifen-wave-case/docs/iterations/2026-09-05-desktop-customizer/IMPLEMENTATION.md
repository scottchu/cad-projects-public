# CC-IMP-01 implementation receipt

Status: candidate implemented; independent browser validation, critique and
formal review pending. Owner `/root/desktop_implementation`. Baseline
`fef4f264d6af6904e8debd99d522ce186bcec49d`; branch
`codex/container-desktop-customizer`. No commit or deployment by this worker.

Before edits, verified BRIEF `f621ab21455ac5f7b3beede761b1666b784984b8c6db7f16f679d0b7982f8d3d`,
initial DESIGN `a17466cdc49dc7b050fa1a6b7c1f18a31cf3bb36be713ccfc5586aa998e6d51e`
and every source/test path in its SHA-256 manifest using a root `uv run python`
assertion. Accepted and verified the narrow always-visible-drains amendment:
DESIGN `b483baf312658d382549c3bdf8dbabd1d5d08a8c80a80c70a73d3fdc10a32dc2`.
Read repository instructions, state, next-agent, requirements, experience and
decision index. Inspected revised selected image; read Product Design
image-to-code/router/critical overrides and user-context preflight (no saved
context). Real THREE geometry supersedes the illustrative model asset.

## Implemented contract

- CC-01/07: viewport-sized desktop canvas left, 380px right panel, four consistent
  labeled input/unit rows, always-visible drains, collapsible lid/export options,
  local panel scrolling, fixed action footer, readable focus/error/status states,
  stacked mobile viewer and sticky labeled actions. Browser fit remains pending.
- CC-02/03: pure dimension adapter returns the complete exact BROWSER_PRESET at
  defaults, scales Auto lid without rounding the compiled value, derives OD and
  overall height, and applies original schema validation. No SCAD/schema/worker
  or dependency-lock change. All four basic measurements remain user targets.
- CC-04: separate lifecycle reserves epoch before any await; edit/cancel/reset,
  supersession and timeout invalidate the request. Worker ID plus identity,
  source and lock verification gate results; queued duplicate results are
  rejected by retiring completed epochs. Exact returned byte slice enters Blob.
  First opening generates once; edits require Generate. Reset clears old mesh.
- CC-05: actual compiled STL mesh with double-sided plane clipping; 3D and
  Cutaway switch display only; camera framing follows actual mesh bounds.
  Generated-snapshot dimensions are projected into a transparent canvas on
  Cutaway, with accessible text. Part/layout outputs suppress whole-container
  dimensions. Stale preview remains explicitly labeled after edits.
- CC-06: default bottom drains remain visible; Auto/manual lid, Off/Top/Bottom
  drains, assembled/body/cap/print-layout exports remain available. Smooth only;
  Diamond unavailable. No downloadable geometry is manufactured by the viewer.

### Boundary finding

Advertised wall minimum is **4 mm**. The unchanged source schema rejects exact
D=12.5, W=3.95, OD=20.4 because floating evaluation of its female-thread residual
is below 1.8. D=30 and 39 happened to accept 3.95, so that value is not a stable
advertised floor across the diameter range. Node regression captures this
specific failing boundary and verifies D12.5/W4 passes. No hidden perturbation
or silent thickening occurs; 3mm walls produce a plain inline error.

## Commands actually run and results

- `node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs`:
  **11 passed**. Covers exact default, proportional lid, daily-size valid mapping,
  blanks/nonfinite/range constraints, 3mm rejection, min-diameter drains,
  original floating boundary, cancellation/reset/edit during identity await,
  supersession/queued duplicate output, active worker edit, timeout, mismatched
  provenance/empty output, and exact Blob subarray bytes.
  Initial test fixture D12.4 did not exhibit the floating error and failed;
  corrected it to measured exact D12.5/OD20.4 and reran successfully.
- `uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q`:
  **4 passed**. Preserved engine, lock/setup, source identity/schema guards;
  replaced obsolete UI string assertions with labeled control presence checks.
  Behavioral evidence is the Node suite; CSS strings do not establish layout.
- `npm run build:openscad-simulator --workspace laifen-wave-case`: **passed**,
  Vite 6.4.3, 14 modules; THREE-containing bundle emits a >500KB advisory.
- `git diff --check`: **passed** after removing an extra test-file EOF blank line.
- `shasum -a 256` on runtime, tests, README and immutable generator files:
  candidate hashes below; immutable inputs remain unchanged.
- `uv run python /Users/scottchu/.codex/plugins/cache/openai-curated-remote/product-design/0.1.53/skills/user-context/scripts/user_context_preflight.py`:
  no saved product context.

README records the focused verification commands. No Python environment,
package installation, root lock, other project, hosted service, CAD export,
slicer or printer change was made by this worker.

## Candidate path-and-content hashes

Paths relative to `projects/laifen-wave-case/`:

```text
67e6bb6da2a57f2953fe84e93afa848b912e8105ebac796f52ad49bad858b5b6 preview/openscad-wasm-simulator/index.html
724595e26f94c1ad24e96c9814f442ad7cdc18cdc073ef9096527d25989dea0a preview/openscad-wasm-simulator/style.css
8e069d5a15938c3300d663584387d4af0f723f85df674dfb31f29a9911dd27ec preview/openscad-wasm-simulator/src/main.mjs
6660e7b7c133113cf448d672cf7acf455cf0042e22a072c24c5200dfcee0cbd8 preview/openscad-wasm-simulator/src/adapter.mjs
62061fa33b78fdce1f45c4cf1b7ce859257499f41d9558defb54d44e9cfead29 preview/openscad-wasm-simulator/src/lifecycle.mjs
4dea60682d89515f72e917ca140d9297cb0a021b063e1c216bbb07a5140c8a8c preview/openscad-wasm-simulator/src/viewer.mjs
e65e4634bcdcfa01c2ada69a5bc7e594db5045aa0fa973b02d43540cbda70798 tests/node/desktop-customizer.test.mjs
1d58bf29eb8c7e8f2a09892aa294ed3313ba60205aeeea47efdf9e796a88c7e8 tests/test_openscad_wasm_simulator.py
f1a32696b1f1821709d1bf088841b634360dc6f1acc26c273af61a9f8c45446c README.md
```

Immutable: schema `894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`,
worker `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`,
lock `6d4a6b007f96b00752efd33cf1cf9e4eff5daaf82f011edd0655ea68c20e09b8`,
SCAD `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.

## Remaining gate and risks

No self-approval. Independent owner must run real browser WASM compilation for
all four outputs, compare geometry bounds and exact download identity across
view changes, inspect desktop 1280×800/1440×900 and mobile/keyboard states,
and run design QA against the selected image. Cutaway deliberately has no
invented caps on clip faces. Actual fit, slicing, thread strength and physical
acceptance remain outside this UI candidate. Root owns continuity indexes and
next task scheduling. Implementation work paused at this candidate freeze.

## Repair cycle 1 and independent browser evidence

The original candidate failed real browser generation with `TypeError: Illegal
invocation`: native browser timer functions were stored on the Generation
instance and called with the wrong receiver. Repair 1 wraps default timer
calls through `globalThis`. A branded-timer regression now checks the receiver.
Independent review also found dimension anchors could fall below the floor
for a valid tall manual lid and through a default drain hole. The new pure
`dimensions.mjs` places side dimensions between floor and seam and the end
thickness anchor beyond all drain-hole envelopes, inside the bore. Focused
anchor checks cover tall manual lids, minimum/maximum diameter and all three
drain selections. No CAD/source geometry or STL bytes were changed.

Rerun commands were the same Node suite, Python simulator suite, Vite build and
`git diff --check` listed above: **13 Node tests, 4 Python tests, build and diff
checks passed**. Build used 15 modules; the existing >500KB advisory remains.
Repair-specific final hashes supersede the corresponding initial entries:

```text
62f6d413af9347e36e1992cde3c189140821e86b83f862a2877fdb34cbd5e60b preview/openscad-wasm-simulator/src/lifecycle.mjs
7f73511fec8aa507e86c3614698e3e52e9d89f6c18d86ae60eaa541605fc61bd preview/openscad-wasm-simulator/src/viewer.mjs
b19403cf4ae364cb3422937ff2a0761513380a724d7e9dbaaa80ec4932afa479 preview/openscad-wasm-simulator/src/dimensions.mjs
7f8fac641b3a1db7e1a79b4ad2267bec7a2c1a1391e6c71d5f156d0922afb1b7 tests/node/desktop-customizer.test.mjs
```

[Independent validation](VALIDATION.md) subsequently confirmed actual browser
generation and interaction checks. The edited D39/H60/W4/T4 closed-container
STL contains four degenerate seam faces and fails strict manifold validation;
its separately generated body, lid and print-layout samples are watertight.
These are exact generated artifacts from unchanged source, not repaired exports.
The advertised minimum remains 4 mm, with 3 mm walls unsupported. UI validation
does not establish slicing or physical acceptance, and formal disposition
belongs to the independent reviewer and root continuity records.
