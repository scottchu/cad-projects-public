# CC-CRIT-01 independent design critique

Status: C2 independent UI/source critique and visual QA passed with explicit acceptance limits. Historical checkpoints below preserve earlier findings and repairs.
Owner: `/root/desktop_critic`, distinct from design, implementation, validation and formal review.
Reviewed 2026-09-05. No runtime implementation files were inspected during concurrent edits.

## Frozen evidence

Verified `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-05-desktop-customizer/inputs/design.sha256`: all three paths OK.

- BRIEF: `f621ab21455ac5f7b3beede761b1666b784984b8c6db7f16f679d0b7982f8d3d`.
- DESIGN: `a17466cdc49dc7b050fa1a6b7c1f18a31cf3bb36be713ccfc5586aa998e6d51e`.
- Selected desktop image: `f4a915c98ad96009436e170d7b65521d32c4735f8887f51d11c1b36172092267`.

Read BRIEF and DESIGN and visually opened the selected desktop image with `view_image`. No tests, generation or physical inspection performed by this role in this phase.

## User-intent assessment

No blocking contract defect found within the explicitly frozen scope of preserving current screw mechanics. The contract directly addresses the user's central complaint: canvas left, dimensions right, no introductory header, four direct measurements rather than competing bore/outer-diameter controls. Generate, Cancel, Reset dimensions, Reset view and exact-current Download have separately defined effects. The selected image is a direction for composition and clarity, not geometry authority.

The following are material limits and acceptance checks, not approval of unseen implementation:

1. **Medium — generic-container promise remains incomplete.** The requested 3 mm wall cannot be produced by unchanged mechanics. The explicit, plain-language rejection is honest and acceptable for this bounded UI iteration, but completion must not be reported as satisfying that geometry example. A separate mechanics decision is still needed if 3 mm remains required.
2. **Medium — defaults retain drainage.** Bottom holes are hidden by the collapsed options panel. This preserves the existing preset but is a poor general storage default, especially for small items. Preserve it for this iteration as specified; final communication should identify that this is the existing container preset, not an undrained everyday-storage default. A later explicit default change requires its own source/preset decision.
3. **Medium — cutaway must teach dimensions.** Real clipping without invented section caps is appropriate. Acceptance must check that floor, wall, interior and tall lid remain intelligible at normal desktop scale, and that dimension arrows reference generated geometry. A plausible cylinder illustration does not meet this gate.
4. **Medium — state clarity determines usefulness.** Four inputs alone are insufficient if users cannot tell whether the canvas reflects them. Inspect readable previous-generation, invalid and busy states and persistent footer at the specified viewports. Download must never retrieve an earlier shape after an edit or reset.
5. **Low — parameter helper text is necessary.** Body-side wall thickness and a slightly wider lid are understandable only with the short helper text promised by DESIGN. Keep numerical relationships internal; do not expose more adjustment controls to explain them.

Coverage: CC-01/02/04/06/07 contract supports intended workflow; CC-03/05 are credible but require actual candidate evidence. CAD, STL and physical acceptance are not established by this critique.

Next: receive frozen candidate and validator screenshots, compare reference and implementation together, then record final visual critique/design QA. Do not reopen unchanged design solely for raster differences in the AI illustration.

## Candidate 01 independent source critique — blocked

Candidate manifest itself verified SHA-256 `2146d1d4e338c35d52498172b337d03d9faa47673193fcd2c0369e76679830ce`. Full `shasum -a 256 -c .../inputs/candidate-01.sha256` returned exit 1: `tests/test_openscad_wasm_simulator.py` mismatched; all other entries matched. This is a provenance stop, not a runtime finding. Root was notified immediately. Read-only analysis of the matching adapter, lifecycle, main, viewer, HTML/CSS and authoritative SCAD identified the following repair. No C1 gate pass is granted.

### P2 — measurement arrows can reference empty space

Location: `preview/openscad-wasm-simulator/src/viewer.mjs`, `drawDimension()`.

The diameter/wall anchor uses `min(T+H*.25,H+2T-L-12)`. A valid manual lid case H=60,T=4,L=60 produces section Z=-4, below the entire container. A single executable probe through `adapt({...DEFAULTS,height:"60",ends:"4",lid:"60",auto:false})` returned `errors:{}` and computed `sectionZ:-4`. Exact command:

```sh
node --input-type=module -e 'import {adapt,DEFAULTS} from "./projects/laifen-wave-case/preview/openscad-wasm-simulator/src/adapter.mjs"; const a=adapt({...DEFAULTS,height:"60",ends:"4",lid:"60",auto:false}); console.log(JSON.stringify({errors:a.errors, values:a.values,sectionZ:Math.min(4+60*.25,60+8-60-12)}));'
```

The end-thickness anchor defaults to x=D*.27=8.1,y=0. The authoritative default bottom drain is centered x=9,y=0 with radius 1.5, so the whole thickness arrow lies inside a hole. The height arrow also uses the central drain axis, a less severe ambiguity but worth resolving with the same helper. Verified source `drain_pattern` explicitly creates the center hole and six ring holes.

Impact: the visual teaching aid points to missing material, undermining the user's reason for choosing cutaway and violating CC-05. Fix: derive a bore/wall section between the floor and actual body seam, and place end/height anchors at a guaranteed undrilled interior coordinate. Preserve CAD/export geometry; only annotations need correction. Root routed this grouped defect to implementation repair 1.

The earlier hidden-drain concern is addressed in amended DESIGN SHA `b483baf312658d382549c3bdf8dbabd1d5d08a8c80a80c70a73d3fdc10a32dc2`: Drain holes is now always visible directly below the four dimensions. Candidate HTML follows that instruction. Full final visual verification remains pending.

Root reports independent live-browser P0: native timer receiver binding throws `Illegal invocation` in `Generation.release`, preventing Generate on a fresh reload at 23:49:51 UTC. This role did not own or reproduce the browser; use the validator's evidence for that finding. It is independently sufficient to keep C1 blocked.

Stop C1 review here. Next: receive C2 freeze after the lifecycle/annotation repairs, verify all frozen paths, and compare actual screenshots to the selected reference in one tool input. No implementation visual pass, physical acceptance or export acceptance is inferred from this source critique.

## Candidate 02 source repair verification

Manifest SHA-256 `b57642a532d834fddeb56c938496af44a03d3635e4a748ad46ada0cf86df609c` verified; `shasum -a 256 -c .../inputs/candidate-02.sha256` returned exit 0 with all 16 entries OK. Reviewed new `dimensions.mjs` and revised `lifecycle.mjs`.

The grouped C1 P2 is resolved in source: diameter/wall section Z is the midpoint between floor and actual body seam; because the adapter requires seam > T+2, it stays above the floor and below the one-millimetre shoulder. End thickness chooses the midpoint between the outer radial extent of all drain holes and body bore, so the endpoints describe solid floor material. Native timers are now wrappers calling `globalThis.setTimeout/clearTimeout`, addressing the receiver-binding defect; actual browser success remains the validator/root's gate.

The height line remains at the central axis. That is an acceptable nominal interior-height measurement, though moving its endpoint to an undrilled floor area could improve teaching clarity (P3 only).

Source review finds no remaining P0/P1/P2 in these repairs. This is not yet a final visual pass. Await actual screenshots matching the selected reference and required desktop/mobile states.

## C2 final critique receipt

Status: **passed for reviewed UI/source and visual-design scope**; no remaining actionable P0/P1/P2 in that scope. Final `shasum -a 256 -c .../inputs/candidate-02.sha256` again returned exit 0, all 16 entries OK. Manifest SHA remains `b57642a532d834fddeb56c938496af44a03d3635e4a748ad46ada0cf86df609c`.

Applied the Product Design `design-qa` comparison workflow. Opened the frozen reference and root-captured actual default compiled Cutaway together in one `functions.exec` input, matching 1487×1058 pixels/CSS viewport and DPR 1. The project-root `design-qa.md` records the five fidelity surfaces, permitted real-geometry/sidebar differences, C1 repair history and full final evidence. Also opened actual 1280×800 current/stale/busy captures, 1440×900 edited/cancel/Print layout/invalid/keyboard captures, and 390×844 mobile invalid/ready captures. Primary inputs/actions fit; error/focus, stale values, busy cancellation and mobile footer are legible. No extra illustrative geometry, unsupported controls or title block were introduced.

Read the validator's independent receipt for adapter/lifecycle/artifact checks, and opened root's final clean-reload console result: since `2026-09-05T23:59:28.249Z`, `errors: []`. Browser operation remained root-owned under validator instructions. Critic did not run an alternative browser or claim the validator's tests as its own.

Requirement coverage: CC-01/02/04/05/06/07 reviewed UI contracts and visual states pass; CC-03's preserved geometry is supported by unchanged source fingerprint and validator's snapshot/bounds evidence. Source review confirms the grouped C1 annotation P2 repairs. P3 only: height line could move off the central drain axis and seam lighting could be clearer. Neither blocks the operative desktop direction.

Separate unresolved acceptance limits: 3 mm requested walls remain unsupported (advertised minimum 4 mm under preserved screw mechanics); default Bottom drains remain visible; physical fit/printing/slicing are unverified. Validator identifies an edited assembled-STL artifact limitation: four near-zero-area seam triangles/four nonmanifold edges, while body/lid/Print layout pass its watertight checks. This visual pass does not approve that assembled artifact as manifold or print-ready. Exact downloaded bytes remain unchanged by the UI.

Changed paths by this role only: this `CRITIQUE.md` and project-root `design-qa.md`. No source, tests or artifacts changed. Next: distinct formal reviewer joins frozen C2 with validation and design-QA receipts; root handles continuity and a clearly scoped handoff.
