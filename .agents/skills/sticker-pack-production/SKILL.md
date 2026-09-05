---
name: sticker-pack-production
description: Prepare and validate source-based sticker packs through source intake, scene-contract approval, risk pilots, and bounded art waves (G0-G3). Use when identity, source fidelity, transparent die-cut art, exact optional text, and exhaustive per-sticker review matter; do not use this skill alone to export, release, upload, or publish a pack.
---

# Sticker Pack Production

Move a sticker pack only through G0-G3: source authority, design contract,
representative pilot, then bounded art waves. The user approves design intent and
character feel; the production team remains responsible for finding technical
and visual defects.

## Hard boundaries

- Preserve supplied sources byte-for-byte and bind every authority file by
  path and SHA-256. A later user correction for a named slot outranks its older
  source; otherwise do not reinterpret the source to improve novelty.
- Treat exact text as data. Record the exact Unicode string or `null`; do not
  ask image generation to render final text.
- Keep these outcomes separate: machine audit, independent human review, and
  user design approval. None implies either of the others.
- Never auto-approve identity, style, source semantics, prop ownership,
  anatomy, occlusion, or text meaning from pixel heuristics.
- Do not edit art, change an approved hash, upload, publish, alter privacy, or
  create a platform release unless the user explicitly puts that action in
  scope. This skill ends at accepted art masters, before composition/export.

## Route by current gate

| Gate | Owner and decision | Unlocks |
|---|---|---|
| G0 source intake | coordinator freezes originals, names, count, order, platform partition, roles, hashes, and authority order | G1 contract work |
| G1 design contract | user approves intended scene/pose/prop/text and allowed differences; recorder freezes one row per slot | G2 pilot production |
| G2 risk pilot | machine preflight first, user judges identity/feel, distinct critic judges defects | only the represented production methods |
| G3 bounded wave | machine audit plus a distinct reviewer dispositions every slot and size | next wave or accepted masters |

Read [references/gates-g0-g3.md](references/gates-g0-g3.md) before planning or
advancing a gate. Read
[references/review-rubric.md](references/review-rubric.md) before selecting a
pilot, briefing a critic, or completing a review CSV.

## Contract and machine evidence

Start from [templates/pack-contract.example.json](templates/pack-contract.example.json),
replace every example authority path/hash and scene field, then run from the
repository root:

```bash
npm run --workspace example-sticker-pack audit:stickers -- contract \
  --contract <contract.json>

npm run --workspace example-sticker-pack audit:stickers -- candidate \
  --contract <contract.json> --masters <masters-dir> \
  --out <absent-evidence-dir> --implementer <stable-implementer-id>

npm run --workspace example-sticker-pack audit:stickers -- review-lint \
  --contract <contract.json> --review <review-disposition.csv> \
  --out <absent-review-lint-dir> --implementer <same-stable-implementer-id>
```

Inputs are read-only. Both output directories must be explicit, absent, and
outside any `release`, `accepted`, or `withdrawn` path component. Keep each run
versioned; never overwrite an earlier evidence directory.

Choose one stable ASCII implementer identity for the candidate and reuse it
unchanged for `review-lint`. Candidate evidence binds that identity. Every CSV
`reviewer` must name a different person or agent; matching reviewer and
implementer identities remain `PENDING` with exit code `5`.

Interpret exit codes literally:

| Code | Meaning |
|---:|---|
| 0 | valid contract, or complete all-PASS human review |
| 2 | candidate machine failure, or a completed human FAIL |
| 3 | invalid contract or missing/changed source authority |
| 4 | unsafe/existing/unwritable output target |
| 5 | machine checks passed but human review is pending/incomplete |

`candidate` normally returns `5` after a clean audit because it creates an
empty review sheet. Do not translate that into success or failure. Inspect
`audit.json`, then complete the CLI-generated `review-disposition.csv`; the
header-only [template](templates/review-disposition.csv) is a field reference,
not a substitute for the hash-bound generated sheet.

## Art production

For new bitmap art or a coherent figure edit, use the available
`creative-production:produce` workflow and `imagegen`. Keep all candidates in
the same active board when a Creative Production board is used. Preserve the
source authority and exact-content contract; one selectable asset belongs in
each review item, while contact sheets remain supplemental evidence.

Choose pilot slots by risk and production-method coverage, not by slot order.
After G2, generate no more than eight unreviewed slots at a time, with at most
four native-image workers and two total native attempts per slot. Preserve
passing hashes and retry only failed slots.

If two or more slots share a failure, stop the wave and reopen the common
identity/style/prompt/method contract. Do not spend isolated retries or widen
local masks to hide a shared defect. Anatomy, pose, scene, or global identity
repairs require a coherent whole-figure edit or regeneration.

## Stop conditions

Stop at the earliest affected gate when source hashes change, a contract row is
ambiguous, a production method lacks a representative pilot, machine audit
fails, review rows are incomplete, a distinct reviewer is unavailable, or
identity/anatomy/semantics are disputed. Return only the unresolved design
choice to the user; do not make the user search the pack for defects.
