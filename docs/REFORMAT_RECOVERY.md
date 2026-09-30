# Reformat recovery — 2026-09-29

## Scope and authority

This delivery preserves CAD projects, sticker projects, design-workbench (local directory `CAD-workbench`), and the superseded workflow-library draft. It does not certify a full-computer backup or preserve unrelated repositories, credentials, Codex task history, global skills, or global memories.

The GitHub repository was renamed from `design-projects` to `cad-projects`. The local old-name symlink is a compatibility path to the same canonical checkout. Historical names, source paths, manifests, and review identities remain unchanged where they describe past evidence.

## Off-machine recovery

[Private GitHub recovery release](https://github.com/scottchu/cad-projects/releases/tag/reformat-recovery-20260929).

All 23 initial assets were downloaded from GitHub and SHA-256 verified. Every archived payload was compared with its source bytes before upload. All 13 recorded tracked worktree states replayed into isolated Git indexes. Four self-contained Git bundles preserve every local ref, including the CAD stash. See [asset inventory](recovery/2026-09-29/archives.json), [checksums](recovery/2026-09-29/SHA256SUMS), [bundle refs](recovery/2026-09-29/BUNDLE_REFS.json), [download verification](recovery/2026-09-29/REMOTE_VERIFIED.json), and [patch restoration](recovery/2026-09-29/RESTORE_VERIFIED.json). The release also contains the complete inventory of excluded rebuildable environments/caches.

| Recovery asset | Preserved source and disposition |
| --- | --- |
| `00-cad-projects.tar.gz` | Canonical checkout's substantive ignored files before integration. |
| `01-cad-projects.tar.gz` | Sticker live-pilot worktree `3fc3`: unapproved TD06/V3 previews and production pause. Restore separately; never overlay accepted sticker art. |
| `02-cad-projects.tar.gz` | Laifen `4f8c`: ignored CAD exports, diagnostic media and scratch evidence. Committed source is already on main. |
| `03-cad-projects.tar.gz` | Lunch-and-learn `740e`: completed 20-slide HTML, assets and review records, now imported into main. |
| `04-cad-projects.tar.gz` | Grenadier `a1ea952b...`: completed development preview and nozzle-comparison source/evidence imported into main. Other old XT60/Kage/root-policy deltas remain recovery-only; do not overlay them on current main. |
| `05-cad-projects.tar.gz` | Historical XT60 `a373f6e6...` substantive ignored outputs. |
| `06-cad-projects.tar.gz` | Clean historical Kage viewer checkout `b478a5e4...`; baseline metadata. |
| `07-cad-projects.tar.gz` | Kage roller-mount source and R3/R4 stop evidence from `printing-profiles-pr.Ve1PlT`; not an accepted product candidate. |
| `08-cad-projects.tar.gz` | Completed September 10 delivery worktree and remaining output. |
| `09-cad-projects.tar.gz` | Completed workflow-separation worktree and substantive local evidence. |
| `10-sticker-projects.tar.gz` | Clean sticker checkout metadata; full history in `sticker-projects.bundle`. |
| `11-CAD-workbench.tar.gz` | Workbench local runtime/diagnostic records; full history in `CAD-workbench.bundle`. |
| `12-workflow-library.tar.gz` | Superseded uncommitted draft; not a second workflow authority. |
| `previous-main-backup.tar.gz` | September 10 exact-file backup and associated recovery records. |
| `sticker-rejected-release-quarantine.tar.gz` | Both rejected sticker release trees and the original recovery receipt from Trash. Never distribute them as accepted releases. |

## Completed delivery and preserved knowledge

- The offline lunch-and-learn HTML retains the reviewed SHA-256 `5513552455b32e0f4124e15a3cbaea22d0b076e44d83d66e43b71b9a42d85b53`. Its 52 durable manifest entries matched before integration; 118 temporary inputs were already missing in the original review and remain unavailable. Documentation headings were normalized for repository continuity; the HTML and its assets are unchanged.
- Grenadier source/GLB preview and native 0.2/0.4 mm nozzle studies are preserved as development evidence. The user selected 0.2 mm. Final scale, material, fine-detail reproduction, structural connectivity, magnets, thumbnails and physical acceptance remain unresolved. No fabrication is authorized by this delivery.
- Kage's newest archived investigation is the September 8 native-3MF topology bisect. Primitive controls passed; the full fork still has zero-area/open-edge failures at the capture/backbone seam. The iteration exhausted its repair ceiling and formally stopped. Restore archive 07 on `d47baf15e00d98a3b20202293972af9c9dd18746` before any new scoped investigation. No restart CAD or print candidate is accepted.
- The sticker pilot remains paused and unapproved. Accepted V1/V2 source and releases remain owned by `sticker-projects`; recovery does not promote V3 experiments.
- Local-only commits `d47baf1` (blocked Kage R2 evidence) and `dfd4e79` (old no-CI proposal), and stash `5574ede`, are preserved in `cad-projects.bundle`. The no-CI change is superseded by current main; it must not revert modern repository policies.
- Old documentation PR 14 predates the sticker split and newer XT60/Laifen states. Its complete branch is in GitHub and the bundle; current main's project discovery and state pointers govern. Its obsolete mixed-repository changes are not merged wholesale.
- Birthday PR 25 was withdrawn by commit `053cce9`, leaving only broken README/lock references. Those references are not brought into main. Its source history remains on GitHub and in the bundle.
- Historical Kage Trash path `/Users/scottchu/.Trash/kage-cleanup-2026-08-22` was already absent at intake. This backup makes no claim to restore that missing directory from disk; retained committed history remains in the bundle.

## Restore on another computer

Authenticate GitHub, clone the normal main branches, then download recovery assets only if historical work is needed:

```sh
gh repo clone scottchu/cad-projects
gh repo clone scottchu/sticker-projects
gh repo clone scottchu/design-workbench CAD-workbench
mkdir reformat-recovery
cd reformat-recovery
gh release download reformat-recovery-20260929 --repo scottchu/cad-projects
shasum -a 256 -c SHA256SUMS
git clone cad-projects.bundle restored-cad
```

Each numbered tar contains `metadata.json`, `index.patch`, `worktree.patch`, and `payload/`. Extract into a separate staging directory, inspect metadata, and check out its exact `head` in the restored repository. Apply nonempty `index.patch` with `git apply --index`; then apply nonempty `worktree.patch` with `git apply`. Overlay `payload/` at the repository root, preserving symlinks and file modes. Do not apply old snapshots over current main or interpret restored experiments as approved designs.

Git bundles include all advertised refs, but cloning normally exposes branch refs; recreate a non-branch stash/ref explicitly from its hash in `BUNDLE_REFS.json` if needed. Dependency environments, npm installs, compiler caches and Python caches are rebuildable and excluded. Use repository setup instructions after cloning. Historical local preview addresses and processes are not restored services.

## Validation and retirement

Current integration checks: 25 repository/Grenadier Python checks; 10 supported XT60 checks; 6 presentation checks; 26 JavaScript tests; npm workspace builds; uv lock check. The presentation rebuilt to its exact reviewed HTML hash. Imported historical HTML, shaders, G-code, SVG and evidence retain original whitespace; the full diff whitespace check reports those existing bytes, which were not normalized because hashes are authoritative. Newly authored recovery records pass the scoped whitespace check. No new visual, slicer, printer, or physical validation occurred. Added continuity indexes link existing evidence without claiming new independent verdicts.

After this completed-work delivery reaches GitHub main, retire the nine linked CAD worktrees only after comparing their tracked deltas and substantive file hashes with the verified archives. The canonical repositories remain on clean main branches. Final retirement results are attached to the same recovery release as `RETIREMENT.json`; archived source paths are historical identities, not active checkout locations.
