import json
from pathlib import Path
import re
import tomllib

import yaml


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


SKILL_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}


def _skill_document(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)(.*)$", text, re.DOTALL)
    assert match is not None
    frontmatter = yaml.safe_load(match.group(1))
    assert isinstance(frontmatter, dict)
    return frontmatter, match.group(2).strip()


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
        "docs/WORKSHOP.md",
    )

    assert all((ROOT / path).is_file() for path in required)


def test_repository_local_skills_have_valid_entrypoints() -> None:
    skills_root = ROOT / ".agents/skills"
    if not skills_root.exists():
        return

    for skill in (path for path in skills_root.iterdir() if path.is_dir()):
        entrypoint = skill / "SKILL.md"
        assert entrypoint.is_file()
        fields, body = _skill_document(entrypoint)
        assert {"name", "description"} <= set(fields)
        assert set(fields) <= SKILL_FRONTMATTER_KEYS
        assert isinstance(fields["name"], str) and fields["name"]
        assert isinstance(fields["description"], str) and fields["description"]
        assert fields["name"] == skill.name
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"])
        assert len(fields["name"]) <= 64
        assert len(fields["description"]) <= 1024
        assert body
        assert "TODO" not in entrypoint.read_text()

        interface = skill / "agents/openai.yaml"
        if interface.exists():
            assert interface.is_file()
            config = yaml.safe_load(interface.read_text())
            assert isinstance(config, dict)
            assert set(config) <= {"interface", "dependencies", "policy"}
            ui = config["interface"]
            assert isinstance(ui, dict)
            assert isinstance(ui.get("display_name"), str) and ui["display_name"]
            assert isinstance(ui.get("short_description"), str)
            assert 25 <= len(ui["short_description"]) <= 64
            assert isinstance(ui.get("default_prompt"), str)
            assert ui["default_prompt"].startswith(f"${skill.name}")


def test_repository_delivery_policy_is_parseable() -> None:
    policy = tomllib.loads((ROOT / ".github/repository-policy.toml").read_text())
    delivery = policy["trunk_delivery"]

    required = {
        "branch": "main",
        "pull_request_required": True,
        "github_project_item_required": False,
        "override_authority": "explicit-user-per-change",
        "server_enforcement_claimed": False,
    }
    assert required.items() <= delivery.items()


def test_pull_request_ci_targets_main_with_stable_job() -> None:
    workflow = yaml.load(
        (ROOT / ".github/workflows/validate.yml").read_text(), Loader=yaml.BaseLoader
    )

    assert workflow["on"]["pull_request"]["branches"] == ["main"]
    assert "workflow_dispatch" in workflow["on"]
    assert workflow["permissions"] == {"contents": "read"}
    job = workflow["jobs"]["repository-tests"]
    assert job["timeout-minutes"] == "12"
    steps = job["steps"]
    step_names = [step["name"] for step in steps]
    node_setup = next(step for step in steps if step["name"] == "Set up Node.js")
    node_index = step_names.index("Set up Node.js")
    assert node_index + 1 == step_names.index("Run XT60 supported P13 gate")
    assert node_setup["uses"] == "actions/setup-node@v4"
    assert node_setup["with"]["node-version"] == "22"
    runs = [step["run"] for step in steps if "run" in step]
    named_runs = {step["name"]: step["run"] for step in steps if "run" in step}
    assert named_runs["Run repository structure tests"] == (
        "uv run pytest tests/test_repository_structure.py"
    )
    supported = named_runs["Run XT60 supported P13 gate"]
    assert supported.startswith(
        "uv run --project projects/xt60-bend-jig pytest "
    )
    assert "test_p13_four_plate_three_rod.py::" in supported
    assert "test_p13_motion.py::" in supported
    assert "test_p13_rod_fit_coupon_3p8.py::" in supported
    assert "projects/*/tests" not in supported
    assert all("projects/*/tests" not in command for command in runs)
    assert "npm test --workspaces --if-present" in runs
    assert "npm run build --workspaces --if-present" in runs


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
