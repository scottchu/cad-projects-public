# S-V rendering and factual validation

Status: **REPAIR REQUIRED — one concrete direction mismatch**, initial candidate. Owner `/root/first_layer_validator`, independent of writer and editorial readers. All required rendered views inspected on 2026-09-02. Source read gate released after this receipt; initial captures remain immutable evidence.

Candidate HTML `cd7eaf1b751cbe0a1511daa9466600e17f31165d69685a4a92b1acbd81094b22`; CANDIDATE.sha256 `cbf116c59797c80055ee6620fb22abf07b4e5a042d0dc6f3578437106e3b022d`, **32/32 entries verified before and after capture**. Ten slides. Only this receipt and `/tmp/cad-story-refinement-validation` validation artifacts written.

## Finding

**S-V01, P2, slide4 desktop and print:** the introductory curved turning arrow points clockwise; the following slide5 start/end radius turns counterclockwise, matching the documented left-plate +45° example and DESIGN's declared one-left-plate scope. Reverse slide4's arrow to agree with slide5. The mobile slide4 has no turn arrow. This is a visual teaching inconsistency, not a failure of the stationary-axle/curved-guide relationship itself. No other material rendering or factual failure found. Independent editor/questioner findings remain their own receipts and may be consolidated into the same bounded repair.

## Checks and evidence

Commands from repository root, Node `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node`:

- `shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-02-story-refinement/CANDIDATE.sha256`:32/32 PASS.
- `node --test projects/cad-agent-lunch-and-learn/test/deck.test.mjs`:5/5 PASS.
- `node /tmp/cad-story-refinement-validation/capture.mjs cbf116c59797c80055ee6620fb22abf07b4e5a042d0dc6f3578437106e3b022d 10`:exit0, exact before/after identity in report.json.
- `swift /tmp/cad-story-refinement-validation/pdf-inspect.swift /tmp/cad-story-refinement-validation 10`:exit0, **10 actual PDF pages**, all rendered and inspected.
- Source reads and comparison: exact `fitGeometry` retained from frozen baseline; presentation/view code intentionally changed and freshly tested. Primary rail handoff, profile brief, experience and current user recollection are frozen inputs.

Pixel coverage: all10 `1280x800-slide-N.png`, all10 `390x844-slide-N.png`, all9 mobile `-bottom.png` continuations, all10 actual `print-N.png`, plus desktop/mobile `fallback-7` and its mobile continuation. No page-level horizontal overflow: desktop widths1280, mobile390. Mobile long pages scroll with complete accessible content. Slide5 subtitle fits desktop and wraps cleanly in PDF; its full graphic/result/status fit both. The normal mobile navigation has a horizontally scrolling toolbar, with final button partly outside the initial viewport; inherited behavior, not a new slide obstruction.

Runtime: Network explicitly offline before local load; zero external runtime requests and zero browser exceptions. Slide7 actual WebGL context1/draws12 desktop and16 after mobile resize, canvas525×290 and335×265; fallback hidden while ready. Forced getContext failure yields zero contexts/canvas and readable static explanation on both sizes. PDF uses the readable static fit illustration. No audience inputs/forms/interactive scene controls. End/Home/Right/Left correctly produce slides10/1/2/1 and matching10-slide counters/hashes; overview count10.

## Factual and visual boundaries

Slides4/5 distinguish the stationary purple axle from a separate turning center; the curved slot moves with the plate while the axle stays at the same relative world position in both panels. Their captions explicitly describe simplified archived relationships, not the missing original simulator or proof of a working whole jig. The source limits the accepted relationship and retains other contacts/physical unknowns. The arrow mismatch above must be repaired.

The current user's personal recollection supports repeated frustration, reliance on an imagined solution and learning through simulation. No invented numeric attempt count, dialogue or completed physical mechanism added. Slide6's accepted profile before full preview is grounded in the P20R4 brief and visibly limited to a preview. Slide7's earlier OD4 coupon remains a separate case: exact recorded qualitative outcomes, 4.15 sliding reference, 4.05 model shown, enlarged gap disclosed; no undocumented agent actor. Orthographic rod/guide/gap leaders were inspected and readable. Kage's shaft/solid-gear overlap remains explicitly digital and restart tests pending. Camera/sensor/robot example is explicitly a future illustration. Pilot and printed-center-shaft episodes are absent from the main story, so no cross-case physical-defect attribution occurs.

Next: make consolidated focused repair, freeze a new exact candidate, compare sections/CSS/scripts with this initial candidate, then recapture only changed slides and actual PDF pages. Carry unchanged runtime/source evidence only when exact parity is established. No production CAD, slicer/printer, dependency, Git or hosting work performed.

## Repair1 final verdict — PASS

Final HTML **`2b3f920093ec773643d776d20fc38daa96e4de25a42b4c48cba98291ff299b7e`**; final candidate manifest **`fff210b837e87c698e18c18b47c8e18caf993ab06aa0d337289902d41ad66605`**,32/32 entries independently verified before/after fresh captures. S-V01 is closed. No remaining material factual/rendering issue. Source read gate released; editorial and formal review remain separate gates.

Compared against the exact initial source frozen in `/tmp/cad-story-refinement-repair1-baseline/projects/cad-agent-lunch-and-learn/`: changed sections are exactly2/4/5/6/7; sections1/3/8/9/10, shared CSS, both executable scripts, simulator and existing tests are byte-identical. `/tmp/cad-story-refinement-repair1-validation/parity.json` records the result. The newly rendered unchanged PDF pages are also pixel-file identical to initial pages1/3/8/9/10. Their initial reviewed evidence and the5/5 test result therefore carry forward; no broad test rerun was necessary.

Fresh command: `node /tmp/cad-story-refinement-validation/capture.mjs fff210b837e87c698e18c18b47c8e18caf993ab06aa0d337289902d41ad66605 10 /tmp/cad-story-refinement-repair1-validation 2,4,5,6,7` → exit0. `swift /tmp/cad-story-refinement-validation/pdf-inspect.swift /tmp/cad-story-refinement-repair1-validation 10` → exit0,10 actual pages. Reviewed all five changed desktop screenshots, five mobile top/bottom pairs, five changed actualPDF pages and refreshed desktop/mobile fallback7. Capture report again has zero external requests/exceptions/controls, correct ten-slide navigation, width1280/390 with mobile scrolling, actual offline WebGL and readable forced fallback.

Pixels confirm slide4's arrow now turns counterclockwise in agreement with slide5. Slide5's new leaders identify the actual curved groove and orange orientation mark in both states, including mobile and print; fixed axle remains stationary while the plate/slot rotate. Subtitle and result fit. No original-simulator recovery, full physical closure or working-jig claim added. Slide2 honestly labels the image as an early digital task sketch and introduces the later purple-axle layout in a separate caption, without attaching a false fixed-member label to the historical pictured part. Slide6 now describes agreeing a small picture in past tense and the complete model as the next intended preview; the source-supported accepted profile and physical-unproven boundary remain intact. Slide7's “Model hole” wording is accurate and preserves exact observed outcomes, model/print separation and different highlighted4.15 sample.

Changed paths: this VALIDATION receipt and temporary capture/parity/PDF artifacts only. Primary project/source facts remain read-only. Final next action: join this exact-candidate PASS with matching editor/questioner and formal-review receipts. No further validator repair requested.
