# DC-CRIT-01 — independent drain-count critique

## Candidate C1 provenance

- Candidate manifest: `inputs/candidate-01.sha256`, SHA-256
  `bc85262f41c82ab2ae561d91237a4962cb67e3cab5cce12b403530b31a76e748`.
- Verification: all 22 declared paths passed `shasum -a 256 -c` before review.
- Frozen contract: `DESIGN.md` SHA-256
  `41c1717355117185850b8d17783278ca81a65b6bcf020a83c0a32f6b6e017ce0`;
  `BRIEF.md` SHA-256
  `ea8612dbf0efa5bd946919f92c9b413c114112b1b3311781e0a35ccc3781d85d`.
- Visual evidence supplied by the root's native Safari run at 1440 x 900:
  `/tmp/container-count-browser/desktop-default.png` and
  `/tmp/container-count-browser/desktop-count-error.png`.

## Candidate C2 provenance

- Candidate manifest: `inputs/candidate-02.sha256`, SHA-256
  `89a10a72a83ba6104971ce4b24716c014ca5f9c4045df286c35809c0a6680e00`.
- All 22 declared paths passed `shasum -a 256 -c` before the C2 review.
- The root's native Safari accessibility inspection found that blanking the
  active count disabled both its exact input and range.

## Candidate C3 provenance

- Candidate manifest: `inputs/candidate-03.sha256`, SHA-256
  `6fa4bb84a83bc859b95b0568d43e34227a5bc2be7f82fe8fb6a2f11796953f57`.
- All 22 declared paths passed `shasum -a 256 -c` before C3 source review.
- Focused recovery test passed 1/1. The root then completed the prescribed
  native Safari interaction pass at 1440 x 900 and 390 x 700.

## Findings

### C1-01 — high — legacy adapter ignores and silently replaces the requested count

`preview/openscad-wasm-simulator/src/adapter.mjs:23-24` never reads
`raw.drainCount`; it emits `Math.min(7, max)`. A focused probe showed that
`D=30, N=17` emits `7`, while `D=11, N=8` also emits `7` without an error.
This violates DC-01's shared count and DC-05's no-clamp/error contract, and
leaves the adapter inconsistent with the schema/controller path. Blocking.

Disposition: resolved in C2. Focused probes showed `D=30, N=17` emitting 17
and `D=11, N=8` returning the same coupled maximum-7 issue on both fields.

### C1-02 — high — malformed active count leaves its range enabled

`bounds.mjs:74-75` substitutes `1` for an invalid count before computing count
state; `bounds.mjs:95-97` therefore reports an enabled range. The focused probe
for active raw `x` returned `canGenerate=false`, the correct direct error, but
`drainCount.disabled=false` and `max=17`. The frozen design requires the paired
range to be disabled while exact count text is directly invalid. Blocking.

Disposition: the range-disable requirement is resolved in C2, but the repair
also disables the exact input and creates C2-04 below.

### C1-03 — medium — coupled-error count thumb communicates the wrong draft

For `D=11, N=8`, Safari correctly preserved exact `8`, reported maximum `7`,
disabled Generate, and offered a diameter repair at `11.9` mm. However,
`controller.mjs:36` forces the count range thumb to `1` whenever the exact
value exceeds the dynamic maximum. The visible pair therefore says `8` and
`1` simultaneously. Seven is the nearest count repair and matches the stated
maximum; using the minimum makes the repair affordance unnecessarily
misleading. This is a focused UX issue, not a geometry error.

Disposition: resolved in C2. `controller.mjs` now places the coupled-error
range thumb at the nearest valid repair, 7, and the rule explicitly says the
preserved draft 8 is too high. The diameter repair remains correctly 11.9 mm.

### C2-04 — high — invalid active count disables its own repair input

`bounds.mjs:95-97` correctly disables the paired range for malformed active
count text, but `controller.mjs:33` applies the same `count.disabled` flag to
the exact text input. Native Safari accessibility evidence confirmed that
blanking **Number of holes** disables both controls. The field then says to
correct the count while preventing the user from typing that correction.
DC-05 requires malformed text to remain editable and only its range to pause;
the whole pair is disabled only when neither drain end is selected. Blocking.

Disposition: resolved in C3. `bounds.mjs` now reports whether a drain end is
active separately from range availability. `controller.mjs:33` disables the
exact input only when neither end is selected, while line 35 disables the
range for malformed count or unavailable bounds. Focused tests cover `x`,
blank, and invalid diameter recovery.

Surrounding whitespace in a whole-number draft is not recorded as a defect:
the frozen contract does not explicitly reject it, and the existing trimmed
parser is a defensible interpretation.

## C3 visual and interaction review

Direct visual inspection covered:

- `c3-desktop-count.png`: the default shared label reads **Number of holes**
  with **each end**, value 7, maximum 17, and intact canvas/icon footer.
- `c3-desktop-coupled.png`: `D=11, N=8` preserves exact 8, places the repair
  thumb at 7, names the draft/max relationship, shows the coupled 0.4 mm error,
  and disables Generate without clipping the controls.
- `c3-mobile-slider.png`: exact and range show 9 together; **Previous
  generation** makes the result stale while the fixed canvas and icon footer
  remain visible at 390 x 700.
- `c3-mobile-reset.png`: Reset visibly restores 7 and Bottom-only, clears the
  mesh, and asks for explicit generation while the footer remains pinned.

The root's same Safari pass also exercised blank, `abc`, `2.5`, `0`, and `25`;
all retained editable raw text, disabled the range and Generate, and recovered
when corrected. None remembered `abc`, disabled both count controls, allowed
drain-free generation, and restored the error unchanged when Top was enabled.
All four end selections, `D10/N1`, `D11/N8`, `D30/N17`, explicit generation of
17 holes on both ends, and a real slider click plus Left-key interaction were
covered. Programmatic slider `setValue` did not change the native control and
is not treated as evidence.

## Requirement coverage and disposition

- DC-02 through DC-04: no source-level contradiction found in the inspected
  center-plus-ring loop or ligament equations; independent compiled-solid
  validation remains outside this critique.
- DC-06: supplied screenshots retain the pinned canvas and icon footer; the
  root observed stale marking and no automatic generation after an exact edit.
- DC-01 and adapter portions of DC-05/DC-07: C1-01 is resolved in C2.
- DC-05 invalid recovery: C2-04 is resolved in C3.
- DC-01 and DC-05 through DC-07: C3 source and prescribed Safari behavior pass
  this independent critique with no remaining blocking or medium finding.
- DC-02 through DC-04 compiled-solid evidence and source/export parity remain
  owned by independent validation/formal review; no physical acceptance is
  claimed here.

## Commands actually run

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-01.sha256 projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/BRIEF.md projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/DESIGN.md
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-01.sha256
git diff --unified=80 2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f -- projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad projects/laifen-wave-case/preview/openscad-wasm-simulator/index.html projects/laifen-wave-case/preview/openscad-wasm-simulator/src/adapter.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/bounds.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/controller.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/drain-layout.mjs projects/laifen-wave-case/preview/openscad-wasm-simulator/src/schema.mjs projects/laifen-wave-case/tests/node/compact-controller.test.mjs
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-02.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-03.sha256
node --test --test-name-pattern='malformed count disables its paired range' projects/laifen-wave-case/tests/node/compact-controller.test.mjs
```

The focused C3 test passed 1/1. Active compile cancellation is covered by Node
tests rather than a fresh Safari interruption. No new file download was made
in the Safari pass; download currency changed correctly when the draft became
stale. Next action: join this passing critique with the independent validator
receipt against the exact C3 candidate.
