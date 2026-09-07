# Pattern performance brief — PERF-DES

Baseline commit `7f15b1649a5d83c77512c9ba0864943ac68996b6`; authoritative
`openscad/laifen_case_customizer_v1.scad` SHA
`3b96cc2d5a5100e2daa2fe5a14c21e510728f108cfbc9afd5ae80bf1ef5dde40`.
The 39 paths in `inputs/baseline.sha256` verified before profiling; manifest SHA
`cb29435ee9074f3e5e87685cce25a5aad6117289a769195765bde5b93cd34e48`.

The user reports slow Rings/Spiral and requests optimization of the mathematics
for every pattern. Audit Smooth, Diamond, Ribs, Rings and Spiral, then spend
implementation effort on measured costs. Existing parameter behavior and visual
quality are invariants; the earlier revolve/twist suggestion is an alternative,
not an approved algorithm. There are no new physical dimensions or fit findings.

| ID | Class | Required outcome |
| --- | --- | --- |
| PERF-01 | Invariant | Audit all five source paths with the same pinned runtime and default tuple; distinguish fresh measurements from historical timings. |
| PERF-02 | Invariant | First candidate changes evaluation/representation work only; retain exact original output bytes, primitive/face order, winding, phase, clipping, samples and guards. |
| PERF-03 | Invariant | Preserve all internals, chamfers, drains/count, four output transforms and control semantics, including exact values, allowed limits and explicit Generate/current-only Download. |
| PERF-04 | Derived | Demonstrate paired performance improvement using DESIGN's benchmark, with initialization, callMain, output read and compiler-reported render time separated. |
| PERF-05 | Invariant | Retain source/lock/full job identity, cancellation and stale-result protection; no worker, engine, dependency or live build mutation in the first candidate. |
| PERF-06 | Physical unknown | Runtime and STL success do not establish STEP, slicing, grip, fit, strength or physical acceptance. |

All dimensions remain mm and the existing shared global-Z seam is unchanged.
No artifact may be repaired by editing STL. No new UI controls, service settings,
Tailscale/8448, public hosting, printer action or main merge belongs to this task.
Private 8453 remains on the delivered R2 build until independent review/delivery.

## Frozen task contracts

| ID / role | Dependency and done gate | Exclusive writes / evidence |
| --- | --- | --- |
| PERF-DES / design | Baseline39 verified; all-five audit and bounded optimization/benchmark contract frozen. | This BRIEF/DESIGN and `/tmp/pattern-performance-design`; receipt with hashes and stage timings. |
| PERF-IMP / implementation | Frozen design; exact-output candidate and reproducible paired benchmark receipt. | Declared SCAD/helpers/focused tests only; root freezes exact write manifest before dispatch. |
| PERF-VAL / validator | Frozen candidate; independent paired timing, parity and meaningful geometry/state regressions pass. | Validator-only tests and validation receipt/scratch. |
| PERF-CRIT / critic | Frozen candidate; inspect correctness/performance claims, numerical operation preservation and remaining risks. | Critique receipt only; no implementation writes. |
| PERF-REV / formal review | Validator+critic pass against the same candidate; resolve evidence/manifest join. | Review receipt only. |
| PERF-DEL / delivery | Formal approval; build, six served-file parity and one current live generation/download. | Authorized build/deployment evidence only; root coordinates. |

DAG: `DES -> IMP -> (VAL || CRIT) -> REV -> DEL`. Design owner is
`/root/pattern_family_design`; implementation workstream is
`/root/pattern_direct_implementation`. Root freezes the remaining distinct owner
identities and each task's exact immutable input/write manifest in HANDOFF before
dispatch. No implementer may approve its own candidate. At most three workers,
one source writer, and one active timed benchmark process; no concurrent load
from CAD/browser renders during performance comparisons.

Qualitative model ceilings: strong/high design, critique and acceptance;
balanced/medium prescribed implementation; deterministic inventory may use fast/low.
Design checkpoint8min/ceiling15min; downstream tasks checkpoint5min/ceiling20min
unless root records a justified extension. Initial attempt plus two focused
repairs maximum; reopen scope on byte mismatch, noisy timing, numerical drift,
unmet target or exhausted repairs. No density reduction follows automatically.

Mutable scheduling, task progress, candidate manifests and delivery status live
in HANDOFF/PROJECT_STATE/NEXT_AGENT, outside this frozen design input. Every
receipt states owner, exact hashes, commands/results, severity, requirement
coverage, unresolved risks and next action; retain compact evidence, not diaries.
