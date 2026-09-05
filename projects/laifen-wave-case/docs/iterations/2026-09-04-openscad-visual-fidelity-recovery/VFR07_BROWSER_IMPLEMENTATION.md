# VFR-07 private browser implementation receipt

Status: **candidate PASS for private implementation evidence; no public
Diamond enablement or deployment**. This receipt does not approve the
candidate. Independent critic, validator, and formal review remain required
before any public control change.

## Frozen provenance and scope

- Owner: `/root/openscad_vfr07_browser_impl` (sole private browser implementation role).
- Input manifest: `inputs/VFR07_BROWSER_IMPLEMENTATION_INPUTS.sha256`, verified 10/10; fingerprint `9cd33521b07b792cd3a03af4d39001885b9f9f8dfa55d99f5015bb5abdfd7c54`.
- Source: `openscad/laifen_case_customizer_v1.scad`, SHA-256 `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.
- Candidate schema: `preview/openscad-wasm-simulator/src/schema.mjs`, SHA-256 `894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`.
- Focused tests: `tests/test_openscad_wasm_simulator.py`, SHA-256 `caab4001caf57e36ad3d54e0de366ecb02306cb462c3ea5e0b965568e3fae4eb`.
- Private harness: `scratch/vfr07-browser-implementation/browser_gate.py`, SHA-256 `57cbdc4bcf28b5bb86f40d75da30d87183926307e9f518b099f2449f0a3fe994`.
- Browser: Chromium `151.0.7922.34`, local HTTP only.

The only production change is `JOB_ALLOWLIST=ALLOWLIST` plus removal of the
smooth-only rejection in `schema.mjs`. Snapshot validation still applies all
existing enums, ranges, numeric constraints, and depth rejection. The test
file adds the complete allowlist contract. `main.mjs`, the worker, index, CSS,
vendor/runtime, lock, OpenSCAD source, services, and served bytes stayed
unchanged at their frozen hashes:

```text
main.mjs       98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353
openscad.worker.js fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845
index.html     997c2fbc80f453911c3ba68fed55ab17b3c9d2d56d7bb99ceee43a9e0ee82d6f
style.css      2da7d5b1e50db178ec6859f182a0b232e7d586654071cb9fa93af5c003a07530
dependency-lock.json 6d4a6b007f96b00752efd33cf1cf9e4eff5daaf82f011edd0655ea68c20e09b8
```

## Gates and evidence

P0 passed in the browser harness. The smooth preset remains smooth, all four
Diamond keys occur exactly once in the snapshot, `-D` argv, canonical JSON,
and the identity input. Changing each Diamond value changes identity, and
`diamond_depth=0.6001` is rejected. Existing focused tests passed **5/5**.

P1 passed with the default C1 Diamond values and `output_mode="body"` in a
fresh real worker. Worker-created to result received was **4037.5 ms**;
probe was **16.2 ms** and compile-to-result was **3973.0 ms**. Returned
identity, source hash, and lock fingerprint exactly matched the expected
tuple. All four Diamond argv assignments occurred once. The transferred and
download-equivalent bytes are `scratch/vfr07-browser-implementation/body.stl`
(`14,646,495` bytes, SHA-256
`6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8`). The
mesh is one positive-volume watertight, winding-consistent component with
Euler `-12`, 55,772 triangles, no degenerate faces, and every unique edge
incident exactly twice. Bounds are `[[-19.5,-19.49826809,0],[19.5,19.49826809,144]]`.

P2 passed only after P1 with a fresh real worker and `output_mode="cap"`.
Worker-created to result received was **2615.9 ms**; probe was **16.0 ms**
and compile-to-result was **2549.2 ms**. The returned identity tuple and
single-occurrence Diamond argv checks passed. The transferred and
download-equivalent bytes are `scratch/vfr07-browser-implementation/cap.stl`
(`10,978,686` bytes, SHA-256
`e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514`). The
mesh is one positive-volume watertight, winding-consistent component with
Euler `2`, 40,510 triangles, no degenerate faces, and every unique edge
incident exactly twice. Bounds are `[[-19.5,-19.49826809,0],[19.5,19.49826809,84]]`.

P3 passed on the unchanged production main with Diamond controls still
disabled: stale/download invalidation after a control edit, cancellation and
late-result rejection, validation toast and focus return, compiler-error
status/toast, timeout status, collapsed diagnostic details, sticky preview,
reachable Generate action, and 390 x 844 layout. No page errors occurred.

The complete machine receipt is `scratch/vfr07-browser-implementation/browser-gates.json`,
SHA-256 `ffd856ed003278d38c0314bb5ec3035fc77f918b002b5455239a1fc52dc9e11f`.

## Commands and boundaries

```text
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
5 passed
npm run build:openscad-simulator --workspace laifen-wave-case
vite build completed
uv run python projects/laifen-wave-case/scratch/vfr07-browser-implementation/browser_gate.py
PASS; Chromium 151.0.7922.34; P1 4037.5 ms; P2 2615.9 ms; P3 PASS
```

The build was local candidate preparation only; no `dist` bytes were served
or deployed. CAD, written-artifact/slicer, physical fit, strength, drainage,
and public hosting acceptance remain outside this role. Route this exact
candidate fingerprint and receipt to distinct independent critic and
validator owners, then to the formal reviewer. Keep public Diamond controls
disabled until that join passes.
