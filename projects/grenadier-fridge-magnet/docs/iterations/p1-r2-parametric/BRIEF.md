# P1 R2 — editable flat and relief source experiment

## Frozen contract
Accepted 2D baseline: face candidate f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652; git a8834040afe401637d36e94bd8fdd9e1d9874d35. Baseline files remain immutable. This iteration supersedes the historical face-only prohibition on new 3D source and the S2 proposed size question, without rewriting old contracts.

Latest user correction: scale can be done later; a real BMW print required enlargement and enlarged logo/text even with a 0.2 mm nozzle. Do not make a chosen width a prerequisite. Proceed with independently editable XY scale and Z heights, retaining both variants. Geometry is a development study, not printable acceptance or product-dimension approval.

GM-R2-01: identical approved top-view artwork and silhouette for flat and relief; black continuous backing. GM-R2-02: flat top coplanar. GM-R2-03: relief low glass/grille, middle body, high lamps/bumper, plate lettering flush with plate white. GM-R2-04: no holes, no motion, no physical-scale decision. GM-R2-05: four real filament intents black/gray/white/deep-blue; fifth visible glass-mix class is a blue+white process placeholder. GM-R2-06: width and Z parameters independent; feature-adjustment schema initially identity only. GM-R2-07: no detail deletion, smoothing, recoloring, or original lettering modification. Later enlargement/thickening requires an explicit delta and new review.

Frame: source pixel-grid u right/v down maps to XY with X right/Y up as viewed from front, origin at source-canvas center; back plane Z=0, front +Z. No movable parts, states or assembly motion. Installed back faces fridge; front faces viewer. Development model back-down display is not a confirmed print profile. No user spatial ambiguity remains in this simple static mapping; numeric values below are declared developer visualization choices only.

Use sequence: regenerate both source-driven variants → inspect relative heights and retained face → later choose candidate scales via real resolved toolpaths → locally adjust failing text/logos if needed → verify physical print. No slicing, network, printer, magnet retention or release work in this task.

## Execution DAG and mutable status
P2-D design → P2-I implementation → (P2-C independent critique || P2-V independent validation) → P2-R independent review join → user surface preview.

| Task | Owner/role | Dependencies/input | Exclusive writes | Done gate | Ceiling/status |
|---|---|---|---|---|---|
| P2-D | /root/parametric_magnet_design design | accepted face; input-manifest.json | this iteration contract; state indexes | implementation-ready frozen contract | balanced/medium; 4 min; 1 repair; done |
| P2-I | root assigns implementation identity | P2-D fingerprint | project new source/tests/exports; excludes accepted files | both variants + manifest + focused evidence | balanced/medium; 15 min checkpoint; initial +2 repairs |
| P2-C | distinct root-assigned critic | exact P2-I candidate | read-only artifact; REVIEW evidence | independent visual requirement findings | strong/high; 5 min |
| P2-V | distinct root-assigned validator | exact P2-I candidate | read-only source/artifacts; VALIDATION evidence | independent structural/parity checks | balanced/medium; 5 min |
| P2-R | distinct formal reviewer | C+V receipts same candidate | REVIEW join only | risks and acceptance reconciled | balanced/medium; 3 min |

Task scopes: allowed reads project and applicable policy/dependencies; forbidden unrelated projects, accepted SVG/PNG/source mutation, root dependency changes without root coordination, slicing/printer/network/PR. Inputs frozen SHA-256 manifest excludes only mutable orchestration/evidence/status. One writer per namespace, max3 active workers, receipts <=700 words with fingerprint, commands, changes, findings, risks and next step. Stop on baseline mismatch, mask gaps/overlaps, impossible closed mesh, stale inputs; checkpoint computational cost before full export. Do not solve cost by silent art simplification.

