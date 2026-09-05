# Brief

## Objective

Recover visual fidelity of the live Laifen Wave case preview while retaining OpenSCAD WASM as the sole geometry authority. The preview should communicate the same component identity, diamond texture, and seam relationship as the printed/reference case, without manufacturing a look-alike in Three.js.

## User-visible contract

- On mobile, keep the canvas fixed or sticky at the top of the viewport.
- Let parameters scroll independently beneath the canvas.
- Keep `Generate` easy to reach with a sticky action affordance.
- Present errors as an accessible toast with concise, actionable text.
- Keep raw diagnostic output in collapsed details for inspection.
- Filter or demote localization warnings when they are non-fatal; preserve and surface real errors.

## Geometry contract

- OpenSCAD WASM is the only geometry authority for generated and downloadable closed geometry.
- Three.js may display OpenSCAD output and a component-aware, closed preview seam, but may not fake or deform case geometry.
- A display-only seam treatment must not corrupt the downloadable closed geometry.
- Verify the existing diamond manifold, including the `N34` crest versus `N33` valley and `0.18` plateau hypotheses, before any source change.
- Verify the broad smooth collar relationship (body 2 mm before seam; cap 11 mm above seam) before changing texture or seam parameters.

## Staged DAG

### VFR-02 — Read-only diamond manifold benchmark

Allowed reads: current project continuity records, OpenSCAD source, existing benchmark/test artifacts, and the supplied reference evidence. Allowed writes: this iteration's benchmark receipt and derived read-only notes only. Forbidden: production source edits, generated artifact replacement, UI implementation, slicer/printer/public actions.

Done gate: a frozen benchmark identifies the current manifold's source revision, measured crest/valley/plateau/seam relationships, component identities, and a SHA-256 candidate fingerprint. It records whether each hypothesis is confirmed, rejected, or unresolved.

Role: independent geometry investigator. The investigator must not approve an implementation.

### VFR-03 — Cheap 2D seam/pattern intent gate

Dependency: VFR-02 done.

Allowed reads: VFR-02 receipt and frozen current source/reference evidence. Allowed writes: a small reviewable 2D/customizer gate and its validation record under this iteration. Forbidden: 3D CAD/BREP edits, STEP/mesh/slicer/print work, and production UI integration while the gate is open.

Done gate: the user can inspect one or two isolated relationships: component identity and the seam/diamond pattern relationship. The gate plainly states what is fixed, what is adjustable, what action to take, and asks an explicit pass/fail. The user's exact confirmation or rejection is recorded.

Role: intent-gate designer, distinct from VFR-02 and VFR-04.

### VFR-04 — Implementation after user pass

Dependency: VFR-02 done and VFR-03 explicitly passed by the user.

Allowed reads: frozen benchmark, passed intent record, current production source, and requirements. Allowed writes: implementation source, focused tests, review artifacts, and continuity records in this iteration. Forbidden: fake Three.js deformation, altered downloadable closed geometry outside OpenSCAD, MakerWorld/public release, printer actions, or production registration.

Done gate: the mobile layout and diagnostics contract is implemented; OpenSCAD output remains authoritative; component-aware closed preview/display-only seam behavior is proven; localization warnings are filtered/demoted and real errors remain accessible; focused math, geometry, constraint, requirement, source/export parity, and visual checks pass; an independent reviewer signs the result.

Role: implementer. Critic, validator, and reviewer must be distinct identities from the implementer.

## Candidate and provenance

Current candidate fingerprint: `PENDING_ROOT_HASH`.

Every later receipt must name the exact source revision, immutable input manifest, generated artifact paths, commands actually run, hashes, and separate CAD, artifact, and physical acceptance states. Physical validation remains open until an actual print/assembly is performed and documented.

