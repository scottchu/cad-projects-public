# IMP-GEN-01a core implementation receipt

Owner `/root/generator_core`; phase A only; 2026-09-01. Read and verified all 68 entries of `inputs/skin-contract.sha256`, fingerprint `e63eecf9e47d97d37787e58f92e5b3f394e18abf33a33e2d10f126286501c027`. Frozen R2 source/artifacts and the R3 design contract are unchanged. Root owns continuity indexes and the later geometry task.

## Implemented

`cad/p1_r3_generator/params.py` provides frozen Params/Derived, semantic dimensions, failed-inequality rejection, preset data and a parameter fingerprint. Generic derivation is independent of Laifen. The short preset retains max OD39; the provisional Laifen preset explicitly rejects while its cap split/end contact remain undecided. Large phase values that cannot retain cell fractions are rejected rather than producing numerically meaningless texture.

`thread_profile.py` contains the one normalized original profile, male/female min/max scalar envelopes, lazy actual BREP helix construction, and the repaired redundant clipping envelope. At defaults the sweep path/profile/core dimensions reproduce the repaired R2 construction. Tests establish scalar equivalence only; no newly built R3 neck, default solid equivalence, changed-parameter solid sections, screw poses, or old STEP parity claim is made.

`skin.py` evaluates the exact periodic diamond or optional crosswave field, cosine envelope and radius. Five oriented developed polygons partition each complete diamond cell into a plateau and four flanks, with no independent floating grip cells. These are seeds for future crease-preserving meshing, not a completed mesh. Conservative triangle Taylor bounds allocate Cartesian interpolation error between angular, axial and mixed derivatives. Mandatory crease/fade splits are explicit. The reported grid count is a lower estimate before those splits.

`generator.py` is a working CLI that accepts every meaningful Params input and emits derived dimensions, parameter fingerprint, tessellation budgets and separate pending acceptance states as JSON. `--dry-run` is supported and the default. `--write-step` currently exits2 with the pending geometry gate; it never reports stale geometry or pretends Viewer controls regenerate CAD. No full body/cap builder is claimed in phase A.

## Reproduction and evidence

Run from the repository root, using its uv-managed Python:

```sh
uv run pytest projects/laifen-wave-case/tests/test_generator.py -q
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --preset short-grip --dry-run
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --cavity-length 82.1 --dry-run
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --cavity-length 82.1 --cap-height 47 --thread-pitch 2.4 --engagement 7.2 --dry-run
uv run python projects/laifen-wave-case/cad/p1_r3_generator/generator.py --body-bore 24 --cap-bore 25 --dry-run
```

Five focused tests PASS; raw result `scratch/generator-core/pytest.txt`. Four successful JSON outputs are in the same scratch directory. The first run had four passes and one test-witness mismatch: the intended oversteep pz3/h0.6 case first violated plateau width. One focused repair used h0.6 with smooth_crosswave to isolate slope rejection; the valid constraint was retained. Other witnesses cover C60, low wall, narrow plateau, nonfinite input, extreme arc pitch, OD, phase representability, preset gate and honest CLI failures. The default gives C72.5/H43.4, bands24/24, N31 and outer length78.5. Adding9.6 to C adds exactly two axial periods to the body band while preserving cap band and both pitches. Feasible p2.4/E7.2 and bore24/25 examples derive successfully; this is not geometric acceptance.

Default normalized male and three female profiles agree with the frozen R2 scalar functions to1e-12 over four angles and21 axial points, including the previously filled valleys. Analytic checks cover seam identity, nonnegative raised field, fade endpoints, cell area partition, sampled axial slope and the conservative tessellation error sum. Object collision, written artifacts and manufacturing checks require phase B actual solids.

## Risks and next action

**High implementation cost:** conservative full Cartesian error bounds require approximately1,103,972 body and1,104,048 cap grid triangles even before crease splitting at defaults. This stronger bound is not evidence that these face counts are minimal. Building millions of OCC triangle faces is inappropriate without a bounded patch/time probe. The next worker should use a small periodic patch and either prove a tighter radial/chord error bound or bound a periodic surface fit while preserving the exact field and crease topology. Never silently coarsen or replace the mathematical skin.

**Pending geometry:** no new skin BREP or STEP was generated, so no primary-artifact snapshot/viewer link applies to this core receipt. Thread geometry, final solid validity, wall after approximation, surface deviation, actual plateau width, print orientation and complete STEP export remain pending. Default R2 source evidence does not extend to changed pitch/bore parameters or resolve its separate old STEP-parity contradiction. Physical grip/fit/printing/wear remain unknown. Independent critique/validation/review must use the frozen core candidate; this implementation receipt is not acceptance.

Input verification and evidence hashes are in `inputs/core-candidate.sha256` and `inputs/core-candidate.json`. Two owned stalled default-rg sessions2686/33660 were terminated, each exit130; subsequent commands used login:false. No environment, config, runtime or printer changes occurred.
