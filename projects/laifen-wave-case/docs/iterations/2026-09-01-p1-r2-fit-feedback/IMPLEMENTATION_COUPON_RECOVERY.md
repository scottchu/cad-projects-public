# CIM-02 prescribed thread repair receipt

Owner `/root/coupon_fix`, implementation only, 2026-09-01. Baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`; project `projects/laifen-wave-case`, iteration `2026-09-01-p1-r2-fit-feedback`. Verified all 39 recovery inputs, manifest SHA-256 `ef86c629a4fee512d53ada3133ebbff09f2140fa8e628545f08a04393e8f802c` before editing.

**Stopped and frozen by user steering:** the two narrow grip rows are superseded. Retain this thread-repair evidence for the new R3 design owner; do not fabricate this old skin. No mesh was produced. No independent approval, physical acceptance or printer operation occurred.

Frozen candidate: 59-entry `inputs/coupon-fixed-candidate.sha256`, fingerprint `3da2cac2b8d29b379b3be6309e3b7eb623fc50f6766dd5a573438a49517f6e4d`. It binds all 39 recovery inputs plus live ten Python files, nine STEP siblings and test source. Evidence and mutable orchestration records are excluded.

## Changes and source evidence

Changed `cad/p1_r2_coupons/coupon.py` only in the prescribed construction: named clipping overbuild delta0.10 with unchanged 0.6 lead slopes, and six explicit planar grip faces retaining the exact eight vertices. Functional radius equations, clearances, datums, cap bodies and lattice remain unchanged. Regenerated all nine existing STEP siblings. Strengthened `tests/test_coupons.py` with valley probes, diagnostic phase coordinates, true tip minimum width, face normals, positive shell overlap, and joint-driven pose/phase assertions. Fixed eager classifier construction without reducing samples or tolerance.

`uv run python -m pytest projects/laifen-wave-case/tests/test_coupons.py -v -s` passed all five tests in143.50s (`scratch/coupon-fix/pytest.txt`). Maximum source section error0.0000549316406264mm at male theta270/z4, below the unchanged0.01mm limit. All30 prescribed screw-pose intersections were zero. After switching pose checks to generated joint assemblies, `uv run python -m pytest projects/laifen-wave-case/tests/test_coupons.py -v -s -k screw_path` passed in39.93s (`screw-joints.txt`): all30 intersections zero, source joint Z/rotation verified, straight extraction g9/10/11 zero for each cap, negative-stop intersections4.38427643/4.27298661/4.16138021mm3 for c20/25/30.

`uv run python projects/laifen-wave-case/scratch/coupon-fix/topology.py` passed its diagnostic run. Trimmed neck has16 faces, volume1850.6439001339238mm3, and an explicit `BRepCheck_NotClosed` shell finding; it is not an accepted standalone solid. Final base union/clean has21 faces, volume4533.280016583524mm3, valid topology and valid `BRepAlgoAPI_Check`. Both intermediate and final solids classify r17.2 at theta0/z3 and7 OUT, z4 and8 IN. Final grip has six planar faces, positive volume1.9129174322991191mm3, valid topology and valid BOP check. `topology.txt` records the intermediate free-edge diagnostic; no tolerance or geometry was changed to suppress it.

## STEP evidence and unresolved parity finding

All commands ran from repository root through its uv-managed Python3.12. Installed CAD skill path prefix is `/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/`.

Generation command was `uv run python <skill-prefix>gen` followed by these explicit project-relative targets, then `--write --force --mesh-tolerance 0.01 --json`: `cad/p1_r2_coupons/male.step.py`, `cap_c20.step.py`, `cap_c25.step.py`, `cap_c30.step.py`, `closed_c20.step.py`, `closed_c25.step.py`, `closed_c30.step.py`, `exploded_c25.step.py`, `print_layout.step.py` (every target prefixed `projects/laifen-wave-case/cad/p1_r2_coupons/`). All nine built successfully; `scratch/coupon-fix/generation.txt` contains results.

`uv run python <skill-prefix>inspect refs projects/laifen-wave-case/cad/p1_r2_coupons/print_layout.step --facts --planes --positioning` completed. Corresponding `inspect validate` passed: four occurrences, zero failures/errors (`inspect-refs.json`, `inspect-validate.json`).

`uv run python projects/laifen-wave-case/scratch/coupon-fix/parity.py` stopped at cap_c20: source volume8545.500971435305 versus imported STEP8545.893335119052mm3, delta0.39236368374622543mm3. The diagnostic's0.001mm3 gate was not relaxed. Male had one solid, identical bounds, volume delta0.000282883806904mm3. Remaining seven output comparisons and STEP section/path checks did not run after the failed assertion.

`uv run python projects/laifen-wave-case/scratch/coupon-fix/parity_diagnose.py` completed (`parity-diagnose.txt`). Cap source and written STEP are both topology/BOP valid, both360 faces, with identical type counts:336 planar,8 BSpline,9 cylindrical,7 conical. Both directional Boolean differences contain zero solids and zero volume. Adaptive integration at1e-9 still gives8545.505395321354 versus8545.897785005805mm3; tightening integration did not resolve the discrepancy. **Unresolved:** the contradiction between empty geometric differences and nonzero integrated volume difference requires focused independent disposition. This receipt does not claim source/export parity or permit meshes.

## Visual and acceptance boundary

The two mandatory snapshot commands targeted written `print_layout.step` (camera iso) and `closed_c25.step` (section mode/front), output under `scratch/coupon-fix/`, width1400/height1000. Both exited immediately because the root environment lacks Python `playwright`; the skill reported its dependency explicitly. No snapshots exist and no visual approval is claimed. No dependency was installed or alternate interpreter used. User steering then stopped further old-appearance renders. Root owns viewer runtime/readiness; no service was changed.

CAD source evidence passes the focused implementation checks, but CAD acceptance awaits independent gates and the intermediate/parity findings. Written STEP validity passed the primary layout; complete source/export parity remains unresolved. Mesh/slicer/physical acceptance are absent. Grip comfort, fit, five-cycle wear, strength and full-case dimensions remain physical or future-design gates. Next: preserve this fingerprint, route the cap parity contradiction to the independent validator, and let the R3 design owner specify the newly requested hand-grippable surface before further CAD/export work.
