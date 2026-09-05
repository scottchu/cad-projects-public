# REV-CAD-CV1-01 formal independent review

**Owner:** `REV-CAD-CV1-01`  
**Role:** distinct formal independent-review join  
**Status:** **PASS** for the exact default CAD/source and written STEP candidate.  
**Candidate:** `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`

## Acceptance decision

| Evidence layer | Decision | Scope |
| --- | --- | --- |
| CAD/source | **PASS** | The standalone parametric-core refactor preserves the frozen default P1 R7 source geometry, datums, placements, and boundary contract. |
| Written STEP | **PASS** | The exact four candidate STEP artifacts below preserve the P1 R7 serialized geometry and pass the joined imported-solid evidence. |
| Slicer/process | **HOLD** | No slicer profile, toolpath, support analysis, adhesion result, or process acceptance is joined here. |
| Physical acceptance | **PARTIAL / UNBOUND** | The user report selects the already printed first version as the design baseline. Its exact source/STEP/slicer identity and complete fit, closure, drain, strength, and wear observations are not bound to this candidate. |

This decision advances only the exact default refactor candidate at the first
two evidence layers. It does not approve STL/3MF release, slicing, printing,
or any nondefault parameter combination.

## Frozen join and artifact identity

- Frozen design manifest: 57 entries, SHA-256
  `1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83`.
- Frozen candidate manifest: 27 entries, SHA-256
  `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`.
- Frozen implementation evidence manifest: 42 entries, SHA-256
  `0214bd39e094aed9bf84a0cfedde97cb795a2a946ccb7cd25bb84c989f250acc`.
- Formal review join: 160 entries at
  `scratch/container-generator-v1-formal-review/review-join.sha256`, SHA-256
  `2d5715f20a7e211cd98e4d1af0b5ec91046157b980a514a1cd8fc7b6f3a0363c`.
  All 160 entries passed `shasum -a 256 -c`.

Joined receipt and focused-evidence hashes:

| Record | SHA-256 |
| --- | --- |
| `IMPLEMENTATION.md` | `b03bc43d71be6e550a9521ca70ceac802d203e054c93af072e95ac47e676014f` |
| `CRITIQUE.md` | `9cd82b58376d4346d386012cb289349ff09c10d43d4ab75ae083b78089627091` |
| `VALIDATION.md` | `c53da3e1bac680ccefae837189c72d1de006ee167091c6f0c2b6be04d1a636ce` |
| `VALIDATION_RECOVERY.md` | `df63bc40ec651b54756aaf50ab0f793996cddadfa5c62303c84b8b9b3fd1d053` |
| Recovery result JSON | `74fd816da9aa312c0aa86bc2a91b7ceff3ed36350440d7b04b451812d79d9b79` |
| Formal serialization audit JSON | `3dfb6c7fed125f28bd04d2968fe45827511f21b120f84366b377c4dcb6610d7a` |

Exact candidate STEP hashes:

| Artifact | SHA-256 |
| --- | --- |
| `cad/container_generator_v1/body.step` | `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a` |
| `cad/container_generator_v1/cap.step` | `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0` |
| `cad/container_generator_v1/closed.step` | `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2` |
| `cad/container_generator_v1/print_layout.step` | `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b` |

The design, candidate, and implementation-evidence manifests passed at review
entry. A current substantive namespace inventory also matches all 27 candidate
entries: 23 top-level package files plus the four assigned tests. All frozen
source, test, and STEP contents therefore remain unchanged after candidate
freeze.

## Role and provenance audit

The repository records distinct stable owners for every acceptance role:
`DES-CAD-FV1-01` designed and froze the contract; `IMP-CAD-CV1-01` wrote the
candidate; `CRIT-CAD-CV1-01` performed the read-only CAD/visual critique;
`VAL-CAD-CV1-01` performed the first independent validation;
`VAL-CAD-CV1-02` performed the separately assigned bounded recovery; and
`REV-CAD-CV1-01` performs this read-only formal join. The implementer does not
approve its work, the critic and both validators identify the same candidate
fingerprint, and this review changed no candidate source, test, or artifact.

`VAL-CAD-CV1-01` exhausted its own method-repair ceiling and correctly returned
BLOCK rather than promote incomplete evidence. The fresh `VAL-CAD-CV1-02`
receipt used one focused report-serialization repair after its geometry work
had completed; that repair stringified report keys only and did not change the
candidate or its acceptance thresholds. Treating the recovery as a new,
distinct validation owner preserves the role and retry boundaries.

## Disposition of the VAL-CAD-CV1-01 block

The original BLOCK was procedural evidence incompleteness, with no observed
candidate defect. The two validation receipts now form one complete chain:

| Missing gate named by VAL-01 | Recovery evidence | Disposition |
| --- | --- | --- |
| Old/new source-native cap | One valid solid each; 6,396 faces, 12,348 edges, 5,956 vertices; identical surface census and rounded vertex set; zero volume, bounds, and centroid delta | **Closed** |
| New source-native body/cap to actual written STEP | Body volume delta `+0.000009263720130547881 mm3`; cap delta `-0.000007612099580001086 mm3`; maximum bounds delta `6.885159109515371e-12 mm` for each | **Closed** under the frozen `0.001 mm3` / `1e-6 mm` gates |
| Cap datums and complete occurrence placement chain | Old/new cap point datums match; native closed count/length pass; written closed frames are identity; print frames are body `(23,0,135)` and cap `(-23,0,84), Rx180` | **Closed** |
| Openings-up and no-new-roof relationship | All written-layout axial void samples are outside material; both mouth samples immediately below the print-pose tops are open | **Closed** |

VAL-01 had stopped on an added source-native-versus-STEP surface-type census
equality assertion. That assertion is not in the frozen design contract. STEP
serialization may map source BEZIER faces to BSPLINE while preserving the
solid. The applicable source-to-written gates are face count, volume, and
bounds; baseline-to-candidate written STEP carries the topology and geometry
equivalence gate. VAL-02 applied those frozen requirements without relaxing a
tolerance.

The `screw_axis` record is also preserved: old and new part source use the same
`Axis.Z`, linear range `(-0.1, neck_height + 2)`, and angular range
`(-10,2500)` construction, while the assembly still connects the body
`screw_axis` to the cap `shoulder` using the pitch-derived axial position. The
closed and print-layout occurrence frames independently match the contract.

## STEP serialization and global self-intersection limitation

The four new STEP byte hashes differ from P1 R7, but the direct streaming audit
found exactly ten changed lines:

- body: timestamp and `cadgen:sourceHash`;
- cap: timestamp, renamed `cadgen:sourcePath`, and `cadgen:sourceHash`;
- closed: timestamp, renamed `cadgen:sourcePath`, and `cadgen:sourceHash`;
- print layout: timestamp and `cadgen:sourceHash`.

Every other serialized line is identical to the already reviewed P1 R7 STEP.
This is the exact narrow metadata variance allowed by `DESIGN.md`; it proves
that the candidate written geometry, topology, and occurrence records did not
change.

The dense whole-body global self-intersection operation did not complete in
the bounded implementation run and was not rerun by either validator or this
reviewer. This review therefore does **not** claim an independently completed
global self-intersection scan. For this exact preservation refactor, the gap
does not block CAD/source or written STEP because the joined evidence shows:

1. native old/new body and cap equivalence, including validity, positive
   one-solid topology, face/edge/vertex counts, surface census, rounded vertex
   coordinates, mass properties, bounds, and centroids;
2. imported candidate body/cap/closed/layout BREP validity, closed shells,
   positive volumes, and required `1/1/2/2` leaf-solid counts;
3. line-identical nonmetadata STEP geometry against the formally reviewed P1
   R7 baseline; and
4. an actual-solid Boolean over the only possible body/cap overlap zone with
   `0 mm3` intersection and `0.20342035704394792 mm` minimum distance.

These facts show that the refactor introduced no new global or inter-part
geometry condition. The unfinished dense scan remains a named tool-performance
limitation and cannot be generalized to changed geometry, a nondefault
parameter set, fabrication-process acceptance, or engineering certification.

## Requirement coverage

| Requirement | Formal disposition | Joined evidence |
| --- | --- | --- |
| `CV1-ORIGINAL` | **PASS** | All 57 frozen inputs and 20 P1 R7 oracle entries verify; the new runtime is standalone and uses no downloaded/mesh geometry; native and written default geometry preserve P1 R7. |
| `CV1-PARAMETERS` | **PASS** | One 26-row registry covers 12 adjustable geometry fields, one reference/readout-only field, and 13 locked constants with defaults, units, domains, targets, and oracles. `device_diameter` changes only readouts. |
| `CV1-DERIVE` | **PASS** | One pure definition returns the immutable complete default record; builders consume the resolved record; four entrypoints call the boundary; invalid and locked-input checks stop before BREP work. |
| `CV1-SOLIDS` | **PASS** | Joined native body/cap and imported written-solid evidence covers valid positive closed solids, topology, walls, floors, drains, chamfers, skin, thread region, and focused collision. The global-scan limitation above remains explicit. |
| `CV1-JOINTS` | **PASS** | Required rigid datum names/values and `screw_axis` construction are preserved; body remains fixed; pitch/angle placement and closed/layout frames match the frozen contract. |
| `CV1-OUTPUTS` | **PASS** | The manifest contains exactly four matching `.step.py`/`.step` pairs and no candidate-root STL, 3MF, or GLB output. |
| `CV1-EQUIVALENCE` | **PASS** | Old/new native body and cap, source-to-written parity, exact baseline/candidate STEP geometry serialization, counts, measurements, and closed/layout occurrences all meet the frozen tolerances. |
| `CV1-FDM` | **PASS for CAD intent only** | Positive shoulder, zero thread-zone collision, retained slope bounds, bounded drains/floors, open axial cavities, and openings-up separated print poses pass. Slicer and physical proof remain outside this status. |
| `CV1-BOUNDARY` | **PASS** | No candidate mesh export, alternate family, simulator/live route, OpenSCAD, slicer, or printer state is present or claimed. |

## Visual review and findings

The formal reviewer spot-checked the frozen actual-STEP contact sheet,
longitudinal section, and thread/shoulder close-up. They show the two-piece
39 mm textured form, continuous seam field, open cavities, retained thread and
positive shoulder, seven drains at each floor, circular end chamfers, and two
separated openings-up print poses. No visual refactor drift or omitted required
feature was found.

No critical, major, or minor candidate finding remains. One noncandidate
housekeeping fact is retained: the package currently has ignored/reproducible
`__cadgen__` and `__pycache__` files created after freeze, including eight
viewer-cache GLBs. They are excluded from the 27-entry candidate and from this
acceptance decision; the root must keep them out of delivery and commits.

## Checks performed by REV-CAD-CV1-01

The reviewer did not regenerate CAD or rerun the heavy solid suites. The exact
review work was:

- `shasum -a 256 -c` on the 57-entry design, 27-entry candidate, and 42-entry
  implementation-evidence manifests;
- direct `diff -u` on all four P1 R7/candidate STEP pairs;
- `PYTHONDONTWRITEBYTECODE=1 uv run python projects/laifen-wave-case/scratch/container-generator-v1-formal-review/serialization_audit.py`, exit 0;
- source/test scope, datum/axis, output, validation-log, and candidate namespace
  inspection with `/opt/homebrew/bin/rg`, `find`, `diff`, `jq`, and `shasum`;
- visual inspection of the exact hashed contact sheet, longitudinal section,
  and thread/shoulder close-up; and
- `shasum -a 256 -c projects/laifen-wave-case/scratch/container-generator-v1-formal-review/review-join.sha256`, PASS 160/160.

## Next action

The root orchestrator may promote candidate
`6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`
as the default P1 R7 parametric CAD/source and written-STEP authority after it
reverifies this formal receipt and updates `PROJECT_STATE.md`, `NEXT_AGENT.md`,
`docs/iterations/CURRENT`, and this iteration's `HANDOFF.md`. Keep slicer/process
at HOLD and physical acceptance PARTIAL / UNBOUND. Any STL/3MF, slicing,
printer, or physical-acceptance step requires its own authorized evidence path.
