# Requirements
All dimensions mm. Values below are user targets/placeholders, not measured toothbrush dimensions. Downloaded mesh measurements are diagnostic references only; downloaded geometry must never be copied or modified into the original new design. Current fit revision: DEC-05 / P1 R2. Previous requirements are preserved in iterations/2026-09-01-p1-r2-fit-feedback/inputs/REQUIREMENTS.r1.md.
| ID | Requirement and classification |
|---|---|
| REQ-01 | Invariant: original build123d parametric two-piece Laifen Wave case; never copy downloaded case mesh. |
| REQ-02 | Physical unknown: verify installed-head overall L and maximum diameter D; provisional L=208, D=29; both editable. |
| REQ-03 | Derived: usable closed cavity C=L+5 initially 213; after full engagement >=3 total axial clearance. P1 R2 accepted width preference: retain nominal lower bore30 / upper bore31; D edits do not resize bores. Nominal per-side gaps (30-D)/2 and (31-D)/2 are readouts, not measured printed clearances. Prior ID32 / >=1 radial target is superseded by DEC-05; actual fit remains pending. |
| REQ-04 | Invariant: toothbrush never acts as closure stop; positive external shoulder. Literal prevention of contact with EITHER internal end remains unresolved, not waived. |
| REQ-05 | Approximate targets: long lower/short upper cavity 137+81-overlap5=213; OD approximately <=39, nominal wall2.4, closed-end floor3, support-free drains. |
| REQ-06 | Original FDM screw: pitch2, effective engagement5..6, initial radial thread gap0.25 per side; representative 0.20/0.25/0.30 coupons before full print. |
| REQ-07 | Smooth threads/shoulder; thread-start elephant-foot relief; effective engagement excludes nonfunctional lead/runout regions. |
| REQ-08 | Constant axial texture pitch with derived repeat count and phase matched across assembled parts; never Z-scale. Smooth zones >=2 near thread, shoulder, floor and openings. |
| REQ-09 | Shallow flutes/waves/diamonds, depth <=0.6..0.8 and residual wall >=1.8 in texture zone. Thread-root minimum1.8 is a DESIGN ASSUMPTION, not a stated user constraint. |
| REQ-10 | Print both parts vertically, openings up, U1 PLA, nozzle0.4, layers0.2, supports off, intended unsupported overhang <=45 degrees. |
| REQ-11 | Later deliver original source, named joints/datums, STEP body/cap/coupons/assembly; validate STEP before STL/3MF; show section, device envelope, closed length, overlap and end clearances. |
| REQ-12 | Named parameters for future full CAD: L,D,axial/radial clearance,wall,thread clearance,texture pitch; derive dependent dimensions. Current P1 R2 preview locks accepted reference bores30/31 and derives radial gaps from D; it does not implement or waive later radial-fit parameterization. |
| REQ-13 | Physical acceptance: coupon fit/no wobble, five empty screw cycles, full engagement with brush, >=3 total axial clearance and physically confirmed original-width fit without binding, no visible texture discontinuity; both parts slice support-free. |
| REQ-14 | Current gate only: measured dimensions and explicit user relationship confirmation precede full CAD; preview/source/artifact/physical evidence remain separate. |
Non-goals now: mesh imitation, full case architecture approval, source solids, exports, slicing, upload/start and physical acceptance. Future topology/support choices remain unresolved.
