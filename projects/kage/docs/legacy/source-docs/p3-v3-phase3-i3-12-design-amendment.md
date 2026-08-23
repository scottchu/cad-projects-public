# KAGE P3 V3 Phase-3 I3.12 — relationship stage and RGBA8 thumbnail closure

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation; print release remains RED**

Date: **2026-08-19**

Supersedes only I3.11's relationship `target_uri` field name/stage and
I3.9/I3.10's optional-PNG decoding breadth. All I3.8-I3.11 phase, tool, member,
parity, backend, profile, print-release, RED, copy, and physical-proof gates
remain active.

Immutable immediate predecessor:

```text
I3.11 da99646a7c7bf0f4f7487ee7898c504771dc62b467e66b934fc679a25a6598fd
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

The parity projection schema string becomes
`kage.i3.12.3mf-parity-projection.v3`.

## 1. Exact relationship reference stages

Replace I3.11 relationship field `target_uri` with
`normalized_target_reference`. The relationship projection entry is exactly:

```json
{
  "source_part": "/",
  "id": "relationship-id",
  "type": "absolute-type-uri",
  "target_mode": "internal",
  "normalized_target_reference": "pre-resolution-reference",
  "resolved_part_name": "/final/absolute/package/part"
}
```

The stages are normative and may not be combined:

1. Decode the XML `Target` attribute according to XML1.0 from valid UTF-8 XML
   bytes. Character/entity references are resolved here. Reject literal
   non-ASCII, control characters, backslash, scheme, authority, query,
   fragment, invalid percent triplet, or any inherited I3.11 URI violation.
2. Normalize percent escapes in that decoded attribute: uppercase hex digits
   and decode only percent-encoded RFC3986 unreserved ASCII bytes. Reject the
   inherited encoded slash, backslash, NUL, dot-segment, UTF-8/non-ASCII, and
   ambiguous-encoding cases. Do not apply a base and do not remove literal dot
   segments. The exact result of this stage is
   `normalized_target_reference`.
3. Resolve that reference against the I3.11 source-part base directory, or the
   package root when it begins `/`. Then apply RFC3986 dot-segment removal and
   every inherited collision/traversal/member-existence rule. The exact final
   leading-slash absolute package path is `resolved_part_name`.

Examples:

```text
source_part                 raw XML Target
/3D/3dmodel.model          ../Metadata/model_settings.config
normalized_target_reference ../Metadata/model_settings.config
resolved_part_name          /Metadata/model_settings.config

source_part                 raw XML Target
/                           3D/%33dmodel.model
normalized_target_reference 3D/3dmodel.model
resolved_part_name          /3D/3dmodel.model

source_part                 raw XML Target
/3D/3dmodel.model          /Metadata/plate_1.png
normalized_target_reference /Metadata/plate_1.png
resolved_part_name          /Metadata/plate_1.png
```

`%33` decodes to unreserved ASCII `3` before storage. By contrast
`../Metadata/a%2fb.png` is RED because normalized `%2F` encodes a reserved
slash, and `%2e%2e/Metadata/x` is RED because it encodes a dot segment. A
projection that stores the final resolved path in both fields, removes `..`
before recording the reference, preserves lowercase escape hex, or records the
raw pre-percent-normalized attribute is RED.

Sort relationships lexicographically by `source_part`, `id`, `type`,
`target_mode`, `normalized_target_reference`, then `resolved_part_name`.

## 2. Optional six-thumbnail PNG contract

The six exact I3.9 `Metadata/plate_1.png` through `plate_6.png` members remain
optional all-or-none. An implementation may omit all six. If present, every
thumbnail must satisfy all of these restrictions:

```text
PNG signature          exact standard 8 bytes
IHDR bit depth         8
IHDR color type        6 (RGBA)
IHDR compression       0
IHDR filter method     0
IHDR interlace         0 (non-interlaced)
allowed chunk types    IHDR, one or more IDAT, IEND only
row order              top-to-bottom
pixel order            left-to-right RGBA, 4 bytes per pixel
```

Width and height are positive integers within the implementation's recorded
resource limits. Verify chunk lengths, ordering, CRCs, one IHDR, one IEND, and
a complete zlib stream. Reconstruct each scanline using its PNG filter byte
0-4 and the PNG RGBA8 bytes-per-pixel value4. After filter reconstruction,
concatenate the scanline payload bytes unchanged in top-left row-major order;
the canonical pixel buffer is exactly `width*height*4` bytes and its SHA-256 is
`pixel_sha256`.

No palette expansion, grayscale expansion, RGB alpha insertion, 16-to-8-bit
conversion, premultiplication, channel reorder, interlace pass assembly,
gamma/ICC/sRGB/chromaticity conversion, or other color management is allowed.
Bit depths other than8; color types other than6; interlace1; `PLTE`, `tRNS`,
`gAMA`, `cHRM`, `iCCP`, `sRGB`, any other ancillary chunk, or any unknown chunk
is RED. Omitting the complete optional six-PNG set is valid and produces an
empty `members.png` object.

For a present PNG entry, I3.10's projection fields remain exact, but
`color_type` must be6, `bit_depth` must be8, `row_order` must be
`"top-to-bottom"`, and `pixel_format` must be `"RGBA8"`.

## 3. Preserved parity/phase gates and I3.12 anchors

Semantic parity compares only complete RFC8785 JCS bytes of the I3.12 v3
projection. Detached raw archive/member hashes remain provenance and may differ
without failing parity. Unknown members, grammar failures, canonical JSON/XML
differences, parsed project differences, relationship-stage differences, or
canonical RGBA8 pixel differences remain RED.

I3.8's phase split remains unchanged: complete CAD/STEP/source-3MF evidence may
pass with backend status `DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE`; final print
release remains RED/PENDING until six actual G-codes pass all inherited
profile/T0/first-layer gates; neither proves physical acceptance.

Add I3.12 RED tests for wrong relationship field/stage, pre-resolution dot
removal, unresolved final path, percent-normalization drift, changed sort key,
partial thumbnail set, non-RGBA8 or interlaced PNG, ancillary chunk, decoded
pixel conversion, wrong row/channel order, or pixel-buffer length/hash drift.
All I3.8-I3.11 RED rules remain active.

The I3.12 SHA-256 is externally published after this immutable file closes and
is not embedded in itself. Before implementation, copy it into the evidence
root. `i3_12_locked_copy_preservation_report.json` records the published I3.12
hash, equal source/copy pre/post hashes, I3.1-I3.11 and frozen STEP hashes,
detached traceability JCS hash, I3.12 v3 projection JCS hash, and an empty
violations array for the phase accepted. The detached main manifest adds the
published I3.12 hash but not its own digest; its sibling `.sha256` hashes final
manifest bytes.
