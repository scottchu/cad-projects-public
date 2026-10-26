# Direct editing handoff

Current request revision3: remove mode toggle; drag each endpoint directly,
translate whole rail by dragging it, and shape each curve using its midpoint dot.
Implemented and checked on the existing private Tailscale URL; bounded
independent review passed. PR delivery receipt follows. Exact source/contract candidate is CANDIDATE.sha256.
The prior recovery iteration remains historical and its fingerprint is preserved.

Hosting: loopback5208, Tailscale HTTPS8480; only the single HTML is served.
Task-owned server PID and log are in ignored scratch/rail-hosting; retain that
active runtime and the worktree. Do not delete scratch wholesale or stop this
server during browser-diagnostic cleanup.


## Final outcome

Direct endpoint, whole-path and curve-dot editing implemented and verified on
the same HTTPS URL. Both reference-layer hit-test defects fixed and covered by
BROWSER_CHECK.py, a durable repeatable browser regression. Eight focused Node
checks, all workspace tests/builds and 11 repository checks pass. Critic,
numeric validator and formal evidence join PASS with explicit packet limits.
The final HTTP response matches the standalone HTML SHA256 in VALIDATION.

No hosted CI configured, no merge authorized. Updating existing PR27 preserves
this correction and the reviewed source manifest. The previous recovery
manifest is historical, tied to its earlier source commit, not this iteration.

Cleanup preserves active scratch/rail-hosting runtime/PID/log and the worktree
because the preview reads its HTML. Diagnostic browser output and dependency
symlink can be retired after records readback; browser reproduction is tracked
in this iteration. Primary main and unrelated worktrees remain untouched.
