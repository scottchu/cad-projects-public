# CRIT-GCS-R13-01 independent visual and UX critique

**Verdict: BLOCK.** Candidate manifest fingerprint `9f79d2ca92c04a159ff8a79c5279dfa00fe9d0b5bb2c6f16d639be26bfc9c468` verifies, and this run captured fresh desktop and mobile evidence from the exact R13 preview. The sheet is materially better than R12: proportions, split position, section families, closure mode, drain-face assignment, Basic/Advanced gating, invalid clearing, and the conceptual-only disclosure are now visible. It still fails the user-facing recognition goal because too much of the claimed observability is carried by generic top-right field-witness triangles and tiny abstract glyphs instead of readable part proxies. This remains a conceptual browser-intent result only; it makes no CAD, OpenSCAD, STEP/export, slicer, fit, printability, or physical claim.

## Provenance and method

- Owner and role: `CRIT-GCS-R13-01`, independent visual/UX critic. Candidate source and tests stayed read-only. This task wrote only this critique, `CRITIQUE_EVIDENCE_MANIFEST.sha256`, and `scratch/r13-critique/**`.
- `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r13-renderer-fidelity-recovery/CANDIDATE_MANIFEST.sha256` passed for all nine candidate entries. The manifest's own SHA-256 is the required candidate fingerprint above.
- I read the frozen R13 brief, design, handoff, and implementation receipt, plus the current project continuity files and the prior blocked R12 critique/validation only as comparison context. The visual findings below use current-run evidence only.
- Fresh capture run: `uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r13-critique/capture.py`. It served the exact preview from an ephemeral loopback server and saved 72 current-run records: desktop and mobile tier states, preset/split sheets, section families, closure families, end families, all ten patterns, fades, relief modes, labels, attachments, drains, and invalid clearing.
- The accepted evidence is frozen in `projects/laifen-wave-case/scratch/r13-critique/capture.json`, the underlying screenshots in `projects/laifen-wave-case/scratch/r13-critique/screenshots/`, and the category contact sheets in `projects/laifen-wave-case/scratch/r13-critique/sheets/`.

## P1 blockers

### R13-C01 — generic field-witness triangles are doing too much of the teaching

The top-right witness triangles appear on almost every surface and often carry the clearest difference in the frame, while the actual part proxy stays small, abstract, or unchanged in emphasis. This is easiest to see in the preset and split captures (`10`–`12`, `130`–`132`), the closure cards (`40`–`43`), the end cards (`50`–`54`), the label cards (`91`–`95`), and the attachment cards (`100`–`109`): the triangles loudly confirm that a field changed, but they do not explain the relationship the user is meant to validate. On mobile (`140-mobile-complex-state.png`) that problem gets worse because the witness labels shrink to near-illegibility while still adding visual noise and vertical length.

This matters because the contract is not “some rendered bytes changed.” The contract is that the user can recognize the fixed topology and the adjustable relationships. A generic badge that changes color, width, or slope is evidence for a hash oracle; it is not a semantic proxy for a closure, end profile, patch margin, or attachment dimension.

**Smallest correction:** keep machine-readable field targets, but demote the witness triangles out of the main teaching surface and make the semantic geometry or labeled proxy carry the difference. If a parameter needs an annotation, the annotation should explain the actual local feature it changes.

### R13-C02 — pattern families are still mostly a uniform grid, not recognizable named surfaces

The surface map now responds to parameters, fades, and relief. That is real progress. But the ten family captures (`60`–`69`) still read mostly as the same rectangular grid of aqua cells with slight spacing or sizing changes. The names `smooth`, `blunt_diamond`, `recessed_diamond`, `rugged_hex`, `shallow_helix`, and `quilted_diamond` are not visually self-evident from the cells alone; the selected family text and witness triangles do too much of the disambiguation. The fade states (`70`–`74`) and relief section (`80`–`82`) are understandable, but they are acting on a pattern sheet whose family identity is still weak.

This misses the stated goal for “all pattern families/fades/relief.” A user should be able to tell that they are looking at different families before reading the caption. Here the family identity is often only inferable after reading the caption.

**Smallest correction:** render each family with a visibly different motif silhouette or stroke language across the same unwrapped field area, then apply fade and relief to that motif. The family should survive if the text caption and witness badges are hidden.

### R13-C03 — attachment semantics remain tiny icon snippets instead of reviewable attachment proxies

The five attachment modes are now distinct in byte terms, but the visible treatment is still too small and too detached from the container to teach the intended semantics. In `100`–`105`, each mode is a tiny pink glyph in a large empty card, and the per-field witness triangles dominate the rest of the frame. The placement states (`106`, `107`) show upper versus lower attachment on the main elevation, but the overlaid title text collides with the body drawing and the actual mounted feature remains tiny. The angle states (`108`, `109`) barely differ visually because the section card still centers the body while the attachment cue is reduced to a small label-level signal.

This means the user can tell that “some attachment mode was selected,” but not reliably validate distinct attachment semantics such as eyelet versus captured loop versus clip link versus bridge handle, or how angle and half placement actually affect the mounted relationship.

**Smallest correction:** scale the attachment proxy up, anchor it to a clear body datum, and give each mode an unmistakable silhouette plus one local annotation for opening, bridge, hole, or stand-off only where that dimension matters.

## Passes and partial passes

| Relationship | Result | Current-run evidence |
| --- | --- | --- |
| Preset proportions and split location | PASS | `10`–`12`, `130`–`132` show tall/slender, narrow/tall, and wide/short bodies plus readable seam movement. |
| Round and polygon section families; side count, roundness, rotation | PASS | `20`–`31` show clear circle, 3/4/5/6/7/8/12-sided silhouettes and visible roundness/rotation change. |
| Screw versus bayonet mode and tuned closure parameters | PASS, noisy | `40`–`43` show thread-like loops for screw and discrete lugs/lock arc for bayonet, but witness badges still compete for attention. |
| End profile linking and independent top/bottom state | PARTIAL | `50`–`54` show flat, chamfer, rounded-fillet, dome, and linked/unlinked state, but the actual end curves are very small relative to the canvas. |
| Fade direction and relief placement | PASS | `70`–`74`, `80`–`82` visibly distinguish bottom/top/center fade and inset/outset/balanced wall treatment. |
| Label inset/outset, patch, orientation, target placement, and future OpenSCAD disclosure | PASS, noisy | `91`–`95` show patch presence, vertical orientation, lower/upper placement, and explicit future-font disclosure. |
| Drain ends, top/bottom/both/none, and linked-versus-independent records | PASS | `120`–`123` clearly distinguish top and bottom face assignments with labeled faces and visible hole counts. |
| Basic/Advanced tiering | PASS | `01`–`04` show a smaller Basic entry state and the longer Advanced state on desktop and mobile. |
| Invalid active input clearing | PASS | `141` and `142` clear the sheet and expose the invalid-state alert. |
| Conceptual-only boundary | PASS | `01`–`04` and `140` keep “Conceptual descriptor preview only — not CAD, OpenSCAD, or a printable/exportable model.” adjacent to the sheet. |

## Why this remains blocked

R13 solved the outright “everything looks the same rectangle” failure from R12. The remaining problem is subtler but still material: the sheet now proves many differences to a test harness, yet several of the hardest user-facing families still read as abstract badges plus tiny proxy fragments. That is enough for a technical observability demo. It is not enough for the promised recognition sheet that is supposed to teach the relationships before the user validates them.

The candidate should not advance to formal PASS. The smallest next action is one more visual-adapter repair focused on teaching clarity, not broader feature work: demote the generic witness triangles, strengthen pattern-family motifs, and scale the attachment and end-profile proxies so the relationship remains understandable without reading captions or target labels.
