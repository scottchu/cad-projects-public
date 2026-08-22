# KAGE P3 V3 Phase-3 I3.7 — deterministic CLI and tool-0 closure

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation**

Date: **2026-08-19**

Supersedes I3.6 only where this document is more specific about CLI loading,
profile flattening, six-object filament assignment, and G-code tool gates.

Immutable predecessors:

```text
I3.1  abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77
I3.2  9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3
I3.3  4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691
I3.4  c6fb12ceab347b258b4f3be65b61d32f178bbf3075cf68869d5d87e9d47636e1
I3.5  08ab0d28e84036a3bcf17e74e9d3ab18d22c376f8a9f71f4cd1fd6494ede35d6
I3.6  326f9dbd21fa04885447c8080390a70187176f90020f0ebfee212255bc4154f9
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

This amendment specifies implementation evidence only. It does not alter CAD,
source, tests, meshes, tooth geometry, moving-half geometry, or physical
acceptance gates.

## 1. Verified CLI identity and precedence

The only accepted executable remains:

```text
/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca
SHA-256 4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe
```

The application `Info.plist` short version is `2.3.5`. A read-only `--help`
invocation on 2026-08-19 emitted the different internal CLI banner
`Snapmaker_Orca-01.10.01.50`; both strings are mandatory report fields and are
not treated as interchangeable versions.

That same help output exposes `--datadir`, `--load-settings`,
`--load-filaments`, `--load-filament-ids`, `--export-settings`,
`--export-3mf`, `--outputdir`, and `--slice`. It states this precedence:

```text
1. command-line setting values
2. values loaded by --load-settings and --load-filaments
3. values embedded in the 3MF
```

The CLI does not expose direct `--brim-width`, `--skirt-loops`, or
`--enable-prime-tower` options. Inventing such flags is RED. Those values are
therefore supplied in the source-owned flattened settings JSON described
below. The help text does not guarantee execution order for multiple export or
slice actions in one process, so I3.7 forbids a combined multi-action command.

## 2. Six-object filament and physical-tool mapping

The source project has exactly six objects in this exact order, one object on
each of six plates:

```text
1 hour   I3_half_A_130T_beta15p230769
2 hour   I3_half_B_130T_beta195p230769
3 minute I3_half_A_130T_beta15p230769
4 minute I3_half_B_130T_beta195p230769
5 second I3_half_A_130T_beta15p230769
6 second I3_half_B_130T_beta195p230769
```

Every 3MF object mapping must contain Orca property `extruder=1`. Every CLI
invocation must additionally pass `--load-filament-ids '1,1,1,1,1,1'`.
Within Orca's one-based object/filament mapping, filament ID1 maps to the first
loaded filament and physical tool index0; generated tool-selection G-code is
therefore `T0`.

For each of the six G-code files, strip `;` comments, ignore blank lines, and
read the first command word case-insensitively. The set of standalone tool
selection commands must be exactly `{T0}`. In particular the raw-file regex
`(?im)^[ \t]*T[123](?:[ \t;]|$)` must have zero matches, and parsed deposited
extrusion must occur only while physical tool0 is active. A `T1`, `T2`, or `T3`
address operand on a non-tool-selection command such as `M104` is reported
separately and does not change the active tool; it may not be misclassified as
a standalone tool change. Missing T0, any standalone T1/T2/T3, or deposition
with tool1/2/3 is RED.

## 3. Immutable copied datadir and input bundle

The implementation evidence root is exactly:

```text
/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli
```

Its immutable datadir seed is:

```text
input/datadir_seed/Snapmaker_Orca.conf
input/datadir_seed/system/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json
input/datadir_seed/system/Snapmaker/machine/fdm_U1.json
input/datadir_seed/system/Snapmaker/machine/fdm_toolchanger.json
input/datadir_seed/system/Snapmaker/machine/fdm_klipper.json
input/datadir_seed/system/Snapmaker/process/0.20 Standard @Snapmaker U1 (0.4 nozzle).json
input/datadir_seed/system/Snapmaker/process/fdm_process_U1_0.20.json
input/datadir_seed/system/Snapmaker/process/fdm_process_U1_common.json
input/datadir_seed/system/Snapmaker/process/fdm_process_U1.json
input/datadir_seed/user/default/filament/PETG.json
input/datadir_seed/system/Snapmaker/filament/Generic PETG.json
input/datadir_seed/system/Snapmaker/filament/Generic PETG @base.json
input/datadir_seed/system/Snapmaker/filament/fdm_filament_pet_generic.json
input/datadir_seed/system/Snapmaker/filament/fdm_filament_common_generic.json
```

Every file is a byte-for-byte copy of the exact I3.6 active source path and
must reproduce its full I3.6 SHA-256. In particular the active system machine
leaf remains hash
`545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d`.
The bundled application profile hash
`67047c9fd6d2e935c1e0b84afaf6a674698e326a7785d7c6febd47f3d7d3e765`
is nonactive and must not enter the seed or flattened bundle.

The source-owned input bundle paths are exactly:

```text
input/profile_bundle/i3_7_machine_process_flat.json
input/profile_bundle/i3_7_petg_flat.json
input/profile_bundle/i3_7_profile_bundle_manifest.json
input/project/i3_7_six_moving_halves_source.3mf
```

The immutable seed is never passed directly to a process that may write it.
Before the three commands in Section 5, copy it byte-for-byte into these three
fresh, initially absent directories and verify the complete copied-file hash
map before launch:

```text
work/datadir_export_settings
work/datadir_export_3mf
work/datadir_slice_all
```

No prior run state, user home datadir, OTA profile, backup profile, bundle
profile, cache, or GUI selection may be visible through `--datadir`.

## 4. Deterministic flattening and canonical JSON

Reject duplicate JSON keys. Parse every copied profile as UTF-8 JSON. Merge by
top-level key with whole-value replacement; arrays are replaced, never
concatenated, and nested objects are replaced, never recursively merged. For
the machine/process flat file, apply sources in this exact oldest-to-newest
order:

```text
1 machine fdm_klipper
2 machine fdm_toolchanger
3 machine fdm_U1
4 machine Snapmaker U1 (0.4 nozzle), active system hash
  545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d
5 process fdm_process_U1
6 process fdm_process_U1_common
7 process fdm_process_U1_0.20
8 process 0.20 Standard @Snapmaker U1 (0.4 nozzle)
9 explicit I3.7 overrides
```

At steps1-8 omit only profile metadata keys `name`, `inherits`, `version`, and
`from`; all slicer-setting keys participate. Step9 is exactly this Orca-native
serialized object:

```json
{
  "brim_width": "3.5",
  "enable_prime_tower": "0",
  "skirt_loops": "0"
}
```

The semantic types are respectively float millimetres3.5, boolean false, and
integer0. String storage is mandatory because these Snapmaker Orca preset JSONs
serialize config values as strings; converting them to JSON number/boolean
types is RED. Add final metadata `name="I3.7 U1 0.4 moving"`, `from="User"`,
`inherits=""`; no inherited lookup remains in the flat output.

Flatten PETG independently in this exact oldest-to-newest order:

```text
1 fdm_filament_common_generic
2 fdm_filament_pet_generic
3 Generic PETG @base
4 Generic PETG
5 user/default/filament/PETG
```

Use the same omission and whole-value replacement rules, then add final
metadata `name="I3.7 PETG"`, `from="User"`, `inherits=""`. The resolved identity
and temperatures must remain:

```text
filament_type                         PETG
filament_vendor                       Generic
filament_id                           GFG00
nozzle_temperature_initial_layer      240 C
nozzle_temperature                    225 C
hot_plate_temp_initial_layer          80 C
hot_plate_temp                        80 C
```

Serialize both flat objects canonically as UTF-8 without BOM: object keys
sorted by ascending UTF-8 byte sequence, arrays kept in source order, no
insignificant whitespace, JSON escapes only where required by RFC 8259, and
one terminal LF. The profile-bundle manifest records each source absolute
path, copied relative path, full SHA-256, inheritance edge, merge ordinal,
every final key's winning owner, the three typed override interpretations, and
both canonical output SHA-256 values. Re-flattening twice in fresh processes
must produce byte-identical outputs.

## 5. Exact isolated CLI commands

Create the output directories before launch. Execute exactly these three
commands separately and in order; capture stdout, stderr, exit status, start
time, and end time for each. No command may use `--uptodate`,
`--load-defaultfila`, `--skip-modified-gcodes`, or an unlisted setting source.

### 5.1 Export resolved settings

```sh
'/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca' \
  --datadir '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/work/datadir_export_settings' \
  --load-settings '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/profile_bundle/i3_7_machine_process_flat.json' \
  --load-filaments '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/profile_bundle/i3_7_petg_flat.json' \
  --load-filament-ids '1,1,1,1,1,1' \
  --outputdir '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/out/settings' \
  --export-settings '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/out/settings/i3_7_resolved_settings.json' \
  '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/project/i3_7_six_moving_halves_source.3mf'
```

### 5.2 Export resolved project 3MF

```sh
'/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca' \
  --datadir '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/work/datadir_export_3mf' \
  --load-settings '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/profile_bundle/i3_7_machine_process_flat.json' \
  --load-filaments '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/profile_bundle/i3_7_petg_flat.json' \
  --load-filament-ids '1,1,1,1,1,1' \
  --outputdir '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/out/project' \
  --export-3mf '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/out/project/i3_7_six_moving_halves_resolved.3mf' \
  '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/project/i3_7_six_moving_halves_source.3mf'
```

### 5.3 Slice all six plates

```sh
'/Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca' \
  --datadir '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/work/datadir_slice_all' \
  --load-settings '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/profile_bundle/i3_7_machine_process_flat.json' \
  --load-filaments '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/input/profile_bundle/i3_7_petg_flat.json' \
  --load-filament-ids '1,1,1,1,1,1' \
  --outputdir '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/out/gcode' \
  --slice 0 \
  '/Users/scottchu/Projects/personal/3d-print/design/japandi-shadow-clock-simulator/evidence/i3_7_cli/out/project/i3_7_six_moving_halves_resolved.3mf'
```

All three exit statuses must be0. The export-settings invocation must produce
exactly `out/settings/i3_7_resolved_settings.json`; the project invocation must
produce exactly `out/project/i3_7_six_moving_halves_resolved.3mf`; the slice
invocation must produce exactly six regular G-code files and no extra G-code.
Because the installed CLI exposes only an output directory for slicing, their
actual slicer-generated basenames are implementation outputs: sort them by
UTF-8 basename, record all six exact relative paths and SHA-256 values in the
manifest, and bind each to its plate index and sole object identity. Renaming
or guessing a basename before hashing is RED.

## 6. Acceptance manifest and RED gates

`i3_7_cli_manifest.json` must contain:

- executable path/hash, `Info.plist` path/hash and version2.3.5, plus CLI
  banner `Snapmaker_Orca-01.10.01.50`;
- immutable datadir seed hash map, three pre-launch copied-datadir hash maps,
  profile-bundle manifest/hash, source 3MF hash, and all three exact argv arrays;
- each command's stdout/stderr path/hash, exit status and times;
- resolved settings path/hash and parsed key/type/value assertions for
  machine, 0.4 nozzles, raw bed type3, process, PETG identity/temperatures,
  brim width3.5, skirt loops0, and prime tower false;
- resolved 3MF path/hash and exactly six plate/object mappings, each
  `extruder=1`, filament ID1, physical tool0;
- six sorted G-code relative paths/hashes, plate/object bindings, parsed tool
  command sets, deposited-extrusion tool sets, and raw standalone-T1/T2/T3
  match counts;
- inherited I3.5 full first-layer path-containment, startup-line,
  brim-measurement, skirt, prime-tower, and violation fields.

Every G-code must prove `{T0}` as its complete standalone tool-selection set,
tool0 as its complete deposited-extrusion tool set, zero standalone T1/T2/T3,
PETG 240 C first-layer and 225 C subsequent nozzle targets, 80 C first/current
bed targets for raw bed type3, no prime-tower marker or extrusion, no skirt
extrusion, and measured 3.50 mm brim within the inherited 0.05 mm tolerance.
Embedded-3MF conflicts are acceptable only when the exported resolved settings
and resolved 3MF prove the CLI-loaded value won under the verified precedence.

Any missing object, non-1 object extruder mapping, non-1 CLI filament ID,
physical tool other than0, standalone T1/T2/T3, non-PETG identity/temperature,
unresolved inheritance, bundled application machine substitution, direct config-key
flag, combined multi-action process, reused mutable datadir, stale output,
unhashed basename, skirt, prime tower, or non-3.50 moving brim is RED.

## 7. I3.7 hash and locked-copy proof

The I3.7 SHA-256 is published externally after this immutable file is closed;
it is not embedded in itself. Before any implementation work, copy this exact
document into the evidence root and record source and copy byte hashes in
`i3_7_locked_copy_preservation_report.json`. After all CLI work, rehash the
workspace document, evidence copy, I3.1-I3.6 documents, frozen STEP, I3.6
render-package inputs, the immutable datadir seed, profile bundle, source 3MF,
resolved settings, resolved 3MF, and six G-codes. The report requires identical
pre/post I3.7 document bytes, equality between source and evidence-copy hashes,
the externally published I3.7 hash, and an empty violations array.

The detached validation manifest includes the published I3.1-I3.7 hashes but
does not include its own digest. Its sibling `.sha256` file hashes the final
manifest bytes. A self-referential manifest, post-implementation spec edit,
missing I3.7 evidence copy, hash mismatch, or incomplete six-G-code set is RED.
