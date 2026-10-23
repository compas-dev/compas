from types import SimpleNamespace

import pytest

from compas.geometry import Brep
from compas.geometry import BrepEdge
from compas.geometry import BrepFace
from compas.geometry import BrepLoop
from compas.geometry import BrepTrim
from compas.geometry import BrepType
from compas.geometry import BrepVertex
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Ellipse
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import PlanarSurface
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import conforming_delaunay_triangulation
from compas.geometry import constrained_delaunay_triangulation
from compas.plugins import PluginNotInstalledError


def test_brep_type_values_include_solid():
    assert BrepType.COMPOUND == 0
    assert BrepType.COMPSOLID == 1
    assert BrepType.SOLID == 2
    assert BrepType.SHELL == 3
    assert BrepType.FACE == 4
    assert BrepType.WIRE == 5
    assert BrepType.EDGE == 6
    assert BrepType.VERTEX == 7
    assert BrepType.SHAPE == 8


@pytest.mark.parametrize(
    "property_name",
    [
        "orientation",
        "type",
        "is_valid",
        "is_orientable",
        "is_closed",
        "is_infinite",
        "is_convex",
        "is_manifold",
        "is_surface",
        "is_compound",
        "is_compoundsolid",
        "is_shell",
        "is_solid",
        "points",
        "curves",
        "surfaces",
        "vertices",
        "edges",
        "trims",
        "loops",
        "faces",
        "shells",
        "solids",
        "frame",
        "area",
        "volume",
        "centroid",
    ],
)
def test_brep_properties_require_backend_implementation(property_name):
    brep = Brep()

    with pytest.raises(PluginNotInstalledError):
        getattr(brep, property_name)


def test_brep_is_the_public_wrapper_for_native_backend_data():
    native_brep = object()
    brep = Brep(native_brep=native_brep)

    assert type(brep) is Brep
    assert brep.native_brep is native_brep


def test_brep_string_uses_area_and_volume_properties():
    class TestBrep(Brep):
        vertices = []
        edges = []
        loops = []
        faces = []
        frame = "frame"
        area = 1.0
        volume = 2.0

    brep = object.__new__(TestBrep)

    assert "Area: 1.0" in str(brep)
    assert "Volume: 2.0" in str(brep)


@pytest.mark.parametrize(
    ("operator", "factory_name"),
    [
        (lambda a, b: a - b, "from_boolean_difference"),
        (lambda a, b: a & b, "from_boolean_intersection"),
        (lambda a, b: a + b, "from_boolean_union"),
    ],
)
def test_brep_boolean_operators_return_factory_result(operator, factory_name):
    result = object()

    class TestBrep(Brep):
        pass

    def factory(cls, brep_a, brep_b):
        assert isinstance(brep_a, TestBrep)
        assert isinstance(brep_b, TestBrep)
        return result

    setattr(TestBrep, factory_name, classmethod(factory))
    brep_a = object.__new__(TestBrep)
    brep_b = object.__new__(TestBrep)

    assert operator(brep_a, brep_b) is result


def test_brep_remaining_operations_require_backend_implementation():
    brep = Brep()
    vertex = BrepVertex()
    edge = BrepEdge()
    plane = Plane.worldXY()

    operations = [
        lambda: brep.to_tesselation(),
        lambda: brep.to_viewmesh(),
        lambda: brep.vertex_neighbors(vertex),
        lambda: brep.vertex_edges(vertex),
        lambda: brep.vertex_faces(vertex),
        lambda: brep.edge_faces(edge),
        lambda: brep.edge_loops(edge),
        lambda: brep.trim(plane),
        lambda: brep.trimmed(plane),
        lambda: brep.fillet(1.0, exclude=[edge]),
        lambda: brep.filleted(1.0, exclude=[edge]),
        lambda: brep.slice(plane),
        lambda: brep.split(brep),
        lambda: brep.overlap(brep),
    ]

    for operation in operations:
        with pytest.raises(PluginNotInstalledError):
            operation()


def test_brep_loop_validation_requires_backend_implementation():
    with pytest.raises(NotImplementedError):
        BrepLoop().is_valid


@pytest.mark.parametrize(
    ("component", "property_name"),
    [
        (BrepVertex(), "point"),
        (BrepVertex(), "native_vertex"),
        (BrepTrim(), "curve"),
        (BrepTrim(), "iso_status"),
        (BrepTrim(), "is_reversed"),
        (BrepTrim(), "native_trim"),
        (BrepTrim(), "start_vertex"),
        (BrepTrim(), "end_vertex"),
        (BrepTrim(), "vertices"),
        (BrepLoop(), "vertices"),
        (BrepLoop(), "edges"),
        (BrepLoop(), "native_loop"),
        (BrepEdge(), "is_line"),
        (BrepEdge(), "is_circle"),
        (BrepEdge(), "is_ellipse"),
        (BrepEdge(), "is_hyperbola"),
        (BrepEdge(), "is_parabola"),
        (BrepEdge(), "is_bezier"),
        (BrepEdge(), "is_bspline"),
        (BrepEdge(), "is_other"),
        (BrepEdge(), "is_valid"),
        (BrepEdge(), "vertices"),
        (BrepEdge(), "first_vertex"),
        (BrepEdge(), "last_vertex"),
        (BrepEdge(), "length"),
        (BrepEdge(), "curve"),
        (BrepEdge(), "orientation"),
        (BrepEdge(), "type"),
        (BrepEdge(), "native_edge"),
        (BrepFace(), "is_plane"),
        (BrepFace(), "is_cylinder"),
        (BrepFace(), "is_sphere"),
        (BrepFace(), "is_torus"),
        (BrepFace(), "is_cone"),
        (BrepFace(), "is_bspline"),
        (BrepFace(), "vertices"),
        (BrepFace(), "edges"),
        (BrepFace(), "loops"),
        (BrepFace(), "surface"),
        (BrepFace(), "native_face"),
        (BrepFace(), "nurbssurface"),
        (BrepFace(), "area"),
        (BrepFace(), "centroid"),
        (BrepFace(), "is_reversed"),
        (BrepFace(), "is_valid"),
        (BrepFace(), "type"),
    ],
)
def test_brep_component_properties_require_backend_implementation(component, property_name):
    with pytest.raises(NotImplementedError):
        getattr(component, property_name)


@pytest.mark.parametrize(
    ("constructor", "value"),
    [
        (BrepVertex.from_point, Point(0, 0, 0)),
        (BrepLoop.from_edges, []),
        (BrepLoop.from_polyline, Polyline([[0, 0, 0], [1, 0, 0], [0, 0, 0]])),
        (BrepLoop.from_polygon, Polygon([[0, 0, 0], [1, 0, 0], [0, 1, 0]])),
        (BrepEdge.from_vertices, [BrepVertex(), BrepVertex()]),
        (BrepEdge.from_points, [[0, 0, 0], [1, 0, 0]]),
        (BrepEdge.from_line, Line([0, 0, 0], [1, 0, 0])),
        (BrepEdge.from_circle, Circle(1.0)),
        (BrepEdge.from_ellipse, Ellipse(2.0, 1.0)),
        (BrepEdge.from_curve, Circle(1.0)),
        (BrepFace.from_plane, Plane.worldXY()),
        (BrepFace.from_cylinder, Cylinder(1.0, 2.0)),
        (BrepFace.from_cone, Cone(1.0, 2.0)),
        (BrepFace.from_sphere, Sphere(1.0)),
        (BrepFace.from_torus, Torus(2.0, 1.0)),
        (BrepFace.from_surface, PlanarSurface()),
    ],
)
def test_brep_component_constructors_require_backend_implementation(constructor, value):
    with pytest.raises(NotImplementedError):
        constructor(value)


@pytest.mark.parametrize(
    "conversion",
    [
        BrepEdge().to_line,
        BrepEdge().to_circle,
        BrepEdge().to_ellipse,
        BrepEdge().to_hyperbola,
        BrepEdge().to_parabola,
        BrepEdge().to_bezier,
        BrepEdge().to_bspline,
        BrepEdge().to_curve,
    ],
)
def test_brep_edge_conversions_require_backend_implementation(conversion):
    with pytest.raises(NotImplementedError):
        conversion()


@pytest.mark.parametrize(
    "operation",
    [
        BrepFace().to_polygon,
        BrepFace().to_polygons,
        BrepFace().to_plane,
        BrepFace().to_cylinder,
        BrepFace().to_cone,
        BrepFace().to_sphere,
        BrepFace().to_torus,
        BrepFace().to_nurbs,
        BrepFace().adjacent_faces,
        BrepFace().as_brep,
        BrepFace().try_get_nurbssurface,
    ],
)
def test_brep_face_operations_require_backend_implementation(operation):
    with pytest.raises(NotImplementedError):
        operation()


def test_brep_face_mutations_and_evaluation_require_backend_implementation():
    face = BrepFace()

    with pytest.raises(NotImplementedError):
        face.add_loop(BrepLoop())
    with pytest.raises(NotImplementedError):
        face.add_loops([BrepLoop()])
    with pytest.raises(NotImplementedError):
        face.frame_at(0.0, 0.0)


def test_brep_face_polygon_conversions_distinguish_outer_and_inner_loops():
    class FaceWithLoops(BrepFace):
        @property
        def loops(self):
            outer = SimpleNamespace(
                vertices=[
                    SimpleNamespace(point=Point(0, 0, 0)),
                    SimpleNamespace(point=Point(2, 0, 0)),
                    SimpleNamespace(point=Point(0, 2, 0)),
                ]
            )
            inner = SimpleNamespace(
                vertices=[
                    SimpleNamespace(point=Point(0.25, 0.25, 0)),
                    SimpleNamespace(point=Point(0.5, 0.25, 0)),
                    SimpleNamespace(point=Point(0.25, 0.5, 0)),
                ]
            )
            return [outer, inner]

    face = FaceWithLoops()

    assert face.to_polygon() == face.to_polygons()[0]
    assert len(face.to_polygons()) == 2


def test_constrained_delaunay_requires_plugin():
    boundary = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]

    with pytest.raises(PluginNotInstalledError):
        constrained_delaunay_triangulation(boundary)


def test_conforming_delaunay_requires_plugin():
    boundary = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]

    with pytest.raises(PluginNotInstalledError):
        conforming_delaunay_triangulation(boundary)
