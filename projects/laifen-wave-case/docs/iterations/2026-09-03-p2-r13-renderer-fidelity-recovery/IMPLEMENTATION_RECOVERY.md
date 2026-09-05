# IMP-GCS-R13-01 implementation receipt

**Status:** implementation PASS; candidate is frozen for independent validation and critique. This is a conceptual browser-intent artifact and does not grant delivery or product acceptance.

## Provenance and scope

- Verified frozen R13 design fingerprint: `3a322e3d836cb07fa44600feba4b27ada6c91c07e90015b0184edcb62a3fc42d` from `inputs/frozen-inputs.sha256`.
- Candidate manifest fingerprint: `9f79d2ca92c04a159ff8a79c5279dfa00fe9d0b5bb2c6f16d639be26bfc9c468`.
- Verified nested R12 candidate, implementation, validation, and critique manifests before work. The R12 core remained imported read-only.
- Descriptor sufficiency PASS: section supports, closure primitive, end paths, surface field and relief facts, drain masks, label primitives, attachment primitive/bounds, envelope facts, and split projection cover all 84 ordered render rows. No descriptor gap and no core edit.
- Created only the permitted R13 preview, five R13 tests, and this R13 role evidence. No continuity record, R12 source/test/evidence, route, service, CAD, OpenSCAD, STEP, export, slicer, printer, or physical record changed.

## Candidate behavior

- The descriptor-only renderer emits eleven named R13 surfaces and one visible semantic target per active canonical field. Polygon plans use the frozen support samples for every side count 3 through 32; closure, ends, surface field, drains, labels, and attachments consume descriptor geometry rather than raw state or effect tokens.
- Basic displays 14 default active Basic fields; Advanced displays the 13 active relevant Advanced fields in addition. `[hidden]` has an explicit `display:none!important` rule. Invalid active input clears the sheet transactionally.
- The persistent disclosure says: “Conceptual descriptor preview only — not CAD, OpenSCAD, or a printable/exportable model.” The fit-to-view/not-calibrated disclosure remains separate.

## Executed evidence

All cheap gates passed before browser execution:

```sh
node projects/laifen-wave-case/tests/test_p2_r13_target_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r13_render_observability.mjs
node projects/laifen-wave-case/tests/test_p2_r13_visual_families.mjs
node projects/laifen-wave-case/tests/test_p2_r13_ui_contract.mjs
```

Results: descriptor-only surface/target contract PASS; **84/84** ordered target hashes changed; all 30 polygon silhouettes plus required rotation/roundness variants were unique; categorical closure/end/pattern/envelope/relief/label/attachment/drain families were unique; tier and disclosure contract PASS.

Frozen R12 regressions were rerun before candidate freeze:

```sh
node projects/laifen-wave-case/tests/test_p2_r10_schema_coverage.mjs
node projects/laifen-wave-case/tests/test_p2_r10_geometry.mjs
node projects/laifen-wave-case/tests/test_p2_r10_descriptor_sensitivity.mjs
node projects/laifen-wave-case/tests/test_p2_r10_renderer.mjs
```

All passed. The R12 compact audit also passed in an isolated temporary mirror and its regenerated `audit.json` and `SUMMARY.md` matched frozen bytes exactly: **84/84** coverage and **58/58** inactive poison.

```sh
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r13_browser.py
```

Chromium, Firefox, and WebKit passed at 1280×900 and 390×844 with no page errors, horizontal overflow, stale invalid output, or visible hidden controls.

## Retry accounting and next action

Two focused renderer corrections were used: the minimum-wall witness now consumes descriptor minimum-wall rather than residual wall, and axial/arc pitch witnesses now consume sampled descriptor field values. A test-only syntax typo was corrected before the family test executed. No unresolved implementation failure remains.

Independent `VAL-GCS-R13-01` and `CRIT-GCS-R13-01` must review this exact candidate fingerprint, followed by `REV-GCS-R13-01`. No live route or served copy is authorized.
