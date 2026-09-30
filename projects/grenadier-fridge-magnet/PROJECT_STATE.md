# Project state

## Baseline

Accepted development source/GLB preview is the P1 R2 color-corrected candidate. Completed P3/P4 diagnostic comparisons retain their exact source and artifacts.

## Active iteration

`p1-r4-nozzle04`; completed native-profile comparison. User subsequently selected a 0.2 mm nozzle.

## Acceptance state

Development preview and diagnostic comparison only. Prepared print release, fine-detail survival, real materials, magnets, and physical validation remain blocked or unverified.

## Next action

Agree the scope of a detail coupon and its material/physical test before new fabrication. No automatic regeneration, scaling, upload, or print start follows from this preservation delivery.

## Historical project records

GM-NOZZLE-01 / 2026-09-06: user confirmed “0.2 it is” after the 0.4 mm comparison. Selected nozzle diameter is **0.2 mm**. This choice does not select final size, filament brand or all other process settings, and does not authorize coupon generation or printer/upload/start actions; existing diagnostic and physical acceptance boundaries remain.

Active iteration: `docs/iterations/p1-r4-nozzle04`. User requested a 0.4 mm comparison after inspecting the 0.2 mm preview. Both unchanged variants sliced with native U1 0.4 mm / 0.08 High Quality settings, child exit 0. Flat estimate 3h45m53s / 23.15 g; relief 4h12m17s / 22.43 g. Size remains 125 × 101.8 mm and is not final. Native first-layer, wall, shell and speed settings also differ, so this is a comparison of native profiles.

P4 output manifest `bb4177d216e744e665ced60ead6646a8f38f90f14310129a4137441322efb1bc`; independent validator fingerprint `96f8e8046ddb896e59e0bf8e07d10511745defc4fde1e8e0ff1e44a971bcb68f`; review media `10e249a13ae7a74f5a449d5755ca21cb145b2402e4cc1f27522f1d2af76a5162`. See active `SETTINGS_RESULTS.md`, `INDEPENDENT_VALIDATION.md` and `HANDOFF.md`. Actual paths preserve readable plate and four main lamp rings, but GRENADIER white strokes are substantially incomplete at the inspected surface layers in both variants; fine concentric details coarsen. Broad blue-gray letter regions mean no depicted path, not fused white extrusion or proven through-holes. This corrects the initial merged-letter interpretation. Temporary PNG diagonal hatching was a rasterization artifact, excluded from findings. No source redesign, physical print or mixing validation. Final scale remains deferred; no printer operation is authorized. Current comparison: https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-nozzles ; corrected delivery fingerprint `a945071c8507c288287f1622ac146a7c88a9dc3a3f2031228a8b31b436982fc8`.

## Retained P3 baseline evidence

Previous iteration: `docs/iterations/p1-r3-slice-probe`. **Both unchanged development variants have real native 0.2 mm diagnostic toolpaths.** The earlier profile-loading crash is resolved by P3-D's bounded profile-layout correction; its two failed attempts remain historical evidence.

Authoritative source/GLB development candidate remains `p1-r2-parametric/color-corrected-candidate-manifest.json`, fingerprint `1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0`. Source `src/parametric_magnet.py`, GLBs `GLB/p1-r2-color-corrected/{flat,relief}.glb`, and accepted D4 face are unchanged. P3 recovery output fingerprint is `3b686c6e33c7bd98562803a6478f78c4ce1c7e8f277c174ff4901931cd9ec39d`.

Native Snapmaker Orca 2.3.5, four 0.2 mm nozzles, 0.08 High Quality, provisional Generic PLA/Textured PEI, current 125 ×101.8 mm work scale. Flat: 25 layers, estimated 6h52m1s/18.37g; relief: 30 layers, 7h12m22s/19.62g. Gcodes: `slicer/p1-r3-recovery/{flat,relief}-run1/plate_1.gcode`. Flat child exit243 occurred after complete Gcode during container path export; relief exit0 also produced `relief-sliced.3mf`. Exact hashes and commands are in active HANDOFF and SETTINGS_DIAGNOSIS.

P3-V independently passed packaging parity and limited feature survival: DJZY 608, GRENADIER and all four main lamp motifs appear in actual toolpaths. Fine gray central lamp trim is fragmented; plate strokes/wordmark edges have small gaps. Surface paths reach about 0.0943 mm, and relief intermediate paths about 0.0443 mm: physical reproduction remains unknown. T0 black/T1 gray/T2 white/T3 blue all extrude. Glass-mix, including pale plate subregions, is provisionally white; no Full Spectrum recipe is accepted.

Acceptance: source/GLB development preview remains accepted; real diagnostic slicing and bounded independent path inspection completed. **Prepared/print release remains blocked**, including missing embedded thumbnails and unresolved detail/structural/material gates. No STEP/BREP or physical acceptance. First-layer bead connectivity, thin/pinched contacts, backing strength, adhesion and magnets remain unverified.

Next smallest material experiment is a scoped plate/wordmark/central-lamp detail coupon after its intent, material and printer authorization. Do not choose final width as a prerequisite, automatically enlarge artwork, or upload/start a print. Actual review-media delivery is complete as recorded below. Existing model review is `https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model`; its P2 PREVIEW_DELIVERY record owns lifecycle.


Actual diagnostic path review: `https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-slice`. P3-DL delivery fingerprint `70e67427e14b88e65c764b475481adeb0e5c7906d696e636286982ee6cc7ca29`; `SLICE_PREVIEW_DELIVERY.md` owns the route,17 HTTP/hash checks and rollback. Root reported Mac-browser plate, wordmark and flat-lamp crops rendered readably. User phone experience is unobserved. Isolated loopback64621 process PID77457 has no autostart; existing model routes and443 Funnel remain unchanged.
