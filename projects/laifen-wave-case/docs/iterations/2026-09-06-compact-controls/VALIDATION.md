# MC-VAL-01 — independent validation

## Planned stage

This section records the plan made before an implementation candidate was
available. The executed C2 receipt follows it.

Validation authority is the frozen design manifest
`inputs/design.sha256` at
`8899be6114a32a418cf6d2bd0d0766b15bfc77c78631d5ac19a4a8a1a425f8a2`.
Its baseline manifest is
`d0efe353a06e7dc48a5b8a055eb45121d4e2cd2a37cff0428572bf36c580bd49`.
The validator may write this file and temporary independent oracle code under
`/tmp`; candidate source, tests, artifacts, services, and hosting are immutable.

### Numeric oracle

Use an independent Decimal/Fraction oracle in `/tmp`, with `k = 28/73`, to
compare the candidate range adapter and every slider-produced snapshot. Closed
bounds are included; a 0.1 mm slider ceiling/floor is rounded inward, with one
tick added or removed for strict inequalities. Direct typed values are checked
against the unrounded equation and must retain their literal draft string.

| Witness | Expected result and failure caught |
|---|---|
| Adapter defaults `D30 W4.5 H213 T3`, Auto | derived lid `84`; formula-computed slider rules `D 11–69`, `W 4–25`, `H 46.2–305`, `T 2–8`; catches static schema ranges. The corrected frozen design witness agrees with the equations and actual default. |
| `D10 W5` | `D 10–69`, `W 5–35`; changing either slider leaves the other field unchanged and validates; catches reciprocal OD coupling/clamping |
| `D69 W5.5` | `D 10–69`, `W 4–5.5`; endpoints validate; catches inclusive 80 mm OD ceiling |
| Auto `T3` | `H` slider minimum `46.2`; `H46.2` gives lid `20.0219178…`; typed exact boundary `H=323/7` gives lid `20` and is valid, while `46.14` is retained and invalid; catches premature decimal rounding |
| Auto `H36.2 T8` | `T` slider is `8–8` and lid is `20.0219178…`; with arbitrary `H36 T8`, the pure oracle reports no usable Auto `T` interval; catches empty-interval handling |
| Manual defaults `H213 T3 L84` | `H 83.1–305`, `L 20–213.9`; typed `H83` and `L214` are retained and invalid, while `H83.0001` and `L213.999` satisfy the unrounded strict equations; catches treating strict bounds as closed |
| Manual `H30 T8 L35` | `T 7.1–8`, `L 20–35.9`; typed `T7` or `L36` is retained and invalid; catches strict tick movement |
| Invalid dependency | Blank `D`, then typed `70`, remains visible with `aria-invalid`; `D` slider and Generate disable; `W` rule uses last valid `D30` and says so; catches native coercion and hidden dependency fallback |

For each slider endpoint and one interior tick, assert that only the selected
draft field changes, the candidate snapshot validates, derived values and rule
text update, and no generation callback runs. Cover range `input`, `change`,
pointer release, and keyboard release. Verify Auto-off preserves the shown lid
as the manual starting value; Auto-on recomputes it. Reset must restore the
complete adapter defaults and selector positions, clear current mesh/download,
and record zero generation calls.

After a frozen candidate is supplied, verify its manifest first, inspect only
that candidate, create the independent `/tmp` oracle, then run the focused Node
range/DOM/lifecycle tests, focused Python schema tests, and the root npm build
using the exact commands named in the implementation receipt. Record commands,
exit status, assertion counts, candidate fingerprint, and any changed generated
paths. Do not accept a test that imports expected bounds from the candidate.

### Root-executable Safari checklist

Serve only the frozen `dist` already assigned to ports 5178/8453. In Safari
Responsive Design Mode, capture a clean-load image and accessibility state at
each size below, then perform the interactions on the same candidate:

1. At `390x700`, expect a 238 px preview row; at `390x844`, expect a 280 px
   preview row. Scroll the parameter rail from top to bottom and capture before
   and after. Preview top/bottom bounds must be unchanged within 1 CSS px, the
   document must not scroll, and the dock must remain visible without overlap
   or horizontal overflow.
2. Repeat layout captures at `760x800`, `761x800`, `1280x800`, and `1440x900`.
   `760` must use pinned preview-over-controls rows; `761` and wider must use a
   full-height canvas-left/control-right grid with a 360–400 px independently
   scrolling rail.
3. Inspect the three preview controls and three dock controls. Each target must
   measure at least `44x44` CSS px with at least 8 px spacing and no visible text
   action label. Accessibility names and SVG titles must be exactly `3D view`,
   `Cutaway view`, `Reset view`, `Generate preview` (or `Cancel` while busy),
   `Reset dimensions`, and `Download STL`. Tab to every control and hover each:
   tooltip and 2 px focus ring must be visible. Toggle 3D/Cutaway and confirm
   `aria-pressed` plus border/background change; verify disabled Download remains
   named and discernible.
4. Record defaults and their rule lines. Clear `D`, then enter `70`. In both
   cases the literal input remains visible, `aria-invalid=true`, a specific
   inline error appears, its slider and Generate disable, and `W` says it is
   using last valid `D` with the prior numeric interval. Correct to `30`; all
   provisional cues clear and slider/value synchronize.
5. Drag `D` from `30` to `69`. Confirm `W` remains `4.5`, outside diameter/rules
   update, the selected overlay follows `D`, preview becomes stale, Download is
   unavailable, and no busy/Cancel state or new mesh appears. Repeat one tick
   with arrow keys. Slider release must not generate.
6. With Auto on, lid is read-only and derived. Turn Auto off: the displayed lid
   becomes editable without changing value. Exercise the manual strict witness
   `H30 T8 L35`, then type `L36`; confirm retention, the specific error, and
   disabled Generate. Restore valid values and re-enable Auto; lid recomputes.
7. Change drains and export selections, then use Reset dimensions. Compare every
   value and selector with the recorded clean-load defaults: Auto, drains,
   output, ranges, and slider positions must match; mesh/current Download must
   clear; no generation may start.
8. Generate defaults and await current status. Download must enable only then;
   activate it and verify a newly downloaded non-empty STL. Edit one slider and
   confirm the link disables immediately. Explicitly generate the edited draft,
   download again, and verify its bytes/checksum differ when geometry differs.
   Start another generation and activate Cancel if the busy slot remains visible;
   otherwise rely on the focused lifecycle cancellation test and record that the
   manual Cancel window was too short. Late/cancelled output must never re-enable
   a stale download.

The browser receipt must attach size-labeled before/after captures, measured
bounds, accessibility observations, generation/download file evidence, and a
requirement map for MC-REQ-01 through MC-REQ-08. It must keep CAD, written mesh,
and physical/print acceptance explicitly separate; this UI validation creates
no print-ready claim.

## C2 execution receipt

Status: **rejected for focused repair**. Candidate C1 failed its first integrity
gate because `src/main.mjs` changed after freeze; no C1 test or build gate ran.
That writer drift was resolved by freezing C2. C2 manifest
`inputs/candidate-02.sha256` has SHA-256
`68e98695f4c1328124f7a1bf1e3878b104298e1080dd835582e22ba9fe1b6c72`;
all 19 declared paths passed before execution and again after the gates below.

### Deterministic evidence

- `node /tmp/mc-val-01-oracle.mjs` — pass for valid states. An independent
  equation implementation matched 26 dynamic intervals and exhaustively checked
  22,458 produced 0.1 mm values through the unchanged adapter/snapshot. The exact
  Auto boundary `H=323/7`, the invalid `46.14` witness, D/W coupling, Auto floor,
  and manual strict bounds behaved as specified. Scratch oracle SHA-256:
  `e44bc48ff24252a2cb49564d5070f662eab3cd51630c01543d2b7a9596497688`.
- `node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs`
  — 16 passed, 0 failed in 42.76 ms.
- `uv run python -m pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py`
  — 4 passed in 0.01 s.
- `npm run build:openscad-simulator --workspace laifen-wave-case` — pass; Vite
  transformed 16 modules and built `dist` in 535 ms. The 536.71 kB JavaScript
  chunk produced only Vite's advisory chunk-size warning.

The valid-state math and unchanged schema gates pass, but the focused tests do
not exercise the integrated DOM state machine that failed below.

### Findings

1. **High — slider and numeric draft diverge (MC-REQ-04, MC-REQ-06).** The range
   handler updates `raw` and calls `edit()` but never assigns the same value to
   the numeric input (`src/main.mjs:64`); `refreshFields()` also does not sync
   ordinary numeric inputs (`src/main.mjs:15-32`). Root's Safari run at 390x700
   dragged diameter to 11: accessibility state showed slider 11, numeric input
   30, outside diameter 20, and wall rule 4.5–34.5. This is a visible ambiguity
   about what Generate will use. Evidence:
   `/tmp/container-compact-validation/c2-slider-state.txt`, SHA-256
   `07d4ec0978f2b21d9511bfe4e61532eff6ab1912472e76ad01ddabea390e1ca5`.

2. **Critical — an edit during an explicitly started generation can accept and
   download the obsolete result (MC-REQ-06, MC-REQ-07).** The first draft edit
   sets `draftDirty=true` (`src/main.mjs:58`). Generate starts without clearing
   it (`src/main.mjs:66`), and it is cleared only after a result becomes current
   (`src/main.mjs:34-41`). Therefore a further edit while that generation is
   active skips `generation.invalidate()` at line 58. Its epoch remains owned,
   so the old result can install bytes and mark the changed UI current. Existing
   lifecycle unit tests cover direct invalidation, but no DOM/integration test
   covers this wiring path.

3. **High — finite invalid dependencies neither use nor label last-valid bounds
   (MC-REQ-05).** With typed `D=70` and last-valid `D=30`, the independent probe
   found the D slider still enabled and the dependent wall slider disabled with
   `No allowed value with the current dimensions`, instead of D disabling and W
   retaining 4–25 with a named last-valid cue. `numberDraft()` prefers every
   finite string regardless of constraint validity (`src/bounds.mjs:8`), while
   the own-field guard rejects only blank/nonfinite text (`src/bounds.mjs:22-30`).
   In the UI, the provisional-note predicate also treats blank `''` as numeric
   zero and detects no finite out-of-range value (`src/main.mjs:26`); line 30 can
   even record `D=70` as last valid because the adapter attaches the OD error to
   wall. The current unit test checks only the bounds result for a blank value,
   not the required displayed cue or finite-invalid case.

4. **Moderate — Cancel does not occupy Generate's slot (MC-REQ-03, MC-REQ-07).**
   Busy state unhides Cancel but never hides Generate (`src/main.mjs:34-41`), and
   the flex action row gives both separate positions. The candidate also labels
   it `Cancel generation`, while the frozen compact contract calls for `Cancel`.

5. **Low — the widest desktop rail exceeds the frozen 360–400 px contract
   (MC-REQ-02).** CSS changes the rail from 380 px to 420 px at 1600 px and wider.
   The prescribed browser matrix stops at 1440, so this is source evidence only.

### Browser checkpoint and coverage

Root loaded and completed a real default WASM generation at 390x700 before the
first slider interaction. The top capture visually shows compact icons, the
pinned 238 px preview row, sliders/rules, and the fixed action dock:
`/tmp/container-compact-validation/c2-mobile-top.png`, SHA-256
`3afba0480152f7a6cd7d53ea295eefcc64a1432aa1761a53900dfb3b0e973477`.
The run stopped after reproducing finding 1, so full scroll-bound measurements,
760/761/desktop captures, tooltip/keyboard checks, invalid-entry interaction,
Auto/manual/Reset, Cancel, and fresh-download byte checks remain pending for a
repaired candidate. MC-REQ-08 remains covered only by unchanged candidate hashes
plus the passing schema/Python gates; no CAD geometry, slicing, print, assembly,
or physical acceptance was performed or claimed.

### Changed paths and next action

The validator changed only this receipt. `/tmp/mc-val-01-oracle.mjs` is disposable
scratch; the authorized build regenerated ignored `dist`. Candidate source and
tests were read-only. Repair the three high/critical integrated-state defects,
replace Generate with Cancel in the same slot, constrain the wide rail, add DOM
regressions for slider/value synchronization, finite-invalid last-valid rules,
and edit-during-generation cancellation, then refreeze. Rerun the focused tests,
oracle, build, and the complete Safari matrix on that new fingerprint.

## C3/C4 repair receipts and design reopen

C3 (`inputs/candidate-03.sha256`
`151491f84ca8853763b023a4a478f5001c4feb368cf3554b6a099535dee33395`)
resolved C2's slider/value synchronization, finite-invalid D fallback, active
generation invalidation, Cancel slot/label, and 420 px rail findings. Its build
passed in 517 ms; Node passed 18/18, Python 4/4, the independent oracle again
covered 26 intervals and 22,458 slider ticks, and a fake controller using the
exact `edit()` and Generate handler proved that an edit during identity work or
after worker creation invalidates the job and rejects queued output. Root Safari
at 390x700 confirmed slider 40/input 40, a stale preview with no automatic
generation, and retained blank/70 inputs with the last-valid D rule. C3 was
rejected because cross-field failures still followed adapter error placement:
manual H/T and Auto T edits blamed another field. A valid correction also left
the stale `Check the highlighted dimensions.` status.

C4 (`inputs/candidate-04.sha256`
`dd9dfcbe25d7946207d009ddb8e2ee1a499442b6d712202bed31f7fe192d0d1d`)
passed all 20 manifest paths before and after execution. The authorized build
passed in 510 ms (17 modules; only Vite's standard large-chunk advisory), Node
passed 19/19, Python passed 4/4, and the independent controller test passed both
in-flight edit windows. The corrected bounds layer passes the specific ownership
oracles: manual `H83/T3/L84` disables H; manual `H30/T7/L35` identifies T with
the independent usable interval 7.1–8 and preserves current L35; Auto `H36/T7.5`
identifies T. Valid correction status is also repaired.

C4 remains **rejected** because ownership is fixed only in the range layer.
`refreshFields()` still sets `aria-invalid` and inline error text directly from
`adapt(raw).errors[key]`. The independent run recorded these adapter results:

- manual `H83/T3/L84` -> `errors.lid`;
- manual `H30/T7/L35` -> `errors.lid`;
- Auto `H36/T7.5` -> `errors.height`.

Consequently the edited H or T slider disables, but the numeric field remains
`aria-invalid=false` with no own error while Lid or H is falsely highlighted.
This fails MC-REQ-05's required retained invalid field, own disabled slider, and
specific associated error as one coherent state. Passing source tests cover
`fieldInvalid()` and slider state, not the integrated error association.

Root captured the C4 responsive matrix at 390x700, 390x844, 760x800, 761x800,
1280x800, and 1440x900. The paired mobile top/bottom captures show the preview
pinned while the parameter rail scrolls and the dock stays visible; the
760/761 captures show the intended row-to-column breakpoint. Evidence is under
`/tmp/container-compact-validation/c4-*.png`; representative SHA-256 values are
`45f4e5777c9748a25edcf0211101c7fbf550d3806fb50646fe78ad93b8e3bb39`
(390x700 top),
`0e74a4f43afd9f9bc5baca6609a93f42a30a211b2ca24ae7b030582cd1a5f279`
(390x700 bottom),
`49992357af388e45633d4bc284c40f867c02175a51bec11cf89ba6538d77abdd`
(761x800), and
`57cee430f074793dc7e9bf8767c806fd8e6bca81ae6eee18c6ddf46be74fdd48`
(1440x900). Broader C4 interaction checks stopped after the blocking integration
finding.

The initial implementation plus two bounded repair cycles are exhausted. Root
has reopened design as MC-DES-02 to simplify invalid typed behavior while
retaining the user's pinned canvas, compact icons, sliders, and truthful allowed
rules. No further C4 repair or acceptance gate is authorized. The next validator
must use the new frozen contract and candidate fingerprint; C4 evidence may be
reused only for gates whose declared inputs remain unchanged.

## C5 revised-contract receipt

Status: **deterministic pass; fresh browser acceptance blocked pending desktop
unlock**. This is not a full UI acceptance or release claim.

The revised authority is `RULES-REVISION.md` SHA-256
`53f9dd990507ec640f615cac30dbc466e1ecff325494886af2535c96e586a6ca`
under `inputs/rules-revision.sha256`
`75b16b2f8d2e59847ef2689266d5b3b634cfae75cdd57ecd8e1b34eaf5b920be`.
C5 `inputs/candidate-05.sha256` SHA-256 is
`f51607ab4e80b2d2b6fa753d90f55f1cb64504c42c3b5919e6175d27e100e714`;
all 23 paths passed before execution and again after the gates.

Executed evidence:

- `npm run build:openscad-simulator --workspace laifen-wave-case` — pass, 18
  modules in 521 ms; `dist/index.html` 6.90 kB, CSS 4.90 kB, main JavaScript
  539.52 kB, with only Vite's standard large-chunk advisory.
- `node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs projects/laifen-wave-case/tests/node/compact-controller.test.mjs`
  — 25 passed, 0 failed in 257.62 ms.
- `uv run python -m pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py`
  — 4 passed in 0.01 s.
- `node /tmp/mc-val-02-oracle.mjs` — pass; independent equations matched 26
  current valid intervals and exhaustively checked 22,458 slider ticks through
  the unchanged adapter/snapshot. Scratch SHA-256:
  `0c257f43c0e4f5bcded14ef5f71d82b4d342e98156bb03ef09c9f209fd620457`.

The independent invalid-state checks passed the revised contract: blank D and
D70 preserve the exact draft, disable all dimension sliders, keep the complete
default last-valid snapshot, label every rule `Last valid`, and block Generate;
manual H30/T7/L35 produces one stable H/T/L issue and clears at T7.1; Auto
H36/T7.5 produces one H/T issue and clears at H36.2/T8; an invalid selector
blocks Generate while coherent dimension sliders continue using current ranges.
The full fake controller additionally proves error/`aria-describedby`
projection, selector stability, slider-to-number synchronization without
generation, edit-during-generation cancellation, Auto/manual preservation, and
Reset without generation. `src/main.mjs` is now only browser composition; the
controller consumes one `deriveDraftState()` result for rules, errors, summary,
sliders, last-valid state, and generation eligibility.

Fresh Safari checks could not start after the C5 build. Computer Use returned
`-10005 cgWindowNotFound` for the existing Safari binding, a fresh Safari app
lookup/window key, Chrome lookup, and a reset session. Surface inventory still
reported Safari running but no browser providers, consistent with a locked or
otherwise unavailable desktop session. Root requested a user unlock and did not
claim a C5 runtime generation or fresh capture.

Root separately compared the six local C5 `dist` files byte-for-byte with their
HTTPS responses on port 8453 using Python URL retrieval and `curl --fail
--max-time 20`. All six delivered bytes passed: `index.html` 6,899 bytes SHA-256
`86913f5d39fffd1b3b68113e58a7cb3ab6bb26d9180a69129a9879bfa414020c`;
main JavaScript 539,516 bytes
`55099cc8d29aa353b94eb3ac5641bb8925e67616e1104254d5bd6054c50819dd`;
CSS 4,902 bytes
`d7eab67b67d7bc25338e98f81859a2df07dd719fb357aca1a7ed8a1521b17780`;
OpenSCAD engine 124,567 bytes
`904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e`;
WASM 9,603,115 bytes
`f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`;
and worker 1,823 bytes
`cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e`.
This proves the private URL serves the frozen build; it is not browser or
interaction acceptance.

The C4 responsive captures remain valid evidence only for MC-REQ-01/02 layout:
C4 and C5 have the exact same `style.css` SHA-256
`a25b47f668009b1d8b15c29179b566ae5fd5018105f8c4d2ca03a3cee2c643be`.
They show the pinned 390x700/844 preview, fixed dock, 760/761 breakpoint, and
desktop columns. C5 still needs fresh Safari checks for its changed controller
and markup: blank/70 and manual/Auto coupled issue rendering, icon keyboard and
tooltip behavior, Auto/manual, Reset, slider no-generation, an edit during live
generation, and current-only real STL generation/download. MC-REQ-08 has
unchanged-source/hash and deterministic schema coverage only. No slicer, print,
assembly, or physical acceptance was performed or claimed.

The validator changed only this receipt and disposable `/tmp` oracle code; the
authorized build regenerated ignored `dist`. Candidate source/tests remained
read-only. Next action is to unlock the desktop, reverify the C5 fingerprint,
and run the pending narrow Safari interactions without changing or refreezing
the candidate.
