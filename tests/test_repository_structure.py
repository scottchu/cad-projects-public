import hashlib
import json
import os
import subprocess
from pathlib import Path
import re
import tomllib



ROOT = Path(__file__).resolve().parents[1]

CONTINUITY_FILES = (
    "PROJECT_STATE.md",
    "NEXT_AGENT.md",
    "PRINTING_PROFILE.md",
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
        "docs/WORKSHOP.md",
        "docs/FDM_DESIGN_RULES.md",
    )

    assert all((ROOT / path).is_file() for path in required)



def test_repository_delivery_policy_is_parseable() -> None:
    policy = tomllib.loads((ROOT / ".github/repository-policy.toml").read_text())
    delivery = policy["trunk_delivery"]

    required = {
        "branch": "main",
        "pull_request_required": True,
        "override_authority": "explicit-user-per-change",
        "server_enforcement_claimed": False,
    }
    assert required.items() <= delivery.items()
    assert "github_project_item_required" not in delivery


def test_repository_does_not_use_hosted_ci_workflows() -> None:
    workflows = ROOT / ".github/workflows"
    assert not (workflows / "validate.yml").exists()
    assert not list(workflows.glob("*.yml"))
    assert not list(workflows.glob("*.yaml"))

    for path in ("AGENTS.md", "README.md", "docs/ARCHITECTURE.md"):
        text = (ROOT / path).read_text().lower()
        assert "hosted ci workflows are not used" in text or "not hosted ci workflows" in text
        assert "does not waive testing" in text


def test_local_validation_command_contract() -> None:
    readme = (ROOT / "README.md").read_text()

    assert "Validate all currently registered workspace projects with Node.js 22 or newer:" in readme
    for command in (
        "uv lock --check",
        "uv sync --all-packages --all-groups",
        "uv run pytest tests/test_repository_structure.py",
        "npm ci --ignore-scripts",
        "git diff --exit-code -- package-lock.json",
        "npm test --workspaces --if-present",
        "npm run build --workspaces --if-present",
    ):
        assert command in readme

    for test in (
        "test_gate0_hash_p21_pivot_and_independent_stroke_derivations",
        "test_one_connected_complete_workpiece_has_required_extrema_and_90_degree_path",
        "test_three_rods_are_tangent_at_contact_then_apply_locked_wire_preload",
        "test_exact_occurrence_census_and_upward_journal_topology",
        "test_right_cap_physical_fit_contract_is_rigid_clear_and_floor_blocked",
        "test_continuous_full_domain_motion_and_removal_certificates",
        "test_motion_entry_has_exact_sixteen_stable_open_occurrences_and_envelope",
        "test_javascript_solver_matches_python_kinematics_on_dense_grid",
        "test_motion_contact_preload_directions_and_loop_are_exact",
        "test_written_step_and_model_only_3mf_roundtrip_are_valid",
    ):
        assert test in readme

    assert "projects/*/tests" not in readme





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


def test_printing_profiles_have_settings_and_evidence_sections() -> None:
    """Catch missing profiles or an empty settings-only file that loses run evidence."""
    profiles = []
    profiles.extend(
        project / "PRINTING_PROFILE.md"
        for project in (ROOT / "projects").iterdir()
        if project.is_dir()
    )
    for profile in profiles:
        assert profile.is_file(), profile
        text = profile.read_text()
        for heading in (
            "## Profile",
            "## Intended settings",
            "## Part orientation and fits",
            "## Verified slice and print runs",
            "## Concerns",
        ):
            assert heading in text, (profile, heading)
            section = text.split(heading, 1)[1].split("\n## ", 1)[0].strip()
            assert section, (profile, heading)


def test_external_workflow_binding_is_pinned_and_scoped() -> None:
    """Catch unresolved provider identities and broken policy navigation."""
    binding = json.loads((ROOT / "docs/workflows-binding.json").read_text())
    provider = binding["provider"]
    assert provider["repository"] == "https://github.com/scottchu/CAD-workbench"
    assert re.fullmatch(r"[0-9a-f]{40}", provider["revision"])
    assert re.fullmatch(r"[0-9a-f]{64}", provider["policy_manifest_sha256"])
    assert provider["policy_manifest"] == "catalog/POLICY.sha256"
    assert binding["project_repository"]["workshop"] == "docs/WORKSHOP.md"
    for name, target in binding["policies"].items():
        assert target.startswith("workflows/policies/")
        assert ".." not in Path(target).parts
        pointer = (ROOT / "docs" / f"{name}.md").read_text()
        assert target in pointer
        assert "workflows-binding.json" in pointer
    assert not (ROOT / ".agents/skills").exists()
    assert not (ROOT / "docs/templates").exists()
    assert not (ROOT / "tools/cad-viewer-service").exists()


def test_bound_workflows_match_pinned_provider_catalog() -> None:
    """Read external authority to catch IDs/recipes that merely look plausible.

    Set CAD_WORKBENCH_CHECKOUT when Workbench is not a sibling checkout.
    Only Git object reads occur; no provider runtime or network is started.
    """
    binding = json.loads((ROOT / "docs/workflows-binding.json").read_text())
    provider = binding["provider"]
    checkout = Path(os.environ.get("CAD_WORKBENCH_CHECKOUT", ROOT.parent / "CAD-workbench"))
    assert checkout.is_dir(), "Resolve pinned Workbench checkout via CAD_WORKBENCH_CHECKOUT"

    def pinned_bytes(path: str) -> bytes:
        assert not Path(path).is_absolute() and ".." not in Path(path).parts
        return subprocess.check_output(
            ["git", "-C", str(checkout), "show", f"{provider['revision']}:{path}"],
            timeout=15,
        )

    manifest = pinned_bytes(provider["policy_manifest"])
    assert hashlib.sha256(manifest).hexdigest() == provider["policy_manifest_sha256"]
    hashes = {path: digest for digest, path in (line.split("  ", 1) for line in manifest.decode().splitlines())}
    catalog_bytes = pinned_bytes(binding["catalog"])
    assert hashlib.sha256(catalog_bytes).hexdigest() == hashes[binding["catalog"]]
    catalog = json.loads(catalog_bytes)
    workflows = {workflow["id"]: workflow for workflow in catalog["workflows"]}
    for selected in binding["workflows"]:
        assert selected["id"] in workflows, selected["id"]
        assert selected["path"] == workflows[selected["id"]]["recipe"]
