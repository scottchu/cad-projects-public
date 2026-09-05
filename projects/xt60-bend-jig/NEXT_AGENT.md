# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under
`docs/iterations/p19-r1-front-edge-short-tail/` before changing this project.

## Resume point

- Active iteration: `p19-r1-front-edge-short-tail`.
- P19 R1 is digitally accepted for CAD, six written STEP artifacts, and exact
  Viewer handoff only.
- Exact candidate-manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- Independent validation: `PASS`, report SHA-256
  `304239aecb3b939a6ef1412d1b31979b4bafda2b2e997ca7e7311b36adfb88ef`.
- Formal review: `ACCEPT`, report SHA-256
  `7b5436c57070547b14241bc3de6cbc7047c07cbd1e4070b036f0d8d51040aba3`.
- Active handoff:
  `docs/iterations/p19-r1-front-edge-short-tail/HANDOFF.md`.

## Frozen current mechanism

- FRONT: `+Z` XT60 mating-head/up; `+Y` short-tail/tool right/outward.
- Three `OD4 x 50 mm` stainless rods, six permanent caps, four plates, one
  real fixed stepped axle at `A=(-13,-9)`; virtual rotation datum `C=(0,0)`.
- Shared motion only: `alpha_left=-5u`, `alpha_right=+5u`.
- Plate ODs `54.40/54.70/55.00 mm`; cutters `OD4.15 mm`.
- OPEN exact right angle; END exact ordered diagonal; identities unchanged.
- Six inverse-derived rail center travels are all at least `4.00 mm`.
- Minimum actual web `2.405845 mm`; rank `3`; worst condition `13.007687`.
- Completed-pigtail rigid removal is digitally clear by exactly the active
  `0.75 mm` nominal threshold, with zero actual-solid intersection.

## Next smallest action

GitHub [PR #11](https://github.com/scottchu/design-projects/pull/11) is merged.
Request human Viewer review of the exact P19 full-motion artifact before any
separately authorized mesh/3MF/slicing/printing or physical acceptance. Any
geometry change reopens the candidate fingerprint, validation, and formal
review.

## Printing-profile addendum — 2026-08-31

Read [PRINTING_PROFILE.md](PRINTING_PROFILE.md) before future authorized print
preparation; P19 process selection and manufacturing/physical gates remain open.
See the [repository-policy handoff](../../docs/iterations/2026-08-31-printing-profiles/HANDOFF.md) for independent status.
No CURRENT, frozen contract/fingerprint or design acceptance changes follow.

## Documentation-refresh addendum — 2026-09-05

The project README now foregrounds the focused P19 regression and uses the
installed CAD and CAD Viewer workflows without a stale plugin-cache pin or old
service command. Resume from the same accepted candidate and human review action;
no source, artifact, or acceptance boundary changed.
