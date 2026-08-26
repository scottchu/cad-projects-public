# P17-I13 D13 review materialization receipt

Status: exact frozen D13 candidate materialized for CAD review. This is **not**
an implementation acceptance, service pass, force proof, lock proof, print
release, or physical acceptance.

## Frozen input

- Baseline commit: `8adfb20f352e36cede54a3414307ced3de81c2b8`.
- `IMPLEMENTATION_INPUT_MANIFEST.sha256` file SHA-256:
  `0b96b9dd4821f4f848fee0d44eb79ce004ee35250a8d8aa802c7277463d5247c`.
- Manifest payload verification: `14/14 OK` before source edits.
- DESIGN SHA-256:
  `0133dc4d45f38e91a20311d490b9b2fef2c8c0c6a07081c6b0c75fb19d620f95`.

## Implemented exactly

- Frozen I10 guide table remains explicit; the final D13 `GUIDES` are derived
  from one common `D=(+16.1869657526,+10.2949747468)` translation.
- Workpiece stays the finite modeled I10 workpiece: body `(-6.5,22.5)`, bend
  `(-0.5,3.5)`, vertical wire `Y=-6.5`, horizontal wire `Z=-2.5`, finite
  horizontal segment length `12.0`, separate extract datum `Y=17.265`.
- `C=(3,12)`, `A=(-29,12)`, linear `theta=24u`, left/right outer angles
  `-theta/+theta`, three OD4x50 rods, six permanent caps and existing four
  plate envelopes remain unchanged in architecture.
- `transform_point_between_frames` implements
  `p_target=T_target^-1*T_source*p_source`; `derive_mating_rail` applies it to
  a parameterized source path. All six rod outer rails delegate to this one
  pure-math authority. Three inner tracks remain direct straight capsules.

## Deterministic evidence

- Focused pytest:
  `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -x`
  -> `22 passed`.
- CAD 0.4.27 `scripts/gen --write --force` on the ten explicit generators ->
  `10 built`; a final `scripts/gen --json` check -> `10 current` against the
  final source closure.
- CAD 0.4.27 `scripts/inspect validate --skip-self-intersection` -> `10/10`
  STEP files passed, `failureCount=0`.
- CAD 0.4.27 `scripts/inspect refs --facts --positioning --plane-limit 2` ->
  `10/10` passed, `errors=[]`.
- Four transparent axis-camera PNGs were rendered and visually inspected.
  The snapshot CLI burned `ISO` labels despite explicit `+X/-X` directions;
  filenames and artifact provenance record the intended directions, and no
  contrary visual-label claim is made.
- Motion GIF: `72` decoded RGB frames, all `71/71` adjacent frame differences
  nonempty; first/mid and first/last differences are nonempty.

## Known failures retained

- OPEN bottom rod signed XT60 body clearance: `-2.000 mm`; actual intersection
  `199.8052927683109 mm3`.
- OPEN bottom rod/finite vertical-wire centerline separation:
  `1.7016843784 mm`; radial overlap `2.4483156216 mm`; actual intersection
  `53.787371493712925 mm3`.
- END former contact is lost. Infinite-straight diagnostic surface gaps are
  bottom `8.1369657526 mm` and upright `2.2449747468 mm`; the exact finite
  modeled-wire gaps are bottom `8.1369657526 mm`, diagonal
  `16.71834015015733 mm`, upright `7.877883157765334 mm`.
- D13 rail/path asymmetry remains. It is a geometric diagnostic, not a
  physical hand-force result.

## Frozen candidate

- Independent gate manifest:
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-d13-independent-gate-manifest.sha256`.
- Entry verification: `21/21 OK`.
- Candidate fingerprint / manifest-file SHA-256:
  `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`.
- Provenance and review packet are under
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/`.

Independent critic, validator, formal reviewer, and physical testing remain
separate downstream gates. No mesh, 3MF, slicer or Viewer runtime was changed.
