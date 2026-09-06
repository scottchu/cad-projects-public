# SP-VAL-01 — independent surface-pattern validation

## Verdict and provenance

**Deterministic source, state, build, and scoped mesh gates pass. Full validation remains pending.** Candidate 03 is not yet approved for UI acceptance because the required current browser jobs and held-real-worker cancellation race could not run after the browser transport closed. The whole-solid nonadjacent-self-intersection and geometric vertex-on-edge T-junction requirements also remain open; the completed exact-edge topology and exterior field audits do not substitute for those checks.

The final candidate manifest is `inputs/candidate-03.sha256`, SHA-256 `412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`. All 23 paths verified before and after validation. Revised contract hashes are BRIEF `5df06828d9794d6fd75e0cce4412858f4ded86ef6d3f6241f47090fd77f3d5bd` and DESIGN `176bb99dc05b08b52ae757682b8f70ae1ccdf8a3e470a89476dfad4701e3d924`. Authoritative SCAD stayed `517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`; worker `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`; dependency lock `6d4a6b007f96b00752efd33cf1cf9e4eff5daaf82f011edd0655ea68c20e09b8`; pinned JS/WASM `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` / `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.

## Deterministic gates

- Candidate 03 Node state/lifecycle tests: 32/32 pass. These cover Smooth default/Reset, raw Diamond selection, exact fixed tuple, schema/adapter/draft shared preflight, wall and literal triangle boundaries, direct versus coupled error ownership, no automatic generation, cancellation, stale and superseded events, tuple mismatch, duplicate result, exact Blob bytes, drain/count preservation, and existing compact controls.
- Relevant Python source/geometry contracts: 12/12 pass.
- Independent math oracle passes the complete browser OD tenth-grid: Diamond count 17..68, actual arc pitch 3.529671746..3.732951271 mm, developed plateau 1.023699639..1.060821729 mm, slope 0.29296875, and W4.4 residuals body 3.95 / cap 3.45 / female-thread 1.80 / entry-relief 1.90 mm. Default estimates are body 119,328 and cap 74,448. Fixed pitch/arc/depth/phase mutations are rejected.
- The N68 source boundary was executed independently through the pinned WASM hidden-math branch, so all top-level SCAD assertions ran without constructing a large mesh. Isolated role heights 136.7 and 136.799999999 mm pass; literal 136.8, 136.8000000001, and 136.9 mm fail the exact source assertion. Candidate 03 matches it: manual cap slider max 136.7; cap 136.8 fails; body 136.7 passes and 136.8 fails. This found and closed Candidate 01's epsilon mismatch.
- The final isolated production build completed in 536 ms at `/tmp/surface-pattern-validation/early-build-backup`. All six files served at temporary port 5181 were byte-identical to that directory. Product `dist` and private 8453 were not changed by validation.

## Actual compiled meshes

Because SCAD, worker, lock, and pinned runtime are byte-identical, the baseline-preparation default Diamond compilations remain exact geometry evidence for Candidate 03:

| Output | Time | Triangles / components | STL SHA-256 | Result |
| --- | ---: | ---: | --- | --- |
| body | 2.625 s | 55,772 / 1 | `6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8` | closed, positive; Bottom N7 gives 8 section loops |
| cap | 2.123 s | 40,510 / 1 | `e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514` | closed, positive; one closed-floor section loop |
| assembled | 6.558 s | 96,100 / 2 | `5cfe2f06339bcc3df70dbc7072448789e5078aee9998a6599016298a148260fe` | closed, positive; volume sum delta `-1.98e-9 mm3`; expected native retessellation of 182 triangles |
| print layout | 5.472 s | 96,282 / 2 | `73dc750bd9bea35d1e65e4cd05ec7a56b1cc5cdd42faf8a1649455694d83062e` | closed, positive; exact constituent triangle and volume sums |

All have zero non-two-use edges and zero degenerate faces. Default body/cap preserve the 15/15.5 mm bores, 0..3 / 81.01..84 mm off-hole floor intervals, 19.05..19.50 mm patterned relief, and 99 exact shared seam XY vertices. Compared Smooth witnesses remain distinct while protected bores and floors are unchanged. Exhaustive classification of every identified radial-side triangle at vertices, three edge midpoints and centroid covered 138,864 body and 88,440 cap samples; maximum analytic field error was 0.012887 mm, below 0.025 mm.

One new usable wide/short case used the actual Candidate 01 mapping before the JavaScript-only repairs: UI D39/H60/W4.4/T4/Auto/both/N17/Diamond/print layout, OD47.8 and lid 26.082191781. The exact tuple is unchanged in Candidate 03. It compiled in 2.194 s to 23,731,286 bytes, SHA-256 `4f42c45b9a847f5de188359cbe710b0d631450901a70173aec4f1e371c7d3041`. Its two actual parts have 42,244 body and 37,854 cap faces; each is watertight, winding-consistent, positive-volume, and has zero non-two edges, degenerate faces, or duplicate faces. Independent sections find 17 through openings on each end. Exterior classification covers 59,532 body and 39,032 cap samples with maximum error 0.010306 mm.

The attempted independent broad-phase whole-mesh triangle intersection scan did not complete within its bounded 95-second allocation and was interrupted without a verdict. Therefore no comprehensive whole-solid nonadjacent-self-intersection claim is made. Two-use edges prove closed topology, but do not exclude a geometric T-junction where an unrelated vertex lies in another edge. A later validator needs a bounded global certifier or the design must explicitly narrow these requirements to the source-native/exterior evidence available here.

## Browser and lifecycle harness

The isolated harness at `/tmp/surface-pattern-validation/harness` is bound to Candidate 03. `binding.json` SHA-256 is `66ae139cdfe32a971633f981bddc82c5d881f60428e2f079a656141c64e38191`. The served page imports the exact Candidate 03 controller `671fb5aaf0406be79a75b07dd0f694177e6cbf61cda517315efd3b9e63d8c311`, lifecycle `62f6d413af9347e36e1992cde3c189140821e86b83f862a2877fdb34cbd5e60b`, schema `9a2dca8b1431ed161a510f5b6c08ea9f20227874d8915c2978528550b9241cbe`, source, lock, real worker, and pinned WASM. Its only wrapper intercepts a genuine completed worker result, records exact id/identity/source/lock/byte hash, and lets visible controls deliver that same result after actual controller Cancel or after a newer actual job. Visible checks compare status, current flag, viewer install, Blob count/hash, and download href before and after stale delivery; the accepted newest job requires identical held/view/Blob hashes. It does not mirror ownership logic.

All 12 harness HTTP dependencies returned 200 at port 8461 with local byte parity, including source, lock, transformed harness index, harness module, controller/lifecycle/schema/adapter/bounds, worker, and both vendor files. The harness remained unexecuted: native Safari first failed `cgWindowNotFound`; Chrome briefly established Candidate 02 Smooth and duplicated-error observations, then the entire computer-use transport closed before Candidate 03 or the late-result sequence. Candidate 02 screenshots cannot validate the repaired Candidate 03 error or its browser behavior.

The replay source is retained at `tests/browser/surface-pattern-harness/` so
this gate does not depend on the temporary directory surviving a reboot. Its
`HARNESS_INPUTS.sha256` has SHA-256
`4b423fb84367a3a08c045da92119988f0dc0c7aa7079fe37e75edb9392581ca2`
and verifies the Candidate 03 manifest plus the generator, browser module,
CSS, and README. `node --check` passes for both modules. The README gives the
exact repository-root generation and root-venv server commands; generation
copies verified inputs only into caller-selected `/tmp` output and retains no
vendor, mesh, log, page, or screenshot in the repository. This durability
check is source/syntax evidence only and does not close the manual browser
sequence.

Required pending browser evidence is Candidate 03 at 1280x900 and 390x844: default Smooth, Diamond selection/no auto-run/stale invalidation, W4.3 error and W4.4 repair, N68 triangle error and repair, focus-visible cards and single error announcement, all four real jobs with render/download identity, responsive reachability, and the harness Cancel/late/superseded/latest sequence. Chromium evidence can close Chromium only; native Safari remains unverified.

## Evidence and commands

Primary receipts: `readiness.json` `3c4b5c2c5fe3256ebd59b3211fc77d605d7169ca0e4d78924e1911bf433476a3`; `default-field-audit.json` `389029c9930d7feb1a1f948a52dc0392270473727d512adb0b7871b019025d52`; `wide-compile.json` `404109742ef28895ff47943ff84526b9ac6ce84e7b254608f9bd0221167620f9`; `wide-mesh-audit.json` `0c113137f604d843ada6a8c750c6b08dd84c14bb7fcfb20687aa839fea2b4bb9`; `triangle-guard.json` `7df733a188a888f2c6e89d6ee05645ddfb3e018582fae5889bf6a07ddabb54bb`; final `math-oracle.json` `e6423136dcb2414b72575cb5ee3f59e0fd0e6d3e778e7099f2cfd60881e973b5`; harness module `420a98966a03339a6601022fd484ffe12e6bbfdce80af16a7c2413f9debf24f4`.

Commands run from the repository root included:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-surface-pattern/inputs/candidate-03.sha256
node --test projects/laifen-wave-case/tests/node/compact-controller.test.mjs projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs
PYTHONDONTWRITEBYTECODE=1 uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_vfr08_functional_repair.py -p no:cacheprovider
node /tmp/surface-pattern-validation/triangle_guard_probe.mjs
node /tmp/surface-pattern-validation/math_oracle.mjs
node /tmp/surface-pattern-validation/compile_wide.mjs
uv run python /tmp/surface-pattern-validation/default_field_audit.py
uv run python /tmp/surface-pattern-validation/wide_mesh_audit.py
npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir /tmp/surface-pattern-validation/early-build-backup --emptyOutDir
```

CAD/STEP remains the existing P1 R7 authority. Slicing, supports, grip, drainage in use, thread wear/strength, printing, fit, and physical acceptance were not evaluated. No printer, Tailscale, dependency, source, product build directory, or private-service mutation occurred in this validation.
