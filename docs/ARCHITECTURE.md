# Repository architecture

This repository contains independent projects under `projects/<project-slug>/`. Each owns its source, generation logic, dependencies, tests, requirements, decisions, assets, releases and physical observations. Historical project records remain at their established paths.

CAD Workbench owns reusable capabilities, workflow policy, recipes, templates, skills and viewer-service source. [workflows-binding.json](workflows-binding.json) identifies its exact revision and policy-manifest hash. The four legacy policy filenames here are compatibility pointers. Skills are external source packages requiring explicit discovery; no skill, plugin or service is installed by this binding.

The root uv workspace uses Python 3.12, one `.venv` and one `uv.lock`. The root npm workspace uses one install and `package-lock.json`. Project manifests own dependencies; root manifests provide workspace configuration and repository-check tools. Run tooling from the root and never use another checkout's environment as a fallback. See README for setup and validation commands.

Current project entrypoints include README.md, PROJECT_STATE.md, NEXT_AGENT.md, PRINTING_PROFILE.md and project-local requirements, experience, decisions and active iteration records. Printing profiles retain intended settings and verified-run evidence. [WORKSHOP.md](WORKSHOP.md) retains local equipment facts. Existing historical paths can mention superseded tools; consult the current binding when executing work.

The Example sticker project moved to the private sticker-projects repository, retaining `projects/example-sticker-pack` paths and history. The source recovery branch `recovery/workflow-ownership-71d661c` retains the pre-separation tree. Distinct V3 WIP is preserved in the destination recovery archive and original worktree; it is not overlaid onto accepted releases. See [separation records](iterations/2026-09-07-workflow-ownership/HANDOFF.md).

Trunk-bound changes use a non-main branch and GitHub pull request unless explicitly overridden by the user for that change. The repository-local declaration is `.github/repository-policy.toml`. Repository-hosted CI workflows are not used; their absence does not waive testing. Project source/CAD, written artifact/slicer and physical acceptance remain separate evidence states under the bound workflow.
