# P17-D11 handoff

## Design role `/root/three_rod_design`

Status: **BLOCKED / STOP P17-I09**.

Verified baseline `8adfb20f352e36cede54a3414307ced3de81c2b8` on branch
`codex/xt60-p17-r2-outer-force-balance`. Every row of
`INPUT_MANIFEST.sha256` matched; its file SHA-256 is
`0281978fbc5c3a41d9eb1f26ca7fd3861535437ba417052bf4f20c91b6ab75fc`.

The defect is reproduced and common-`C`-only repair is analytically
infeasible within the necessary frozen plate/axle envelope. Equal/opposite
nonlinear motion can satisfy the new geometric balance thresholds, but the
best fully evaluated frontier fails actual plate-guide collision and
two-sided-support gates. `DESIGN.md` contains equations, thresholds, exact
numbers and rejected candidates.

No source, test, CAD artifact, requirement, experience, project state or git
state was changed. The next action is a new bounded design decision from the
root/user on reopening one outer envelope variable. Do not implement the
rejected frontier and do not weaken collision, web or support thresholds.

The implementation manifest records exact inputs for provenance only. Its
blocked handoff status supersedes the normal P17-I09 dependency.

## P17-D11-R1 outer-envelope repair receipt

Status remains **BLOCKED / STOP P17-I09**. Candidate `C=(-0.5,21.0)`,
`beta=24[0.30u+0.70u^12]` passes force, web, actual collision, guide,
conditioning and service gates, but fails continuous `0.30 mm` two-sided
support because the swept rail internally removes the probe material. Its
derived required diameter is only `73.301702 mm`, below both existing outer
diameters, proving shared or independent plate growth cannot fix the failure.
No source/test/artifact change is authorized.

Next action requires explicit reopening of rail topology/motion family while
keeping the product architecture and world states, or an explicit change to
the support requirement. Neither is within R1.

## P17-D11-R2 final receipt

Status: **BLOCKED / FINAL STOP P17-I09**. The authorized two-segment monotone
`C1` family produced `1,785` force-pass candidates. Full shortlist A
`C=(1,23), h=0.10, p=240, m0=12.631578947` passes force, web, collision,
guide, service and conditioning gates but has outer endpoint material ratio
`0.0` and fails continuous two-sided support. Smoother shortlist B
`C=(1,22), h=0.20, p=200, m0=4.444444444` also passes force/web and fails the
same support gate. Final repair ceiling is exhausted; do not implement either
candidate or continue unapproved search.
