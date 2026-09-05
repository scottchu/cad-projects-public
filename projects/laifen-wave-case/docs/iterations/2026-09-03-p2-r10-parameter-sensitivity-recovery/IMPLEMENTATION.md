# IMP-GCS-R10-01A/B receipt — noncandidate stop

**Status:** STOPPED NONCANDIDATE at Phase B.  Phase C was not started.

## Provenance

- Frozen R10 input manifest verified with `shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r10-parameter-sensitivity-recovery/inputs/frozen-inputs.sha256` before implementation.  Its required R9 evidence and R10 intake entries all returned `OK`.
- Design fingerprint supplied to this workstream: `7dc696650c828aa0705c2fd8f67c23a3036f04bba10f5078500950dea233864c`.
- Writes are limited to the R10 preview namespace, the three completed authorized test paths, and this R10 receipt. No R6–R9, live P2 R3 route/service, CAD, OpenSCAD, export, slicer, printer, or continuity record was changed.

## Work completed

Phase A passed after one focused repair to give straight micro flutes a distinct finite sampler signature:

```sh
node projects/laifen-wave-case/tests/test_p2_r10_schema_coverage.mjs
# R10 schema coverage passed: 83 fields + canonical split-percent projection
node projects/laifen-wave-case/tests/test_p2_r10_geometry.mjs
# R10 geometry gates passed
```

The pure-model namespace contains 83 schema fields (including `surface.keepout`), coverage records plus a split-percent projection, named flatten names, active-value validation, exact result/null shape, immutable JSON descriptor construction, pattern sampling, profile paths, coaxial bayonet data, drain masks, safe label policy, and accessory primitives.

## Stopping gate

Phase B began descriptor sensitivity testing. Its initial run found an invalid end-profile witness. Repair 1 supplied a companion positive end size after a profile change. Repair 2 constrained the end-size alternate to its profile-specific bound. The mandatory rerun still fails:

```text
AssertionError [ERR_ASSERTION]: ends.top.profile A valid:
[{"path":"ends.top.size","id":"flat-size","message":"Flat end size must be zero."}]
```

The remaining witness setup applies `linked:false`, `top.profile:"chamfer"`, and `top.size:1`, then overwrites the profile with `flat` without clearing the companion size. This is a valid validator rejection, but it prevents the required valid A/B sensitivity pair. The iteration ceiling allows an initial attempt and at most two focused repairs. Both repairs have been used, so this implementation owner did not make a third repair and did not begin renderer/UI/browser work.

## Coverage and risks

- Phase A: 83 schema leaves and 84 coverage rows (the extra row is the split-percent projection) passed schema and geometry gates.
- Phase B: descriptor sensitivity is failing before coverage count can be claimed; no frozen candidate exists.
- Phase C: no renderer, HTML, CSS, browser service, screenshots, or browser test was created or run.
- Independent validation, critique, review, delivery, fabrication, and physical acceptance remain pending and cannot use this noncandidate.

The smallest next action requires an explicit reopened or reduced contract from the coordinator. It should fix only the `ends.top.profile` A-pair setup and rerun Phase B before any renderer work.
