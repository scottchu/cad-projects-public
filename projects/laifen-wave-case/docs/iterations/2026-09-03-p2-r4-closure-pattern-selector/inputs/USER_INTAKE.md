# Frozen user intake — P2 R4 closure, pattern, and end-profile selector

The requested visual revision remains a generic two-piece cylindrical container with a configurable middle split and continuous outside diameter across that split. It must preserve the existing screw controls and add a closure selector:

- `screw_thread`: retain pitch, turns, lead/runout, form-height reference, and screw radial clearance.
- `bayonet_twist_lock`: add lock angle, lug count, axial capture/engagement, ramp rise, and bayonet radial clearance. The default demonstrates a quarter-turn while allowing generic wide/short forms.

Add the original `recessed_diamond` pattern. It must be mathematically generated on global theta/Z datums, remain periodic at constant pitch, preserve phase through the configurable split, accept depth and smooth keepouts, and be visibly distinct from the current positive blunt-diamond relief.

Add a parametric closed-end family: `flat`, `chamfer`, `rounded_fillet`, and `dome`. Expose linked or independent top/bottom sizing with `bottomEndSize` and `topEndSize`; their interpretation follows the selected family (chamfer distance, fillet radius, dome rise). Keep the circular cylinder cross-section and continuous OD at the middle seam. Only closed external ends may change. The current R7 1.20 mm chamfer is a migrated preset, not a CAD change.

Keep exactly two pieces, the Laifen and wide-short presets, mobile/accessibility behavior, visual-only honesty, deterministic pure math, invalid-state clearing, and true-scale/magnifier presentation. Do not copy reference geometry, modify P1 R7, make CAD/OpenSCAD/STEP/slicing/printing/MakerWorld claims, or change routes/services.

## Reference evidence only

`7CB9C9E6-5BFD-47BB-AEA4-F99DAAD380FC/1-Pasted-Image-1.jpg` shows a dark cylindrical container with a fine recessed-looking diamond field. It supplies only desired visual character; its topology, dimensions, closure, texture equations, and geometry are not imported.

`3198CBDD-768E-430F-839B-C52891705FEA/1-Pasted-Image-1.jpg` shows an external container reference with rounded/domed end proportions. It supplies only the idea that end shapes can vary; its geometry, dimensions, closure, drainage, and features are not imported.

`DF995206-7C70-46C7-8E81-13FE557711A9/1-Pasted-Image-1.jpg` is visual evidence only for the desire that a closed patterned seam can look phase-aligned. It imports no geometry, pattern field, thread, dimension, source, or claim of physical seam invisibility.

`219FCBFC-A54B-464B-B68D-E551554F8300/1-Pasted-Image-1.jpg` is visual evidence only for knitted-loop character. It does not import any character, mesh, texture, topology, or stitch geometry.

`6A8DD613-652A-4574-A606-889128C02803/1-Pasted-Image-1.jpg` is visual evidence only for a relief field that fades over a container. It does not import any container geometry, facet field, dimensions, or texture equations.

Add `matchPatternClosed` (default true). Upper open/manufactured phase must be precompensated by final closure rotation so the locked assembled seam matches in the visual field; the user can disable it for comparison. Show both open precompensation and locked residual honestly. This is not a physical seam-invisibility claim.

Add original `knit_stitch` using pure periodic global theta/Z loop math. Reuse `arc`, `axial`, and `depth` as stitch width, row height, and relief depth; add only `stitchTightness` (0…1) for row stagger/tightness. Keep it shallow, global-phase matched, visually support-oriented, and visual-only.

Add `patternEnvelope ∈ {full,fade_from_bottom,fade_from_top,center_band}`, `patternCoverage` (0…1), and `fadeMetric ∈ {depth,density}`. Repeats remain constant pitch: the envelope only multiplies amplitude (`depth`) or deterministically activates cells (`density`) with continuous smoothstep behavior, respecting existing end/thread/seam keepouts and closed-phase matching. Laifen remains `full`; wide-short may demonstrate bottom fade.

`A384434E-BC04-4CE3-AF5C-FF76E994AF4A/1-Pasted-Image-1.jpg` is visual evidence only for fine straight flute character and rounded end proportion. It does not import geometry, dimensions, lanyard hardware, thread topology, or texture mesh.

Add original `straight_micro_flutes` with adjustable angular count/pitch, duty/width, shared relief depth and existing envelope/fade. It uses global theta/Z and closure compensation. Preserve a uniform continuous maximum OD: no raised seam collar and no thicker thread zone. A rounded end may demonstrate the family. Do not infer or add lanyard hardware.

`730E4E64-8A3E-4D32-94FD-036BD46854AE/1-Pasted-Image-1.jpg` is visual evidence only for optional rugged/accessory character. It imports no geometry, clip, loop, hardware, dimensions, mesh, printability, or support claim.

Add optional `accessoryMode∈{none,integrated_lanyard_eyelet,captured_loop,separate_clip_link}`, `attachHalf∈{upper,lower}`, loop opening width/height, member thickness, and pivot/print clearance. Core container stays exactly two pieces; captured/separate modes are explicitly extra accessory body/part. Show any maximum envelope beyond nominal OD. Add original `rugged_hex` if implemented with global periodic math. Preserve no-collar core OD. Do not claim print-in-place, support-free, or physical behavior.
