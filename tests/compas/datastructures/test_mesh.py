import tempfile
import pytest
import json
import random
import compas

from compas.datastructures import Mesh
from compas.geometry import Sphere
from compas.geometry import Box
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Translation

from compas.tolerance import TOL


@pytest.fixture
def halfedge():
    vertices = [None, None, None, None]
    faces = [[0, 1, 2], [0, 3, 1]]
    he = Mesh()
    for vertex in vertices:
        he.add_vertex()
    for face in faces:
        he.add_face(face)
    return he


@pytest.fixture
def vertex_key():
    return 2


@pytest.fixture
def face_key():
    return 1


@pytest.fixture
def edge_key():
    return (0, 1)


@pytest.fixture
def sphere():
    sphere = Sphere(radius=1.0)
    mesh = Mesh.from_shape(sphere, u=16, v=16)
    return mesh


def _box():
    box = Box.from_width_height_depth(2, 2, 2)
    return Mesh.from_shape(box)


# @pytest.fixture
# def box():
#     box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 1.0)
#     mesh = Mesh.from_shape(box)
#     return mesh


@pytest.fixture
def grid():
    mesh = Mesh.from_meshgrid(dx=10, nx=10)
    return mesh


def _tet():
    return Mesh.from_polyhedron(4)


@pytest.fixture
def tet():
    return _tet()


def _cube():
    return Mesh.from_polyhedron(6)


@pytest.fixture
def cube():
    return _cube()


# def _box():
#     box = Box.from_width_height_depth(2, 2, 2)
#     return Mesh.from_shape(box)


@pytest.fixture
def box():
    return _box()


def _hexagon():
    polygon = Polygon.from_sides_and_radius_xy(6, 1)
    vertices = polygon.points
    vertices.append(polygon.centroid)
    faces = [[0, 1, 6], [1, 2, 6], [2, 3, 6], [3, 4, 6], [4, 5, 6], [5, 0, 6]]
    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def hexagon():
    return _hexagon()


def _hexagongrid():
    polygon = Polygon.from_sides_and_radius_xy(6, 1)
    vertices = polygon.points
    vertices.append(polygon.centroid)
    x, y, z = zip(*vertices)
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
    mesh = meshes[0]
    for other in meshes[1:]:
        mesh.join(other)
    mesh.weld()
    return mesh


@pytest.fixture
def hexagongrid():
    return _hexagongrid()


def _biohazard():
    polygon = Polygon.from_sides_and_radius_xy(6, 1)
    vertices = polygon.points
    vertices.append(polygon.centroid)
    faces = [[0, 1, 6], [2, 3, 6], [4, 5, 6]]
    return Mesh.from_vertices_and_faces(vertices, faces)


@pytest.fixture
def biohazard():
    return _biohazard()


def _triangleboundarychain():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    faces = mesh.faces_on_boundaries()[0]
    for face in faces:
        mesh.insert_vertex(face)
    return mesh


@pytest.fixture
def triangleboundarychain():
    return _triangleboundarychain()


# --------------------------------------------------------------------------
# constructors
# --------------------------------------------------------------------------


def test_constructor():
    mesh = Mesh()
    a = mesh.add_vertex()
    b = mesh.add_vertex(x=1.0)
    c = mesh.add_vertex(x=1.0, y=1.0)
    d = mesh.add_vertex(y=1.0)
    mesh.add_face([a, b, c, d])
    assert mesh.vertex_coordinates(a) == [0.0, 0.0, 0.0]
    assert mesh.vertex_coordinates(b) == [1.0, 0.0, 0.0]
    assert mesh.vertex_coordinates(c) == [1.0, 1.0, 0.0]
    assert mesh.vertex_coordinates(d) == [0.0, 1.0, 0.0]
    assert mesh.vertex_coordinates(a) == mesh.vertex_attributes(a, "xyz")
    assert mesh.vertex_coordinates(b) == mesh.vertex_attributes(b, "xyz")
    assert mesh.vertex_coordinates(c) == mesh.vertex_attributes(c, "xyz")
    assert mesh.vertex_coordinates(d) == mesh.vertex_attributes(d, "xyz")


def test_from_obj():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.number_of_faces() == 25
    assert mesh.number_of_vertices() == 36
    assert mesh.number_of_edges() == 60


def test_from_ply():
    mesh = Mesh.from_ply(compas.get("tubemesh.ply"))
    assert mesh.number_of_faces() == 342
    assert mesh.number_of_vertices() == 200
    assert mesh.number_of_edges() == 541


def test_from_stl():
    mesh = Mesh.from_stl(compas.get("cube_ascii.stl"), precision=6)
    assert mesh.number_of_faces() == 8016
    assert mesh.number_of_vertices() == 4020
    assert mesh.number_of_edges() == 11368

    mesh = Mesh.from_stl(compas.get("cube_binary.stl"), precision=6)
    assert mesh.number_of_faces() == 12
    assert mesh.number_of_vertices() == 8
    assert mesh.number_of_edges() == 18


def test_from_off():
    mesh = Mesh.from_off(compas.get("cube.off"))
    assert mesh.number_of_faces() == 6
    assert mesh.number_of_vertices() == 8
    assert mesh.number_of_edges() == 12


def test_from_lines():
    lines = compas.json_load(compas.get("lines.json"))
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
    if not compas.IPY:
        points = [
            [1.0, 0.0, 3.0],
            [1.0, 1.25, 0.0],
            [1.5, 0.5, 0.0],
            [1.0, 10.75, 0.2],
            [1.0, 1.0, 4.0],
        ]
        mesh = Mesh.from_points(points)
        assert mesh.number_of_faces() == 3
        assert mesh.number_of_vertices() == 5
        assert mesh.number_of_edges() == 7


def test_from_ploygons():
    polygon = [
        [[1.0, 0.0, 3.0], [1.0, 1.25, 0.0], [1.5, 0.5, 0.0]],
        [[1.0, 0.0, 3.0], [1.0, 5.25, 0.0], [1.5, 0.5, 0.0]],
    ]
    mesh = Mesh.from_polygons(polygon)
    assert mesh.number_of_faces() == 2
    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_edges() == 5


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "halfedge",
    [
        _tet(),
        _cube(),
        _box(),
        _hexagon(),
        _hexagongrid(),
        _triangleboundarychain(),
    ],
)
def test_mesh_data(halfedge):
    other = Mesh.__from_data__(json.loads(json.dumps(halfedge.__data__)))

    assert halfedge.__data__ == other.__data__
    assert halfedge.default_vertex_attributes == other.default_vertex_attributes
    assert halfedge.default_edge_attributes == other.default_edge_attributes
    assert halfedge.default_face_attributes == other.default_face_attributes
    assert halfedge.number_of_vertices() == other.number_of_vertices()
    assert halfedge.number_of_edges() == other.number_of_edges()
    assert halfedge.number_of_faces() == other.number_of_faces()

    if not compas.IPY:
        assert Mesh.validate_data(halfedge.__data__)
        assert Mesh.validate_data(other.__data__)


# --------------------------------------------------------------------------
# converters
# --------------------------------------------------------------------------


def test_to_obj():
    _, fname = tempfile.mkstemp(suffix=".obj", prefix="temp_mesh_test")
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    mesh.to_obj(fname)
    mesh = Mesh.from_obj(fname)
    assert mesh.number_of_faces() == 25
    assert mesh.number_of_vertices() == 36
    assert mesh.number_of_edges() == 60


def test_to_vertices_and_faces():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    vertices, faces = mesh.to_vertices_and_faces()
    assert len(vertices) == 36
    assert len(faces) == 25


def test_to_vertices_and_faces_triangulated():
    # tri
    mesh = Mesh.from_shape(Polyhedron.from_platonicsolid(4))
    vertices, faces = mesh.to_vertices_and_faces(triangulated=True)
    assert len(vertices) == 4
    assert len(faces) == 4

    # quad
    mesh = Mesh.from_shape(Polyhedron.from_platonicsolid(6))
    vertices, faces = mesh.to_vertices_and_faces(triangulated=True)
    assert len(vertices) == 8
    assert len(faces) == 12

    # ngon
    mesh = Mesh.from_shape(Polyhedron.from_platonicsolid(12))
    vertices, faces = mesh.to_vertices_and_faces(triangulated=True)
    assert len(vertices) == 32
    assert len(faces) == 60


def test_to_lines():
    lines = compas.json_load(compas.get("lines.json"))
    mesh = Mesh.from_lines(lines)
    lines = mesh.to_lines()
    assert len(lines) == mesh.number_of_edges()


def test_to_points():
    # tri
    mesh = Mesh.from_shape(Polyhedron.from_platonicsolid(4))
    points = mesh.to_points()
    assert len(points) == 4

    # quad
    mesh = Mesh.from_shape(Polyhedron.from_platonicsolid(6))
    points = mesh.to_points()
    assert len(points) == 8

    # ngon
    mesh = Mesh.from_shape(Polyhedron.from_platonicsolid(12))
    points = mesh.to_points()
    assert len(points) == 20


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def test_copy():
    mesh1 = Mesh.from_obj(compas.get("faces.obj"))
    mesh2 = mesh1.copy()
    assert mesh1.number_of_faces() == mesh2.number_of_faces()
    assert mesh1.number_of_vertices() == mesh2.number_of_vertices()
    assert mesh1.number_of_edges() == mesh2.number_of_edges()


def test_clear():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    mesh.clear()
    assert mesh.number_of_faces() == 0
    assert mesh.number_of_vertices() == 0
    assert mesh.number_of_edges() == 0


# --------------------------------------------------------------------------
# samples
# --------------------------------------------------------------------------


def test_vertex_sample(halfedge):
    for vertex in halfedge.vertex_sample():
        assert halfedge.has_vertex(vertex)
    for vertex in halfedge.vertex_sample(size=halfedge.number_of_vertices()):
        assert halfedge.has_vertex(vertex)


def test_edge_sample(halfedge):
    for edge in halfedge.edge_sample():
        assert halfedge.has_edge(edge)
    for edge in halfedge.edge_sample(size=halfedge.number_of_edges()):
        assert halfedge.has_edge(edge)


def test_face_sample(halfedge):
    for face in halfedge.face_sample():
        assert halfedge.has_face(face)
    for face in halfedge.face_sample(size=halfedge.number_of_faces()):
        assert halfedge.has_face(face)


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------


def test_add_vertex():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    v = mesh.number_of_vertices()
    key = mesh.add_vertex(x=0, y=1, z=2)
    assert mesh.vertex_attributes(key, "xyz") == [0, 1, 2]
    assert mesh.number_of_vertices() == v + 1


def test_add_face():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    v = mesh.number_of_faces()
    key = mesh.add_face([0, 1, 2])
    assert mesh.face_vertices(key) == [0, 1, 2]
    assert mesh.number_of_faces() == v + 1


# --------------------------------------------------------------------------
# modifiers
# --------------------------------------------------------------------------


def test_delete_vertex():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    v = mesh.number_of_vertices()
    f = mesh.number_of_faces()
    e = mesh.number_of_edges()
    mesh.delete_vertex(0)
    assert mesh.number_of_vertices() == v - 1
    assert mesh.number_of_faces() == f - 4
    assert mesh.number_of_edges() == e - 4


def test_insert_vertex():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    v = mesh.number_of_vertices()
    f = mesh.number_of_faces()
    e = mesh.number_of_edges()
    mesh.insert_vertex(0)
    assert mesh.number_of_vertices() == v + 1
    assert mesh.number_of_faces() == f + 2
    assert mesh.number_of_edges() == e + 3


def test_delete_face():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    f = mesh.number_of_faces()
    mesh.delete_face(0)
    assert mesh.number_of_faces() == f - 1


def test_cull_vertices():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    mesh.add_vertex()
    v = mesh.number_of_vertices()
    mesh.cull_vertices()
    assert mesh.number_of_vertices() == v - 1


# --------------------------------------------------------------------------
# info
# --------------------------------------------------------------------------


def test_is_valid():
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    assert mesh.is_valid()

    mesh_test = mesh.copy()
    del mesh_test.face[0]
    assert not mesh_test.is_valid()

    mesh_test = mesh.copy()
    del mesh_test.vertex[0]
    assert not mesh_test.is_valid()


def test_is_regular():
    mesh = Mesh.from_off(compas.get("cube.off"))
    assert mesh.is_regular()

    mesh.insert_vertex(0)
    assert not mesh.is_regular()


def test_is_manifold(cube, biohazard):
    assert cube.is_manifold()
    assert not biohazard.is_manifold()


@pytest.mark.skip(reason="euh")
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
# vertex attributes
# --------------------------------------------------------------------------


def test_default_vertex_attributes():
    he = Mesh(name="test", default_vertex_attributes={"a": 1, "b": 2})
    for vertex in he.vertices():
        assert he.vertex_attribute(vertex, name="a") == 1
        assert he.vertex_attribute(vertex, name="b") == 2
        he.vertex_attribute(vertex, name="a", value=3)
        assert he.vertex_attribute(vertex, name="a") == 3


def test_vertex_attributes_key_not_found(halfedge):
    with pytest.raises(KeyError):
        halfedge.vertex_attributes(halfedge.number_of_vertices() + 1)


def test_vertex_attributes_from_defaults(halfedge):
    halfedge.update_default_vertex_attributes({"foo": "bar"})
    assert halfedge.vertex_attributes(halfedge.vertex_sample(size=1)[0])["foo"] == "bar"


def test_vertex_attributes_not_in_defaults(halfedge):
    halfedge.update_default_vertex_attributes({"foo": "bar"})
    attrs = halfedge.vertex_attributes(halfedge.vertex_sample(size=1)[0])
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_vertex_attribute_from_view(halfedge, vertex_key):
    halfedge.vertex_attribute(vertex_key, name="foo", value="bar")
    attrs = halfedge.vertex_attributes(vertex_key)
    assert attrs["foo"] == "bar"


def test_set_vertex_attribute_in_view(halfedge, vertex_key):
    attrs = halfedge.vertex_attributes(vertex_key)
    attrs["foo"] = "bar"
    assert halfedge.vertex_attribute(vertex_key, name="foo") == "bar"


def test_del_vertex_attribute_in_view(halfedge, vertex_key):
    halfedge.vertex_attribute(vertex_key, name="foo", value="bar")
    attrs = halfedge.vertex_attributes(vertex_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# --------------------------------------------------------------------------
# face attributes
# --------------------------------------------------------------------------


def test_default_face_attributes():
    he = Mesh(name="test", default_face_attributes={"a": 1, "b": 2})
    for face in he.vertices():
        assert he.face_attribute(face, name="a") == 1
        assert he.face_attribute(face, name="b") == 2
        he.face_attribute(face, name="a", value=3)
        assert he.face_attribute(face, name="a") == 3


def test_face_attributes_is_empty(halfedge):
    assert halfedge.face_attributes(halfedge.face_sample(size=1)[0]) == {}


def test_face_attributes_from_defaults(halfedge):
    halfedge.update_default_face_attributes({"foo": "bar"})
    assert halfedge.face_attributes(halfedge.face_sample(size=1)[0])["foo"] == "bar"


def test_face_attributes_not_in_defaults(halfedge):
    halfedge.update_default_face_attributes({"foo": "bar"})
    attrs = halfedge.face_attributes(halfedge.face_sample(size=1)[0])
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_face_attribute_from_view(halfedge, face_key):
    halfedge.face_attribute(face_key, name="foo", value="bar")
    attrs = halfedge.face_attributes(face_key)
    assert attrs["foo"] == "bar"


def test_set_face_attribute_in_view(halfedge, face_key):
    attrs = halfedge.face_attributes(face_key)
    attrs["foo"] = "bar"
    assert halfedge.face_attribute(face_key, name="foo") == "bar"


def test_del_face_attribute_in_view(halfedge, face_key):
    halfedge.face_attribute(face_key, name="foo", value="bar")
    attrs = halfedge.face_attributes(face_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# --------------------------------------------------------------------------
# edge attributes
# --------------------------------------------------------------------------


def test_default_edge_attributes():
    he = Mesh(name="test", default_edge_attributes={"a": 1, "b": 2})
    for edge in he.vertices():
        assert he.edge_attribute(edge, name="a") == 1
        assert he.edge_attribute(edge, name="b") == 2
        he.edge_attribute(edge, name="a", value=3)
        assert he.edge_attribute(edge, name="a") == 3


def test_edge_attributes_is_empty(halfedge, edge_key):
    assert halfedge.edge_attributes(edge_key) == {}


def test_edge_attributes_from_defaults(halfedge, edge_key):
    halfedge.update_default_edge_attributes({"foo": "bar"})
    assert halfedge.edge_attributes(edge_key)["foo"] == "bar"


def test_edge_attributes_not_in_defaults(halfedge, edge_key):
    halfedge.update_default_edge_attributes({"foo": "bar"})
    attrs = halfedge.edge_attributes(edge_key)
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_edge_attribute_from_view(halfedge, edge_key):
    halfedge.edge_attribute(edge_key, name="foo", value="bar")
    attrs = halfedge.edge_attributes(edge_key)
    assert attrs["foo"] == "bar"


def test_set_edge_attribute_in_view(halfedge, edge_key):
    attrs = halfedge.edge_attributes(edge_key)
    attrs["foo"] = "bar"
    assert halfedge.edge_attribute(edge_key, name="foo") == "bar"


def test_del_edge_attribute_in_view(halfedge, edge_key):
    halfedge.edge_attribute(edge_key, name="foo", value="bar")
    attrs = halfedge.edge_attributes(edge_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# --------------------------------------------------------------------------
# accessors
# --------------------------------------------------------------------------


def test_vertices(cube):
    if compas.PY3:
        assert hasattr(cube.vertices(), "__next__")
    else:
        assert hasattr(cube.vertices(), "__iter__")


def test_faces(cube):
    if compas.PY3:
        assert hasattr(cube.faces(), "__next__")
    else:
        assert hasattr(cube.faces(), "__iter__")


def test_edges(cube):
    if compas.PY3:
        assert hasattr(cube.edges(), "__next__")
    else:
        assert hasattr(cube.edges(), "__iter__")


# --------------------------------------------------------------------------
# halfedges before/after
# --------------------------------------------------------------------------


def test_halfedge_after_on_boundary(grid):
    corners = list(grid.vertices_where(vertex_degree=2))
    corner = corners[0]
    nbrs = grid.vertex_neighbors(corner, ordered=True)
    nbr = nbrs[-1]
    edge = grid.halfedge_after((nbr, corner))
    assert edge[0] == corner
    assert grid.is_edge_on_boundary(edge)
    assert grid.halfedge_face(edge) is None


def test_halfedge_before_on_boundary(grid):
    corners = list(grid.vertices_where(vertex_degree=2))
    corner = corners[0]
    nbrs = grid.vertex_neighbors(corner, ordered=True)
    nbr = nbrs[0]
    edge = grid.halfedge_before((corner, nbr))
    assert edge[1] == corner
    assert grid.is_edge_on_boundary(edge)
    assert grid.halfedge_face(edge) is None


# --------------------------------------------------------------------------
# loops and strips
# --------------------------------------------------------------------------


def test_loops_and_strips_closed(sphere):
    # type: (Mesh) -> None
    poles = list(sphere.vertices_where({"vertex_degree": 16}))

    for nbr in sphere.vertex_neighbors(poles[0]):
        meridian = sphere.edge_loop((poles[0], nbr))

        assert len(meridian) == 16, meridian
        assert meridian[0][0] == poles[0]
        assert meridian[-1][1] == poles[1]

        for edge in meridian[1:-1]:
            strip = sphere.edge_strip(edge)

            assert len(strip) == 17, strip
            assert strip[0] == strip[-1]

        for edge in meridian[1:-1]:
            ring = sphere.edge_loop(sphere.halfedge_before(edge))

            assert len(ring) == 16, ring
            assert ring[0][0] == ring[-1][1]


def test_loops_and_strips_open(grid):
    assert grid.number_of_edges() == 220

    edge = 47, 48
    strip = grid.edge_strip(edge)
    loop = grid.edge_loop(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(strip[0])
    assert grid.is_edge_on_boundary(strip[-1])

    assert edge in loop
    assert len(loop) == 10
    assert grid.is_vertex_on_boundary(loop[0][0])
    assert grid.is_vertex_on_boundary(loop[-1][1])


def test_loops_and_strips_open_corner(grid):
    assert grid.number_of_edges() == 220

    edge = 0, 1
    loop = grid.edge_loop(edge)
    strip = grid.edge_strip(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(strip[0])
    assert grid.is_edge_on_boundary(strip[-1])
    assert edge == strip[-1]

    assert edge in loop
    assert len(loop) == 10
    assert edge == loop[0]

    edge = 1, 0
    loop = grid.edge_loop(edge)
    strip = grid.edge_strip(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(strip[0])
    assert grid.is_edge_on_boundary(strip[-1])
    assert edge == strip[0]

    assert edge in loop
    assert len(loop) == 10
    assert edge == loop[-1]


def test_loops_and_strips_open_boundary(grid):
    assert grid.number_of_edges() == 220

    edge = random.choice(grid.edges_on_boundary())
    u, v = edge

    loop = grid.edge_loop(edge)
    strip = grid.edge_strip(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(strip[0])
    assert grid.is_edge_on_boundary(strip[-1])

    assert edge in loop
    assert len(loop) == 10

    if grid.halfedge[u][v] is None:
        assert edge == strip[-1]
    else:
        assert edge == strip[0]


def test_split_strip_closed(box):
    edge = box.edge_sample()[0]

    box.split_strip(edge)

    assert box.is_valid()
    assert box.number_of_faces() == 10


def test_split_strip_open(grid):
    edge = grid.edge_sample()[0]

    grid.split_strip(edge)

    assert grid.is_valid()
    assert grid.number_of_faces() == 110


def test_split_strip_open_corner(grid):
    corner = list(grid.vertices_where({"vertex_degree": 2}))[0]

    for edge in grid.vertex_edges(corner):
        grid.split_strip(edge)

    assert grid.is_valid()
    assert grid.number_of_faces() == 121


def test_strip_faces_closed(box):
    edge = box.edge_sample()[0]

    strip, faces = box.edge_strip(edge, return_faces=True)

    assert len(strip) == 5
    assert len(faces) == 4
    assert box.edge_faces(strip[0]) == box.edge_faces(strip[-1])


def test_strip_faces_open(grid):
    edge = grid.edge_sample()[0]

    strip, faces = grid.edge_strip(edge, return_faces=True)

    assert grid.is_face_on_boundary(faces[0])
    assert grid.is_face_on_boundary(faces[-1])


# --------------------------------------------------------------------------
# vertex topology
# --------------------------------------------------------------------------


def test_has_vertex(cube):
    assert cube.has_vertex(next(cube.vertices()))
    assert not cube.has_vertex(-1)


def test_is_vertex_connected():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.is_vertex_connected(0)
    k = mesh.add_vertex()
    assert not mesh.is_vertex_connected(k)


def test_is_vertex_on_boundary():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.is_vertex_on_boundary(0)
    assert not mesh.is_vertex_on_boundary(15)


def test_vertex_neighbors():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_neighbors(0) == [1, 6]


def test_vertex_neighborhood():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_neighborhood(0) == {1, 6}


@pytest.mark.skip(reason="euh")
def test_vertex_degree():
    pass


def test_vertex_min_degree():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_min_degree() == 2


def test_vertex_max_degree():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_max_degree() == 4


def test_vertex_faces():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    corners = list(mesh.vertices_where({"vertex_degree": 2}))
    boundary = list(mesh.vertices_where({"vertex_degree": 3}))
    internal = list(mesh.vertices_where({"vertex_degree": 4}))
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
    edge = next(cube.edges())
    assert len(cube.edge_faces(edge)) == 2


def test_is_edge_on_boundary():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.is_edge_on_boundary((0, 1))
    assert not mesh.is_edge_on_boundary((15, 16))


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
    mesh = Mesh.from_obj(compas.get("faces.obj"))
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
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.face_adjacency_halfedge(0, 1) == (1, 7)


def test_face_adjacency_vertices():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.face_adjacency_vertices(0, 1) == [1, 7]


def test_is_face_on_boundary():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.is_face_on_boundary(0)
    assert not mesh.is_face_on_boundary(8)


def test_area():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.area() == 100

    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    assert mesh.area() == 6

    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.area(), 22.802429316496635)


def test_centroid():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.centroid() == [5.0, 5.0, 0.0]

    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    assert mesh.centroid() == [0.0, 0.0, 0.5]

    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_allclose(mesh.centroid(), [2.508081952064351, 2.554046390557884, 1.2687133268242006])


def test_normal():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.normal() == [0.0, 0.0, 1.0]

    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    assert mesh.normal() == [0.0, 0.0, 0.0]

    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_allclose(
        mesh.normal(),
        [
            -2.380849234996509e-06,
            4.1056122145028854e-05,
            0.8077953732329284,
        ],
    )


def test_volume():
    import math

    # Test with a cube
    mesh = Mesh.from_stl(compas.get("cube_binary.stl"))
    volume = mesh.volume()
    assert volume is not None
    # The cube in cube_binary.stl has side length 1, so volume should be 1
    assert TOL.is_close(volume, 1.0)

    # Test with a tetrahedron
    tet = Mesh.from_polyhedron(4)
    volume = tet.volume()
    assert volume is not None
    assert volume > 0

    # Test with a cube from polyhedron
    cube = Mesh.from_polyhedron(6)
    volume = cube.volume()
    assert volume is not None
    assert volume > 0

    # Test with a sphere approximation
    sphere_mesh = Mesh.from_shape(Sphere(radius=1.0), u=32, v=32)
    volume = sphere_mesh.volume()
    assert volume is not None
    expected_sphere_volume = (4.0 / 3.0) * math.pi * (1.0**3)
    # Allow for ~1% error due to discretization
    assert TOL.is_close(volume, expected_sphere_volume, rtol=0.02)

    # Test with an open mesh (should return None)
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    volume = mesh.volume()
    assert volume is None


# --------------------------------------------------------------------------
# vertex geometry
# --------------------------------------------------------------------------


def test_vertex_coordinates():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_coordinates(15) == [6.0, 4.0, 0.0]
    assert mesh.vertex_coordinates(15, "yx") == [4.0, 6.0]


def test_vertex_area():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_area(0) == 1
    assert mesh.vertex_area(15) == 4


def test_vertex_laplacian():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_laplacian(0) == [1.0, 1.0, 0.0]
    assert mesh.vertex_laplacian(1) == [0.0, 0.6666666666666666, 0.0]


def test_vertex_neighborhood_centroid():
    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.vertex_neighborhood_centroid(0) == [1.0, 1.0, 0.0]
    assert mesh.vertex_neighborhood_centroid(1) == [2.0, 0.6666666666666666, 0.0]


def test_vertex_normal():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_allclose(
        mesh.vertex_normal(0),
        [
            -0.7875436283909406,
            0.07148692938164082,
            0.6120985642103861,
        ],
    )
    assert TOL.is_allclose(
        mesh.vertex_normal(5),
        [
            -0.482011312317331,
            -0.32250183520381565,
            0.814651864963369,
        ],
    )


def test_vertex_curvature():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.vertex_curvature(0), 0.0029617825994936453)
    assert TOL.is_close(mesh.vertex_curvature(5), 0.036193074384009094)


def test_face_coordinates():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert mesh.face_coordinates(0, "xyz") == [
        [3.661179780960083, 2.32784628868103, 1.580246925354004],
        [3.775796413421631, 1.727785348892212, 1.382716059684753],
        [4.22069787979126, 1.696692585945129, 1.086419701576233],
        [4.109739303588867, 2.34430718421936, 1.283950567245483],
    ]
    assert mesh.face_coordinates(0, "zy") == [
        [1.580246925354004, 2.32784628868103],
        [1.382716059684753, 1.727785348892212],
        [1.086419701576233, 1.696692585945129],
        [1.283950567245483, 2.34430718421936],
    ]


def test_face_normal():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_allclose(
        mesh.face_normal(0),
        [0.5435358481001584, -0.16248515023849733, 0.8235091728584537],
    )


def test_face_centroid():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_allclose(
        mesh.face_centroid(0),
        [
            3.94185334444046,
            2.024157851934433,
            1.3333333134651184,
        ],
    )


def test_face_center():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_allclose(
        mesh.face_center(0),
        [
            3.944329439044577,
            2.0258867968680776,
            1.332040166602369,
        ],
    )


def test_face_area():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.face_area(0), 0.3374168482414756)


def test_face_flatness():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.face_flatness(0), 0.23896112582475654)

    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.face_flatness(0) == 0


def test_face_aspect_ratio():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.face_aspect_ratio(0), 1.2813792520925738)

    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.face_aspect_ratio(0) == 1


def test_face_skewness():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.face_skewness(0), 0.2432393485343291)

    mesh = Mesh.from_obj(compas.get("faces.obj"))
    assert mesh.face_skewness(0) == 0


def test_face_curvature():
    mesh = Mesh.from_obj(compas.get("quadmesh.obj"))
    assert TOL.is_close(mesh.face_curvature(0), 0.0035753184898039566)

    mesh = Mesh.from_obj(compas.get("faces.obj"))
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


def test_face_attributes_includes_all_defaults(box):
    box.update_default_face_attributes({"attr1": "value1", "attr2": "value2"})

    random_fkey = box.face_sample(size=1)[0]
    assert sorted(box.face_attributes(random_fkey).keys()) == ["attr1", "attr2"]

    box.face_attribute(random_fkey, "attr3", "value3")
    assert sorted(box.face_attributes(random_fkey).keys()) == [
        "attr1",
        "attr2",
        "attr3",
    ]

    assert box.face_attribute(random_fkey, "attr3") == "value3"


# --------------------------------------------------------------------------
# bounding volumes
# --------------------------------------------------------------------------

if not compas.IPY:

    def test_compute_aabb():
        mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
        aabb = mesh.compute_aabb()

        assert isinstance(aabb, Box)
        assert len(aabb.points) == 8
        assert aabb.contains_points(mesh.to_points())

    def test_compute_obb():
        mesh = Mesh.from_obj(compas.get("tubemesh.obj"))
        obb = mesh.compute_obb()

        assert isinstance(obb, Box)
        assert len(obb.points) == 8
        assert obb.contains_points(mesh.to_points())
