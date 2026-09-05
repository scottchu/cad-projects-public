# VAL-CLEAN-GCS-02-01 independent validation

**Verdict: PASS** on 2026-09-04. The frozen CLEAN-GCS-02 selection is intact and recoverable from Trash, its original paths are absent, the narrowed move stayed inside its exact project scope, protected project evidence and source remain byte-identical to the available pre-cleanup records, and the live delivery surfaces still respond with the delivered bytes. No blocking finding remains.

## Inputs and provenance

Validation used the corrected cleanup receipt and the immutable recovery records at `/Users/scottchu/.Trash/laifen-wave-case-cleanup-2026-09-03.HcZ1MJ/`:

| record | SHA-256 |
| --- | --- |
| `RECEIPT.md` | `7937a2260831df09b1bf66b101b7fd56844f0715926f4ce0132908b28f0ea5a8` |
| quarantine `RECOVERY.md` | `92de85419f64d11e084ce73c3c910823bb1a60e50ab133cb525c6f569580e251` |
| `recovery/inventory.txt` | `4d0b2ed99d87e1dde0ef3800ec200c886ac47e20641239f1fb18b0abefacbf22` |
| `recovery/original-paths.txt` | `0e0fd07b618a85707e4347c58f88cec6692feaf21f7d3d58c49a962c3662ef9d` |
| `recovery/files.sha256` | `71d4d84ac83bfdc8a23662be43be7e6afde32d3e8b56dcdcd1b9c8b752205e8e` |
| CLEAN-GCS-01 pre-cleanup `inventory.json` | `04310c458b9a81beee7ff8315255c593acd66a73938c18cc54523a73f72b7488` |
| CLEAN-GCS-01 `canonical-key-files.sha256` | `73aeefc1c1885a97341dc485e5c9c27149705ba6e7a1ce05e75a46d42756ca70` |
| CLEAN-GCS-01 `proposed-move-files.sha256` | `d277213da58c026a0636d246bfbb337e17e2c8c2c649a6e6849265174ce09c42` |
| CLEAN-GCS-01 `proposed-move-symlinks.tsv` | `0c54dc28d2bad81b222d87fbf315b79075c229b8a743ee88fe7016447acd7fd0` |
| P2 R3 `DELIVERY.md` | `caa5f1a5d4293599fb5d414ba50e544638feb7ac32be55300d814b36e43368a2` |
| P2 R3 `inputs/delivery-evidence.sha256` | `d9f0c05cffe89abd7bacf8bae44138e46d051d56fa26317ca0a6c6e72fef46ee` |

The receipt correction is consistent with the independent count: CLEAN-GCS-01 recorded 158 initially requested roots; the five live P2 R3 evidence roots were removed from that set before movement, leaving 153 moved roots.

## Quarantine integrity and exact scope

- `original-paths.txt` contains 153 unique, non-overlapping roots: 10 P2 R13-R22 preview roots, 93 immediate `scratch/` children, and 50 P2 R13-R22 test files.
- The final 153-root set is exactly the 158-root pre-cleanup requested set minus the five preserved live P2 R3 evidence directories. There are zero unexpected or missing roots and zero paths outside `projects/laifen-wave-case`.
- The quarantine contains 6,162 regular files, 2,440 selected directories, two symlinks, no special files, and 905,386,031 regular-file bytes. Its `du`-rounded size is exactly 917,839,872 bytes, matching the receipt.
- All 6,162 manifest entries parsed cleanly. Every entry has one selected-root owner and one destination under the quarantine. There are zero duplicate paths, missing destinations, hash mismatches, unmanifested regular files, or manifest paths absent from the quarantine.
- All 153 original source roots are absent, while every corresponding quarantined root exists.
- The two untraversed symlinks match the pre-cleanup symlink record exactly. Both point from the R13/R16 audit mirrors to the preserved absolute project `preview` directory; target-string SHA-256 is `e42ecb07895eb3662fe61dbce307fe9f1c0d6c2354f55a8ce881674352d9de08`. They did not cause external files to enter the move manifest.

This establishes recoverability for every selected file and filesystem object. Nothing in the selected set was permanently deleted.

## Preserved data

- The CLEAN-GCS-01 pre-cleanup canonical manifest passes **240/240** entries with zero failures. It covers the project continuity and design documents, `scratch/presentation`, the R7 receipts/recovery paths, P2 R10 core source and tests, and the P1 R7 CAD tree.
- The five preserved live P2 R3 evidence directories contain 299 files. All 299 match their hashes in the pre-cleanup proposed-move manifest; none is missing or changed.
- `cad/p1_r7_end_chamfer/print_layout.step` is present, 74,416,394 bytes, SHA-256 `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
- The active `scratch/` root contains exactly the narrowed exclusions: `presentation`, the five live P2 R3 evidence directories, six `r7-*` receipt/response files, `r7-recovery`, and `readme-refresh-receipt.md`. No unapproved immediate scratch child remains.
- All eight registered Git worktrees exist with their `.git` markers. The current worktree remains on `codex/laifen-wave-measurement-gate` at `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`; unrelated top-level `kage`, `projects`, and `xt60-bend-jig` project entries remain present. Because every moved root is confined to the Laifen project, no unrelated project or worktree path entered the quarantine.

## Live delivery

The loopback and private `/container-simulator/` roots each returned HTTP 200. Each served asset returned HTTP 200 and matched the P2 R3 delivery evidence from both surfaces:

| asset | loopback/private SHA-256 |
| --- | --- |
| `index.html` | `ace28e8dd08de7f9ca9bf916887911e0d118c6dd4b0d2e6594f2a88950b878a5` |
| `app.js` | `575f3734f76dd6313ccc9e33b33ffb72008292c20b4dbfc3f5db517d9789affe` |
| `math.mjs` | `b3e4c734b166349251c9b7683aa23d428cb4d2f8f167ff29349def7dc024337b` |
| `style.css` | `a19c755ca5c27dbe602283ba2652c5b2ff005c2a59266b078c5930b58ff6ccf3` |

`http://127.0.0.1:3245/` and `http://127.0.0.1:3249/` both returned HTTP 200 and the same 1,750-byte response, SHA-256 `ee517c431df11748a4fd11cd65f65143ea205985c7e43088d27a9759aa99ac3a`. Current `tailscale serve status --json` retains `/container-simulator` -> `127.0.0.1:8972/container-simulator`, the existing `/laifen-full-section` route, public-root proxy `443` -> `3245`, and private-root proxy `8449` -> `3249`.

## Commands and results

Commands ran from `/Users/scottchu/.codex/worktrees/4f8c/design-projects`:

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-03-cleanup-reversible/RECEIPT.md \
  /Users/scottchu/.Trash/laifen-wave-case-cleanup-2026-09-03.HcZ1MJ/RECOVERY.md \
  /Users/scottchu/.Trash/laifen-wave-case-cleanup-2026-09-03.HcZ1MJ/recovery/inventory.txt \
  /Users/scottchu/.Trash/laifen-wave-case-cleanup-2026-09-03.HcZ1MJ/recovery/original-paths.txt \
  /Users/scottchu/.Trash/laifen-wave-case-cleanup-2026-09-03.HcZ1MJ/recovery/files.sha256

uv run --package laifen-wave-case python - <<'PY'
# Read-only Python checks parsed all roots and manifest rows, mapped each old
# absolute path beneath the quarantine, recomputed every SHA-256, enumerated
# regular files/directories/symlinks with os.walk(followlinks=False), compared
# exact path sets, checked root ownership/scope, and checked original absence.
PY

set -o pipefail
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-clean-gcs-01-reversible-cleanup/canonical-key-files.sha256 \
  | awk 'BEGIN{ok=0;bad=0} /: OK$/{ok++} !/: OK$/{bad++; print} END{printf "canonical_manifest_ok=%d canonical_manifest_bad=%d\n",ok,bad}'
# canonical_manifest_ok=240 canonical_manifest_bad=0

curl -k -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8972/container-simulator/
curl -k -sS -o /dev/null -w '%{http_code}' https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator/
tailscale serve status --json
git worktree list --porcelain
```

The HTTP asset checks used `uv run --package laifen-wave-case python` with `urllib.request`, a 20-second timeout, and SHA-256 over response bytes for both base URLs and all four asset names. Both root checks returned 200; all eight asset responses returned 200 with the hashes above. The same checker read 3245 and 3249 and found HTTP 200 with byte-identical bodies.

## Findings and limits

There are no cleanup blockers. The first receipt version said 158 selected paths, using the pre-narrowing count; the corrected receipt now truthfully distinguishes 158 requested roots from 153 moved roots and has been rehashed above.

No comprehensive byte manifest exists for every unrelated repository and external-worktree file. The validation therefore proves unrelated preservation through exact quarantine-path confinement plus current project/worktree presence, while the 240 canonical files and 299 live-evidence files have true pre/post byte parity. Runtime checks are point-in-time observations. Recovery remains dependent on retaining the Trash quarantine; it must not be emptied without separate authorization.
