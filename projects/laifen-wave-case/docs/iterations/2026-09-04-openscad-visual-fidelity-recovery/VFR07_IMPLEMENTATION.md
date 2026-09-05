# VFR-07 implementation receipt

Status: **PARTIAL — scratch recovery and C1 integration pass; the unchanged
smooth-only browser worker prevents the required diamond worker gates. No
implementer approval is given.**

Owner role: `/root/openscad_vfr07_impl`, syntax-first recovery implementer.
Input fingerprint: `c1ca4607826e202b2c42a88dc5c747ecc1d0bb75752b64cb311aa3b550218b90`
(18/18 OK). Recovery-design input fingerprint:
`ffb1d5bf59b3a6381b7b747e4843825a43c98f8ebf0c59c0e9214194fdc00b39`
(12/12 OK when evaluated from the project directory; its manifest uses
project-relative paths).

## Scratch recovery

The retained VFR-06 attempt-2 source hash was
`47d0db738e9691e4441d212ba58810cea02f47abca8efbb803d085ae91e7c2e9`.
The only source correction was the missing outer list terminator in
`v06_disk`:

```text
...ring[(i+1)%len(ring)]];
...ring[(i+1)%len(ring)]]];
```

This has no numeric or topology meaning beyond completing the list returned
by the existing list comprehension. `verify-delta.py` proves that exact
one-fragment replacement and that the candidate test is byte-identical to
the retained VFR-06 attempted test. The scratch candidate hash is
`48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`.

Pinned vendor hashes were unchanged: `openscad.js`
`904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` and
`openscad.wasm` `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.

The cumulative source-only preflights used the pinned WASM runner and passed
with no parser error, warning, assertion, `undef`, nonfinite result, or
missing marker:

| Stage | Wall time |
|---|---:|
| 00-parse | 73.540 ms |
| 10-address | 71.869 ms |
| 20-clip-ownership | 110.796 ms |
| 30-mesh-data | 393.332 ms |
| 40-profile-zip-direct | 3,899.989 ms |

The last stage forced default direct arrays within the 10 s ceiling and
reported body `17909` points / `35814` faces and cap `11636` points /
`23268` faces. `verify-preflight.py` confirmed that all 50 changed
`diamond_*` / `v06_*` helpers are declared by the probes and all receipts bind
the same source and vendor hashes.

## C1 and local geometry evidence

`integrate.py` atomically installed the exact scratch pair. The authoritative
source is now `48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`;
the focused test is `be973544f458701851aa1b01d3aa638121b50733663245fb84983124331ae6b4`.
The required focused pytest command passed: **14 passed**.

Pinned-WASM Manifold G2 export (`131.93..139.06 mm`, 7.13 mm band) completed
in 273.160 ms total / 249.240 ms compile. Its STL is
`scratch/vfr07-implementation/g2-short-band.stl`, SHA-256
`1923d030999cacbd256d4c551b539c29d5a08ec1ed84d35edc9f2c79be7fe00f`:
1,586 vertices, 3,168 faces, watertight, winding-consistent, one component,
Euler 2, all edges used exactly twice, and zero degenerate faces.
Using seed 404, three triangle-interior samples for each of its 2,706 side
triangles gave 8,118 source-artifact field checks: maximum
0.0128831435 mm, p99 0.0118663137 mm and mean 0.0045422439 mm. This is below
the 0.025 mm contract, but remains implementer evidence pending independent
reproduction.

The unchanged source also produced final local Manifold body and cap STL
probes: body 55,744 faces, 2.680 s wall,
`0cb0fcd9f420e68b548302bd0018d6f7a848f55caaf1653e3eeb13208605c4a3`;
cap 40,510 faces, 1.738 s wall,
`e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514`.
Each was watertight, winding-consistent, one component, had edge use exactly
two and no degenerate faces. These are implementer measurements only; they do
not replace the required independent accuracy, protected-geometry, or worker
validation.

## Stop boundary

V06-3B and V06-3C require the exact browser worker to accept a diamond job.
The frozen unchanged worker/UI contract is smooth-only: its job allowlist
removes diamond controls, while VFR-07 forbids worker/UI changes and Diamond
enablement. Therefore that gate cannot be truthfully run from this task’s
authorized scope. V06-3P also remains pending because it requires the worker
evidence plus distinct critic, validator and formal-review identities.

No browser/UI/worker/vendor/runtime/lock, Python oracle, continuity,
STEP/slicer/service/printer path was changed. No deployment or Diamond
enablement occurred. C1 remains integrated for the root to route to the
separate authorized worker/independent-review gates or restore if that route
is rejected.

Exact scripts, probes, receipts and local STL evidence are retained under
`scratch/vfr07-implementation/`.
