# R-E factual handoff

Status: **verified evidence available for actual collaboration**. Owner `/root/first_layer_validator`; facts only, no slide design or implementation. Sources inspected read-only on 2026-09-02 using `sed`, `nl -ba`, `rg`, `shasum -a 256`; no memory/session search needed. Presentation baseline HTML `1798b4c485f9923b45bf740ba7df9a27b577e2cf4c0192511b18322215d39651`.

## Actual person → agent → decision chain

Use **P13 R2 center-hole fit repair**, a different fit case from the OD4 rod coupon and separate from the later print pilot.

- Person observation: `projects/xt60-bend-jig/docs/EXPERIENCE.md:31–36` records the user's printed “middle stick” too thick for the “center hole.” These initially ambiguous words are the recorded observation, not invented dialogue.
- Documented agent contribution: `projects/xt60-bend-jig/docs/iterations/p13-r2-center-hole-fit-repair/HANDOFF.md:20–36` identifies the printed D shaft and the D-shaped bores in two cam plates; unrelated rod, journal, keeper and cap interfaces were not enlarged. Lines **39–49**, explicitly titled “Agent receipt / ledger,” name `/root/design_diagnosis` for exact-mate diagnosis and `/root/implementation` for a failing witness, source edit and regenerated artifacts. This is direct actor attribution, not an inference from passive voice.
- Changed source: same handoff **30–31** records bore OD `5.70 → 5.75 mm` and across-flat `5.25 → 5.30 mm`. The `OD5.60 / AF5.15 mm` shaft stayed unchanged. Both controls then had nominal `0.15 mm` allowance. These are source dimensions, not measured printed dimensions.
- Changed next decision: **101–114** says reprint the two repaired plates with the unchanged shaft, then check passage through both bores by hand without forcing, binding, visible damage or unacceptable play. This is a proposed next physical check, not a completed successful reprint.
- Status: **5–7 and 103–106** distinguish accepted digital/source and artifact/slicer evidence from failed/pending physical acceptance; repaired cam plates had not been printed in this record.

Verified handoff SHA-256: `870120a2dc5460468ef6ceed86188c6422fd7e6006fe17398dca86a1de583cf4`. Corroborating `BRIEF.md:23–27` identifies the real physical failure; SHA-256 `588ef22b8b4d6159eac38185a73b5bc626bb35497cfbbf46d37ae26badc1cb2c`. Include the handoff and S01 in the new candidate manifest/source register if used.

## Preserve attribution and case boundaries

- S01 OD4 rod coupon (`EXPERIENCE.md:5–15`) supplies exact qualitative outcomes and the 4.15 mm reference. It does not identify which agent interpreted or changed that coupon. Do not combine the D-shaft repair's actors/dimensions with this separate sliding-rod test.
- S06 `/Users/scottchu/Projects/personal/orca-slicer-mcp/docs/logs/2026-08-23-snapmaker-orca-u1-petg-print-pilot.md:13–18,89–102,130–153` attributes the request and physical handling to the user, but describes profile repair/file validation in passive voice. It does **not** support a named historical agent contribution. The exact logged physical result is completion followed by fit/mechanism-design failures; the log does not identify the failed interface.
- Related P13 observations (`EXPERIENCE.md:43–67`) record four caps fitting and two too tight on the same nominal rods, plus uncertain locking. They are not explicitly linked to the pilot's exact artifact. Do not present those cap dimensions/failures as the pilot's defect. A referenced physical photo is absent at its recorded `/tmp/codex-remote-attachments/.../3-Photo-3.jpg` path; no inspected photo is available from that pointer.

## Grounded schematic/visual pointers

- Wire error: S02 `/Users/scottchu/Projects/personal/design-projects/projects/xt60-bend-jig/docs/iterations/p20-r2-fixed-rod-arc-rail/HANDOFF.md:64–87` specifies intended vertical leg → tangent quarter arc → horizontal leg at 90°, against a shared END-derived diagonal assumption in source/tests. A labelled wire-path schematic may compare those relationships; it is not a regenerated production model. Correction is proposed, not completed in that record.
- Kage: S03 `/Users/scottchu/Projects/personal/design-projects/projects/kage/docs/legacy/source-docs/CONTINUATION_RESTART_2026-08-22.md:134–152` records pinions without shaft bores and approximately 33.301 mm³ shaft/hub intersection. A schematic solid gear crossed by a shaft depicts the missing bore; no measured printed geometry is implied. Restart coupons/one ring/one drive are proposed at **408–450**.
- D-shaft repair: the verified handoff above supports a D-shaped shaft and matching D-shaped holes in two plates, with the holes enlarged and shaft retained. A schematic may show that relationship, labelled as illustrative; avoid invented printed clearances or successful insertion.

No uncertainty blocks the actual collaboration case. Remaining limits: no proven successful repaired physical fit; no exact pilot-defect attribution; no fabricated conversation or missing-photo substitute. Next: R-I implements against these source facts; R-V checks the frozen presentation independently.
