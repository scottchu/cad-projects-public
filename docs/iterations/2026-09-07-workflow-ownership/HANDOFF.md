# Workflow ownership separation handoff

Status: independent V1/V2/R1 acceptance complete for source implementation `b8b0f5d9e38a2b2d1f1f6b07b9ec6f9f283c8565`. Coordinator pushed the review branch and opened [PR 23](https://github.com/scottchu/design-projects/pull/23). No merge or printer/service operation. Original worker checkpoints below retain their historical scope.

## Baseline and authority

Source baseline `71d661c14098860b7a374e13043fb084994be8a0`, branch `codex/separate-sticker-repository`, replacement checkout `/Users/scottchu/Projects/personal/design-projects-workflow-separation`. Original `0868` checkout disappeared externally; the coordinator recreated this checkout from the same retained branch. Recovery branch `recovery/workflow-ownership-71d661c` retains the original source tree. The canonical dirty checkout and original V3 live-pilot worktree were untouched.

The user assigned reusable workflows to CAD Workbench and projects/assets/evidence to project repositories. I3 verified all eight frozen source inputs using Workbench `.workbench/workflow-ownership/I3-source-inputs.sha256` before edits. Source retirement followed coordinator release confirming independent V1 byte/path/recovery PASS, forty Workbench extraction mappings PASS and sticker root checks PASS. See the bound Workbench revision's `docs/iterations/2026-09-07-workflow-ownership/` records.

## Ownership and references

| Former source path | Current owner/reference |
| --- | --- |
| `docs/CAD_WORKFLOW.md`, `PROJECT_CONTINUITY.md`, `FDM_DESIGN_RULES.md`, `ADDING_A_PROJECT.md` | Same-named files under Workbench `workflows/policies/`; original filenames retained here only as pointers |
| `docs/templates/project-continuity/` | Workbench `templates/project-continuity/` |
| `.agents/skills/design-reflection/` | Workbench `skills/design-reflection/` |
| `.agents/skills/sticker-pack-production/` | Workbench `skills/sticker-pack-production/`; historical exact bytes also retained by sticker import |
| `tools/cad-viewer-service/` | Workbench same relative path; installed services were not changed |
| `projects/example-sticker-pack/` | Private `https://github.com/scottchu/sticker-projects`, same relative path |
| Other projects, historical root iterations, `docs/WORKSHOP.md` | Remain here, byte-for-byte |

`docs/workflows-binding.json` pins Workbench review candidate `36f41715ee2257c0f2e41e40329216e3d2b2747f` and `catalog/POLICY.sha256` hash `6f1ab6580b67cd9e58dd2302f07cdc65a3a2bfa2213e650139a7ce4542bf9536`. This is not an installed runtime or plugin. Workbench's exact extraction map has SHA-256 `7333d1a41e77be32b679bce3e711f901bb6c60634ea265ec5105a79427bfed52` at `docs/iterations/2026-09-07-workflow-ownership/EXTRACTION.json`.

The accepted V2 GitHub release remains at `https://github.com/scottchu/design-projects/releases/tag/example-v2-anatomy-r1`. Destination migration records bind accepted source bytes and filtered history. The destination `recovery/live-pilot-fef4f264/` retains distinct binary tracked delta and tar recovery; restore only into an isolated checkout of its recorded baseline, never over accepted main. Original WIP remains available. Source recovery: inspect or create an isolated worktree at `recovery/workflow-ownership-71d661c`; do not reset this branch or overlay unrelated work.

## Implementation and evidence

- Concise root instructions, README, architecture and four compatibility pointers replace embedded shared policy. No project generation logic changed.
- Retired 884 migrated tracked paths, enumerated with original SHA-256 bytes in `RETIRED.sha256`.
- Verified all 2,504 remaining project files, historical root iteration files and workshop inventory against baseline Git blob identities; their current hashes are in `PRESERVED.sha256`.
- Root tests retain workspace, continuity, printing profile and delivery checks. Shared skill/template/policy phrase tests moved out of the consumer's responsibility. A focused binding check catches unresolved identities and broken pointers.
- `uv lock` removed only the Example workspace entry/package. `npm install --package-lock-only --ignore-scripts` removed its workspace/sharp-only dependencies; root manifests unchanged. `npm ci --ignore-scripts` passed and retained the generated lock byte-for-byte.
- `uv sync --all-packages --all-groups` passed, creating this checkout's sole root environment with CPython 3.12.13. `uv lock --check` passed. No project-local environment or lock was created.
- Final `uv run pytest tests/test_repository_structure.py`: **9 passed, 1 failed**. The remaining failure is pre-existing: `projects/laifen-wave-case/docs/iterations/2026-09-06-pattern-reference-intake/VALIDATION.md` is absent while CURRENT points there. `git cat-file -e 71d661c:<path>` confirms it is absent in the frozen baseline. The continuity check remains enforced; no skip or fabricated project evidence was added.
- Verified pinned provider manifest bytes from `git show <revision>:catalog/POLICY.sha256` and every declared entry from that exact commit using SHA-256: PASS.
- `git diff --check` and `git diff --cached --check`: PASS.

## Limits and next action

Implementation checks do not substitute for independent joined review. The known Laifen continuity defect remains outside this separation scope and must be reported in delivery. No CAD suite, project regeneration, real viewer/service test, external platform acceptance or physical acceptance is claimed. Coordinator should freeze the candidate, join independent checks/review, and deliver via PR without merge. Historical project links remain unchanged; follow compatibility pointers and the binding for current external workflow locations.

## V2 repair 1 — canonical workflow identity

V2 found the local recipe slug `cad-fabrication` did not match catalog ID `WF-CAD-FABRICATION`. Corrected only the binding ID and strengthened the consumer test to read the actual catalog from the exact pinned Workbench Git commit. It verifies the policy-manifest hash, the catalog hash listed by that manifest, and each selected ID/recipe pair. Set `CAD_WORKBENCH_CHECKOUT` when Workbench is not a sibling checkout; the check performs local Git object reads, without network or provider runtime execution.

Exact commands from this source root:

```sh
CAD_WORKBENCH_CHECKOUT=/Users/scottchu/.codex/worktrees/7e46/CAD-workbench uv run pytest tests/test_repository_structure.py -k 'external_workflow or bound_workflows'
CAD_WORKBENCH_CHECKOUT=/Users/scottchu/.codex/worktrees/7e46/CAD-workbench uv run pytest tests/test_repository_structure.py
git diff --check
```

Results: affected checks **2 passed, 9 deselected**; whole root file **10 passed, 1 pre-existing Laifen continuity failure**; whitespace PASS. No project source or other binding values changed. Refreshed `CANDIDATE.sha256` covers the repaired binding and tests.

Coordinator additionally authorized root `.gitignore` exclusion `*.egg-info/` for editable-install metadata created by the root uv setup. The generated Kage directory remains in place and is ignored; no project source was deleted. `.gitignore` is included in the refreshed candidate.

## Coordinator delivery

Migration validation and review are recorded in [Workbench PR 1](https://github.com/scottchu/CAD-workbench/pull/1), under docs/iterations/2026-09-07-workflow-ownership/{PRESERVATION_VALIDATION,VALIDATION,REVIEW}.md. [Sticker PR 1](https://github.com/scottchu/sticker-projects/pull/1) preserves accepted history and recovery refs. Root checks finished at 10 pass and 1 confirmed preexisting Laifen missing-VALIDATION failure. The provider binding and fourteen-file CANDIDATE manifest remain unchanged after acceptance. This follow-up changes delivery records only.
