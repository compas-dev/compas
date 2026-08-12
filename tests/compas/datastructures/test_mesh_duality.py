import pytest

from compas.datastructures import Mesh
from compas.datastructures.mesh.duality import mesh_dual
from compas.tolerance import TOL


@pytest.fixture
def irregular_tetrahedron():
    vertices = [[0, 0, 0], [2, 0, 0], [0, 3, 0], [0, 0, 5]]
    faces = [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def irregular_fan():
    vertices = [[0, 0, 0], [3, 0, 0], [4, 2, 0], [0, 4, 0], [1, 1, 1]]
    faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
    return Mesh.from_vertices_and_faces(vertices, faces)


def assert_point_equal(actual, expected):
    assert TOL.is_allclose(actual, expected)


@pytest.mark.parametrize("number_of_faces", [4, 6, 12])
def test_closed_mesh_dual_has_theoretical_counts_and_topology(number_of_faces):
    mesh = Mesh.from_polyhedron(number_of_faces)
    dual = mesh_dual(mesh)

    assert dual.number_of_vertices() == mesh.number_of_faces()
    assert dual.number_of_edges() == mesh.number_of_edges()
    assert dual.number_of_faces() == mesh.number_of_vertices()
    assert dual.is_valid()
    assert dual.is_closed()


def test_closed_mesh_dual_geometry_and_oriented_connectivity(irregular_tetrahedron):
    mesh = irregular_tetrahedron
    dual = mesh_dual(mesh)

    assert set(dual.vertices()) == set(mesh.faces())
    assert set(dual.faces()) == set(mesh.vertices())

    for face in mesh.faces():
        assert_point_equal(dual.vertex_coordinates(face), mesh.face_centroid(face))

    for vertex in mesh.vertices():
        assert dual.face_vertices(vertex) == mesh.vertex_faces(vertex, ordered=True)

    expected_edges = {
        frozenset((mesh.halfedge[u][v], mesh.halfedge[v][u]))
        for u, v in mesh.edges()
    }
    assert {frozenset(edge) for edge in dual.edges()} == expected_edges


def test_include_boundary_does_not_change_closed_mesh_dual(irregular_tetrahedron):
    mesh = irregular_tetrahedron
    dual = mesh_dual(mesh)
    dual_with_boundary = mesh_dual(mesh, include_boundary=True)

    assert dual_with_boundary.__data__ == dual.__data__


def test_open_mesh_dual_excludes_boundary_vertices(irregular_fan):
    mesh = irregular_fan
    dual = mesh_dual(mesh)
    interior_vertex = 4

    assert set(dual.vertices()) == set(mesh.faces())
    assert list(dual.faces()) == [interior_vertex]
    assert dual.face_vertices(interior_vertex) == mesh.vertex_faces(interior_vertex, ordered=True)
    assert dual.number_of_edges() == mesh.number_of_faces()
    assert dual.is_valid()
    assert not dual.is_closed()

    for face in mesh.faces():
        assert_point_equal(dual.vertex_coordinates(face), mesh.face_centroid(face))


def test_open_mesh_dual_includes_theoretical_boundary_elements(irregular_fan):
    mesh = irregular_fan
    dual = mesh_dual(mesh, include_boundary=True)
    boundary = mesh.vertices_on_boundary()
    if boundary[0] == boundary[-1]:
        boundary = boundary[:-1]
    boundary_edges = mesh.edges_on_boundary()

    assert dual.number_of_vertices() == mesh.number_of_faces() + len(boundary_edges) + len(boundary)
    assert dual.number_of_faces() == mesh.number_of_vertices()
    assert dual.number_of_edges() == dual.number_of_vertices() + dual.number_of_faces() - 1
    assert dual.is_valid()
    assert not dual.is_closed()

    for face in mesh.faces():
        assert_point_equal(dual.vertex_coordinates(face), mesh.face_centroid(face))

    generated_vertices = list(set(dual.vertices()) - set(mesh.faces()))
    edge_vertex = {}
    vertex_vertex = {}
    for edge in boundary_edges:
        midpoint = mesh.edge_midpoint(edge)
        matches = [
            vertex
            for vertex in generated_vertices
            if TOL.is_allclose(dual.vertex_coordinates(vertex), midpoint)
        ]
        assert len(matches) == 1
        u, v = edge
        edge_vertex[u, v] = edge_vertex[v, u] = matches[0]
    for vertex in boundary:
        point = mesh.vertex_coordinates(vertex)
        matches = [
            candidate
            for candidate in generated_vertices
            if TOL.is_allclose(dual.vertex_coordinates(candidate), point)
        ]
        assert len(matches) == 1
        vertex_vertex[vertex] = matches[0]

    interior = set(mesh.vertices()) - set(boundary)
    for vertex in interior:
        assert dual.face_vertices(vertex) == mesh.vertex_faces(vertex, ordered=True)

    boundary_faces = [face for face in dual.faces() if face not in interior]
    for vertex in boundary:
        face = next(face for face in boundary_faces if vertex_vertex[vertex] in dual.face_vertices(face))
        neighbors = mesh.vertex_neighbors(vertex, ordered=True)[::-1]
        expected = [vertex_vertex[vertex], edge_vertex[vertex, neighbors[0]]]
        expected.extend(mesh.halfedge_face((vertex, neighbor)) for neighbor in neighbors[:-1])
        expected.append(edge_vertex[vertex, neighbors[-1]])
        assert dual.face_vertices(face) == expected[::-1]


def test_mesh_dual_preserves_or_overrides_mesh_type(irregular_tetrahedron):
    class CustomMesh(Mesh):
        pass

    class OtherMesh(Mesh):
        pass

    mesh = CustomMesh.from_vertices_and_faces(
        [irregular_tetrahedron.vertex_coordinates(vertex) for vertex in irregular_tetrahedron.vertices()],
        [irregular_tetrahedron.face_vertices(face) for face in irregular_tetrahedron.faces()],
    )

    assert type(mesh_dual(mesh)) is CustomMesh
    assert type(mesh_dual(mesh, cls=OtherMesh)) is OtherMesh
