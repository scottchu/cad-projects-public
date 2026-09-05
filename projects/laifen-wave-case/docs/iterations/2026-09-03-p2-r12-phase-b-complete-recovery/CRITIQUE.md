# CRIT-GCS-R12-01 independent visual and UX critique

**Verdict: BLOCK.** Candidate `51727da73c72db6e391f4f83014a54076dc2ffbdc5bc617f753c72a8fc1a2221` is byte-verified, and its Phase-B coverage repair is outside this critique's objection. The Phase-C visual model does not let a user recognize or validate the required product relationships. This is a browser-intent result only; it makes no CAD, OpenSCAD, STEP, export, slicer, print, drainage, fit, or physical claim.

## Provenance and method

- Owner and role: `CRIT-GCS-R12-01`, independent visual/UX critic. Candidate source and tests were read-only. This task wrote only this critique, its two manifests, and `scratch/r12-critique/`.
- `shasum -a 256 -c CANDIDATE_MANIFEST.sha256` passed every one of the 15 candidate entries. The manifest's own SHA-256 is the required candidate fingerprint above.
- I read the R12 brief/design/implementation recovery, R10 frozen recovery brief/design, current project continuity, requirements, and experience record. R10 requires recognisable visual proxies for section, closure, end, pattern/fade, readable labels/patches, drain masks, and accessories; Phase C is a descriptor-only conceptual visual, not a CAD substitute.
- I used the exact candidate through an ephemeral loopback server and inspected its current Chrome UI. The paired scripted capture used fresh Chromium at 1280x900 and 390x844, saving and then visually inspecting 42 screenshots. It covers Basic/Advanced, all three presets, round/polygon, screw/bayonet, all four ends, all ten patterns, all three fades, inset/outset labels, every attachment, all drain modes, and invalid clearing. `scratch/r12-critique/capture.json` names each state; `CRITIQUE_EVIDENCE_MANIFEST.sha256` freezes their hashes.
- Independent prescribed checks passed: `node projects/laifen-wave-case/tests/test_p2_r10_renderer.mjs`; `uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r10_browser.py`. Those checks establish descriptor serialization, runtime reachability, and transactional invalid clearing; they do not establish visual comprehension.

## P1 blockers

### CR12-P1-01 — the Basic/Advanced control gate does not disclose different groups

`01-desktop-basic-default.png` and the live accessibility tree expose Wall, Floor, screw detail fields, surface detail fields, and the other non-Basic controls while the toggle reads **Show Advanced**. After activation the button becomes **Show Basic**, but the same fields remain exposed. This breaks R10-03/R10-04's tier promise and makes the phone flow unnecessarily long before a user reaches the viewer. Conditional fields such as screw versus bayonet do react, but the tier itself is not a usable progressive gate.

**Smallest correction:** make the Basic state contain only its declared decision controls, then reveal the existing active advanced fields only after the toggle. Rerun the Basic/Advanced browser matrix at both viewports.

### CR12-P1-02 — proportions, cross-section, and closure topology collapse to one rectangle and one seam curve

The Laifen and wide-short preset screens (`04`, `05`) retain the same 220-by-290 rectangular body. OD and height change only the written Ø readout; the wide-short preset cannot be understood as wide and short. Round and rotated polygon (`06`, `07`) also share the same body outline; there is no polygon silhouette, side count, or rotation cue.

Screw and bayonet (`08`, `09`) share the same single yellow seam curve. The only mode distinction is the sentence changing from “screw” to “bayonet”; there are no thread turns/runout or bayonet lugs, capture, ramp, lock travel, or axial phase witness. A user therefore cannot validate the intended two-piece mid split, short-thread choice, or bayonet operation from the visual.

**Smallest correction:** derive the main silhouette from height/OD/section support, and draw mode-specific seam proxies: threads/runout for screw; discrete lugs, a capture/ramp path, and quarter-turn/lock annotation for bayonet. Keep both cores coaxial and make the phase relation a separate annotation rather than tilting a side view.

### CR12-P1-03 — patterns, fades, and most end families are named rather than visibly represented

All ten pattern captures (`14`–`23`) show only a small yellow sampled line across a plain rectangular sidewall plus the selected pattern's text. Smooth is a flat line; the remaining families differ only as small waveform changes at one axial stripe. Knit, diamonds, hex, flutes, helix, wave, and quilt do not read as surface families on the object. The three fade states (`24`–`26`) do not visibly fade or band the sidewall.

The end comparison cards do not serialize the derived meridian paths: flat is rectangular, while chamfer and rounded-fillet are the same oval card; dome is only slightly different. The integrated chamfer/fillet/dome end accents (`11`–`13`) are too small to explain the named profile or to compare the families at one scale. This fails R10-10 and R10-13's visual-recognition purpose even though their descriptor values can differ.

**Smallest correction:** render the existing derived surface field across the sidewall with family-specific motifs and fade weighting, then render each actual end path in the comparison strip at one shared scale. The visual adapter must consume the field/envelope/path data rather than the selected name alone.

### CR12-P1-04 — attachments and the label patch use inert or indistinguishable proxies

Each attachment selection (`29`–`33`) uses the same arch-and-hole outline at the same location; only the small text name changes. It is not possible to distinguish an eyelet, captured loop, separate clip link, keyring tab, and bridge handle by their shape or attachment semantics. The total-envelope number changes but the viewer offers no corresponding visible envelope comparison.

The label-patch pair is byte-identical: `40-label-patch-on.png` and `41-label-patch-off.png` both hash to `50b26c0d1865b6f697175e9e96b24611d9e7934730eb7fe149e32b84e6ff84ad`. The text itself is very small and the dark rounded rectangle appears whether patch is on or off, so the selected patch cannot be evaluated. Inset/outset is also not visibly directional in `27`/`28`.

**Smallest correction:** serialize each attachment's existing primitive geometry as a distinct silhouette and give `separate_visual` a visibly detached presentation. Make patch state, inset/outset direction, and target location visible through an actual patch/mask and relief cue; retain outward-readable text at a reviewable size.

### CR12-P1-05 — the required conceptual and no-CAD/OpenSCAD boundary is incomplete

The header correctly says “Dimensionally proportional visual. Pixels are fit-to-view, not calibrated.” That limits scale, but it does not say the preview is conceptual/visual-only or explicitly state that it is not CAD or OpenSCAD. The OpenSCAD family appears as a field only when a label is active and as an SVG title, neither of which supplies a persistent honest product boundary. This fails the requested disclosure audit and risks a user treating this as an exportable CAD view.

**Smallest correction:** place a persistent, plainly worded boundary adjacent to the viewer: “Conceptual descriptor preview only — not CAD, OpenSCAD, or a printable/exportable model.” Keep the existing calibrated-pixel limitation separately.

## Behaviors confirmed by this critique

| Relationship | Result | Evidence |
| --- | --- | --- |
| Invalid active value clears stale visual output and exposes error | PASS | `42-desktop-invalid-state-clears-viewer.png`; viewer/detail/comparison/readouts are absent and the OD field has a linked error. |
| Conceptual pixel scale is disclosed | PASS, limited | Header and SVG state “dimensionally proportional” / “fit-to-view, not calibrated.” |
| Drains are present as masks for bottom/top/both | PASS, limited | `34`–`37` place differing hole sets and report the combined count. End assignment is still less legible than explicit top/bottom labels. |
| Phone surface has no visible horizontal escape | PASS, limited | `38-phone-bayonet-quilt-label-attachment-drains.png` shows a scrollable visual card. It inherits the recognition failures above and the overlong tier disclosure. |

## Next action

Do not advance this candidate to formal review or delivery. Open a new frozen visual-adapter repair after the R12 recovery ceiling is reconciled. The repair should use a small user-confirmable 2D/preview gate that asks separately whether the user can recognize: wide-short versus tall proportions; round versus rotated polygon; screw versus bayonet action at the mid seam; the four end profiles; pattern/fade identity; label patch/relief; five attachments; and the persistent conceptual/non-CAD boundary. Regenerate a candidate fingerprint and rerun independent visual critique and validation after that gate passes.
