# VFR-12 mobile viewport and action alignment contract

Status: frozen when the sibling input manifest is written and verified. Task ID `VFR12-D`; owner `/root/openscad_vfr12_mobile_designer`, independent contract designer. Project `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`; active iteration `2026-09-04-openscad-visual-fidelity-recovery`.

## User evidence and bounded intent

The supplied iPhone screenshot at `/tmp/codex-remote-attachments/01a06004-6842-76f1-bf1e-486590d05ac5/8B8CE7A0-DC92-43D9-9A96-0CD21F0B6A61/1-Pasted-Image-1.jpg` shows the remaining ready-status sentence above a padded, bordered canvas card. The user explicitly rejects that visible sentence and requests a borderless fullscreen canvas; subsequent steering identifies the small, uncentered action glyphs. This is actual-user delivery feedback on VFR-11, not a geometry observation.

Interpret fullscreen as an edge-to-edge, full-width top viewer with parameters below. Retain the earlier explicit requirement that the initial phone viewport includes an entire editable field and reachable Generate. Browser Fullscreen API or a full-height canvas would defeat that requirement and are outside this correction.

Baseline: delivered VFR-11 C2 candidate manifest `ad7c14d9f40f354c70cbaf0394b89a9a03f795ec9e4d767c55c263096f054968`. Live baseline CSS, HTML, main, schema, worker and focused test hashes were verified against its delivery chain before this contract was written. VFR-12 supersedes mobile presentation only.

## Delta mask

All visible changes below apply only inside `@media(max-width:700px)`.

| Object | Allowed delta | Invariant |
| --- | --- | --- |
| `main`, `.layout`, `.result`, `#viewer` | Remove mobile outer viewer inset; zero result border, radius, padding and margin; make canvas block-level, full available width, zero border/radius/margin | Result remains sticky at top 0; preview remains above controls; no horizontal overflow |
| `#status` | Visually hide using absolute 1px clipped live-region treatment, zero margin/padding/border; remove it from visible layout flow | Remains in DOM, `aria-live="polite"`, display/visibility not hidden, text and runtime updates preserved |
| `#viewer` height | Retain `clamp(190px,26vh,220px)`; height represents the whole initial visible preview pane once status/card spacing is removed | At 390x844 expected 219.4375px from browser layout, acceptable 218–221px; no full-height viewport takeover |
| `.control-panel`, form | Preserve sensible 10px internal field inset; any wrapper margin needed to keep fields inset may be mobile-only | Existing independent form scroll, end scroll reserve and last-field clearance remain; no missing label/input |
| `.actions > *` and `::before` | Center content with both `align-items:center` and `justify-content:center`; pseudo icon uses a 24x24px box, 24px font-size and centered line placement | Five controls in the same order and a single row, >=44x44px touch targets; visible words remain hidden on mobile; meaningful DOM wording and all states preserved |
| `#stale`, `#viewer-note`, toast | Only local inset styling if needed after the result card is removed | Active warnings/fallbacks remain visible; toast, dismissal/focus and stale/download semantics unchanged |

Keep existing glyph meanings/order. Use no new dependency. Desktop (>700px) CSS layout, title/status visibility, action labels and sizes must remain unchanged. HTML, main, schema, worker, SCAD, runtime/vendor, build configuration, listeners, DOM IDs/order, geometry and all acceptance holds are immutable. Public Diamond controls remain disabled. No CAD generation or print acceptance is part of this task.

## Done gates and exact measurements

Independent browser validation consumes a frozen candidate and a real built bundle, with no CSS injection or mocked compiler. Record screenshot paths, exact rectangles/styles, commands and artifact hashes.

1. **V12-01, initial 390x844 at page/form scroll 0:** no visible title, ready-status sentence or card frame. `#status` retains its live-region attribute and text; computed display is not none and visibility is not hidden. Its clipped 1px box consumes no normal-flow height. Header remains hidden.
2. **V12-02, edge-to-edge preview:** initial result/viewer left 0 and right 390 within 1px; top 0 within 1px; viewer width equals viewport width within 1px. Result and canvas have zero border widths, radius and padding; no outer mobile main padding causes gutters. Initial result bottom equals viewer bottom within 1px, with viewer height 218–221px. Browser chrome is outside these CSS measurements.
3. **V12-03, reachable fields/actions:** at least one complete Basic label plus associated input, including its full >=44px input height, is visible and hit-testable below the viewer on first screen. All five actions appear simultaneously in one row with targets >=44x44px and no horizontal overflow (`scrollWidth <= clientWidth+1`). Controls have >=10px horizontal input inset. At maximum form scroll with document scroll 0, the final Output select is entirely above the actions, with >=8px clearance; top/center/bottom hit tests return the select.
4. **V12-04, glyph centering:** each action's visible pseudo box is 24x24px; computed font-size 24px, with centered inline/block alignment. Measure each pseudo box center relative to the button/anchor content center; horizontal and vertical delta <=1px. Inspect screenshot to catch glyph font metrics that appear off-center despite passing box math. Center click/tap hits the intended control. Disabled and enabled icons retain distinct states.
5. **V12-05, responsive edges:** at 360x640 and 430x932 verify full-width borderless viewer, no horizontal overflow, five >=44px targets, first complete field visible, and final field reachable. At <=700px use mobile treatment; a focused 700/701px computed-style boundary check confirms desktop rules begin only above 700px.
6. **V12-06, scroll/state regression:** viewer remains sticky at top while parameters scroll; existing actionable toast is readable and returns focus after dismissal. Real smooth generate still displays a model and enables Download; subsequent edit retains visible stale notification and disables Download. All five surface/Diamond controls remain disabled. These are browser flow checks, not mesh acceptance.
7. **V12-07, desktop preservation:** fresh 1440x1200 screenshot retains heading/status and visible 16px action words, 580px canvas and prior desktop layout, with no new overflow. Verify unchanged immutable source hashes and focused existing tests.
8. **V12-08, private delivery:** after independent validation, critique and formal review, verify the exact authorized Tailscale route against the approved bundle and inspect mobile screenshot. Controlled browser checks do not claim actual iPhone/Safari acceptance; report that limit honestly.

## Frozen inputs and role DAG

`inputs/VFR12_MOBILE_VIEWPORT_INPUTS.sha256` is a sorted SHA-256 path-and-content list with project-relative paths. Its own SHA-256 is the input fingerprint. It binds this task, active BRIEF/DESIGN, requirements, six baseline source/test files, and VFR-11 C2 manifest plus contract/implementation/validation/critique/formal/delivery records. Mutable PROJECT_STATE, NEXT_AGENT, HANDOFF and new evidence are read for continuity but excluded from gate invalidation. Changed manifest members invalidate only dependent VFR-12 gates and require refreezing before work.

| Stable task | Role and dependency | Exclusive writes / done gate |
| --- | --- | --- |
| VFR12-D | Independent designer; current role | This task and input manifest only; exact baseline verified, contract frozen |
| VFR12-I | Implementer after D; distinct identity | Mobile CSS, focused existing test updates only if required, implementation receipt and own scratch evidence; freeze resulting candidate, no self-approval |
| VFR12-V | Independent validator after I | Own validation report and scratch evidence; execute V12 gates, no source edits |
| VFR12-C | Independent critic after I; may run alongside V | Own critique report; independently inspect exact candidate and screenshots against user evidence |
| VFR12-F | Distinct formal reviewer after V and C pass | Own formal receipt; join matching fingerprints and decide delivery readiness |
| VFR12-L | Authorized private delivery after F | Existing private route bundle and delivery receipt; verify exact served bytes and phone-size browser layout |

Root assigns concrete runtime owner identities before scheduling each downstream role, caps active workers at three and preserves disjoint writes. Designer uses strong/high; implementation balanced/medium; critique, validation and formal review strong/high. Each role has a qualitative 15-minute/one-receipt ceiling with concise output; implementation permits initial candidate plus at most two focused repairs, each invalidating affected downstream gates. No parallel writer in any source/artifact namespace. If input hashes drift, an out-of-mask change is needed, or two repairs fail, stop and report the exact gate; do not expand to runtime, geometry or service repair. Every return names status, input/candidate fingerprint, changed paths, exact commands/results, relevant hashes, requirement coverage, findings/severity, unresolved limits and next action.

Design receipt: all six assigned baseline source/test hashes and C2 manifest matched. Source/current-state/active/VFR-11 records and user screenshot were inspected. This role performs no implementation, browser validation, deployment, continuity mutation or CAD acceptance.
