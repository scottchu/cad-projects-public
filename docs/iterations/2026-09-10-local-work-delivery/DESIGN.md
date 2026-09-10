# Local-work delivery design

## Scope rationale

This candidate reconciles intentional branch and dirty-worktree content onto
modern main without changing CAD geometry. Main remains authoritative for
repository policy, workflow binding, shared templates, repository tests, Kage,
the separated sticker boundary, and unrelated projects. Source commit
`a883404` and recovery snapshot `design-main-20260910T101124` are immutable
provenance inputs.

The merge preserves three independent bodies of work:

1. XT60 branch additions and unique WIP source, tests, CAD artifacts, review
   media, iteration records, and authored HTML intent gates.
2. Pill Click's already reviewed source-preserving workspace migration.
3. The inactive drone OpenSCAD/STL tree under `archives/drone`.

Only continuity pointers are reconciled. XT60 P25 is the sole current
first-CAD review iteration; P19 remains the latest accepted digital mechanism
baseline. P17-P24 remain preserved historical evidence under their individual
accepted, rejected, superseded, experimental, or preview-only dispositions.
The known P20 R4 print-kit hash-guard failures remain visible and are not
repaired or reclassified.

Pill Click and drone snapshot bytes remain exact. One ignored Pill Click review
job referenced by the preserved migration manifest was absent from the recovery
snapshot; it is imported byte-for-byte from the immutable original checkout and
force-staged as explicit provenance. The root lock is recomputed through `uv
lock`, adding only the Pill Click workspace member and its `networkx` dependency.
No old root policy or lock is copied.

No CAD regeneration, slicing, printer operation, service mutation, push, pull
request, or merge is part of this implementation role.
