# Pre-merge cleanup recovery

The cleanup is recoverable from:

`/Users/scottchu/.Trash/laifen-wave-case-premerge-cleanup-2026-09-05.46d83abc57`

`MOVE_MANIFEST.tsv` maps every original repository-relative root to its quarantine location and records its type, file/link count, directory count, byte count, tree fingerprint, and status. `PREMOVE.sha256` and `POSTMOVE.sha256` contain identical per-file hashes under original logical paths. No Trash contents were deleted.

To restore the full quarantine, stop first if any original path now exists. From the worktree root, run this reviewable Python snippet:

```bash
uv run python - <<'PY'
import csv
import shutil
from pathlib import Path
root = Path('/Users/scottchu/.codex/worktrees/4f8c/design-projects')
manifest = root / 'projects/laifen-wave-case/docs/iterations/2026-09-05-premerge-cleanup/MOVE_MANIFEST.tsv'
with manifest.open(newline='') as stream:
    for row in csv.DictReader(stream, delimiter='\t'):
        if row['status'] != 'MOVED':
            continue
        source = Path(row['quarantine_path'])
        target = root / row['original_path']
        if target.exists() or target.is_symlink():
            raise SystemExit(f'refusing to overwrite: {target}')
        if not source.exists() and not source.is_symlink():
            raise SystemExit(f'missing quarantine source: {source}')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
PY
```

After restoration, recompute hashes and compare them to `PREMOVE.sha256`. Do not empty the quarantine directory until recovery is no longer needed and the user explicitly authorizes permanent deletion.

The restore spot-check used `projects/laifen-wave-case/openscad/__pycache__`: it was restored, its tree fingerprint was verified, and it was moved back to quarantine. `RESTORE_SPOT_CHECK.txt` records the identical pre-restore, restored, and final fingerprints; the final state remains quarantined.
