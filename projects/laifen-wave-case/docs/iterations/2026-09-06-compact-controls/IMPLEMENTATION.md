# MC-IMP-01 — compact controls implementation

Baseline: `5acaede2114614882ed92cd362b3bc120deed5d7`. Frozen design input:
`DESIGN.md` SHA-256 `fd385da0617aa88db674eba18d684e4fca403318a5cda859d4834e06cc636d2c`;
the corresponding `inputs/design.sha256` is
`8899be6114a32a418cf6d2bd0d0766b15bfc77c78631d5ac19a4a8a1a425f8a2`.

Implemented the compact responsive UI only. At <=760px the workspace is a
fixed `100dvh` two-row grid with a pinned preview row; `.panel-scroll` is the
only parameter scroller and the one-line action dock remains in the control
row. Desktop preserves the canvas-left/control-rail layout. View, generation,
reset, cancel, and download actions are 44px inline-SVG controls with labels,
SVG titles, tooltips, keyboard focus and pressed/disabled state.

Each editable dimension now has a direct numeric input, 0.1mm range control,
and live allowed-range rule. `src/bounds.mjs` evaluates the frozen D/W and
H/T/lid constraints with other dimensions held fixed. Invalid typed values
remain raw and disable their own slider and Generate; dependent sliders use a
last valid dependency where available. Range input only uses the existing edit
invalidation path and never calls generation. Auto/manual lid, drain/export
options, reset, viewer mode, existing worker epochs and exact download logic
remain in place. Schema, worker, dependency lock, and SCAD were untouched.

Focused verification run (no build, because `dist` is the live-preview input):

`npm exec --workspace laifen-wave-case -- node --test tests/node/desktop-customizer.test.mjs`

Repair cycle 1 addressed C2 critique/validation findings: finite but invalid
typed values now disable their own slider, related bounds resolve from the
specific last valid dependency, range events synchronize the paired text input
and viewer dimension selection, and edits during an active generation always
invalidate that job. The dock is one status-plus-icons row; Cancel replaces
Generate in its first slot. Exact-entry fields are decimal text inputs so raw
invalid text is not browser-sanitized. Rule lines include purpose text and
right-edge tooltips anchor inward.

Result: 18 passing, 0 failing. The added oracle tests cover default bounds
(including D 11–69 at W 4.5), D/W coupling, strict lid limits, the 46.2mm auto
height witness, valid slider snapshots, out-of-range last-valid dependency
behavior, and fake-DOM range synchronization. Browser-size, keyboard,
tooltip, and actual WASM generation checks remain for independent validation.

Repair cycle 2 removes adapter error placement from per-field control validity.
The edited field is checked against its own equations; only its related rules
substitute the last valid field and name that substitution. Manual lid now also
uses a decimal text input. Focused regressions cover manual H/T/lid strict
endpoints, Auto derived-lid constraints, and recovery from an invalid edit.
