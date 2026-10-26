# Rail customizer recovery

Request revision 2, 2026-10-26. Owner: root. Baseline: `bfdab11`.

Recreate the missing `inner-outer-rails-3d.html` as a durable offline HTML
simulator. The user explicitly selected dragging **both OPEN and END positions**.
Recover the P20 R4 saved profile and inverse-frame rail math; do not claim
byte-for-byte recovery of the missing interface. This is simulator recovery,
not a mechanism redesign, CAD generation or fabrication release.

## Frozen contract

- RC-1: Three named rods, editable OPEN and END YZ centers, pointer/touch drag
  and numeric keyboard-accessible controls; mm, +Y right, +Z up, stack along X.
- RC-2: Linear world paths from the saved P20 R4 profile, 361 samples;
  outer paths `R(-theta*u) P(u)`, left +45°, right -45° by default. Inner
  plate and axle remain fixed. Render full rail cuts fixed in each local
  plate frame; motion changes only rod markers in local views.
- RC-3: Restore exact archived defaults, show motion at OPEN/MID/END and
  animate; allow travel angle, plate radius and slot diameter experiments.
- RC-4: Save/load versioned JSON without silent invalid values; export all
  three plate-local SVG rail drawings with mm units. No network required.
- RC-5: Show sampled path lengths, rim/web diagnostics and limitations.
  Preserve known unsafe defaults rather than implying manufacturing approval.
- RC-6: Keep source and tests in this project and deliver through a PR.

## Evidence plan

Compare the default against the preserved P20 R4 source/profile and coupon
witness. Test inverse/forward reconstruction across states and edited endpoints,
stationary Green, import rejection and SVG units. Exercise drag, scrub,
save/load/reset and responsive UI in a browser. Run required repository checks.

## Bound workflow and limits

CAD Workbench revision `1d7f4fcd65e04136bb6bad24e90015ca36d97f2f`, policy
manifest verified as `b95f77ef16d317366d1c93f7ff76dee92c0e69976ce55facec10512e23b6c3cf`.
No BREP or equipment/service operation. The substantial-CAD design/implementation
split is N/A for this prescribed simulator recovery; independent critique,
validation and formal acceptance remain separate from implementation.

## Plan and status

1. Root: recover source math and implement isolated offline simulator.
2. Distinct critic and validator: inspect one frozen candidate, read-only.
3. Distinct formal reviewer: join their findings; root resolves bounded defects.
4. Root: durable records, checks, commit/push and PR. Merge not authorized.

Maximum two focused repair rounds. No new runtime/dependency or server is needed.
Working state: implementation in progress; review and repository checks pending.
Temporary-file checkpoint: no prior `.decompozr/flow` records in the clean primary
checkout; task worktree newly created. No existing task artifacts removed.
