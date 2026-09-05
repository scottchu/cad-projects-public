# P2 R5 exact cross-section contract

Baseline is R4 design fingerprint `8f99920f51096d8e51a17211917be5dc071b8d46481401618d692faf03660810`; R4 is superseded and must not be implemented. Start from the exact P2 R3 source/test hashes frozen in R4 inputs, after an inventory of any partial R4 edits. Only a newly frozen R5 candidate may proceed to independent gates.

## Pure section math

`OD` is maximum across-corners diameter and `R=OD/2`. For round, `support(theta)=R`. For polygon, with `n=sideCount`, `alpha=2*pi/n`, `beta=mod(theta-sectionRotation+alpha/2,alpha)-alpha/2`, and apothem `a=R*cos(pi/n)`, sharp support is `rSharp(theta)=a/cos(beta)`. `cornerRoundness=q∈[0,1]` blends no geometry beyond the same R: `support(theta)=(1-q)*rSharp(theta)+q*R`. This preserves `max_theta support=R`; across-corners is `2R=OD`; across-flats is `2a` before rounding and `min_theta 2*support(theta)` after rounding. Reject noninteger n, n<3/n>32, nonfinite q, rotation outside [0,360), nonpositive OD, and any derived invalid state.

Both pieces use exactly the same global `sectionRotation` and support. `sectionPhaseCompensation(mode,N,lockAngle,match)` equals `upperPhaseCompensation(match,closureRotation(...))`; assembled upper local angle is transformed by final closure rotation before support/pattern evaluation. Thus `supportUpperLocked(theta)=supportLower(theta)` and the existing R4 global pattern field obeys the same closed seam equation. Off matching exposes the open/precompensated relationship but may not make core shapes misalign in locked state: shape frame is always mechanically aligned in the visual model; match only affects pattern field.

Core max envelope is always `OD`. Accessory envelope is `max(OD, accessoryMaxEnvelope)` and must be shown alongside across-flats/corners for polygon mode. Camera fitting uses the actual visual bounding box including enabled accessory, not nominal OD alone. Pattern relief stays within the core support radius, never creates a collar, and global end/thread/seam keepouts remain unchanged.

## Required tests

- round support is R for sampled theta; triangle, pentagon, hexagon and octagon have corners R and stated across-flats; rotations change angular location but not envelopes; q=0/1 endpoints are exact and q changes support monotonically toward R.
- all named preset sides 3…8, plus upper bound 32, pass valid domain; invalid side/roundness/rotation clears preview.
- same global theta/z at seam yields section alignment and R4 pattern equality for screw turns 1/2/3 and valid bayonet angles with matching on; closed shape alignment remains true when matching off.
- accessory enabled/disabled reports envelope and visual extra-body semantics; core remains exactly lower/upper groups and has no raised seam/thicker thread band.
- browser snapshots cover round, triangle, pentagon, hexagon, octagon, rotated rounded polygon, Laifen and wide-short modes, accessible errors, mobile framing and magnifier honesty.

No equation above describes BREP, actual clearance, printable wall, support-free manufacturing, real closure, or physical fit.

Add `flowing_flutes`, distinct from `straight_micro_flutes`. Reuse `fluteCount`, `fluteDuty`, and `depth`; add `fluteWaveAmplitude∈[0,pi/fluteCount)` and `fluteWaveWavelength>0`, with `fluteWavePhase∈[0,2*pi)` and `fluteWaveDirection∈{-1,1}`. Let global `v=(z-zPhase)/fluteWaveWavelength`, displaced angular centerline `delta(z)=direction*amplitude*sin(2*pi*v+phase)`, and `w=fract(fluteCount*(theta-theta0-delta(z))/(2*pi))`. The groove is `-depth*smootherstep((fluteDuty-w)/fluteDuty)` when `w<fluteDuty`, else zero, before common global keepout/envelope/upper-phase compensation. The axial wavelength is an explicit physical parameter: H changes repeat count or partial repeat but never Z-scales a finished texture. Tests sample theta periodicity, z+wavelength periodicity, seam equality under screw/bayonet matching, and independent sensitivity to count/duty/depth/amplitude/wavelength/phase/direction. The reference is never copied.
