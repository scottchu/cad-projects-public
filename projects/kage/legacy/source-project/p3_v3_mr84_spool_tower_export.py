"""Fresh-process staged exporter for the MR84/profiled-spool tower successor."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from build123d import Compound, export_step, import_step

from p3_v3_mr84_spool_tower_geometry import (
    make_role_module,
    make_role_service_module,
    make_stationary_module,
    make_stationary_service_module,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_mr84_spool_tower_fix"
STAGE_ROOT = MODEL_ROOT / "staged"


def stage_path(kind: str, role: int | None = None) -> Path:
    suffix = "stationary" if role is None else ("hour", "minute", "second")[role]
    return STAGE_ROOT / f"p3_v3_mr84_{kind}_{suffix}_module.step"


def export_one(kind: str, role: int | None) -> Path:
    STAGE_ROOT.mkdir(parents=True, exist_ok=True)
    if kind == "assembled":
        shape = make_stationary_module() if role is None else make_role_module(role)
    elif kind == "service":
        shape = make_stationary_service_module() if role is None else make_role_service_module(role)
    else:
        raise ValueError(kind)
    path = stage_path(kind, role)
    export_step(shape, path)
    return path


def compose(kind: str) -> Path:
    modules = [import_step(stage_path(kind, None))]
    modules.extend(import_step(stage_path(kind, role)) for role in range(3))
    final = Compound(
        children=modules,
        label=(
            "p3_v3_mr84_COMPLETE_assembly"
            if kind == "assembled"
            else "p3_v3_mr84_COMPLETE_service_exploded"
        ),
    )
    output = MODEL_ROOT / f"p3_v3_mr84_spool_tower_{kind}.step"
    export_step(final, output)
    return output


def run_all() -> None:
    STAGE_ROOT.mkdir(parents=True, exist_ok=True)
    for kind in ("assembled", "service"):
        for role_arg in ("stationary", "0", "1", "2"):
            completed = subprocess.run(
                [sys.executable, __file__, "stage", kind, role_arg],
                cwd=ROOT,
                check=False,
            )
            if completed.returncode:
                raise SystemExit(completed.returncode)
        completed = subprocess.run(
            [sys.executable, __file__, "compose", kind], cwd=ROOT, check=False
        )
        if completed.returncode:
            raise SystemExit(completed.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="command", required=True)
    stage = subs.add_parser("stage")
    stage.add_argument("kind", choices=("assembled", "service"))
    stage.add_argument("role", choices=("stationary", "0", "1", "2"))
    compose_parser = subs.add_parser("compose")
    compose_parser.add_argument("kind", choices=("assembled", "service"))
    subs.add_parser("all")
    args = parser.parse_args()
    if args.command == "stage":
        print(export_one(args.kind, None if args.role == "stationary" else int(args.role)))
    elif args.command == "compose":
        print(compose(args.kind))
    else:
        run_all()


if __name__ == "__main__":
    main()
