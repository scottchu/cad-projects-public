# VFR-03 pattern gate validation

**Validator:** `/root/openscad_pattern_gate_validator`  
**Candidate fingerprint:** `38e3d9efb6ecd093cc9f058443a8477097bdf9d3e4471e6fea14dbb0b8fb89f3`  
**Result:** **PASS after repair cycle 2** (cycle 1 failed; see blocking finding below)

## Evidence

The candidate manifest is byte exact. `shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/PATTERN_GATE_CANDIDATE.sha256` returned `OK` for `app.js`, `styles.css`, the frozen input manifest, and `index.html`; hashing the candidate manifest itself returned the declared fingerprint. `node --check preview/openscad-pattern-gate/app.js` exited 0.

The local browser page rendered at desktop and mobile sizes. It contains a single obvious A/B relationship control and the display-only seam highlight. A selected state shows the current OpenSCAD facts (`N34`, crest-derived, 2 mm body blank, 11 mm cap blank, 13 mm band); B selected state shows preserved R7 facts (`N33`, valley-derived, `0.18` crest plateau, shared phase). The B state rendered 120 SVG paths and retained the CAP, BODY, and shared seam labels. The browser DOM reports the corrected region mapping: cap fill `#e9dcf4` at `y=58`, body fill `#d7e8e7` at `y=258`.

The exact benchmark question is present verbatim:

> Should the OpenSCAD recovery use relationship B: two visibly separate pieces, N33 derived at the valley radius, the R7 0.18 crest plateau, and shared-phase diamonds continuing to both sides of the seam without the current 2 mm/11 mm smooth collar?

The external-request scan found only the required inline SVG namespace (`http://www.w3.org/2000/svg`); there are no external images, canvases, fetch calls, or remote assets.

## Blocking finding

At the desktop viewport the strip visibly escapes its card and page layout. `svg` computes to `overflow: visible`, while the pattern generator deliberately creates paths from one cell before the left edge through one cell after the right edge. The rendered document width was `1521px` against a `720px` SVG viewBox and an approximately `880px` content card. Diamonds extend into the page margins and surrounding card content, with labels and the smooth A blank region visually overlapping the pattern. This fails the task's desktop readability/structure gate even though the narrow mobile viewport did not expose horizontal document overflow (`390px` scroll width at a `390px` viewport).

The candidate therefore cannot be accepted as a reviewable mobile-first **and desktop** intent gate. The smallest repair is to clip the explanatory pattern to the strip/card bounds (or otherwise constrain the SVG overflow) while preserving the current deterministic phase math, labels, A/B facts, and exact question. Re-run the desktop screenshot and the checks above after that repair. User pass/fail remains open; this validation does not approve VFR-04.

## Commands actually run

```sh
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/PATTERN_GATE_CANDIDATE.sha256
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/PATTERN_GATE_CANDIDATE.sha256
node --check preview/openscad-pattern-gate/app.js
/opt/homebrew/bin/rg -n 'https?://|<img|<canvas|fetch\\(' preview/openscad-pattern-gate
```

Browser evidence was collected from the local static server at `http://127.0.0.1:8765/`, including A/B interaction, DOM facts, 1521px desktop layout measurement, and a 390x844 mobile emulation check.

## Repair cycle 2 — validation of clipped strip

The repaired candidate fingerprint is `6bfa2c2225e0abcf9fdb4f841f759196630a7f5daf544731ef57306c99732e8e`. The candidate manifest check returned `OK` for all four entries, and hashing the manifest returned that exact fingerprint. `node --check preview/openscad-pattern-gate/app.js` exited 0. The only candidate source change is `styles.css`, changing the SVG overflow behavior to `hidden`; `app.js` and `index.html` remain byte-identical to the prior candidate.

At desktop, the SVG computed `overflow: hidden`; its rendered width was `834.8px` inside the `880px` diagram card, and the document had no horizontal overflow (`scrollWidth == innerWidth`). The screenshot shows the generated diamonds clipped to the strip, with the surrounding facts and pass/fail card readable. At mobile emulation (`390x844`), `scrollWidth` remained `390px`, the controls switched to a column layout, and the facts switched to one column. B remained selectable with `[false, true]`, the exact N33/valley/0.18/shared-phase summary, 120 paths, and CAP/BODY/seam labels.

**Repair cycle 2 result: PASS.** The prior desktop readability blocker is resolved. The VFR-03 implementation now satisfies its deterministic manifest, syntax, no-external-request, A/B, numeric-fact, phase, component-mapping, exact-question, and mobile/desktop readability checks. User pass/fail remains open, and this gate still does not approve VFR-04.
