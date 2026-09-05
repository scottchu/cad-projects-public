# CRIT-MW-01 independent MakerWorld simulator critique

**Status: HOLD — the frozen candidate passes its source-only checks, but it does
not yet provide a reliable visual intent gate.** This is a product/visual critique
only; it does not approve CAD, mesh, slicer, printability, fit, thread strength,
or physical acceptance.

## Scope and provenance

Owner: `/root/mw_sim_critic`, independent of the implementation and validation
roles. The supplied implementation candidate manifest
[`inputs/implementation-candidate.sha256`](inputs/implementation-candidate.sha256)
SHA-256 `26e5717885bfd4dcc6a473f455a405767011cca3f94a4ec1cd47ee5fda4fcb6d`
verified before and after review. The frozen design-input fingerprint
`b060787132e71d20b995624e7deced8403d3c76c61507f2287170f28d0dc29b6`
also verified against `inputs/current-baseline.sha256`.

The static page was served read-only from the candidate preview directory on
loopback port 8992 and captured with root-venv Playwright/Google Chrome. The
critic wrote only `scratch/makerworld-simulator-critique/`, this receipt, and
[`inputs/critique-evidence.sha256`](inputs/critique-evidence.sha256). No simulator
source, test, CAD, route, service, slicer, or printer state changed.

## Accepted visual evidence

| View | Evidence | Observation |
| --- | --- | --- |
| Desktop default, S=84 | `scratch/makerworld-simulator-critique/01-desktop-default.png` | The controls/readouts are legible and state the top datum, S=84, H=219, full band 135–144 and effective band 136.5–142.5. The overlapping exterior, however, renders as an alternating cyan/orange/pale band rather than one closed silhouette plus a clear joint. |
| Desktop S=50 / S=169 | `02-desktop-s50.png`, `03-desktop-s169.png` | The horizontal band moves with the requested split range and remains a mid-body band. Both boundary views preserve the same ambiguous coincident-surface rendering. |
| Desktop wave/flutes | `05-desktop-wave.png` | The selected pattern is announced by the select control, but at the default camera it reads nearly as a smooth single-colour cylinder; the visual difference is not strong enough to support a pattern-choice gate on its own. |
| Desktop exploded | `06-desktop-exploded.png` | The orange/teal pieces separate, while the seam/full/effective overlays remain at the original assembled global-Z band and float in the resulting gap. |
| Device length 250; percent 77.17 | `07-desktop-device250-percentmax.png` | The unchanged visible percent maximum produces S=201.4137 mm and the red out-of-range error. |
| Mobile default / 50% | `08-mobile-default.png`, `09-mobile-percent50.png` | The narrow responsive layout has no clipped form/readout content; 50% converts to 109.5 mm. The central band remains visually ambiguous and the canvas has no meaningful non-visual rendering alternative. |

## Findings

### C-MW-01 — high — coincident outer skins make the core joint ambiguous

`app.js` renders the lower exterior through `z_seam + P` and the upper exterior
from `z_seam`; at default both opaque patterned meshes occupy the same cylindrical
surface for 9 mm. The default and both boundary screenshots visibly show the
result as a mottled cyan/orange/pale ring. It cannot be read as a single closed
outer silhouette with two identifiable pieces, and it does not clearly distinguish
the full band from its effective sub-band.

This blocks the visual portion of **MW-REQ-01** and **MW-REQ-07**, and the visual
gate required by DESIGN “Pattern law and clipping”/“Focused validation plan”. Keep
the 9 mm overlap as axial-accounting data, but render a single chosen exterior in
the coincident interval for assembled view. Depict full and effective ranges with
two non-coincident, labelled overlays (for example, offset annuli/boundary lines)
whose labels name each range. Re-capture default and both S boundaries before
release.

### C-MW-02 — high — percentage adapter no longer maps only to allowed S after H changes

With `device_length=250`, H becomes 261 and the visible percent control retains
the default 22.83–77.17 limits. Its displayed maximum maps to
`261 * 77.17 / 100 = 201.4137 mm`, beyond the declared S maximum of 169, then
emits a red error. This is a reachable invalid state from an advertised control,
not a deliberately tested invalid input.

This fails **MW-REQ-02** and DESIGN’s parameter-contract statement that allowed
percent input maps into the S range. On every H change, derive and update both
percent controls’ min/max/value from `100*50/H` and `100*169/H`; retain S as the
canonical value and add a UI regression for the altered-H min, max and round trip.

### C-MW-03 — medium — exploded mode leaves thread/seam graphics detached from either piece

The exploded screenshot shows the pieces displaced by 7 mm in opposite directions
but the seam, full-thread and effective-thread annuli stay at assembled global Z.
The floating rings falsely imply a third object or an unconnected thread location.

This weakens the “display-only exploded spacing” promise in **MW-REQ-01** and the
required thread-band readout/visual relationship in **MW-REQ-07**. Either hide
assembled-only overlays while exploded, or move/partition them with the relevant
piece and explicitly label the assembled datum. Validate the resulting image at
default S.

### C-MW-04 — medium accessibility and pattern-choice risk

The primary visual result is a pointer-orbit WebGL canvas. The surrounding section
has an aria label, but the canvas has no role, text alternative, keyboard orbit,
or state description that conveys the rendered seam/piece relationship. The legend
also combines “Full / effective thread band” behind one swatch. This means a
non-pointer or non-visual user cannot independently make the stated topology gate,
and the pattern select’s wave/flutes choice is barely perceptible in the accepted
desktop capture.

This leaves the semantic/accessibility target in DESIGN’s focused validation plan
open and weakens **MW-REQ-06**/**MW-REQ-07** as an intent surface. Add an updated,
live textual visual-state summary (piece spans, selected pattern and separate
overlay identities), a keyboard-accessible camera reset or static orientation,
and separate legend entries. Treat this as accessibility evidence only, not a CAD
or fabrication claim.

## What did pass within this limited critique

The language consistently calls the parts upper/lower pieces rather than a cap;
the default gives a visibly substantial upper piece; the top datum and mm/% values
are readable; the 50% mobile edit produced 109.5 mm; and the caution visibly says
the page is not CAD, printable geometry, a fit proof, wall-thickness proof or
device-retention proof. The global-Z phase contract is supported by the existing
pure-math test, but the coincident render prevents this critic from calling the
seam visually intelligible.

## Commands and handoff

```sh
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r1-makerworld-simulator/inputs/implementation-candidate.sha256
node projects/laifen-wave-case/tests/test_makerworld_simulator.mjs
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 -m http.server 8992 --directory projects/laifen-wave-case/preview
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 projects/laifen-wave-case/scratch/makerworld-simulator-critique/capture.py
```

The manifest and Node test passed before and after capture. A distinct
implementation role must repair C-MW-01 through C-MW-04; then the candidate
manifest changes and independent validation/critique must rerun. Formal review
must not release the current candidate for private delivery while these visual
intent blockers remain open.
