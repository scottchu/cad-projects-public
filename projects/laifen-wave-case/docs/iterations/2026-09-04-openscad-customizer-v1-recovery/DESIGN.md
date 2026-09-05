# OSC-05 recovery design contract

## Fixed contract

The existing OpenSCAD source and UI contract remain authoritative: OD39; body/cap bores30/31; device L208; allowance5; cavity213; closed219; body/cap144/84; floor3; pitch2; 3 turns; engagement6; clearance/side0.25; thread depth/height0.5; end chamfer1.2; diamond pitches4.8/3.63, depth0.45; seven drains; and the existing split, drainage, surface, and output selectors. The source path and all visible parameter names/defaults remain unchanged.

## Smallest geometry correction

Introduce one named internal constant `THREAD_EMBED_EPS` (implementation-selected small positive value, bounded by the existing wall and clearance assertions). The male ridge polygon's root vertices must be placed at `thread_root_radius-THREAD_EMBED_EPS`, so its base overlaps the body root cylinder instead of merely touching it. The female groove profile must use the same constructive overlap convention against its root-clearance cylinder, with the epsilon directed into the tool volume. The correction must preserve the helix centreline, pitch, 6 mm active interval, 1.5 mm transitions, 0.25 mm radial clearance, and minimum threaded-cap wall 1.8 mm. It must not substitute a larger clearance cylinder or swallow the female helix.

The round and smooth shell profiles must use `outer_radius` as their exterior radius; `valley_radius` is only for diamond valleys. Body and cap cavities remain closed-floor shells with the positive external shoulder as the closure stop. Diamond grooves retain the shared global-Z phase and existing 2 mm functional keepouts. Compile slices/fragment counts must be bounded by the practical ceiling recorded by implementation; no uncontrolled increase in `$fn`, twist slices, or groove count is authorized.

## Required implementation and evidence gates

Implementation may change only the SCAD geometry source, its focused regression test, and recovery evidence. Add pure deterministic checks for default dimensions, split round-trip, thread interval/epsilon bounds, wall and clearance inequalities, exact OD in round/smooth, seven-drain selection, and phase equality at the seam. Native OpenSCAD CLI gates must compile default round, smooth, and diamond body/cap/assembled outputs to temporary STL, then validate positive volume, manifold/watertight status, expected solid count, bounds, and no unexpected disconnected components. A practical compile-time ceiling and command duration must be recorded. Snapshots must show default smooth assembled/body/cap and default diamond body/cap, with one changed-and-reset control trace.

Acceptance is blocked if any default output is zero-volume, non-manifold, disconnected unexpectedly, changes a visible default, violates the 1.8 mm wall/0.25 mm clearance contract, or exceeds the declared compile ceiling. Slicer, printer, fit, strength, and physical acceptance remain outside this recovery.
