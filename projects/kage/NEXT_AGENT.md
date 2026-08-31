# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`, `docs/decisions/README.md`, and every file in the iteration named by `docs/iterations/CURRENT`. Recompute `manifests/candidate.sha256` and require SHA-256 `da3bcedc68ed5324cf805f42ff0bca48cd1ccbcf89db7aa9207908b5df27f631` with 805 rows before acting.

Pull request [#5](https://github.com/scottchu/design-projects/pull/5) records the formally accepted reversible Kage cleanup plus the now-superseded generic preview launcher. Pull request [#6](https://github.com/scottchu/design-projects/pull/6) records its removal and the accepted direct-Viewer workflow. Do not restore that launcher. Use the installed `cad-viewer` workflow directly with:

```text
workspace: projects/kage/references
file: locked-direct-gear/p3_v3_direct_gear_race_assembled.step
```

Resolve the workspace to an absolute path. Before returning a ready link, require the exact review page HTTP `200` and exact artifact endpoint HTTP `200` with JSON `state == "ready"`. After visual inspection, the general claim is limited to “the requested artifact rendered with no visible error state”; every feature-specific claim must name the inspected features and views. The locked STEP SHA-256 remains `dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7`.

Both retired trees must remain intact under `/Users/scottchu/.Trash/kage-cleanup-2026-08-22`; do not empty Trash. Require both old active paths and the restart worktree registration to remain absent and branch `kage/restart-20260822` to remain. Migration delivery is recorded in pull request [#2](https://github.com/scottchu/design-projects/pull/2); pull request #1 remains superseded. GitHub Projects are no longer used. Do not resume Half-Z or promote Q3-R0. The only next CAD action is `KAGE-EXP-001`: first author the minimal restart-namespace two-half Q3 seam coupon and focused geometry/export test defined in the restart design record; no coupon exists now.

## Printing-profile addendum — 2026-08-31

Read [PRINTING_PROFILE.md](PRINTING_PROFILE.md) before future manufacturing work.
For repository integrity only, use the new 806-row snapshot
`a49cdaf17eed504e7aba262d844499efba6da3ed6874fbfafa76ea43d9f7306f`
instead of the historical 805-row check above. Only shared printing policy and
the new profile changed in that manifest; the old verdict is not transferred.
See the [repository-policy handoff](../../docs/iterations/2026-08-31-printing-profiles/HANDOFF.md) for independent status.
No new design baseline, selected process or upright-fastening approval follows.
