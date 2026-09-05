# CLEAN-GCS-02 reversible cleanup receipt

**Status:** PASS; recoverable quarantine completed 2026-09-03.

Quarantine: `/Users/scottchu/.Trash/laifen-wave-case-cleanup-2026-09-03.HcZ1MJ/`

The narrowed set moved intact consisted of every immediate `scratch/` child except `presentation`, `r7-*`, `r7-recovery`, `readme-refresh-receipt.md`, and the five live P2 R3 directories (`generic-container-sync-validation`, `generic-container-sync-critique`, `generic-container-sync-recovery`, `generic-container-validation`, `generic-container-formal-review`), plus preview directories and tests for P2 R13 through R22.

Pre-move inventory: 153 moved source roots, 6,162 files, 2,440 directories, 2 symlinks, 917,839,872 bytes (du-rounded working-tree bytes). The initial requested scope enumerated 158 roots; five live P2 R3 evidence directories were preserved and excluded before the move. Recovery records are `recovery/original-paths.txt`, `recovery/files.sha256` (SHA-256 `71d4d84ac83bfdc8a23662be43be7e6afde32d3e8b56dcdcd1b9c8b752205e8e`), and `recovery/inventory.txt`; restoration instructions are in quarantine `RECOVERY.md` (SHA-256 `92de85419f64d11e084ce73c3c910823bb1a60e50ab133cb525c6f569580e251`).

Verification passed:

- All 6,162 quarantine files matched the pre-move SHA-256 manifest; selected originals are absent.
- Exact P1 R7 `cad/p1_r7_end_chamfer/print_layout.step` hash: `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
- Live simulator loopback and private HTTPS `/container-simulator/`: HTTP 200; public 3245 and private 3249 loopbacks: HTTP 200.
- Existing Tailscale routes, including `/container-simulator`, `/laifen-full-section`, 3245, and 3249, remained configured.
- `scratch/presentation`, P2 R3 live evidence directories, P2 R10 preview/source/tests, project docs, and unrelated worktrees were preserved.

No permanent deletion occurred. Remaining risks are limited to user-device comprehension and future recovery handling; Trash must remain intact until explicitly retired.
