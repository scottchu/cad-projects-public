# Printing profiles — standalone main-based PR

## Frozen contract

Baseline: `b69b6ad12af611644987f026eef4940db9c7bb34` (origin/main), branch
`codex/project-printing-profiles`. User authorized a standalone PR, not merge.
Port only printing-profile documentation/test changes from the earlier local
`3192c326...` documentation candidate. That candidate is prior evidence only;
this main-specific packet requires new independent gates.

- Every project gets an editable printing profile: nozzle, material, process,
  part orientation/loads/fits, traced slice/print runs and growing concerns.
- Preserve available/intended/verified-slice/physical-observation distinctions;
  unknown values stay pending, non-print projects explain N/A.
- Copy shared FDM rules, template and Kage profile unchanged. Adapt the new XT60
  profile to main's P19 R1, never import local unmerged design work as authority.
- Only printing-profile additions to root policies/tests, append-only pointers
  in project state/NEXT/active HANDOFF, and this repository-policy iteration.
- Kage manifest changes only shared CAD_WORKFLOW hash and new profile row;
  source/target authority manifests and every other original row stay intact.
- Preserve project CURRENT, frozen design contracts, source/tests/artifacts,
  AGENTS, dependencies/locks and all CAD/slicer/physical verdicts. No CAD,
  preview, slicing, printer, source-worktree or Git index/ref mutation.

Done: scoped main-port candidate, focused tests and independent critic/validator
receipts joined by a distinct formal reviewer, then root-owned PR delivery.

## Frozen pre-edit input manifest

SHA-256 path-and-content list below. Full BRIEF/DESIGN and decision-bearing
outputs enter CANDIDATE.sha256 after implementation. Mutable status/evidence
indexes and receipts are excluded; unchanged CAD is protected, not redesigned.

```text
22a4b39ab1439018f2570d0d90326f700f07647ae399a34655a8a5be347382c5  AGENTS.md
ab7905ec25aff20a8befe996642124b01785682f292f3e4187fe68224ce9fdbf  docs/ADDING_A_PROJECT.md
352252641e34571b281df84f70b45907b1779d42d02a78d80286318313b27f06  docs/ARCHITECTURE.md
55eaba17c19970620d203fb187ef4cf95928498e9e3ede744ab7accebd603d7c  docs/CAD_WORKFLOW.md
cc9a100a8e6f552d8d44beaaaf9d5f1348465ad52b7dabf4a02d5b2a71074120  docs/PROJECT_CONTINUITY.md
9e149b661d6b2989287f39e46d821fc253f5a79c878f8c1ebc811b5f16d61375  docs/WORKSHOP.md
1b010b016a7fc7edc47ce984f09391771f6dc1586ea56274c6d6d27563e02309  projects/kage/docs/EXPERIENCE.md
a36789c14d0b21f43e1e36ac3a7a43b31ebedd816e61dd9826fd458264de3ec8  projects/kage/docs/REQUIREMENTS.md
4c0fe07c882c9fbdf25c2d098a0200be4d4e50a1f29ec9f8297b1806e89c926c  projects/kage/docs/decisions/README.md
1e077da21ad8bd0721fe5d469b4563c4d486487e95c5ee4cad607b9d007fe72e  projects/kage/docs/iterations/2026-08-23-direct-cad-viewer/BRIEF.md
1f19b9bb92cea1718de295460a8872a7e61f7317c22e434cfc744abda2168013  projects/kage/docs/iterations/2026-08-23-direct-cad-viewer/DESIGN.md
4b23ae3a0c65fb861e1215e95ba435b5747d2d3c4f085a6e07a925af37263f5c  projects/xt60-bend-jig/docs/EXPERIENCE.md
07e86ede330777bca4f1d9975604024aada7fdf7e3d7b261bc524135cfc3cc82  projects/xt60-bend-jig/docs/REQUIREMENTS.md
555a449864b5498400bcccfa45e69097359cecf7f2df5472a9801fd4b55ce105  projects/xt60-bend-jig/docs/decisions/README.md
e3768301a271145d3fa49d8ab9f138435fa1988ae78f691711784b264580d824  projects/xt60-bend-jig/docs/iterations/p19-r1-front-edge-short-tail/BRIEF.md
169583198638b23201b5c47835a66537551f87a837e78c21bb519161e3704fb7  projects/xt60-bend-jig/docs/iterations/p19-r1-front-edge-short-tail/DESIGN.md
e05fca71582358cfd1c14445a28abd4a814f82fcca6332ff7692826bc15d3d12  tests/test_repository_structure.py
```

## Mutable task DAG

| ID | Owner / role | Dependencies | Exclusive write scope / done gate |
|---|---|---|---|
| PRINT-PR-IMPL | /root/printing_docs, implementer | frozen contract | allowlisted docs/profile/test/manifest; no self-approval |
| PRINT-PR-VALIDATE | root-assigned distinct validator | frozen candidate | VALIDATION only; tests, links, hashes, preservation |
| PRINT-PR-CRITIC | root-assigned distinct critic | frozen candidate | REVIEW only; rule/profile/evidence critique |
| PRINT-PR-REVIEW | root-assigned distinct reviewer | VALIDATE + CRITIC | REVIEW serial join; scoped acceptance |
| PRINT-PR-DELIVER | /root, delivery | REVIEW | commit/push/PR only; no merge |

Read scope: relevant policy/project records and frozen candidate. One writer per
namespace, at most three workers. Inherited model/effort; approximately eight
minutes/eight-thousand tokens per implementation checkpoint, bounded independent
checks, receipt <=1000 words. Initial attempt plus at most two focused repairs.
Stop for input drift, broader manifest changes or scope expansion. Actual owners,
fingerprints and disposition are recorded in VALIDATION/REVIEW/HANDOFF.
