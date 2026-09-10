# P20 R1 fixed-rod reset independent design critique

Date: `2026-08-26`

Task: `P20-CRITIC-01`

Owner/role: `/root/p20_design_critic`, independent mechanism/topology
critic. This role did not design or implement the candidate.

Status: **PASS THE BLOCKED DISPOSITION.** The P20 analytic design gate is
internally consistent and its OPEN collision is independently reproduced.
The current frozen contract cannot advance to implementation. This is not a
PASS for a CAD candidate.

## Provenance and fingerprint verification

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD:
  `e0474bd6f3475cc26c71a9e84148f78b606a1db4`.
- P19 product baseline:
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Candidate manifest:
  `DESIGN_CANDIDATE.sha256`.
- Candidate-manifest SHA-256: expected and observed
  `fd00b98112ddcd83eb4cb5bcecf384b93fa34764e4b09cfe7e9653ac3acddc89`.
- All `4/4` candidate-manifest entries matched their current contents.
- The nested `DESIGN_INPUT_MANIFEST.sha256` matched SHA-256
  `b26fcf469f3c06c30d89896d91b262c3b0eaeb650a5c00a9d562fd4177b1633b`;
  all `14/14` declared entries matched, including both `git:b69b6ad...`
  snapshots.

The first local verifier attempt used `path` as a zsh loop variable, which is
a zsh special array and temporarily removed commands from `PATH`; it failed
before producing any candidate result. The corrected verifier used `target`
and absolute tool paths. The corrected checks were:

```text
shasum -a 256 DESIGN_CANDIDATE.sha256
=> fd00b98112ddcd83eb4cb5bcecf384b93fa34764e4b09cfe7e9653ac3acddc89

for each candidate entry: shasum -a 256 <target>
=> 4 PASS, 0 FAIL

for each input entry: shasum -a 256 <path>, or
git show <commit>:<path> | shasum -a 256
=> 14 PASS, 0 FAIL
```

## Independent transform check

Using only `C=(0,0)`, `A_old=(-13,-9)`, the proposed
`A=(-15,-11)`, and

```text
alpha_left(u)  = -45 deg * u
alpha_right(u) = +45 deg * u
T_s(q,u)       = A + R(alpha_s(u))q,
```

independent samples at `u={0,0.25,0.5,0.75,1}` reproduced:

- `A_y < A_old_y` and `A_z < A_old_z`: strict lower-left direction PASS;
- old eccentricity `15.811388300842 mm`;
- proposed eccentricity `18.601075237738 mm`, an increase of
  `17.643529359%`;
- local axle coordinate `(0,0)` on both sides at every sample;
- maximum stationary-axle reconstruction residual `0.000e+00 mm`;
- maximum generic transform/inverse round-trip residual
  `3.662e-15 mm`;
- END angles `-45/+45 deg` and relative twist `90.0 deg`.

This proves sufficiency: rotating the rigid outer plate about stationary `A`
makes the axle's plate-local locus one point, so a constant round journal is
center-equivalent. It is also physically necessary under the requested
center-equivalence: if the plate continues rotating about `C != A`, the
stationary axle has local locus `R(-alpha)(A-C)`, a nonzero-radius arc rather
than a singleton.

One representation nuance does not change the result: setting the plate-local
origin to `A` is sufficient and convenient, but is not the only coordinate
encoding. A disk-centered local frame could retain local origin `C` and use
the rigid placement `x=A+R(alpha)(q-A)`, with the fixed bore at constant local
point `A-C`. The actual invariant is **physical rotation about A plus a
constant local axle coordinate**, not the name of the local origin.

## Independent boundary and clearance check

The proposed datum reproduced the design report's conservative checks:

| Check | Independent result | Disposition |
|---|---:|---|
| inner OD54.40 to AF8.15 containing circle | `3.893520068366 mm` web | PASS `>=2.20` |
| left outer OD54.70 to OD7.90 journal | `4.798924762262 mm` web | PASS `>=2.20` |
| right outer OD55.00 to OD7.90 journal | `4.948924762262 mm` web | PASS `>=2.20` |
| bottom retained track | `22.219595306105 mm` conservative clear web | PASS |
| diagonal retained track | `26.759583482386 mm` conservative clear web | PASS |
| upright retained track | `28.666719418691 mm` conservative clear web | PASS |

`A=(-15,-11)` is therefore a valid directional and clearance witness. It is
not a uniquely optimized coordinate and does not prove torque, hand force, or
the user's physical “rotation power” outcome. The design report already
states those limits correctly.

## Independent OPEN collision proof

The exact P19 formulas independently produce the required X intervals:

```text
rod                         [-25.00,+25.00]
left outer plate            [-16.00,-12.80]
left inner plate            [-12.40, -9.20]
central clear span          [ -9.20, +9.20]
right inner plate           [ +9.20,+12.40]
right outer plate           [+12.80,+16.00]
left cap                    [-25.35,-16.30]
right cap                   [+16.30,+25.35]
```

Thus every uncut rod overlaps each outer-plate slab through the full
`3.20 mm` plate thickness. At OPEN the independently computed full-section
rim margins are all positive:

| Rod | left outer margin | right outer margin | clearance to new axle bore |
|---|---:|---:|---:|
| bottom | `14.169660112501 mm` | `14.319660112501 mm` | `23.050000000000 mm` |
| diagonal | `2.630845086139 mm` | `2.780845086139 mm` | `35.210174926742 mm` |
| upright | `2.982601384540 mm` | `3.132601384540 mm` | `29.497124112586 mm` |

The rod section is therefore wholly inside each solid disk and does not
escape through the axle journal. With all six outer rod apertures removed,
the unavoidable intersection is:

```text
V_pair = pi * (2.00 mm)^2 * 3.20 mm
       = 40.212385965949 mm^3

V_total = 6 * V_pair
        = 241.274315795696 mm^3
```

OPEN is a required state, so this one exact counterexample is sufficient to
falsify the current candidate. Moving `A` in YZ, sampling more motion states,
or proceeding to BREP cannot remove an X-interval and full-section overlap
that already exists at OPEN.

No hidden interpretation inside the current frozen contract avoids the
collision. A round clearance hole, clearance window, retained non-guiding
void, shorter/relocated rod, moved outer plate, altered OPEN placement, or
changed plate body would reopen an explicitly frozen object or topology. Any
of those may be a reasonable next design, but none is authorized by this
candidate.

## Review-image inspection

The SVG is valid vector markup and the rendered PNG is a readable
`1600 x 1000` RGBA image. Direct visual inspection confirms that it shows:

- FRONT-YZ orientation and numeric old/new axle datums;
- all three OPEN rod identities and retained inner paths;
- zero retained outer rod rails;
- the centered-equivalent OPEN/mid/END motion and `-45/+45 deg` endpoints;
- the exact X stack and hatched outer slabs;
- the OPEN blocker and `241.274 mm^3` total analytic collision.

The image is suitable for the user decision. It correctly separates the
green math PASS from the red topology BLOCKER.

## Findings and severity

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| `P20-C01` | BLOCKER | Six unavoidable rod/solid-outer-plate intersections exist at OPEN under the frozen no-aperture topology. | Confirmed; no implementation. |
| `P20-C02` | LOW | “Frame origin must be A” is stronger than necessary as a coordinate prescription; physical rotation about A and a constant local axle point are the real invariants. | Documentation nuance only; no effect on blocker or centered-equivalence math. |
| `P20-C03` | INFO | `A=(-15,-11)` is a conservative witness, not a force-selected optimum. | Correctly disclosed as a physical unknown. |

## Requirement coverage

| Requirement | Independent result |
|---|---|
| `P20-REQ-01` | PASS: exact baseline and manifests verified. |
| `P20-REQ-02` | BLOCKER: removing all six outer apertures conflicts with the retained rods. |
| `P20-REQ-03` | PASS analytically: retained inner tracks and conservative clearances reproduced. |
| `P20-REQ-04` | PASS as a directional design witness only. |
| `P20-REQ-05` | PASS mathematically: exact `-45/+45`, relative `90`. |
| `P20-REQ-06` | PASS mathematically, subject to the coordinate-encoding nuance above. |
| `P20-REQ-07` | BLOCKER: uncut P19 rods and frozen X stack contradict solid outer slabs. |
| `P20-REQ-08` | PASS stop behavior: the design returned instead of widening scope. |
| `P20-REQ-09` | PASS stop behavior: no downstream artifact work was performed. |

## Recommendation and receipt

- Recommendation: **PASS the P20-DESIGN-01 BLOCKED disposition; FAIL the
  current contract as an implementation candidate.**
- Changed path: this `DESIGN_CRITIQUE.md` only.
- Evidence actually run: candidate and nested-input SHA-256 verification;
  independent transform/inverse sampling; eccentricity, rim-web and
  point-to-segment clearance math; exact axial-stack reconstruction; OPEN
  rim/bore clearance and collision-volume calculation; PNG/SVG format and
  direct visual inspection.
- Explicitly not run: P20 source/tests, BREP, STEP, Viewer, snapshot, mesh,
  3MF, slicer, print, or physical validation.
- Unresolved physical risks: hand torque/force, friction, backlash, printed
  fit/strength, heat, wear, retention and soldering ergonomics.
- Next user decision: keep the strict no-outer-aperture rule and close P20 as
  infeasible, or explicitly authorize a new topology contract. The smallest
  focused reopening to investigate is a **non-guiding outer-plate clearance
  aperture/window** for each retained rod.
