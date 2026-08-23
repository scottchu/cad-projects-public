"""Fresh-process staged exporter for the complete KAGE P3 V3 R2 model."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from build123d import Compound, export_step, import_step

from p3_v3_full_ring_r2_geometry import (
    make_role_module,
    make_role_service_module,
    make_stationary_module,
    make_stationary_service_module,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_keeper_fix"
STAGE_ROOT = MODEL_ROOT / "staged"


def _stage_path(kind: str, role: int | None = None) -> Path:
    suffix = "stationary" if role is None else ("hour", "minute", "second")[role]
    return STAGE_ROOT / f"p3_v3_keeper_fix_{kind}_{suffix}_module.step"


def export_one(kind: str, role: int | None) -> Path:
    STAGE_ROOT.mkdir(parents=True, exist_ok=True)
    if kind == "assembled":
        shape = make_stationary_module() if role is None else make_role_module(role)
    elif kind == "service":
        shape = make_stationary_service_module() if role is None else make_role_service_module(role)
    else:
        raise ValueError(kind)
    path = _stage_path(kind, role)
    export_step(shape, path)
    return path


def compose(kind: str) -> Path:
    modules = [import_step(_stage_path(kind, None))]
    modules.extend(import_step(_stage_path(kind, role)) for role in range(3))
    label = (
        "p3_v3_r2_COMPLETE_three_ring_three_motor_assembly"
        if kind == "assembled"
        else "p3_v3_r2_COMPLETE_service_exploded"
    )
    final = Compound(children=modules, label=label)
    output = MODEL_ROOT / f"p3_v3_keeper_fix_{kind}.step"
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
            [sys.executable, __file__, "compose", kind],
            cwd=ROOT,
            check=False,
        )
        if completed.returncode:
            raise SystemExit(completed.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    stage = subparsers.add_parser("stage")
    stage.add_argument("kind", choices=("assembled", "service"))
    stage.add_argument("role", choices=("stationary", "0", "1", "2"))
    compose_parser = subparsers.add_parser("compose")
    compose_parser.add_argument("kind", choices=("assembled", "service"))
    subparsers.add_parser("all")
    args = parser.parse_args()

    if args.command == "stage":
        role = None if args.role == "stationary" else int(args.role)
        print(export_one(args.kind, role))
    elif args.command == "compose":
        print(compose(args.kind))
    else:
        run_all()


if __name__ == "__main__":
    main()
