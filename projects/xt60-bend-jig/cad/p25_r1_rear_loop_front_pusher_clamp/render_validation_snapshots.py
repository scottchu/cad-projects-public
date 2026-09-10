"""Render deterministic P25 validation snapshots directly from written STEP.

This is a validation-only fallback because the repository is pinned to cadgen
0.4.15, which has no ``cadgen step snapshot`` or ``cadgen viewer`` command.
It does not generate or modify candidate CAD.
"""

from __future__ import annotations

from pathlib import Path

import vtk
from build123d import import_step


CAD_DIR = Path(__file__).resolve().parent
JOBS = (
    ("p25_r1_latched_end.step", "p25_r1_latched_end_validation.png", "P25 R1  |  LATCHED END"),
    (
        "p25_r1_released_clear.step",
        "p25_r1_released_clear_validation.png",
        "P25 R1  |  RELEASED CLEAR (60 deg)",
    ),
    (
        "p25_r1_modules_exploded.step",
        "p25_r1_modules_exploded_validation.png",
        "P25 R1  |  LEFT + RIGHT MODULES EXPLODED",
    ),
)


def _leaves(shape):
    children = tuple(getattr(shape, "children", ()))
    if not children:
        return [shape]
    return [leaf for child in children for leaf in _leaves(child)]


def _style(label: str):
    name = label.lower()
    if "bottom_od4_rod" in name:
        return (0.08, 0.35, 0.95), 1.0
    if "diagonal_od4_rod" in name:
        return (0.95, 0.25, 0.05), 1.0
    if "upright_od4_rod" in name:
        return (0.05, 0.58, 0.20), 1.0
    if "front_pusher" in name:
        return (0.98, 0.58, 0.05), 1.0
    if "rear_yoke" in name:
        return (0.12, 0.28, 0.43), 1.0
    if "spring_envelope" in name:
        return (0.15, 0.72, 0.86), 0.85
    if "hinge_pin" in name:
        return (0.72, 0.76, 0.80), 1.0
    if "xt60" in name:
        return (1.0, 0.78, 0.05), 0.90
    if "workpiece" in name:
        return (0.78, 0.34, 0.08), 0.80
    if "inner_" in name or "outer_" in name or "keeper" in name:
        return (0.30, 0.33, 0.37), 0.24
    if "axle" in name:
        return (0.50, 0.52, 0.55), 0.45
    return (0.45, 0.48, 0.52), 0.90


def _actor(shape):
    vertices, triangles = shape.tessellate(0.12)
    points = vtk.vtkPoints()
    for vertex in vertices:
        points.InsertNextPoint(float(vertex.X), float(vertex.Y), float(vertex.Z))

    cells = vtk.vtkCellArray()
    for triangle in triangles:
        cell = vtk.vtkTriangle()
        for index, vertex_index in enumerate(triangle):
            cell.GetPointIds().SetId(index, int(vertex_index))
        cells.InsertNextCell(cell)

    mesh = vtk.vtkPolyData()
    mesh.SetPoints(points)
    mesh.SetPolys(cells)

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(mesh)
    normals.ComputePointNormalsOn()
    normals.ConsistencyOn()
    normals.AutoOrientNormalsOn()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    color, opacity = _style(shape.label)
    actor.GetProperty().SetColor(*color)
    actor.GetProperty().SetOpacity(opacity)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetEdgeColor(0.10, 0.11, 0.12)
    actor.GetProperty().SetLineWidth(0.45)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetMetallic(0.05)
    actor.GetProperty().SetRoughness(0.60)
    return actor


def _text(value: str, x: int, y: int, size: int, *, bold: bool = False):
    actor = vtk.vtkTextActor()
    actor.SetInput(value)
    actor.SetPosition(x, y)
    prop = actor.GetTextProperty()
    prop.SetFontSize(size)
    prop.SetColor(0.08, 0.10, 0.13)
    if bold:
        prop.BoldOn()
    return actor


def render(step_name: str, png_name: str, title: str) -> Path:
    shape = import_step(CAD_DIR / step_name)
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.96, 0.97, 0.98)
    renderer.SetBackground2(0.82, 0.86, 0.90)
    renderer.GradientBackgroundOn()
    renderer.UseFXAAOn()
    for leaf in _leaves(shape):
        renderer.AddActor(_actor(leaf))

    renderer.AddViewProp(_text(title, 44, 1115, 26, bold=True))
    renderer.AddViewProp(
        _text(
            "Blue + Green: rear yoke support   |   Orange: front pusher only",
            44,
            76,
            18,
        )
    )

    light = vtk.vtkLight()
    light.SetLightTypeToCameraLight()
    light.SetIntensity(0.90)
    renderer.AddLight(light)
    fill = vtk.vtkLight()
    fill.SetPosition(-100, -80, 140)
    fill.SetFocalPoint(0, 0, 0)
    fill.SetIntensity(0.65)
    renderer.AddLight(fill)

    window = vtk.vtkRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetSize(1600, 1200)
    window.SetMultiSamples(8)
    window.AddRenderer(renderer)

    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(0, 2, 3)
    camera.SetPosition((105, -135, 100) if "exploded" in step_name else (105, -115, 82))
    camera.SetViewUp(0, 0, 1)
    camera.ParallelProjectionOn()
    renderer.ResetCamera()
    camera.Zoom(1.28 if "exploded" in step_name else 1.16)
    window.Render()

    image = vtk.vtkWindowToImageFilter()
    image.SetInput(window)
    image.SetInputBufferTypeToRGBA()
    image.ReadFrontBufferOff()
    image.Update()
    output = CAD_DIR / png_name
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(str(output))
    writer.SetInputConnection(image.GetOutputPort())
    writer.Write()
    return output


if __name__ == "__main__":
    for job in JOBS:
        print(render(*job))
