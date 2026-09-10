# Requirements and migration contract

## Outcome and use sequence

Preserve Pill Click development outside the downloaded-model library so later
work can resume from files. Select a baseline, review its intent, validate the
smallest risky relationship, then separately consider CAD and physical work.

## Invariants

- `MIG-001`: imported `src/`, `tests/`, `models/` stay byte-identical.
- `MIG-002`: root workspace owns environment and lock; no nested lock/environment.
- `MIG-003`: isolate the older root P1 spec; never merge its four-part design into canonical P1.
- `MIG-004`: preserve original README/docs and explicitly record missing references.
- `MIG-005`: migration must not manufacture CAD, artifact, slicer or physical acceptance.

## Derived constraints

P1 three-part geometry and P2 four-part geometry are different experiments;
preserve version-specific contracts. P1 dimensions remain in its original spec;
P2 contract remains in its source/spec.py and tests until a new brief is agreed.

## Design choices

Canonical source remains `src/pill_click/`; P0 history is not silently retired.
Continuity uses current facts, while original assertions remain historical.

## Non-goals

No redesign, CAD regeneration, artifact repair, slicing, printer operation,
upgrading dependencies, commit, push or PR in this migration.

## Physical unknowns

Rail friction, latch fatigue, rebound/holding force, magnet retention, support
removal, bayonet cycling, cleaning, food contact and child resistance.

## Evidence mapping

`MIG-001/003/004`: `source-manifest.json` and legacy evidence; `MIG-002`: root
lock/sync/check; `MIG-005`: separate acceptance labels in state and validation.
