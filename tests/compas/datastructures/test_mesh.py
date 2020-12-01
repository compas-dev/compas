# import pytest
import os
import compas
import json
import pytest

from compas.datastructures import Mesh
from compas.datastructures import meshes_join_and_weld
from compas.geometry import Polygon
from compas.geometry import Translation


@pytest.fixture
def tet():
    return Mesh.from_polyhedron(4)


@pytest.fixture
def cube():
    return Mesh.from_polyhedron(6)


@pytest.fixture
def hexagon():
    polygon = Polygon.from_sides_and_radius_xy(6, 1)
    vertices = polygon.points
    vertices.append(polygon.centroid)
    faces = [[0, 1, 6], [1, 2, 6], [2, 3, 6], [3, 4, 6], [4, 5, 6], [5, 0, 6]]
    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def hexagongrid():
    polygon = Polygon.from_sides_and_radius_xy(6, 1)
    vertices = polygon.points
    vertices.append(polygon.centroid)
    x, y, z = zip(* vertices)
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    faces = [[0, 1, 6], [1, 2, 6], [2, 3, 6], [3, 4, 6], [4, 5, 6], [5, 0, 6]]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    meshes = []
    for i in range(2):
        T = Translation.from_vector([i * (xmax - xmin), 0, 0])
        meshes.append(mesh.transformed(T))
    for i in range(2):
        T = Translation.from_vector([i * (xmax - xmin), ymax - ymin, 0])
        meshes.append(mesh.transformed(T))
    mesh = meshes_join_and_weld(meshes)
    return mesh


@pytest.fixture
def biohazard():
    polygon = Polygon.from_sides_and_radius_xy(6, 1)
    vertices = polygon.points
    vertices.append(polygon.centroid)
    faces = [[0, 1, 6], [2, 3, 6], [4, 5, 6]]
    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def triangleboundarychain():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    faces = mesh.faces_on_boundaries()[0]
    for face in faces:
        mesh.insert_vertex(face)
    return mesh


# --------------------------------------------------------------------------
# constructors
# --------------------------------------------------------------------------

def test_from_obj():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.number_of_faces() == 25
    assert mesh.number_of_vertices() == 36
    assert mesh.number_of_edges() == 60


def test_from_ply():
    mesh = Mesh.from_ply(compas.get('bunny.ply'))
    assert mesh.number_of_faces() == 69451
    assert mesh.number_of_vertices() == 35947
    assert mesh.number_of_edges() == 104288


def test_from_stl():
    mesh = Mesh.from_stl(compas.get('cube_ascii.stl'), '6f')
    assert mesh.number_of_faces() == 8016
    assert mesh.number_of_vertices() == 4020
    assert mesh.number_of_edges() == 11368

    mesh = Mesh.from_stl(compas.get('cube_binary.stl'), '6f')
    assert mesh.number_of_faces() == 12
    assert mesh.number_of_vertices() == 8
    assert mesh.number_of_edges() == 18


def test_from_off():
    mesh = Mesh.from_off(compas.get('cube.off'))
    assert mesh.number_of_faces() == 6
    assert mesh.number_of_vertices() == 8
    assert mesh.number_of_edges() == 12


def test_from_lines():
    with open(compas.get('lines.json'), 'r') as fo:
        lines = json.load(fo)
    mesh = Mesh.from_lines(lines)
    assert mesh.number_of_faces() == 10
    assert mesh.number_of_vertices() == 32
    assert mesh.number_of_edges() == 40


def test_from_polyhedron():
    mesh = Mesh.from_polyhedron(8)
    assert mesh.number_of_faces() == 8
    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_edges() == 12


def test_from_points():
    points = [[1.0, 0.0, 3.0], [1.0, 1.25, 0.0], [1.5, 0.5, 0.0], [1.0, 10.75, 0.2], [1.0, 1.0, 4.0]]
    mesh = Mesh.from_points(points)
    assert mesh.number_of_faces() == 3
    assert mesh.number_of_vertices() == 5
    assert mesh.number_of_edges() == 7


def test_from_ploygons():
    polygon = [[[1.0, 0.0, 3.0], [1.0, 1.25, 0.0], [1.5, 0.5, 0.0]], [[1.0, 0.0, 3.0], [1.0, 5.25, 0.0], [1.5, 0.5, 0.0]]]
    mesh = Mesh.from_polygons(polygon)
    assert mesh.number_of_faces() == 2
    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_edges() == 5


# --------------------------------------------------------------------------
# converters
# --------------------------------------------------------------------------

def test_to_obj():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    mesh.to_obj('data/temp.obj')
    mesh = Mesh.from_obj(compas.get('temp.obj'))
    assert mesh.number_of_faces() == 25
    assert mesh.number_of_vertices() == 36
    assert mesh.number_of_edges() == 60
    os.remove(compas.get('temp.obj'))


def test_to_vertices_and_faces():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    vertices, faces = mesh.to_vertices_and_faces()
    assert len(vertices) == 36
    assert len(faces) == 25


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def test_copy():
    mesh1 = Mesh.from_obj(compas.get('faces.obj'))
    mesh2 = mesh1.copy()
    assert mesh1.number_of_faces() == mesh2.number_of_faces()
    assert mesh1.number_of_vertices() == mesh2.number_of_vertices()
    assert mesh1.number_of_edges() == mesh2.number_of_edges()


def test_clear():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    mesh.clear()
    assert mesh.number_of_faces() == 0
    assert mesh.number_of_vertices() == 0
    assert mesh.number_of_edges() == 0


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------

def test_add_vertex():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    v = mesh.number_of_vertices()
    key = mesh.add_vertex(x=0, y=1, z=2)
    assert mesh.vertex_attributes(key, 'xyz') == [0, 1, 2]
    assert mesh.number_of_vertices() == v + 1


def test_add_face():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    v = mesh.number_of_faces()
    key = mesh.add_face([0, 1, 2])
    assert mesh.face_vertices(key) == [0, 1, 2]
    assert mesh.number_of_faces() == v + 1


# --------------------------------------------------------------------------
# modifiers
# --------------------------------------------------------------------------

def test_delete_vertex():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    v = mesh.number_of_vertices()
    f = mesh.number_of_faces()
    e = mesh.number_of_edges()
    mesh.delete_vertex(0)
    assert mesh.number_of_vertices() == v - 1
    assert mesh.number_of_faces() == f - 4
    assert mesh.number_of_edges() == e - 4


def test_insert_vertex():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    v = mesh.number_of_vertices()
    f = mesh.number_of_faces()
    e = mesh.number_of_edges()
    mesh.insert_vertex(0)
    assert mesh.number_of_vertices() == v + 1
    assert mesh.number_of_faces() == f + 2
    assert mesh.number_of_edges() == e + 3


def test_delete_face():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    f = mesh.number_of_faces()
    mesh.delete_face(0)
    assert mesh.number_of_faces() == f - 1


def test_cull_vertices():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    mesh.add_vertex()
    v = mesh.number_of_vertices()
    mesh.cull_vertices()
    assert mesh.number_of_vertices() == v - 1


# --------------------------------------------------------------------------
# info
# --------------------------------------------------------------------------

def test_is_valid():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    assert mesh.is_valid()

    mesh_test = mesh.copy()
    del mesh_test.face[0]
    assert not mesh_test.is_valid()

    mesh_test = mesh.copy()
    del mesh_test.vertex[0]
    assert not mesh_test.is_valid()


def test_is_regular():
    mesh = Mesh.from_off(compas.get('cube.off'))
    assert mesh.is_regular()

    mesh.insert_vertex(0)
    assert not mesh.is_regular()


def test_is_manifold(cube, biohazard):
    assert cube.is_manifold()
    assert not biohazard.is_manifold()


@pytest.mark.skip(reason="no way of currently testing this")
def test_is_orientable():
    pass


def test_is_trimesh(tet, cube):
    assert tet.is_trimesh()
    assert not cube.is_trimesh()


def test_is_quadmesh(tet, cube):
    assert not tet.is_quadmesh()
    assert cube.is_quadmesh()


def test_is_empty():
    mesh = Mesh()
    assert mesh.is_empty()
    mesh.add_vertex()
    assert not mesh.is_empty()


@pytest.mark.skip(reason="euh")
def test_euler():
    pass


@pytest.mark.skip(reason="euh")
def test_genus():
    pass


# --------------------------------------------------------------------------
# accessors
# --------------------------------------------------------------------------

def test_vertices(cube):
    assert hasattr(cube.vertices(), '__next__')


def test_faces(cube):
    assert hasattr(cube.faces(), '__next__')


def test_edges(cube):
    assert hasattr(cube.edges(), '__next__')


# --------------------------------------------------------------------------
# special accessors
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# vertex topology
# --------------------------------------------------------------------------

def test_has_vertex(cube):
    assert cube.has_vertex(next(cube.vertices()))
    assert not cube.has_vertex(-1)


def test_is_vertex_connected():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.is_vertex_connected(0)
    k = mesh.add_vertex()
    assert not mesh.is_vertex_connected(k)


def test_is_vertex_on_boundary():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.is_vertex_on_boundary(0)
    assert not mesh.is_vertex_on_boundary(15)


def test_vertex_neighbors():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_neighbors(0) == [1, 6]


def test_vertex_neighborhood():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_neighborhood(0) == {1, 6}


@pytest.mark.skip(reason="euh")
def test_vertex_degree():
    pass


def test_vertex_min_degree():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_min_degree() == 2


def test_vertex_max_degree():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_max_degree() == 4


def test_vertex_faces():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    corners = list(mesh.vertices_where({'vertex_degree': 2}))
    boundary = list(mesh.vertices_where({'vertex_degree': 3}))
    internal = list(mesh.vertices_where({'vertex_degree': 4}))
    assert len(mesh.vertex_faces(corners[0])) == 1
    assert len(mesh.vertex_faces(boundary[0])) == 2
    assert len(mesh.vertex_faces(internal[0])) == 4


# --------------------------------------------------------------------------
# edge topology
# --------------------------------------------------------------------------

def test_has_edge(cube):
    assert cube.has_edge(next(cube.edges()))
    assert not cube.has_edge((-1, 0))


def test_edge_faces(cube):
    u, v = next(cube.edges())
    assert len(cube.edge_faces(u, v)) == 2


def test_is_edge_on_boundary():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.is_edge_on_boundary(0, 1)
    assert not mesh.is_edge_on_boundary(15, 16)


# --------------------------------------------------------------------------
# face topology
# --------------------------------------------------------------------------

@pytest.mark.skip(reason="euh")
def test_face_vertices():
    pass


@pytest.mark.skip(reason="euh")
def test_face_halfedges():
    pass


@pytest.mark.skip(reason="euh")
def test_face_corners():
    pass


def test_face_neighbors():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_neighborhood(0) == [1, 5]
    assert mesh.face_neighborhood(0, 2) == [0, 1, 2, 5, 6, 10]


@pytest.mark.skip(reason="euh")
def test_face_degree():
    pass


@pytest.mark.skip(reason="euh")
def test_face_min_degree():
    pass


@pytest.mark.skip(reason="euh")
def test_face_max_degree():
    pass


@pytest.mark.skip(reason="euh")
def test_face_vertex_ancestor():
    pass


@pytest.mark.skip(reason="euh")
def test_face_vertex_descendant():
    pass


def test_face_adjacency_halfedge():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_adjacency_halfedge(0, 1) == (1, 7)


def test_face_adjacency_vertices():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_adjacency_vertices(0, 1) == [1, 7]


def test_is_face_on_boundary():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.is_face_on_boundary(0)
    assert not mesh.is_face_on_boundary(8)


def test_area():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.area() == 100

    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    assert mesh.area() == 6

    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.area() == 22.802429316496635


def test_centroid():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.centroid() == [5.0, 5.0, 0.0]

    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    assert mesh.centroid() == [0.0, 0.0, 0.5]

    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.centroid() == [2.508081952064351, 2.554046390557884, 1.2687133268242006]


def test_normal():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.normal() == [0.0, 0.0, 1.0]

    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    assert mesh.normal() == [0.0, 0.0, 0.0]

    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.normal() == [-2.380849234996509e-06, 4.1056122145028854e-05, 0.8077953732329284]


# --------------------------------------------------------------------------
# vertex geometry
# --------------------------------------------------------------------------

def test_vertex_coordinates():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_coordinates(15) == [6.0, 4.0, 0.0]
    assert mesh.vertex_coordinates(15, 'yx') == [4.0, 6.0]


def test_vertex_area():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_area(0) == 1
    assert mesh.vertex_area(15) == 4


def test_vertex_laplacian():

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_laplacian(0) == [1.0, 1.0, 0.0]
    assert mesh.vertex_laplacian(1) == [0.0, 0.6666666666666666, 0.0]


def test_vertex_neighborhood_centroid():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.vertex_neighborhood_centroid(0) == [1.0, 1.0, 0.0]
    assert mesh.vertex_neighborhood_centroid(1) == [2.0, 0.6666666666666666, 0.0]


def test_vertex_normal():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.vertex_normal(0) == [-0.7875436283909406, 0.07148692938164082, 0.6120985642103861]
    assert mesh.vertex_normal(5) == [-0.482011312317331, -0.32250183520381565, 0.814651864963369]


def test_vertex_curvature():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.vertex_curvature(0) == 0.0029617825994936453
    assert mesh.vertex_curvature(5) == 0.036193074384009094


def test_face_coordinates():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_coordinates(0, 'xyz') == [
        [3.661179780960083, 2.32784628868103, 1.580246925354004], [3.775796413421631, 1.727785348892212, 1.382716059684753],
        [4.22069787979126, 1.696692585945129, 1.086419701576233], [4.109739303588867, 2.34430718421936, 1.283950567245483]]
    assert mesh.face_coordinates(0, 'zy') == [
        [1.580246925354004, 2.32784628868103], [1.382716059684753, 1.727785348892212], [1.086419701576233, 1.696692585945129],
        [1.283950567245483, 2.34430718421936]]


def test_face_normal():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_normal(0) == [0.5435358481001584, -0.16248515023849733, 0.8235091728584537]


def test_face_centroid():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_centroid(0) == [3.94185334444046, 2.024157851934433, 1.3333333134651184]


def test_face_center():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_center(0) == [3.944329439044577, 2.0258867968680776, 1.332040166602369]


def test_face_area():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_area(0) == 0.3374168482414756


def test_face_flatness():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_flatness(0) == 0.23896112582475654

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_flatness(0) == 0


def test_face_aspect_ratio():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_aspect_ratio(0) == 1.2813792520925738

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_aspect_ratio(0) == 1


def test_face_skewness():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_skewness(0) == 0.2432393485343291

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_skewness(0) == 0


def test_face_curvature():
    mesh = Mesh.from_obj(compas.get('quadmesh.obj'))
    assert mesh.face_curvature(0) == 0.0035753184898039566

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.face_curvature(0) == 0


# --------------------------------------------------------------------------
# boundary
# --------------------------------------------------------------------------

def test_vertices_on_boundaries_cube(cube):
    assert cube.vertices_on_boundaries() == []


def test_vertices_on_boundaries_hexagon(hexagon):
    assert len(hexagon.vertices_on_boundaries()) == 1
    assert len(hexagon.vertices_on_boundaries()[0]) == 7


def test_vertices_on_boundaries_hexagongrid(hexagongrid):
    assert len(hexagongrid.vertices_on_boundaries()) == 4
    assert len(hexagongrid.vertices_on_boundaries()[0]) == 9


def test_vertices_on_boundaries_biohazard(biohazard):
    assert len(biohazard.vertices_on_boundaries()) == 3
    assert len(biohazard.vertices_on_boundaries()[0]) == 4


def test_vertices_on_boundaries_triangleboundarychain(triangleboundarychain):
    assert len(triangleboundarychain.vertices_on_boundaries()) == 1
    assert len(triangleboundarychain.vertices_on_boundaries()[0]) == 21


def test_faces_on_boundaries_cube(cube):
    assert cube.faces_on_boundaries() == []


def test_faces_on_boundaries_hexagon(hexagon):
    assert len(hexagon.faces_on_boundaries()) == 1
    assert len(hexagon.faces_on_boundaries()[0]) == 6


def test_faces_on_boundaries_hexagongrid(hexagongrid):
    assert len(hexagongrid.faces_on_boundaries()) == 4
    assert len(hexagongrid.faces_on_boundaries()[0]) == 8


def test_faces_on_boundaries_biohazard(biohazard):
    assert len(biohazard.faces_on_boundaries()) == 3
    assert len(biohazard.faces_on_boundaries()[0]) == 1


def test_faces_on_boundaries_triangleboundarychain(triangleboundarychain):
    assert len(triangleboundarychain.faces_on_boundaries()) == 1
    assert len(triangleboundarychain.faces_on_boundaries()[0]) == 20


# --------------------------------------------------------------------------
# attributes
# --------------------------------------------------------------------------
