from math import pi

import numpy as np
import pytest
from scipy.sparse import isspmatrix_coo
from scipy.sparse import isspmatrix_csc
from scipy.sparse import isspmatrix_csr

from compas.datastructures import Mesh
from compas.geometry import trimesh_cotangent_laplacian_matrix
from compas.geometry import trimesh_gaussian_curvature
from compas.geometry import trimesh_gradient
from compas.geometry import trimesh_pull_points
from compas.geometry import trimesh_sample_points
from compas.geometry import trimesh_smooth_laplacian_cotangent
from compas.geometry import trimesh_vertexarea_matrix
from compas.geometry.trimesh import trimesh_gaussian_curvature as packaged_trimesh_gaussian_curvature


TRIANGLE = (
    [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
    [[0, 1, 2]],
)


def test_trimesh_gaussian_curvature_counts_each_corner_once():
    curvature = trimesh_gaussian_curvature(TRIANGLE)

    assert curvature == [pi / 2, 3 * pi / 4, 3 * pi / 4]


def test_trimesh_gaussian_curvature_uses_full_angular_deficit_at_interior_vertices():
    fan = (
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]],
        [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1]],
    )

    curvature = trimesh_gaussian_curvature(fan)

    assert curvature[0] == pytest.approx(0.0)


def test_trimesh_gradient_accepts_raw_lists_and_all_result_formats():
    array = trimesh_gradient(TRIANGLE)

    assert array.shape == (3, 3)
    assert trimesh_gradient(TRIANGLE, rtype="list") == array.tolist()
    assert isspmatrix_coo(trimesh_gradient(TRIANGLE, rtype="coo"))
    assert isspmatrix_csr(trimesh_gradient(TRIANGLE, rtype="csr"))
    assert isspmatrix_csc(trimesh_gradient(TRIANGLE, rtype="csc"))


def test_trimesh_pull_points_handles_faces_edges_and_vertices():
    pulled = trimesh_pull_points(TRIANGLE, [[0.25, 0.25, 1], [0.75, 0.75, 0], [-1, -1, 0]])

    assert np.allclose(pulled, [[0.25, 0.25, 0], [0.5, 0.5, 0], [0, 0, 0]])


def test_trimesh_sample_points_preserves_normal_direction():
    reversed_triangle = (TRIANGLE[0], [[0, 2, 1]])

    points, normals = trimesh_sample_points(reversed_triangle, 5, return_normals=True)

    assert points.shape == (5, 3)
    assert np.allclose(normals, [[0, 0, -1]] * 5)


def test_trimesh_sample_points_weights_faces_by_area(monkeypatch):
    mesh = (
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [2, 0, 0], [0, 2, 0]],
        [[0, 1, 2], [0, 3, 4]],
    )
    probabilities = None

    def choose_faces(face_count, sample_count, p):
        nonlocal probabilities
        probabilities = p
        return np.zeros(sample_count, dtype=int)

    monkeypatch.setattr(np.random, "choice", choose_faces)

    trimesh_sample_points(mesh, 3)

    assert probabilities is not None
    assert np.allclose(probabilities, [0.2, 0.8])


def test_trimesh_sample_points_rejects_mesh_without_positive_area():
    degenerate = (
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
        [[0, 1, 2]],
    )

    with pytest.raises(ValueError, match="nondegenerate triangle"):
        trimesh_sample_points(degenerate, 1)


def test_trimesh_matrices_support_noncontiguous_vertex_keys():
    mesh = Mesh()
    mesh.add_vertex(key=10, x=0, y=0, z=0)
    mesh.add_vertex(key=20, x=1, y=0, z=0)
    mesh.add_vertex(key=30, x=0, y=1, z=0)
    mesh.add_face([10, 20, 30])

    laplacian = trimesh_cotangent_laplacian_matrix(mesh, rtype="array")
    areas = trimesh_vertexarea_matrix(mesh).diagonal()

    assert np.allclose(laplacian, [[-1, 0.5, 0.5], [1, -1, 0], [1, 0, -1]])
    assert np.allclose(areas, [1 / 6, 1 / 6, 1 / 6])


def test_trimesh_cotangent_laplacian_rejects_zero_weight_sum():
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
        [[0, 1, 2]],
    )

    with pytest.raises(ValueError, match="cotangent weights"):
        trimesh_cotangent_laplacian_matrix(mesh)


def test_trimesh_smoothing_preserves_fixed_vertices():
    mesh = Mesh.from_vertices_and_faces(*TRIANGLE)
    fixed_point = mesh.vertex_coordinates(0)

    trimesh_smooth_laplacian_cotangent(mesh, fixed=[0], kmax=1)

    assert mesh.vertex_coordinates(0) == fixed_point
    assert mesh.vertex_coordinates(1) == pytest.approx([0, 0, 0])
    assert mesh.vertex_coordinates(2) == pytest.approx([0, 0, 0])


def test_trimesh_functions_are_available_from_public_namespaces():
    assert packaged_trimesh_gaussian_curvature is trimesh_gaussian_curvature
