# P13 R2 center-hole fit repair handoff

## Status and baseline

The digital repair iteration is complete and independently accepted for a
repaired PETG test print. Physical acceptance remains failed/pending because
the repaired cam plates have not been printed.

- Requested source baseline: `b0b79253373c7cf80943e99df8ab799958c50d49`.
- Integrated repository-policy baselines: `a5e21e6760d383f900ee30e4457edfb13267e09d`
  and `1484955cc1cfa64164dbdd1ca1222be658933c8e`; neither overlapped the XT60
  candidate.
- Final candidate fingerprint:
  `9f123ad24f46d60fcb89ae305455ba1a0c3b38d4738f82766ec91d02c1350db9`.
- Authoritative source SHA-256:
  `7927bc9bb0d0516faa5410200fc870df408fe16b282c2a226828e712ec801067`.

## Exact diagnosis and repair

The user's printed "middle stick" maps to the separate shallow-D actuator
shaft (`OD5.60 / AF5.15 mm`). The failed "center hole" is the one repeated
shaft interface formed by D bores in the printed `left_cam` and
`right_actuator`. Source, production-object census, motion labels, and the
certified service sequence all agree on this mapping. The purchased rod lanes,
fixed C journals, keeper, and caps are different interfaces and were not
enlarged.

The source-only geometry change is:

- `cam_d_bore_od`: `5.70 -> 5.75 mm`;
- `cam_d_bore_across_flat`: `5.25 -> 5.30 mm`.

Both D-profile controls now provide `0.15 mm` diametral allowance. The shaft,
three purchased `OD4.00 x 50.00 mm` rods, four-plate architecture, motion and
service states, all unrelated fits, and every source-defined print rotation
remain unchanged. Design alternatives, walls, lash, rejected larger bores, and
the exact feature trace are in `DESIGN.md`.

## Agent receipt / ledger

| Task | Owner identity / role | Receipt and disposition |
|---|---|---|
| `P13R2-D01` | `/root/design_diagnosis`, design | Exact mate and `5.75 / 5.30 mm` hole-only contract frozen in `DESIGN.md`. |
| `P13R2-I01` | `/root/implementation`, implementation | Focused failing witness, source edit, all affected STEP/3MF/provenance/snapshots generated; no self-approval. |
| `P13R2-I02` | `/root/implementation_closeout`, implementation closeout | Release manifest reconciled; 36 artifact/provenance entries checked with zero mismatch. |
| `P13R2-C01` | `/root/independent_critic`, critic | Final fingerprint verified; no blocking geometry/scope defect; physical fit and narrow lash/wall margins remain physical risks. |
| `P13R2-V01` | `/root/independent_validator`, validation/test | Found one label-format test blocker; after repair verified final fingerprint, `60 passed`, STEP/parity/mesh/DfAM/slicer/snapshot/Viewer evidence. |
| `P13R2-I03` | `/root/implementation_repair`, implementation repair | Fixed only the exact fixed-three-decimal label assertion; geometry/artifacts byte-identical. |
| `P13R2-R01` | `/root/formal_reviewer`, formal independent review | Joined critic/validator on final fingerprint; accepted CAD/source and artifact/slicer for repaired print; physical pending. |

Canonical commands, results, hashes, findings/severity, requirement coverage,
and acceptance boundaries are recorded in `VALIDATION.md` and `REVIEW.md`.
No raw agent transcript is required to resume.

## Generated release and evidence

- Release manifest: `releases/p13-petg-test/release-manifest.json`, SHA-256
  `406325612e34c5c6fce95d96a2fe074591fdf502f592f172c47d016df5a54356`.
- Production 3MF: `cad/p13_four_plate_three_rod/p13_print_kit.3mf`, SHA-256
  `588f11e47c89a64221e527085e560453d4e7e75a7b6ecc00cf448f7d22bf75a7`.
- Primary STEP: `cad/p13_four_plate_three_rod/p13_print_kit.step`, SHA-256
  `5237fe9bc908781ae5793c9ab004f4fc51d24720244b26846bb1dacba63256b7`.
- All 24 P13 STEP outputs, both P13 3MFs, both provenance files, source-domain
  evidence/certificates, parameter records, release checksums, and two review
  snapshots were regenerated or reconciled from source.
- Review snapshots:
  `docs/review/p13-r2-center-hole-fit-repair/p13-print-kit_20260822T192147Z.png`
  and `p13-motion-locked_20260822T192157Z.png`.

## Validation summary

- Focused concrete-defect regression: failed on the baseline because circular
  diametral allowance was `0.10 mm < 0.15 mm`; passes on the repair.
- Final relevant P13 suite: `60 passed`; repository-structure suite after the
  first policy integration: `8 passed`. The final root policy suite is rerun
  during delivery closeout.
- Written STEP validation: print kit `14` solids, each repaired cam `1`, motion
  `16`, service disassembly `6`; zero validation failures. Actual-solid,
  collision, math, constraint, requirements, motion/service, and parity checks
  pass.
- Exact production 3MF: `12` watertight bodies, `56,946` triangles, source
  orientation selected as best. Generic DfAM flags unchanged `0.8 mm` cap and
  `1.0 mm` keeper p05 walls against its conservative `1.2 mm` default.
- OrcaSlicer 2.4.2: Snapmaker U1, `0.4 mm` nozzle, resolved PETG, supports off,
  source orientation preserved, scratch G-code SHA-256
  `f008ae67936c16e69463cb07b822c87d68c2a02a91d1659483f78d8e8852176c`.
- The `p13_geometry_case.py` six-decimal volume comparison was independently
  audited: worst measured source/STEP delta was below `6e-10 mm^3`, so it does
  not mask the approximately `2.004 mm^3` intended removal per cam.

## Tailscale CAD Viewer

The Viewer listens on `0.0.0.0:3245`. Independent validation and formal review
both confirmed HTTP `200` for the page and the concrete assembly descriptor
(`10` unique components, `14` occurrences):

<http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py>

The exact startup and artifact-resolution commands are in `VALIDATION.md`.

## Acceptance and next smallest action

- CAD/source: accepted for the P13 R2 repaired-print candidate.
- Written artifact/slicer: accepted for a repaired Snapmaker U1 PETG test
  print, with unchanged cap/keeper manufacturing risks documented.
- Physical: failed/pending; do not claim acceptance from these digital results.

Reprint the repaired `left_cam` and `right_actuator` plates and reuse the
unchanged printed D shaft. First test passage through both bores by hand with no
forcing, binding, visible damage, or unacceptable play. If that passes, use the
certified assembly/service order and run the complete dry `0..27 deg` motion,
retention, cycling, wire, heat, removal, cooled-angle, and springback checks.
Append the observations to `docs/EXPERIENCE.md`; open a new iteration for any
further source change.

## Delivery route

The user explicitly requested this completed iteration be committed and pushed
directly to `main` if safe, which is the per-change override to the repository's
default pull-request route. Delivery must still be a fast-forward from the
latest fetched `origin/main`; do not force-push.

## Delivery closeout checks

After fast-forward integration of repository-policy commit `1484955`, the root
coordinator reran the newly prescribed repository and supported-P13 checks:

```bash
uv run pytest tests/test_repository_structure.py
uv run --project projects/xt60-bend-jig pytest \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_gate0_hash_p21_pivot_and_independent_stroke_derivations \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_one_connected_complete_workpiece_has_required_extrema_and_90_degree_path \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_three_rods_are_tangent_at_contact_then_apply_locked_wire_preload \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_exact_occurrence_census_and_upward_journal_topology \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_right_cap_physical_fit_contract_is_rigid_clear_and_floor_blocked \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_continuous_full_domain_motion_and_removal_certificates \
  projects/xt60-bend-jig/tests/test_p13_motion.py::test_motion_entry_has_exact_sixteen_stable_open_occurrences_and_envelope \
  projects/xt60-bend-jig/tests/test_p13_motion.py::test_javascript_solver_matches_python_kinematics_on_dense_grid \
  projects/xt60-bend-jig/tests/test_p13_motion.py::test_motion_contact_preload_directions_and_loop_are_exact \
  projects/xt60-bend-jig/tests/test_p13_rod_fit_coupon_3p8.py::test_written_step_and_model_only_3mf_roundtrip_are_valid
```

Results: repository structure `11 passed`; supported P13 gate `10 passed`.
The 36 release artifact/provenance hashes had zero mismatches, the exact
53-entry candidate fingerprint recomputed to `9f123ad2...50db9`,
`git diff --check` passed, and no nested `.venv`, `uv.lock`,
`package-lock.json`, or `node_modules` was found under the project.

Final Tailscale verification commands:

```bash
PROJECT_DIR="$PWD/projects/xt60-bend-jig"
TAILSCALE_CAD_URL='http://100.70.144.56:3245/Users/scottchu/.codex/worktrees/79caa408-e84c-4bfe-adfd-fa9ba1a1e186/design-projects/projects/xt60-bend-jig?file=cad%2Fp13_four_plate_three_rod%2Fp13_print_kit.step.py'
curl -sS -o /dev/null -w '%{http_code}\n' "$TAILSCALE_CAD_URL"
curl -sS --get --data-urlencode "dir=$PROJECT_DIR" \
  --data-urlencode "file=cad/p13_four_plate_three_rod/p13_print_kit.step.py" \
  'http://100.70.144.56:3245/__cad/artifact'
curl -sS --get --data-urlencode "dir=$PROJECT_DIR" \
  --data-urlencode "file=$PROJECT_DIR/cad/p13_four_plate_three_rod/__cadgen__/models/p13_print_kit.step.py/assembly.json" \
  'http://100.70.144.56:3245/__cad/asset'
```

Results: page HTTP `200`, artifact state `ready`, descriptor HTTP `200`, schema
version `2`, `10` components, and `14` occurrences.
