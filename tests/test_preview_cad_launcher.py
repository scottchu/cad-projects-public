from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "bin/preview-cad"
ROOT_PYTHON = ROOT / ".venv/bin/python"


STUB = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
import time
import fcntl

state_path = Path(os.environ["PREVIEW_STATE"])
events_path = Path(os.environ["PREVIEW_EVENTS"])
lock_stream = state_path.with_suffix(".lock").open("a+")
fcntl.flock(lock_stream, fcntl.LOCK_EX)
name = Path(sys.argv[0]).name
args = sys.argv[1:]

def load():
    return json.loads(state_path.read_text())

def save(state):
    temporary = state_path.with_suffix(".new")
    temporary.write_text(json.dumps(state))
    os.replace(temporary, state_path)

def event(kind, **values):
    with events_path.open("a") as stream:
        stream.write(json.dumps({"kind": kind, **values}) + "\n")

def listeners(state):
    value = state.get("listener")
    if value is None:
        return []
    return value if isinstance(value, list) else [value]

def current_listener(state):
    values = listeners(state)
    return values[0] if values else None

if name == "lsof":
    state = load()
    sequence = state.get("lsof_sequence", [])
    if sequence:
        raw = sequence.pop(0)
        save(state)
        event("lsof", raw=raw)
        print(raw, end="")
    else:
        values = listeners(state)
        event("lsof", count=len(values))
        for listener in values:
            raw = listener.get("raw") or f'p{listener["pid"]}\nc{listener.get("name", "Python")}\nn127.0.0.1:3245\n'
            print(raw, end="")
    raise SystemExit(0)

if name == "ps":
    state = load()
    listener = current_listener(state)
    target = args[-1]
    leader = state.get("leader")
    if leader and target == str(leader["pid"]):
        state["leader_ps_calls"] = state.get("leader_ps_calls", 0) + 1
        action = state.get("leader_cleanup_action") if state["leader_ps_calls"] >= 2 else None
        save(state)
        if action == "absent":
            event("ps", target=target, record=None)
            raise SystemExit(1)
        command = leader["command"] if action != "drift" else "changed process generation"
        record = f'{leader["start"]} {command}'
    else:
        sequence = state.get("ps_sequence", [])
        if sequence:
            record = sequence.pop(0)
            save(state)
        elif listener and target == str(listener["pid"]):
            record = f'{listener.get("start", "Sat Aug 23 12:00:00 2026")} {listener.get("command", "python -m server_py.start_viewer")}'
        else:
            raise SystemExit(1)
    event("ps", target=target, record=record)
    print(record)
    raise SystemExit(0)

if name == "kill":
    state = load()
    event("kill", args=args)
    target = args[-1]
    signal = args[0] if args else ""
    if not target.startswith("-"):
        action = state.get("term_action", "clear")
        listener = current_listener(state)
        if action == "clear":
            state["listener"] = None
        elif action == "recover" and listener:
            listener["page"] = "ok"
        elif action == "drift" and listener:
            listener["command"] = "changed --same-pid"
        elif action == "api_loss_then_clear" and listener:
            listener["api_available"] = False
            state["clear_listener_after_sleep"] = state.get("sleep_calls", 0) + 1
        save(state)
    raise SystemExit(0)

if name == "sleep":
    state = load()
    state["sleep_calls"] = state.get("sleep_calls", 0) + 1
    drift_at = state.get("drift_after_sleep")
    listener = current_listener(state)
    if drift_at == state["sleep_calls"] and listener:
        listener["command"] = "changed --same-pid"
    if state.get("clear_listener_after_sleep") == state["sleep_calls"]:
        state["listener"] = None
    save(state)
    event("sleep", count=state["sleep_calls"])
    time.sleep(0.02)
    raise SystemExit(0)

if name == "curl":
    state = load()
    url = args[-1]
    method = "POST" if "POST" in args else "GET"
    if url.startswith("https://"):
        event("remote", url=url)
        raise SystemExit(0 if state.get("remote_ok", True) else 22)
    listener = current_listener(state)
    if "/__cad/server?" in url:
        event("api", url=url)
        if not listener or listener.get("api_available") is False:
            raise SystemExit(7)
        payload = {"app": listener.get("app", "cad-viewer"), "pid": listener.get("api_pid", listener["pid"])}
        print(json.dumps(payload))
        raise SystemExit(0)
    if "/__cad/artifact?" in url:
        key = "post" if method == "POST" else "poll"
        sequence = state.get(key, [])
        value = sequence.pop(0) if sequence else state.get(f"{key}_default", {"ok": True, "state": "ready"})
        if isinstance(value, dict) and value.get("state") == "ready" and state.get("replace_after_artifact"):
            state["listener"] = state["replace_after_artifact"]
        save(state)
        event("artifact", method=method, url=url, value=value)
        print(value if isinstance(value, str) else json.dumps(value))
        raise SystemExit(0)
    event("page", url=url)
    sequence = state.get("page_sequence", [])
    if sequence:
        page = sequence.pop(0)
        save(state)
    else:
        page = listener.get("page", "404") if listener else "404"
    if page == "ok":
        body, status = '<main id="root"></main>', 200
    elif page == "markerless":
        body, status = "plain page", 200
    else:
        body, status = "Not found", 404
    if "-w" in args:
        print(f"{body}\n__PREVIEW_STATUS__:{status}")
    else:
        print(body)
    raise SystemExit(0 if status == 200 else 22)

if name == "node":
    state = load()
    listener = state.get("start_listener", {
        "pid": 9001,
        "app": "cad-viewer",
        "api_pid": 9001,
        "page": "ok",
        "start": "Sat Aug 23 13:00:00 2026",
        "command": "root-python -m server_py.start_viewer",
    })
    state["listener"] = listener
    state["launch"] = {
        "args": args,
        "cwd": os.getcwd(),
        "python": os.environ.get("VIEWER_CAD_PYTHON"),
        "path": os.environ.get("PATH"),
        "pgid": os.getpgrp(),
    }
    if not state.get("omit_leader"):
        state["leader"] = {
            "pid": state["launch"]["pgid"],
            "start": "Sat Aug 23 12:59:59 2026",
            "command": "bundled-npm --prefix viewer run start",
        }
    save(state)
    event("node", **state["launch"])
    raise SystemExit(0)

raise SystemExit(f"unexpected stub command: {name}")
'''


@dataclass
class Rig:
    root: Path
    workspace: Path
    artifact: Path
    state_path: Path
    events_path: Path
    cache_root: Path
    bundle_dir: Path
    env: dict[str, str]

    def set_state(self, **updates):
        state = self.state()
        state.update(updates)
        self.state_path.write_text(json.dumps(state))

    def state(self):
        return json.loads(self.state_path.read_text())

    def events(self):
        if not self.events_path.exists():
            return []
        return [json.loads(line) for line in self.events_path.read_text().splitlines()]

    def clear_events(self):
        self.events_path.write_text("")

    def run(self, *args: str, cwd: Path | None = None):
        command = [str(LAUNCHER), *(args or (str(self.workspace), self.artifact.relative_to(self.workspace).as_posix()))]
        return subprocess.run(
            command,
            cwd=cwd or self.root,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=15,
        )


@pytest.fixture
def rig(tmp_path: Path) -> Rig:
    workspace = tmp_path / "workspace with spaces"
    artifact = workspace / "nested dir/model name.step"
    artifact.parent.mkdir(parents=True)
    artifact.write_bytes(b"fixture-step")

    cache_root = tmp_path / "Viewer cache with spaces"
    for version in ("0.4.9", "0.4.25", "01.9.0"):
        viewer = cache_root / version / "skills/cad-viewer/scripts/viewer"
        (viewer / "dist").mkdir(parents=True)
        (viewer / "package.json").write_text('{"scripts":{"start":"node scripts/start-viewer.mjs"}}')
        (viewer / "dist/index.html").write_text('<div id="root"></div>')
    incomplete = cache_root / "0.5.0/skills/cad-viewer/scripts/viewer"
    incomplete.mkdir(parents=True)
    (incomplete / "package.json").write_text("{}")

    commands = tmp_path / "commands"
    commands.mkdir()
    stub_source = commands / "stub.py"
    stub_source.write_text(STUB)
    stub_source.chmod(0o755)
    for name in ("curl", "lsof", "ps", "kill", "sleep"):
        (commands / name).symlink_to(stub_source)

    bundle_dir = tmp_path / "bundled node with spaces"
    bundle_dir.mkdir()
    node = bundle_dir / "node"
    node.symlink_to(stub_source)
    npm = bundle_dir / "npm"
    npm.write_text("#!/bin/sh\nexec node \"$@\"\n")
    npm.chmod(0o755)

    state_path = tmp_path / "state.json"
    events_path = tmp_path / "events.jsonl"
    state_path.write_text(json.dumps({"listener": None, "remote_ok": True}))
    events_path.write_text("")
    env = {
        **os.environ,
        "PATH": "/usr/bin:/bin",
        "PREVIEW_STATE": str(state_path),
        "PREVIEW_EVENTS": str(events_path),
        "PREVIEW_CAD_CACHE_ROOT": str(cache_root),
        "PREVIEW_CAD_BUNDLED_NPM": str(npm),
        "PREVIEW_CAD_CURL": str(commands / "curl"),
        "PREVIEW_CAD_LSOF": str(commands / "lsof"),
        "PREVIEW_CAD_PS": str(commands / "ps"),
        "PREVIEW_CAD_KILL": str(commands / "kill"),
        "PREVIEW_CAD_SLEEP": str(commands / "sleep"),
        "PREVIEW_CAD_MAX_POLLS": "5",
        "PREVIEW_CAD_CACHEBUSTER": "fixed token",
        "PREVIEW_CAD_LOG_PATH": str(tmp_path / "viewer startup.log"),
        "TAILSCALE_HOST": "viewer.example.ts.net",
    }
    env.pop("PREVIEW_CAD_NPM", None)
    return Rig(tmp_path, workspace, artifact, state_path, events_path, cache_root, bundle_dir, env)


def viewer(pid=7101, *, app="cad-viewer", api_pid=None, page="ok", command="python -m server_py.start_viewer"):
    return {
        "pid": pid,
        "app": app,
        "api_pid": pid if api_pid is None else api_pid,
        "page": page,
        "start": "Sat Aug 23 12:00:00 2026",
        "command": command,
        "name": "Python",
    }


def kinds(rig: Rig):
    return [event["kind"] for event in rig.events()]


def kill_events(rig: Rig):
    return [event for event in rig.events() if event["kind"] == "kill"]


def test_shell_syntax_and_executable_mode():
    assert subprocess.run(["sh", "-n", str(LAUNCHER)]).returncode == 0
    assert os.access(LAUNCHER, os.X_OK)
    assert "-KILL" not in LAUNCHER.read_text()


def test_all_invalid_inputs_fail_before_lsof_or_viewer_action(rig: Rig):
    outside = rig.root / "outside.step"
    outside.write_text("outside")
    escape = rig.workspace / "escape.step"
    escape.symlink_to(outside)
    missing = subprocess.run(
        [str(LAUNCHER)], cwd=rig.root, env=rig.env, text=True, capture_output=True, timeout=15
    )
    assert missing.returncode != 0 and missing.stdout == "" and rig.events() == []
    cases = [
        (str(rig.workspace), str(rig.artifact)),
        (str(rig.workspace), "../outside.step"),
        (str(rig.workspace), "escape.step"),
        ("--sha256", "F" * 64, str(rig.workspace), rig.artifact.relative_to(rig.workspace).as_posix()),
        ("--sha256", "0" * 64, str(rig.workspace), rig.artifact.relative_to(rig.workspace).as_posix()),
    ]
    for arguments in cases:
        rig.clear_events()
        result = rig.run(*arguments)
        assert result.returncode != 0
        assert result.stdout == ""
        assert rig.events() == []


def test_whitespace_cache_strict_semver_bundled_node_root_python_prefix_and_cwd(rig: Rig):
    result = rig.run()
    assert result.returncode == 0, result.stderr
    launch = rig.state()["launch"]
    selected = rig.cache_root / "0.4.25/skills/cad-viewer/scripts/viewer"
    assert launch["args"][:2] == ["--prefix", str(selected)]
    assert launch["cwd"] == str(rig.workspace.resolve())
    assert launch["python"] == str(ROOT_PYTHON)
    assert launch["path"].split(":", 1)[0] == str(rig.bundle_dir)
    assert "starting CAD Viewer runtime 0.4.25" in result.stderr
    assert "node" in kinds(rig)


def test_healthy_viewer_is_reused_without_start_or_signal(rig: Rig):
    rig.set_state(listener=viewer())
    result = rig.run()
    assert result.returncode == 0, result.stderr
    assert "reusing healthy CAD Viewer" in result.stderr
    assert "node" not in kinds(rig)
    assert kill_events(rig) == []


@pytest.mark.parametrize(
    ("listener", "message"),
    [
        (viewer(app="not-viewer"), "not CAD Viewer"),
        ([viewer(7101), viewer(7102)], "multiple listener PIDs"),
    ],
)
def test_non_viewer_and_multiple_listener_refuse_without_signal(rig: Rig, listener, message):
    rig.set_state(listener=listener)
    result = rig.run()
    assert result.returncode != 0
    assert result.stdout == ""
    assert message in result.stderr
    assert kill_events(rig) == []
    assert "node" not in kinds(rig)


def test_api_pid_mismatch_refuses_without_signal(rig: Rig):
    rig.set_state(listener=viewer(api_pid=9999))
    result = rig.run()
    assert result.returncode != 0
    assert "API/listener PID" in result.stderr
    assert kill_events(rig) == []


@pytest.mark.parametrize("drift", ["ps", "lsof"])
def test_same_pid_ps_or_full_lsof_drift_refuses_before_term(rig: Rig, drift: str):
    stale = viewer(page="404")
    updates = {"listener": stale, "page_sequence": ["404"]}
    if drift == "ps":
        updates["ps_sequence"] = [
            "Sat Aug 23 12:00:00 2026 python original",
            "Sat Aug 23 12:00:01 2026 python changed",
        ]
    else:
        updates["lsof_sequence"] = [
            "p7101\ncPython\nn127.0.0.1:3245\n",
            "p7101\ncPython\nn127.0.0.1:3245 (LISTEN changed)\n",
        ]
    rig.set_state(**updates)
    result = rig.run()
    assert result.returncode != 0
    assert "token drift before TERM" in result.stderr
    assert kill_events(rig) == []


def test_api_ready_artifact_but_spa_404_restarts_then_starts_current_runtime(rig: Rig):
    rig.set_state(listener=viewer(page="404"), term_action="clear", post=[{"ok": True, "state": "ready"}])
    result = rig.run()
    assert result.returncode == 0, result.stderr
    assert [event["args"] for event in kill_events(rig)] == [["-TERM", "7101"]]
    assert "node" in kinds(rig)
    assert rig.state()["launch"]["args"][1].endswith("0.4.25/skills/cad-viewer/scripts/viewer")
    event_kinds = kinds(rig)
    assert event_kinds.index("kill") < event_kinds.index("node") < event_kinds.index("artifact")


def test_page_recovery_immediately_before_term_reuses_without_signal(rig: Rig):
    rig.set_state(listener=viewer(page="404"), page_sequence=["404", "ok", "ok"])
    result = rig.run()
    assert result.returncode == 0, result.stderr
    assert "recovered before TERM" in result.stderr
    assert kill_events(rig) == []
    assert "node" not in kinds(rig)


def test_post_term_same_pid_token_drift_refuses_restart(rig: Rig):
    rig.set_state(listener=viewer(page="404"), term_action="keep", drift_after_sleep=1)
    result = rig.run()
    assert result.returncode != 0
    signals = [event["args"] for event in kill_events(rig)]
    assert signals == [["-TERM", "7101"]]
    assert "drift after TERM" in result.stderr
    assert "node" not in kinds(rig)


def test_same_stale_listener_past_term_timeout_fails_without_further_signal(rig: Rig):
    rig.set_state(listener=viewer(page="404"), term_action="keep")
    result = rig.run()
    assert result.returncode != 0
    assert [event["args"] for event in kill_events(rig)] == [["-TERM", "7101"]]
    assert "remained after bounded TERM wait" in result.stderr
    assert "node" not in kinds(rig)


def test_post_term_api_loss_then_port_free_starts_current_runtime(rig: Rig):
    rig.set_state(listener=viewer(page="404"), term_action="api_loss_then_clear")
    result = rig.run()
    assert result.returncode == 0, result.stderr
    assert [event["args"] for event in kill_events(rig)] == [["-TERM", "7101"]]
    assert "node" in kinds(rig)
    term_index = kinds(rig).index("kill")
    node_index = kinds(rig).index("node")
    assert not any(event["kind"] == "api" for event in rig.events()[term_index + 1 : node_index])


@pytest.mark.parametrize(
    "start_listener",
    [viewer(9001, api_pid=9999), viewer(9001, page="404")],
    ids=["api-pid-failure", "page-failure"],
)
def test_matched_owned_startup_failure_sends_group_term_only(rig: Rig, start_listener):
    rig.set_state(start_listener=start_listener)
    result = rig.run()
    assert result.returncode != 0
    assert result.stdout == ""
    pgid = str(rig.state()["launch"]["pgid"])
    signals = [event["args"] for event in kill_events(rig)]
    assert signals == [["-TERM", f"-{pgid}"]]
    assert all(args[-1].startswith("-") for args in signals)


@pytest.mark.parametrize("action", ["absent", "drift"])
def test_owned_leader_absent_or_drifted_at_cleanup_gets_no_signal(rig: Rig, action):
    rig.set_state(start_listener=viewer(9001, api_pid=9999), leader_cleanup_action=action)
    result = rig.run()
    assert result.returncode != 0
    assert result.stdout == ""
    assert kill_events(rig) == []
    expected = "is absent; no cleanup signal" if action == "absent" else "generation drifted; no cleanup signal"
    assert expected in result.stderr


def test_owned_leader_never_captured_gets_no_signal(rig: Rig):
    rig.set_state(omit_leader=True)
    result = rig.run()
    assert result.returncode != 0
    assert result.stdout == ""
    assert kill_events(rig) == []
    assert "no cleanup signal is authorized" in result.stderr


def test_ready_urls_are_encoded_cache_busted_https_and_exactly_two_lines(rig: Rig):
    rig.set_state(
        listener=viewer(),
        post=[{"ok": True, "state": "generating"}],
        poll=[{"ok": True, "state": "ready"}],
    )
    result = rig.run()
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert len(lines) == 2
    assert lines[0].startswith("http://127.0.0.1:3245/")
    assert lines[1].startswith("https://viewer.example.ts.net/")
    assert ":3245" not in lines[1]
    assert "file=nested%20dir%2Fmodel%20name.step" in lines[0]
    assert "cb=fixed%20token" in lines[0] and "cb=fixed%20token" in lines[1]
    artifact_events = [event for event in rig.events() if event["kind"] == "artifact"]
    assert [event["method"] for event in artifact_events] == ["POST", "GET"]


@pytest.mark.parametrize(
    ("post", "poll"),
    [
        ([{"ok": False, "state": "ready"}], []),
        ([{"ok": True, "state": "error"}], []),
        (["not-json"], []),
        ([{"ok": True, "state": "generating"}], [{"ok": True, "state": "generating"}] * 10),
    ],
)
def test_bad_artifact_states_fail_silently_and_cleanup_owned_group(rig: Rig, post, poll):
    rig.set_state(post=post, poll=poll)
    result = rig.run()
    assert result.returncode != 0
    assert result.stdout == ""
    pgid = str(rig.state()["launch"]["pgid"])
    signals = [event["args"] for event in kill_events(rig)]
    assert signals == [["-TERM", f"-{pgid}"]]


def test_final_listener_token_replacement_suppresses_both_urls(rig: Rig):
    rig.set_state(listener=viewer(), replace_after_artifact=viewer(7202))
    result = rig.run()
    assert result.returncode != 0
    assert result.stdout == ""
    assert "listener generation changed after artifact became ready" in result.stderr
    assert kill_events(rig) == []


def test_remote_unreachable_warns_only_after_local_ready(rig: Rig):
    rig.set_state(listener=viewer(), remote_ok=False)
    result = rig.run()
    assert result.returncode == 0
    assert len(result.stdout.splitlines()) == 2
    assert "warning: Tailscale URL is not reachable after local artifact readiness" in result.stderr
    event_kinds = kinds(rig)
    assert event_kinds[-1] == "remote"
    assert "artifact" in event_kinds[: event_kinds.index("remote")]


def test_runtime_provenance_manifest_has_six_current_hashes():
    manifest = ROOT / "projects/kage/manifests/cad-viewer-runtime-0.4.25.sha256"
    rows = []
    for line in manifest.read_text().splitlines():
        digest, path = line.split("  ", 1)
        rows.append((digest, Path(path)))
    assert len(rows) == 6
    assert len({path for _, path in rows}) == 6
    for expected, path in rows:
        assert path.is_file()
        assert sha256(path.read_bytes()).hexdigest() == expected
