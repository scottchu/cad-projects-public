# KAGE P3 V3 Phase-3 I3.9 — exact source-3MF member grammar

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation; print release remains RED**

Date: **2026-08-19**

Supersedes only I3.8 Section5's ambiguous member-grammar language. I3.8's
CAD/STEP/source-3MF versus print-release split, six frozen name/UUID/extruder1/
filament-slot1/T0 mappings, backend-failure evidence, RFC8785 implementation
and vectors, active I3.6 profile chains, and physical-proof boundary remain
unchanged.

Immutable immediate predecessor:

```text
I3.8  3ca35b53d725c54b3e1299dd3a757a09baba7562dd7e984f1fbd7128be22cf4c
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

## 1. ZIP member path grammar

Decode ZIP member names as UTF-8. Every name uses `/` separators, has no
leading `/`, trailing `/`, empty segment, `.` segment, `..` segment, backslash,
NUL, control character, or Unicode normalization change under NFC. Reject
encrypted entries, symlinks, duplicate byte names, NFC-normalized duplicates,
and ASCII-case-fold collisions. Directory entries are omitted; only regular
file members participate.

Classification is by exact full path from Sections2 and3. A suffix or extension
never selects a grammar. In particular `.config` does not mean XML or JSON.

## 2. Required six-plate source member set

The source-owned unsliced six-plate 3MF contains every member below exactly
once. Each path has the one grammar shown:

| Exact member path | Required grammar |
|---|---|
| `[Content_Types].xml` | XML, Canonical XML1.1 without comments |
| `_rels/.rels` | XML, Canonical XML1.1 without comments |
| `3D/3dmodel.model` | XML, Canonical XML1.1 without comments |
| `Metadata/project_settings.config` | JSON, RFC8785 JCS |
| `Metadata/model_settings.config` | XML, Canonical XML1.1 without comments |
| `Metadata/model_settings.json` | JSON, RFC8785 JCS |
| `Metadata/plate_data.json` | JSON, RFC8785 JCS |

`Metadata/project_settings.config` is JSON despite its `.config` suffix.
`Metadata/model_settings.config` is XML despite the same suffix. The two paths
may not share a parser. Every JSON member must satisfy I3.8's pinned RFC8785
input restrictions and canonicalize through its pinned implementation. Every
XML member must be well-formed XML1.0, use namespace processing, disable DTDs,
external entities and network access, and canonicalize as Canonical XML1.1
without comments. A parse or canonicalization failure is RED.

The required member set represents an unsliced source project. Embedded
`*.gcode`, `*.gcode.md5`, slicedata, print-job payloads, or firmware packages
are not source-project members and are RED.

## 3. Closed optional-member allowlist

Only these exact optional paths are allowed, with the assigned grammar:

| Exact optional member path | Grammar | Presence rule |
|---|---|---|
| `3D/_rels/3dmodel.model.rels` | XML, Canonical XML1.1 without comments | zero or one; every relationship target must resolve to another allowlisted member |
| `Metadata/plate_1.png` | raw binary PNG | all six PNGs present or all absent |
| `Metadata/plate_2.png` | raw binary PNG | all six PNGs present or all absent |
| `Metadata/plate_3.png` | raw binary PNG | all six PNGs present or all absent |
| `Metadata/plate_4.png` | raw binary PNG | all six PNGs present or all absent |
| `Metadata/plate_5.png` | raw binary PNG | all six PNGs present or all absent |
| `Metadata/plate_6.png` | raw binary PNG | all six PNGs present or all absent |

Optional PNGs must have the eight-byte PNG signature, decode without error,
and receive raw-byte SHA-256 values. PNG encoding bytes are traceability data,
not source-3MF semantic parity authority; decoded width, height, color type,
bit depth and RGBA pixel SHA-256 are added to the semantic manifest.

There is no wildcard or extension-based optional policy. Any other member is
unknown and RED unless a later accepted amendment names its exact full path,
assigns exactly one grammar, and defines its semantic-parity fields.

## 4. Grammar-specific semantic manifest

After the path checks, process members as follows:

- JCS JSON: store exact path, uncompressed size, raw traceability SHA-256, and
  SHA-256 of the RFC8785 JCS bytes;
- C14N1.1 XML: store exact path, uncompressed size, raw traceability SHA-256,
  and SHA-256 of Canonical XML1.1 bytes without comments;
- raw binary: store exact path, uncompressed size, raw SHA-256, media
  validation result, and the decoded PNG facts required by Section3.

The top-level semantic manifest is itself RFC8785 JCS. Its `members` object has
exactly the required paths plus the present optional paths and no others. A
member assigned to multiple grammars, parsed according to its suffix, omitted
after extraction, silently retained as unknown, or accepted despite a grammar
failure is RED.

ZIP member order, timestamp, compression and central-directory bytes remain
nonsemantic exactly as I3.8 specifies. Two archives have source-3MF semantic
parity only when their I3.9 JCS semantic-manifest bytes match and the parsed
six-plate model/object/UUID/extruder/filament/tool assertions all pass.

## 5. Phase status, RED anchors, and I3.9 copy proof

I3.8's phase status is unchanged. Complete CAD/STEP/source-3MF evidence may
pass with backend status `DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE`. Final print
release stays RED/PENDING until six real G-codes pass the I3.8 validation and
T0-only semantic parser. Neither state proves physical acceptance.

Add I3.9 to the RED suite for: a missing required member, unknown member,
partial six-PNG set, suffix-selected grammar, JSON/XML confusion between the
two `.config` paths, any parse/canonicalization failure, external XML entity,
unresolved relationship, embedded G-code, or semantic-manifest mismatch. The
documented exit139 crashes, exit143 bounded hang, and unavailable Prusa/Cura
remain an external print-release gate, not a false CAD-phase test failure or
pass.

The I3.9 SHA-256 is published externally after this immutable file closes and
is not embedded in itself. Before implementation, copy this exact file into
the evidence root. `i3_9_locked_copy_preservation_report.json` records the
published I3.9 hash, source/copy pre/post hashes, I3.1-I3.8 hashes, frozen STEP
hash, source archive traceability hash, I3.9 semantic-manifest hash, and an
empty violations array for the phase accepted. The detached main manifest adds
the published I3.9 hash but not its own digest; its sibling `.sha256` hashes the
final manifest bytes.
