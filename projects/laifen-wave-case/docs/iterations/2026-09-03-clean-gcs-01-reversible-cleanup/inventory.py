"""Deterministic CLEAN-GCS-01 inventory. It never moves or deletes files."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
PROJECT = REPO / "projects/laifen-wave-case"
OUT = Path(__file__).resolve().parent

PREVIEW_RE = re.compile(r"p2-r(?:1[3-9]|2[0-2])(?:-|$)")
TEST_RE = re.compile(r"test_p2_r(?:1[3-9]|2[0-2])(?:_|\.)")
SCRATCH_EXACT_EXCLUDES = {"presentation", "r7-recovery", "readme-refresh-receipt.md"}

# A whole-root hold is deliberately conservative: each root contains CAD source,
# STEP/BREP/GLB solids, or code that constructs/inspects CAD. It cannot be part
# of CLEAN-GCS-01 while the user has prohibited moving any CAD/STEP/OpenSCAD.
PROTECTED_CAD_SCRATCH_ROOTS = {
    "coupon-fix",
    "coupon-recovery-design",
    "end-chamfer-impl",
    "end-chamfer-validation",
    "export-evidence-design",
    "fullcase-critique",
    "fullcase-export-repair",
    "fullcase-validation",
    "generator-core",
    "generator-presentation",
    "generator-validation",
    "generator-validation-des06",
    "thread-export-validation",
    "uniform-skin-critique",
    "uniform-skin-impl",
    "uniform-skin-validation",
}


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def descendants(root: Path):
    """Yield root and descendants without following symlinks."""
    yield root
    try:
        mode = root.lstat().st_mode
    except FileNotFoundError:
        return
    if not stat.S_ISDIR(mode):
        return
    stack = [root]
    while stack:
        current = stack.pop()
        with os.scandir(current) as entries:
            children = sorted(entries, key=lambda entry: entry.name, reverse=True)
        for entry in children:
            path = Path(entry.path)
            yield path
            if entry.is_dir(follow_symlinks=False):
                stack.append(path)


def classify(roots: list[Path]):
    files: list[Path] = []
    directories: list[Path] = []
    symlinks: list[Path] = []
    special: list[Path] = []
    for root in roots:
        for path in descendants(root):
            mode = path.lstat().st_mode
            if stat.S_ISREG(mode):
                files.append(path)
            elif stat.S_ISDIR(mode):
                directories.append(path)
            elif stat.S_ISLNK(mode):
                symlinks.append(path)
            else:
                special.append(path)
    files = sorted(set(files), key=rel)
    directories = sorted(set(directories), key=rel)
    symlinks = sorted(set(symlinks), key=rel)
    special = sorted(set(special), key=rel)
    counts = {
        "files": len(files),
        "directories": len(directories),
        "symlinks": len(symlinks),
        "special": len(special),
        "fileBytes": sum(path.lstat().st_size for path in files),
        "symlinkTargetBytes": sum(len(os.readlink(path).encode()) for path in symlinks),
    }
    return files, directories, symlinks, special, counts


def root_record(path: Path) -> dict:
    files, directories, symlinks, special, counts = classify([path])
    return {"path": rel(path), **counts}


preview_roots = sorted(
    [path for path in (PROJECT / "preview").iterdir() if path.is_dir() and PREVIEW_RE.match(path.name)],
    key=rel,
)
test_roots = sorted(
    [path for path in (PROJECT / "tests").iterdir() if path.is_file() and TEST_RE.match(path.name)],
    key=rel,
)
scratch_requested = sorted(
    [
        path
        for path in (PROJECT / "scratch").iterdir()
        if path.name not in SCRATCH_EXACT_EXCLUDES and not path.name.startswith("r7-")
    ],
    key=rel,
)
scratch_protected = [path for path in scratch_requested if path.name in PROTECTED_CAD_SCRATCH_ROOTS]
scratch_proposed = [path for path in scratch_requested if path.name not in PROTECTED_CAD_SCRATCH_ROOTS]

requested_roots = preview_roots + test_roots + scratch_requested
proposed_roots = preview_roots + test_roots + scratch_proposed

with (OUT / "proposed-move-roots.txt").open("w") as stream:
    for path in sorted(proposed_roots, key=rel):
        stream.write(rel(path) + "\n")

requested = classify(requested_roots)
proposed = classify(proposed_roots)
protected = classify(scratch_protected)

inventory = {
    "schema": "clean-gcs-01-inventory-v1",
    "repo": str(REPO),
    "project": rel(PROJECT),
    "countDefinitions": {
        "directories": "root directories plus descendant directories; symlink directories are symlinks and are not followed",
        "files": "regular files only",
        "fileBytes": "sum of regular-file lstat sizes; excludes directory metadata and symlink target strings",
    },
    "requestedScope": {
        "roots": len(requested_roots),
        "previewRoots": len(preview_roots),
        "testFiles": len(test_roots),
        "scratchChildren": len(scratch_requested),
        **requested[4],
    },
    "protectedCadScratchHold": {
        "roots": len(scratch_protected),
        **protected[4],
    },
    "proposedMoveScope": {
        "roots": len(proposed_roots),
        "previewRoots": len(preview_roots),
        "testFiles": len(test_roots),
        "scratchChildren": len(scratch_proposed),
        **proposed[4],
    },
    "roots": {
        "preview": [root_record(path) for path in preview_roots],
        "tests": [root_record(path) for path in test_roots],
        "scratchProposed": [root_record(path) for path in scratch_proposed],
        "scratchProtectedCad": [root_record(path) for path in scratch_protected],
    },
}
(OUT / "inventory.json").write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")

files, directories, symlinks, special, _ = proposed
with (OUT / "proposed-move-files.sha256").open("w") as stream:
    for path in files:
        stream.write(f"{sha_file(path)}  {rel(path)}\n")
with (OUT / "proposed-move-directories.txt").open("w") as stream:
    for path in directories:
        stream.write(rel(path) + "\n")
with (OUT / "proposed-move-symlinks.tsv").open("w") as stream:
    stream.write("sha256_target\tpath\ttarget\n")
    for path in symlinks:
        target = os.readlink(path)
        digest = hashlib.sha256(target.encode()).hexdigest()
        stream.write(f"{digest}\t{rel(path)}\t{target}\n")
with (OUT / "proposed-move-special.tsv").open("w") as stream:
    stream.write("path\tmode\n")
    for path in special:
        stream.write(f"{rel(path)}\t{oct(path.lstat().st_mode)}\n")
with (OUT / "protected-cad-scratch-roots.tsv").open("w") as stream:
    stream.write("path\tfiles\tdirectories\tsymlinks\tfile_bytes\treason\n")
    for path in scratch_protected:
        record = root_record(path)
        stream.write(
            f"{record['path']}\t{record['files']}\t{record['directories']}\t"
            f"{record['symlinks']}\t{record['fileBytes']}\tcontains CAD source or STEP/BREP/GLB artifact\n"
        )

canonical_roots = [
    PROJECT / "PROJECT_STATE.md",
    PROJECT / "NEXT_AGENT.md",
    PROJECT / "README.md",
    PROJECT / "PRINTING_PROFILE.md",
    PROJECT / "pyproject.toml",
    PROJECT / "cad/p1_r7_end_chamfer",
    PROJECT / "docs/REQUIREMENTS.md",
    PROJECT / "docs/EXPERIENCE.md",
    PROJECT / "docs/WORKFLOW_DEMO.md",
    PROJECT / "docs/decisions",
    PROJECT / "docs/observations",
    PROJECT / "docs/iterations/2026-09-03-p1-r7-end-chamfer",
    PROJECT / "preview/p2-r1-makerworld-simulator",
    PROJECT / "preview/p2-r2-generic-container-simulator",
    PROJECT / "docs/iterations/2026-09-03-p2-r1-makerworld-simulator",
    PROJECT / "docs/iterations/2026-09-03-p2-r2-generic-container-simulator",
    PROJECT / "docs/iterations/2026-09-03-p2-r3-control-sync-recovery",
    PROJECT / "tests/test_makerworld_simulator.mjs",
    PROJECT / "tests/test_generic_container_simulator.mjs",
    PROJECT / "preview/p2-r10-parameter-sensitivity-recovery/core",
    PROJECT / "docs/iterations/2026-09-03-p2-r10-parameter-sensitivity-recovery",
    PROJECT / "tests/test_p2_r10_browser.py",
    PROJECT / "tests/test_p2_r10_descriptor_sensitivity.mjs",
    PROJECT / "tests/test_p2_r10_geometry.mjs",
    PROJECT / "tests/test_p2_r10_renderer.mjs",
    PROJECT / "tests/test_p2_r10_schema_coverage.mjs",
    PROJECT / "scratch/presentation",
    PROJECT / "scratch/r7-recovery",
    PROJECT / "scratch/readme-refresh-receipt.md",
]
canonical_roots.extend(sorted((PROJECT / "scratch").glob("r7-*"), key=rel))
canonical_roots = sorted({path for path in canonical_roots if path.exists() or path.is_symlink()}, key=rel)
canonical = classify(canonical_roots)
with (OUT / "canonical-key-files.sha256").open("w") as stream:
    for path in canonical[0]:
        stream.write(f"{sha_file(path)}  {rel(path)}\n")
(OUT / "canonical-key-inventory.json").write_text(
    json.dumps({"roots": [rel(path) for path in canonical_roots], **canonical[4]}, indent=2, sort_keys=True) + "\n"
)

# Find literal references from retained docs to paths proposed for quarantine.
candidate_entries = {rel(path) for part in proposed[:4] for path in part}
token_re = re.compile(r"(?:projects/laifen-wave-case/)?(?:scratch|preview|tests)/[^\s`\"'<>|)\]}:,;]+")
doc_sources = [PROJECT / "PROJECT_STATE.md", PROJECT / "NEXT_AGENT.md", PROJECT / "README.md"]
doc_sources.extend(path for path in (PROJECT / "docs").rglob("*") if path.is_file() and OUT not in path.parents)
references: set[tuple[str, str, str]] = set()
for source in sorted(doc_sources, key=rel):
    try:
        text = source.read_text(errors="ignore")
    except OSError:
        continue
    source_rel = rel(source)
    if "/2026-09-03-p2-r1-" in source_rel or "/2026-09-03-p2-r2-" in source_rel or "/2026-09-03-p2-r3-" in source_rel or source_rel.endswith(("PROJECT_STATE.md", "NEXT_AGENT.md", "README.md")):
        tier = "canonical-foundational-live"
    else:
        tier = "retained-history"
    for match in token_re.finditer(text):
        target = match.group(0)
        if not target.startswith("projects/"):
            target = "projects/laifen-wave-case/" + target
        target = target.rstrip(".")
        if target in candidate_entries:
            references.add((tier, source_rel, target))
with (OUT / "retained-reference-overlaps.tsv").open("w") as stream:
    stream.write("tier\tsource\tproposed_target\n")
    for row in sorted(references):
        stream.write("\t".join(row) + "\n")

external = Path("/Users/scottchu/Downloads/Laifen+Wave+case.3mf")
diagnostics = []
for path in [
    PROJECT / "scratch/download-design-compare/mesh-evidence.json",
    PROJECT / "scratch/download-design-compare/original-mesh-comparison.png",
    PROJECT / "scratch/download-diagnosis/triangle-evidence.json",
    PROJECT / "scratch/download-diagnosis/conditional-section.png",
]:
    diagnostics.append({"path": rel(path), "bytes": path.stat().st_size, "sha256": sha_file(path)})
(OUT / "unique-assets.json").write_text(
    json.dumps(
        {
            "diagnosticOutputs": diagnostics,
            "externalInput": {
                "path": str(external),
                "existsNow": external.is_file(),
                "bytes": external.stat().st_size if external.is_file() else None,
                "sha256": sha_file(external) if external.is_file() else None,
            },
            "policy": "Keep these outputs in quarantine indefinitely; the input is outside the repository and may disappear.",
        },
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

print(json.dumps({"requested": requested[4], "proposed": proposed[4], "protected": protected[4], "references": len(references)}, sort_keys=True))
