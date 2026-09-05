# OSW-03 independent app critique

**Date:** 2026-09-04  
**Owner/role:** `/root/render_controls_critique`, independent application critic  
**Candidate input fingerprint:** `2fc5dff7f37e3ca82dceae56427a4dc21802d57c081f3962b248b83a8ff856da`  
**Verdict:** **BLOCK**. The static build is reproducible, but the delivered browser app cannot currently initialize the pinned OpenSCAD engine and has stale-result and parameter-parity defects.

## Scope and provenance

This review inspected the frozen OSW BRIEF/DESIGN/HANDOFF, the OSW-02 implementation receipt, the app source, focused tests, and the locked local vendor files. The authoritative SCAD was inspected only for app source/default parity; its independent geometry review is separately blocked by OSC-04 and is not re-evaluated here.

Reviewed source hashes:

```text
dependency-lock.json       6d4a6b007f96b00752efd33cf1cf9e4eff5daaf82f011edd0655ea68c20e09b8
setup-openscad-wasm.mjs    1be2dd1423d32d4a793fdde6890e4a65e71eb80d4205f86789d2998015b1294e
schema.mjs                 eb03ccc492de19a60f4ccd5059b42236063f2320973f1a03fa85713620d0afab
main.mjs                   0a4fe9643d26ed839cf1a9866f6769aec640feb39f94dc205e62139b7cea51f4
openscad.worker.js         d59042683855dfe0f735dcfd8e541f622c3d4a04b6a1e74cadf72c1411a3b141
test_openscad_wasm_simulator.py
                            f7dfc11fd2b64e1f0a1e6dcb826d431efa32a551b93a28ba5434139900ea560
laifen_case_customizer_v1.scad
                            7f5aa5a7adf854a6d23ba3c931e4ed4b4b8530dd48cfd12f32928b1cef743c89
vendor/openscad.js         904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e
vendor/openscad.wasm       f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26
```

The vendor files match the dependency lock. The focused test result was:

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
...                                                                      [100%]
```

The Vite build also passed with the locked assets:

```text
npm --workspace laifen-wave-case run build:openscad-simulator
vite v6.4.3; 10 modules transformed; built in 515ms
```

The build check does not execute the worker or compile a real STL.

## Blocking findings

### P1 — the worker never obtains the official ESM factory

`workers/openscad.worker.js:3` dynamically imports `vendor/openscad.js`, then
looks only at `self.createOpenSCAD || self.OpenSCAD || self.Module`. The locked
vendor file is an ES module ending in `export default OpenSCAD;`; its default
export is returned by `import()` and is not installed on `self`. A real worker
therefore throws `official OpenSCAD factory unavailable` before `callMain`.

Smallest repair: retain the relative dynamic import but capture its namespace,
then select `moduleNamespace.default` (with any documented fallback only if the
locked engine actually provides one). Add a real-browser smoke that initializes
the worker and compiles one smooth job before accepting the candidate.

### P1 — `minimum_wall` is not the source parameter `wall`

`src/schema.mjs:1,4-8` exposes and serializes `minimum_wall`, while the current
authoritative SCAD declares `wall`. OpenSCAD accepts the unknown override but
the wall control does not change the source geometry. This violates source,
default, and control parity and makes the UI misleading.

Smallest repair: rename the browser key to `wall` everywhere, or explicitly map
the public `minimum_wall` control to `wall` in the serializer and prove the
binding with a source/schema test. Keep the public label/reference wording
clear if the value remains a design minimum rather than a measured wall.

### P1 — stale STL remains downloadable after edit, cancel, and compiler error

`src/main.mjs:3,5-6` marks a result stale when controls change, but leaves the
previous `href` and `download` attributes active. `cancel` and the worker error
path also leave the previous link enabled. A user can therefore download an STL
that does not match the visible current controls, contrary to the job contract.

Smallest repair: centralize `invalidateResult()` and call it on edit, cancel,
error, and reset as required by the contract. Revoke the old object URL, remove
the active download target, and set `aria-disabled`/keyboard reachability until
the current job succeeds.

### P1 — result identity is computed without the dependency-lock fingerprint

`src/schema.mjs:8` hashes SCAD bytes and parameter JSON only. The design contract
requires SCAD bytes, dependency-lock fingerprint, canonical parameters, and
output mode. Although output mode is included in the parameter object, engine
provenance is absent; changing the pinned WASM while retaining the same source
and parameters can produce the same displayed identity.

Smallest repair: import or build the locked dependency fingerprint into the
canonical identity input, and make the result/download/readout use that exact
record. Add a test that changing the lock fingerprint changes identity.

## Important secondary findings

* **P2 — late identity is not checked.** `main.mjs:6` rejects a different job id
  but accepts a current-id result with a mismatching `identity`. Check both id
  and canonical identity before parsing/installing bytes.
* **P2 — setup replacement is not atomic.** `setup-openscad-wasm.mjs` removes
  the existing vendor directory before renaming the verified staging directory.
  An interruption after removal loses a valid cache. Rename the staged directory
  into a versioned destination and replace the pointer/directory atomically,
  preserving the prior verified cache until the replacement is complete.
* **P2 — constraint validation is incomplete.** `snapshot()` checks finiteness,
  scalar ranges, enums, and one OD/wall inequality, but does not mirror the
  source/Python cavity budget, split/thread interval, drain reach, chamfer, or
  support constraints before starting a job. OpenSCAD assertions remain final,
  but the browser contract calls for equivalent cheap preflight checks.
* **P2 — generated Three resources leak.** Replacing the mesh removes the old
  object from the scene but does not dispose its geometry or material. Blob URLs
  are revoked only on the next successful result, not on cancel/edit/error.
* **P2 — viewer framing and identity are incomplete.** The camera is fixed to a
  hard-coded target; it does not frame compiled STL bounds or show axis,
  orientation, output identity, or full result identity as required. Wide/short
  variants can be clipped or poorly framed.
* **P2 — required failure/accessibility behavior is incomplete.** WebGL renderer
  construction is unguarded, so WebGL failure can prevent the controls/download
  fallback. Inputs have no `aria-describedby` error association or persistent
  units/ranges, and no reduced-motion handling is present. Real 360 px keyboard,
  screen-reader, CSP, and mobile delivery checks were not performed.
* **P3 — state staging is only partial.** The worker reports `loading`,
  `compiling`, and `parsing`, but no explicit `ready` state. This is secondary
  to the initialization block.

## Passing checks and boundaries

The app uses a module worker with route-relative Vite URLs, an allowlisted array
of `-D` arguments, quoted enum values, finite numeric parsing, job termination
for supersede/cancel, and the same returned STL bytes for `STLLoader` and the
download path. Vite bundled the local Three/OpenSCAD assets and emitted no
external runtime dependency in the inspected source.

These static passes do not prove that the browser can execute OpenSCAD. The
SCAD geometry itself remains a separate OSC-04 BLOCK; this critique does not
approve or repair that source. No STEP, slicer, printability, fit, or physical
acceptance claim follows from this app review.

## Repair order and re-review gate

Repair the factory import, source parameter mapping, download invalidation, and
identity provenance first. Then add real-browser worker/STL smoke and rerun the
focused state, parity, and dependency tests. Before delivery, independently
verify cancellation/supersession/late identity, exact-byte download parity,
mobile/accessibility behavior, CSP/MIME headers, bounds framing, and cache
replacement recovery. The candidate remains BLOCK until those gates pass on a
single updated fingerprint.
