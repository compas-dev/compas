import pytest

from compas.datastructures import Mesh
from compas.datastructures import mesh_conway_ambo
from compas.datastructures import mesh_conway_bevel
from compas.datastructures import mesh_conway_dual
from compas.datastructures import mesh_conway_expand
from compas.datastructures import mesh_conway_gyro
from compas.datastructures import mesh_conway_join
from compas.datastructures import mesh_conway_kis
from compas.datastructures import mesh_conway_meta
from compas.datastructures import mesh_conway_needle
from compas.datastructures import mesh_conway_ortho
from compas.datastructures import mesh_conway_snub
from compas.datastructures import mesh_conway_truncate
from compas.datastructures import mesh_conway_zip
from compas.tolerance import TOL


OPERATORS_AND_COUNTS = [
    (mesh_conway_dual, lambda V, E, F: (F, E, V)),
    (mesh_conway_join, lambda V, E, F: (V + F, 2 * E, E)),
    (mesh_conway_ambo, lambda V, E, F: (E, 2 * E, V + F)),
    (mesh_conway_kis, lambda V, E, F: (V + F, 3 * E, 2 * E)),
    (mesh_conway_needle, lambda V, E, F: (V + F, 3 * E, 2 * E)),
    (mesh_conway_zip, lambda V, E, F: (2 * E, 3 * E, V + F)),
    (mesh_conway_truncate, lambda V, E, F: (2 * E, 3 * E, V + F)),
    (mesh_conway_ortho, lambda V, E, F: (V + E + F, 4 * E, 2 * E)),
    (mesh_conway_expand, lambda V, E, F: (2 * E, 4 * E, V + E + F)),
    (mesh_conway_gyro, lambda V, E, F: (V + F + 2 * E, 5 * E, 2 * E)),
    (mesh_conway_snub, lambda V, E, F: (2 * E, 5 * E, V + F + 2 * E)),
    (mesh_conway_meta, lambda V, E, F: (V + E + F, 6 * E, 4 * E)),
    (mesh_conway_bevel, lambda V, E, F: (4 * E, 6 * E, V + E + F)),
]


@pytest.fixture
def irregular_tetrahedron():
    vertices = [[0, 0, 0], [2, 0, 0], [0, 3, 0], [0, 0, 5]]
    faces = [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
    return Mesh.from_vertices_and_faces(vertices, faces)


def assert_vertex_coordinates(mesh, expected):
    assert mesh.number_of_vertices() == len(expected)
    for vertex, xyz in zip(mesh.vertices(), expected):
        assert TOL.is_allclose(mesh.vertex_coordinates(vertex), xyz)


@pytest.mark.parametrize(
    ("operator", "counts"),
    OPERATORS_AND_COUNTS,
)
@pytest.mark.parametrize("number_of_faces", [4, 6])
def test_conway_operator_counts_and_topology(operator, counts, number_of_faces):
    mesh = Mesh.from_polyhedron(number_of_faces)
    V = mesh.number_of_vertices()
    E = mesh.number_of_edges()
    F = mesh.number_of_faces()

    result = operator(mesh)

    assert (result.number_of_vertices(), result.number_of_edges(), result.number_of_faces()) == counts(V, E, F)
    assert result.is_valid()
    assert result.is_closed()


@pytest.mark.parametrize("operator", [operator for operator, _ in OPERATORS_AND_COUNTS])
def test_conway_operator_preserves_mesh_subclass(operator):
    class CustomMesh(Mesh):
        pass

    mesh = CustomMesh.from_polyhedron(6)

    assert type(operator(mesh)) is CustomMesh


def test_conway_dual_geometry_and_oriented_connectivity(irregular_tetrahedron):
    mesh = irregular_tetrahedron
    result = mesh_conway_dual(mesh)
    faces = list(mesh.faces())
    face_vertex = {face: index for index, face in enumerate(faces)}

    assert_vertex_coordinates(result, [mesh.face_centroid(face) for face in faces])
    assert [result.face_vertices(face) for face in result.faces()] == [
        [face_vertex[face] for face in reversed(mesh.vertex_faces(vertex, ordered=True))]
        for vertex in mesh.vertices()
    ]


def test_conway_join_geometry_and_oriented_connectivity(irregular_tetrahedron):
    mesh = irregular_tetrahedron
    result = mesh_conway_join(mesh)
    vertices = list(mesh.vertices())
    faces = list(mesh.faces())
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    face_vertex = {face: len(vertices) + index for index, face in enumerate(faces)}

    assert_vertex_coordinates(
        result,
        [mesh.vertex_coordinates(vertex) for vertex in vertices] + [mesh.face_centroid(face) for face in faces],
    )
    assert [result.face_vertices(face) for face in result.faces()] == [
        [vertex_index[u], face_vertex[mesh.halfedge[v][u]], vertex_index[v], face_vertex[mesh.halfedge[u][v]]]
        for u, v in mesh.edges()
    ]


def test_conway_kis_geometry_and_oriented_connectivity(irregular_tetrahedron):
    mesh = irregular_tetrahedron
    result = mesh_conway_kis(mesh)
    vertices = list(mesh.vertices())
    faces = list(mesh.faces())
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    face_vertex = {face: len(vertices) + index for index, face in enumerate(faces)}

    assert_vertex_coordinates(
        result,
        [mesh.vertex_coordinates(vertex) for vertex in vertices] + [mesh.face_centroid(face) for face in faces],
    )
    assert [result.face_vertices(face) for face in result.faces()] == [
        [vertex_index[u], vertex_index[v], face_vertex[face]]
        for face in faces
        for u, v in mesh.face_halfedges(face)
    ]


def test_conway_gyro_geometry_and_oriented_connectivity(irregular_tetrahedron):
    mesh = irregular_tetrahedron
    result = mesh_conway_gyro(mesh)
    vertices = list(mesh.vertices())
    faces = list(mesh.faces())
    halfedges = [(u, v) for u in vertices for v in mesh.halfedge[u]]
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    face_vertex = {face: len(vertices) + index for index, face in enumerate(faces)}
    halfedge_vertex = {
        halfedge: len(vertices) + len(faces) + index for index, halfedge in enumerate(halfedges)
    }

    assert_vertex_coordinates(
        result,
        [mesh.vertex_coordinates(vertex) for vertex in vertices]
        + [mesh.face_centroid(face) for face in faces]
        + [mesh.edge_point(halfedge, t=0.33) for halfedge in halfedges],
    )
    assert [result.face_vertices(face) for face in result.faces()] == [
        [
            halfedge_vertex[u, v],
            halfedge_vertex[v, u],
            vertex_index[v],
            halfedge_vertex[v, mesh.face_vertex_descendant(face, v)],
            face_vertex[face],
        ]
        for face in faces
        for u, v in mesh.face_halfedges(face)
    ]
