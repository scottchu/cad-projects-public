# MC-DES-02 — coherent draft-state revision

Input errors must have one owner: a pure draft-state derivation consumed by the
entire UI. Remove `editedKey`, per-field last-valid values, adapter-owned display
errors, and mixed current/fallback range calculation.

## Pure state contract

Maintain `raw` and `lastValidDimensions`. `raw` contains the exact strings for
D/H/W/T/L plus Auto, drains, and output. `lastValidDimensions` is one complete
dimension snapshot that passed all active equations; it is never assembled from
independently saved fields.

```text
deriveDraftState(raw, lastValidDimensions) -> {
  issues,                 // canonical direct and coupled validation issues
  fieldErrors, formError, // display/accessibility projections of issues
  sliders[key],           // {disabled,min,max,source,rule}
  summary,
  generationValues|null,
  canGenerate,
  nextLastValidDimensions
}
```

This function parses active dimension strings, checks static bounds and all D/W
and H/T/L equations, and applies the unchanged schema `snapshot()` assertion.
Direct syntax/static issues belong to their field. A coupled issue has a stable
message and the complete set of participating fields; it is shown once as the
form error and referenced by those fields with `aria-describedby`. There is no
event-history-based error owner. `fieldErrors`, rule text, slider state, summary,
and `canGenerate` are projections of this same result. The controller must not
call `adapt()` or a second bounds validator to decide any of them.

When all active dimensions are valid, compute every 0.1 mm interval from that
exact draft using the equations already frozen in `DESIGN.md`. Each slider uses
its current interval and its rule says `Allowed now: min–max mm`. Auto Lid stays
read-only/disabled. `nextLastValidDimensions` becomes the complete current
dimension snapshot. Generate is enabled only when the same result contains
`generationValues` and selectors are valid.

When any active dimension is blank, nonnumeric, out of bounds, or violates a
coupled rule:

- preserve every raw string exactly and show the canonical error;
- disable **all dimension sliders** and Generate;
- do not compute a range from the invalid draft or splice in field fallbacks;
- derive each display interval from the complete `lastValidDimensions` and say
  `Last valid range: min–max mm · correct the highlighted dimensions to use sliders`;
- leave `lastValidDimensions` unchanged until the whole dimension draft is valid.

This makes the range statement truthful about its source and gives one recovery
path: correct the exact entry. Changing drains or output cannot erase or move a
dimension issue. Selector errors block Generate but do not pause sliders when
the dimensions themselves are valid. Reset replaces `raw` and
`lastValidDimensions` with complete defaults, clears generated/download state,
and does not generate. Slider input is accepted only from an enabled interval,
updates its paired raw value, derives state once, invalidates current generation,
and never starts generation.

## Superseded clauses

This revision supersedes `DESIGN.md` only where it says an invalid field disables
only its own slider, dependent rules mix in per-field last-valid values, or
`editedKey` determines ownership. It temporarily relaxes MC-REQ-04's
current-draft slider availability during invalid entry: sliders pause until the
exact draft is coherent. MC-REQ-05 remains: raw input is retained, Generate is
blocked, and rules visibly identify their last-valid source. All valid-state
equations, intervals, responsive layout, icons, lifecycle behavior,
defaults, SCAD/schema/worker behavior, and acceptance boundaries remain intact.

## Required integrated checks

| State/event | One derivation must prove |
|---|---|
| Defaults | Current rules D 11–69, W 4–25, H 46.2–305, T 2–8; sliders and Generate enabled. |
| D blank, then `70` | Literal retained; D direct error; every dimension slider disabled; all rules labeled last-valid; W/raw unchanged; Generate blocked. |
| Manual H30/T7/L35 | One stable H/T/L coupled issue; all sliders paused; correction to T7.1 clears it and restores current ranges. |
| Auto H36/T7.5 | One stable Auto H/T issue; no manual-L dependency; correction restores current ranges. |
| Invalid dimensions, then drains/output change | Identical dimension issue, last-valid snapshot, paused sliders, and rules. |
| Same final raw entered in different orders | Identical issues, rules, slider state, and Generate state for the same last-valid snapshot. |
| Enabled slider input | Paired exact value and summary update; current bytes become stale; zero generation calls. |
| Generate | Uses only this result's `generationValues`; invalid state cannot submit. |

Test these through the full `main.mjs` controller with a fake DOM, in addition
to pure equation tests. Assertions against isolated bounds helpers are
insufficient because C4's failure was disagreement between helper, displayed
error, and Generate state.
