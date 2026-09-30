# R-V independent factual and browser validation

Status: **PASS**. Owner `/root/first_layer_validator`, distinct from R-I/R-C/R-R. This role supplied source facts in R-E but did not design or implement slides. No blocking validation finding; read gate released.

Exact HTML `c695741af9b8384f19e3ad847ff1bc54f869578ea7d1a9e19bdc21aa2a112619`; `CANDIDATE.sha256` `a83d2dfa63e328fa19ee86067538a6d3b80dc354f5846a7c7c5e7ab74c3ad86c`. All **27 entries verified before and after capture**. All eight frozen baseline `INPUTS.sha256` entries verified. Baseline HTML `1798b4c485f9923b45bf740ba7df9a27b577e2cf4c0192511b18322215d39651`.

## Commands and results

From repository root:

- `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node --test projects/cad-agent-lunch-and-learn/test/deck.test.mjs`: **5/5 pass**, output `/tmp/cad-collaboration-story-validation/tests.log`.
- `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-collaboration-story-validation/capture.mjs a83d2dfa63e328fa19ee86067538a6d3b80dc354f5846a7c7c5e7ab74c3ad86c 13`: Chrome headless/SwiftShader, network forced offline before local HTML navigation. **13 slides, 13 overview entries, zero audience controls, external runtime resources or uncaught runtime exceptions.** Keyboard End/Home/Right/Left reaches 13/1/2/1, with correct counters and URL hashes.
- `swift /tmp/cad-collaboration-story-validation/pdf-inspect.swift /tmp/cad-collaboration-story-validation 13`: actual PDF **13 pages**, all rendered to PNG and inspected.
- Independent source comparison (`parity.json`): `const nav` and `fitGeometry` byte-identical to the frozen baseline. The simulator change adds projected leader labels; it does not change fit geometry or recorded results.

## Rendered evidence

Reviewed **all 13 desktop slides at 1280×800**, **all 13 mobile slides at 390×844 with every applicable bottom continuation**, **all 13 actual PDF pages**, and desktop/mobile fit fallback. No horizontal overflow or clipped desktop/print claim, diagram, source footer or evidence boundary. Mobile scrolling reaches every section; largest height is 1335 px (1355 px fallback). Slide 5's small mobile schematic labels repeat objects explicitly named in the adjacent readable prose.

Slide 4 has one real WebGL context with 12 initial draw calls and 16 after mobile resize; visible canvas is 525×290 desktop and 335×265 mobile. New leader labels attach to the correct metal rod and printed guide surfaces, remain readable at both sizes, and follow the resized projection. Forced no-WebGL yields zero contexts/draws and the labelled static diagram. Actual print uses that static section and preserves the complete observed-fit table.

## Factual and requirement coverage

- **Actual collaboration / REQ-024:** slide 5 clearly separates the printed center-shaft case from the OD4 sliding-rod coupon. S14's P13 R2 handoff identifies the actual shaft/holes, names diagnosis/implementation agents in its receipt ledger, records the responsible bore-only source change, and preserves the reprint/hand-fit next step. The deck states digital checks passed while repaired physical fit was pending. No invented conversation, actor or successful reprint.
- **Visible failure relationships:** slide 3 sketches the intended 90° wire task; slide 7 shows the required bend versus copied diagonal reference; slide 8 shows shaft/solid-gear overlap. All are labelled conceptual/schematic, with historical CAD and physical evidence distinguished. Source repair proposals are not presented as completed physical outcomes.
- **Pilot fidelity:** slides 9/10 preserve requested head 3/T2, wrong T0 profile result, corrected file, 22/22 completion, and later unaccepted mechanism. They explicitly state that the pilot does not name its failed feature and the center-shaft repair is a separate case. No cap-failure or agent-actor attribution is invented for the pilot.
- **One model and application / REQ-022–024:** slide 6 connects observation to changed agent work/next physical check. Slide 11 provides an explicitly illustrative future arm → camera/force observation → shared next decision loop; no demonstrated integration or force threshold is claimed. Slide 12 gives the portable expect/observe/change-plan statement and concrete too-tight/wobble decision criterion while retaining the actual 4.15 mm observation.
- **REQ-005/006/007/009/014/021:** source attribution, acceptance boundaries, offline delivery, navigation, read-only Three.js, mobile and print remain satisfied. No audience questions or controls were introduced.

Evidence folder `/tmp/cad-collaboration-story-validation/`: `capture.mjs`, `pdf-inspect.swift`, `report.json`, `capture.log`, `parity.json`, `tests.log`, `1280x800-slide-N.png`, `390x844-slide-N*.png`, `*fallback-4*.png`, `deck-print.pdf`, `print-N.png`, and `print-text.txt`. Ordered pixels/count/hash were sent to the independent expert before explanations.

Remaining limits are intentional: teaching geometry is not production CAD or measured print geometry; future tools are illustrative; physical acceptance remains at the recorded source status. R-V made no source/artifact, CAD, slicing, printer/robot, dependency, Git or hosting changes. Next: R-R joins this exact-candidate receipt with R-C's editorial verdict. No further validation is needed unless declared inputs change.
