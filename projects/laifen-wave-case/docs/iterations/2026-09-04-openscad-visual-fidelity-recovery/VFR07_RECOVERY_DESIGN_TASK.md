# VFR-07 syntax-first recovery design task

Status: ready after `inputs/VFR07_RECOVERY_DESIGN_INPUTS.sha256` is frozen.

Task ID: VFR-07-D. Owner role: independent recovery designer. VFR-06 is
closed as blocked under its nonrenewable budget. This new task must not rewrite
that history or treat the two parser failures as geometry evidence.

Design the smallest new implementation process that can translate the selected
VFR-06 periodic knot-lattice architecture into parser-valid OpenSCAD without
spending a geometry candidate attempt on basic syntax. Inspect both retained
failed source snapshots and exact diagnostics. Define a scratch-only staged
parser/type/shape preflight for every new helper, then a single atomic source
integration and the unchanged V06-1 through V06-3P geometry gates. The
preflight must use the pinned OpenSCAD WASM runtime and production-equivalent
source fragments; it may not generate or substitute host geometry.

Decide whether the retained attempt-2 source is a sound enough transcription to
repair through scratch preflight, or whether it must be regenerated from the
architecture. Specify exact allowed edits, executable preflight commands,
evidence, stop conditions, and one candidate plus one focused geometry repair
budget. Preserve B, all dimensions, thresholds, source authority, smooth path,
browser files and services. The sole write is `VFR07_RECOVERY_DESIGN.md`; do
not edit source, tests, artifacts, browser/UI, continuity or prior evidence.
