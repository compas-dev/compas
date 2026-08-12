import pytest

from compas.datastructures import Mesh
from compas.datastructures.mesh.remesh import trimesh_remesh


@pytest.fixture
def triangle():
    return Mesh.from_vertices_and_faces(
        [[0, 0, 0], [2, 0, 0], [0, 2, 0]],
        [[0, 1, 2]],
    )


@pytest.mark.parametrize("target", [0.0, -1.0])
def test_remesh_rejects_nonpositive_target_length(triangle, target):
    with pytest.raises(ValueError, match="greater than zero"):
        trimesh_remesh(triangle, target)


def test_remesh_splits_long_boundary_edge(triangle):
    trimesh_remesh(
        triangle,
        target=0.5,
        kmax=1,
        allow_boundary_split=True,
        smooth=False,
    )

    assert triangle.number_of_vertices() == 4
    assert triangle.number_of_edges() == 5
    assert triangle.number_of_faces() == 2
    assert triangle.is_valid()


def test_remesh_calls_callback_after_iteration():
    mesh = Mesh.from_polyhedron(4)
    target = max(mesh.edge_length(edge) for edge in mesh.edges())
    events = []
    callback_args = {"name": "iteration"}

    def callback(current_mesh, iteration, args):
        events.append((current_mesh, iteration, args))

    trimesh_remesh(
        mesh,
        target=target,
        kmax=1,
        smooth=False,
        callback=callback,
        callback_args=callback_args,
    )

    assert events == [(mesh, 0, callback_args)]
    assert mesh.is_valid()
