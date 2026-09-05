# R21 critique — independent visual and interaction review

- Role: `CRIT-GCS-R21`
- Date: 2026-09-04
- Verdict: `BLOCK`
- Severity: `P1`
- Candidate fingerprint: `3d2ce130e8724af9b80a7617296276c71e8d08c02b3117d94f1ad52ff004f443`
- Frozen design fingerprint: `6d862ad3294a460da1cfdceace4e499d3fe23c809e5bb520767713cad18205df`
- Implementation evidence fingerprint verified: `41f76a57cded945c9be3f5dd7164c29389438f5e57aeaee998ec6f533ec9f7ad`

## Provenance

- Verified candidate manifest with `/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r21-threejs-interaction-fidelity-recovery/candidate-files.sha256`
- Verified manifest fingerprints for `candidate-files.sha256` and `evidence-files.sha256`
- Fresh current-run captures generated with `uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r21-critique/capture.py`
- Supplementary browser matrix rerun with `uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r21_browser.py`

## Blockers

1. **Screw versus bayonet is still not visually understandable from the real viewport.**  
   Evidence: `scratch/r21-critique/screenshots/10-closure-screw.png`, `11-closure-bayonet.png`, `scratch/r21-critique/sheets/closures.png`.  
   Orbit works, but the captured closure states still read almost the same in the primary review angle. The bayonet state does not surface countable lugs or receiving geometry strongly enough to separate it from the screw state without already knowing which control was selected.

2. **Label coverage is incomplete because the patch state is not visually readable.**  
   Evidence: `scratch/r21-critique/screenshots/43-label-inset-lower.png`, `44-label-outset-upper-vertical.png`, `45-label-patch.png`, `scratch/r21-critique/sheets/labels.png`.  
   Inset and vertical label placement are present, but they are still small. The patch scenario does not produce a strong, unmistakable patch read in the viewport. This leaves `label.patch` below the required no-caption clarity bar.

3. **One required attachment mode still disappears: keyring tab is not visibly distinct.**  
   Evidence: `scratch/r21-critique/screenshots/49-attachment-keyring.png`, `scratch/r21-critique/sheets/attachments.png`.  
   Eyelet, captured loop, separate clip link, and bridge handle show distinct accessory geometry. `keyring_tab` does not. In the current-run screenshot it collapses into the body view and is not independently understandable as a tab plus bore.

4. **Several surface family distinctions still depend too much on color and remain too weak as shape differences.**  
   Evidence: `scratch/r21-critique/sheets/patterns.png`, `scratch/r21-critique/sheets/fades-relief.png`.  
   The WebGL surface is real and the families are more separated than R20, but some pairs still miss the intended “understandable from the viewport alone” standard. `blunt_diamond` versus `recessed_diamond`, the three fade states, and the three relief states rely heavily on line color and subtle amplitude changes. They do not yet teach their differences as clearly as the polygon and drain views do.

## Passes

- Pointer orbit and wheel zoom are real and usable. My independent drag/zoom probe changed camera pose and pixels: `camera_changed=True`, `changed_pixels=243879`, `rms=24.1510`. Evidence: `scratch/r21-critique/screenshots/06-orbit-before.png`, `07-orbit-after.png`.
- Camera fit is materially better than R20. The assembled and exploded states stay in frame on desktop and mobile. Evidence: `scratch/r21-critique/screenshots/51-assembled.png`, `52-exploded.png`, `53-mobile-viewport-default.png`, `56-mobile-viewport-exploded.png`.
- There is no visible SVG card, proxy witness sheet, hash witness, or fake placeholder geometry. The main surface is real WebGL.
- Conceptual-only disclosure is visible and honest on the page. Evidence: `scratch/r21-critique/screenshots/01-desktop-basic-full.png`, `02-desktop-advanced-full.png`, `03-mobile-basic-full.png`, `04-mobile-advanced-full.png`.
- Polygon progression is readable in top view across `3/4/5/6/7/8/12`. Evidence: `scratch/r21-critique/sheets/polygons.png`.
- Drain modes `none/bottom/top/both` are readable in top view. Evidence: `scratch/r21-critique/sheets/drains.png`.
- End profiles `flat/chamfer/rounded/dome` are more distinct and readable than in R20. Evidence: `scratch/r21-critique/sheets/ends.png`.
- Assembled versus exploded same-diameter states are clear. Evidence: `scratch/r21-critique/sheets/assembled-exploded-mobile.png`.
- Desktop and mobile page composition stayed stable in the current-run browser matrix and in the independent full-page captures.

## Unresolved risks

- The current camera presets can expose some families better than the default ISO view, but the most important acceptance question is still whether a reviewer can tell the semantic differences from the viewport itself. R21 now has the interaction tools, yet several required states still do not communicate enough once captions and readouts are removed.
- The separate truthful OpenSCAD font metadata is visible on the full page, but the label geometry itself remains the limiting factor for human readability.

## Conclusion

R21 fixes the interaction failure and restores several real visual families, so it is a meaningful recovery over R20. It still does not clear the independent critique gate because closure mode, patch visibility, keyring-tab visibility, and some pattern/fade/relief distinctions remain too weak for a no-caption human read from the real viewport.
