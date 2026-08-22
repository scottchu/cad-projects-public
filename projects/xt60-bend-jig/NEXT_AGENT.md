# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`, `docs/decisions/README.md`, and every file under the iteration named by `docs/iterations/CURRENT` before changing the project.

## Exact baseline

- Repository project: `projects/xt60-bend-jig`
- Completed baseline iteration: `p13-r1-monorepo-migration`
- Supported design: P13 only
- Authoritative source: `src/xt60_bend_jig/p13_four_plate_three_rod.py`
- Imported source SHA-256: `e424fac8064d35713ed15748bb8a0e1f966ef429b507ba4be5a5dc31cfc7c72b`

## Immediate task

- Create `docs/iterations/p13-r2-center-hole-fit-repair/`, update `docs/iterations/CURRENT`, and record the defect before changing source.
- The user printed the latest P13 version. The user's exact observation is: the "middle stick" is too thick for the "center hole". Treat this as a real physical assembly failure.
- Identify the exact printed parts and mating feature from source and release artifacts. Do not infer that every rod/shaft bore needs the same change.
- Add a regression that represents the failed fit, then enlarge only the responsible source-controlled hole through a named parameter.
- Regenerate every affected STEP, 3MF, and provenance artifact; rerun focused solid/export tests and snapshots.
- Start CAD Viewer on a Tailscale-reachable host and provide the exact Tailscale render URL in the handoff and final response.
- Use root-owned `uv` and npm workspaces; do not create nested environments or locks.

## Preserve

- Do not modify either legacy source directory.
- Do not redesign P13 during migration.
- Preserve the current fixed 90-degree outcome, four-plate/three-rod architecture, purchased rod constraints, source-defined print orientation, and separate acceptance states.
- Preserve physical observations in `docs/EXPERIENCE.md` and legacy files under `docs/legacy/`.

## Do not assume

- Historical validation is not current-workspace validation until reproduced.
- CAD/source acceptance does not imply written artifact, slicer, or physical acceptance.
- `4.15 mm` is evidence for the sliding rod-hole role, not a universal bore dimension.
- The user's "middle stick" and "center hole" identify a real printed-fit failure but not yet an unambiguous CAD feature. Diagnose the exact interface before resizing it.
- Session history is not authoritative when it conflicts with repository evidence.
