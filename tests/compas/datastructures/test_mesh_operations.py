import pytest

from compas.datastructures import Mesh
from compas.datastructures.mesh.operations.collapse import is_collapse_legal
from compas.datastructures.mesh.operations.collapse import trimesh_collapse_edge
from compas.datastructures.mesh.operations.insert import mesh_add_vertex_to_face_edge
from compas.datastructures.mesh.operations.insert import mesh_insert_vertex_on_edge
from compas.datastructures.mesh.operations.merge import mesh_merge_faces
from compas.datastructures.mesh.operations.split import mesh_split_edge
from compas.datastructures.mesh.operations.split import mesh_split_strip
from compas.datastructures.mesh.operations.split import trimesh_split_edge
from compas.datastructures.mesh.operations.substitute import mesh_substitute_vertex_in_faces
from compas.datastructures.mesh.operations.swap import trimesh_swap_edge
from compas.datastructures.mesh.operations.weld import mesh_unweld_edges
from compas.datastructures.mesh.operations.weld import mesh_unweld_vertices
from compas.tolerance import TOL

# from compas.datastructures import mesh_substitute_vertex_in_faces


@pytest.fixture
def mesh_0():
    vertices = [
        [1.0, 0.0, 0.0],
        [1.0, 2.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 1.0, 0.0],
        [0.0, 0.0, 0.0],
    ]
    faces = [[0, 1, 2], [0, 3, 1]]

    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def mesh_quads():
    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 1.0, 0.0],
    ]
    faces = [[0, 1, 2, 3], [1, 4, 5, 2]]

    return Mesh.from_vertices_and_faces(vertices, faces)


def test_add_existing_vertex_to_face_edge():
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2]],
    )
    key = mesh.add_vertex(x=0.5, y=0.0, z=0.0)
    mesh.edge_attribute((0, 1), "name", "edge")

    mesh_add_vertex_to_face_edge(mesh, key, 0, 1)

    assert mesh.face_vertices(0) == [0, key, 1, 2]
    assert mesh.face_halfedges(0) == [(0, key), (key, 1), (1, 2), (2, 0)]
    assert not mesh.edgedata
    assert mesh.is_valid()


def test_insert_new_vertex_on_shared_edge(mesh_0):
    point = mesh_0.edge_midpoint((0, 1))

    key = mesh_insert_vertex_on_edge(mesh_0, (0, 1))

    assert key == 5
    assert mesh_0.face_vertices(0) == [0, key, 1, 2]
    assert mesh_0.face_vertices(1) == [key, 0, 3, 1]
    assert TOL.is_allclose(mesh_0.vertex_coordinates(key), point)
    assert mesh_0.is_valid()


def test_insert_existing_vertex_preserves_position(mesh_0):
    point = mesh_0.vertex_coordinates(4)

    key = mesh_insert_vertex_on_edge(mesh_0, (0, 2), vkey=4)

    assert key == 4
    assert mesh_0.face_vertex_descendant(0, 2) == 4
    assert mesh_0.vertex_coordinates(4) == point
    assert mesh_0.is_valid()


# def test_mesh_substitute_vertex_in_faces(mesh_0):
#     mesh_substitute_vertex_in_faces(mesh_0, 0, 4)
#     assert 4 in mesh_0.face_vertices(0)
#     assert 0 not in mesh_0.face_vertices(0)
#     assert 4 in mesh_0.face_vertices(1)
#     assert 0 not in mesh_0.face_vertices(1)
#     mesh_substitute_vertex_in_faces(mesh_0, 4, 0, [1])
#     assert 4 in mesh_0.face_vertices(0)
#     assert 0 not in mesh_0.face_vertices(0)
#     assert 0 in mesh_0.face_vertices(1)
#     assert 4 not in mesh_0.face_vertices(1)


def test_mesh_split_face(mesh_quads):
    mesh_quads.split_face(0, 0, 2)
    assert mesh_quads.number_of_faces() == 3


def test__split_face_vertex_not_in_face(mesh_quads):
    with pytest.raises(ValueError):
        mesh_quads.split_face(0, 0, 4)


def test_mesh_split_face_vertex_nbors(mesh_quads):
    with pytest.raises(ValueError):
        mesh_quads.split_face(0, 0, 1)


# --------------------------------------------------------------------------
# collapse
# --------------------------------------------------------------------------


def test_is_collapse_legal_rejects_missing_and_boundary_edges(mesh_quads):
    assert not is_collapse_legal(mesh_quads, (0, 99))
    assert not is_collapse_legal(mesh_quads, (0, 1))


def test_mesh_collapse_edge_validates_edge_and_parameter():
    mesh = Mesh.from_polyhedron(20)
    edge = next(mesh.edges())

    with pytest.raises(ValueError):
        mesh.collapse_edge((edge[0], 99))
    with pytest.raises(ValueError):
        mesh.collapse_edge(edge, t=-0.1)
    with pytest.raises(ValueError):
        mesh.collapse_edge(edge, t=1.1)


def test_mesh_collapse_edge_respects_fixed_vertices():
    mesh = Mesh.from_polyhedron(20)
    edge = next(mesh.edges())
    vertices = mesh.number_of_vertices()

    assert mesh.collapse_edge(edge, fixed=[edge[0]]) is False
    assert mesh.number_of_vertices() == vertices
    assert mesh.has_vertex(edge[0])
    assert mesh.has_vertex(edge[1])


def test_mesh_collapse_edge_updates_topology_and_position():
    mesh = Mesh.from_polyhedron(20)
    edge = next(mesh.edges())
    point = mesh.edge_point(edge, t=0.25)
    vertices = mesh.number_of_vertices()

    assert mesh.collapse_edge(edge, t=0.25) is None
    assert mesh.number_of_vertices() == vertices - 1
    assert mesh.has_vertex(edge[0])
    assert not mesh.has_vertex(edge[1])
    assert TOL.is_allclose(mesh.vertex_coordinates(edge[0]), point)
    assert mesh.is_valid()


def test_trimesh_collapse_edge_returns_success_status():
    mesh = Mesh.from_polyhedron(20)
    edge = next(mesh.edges())

    assert trimesh_collapse_edge(mesh, edge)
    assert mesh.is_valid()
    assert mesh.is_manifold()


# --------------------------------------------------------------------------
# remaining operations
# --------------------------------------------------------------------------


def test_merge_adjacent_faces():
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2], [0, 2, 3]],
    )

    face = mesh_merge_faces(mesh, [0, 1])

    assert face is not None
    assert mesh.face_vertices(face) == [0, 1, 2, 3]
    assert mesh.number_of_faces() == 1
    assert mesh.is_valid()


def test_merge_requires_two_adjacent_faces():
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0], [2.0, 1.0, 0.0]],
        [[0, 1, 2], [3, 4, 5]],
    )

    assert mesh_merge_faces(mesh, [0, 1]) is None
    with pytest.raises(ValueError):
        mesh_merge_faces(mesh, [0])


def test_split_edge_boundary_policy(mesh_quads):
    assert mesh_split_edge(mesh_quads, (0, 1)) is None

    vertex = mesh_split_edge(mesh_quads, (0, 1), allow_boundary=True)

    assert vertex is not None
    assert mesh_quads.has_vertex(vertex)
    assert mesh_quads.is_valid()


def test_trimesh_split_edge_preserves_validity():
    mesh = Mesh.from_polyhedron(20)
    edge = next(mesh.edges())
    vertices = mesh.number_of_vertices()
    faces = mesh.number_of_faces()

    vertex = trimesh_split_edge(mesh, edge)

    assert vertex is not None
    assert mesh.number_of_vertices() == vertices + 1
    assert mesh.number_of_faces() == faces + 2
    assert mesh.is_valid()


def test_split_face_rejects_cyclic_neighbors(mesh_quads):
    with pytest.raises(ValueError):
        mesh_quads.split_face(0, 0, 3)


def test_split_strip(mesh_quads):
    vertices = mesh_split_strip(mesh_quads, (1, 2))

    assert len(vertices) == 3
    assert mesh_quads.number_of_vertices() == 9
    assert mesh_quads.number_of_faces() == 4
    assert mesh_quads.is_valid()


def test_substitute_vertex_accepts_face_iterables(mesh_0):
    faces = mesh_substitute_vertex_in_faces(mesh_0, 0, 4, (face for face in [0]))

    assert faces == [0]
    assert 4 in mesh_0.face_vertices(0)
    assert 0 not in mesh_0.face_vertices(0)
    assert 0 in mesh_0.face_vertices(1)
    assert mesh_0.is_valid()


def test_swap_edge_preserves_trimesh_topology():
    mesh = Mesh.from_polyhedron(20)
    edge = next(mesh.edges())
    faces = mesh.number_of_faces()

    result = trimesh_swap_edge(mesh, edge)

    assert result is not False
    assert mesh.number_of_faces() == faces
    assert mesh.is_valid()
    assert mesh.is_manifold()


def test_unweld_face_vertices_preserves_attributes():
    mesh = Mesh.from_polyhedron(6)
    face = next(mesh.faces())
    mesh.face_attribute(face, "name", "face")
    for vertex in mesh.face_vertices(face):
        mesh.vertex_attribute(vertex, "name", "vertex")
    vertices = mesh.number_of_vertices()

    unwelded = mesh_unweld_vertices(mesh, face)

    assert mesh.number_of_vertices() == vertices + 4
    assert mesh.face_vertices(face) == unwelded
    assert mesh.face_attribute(face, "name") == "face"
    assert all(mesh.vertex_attribute(vertex, "name") == "vertex" for vertex in unwelded)
    assert mesh.is_valid()


def test_unweld_edge_loop_opens_closed_mesh():
    mesh = Mesh.from_polyhedron(6)
    face = next(mesh.faces())
    edges = mesh.face_halfedges(face)

    mesh_unweld_edges(mesh, edges)

    assert not mesh.is_closed()
    assert mesh.edges_on_boundary()
    assert mesh.is_valid()
