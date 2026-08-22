# KAGE P3 V3 Phase-3 I3.11 — transform and OPC projection closure

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation; print release remains RED**

Date: **2026-08-19**

Supersedes only I3.10's transform, content-type, XML-equivalence, and
relationship projection clauses. All I3.8-I3.10 phase, tool, member grammar,
detached traceability, parity, backend-failure, profile, print-release, RED,
and physical-proof gates remain active.

Immutable immediate predecessor:

```text
I3.10 e398947925734687a060324adcf91d2c12584739f70dfe48c76a9cd2834d9e0b
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

The parity projection schema string becomes
`kage.i3.11.3mf-parity-projection.v2`.

## 1. Exact 3MF build-item transform

`project.objects[*].transform` comes only from the corresponding
`3D/3dmodel.model` XML `build/item/@transform`. A missing attribute means the
exact identity token sequence `1 0 0 0 1 0 0 0 1 0 0 0`. Otherwise split on
XML whitespace characters U+0020, U+0009, U+000D, and U+000A, collapsing runs
and removing leading/trailing whitespace. Exactly 12 nonempty tokens are
required in this order:

```text
m00 m01 m02 m10 m11 m12 m20 m21 m22 m30 m31 m32
```

They form the 3MF row-vector affine matrix:

```text
      [m00 m01 m02 0]
M  =  [m10 m11 m12 0]
      [m20 m21 m22 0]
      [m30 m31 m32 1]

[x' y' z' 1] = [x y z 1] * M
x'=x*m00+y*m10+z*m20+m30
y'=x*m01+y*m11+z*m21+m31
z'=x*m02+y*m12+z*m22+m32
```

Accepted token syntax is ASCII only and exactly:

```text
[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?
```

Thus decimal or exponent form is accepted; hexadecimal floats, commas,
underscores, bare signs, `INF`, `-INF`, `NaN`, and non-ASCII digits are RED.
Parse the mathematical decimal value according to XML Schema `double` value
semantics into IEEE754 binary64 using round-to-nearest ties-to-even. Preserve
finite normal and subnormal results; reject overflow, any nonfinite result, or
an implementation that does not prove correct rounding. Normalize both
positive and negative binary64 zero to JSON integer0 before RFC8785 JCS.

The projection stores the 12 normalized numbers in the exact token order above,
not a transposed or expanded 16-value matrix. Token-count drift, row/column
swap, host-locale parsing, extended-precision leakage, or negative-zero JSON is
RED.

## 2. OPC content-type projection

Replace I3.10 `project.content_types` with exactly:

```json
"content_types": {
  "defaults": [],
  "overrides": [],
  "resolved": []
}
```

Parse `[Content_Types].xml` only in its OPC namespace. Normalize every package
part name to a leading-slash absolute form using the internal-target path rules
in Section4; the ZIP member `[Content_Types].xml` itself is not a declared part.

`defaults` entries contain exactly `extension` and `content_type`. Extension is
nonempty ASCII without dot or slash and is normalized to lowercase ASCII.
Extensions are unique under ASCII case folding; conflicting or duplicate
defaults are RED. Sort by normalized extension.

`overrides` entries contain exactly `part_name` and `content_type`. Part names
start with one `/`, resolve to an existing I3.9-allowlisted member, and are
unique after path and percent normalization. ASCII-case-fold collisions are
RED even though package lookup itself is case-sensitive. Sort by normalized
part name.

A content type is exactly one ASCII RFC6838-style `type/subtype` with no
parameters or surrounding whitespace. Each type and subtype uses only letters,
digits, `!#$&^_.+-`; normalize ASCII letters to lowercase. Invalid, duplicate,
or conflicting declarations are RED.

`resolved` has one entry for every accepted member except
`[Content_Types].xml`, sorted by normalized leading-slash `part_name`. Each
entry has exactly `part_name`, `content_type`, and `source`, where source is
`"override"` or `"default"`. An exact normalized override wins; otherwise use
the member's final extension after the last dot and its normalized default.
Missing declarations, an override for a nonexistent member, two applicable
overrides, an extensionless member without override, or a resolved type that
conflicts with the relationship/model grammar is RED.

## 3. Narrow Canonical XML claim

XML member parity continues to use Canonical XML1.1 bytes without comments.
Only lexical changes that produce identical C14N1.1 bytes retain the XML member
canonical hash. C14N does not normalize element/attribute values as typed
numbers or URIs.

Consequently `1`, `1.0`, and `1e0` may normalize to the same parsed binary64
transform value in Section1 but generally have different C14N bytes and are not
guaranteed semantic parity while the full XML canonical hash remains in the
projection. The same limitation applies to URI and content-type lexical forms.
A future amendment may define and substitute a typed normalized XML projection;
until then, parsed fields add assertions but do not erase C14N differences.

Claims that arbitrary XML reformatting, numeric spelling, namespace-prefix,
attribute-value, URI spelling, or content-type spelling is semantic-equivalent
without byte-identical C14N1.1 output are RED.

## 4. OPC relationship target resolution

Only `_rels/.rels` and optional `3D/_rels/3dmodel.model.rels` are relationship
parts. Their source parts are respectively package root `/` and
`/3D/3dmodel.model`. Deriving another source by suffix or guessing is RED.

For every `Relationship`, require unique nonempty XML `Id`, nonempty absolute
ASCII RFC3986 `Type` URI, and nonempty `Target`. `TargetMode` omitted or ASCII-
case-insensitive `Internal` means internal. ASCII-case-insensitive `External`
means external; all other values are RED. External targets are forbidden in
the I3.11 source project and therefore RED before dereference or network access.

An internal `Target` is an ASCII URI-reference path only. Literal non-ASCII,
backslash, control characters, invalid `%` triplets, scheme, authority, query,
or fragment are RED. Normalize percent triplets to uppercase hex and decode
percent-encoded RFC3986 unreserved bytes only (`ALPHA`, `DIGIT`, `-._~`). Keep
reserved bytes percent-encoded; percent-encoded slash, backslash, NUL, dot
segment, or UTF-8/non-ASCII byte is RED to prevent alternate path readings.

Resolve a relative target against the source part's containing directory; an
initial `/` is package-root absolute. Apply RFC3986 dot-segment removal after
unreserved decoding. Traversal above root, empty final part, trailing slash,
double slash, or a remaining `.`/`..` segment is RED. The normalized result has
exactly one leading `/`; strip that slash only when matching the exact UTF-8 ZIP
member name. Lookup is case-sensitive, while any ASCII-case-fold or NFC
collision with another member is RED. The resolved member must exist and be in
the I3.9 required/optional allowlist.

Replace I3.10 relationship entries with exactly:

```json
{
  "source_part": "/",
  "id": "relationship-id",
  "type": "absolute-type-uri",
  "target_mode": "internal",
  "target_uri": "normalized-reference",
  "resolved_part_name": "/normalized/package/part"
}
```

Normalize `target_mode` to lowercase. Sort entries lexicographically by
`source_part`, `id`, `type`, `target_mode`, `target_uri`, then
`resolved_part_name`. Duplicate IDs within one relationship part, duplicate
normalized semantic tuples, two lexical targets resolving ambiguously, missing
targets, relationship cycles prohibited by OPC/3MF grammar, or any external
relationship are RED.

## 5. Preserved gates and I3.11 anchors

Semantic parity still compares only complete RFC8785 JCS bytes of the I3.11 v2
projection. Detached archive/member raw hashes and sizes remain provenance and
may differ without failing parity. Unknown members, wrong grammar, canonical
member differences, decoded PNG differences, parsed project differences, or
any Section1-4 violation remain RED.

I3.8's phase split is unchanged: CAD/STEP/source-3MF acceptance may pass with
`DEFERRED_EXTERNAL_BACKEND_UNAVAILABLE`; final print release remains
RED/PENDING until six real G-codes pass all inherited profile/T0/first-layer
gates; neither proves physical acceptance.

Add I3.11 RED tests for transform token/parser/order errors, negative zero,
content-type default/override ambiguity, missing resolved declarations,
overbroad C14N equivalence, invalid or external relationship targets,
percent/path traversal ambiguity, collision, or relationship projection/order
drift. All I3.8-I3.10 RED rules remain active.

The I3.11 SHA-256 is externally published after this immutable file closes and
is not embedded in itself. Before implementation, copy it into the evidence
root. `i3_11_locked_copy_preservation_report.json` records the published I3.11
hash, equal source/copy pre/post hashes, I3.1-I3.10 and frozen STEP hashes,
detached traceability JCS hash, I3.11 v2 projection JCS hash, and an empty
violations array for the phase accepted. The detached main manifest adds the
published I3.11 hash but not its own digest; its sibling `.sha256` hashes final
manifest bytes.
