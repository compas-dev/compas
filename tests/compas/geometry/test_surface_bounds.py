from math import sqrt

import pytest

from compas.geometry import ConicalSurface
from compas.geometry import CylindricalSurface
from compas.geometry import Frame
from compas.geometry import PlanarSurface
from compas.geometry import SphericalSurface
from compas.geometry import ToroidalSurface


FRAME = Frame([1.0, 2.0, 3.0], [1.0, 1.0, 0.0], [-1.0, 1.0, 1.0])


def assert_box(box, center, extents):
    assert list(box.frame.point) == pytest.approx(center)
    assert box.dimensions == pytest.approx([2.0 * extent for extent in extents])
    assert box.frame == Frame(box.frame.point)


def test_planar_surface_aabb_is_exact_for_rotated_frame_and_degeneracy():
    surface = PlanarSurface(xsize=2.0, ysize=0.0, frame=FRAME)
    xaxis = surface.frame.xaxis
    yaxis = surface.frame.yaxis
    center = surface.frame.point + surface.xsize * 0.5 * xaxis
    extents = [0.5 * (surface.xsize * abs(xaxis[i]) + surface.ysize * abs(yaxis[i])) for i in range(3)]

    assert_box(surface.aabb, center, extents)


def test_cylindrical_surface_aabb_is_exact_for_rotated_frame():
    surface = CylindricalSurface(radius=2.0, frame=FRAME)
    xaxis = surface.frame.xaxis
    yaxis = surface.frame.yaxis
    zaxis = surface.frame.zaxis
    vmin, vmax = surface.domain_v
    center = surface.frame.point + 0.5 * (vmin + vmax) * zaxis
    extents = [surface.radius * sqrt(xaxis[i] ** 2 + yaxis[i] ** 2) + 0.5 * (vmax - vmin) * abs(zaxis[i]) for i in range(3)]

    assert_box(surface.aabb, center, extents)


def test_conical_surface_aabb_is_exact_for_rotated_frame():
    surface = ConicalSurface(radius=2.0, height=3.0, frame=FRAME)
    origin = surface.frame.point
    apex = origin + surface.height * surface.frame.zaxis
    minimum = []
    maximum = []
    for i in range(3):
        radial = surface.radius * sqrt(surface.frame.xaxis[i] ** 2 + surface.frame.yaxis[i] ** 2)
        minimum.append(min(origin[i] - radial, apex[i]))
        maximum.append(max(origin[i] + radial, apex[i]))

    assert_box(
        surface.aabb,
        [0.5 * (a + b) for a, b in zip(minimum, maximum)],
        [0.5 * (b - a) for a, b in zip(minimum, maximum)],
    )


def test_spherical_surface_aabb_is_exact_and_frame_independent():
    surface = SphericalSurface(radius=2.0, frame=FRAME)

    assert_box(surface.aabb, surface.center, [2.0, 2.0, 2.0])


def test_spherical_surface_aabb_supports_zero_radius():
    surface = SphericalSurface(radius=0.0, frame=FRAME)

    assert_box(surface.aabb, surface.center, [0.0, 0.0, 0.0])


def test_toroidal_surface_aabb_is_exact_for_rotated_frame():
    surface = ToroidalSurface(radius_axis=2.0, radius_pipe=0.5, frame=FRAME)
    extents = [surface.radius_axis * sqrt(surface.frame.xaxis[i] ** 2 + surface.frame.yaxis[i] ** 2) + surface.radius_pipe for i in range(3)]

    assert_box(surface.aabb, surface.center, extents)
