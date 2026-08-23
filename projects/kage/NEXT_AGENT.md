# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`, `docs/decisions/README.md`, and every file in the iteration named by `docs/iterations/CURRENT`. Recompute `manifests/candidate.sha256` and require `495265a08a78dcd5fd2639ab41e8e9ef0aa62595e106f1229b6fa7a6355ed60a` with 805 rows before acting.

Pull request [#5](https://github.com/scottchu/design-projects/pull/5) is the delivery record for the formally accepted reversible Kage cleanup plus the generic repository launcher `bin/preview-cad`. Kage owns no launcher wrapper. Its pinned reference invocation is:

```sh
bin/preview-cad --sha256 dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7 \
  projects/kage/references locked-direct-gear/p3_v3_direct_gear_race_assembled.step
```

Both retired trees must remain intact under `/Users/scottchu/.Trash/kage-cleanup-2026-08-22`; do not empty Trash. Require both old active paths and the restart worktree registration to remain absent and branch `kage/restart-20260822` to remain. Migration delivery is recorded in pull request [#2](https://github.com/scottchu/design-projects/pull/2); pull request #1 remains superseded. GitHub Projects are no longer used. Do not resume Half-Z or promote Q3-R0. The only next CAD action is `KAGE-EXP-001`: first author the minimal restart-namespace two-half Q3 seam coupon and focused geometry/export test defined in the restart design record; no coupon exists now.
