"""Fail-closed consumer for content-addressed R2 releases.

This is deliberately small enough to exercise at Checkpoint A: it pins the
``current`` symlink exactly once and refuses missing, stale, malformed, or
mutable-root substitutes.  Later checkpoints add the complete manifest schema.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re


CONTENT_ID = re.compile(r"^[0-9a-f]{64}$")


class ArtifactRejected(RuntimeError):
    """Stable fail-closed rejection raised by every production consumer."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class PinnedRelease:
    content_id: str
    directory: Path

    def read_bytes(self, relative_name: str) -> bytes:
        relative = PurePosixPath(relative_name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ArtifactRejected("R2_ARTIFACT_PATH_ESCAPE")
        path = self.directory.joinpath(*relative.parts)
        if not path.is_file():
            raise ArtifactRejected("R2_ARTIFACT_PAYLOAD_MISSING")
        return path.read_bytes()


def pin_current_release(artifact_root: Path) -> PinnedRelease:
    """Read and pin ``current`` once; never inspect root-level payloads."""

    current = artifact_root / "current"
    try:
        target = os.readlink(current)
    except FileNotFoundError as exc:
        raise ArtifactRejected("R2_ARTIFACT_CURRENT_MISSING") from exc
    except OSError as exc:
        raise ArtifactRejected("R2_ARTIFACT_CURRENT_NOT_SYMLINK") from exc

    target_path = PurePosixPath(target)
    if (
        target_path.is_absolute()
        or len(target_path.parts) != 2
        or target_path.parts[0] != "releases"
        or not CONTENT_ID.fullmatch(target_path.parts[1])
    ):
        raise ArtifactRejected("R2_ARTIFACT_CURRENT_TARGET_INVALID")

    content_id = target_path.parts[1]
    directory = artifact_root / "releases" / content_id
    if not directory.is_dir():
        raise ArtifactRejected("R2_ARTIFACT_CURRENT_STALE")
    manifest_path = directory / "release_manifest.jcs.json"
    if not manifest_path.is_file():
        raise ArtifactRejected("R2_ARTIFACT_MANIFEST_MISSING")
    try:
        manifest = json.loads(manifest_path.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactRejected("R2_ARTIFACT_MANIFEST_INVALID") from exc
    if manifest.get("content_id") != content_id:
        raise ArtifactRejected("R2_ARTIFACT_CONTENT_ID_MISMATCH")
    return PinnedRelease(content_id=content_id, directory=directory)

