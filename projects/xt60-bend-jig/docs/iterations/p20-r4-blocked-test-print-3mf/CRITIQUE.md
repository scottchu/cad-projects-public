# P20 R4 blocked test-print 3MF independent critique

Date: `2026-08-27`

Task: `P20R4-3MF-CRITIQUE-01`

Owner/role: `/root/p20_3mf_critic`, independent artifact and handoff critic.
This role did not edit source, STEP, 3MF, tests, provenance, or continuity
records and does not approve manufacturing, slicing, upload, or printing.

## Candidate identity

- Implementation candidate manifest:
  `docs/iterations/p20-r4-blocked-test-print-3mf/IMPLEMENTATION_CANDIDATE.sha256`
- Verified manifest fingerprint:
  `e11c3f94b1d4081a4e58db0ec74c76651f234ce97f2e8faa06f59600dc2be871`.
- Child `sha256sum -c` result: all `14/14` pinned files passed.
- Restored parent manifest fingerprint:
  `e90f0f63687118ce9826801335263ea861d546016011c8bb98f31032963f61db`;
  all `30/30` parent rows passed.
- Reviewed 3MF SHA-256:
  `cd90dc1afa0c0658981b75a040daa2a8cc91d9addf362ae3bd09420ea4b05135`.
- Reviewed STEP SHA-256:
  `fb1188097e74752522e90dac96996b98c3d1379d42432d09607e62eea47b39e3`.

## Focused repair review

The repair restored the authoritative parent source byte-for-byte to SHA-256
`38ed907ea1ec0e22ff8c42c2c03e047049b65ea9962b2fe7e58ea914aecac93e`.
No print-kit constants or builders remain in that file. All print-kit-only
composition now lives in
`src/xt60_bend_jig/p20_r4_blocked_test_print_3mf.py` at SHA-256
`b850d90c26b7326a885c028978f029d414814050cf9fc1b08d25c6c9c85f04cf`,
which imports the frozen parent builders and refuses to run if the parent
source hash changes. The STEP generator, exporter, and focused tests all use
this isolated child module.

Independent comparison against the metrics inspected in the pre-repair
critic run found no geometry or layout delta. All 13 labels, per-object BREP
and mesh volumes, bounds, vertex counts and triangle counts are identical;
the totals remain `23,384` vertices and `46,788` triangles, the footprint
remains `228.5 x 145.8 mm`, all objects remain on `Z=0`, and XY overlap count
remains `0`. Both repaired snapshots show the same separated 13-object layout.

## Findings

### Medium - the artifact can be misread as print-ready if detached from its handoff

The filename `p20_r4_print_kit.3mf` and the white 3MF snapshot do not visibly
say `blocked`. Arbitrary 3MF metadata may also be hidden by a slicer. The
archive and provenance correctly identify the artifact as
`blocked-test-model-only-13-printable-objects`, and the embedded flags say
`manufacturingAccepted=false` and `printingInitiated=false`, but those guards
are not sufficient if someone receives only the file.

Disposition: handoff is allowed only with the exact blocked-test warning from
the BRIEF adjacent to the 3MF link. Do not describe it as `print-ready`, and do
not begin slicing, upload, or printer action from this candidate. A future
standalone release should use a visibly blocked filename or equivalent
user-visible warning, but that is outside this critique's write scope.

### No artifact mismatch found - exact printable census and exclusions

Source composition, STEP, 3MF object labels, build items, focused tests, and
provenance agree on exactly `13` distinct printable objects in the frozen
order:

- four plates;
- one fixed stepped axle;
- two permanent outer keepers;
- six unchanged `H9.05 mm` caps.

The three purchased OD4 x 50 mm rods, XT60 reference, 90-degree wire/workpiece,
motion/reference geometry, tools, and coupon geometry are excluded. Each 3MF
object remains its own mesh and identity-transform build item. The archive has
only `3D/3dmodel.model`, `[Content_Types].xml`, and `_rels/.rels`; no slicer,
G-code, support, material, or printer-control payload was found.

### No layout ambiguity found in the supplied review surfaces

Independent visual inspection counted all `13` objects in both pinned TOP
snapshots:

- STEP: four individually separated plates, one axle, two keepers, and six
  caps are clearly visible; source colors make the groups easy to distinguish.
- 3MF: the same thirteen silhouettes are visible and spatially separated. The
  all-white render reduces semantic clarity but does not hide, merge, or
  overlap an object.

The recorded footprint is `228.5 x 145.8 mm`, every object contacts `Z=0`, and
the recorded pairwise XY bounding-box overlap count is `0`. This demonstrates
the deterministic model layout only; it does not establish fit on a particular
printer bed or validate slicer spacing.

### Known parent failures remain visible in provenance but not in this print layout

The print-kit layout cannot visually demonstrate the assembled Blue-rod/XT60
collisions, `1.152 mm` inner-rim web, `1.715 mm` left Blue-Orange rail web,
rod/workpiece contacts, or physical acceptance of the caps and plate gap.
These are correctly retained in provenance and the required handoff warning;
none is waived by the separated-part snapshots or valid meshes.

## Evidence checked

- Read frozen `BRIEF.md`, `TASK_DAG.md`, implementation receipt, candidate
  manifest, isolated print-kit composition, frozen parent source, exporter,
  focused tests, and provenance.
- Recomputed the child and parent manifest fingerprints and verified every
  pinned SHA-256 row: child `14/14`; parent `30/30`.
- Ran:
  `uv run pytest -q projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py projects/xt60-bend-jig/tests/test_p20_r4_print_kit_3mf.py`
  -> `9 passed`.
- Inspected the repaired pinned STEP and 3MF TOP snapshots at original
  resolution and counted the same thirteen separate objects in each.
- Inspected the 3MF ZIP entry list and found only the three standard model
  package entries described above.

## Critic disposition

**PASS FOR USER PREVIEW/HANDOFF ONLY AS AN EXPLICITLY BLOCKED, MODEL-ONLY TEST
ARTIFACT. FAIL FOR PRINT-READY, MANUFACTURING-ACCEPTED, SLICED, UPLOADED, OR
PRINTED STATUS.**

Required adjacent handoff wording:

> P20 R4 model-only 3MF prepared as a blocked test artifact. It contains 13
> printable plastic objects and no rods, XT60, or wire. Mesh/STEP validation
> does not waive the XT60 collision or thin-web failures. It has not been
> sliced, uploaded, or printed.

Next action: an independent validator must recompute the same candidate
fingerprint and artifact facts. Formal review may then decide only whether this
exact file can be shown to the user under the warning above.
