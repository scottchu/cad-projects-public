"""Run every P13 pytest node in a fresh process to bound OCC memory."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
TEST_FILE = "tests/test_p13_four_plate_three_rod.py"


def main() -> int:
    collected = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", TEST_FILE],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    nodeids = [line.strip() for line in collected.stdout.splitlines() if line.startswith(TEST_FILE + "::")]
    if not nodeids:
        raise RuntimeError("P13 test collection returned no node IDs")
    for index, nodeid in enumerate(nodeids, start=1):
        print(f"[{index}/{len(nodeids)}] {nodeid}", flush=True)
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", nodeid],
            cwd=ROOT,
            text=True,
        )
        if completed.returncode != 0:
            return completed.returncode
    print(f"P13 fresh-process matrix PASS: {len(nodeids)} nodes", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
