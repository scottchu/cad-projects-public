# DC-IMP-01 — drain-hole count implementation

Implemented against baseline `2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f` and
frozen design `41c1717355117185850b8d17783278ca81a65b6bcf020a83c0a32f6b6e017ce0`.

The browser retains `drainCount` as raw text, exposes an integer range paired
control, and emits a canonical `7` only while drains are disabled and the raw
text is not source-valid. `drain-layout.mjs` is the shared geometry owner for
the center-plus-ring center list and the `g=0.4 mm` feasibility maximum. The
SCAD source now independently validates the count and all active drain
ligaments, then uses the same center plus `N-1` polar ring construction.

Changed implementation paths:

- `openscad/laifen_case_customizer_v1.scad` — `517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`
- `preview/openscad-wasm-simulator/index.html` — `070bffc58ed2d95aa689c751cc81b952b761e7f9da78d6d258d1b2e11e511e25`
- `preview/openscad-wasm-simulator/src/{schema,bounds,adapter,controller,drain-layout}.mjs`
- `tests/node/compact-controller.test.mjs` — `9bcf58a46afb2d47650d37bac04eb60d365d7dbaa6009c3586bfdcaf9458dd80`

Focused checks passed:

```text
node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs projects/laifen-wave-case/tests/node/compact-controller.test.mjs
# 28 pass, 0 fail

uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py -q
# 9 passed

git diff --check
# passed
```

## Repair cycle 2

The exact Number of holes field is disabled only while neither end is selected.
It remains editable for active blank, malformed, invalid-diameter, and coupled
count drafts; its paired range remains independently disabled whenever it has
no safe numeric projection. The focused controller test now covers those states
and passed 8/8 with `git diff --check`.

Coverage includes reset/default `N=7`, all drain checkbox modes, inactive raw
count retention with canonical inactive emission, active count errors, dynamic
`D=10/11/30` limits, paired control synchronization, cancellation and explicit
generation. This receipt does not claim compiled-WASM opening counts, mesh
validity, browser visual review, slicer behavior, or physical acceptance; those
remain independent gates.

## Repair cycle 1

DC-IMP-02 corrected two critic findings without changing the raw-draft model:
`adapt()` now treats an explicitly supplied valid count as authoritative and
returns the same active count/diameter errors as the draft owner; when drains
are off, invalid raw text still emits canonical `7`. A malformed active count
now disables its paired range. For a valid count above the current maximum,
the range thumb displays the nearest valid repair maximum while the exact raw
text remains unchanged and the rule explicitly identifies that draft.

Added focused regressions cover `D=11,N=8`, `N=17`, inactive malformed raw
emission, malformed-range disabling, and unchanged raw text. Re-ran:

```text
node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs projects/laifen-wave-case/tests/node/compact-controller.test.mjs
# 29 pass, 0 fail

git diff --check
# passed
```
