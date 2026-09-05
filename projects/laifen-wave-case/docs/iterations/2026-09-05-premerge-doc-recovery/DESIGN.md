# LC-DOC-DES-01 — correction design

## Boundary

This is an evidence-only recovery. The baseline is commit `d0aab1ff` plus the
currently staged candidate manifest
`515b249a19509e5509d4785a47e41896abc34d4d604494e708a0fe5afe33c624`.
It binds the formal finding that the 57-test README claim and the listed
evidence paths are inaccurate. This document does not approve the candidate.

## Exact corrections

### Test scope

The README must say that the command has 55 tests whose required source and
written release inputs are retained by the Git boundary, plus two named
`LOCAL-FIXTURE-ONLY` tests whose R7 fixtures are excluded. The two local-only
tests may remain documented as local regression checks, but must be removed
from a command or sentence labelled fresh-clone-relevant. The corrected text
must preserve the existing limits: no clean clone/install occurred and no
physical acceptance follows.

### Path resolution

For a manifest in
`projects/laifen-wave-case/docs/iterations/2026-09-05-premerge-cleanup/`,
resolve each relative filename against that directory, never against the
repository root or the shell's current directory. Therefore project-root
resources use `../../../`, for example:

```
../../../PROJECT_STATE.md
../../../NEXT_AGENT.md
../../../README.md
../../../docs/WORKFLOW_DEMO.md
../../../openscad/laifen_case_customizer_v1.scad
../../../cad/p1_r7_end_chamfer/print_layout.step
```

The historic visual-fidelity handoff is a sibling iteration and resolves as
`../2026-09-04-openscad-visual-fidelity-recovery/HANDOFF.md`.

`CRITIQUE_EVIDENCE.sha256` and `VALIDATION_DELTA_EVIDENCE.sha256` must replace
only their malformed project-root references with the equivalent paths above.
Their own local files remain bare names. No checksum may name a path that does
not exist at the time it is written.

### Live-route evidence

The previous `live-8448-index.html` entry is invalid because it names no
written file. Capture the exact private URL once with a read-only request:

```
curl --fail --silent --show-error --location --max-time 20 \
  -D LIVE_8448_HEADERS.txt -o LIVE_8448_INDEX.html \
  https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/
```

Run it from the existing `2026-09-05-premerge-cleanup` directory. The response
headers must include a final 200 status; the body is a receipt of the route at
capture time only. Hash both written files and list them by their bare names in
`VALIDATION_DELTA_EVIDENCE.sha256`. This reads the already-running service; it
does not imply that the service artifact is tracked or reproducible from the
capture.

## Required independent checks

1. A validator runs a resolver from each evidence manifest's own directory,
   checks all listed SHA-256 values, and confirms there are no dangling paths.
2. A distinct reviewer verifies the README's 55/2 language against the test
   node selection and excluded fixture boundary.
3. Both verify that the two authority hashes in the brief are unchanged.
4. The coordinator produces a new staged-candidate manifest after all allowed
   documents are in place. No old validation, critique, or formal receipt can
   approve that new fingerprint automatically.
