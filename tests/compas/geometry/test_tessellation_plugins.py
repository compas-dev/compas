import subprocess
import sys
from types import SimpleNamespace
from typing import get_type_hints

import pytest

import compas.plugins
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
        (boolean_union_mesh_mesh, "A"),
        (boolean_difference_mesh_mesh, "A"),
        (boolean_intersection_mesh_mesh, "A"),
        (intersection_mesh_mesh, "A"),
        (intersection_ray_mesh, "mesh"),
        (trimesh_gaussian_curvature, "mesh"),
        (trimesh_principal_curvature, "mesh"),
        (trimesh_mean_curvature, "mesh"),
        (trimesh_geodistance, "mesh"),
        (trimesh_isolines, "mesh"),
        (trimesh_massmatrix, "mesh"),
        (trimesh_harmonic, "mesh"),
        (trimesh_lscm, "mesh"),
        (trimesh_remesh, "mesh"),
        (trimesh_remesh_constrained, "mesh"),
        (trimesh_remesh_along_isoline, "mesh"),
        (trimesh_slice, "mesh"),
    ],
)
def test_geometry_processing_contracts_accept_tessellation(operation, parameter):
    assert get_type_hints(operation)[parameter] is Tessellation


@pytest.mark.parametrize(
    "operation",
    [
        boolean_union_mesh_mesh,
        boolean_difference_mesh_mesh,
        boolean_intersection_mesh_mesh,
        trimesh_remesh,
        trimesh_remesh_constrained,
        trimesh_remesh_along_isoline,
    ],
)
def test_geometry_processing_geometry_results_are_tessellations(operation):
    assert get_type_hints(operation)["return"] is Tessellation


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


def test_geometry_result_plugin_returns_tessellation(monkeypatch):
    calls = []
    result = Tessellation(TRIANGLE.vertices, TRIANGLE.triangles)

    def implementation(A, B):
        calls.append((A, B))
        return result

    monkeypatch.setattr(
        compas.plugins.plugin_manager,
        "select",
        lambda extension_point: SimpleNamespace(id="tests.boolean", method=implementation),
    )

    assert boolean_union_mesh_mesh(TRIANGLE, TRIANGLE) is result
    assert calls == [(TRIANGLE, TRIANGLE)]


def test_raw_mesh_tuple_is_rejected_before_plugin_dispatch(monkeypatch):
    calls = []

    def select(extension_point):
        calls.append(extension_point)
        return None

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    with pytest.raises(TypeError, match="Tessellation"):
        trimesh_geodistance((TRIANGLE.vertices, TRIANGLE.triangles), 0)  # pyright: ignore[reportArgumentType]
    assert calls == []


def test_geometry_result_plugin_rejects_raw_tuple(monkeypatch):
    def implementation(mesh, target_edge_length, number_of_iterations=10, do_project=True):
        return mesh.to_vertices_and_triangles()

    monkeypatch.setattr(
        compas.plugins.plugin_manager,
        "select",
        lambda extension_point: SimpleNamespace(id="tests.remesh", method=implementation),
    )

    with pytest.raises(TypeError, match="return a Tessellation"):
        trimesh_remesh(TRIANGLE, 1.0)
