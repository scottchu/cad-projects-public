# Kage R0 migration design

## Selected contract

Use a two-level project layout. A small active surface exposes the Kage simulator/optics runtime, normalized continuity, root-workspace metadata, selected frozen/candidate references, and migration-integrity tests. A source-only `legacy/source-project/` mirror retains meaningful Python, JavaScript, tests, model generators, and textual metadata in original relative layout. `docs/legacy/` preserves original continuity and handoff records byte-for-byte. Historical tests are evidence, not the normal acceptance suite.

The locked direct-gear assembled STEP is the only retained 44 MB binary reference. Q3-R0 retains exactly four small written STEP/3MF artifacts as a candidate reference. Generated binary bulk, renders, screenshots, caches, environments, logs, and rollback duplication are excluded. All selection, relocation, adaptations, hashes, counts, and acceptance boundaries are machine-readable or indexed.

The only workspace adaptations are naming Kage, Python `>=3.12,<3.13`, CLI `kage-clock`, root uv membership/lock, root npm workspace/lock, and preservation of existing dependency pins. `cadgen.py` remains a local compatibility shim, not an external dependency.

## Alternatives and tradeoffs

- Whole-directory copy: rejected because it would import gigabytes of stale generated artifacts, caches, nested environments, locks, and false-current versions.
- Current-only rewrite: rejected because it would erase failures, decisions, physical observations, and source recoverability.
- Legacy mirror only: rejected because a fresh agent would lack a clear active runtime and clean-restart authority.
- Regenerate artifacts during migration: rejected because serializer drift could destroy provenance and because migration does not authorize CAD changes.

## Assumptions and risks

- The source directory is untracked at its parent Git revision, so the migration manifest—not Git history—is its provenance record.
- Legacy source may contain absolute paths and old project-local environment commands; those remain historical and are not active instructions.
- The locked STEP can be hash- and structure-checked, but its tiny nominal clearances and motion remain untrusted for PETG.
- Q3-R0’s identical-sector/U1 claims remain candidates until refreshed digitally and physically.

## Reflection and next experiment

`KAGE-EXP-001` is the sole active experiment. The immediate action is to **author**, not claim to possess or print, a minimal restart-namespace two-half Q3 seam coupon plus one focused geometry/export regression. It binds `KAGE-DC-001` and `KAGE-DC-002`.

Inherited controls are explicitly unaccepted: `3 + 3 mm` lap; `R70–124` lap band; donor/receiver tangent half-widths `13.0/13.2 mm`; `0.2 mm` plan clearance; and four `Ø3.3 mm` holes at `R76/R118` with tangent offsets `±7 mm`.

After authorship, generate explicit STEP and 3MF outputs and verify two solids, the lap and hole dimensions, and U1 footprint. Then print both halves in PETG on the Snapmaker U1 with a `0.4 mm` nozzle using identical profile and orientation; assemble four M3 fasteners finger-snug; wait one hour; and measure seam gap, face step, and flatness without sanding or forcing.

Pass only if gap is `0.05–0.30 mm`, step is at most `0.25 mm`, flatness deviation is at most `0.50 mm`, and there is no crack, forced fit, or visible bow. The exact hypothesis/evidence edge is:

```text
KAGE-DC-001/002 → author coupon source+regression → CAD/export validation → physical coupon → base-adoption decision
```

No coupon source, generated coupon artifact, or physical coupon exists now.
