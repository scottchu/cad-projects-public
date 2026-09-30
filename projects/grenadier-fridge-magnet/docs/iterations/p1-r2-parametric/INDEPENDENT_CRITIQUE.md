# P2-C independent connected-model visual critique

2026-09-06; owner `/root/parametric_magnet_critic`; independent of design, implementation and validation. **PASS geometry and relative-height development preview; FAIL exact face-color fidelity pending color-encoding investigation.** This is not user intent acceptance or print approval.

## Provenance

Verified every path/content hash in `connected-candidate-manifest.json` and independently recomputed its sorted path-NUL-hash-LF fingerprint: `2541d21cfbb28d29eede289a3ae978c9d516a91b1e5f07e045f8d6c8286993ce`; zero mismatches. Shell command: `uv run python -` with `json`, `pathlib`, `hashlib` entry verification and fingerprint reconstruction. `urllib.request.urlopen` read the actual HTTPS delivery assets and SHA-256 matched:

- `/grenadier-model/models/flat.glb`: 5,915,688 bytes; `3d7f7e8f9e2bcc4ffbb2355abd9f1aba848cb3a18cff64059d2cd6011309008b`.
- `/grenadier-model/models/relief.glb`: 6,273,860 bytes; `86d99b9b6ca36f31969e71db48a61dbb1c4f84024e32a46a1a2a521202eb2a75`.

Read BRIEF, DESIGN, BACKING_REPAIR, requirements, experience, decision index and continuity. Directly viewed `references/d4-approved.png`. No relevant memory evidence used.

## Observations and coverage

CUA Chrome inspection at `https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-model`: flat front and oblique; relief front, default oblique, enlarged oblique, opposite oblique and back. These were actual rendered GLBs, not replacement illustrations.

- GM-R2-01/07: whole vehicle composition, wheels, roof, mirrors, four circular lamps, GRENADIER and DJZY 608 remain recognizable and visually aligned with D4. Both front views agree. Tiny contour roughness is visible close up; no broad new outline bulge or face redesign observed.
- GM-R2-02/03: flat appears coplanar; relief close oblique shows inset grille and glass, middle body and raised circular lamps/bumper/plate. Plate blue glyphs appear flush with its white field, without separately raised letter sidewalls. Exact mask boundaries and coplanarity require the separate deterministic gate.
- GM-R2-01/04: back view shows a continuous black vehicle-shaped field without visible holes. Edge bridges do not disrupt whole-face recognition. Individual 176 added backing pixels cannot be visually counted or strength-qualified at this view.
- GM-R2-05/06: classes remain distinguishable; no final scale decision required by preview. Parameter independence and real glass mixing are outside this visual check.

## Findings and limits

Minor presentation: page calls connectors “隱藏連接區”; repair contract states they can be visible through former contour gaps. Requested preview owner disclose tiny black edge additions instead.

Blocking color fidelity: plate blue appears cyan and whites gray in current rendering. The plate hue differs materially from approved royal/deep-blue intent. Root reports a possible sRGB-byte versus linear glTF vertex-color encoding mismatch; this cause was not independently established in this visual role. Do not attribute the discrepancy solely to lighting or treat this candidate as color-faithful. Correct encoding requires a fresh artifact fingerprint and focused independent color rereview. No geometry or source-art palette change is requested.

Agent-side delivery inspection does not prove the user's device experience. No STEP/BREP, slicer, welded STL or physical acceptance is supplied here. Thin bridges and small lettering remain later process risks. Next: resolve color encoding and review the new artifact, then join independent validation/formal review before asking the user to compare surfaces.
