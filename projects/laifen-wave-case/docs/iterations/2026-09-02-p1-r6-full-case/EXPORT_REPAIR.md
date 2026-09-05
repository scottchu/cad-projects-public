# IMP-R6-02 export/parity diagnosis

Owner `/root/case39_impl`, implementation/diagnosis role. Status: source topology cause localized; no correction approved or applied. Candidate135 remains immutable, SHA256 `4c2750ad632639be5547074173408aa14dfc579faed8d45890ed7233b00c0351`. All135 path/content pairs were verified at entry and after the first full source/written comparison. Only this receipt and `scratch/fullcase-export-repair/` were written. No source, official STEP, validator evidence, tool environment, service, Git or printer change occurred.

## Finding and cause

The cap parity failure is a tolerance-covered source trim inconsistency at the female thread's upper runout, near z9. It is not located in the long diamond skin or closed floor. In the exact source cap, the shared edge of zero-based faces656 (thread BSpline flank) and657 (runout cone) ends at `(-16.15941564536269,5.744195853242431,9)`, while its own stored topological endpoint vertex is `(-16.1585575799622,5.74660916846158,9)`. The source vertex tolerance is0.00256132140603368mm, covering the approximately0.00256132mm tangential discrepancy. This explains why generic BREP validity passes despite unstable trim/vertex consistency.

STEP preserves that topological vertex's coordinates to rounding precision but moves the curve-trim endpoint to `(-16.15855755521607,5.7466091596606725,8.999999947476617)`. The shared edge length changes2.2267686603034575 to2.224207339049452mm; its topological vertex tolerance falls to0.0000339391330147004mm. The source/written underlying flank surface agrees to7.8574e-12mm in the bounded same-UV probe. The two faces retain9 and4 edges respectively. This is trim normalization around a nearly tangential Boolean intersection, with a geometric boundary change; calling it only decimal rounding or integration noise would be unsupported.

The local inspection identifies the changed representation, but does not establish whether the normalization occurs in STEP writer transfer or reader shape healing. That distinction does not remove the source inconsistency or justify changing the parity limit.

## Discriminating evidence

1. Reproduced conventional adaptive Gauss at eps1e-10: source35022.73685038005 versus written35022.740655030386mm3, delta0.003804650332313031mm3. Error estimates about1.0175e-10 relative. Gate remains<=0.001mm3 and fails.
2. Gauss–Kronrod with explicit spline spans at eps1e-8: source35022.736859017554 versus written35022.74067033322mm3, delta0.0038113156697363593mm3. Thus an alternative exact-surface integration method does not resolve the discrepancy.
3. Paired all6593 faces one-to-one by bounding coordinates for contribution localization. A common-origin surface-integral comparison attributes0.0037885730756670455mm3 to face656 and0.000010635079327414587mm3 to adjacent cone657. Exterior skin/end-plane contribution differences are around1e-8mm3. This localization is not a replacement absolute-volume acceptance method: its common-origin totals differ from whole-solid integrals, while paired deltas independently identify the offending faces.
4. One targeted scratch export with `write_pcurves=False` and unchanged default precision remains valid/one solid but gives35022.74065234835mm3 and delta0.0038019683124730363mm3. Omitting pcurves is not a fix. No speculative precision sweep was run.
5. Focused shared-edge 3D/pcurve/vertex probes establish the source endpoint-to-vertex mismatch and its STEP normalization above. Source shared-edge tolerance5e-6 becomes1e-7; the much larger source endpoint-vertex tolerance is the relevant hidden inconsistency.

## Commands and scratch evidence

All Python commands ran through root uv Python3.12, with no official files changed:

```sh
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/diagnose_gk.py
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/localize.py
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/no_pcurves.py
uv run python projects/laifen-wave-case/scratch/fullcase-export-repair/trim_probe.py
```

The first command was run under an outer root-Python subprocess timeout420s; it completed65.160s internally. Localization completed4.069s; the scratch no-pcurve export/reimport completed7.023s. Localize's first launch hit a diagnostic binding error (`Shape.cast` returnedNone); selecting its existing single solid through TopExp resolved that helper issue without changing any geometry. Bounding-pair, edge-length and topological-vertex summaries were produced by root `uv run python` inline reads of the saved BREP files.

Canonical evidence: `scratch/fullcase-export-repair/{gk.json,diagnose.log,localized.json,paired.json,no-pcurves.json,trim-probe.json,edge-counts.json,vertex-probe.json}`. `source.brep` and `written.brep` are exact scratch caches from the initial comparison. `cap-no-pcurves.step` is a failed diagnostic alternative, never a replacement or release artifact. The corrected `vertex-probe.json` uses `BRep_Tool.Pnt_s`; a transient initial probe read object placement rather than vertex geometry and was corrected before interpreting coordinates.

## Proposed smallest correction and next gate

Root should authorize a bounded source-native normalization/rebuild of the female upper-runout trim so its 3D curve endpoint, pcurve trim and topological vertex agree before the cap is measured or exported. Target the identified near-z9 edge/Boolean boundary, keeping the selected root/crest, lead/runout equations, collar/taper, bores, exterior and floors unchanged. Merely reducing tolerance metadata is not a repair; nor is changing the0.001mm3 gate. Avoid a global all-face repair or a parameter/skin redesign.

The next diagnostic should first try a focused native edge/wire consistency operation in scratch, compare endpoint-to-vertex residuals and actual interface laws, then export/reimport it with unchanged normal settings and rerun conventional and GK parity. A scratch canonical STEP roundtrip may serve as a comparison baseline for the normalization, but has not been tested as a production strategy. If local native normalization cannot be made stable, revisit the redundant female-thread trimming-tool termination as a separately evidenced construction repair; do not silently move functional datums.

No successful repair is claimed here. After a demonstrated minimal correction, root must authorize source/candidate changes, regenerate affected official targets, freeze a new fingerprint and request independent validator/critic/formal review. Physical fit, source/STEP acceptance and the existing CAD uncertainty remain separate. All previously passing gates are evidence for the frozen candidate only.
