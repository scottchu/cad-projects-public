# MC-CRIT-01 — independent compact-controls critique

## Checkpoint verdict

**NEEDS REPAIR (source gate); current-candidate visual acceptance pending.**

Reviewed frozen candidate C2 from `inputs/candidate-02.sha256`, manifest SHA-256
`68e98695f4c1328124f7a1bf1e3878b104298e1080dd835582e22ba9fe1b6c72`.
All 19 declared paths passed `shasum -a 256 -c` from repository root. C1 is
superseded and is not accepted by this critique.

### P1 — invalid finite text leaves its slider active and corrupts dependent rules

`sliderBounds()` disables a field only when its draft is nonfinite. A finite
but invalid draft such as diameter `70` therefore leaves the diameter slider
enabled. More seriously, `numberDraft()` prefers any finite current draft over
`lastValid`, so the wall interval is computed from invalid `D=70` rather than
the last valid `D=30`. `refreshFields()` then adds only the generic phrase
`using last valid value`; it neither names `D` nor limits that note to rules
which actually depend on `D`.

This fails MC-REQ-05 and the explicit invalid/dependency contract. For the
specified `D=70` witness, the literal input and Generate state may be right,
but the diameter slider must disable and the wall rule must retain the prior
numeric interval with `using last valid D`. Independent H/T rules must not
claim they used D. The repair needs validity-aware dependency resolution, not
only a different sentence.

### P1 — slider movement does not synchronize the exact numeric input

The range listener updates `raw[key]`, but `refreshFields()` never writes that
new value to the paired numeric input. Root's C2 Safari evidence after moving
diameter to its lower endpoint shows the slider at `11` while the number field
still displays `30`; the derived outside diameter is `20 mm`, proving the
model state followed the slider while the exact entry did not. This directly
fails MC-REQ-04 and creates a dangerous false parameter readout. Every slider
input must update its paired visible exact value in the same refresh, without
rewriting independently typed invalid text.

### P1 — the mobile dock is still two rows rather than one compact action row

The footer contains the status paragraph followed by `.action-row`, whose CSS
adds an 8 px top margin. The status therefore occupies a separate row above
the icons. This conflicts with the user's request for a single compact icon
action row and DESIGN's status-at-left/actions-at-right contract, and consumes
avoidable vertical space in the parameter viewport. Lay out status and the
three action slots in one row while preserving a readable live status.

### P1 — Cancel does not occupy Generate's slot

Busy state reveals `#cancel` but never hides `#generate`; it only disables
Generate. The dock consequently expands from three controls to four while a
job runs, and Cancel appears after Reset rather than in Generate's exact slot.
Use one stable first action slot whose visible control switches between
Generate and Cancel. Keep Reset and Download stationary.

### P2 — exact invalid strings are not reliably preservable with `type=number`

All exact-entry controls use `type="number"`. Browser value sanitization can
turn non-number strings into an empty value, so the stated promise that blank,
nonfinite, and invalid literal text remains visible cannot be met for every
case. A decimal text input with an appropriate input mode, plus the existing
explicit parser, would make the typed string truly authoritative. If the
product intentionally accepts only numeric browser syntax, narrow the frozen
claim rather than asserting preservation the control cannot provide.

### P2 — rule text and accessible names do not fully follow the frozen contract

Only diameter retains purpose text in its rule line; height, wall and end
thickness show only the interval despite DESIGN requiring the short purpose
text to move into each rule line. The end-thickness numeric input is named
`Top & bottom thickness`, while its slider is named `Top and bottom thickness`,
so the paired controls do not have the same accessible name. Busy Cancel is
named `Cancel generation` in both ARIA and SVG title while the frozen browser
check specifies `Cancel`. Align these strings with the contract.

### P2 — edge tooltips are likely clipped and need screenshot evidence

Tooltips are centered under each icon. Reset view and Download sit at the
right edge, while both the fixed layout and mobile preview clip overflow.
Their max-180 px tooltips can extend beyond the viewport. Current screenshots
must prove the full tooltip is visible; otherwise anchor right-edge tooltips
to the right edge. This remains a source-based risk until current C2 hover and
focus captures are supplied.

## Requirement coverage at this checkpoint

- MC-REQ-01/02: source structure supports a pinned mobile preview with only
  `.panel-scroll` scrolling, and preserves desktop canvas-left/controls-right.
  Current 390x700/390x844 and desktop captures are still required.
- MC-REQ-03: icon-only 44 px controls, local SVG, labels, titles, focus styling
  and pressed styling are present in source; Cancel slot, exact name and
  tooltip visibility fail or remain open as above.
- MC-REQ-04/05: paired sliders/rules exist, but invalid and dependent behavior
  is blocking.
- MC-REQ-06: range listeners call the edit/invalidation path and contain no
  generation call. Runtime evidence remains with the independent validator.
- MC-REQ-07: existing view, reset, generation, download and options wiring is
  retained in source; busy-slot behavior fails. Actual CAD runtime remains to
  be observed independently.
- MC-REQ-08: the frozen SCAD, schema and worker paths are present in the
  verified manifest. This critique makes no CAD, mesh, slicer, printability or
  physical-acceptance claim.

## Evidence and scope

Read project `PROJECT_STATE.md`, `NEXT_AGENT.md`, `README.md`, requirements,
experience, active BRIEF/DESIGN, implementation receipt, candidate HTML/CSS,
UI bounds/adapter/dimensions/lifecycle wiring, and the supplied phone image.
The inspected `/tmp/container-compact-validation/baseline-mobile.png` is the
previous baseline only and was not used to accept C2. Root then supplied actual
C2 Safari evidence at `/tmp/container-compact-validation/c2-mobile-top.png`
and `/tmp/container-compact-validation/c2-slider-state.txt`. It confirms the
238 px pinned preview and compact icon toolbar at 390x700, the two-row dock,
and the blocking 11-versus-30 slider/input mismatch. At screenshot scale the
3D/Cutaway pair and the two reset icons are very similar; icon comprehension
remains an actual-user acceptance question even after functional repair.
No service, generation, download, test, CAD, slicer or printer action was
performed by this critic.

Commands: `/opt/homebrew/bin/rg --files ...`; `sed`/`nl` reads; `shasum -a 256
inputs/candidate-02.sha256`; `wc -l ...`; and repository-root `shasum -a 256 -c
projects/laifen-wave-case/docs/iterations/2026-09-06-compact-controls/inputs/candidate-02.sha256`
(19/19 OK).

Changed path: this `CRITIQUE.md` only. Next action: implement the three P1
repairs, refreeze the candidate, then supply actual Safari 390x700/390x844 and
desktop captures for layout, tooltip, focus and hierarchy acceptance.

## C3 repair review

Candidate C3 manifest SHA-256
`151491f84ca8853763b023a4a478f5001c4feb368cf3554b6a099535dee33395`
contains 20 paths and passed 20/20 content checks. C3 resolves C2's slider/input
synchronization, one-row dock, Generate/Cancel slot, generic dependency label,
right-edge tooltip, ordinary exact-input type and purpose/name findings in
source. It does **not** yet pass the source gate:

### P1 — constraint-invalid ownership is still inferred from adapter blame

The new `valid(raw,key)` asks whether `adapt(raw).errors[key]` exists. That
adapter reports a coupled lid failure under one field for generation guidance;
it is not a per-field feasible-value oracle. Consequently:

- manual `H83 T3 L84` reports a lid error and leaves H's slider enabled at
  `83.1–305`, though H is the typed strict-endpoint violation;
- manual `H30 T7 L35` treats L as the invalid dependency, falls back to stale
  `L84`, and reports no T interval instead of the truthful `7.1–8` interval;
- Auto `H36 T7.5` reports a height error and leaves T's slider enabled at
  `2–8`, although current T violates the derived 20 mm lid floor.

These outcomes were reproduced with a read-only Node invocation of `adapt()`,
`sliderBounds()` and `provisionalDependencies()`. They fail MC-REQ-04/05 and
the explicit manual strict/Auto dependent-invalid cases. Per-field feasibility
and the actual edited field must determine its invalid state; adapter error
placement cannot stand in for that rule. Auto mode must also omit manual L from
the dependency set. Manual lid remains `type=number`, so the earlier exact
literal-preservation issue still applies to L after Auto is turned off.

## C4 final source review

Candidate C4 manifest SHA-256
`dd9dfcbe25d7946207d009ddb8e2ee1a499442b6d712202bed31f7fe192d0d1d`
contains 20 paths and passed 20/20 content checks. It resolves the scoped C3
invalid-ownership witnesses and changes manual lid to a literal-preserving
decimal text input. One blocking range-truth issue remains.

### P1 — an invalid axial field disables unrelated diameter and wall sliders

`feasible()` enforces every diameter, wall, height, end and lid constraint for
every candidate field. The frozen allowed-range table defines two independent
subsystems: D/W rules depend on D/W, while H/T/L rules depend on H/T/L and Auto.
With manual `H30 T7 L35` and T as the edited invalid field, C4 correctly
disables T but also reports `No allowed value with the current dimensions` for
both D and W. Auto `H36 T7.5` causes the same unrelated D/W failure. D and W
remain mechanically feasible in both cases, and DESIGN explicitly says an
empty interval disables only that slider. Field-specific feasibility must not
allow an axial error to erase truthful radial ranges.

There is a second persistence edge: dimension-invalid ownership is held in one
`editedKey`, but drain/output input overwrites it. If a coupled invalid
dimension remains and the user changes one of those selectors, its own slider
can cease to be recognized as the edited invalid field. Non-dimension controls
should not clear dimension error ownership.

Read-only reproduction used Node to print `fieldInvalid()`, `sliderBounds()`
and `provisionalDependencies()` for the frozen manual and Auto witnesses. No
candidate or test file was changed.

### C4 visual matrix

Root supplied actual Safari Responsive Design Mode captures for C4. The
390x700 preview is 238 px high and the 390x844 preview is 280 px high; each
remains unchanged between its top-scroll and bottom-scroll capture. The
single-row dock stays visible. Captures at 760x800 use the stacked layout, while
761x800, 1280x800 and 1440x900 use the preserved canvas-left/control-right
layout. Across the eight captures there is no visible page scroll, horizontal
overflow, canvas/control overlap or hidden dock. Icons, exact entries, sliders
and embedded rule lines materially reduce the space used by the supplied
phone baseline. This passes the responsive visual composition portion of
MC-REQ-01/02/03; actual-user icon comprehension remains open.

Evidence paths: `/tmp/container-compact-validation/c4-390x700-top.png`,
`c4-390x700-bottom.png`, `c4-390x844-top.png`, `c4-390x844-bottom.png`,
`c4-760x800.png`, `c4-761x800.png`, `c4-1280x800.png`, and
`c4-1440x900.png`. The captures do not establish hover/focus tooltip behavior,
busy Cancel behavior, generation, download bytes or runtime algebra.

## C4 final verdict

**REJECTED / NEEDS REDESIGN.** Responsive composition passes, and the C2/C3
repair findings are resolved, but C4 cannot be accepted while an invalid axial
field disables unrelated D/W sliders and non-dimension edits can discard the
dimension-invalid owner. MC-REQ-04/05 and the explicit `disables only that
slider` contract remain uncovered. The project reopened design after the two
implementation repair cycles; a new frozen contract/candidate must receive a
new source and visual gate.

Critic writes for this stage: this file, project `design-qa.md`, and the
authorized append-only digital observation in `docs/EXPERIENCE.md`. No
application, test, CAD, artifact, service or hosting path was changed by the
critic. No CAD, mesh, slicer, printability or physical acceptance is claimed.

## C5 revised-contract review

### Provenance and source verdict

Frozen candidate C5 manifest
`inputs/candidate-05.sha256`, SHA-256
`f51607ab4e80b2d2b6fa753d90f55f1cb64504c42c3b5919e6175d27e100e714`,
contains 23 paths and passed 23/23 content checks. The governing revision is
`RULES-REVISION.md` SHA-256
`53f9dd990507ec640f615cac30dbc466e1ecff325494886af2535c96e586a6ca`.

**Source gate: PASS.** C5 replaces event-history and mixed fallback state with
one pure `deriveDraftState(raw,lastValidDimensions)` result consumed by field
errors, form error, range rules/state, summaries, generation values and
Generate availability. Direct strings remain literal. A dimension issue pauses
all dimension sliders and labels every rule from one complete last-valid
snapshot; selector edits do not change that snapshot or issue. Coupled manual
and Auto errors have stable participant sets and one form-level message linked
from participant inputs/ranges. Valid states restore current-source intervals.
The controller accepts only enabled in-range slider input, synchronizes its
exact field, invalidates current bytes and never implicitly generates.

The critic independently invoked the pure derivation for defaults, blank D,
D70, manual H30/T7/L35, corrected T7.1, Auto H36/T7.5, and an invalid selector.
Observed default intervals are D11–69, W4–25, H46.2–305 and T2–8. Invalid
dimension states preserve the raw value, block Generate, pause all sliders and
show last-valid rules. The manual and Auto coupled messages name the correct
participants; T7.1 restores the valid current-source T7.1–8 interval. An
invalid selector blocks Generate while dimension sliders remain current and
enabled. Source inspection also confirms one-row Generate/Cancel slot, exact
entry synchronization, reset/default restoration, view controls, current-byte
download ownership and unchanged worker lifecycle integration.

No actionable P0/P1/P2 source UX issue remains against MC-DES-02. C2, C3 and
C4 remain rejected historical candidates; their findings are not approvals.

### Visual verdict

**BLOCKED pending a fresh C5 browser capture.** Root's Safari automation failed
with `CUA-10005 cgWindowNotFound`; a fresh app/window/session did not expose a
controllable provider. C5 therefore has no actual browser capture of the new
coupled form error, last-valid rule presentation, focus/error associations,
tooltips or busy Cancel slot.

C4's eight Safari captures remain useful historical layout evidence because
C4 and C5 have byte-identical `style.css`
(`a25b47f668009b1d8b15c29179b566ae5fd5018105f8c4d2ca03a3cee2c643be`).
They show the pinned 238/280 px mobile previews, one compact dock, the 760/761
breakpoint and desktop two-pane layouts without visible overflow or overlap.
The C5 HTML adds the coupled form-error element, so those C4 images cannot
accept its actual error-state layout or accessibility behavior.

Final MC-CRIT-01 result is **SOURCE PASS / VISUAL BLOCKED**. The minimum closing
evidence is one fresh C5 mobile invalid-state capture plus accessibility state,
and one current desktop/default capture; the existing C4 size matrix need not
be repeated unless the CSS changes. Actual-user icon comprehension remains a
separate acceptance step. This review does not establish generation/download
runtime, CAD, mesh, slicer, printability or physical acceptance.

Commands run by the critic: explicit Homebrew `rg` inventory/search; `sed` and
`nl` source reads; repository-root `shasum -a 256 -c` for C2 through C5;
read-only Node calls to the frozen range/state exports; and `view_image` on the
C2/C4 evidence supplied by root. Final critic-authored paths are this file,
project `design-qa.md`, and OBS-15 in `docs/EXPERIENCE.md`.
