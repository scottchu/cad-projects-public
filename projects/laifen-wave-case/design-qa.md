# Desktop customizer design QA — CC-CRIT-01

final result: passed

Scope: UI composition, clarity and reviewed interaction states. No remaining actionable P0/P1/P2 visual issue. This is not CAD, manifold-export, slicer or physical-print acceptance.

## Comparison target and provenance

Independent owner `/root/desktop_critic`; source/implementation are read-only to this role. Candidate C2 manifest `docs/iterations/2026-09-05-desktop-customizer/inputs/candidate-02.sha256`, SHA-256 `b57642a532d834fddeb56c938496af44a03d3635e4a748ad46ada0cf86df609c`; all 16 entries verified.

Source visual truth: `docs/iterations/2026-09-05-desktop-customizer/inputs/selected-desktop.png`, SHA-256 `f4a915c98ad96009436e170d7b65521d32c4735f8887f51d11c1b36172092267`. Frozen DESIGN governs intentional mechanics/layout differences and visible Drain holes.

Implementation screenshot: `/tmp/container-desktop-validation/c2-default-cutaway.png`. Root captured the real local browser after actual default STL compilation; this critic did not own the browser. Source and implementation both 1487×1058 pixels, implementation CSS viewport 1487×1058 and DPR 1 as reported from DOM. No density resampling or browser-chrome cropping needed. State matches: default 30/213/4.5/3, assembled Cutaway, Inside height focused, successful current generation and Download enabled.

Opened source and implementation together in one `functions.exec` call using two `view_image` results. This is combined full-view evidence, not a memory-only comparison. Input labels, helper text, units, focus, status and footer were all readable in the full-resolution view; a separate crop is unnecessary for this initial state.

## Findings and required fidelity surfaces

No actionable P0/P1/P2 visual mismatch found in the initial matched desktop state.

- **Fonts/typography:** consistent system sans, modest label weight, readable helpers and clear numeric entries. The implementation scales labels and buttons down from the raster mock while retaining hierarchy and legibility in the specified compact sidebar. No broken wrapping or truncation.
- **Spacing/layout:** canvas dominates left; consistent four field rows on right; no introductory heading. Visible Drain holes is intentional amended scope. The 380 px sidebar is within DESIGN's 360–400 px contract; mock's approximately 480 px sidebar is not a required fixed width. Actions remain grouped in a distinct bottom footer. Borders and restrained radii follow the quiet reference.
- **Colors/tokens:** pale canvas and white settings, dark text, blue focus/active/Generate, outlined Download and green current state. No decorative colors or unrelated card system introduced. Additional captures show readable red inline error, blue keyboard focus, muted disabled controls and amber previous-generation notice.
- **Image quality:** actual compiled tall screw geometry is visibly slender, with a deep cap and drilled floor; these differ intentionally from the idealized raster. Real clipping exposes interior and height arrow without fabricating section faces or threads. The seam is less visually prominent than the mock, but exists and remains inspectable; lighting polish is P3. No image substitution is appropriate for an operative CAD canvas.
- **Copy/content:** direct everyday measurement labels, millimetres, explicit body/lid differences, visible Drain holes, meaningful Generate/Reset dimensions/Download STL and separate Reset view. Derived external dimensions remain results rather than competing inputs. Compiler details are collapsed. No local-development subtitle or implementation narrative dominates the workspace.

## Comparison history

C1 was blocked before visual certification. Its frozen manifest contained one stale test hash; independent source critique found diameter/wall anchors below geometry for a valid long-lid case and a floor-thickness arrow inside a default drain. Validator/root additionally found P0 native-timer receiver binding preventing Generate.

C2 repairs use a floor-to-seam midpoint, an undrilled radial interval for end thickness, and wrapped global timers. Full frozen manifest now verifies. The root's C2 real compiled default screenshot supplies post-repair visible evidence that Generate succeeds and the expected default Cutaway appears. Repaired end/wall edge anchors have source evidence and validator's independent 1,881 accepted-combination probe. The reviewed stale capture shows the repaired end annotation at the floor edge rather than inside a ring hole.

## Additional rendered evidence and completed checklist

All following images are under `/tmp/container-desktop-validation/`, captured by root as browser tool operator following the independent validator's checklist, then opened by this critic. They are temporary review evidence, not committed release images. Desktop/mobile captures use DPR 1; screenshots match their CSS viewport. They are additional states without equivalent mock states, so no false pixel-diff claim is made.

- `c2-desktop1280.png`, `c2-stale.png`, `c2-busy.png` — 1280×800. Four inputs, Drain holes and action footer remain visible. Generate/Reset/Cancel fit while busy. Draft 4 mm ends retain a clearly marked previous 3 mm generated preview and disabled Download.
- `c2-edited-cutaway.png` — 1440×900. Actual D39/H60/W4/T4 assembled model, correct generated 60 mm label, inspectable cavity, cap/thread band and drilled floor. All main inputs/actions fit.
- `c2-cancel.png`, `c2-print-layout.png` — 1440×900. Clear cancelled/stale state versus current Print layout result; irrelevant whole-container dimension overlay suppressed for separate output pieces. Expanded options scroll locally above the persistent footer.
- `c2-invalid.png`, `c2-keyboard.png` — 1440×900. Blank diameter gets a readable inline error; Generate/Download are disabled; Tab advances to Inside height with visible focus. Root additionally checked `aria-invalid=true` and semantic field association.
- `c2-mobile.png`, `c2-mobile-ready.png` — 390×844. Stacked viewer/controls, readable fields, visible ready or invalid status and bottom action footer; normal vertical scrolling exposes remaining fields without horizontal overflow. Root measured document width 390, height 1283 and Download bottom 830. Valid capture shows real default mesh and its dimension. Mobile has no supplied visual target, so acceptance is usability fallback rather than desktop mock fidelity.

Full-resolution images made the relevant small text and controls readable; no separate focused crops were needed. No image was recreated, retouched or substituted.

Primary interaction evidence is recorded in iteration `VALIDATION.md`: real default/edited/body/lid/print-layout compilation and download; viewing-mode/reset-view byte parity; cancellation, editing during work, reset during work, inline validation and keyboard progression. This critic reviewed screenshots/source and that independent receipt rather than claiming ownership of the browser sequence. Final clean reload since `2026-09-05T23:59:28.249Z` reached current default/Download enabled; `/tmp/container-desktop-validation/c2-final-errors.json` records `errors: []`, opened by this critic.

Artifact caveat remains separate: edited assembled STL contains four near-zero-area seam faces and four nonmanifold edges; the validator reports body, lid and Print layout watertight. The UI preserves exact generated bytes. Do not call the edited assembled artifact manifold or print-ready; source mechanics were intentionally unchanged. The unsupported 3 mm wall example also remains a disclosed mechanics limitation.

No implementation correction remains from this visual review. Final C2 source manifest reverified with all 16 entries OK; future candidate changes require the affected gate to be rerun.

## Follow-up polish

P3: move the nominal inside-height line off the central drain axis to a solid floor location if it improves teaching clarity. P3: subtle lighting/angle improvement could make the real seam more legible without fabricating section caps or altering geometry. Neither warrants a new feature or blocks the current core desktop composition.

# Compact controls design QA — MC-CRIT-01 C4

final result: rejected; responsive composition passed, truthful invalid-rule
behavior failed

Frozen C4 candidate manifest
`docs/iterations/2026-09-06-compact-controls/inputs/candidate-04.sha256`,
SHA-256 `dd9dfcbe25d7946207d009ddb8e2ee1a499442b6d712202bed31f7fe192d0d1d`,
passed all 20 declared path checks. The independent critic reviewed source,
the user's supplied phone image, and eight actual Safari responsive captures.

The visual matrix passes. At 390x700 and 390x844 the canvas remains pinned at
238 px and 280 px while the parameter rail scrolls from top to bottom; the
single compact icon dock remains visible. Width 760 stays stacked, and widths
761, 1280 and 1440 preserve the desktop canvas-left/control-right layout.
There is no visible overlap, horizontal overflow or hidden dock. The icon
toolbar, sliders, exact entries and embedded rule lines use substantially less
space than the reported baseline.

C4 is rejected because its range oracle enforces all constraint groups for
every field. An invalid manual or Auto axial field can disable the unrelated
diameter and wall sliders with `No allowed value`, contrary to the field-wise
allowed-range table and the requirement to disable only the affected slider.
Changing Drain holes or Export shape can also replace the remembered edited
dimension and re-enable a still-invalid coupled slider. Exact reproduction and
full provenance are in the active iteration `CRITIQUE.md`.

This is a digital UI finding. It does not change or assess CAD geometry,
generated mesh, slicer readiness, printability or physical acceptance. The
design contract has been reopened; later acceptance requires a newly frozen
candidate and renewed source/visual evidence.

# Compact controls design QA — MC-CRIT-01 C5

final result: source passed; final visual acceptance blocked pending browser

C5 manifest
`docs/iterations/2026-09-06-compact-controls/inputs/candidate-05.sha256`,
SHA-256 `f51607ab4e80b2d2b6fa753d90f55f1cb64504c42c3b5919e6175d27e100e714`,
passed all 23 declared path checks. The revised draft-state contract is
`RULES-REVISION.md` SHA-256
`53f9dd990507ec640f615cac30dbc466e1ecff325494886af2535c96e586a6ca`.

Independent source review passes. One pure derivation now owns direct and
coupled errors, all-slider pause, whole-snapshot last-valid rules, summaries,
generation values and Generate state. The critic independently reproduced the
default bounds, blank/out-of-range retention, manual and Auto coupled states,
T7.1 recovery, and selector-only invalid state. The previously blocking mixed
fallback and unrelated-range behavior is gone. No actionable P0/P1/P2 source
UX finding remains against the revised contract.

The responsive layout has strong but historical visual evidence: C4 and C5
share byte-identical CSS, and eight C4 Safari captures passed pinned 390x700
and 390x844 canvas scrolling, the 760/761 breakpoint, desktop two panes, compact
icon dock, and visible overflow/overlap inspection. C5 adds a coupled form-error
element that those captures do not show.

Fresh C5 visual acceptance is blocked because Safari automation returned
`CUA-10005 cgWindowNotFound` and exposed no controllable provider after fresh
window/session attempts. Do not claim the new invalid-state layout, tooltip,
focus, ARIA presentation or busy Cancel state visually accepted. Close this
gate with a fresh C5 mobile invalid-state screenshot/accessibility state and a
current desktop/default capture. This UI review carries no CAD, mesh, slicer,
printability or physical acceptance claim.
