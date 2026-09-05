# VAL-CAD-CV1-01 independent CAD/STEP validation

**Owner:** `VAL-CAD-CV1-01`  
**Status:** **BLOCK — independent source-native equivalence chain incomplete**  
**Verified design fingerprint:** `1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83`  
**Verified candidate fingerprint:** `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`  
**Verified implementation-evidence fingerprint:** `0214bd39e094aed9bf84a0cfedde97cb795a2a946ccb7cd25bb84c989f250acc`

## Verdict

The candidate has **no identified geometry defect** in the completed checks.
The independent verdict is nevertheless **BLOCK** because the validator's final
bounded harness stopped after old/new native body equivalence and before it
independently completed the native cap and complete source-native-to-written
STEP chain. The two allowed focused harness repairs were already consumed. This
role therefore cannot promote the candidate from implementation evidence alone.

The block is an evidence-completeness block, not evidence that the cap or STEP
geometry is wrong. A fresh validator may inspect this unchanged candidate; no
candidate repair is indicated by this receipt.

## Frozen provenance

All hashes were checked before geometry work and rechecked after the stopped
harness and actual-written STEP inspection:

| Manifest | Entries | Result |
| --- | ---: | --- |
| `inputs/frozen-inputs.sha256` | 57 | PASS; manifest SHA-256 matches the frozen design fingerprint |
| `candidate-files.sha256` | 27 | PASS; every source, test, and STEP entry matches; manifest SHA-256 matches the assigned candidate |
| `evidence-files.sha256` | 42 | PASS; every implementation evidence entry matches |

The root environment was Python `3.12.13` at
`.venv/bin/python3`, build123d `0.11.1`. `cad/p1_r7_end_chamfer/`
remained byte-identical to the 20 frozen P1 R7 entries. Validation wrote only
this receipt and `scratch/container-generator-v1-validation/**`.

## Completed independent candidate evidence

### Parameter and derivation contract — PASS

`PARAMETER_SPECS` has exactly 26 unique rows covering every `Parameters` field:
12 adjustable geometry values, `device_diameter` as the sole reference/readout
value, and 13 locked constants. Defaults, classifications, domains, geometry
targets, and one-definition/four-entrypoint `derive` structure passed. A change
to each adjustable field either changed a downstream derived field or had a
direct fabrication-source consumer. Changing `device_diameter` changed only
itself and the two gap readouts; fabrication modules do not consume it.

The independently evaluated default record reproduced:

- cavity `213`, cap height `84`, body depth `132`, thread tool zone `9`, and
  closed outer length `219` mm;
- full-thread datums `Z=2..8`, hence `6` mm effective engagement;
- crest/valley radii `19.5/19.05`, body/cap bores `30/31` mm, thread
  root/crest `16.4/16.9`, female minimum wall `1.85`, and overall minimum wall
  `1.4` mm;
- lattice count `33`, end radius `18.3`, `1.2` mm 45-degree chamfer, seven
  drain centers, body print translation `(23,0,135)`, and cap print transform
  `(-23,0,84), Rx180`.

The candidate's cheap suite independently reran as:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider \
  projects/laifen-wave-case/tests/test_container_generator_v1_parameters.py \
  projects/laifen-wave-case/tests/test_container_generator_v1_requirements.py -q
```

Result: **PASS, 28 tests**.

### Serialization-only STEP variance — PASS

The validator streamed every baseline/candidate STEP pair line by line before
loading geometry. Every serialized geometry/topology/placement record is
identical. The ten changed records are limited to the expressly permitted
metadata:

| STEP | Changed lines | Permitted records only |
| --- | ---: | --- |
| body | 2 | `FILE_NAME` timestamp and `cadgen:sourceHash` |
| cap | 3 | timestamp, renamed source path, source hash |
| closed | 3 | timestamp, renamed source path, source hash |
| print layout | 2 | timestamp and source hash |

The independently observed candidate STEP hashes match `candidate-files.sha256`:

- body `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a`
- cap `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0`
- closed `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`
- print layout `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`

This is strong evidence that the written candidate cannot contain a geometric
change from the already reviewed P1 R7 STEP baseline.

### Old/new source-native body — PASS

The final harness independently built both the old P1 R7 body and the new
resolved-record body from source. Both builders reported the same one-solid
body with 10,255 faces and build123d volume `65470.38584513924 mm3`.
The independent comparison passed valid topology, one solid/one closed shell,
zero free edges, face/edge/vertex counts, surface-type census, full paired
vertex coordinates, bounds, centroid, and adaptive volume at `eps=1e-10`
under the frozen `1e-6 mm` and `0.001 mm3` tolerances. Old/new body joint
names and source-local datum/axis records also matched.

This completed before the later source-to-STEP harness assertion stopped the
run. The corresponding native cap build/comparison did not run in the final
attempt and is the primary reason for **BLOCK**.

### Actual written STEP loading and validity — PASS within stated limitation

The CAD CLI can resolve a same-stem `.step` back to `.step.py`; therefore the
validator created hard links with names that have no sibling generator:

```sh
mkdir -p projects/laifen-wave-case/scratch/container-generator-v1-validation/inspection
for name in body cap closed print_layout; do
  ln -f projects/laifen-wave-case/cad/container_generator_v1/${name}.step \
    projects/laifen-wave-case/scratch/container-generator-v1-validation/inspection/${name}-written.step
done
```

Inode and SHA-256 checks confirmed that each alias is the exact candidate STEP.
The actual imported files were then checked with:

```sh
CAD_INSPECT=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/inspect
for name in body cap closed print_layout; do
  PYTHONDONTWRITEBYTECODE=1 uv run python "$CAD_INSPECT" validate \
    "projects/laifen-wave-case/scratch/container-generator-v1-validation/inspection/${name}-written.step" \
    --skip-self-intersection
done
```

Result: **PASS**, `1/1/2/2` leaf occurrences, zero failures. This establishes
valid topology, closed shells, positive per-solid volume, and the required
solid counts on the written artifacts. The full global Boolean
self-intersection check was deliberately not rerun; see Limitations.

`inspect refs --facts --planes --positioning` against the same four hard links
also passed:

| Artifact | Leaf solids | Faces | Bounds mm |
| --- | ---: | ---: | --- |
| body | 1 | 10,255 | `[-19.5,-19.498274,-135]..[19.5,19.498274,9]` |
| cap | 1 | 6,396 | `[-19.5,-19.498274,0]..[19.5,19.498274,84]` |
| closed | 2 | 16,651 | `[-19.5,-19.498274,-135]..[19.5,19.498274,84]` |
| print layout | 2 | 16,651 | `[-42.5,-19.498274,0]..[42.5,19.498274,144]` |

The direct explicit STEP imports independently found body cylindrical faces at
radii `1.5, 15.0, 16.4` and cap cylindrical faces at radii
`1.5, 15.5, 16.65, 17.15`, covering the seven diameter-3 drains and the
30/31 mm bores. Each imported part has exactly one end-local conical face. Its
actual OCP cone is `44.999999999974314` degrees with reference radius `18.29`
at the cutter-overbuild origin; advancing `0.01` mm to the real closed end
recovers radius `18.30` mm. The body end spans approximately
`Z[-135,-133.8]`; the cap end face reaches `Z=84`.

The imported print layout independently measured bed minima near
`-1.0e-7 mm`, tops `144.0000001/84.0000001`, centers `+23/-23`, and overall
size `85.0000002 x 38.99654808241401 x 144.00000020000078 mm`. These agree
with the frozen placement and openings-up orientation contract.

### Actual-solid thread-zone collision — PASS

A direct `build123d.import_step` of `closed.step` produced two solids. Each was
intersected with a radius-17.5 cylinder restricted to `Z=0.001..8.999`, the
only possible body/cap overlap zone. The cropped body/cap regions had 15/16
faces and positive volumes `1431.0666064273557/535.6052850213305 mm3`.
Their actual Boolean intersection volume was `0 mm3`; OCP minimum distance was
`0.20342035704394792 mm`. This passes the zero-collision and at-least-0.20 mm
interlock-clearance risk gate without operating on the dense external skin.

The same direct import probed the seam at radii `17.4`, `18`, and `19` mm:
body material exists immediately below `Z=0` only, and cap material exists
immediately above `Z=0` only. Together with zero thread-zone intersection and
the identical baseline STEP payload, this supports the positive external
shoulder stop. It does not make a physical torque or retention claim.

## Validator harness failures

These are validator-method failures, separated from candidate findings:

1. `independent-attempt1.log`: stopped before geometry because the harness
   hardcoded `derive` at source line 90; the sole definition is at line 91.
   Repair: assert one definition in `derive.py`, independent of formatting.
2. `independent-attempt2.log`: old/new native body construction and comparison
   completed, then the harness compared native Z bounds with exact tuple
   equality. The design allows `1e-6 mm`. Repair: compare Z min/max with that
   tolerance. Python slice `[2:6:3]` correctly selects tuple indices 2 and 5.
3. `independent-final.log`: old/new native body equivalence passed. The harness
   then stopped on an added requirement that source-native and imported STEP
   expose exactly the same surface-type census. The frozen design does not
   require that representation-level equality: it requires source-to-STEP
   volume/bounds parity and baseline-to-candidate STEP topology/equivalence.
   Since this was the final allowed repair attempt, the assertion was not
   removed and native cap plus the remaining source-to-STEP checks were not
   rerun.

An ad hoc explicit-written-file preflight was also interrupted when a dense
radial `is_inside` bisection proved needlessly slow. It was not an acceptance
gate and produced no candidate finding; direct OCP cone inspection supplied the
bounded actual-chamfer evidence instead.

## Requirement coverage

| Requirement | Independent status | Evidence / gap |
| --- | --- | --- |
| `CV1-ORIGINAL` | PASS | 57 frozen inputs and all 20 immutable P1 R7 entries verified; new package scan/tests reject old runtime imports and mesh geometry. |
| `CV1-PARAMETERS` | PASS | Complete 26-row classification/default/domain/dataflow checks; reference diameter remains nonfabrication. |
| `CV1-DERIVE` | PASS | One pure definition, immutable complete default record, four entrypoint calls, invalid/locked input suite. |
| `CV1-SOLIDS` | BLOCK | Written body/cap validity and features pass; source-native body passes; source-native cap was not independently completed. |
| `CV1-JOINTS` | BLOCK | Default record and old/new native body joints pass; cap native joint comparison and full source occurrence chain remain incomplete. |
| `CV1-OUTPUTS` | PASS | Exactly four frozen `.step.py`/`.step` pairs; actual STEP hashes and hard-link imports verified. |
| `CV1-EQUIVALENCE` | BLOCK | Serialization-exact baseline/new STEP and old/new native body pass; native cap and full source-to-written parity did not complete independently. |
| `CV1-FDM` | PARTIAL | Written end cone/drains/closed stop/thread zone and vertical layout facts pass; independent top-axis void probes did not complete in the final harness. Slicer/process remains HOLD regardless. |
| `CV1-BOUNDARY` | PASS | Cheap scope suite confirms no mesh family, simulator/live, slicer, or printer output in the candidate. |

## Global self-intersection limitation

The implementer's dense whole-body `BRepAlgoAPI_Check` did not complete after
about 6.5 minutes. This validator did not repeat that unbounded operation, as
directed. The omission alone would not block this exact refactor candidate:
native/imported BRep validity passes, shells are closed and positive, the
written geometry payload is line-identical to the formally reviewed P1 R7
baseline, old/new native body equivalence passes, and the only body/cap overlap
zone has a completed actual-solid Boolean and positive clearance.

The present **BLOCK** instead comes from the incomplete independent native-cap
and source-to-written chain after the harness retry ceiling was exhausted.

## Next action

Assign a fresh independent validator to the unchanged candidate fingerprint.
It should run only the missing bounded gates: old/new source-native cap
equivalence, source-native body/cap to actual-written STEP adaptive
volume/bounds/vertex parity, cap joints, and the two openings-up axis probes.
It should not require source-native/STEP surface-type census equality and must
use no-sibling hard-link names for CAD CLI inspection. Do not rerun the global
dense self-intersection checker. No candidate-source repair is supported by
this receipt.
