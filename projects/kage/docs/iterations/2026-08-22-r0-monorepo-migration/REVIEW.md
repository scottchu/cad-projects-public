# Independent review

## Review baseline and provenance

- Task: `KAGE-MIG-005`; formal reviewer: `/root/kage_migration_formal_review`.
- Repository baseline: `1484955cc1cfa64164dbdd1ca1222be658933c8e`; branch: `codex/migrate-kage`.
- Candidate: 798-row `manifests/candidate.sha256`, SHA-256 `81b98d4c043560512076b2599b7200e3ffe90a6e84a5300b25ac9941c5e57fb0`, verified before and after this review with every row valid.
- Independence: implementation owner `/root/kage_migration_impl`; critic `/root/kage_migration_critic`; validator `/root/kage_migration_validator`; formal reviewer `/root/kage_migration_formal_review`. The critic and validator were read-only and changed no paths. This reviewer changed only this excluded evidence record and did not repair or approve implementation on its own behalf.
- The failed critic/validator receipts for candidate `2901b2b7…` remain historical evidence only. The repair invalidated their acceptance value; the verdict below uses only the distinct reruns on `81b98d4c…`.

## Requirement and scope traceability

| Contract | Evidence and disposition |
|---|---|
| One-project migration; display name Kage; no XT60 | The changed scope is `projects/kage/**` plus root `uv.lock` and `package-lock.json`; `git diff --quiet -- projects/xt60-bend-jig` passed. Project/package metadata names **Kage**. `KAGE-NG-003` remains explicit. |
| Restart authority and historical rejection | Restart document hash `f5cf4e42…` and locked STEP hash `dea274f6…` match the authority manifests. ADR-0001, requirements, state, and reference READMEs reject Half-Z, low-Z, M1/M1B, Q4, I3/R1/R2, false-current version selection, and in-place reference edits. |
| Parametric source, tests, decisions, observations, and provenance preserved | Target checks passed for 8 authority rows, 60 legacy-doc rows, 667 legacy source/test rows, and 4 legacy-tooling rows. The 667 source rows and all five selected binaries are byte-identical to the original project; the original docs tree and README also compare exactly. Current continuity records preserve requirements, ADRs, the append-only experience facts, iteration reasoning, commands, findings, and acceptance gaps. |
| Root uv/npm workspaces | Validator: active suite 7 passed; compatibility suite 68 passed; repository structure 11 passed; CLI smoke passed; `uv lock --check`, npm workspace inspection, and npm dry-run passed. No nested environment, lock, dependency tree, cache, bytecode, or egg-info debris was found. |
| No CAD redesign; bounded binary selection | Exactly five CAD binaries are present: one locked STEP and the four Q3 STEP/3MF references, with original bytes and declared hashes. No historical artifact was regenerated or promoted. |
| Active/compatibility isolation and Q3 labeling | Normal tests contain only `test_migration_integrity.py`; four simulator/optics modules are explicitly optional and non-normative under `compatibility-tests/`. Q3-R0 is candidate/reference only, non-runnable in place, and not current, slicer accepted, or physically accepted. |
| Exactly one next experiment | `KAGE-EXP-001` is the sole experiment. It starts by authoring new restart-namespace coupon source plus a focused regression; it does not claim that a coupon exists. Inherited dimensions are unaccepted controls, with digital and physical pass/fail criteria bound to `KAGE-DC-001/002`. |

## Findings and dispositions

| ID | Prior severity | Repaired-candidate disposition |
|---|---:|---|
| `CRIT-001` | high | Resolved: rejected historical runtime tests are isolated from normal acceptance and labeled non-normative. |
| `CRIT-002` | medium | Resolved: both frozen packets provide exact legacy recovery routes and prohibit in-place generation. |
| `CRIT-003` | medium | Resolved: the 798-row candidate guard enforces sorted, unique, exact set closure, includes `BRIEF.md`, and requires the six declared exclusions to exist. |
| `CRIT-004` | low | Resolved: `KAGE-EXP-001` now begins with source/regression authorship and has falsifiable digital/physical criteria without a coupon-exists claim. |
| `VAL-001` | major | Resolved: `PROJECT_STATE.md` has all four required headings; the 11-test repository-structure gate passes. |
| New findings | none | No critical, high, or medium finding remains; no new low finding was identified. |

The repaired critic independently verified 798-row exact closure and reported all `CRIT-001..004` resolved. The repaired validator independently verified the same fingerprint before/after, reran workspace/integrity gates, confirmed unchanged authority, lock, and artifact hashes, and resolved `VAL-001`. Prior written STEP/3MF structural evidence remains applicable because every declared source and artifact input hash is unchanged; it does not establish slicer or physical acceptance.

## Acceptance layers and unresolved risks

- **CAD/source:** accepted for migration integrity only. Source authority, historical tests, decisions, failures, and provenance are preserved. There is no restart CAD candidate and no mechanism, fit, collision, motion, service, or manufacturing design accepted by this verdict.
- **Written artifact/slicer:** exact-byte preservation and prior structural STEP/3MF evidence are accepted as migration evidence. Q3-R0 remains a frozen candidate/reference. Current slicer profile, orientation, brim footprint, and print-release acceptance remain pending.
- **Physical print/assembly:** pending. No completed physical-results set exists. PETG seam fit/strength/flatness, motor dimensions, backlash, guidance clearance, sag, service access, optics, heat, wear, noise, and full assembly behavior remain unknown.

## Formal verdict

**Accepted for Kage migration integrity and GitHub delivery only.** Candidate `81b98d4c…` may proceed to delivery; it is not accepted as restart CAD, slicer-ready output, or physical proof. The next design action after delivery is only `KAGE-EXP-001`.

Delivery is not complete until the root agent updates the excluded continuity status/receipt ledger, creates or links the GitHub Project item, commits and pushes this non-`main` branch, and opens the pull request with this provenance, the three acceptance boundaries, unresolved risks, and next action.
