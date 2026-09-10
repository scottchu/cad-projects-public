"""Artifact compatibility regressions for the current P1 print bundle."""

from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import pytest

from pill_click.threemf_compat import (
    CONTENT_TYPES_NS,
    CONTENT_TYPES_PART,
    RELATIONSHIPS_NS,
    RELATIONSHIPS_PART,
    normalize_3mf_opc_wrappers,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRINT_3MF = (
    PROJECT_ROOT
    / "models"
    / "p1_hollow_magnetic_dispenser"
    / "print"
    / "p1_three_part_test_bundle.3mf"
)

CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"


def _assert_default_namespace_wrapper(data: bytes, namespace: str) -> None:
    text = data.decode("utf-8")
    assert f'xmlns="{namespace}"' in text
    assert "ns0:" not in text
    assert ET.fromstring(data).tag.startswith(f"{{{namespace}}}")


def _orca_cli() -> Path | None:
    for candidate in (
        shutil.which("orca-slicer"),
        shutil.which("OrcaSlicer"),
        "/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer",
    ):
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    return None


def test_checked_p1_3mf_has_strict_slicer_default_namespace_wrappers() -> None:
    assert PRINT_3MF.is_file()
    with ZipFile(PRINT_3MF) as package:
        assert package.testzip() is None
        assert "3D/3dmodel.model" in package.namelist()
        _assert_default_namespace_wrapper(
            package.read(CONTENT_TYPES_PART),
            CONTENT_TYPES_NS,
        )
        _assert_default_namespace_wrapper(
            package.read(RELATIONSHIPS_PART),
            RELATIONSHIPS_NS,
        )


def test_checked_p1_3mf_has_exactly_three_named_print_meshes() -> None:
    with ZipFile(PRINT_3MF) as package:
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    ns = {"m": CORE_NS}
    objects = root.findall("m:resources/m:object", ns)
    mesh_objects = [item for item in objects if item.find("m:mesh", ns) is not None]
    assembly_objects = [
        item for item in objects if item.find("m:components", ns) is not None
    ]
    assert {item.attrib["name"] for item in mesh_objects} == {
        "housing",
        "integrated_inner",
        "rear_cover",
    }
    assert len(assembly_objects) == 1
    components = assembly_objects[0].findall("m:components/m:component", ns)
    assert len(components) == 3
    assert len(root.findall("m:build/m:item", ns)) == 1


def test_3mf_wrapper_normalizer_is_idempotent(tmp_path: Path) -> None:
    copy = tmp_path / PRINT_3MF.name
    shutil.copy2(PRINT_3MF, copy)
    normalize_3mf_opc_wrappers(copy)
    normalize_3mf_opc_wrappers(copy)
    with ZipFile(copy) as package:
        assert package.testzip() is None
        _assert_default_namespace_wrapper(
            package.read(CONTENT_TYPES_PART),
            CONTENT_TYPES_NS,
        )
        _assert_default_namespace_wrapper(
            package.read(RELATIONSHIPS_PART),
            RELATIONSHIPS_NS,
        )


def test_checked_p1_3mf_loads_in_orca_cli_when_present(tmp_path: Path) -> None:
    executable = _orca_cli()
    if executable is None:
        pytest.skip("OrcaSlicer CLI is not installed")
    completed = subprocess.run(
        [
            str(executable),
            "--datadir",
            str(tmp_path / "orca-data"),
            "--info",
            str(PRINT_3MF),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    output = f"{completed.stdout}\n{completed.stderr}".lower()
    assert completed.returncode == 0, output
    assert "loading of a model file failed" not in output
    assert "run found error" not in output
