# P19-REVIEW-05 formal independent join

Reviewer: `/root/p17_optimizer_formal_review`
Date: `2026-08-26`
Decision: **ACCEPT — P19 R1 CAD, six written STEP artifacts, and exact-artifact Viewer handoff only**.

This accepts the repaired immutable P19 R1 candidate as a digitally coherent
parametric CAD baseline. It does not accept mesh/3MF, slicing, printing,
physical fit, retention, hand force, friction, backlash, heat, wear, clamp
force, self-locking, or real soldering ergonomics.

## Frozen provenance

- Formal-review input manifest SHA-256:
  `9d9bfcdf1a0ae3aa7162efcdecb132eafaeed6d4853daf1aaddb6c3ce87d66bc`
- Formal-review inputs: `6/6` content entries independently verified.
- Candidate-manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`
- Candidate contents: `20/20` independently verified.
- Repaired design SHA-256:
  `36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4`
- Repaired critique SHA-256:
  `2ee1782bc64805522263bcb09e017ccce1e296a2ef507266ed0592be860b2248`
- Implementation receipt SHA-256:
  `72bd3b928e8733af79457d92f9c4f738c0f3e62600d7e39324f0f6339371d73f`
- Independent validation SHA-256:
  `304239aecb3b939a6ef1412d1b31979b4bafda2b2e997ca7e7311b36adfb88ef`

The checksum warnings are caused only by human-readable comment or blank
lines in the manifests; no declared candidate or formal-review entry failed.

## Formal join findings

- The accepted source preserves one shared normalized motion state, opposite
  `-5/+5 deg` outer-plate rotation, `C=(0,0)`, the real fixed stepped axle
  `A=(-13,-9)`, the ordered OPEN right angle, the ordered collinear END state,
  and unchanged bottom/diagonal/upright identities.
- The six inverse-derived rail travels pass the frozen `>=4.00 mm` gate. The
  left/bottom and right/upright rails sit on the active `4.00 mm` boundary;
  no decorative or hand-added rail extension is present.
- Actual-solid evidence passes: minimum web is
  `2.405845086139 mm >= 2.20 mm`, the four-contact system remains rank `3`,
  worst condition is `13.007686517253 <= 15`, and the sampled production,
  support, cap/axle and service collision gates pass.
- The repaired completed-pigtail removal check evaluates five finite pigtail
  features pairwise against every OPEN production solid. Its 123-state BREP
  sweep and 3003-state analytic sweep report zero intersection. The retained
  regression detects the former two `47.2594024 mm3` bent-wire/diagonal-rod
  collisions, so the prior compound-aggregation defect is not hidden.
- Independent validation reports all six written STEP files as valid, closed,
  positive-volume assemblies and every generator/import pair unchanged in
  kind, topology, geometry, bounds and counts.

## Snapshot review and Viewer boundary

The exact three candidate PNGs were independently inspected at original
resolution:

- OPEN SHA-256 `c11badf0493dfdca2a515d176571437d04d3c2e4f1f3870da2e85f02c7fa9a88`:
  accepted right-edge OPEN topology, short-tail/tool direction and eccentric
  fixed axle are visible.
- END SHA-256 `4bfde7743df3a1f031b51a0cb9b63b05af276b469b60943b307c8499b4e2640f`:
  the three named rods reach the accepted END ordering without a visible swap.
- Exploded SHA-256 `470e06e2c9cdb4465db26085c5f3f3b9939d43bc710d5c419d94ea0d8c2ee0ff`:
  four plates, one continuous stepped axle, two keepers, three rods and six
  caps are present; no extra yoke, linkage, gear or stability bar is visible.

The state PNG filenames say `front`, while the images explicitly badge the
camera as `RIGHT`. This is non-blocking for topology/orientation review but is
not evidence of a literal front-camera snapshot.

The exact `p19_r1_full_motion.step` artifact may be handed to CAD Viewer and
shown to the user. A live-preview-ready claim still requires the exact Viewer
page to return HTTP `200`, the exact artifact endpoint to return HTTP `200`
with `state == "ready"`, and visual confirmation of no error state. This
review neither starts nor edits Viewer state.

## Exact-margin and physical-risk boundary

- The limiting pigtail pair is `bentWire0 :: diagonalRod` at seated OPEN.
  Reported clearances are `0.7499999999996648 mm` BREP and
  `0.7499999999996647 mm` analytic. These pass the nominal `0.75 mm` contract
  only within declared numerical tolerance and provide effectively **zero
  positive manufacturing margin**.
- The complete solder-tool keepout also begins exactly `0.75 mm` outside the
  OD55 rim. This proves nominal digital non-intersection, not real iron access
  under printer, wire, tool-position or hand-placement variation.
- Both active `4.00 mm` rails have no extra travel margin. The exact upright
  tangency remains a serious friction, wedging, backlash and force-transfer
  unknown despite nominal rank/conditioning closure.
- PETG rail fit, OD4 stock tolerance, permanent-cap retention, keeper/axle fit,
  flex, heat exposure, wear, short-ESC-tail handling, release force, clamp
  force and self-lock behavior require physical testing.
- No mesh, 3MF, slicer, printability or physical acceptance is granted.
