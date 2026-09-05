# Repository documentation refresh design

## Frozen selected design contract

Baseline: `5c147579bd5870b65dc8fc4e54ed65ea89962085` on
`codex/refresh-project-documentation`. Frozen repository/project inputs are
listed by path and content in `INPUTS.sha256`, whose SHA-256 is
`30dc2df5386a273919ef1d6359839510ec97ffdb6f332360554d7a2f5c56bd73`.
The separately admitted baseline Example printing profile is frozen in
`PROFILE_INPUT.sha256`, whose SHA-256 is
`de071c40d8cba1ad1d7acda3cfb3a0534de8e016f6c5212204233baa81de900f`.

The root README opens with the three checked-in projects and their current
evidence boundaries, followed by the repository introduction, setup, validation,
and policy. Project links lead to each README, state, and next action. The
existing root validation command contract remains verbatim so this refresh does
not silently redefine required gates.

Example current-facing documentation presents V2 anatomy R1 as the formally
accepted private prerelease delivered through merged PR #13. It retains the
separation between accepted local assets/GitHub delivery and unverified
LINE/WhatsApp client, service, and privacy behavior. Its N/A printing profile is
normalized to the repository-required headings and points to the real-client
test rather than the already completed export implementation. Setup is
dependency installation only; immutable V1/V2 release paths are never presented
as safe build targets. Reproduction and validation point to the accepted
anatomy-repair evidence and require an isolated disposable checkout.

XT60 current-facing documentation presents P19 R1 as the accepted CAD/STEP
baseline delivered through merged PR #11. Its focused P19 test is the first
project test command. CAD and Viewer instructions use the installed workflows
without a versioned plugin-cache pin or stale worktree endpoint. Viewer startup
is bound to `VIEWER_CAD_PYTHON="$PWD/.venv/bin/python3"` from the repository root,
with `uv sync --all-packages --all-groups` as the repair path. Historical P13 root
regression commands, P17/P18 history, and all physical unknowns remain.

Kage current-facing documentation already accurately describes a clean restart
with no accepted mechanism and the direct installed Viewer workflow. It remains
unchanged to preserve its manifest-protected evidence.

Continuity addenda are appended to the two touched projects' state, next-agent,
and current handoff records. They record only the documentation reconciliation;
`CURRENT`, source, tests, generated artifacts, locks, manifests, and prior
verdicts remain unchanged. Include the applicable content in every dependent
task's manifest.

## GitHub repository description proposal

If the independently reviewed documentation candidate is accepted, update the
private repository's GitHub About description to:

> Personal design monorepo for digital artwork, parametric CAD, simulation,
> fabrication, and physical validation.

This metadata change is delivery work for the root coordinator after review. It
does not change repository policy or any project acceptance state.

## Rejected approaches

- Listing migrations before real projects: rejected because all three projects
  are already present and have current authority records.
- Presenting Example V2 as planned or text-free: rejected by the accepted
  anatomy-repair release and source-selective typography evidence.
- Updating Kage for symmetry: rejected because no demonstrated stale
  current-facing claim requires a change.
- Pinning a current CAD plugin cache path or reusing an old Viewer URL: rejected
  because installed skills and the current absolute workspace are runtime
  authority.
- Rewriting historical iterations or candidate manifests: rejected because this
  refresh changes navigation and current status, not historical evidence.

## Residual risks

- GitHub links require repository access because the repository and Example
  prerelease are private.
- Installed CAD and Viewer workflows can change; their current skill entrypoints
  must be read at execution time.
- README summaries are navigation aids. Project state, active iteration records,
  manifests, and exact artifacts remain the detailed authority.
