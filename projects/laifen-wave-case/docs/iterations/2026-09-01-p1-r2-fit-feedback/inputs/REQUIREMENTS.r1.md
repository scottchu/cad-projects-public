# Requirements
All dimensions mm. Values below are user targets/placeholders, not measured toothbrush dimensions. No downloaded mesh is an authoritative input.
| ID | Requirement and classification |
|---|---|
| REQ-01 | Invariant: original build123d parametric two-piece Laifen Wave case; never copy downloaded case mesh. |
| REQ-02 | Physical unknown: verify installed-head overall L and maximum diameter D; provisional L=208, D=29; both editable. |
| REQ-03 | Derived: usable closed cavity C=L+5 initially 213; ID=D+2.5..3 initially 32; after full engagement >=3 total axial and >=1 radial clearance. |
| REQ-04 | Invariant: toothbrush never acts as closure stop; positive external shoulder. Literal prevention of contact with EITHER internal end remains unresolved, not waived. |
| REQ-05 | Approximate targets: long lower/short upper cavity 137+81-overlap5=213; OD approximately <=39, nominal wall2.4, closed-end floor3, support-free drains. |
| REQ-06 | Original FDM screw: pitch2, effective engagement5..6, initial radial thread gap0.25 per side; representative 0.20/0.25/0.30 coupons before full print. |
| REQ-07 | Smooth threads/shoulder; thread-start elephant-foot relief; effective engagement excludes nonfunctional lead/runout regions. |
| REQ-08 | Constant axial texture pitch with derived repeat count and phase matched across assembled parts; never Z-scale. Smooth zones >=2 near thread, shoulder, floor and openings. |
| REQ-09 | Shallow flutes/waves/diamonds, depth <=0.6..0.8 and residual wall >=1.8 in texture zone. Thread-root minimum1.8 is a DESIGN ASSUMPTION, not a stated user constraint. |
| REQ-10 | Print both parts vertically, openings up, U1 PLA, nozzle0.4, layers0.2, supports off, intended unsupported overhang <=45 degrees. |
| REQ-11 | Later deliver original source, named joints/datums, STEP body/cap/coupons/assembly; validate STEP before STL/3MF; show section, device envelope, closed length, overlap and end clearances. |
| REQ-12 | Named parameters: L,D,axial/radial clearance,wall,thread clearance,texture pitch; derive dependent dimensions. |
| REQ-13 | Physical acceptance: coupon fit/no wobble, five empty screw cycles, full engagement with brush, >=3 total axial and >=1 radial clearance, no visible texture discontinuity; both parts slice support-free. |
| REQ-14 | Current gate only: measured dimensions and explicit user relationship confirmation precede full CAD; preview/source/artifact/physical evidence remain separate. |
Non-goals now: mesh imitation, full case architecture approval, source solids, exports, slicing, upload/start and physical acceptance. Future topology/support choices remain unresolved.
