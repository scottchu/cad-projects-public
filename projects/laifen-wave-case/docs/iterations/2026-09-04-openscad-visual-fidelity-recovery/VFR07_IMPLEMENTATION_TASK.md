# VFR-07 implementation task

Status: ready after `inputs/VFR07_IMPLEMENTATION_INPUTS.sha256` is frozen.

Task ID: VFR-07-I. Owner role: sole syntax-first recovery implementer. Follow
`VFR07_RECOVERY_DESIGN.md` exactly. Repair and validate the retained VFR-06
attempt only in scratch through its full-file parse, cumulative helper
type/shape, and source-emitted array preflights. Scratch preflight failures do
not create a candidate and may be corrected only inside the frozen VFR-06
architecture. Integrate into authoritative source atomically only after every
preflight passes.

After integration, run the unchanged V06-1 through V06-3P geometry gates. The
budget is one authoritative candidate C1 plus one focused geometry repair. A C1
gate failure or timeout consumes the candidate; a second failed candidate stops
the task. Parser/type/shape defects must be exhausted before C1 and cannot be
fixed after integration as an uncounted attempt.

Exclusive writes:

- `openscad/laifen_case_customizer_v1.scad`
- focused implementation assertions in `tests/test_openscad_customizer.py`
  and at most one new focused VFR-07 test
- new evidence under `scratch/vfr07-implementation/`
- passing artifacts under `openscad/generated_vfr07/`
- `VFR07_IMPLEMENTATION.md`

All browser/UI/worker/vendor/runtime/lock files, Python oracle, prior evidence,
continuity, build123d/STEP, slicer, service and printer namespaces are read
only. Do not enable Diamond or deploy. Restore frozen source/tests after a
second candidate failure. The receipt must bind exact commands, timings,
topology/error/protected-geometry results and hashes. The implementer cannot
approve its own result.
