import inspect

import pytest

import compas.geometry as geometry
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import PlanarSurface
from compas.geometry import Sphere
from compas.geometry import Torus


@pytest.mark.parametrize(
    ("producer", "kwargs", "vertex_count", "face_count", "triangle_count"),
    [
        (Box(1.0), {}, 8, 6, 12),
        (Cylinder(1.0, 2.0), {"nu": 6}, 14, 18, 24),
        (Cone(1.0, 2.0), {"nu": 6}, 8, 12, 12),
        (Capsule(1.0, 2.0), {"nu": 6, "nv": 4}, 26, 30, 48),
        (Sphere(1.0), {"nu": 6, "nv": 4}, 20, 24, 36),
        (Torus(2.0, 0.5), {"nu": 6, "nv": 4}, 24, 24, 48),
        (PlanarSurface(), {"nu": 2, "nv": 3}, 12, 6, 12),
    ],
)
def test_structured_conversions_are_exactly_composed(producer, kwargs, vertex_count, face_count, triangle_count):
    data = producer.__data__
    polygonal = producer.to_polygonal_surface(**kwargs)
    direct = producer.to_tessellation(**kwargs)
    composed = polygonal.triangulated()

    assert len(polygonal.vertices) == vertex_count
    assert len(polygonal.faces) == face_count
    assert direct.number_of_triangles == triangle_count
    assert direct.vertices == composed.vertices
    assert direct.triangles == composed.triangles
    assert producer.__data__ == data


def test_surface_preserves_aligned_normals_and_uvs():
    result = PlanarSurface().to_tessellation(nu=2, nv=3)
    assert len(result.vertex_normals) == result.number_of_vertices
    assert len(result.texture_coordinates) == result.number_of_vertices


def test_default_resolutions_and_exact_signatures():
    assert str(inspect.signature(Box.to_polygonal_surface)) == "(self) -> 'PolygonalSurface'"
    assert str(inspect.signature(Cone.to_polygonal_surface)) == "(self, *, nu: int = 64) -> 'PolygonalSurface'"
    assert str(inspect.signature(Sphere.to_tessellation)) == "(self, *, nu: int = 64, nv: int = 64) -> 'Tessellation'"
    assert str(inspect.signature(PlanarSurface.to_tessellation)) == "(self, *, nu: int = 64, nv: int = 64) -> 'Tessellation'"
    assert Sphere(1.0).to_tessellation().number_of_vertices == 4034
    assert PlanarSurface().to_tessellation().number_of_vertices == 4225


@pytest.mark.parametrize("invalid", [True, 3.0, "3"])
def test_resolution_rejects_bool_and_non_integral_values(invalid):
    with pytest.raises(TypeError):
        Sphere(1.0).to_polygonal_surface(nu=invalid)


def test_resolution_minimums_and_capsule_even_nv():
    with pytest.raises(ValueError):
        Cone(1.0, 2.0).to_polygonal_surface(nu=2)
    with pytest.raises(ValueError):
        PlanarSurface().to_polygonal_surface(nu=0)
    with pytest.raises(ValueError):
        Capsule(1.0, 2.0).to_polygonal_surface(nv=3)
    with pytest.raises(ValueError, match="even"):
        Capsule(1.0, 2.0).to_polygonal_surface(nv=5)


def test_structured_results_are_fresh():
    shape = Sphere(1.0)
    first = shape.to_polygonal_surface(nu=6, nv=4)
    second = shape.to_polygonal_surface(nu=6, nv=4)
    first.vertices[0][0] = 99
    assert second.vertices[0][0] != 99


def test_removed_continuous_entry_points_and_strategies_are_absent():
    for producer in (Box(1.0), PlanarSurface()):
        assert not hasattr(producer, "polygonize")
        assert not hasattr(producer, "tessellate")
    for producer in (Box(1.0), Cone(1.0, 2.0), Cylinder(1.0, 2.0)):
        assert not hasattr(producer, "_tessellation_strategy")
    for name in ("TessellationStrategy", "Native", "UGrid", "UVGrid", "Deflection", "Adaptive"):
        assert not hasattr(geometry, name)
