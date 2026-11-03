import pytest

from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import BrepFace
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Native
from compas.geometry import PlanarSurface
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import UGrid
from compas.geometry import UVGrid


def test_parametric_surface_requires_uvgrid():
    surface = PlanarSurface()

    polygonal = surface.polygonize(UVGrid(2, 3))
    tessellation = surface.tessellate(UVGrid(2, 3))

    assert len(polygonal.vertices) == 12
    assert len(polygonal.faces) == 6
    assert all(len(face) == 4 for face in polygonal.faces)
    assert tessellation.number_of_vertices == 12
    assert tessellation.number_of_triangles == 12
    assert tessellation.vertex_normals is not None
    assert tessellation.texture_coordinates is not None
    assert not hasattr(surface, "resolution_u")
    assert not hasattr(surface, "resolution_v")

    with pytest.raises(TypeError):
        surface.tessellate(UGrid(3))


def test_surface_tessellation_default_is_uvgrid_64():
    surface = PlanarSurface()
    data = surface.__data__

    omitted = surface.tessellate()
    none = surface.tessellate(None)
    explicit = surface.tessellate(UVGrid(64, 64))

    assert omitted.number_of_vertices == 4225
    assert omitted.number_of_triangles == 8192
    assert omitted.vertices == explicit.vertices
    assert omitted.triangles == explicit.triangles
    assert none.vertices == explicit.vertices
    assert none.triangles == explicit.triangles
    assert omitted is not none
    assert omitted.vertices is not none.vertices
    assert surface.__data__ == data


@pytest.mark.parametrize(
    ("shape", "strategy", "vertex_count", "triangle_count"),
    [
        (Box(1.0), Native(), 8, 12),
        (Cylinder(1.0, 2.0), UGrid(64), 130, 256),
        (Cone(1.0, 2.0), UGrid(64), 66, 128),
        (Capsule(1.0, 2.0), UVGrid(64, 64), 4098, 8192),
        (Sphere(1.0), UVGrid(64, 64), 4034, 8064),
        (Torus(2.0, 0.5), UVGrid(64, 64), 4096, 8192),
    ],
)
def test_shape_tessellation_defaults(shape, strategy, vertex_count, triangle_count):
    data = shape.__data__

    omitted = shape.tessellate()
    none = shape.tessellate(None)
    explicit = shape.tessellate(strategy)

    assert omitted.number_of_vertices == vertex_count
    assert omitted.number_of_triangles == triangle_count
    assert omitted.vertices == explicit.vertices
    assert omitted.triangles == explicit.triangles
    assert none.vertices == explicit.vertices
    assert none.triangles == explicit.triangles
    assert omitted is not none
    assert omitted.vertices is not none.vertices
    assert shape.__data__ == data


def test_explicit_tessellation_strategy_overrides_default():
    sphere = Sphere(1.0)

    default = sphere.tessellate()
    explicit = sphere.tessellate(UVGrid(6, 4))

    assert default.number_of_vertices == 4034
    assert explicit.number_of_vertices == 20


@pytest.mark.parametrize("geometry", [Box(1.0), PlanarSurface(), Brep(), BrepFace()])
def test_persistent_and_deflection_materialization_remain_explicit(geometry):
    with pytest.raises(TypeError):
        geometry.polygonize()

    if isinstance(geometry, (Brep, BrepFace)):
        with pytest.raises(TypeError):
            geometry.tessellate()


@pytest.mark.parametrize(
    ("shape", "strategy", "vertex_count", "face_count"),
    [
        (Box(1.0), Native(), 8, 6),
        (Cylinder(1.0, 2.0), UGrid(6), 14, 18),
        (Cone(1.0, 2.0), UGrid(6), 8, 12),
        (Capsule(1.0, 2.0), UVGrid(6, 4), 26, 30),
        (Sphere(1.0), UVGrid(6, 4), 20, 24),
        (Torus(2.0, 0.5), UVGrid(6, 4), 24, 24),
    ],
)
def test_shapes_use_explicit_strategy_dimensions(shape, strategy, vertex_count, face_count):
    polygonal = shape.polygonize(strategy)
    tessellation = shape.tessellate(strategy)

    assert len(polygonal.vertices) == vertex_count
    assert len(polygonal.faces) == face_count
    assert tessellation.number_of_vertices == vertex_count
    assert not hasattr(shape, "resolution_u")
    assert not hasattr(shape, "resolution_v")


def test_continuous_materialization_is_fresh():
    shape = Sphere(1.0)
    strategy = UVGrid(6, 4)

    first = shape.polygonize(strategy)
    second = shape.polygonize(strategy)

    assert first is not second
    assert first.vertices is not second.vertices
    first.vertices[0][0] = 99
    assert second.vertices[0][0] != 99


@pytest.mark.parametrize(
    ("shape", "invalid_strategy"),
    [
        (Box(1.0), UVGrid(3, 4)),
        (Cylinder(1.0, 2.0), UVGrid(3, 4)),
        (Cone(1.0, 2.0), Native()),
        (Capsule(1.0, 2.0), UGrid(4)),
        (Sphere(1.0), UGrid(4)),
        (Torus(2.0, 0.5), Native()),
    ],
)
def test_shapes_reject_unsupported_strategies(shape, invalid_strategy):
    with pytest.raises(TypeError):
        shape.polygonize(invalid_strategy)
    with pytest.raises(TypeError):
        shape.tessellate(invalid_strategy)


def test_capsule_rejects_odd_v_resolution():
    capsule = Capsule(1.0, 2.0)

    with pytest.raises(ValueError):
        capsule.polygonize(UVGrid(6, 5))
    with pytest.raises(ValueError):
        capsule.tessellate(UVGrid(6, 5))


def test_polygonize_returns_independent_serializable_geometry():
    shape = Box(1.0)
    surface = shape.polygonize(Native())
    surface.vertices[0][0] = 100.0

    assert shape.polygonize(Native()).vertices[0][0] != 100.0
    assert surface.__data__


@pytest.mark.parametrize("geometry", [PlanarSurface(), Box(1.0)])
def test_legacy_continuous_tessellation_entry_points_are_removed(geometry):
    assert not hasattr(geometry, "tessellation")
    assert not hasattr(geometry, "compute_tessellation")
    assert not hasattr(geometry, "to_tessellation")
    assert not hasattr(geometry, "to_polygonal_surface")
    assert not hasattr(geometry, "mesh")
    assert not hasattr(geometry, "compute_mesh")
