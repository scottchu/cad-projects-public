# P17-D14 task DAG

| ID | Role | Dependency | Deliverable | Status |
|---|---|---|---|---|
| D14-01 | mechanism designer | frozen I08/I10 and rejected D13 | joint `C,D` equations and hard-contact reduction | complete |
| D14-02 | mechanism designer | D14-01 | bounded deterministic rail search and analytic web gate | complete: infeasible |
| D14-03 | user decision | D14-02 | choose which frozen invariant may reopen | blocked pending user |
| I14 | implementation | accepted feasible D14 contract | source/tests/CAD | not dependency-ready |

Retry ceiling used: initial bounded search plus one focused numerical refinement. No architecture search or implementation was started.
