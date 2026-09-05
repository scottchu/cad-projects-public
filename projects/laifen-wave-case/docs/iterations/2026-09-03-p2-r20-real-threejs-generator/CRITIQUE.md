# R20 critique — independent visual and UX review

- Role: `CRIT-GCS-R20-01`
- Date: 2026-09-04
- Verdict: `BLOCK`
- Severity: `P1`
- Candidate fingerprint: `ae45f4e28fd6c34b09c56c34a4d55eb0bed7620f101559e028aa31d12fd98ad4`

## Provenance

- Verified candidate with `/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r20-real-threejs-generator/candidate-files.sha256`
- Fresh current-run viewport and page captures generated with `uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r20-critique/capture.py`
- Supplementary browser matrix rerun with `uv run python projects/laifen-wave-case/tests/test_p2_r20_browser.py`

## Blockers

1. **Orbit inspection is missing, so the user cannot actually inspect the 3D object.**  
   Evidence: `scratch/r20-critique/screenshots/48-orbit-before.png`, `49-orbit-after.png`, `scratch/r20-critique/sheets/closures.png`.  
   The viewport drag probe produced `changed_pixels=0` and `rms=0.0000`. The camera stays fixed even after a deliberate drag gesture. This is a direct UX failure for a Three.js review surface because many distinctions depend on changing the view, yet the app gives the user no orbit, pan, or zoom control.

2. **Several required visual families still collapse into one generic textured cylinder.**  
   Evidence: `scratch/r20-critique/sheets/patterns.png`, `scratch/r20-critique/sheets/fades-relief.png`, `scratch/r20-critique/sheets/closures.png`.  
   The viewport is real WebGL, but the scene does not become human-readable. `smooth`, `blunt_diamond`, and `recessed_diamond` are too close; `straight_micro_flutes`, `flowing_flutes`, and `wave_flutes` also read as small variations of the same wrapped line texture. Fade-from-bottom, fade-from-top, and center-band are barely distinguishable at this camera angle, and relief inset/outset/balanced remains subtle. Screw versus bayonet is also not visually understandable from the fixed scene because the visible seam stays almost the same.

3. **Label behavior is clipped and incomplete, and the OpenSCAD font metadata is not visible to the reviewer.**  
   Evidence: `scratch/r20-critique/sheets/labels.png`, `scratch/r20-critique/screenshots/02-desktop-advanced-full.png`, `04-mobile-advanced-full.png`.  
   The lower inset label is partially readable, but the upper vertical label is clipped off the top edge of the viewport. The patch state is also hard to read because it sits on the same dark blue geometry with limited contrast. The prompt asked for label evaluation, including font-related behavior, but the OpenSCAD font metadata is not surfaced anywhere on the visible page or viewport. A hidden scene object is not enough for a human critique surface.

4. **Attachment modes are not visually distinct enough, and some accessory states clip outside the frame.**  
   Evidence: `scratch/r20-critique/sheets/attachments.png`.  
   `integrated_lanyard_eyelet` and `bridge_handle` both read as the same floating torus. `separate_clip_link` mainly changes vertical offset, not attachment identity. `keyring_tab` is partially clipped off the lower-left edge. This makes attachment mode, presentation, half, and angle hard to understand without source knowledge.

5. **Drain and polygon review remains too weak for a caption-free decision.**  
   Evidence: `scratch/r20-critique/sheets/drains.png`, `scratch/r20-critique/sheets/polygons.png`.  
   Drains are technically present, but top/bottom/both differences are tiny dark holes near the rim and are easy to miss at review size. Polygon `3` is obvious, but `5`, `6`, `7`, `8`, and `12` compress toward the same oblique silhouette. Without orbit or a more explanatory viewpoint, the side-count progression is not reliably readable.

## Passes and preserved behavior

- The page does use a real Three.js viewport rather than SVG witness cards.
- The conceptual-only disclosure is visible and honest on the full-page UI. Evidence: `scratch/r20-critique/screenshots/01-desktop-basic-full.png`, `02-desktop-advanced-full.png`.
- Desktop and mobile layouts stay intact in the current-run browser evidence; the blocking issue is scene readability, not overflow or page failure.
- The same-diameter two-piece form is visible, and an exploded state is visible in `scratch/r20-critique/screenshots/06-exploded-viewport.png`.
- End profiles improve somewhat over R19: chamfer, rounded, and dome are more visible than before, with dome the clearest. Evidence: `scratch/r20-critique/sheets/ends.png`.
- No generic hash-derived witness triangles or other visible hash gimmicks appeared in the current-run evidence.

## Conclusion

R20 fixes the earlier SVG-card architecture, but the main critique goal is still not met. The viewport is real, yet it remains hard to learn from because the camera is fixed, many families still read as the same cylindrical proxy, labels and attachments clip or disappear, and several required distinctions are too subtle for caption-free human review. This candidate should not pass until the scene is inspectable and each required family has a clearly different visual expression from the actual viewport.
