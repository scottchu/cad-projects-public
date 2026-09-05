# DES-R4-01 numeric and provenance receipt

Status: design contract complete; source/CAD implementation, written STEP, slicing and physical R4 gates pending. Owner `/root/uniform_skin_design`. No CAD/source/test/artifact mutation in R3 or candidate CAD namespaces. Initial arithmetic draft mistakenly added an extra1mm to J/A; before freeze it was corrected against live frozen Params/derive to collar_end10.2 and cap_straight_start12.4. No generated CAD used the mistaken draft.

All58 baseline paths passed SHA-256 verification against `inputs/baseline.sha256`; fingerprint `fef9b674d14d5fb0469425db28e65cf14f4c8b58b9018cdf9eca8c830dcf8e3f`. Supplied photo visually inspected; source preserved. Source was read at HEAD `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c` plus the explicitly frozen worktree files. Full design inputs include the frozen baseline entries and frozen contract snapshots; `inputs/design-contract.sha256` lists paths/content, `inputs/design-contract.fingerprint.txt` names the manifest SHA-256.

Commands actually run from repo root:

- `uv run python projects/laifen-wave-case/preview/p1-r4-profile-study.py`: generated SVG/PNG and printed numeric values below; internal mathematical assertions passed.
- `uv run python` read-only probe importing `p1_r3_generator.params.Params,derive`: confirmed neck9, full form2..8, collar_end10.2, cap_straight_start12.400000000000002, bands(-30.1,-6.1)/(14.4,38.4). No BREP built.
- `uv run python` using pathlib/hashlib: checked every baseline file and generated sorted path/content manifest for the contract. No baseline mismatches.
- `view_image` inspected supplied photo and generated PNG. Formula study shows the narrower R3 textured regions and widened collar versus a continuous R4 envelope; this is no CAD render or engineering acceptance.

| Derived item | Result |
|---|---:|
| Required crest OD at h0.45/budget0.30/wall1.8 |39.90mm|
| Selected crest OD / valley radius |40.00 /19.55mm|
| Female minimum wall at budget0.30 / c25 |1.85 /1.90mm|
| Body / cap straight bore minimum wall |4.55 /4.05mm|
| N / shared arc pitch |34 /3.6128315516mm|
| Developed plateau width |1.0391605637mm|
| Rational-map plateau lower bound |1.0376825178mm|
| Full-depth skin radial-z slope |0.29296875|
| Skin plus0.20rad/0.30axial textured relief |0.9596354167 (<1)|
| Conservative relief overhang from vertical |43.819988deg|
| Closed / standalone body / standalone cap length |78.5 /44.1 /43.4mm|

N31->34 deliberately preserves physical arc pitch near3.63 when radius increases; keeping31 would broaden the arc pitch to3.96246mm. Root accepted N34, OD40/h0.45 and textured0.20/0.30 relief as scoped design choices. No extra user confirmation is required for the already stated outside relationship. Root should present the diagram and proceed to implementation.

Coverage: R4-01/02/05/06 have explicit formulas and diagram; R4-03/04 have exact frozen functional geometry/datums and prescribed comparison gates; R4-07/08 have exact target counts/print transforms and future artifact checks; R4-09 remains physical. High unresolved implementation risks: sewing noncircular planar ends and preserving thread cavity while decoupling radius-derived fields. Medium: actual radial field/normal/ligament and export agreement must be independently checked. Historical R3 export HOLD remains separate, not a transferred R4 verdict.
