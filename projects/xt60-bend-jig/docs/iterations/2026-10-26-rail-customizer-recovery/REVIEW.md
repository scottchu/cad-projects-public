# Independent simulator review

Candidate manifest: `CANDIDATE.sha256`. Implementation owner: root.

- Critic: `/root/rail_critic`, read-only, gpt-6.1-sol/high.
- Validator: `/root/rail_validator`, read-only, gpt-6.1-sol/medium.
- Formal reviewer: pending join after critic/validator PASS.

Model choice: high for geometric/interaction critique, medium for deterministic
validation. One bounded pass plus at most two focused repair rounds. Only
read-only roles are delegated; this task creates no CAD candidate.

Initial critic finding P2: valid large diagonal endpoints clipped rotating local
rails because the viewport bounded only raw coordinates. RESOLVED by bounding
endpoint Euclidean norms plus stroke envelopes and padding. Linear interpolation
cannot exceed the maximum endpoint norm; rotations preserve it. Added the exact
extreme-diagonal regression across both ±180° frames and fixed axle.

P3 copy assumed default opposite rotations and fixed axle while profiles can
vary these. RESOLVED by qualifying defaults. Added a warning for slots narrower
than the purchased Ø4 rod.

Critic focused repair receipt: PASS on manifest
`3fe9b64214c53a9e6ecf0c7df753e4e0cab65308267c1c5cebea3357d30641a5`;
all nine entries verified, six tests PASS, and standalone/source exact match.
Original reproduction now has bound `93.928 mm` versus maximum slot envelope
`86.928 mm`. Critic inspected source and the supplied prior desktop screenshot;
did not perform live interaction or claim CAD/physical acceptance.

Validator independently PASS on the same repaired manifest, including fresh
offline browser interaction and actual extreme-coordinate clipping regression.
Canonical command/results and limits are in VALIDATION.md.

No final acceptance decision yet. P19/P25 and fabrication statuses remain as recorded.


## Formal join

`/root/rail_acceptance`, distinct formal reviewer, gpt-6.1-sol/high: PASS for
bounded simulator acceptance and advancement to PR preparation on manifest
`3fe9b64214c53a9e6ecf0c7df753e4e0cab65308267c1c5cebea3357d30641a5`.
RC-1..5 supported; RC-6 remote delivery remains pending. No unresolved candidate
defect. Critic and validator inspected the same exact candidate independently.

Formal reviewer limitation: evidence synthesis from parent-relayed document
transcriptions and distinct critic/validator receipts. Its direct shell reads
failed with EMFILE and its Node tool was unavailable; a first formal worker
returned inconclusive without reviewing. The replacement reviewer did not read
candidate files, recompute hashes, run tests or operate the browser. Root Node
FS independently read back all nine members after the role receipts and checked
every hash. This is packet-based independent synthesis, not a claimed direct
filesystem re-review. No CAD, fabrication, physical-touch or user acceptance.
