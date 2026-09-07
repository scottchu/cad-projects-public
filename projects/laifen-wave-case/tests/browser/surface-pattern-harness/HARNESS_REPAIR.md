# Superseded-result observation repair

Candidate 03 product source is unchanged. This repair affects only the
validator-owned browser harness.

The first root-owned replay proved the cancel gate and genuine payload checks,
but the superseded-result gate reported `loading…` before delivery and
`parsing…` afterward. The protected result state remained unchanged: no current
preview, download URL, viewer install, render hash, Blob, or Blob hash appeared.
The event timeline showed Worker 3 started after Worker 2 was terminated, then
produced and held its genuine result before Worker 2 was delivered late.

The failure was an observation-window defect. The harness stored its comparison
snapshot when Worker 3 was created. Genuine Worker 3 progress could therefore
change status while its pinned OpenSCAD compilation ran, before the stale Worker
2 result was delivered. Status progress was incorrectly attributed to stale
delivery.

The repaired gate first requires Worker 3's genuine result to be held, then
captures the complete status/render/Blob/download snapshot immediately before
delivering Worker 2. It compares again after delivery using the existing exact
equality check. The fixed pattern tuple checks, result request identity checks,
nonempty byte check, and accepted held/view/Blob SHA-256 identity check are
unchanged.

`HARNESS_INPUTS.sha256` is preserved as the provenance of the first replay.
`HARNESS_INPUTS-02.sha256` binds this repair and the frozen Candidate 03 inputs.
Local validation covers manifest integrity and JavaScript syntax. Browser replay
remains root-owned and is required before the repaired supersession gate can be
reported as passing.
