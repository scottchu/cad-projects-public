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

## Execution DAG and owners (mutable coordination)

| ID | Role / owner | Dependencies | Exclusive writes | Done gate | Budget/status |
| --- | --- | --- | --- | --- | --- |
| D1 | Narrative and evidence design / deck_design | approved brief | project DESIGN.md, REQUIREMENTS.md, SOURCES.md, input manifest, initial README/pyproject/EXPERIENCE/decision index/PRINTING_PROFILE | sourced slide plan, exact claims, visual paths, frozen input manifest | strong/high, ~8 minutes, 12k tokens, initial + 2 focused repairs; ready |
| V0 | Validation environment / deck_validation | approved brief | temporary validation tooling outside repository | identify an isolated local browser verification route | strong/high, ~3 minutes, 4k tokens; ready |
| I1 | HTML implementation / deck_implementation | D1 frozen | project index.html, source builder if needed, assets, package.json, focused tests, README usage | complete offline deck and author checks, candidate manifest | balanced/medium, ~12 minutes, 18k tokens, initial + 2 repairs; waiting |
| R0 | Narrative/source pre-review / deck_review | D1 frozen | REVIEW.md draft | identify any material factual or narrative defect before HTML freeze | strong/high, ~3 minutes, 5k tokens; ready |
| V1 | Independent validation / deck_validation | I1 frozen | VALIDATION.md, temporary screenshots outside tracked tree | browser behavior, render/overflow evidence on every slide, print and offline checks, findings against exact manifest | strong/high, ~8 minutes, 12k tokens, initial + 2 reruns; waiting |
| R1 | Independent review / deck_review | I1 frozen; final verdict joins V1 | REVIEW.md | factual/narrative and visual review, coverage and evidence-boundary audit, final verdict | strong/high, ~8 minutes, 10k tokens, initial + 2 reviews; waiting |

Root owns only coordination, provenance checks, synthesis, and concise continuity indexes. At most three workers active; implementation source has one writer. Validation/review may run concurrently read-only against one frozen candidate. Repairs invalidate affected gates and go back to the original role owner.

Environment note: template/dependency-loader and browser-control execution tools were not exposed after discovery. The artifact remains HTML (no PowerPoint builder required). Browser skill was read; validation may use an isolated headless browser fallback with a fresh temporary profile, without accessing user browser data. The repository's Python environment is absent; prefer the installed Node runtime and no added dependencies.

Each owner declares a SHA-256 path/content manifest of relevant immutable inputs, with mutable status/evidence records excluded, verifies it on return, and reports status, changed paths, commands/results, findings, coverage, risks and next action. No per-agent diaries or raw conversation transcripts.

## Delivery gate

## User-authorized follow-up: private Tailscale presentation

H1 / `presentation_host`: bounded hosting implementation, independent of presentation editing. User explicitly requested a Tailscale link. Inputs: existing `CANDIDATE.sha256` (manifest hash `b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`) and HTML hash `911353124f9ab5a7537333d126ff4ad0da3a9d162491a2f4dac33f605f89d81f`. Read-only project artifacts; exclusive writes: dedicated preview service under user Library, one unused private Tailscale Serve path on HTTPS 8448, and `HOSTING.md` in this iteration. Preserve every existing handler and Funnel setting. Done: persistent loopback service, private HTTPS 200, response hash equals artifact, existing configuration preserved. Balanced/medium, ~5 minutes / 6k tokens, initial plus two focused repairs, one worker. Stop on port/route collision or unrelated configuration changes. Receipt records commands, service identity, URL, hashes, verification, recovery and limitations. Root performs focused independent URL/hash verification and continuity synthesis. Existing artifact acceptance does not authorize printer actions.

V2-D / `presentation_visual_design`: after the accepted first deck, design a bounded enhancement requested by the user: explicit diagrams/flow charts/table and a Three.js teaching simulator. Read the frozen first-deck candidate and source register. Exclusive writes: a new `2026-09-01-visual-simulator` iteration contract/manifests, requirements addendum and decision/experience records. No source-project or HTML edits. Done: grounded compact design with exact slide changes, simulator mathematics and limitations, offline dependency plan, and frozen implementation inputs. Strong/high, ~5 minutes / 8k tokens, initial plus two focused repairs. Root activates dependent implementation and distinct validation/review roles after freeze.

V2-E / `presentation_visual_validation`: environment preparation parallel to V2-D, with no candidate acceptance yet. Read-only baseline HTML and prior temporary CDP harness; write only a new temporary browser harness. Done: isolated browser with a real working WebGL2 context suitable for later Three.js checks, and recorded exact invocation. Fast/low, ~2 minutes / 3k tokens, initial plus one retry. No dependencies, project source, user browser profile or runtime-host changes. Same independent validator may continue V2-V after the implementation candidate is frozen.

Final status: D1/V0/I1/R0/D2/I2/W1 complete; independent V1 and R1 PASS for HTML candidate `b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`. The 22-slide local first draft is ready for user review. Actual browser, source-provenance and 22-page print evidence are in VALIDATION.md and REVIEW.md; HANDOFF.md is the concise continuation index. No P1/P2 findings remain. Minor UI polish limits remain visible in REVIEW.md, not hidden by the acceptance result.

W1 / deck_implementation: after I2, refresh the root workspace lock metadata for the new dependency-free project if required. Exclusive writes are `uv.lock` and `package-lock.json` plus a compact workspace receipt; no dependency upgrades or installs. Preserve the ten-file HTML candidate and its acceptance gates. Done: workspace registries include the project, generated lock diff is limited to this addition, and the HTML candidate still verifies. Ceiling ~2 minutes / 2k tokens, initial plus one focused retry; stop on unrelated dependency churn.

Reopened implementation design after I1's two focused repair cycles: candidate `8b200517637b42569e8e51e232a51679847bc5e2e6a8476158f400db70b62783` passes desktop story/behavior but exposes three bounded design weaknesses: page/component selector collision creates an extra print page; late component CSS overrides the mobile Kage diagram; manual source-hash copying introduces a provenance typo. D2 / deck_design owns a compact revised implementation contract for isolated page/component styles, responsive rule priority, and source-register-derived hashes (~2 minutes, no narrative change). I2 / deck_implementation implements only that frozen contract (~3 minutes, initial plus at most one focused repair), then V1 and R1 verify the exact new candidate. This is a scoped design reopening, not another unspecific I1 repair loop. Preserve prior receipts and rendered evidence.

Coordination checkpoint: D1 complete after one focused repair to include bounded multi-agent development separately from long-term product roles. Final design manifest SHA-256 `520a8871f4056ae9278c7210f2f543cb5a7be627cbb65245776400f0bc94cb46`, 26/26 entries verified. V0 passed via isolated headless Chrome and Node built-in CDP, without dependency installation. I1 now ready; V1 and R1 wait for its candidate.

Openable HTML, coherent story, truthful source-linked examples, no broken assets, usable keyboard/presenter controls, legible slides at common laptop/projector sizes, independent validation and review with material issues resolved. Update PROJECT_STATE, HANDOFF and NEXT_AGENT. Keep delivery local for this presentation-first review; GitHub PR is required if subsequently delivered to main.
