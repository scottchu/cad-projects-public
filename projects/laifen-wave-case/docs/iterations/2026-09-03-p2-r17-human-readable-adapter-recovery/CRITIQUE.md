# CRIT-GCS-R17-01 independent visual and UX critique

**Verdict: BLOCK.** Candidate manifest fingerprint `5fe1228ca56d11f6e0d6d30c2c7e832118dcb3b67293cd79fbc475dc2da9a9c6` verifies, and this run captured fresh desktop and mobile evidence from the exact R17 preview. R17 preserves the honest conceptual disclosure, the no-hash/no-witness direction, and several readable preserved categories. It still misses the requested no-caption teaching gate because the `labels` and `attachment` cards remain crowded, and the `surface` card still leaves at least one required family pair too close for confident recognition without text. This remains conceptual browser-preview evidence only; it grants no CAD, OpenSCAD, STEP/export, slicer, fit, printability, or physical acceptance.

## Provenance and method

- Owner and role: `CRIT-GCS-R17-01`, independent visual/UX critic. Candidate source and tests remained read-only. This task wrote only this critique, `CRITIQUE_EVIDENCE_MANIFEST.sha256`, and `scratch/r17-critique/**`.
- Candidate verification command: `/usr/bin/shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r17-human-readable-adapter-recovery/CANDIDATE_MANIFEST.sha256`. All listed candidate entries passed, and the manifest SHA-256 matches the required fingerprint above.
- I read the frozen R17 brief, design, handoff, and implementation receipt. The findings below use only current-run screenshot evidence.
- Fresh evidence command: `uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r17-critique/capture.py`.
- The capture run served the exact preview from an ephemeral loopback server and saved 47 current-run records: desktop/mobile full UI, invalid-clearing states, focused category-card states, and contact sheets for main UI, surface, labels, attachment, preserved categories, and the teaching strip.

## P1 blockers

### R17-C01 — the labels card is still crowded, and the metadata banner is still inside the active card

R17 was supposed to separate the OpenSCAD font metadata from the active label geometry. In the current-run label states `18` through `27`, the large “Future OpenSCAD font” banner still occupies the top of the same card that is supposed to teach label mode, font, weight, orientation, target, axial position, and patch. The active label geometry remains stacked under and across that banner, with multiple nested rectangles, brackets, and glyphs overlapping in the same small area.

This is easiest to see in `18-label-inset-patch.png`, `19-label-outset-vertical.png`, `20-label-target-lower.png`, `21-label-target-upper.png`, and the font/weight states `22`–`25`. The user can tell that label-related content exists, but not cleanly validate the intended relationships without reading the caption and mentally unpacking the overlap. That fails `R17-10` and `R17-11`.

**Smallest correction:** move the metadata badge fully out of the live label card or into a separate noncompeting strip, then give label geometry one dominant local teaching area with only one active dimension/annotation at a time.

### R17-C02 — the attachment card still compresses too many meanings into one frame

The attachment card remains visually dense in the current run. In `28-attachment-eyelet.png` through `36-attachment-opening-large.png`, the body datum, body pocket, attachment silhouette, half-placement cues, angle cues, and opening-size dimensions all crowd the same horizontal band. The mode changes are partly visible, but half, angle, and size changes still compete with each other instead of being taught clearly.

This is most obvious in `33-attachment-angle-15.png` and `34-attachment-angle-180.png`, where the nominal angle change is present but embedded in an already busy attachment cluster, and in `35-attachment-opening-small.png` versus `36-attachment-opening-large.png`, where the dimensional difference is there but not dominant enough for a clean no-caption read.

**Smallest correction:** keep one dominant attachment proxy per state and separate the half/angle/size teaching into local subareas or isolated state cards so the changed relationship dominates the frame.

### R17-C03 — the surface card improved, but blunt versus recessed diamond is still too close

The surface card is better than R16. `knit` and `wave_flutes` are now visibly different, and `shallow_helix` is distinct from the denser lattice states. But `10-surface-blunt.png` and `11-surface-recessed.png` remain too similar for a reliable no-caption recognition gate. Both still read as the same broad diamond-and-strut field on first glance, with only subtle local differences in line placement and crossing. That is weaker than the brief’s requirement to keep surface families human-readable without captions.

The teaching strip helps show blunt versus helix (`48` and `49`), but it does not resolve the main surface card’s blunt-versus-recessed distinction. The asked review gate is about the teaching cards and main UI, not only the extra strip.

**Smallest correction:** give recessed diamond an unmistakably opposite relief/read pattern from blunt diamond so the pair separates at a glance in the main surface card, not only in a supplemental explainer.

## Passes and preserved behavior

| Relationship | Result | Current-run evidence |
| --- | --- | --- |
| Honest conceptual-only disclosure | PASS | `01`–`04` and `50-mobile-complex-full.png` keep the conceptual/non-CAD message visible and not misleading. |
| No generic witness/hash gimmick visible | PASS | Current-run cards do not show the old generic witness triangles or obvious hash-colored badges. |
| Round/polygon and polygon 3/12, roundness, rotation | PASS | `41`–`44` show readable section differences and a visible rotation arc/datum. |
| Split preservation | PASS | `45-container-split-middle.png` plus the main UI preserve the middle-split reading. |
| Screw versus bayonet and tuning preservation | PASS | `39-closure-screw.png` and `40-closure-bayonet.png` remain clearly distinct. |
| End profile preservation | PASS | `46-ends-flat.png` and `47-ends-dome.png` keep flat and dome states readable, with nonzero default geometry. |
| Drains top versus bottom | PASS | `37-drain-bottom.png` and `38-drain-top.png` are visibly distinct by face placement and hole location. |
| Invalid clearing | PASS | `51` and `52` clear the rendered sheet and surface the invalid-state alert. |
| Mobile overflow | PASS | The current-run mobile full pages remain within the page width; no page-level horizontal overflow was visible. |

## Additional observations

- The new teaching strip is useful as a secondary explainer, especially for helix versus blunt and for separating metadata from a standalone example. But the main criterion here is whether the active cards themselves are understandable without relying on captions, and the weakest cards still miss that bar.
- I did not observe zero-area “missing target” behavior in the preserved categories from current-run screenshots. The critique blocker is clarity, not disappearance.

## Why this remains blocked

R17 preserved the honest parts of R16 and repaired some real technical issues. The remaining failure is still human teaching quality. The `labels` card and `attachment` card read as dense audit composites rather than clean relationship explainers, and the `surface` card still leaves at least one required pair too close for confident no-caption recognition.

The smallest next action is one more bounded clarity repair that keeps the current source-ban and exact-one target discipline, but focuses only on the three weak teaching surfaces: fully separate label metadata from label geometry, simplify attachment-card hierarchy so one changed relationship dominates, and make blunt versus recessed diamond unmistakably different in the main surface card.
