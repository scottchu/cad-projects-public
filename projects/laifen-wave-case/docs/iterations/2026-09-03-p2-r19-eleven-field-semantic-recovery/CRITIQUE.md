# R19 critique — independent visual/UX review

- Role: `CRIT-GCS-R19-01`
- Date: 2026-09-03
- Verdict: `BLOCK`
- Severity: `P1`
- Candidate fingerprint: `566aa6bc8c0aa57f1aeea341805a48db7d54c2078a48cebc4f9204a685e2fc74`

## Provenance

- Verified candidate with `/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/candidate-files.sha256`
- Fresh current-run captures generated with `uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r19-critique/capture.py`
- Supplementary browser check rerun with `uv run python projects/laifen-wave-case/tests/test_p2_r19_browser.py`

## Blockers

1. **Label mini-panels are blank, so the label teaching surface is missing.**  
   Evidence: `scratch/r19-critique/screenshots/42-label-panels.png`, `scratch/r19-critique/sheets/labels.png`, `scratch/r19-critique/screenshots/02-desktop-advanced-full.png`.  
   The OpenSCAD metadata is now outside the active label geometry, which fixes the R17 overlap problem, but the six label mini-panels are empty placeholders. Caption-hidden review therefore does not provide a readable per-field explanation for mode, font, weight, orientation, target, patch, or position. The only visible label explanation is the crowded main label card, which is not enough for an independent no-caption read.

2. **Attachment mini-panels are blank, so the attachment teaching surface is also missing.**  
   Evidence: `scratch/r19-critique/screenshots/46-attachment-panels.png`, `scratch/r19-critique/sheets/attachments.png`, `scratch/r19-critique/screenshots/02-desktop-advanced-full.png`.  
   The four attachment mini-panels render as empty framed boxes. A reviewer cannot independently confirm mode, half, angle, and size from those panels because there is nothing in them. The remaining attachment category card still compresses several annotations into one diagram, so the panel set does not recover human readability.

3. **Polygon preservation is not visually faithful across side counts.**  
   Evidence: `scratch/r19-critique/screenshots/49-poly-3.png` through `55-poly-12.png`, `scratch/r19-critique/sheets/preserved.png`.  
   `poly-4`, `poly-5`, `poly-6`, `poly-7`, `poly-8`, and `poly-12` collapse into nearly the same rectangular proxy. The captures do not teach the intended side-count progression without captions. This violates the requirement that polygon states remain understandable on the visual surface itself.

4. **End-profile visibility is too weak for caption-hidden review.**  
   Evidence: `scratch/r19-critique/screenshots/56-end-flat.png`, `57-end-dome.png`, `scratch/r19-critique/sheets/categories-caption-hidden.png`, `scratch/r19-critique/sheets/preserved.png`.  
   The dome state is visible, but the flat state collapses to tiny marks and the generic ends category card is close to unreadable. The end surface does not carry its own explanation strongly enough once captions are removed.

## Passes and preserved behavior

- No generic/hash witness gimmick was visible in the current-run evidence. The failures come from blank or overly generic proxy visuals, not hidden hash triangles.
- OpenSCAD font metadata is now outside the active label geometry. Evidence: `scratch/r19-critique/screenshots/43-label-font-metadata.png`.
- The ten explicit surface pattern families are visually distinct enough as an isolated sheet, including blunt versus recessed depth. Evidence: `scratch/r19-critique/sheets/surface-patterns.png`.
- Closure screw versus bayonet remains distinguishable. Evidence: `scratch/r19-critique/screenshots/47-closure-screw.png`, `48-closure-bayonet.png`.
- Drains none, bottom, top, and both remain distinguishable in the preserved-state sheet. Evidence: `scratch/r19-critique/screenshots/58-drain-none.png` through `61-drain-both.png`.
- Split position remains visible between low and mid. Evidence: `scratch/r19-critique/screenshots/62-split-low.png`, `63-split-mid.png`.
- The conceptual-only disclosure remains honest and visible in the normal UI. Evidence: `scratch/r19-critique/screenshots/01-desktop-basic-full.png`, `02-desktop-advanced-full.png`.
- The rerun browser matrix passed Chromium, Firefox, and WebKit at desktop and mobile sizes, so this BLOCK is about human-visible teaching quality rather than page breakage or target absence.

## Conclusion

R19 fixes the metadata-overlap issue and keeps the renderer technically alive, but it still fails the human-readable recovery goal. Blank label and attachment panel sets remove the intended teaching surfaces, polygon side-count differences collapse into generic proxies, and end profiles are too weak under caption-hidden review. This candidate should not advance until those visual explanations exist on the page itself.
