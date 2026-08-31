# CAD workflow and testing standard

## Purpose

This is the default workflow for parametric CAD work in this repository. It is deliberately evidence-driven without rewarding large test counts.

The objective is not to prove every imaginable property. It is to catch the failures that would make the current design wrong, unassemblable, unprintable, or inconsistent with the user's intent.

## Lessons from the existing projects

The XT60 bend-jig and Japandi shadow-clock histories exposed recurring failure patterns:

- A model can pass many tests while solving the wrong operation or testing only an isolated coupon rather than the promised assembly.
- An agent can review the wrong version unless the baseline path, version, and immutable artifacts are explicit.
- Nominal equations and parameter assertions can pass while actual solids overlap.
- A collision-free final pose can still have an impossible insertion, removal, or service path.
- Source geometry can be correct while the written STEP or 3MF is transformed, incomplete, malformed, badly oriented, or packaged incorrectly.
- A CAD clearance can be nominally valid but physically wrong because printed holes, rods, warping, elephant foot, and material behavior differ from the model.
- Broad agent activity and very large test suites create noise when roles, scope, and acceptance gates are unclear.

The most useful historical checks caught concrete defects: wrong gear interfaces, hardware collisions, a shallow axle socket, weak screw-hole ligaments, fin-path intersections, duplicate export transforms, malformed 3MF packaging, and real rod-fit differences found by printed coupons.

## Workflow overview

```text
intent and exact baseline
        ↓
requirements + invariants + risks
        ↓
small test plan and numeric design contract
        ↓
design → implementation → (critic || independent validation) → formal independent-review join
        ↑                         findings          │
        └──── smallest-source repair and rerun ────┘
        ↓
STEP/export + snapshot + fabrication handoff
        ↓
physical observation, kept separate from CAD acceptance
```

Scale the depth to the risk. A simple static part needs a short contract and a few checks. A mechanism, repeated assembly, fit-critical interface, or print release needs the full loop.

## Phase 0: establish the exact baseline

Before design work:

1. Identify the canonical project, source entrypoint, current version, and relevant output artifacts.
2. Record the path and, for a locked baseline, a source or artifact hash/manifest.
3. Distinguish accepted baseline, experimental branches, rejected versions, and stale exports.
4. Confirm what may change and what must remain unchanged.

“Locked” does not mean the design can never evolve. It means every change is intentional, versioned, scoped, and regression-tested. Never silently modify the baseline or send an agent an ambiguous “latest” file.

## Phase 1: turn intent into a contract

Write a compact brief before modeling. It must include:

- the real user outcome and use sequence;
- supplied references and observed physical failures;
- units and coordinate convention;
- purchased parts and measured dimensions;
- material, printer, nozzle, bed, and assembly assumptions when relevant;
- required parts, roles, states, motion, access, and service sequence;
- explicit non-goals and excluded components;
- output paths and desired artifacts;
- properties that remain physical unknowns.

Classify each statement:

| Class | Meaning | Treatment |
|---|---|---|
| Invariant | Must remain true in every accepted version | Fails the design immediately if violated |
| Derived constraint | Computed from other parameters or interfaces | Prove with math and geometry |
| Design choice | May change without violating intent | Review visually and document |
| Physical unknown | Depends on print, material, heat, force, wear, or real hardware | Use a coupon or physical test; do not claim CAD proof |

Give hard requirements stable IDs such as `REQ-01`. Each ID must map to automated evidence, a manual visual check, or an explicitly pending physical gate.

For printed parts, consult [FDM design rules](FDM_DESIGN_RULES.md) and the
project's `PRINTING_PROFILE.md` while forming this contract. Record load-relative
print orientation, nozzle/material choices and unresolved concerns there; workshop
inventory alone is neither a project selection nor process validation.

## Phase 2: choose the smallest useful test plan

Start with the four core categories below. Use one or a few high-value checks in each category rather than generating many near-duplicates.

Before adding a test, answer:

> What credible defect would this test catch, and has that defect not already been covered more directly?

Do not add the test if there is no concrete answer.

### 1. Object-collision tests

Test actual BREP/solid geometry, not only center distances or bounding boxes.

Cover:

- unexpected part-to-part intersection volume;
- hardware, purchased-part envelopes, keep-outs, and tool-access envelopes;
- expected contacts, which must be explicitly allow-listed;
- critical open, mid, locked, and worst-case poses;
- insertion, removal, assembly, and service paths when the part must move through space.

A zero-collision check at one final pose is insufficient for a mechanism. Sample only meaningful states and risk boundaries; do not sweep thousands of states when a small set plus a monotonic/geometric proof covers the same risk.

### 2. Math tests

Test derived behavior rather than copying source constants into assertions.

Useful targets include:

- tangency, angles, bend radius, gear ratios, pitch, and center distances;
- conserved length or synchronized travel;
- transforms, symmetry, identity placement, and coordinate-frame relationships;
- monotonic motion and endpoint calculations;
- tolerance-stack calculations and clearance budgets.

Use nominal and boundary values. Add pairwise parameter cases only when parameters interact. Exhaustive parameter grids are justified only when the domain is small and the invariant cannot be proven more directly.

### 3. Constraint tests

Verify the physical and fabrication contract:

- required dimensions and bounding boxes;
- minimum wall, ligament, floor, engagement, and edge distances;
- holes, fits, clearances, alignment, and coplanar assembly datums;
- exact occurrence counts and named part roles where these matter;
- printer-bed fit measured from the written artifact, including required brim/spacing;
- allowed parameter domains and locked-baseline preservation.

Constraints must be checked on the geometry or written artifact that will actually be handed off whenever possible.

### 4. User-requirement tests

Trace tests back to requirement IDs. These checks catch a design that is internally consistent but answers the wrong request.

Examples:

- exactly three rods and four plates;
- one identical sector printed three times;
- no underlying rail, replacement base, motor, or electronics in the current MVP;
- a required open soldering window or removable bridge exists;
- the promised output contains the correct part quantities;
- unrelated locked geometry remains unchanged.

Test both required presence and important absence. Part counts alone are not enough; roles and relationships must also match the brief.

## Phase 3: freeze the design contract, then implement source-first

Before implementation begins:

1. Resolve architecture questions with a short design comparison, simulator, ADR, or review view when the user cannot judge the mechanism from prose alone.
2. Freeze the selected baseline, numeric parameters, datums, part roles, motion states, and test targets.
3. Write failing focused checks first for risky invariants when practical. Do not require test-first work for purely cosmetic edits.
4. Confirm that the implementation agent has the exact source and version, not an ambiguous “latest” directory.

Implementation rules:

- keep meaningful dimensions and choices as named parameters;
- derive dependent geometry from those parameters rather than duplicating numbers;
- use part-local coordinate frames and named mating/service datums;
- use measured or canonical purchased-part geometry when available, otherwise document a conservative envelope;
- edit parametric source, never generated STEP, 3MF, STL, GLB, or render output;
- generate explicit targets into a versioned namespace;
- keep STEP as the primary validated CAD artifact and derive fabrication meshes from it/source;
- preserve the accepted baseline unless the brief explicitly authorizes a scoped change.

Run gates in this order so cheap failures stop expensive work:

1. fast requirement, math, and parameter-domain checks;
2. generate the explicit primary STEP target;
3. validate topology, dimensions, constraints, actual-solid collisions, and applicable motion/service states;
4. render and review required snapshots;
5. generate secondary fabrication artifacts;
6. validate source/export parity, mesh/3MF packaging, orientation, and slicer behavior;
7. freeze the generated candidate, then hand it to the independent critic and validation roles; formal independent review joins their results.

Do not regenerate an entire project when only one explicit target changed.

## Additional evidence, used only when relevant

### Motion, assembly, and service-path checks

Add these for moving or assembled designs. Check representative poses, end stops, hardware-inclusive sweeps, insertion/removal directions, and exploded/service states. This is often more valuable than adding more nominal dimension tests.

### Source-to-artifact parity

Add this whenever STEP, 3MF, STL, or other fabrication artifacts are delivered.

Verify:

- source and written output have the intended solid/occurrence counts and bounds;
- placement is not transformed twice;
- meshes are manifold and have valid volume;
- 3MF manifests, quantities, units, and object transforms are correct;
- repeated clean exports are stable within measured serializer tolerance;
- artifact paths and hashes point to the current version, not stale output.

### Manufacturing and slicer checks

Use for print-ready claims:

- intended source-defined orientation;
- first-layer footprints and early-layer continuity;
- overhangs, bridges, support assumptions, and fragile small features;
- bed fit with brim and spacing;
- the actual printer, nozzle, material, and slicer profile when available.

Do not use a slicer workaround to hide a source-geometry defect.

Bind the exact source/artifact and resolved slicer settings, including part/plate
overrides, to a versioned run in `PRINTING_PROFILE.md`. Preserve prior run evidence
when settings change. Profile completion does not waive design blockers or replace
separate CAD, written artifact/slicer and physical acceptance.

### Visual review

After deterministic checks, render and inspect the primary STEP and the views needed to understand it: assembled, exploded/service, and critical closeups. This visual inspection checks intent, usability, and obvious omissions; it does not replace measurements or collision tests, and it is not the formal independent reviewer role described below.

Use the installed `cad-viewer` workflow directly for live review; do not maintain a
repository wrapper around its runtime or process lifecycle. Give it the explicit file,
choose an absolute workspace directory, and use the file path relative to that
workspace in the review URL.

Viewer startup and URL production are not preview-success evidence. Before calling a
preview ready, independently require the exact review page to return HTTP `200` and
the exact artifact endpoint to return HTTP `200` with JSON `state == "ready"`. An HTTP
`200` page alone can still contain an artifact-build error. After visual inspection of
the loaded page or a snapshot, the general claim is limited to “the requested artifact
rendered with no visible error state.” Any feature-specific visual claim must name the
inspected features and views. Record endpoint readiness and visual observations
separately, and never promote either to CAD, slicer, or physical acceptance.

### Defect regression

Every concrete defect found by a reviewer, slicer, print, photo, or assembly attempt should produce one focused regression when it can be represented digitally. Keep that regression after the repair. Do not preserve large obsolete suites for rejected designs unless they protect a still-supported baseline.

### Physical coupon or observation gate

Use the smallest physical test that resolves a real uncertainty: hole/shaft fit, cap retention, wall quality, friction, snap force, thermal behavior, or assembly access. Record the measured part and result. Feed it back into parameters and regression tests.

CAD evidence cannot prove physical fit, strength, friction, heat behavior, wear, or print quality.

## What does not count as sufficient evidence

- a large passing-test count without requirement coverage;
- tests that simply restate parameter literals;
- collision checks using only bounding boxes for detailed interfaces;
- one screenshot or one final pose for a moving assembly;
- a focused coupon passing when the promised full assembly uses different geometry;
- source tests without checking the written STEP/3MF that will be printed;
- an implementation agent approving its own design;
- “CAD passed” presented as “physically proven.”

## Delegated execution protocol for substantial CAD

The orchestrator owns the task DAG, frozen inputs, scheduling, provenance checks, receipt collection, conflict synthesis, and concise continuity-index maintenance. It does not quietly substitute for substantive design, implementation, critique, formal review, or validation deliverables. Each material task has a stable ID and owner identity, a single bounded role, objective/done gate, dependencies, exact project/iteration/baseline, task-specific immutable input manifest/candidate fingerprint, allowed reads and exclusive writes, forbidden scope, deliverables/evidence, model/effort, time/token/output/retry/concurrency ceilings, and stop/escalation conditions.

Create each immutable input manifest with SHA-256 over a sorted list of its declared decision-bearing paths and content hashes: the relevant frozen requirements, the `BRIEF.md` frozen design contract section, the frozen selected design contract in `DESIGN.md`, and applicable authoritative source, tests, and artifacts. The candidate fingerprint names that manifest and its exact baseline. Exclude only mutable orchestration/status and evidence records: the delegated-plan/status area of `BRIEF.md`, mutable progress in `DESIGN.md`, `VALIDATION.md`, `REVIEW.md`, `HANDOFF.md`, receipts, and indexes. When a path or declared section changes, invalidate only a gate whose declared manifest includes it; do not discard unrelated evidence merely because a mutable coordination or evidence record changed.

Use separate roles with bounded deliverables:

1. **Design agent:** produces the numeric contract, parameters, datums, risks, and test targets; does not implement.
2. **Implementation agent:** edits parametric source and generates explicit artifacts; does not approve its own work.
3. **Critic agent:** challenges mechanical intent, assembly, usability, DfAM, and likely failure modes using the exact baseline and generated artifacts.
4. **Formal review agent:** independently checks scope, requirement traceability, version preservation, and whether critic/validator findings were actually resolved. This acceptance role is distinct from visual inspection.
5. **Validation/test agent:** independently runs the focused tests, actual-solid checks, source/export parity, and artifact inspection.

### Frozen DAG and parallelism

Default to no more than three workers while the orchestrator retains coordination capacity. One writer owns each project/source/artifact namespace. Parallelize only dependency-ready nodes that have frozen inputs and disjoint write scopes or are read-only. Do not assign duplicate agents to the same role and revision unless an independent arbitration or comparison is explicitly required. A runtime agent may be reused for follow-up or focused repair in the same bounded role/workstream; record its stable identity. The implementer, critic, validator, and formal reviewer identities must be distinct for the same candidate.

For substantial CAD, use this order:

1. Discovery branches may run in parallel before design, read-only against the frozen baseline.
2. The design role selects and freezes the candidate contract before implementation. The implementation role alone mutates the candidate source/tests/artifacts and never approves its own result.
3. After that candidate is frozen, the critic and independent validation roles may run in parallel, read-only against the same candidate fingerprint.
4. Formal independent review is their join gate: it audits their provenance, requirement coverage, findings, and dispositions, and determines whether the candidate can advance.
5. Any candidate change invalidates only downstream critique, validation, or review gates whose declared input manifests include the changed path; rerun those affected independent gates on the new fingerprint.

Use the least expensive adequate model: fast/low for deterministic inventory, formatting, and command checks; balanced/medium for prescribed implementation or simple parts; strong/high for mechanisms, fit, critique, review, and acceptance checks; frontier/max only for unresolved architecture, repeated material failure, or physical-defect diagnosis. A max model never substitutes for a clear brief. Establish checkpoints and timeboxes; if exact controls are unavailable, record qualitative ceilings. After an initial attempt, permit at most two focused repair cycles within the task retry ceiling before reopening design, reducing scope, or escalating to the user. Stop stale, duplicate, and superseded tasks.

The orchestrator must:

- give every role exact paths, version, frozen artifacts, and non-goals;
- prevent agents from reviewing a stale or wrong branch;
- avoid parallel implementation against a moving contract;
- stop or reuse idle roles instead of accumulating agents;
- report findings and progress in terms of unresolved risks, not agent count or test count.

Each role returns a concise receipt: stable owner identity and role; status; verified fingerprint; changed paths/artifacts; canonical links to exact commands/results, hashes/manifests, findings/severity, and requirement coverage; unresolved risks; and next action. Record distinct critic, validator, and formal reviewer provenance without copying raw reports. The orchestrator verifies provenance, synthesizes conflicts instead of concatenating reports, routes the smallest correction, and records durable evidence. Raw transcripts and per-agent diaries are prohibited.

When a finding occurs:

1. isolate the smallest failed invariant or interface;
2. send the numeric correction to design when architecture is affected;
3. let implementation change only the responsible source;
4. rerun the failed focused gate and affected regressions;
5. return immutable regenerated artifacts to independent critic and validation, then to formal independent review as their join gate;
6. repeat only within the task retry ceiling; otherwise reopen design, reduce scope, or escalate.

Do not restart the whole design for a local defect unless the evidence shows the architecture is impossible.

## Handoff and acceptance labels

Every handoff states these separately:

### CAD accepted

- requirements and invariants are traced;
- core math, constraint, collision, and user-requirement checks pass;
- applicable motion/service checks pass;
- the primary STEP validates and snapshots were reviewed.

### Artifact/slicer accepted

- source/export parity and written-artifact checks pass;
- the intended print artifact loads, fits the bed, and uses the intended orientation/profile assumptions.

### Physical validation pending or accepted

- list the exact coupon, print, fit, assembly, motion, heat, and durability observations still required;
- mark physical acceptance only after those observations are recorded.

The final report includes exact commands, paths, versions/hashes where useful, checks that actually ran, unresolved physical unknowns, and the next smallest physical test.
