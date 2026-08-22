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


def test_orchestration_policy_has_bounded_delegation_contract() -> None:
    agents = (ROOT / "AGENTS.md").read_text().lower()
    cad = (ROOT / "docs/CAD_WORKFLOW.md").read_text().lower()

    for phrase in (
        "orchestration and delegation",
        "task dag",
        "one writer per project/source/artifact namespace",
        "at most three worker agents",
        "implementation agent must not approve its own work",
        "at most two focused repair cycles",
        "raw transcripts",
        "only gates whose declared input manifest changed",
        "distinct identities",
    ):
        assert phrase in agents or phrase in cad

    for phrase in (
        "critic and independent validation roles may run in parallel",
        "review is their join gate",
        "candidate change invalidates only downstream",
        "least expensive adequate model",
        "verified fingerprint",
        "formal independent review is their join gate",
        "sha-256 over a sorted list",
        "visual inspection",
        "runtime agent may be reused",
        "relevant frozen requirements",
        "brief.md` frozen design contract section",
    ):
        assert phrase in cad


def test_continuity_templates_capture_delegated_receipts() -> None:
    template_root = ROOT / "docs/templates/project-continuity"
    brief = (template_root / "ITERATION_BRIEF.md").read_text()
    design = (template_root / "ITERATION_DESIGN.md").read_text()
    review = (template_root / "ITERATION_REVIEW.md").read_text()
    validation = (template_root / "ITERATION_VALIDATION.md").read_text()
    handoff = (template_root / "ITERATION_HANDOFF.md").read_text()
    next_agent = (template_root / "NEXT_AGENT.md").read_text().lower()

    for heading in (
        "Frozen design contract",
        "Mutable delegated execution plan and status (when delegated)",
        "ID | Role | Deps | Immutable inputs | Exclusive write scope | Done condition",
        "Model / effort / time / token ceiling",
        "Task detail: `TASK-001`",
        "Owner identity and role:",
        "Allowed reads:",
        "Forbidden scope:",
        "Time / token / output / retry / concurrency ceilings:",
        "Include it in every dependent task's manifest.",
    ):
        assert heading in brief
    assert "Critic provenance:" in review
    assert "Independent reviewer provenance:" in review
    assert "Candidate fingerprint:" in review
    assert "Read-only status:" in review
    assert "Validator provenance:" in validation
    assert "Candidate fingerprint:" in validation
    assert "Read-only status:" in validation
    assert "Agent receipt / ledger" in handoff
    assert "Owner identity / role" in handoff
    assert "Canonical commands/results, hashes, findings/severity, requirement coverage" in handoff
    assert "Next collect/refine action" in handoff
    assert "do not duplicate" in next_agent
    assert "Frozen selected design contract" in design
    assert "Include the applicable content in every dependent task's manifest." in design


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
