# G0-G3 gate procedure

Use one immutable candidate fingerprint at a time. A later correction reopens
the earliest gate it affects and creates a new candidate; it does not erase the
older evidence.

## DESIGN-PREVIEW: small-set intent gate

For one to three new assets or a narrow edit, freeze reused reference hashes and
one sentence of user intent classified as expression, identity, action, or
technical. Record the allowed delta, invariants, exact text or `null`, output
paths, and stop condition. One concise receipt may cover the batch.

Record clarification and the user's selection as contract formation. Begin
execution-rework counting only after that contract is unambiguous and frozen;
also record any defect that leaks past the gate expected to catch it.

Use one initial native call per native-art asset; a deterministic text-only
pilot uses zero native image calls. Apply narrow deterministic checks and a
distinct reviewer for the requested change and plausible regressions. Do not
require the complete G2/G3 pack evidence set or start an automatic retry loop.
If alpha or another machine fact fails, label the result non-production; do not
export it or scale generation. Before leaving the small preview, run one
representative real-alpha pilot at intended platform sizes through the normal
machine and independent-review gates.

Keep one current-authority index. On user approval, immediately bind the exact
approved path and SHA-256 there. When feedback changes authority, update that
pointer and retain older evidence as superseded history rather than stacking
competing current-status summaries.

### Text-only delta

Freeze the base image, exact Unicode, actual approved font file, renderer or
composition method, treatment map, and visual examples by path and SHA-256.
Freeze placement, case, punctuation, fill/stroke/halo, and overlay bounds. A
generic replacement font or copied configuration without rendered evidence
reopens this gate.

The production owner renders one overlay from those inputs. Machine evidence
compares decoded base/output pixels and requires zero changes outside the
overlay's actual nonzero-alpha mask. A distinct reviewer checks the rendered
text and contract-required outline or halo (white only when specified) at native
and relevant small sizes, plus focused overlap, crop, and readability
regressions. Reuse the frozen context and do not repeat a full-pack audit unless
the delta or a shared failure expands scope.

## G0: source authority

Record before generation:

- byte-preserved originals with role, dimensions, and SHA-256;
- canonical names, pack count, stable slot order, and platform partition;
- whether each input is a finished asset, scene cell, identity anchor, or
  correction example;
- explicit authority order including `user_correction`, `source`, `identity`,
  and `text`;
- external actions that are outside the current authorization.

Stop if a source is missing, mutable, ambiguously assigned, or its hash changes.

## G1: per-slot design contract

Create one ordered row per sticker. Freeze its source, observable action, prop
and contact, body/camera/crop, expression, visible limb counts, named
occlusions, forbidden ambiguous forms, effects and completeness, exact text or
`null`, production method, allowed delta, invariants, risks, and master
filename.

Run `contract` before showing the source-to-plan sheet. Duplicate semantic
signatures are advisory. Do not rewrite a source-faithful scene merely to make
the pack more varied. Ask the user to approve whether the rows describe the
intended stickers, including similarities the user wants preserved.

## G2: risk-representative pilot

Select the smallest set that covers every planned production method and these
risks when present:

- identity close-up and characteristic style;
- full-body topology with visible hands and feet;
- prone or intentionally occluded anatomy;
- large prop with explicit hand/body ownership;
- edge-dense effects, hands, feet, prop, and white border;
- densest exact copy as a separate deterministic typography pilot.

Run `candidate` before visual review. Review each hash-bound candidate beside
its exact source at native size and at 512, 370, and 190 pixels on white and
dark backgrounds. The user owns identity, intent, and overall feel. A distinct
critic owns anatomy, crop, border, prop/effect completeness, and consistency.

Approval applies only to the methods represented. Changing a method returns
that method to G2.

## G3: bounded production waves

Treat the approved pilot as the first wave. Then allow at most eight unreviewed
slots before closing another review. Preserve passed candidate hashes.

For every wave:

1. Generate or edit against the exact slot contract.
2. Run `candidate` to an absent evidence directory with one stable implementer
   identity; preserve that identity in the candidate provenance.
3. Resolve all machine failures before human review.
4. Have a reviewer distinct from the art implementer inspect every slot and
   complete the generated CSV.
5. Run `review-lint` to an absent directory with the same implementer identity.
6. Advance only when machine status is `PASS`, human status is `PASS`, and all
   required user design approvals for represented methods are bound to the
   candidate hashes.

Two shared failures stop the wave and reopen the common contract. A slot-level
failure may retry only that slot within its attempt ceiling. Never promote from
a contact-sheet impression, partial row set, or machine status alone.

If any CSV reviewer identity equals the bound implementer identity,
`review-lint` must remain `PENDING` with exit code `5`; assign a genuinely
distinct reviewer rather than renaming the same reviewer.

## Required evidence through G3

- canonical contract output and source hashes;
- candidate `audit.json`, summaries, checksums, and warning triage;
- per-slot source/candidate comparison;
- per-slot multi-size light and dark evidence;
- one selectable manifest item per slot; supplemental contact sheet;
- completed hash-bound review CSV and `review-lint` result;
- exact user approval statement for G1/G2 when required.

The audit tool proves deterministic image facts and review-record completeness.
It does not prove that the reviewer made a correct visual judgment.

## Evidence reuse and interrupted runs

- `review-lint` checks consistency of the reviewed candidate recorded beside
  the CSV. It does not inspect a current masters directory or prove the visual
  judgment correct. Before promoting or calling the latest masters accepted,
  compare every current master path and SHA-256 to the corresponding candidate
  `audit.json` row. Any mismatch requires a fresh candidate audit and review;
  retain the earlier PASS as historical evidence.
- If a run is interrupted, preserve its output and owned `.*.audit-tmp` residue
  for diagnosis. Retry once at a new explicit absent output target. Do not
  broadly delete temp paths, silently reuse the blocked target, or loop retries.
  Cleanup needs verified ownership and a separately authorized, recoverable
  action.
