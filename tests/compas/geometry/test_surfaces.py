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
