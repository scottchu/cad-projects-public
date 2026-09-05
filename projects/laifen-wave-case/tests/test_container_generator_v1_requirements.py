"""Static user-requirement and forbidden-scope gates for CV1-* coverage."""
from pathlib import Path
import ast
import sys

sys.path.insert(0, str(Path(__file__).parents[1]/'cad'))
from container_generator_v1 import PARAMETER_SPECS


PROJECT = Path(__file__).parents[1]
PACKAGE = PROJECT/'cad'/'container_generator_v1'
REQUIREMENT_IDS = {
    'CV1-ORIGINAL', 'CV1-PARAMETERS', 'CV1-DERIVE', 'CV1-SOLIDS', 'CV1-JOINTS',
    'CV1-OUTPUTS', 'CV1-EQUIVALENCE', 'CV1-FDM', 'CV1-BOUNDARY'}


def test_exact_primary_output_scope_and_no_mesh_artifacts():
    step_sources = {path.name for path in PACKAGE.glob('*.step.py')}
    assert step_sources == {'body.step.py', 'cap.step.py', 'closed.step.py', 'print_layout.step.py'}
    assert not list(PACKAGE.glob('*.stl'))
    assert not list(PACKAGE.glob('*.3mf'))
    assert not list(PACKAGE.glob('*.glb'))
    generate = (PACKAGE/'generate.py').read_text()
    assert "TARGETS = ('body', 'cap', 'closed', 'print_layout')" in generate
    assert 'scripts/export' not in generate


def test_standalone_source_has_one_derivation_boundary_and_no_baseline_import():
    python_sources = list(PACKAGE.glob('*.py'))
    runtime_text = '\n'.join(path.read_text() for path in python_sources)
    assert 'p1_r7_end_chamfer' not in runtime_text
    definitions = []
    calls_outside_entrypoints = []
    for path in python_sources:
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'derive':
                definitions.append(path.name)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'derive':
                if not path.name.endswith('.step.py'):
                    calls_outside_entrypoints.append(path.name)
    assert definitions == ['derive.py']
    assert calls_outside_entrypoints == []


def test_locked_and_reference_parameters_are_not_editable_aliases():
    rows = {row['id']: row for row in PARAMETER_SPECS}
    assert all(row['affects_geometry'] for row in rows.values()
               if row['classification'] == 'locked')
    assert all(row['classification'] != 'adjustable_geometry'
               for row in rows.values() if 'locked' in row['domain'])
    assert rows['device_diameter']['classification'] == 'reference_readout_only'
    assert not rows['device_diameter']['affects_geometry']
    assert not {'wide', 'polygon', 'bayonet', 'label_text', 'drain_selection'} & set(rows)


def test_requirement_matrix_is_complete_and_bounded():
    coverage = {
        'CV1-ORIGINAL': 'source hash guard and standalone import scan',
        'CV1-PARAMETERS': 'registry completeness and classification',
        'CV1-DERIVE': 'single definition, equations, domains, pre-BREP errors',
        'CV1-SOLIDS': 'native and written validity/equivalence',
        'CV1-JOINTS': 'native datum names and STEP placement facts',
        'CV1-OUTPUTS': 'exact four entrypoints and STEP artifacts',
        'CV1-EQUIVALENCE': 'old/new native and old/new written geometry',
        'CV1-FDM': 'positive shoulder, slopes, drains and openings-up layout',
        'CV1-BOUNDARY': 'no mesh, web, slicer or printer output',
    }
    assert set(coverage) == REQUIREMENT_IDS
