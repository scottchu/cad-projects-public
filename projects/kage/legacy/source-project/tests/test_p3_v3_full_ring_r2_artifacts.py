"""Staged/final STEP parity for the memory-bounded R2 export."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_keeper_fix"


def _inspect(path: Path) -> dict:
    script = textwrap.dedent(
        """
        import json
        import sys
        from build123d import import_step

        shape = import_step(sys.argv[1])
        bounds = shape.bounding_box()
        print(json.dumps({
            "children": len(shape.children),
            "solids": len(shape.solids()),
            "labels": [child.label for child in shape.children],
            "bounds": [
                bounds.min.X, bounds.min.Y, bounds.min.Z,
                bounds.max.X, bounds.max.Y, bounds.max.Z,
            ],
        }, sort_keys=True))
        """
    )
    completed = subprocess.run(
        [sys.executable, "-c", script, str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads([line for line in completed.stdout.splitlines() if line.strip()][-1])


def test_staged_assembled_modules_preserve_source_counts_labels_and_bounds():
    stationary = _inspect(MODEL_ROOT / "staged" / "p3_v3_keeper_fix_assembled_stationary_module.step")
    assert stationary["children"] == stationary["solids"] == 18
    assert stationary["bounds"] == pytest.approx((-150, -150, -28, 150, 150, 13.8))
    assert sum("outer_front_ring_quadrant" in label for label in stationary["labels"]) == 4

    expected_tops = (17.152, 21.1867, 24.2514)
    for role, expected_top in zip(("hour", "minute", "second"), expected_tops):
        payload = _inspect(MODEL_ROOT / "staged" / f"p3_v3_keeper_fix_assembled_{role}_module.step")
        assert payload["children"] == payload["solids"] == 54
        assert payload["bounds"][5] == pytest.approx(expected_top)
        assert sum(f"p3_v3_r2_{role}_M1_260T_quadrant" in label for label in payload["labels"]) == 4
        assert sum(f"p3_v3_r2_{role}_keeper" in label for label in payload["labels"]) == 21


@pytest.mark.parametrize(
    "name,expected_bounds",
    (
        ("assembled", (-150, -150, -29.8, 150, 150, 24.2514)),
        ("service", (-154.7755, -153.0924, -53, 155.3, 150, 71.8)),
    ),
)
def test_final_step_composes_four_named_modules_without_fusing(name, expected_bounds):
    payload = _inspect(MODEL_ROOT / f"p3_v3_keeper_fix_{name}.step")
    assert payload["children"] == 4
    assert payload["solids"] == 180
    assert payload["bounds"] == pytest.approx(expected_bounds, abs=1e-4)
    assert payload["labels"][1:] == [
        f"p3_v3_r2_hour_{'complete' if name == 'assembled' else 'service'}_role_module",
        f"p3_v3_r2_minute_{'complete' if name == 'assembled' else 'service'}_role_module",
        f"p3_v3_r2_second_{'complete' if name == 'assembled' else 'service'}_role_module",
    ]
