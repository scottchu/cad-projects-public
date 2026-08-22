from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_root_workspace_contract() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())

    assert config["project"]["requires-python"] == ">=3.12,<3.13"
    assert config["tool"]["uv"]["package"] is False
    assert config["tool"]["uv"]["workspace"]["members"] == ["projects/[!.]*/"]


def test_required_repository_docs_exist() -> None:
    required = (
        "README.md",
        "AGENTS.md",
        "docs/ARCHITECTURE.md",
        "docs/ADDING_A_PROJECT.md",
    )

    assert all((ROOT / path).is_file() for path in required)


def test_workspace_members_do_not_own_environments_or_locks() -> None:
    project_root = ROOT / "projects"

    for project in (path for path in project_root.iterdir() if path.is_dir()):
        assert not (project / ".venv").exists()
        assert not (project / "uv.lock").exists()
