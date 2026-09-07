# DC-VAL-01 independent validation

- Owner / role: `/root/drain_count_validation`, independent validator
- Date: 2026-09-06
- Verdict: **PASS for frozen source, state, build, and compiled mesh evidence**
- Baseline commit: `2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f`
- Baseline manifest SHA-256: `e0304165a054bd228d59d48b024bd9eeed2dfd1f7140f1a202b69411e08390aa`
- Frozen design SHA-256: `41c1717355117185850b8d17783278ca81a65b6bcf020a83c0a32f6b6e017ce0`
- Candidate manifest: `inputs/candidate-03.sha256`, SHA-256 `6fa4bb84a83bc859b95b0568d43e34227a5bc2be7f82fe8fb6a2f11796953f57`

## Provenance and focused checks

All 22 candidate paths passed SHA-256 verification before validation and after
the final build. The candidate SCAD SHA-256 is
`517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`.
The baseline was extracted from the named commit into
`/tmp/drain-count-validation`; all 19 baseline-manifest paths verified there.
The pinned OpenSCAD runtime hashes were `904a47f2...` for `openscad.js` and
`f72ce246...` for `openscad.wasm`, matching `dependency-lock.json`.

Commands run from the repository root:

```text
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-06-drain-count/inputs/candidate-03.sha256
  22/22 paths OK

node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs
  29 passed, 0 failed

uv run pytest -q projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_vfr08_functional_repair.py
  12 passed

npm run build:openscad-simulator -w laifen-wave-case
  Vite 6.4.3: 19 modules transformed; build passed
```

The build emitted only Vite's non-blocking chunk-size advisory. It wrote the
authorized ignored private-preview `dist`; it did not alter any candidate
manifest path.

## Independent math and source checks

`/tmp/drain-count-validation/source_math_probe.mjs` independently imported the
frozen helper, schema, and adapter and passed these checks:

- `N=1` is exactly the center; `N=2` is center plus `+X`; `N=7` reproduces
  angles `0,60,...,300` degrees.
- Browser maxima are exactly `D10 -> 1`, `D11 -> 7`, and `D30 -> 17`.
- The schema accepts the safe side of the sidewall, center-to-ring, and
  adjacent-ring equations and rejects the unsafe side.
- `drainage_mode="none"` accepts `N=24,d=5,R=2`, proving physical-spacing
  checks are skipped while legal source domains remain enforced.
- The adapter preserves active raw count `17`, rejects active `D11/N8`, and
  emits canonical `7` for an inactive malformed draft.

The focused controller suite separately proves exact malformed text remains
repairable while its paired range is disabled, none-selected state remembers
the raw draft, re-enabling exposes the same error, slider edits do not generate,
edits cancel active work, and Reset restores Bottom-only with count 7.

## Pinned-WASM actual geometry

`/tmp/drain-count-validation/drain_geometry_probe.mjs` compiled smooth parts
from the exact candidate SCAD with the pinned WASM. It compares each active
part against a no-drain reference at the same dimensions. Every accepted mesh
has positive volume, zero non-two-use edges, and unchanged bounds.

| Case | Actual section openings | Minimum pair ligament | Minimum sidewall | Result |
|---|---:|---:|---:|---|
| D30 / N1 / body | 1 | n/a | 13.5 mm | pass |
| D30 / N2 / body | 2 | 6.0 mm | 4.5 mm | pass |
| D30 / N7 / body | 7 | 6.0 mm | 4.5 mm | pass |
| D30 / N17 / body | 17 | 0.5116 mm | 4.5 mm | pass |
| D11 / N7 / body | 7 | 0.5 mm | 0.5 mm | pass |
| D11 / N7 / cap | 7 | 0.5 mm | 0.5 mm | pass |
| D10 / N1 / body | 1 | n/a | 3.5 mm | pass |
| D10 / N1 / cap | 1 | n/a | 3.5 mm | pass |

For every case, center-point probes found void at each intended opening;
midpoint probes found solid center/ring and adjacent-ring ligaments; radial
probes found retained sidewall. Cross-section loop topology counted exactly
`N` openings. Measured volume loss matched `N` independent 96-sided cutter
prisms within `7e-10 mm^3`, providing an independent missing/extra/overlapping
cutter check.

The same runtime rejected `D10/N2`, `D11/N8`, and `D30/N18` with the named
0.4 mm ligament assertions. Direct source edits also passed at `R=13.099`
(sidewall), `R=3.401` (center/ring), and `R=3.919100...` for `N=8`
(adjacent ring), then failed at `13.101`, `3.399`, and `3.917100...`.
Values just outside `d=[1,5]` and `R=[2,14]` were rejected. Valid-domain
`D10,d=5,N1` and drain-free `D10,N24,d=5,R=2` compiled as closed solids.

## Root-owned Safari evidence

Root performed the native Safari interaction pass against the frozen C3 build;
these are attributed observations, not an independent browser claim by the
validator:

- At 1440 x 900, the initial state showed count 7 per selected end and maximum
  17. Blank, `abc`, `2.5`, `0`, and `25` remained exact editable drafts while
  the paired range and Generate were disabled; entering `7` repaired the state.
- With neither drain end selected, raw `abc` remained remembered while both
  count controls were disabled and Generate was enabled. Re-enabling an end
  restored the unchanged `abc` draft and its error. All four end-selection
  modes were exercised.
- `D11/N8` kept exact text `8`, put the slider thumb at 7, and showed the
  explicit too-high coupled error. `D10`, wall 5, `N1` exposed maximum 1;
  `D30/N17` exposed maximum 17. Explicit Generate with `N17` and both ends
  completed at `Preview up to date`.
- At 390 x 700, the scrolling parameter panel kept the canvas and action footer
  pinned. An actual slider click followed by Left produced count 9, synchronized
  the exact field and range, marked the prior result stale, and did not generate.
  Entering `abc`, selecting neither end, and Reset preserved the expected
  disabled/remembrance transitions; Reset restored 7, Bottom-only, cleared the
  mesh, and did not generate.

Screenshots are
`/tmp/container-count-browser/c3-{desktop-count,desktop-coupled,desktop-generated,mobile-top,mobile-count,mobile-slider,mobile-invalid,mobile-none,mobile-reset}.png`.
No active compile interruption or STL download was exercised in this Safari
turn; cancellation behavior is covered by the focused Node gate, while exact
download bytes remain prior-iteration evidence. This pass does not claim a
broader UI regression matrix.

## Private delivery byte parity

The validator used bounded
`curl --fail --silent --show-error --max-time 20` requests to compare every
file served by the existing private `https://mac-mini.duckbill-ionian.ts.net:8453/`
route with the final local `dist`. All six responses were byte-identical:

| Built/served file | Bytes | SHA-256 |
|---|---:|---|
| `index.html` | 7,478 | `7a4eddd8144fdc0d26a64d4ec4c9d8adb1c432bd71d078552ca3670f286ed131` |
| `index-Bmck2Ywj.css` | 5,322 | `1e46f000a5298380ca3a0b123e6ac90ba0cfc512bb8cd914c3c49de8b2225a9e` |
| `index-C4TURRus.js` | 543,919 | `e1bc77c309808b5e3665a46f86568fda4623a13c881e500a978b5be1d7835e88` |
| `openscad-CutNEzGH.js` | 124,567 | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `openscad-DIKIGOy4.wasm` | 9,603,115 | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| `openscad.worker-Csx1v_-i.js` | 1,823 | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |

This establishes that the private route serves the locally validated build; it
does not add browser-interaction or physical acceptance.

## Locked default parity and acceptance boundary

The frozen baseline default smooth assembled Bottom-only STL and candidate
default `N=7` STL are byte-identical:

```text
b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169
```

This evidence covers DC-01 through DC-07 at the source, browser-state,
compiled-geometry, private-build, and served-byte levels. The root-owned Safari
observations cover the requested compact desktop/mobile states. No validator
browser or service was started. No STEP, slicer, printer, drainage-performance,
strength, water-passage, fit, or physical acceptance claim is made.
