# Legacy evidence index

The legacy source directory was untracked beneath parent Git HEAD `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`. These preserved files therefore use content manifests as provenance.

- `README.original.md`: the original project README, byte-for-byte.
- `source-docs/`: every textual file beneath the original `docs/`, retaining relative paths and bytes. This includes handoffs, amendments, physical-test plans/contracts, harness evidence, and the authoritative clean-restart document.
- `tooling/`: original `pyproject.toml`, `package.json`, `uv.lock`, and `package-lock.json`, byte-for-byte but renamed `.legacy` so they cannot act as nested workspaces or locks.
- `../../legacy/source-project/`: meaningful textual Python/JavaScript source, tests, model generator wrappers, README files, and metadata in original relative layout. Historical tests are not active acceptance tests.
- `../../manifests/legacy-docs.sha256` and `../../manifests/legacy-source.sha256`: target-relative content manifests.

Status labels inside these files are historical evidence. They do not override `CONTINUATION_RESTART_2026-08-22.md`, `PROJECT_STATE.md`, or ADR-0001.
