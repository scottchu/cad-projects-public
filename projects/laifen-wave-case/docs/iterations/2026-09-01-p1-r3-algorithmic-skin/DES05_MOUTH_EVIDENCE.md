# DES-MOUTH-05: measured mouth geometry and native tolerance metadata

Owner `/root/skin_design`, design/evidence disposition only, 2026-09-02. Scope: this file and `inputs/mouth-evidence-*`; no CAD, tests, configuration, tolerances or prior contracts changed. Task-specific input manifest binds the exact DES03 implementation source, Params, copied-curve probe/output and governing contracts; moving skin work is excluded.

## Decision and exact scope

**PASS for the measured C20 mouth endpoint, Z-plane/range and lifted-p-curve endpoint criteria.** The DES03 cutter extension has removed the prior negative-Z curve extension in this diagnostic. Its native vertex tolerance field alone does not justify another thread redesign. This is a narrow disposition of actual source mouth geometry, not whole-cap CAD/BOP, thread profile, written STEP, skin, slicer or physical acceptance.

DES03's additional `corresponding vertex tolerance<=1e-4mm` automatic-rejection clause is explicitly superseded: **native tolerance above1e-4 triggers recorded geometric verification; it is not itself a measured-error failure**. All actual endpoint/plane/p-curve limits remain1e-4mm, source/written mouth boundary correspondence remains<=0.001mm, and the global functional geometry limit remains0.01mm. No stored tolerance may be reduced, increased or rewritten to satisfy a report.

## Evidence reviewed

Authoritative diagnostic is `scratch/generator-core/mouth-probe-copied-curves.py/.txt`. It explicitly copies each B-spline/Bezier curve before segmenting to its actual trim interval, so this inspection does not mutate source curve geometry. The earlier non-copying probe is historical corroboration only and is not the basis of this disposition.

Source construction is `thread_profile.untextured_cap(Params(thread_clearance=0.20))`, using the DES03 lower cutter/relief extent-p. The copied-curve run reports valid source topology,23 faces, volume13084.525411459956mm3 and1.825300459seconds. The initial run was2.475seconds; timing is not an acceptance criterion.

Across all12 reported boundary edges of the selected radius17.6 mouth cylinder:

| Quantity | Observed value | Unchanged measured gate |
|---|---:|---:|
| Maximum actual trimmed 3D endpoint to associated nearest boundary vertex | 0.00004381744947079222mm | <=0.0001mm |
| Maximum lifted p-curve endpoint to actual 3D endpoint | 0.0000438221703060061mm | <=0.0001mm |
| Minimum complete trimmed-curve Z lower bound | 0mm | >=-0.0001mm |
| Mouth-plane circular edges0/1/2 | constantZ0 | complete edge within0.0001mm ofZ0 |
| Largest native vertex tolerance | 0.00013442580515245624mm | explicit geometric verification triggered |

Endpoint/vertex pairing was assessed from the printed coordinates and edge endpoints. The maximum vertex discrepancy occurs on the two adjoining Z0 circular edges; the p-curve endpoint discrepancy peaks on edge11. The affected topological mouth vertex has Z1.311736326649346e-16mm, so its observed offset is in-plane rather than the old below-mouth extension. Circle/line lower bounds are analytic; copied trimmed spline pole minima supply the reported complete-curve lower bounds. The numerical inspection uses ordinary OCCT/double precision, not formal interval arithmetic.

The probe ends at its old metadata assertion. That exit is therefore not an overall passing test report. Its already-emitted measured values independently satisfy the three actual-geometry criteria above. There is no assertion that an unexecuted final success message or later STEP check passed. Finite endpoint checks prove the endpoint requirement only; they do not establish continuous full p-curve/3D agreement everywhere along an edge.

## Revised diagnostic rule

For every mouth vertex/edge, always record the native tolerance. If it exceeds1e-4, retain that value and explicitly verify:

1. Actual trimmed 3D endpoints against their associated vertices, with maximum Euclidean discrepancy<=1e-4; record coordinates and trim ranges so a wrong endpoint correspondence cannot be hidden.
2. Actual mouth-plane curves stay within1e-4 ofZ0 over their full trimmed ranges, and every other mouth-face boundary curve has Z>=-1e-4. Use analytic/control-hull bounds or a stated derivative-bounded method rather than vertices or tolerance-expanded bounds alone.
3. Lifted p-curve endpoints agree with the actual 3D endpoints within1e-4 on the relevant face. Check consistent parameter orientation/ranges and identify each incident face tested.

A missing bound remains pending. An actual error above the limit remains a failure and needs the smallest construction correction; a native tolerance below the limit is also not a substitute for these actual checks. The observed high metadata is retained as source-quality context, not erased. Do not heal through STEP and then call the healed artifact authoritative source.

The implementation may now replace its metadata-only assertion by this evidence-trigger rule and continue the DES03 planned checks. This authorizes no mathematical thread, clearance, lead, shoulder or mouth-plane change. It is unnecessary to introduce another Boolean construction based solely on the printed0.0001344 uncertainty field while the measured geometry remains below0.0001.

## Remaining gates and handoff

Repeat the same actual source criteria for C25/C30 and the supported p2.4/E7.2 case. Export/import the explicit diagnostics or final caps and require the unchanged<=0.001mm mouth-boundary correspondence with its stated continuous/sampling bound; inspect written endpoints/planes as well. Final source BOP, complete source/STEP profile and assembly-path evidence, skin integration and labels still require their own checks. No partial C20 result covers those cases automatically.

The exact task receipt is `inputs/mouth-evidence-contract.sha256` plus `.fingerprint.txt`; the machine-readable extraction of the frozen diagnostic is `inputs/mouth-evidence-summary.json`. Root verifies the frozen inputs and routes this narrow criterion revision to the implementer. Independent validation/formal review remains distinct. No new CAD/export/snapshot was generated for this disposition.
