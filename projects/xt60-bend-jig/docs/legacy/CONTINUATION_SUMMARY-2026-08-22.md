# XT60 Bend Jig — Complete Continuation Summary

Date: 2026-08-22  
Source checkout: `/Users/scottchu/Projects/personal/3d-print/design/xt60-bend-jig`  
Restart worktree: `/Users/scottchu/Projects/personal/3d-print-xt60-restart`  
Restart branch: `restart/xt60-bend-jig-20260822`

This is a continuation summary, not a task handoff. The user reported that the
working data should be treated as damaged/untrusted and wants a fresh start in
another Git worktree. Preserve the original directory. Treat all recorded CAD,
test, slicer, and hash results below as traceable historical evidence only until
they are reproduced from source in the restart worktree.

## 1. Goal state

Create a parametric PETG jig that holds and forms only the two insulated XT60
pigtail wires while soldering and cooling. The XT60 plastic body must not be the
clamped load. The intended cooled wire path is a fixed 90-degree bend from the
ESC solder pads toward the XT60.

Current P13 architecture:

- four principal circular plates: two fixed guides and two synchronized cams;
- one rotary input;
- three purchased, uncut 304 stainless rods, each `OD4.00 x 50.00 mm`;
- three rods move equal scalar travel along different straight guide paths;
- rod roles are asymmetric: forming, supporting, and locking;
- `0 deg` is OPEN;
- approximately `22 deg` is nominal first geometric wire contact;
- `22..27 deg` is the final closing stage;
- `27 deg` is LOCKED;
- no base, frame holder, decorative handle, or adjustable bend angle in P13.

## 2. Critical acceptance boundary

CAD/export evidence and physical proof are separate.

CAD can establish named parameters, occurrence counts, nominal motion,
clearance/intersection facts, valid solids, source/export parity, and written
STEP/3MF provenance. It cannot prove printed fit, actuation force, PETG
stiffness, creep, heat resistance, insulation safety, cap retention, soldering
access, removal usability, or cooled springback.

No complete P13 PETG assembly has been physically accepted. The restart must not
label this design production-ready.

## 3. Physical observations already available

Rod-hole PETG coupon, 0.4 mm nozzle:

| Nominal hole | Observation |
| --- | --- |
| 4.05 mm | Very tight; coupon was used to push it back out |
| 4.10 mm | Tight; hand push/pull possible |
| 4.15 mm | Best sliding fit; slight friction |
| 4.20 mm | Similar but looser |
| 4.25 mm | Loose with wobble |

`4.15 mm` is the evidence-backed rod sliding-fit reference. It is not a blanket
replacement for every bore; each bore has a separate role.

The latest P16 cap-throat specimens were all judged usable, with the two left
specimens feeling nearly identical. This is only initial hand-fit evidence for
the exact upright-printed removable right-cap `4.10` functional core. It does
not prove the unslit permanent left `ID3.90` cap, cycling, wear, heat, or
retention.

## 4. Current P13 design decisions

Wire geometry:

- nominal insulated wire OD: `4.30 mm`;
- rod radius: `2.00 mm`;
- wire radius: `2.15 mm`;
- tangent centre offset: `4.15 mm`;
- `wire_preload = 0.25 mm`;
- `contact_stroke = 3.7642135623730946 mm`;
- `common_stroke = 4.014213562373095 mm`;
- locked centre offset: `3.90 mm`;
- source-accepted preload range: `0.00..0.40 mm`.

`wire_preload` is only a geometric compression proxy, not a force calculation.

Printability repair prompted by the user's Snapmaker preview:

- the old print layout placed large plate faces above the bed and produced
  missing-half/floating first layers;
- the old shared `0.10 + 0.10 mm` cam/fixed thrust-land arrangement was not
  faithfully printable with a `0.25 mm` first layer;
- repaired contract: fixed thrust land `0.20 mm`, cam thrust land `0.00 mm`,
  `main_face_gap = 0.30 mm`, nominal axial clearance remains `0.10 mm`;
- fixed-land shaft clearance is `ID5.70`; the principal fixed C-journal remains
  `ID4.80`;
- four plate print rotations are source-defined so every principal plate has a
  large authored face at `Z=0`, with hub/land upward;
- all six caps are source-oriented closed-end-down/socket-up;
- do not manually use slicer `Lay on face`, negative Z, or ad-hoc flipping to
  repair generated geometry.

## 5. Authoritative source and contract files

- `src/xt60_bend_jig/p13_four_plate_three_rod.py`
- `docs/p13-four-plate-three-rod-brief.md`
- `docs/p13-cad-source-domain-amendment.md`
- `docs/p13-parameter-table.md`
- `docs/p13-default-parameter-manifest.json`
- `docs/p13-dependency-graph.json`
- `docs/p13-continuous-certificates.json`
- `docs/physical-record-schema.json`
- `tests/test_p13_four_plate_three_rod.py`
- `tests/test_p13_motion.py`
- `tests/p13_geometry_case.py`
- `scripts/export_p13_3mf.py`
- `cad/p13_four_plate_three_rod/p13_print_kit.step.py`
- `cad/p13_four_plate_three_rod/p13_motion.step.py`
- `cad/p13_four_plate_three_rod/p13_locked.step.py`
- `cad/p13_four_plate_three_rod/p13-artifact-provenance.json`
- `cad/p13_four_plate_three_rod/p13-3mf-provenance.json`

Generated STEP/3MF files must be regenerated from Python source and must never
be hand-edited.

## 6. Historical generated artifacts and hashes

These hashes describe the last artifact set in the source checkout. Recompute
them in the restart worktree before trusting them.

- production 3MF:
  `cad/p13_four_plate_three_rod/p13_print_kit.3mf`
  - SHA-256 `d163cb311a78fbf8ffbc231593c492930696c5a03e4826b55cb68728c89fab35`
- print-kit STEP:
  `cad/p13_four_plate_three_rod/p13_print_kit.step`
  - SHA-256 `52272f7ec3e57be6cb72b8c906a697684434cdbe9dcda71e48b470c7e08ef3ec`
- motion STEP:
  `cad/p13_four_plate_three_rod/p13_motion.step`
  - SHA-256 `61d33734c5e286aab44014705147ba9829021485c39c19694746a6300ebc5f20`
- fit-coupon 3MF:
  `cad/p13_four_plate_three_rod/p13_fit_coupons.3mf`
  - SHA-256 `4e78b8dc5ecf2906ab53fc91e46f6666dd7932dfe8207be95872251bf7604db6`
- parent brief SHA-256:
  `9c2102114cbf87ccabaa4388ed3814b91cdf3f8f654c775f5ddd8a5d05272322`
- controlling amendment SHA-256:
  `b50e850ac5425fe7bad0e49555de10b0e30f63e04934bdbf66d4220f44e1f590`

The final historical provenance contract embedded both accepted-spec hashes in
all 24 written P13 STEP roots, both written 3MF metadata blocks, both v2 3MF
sidecar roles, and all 23 production artifact provenance rows.

## 7. Tests and validations historically run

Results actually reported for the repaired artifact set:

- focused repair suite: `8 passed in 88.28s`;
- provenance-focused suite: `3 passed in 63.38s`;
- all-24-written-STEP provenance test: `1 passed in 43.63s`;
- independent final provenance review: `3 passed in 44.89s`;
- independent final artifact checks: `2 passed in 44.01s`;
- source/STEP print-kit parity: `PASS`;
- STEP print-kit validation: `14 occurrences`, `0 failures`;
- production 3MF: 12 objects, lib3mf round-trip valid, all manifold and
  consistently oriented, zero XY bounding-box overlaps;
- principal plate written mesh bed areas: approximately
  `1089.976..1110.022 mm^2`, all `minZ=0`, no large down-facing face above bed;
- six cap bed areas: approximately `38.481 mm^2`, closed-end-down;
- independent OrcaSlicer 2.4.2 check used Snapmaker U1, 0.4 mm nozzle, PETG,
  `0.25 mm` first layer, `0.20 mm` later layers, supports disabled;
- that slicer run found all 12 objects extruding on layers 1 and 2, complete
  principal footprints, and no Support, Support interface, or external Bridge
  blocker;
- final DfAM result reported only `48.13 mm^2` sub-45-degree down-facing area
  (`0.4%`) and a coarse `0.1%` support-volume ratio.

Important exclusions:

- the full approximately 15-minute suite was not rerun after the final repair;
- the earlier `52 passed` result predates the print-layout repair and is stale;
- none of the checks above is physical P13 acceptance;
- the simulator was not proven complete or validated by the earlier evidence.

## 8. Environment and execution rules

- Python `>=3.12`.
- Use `uv` for every Python environment, test, and generation command.
- Project dependencies are declared in `pyproject.toml` and locked in
  `uv.lock`.
- Never use bare `python` for project work.
- Node/npm may not be on `PATH`. A known bundled runtime is:
  `/Applications/ChatGPT.app/Contents/Resources/cua_node/bin`.
- Current npm dependencies are pinned in `package-lock.json`.
- CAD plugin paths in old README examples may be stale; discover and use the
  installed CAD skill runtime rather than assuming version `0.4.15`.

## 9. Git/worktree state at restart

- Parent repository root:
  `/Users/scottchu/Projects/personal/3d-print`
- Parent branch: `main`
- Parent HEAD:
  `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`
- The complete `design/xt60-bend-jig` directory is untracked by the parent
  repository. A new worktree therefore cannot obtain it from Git history; it
  must be copied explicitly.
- Source project size before copy: approximately `1.5 GB`, `20,118` files.
- Major local-only contents include `.venv` (~1.1 GB), `cad` (~341 MB),
  `node_modules` (~41 MB), `.pytest_cache`, `__cadgen__`, logs, snapshots, and
  generated artifacts.
- The restart copy intentionally includes all of those files because the user
  asked to transfer the complete project. Do not commit caches or generated
  runtime debris without a separate, audited commit request.

## 10. Remaining work in the restart worktree

1. Verify the copied tree byte-for-byte before modifying it.
2. Treat the copied `.venv`, caches, generated artifacts, and prior hashes as
   untrusted convenience data; recreate the environment with `uv sync --frozen`
   when beginning validation.
3. Inspect the current source/brief/amendment and decide whether to preserve P13
   or truly restart the mechanism architecture. Do not infer permission for a
   new architecture from this copy operation.
4. If preserving P13, regenerate explicit STEP/3MF outputs from source, rerun
   the full test suite, run source/export parity, validate written artifacts,
   and repeat the Snapmaker U1 slicer check.
5. If restarting from first principles, retain only measured physical inputs
   and purchased-hardware constraints as evidence; do not reuse nominal CAD
   acceptance as proof.
6. Before soldering, dry-assemble and sweep `0..27 deg`; record binding, cap
   insertion/removal, actual wire OD, first contact, locked preload, insulation
   marking, XT60-body loading, and removal access.
7. Only after the dry test succeeds, test soldering/cooling and record PETG
   flex, cracking, creep, heat softening, final cooled bend angle, and
   springback.

## 11. Worktree copy result

- New worktree created at:
  `/Users/scottchu/Projects/personal/3d-print-xt60-restart`
- Branch:
  `restart/xt60-bend-jig-20260822`
- Worktree HEAD:
  `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`
- Complete project copied to:
  `/Users/scottchu/Projects/personal/3d-print-xt60-restart/design/xt60-bend-jig`
- Copied project payload: `1,579,226,304 bytes`, `20,119` regular files.
- A post-copy `rsync -a -c -n --delete --itemize-changes` checksum dry run
  reported `0` differences.
- The production 3MF hash matched between source and destination after copy.
- The original project remains intact at its source path.
- The copied project remains untracked in the restart branch. No files were
  staged or committed.

## 12. Immediate restart rule

Do not continue by trusting this summary alone. Start with filesystem and source
inspection in the restart worktree, reproduce the relevant checks, and keep all
CAD/export findings separate from the user's physical observations.
