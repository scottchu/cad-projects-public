# Rail customizer handoff

Status: reconstructed simulator implemented and self-checked; independent
review/edge-case repair and PR delivery in progress. Root owns integration.

Open `preview/xt60-rail-customizer.html` directly in a browser. Source lives in
`preview/rail-customizer/`; rebuild from repository root with
`npm run build:rails --workspace projects/xt60-bend-jig`. The user explicitly
requires both OPEN and END editing. Default equations come from the frozen
P20 R4 profile, not rounded screenshots or a redesigned mechanism.

See BRIEF for RC-1..6, DESIGN for geometry/interaction decisions, VALIDATION
for exact checks and REVIEW for independent findings. CANDIDATE.sha256 freezes
decision inputs and delivered source/HTML. Mutable evidence records are excluded.

No geometry, STEP, slicer, printer or service was operated for this task.
P19 remains the accepted digital baseline; P25 is first-CAD preview only.
The default thin-rim/web warnings and whole-product physical gaps remain open.

Task worktree: `/Users/scottchu/Documents/Codex/2026-10-26/task/xt60-rail-customizer`,
branch `recreate-xt60-rail-customizer`. Root npm install and Python environment
are in the canonical primary repository. The temporary task-root node_modules
symlink must be removed after checks. Ignore and retire only task-owned scratch
after durable results and recovery are verified. Keep worktree until its HTML
and pending PR are safely retained; no merge authority was requested.


Independent critic/validator and formal evidence join PASS on the repaired
candidate. The formal reviewer used a relayed packet because its direct tools
failed; exact limits are in REVIEW. All required local checks passed. Root
opened the standalone HTML via macOS. PR commit/push/readback is the remaining
delivery step. Temporary dependency symlink removed; canonical install retained.
