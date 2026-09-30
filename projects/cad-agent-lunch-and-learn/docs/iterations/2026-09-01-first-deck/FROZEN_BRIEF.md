# First HTML presentation

## Frozen user brief

Build an English HTML lunch-and-learn presentation about the user's 3D CAD and agent-managed slicer-MCP workflow. Tell the reasoning journey: why/how/what; expected reality versus observed reality; identify and understand the gap; decompose into phases and subsystem responsibilities; compose the system; obtain feedback and repeat. Kage and XT60 jig clamp are the central real histories. Discuss the many iterations, challenges, how they were tackled, and how the working process evolved. Presentation first; a live end-to-end demo is future work.

Working assumption: mixed technical audience, 40–45 minutes including discussion. Deliver a standalone offline HTML deck with embedded real existing visuals where available, presenter notes, honest evidence and source references, keyboard navigation, overview and print layout. The first draft should be easy to review and revise.

## Baseline and boundaries

- New project `projects/cad-agent-lunch-and-learn`, branch `codex/cad-agents-lunch-and-learn`, parent `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`.
- Read-only source histories: this worktree and `/Users/scottchu/Projects/personal/design-projects/projects/{kage,xt60-bend-jig}`; slicer vision and ADR 0033 in `/Users/scottchu/.codex/worktrees/7f9f/orca-slicer-mcp`.
- No CAD/source changes, new slicing, printer actions, deployment, publication, or claims of physically proven mechanisms.
- Distinguish directory/amendment counts from build-test/print counts; distinguish planned responses from completed repairs. Do not present target product vision as current integrated capability.
- No dependency installation outside repository-managed workspaces; prefer zero-runtime-dependency HTML and JS.


This immutable extract excludes mutable task orchestration and status.
