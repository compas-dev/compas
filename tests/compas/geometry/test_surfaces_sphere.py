import pytest

from compas.utilities import linspace
from compas.geometry import Frame
from compas.geometry import SphericalSurface


def test_create_spherical_surface():
    surf = SphericalSurface(radius=1.0)

    assert surf.radius == 1.0
    assert surf.frame == Frame.worldXY()

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert surf.point_at(u, v) == surf.point_at(u, v, world=False)


@pytest.mark.parametrize(
    "frame",
    [
        Frame.worldXY(),
        Frame.worldZX(),
        Frame.worldYZ(),
    ],
)
def test_create_spherical_surface_frame(frame):
    surf = SphericalSurface(radius=1.0, frame=frame)

    assert surf.radius == 1.0
    assert surf.frame == frame

    for u in linspace(0.0, 1.0, num=100):
        for v in linspace(0.0, 1.0, num=100):
            assert surf.point_at(u, v) == surf.point_at(u, v, world=False).transformed(surf.transformation)


# =============================================================================
# Constructors
# =============================================================================


def test_create_sphere_from_plane_and_radius():
    pass


def test_create_sphere_from_three_points():
    pass


def test_create_sphere_from_points():
    pass


# =============================================================================
# Properties and Geometry
# =============================================================================

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
