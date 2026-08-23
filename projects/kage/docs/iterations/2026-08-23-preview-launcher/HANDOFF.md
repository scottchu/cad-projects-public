# Preview launcher handoff

## R3 safety scope reduction — current

Independent critic found a high PGID-reuse risk in candidate `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f`, plus join/wait gaps. `KAGE-PREVIEW-001-R3` reopens design rather than authorizing a third focused repair. The candidate and all downstream review/validation evidence are invalid for delivery, while prior findings remain historical.

R3 preserves the generic root tool and Kage consumer contract but removes every KILL path. A pre-existing stale Viewer requires exact listener token/API/page revalidation before TERM; post-TERM API loss is expected while waiting for that token to vanish or the port to free. An invocation-owned process group requires a stable leader token; mismatch/absence receives no signal, match receives TERM only. Artifact-ready must be followed by exact `CURRENT_TOKEN` equality before URL output.

## R3 next action

Assign a new implementation against R3 with the added hermetic generation-token regressions. It must not recycle candidate `3d6609aa…` evidence. After a new candidate is frozen, route it to distinct critic and validator roles, then formal review.

## R2 architecture amendment — current

The user expanded this work to a repository-wide generic launcher. `KAGE-PREVIEW-001-R2` supersedes the Kage-local implementation architecture: the accepted target is root `bin/preview-cad [--sha256 EXPECTED] <workspace-dir> <file-relative-to-workspace>` with root `tests/test_preview_cad_launcher.py`; Kage is only a checksum-pinned consumer. The prior local-candidate findings/evidence below are retained as history, but candidate `715e85…` and its in-progress repair are invalid and must not advance to critic/validator/formal review. R2 still requires bundled npm fallback, listener/PID safety, owned-startup cleanup, dynamic current-runtime provenance, SPA shell health, URL encoding, and HTTPS Tailscale reachability warning.

## R2 next action

Assign a new `KAGE-PREVIEW-002` implementation against frozen R2. It must remove/supersede the Kage-local launcher and test, then produce a new root-tool candidate manifest. Kage validation must invoke the generic CLI using `projects/kage/references`, `locked-direct-gear/p3_v3_direct_gear_race_assembled.step`, and its mandatory SHA-256. Only then route that new exact candidate to separate critic and validator roles.

## R2 implementation receipt — KAGE-PREVIEW-002

Root `bin/preview-cad` and `tests/test_preview_cad_launcher.py` now supersede the deleted Kage-local launcher/test. Kage README supplies the checksum-pinned consumer command and `manifests/cad-viewer-runtime-0.4.25.sha256` records the selected runtime inputs. No CAD/reference bytes, port, listener, or live process were touched. Independent critic and validator must treat the regenerated candidate as new and audit the generic lifecycle/safety paths before any acceptance.

## Current status

Design contract frozen by `KAGE-PREVIEW-001`. Implementation `KAGE-PREVIEW-002` added `bin/preview-cad`, hermetic launcher tests, the minimal migration-integrity runtime-debris exclusion, README usage, and a regenerated candidate manifest. It did not launch a real Viewer, touch port 3245, change CAD/reference artifacts, or approve the candidate.

## Next action

Route the frozen candidate independently to critic `KAGE-PREVIEW-003` and validator `KAGE-PREVIEW-004`; do not treat implementation self-check as approval. The validator must recompute `manifests/candidate.sha256`, run the full Kage suite and a controlled real launch only after confirming listener identity, then record the exact candidate fingerprint.

## Open risks

Port ownership/PID reuse, Viewer runtime API drift, missing root runtime/npm, and Tailscale reachability remain to be validated. Preview success is not restart-CAD, slicer, or physical acceptance.

## Repair cycle 2 supersession

Root rejected candidate `a489fbe8496ae2d8eaf4309c06bd3ec9339277e37b59fab9c7a4fd6934d81c9e` (805 rows) because its three root tests and incomplete launcher did not cover the frozen ownership, stale-listener, startup-cleanup, artifact-state, and output contract. Repair cycle 2 supersedes it with the final fingerprint recorded in `manifests/candidate.sha256`; no evidence or acceptance from the rejected candidate carries forward. Route only the repair-2 fingerprint to distinct critic and validator identities, then join them in formal review. Do not live launch or deliver from this implementation receipt.

Repair cycle 2 froze candidate `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f` with 805 rows. Implementation self-checks passed: root launcher `23`, Kage migration-integrity `7`, repository structure `12`, six runtime-provenance hashes, independent `805/805` candidate recomputation, mode/syntax, and `git diff --check`. This is not approval. The next action is independent critique and validation against exactly that fingerprint; controlled live launch belongs only to the validator after listener-safety preflight.

## R3 implementation receipt

Candidate `3d6609aa35269072f8bad57e45d85cf0463646a6201f761f30e7feb6000c539f` and its live-pass evidence are invalid for delivery because the reopened safety contract rejects all KILL paths and requires exact owned-leader and final-listener generation joins. The same implementation workstream made the smallest source/test change and froze R3 candidate `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a` with 805 rows.

R3 implementation self-checks passed: launcher `27`, Kage migration integrity `7`, repository structure `12`, six runtime-provenance hashes, independent `805/805` candidate recomputation, syntax/mode, no production KILL action path, and `git diff --check`. Production cleanup now sends only one `TERM` after an exact generation-token recheck; absent/drifted ownership fails without a signal, stale post-TERM API loss is tolerated only while waiting for exact-token disappearance/port release, and final listener-token replacement suppresses stdout. No live action was run. Route only `495265a0…` to distinct R3 critic and validator identities, followed by formal review; do not reuse R2 acceptance.

## Final R3 acceptance and delivery handoff

- Accepted candidate: `projects/kage/manifests/candidate.sha256` SHA-256 `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a`, 805 sorted unique final-LF rows with `805/805` content checks passing.
- Ownership: the reusable launcher is repository-root `bin/preview-cad` with root `tests/test_preview_cad_launcher.py`. Kage has no local wrapper or launcher test; it owns only the checksum-pinned historical-reference command and runtime-provenance record.
- Independent gates: critic passed with no critical, high, or medium finding; validator passed launcher `27`, focused lifecycle `7`, Kage integrity `7`, repository structure `12`, and runtime provenance `6/6`; formal reviewer accepted `KAGE-PREVIEW-005` for preview scope only.
- Safety: production has no KILL action path. Cleanup sends TERM only after an exact generation-token match, never signals absent or drifted ownership, and suppresses URLs if the final listener generation changes.
- Live evidence: healthy Viewer PID `92119` was reused without a signal and left running. Local page, artifact state, and external HTTPS page returned HTTP 200; the artifact reported `state: ready`; the locked STEP remained `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.
- External review URL: `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/b478a5e4-c0d0-4bb2-a265-df482c0a1937/design-projects/projects/kage/references?file=locked-direct-gear%2Fp3_v3_direct_gear_race_assembled.step&cb=1787527287`.
- Residual low risks: canonical symlink-target CR/LF, newline-bearing Tailscale host override, positive-checksum/type-matrix test completeness, and the theoretical pre-capture PID-generation race under the TERM-only model. These are explicitly nonblocking and belong in a separately manifested hardening change.
- Delivery: pull request [#5](https://github.com/scottchu/design-projects/pull/5) is authorized for the accepted cleanup plus generic-launcher scope. The Trash recovery copy remains untouched and must not be emptied.
- Acceptance boundary: this proves launcher/reference rendering only. It does not accept restart CAD, slicer/fabrication readiness, or physical print/assembly behavior. After delivery, the sole next design action remains `KAGE-EXP-001`.

Role receipt ledger: design `/root/kage_preview_design`; final implementation `/root/kage_preview_impl_repair2`; critic `/root/kage_preview_critic`; validator `/root/kage_preview_validator`; formal review `/root/kage_preview_formal_review`.
