import subprocess
import sys
from types import SimpleNamespace
from typing import get_type_hints

import numpy as np
import pytest

import compas.plugins
from compas._typing import TriangleMeshInput
from compas._typing import CoordinatesCollectionInput
from compas.geometry import Tessellation
from compas.geometry import boolean_difference_mesh_mesh
from compas.geometry import boolean_intersection_mesh_mesh
from compas.geometry import boolean_union_mesh_mesh
from compas.geometry import intersection_mesh_mesh
from compas.geometry import intersection_ray_mesh
from compas.geometry import trimesh_gaussian_curvature
from compas.geometry import trimesh_geodistance
from compas.geometry import trimesh_harmonic
from compas.geometry import trimesh_isolines
from compas.geometry import trimesh_lscm
from compas.geometry import trimesh_massmatrix
from compas.geometry import trimesh_mean_curvature
from compas.geometry import trimesh_principal_curvature
from compas.geometry import trimesh_remesh
from compas.geometry import trimesh_remesh_along_isoline
from compas.geometry import trimesh_remesh_constrained
from compas.geometry import trimesh_slice


TRIANGLE = Tessellation(
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
    [[0, 1, 2]],
)
TETRAHEDRON = (
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    [[0, 2, 1], [0, 1, 3], [1, 2, 3], [0, 3, 2]],
)


def test_geometry_package_imports_in_fresh_interpreter():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from compas.geometry import Box, Tessellation, boolean_union_mesh_mesh, trimesh_gaussian_curvature",
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("operation", "parameter"),
    [
        (intersection_ray_mesh, "mesh"),
        (trimesh_gaussian_curvature, "mesh"),
        (trimesh_principal_curvature, "mesh"),
        (trimesh_mean_curvature, "mesh"),
        (trimesh_geodistance, "mesh"),
        (trimesh_isolines, "mesh"),
        (trimesh_massmatrix, "mesh"),
        (trimesh_harmonic, "mesh"),
        (trimesh_lscm, "mesh"),
    ],
)
def test_geometry_processing_contracts_accept_tessellation(operation, parameter):
    assert get_type_hints(operation)[parameter] is Tessellation


def test_natural_result_plugin_receives_tessellation(monkeypatch):
    calls = []
    selected = []

    def implementation(mesh, source, method="exact"):
        calls.append((mesh, source, method))
        return [0.0, 1.0, 1.0]

    def select(extension_point):
        selected.append((extension_point.category, extension_point.name))
        return SimpleNamespace(id="tests.geodistance", method=implementation)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    assert trimesh_geodistance(TRIANGLE, 0) == [0.0, 1.0, 1.0]
    assert calls == [(TRIANGLE, 0, "exact")]
    assert selected == [("trimesh", "trimesh_geodistance")]


@pytest.mark.parametrize(
    "operation",
    [boolean_union_mesh_mesh, boolean_difference_mesh_mesh, boolean_intersection_mesh_mesh],
)
def test_boolean_contracts_use_structural_triangle_meshes(operation):
    hints = get_type_hints(operation)
    assert hints["A"] == TriangleMeshInput
    assert hints["B"] == TriangleMeshInput
    assert hints["return"] == TriangleMeshInput


def test_boolean_plugin_receives_and_returns_raw_mesh(monkeypatch):
    calls = []
    selected = []

    def implementation(A, B):
        calls.append((A, B))
        return A

    def select(extension_point):
        selected.append((extension_point.category, extension_point.name))
        return SimpleNamespace(id="tests.boolean", method=implementation)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    assert boolean_union_mesh_mesh(TETRAHEDRON, TETRAHEDRON) is TETRAHEDRON
    assert calls == [(TETRAHEDRON, TETRAHEDRON)]
    assert selected == [("booleans", "_boolean_union_mesh_mesh")]


def test_boolean_plugin_accepts_numpy_buffers_without_conversion(monkeypatch):
    vertices = np.asarray(TETRAHEDRON[0], dtype=np.float32, order="F")
    triangles = np.asarray(TETRAHEDRON[1], dtype=np.int64, order="F")
    vertices.flags.writeable = False
    triangles.flags.writeable = False
    mesh = (vertices, triangles)

    def implementation(A, B):
        assert A[0] is vertices
        assert A[1] is triangles
        assert B[0] is vertices
        assert B[1] is triangles
        return A

    monkeypatch.setattr(
        compas.plugins.plugin_manager,
        "select",
        lambda extension_point: SimpleNamespace(id="tests.boolean", method=implementation),
    )

    result = boolean_union_mesh_mesh(mesh, mesh)
    assert result[0] is vertices
    assert result[1] is triangles


def test_boolean_plugin_accepts_empty_result(monkeypatch):
    monkeypatch.setattr(
        compas.plugins.plugin_manager,
        "select",
        lambda extension_point: SimpleNamespace(id="tests.boolean", method=lambda A, B: ([], [])),
    )

    assert boolean_intersection_mesh_mesh(TETRAHEDRON, TETRAHEDRON) == ([], [])


@pytest.mark.parametrize(
    ("operation", "parameters"),
    [
        (intersection_mesh_mesh, ("A", "B")),
        (trimesh_slice, ("mesh",)),
    ],
)
def test_natural_result_contracts_use_structural_triangle_meshes(operation, parameters):
    hints = get_type_hints(operation)
    for parameter in parameters:
        assert hints[parameter] == TriangleMeshInput
    assert hints["return"] == CoordinatesCollectionInput


def test_mesh_intersection_dispatches_raw_buffers(monkeypatch):
    selected = []

    def implementation(A, B):
        assert A is TETRAHEDRON
        assert B is TETRAHEDRON
        return [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]

    def select(extension_point):
        selected.append((extension_point.category, extension_point.name))
        return SimpleNamespace(id="tests.intersection", method=implementation)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    assert intersection_mesh_mesh(TETRAHEDRON, TETRAHEDRON) == [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]
    assert selected == [("intersections", "_intersection_mesh_mesh")]


def test_mesh_slice_dispatches_raw_buffers(monkeypatch):
    selected = []
    planes = [([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])]

    def implementation(mesh, slicing_planes):
        assert mesh is TETRAHEDRON
        assert slicing_planes is planes
        return [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]

    def select(extension_point):
        selected.append((extension_point.category, extension_point.name))
        return SimpleNamespace(id="tests.slice", method=implementation)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    assert trimesh_slice(TETRAHEDRON, planes) == [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]]
    assert selected == [("trimesh", "_trimesh_slice")]


@pytest.mark.parametrize(
    "operation",
    [trimesh_remesh, trimesh_remesh_constrained, trimesh_remesh_along_isoline],
)
def test_remesh_contracts_use_structural_triangle_meshes(operation):
    hints = get_type_hints(operation)
    assert hints["mesh"] == TriangleMeshInput
    assert hints["return"] == TriangleMeshInput


def test_remesh_dispatches_raw_buffers(monkeypatch):
    selected = []

    def implementation(mesh, target_edge_length, number_of_iterations=10, do_project=True):
        assert mesh is TETRAHEDRON
        assert target_edge_length == 0.5
        assert number_of_iterations == 7
        assert do_project is False
        return mesh

    def select(extension_point):
        selected.append((extension_point.category, extension_point.name))
        return SimpleNamespace(id="tests.remesh", method=implementation)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    assert trimesh_remesh(TETRAHEDRON, 0.5, 7, False) is TETRAHEDRON
    assert selected == [("trimesh", "_trimesh_remesh")]


@pytest.mark.parametrize(
    ("operation", "args", "hook"),
    [
        (trimesh_remesh_constrained, (0.5, [[0, 1]], 7, False), "_trimesh_remesh_constrained"),
        (trimesh_remesh_along_isoline, ([0.0, 1.0, 1.0, 0.0], 0.5), "_trimesh_remesh_along_isoline"),
    ],
)
def test_specialized_remesh_dispatches_raw_buffers(monkeypatch, operation, args, hook):
    selected = []

    def implementation(mesh, *parameters):
        assert mesh is TETRAHEDRON
        assert parameters == args
        return mesh

    def select(extension_point):
        selected.append((extension_point.category, extension_point.name))
        return SimpleNamespace(id="tests.remesh", method=implementation)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    assert operation(TETRAHEDRON, *args) is TETRAHEDRON
    assert selected == [("trimesh", hook)]


def test_raw_mesh_tuple_is_rejected_before_plugin_dispatch(monkeypatch):
    calls = []

    def select(extension_point):
        calls.append(extension_point)
        return None

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    with pytest.raises(TypeError, match="Tessellation"):
        trimesh_geodistance((TRIANGLE.vertices, TRIANGLE.triangles), 0)  # pyright: ignore[reportArgumentType]
    assert calls == []
