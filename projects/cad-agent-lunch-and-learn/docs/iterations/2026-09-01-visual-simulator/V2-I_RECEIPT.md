# V2-I implementation receipt

Status: candidate ready for independent critique and validation.

Frozen inputs: `6449532b4b7e1a11537973eb9921350ea4072a7df5931c46d3f1209e51bbcc79`, verified 29/29 before candidate freeze. Candidate manifest: `CANDIDATE.sha256`; its HTML is `0137256dd33156955f9e9382b230b7667ceabe6cc4bf62d6d7e3b6ab8138ec05`.

Changed paths: `build.mjs`, new `simulator.mjs`, regenerated `index.html`, project `package.json`, root `package-lock.json`, and `test/deck.test.mjs`. The lock adds only the project workspace link and exact `three@0.176.0` runtime / `esbuild@0.25.8` build dependency metadata. Existing package versions were not changed.

Implemented slides 3, 6, 13 and 20: reasoning feedback flow, inline-bundled Three.js cutaway with arithmetic/keyboard/camera controls and SVG fallback, three-row semantic evidence table, and implementation/critique/validation/review flow. The simulator uses `D=4.00`, selected `H`, error `e`, and display bore `2 + 8 * (H + e - 4)/2`; it labels all results as hypothetical geometry and retains the independent coupon observations unchanged.

Commands and results:

- `npm install` from the repository root: completed; lock contains the exact scoped dependencies.
- `npm run build --workspace cad-agent-lunch-and-learn`: wrote a 22-slide standalone HTML artifact.
- `npm run check --workspace cad-agent-lunch-and-learn`: 5/5 pass, including parsed inline scripts and no runtime external-resource selectors.
- `shasum -a 256 -c .../FROZEN_INPUTS.sha256`: 29/29 pass.
- `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-visual-validation/validate-v2.mjs <index.html> 0137256dd33156955f9e9382b230b7667ceabe6cc4bf62d6d7e3b6ab8138ec05 normal`: 23 checks, 0 failures. It exercised real SwiftShader WebGL drawing, arithmetic default/contact/interference/range cases, state preservation, keyboard controls, hidden rendering, sources/notes/exercise 2, responsive snapshots, printing, offline requests, and runtime exceptions. Output: `/tmp/cad-agent-visual-validation/0137256dd331-normal/`.

Coverage: REQ-012 through REQ-014 and preserved 22-slide/evidence boundaries. Limits: this is a teaching model, not CAD, slicer, manufacturing, or physical-fit acceptance. Independent critique, fallback-mode validation, print inspection, and formal review remain required.

## Repair 1 candidate

Independent validation and critique rejected the initial candidate for a tapered cone used as a sleeve, unavailable/mismatched fallback, interaction-dependent print content, and disconnected flow edges. The replacement candidate HTML is `bc0b7920e4ec964606e2155ce684cba571616e0b9ce48a4559e58355879683d1`. `simulator.mjs` now creates a 270-degree constant-inner/outer-radius annular `ExtrudeGeometry` with axial cut faces; its rod shares the extrusion axis. The fallback is a filled analytic outer/bore/rod section, and printing uses a separate fixed H=4.15/e=0 section and metrics with all observations. Both flows use shared absolute node/edge coordinates and marker arrowheads in desktop, mobile and print CSS. `npm run build`, `npm run check` (5/5), the candidate manifest (6/6), frozen inputs (29/29), and focused normal WebGL harness (23/23) passed. Independent repair validation/review is still pending.

## Repair 2 — final bounded implementation

Owner: `/root/presentation_visual_repair`, replacing the stopped original implementation owner. Status: author checks complete; frozen for distinct critique, validation and formal review. HTML SHA-256 `9f246ce8a7e52b24ca8c9b2414544b4d21f44628eb98a5150d5a3b75b8cb22c8`; seven-entry candidate manifest SHA-256 `8f62e12039798d71983d0e76a412c7bf2f349bb17b0d5b02ced9f387b332d1d3`. Frozen design remains `6449532b4b7e1a11537973eb9921350ea4072a7df5931c46d3f1209e51bbcc79` (29/29 checked).

Changed in this repair: `build.mjs`, generated `index.html`, `README.md`, candidate manifest and this receipt. Simulator source remains byte-for-byte repair 1: `eb78fb051d0b6d59b641f3b84f739108a7d6eb3ffdc96cd5da4d33c7aa65d2cc`. Package/lock/tests unchanged. Three.js 0.176.0 and esbuild 0.25.8 remain pinned and inline-bundled; no new runtime resources.

- Replaced competing graph layout rules and mixed HTML/SVG coordinates with native SVG rectangles/text/connectors in one coordinate system per responsive layout. Desktop and print show the full reasoning convergence/feedback and agent fork/join; narrow screens use equivalent vertical layouts with readable arrowheads. Unique markers eliminate the stale undefined marker reference.
- Moved the dedicated fixed-default printable teaching section outside the hidden live layout. It contains labeled sleeve/rod geometry, ×8 radial display clearance, all default arithmetic and all five unchanged coupon observations. Print remains independent of the live error control.
- Corrected the actual `.fit-ui #fit-results small` selector to a 14 px context label; mobile content now supports ordinary page scrolling and preserves toolbar separation.
- README identifies current DESIGN, both authoritative source modules, root npm installation/build/check commands, private review address and offline bundled Three.js/fallback behavior.

Commands from root: `PATH=/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin:$PATH npm run build --workspace cad-agent-lunch-and-learn` produced 22 slides; corresponding `npm run check --workspace cad-agent-lunch-and-learn` passed 5/5. `shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-01-visual-simulator/FROZEN_INPUTS.sha256` passed 29/29. `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-repair2-browser.mjs` captured slides 3/6/13/20 at 1280×800, 1920×1080 and 390×844 and wrote actual PDF after setting live error to −0.25. `swift /tmp/cad-agent-visual-validation/pdf-inspect.swift /tmp/cad-agent-repair2-author` confirmed 22 landscape pages at 960×540 pt.

Evidence: `/tmp/cad-agent-repair2-author/` contains `{laptop,projector,mobile}-{3,6,13,20}.png`, `mobile-6-observations.png`, `report.json`, actual `deck-print.pdf`, `print-6.png` and other PDF page renders. PDF SHA-256 `c71be3ba5ec15a54db11998994797ddcf32bcb2493db5ca155a2d0b7ce4409dd`. Author visually inspected laptop slides 3/6/13/20, projector slide 3, mobile diagrams and revealed coupon, and actual printed pages 3/6/20. Page 6 visibly contains H=4.15/e=0.00, +0.15 diametral/+0.075 radial, Geometric gap, the labeled section and all five observations. Caption computed size is 14 px across viewports. An initial headless compositing capture of laptop slide 3 was discarded and recaptured after navigation; the final inspected screenshot is correct.

Coverage: focused C-01/C-02 and V-03/V-04/V-05 repair; no new CAD, slicer, manufacturing or physical claims. Geometry/math/fallback runtime source is unchanged from independently verified repair 1. Independent owners must assess this exact candidate; author checks do not confer acceptance. All browser processes closed. Next: C/V affected gates, then formal R. Root owns continuity-index synthesis.
