# CRIT-GCS-R16-01 independent visual and UX critique

**Verdict: BLOCK.** Candidate manifest fingerprint `14b625606e1abd2a705d1874b557d9a9ba9ad6cc368d306de5d42417c8362a5e` verifies, and this run captured fresh desktop and mobile evidence from the exact R16 preview. R16 did remove the old R13-style generic hash-witness triangles, and several relationships are now clearer. It still fails the requested human-recognition gate because three category cards remain too crowded or too weakly differentiated to teach the intended relationships without captions: `surface`, `labels`, and `attachment`. This remains conceptual browser-preview evidence only; it makes no CAD, OpenSCAD, STEP/export, slicer, printability, fit, or physical claim.

## Provenance and method

- Owner and role: `CRIT-GCS-R16-01`, independent visual/UX critic. Candidate source and tests remained read-only. This task wrote only this critique, `CRITIQUE_EVIDENCE_MANIFEST.sha256`, and `scratch/r16-critique/**`.
- Candidate verification command: `/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r16-final-semantic-mapping-recovery/CANDIDATE_MANIFEST.sha256`. All listed candidate files passed, and the manifest SHA-256 matches the required fingerprint above.
- I read the current project continuity files plus the frozen R16 brief, design, handoff, and implementation receipt. The findings below use only current-run screenshot evidence.
- Fresh evidence command: `uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r16-critique/capture.py`.
- The capture run served the exact preview from an ephemeral loopback server and saved 89 current-run records: desktop/mobile full UI, invalid-clearing screens, and category-state screenshots for `container`, `closure`, `ends`, `surface`, `labels`, `attachment`, and `drains`.
- Accepted evidence is frozen in `projects/laifen-wave-case/scratch/r16-critique/capture.json`, the underlying screenshots in `projects/laifen-wave-case/scratch/r16-critique/screenshots/`, and one contact sheet per category in `projects/laifen-wave-case/scratch/r16-critique/sheets/`.

## P1 blockers

### R16-C01 — the surface card does not teach all ten pattern families

The `surface` card still collapses multiple named families into near-identical local line work. The clearest failure is current-run screenshots `51-surface-blunt-diamond.png` and `52-surface-recessed-diamond.png`: they are visually identical in the captured pixels even before captions are hidden. Several other families read only as small variations on the same central stepped motif with the same black end blocks, so the user is often relying on the caption rather than the rendered family identity. Fade and relief states do change something, but they are acting on a surface card whose family identity is not reliably self-evident.

This fails the requested “all pattern families/fades/relief” recognition gate. A user should be able to tell blunt versus recessed diamond, and broadly distinguish the ten families, from the rendered card itself.

**Smallest correction:** keep the exact-one semantic target discipline, but make each family own a visibly different motif language across the card. Blunt versus recessed diamond needs opposite readable relief, not the same outline.

### R16-C02 — the labels card is dominated by overlapping proxies and the metadata banner

The `labels` card is the weakest card in the current run. In `71-label-inset-patch.png`, `72-label-outset-vertical.png`, `73-label-target-lower.png`, `74-label-target-upper.png`, and the font/weight states `78`–`82`, the large yellow “Future OpenSCAD font” banner occupies the top of the card while black label blocks and brackets stack over one another below it. The result is that inset/outset, target placement, patch, font, and weight states are technically present but not cleanly reviewable as a human teaching surface. The only clearly readable element is often the metadata banner itself, even though the contract says OpenSCAD font should be the only truthful metadata target, not the main visual message.

This means the labels card answers the audit harness more than the user. The user can see that label-related content exists, but not reliably judge the requested relationships without reading the caption and mentally decoding overlapping blocks.

**Smallest correction:** separate the metadata badge from the active label-geometry area and reduce overlap between patch, glyph, and dimension brackets. The label card should still teach its geometry when the metadata line is ignored.

### R16-C03 — the attachment card is still too crowded to validate modes, half, angle, and size cleanly

The `attachment` card now shows more real attachment geometry than R13, but it still overlays too many semantics into one small frame. In `91-attachment-eyelet.png` through `102-attachment-opening-large.png`, multiple arches, tabs, bridge shapes, the body datum, and dimension brackets occupy the same narrow band. The mode changes are partly visible, but half-placement, angle, and opening-size changes are crowded into the same cluster and are hard to validate without the caption. `99-attachment-angle-15.png` and `100-attachment-angle-180.png` are especially weak as human-visible angle states because the rotated shape still sits inside a congested card with several competing lines.

This misses the requested attachment review goal. The user should be able to distinguish the attachment modes and then understand half, angle, and size adjustments from the geometry itself.

**Smallest correction:** give the attachment card more vertical separation or fewer simultaneous overlays so one primary attachment proxy and its one local dimension change dominate the frame.

## Passes and partial passes

| Relationship | Result | Current-run evidence |
| --- | --- | --- |
| Proportions and split position | PASS | `10`–`15` show generic, Laifen, wide-short, and high/mid/low split changes clearly. |
| Round versus polygon and 3/4/5/6/7/8/12 sides | PASS | `16`–`23` show clear section changes without relying on captions. |
| Rotation and roundness | PASS | `24`–`27` visibly change the polygon silhouette. |
| Screw versus bayonet and coarse tuning | PASS | `30`–`37` show distinct screw-wave and bayonet-lug topologies, with visible tuning changes. |
| End profiles | PASS, limited | `40`–`44` distinguish flat, chamfer, rounded-fillet, dome, and linked versus independent state, though the card is sparse. |
| Drains | PASS | `110`–`114` clearly distinguish none, bottom, top, and both, with readable hole placement and diameter/ring cues. |
| Basic/Advanced tiering | PASS | `01`–`04` show a smaller Basic state and longer Advanced state on desktop and mobile. |
| Invalid clearing | PASS | `121` and `122` clear the rendered sheet and surface the invalid-state alert. |
| Conceptual-only disclosure | PASS | `01`–`04`, `120`, and the boundary strip keep the conceptual/non-CAD message visible. |
| Mobile overall readability | PARTIAL | The full mobile page is usable, but `labels` and `attachment` become harder to decode because the same crowded cards are scaled down further in `120-mobile-complex-full.png`. |

## Additional observations

- I did **not** observe the old R13-style generic field-witness triangles or obvious value-hash color gimmicks in the current-run pixels. The failure moved from fake witness geometry to overpacked exact-one semantic cards.
- The main UI on desktop is honest about conceptual status and keeps the seven category cards visible at once. The issue is not disclosure; it is whether several cards are understandable enough to support the intended user-validation gate.

## Why this remains blocked

R16 fixed a real class of earlier problems. The remaining problem is that too many target mappings are still compressed into category cards that read like audit summaries instead of teaching views. The current run is strong enough for machine observability and partial human review, but it is still below the bar for the requested “confirm without relying on captions” recognition pass.

The smallest next action is one more visual-adapter repair that keeps the current no-hash discipline and exact-one target contract, but strengthens the three weak cards only: make all pattern families visually distinct, separate metadata from active label geometry, and give the attachment card a clearer single-feature hierarchy.
