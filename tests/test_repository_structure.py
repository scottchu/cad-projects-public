import json
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]

CONTINUITY_FILES = (
    "PROJECT_STATE.md",
    "NEXT_AGENT.md",
    "docs/REQUIREMENTS.md",
    "docs/EXPERIENCE.md",
    "docs/decisions/README.md",
    "docs/iterations/CURRENT",
)

ITERATION_FILES = (
    "BRIEF.md",
    "DESIGN.md",
    "VALIDATION.md",
    "REVIEW.md",
    "HANDOFF.md",
)


def test_root_workspace_contract() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())

    assert config["project"]["requires-python"] == ">=3.12,<3.13"
    assert config["tool"]["uv"]["package"] is False
    assert config["tool"]["uv"]["workspace"]["members"] == ["projects/[!.]*/"]


def test_root_npm_workspace_contract() -> None:
    config = json.loads((ROOT / "package.json").read_text())

    assert config["private"] is True
    assert config["workspaces"] == ["projects/*"]
    assert (ROOT / "package-lock.json").is_file()


def test_required_repository_docs_exist() -> None:
    required = (
        "README.md",
        "AGENTS.md",
        "docs/ARCHITECTURE.md",
        "docs/ADDING_A_PROJECT.md",
        "docs/PROJECT_CONTINUITY.md",
        "docs/CAD_WORKFLOW.md",
    )

    assert all((ROOT / path).is_file() for path in required)


def test_cad_policy_contains_core_evidence_categories() -> None:
    policy = (ROOT / "docs/CAD_WORKFLOW.md").read_text().lower()

    required_categories = (
        "object-collision tests",
        "math tests",
        "constraint tests",
        "user-requirement tests",
        "source-to-artifact parity",
        "physical coupon or observation gate",
    )

    assert all(category in policy for category in required_categories)


def test_workspace_members_do_not_own_environments_or_locks() -> None:
    project_root = ROOT / "projects"

    for project in (path for path in project_root.iterdir() if path.is_dir()):
        assert not (project / ".venv").exists()
        assert not (project / "uv.lock").exists()
        assert not (project / "package-lock.json").exists()


def test_workspace_members_externalize_project_continuity() -> None:
    project_root = ROOT / "projects"

    for project in (path for path in project_root.iterdir() if path.is_dir()):
        assert all((project / path).is_file() for path in CONTINUITY_FILES)

        current = (project / "docs/iterations/CURRENT").read_text().strip()
        assert current and "/" not in current and current not in {".", ".."}

        iteration = project / "docs/iterations" / current
        assert all((iteration / path).is_file() for path in ITERATION_FILES)

        state = (project / "PROJECT_STATE.md").read_text()
        for heading in ("## Baseline", "## Active iteration", "## Acceptance state", "## Next action"):
            assert heading in state
