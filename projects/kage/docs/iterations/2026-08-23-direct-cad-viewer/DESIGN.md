# Direct CAD Viewer design record

## Selected design

Use the installed `cad-viewer` skill as the sole runtime authority. Call it with an explicit supported artifact, use an absolute workspace path, and construct the review selection from the artifact path relative to that workspace. The repository owns only durable workflow and evidence rules; it owns no launcher, listener lifecycle, plugin-cache discovery, or version pin.

The preview evidence has three deliberately separate levels:

1. **Review page reachable:** the exact review page returns HTTP `200`.
2. **Requested artifact ready:** the exact artifact endpoint returns HTTP `200` and JSON `state == "ready"`.
3. **Visible error-state check:** an inspection of the loaded page or snapshot supports the general claim “the requested artifact rendered with no visible error state.” Any feature-specific visual claim names the inspected features and views.

Levels 1 and 2 are both mandatory before returning a ready preview. Level 3 is mandatory before making the general no-visible-error observation or any named feature-specific visual observation. None of these levels accepts CAD geometry, slicer/fabrication behavior, or physical performance.

For the locked Kage reference, the workspace is the absolute form of `projects/kage/references`, and the selected imported file is `locked-direct-gear/p3_v3_direct_gear_race_assembled.step`. The STEP hash remains a preservation invariant, but the repository does not wrap the Viewer to enforce it.

## Rejected alternatives

- Keep or shorten `bin/preview-cad`: rejected because any repository launcher still duplicates the installed workflow boundary and creates maintenance coupling.
- Keep a runtime checksum manifest: rejected because the installed skill is intentionally the live runtime authority and may change with plugin upgrades.
- Treat startup, a printed URL, or page HTTP `200` as success: rejected because those signals do not prove that the requested artifact built; the observed render-artifact error demonstrates the gap.
- Treat artifact `ready` as evidence of no visible error state: rejected because endpoint state does not establish what the user actually sees.

## Residual risks

- Installed Viewer behavior can change after plugin upgrades; read the installed skill before each use.
- A conflicting or unhealthy listener can block startup. Follow the installed workflow's alternate-port or failure guidance and report the blocker; do not restore repository process automation.
- Visual inspection remains human/agent evidence rather than a deterministic geometry proof.
