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
design → implementation → critique → review → validation
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
7. hand immutable artifacts to independent review and validation.

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

### Visual review

After deterministic checks, render and inspect the primary STEP and the views needed to understand it: assembled, exploded/service, and critical closeups. Visual review checks intent, usability, and obvious omissions; it does not replace measurements or collision tests.

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

## Multi-agent feedback loop for substantial CAD

Use separate roles with bounded deliverables:

1. **Design agent:** produces the numeric contract, parameters, datums, risks, and test targets; does not implement.
2. **Implementation agent:** edits parametric source and generates explicit artifacts; does not approve its own work.
3. **Critic agent:** challenges mechanical intent, assembly, usability, DfAM, and likely failure modes using the exact baseline and generated artifacts.
4. **Review agent:** checks scope, requirement traceability, version preservation, and whether findings were actually resolved.
5. **Validation/test agent:** independently runs the focused tests, actual-solid checks, source/export parity, and artifact inspection.

The orchestrator must:

- give every role exact paths, version, frozen artifacts, and non-goals;
- prevent agents from reviewing a stale or wrong branch;
- avoid parallel implementation against a moving contract;
- stop or reuse idle roles instead of accumulating agents;
- report findings and progress in terms of unresolved risks, not agent count or test count.

When a finding occurs:

1. isolate the smallest failed invariant or interface;
2. send the numeric correction to design when architecture is affected;
3. let implementation change only the responsible source;
4. rerun the failed focused gate and affected regressions;
5. return immutable regenerated artifacts to independent review/validation;
6. repeat until there are no unresolved material findings.

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
