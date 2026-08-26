# P17-C09 independent blocked-design critique

Status: critic agrees this design is blocked. No P17-I09 implementation contract
should start from the D11/R1/R2 evidence. This review is source/CAD read-only
except for this file.

Verified input:

- Checkout: `/Users/scottchu/Projects/personal/design-projects`
- Branch: `codex/xt60-p17-r2-outer-force-balance`
- Manifest: `projects/xt60-bend-jig/docs/iterations/p17-r2-outer-force-balance/IMPLEMENTATION_INPUT_MANIFEST.sha256`
- Manifest SHA-256:
  `df315421f41c0fe4378f3d7715ca6ddcdb6074477db8a4d497b292f54bc66330`
- Manifest entries: 15/15 matched before critique.

## Severity findings

### Blocker: no currently authorized outer-only implementation path

The user-visible defect is real, and the D11 repair space does not produce an
implementable candidate. The baseline end rods have poor useful-normal geometry:
Rod 1 / `bottom` reaches a right-side END crossing of `5.05 deg` and Rod 2 /
`upright` reaches a left-side END crossing of `4.45 deg`, while the middle
`diagonal` rod is much better balanced (`21.43/29.99 deg`). This is documented
in `DEFECT_INPUT.md:33` and reproduced by the D11 baseline table in
`DESIGN.md:51`.

D11 then shows the core failure mode: force-balanced laws can be found, but the
same rail paths cut away required local support. The strongest first frontier
passes the balance metrics but fails actual motion/guide/support with
`0.014479844 mm3` unintended intersection and failed two-sided support
(`DESIGN.md:77`). R1 improves force/web/collision/service but still has
`minimum outer endpoint material ratio = 0.0` and fails normal-side,
endpoint-probe and continuous-strip gates (`DESIGN.md:122`, `DESIGN.md:142`).
R2 finds `1,785` force-pass candidates and two shortlists that pass force/web
and, for shortlist A, collision/service/conditioning; both still fail the
support gate with endpoint material ratio `0.0` (`DESIGN.md:174`,
`DESIGN.md:180`, `DESIGN.md:198`). The handoff correctly records final stop at
`HANDOFF.md:41`.

Disposition: blocker. Do not implement either D11, R1, or R2 candidates. The
failure is not a missing test count; it is an actual geometry contradiction
between balanced through-slot rails and the mandatory local reaction material.

### Blocker: the `0.30 mm` support gate is credible and should not be weakened
without physical evidence

The support gate checks for continuous material beside the slot boundary, not
extra cosmetic plate diameter. Prior D10 made this explicit: material must exist
at slot radius plus `0.30 mm` on both normals, through exact OPEN/contact/END
and 65 states; any void or self-return cavity reopens design
(`../p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:148`). The actual
test code samples 61 offsets from the swept-slot boundary through `+0.30 mm` and
requires `continuousFromSweptBoundaryThroughPlus0p30`
(`tests/test_p17_r2_direct_counter_twist.py:177`).

Mechanically, that is a credible rod-wobble/reaction-path gate for a through
slot carrying hand force through a 4 mm rod in a 4.15 mm guide. If one side of
the local support strip is absent, the rod can bear on a one-sided wall, tip
across clearance, or load a thin/lipped edge. The D11 failures are also not
borderline: R1/R2 report material ratio `0.0`, not a slightly thin wall. D11-R1
specifically explains that the failing probes fall into another portion of the
rail cutter, not beyond the disk perimeter (`DESIGN.md:142`). D11-R2 confirms
the same mechanism and reports only `0.040087 mm` swept-boundary recession for
shortlist B, so the decisive void is internal self-removal rather than outside
diameter (`DESIGN.md:207`).

Disposition: blocker if someone proposes to waive support. The gate may be
changed only by a new physical/mechanical argument and likely a printed
experiment; the current digital evidence does not justify weakening it.

### Major: diameter/profile growth alone is already disproven

R1 proves the balanced candidate's derived circular diameter for `2.20 mm` radial
web is only `73.301702 mm`, already less than existing `82/85 mm` outer plates
(`DESIGN.md:137`). Because the lost material is removed internally by the swept
slot, increasing a shared or independent outer diameter cannot restore the
missing `+0.30 mm` local strip (`DESIGN.md:142`). This rules out the simplest
reading of "outer plate envelope/profile" as merely making the plate bigger.

Disposition: major. Future work should not spend another cycle on diameter-only
or broad outline growth unless it includes a new mechanism for preserving local
slot-wall material.

### Major: force angle is a valid diagnostic, but not a physical force claim

D11's force-balance criterion is mechanically coherent as a geometric diagnostic:
the angle is between the fixed straight-track direction and outer-slot tangent;
`sin(phi)` approximates useful normal component and `1/sin(phi)` is a diagnostic
multiplier (`DEFECT_INPUT.md:28`, `DESIGN.md:21`). It correctly catches the
defect that D10's coupled-rank acceptance did not prove useful force
transmission. It also stays within the physical boundary by not claiming measured
hand force, friction, compliance, or PETG behavior (`DESIGN.md:46`).

Disposition: major evidence boundary to preserve. Do not convert the diagnostic
into a force/torque acceptance claim without physical measurement.

## Smallest safe reopening

The single smallest safe design variable to reopen next is **outer-plate rail
topology/section**, not outer diameter/profile alone.

Rationale:

1. A through-slot centerline whose swept cutter returns near its own endpoint
   necessarily removes material where the support strip wants it. The critic's
   independent analytic proximity check found the same pattern for the D11
   candidates: R1, R2-A, and R2-B produce local support-strip points that fall
   within one slot radius of another sample of the same rod rail, while the D10
   baseline does not show that proxy failure. This matches D11's actual-solid
   result that the failure is internal swept-path removal.
2. Plate diameter/profile growth cannot fill a hole already cut by the rail.
   D11-R1 already proves the candidate fits radially inside the existing outer
   diameters (`DESIGN.md:137`), so outline growth is not the missing variable.
3. Small movement of OPEN/contact/END rod centers may be the next plausible
   mechanical escape if rail topology is not allowed, but it is no longer
   "focus only outer": it changes user-visible rod states, contact/preload
   geometry and probably wire forming assumptions.
4. Small change to fixed-inner straight-track directions is larger, not smaller,
   because the direct fixed tracks are defined by the same frozen rod states and
   are part of the fixed inner reaction path. Changing them reopens inner plates
   and rod motion, not just outer plates.
5. A new follower/part is the most invasive option. It may eventually be
   mechanically clean, but it violates the current no-added-part/no-added-
   mechanism constraint and should not be the next smallest step.

Boundary: if "outer-only" means only changing the existing outer plates, then a
rail topology/section change can still be outer-local in physical location. If
"outer-only" also means the same single through-slot topology, no added
structure, no section/layer trick, no rod-state movement, and no follower
change, then no option remains inside that scope.

## Commands and results

- `git branch --show-current`:
  `codex/xt60-p17-r2-outer-force-balance`
- SHA verification of `IMPLEMENTATION_INPUT_MANIFEST.sha256`: file SHA
  `df315421f41c0fe4378f3d7715ca6ddcdb6074477db8a4d497b292f54bc66330`;
  `entry_count 15`; `failures 0`.
- Inspected user reference images:
  `/Users/scottchu/.codex/attachments/210908bc-9de2-4c43-aedb-8a18d5f90b6a/codex-clipboard-7eb2821f-aa8a-4869-aee0-cbd022b72eac.png`
  and
  `/Users/scottchu/.codex/attachments/e18aec55-2c27-4dce-b652-517697dc7c13/Screenshot 2026-08-25 at 9.57.36 AM.png`.
  They support the stated visual defect: end rods have visibly asymmetric
  shallow/long versus short/steep outer rails, middle rod is the qualitative
  balance reference.
- Independent `uv run --project projects/xt60-bend-jig python` analytic check:
  baseline minimum contact-to-END angle `4.4518 deg`; R1 candidate minimum
  `25.1682 deg`, worst multiplier ratio `1.4744`, worst path ratio `1.4292`;
  R2-A minimum `18.2337 deg`, worst multiplier ratio `1.3702`, worst path ratio
  `1.4230`; R2-B minimum `20.6473 deg`, worst multiplier ratio `1.4980`, worst
  path ratio `1.4881`. A simple same-rail proximity proxy found internal
  support-risk hits for R1/R2 but not the D10 baseline.
- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`
  was interrupted after exceeding the bounded critic window. Initial progress
  reached `.....`; the interrupt occurred inside
  `two_sided_support_evidence()` continuous strip `is_inside` checks. This is
  reported as an interrupted check, not a pass or fail.

## Physical boundary

This critique accepts neither force nor print behavior. It only concludes that
the blocked digital design result is mechanically coherent. Real friction,
hand torque, PETG compliance, wear, cap retention, wire stiffness, insulation
damage, heat, and cooled bend angle remain unproven physical gates.

## Disposition

P17-C09 critic disposition: **BLOCKED**. No implementation candidate is ready.
Next action is a new user/root design authorization that either:

1. reopens outer-plate rail topology/section as an outer-local but architecture-
   relevant variable, while retaining force/web/support/collision gates; or
2. explicitly leaves outer-only scope and reopens small rod-state/path changes.

Do not weaken the `0.30 mm` support gate or implement a D11/R1/R2 candidate.
