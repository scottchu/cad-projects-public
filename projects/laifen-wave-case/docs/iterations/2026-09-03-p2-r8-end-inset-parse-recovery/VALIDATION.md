# VAL-GCS-R8-01 independent validation

**Verdict: BLOCKED.** The one-character R8 parse repair loads cleanly and establishes a useful desktop/mobile behavior baseline, but the exact frozen candidate has independent contract failures. Under the R8 rule that a newly found runtime defect stops recovery rather than widening it, this candidate must not advance to formal PASS or delivery.

## Frozen provenance and scope

- Owner: `/root/gcs_r8_validator`, independent of implementation and critique.
- Exact candidate manifest: `CANDIDATE_MANIFEST.sha256`, SHA-256 `59f9aa1438f185979a47f888988833647aff43a1959969e13f54d1217431d655`; all five entries verified before and after validation.
- Implementation evidence manifest: SHA-256 `e657038fae39820cffa3802e9df4f0f48deacec02ceb347433b00380f63cdb10`; all entries verified.
- Validation input manifest: `VALIDATION_INPUTS.sha256`, SHA-256 `da34cb86de3e9c13d8d00ce50ede25ef3b420610a14d949061d311e5a04caadd`; all 25 entries verified after execution.
- Candidate source and project tests were read-only. Writes are limited to this receipt, the validation input/evidence manifests, and `scratch/r8-validation/`.
- One validator-method retry was used. The first browser runner attempted to drive `#formHeight`, discovered that the required control is absent, and stopped before completing desktop. The repaired runner omitted that nonexistent drive and recorded the missing control as a candidate finding. No candidate byte or threshold changed.

## Checks that passed

- The unchanged command `node projects/laifen-wave-case/tests/test_text_label_generator.mjs` exited 0 with `R6 text label generator analytic checks passed`.
- The independent math/static probe completed 64 checks: 57 passed and 7 failed. Presets, screw and bayonet accounting equations, camera fit, safe-text allowlist, round support, polygon 3/5/6/7/8 and rounded/rotated maximum radius, all pattern functions, pattern envelope weights, transformed-coordinate phase equations, label family/weight boxes, and declared accessory envelope nondecrease passed.
- Fresh Playwright Chromium loaded the exact local page at desktop `1440x1000` and mobile `390x844`. It completed 164 assertions: 138 passed and 26 failed, representing the same 13 candidate failures at both viewports.
- The valid browser matrix retained a canvas, exactly two named core meshes, and a camera fit for Laifen and wide-short presets; screw and bayonet modes; round and polygon 3/5/6/7/8, rounded and rotated variants; every valid end family; smooth, blunt diamond, shallow helix, wave/flowing flutes, knit, recessed diamond, straight micro flutes, and rugged hex; all four envelopes; every accessory selector; and text inset/outset, family, weight, size, orientation, target, angle, axial placement, and patch toggle.
- Unsafe HTML text and invalid OD cleared both core meshes, fit/envelope state, detail output, and field-associated errors. No injected HTML node appeared.
- All controls that exist are inside labels and become visible when their details groups are opened. The responsive mobile layout had no horizontal overflow. The main viewer has an accessible label, status is live, and the static `true scale`/magnifier disclosure is present.
- Zero page errors, zero failed requests, and zero console errors occurred. Four Chromium `GPU stall due to ReadPixels` messages were performance warnings only and are not treated as runtime errors.

## Blocking findings

| ID | Severity | Finding and evidence |
| --- | --- | --- |
| R8-V01 | P1 | Closure controls change accounting but not the model. With a smooth/flat/no-accessory state, two distinct screw settings produced identical canvas hashes at each viewport; two distinct bayonet settings also produced identical hashes. `app.js` contains no thread/lug/bayonet annotation builder, and the required `formHeight` control is absent from HTML. The browser therefore cannot validate closure form, lug count, capture, ramp, or clearance sensitivity. |
| R8-V02 | P1 | Declared `OD`/total envelope is exceeded by outward patterns. At `OD=60`, blunt diamond and shallow helix produced a measured horizontal box of `60.9000015` mm while the readout remained `60.00`; wave flutes measured `60.8999252`, knit `60.8416138`, and rugged hex `60.8179474`. The shell adds positive relief to `sectionSupport` instead of keeping relief inside the across-corners envelope. |
| R8-V03 | P1 | All five non-none accessory modes render the same torus. Their canvas hashes are identical within each viewport, although the UI names eyelet, captured loop, separate clip link, keyring tab, and bridge handle. This does not validate optional accessory identity or the keyring/bridge parameters. |
| R8-V04 | P1 | End-family bounds are not enforced. Flat with nonzero size, chamfer and rounded fillet with size `4 > F=3`, and dome with size `31 > OD/4=15` all remained valid with two meshes at both viewports. The required invalid-state clearing never occurred. |
| R8-V05 | P1 | Locked bayonet pattern alignment is not implemented in the rendered transform. Pure math passes only when upper samples are evaluated at `theta - closureRotation`; the renderer never rotates either piece and instead evaluates the upper field directly with positive phase compensation. The match toggle changes pixels, but the `match locked phase` view does not apply the contract's world/local transform needed to establish alignment. |
| R8-V06 | P2 | A `textTarget=both` patch suppresses texture only under the upper label. The independent sample at the lower label center retained nonzero shallow-helix relief, while the upper label center cleared to zero. |
| R8-V07 | P2 | `mountAngle=NaN` with a bridge handle is accepted as valid. The required finite accessory placement validation is absent, allowing invalid placement values into the render path. |

## Visual review and baseline evidence

The wide-short bayonet is framed within the canvas at both viewports, and mobile stacks preview, controls, and readout without horizontal clipping. Its seam and polygon section are visible, but there is no visible bayonet lug/slot/ramp geometry. Expanded desktop/mobile captures also show invalid-state clearing and all existing controls. Screenshots and machine-readable state evidence are under `scratch/r8-validation/`; `browser-results.json` has SHA-256 `4fb37dd7a4f935af3dcce77a27ea20dba9c00a13ae9614a5ed21d721cc70de1` and `math-results.json` has SHA-256 `aa547dbcdf0c907d360572dd5b37c7b1fb5b77aec121049f90716d539932928b`.

## Protected scope and boundaries

- P1 R7's candidate manifest remains SHA-256 `8d3941772cca549846937dcad6ce4a05e06f5bba104c261668a0cf747c62b6a1`; every repository-resident entry verifies, and `print_layout.step` remains `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`. Six old `/tmp` photo attachments listed by that historical manifest are no longer present, so full external-input replay is unavailable; this is not repository candidate drift.
- P2 R3's five-entry candidate verifies and its manifest remains `15c7c0503e87ec0f0b1a828fb62d471baaefc9a6caecf629d14d4504d0d19224`. P2 R4/R5 BRIEF, DESIGN, and frozen-input manifests match the before-test protected manifest. No protected hash changed after execution.
- Validation used only an ephemeral loopback server on `127.0.0.1:8984`, which was stopped. No Tailscale route, launchd service, served P2 R3 bytes, CAD Viewer route, source, CAD, OpenSCAD, STEP, slicer, printer, continuity file, or Git state was changed.
- This is browser visual-intent evidence only. It does not validate CAD solids, real screw or bayonet geometry, OpenSCAD generation/font availability, mesh/export parity, slicing, printability, fit, strength, wear, drainage, or physical acceptance.
- Independent drain placement `none|bottom|top|both` and schema-driven parameter modules are explicit future-revision scope. Their absence is not an R8 finding.

## Commands

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r8-end-inset-parse-recovery/CANDIDATE_MANIFEST.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r8-end-inset-parse-recovery/IMPLEMENTATION_EVIDENCE_MANIFEST.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r8-end-inset-parse-recovery/VALIDATION_INPUTS.sha256
node projects/laifen-wave-case/tests/test_text_label_generator.mjs
node projects/laifen-wave-case/scratch/r8-validation/math_validate.mjs
.venv/bin/python3 -m http.server 8984 --bind 127.0.0.1
.venv/bin/python3 projects/laifen-wave-case/scratch/r8-validation/browser_validate.py http://127.0.0.1:8984/projects/laifen-wave-case/preview/p2-r6-text-label-system/index.html
shasum -a 256 -c projects/laifen-wave-case/scratch/r8-validation/protected-before.sha256
```

Next action: retain these browser captures/results as the R8 behavior baseline and address the P1/P2 findings only in a newly frozen revision with fresh implementation, validation, critique, and review chains.
