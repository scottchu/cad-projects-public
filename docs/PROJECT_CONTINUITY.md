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

Before material work begins:

1. create or identify the iteration directory;
2. point `docs/iterations/CURRENT` to it;
3. freeze the exact baseline, intent, scope, invariants, non-goals, and planned evidence in `BRIEF.md`;
4. record alternatives, tradeoffs, assumptions, and planned architecture in `DESIGN.md`.

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

Do not commit raw agent transcripts, caches, broad debug logs, redundant screenshots, or speculative notes that did not affect a decision. Summarize the durable fact, rationale, or lesson instead.

## Decision records

Use stable ADR identifiers such as `ADR-0001`. An ADR records context, alternatives, decision, consequences, evidence, and status. When a decision changes, add a new ADR and mark the earlier one superseded; do not erase the old rationale.

## Migration rule

When importing a legacy project, preserve original handoff and continuation files under `docs/legacy/`. Normalize current facts into the continuity structure and create a migration iteration that records source paths, inclusion and exclusion rules, hashes, workspace adaptations, verification, and remaining acceptance gaps.

Templates live under `docs/templates/project-continuity/`.
