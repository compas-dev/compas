from compas.datastructures import Mesh
from compas.datastructures.mesh.slice import mesh_slice_plane
from compas.geometry import Box
from compas.geometry import Plane


def test_slice_closed_mesh_constructs_two_closed_valid_meshes():
    mesh = Mesh.from_shape(Box.from_width_height_depth(2, 2, 2))

    result = mesh_slice_plane(mesh, Plane((0, 0, 0), (1, 0, 0)))

    assert result is not None
    positive, negative = result
    assert positive.is_valid() and positive.is_closed()
    assert negative.is_valid() and negative.is_closed()
    assert positive.number_of_vertices() == 8
    assert negative.number_of_vertices() == 8
    assert positive.number_of_faces() == 6
    assert negative.number_of_faces() == 6


def test_slice_returns_none_without_polygonal_intersection():
    mesh = Mesh.from_shape(Box.from_width_height_depth(2, 2, 2))

    assert mesh_slice_plane(mesh, Plane((5, 0, 0), (1, 0, 0))) is None


def test_slice_preserves_mesh_type():
    class CustomMesh(Mesh):
        pass

    mesh = CustomMesh.from_shape(Box.from_width_height_depth(2, 2, 2))
    result = mesh_slice_plane(mesh, Plane((0, 0, 0), (1, 0, 0)))

    assert result is not None
    assert all(type(part) is CustomMesh for part in result)
