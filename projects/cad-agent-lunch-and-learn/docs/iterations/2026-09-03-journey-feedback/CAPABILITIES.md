# J-O: Orca execution capability audit

Audit date: 2026-09-03. Read-only inspection; no printer, service, deployment, upload, start, calibration, or network-device calls. This is recorded-evidence verification, not a new physical run. Input BRIEF and all primary evidence are frozen in `CAPABILITIES.sha256`.

## Exact state and interpretation

Canonical repository `/Users/scottchu/Projects/personal/orca-slicer-mcp` was at `06e2a903f9ad2426f3580e77e72d65d98cc96d60`, with dirty continuity files (`PROJECT_STATE.md`, `NEXT_AGENT.md`, active HANDOFF/VALIDATION, `docs/widget-delivery.md`). Its current continuity records PR101 deployed as `0710b4bf55edc6908eef614df5fec48614044497`, runtime **0.4.10/schema 14**, observation v16/Camera v12. A subsequent diagnostic slice is pending; it is not a proven camera repair. Reference: `PROJECT_STATE.md:3–32`, active `VALIDATION.md:56–118`.

The requested `7f9f` worktree is older: `f44bd06f7c2a31260045a7a2d3be9a1512120b15`, dirty product-direction/continuity files and untracked decision0033. Its PR58 runtime snapshot must not override the canonical PR101 records. Its `docs/vision.md:3–64` describes workflow ownership and Manager/Teacher/Print Engineer roles as direction; `PROJECT_STATE.md:21–28` expressly says this adds no runtime capability.

**Presentation distinction:** the agent has operated a real slicer and printer successfully using guided shell workflows; the shipped MCP application chiefly exposes read-only observation. These are complementary layers, with different evidence.

## Capability matrix

All paths below are relative to the canonical repository. `LOG23` = `docs/logs/2026-08-23-snapmaker-orca-u1-petg-print-pilot.md`; `LOG25` = `docs/logs/2026-08-25-snapmaker-u1-pla-print-repetitions.md`; `APP` = `plugins/u1-print-studio/app`; `SKILLS` = `plugins/u1-print-studio/skills`.

| Capability | Demonstrated in recorded runs | Implemented / partly automated today | Limit / direction |
|---|---|---|---|
| Slicing | Snapmaker Orca 2.3.5 produced U1 G-code using isolated STLs and resolved profiles; PETG pilot plus two PLA repetitions. LOG23:112–137; LOG25:18–72. | Thin `u1-prepare-print` skill directs actual CLI use and semantic inspection. | No slice tool in current MCP registry. Direct multi-plate 3MF repeatedly crashed or retained invalid bed coordinates. Not universal 3MF compatibility. |
| Profiles and settings | Complete machine/process/four filament-slot inheritance, explicit T2/T3/T1 assignment, walls and temperatures verified in output. LOG23:89–102,128–137; LOG25:20–57. | Prepare skill:20–41 spells out object overrides, bed type and tool verification. | A named preset or exit 0 is insufficient: missing bed selection emitted zero bed heat; object override defeated global walls. No fully automated profile resolver demonstrated as a reusable product service. |
| Orientation and layout | Four isolated identical STL instances were arranged on the U1; in-progress camera showed upright attached parts. LOG25:43–49,63–72. | Prepare skill:31–38 preserves scale/orientation/count and asks geometry/support inspection. | Evidence supports arranging/preserving a selected orientation, not autonomous optimal orientation or tested orientation search. |
| Supports | PETG and both PLA records used support **off**; output setting verified. LOG23:34; LOG25:20–21,34–35,55–57. | Skill accepts explicit support intent/annotations and checks actual support state. | No successful support-generation/painting/optimization run established by inspected evidence. Do not advertise automated supports. |
| Prepared-artifact checks | Tool, settings, layer/object count, movement/extrusion/bounds/temperature checks recorded. LOG23:128–137; LOG25:50–60. | Prepare skill returns artifact/hash/settings separately from uploaded/started states; current knowledge adds genuine embedded-thumbnail inspection tied to final hash (`docs/knowledge/snapmaker-orca-cli-preparation.md:53–99`). | PETG pilot lacked complete source/profile manifest. Current required gates are stricter than historical pilot proof. Generic static validation missed zero bed temperature once. |
| Send / upload / start | Authorized upload, start acknowledgement and observed printing are separately recorded. PETG reached 22/22; PLA reached 380/380 and 188/188. LOG23:139–157; LOG25:23–29,58–72. | Thin `u1-start-print` skill:10–49 specifies readiness, empty-bed evidence, exact artifact, remote verification and fresh printing observation. | No upload/start/control MCP tool in current app. These are demonstrated agent-operated workflows, not a shipped autonomous end-to-end product. |
| Status and focused views | Earlier real status/snapshot calls recorded in `docs/logs/2026-08-25-u1-status-view-prototype.md:42–58,109–129`; live print monitoring in LOG25. | `APP/src/lib/server/app.ts:527–554,861–1089`: `observe_printer` covers overview, progress, thermals, heads, jobs, job_history, queue, fans, bed_mesh. | Domain UI availability is not proof every product requirement is finished: current state retains Queue/Fans/Job History backlog. |
| Camera / monitoring | Adaptive camera/telemetry monitoring observed attached parts and terminal state; first PLA print physically accepted. LOG25:25–29,63–84. | Snapshot/Live UI and service deployed; `u1-monitor-print` skill:12–37,53–80 guides adaptive checks and explicit completion criteria. | Latest user sequence is failure → success after retries → failure around 10 s; Live reliability unresolved. No autonomous physical defect detection/control acceptance. N/N layers alone is not completion. |
| Other real software | Read-only inventory/status and camera transport logged; service shipping and installed-resource behavior separately recorded. | Bed mesh 3D/2D, head/filament temperatures, fans, queue, current job/history projections; privacy/freshness handling; MCP/HTTP/CLI adapters. Registry test `APP/tests/server/app.test.ts:540–583` asserts 2 model-visible + 8 app-only tools. | Bed mesh viewing is not bed calibration. Queue viewing is not queue mutation. No generic G-code/admin passthrough. |

## Software validation evidence

Active `VALIDATION.md:56–118` records exact PR101 independent approval and passing `./scripts/check-repository.sh`: 594 UI tests, 327 server tests/3979 assertions, plus service/shipping tests. Installed Camera resources passed synthetic-host behavior. This audit inspected source/test/record correspondence; it did **not** rerun that suite or claim synthetic media proves real Live connectivity. Current source registry and its matching inventory test independently support the read-only tool classification.

## Actual visual assets inspected

Three existing ignored test screenshots were opened visually and frozen. They are **actual application UI with synthetic fixture data**, not printer photographs, current telemetry or exact deployed-byte acceptance. Their screenshot-generating revision was not recovered; label them “U1 Print Studio UI · test fixture.”

- `APP/test-results/heads-390.png`: four head/material cards and controls; visible “Lab fixture,” generic PLA/PETG, temperatures. Includes a Copy-unavailable toast; prefer a clean replacement if convenient.
- `APP/test-results/overview-590.png`: clear compact overview of all eight observation domains; visible lab fixture and refresh toast. Useful execution-layer illustration; numbers are synthetic.
- `APP/test-results/bed-mesh-orbit-390-false.png`: actual plotted 3D mesh UI, fixture Z/XY axes; no evidence of measured printer bed quality.

No private camera recording, model, profile, address, identifier or credential is included. These assets may be copied by the presentation owner from their exact frozen paths, retaining fixture labels.

## Story facts and suggested concise wording

“The agent can run the slicer, check the output, send an authorized job, and watch it finish. That already happened in recorded experiments. The product runtime currently concentrates on read-only observation; preparation and start remain guided workflows.”

Show the execution layer **beneath** agent judgment: selected experiment → prepare → inspect → authorize/send → observe → physical evaluation → update shared model. Preserve each boundary. The PETG printed successfully but its mechanism failed after assembly; first PLA was physically accepted; second PLA was telemetry-complete with handling unverified. Those outcomes directly illustrate why tool execution does not replace acceptance.

## Receipt

Status: complete. Changed only this report and `CAPABILITIES.sha256`. Commands: `git status --short`, `git rev-parse HEAD`, explicit `/opt/homebrew/bin/rg` inventory/targeted searches, bounded `sed`/`nl` reads, `view_image` of three existing fixture screenshots, SHA-256 of declared inputs. No tests rerun, installations or source-project edits. High-severity presentation risk: conflating successful manual orchestration, current read-only MCP, synthetic tests and physical acceptance. Next: use the matrix and one labeled UI image in the deck; retain real outcome limitations in speaker notes.

## Focused frozen-snapshot refresh — 2026-09-03

Five mutable canonical documents changed during the first audit. The root captured them in `/tmp/cad-journey-evidence/orca-refresh/map.json`; this follow-up read those exact snapshot bytes and verified all five declared SHA-256 values before replacing only those five source-path entries in `CAPABILITIES.sha256`. The map itself is also hashed. Original source-to-snapshot association:

| Original path under canonical Orca repository | Frozen snapshot |
|---|---|
| `PROJECT_STATE.md` | `/tmp/cad-journey-evidence/orca-refresh/8c5fe263e5ff-PROJECT_STATE.md` |
| `NEXT_AGENT.md` | `/tmp/cad-journey-evidence/orca-refresh/07be7863a136-NEXT_AGENT.md` |
| `docs/requirements.md` | `/tmp/cad-journey-evidence/orca-refresh/1b7b992a2558-requirements.md` |
| `docs/iterations/2026-08-23-f0-dual-subsystem-foundation/HANDOFF.md` | `/tmp/cad-journey-evidence/orca-refresh/ef96842fffd9-HANDOFF.md` |
| `docs/iterations/2026-08-23-f0-dual-subsystem-foundation/VALIDATION.md` | `/tmp/cad-journey-evidence/orca-refresh/feeb1b181841-VALIDATION.md` |

**Capability classification unchanged.** These snapshots still identify PR101 (`0710b4bf55edc6908eef614df5fec48614044497`), runtime 0.4.10/schema14, observation v16/Camera v12 as deployed, and still report intermittent phone Live failure. Successful historical jobs and the two-model-visible/eight-app-only read-only registry are unaffected. This is an as-of snapshot claim, not a query of current running services.

**Candidate scope changed, explicitly not deployed:** default Auto with only Auto/Live modes; quiet automatic snapshot polling; no automatic Live on a new mount; compact 88×44 Switch; safe failure-stage footer diagnostics. Shared Footer packaging now plans **Camera v13 and observation v17**, with 32 resources/30 preserved old aliases. Both candidate validation and deployment remain pending. This supersedes the initial report's earlier diagnostic-only scope description, without upgrading any capability. New snapshot references: PROJECT_STATE:3–43; NEXT_AGENT:3–45; HANDOFF:3–44; requirements CAM-008:196–265; VALIDATION:38–66 (candidate) and 68–139 (retained PR101 validation/deployment). Existing earlier line references into these five mutable docs refer to first-pass positions; use these frozen-snapshot sections for current status.

The preparation and handoff requirements were checked again at requirements:569–643: artifact/profile/support provenance and genuine embedded-thumbnail gates remain requirements, not proof of generalized automated preparation/start. No tests, device calls, new research or source-project writes occurred. All other manifest entries retain their original expected hashes; the root's `/tmp/cad-journey-evidence/map.json` supplies matching frozen copies.
