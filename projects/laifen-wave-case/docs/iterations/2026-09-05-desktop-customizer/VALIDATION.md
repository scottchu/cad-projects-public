# CC-VAL-01 — independent validation

Status: C2 UI/runtime validation passed; assembled artifact acceptance partial. Owner:
`/root/desktop_validation`, distinct from implementation, critique and formal
review. No implementation or browser candidate has been examined or tested.

## Verified design inputs

`shasum -a 256` verified on 2026-09-05:

- BRIEF.md: `f621ab21455ac5f7b3beede761b1666b784984b8c6db7f16f679d0b7982f8d3d`
- DESIGN.md: `a17466cdc49dc7b050fa1a6b7c1f18a31cf3bb36be713ccfc5586aa998e6d51e`
- src/schema.mjs: `894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`
- workers/openscad.worker.js: `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`
- openscad/laifen_case_customizer_v1.scad: `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`

Read BRIEF, DESIGN and immutable schema. Paths abbreviated above are those in
DESIGN's project-relative manifest. No authoritative source or tests changed.

## Planned gates

| Gate | Credible failure and required evidence | Coverage |
|---|---|---|
| V1 Adapter | Compare every default snapshot key to BROWSER_PRESET; exercise H60 Auto, D39/W4/T4, D39/W3, exact 3.95 boundary, empty/whitespace/NaN/infinity, short height, manual lid limits, OD limits, small-D drainage. Assert no silent coercion or clamping and friendly field association. | CC-02,03,06,07 |
| V2 Lifecycle | Delayed identity/hash plus queued worker events after edit/Cancel/Reset/supersession; timeout, mismatched job/source/lock/identity. Verify old results cannot restore current status, mesh or download; exact returned bytes enter current Blob; URL cleanup and reset semantics. | CC-04 |
| V3 Artifact | Use root-supplied actual browser downloads and snapshot receipts for default, edited, body, lid and print layout. Independently parse nonempty STL triangles and bounds; compare to compiled dimensions/output shape; hash before/after Cutaway and Reset view. Do not substitute a schematic or source-only assertion for generated evidence. | CC-03,04,05,06 |
| V4 Interaction | Root supplies assigned browser surface or screenshots plus bounding boxes at 1280x800 and 1440x900, mobile fallback, keyboard/focus/error/stale states. Inspect left canvas/right parameters, reachable actions, tall-cap cutaway and generated-only measurement labels. | CC-01,05,07 |

Root must provide candidate path/content SHA-256 manifest and prescribed run
command before V1/V2 execution. V3 needs actual download files, generating
snapshot and browser receipt; V4 needs an explicitly assigned browser surface
or root evidence. Pending evidence is not a pass. Any changed declared input
invalidates the corresponding gate. Validation may read the frozen candidate,
run focused checks and write only this record; no test/code changes, rebuild,
printer, deployment or independent browser automation.

Acceptance boundaries: numeric/source, asynchronous behavior, written STL and
browser usability are separate. Physical fit, strength, slicing and printing
remain unverified. Unsupported 3 mm walls are a disclosed mechanics gap, not
an implementation promise.

Initial planning receipt: only this file added. Commands run: `cat` for BRIEF,
DESIGN and schema; `shasum -a 256` for the five paths above. All specified hashes
matched. No findings against an implementation yet. Next: await frozen
candidate and execution assignment.

## C1 execution checkpoint

Root assigned `inputs/candidate-01.sha256`, declared SHA-256
`2146d1d4e338c35d52498172b337d03d9faa47673193fcd2c0369e76679830ce`.
`shasum -a 256 -c` passed 14 declared paths but failed
`tests/test_openscad_wasm_simulator.py`. Test evidence below is therefore
provisional until its actual content is captured in a replacement manifest.
DESIGN amendment makes Drain holes always visible; default remains Bottom.

Commands completed from repository root:

- `node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs`:
  11 passed, including delayed identity cancellation and exact subarray Blob bytes.
- `uv run python -m pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py`:
  4 passed.
- `npm run build:openscad-simulator --workspace laifen-wave-case`: passed;
  Vite warns about the approximately 534 kB minified JS bundle.
- Independent inline `node --input-type=module` adapter probe: 384 combinations
  across D/H/W/T, 132 accepted and 252 rejected; 20 blank/nonfinite checks
  passed. D39/H60/W4/T4 accepted with outside diameter 47 and automatic lid
  26.082191780821915. First probe used exact equality on differently associated
  floating arithmetic and failed by less than 1e-14; rerun used 1e-12 tolerance.
  This was a validation assertion correction, not a candidate defect.

Findings:

1. **Blocker — browser generation crashes.** Root performed the prescribed
   clean-load and click check twice and observed `Illegal invocation` at
   Generation.release, lifecycle line 7, fresh browser logs 23:49:51 UTC.
   Browser-native timer functions appear called with the Generation receiver.
   Node harness substitutes callbacks and misses this runtime failure.
   No real STL or screenshot acceptance is claimed for C1.
2. **Major — dimensions can describe empty space.** Independent probe accepts
   H60/T3/manual L60, but viewer's section formula produces z=-6, below the
   floor at z=3. Diameter/wall arrows do not satisfy their actual-section
   promise for this valid manual lid. All 132 accepted Auto matrix examples
   kept section z above the floor. Root additionally relayed critic evidence
   that the default end-thickness arrow intersects a drain hole; repair pending.
3. **Provenance — one test file differs from the frozen manifest.** Root
   identifies whitespace drift; a new manifest is still required.

CUA access is session-specific: this validator's `getTab`, browser discovery
and `createBrowserTab` found no available browser. Root is collecting browser
evidence as tool operator under this validator's ordered checklist. Any later
browser result must identify root capture; independent interpretation and mesh
analysis remain owned by CC-VAL-01. No Playwright or other UI route was used.

Next: root freezes C2 after bounded repairs. Rerun affected runtime and
annotation checks, then collect actual browser downloads and geometry evidence.

## C2 deterministic evidence

`inputs/candidate-02.sha256` declared SHA-256
`b57642a532d834fddeb56c938496af44a03d3635e4a748ad46ada0cf86df609c`:
all 16 path/content checks passed with `shasum -a 256 -c`. This includes the
previously drifting Python test and immutable source/schema/worker.

Reran the same Node command: **13 passed**, adding timer receiver and
dimension-anchor regressions. Same Python command: **4 passed**. Build was
successful on C1; C2 build and browser acceptance are not inferred from it.

Independent inline Node probe imported the pure adapter and new
`dimensionAnchor` function. Across 1,881 accepted combinations of diameter,
height, wall, ends, Auto/manual lid and Off/Top/Bottom drains, diameter/wall
anchors were strictly above floor and below seam; end anchors lay beyond the
entire drain envelope and inside bore. H60/T3/manual L60 now yields z=4.5,
fixing the C1 z=-6 regression. This checks geometric anchor math, not raster
visibility or actual mesh intersections; those need browser/artifact evidence.

## C2 browser and artifact evidence

Root captured prescribed actual browser actions through CUA; validator read
the supplied screenshots and parsed ordinary Download results independently
with root-workspace `uv run python` and trimesh. Files are temporary evidence
under `/tmp/container-desktop-validation/`, not committed release artifacts.

Viewed `c2-default-cutaway.png` (1487x1058), `c2-desktop1280.png` (1280x800),
`c2-stale.png` (1280x800), `c2-edited-cutaway.png` (1440x900). Desktop canvas
is left, controls right, with four dimensions, drains and footer reachable.
Root bounding-box inspection reports download bottom 776 at 1280x800 and no
page overflow. The tall default cap and actual cavity are visible. Stale view
correctly shows generated ends 3 mm against draft ends 4 mm, labels Previous
generation and disables Download. Edited result shows generated height 60 mm.
The selected reference is not a pixel-identical contract: actual default is
tall, and the 1487x1058 capture differs in aspect from the 1440x900 gate.

| Download | Bytes / triangles | Bounds or extents | Strict topology |
|---|---|---|---|
| default.stl | 12,160,971 / 39,904 | 39 x 39 x 219 mm | Watertight |
| default-after-view.stl | 12,160,971 / 39,904 | 39 x 39 x 219 mm | Watertight |
| edited.stl | 14,139,130 / 45,092 | 47 x 47 x 67.9999999994 mm | Not manifold; see below |
| body.stl | 7,273,700 / 23,606 | 47 x 47 x 50.9178082192 mm | Watertight |
| lid.stl | 6,711,258 / 21,658 | 47 x 47 x 26.0821917802 mm | Watertight |
| print-layout.stl | 14,186,474 / 45,264 | 101 x 47 x 50.9178082192 mm | Watertight |

Default snapshot is D30/H213/W4.5/T3, Bottom drains. Edited and body snapshots
are D39/H60/W4/T4, Bottom drains, Auto lid 26.082191780821915. Bounds agree
with source-derived output dimensions within 1e-5 mm.

SHA-256 receipts:

- Both default downloads: `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`
- edited.stl: `0bdc49630e2185af92c8353ad5bc3af721d8e542daa3b3085d37b64b91bf5f5b`
- body.stl: `29fc301f817c7521ae743795dbb04d3c83412b69751ffc153e166cd6cd632373`
- lid.stl: `cde025c5145fd82ad1cbc3b72bb3b33c6001888aaa6e9fddaa536ae07cc2a2c8`
- print-layout.stl: `c8bb5aceb64f7813e46edc9dff59457db0e00b39ff4de0e81fc1b46db6a7d143`

The second default download followed Cutaway → 3D → Reset view. Equal exact
hashes demonstrate these controls did not mutate that downloaded STL.

**P2 artifact limitation:** edited assembled STL has zero open boundary edges,
four nonmanifold edges and four near-zero-area triangles at seam z≈41.917808219.
Winding is consistent. Two principal connected components are watertight;
two additional two-face degenerate components remain. In-memory vertex welding
at decimal digits 5–9 does not fix it. An investigative in-memory removal of
the four degenerate faces yields a watertight mesh (45,088 triangles). No file
was modified and no repaired download is supplied. Preserve exact generated
bytes; do not claim this assembled example is manifold or print-ready.
Body's clean topology supports an assembled seam residue explanation, but
this remains an inference. Separate lid and print-layout also pass strict
watertight checks with zero open/nonmanifold edges. CAD source is unchanged,
and source repair is outside the UI iteration.

Read root-captured `c2-cancel.txt`, `c2-edit-busy.txt`, `c2-reset-busy.txt`:
actual Generate then Cancel reports Cancelled and disables Download; Generate
then diameter edit reports Dimensions changed and preserves stale state;
Generate then Reset restores 30/213/4.5/3, Auto lid84, Closed container,
clears prior mesh and asks for explicit Generate. Root reports Bottom retained.
These browser actions complement the deterministic late-callback tests; they
do not independently inject a malformed worker payload.

Viewed `c2-invalid.png`, `c2-keyboard.png` (1440x900) and `c2-mobile.png`
(390x844). Root performed keyboard Select all/Backspace: blank diameter remains
blank, displays Enter a number in millimetres, sets aria-invalid=true and
aria-describedby to diameter-help diameter-error, and disables Generate.
Tab advances to Inside height with clear visible focus. Mobile uses normal
vertical scrolling (document 390x1283), with no horizontal overflow and sticky
Generate/Reset at y728–772 and Download y784–830; screenshot supports action
reachability. This is a focused accessibility check, not an exhaustive audit.

Final C2 recheck: all 16 manifest entries still matched. Repeated production
build on C2 passed (15 modules; main JS 534.44 kB, same >500 kB advisory).

## Gate disposition and handoff

| Requirement | Status | Limit |
|---|---|---|
| CC-01 | Pass | 1280x800 and 1440x900 screenshots; root-supplied DOM bounds |
| CC-02 | Pass | Advertised wall floor is 4 mm; requested 3 mm unsupported |
| CC-03 | Pass within UI scope | Exact preset equality, immutable SCAD, actual tall default; no physical claim |
| CC-04 | Pass | Real Generate/Cancel/edit/Reset/download plus adversarial pure lifecycle tests |
| CC-05 | Pass for display/download integrity | Generated annotations; unchanged download hash across view controls; edited assembled mesh has P2 defect |
| CC-06 | Pass for preserved options | All four outputs generated; Auto/manual/drain mapping checked; no Diamond promise |
| CC-07 | Focused pass | Keyboard, associated blank error, busy/stale and mobile checked; not full assistive-technology certification |

Written-artifact acceptance is **partial**: default, body, lid and print-layout
samples pass bounds and watertight checks; edited closed assembly has four
degenerate seam faces and fails strict manifold validation. CAD/source
mechanics, slicing and physical acceptance remain separate and unproven.

Validator changed only this record; temporary artifacts were root-captured,
read-only analyzed, and never repaired in place. Root's next action is formal
review of C2 with this explicit acceptance gap, then a reviewable development
handoff. Do not describe the UI iteration as a new print-ready CAD release.

Final evidence append: independently viewed root-captured
`c2-mobile-ready.png` (390x844), showing the actual tall default cutaway,
generated Inside height 213 mm annotation, Preview up to date, and reachable
enabled Generate/Reset/Download actions. Read `c2-final-errors.json`: errors
array empty since clean reload at `2026-09-05T23:59:28.249Z`. Root reports that
reload reached the successful default result with Download enabled. This
closes the C1 browser timer regression in actual runtime; no additional tests
or candidate edits were made for this evidence append.
