# KAGE P3 V3 Phase-3 I3.10 — detached 3MF traceability and parity projection

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation; print release remains RED**

Date: **2026-08-19**

Supersedes only I3.9 Section4 where raw archive/member fields were included in
the semantic manifest. I3.8/I3.9 member grammar, unknown-member RED rules,
six object/UUID/extruder1/filament-slot1/T0 mappings, backend evidence, phase
split, profile locks, and physical-proof boundary remain unchanged.

Immutable immediate predecessor:

```text
I3.9  88e3ca6ede27fd37d3fd22039362698994914ff1deceed82178fb170fe88408e
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

## 1. Detached provenance traceability

`i3_10_3mf_traceability.json` records the complete archive SHA-256 and byte
size plus every accepted member's exact path, compressed size, uncompressed
size, CRC32, compression method, and raw uncompressed-member SHA-256. It is
RFC8785 JCS and is required provenance evidence, but neither its bytes nor any
of those raw fields participates in semantic parity equality.

Regeneration may change the archive hash, member raw hash/size, ZIP order,
timestamp, compression, XML lexical form, JSON lexical form, or PNG encoding
without failing semantic parity. Such changes remain visible in detached
traceability. An unknown member, missing required member, disallowed optional
member, path violation, CRC failure, or grammar parse/canonicalization failure
remains RED before either traceability or parity is evaluated.

## 2. Exact semantic `parity_projection` schema

`i3_10_3mf_parity_projection.json` contains exactly these top-level keys:

```json
{
  "schema": "kage.i3.10.3mf-parity-projection.v1",
  "members": {
    "json": {},
    "xml": {},
    "png": {},
    "binary_exact": {}
  },
  "project": {
    "unit": "millimeter",
    "plates": [],
    "objects": [],
    "materials": [],
    "relationships": [],
    "content_types": []
  }
}
```

No raw archive hash, raw member hash, raw size, compressed size, CRC,
compression method, ZIP timestamp/order/extra field, source filesystem path,
or runtime timestamp is permitted anywhere in this projection.

### 2.1 Canonical member projections

`members.json` is an object keyed by each exact I3.9 JCS-JSON member path. Each
value has exactly one key, `jcs_sha256`, containing the lowercase 64-hex
SHA-256 of that member's RFC8785 JCS bytes.

`members.xml` is an object keyed by each exact present I3.9 XML member path.
Each value has exactly one key, `c14n11_sha256`, containing the lowercase
64-hex SHA-256 of its Canonical XML1.1 bytes without comments.

`members.png` is an object keyed by each present allowlisted PNG path. Each
value has exactly these fields:

```json
{
  "width": 0,
  "height": 0,
  "color_type": 0,
  "bit_depth": 0,
  "row_order": "top-to-bottom",
  "pixel_format": "RGBA8",
  "pixel_sha256": "lowercase-64-hex"
}
```

`width` and `height` are positive integers. `color_type` and `bit_depth` are
the source IHDR integers. Decode all PNG filters, interlace passes, palette and
`tRNS` transparency; expand samples to RGBA8 without gamma, ICC, chromaticity,
or color-space conversion. Hash exactly `width*height*4` bytes in top-left,
row-major RGBA channel order with no row padding or header. Ancillary chunks
do not affect parity.

`members.binary_exact` is reserved for a binary member whose exact payload
bytes are explicitly declared semantic by a later accepted amendment. Each
such value has exactly one key, `sha256`. For the I3.10 six-plate source member
set it is exactly `{}`: optional PNGs use decoded pixels, and no current binary
payload is byte-authoritative.

### 2.2 Parsed project projection

`project.unit` is the parsed 3MF model unit. `project.plates` is sorted by
integer plate index and each entry has exactly `plate_index`, `object_uuid`,
and `object_name`. `project.objects` follows 3MF build order and each entry has
exactly `build_index`, `object_uuid`, `object_name`, `resource_id`,
`plate_index`, `transform`, `extruder`, `filament_slot`, and `physical_tool`.
Transforms are arrays of the exact parsed finite JSON numbers in 3MF order;
`extruder` and `filament_slot` are integer1 and `physical_tool` is string
`"T0"` for all six frozen I3.8 objects.

`project.materials` is sorted by integer filament slot and each entry has
exactly `filament_slot`, `profile_name`, `filament_type`, `filament_id`, and
`physical_tool`. Slot1 must resolve to the exact I3.6 user PETG identity and
T0; no slot2-4 object assignment is allowed.

`project.relationships` entries have exactly `source`, `type`, and `target`
and are sorted lexicographically by that three-field tuple. Targets are
normalized package-relative paths and must resolve to I3.9-allowlisted members.
`project.content_types` entries have exactly `part_name` and `content_type`
and are sorted lexicographically by that pair. Missing, extra, duplicate, or
conflicting parsed mappings are RED.

## 3. Sole semantic parity comparison

Validate the exact schema above, then canonicalize the complete projection
with the pinned I3.8 RFC8785 implementation and conformance vectors. Two source
3MF archives have semantic parity if and only if these complete JCS byte
sequences are byte-for-byte equal. The projection SHA-256 is recorded for
indexing, but comparison of the JCS bytes themselves is authoritative.

The detached traceability JSON is never nested, hashed, referenced, or copied
into `parity_projection`; conversely the traceability report records the
projection JCS SHA-256 only as a linkage field that is excluded from parity.
Raw archive/member differences alone cannot fail semantic parity. A canonical
JSON/XML difference, decoded PNG fact/pixel difference, authoritative binary
difference, or parsed project map difference must fail it.

## 4. Preserved phase gates and I3.10 anchors

I3.8's phase split is unchanged. Complete inherited CAD/STEP plus I3.9/I3.10
source-3MF evidence may pass while backend status remains
`DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE`. Final print release remains
RED/PENDING until six actual G-codes pass I3.8's profile, bed, extrusion,
temperature, first-layer, and T0-only gates. Neither phase proves physical
acceptance.

Add I3.10 RED tests for any raw traceability field in the parity projection,
parity comparison of traceability bytes/hashes, omitted canonical member,
wrong PNG row/channel convention, PNG encoding-byte comparison, nonempty
current `binary_exact`, malformed parsed project entry/order, or comparison
other than complete projection JCS bytes. All I3.8/I3.9 unknown-member,
grammar, backend, profile, tool, print-release, and physical-proof RED rules
remain active.

The I3.10 SHA-256 is published externally after this immutable file closes and
is not embedded in itself. Before implementation, copy this exact document
into the evidence root. `i3_10_locked_copy_preservation_report.json` records
the published I3.10 hash, equal source/copy pre/post hashes, I3.1-I3.9 and
frozen STEP hashes, detached traceability JCS hash, parity-projection JCS hash,
and an empty violations array for the phase accepted. The detached main
manifest adds the externally published I3.10 hash but not its own digest; its
sibling `.sha256` hashes final manifest bytes.
