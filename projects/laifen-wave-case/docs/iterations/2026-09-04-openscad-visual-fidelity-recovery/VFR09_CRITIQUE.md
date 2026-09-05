# VFR-09 integrated independent critique

Status: **HOLD FOR PUBLIC DIAMOND ENABLEMENT — private body/cap worker
feasibility passes, the VFR-08 geometry repairs remain valid, and visible
Diamond controls remain disabled, but the frozen evidence does not satisfy the
prescribed final-mesh, smooth-interaction, or default-output browser gates.**

Owner role: `/root/openscad_vfr07_critic`, independent integrated critic. This
document is the sole write. Candidate source, tests, meshes, browser/runtime/
vendor files, built assets, services, continuity, STEP/slicer, and printer state
were read only.

Verified critique-input manifest:
`inputs/VFR09_CRITIQUE_INPUTS.sha256`, SHA-256
`96e584722a1c87cd32dc3bc0482d25bd746e17dbf38416a065e39755d1d29d90`;
all 4 entries passed. The nested 26-entry
`candidate/VFR09_INTEGRATED_CANDIDATE.sha256` passed 26/26. Its nested private
browser `CANDIDATE.sha256` passed 15/15, and the repaired VFR-08 scratch
inventory passed 33/33.

## Passing integrated evidence

### VFR-07 High findings remain resolved

The browser-generated body STL is byte-identical to the reviewed VFR-08
`diamond-bottom-body.stl` at
`6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8`.
It therefore retains the seven complete 3 mm body-floor apertures, one
watertight positive-volume component, Euler -12, 55,772 triangles, no
degenerates, and edge incidence exactly two. The browser cap is byte-identical
to the VFR-08 bottom-mode cap at
`e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514`;
bottom mode correctly leaves that cap undrained. The repaired OpenSCAD source
still contains the VFR-08 forward-bounded cutters and cap-only print-layout
rotation.

The manifest-bound VFR-08 print-layout artifact remains the exact previously
reviewed pair with both closed ends at print Z=0, openings at Z=144/84, and a
7 mm X-envelope gap. Nothing in the schema-only browser delta changes those
solids or transforms. The former blind drains and opening-down cap therefore
do not regress.

### VFR-08 Low hash-inventory finding is resolved

`scratch/vfr08-implementation/hashes.sha256` now omits its impossible
self-entry. Its completed SHA-256 is
`09c35ffd92d87a1034fa70cc5cd03b6dcd5d6fb5fb1729db69ca1bc695793e20`,
and `shasum -c` passes all 33 listed files. The amended VFR-08 implementation
receipt accurately explains that an inventory cannot contain its own stable
digest. No Low finding remains on that issue.

### Private real-worker body/cap feasibility passes

The candidate schema preserves `BROWSER_PRESET.surface_style="smooth"` while
including all four Diamond fields exactly once in snapshot, argv, canonical
identity input, and the returned job tuple. Changing each field changes the
identity, and depth 0.6001 is rejected.

In Chromium 151.0.7922.34, fresh real workers returned the exact identity,
source-hash, and lock-fingerprint tuple for both default Diamond jobs:

| Output | Worker-created to result | Compile to result | Probe | Result |
|---|---:|---:|---:|---|
| Body | 4,037.5 ms | 3,973.0 ms | 16.2 ms | exact VFR-08 body bytes |
| Cap | 2,615.9 ms | 2,549.2 ms | 16.0 ms | exact VFR-08 cap bytes |

Both are far inside the frozen 60-second ceiling. Their OpenSCAD logs report
Manifold `NoError`; the body reports genus 7 and the cap genus 0. No page error
was recorded.

### Public Diamond controls remain disabled; static smooth/mobile code is preserved

`main.mjs`, `openscad.worker.js`, `index.html`, `style.css`, and the dependency
lock remain at the previously frozen hashes. `main.mjs` disables the complete
`surface_style` select, disables every `diamond_*` input, disables the Diamond
option itself, and labels those fields `pending optimization`. P3's executed
assertions also observed the disabled select and option at desktop and 390 x
844. No public-control or service/deployment change occurred.

The unchanged main/index/style sources preserve the sticky 260 px mobile
preview, independently scrollable controls, sticky reachable Generate action,
toast/focus code, collapsed diagnostics, cancellation hooks, stale/download
logic, 180-second UI watchdog, and smooth browser preset. The focused Python
suite passes 17/17. These facts reduce regression risk, but they do not close
the dynamic gaps below.

## Findings blocking public enablement

### High — P1/P2 are missing prescribed final-mesh acceptance checks

`browser_gate.py::analyze()` checks file size/hash, vertices/faces, bounds,
volume, watertightness, winding, component count, Euler characteristic,
degenerate faces, edge incidence, and total triangle count. It does not check
the VFR-07 browser design's required exterior error `<=0.025 mm`, protected
envelope parity `<=0.05 mm`, wall/bore/thread/relief/floor/drain dimensions,
body/cap seam equality, or exterior-only triangle allocation. The P2 analyzer
also does not inspect the required effective cap bore, entry relief, 2.99 mm
floor, groove, drainage selection, and pair seam.

Byte identity with VFR-08 validly joins the drain, pose, dimensions, topology,
and mutual-exclusion evidence already present in the integrated candidate. It
does not create the omitted field-error and protected-parity measurements.
Neither the 26-entry integrated manifest nor the private browser manifest binds
an independent receipt that supplies those omitted measurements for these exact
browser bytes. The implementation receipt must not call the complete P1/P2
final-mesh gates passed until the distinct validator closes them on this
fingerprint.

### High — P3 does not perform the frozen smooth success and fail-closed sequence

The browser design requires a real smooth success followed by a control edit
that invalidates an enabled download. The P3 implementation instead loads the
page with `generated=null`, edits `outer_diameter`, and checks the already
disabled download. No real smooth worker result, rendered mesh, downloadable
bytes, or post-success transition occurs. That assertion cannot prove that a
successful smooth download becomes stale.

The fake late result uses `id=1` only after Cancel increments the active job id.
Production main rejects it at `if(d.id!==id)return`; the test never reaches the
identity/source/lock comparison. It therefore does not dynamically prove
fail-closed behavior for a matching job id with a wrong identity, source hash,
or lock fingerprint. Static source still contains all three comparisons, but
the prescribed browser path was not executed.

P3 also loads `dist/index.html` and its compiled assets, while neither the
15-entry private browser manifest nor the 26-entry integrated manifest records
those exact `dist` bytes. The current built JS asset differs from the prior
served bundle, as expected after the schema build, but the machine receipt does
not record its hash. Consequently the dynamic P3 observations are not bound to
the exact compiled page under review.

The validation toast, compiler-error UI, patched timeout, collapsed details,
mobile dimensions, disabled controls, and no-page-error assertions did execute.
They are useful partial evidence; they do not justify the receipt's blanket
`P3 passed` claim.

### High — the default Diamond output and repaired layout have no real-browser gate

The browser preset's output mode is `assembled`. P1 and P2 override it to body
and cap, so the most likely first Diamond job after public enablement has never
run in the real browser worker. There is no exact browser result for assembled
component/contact topology, combined bounds, identity/download bytes, or the
60-second ceiling.

There is likewise no real-browser Diamond `print_layout` result. The VFR-08
direct-WASM artifact proves the cap rotation and two separated components, but
the browser path has not compiled, transferred, parsed, or downloaded that
repaired layout. VFR-06 explicitly left assembly/contact, two-component layout,
native/browser parity, and exact download behavior as later required gates.
Body and cap success cannot substitute for these distinct output modes.

Public controls must stay disabled until at least the default assembled path
and repaired print-layout path pass under the same identity, byte, topology,
timing, stale/download, and independent-review rules. This is a functional
coverage blocker, not evidence that either output is geometrically defective.

### Medium — the claimed P0 byte-for-byte smooth snapshot/argv/identity oracle is absent

The browser design says the smooth default snapshot, argv, and identity must
remain byte-for-byte equal to the prior result. The harness records only the
new values and does not compare them with a frozen prior oracle. Moreover, the
prior smooth-only schema explicitly removed all `diamond_*` fields from
`JOB_ALLOWLIST`, while the new smooth snapshot and argv include those four
fields. Literal snapshot/argv/identity equality therefore cannot hold across
this intentional schema migration.

Smooth geometry can remain identical because `surface_style="smooth"` ignores
the Diamond field values, but identity semantics still change. Formal review
must explicitly replace the impossible byte-equality clause with an appropriate
migration check: preserve all prior smooth parameter values and output bytes,
record the expected new complete identity, and prove stale/download behavior
against that new identity. It must not silently mark the original P0 clause
passed.

## Requirement and risk coverage

| Area | Integrated critique result |
|---|---|
| VFR-07 drain High / REQ-05 | Resolved digitally; browser body bytes equal the seven-aperture VFR-08 artifact. Physical flow and strength remain open. |
| VFR-07 cap-pose High / REQ-10 | Resolved in source and VFR-08 layout artifact. Real-browser print-layout and slicing remain open. |
| VFR-08 hash Low | Resolved; repaired inventory passes 33/33. |
| Relationship B / REQ-08 | No source or browser-artifact regression detected; N33, 0.18 plateau, shared phase, and exact body/cap bytes are preserved. Physical visible seam remains open. |
| Threads/chamfers/protected dimensions | Source unchanged and VFR-08 artifact identity preserved. Browser analyzer does not itself close the prescribed detailed parity gate. |
| Private Diamond body/cap timing and identity | Pass: fresh real workers, exact tuples/bytes, 4.04 s and 2.62 s. |
| Public controls | Pass for current private state: Diamond remains visibly disabled and pending. |
| Smooth/mobile preservation | Static hashes and partial runtime assertions pass; real post-success smooth invalidation, matching-id tuple rejection, and compiled-asset provenance fail coverage. |
| Default assembled and print-layout browser outputs | Not run; blocks public enablement. |
| DfAM / REQ-13 | No new defect demonstrated. Support-free slicing, printed drainage, fit, strength, wear, and physical seam acceptance remain pending and must not be implied by UI enablement. |
| Delivery surface | Not evaluated; no deployment or served-route authorization exists. |

## Evidence and disposition

Commands run from the assigned roots included:

```text
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR09_CRITIQUE_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR09_CRITIQUE_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR09_INTEGRATED_CANDIDATE.sha256
shasum -a 256 -c scratch/vfr07-browser-implementation/CANDIDATE.sha256
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr08-implementation/hashes.sha256
cmp -s projects/laifen-wave-case/scratch/vfr07-browser-implementation/body.stl projects/laifen-wave-case/scratch/vfr08-implementation/diamond-bottom-body.stl
cmp -s projects/laifen-wave-case/scratch/vfr07-browser-implementation/cap.stl projects/laifen-wave-case/scratch/vfr08-implementation/diamond-bottom-cap.stl
PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider projects/laifen-wave-case/tests/test_vfr08_functional_repair.py projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
```

The focused suite passed 17/17. Manifest checks, exact byte comparisons, source/
harness inspection, browser-receipt inspection, and prior artifact joins were
read only.

Disposition: accept this fingerprint as private evidence that exact VFR-08
Diamond body and cap jobs fit comfortably within the real-worker ceiling and
retain their reviewed geometry. Do not enable public Diamond controls. Route a
focused browser-evidence repair that binds the compiled assets, performs a real
smooth success/stale cycle, exercises matching-id tuple failures, and covers
default assembled plus repaired print-layout outputs. The independent validator
must also close the omitted exterior-error/protected-parity gates on this exact
fingerprint or its explicitly refrozen successor before the formal join can
authorize any public-control change.
