# Project continuity and iteration records

## Purpose

The repository is the durable memory for every design project. Agent sessions, chat summaries, and local recollection are temporary aids and must never be the only place where project state, reasoning, evidence, experience, or next actions exist.

A fresh agent with access only to the repository must be able to determine:

- what the project is trying to achieve;
- the exact accepted or experimental baseline;
- which requirements, invariants, and non-goals govern the work;
- what alternatives were considered and why decisions were made;
- what was attempted, what failed, and what was learned;
- which checks actually ran and what they proved;
- which CAD, artifact/slicer, and physical claims remain unproven;
- the next smallest responsible action.

## Required project records

Every directory under `projects/` must contain:

- `README.md`: stable purpose, authoritative source, setup, generation, and test commands;
- `PROJECT_STATE.md`: concise current-state index with baseline, active iteration, acceptance states, open risks, and next action;
- `NEXT_AGENT.md`: short restart route pointing to canonical records and exact paths or revisions;
- `docs/REQUIREMENTS.md`: stable requirement IDs, invariants, derived constraints, design choices, non-goals, and physical unknowns;
- `docs/EXPERIENCE.md`: append-only measured observations, physical failures, print or assembly lessons, and their design implications;
- `docs/decisions/README.md`: decision index linking stable ADR files and marking current or superseded decisions;
- `docs/iterations/CURRENT`: one line containing the active iteration directory name;
- `docs/iterations/<iteration-id>/`: the active iteration record described below.

Release artifacts should live in a project-owned release location and carry a manifest linking them to source, parameters, commands, checksums, and acceptance states.

## Iteration lifecycle

Use a stable, sortable iteration identifier such as `p13-r1-monorepo-migration` or `2026-08-22-p17-preload-retune`. Do not reuse an identifier for unrelated work.

## Version and evidence-status policy

For design projects that use `P` and `R` labels, `P` identifies the core
product-design baseline and `R` identifies a revision of that same baseline.
Use the labels for design meaning, not for the success or failure of a single
artifact.

- Increment `P` only when the core product-design baseline changes: mechanism
  architecture, user-facing workflow, external interface, fundamental part
  count/roles, or another decision that makes later work incompatible with the
  prior product design.
- Increment `R` for geometry, fit, tolerance, manufacturing, source
  implementation, documentation, artifact, or validation refinement that keeps
  the same core product design.
- Track evidence status independently from version: simulator, CAD/source,
  STEP, mesh/3MF, slicer, and physical acceptance are separate evidence layers.
  A failed simulator, failed STEP export, bad 3MF, or failed physical print can
  reject that artifact or evidence layer without automatically creating a new
  `P` version.
- Every proposed `P` bump must include a durable justification in the active
  iteration brief or an ADR. The justification must name the product-design
  baseline being superseded, the incompatible architecture/interface/workflow
  change, rejected alternatives, and why an `R` revision would be insufficient.

When correcting version labels, preserve the historical evidence record. Add an
explicit correction note instead of erasing failed artifacts, rejected reviews,
or earlier mistaken labels.

Before material work begins:

1. create or identify the iteration directory;
2. point `docs/iterations/CURRENT` to it;
3. freeze the exact baseline, intent, scope, invariants, non-goals, and planned evidence in `BRIEF.md`;
4. record alternatives, tradeoffs, assumptions, and planned architecture in `DESIGN.md`.
5. when work is delegated, record the bounded execution plan as a DAG in `BRIEF.md`, using a summary table plus task detail blocks; do not create separate orchestration documents or per-agent diaries.

While work is in progress:

1. update durable reasoning when a material decision changes;
2. create an ADR when an architectural choice will affect later iterations;
3. append real observations and lessons to `docs/EXPERIENCE.md`;
4. record failed approaches that could otherwise be repeated;
5. keep exact validation commands and outcomes in `VALIDATION.md`;
6. keep independent findings and their disposition in `REVIEW.md`.

Before stopping, switching agents, or closing the iteration:

1. update `HANDOFF.md` with completed work, unresolved risks, changed files, artifacts, and the next smallest action;
2. update `PROJECT_STATE.md` to match the repository and active iteration;
3. update `NEXT_AGENT.md` so a fresh agent can resume without the prior session;
4. distinguish CAD/source, written artifact/slicer, and physical acceptance;
5. ensure every claim cites repository evidence or an exact command that actually ran.

## Iteration files

Each active iteration contains:

- `BRIEF.md`: baseline, outcome, use sequence, scope, requirements, invariants, non-goals, risks, and acceptance targets;
- `DESIGN.md`: alternatives, tradeoffs, selected approach, assumptions, parameter or interface decisions, and rejected approaches;
- `VALIDATION.md`: exact commands, results, artifact facts, failures, reruns, and acceptance boundaries;
- `REVIEW.md`: critic and review findings, severity, resolution, and remaining concerns;
- `HANDOFF.md`: current status, changed paths, artifacts, open work, and precise next-agent instructions.

For delegated work, `BRIEF.md` additionally contains a stable frozen design contract section and a separate mutable execution-plan/status area. The execution-plan summary table records task ID, role, dependencies, immutable inputs, exclusive write scope, done condition, parallel group, model/effort/time/token ceiling, and status. Its task detail blocks record owner identity, allowed reads, forbidden scope, deliverables/evidence, output/retry/concurrency ceilings, and stop/escalation conditions. An immutable input manifest is a declared SHA-256 list of decision-bearing paths and content hashes: relevant frozen requirements, the frozen brief/design contracts, and applicable authoritative source/test/artifact paths. It excludes only mutable orchestration/status and evidence records. `REVIEW.md` records distinct critic and independent formal-reviewer provenance, candidate fingerprint, and read-only status. `VALIDATION.md` records validator provenance and candidate fingerprint. `HANDOFF.md` carries a concise agent receipt/ledger with canonical evidence links and the next collect/refine action. `NEXT_AGENT.md` links to these canonical records rather than copying their contents.

These documents evolve during an active iteration. Once the iteration closes, correct factual errors with an explicit correction note; do not rewrite the historical reasoning to look cleaner than it was.

## What to preserve

Preserve information that can change later work:

- supplied measurements and observed failures;
- design alternatives and the reasons they were accepted or rejected;
- parameter values and their evidence;
- purchased-part assumptions and provenance;
- source and artifact hashes where useful;
- validation commands and summarized results;
- review findings and how they were resolved;
- open physical unknowns and required observations.

Do not commit raw agent transcripts, per-agent diaries, caches, broad debug logs, redundant screenshots, or speculative notes that did not affect a decision. Summarize the durable fact, rationale, or lesson instead.

## Decision records

Use stable ADR identifiers such as `ADR-0001`. An ADR records context, alternatives, decision, consequences, evidence, and status. When a decision changes, add a new ADR and mark the earlier one superseded; do not erase the old rationale.

## Migration rule

When importing a legacy project, preserve original handoff and continuation files under `docs/legacy/`. Normalize current facts into the continuity structure and create a migration iteration that records source paths, inclusion and exclusion rules, hashes, workspace adaptations, verification, and remaining acceptance gaps.

Templates live under `docs/templates/project-continuity/`.
