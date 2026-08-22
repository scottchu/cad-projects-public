# KAGE P3 V3 Phase-3 I3.8 — source-3MF acceptance and print-release split

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation; print release remains RED**

Date: **2026-08-19**

Supersedes I3.7 where this document removes unreachable headless CLI commands,
embeds six object-to-filament mappings in the source project, defines canonical
JSON and semantic 3MF parity, and separates I3 CAD acceptance from print
release. All other I3.1-I3.7 contracts remain active.

Immutable predecessors:

```text
I3.1  abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77
I3.2  9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3
I3.3  4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691
I3.4  c6fb12ceab347b258b4f3be65b61d32f178bbf3075cf68869d5d87e9d47636e1
I3.5  08ab0d28e84036a3bcf17e74e9d3ab18d22c376f8a9f71f4cd1fd6494ede35d6
I3.6  326f9dbd21fa04885447c8080390a70187176f90020f0ebfee212255bc4154f9
I3.7  7dc3657a2cea56bf5061d7be06303f7b265df48b1c55098dfe9864d57248fe48
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

This amendment changes no CAD, source, test, mesh, profile, tooth, race,
joinery, or hardware geometry. It does not claim G-code, print, fit, motion,
thermal, strength, optical, or physical acceptance.

## 1. Frozen source-project object/tool map

The source-owned project is exactly:

`evidence/i3_8_source_3mf/i3_8_six_moving_halves_source.3mf`.

It has exactly six plates and six build objects, one object per plate in the
order below. UUIDs are UUIDv5 values derived with namespace URL
`6ba7b811-9dad-11d1-80b4-00c04fd430c8` and the listed name string:

| Plate | Object name | UUIDv5 name string | Frozen UUID | 3MF `extruder` | Filament slot | Physical tool |
|---:|---|---|---|---:|---:|---:|
| 1 | `hour_I3_half_A_130T_beta15p230769` | `urn:kage:p3-v3:i3.8:moving:hour:half-a` | `fa6a01e8-5e16-50e5-a679-572d6f97eebb` | 1 | 1 | T0 |
| 2 | `hour_I3_half_B_130T_beta195p230769` | `urn:kage:p3-v3:i3.8:moving:hour:half-b` | `8647d48e-3be7-5bcc-96ce-f99edd27d2f1` | 1 | 1 | T0 |
| 3 | `minute_I3_half_A_130T_beta15p230769` | `urn:kage:p3-v3:i3.8:moving:minute:half-a` | `cd27fc98-3338-5c4a-930a-a5f3641c1250` | 1 | 1 | T0 |
| 4 | `minute_I3_half_B_130T_beta195p230769` | `urn:kage:p3-v3:i3.8:moving:minute:half-b` | `cf2d9c10-7eb8-51f4-9acb-70e15bda166e` | 1 | 1 | T0 |
| 5 | `second_I3_half_A_130T_beta15p230769` | `urn:kage:p3-v3:i3.8:moving:second:half-a` | `e2b2957a-7f3c-57ac-a071-f4ad0ed15dd5` | 1 | 1 | T0 |
| 6 | `second_I3_half_B_130T_beta195p230769` | `urn:kage:p3-v3:i3.8:moving:second:half-b` | `1d950c12-033f-5037-8c6d-7b006ed0746a` | 1 | 1 | T0 |

Each object and its sole normal part must carry `extruder="1"` in Orca's
`Metadata/model_settings.config`; the corresponding JSON project metadata must
map the same UUID and object name to filament slot1. The project embeds no
object mapping to slots2-4. I3.8 explicitly removes
`--load-filament-ids '1,1,1,1,1,1'` from every workflow: the flag is omitted,
not passed empty, because its observed object-list behavior is not accepted.

Filament slot1 is the exact I3.6 PETG chain. Orca's one-based filament slot1
maps to physical zero-based tool0 and standalone G-code tool command `T0`.

## 2. Honest backend evidence and I3.7 rejection

I3.7's three mandatory headless commands are unreachable on the installed
backends and are deleted as CAD/3MF acceptance requirements. They may not be
reported as skipped-and-passing.

### 2.1 Snapmaker Orca 2.3.5

The tested executable is the I3.6 binary
`/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca`, SHA-256
`4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe`.
The bundle version is2.3.5 and its CLI banner is
`Snapmaker_Orca-01.10.01.50`.

Using a copied full active Snapmaker datadir and an explicit-extruder1 3MF,
both tested single-action paths failed:

```text
--export-settings only  exit 139 = 128 + SIGSEGV(11)
  stdout SHA-256 22091df019f9a4449ffebf11be8c3442e4e9d25181cac8ed0372959a25753955
  stderr SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

--slice 0 only         exit 139 = 128 + SIGSEGV(11)
  stdout SHA-256 29f47d168b9cc822e712cd6cea26cdf362fa1ac9824397f7fe891bdc923238ec
  stderr SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Both stdout logs stop after static-config initialization and Sentry startup;
neither command produced resolved settings, a resolved 3MF, or G-code. Empty
stderr is evidence, not success. Repeating or combining these commands does not
convert exit139 into acceptance.

### 2.2 Upstream OrcaSlicer and alternative discovery

The discovered upstream binary is
`/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer`, version2.4.2,
SHA-256 `f22fe59f43f167503f11802d49a984787c896bd8a0ebc0c0af6cc6912b33a801`.
Its `Info.plist` SHA-256 is
`f957a583d6ca0a5c0dd98e40ca960972be273db57b7b56e170285e28015a5396`.
A headless all-plate probe with the same explicit-extruder1 3MF emitted zero
stdout bytes and zero stderr bytes, did not produce G-code, did not exit within
the bounded 50-second probe, and was terminated with SIGTERM exit143. It is
classified as a hang, not a slicer result.

The installed `cad:gcode` discovery command reported OrcaSlicer available,
PrusaSlicer unavailable, CuraEngine unavailable, and Bambu Studio unavailable/
not preferred. Thus no verified working headless alternative exists in this
environment as of the audit. Backend availability may be re-audited later,
but no future result may rewrite this historical evidence.

## 3. Acceptance split

### 3.1 Phase I3 CAD, STEP, and source-3MF acceptance

Phase I3 may pass without G-code only after all inherited CAD/STEP gates and
the source-owned 3MF gates in this amendment pass. The accepted scope is:

- parametric source, BREP/STEP exports, occurrence and source/export parity;
- I3.6 bit-exact masks and all inherited actual-solid, joinery, clearance,
  motion-state, contact, manifest, and locked-copy gates;
- one source-owned six-plate 3MF with the exact object name/UUID/extruder map;
- exact source-owned project settings: I3.6 active machine/process/filament
  chains, four 0.4 mm nozzle positions, raw bed type3, PETG slot1, brim3.50,
  skirt loops0, prime tower disabled, one material/object per moving plate;
- canonical JSON and semantic 3MF parity from Sections 4 and5.

For this CAD phase, headless slicing status is
`DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE`, never PASS and never an empty
violation disguised as success. The two Snapmaker crashes, upstream hang, and
alternative-discovery result are required evidence fields. They do not make
valid CAD/STEP/source-3MF evidence RED.

### 3.2 Final print-release gate

Final print release remains **RED / PENDING** until a user-driven Snapmaker
Orca2.3.5 GUI export or a future independently verified working backend
produces six actual plain G-code files from the accepted source project and
exact active profiles. The final G-code basenames and SHA-256 values are
implementation/print-release outputs and cannot be predeclared or fabricated.

Print release additionally requires the inherited I3.5 full first-layer path,
printable-polygon, startup-line, brim, skirt, prime-tower and containment
checks plus Section6 validation. CAD-phase acceptance is not print release.
Neither is physical acceptance: adhesion, warp, flatness, fit, retention,
motion, heat, strength, optical behavior, and full running tests remain open.

## 4. RFC 8785 JSON Canonicalization Scheme

All canonical JSON artifacts use RFC8785 JCS exactly: UTF-8, I-JSON input,
ECMAScript-compatible number serialization, recursive lexicographic property
sorting by UTF-16 code units, minimal required string escaping, no whitespace,
no BOM, and no terminal LF. Duplicate keys, lone surrogates, NaN, and infinity
are RED.

The pinned reference implementation and conformance-vector source is
`https://github.com/cyberphone/json-canonicalization` commit
`19d51d7fe467d4706a3ff08adf8a748f29fc21e0`. Vendor and lock
`node-es6/canonicalize.js`, SHA-256
`f9f498b55c99eefe348c99018ddcfe08efa6f7ff96b9ba9dce4b7090b33c4438`.
Before accepting any project JSON, the implementation must reproduce the six
official input/output pairs `arrays`, `french`, `structures`, `unicode`,
`values`, and `weird` from that commit byte-for-byte. Record the vendored
implementation, all 12 vector files, their full SHA-256 values, Node runtime
identity, and zero vector mismatches in `i3_8_jcs_conformance_report.json`.

The 12 pinned vector SHA-256 values are:

```text
input/arrays.json      e503b6d71d1afa595b1c74b1016445c944cd89f90418066b23de1aeda7d17563
output/arrays.json     099601b171cafed97c333f8878d68e7f8c8f795412adb34b2fdcf0e7c7beac42
input/french.json      03676a951cd8753ac62589f72eb2105cc782c33425418cfe1d517c111f6e5d5a
output/french.json     d99d0ebdcb0033cb858cfa830ae46bc0fb3309413b271f1da828c89901a27ed5
input/structures.json  d66893805be1784116af50af3110d08766c70a6b4aad93374723f72346e7aaa6
output/structures.json 605f65004ec2db7692522a0852c22f1c989e036d547e88963d1a3143cf3195d5
input/unicode.json     4621864e014d4a805a563f55b9ea20aba4a2d2dc09c7394f625496998c00702c
output/unicode.json    0d99aad92a125196ff887876643fd3206786a84ddce2cee52ba4ad256d2381d3
input/values.json      c4a041b503d6bc236036ef44db4dac499272f60fc22c40dc3b7a54870ba6f1c3
output/values.json     2d5e01a318d0f0879ab568c4be289c8b1f64ef8921a53c6277d5e069978baacb
input/weird.json       a3a905266bd4a49a969274ea69baa14ee0c4af0ead926d6fa2b7612b4af75387
output/weird.json      6af595a9aa80110b964b4de3f82a05fa6ae7423005019bacfa2620dddc4e94d1
```

JCS replaces I3.7's ad-hoc sorted-key serialization. All source-project JSON,
profile-effective maps, object maps, semantic 3MF manifests, validation
manifests, and reports use the pinned JCS bytes for authoritative hashes.

## 5. Source-owned 3MF semantic parity

I3.8 explicitly chooses semantic parity rather than repeat-byte equality for
the ZIP container. A 3MF archive's member order, DOS timestamps, compression
method/level, extra fields, data-descriptor choice, and central-directory bytes
are nonsemantic and may vary. The complete archive SHA-256 is still recorded
for traceability, but different archive hashes do not fail parity by themselves.

Reject encrypted members, duplicate member names, absolute paths, `..` path
components, symlinks, CRC failures, undeclared content types, and unreferenced
payloads. Extract in a clean directory. The semantic manifest contains:

- the sorted complete member-name set and uncompressed byte size of each;
- RFC8785 JCS SHA-256 for every JSON member;
- Canonical XML1.1-with-comments-disabled SHA-256 for every XML or `.config`
  member, with namespace processing enabled and external entities/network
  access disabled;
- raw SHA-256 for every binary member;
- parsed 3MF model units, resources, meshes, triangle indices, components,
  build order/transforms, relationships, content types, six plates, and the
  exact Section1 object name/UUID/extruder/filament/tool map.

Pin the Canonical XML implementation executable, version, full SHA-256, and a
source-owned conformance-fixture map before use. Two independently extracted
archives pass semantic parity iff their JCS semantic-manifest bytes are equal.
No test may demand identical ZIP bytes, and no test may ignore a semantic
member difference merely because the model renders similarly.

The GUI project 3MF is source-owned evidence. Its embedded effective project
settings must name and hash every exact I3.6 active profile source and resolve:

```text
machine leaf   /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json
machine SHA    545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d
process leaf   /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/0.20 Standard @Snapmaker U1 (0.4 nozzle).json
process SHA    3342dbe3e995b66ab5700245c676f446a88d35f56498b074ab6fe14039d67763
filament leaf  /Users/scottchu/Library/Application Support/Snapmaker_Orca/user/default/filament/PETG.json
filament SHA   d7a7c0e5911779e70836bf53c29fd736c8702ff45ad46880690c2f092c5433df
brim/skirt/prime tower  3.50 / 0 / false
```

Every parent path and full hash remains exactly the complete I3.6 4-machine,
4-process, and 5-filament chain. The bundled application machine profile, stale
`_old` process, saved Generic TPU selection, OTA copies, and backup copies
remain excluded.

## 6. Future G-code validation and T0 semantics

When six actual G-code files exist, create a source-owned wrapper at
`evidence/i3_8_print_release/input/i3_8_gcode_wrapper.json`. It uses
`backend="orcaslicer"`, the exact active machine leaf as `native_config`, all
eight I3.6 machine and process leaf-and-parent paths as `native_settings`, all five
I3.6 PETG leaf-and-parent paths as `native_filaments`, machine name
`Snapmaker U1 (0.4 nozzle)`, bed size `[270,270]`, Z height270.05, explicit
motion bounds X`[0.5,270.5]`, Y`[1,271]`, Z`[0,270.05]`, filament typePETG,
first-layer nozzle temperature240 C, and bed temperature80 C. Canonicalize and
hash the wrapper with Section4 JCS.

For each G-code, run the installed validation wrapper exactly as:

```sh
/usr/bin/python3 '/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.19/skills/gcode/scripts/gcode_tool.py' validate \
  --gcode '/absolute/path/to/one_actual_plate.gcode' \
  --profile '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_8_print_release/input/i3_8_gcode_wrapper.json' \
  --json
```

The wrapper's `ok:true` proves only nonempty G-code, temperature/movement/
extrusion presence, and configured motion bounds. It does not prove firmware,
thermal, acceleration, extrusion physics, or print safety. Preserve all unknown
command warnings for review; do not suppress them by widening bounds or
editing G-code.

Separately parse each complete file. Strip `;` comments, ignore blanks, and
read the first command word case-insensitively. Standalone tool selection is a
line whose first command word is exactly `Tn`. Require its complete set to be
`{T0}`, regex `(?im)^[ \t]*T[123](?:[ \t;]|$)` count0, and every positive
deposition move to occur with active tool0. `T1/T2/T3` operands on commands
such as `M104` are temperature-address operands, not standalone tool changes;
report their counts separately. Also verify effective PETG identity, 240 C
first-layer and 225 C subsequent nozzle targets, 80 C bed target, startup
explicit extrusion, printable polygon, 3.50 brim, zero skirt, zero prime tower,
and every inherited I3.5 path gate.

## 7. Manifests, RED expectations, and hash/copy proof

`i3_8_validation_manifest.json` has separate `cad_phase` and `print_release`
objects. `cad_phase.status` may become PASS only from complete inherited CAD/
STEP and Section1/4/5 source-3MF evidence. Its `backend_status` must remain
`DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE` with the exact Section2 exit/log facts.
`print_release.status` remains RED/PENDING until all six real G-code hashes,
wrapper reports, semantic T0 parser reports, profile/temperature/settings
proof, and inherited slice gates exist and pass.

The RED suite must assert that exit139, exit143, an absent backend, or missing
G-code can never be a print-release pass. It must not fail otherwise complete
CAD-phase evidence merely because the documented external headless backend is
unavailable. Any fake empty G-code, synthetic success file, omitted crash/hang,
embedded extruder other than1, use of `--load-filament-ids`, non-T0 deposition,
profile substitution, non-JCS JSON, ZIP-byte-equality requirement, semantic 3MF
drift, or claim of physical proof is RED.

The I3.8 SHA-256 is published externally after this immutable document closes;
it is not embedded in itself. Before implementation, copy this exact file into
the evidence root and record source/copy hashes. After CAD-phase work and again
after any future print-release work, rehash the workspace document, evidence
copy, I3.1-I3.7 documents, frozen STEP, all I3.6 active profile files, pinned
JCS implementation/vectors, source 3MF semantic manifest, and every produced
report/output. `i3_8_locked_copy_preservation_report.json` requires the
externally published I3.8 hash, equal source/copy pre/post hashes, no spec byte
drift, and an empty violations array for the phase being accepted.

The detached main manifest contains published I3.1-I3.8 hashes but not its own
digest; its sibling `.sha256` file hashes final manifest bytes. I3.8 CAD-phase
acceptance, future print release, and physical acceptance are three distinct
states and may not be collapsed.
