# Local-work delivery implementation

## Receipt

- Owner/role: `/root/delivery_implementation`, M2 source-preserving implementer.
- Status: complete after two focused documentation/provenance repairs.
- Baseline: `cf8ec46cffc24d8beb26d3908bb6023843824f1f` on
  `codex/reconcile-local-work-20260910`.
- Source commit: `a8834040afe401637d36e94bd8fdd9e1d9874d35`.
- M1 input manifest: `c7162df2da0885d4dee64f70cd1b2e12d8c4062522f8e53a2c7c7291a15b15aa`
  (`1825/1825` reverified in the original checkout).
- Recovery `manifest.json` SHA-256:
  `37c87c541c9bcc8793ea1bc1387c8b1d977ec39d090af962acc98c9cb603cbc1`.
- Frozen contract section SHA-256:
  `af14739aad568286ee5246a40c6f1690ccb4ea578edc7e4511ead0710803f57f`.
- Final source/test/artifact/lock freeze: `703` entries; manifest SHA-256
  `4afc5f670dacd9625ed4f939e17ad4e16d196f007fef67790df8103093a0583d`.
- Final full candidate: `529` entries; manifest SHA-256
  `97357dfeadd1023c178f27e02b02429bf725053fda3f884ae7aa69714dda0210`.

## Implemented result

- Imported `103` exact XT60 branch paths and reconciled the other three XT60
  branch pointers. All `109` branch-changed paths, including three superseded
  root policy files, are accounted for in `PROVENANCE.tsv`.
- Imported `134` exact snapshot XT60 paths and retained the fifteen redundant
  PNGs only in recovery. Current continuity now names one P25 first-CAD preview,
  retains P19 as the accepted digital baseline, and explicitly preserves the
  historical P20 R4 guard failures.
- Imported `158` exact Pill Click snapshot files plus the ignored
  `p1_review_job.json` required by the historical source manifest. The latter
  was inspected, matched SHA-256 `02b48475...e82`, and was force-staged so it
  cannot disappear through `.gitignore`.
- Imported all `106` archived drone snapshot files exactly and registered the
  archive only as inactive historical material in the root README.
- Generated `uv.lock` from modern main with `uv lock`; its only dependency
  additions are workspace member `pill-click` and `networkx 3.6.1`.
- Preserved modern main policy pointers, external workflow binding, templates
  absence, `.agents` absence, tools absence, repository tests, Kage, sticker
  separation, package lock, and unrelated projects.
- No CAD/artifact regeneration, slicing, printer/service operation, commit,
  push, pull request, or merge occurred.

## Exact implementation and verification commands

```sh
git -C /Users/scottchu/Projects/personal/design-projects archive a883404 \
  $(< /tmp/xt60-branch-import-paths.txt) | tar -x -C /Users/scottchu/Projects/personal/design-projects-delivery-20260910
rsync -a --files-from=/tmp/xt60-snapshot-import-paths.txt /Users/scottchu/.codex/backups/design-main-20260910T101124/files/ /Users/scottchu/Projects/personal/design-projects-delivery-20260910/
rsync -a /Users/scottchu/.codex/backups/design-main-20260910T101124/files/projects/pill-click/ /Users/scottchu/Projects/personal/design-projects-delivery-20260910/projects/pill-click/
rsync -a /Users/scottchu/.codex/backups/design-main-20260910T101124/files/archives/drone/ /Users/scottchu/Projects/personal/design-projects-delivery-20260910/archives/drone/
uv lock --check || uv lock
```

`uv lock` resolved `74` packages and added only `networkx v3.6.1` and editable
`pill-click v0.1.0`. The first `--check` correctly reported that the imported
workspace member required lock regeneration; the final `uv lock --check`
passed.

```sh
(cd /Users/scottchu/Projects/personal/design-projects && \
  shasum -a 256 -c /tmp/design-main-inventory-20260910/inputs.sha256)
shasum -a 256 -c docs/iterations/2026-09-10-local-work-delivery/M2-SOURCE-ARTIFACT-FREEZE.sha256
shasum -a 256 -c docs/iterations/2026-09-10-local-work-delivery/CANDIDATE.sha256
node projects/pill-click/docs/iterations/2026-09-01-workspace-migration/check-migration.mjs
shasum -a 256 -c projects/xt60-bend-jig/docs/iterations/p25-r1-rear-loop-front-pusher-clamp/CANDIDATE_MANIFEST.sha256
shasum -a 256 -c projects/xt60-bend-jig/docs/iterations/p24-r1-manual-three-slider-clamp/CANDIDATE.sha256
shasum -a 256 -c projects/xt60-bend-jig/docs/iterations/p20-r3-wire-90deg/CANDIDATE.sha256
```

Results: M1 `1825/1825` inputs stable; both delivery manifests PASS; Pill Click
migration checker PASS (`138` included, `1` excluded, `1` external legacy;
candidate `cf03c7c...bdd37c`); P25 `13/13`, P24 `12/12`, and P20 R3 `12/12`
historical manifests verify. All `547` provenance source rows have current
destination hashes; every exact-import pair matches.

## Repairs and remaining risks

Repair 1 added the ignored Pill Click review-job manifest input, restored the
required XT60 state headings, corrected the root delivery link, and fixed the
P25 handoff disposition. Repair 2 recomputed the two stale PROJECT_STATE
destination hashes and then all destination hashes in the provenance ledger.

Known P20 R4 behavior remains intentional evidence: its targeted P20 R4 + P24
+ P25 suite historically passes `42/42`, while the separate print-kit suite has
one pass and two expected source-hash-guard failures. The inherited Blue/XT60
collision, thin webs, and all fabrication/physical unknowns remain open. Final
acceptance belongs to independent validation, critique, and formal review.
