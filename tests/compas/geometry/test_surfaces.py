from math import inf

import pytest

from compas.tolerance import TOL
from compas.geometry import Frame
from compas.geometry import SphericalSurface
from compas.geometry import CylindricalSurface
from compas.geometry import ConicalSurface
from compas.geometry import ToroidalSurface
from compas.geometry import PlanarSurface


@pytest.mark.parametrize(
    "surface",
    [
        SphericalSurface(radius=1.0, frame=Frame.worldZX()),
        CylindricalSurface(radius=1.0, frame=Frame.worldZX()),
        ConicalSurface(radius=1.0, height=1.0, frame=Frame.worldZX()),
        ToroidalSurface(radius_axis=1.0, radius_pipe=0.3, frame=Frame.worldZX()),
        PlanarSurface(xsize=1, ysize=1, frame=Frame.worldZX()),
    ],
)
def test_surface_geometry(surface):
    assert TOL.is_allclose(
        surface.point_at(0, 0),
        surface.point_at(0, 0, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(0.5, 0),
        surface.point_at(0.5, 0, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(1.0, 0),
        surface.point_at(1.0, 0, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(1.0, 0.5),
        surface.point_at(1.0, 0.5, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(1.0, 1.0),
        surface.point_at(1.0, 1.0, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(0.5, 1.0),
        surface.point_at(0.5, 1.0, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(0, 1.0),
        surface.point_at(0, 1.0, world=False).transformed(surface.transformation),
    )

    assert TOL.is_allclose(
        surface.point_at(0, 0.5),
        surface.point_at(0, 0.5, world=False).transformed(surface.transformation),
    )


def test_surface_frame_is_copied_and_requires_frame_object():
    source = Frame.worldYZ()
    surface = PlanarSurface(frame=source)

    assert surface.frame == source
    assert surface.frame is not source

    source.point = [10.0, 0.0, 0.0]
    assert surface.frame.point == [0.0, 0.0, 0.0]

    with pytest.raises(TypeError):
        surface.frame = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]  # type: ignore[assignment]


def test_surface_transformation_reflects_direct_frame_mutation():
    surface = PlanarSurface()
    _ = surface.transformation

    surface.frame.point = [10.0, 0.0, 0.0]

    assert surface.transformation.translation_vector == [10.0, 0.0, 0.0]
    assert surface.point == [10.0, 0.0, 0.0]


def test_surface_preserves_geometry_bounding_box_property_contract():
    assert isinstance(PlanarSurface.aabb, property)
    assert isinstance(PlanarSurface.obb, property)


@pytest.mark.parametrize(
    "surface, periodic_u, periodic_v",
    [
        (PlanarSurface(), False, False),
        (SphericalSurface(1.0), True, False),
        (CylindricalSurface(1.0), True, False),
        (ConicalSurface(1.0, 1.0), True, False),
        (ToroidalSurface(2.0, 0.5), True, True),
    ],
)
def test_analytic_surface_periodicity(surface, periodic_u, periodic_v):
    assert surface.is_periodic_u is periodic_u
    assert surface.is_periodic_v is periodic_v


def test_surface_discretization_counts():
    surface = PlanarSurface(xsize=2.0, ysize=3.0)

    vertices, faces = surface.to_vertices_and_faces(nu=2, nv=3)

    assert len(vertices) == 12
    assert len(faces) == 6
    assert len(surface.to_quads(nu=2, nv=3)) == 6
    assert len(surface.to_triangles(nu=2, nv=3)) == 12


@pytest.mark.parametrize("nu, nv", [(0, 1), (1, 0), (-1, 1), (1, -1)])
def test_surface_discretization_requires_positive_face_counts(nu, nv):
    with pytest.raises(ValueError, match="at least one face"):
        PlanarSurface().to_vertices_and_faces(nu=nu, nv=nv)


def test_surface_discretization_requires_finite_domains():
    with pytest.raises(ValueError, match="finite parameter domains"):
        PlanarSurface().to_vertices_and_faces(du=(-inf, inf))
