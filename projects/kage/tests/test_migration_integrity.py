from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
MUTABLE_CANDIDATE_EXCLUSIONS = {
    "projects/kage/PROJECT_STATE.md",
    "projects/kage/NEXT_AGENT.md",
    "projects/kage/docs/iterations/CURRENT",
    "projects/kage/docs/iterations/2026-08-22-r0-monorepo-migration/HANDOFF.md",
    "projects/kage/docs/iterations/2026-08-22-r0-monorepo-migration/REVIEW.md",
    "projects/kage/docs/iterations/2026-08-22-r0-monorepo-migration/VALIDATION.md",
    "projects/kage/docs/iterations/2026-08-23-preview-launcher/HANDOFF.md",
    "projects/kage/docs/iterations/2026-08-23-preview-launcher/REVIEW.md",
    "projects/kage/docs/iterations/2026-08-23-preview-launcher/VALIDATION.md",
}
RUNTIME_DEBRIS_PARTS = {"__cadgen__", "__pycache__", ".pytest_cache", ".venv", "node_modules", ".uv-cache"}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    rows = []
    for line in path.read_text().splitlines():
        content_hash, relative_path = line.split("  ", 1)
        rows.append((content_hash, relative_path))
    return rows


def intended_candidate_paths() -> set[str]:
    intended = {
        ".gitignore",
        "README.md",
        "bin/preview-cad",
        "package-lock.json",
        "tests/test_preview_cad_launcher.py",
        "uv.lock",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(REPOSITORY).as_posix()
        if relative == "projects/kage/manifests/candidate.sha256":
            continue
        if relative in MUTABLE_CANDIDATE_EXCLUSIONS:
            continue
        if RUNTIME_DEBRIS_PARTS.intersection(path.parts):
            continue
        if any(part.endswith(".egg-info") for part in path.parts):
            continue
        intended.add(relative)
    return intended


def test_source_authority_manifest_keeps_original_eight_file_fingerprint():
    manifest = ROOT / "manifests/source-authority.sha256"
    assert digest(manifest) == "c838df4fb1edaa4077330db1fb8e24808a065e8738d5646cd76b26077a707cdd"
    assert len(parse_manifest(manifest)) == 8


def test_target_authority_files_match_declared_hashes():
    rows = parse_manifest(ROOT / "manifests/target-authority.sha256")
    assert len(rows) == 8
    for expected, relative_path in rows:
        assert digest(ROOT / relative_path) == expected


def test_frozen_candidate_manifest_is_sorted_and_exactly_closed():
    rows = parse_manifest(ROOT / "manifests/candidate.sha256")
    paths = [relative_path for _, relative_path in rows]
    assert paths == sorted(paths)
    assert len(paths) == len(set(paths))
    assert set(paths) == intended_candidate_paths()
    assert MUTABLE_CANDIDATE_EXCLUSIONS.isdisjoint(paths)
    assert all((REPOSITORY / path).is_file() for path in MUTABLE_CANDIDATE_EXCLUSIONS)
    assert "projects/kage/docs/iterations/2026-08-22-r0-monorepo-migration/BRIEF.md" in paths
    for expected, relative_path in rows:
        assert digest(REPOSITORY / relative_path) == expected


def test_selected_reference_artifacts_are_exact_and_bounded():
    expected = {
        "references/locked-direct-gear/p3_v3_direct_gear_race_assembled.step": "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7",
        "references/q3-r0/written/p3_v3_mvp_base_q3_identical_sector_print_qty3.3mf": "6379eea1cbf06f6abc511b411e20ac73a9d39010537ce85e5a4be0c124706489",
        "references/q3-r0/written/p3_v3_mvp_base_q3_r0_identical_sector_qty3.step": "44bf9348278c64529ac6026972014cc40d7be35969d1ecfa91ed6b5e8db9ca53",
        "references/q3-r0/written/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_assembled.step": "1d8ce2f69fa144a8ab100fc2ddbd84f8d8effd1f2b1f7751e56467155d54e900",
        "references/q3-r0/written/p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_u1_diagonal_beds.step": "d77a496947d44d1b886c4c35d00d53c0d3b6b3487d641ef9e44ea95c0090d941",
    }
    actual_binary = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".step", ".3mf", ".stl", ".glb", ".png"}
        and not RUNTIME_DEBRIS_PARTS.intersection(path.parts)
    }
    assert actual_binary == set(expected)
    for relative_path, expected_hash in expected.items():
        assert digest(ROOT / relative_path) == expected_hash


def test_active_metadata_uses_root_workspaces_and_kage_name():
    pyproject = (ROOT / "pyproject.toml").read_text()
    package = json.loads((ROOT / "package.json").read_text())
    assert 'name = "kage"' in pyproject
    assert 'requires-python = ">=3.12,<3.13"' in pyproject
    assert 'kage-clock = "kage_cli:main"' in pyproject
    assert package["name"] == "kage" and package["displayName"] == "Kage"
    assert package["dependencies"]["three"] == "0.176.0"
    assert package["devDependencies"]["esbuild"] == "0.25.8"
    assert not (ROOT / "uv.lock").exists()
    assert not (ROOT / "package-lock.json").exists()
    assert not (ROOT / ".venv").exists()
    assert not (ROOT / "node_modules").exists()


def test_normal_suite_is_integrity_only_and_compatibility_is_explicit():
    active = {path.name for path in (ROOT / "tests").glob("test_*.py")}
    compatibility = {path.name for path in (ROOT / "compatibility-tests").glob("test_*.py")}
    assert active == {"test_migration_integrity.py"}
    assert compatibility == {
        "test_carrier_pitch_section_contract.py",
        "test_cli_contract.py",
        "test_optics_contract.py",
        "test_threejs_contract.py",
    }
    assert "non-normative" in (ROOT / "compatibility-tests/README.md").read_text()
    assert (ROOT / "legacy/source-project/tests").is_dir()


def test_clean_restart_and_candidate_labels_remain_explicit():
    state = (ROOT / "PROJECT_STATE.md").read_text()
    q3 = (ROOT / "references/q3-r0/README.md").read_text()
    assert "Current restart CAD candidate: none" in state
    assert "candidate/reference only" in state
    assert "not current" in q3.lower()
    assert "not" in q3.lower() and "physically accepted" in q3.lower()
