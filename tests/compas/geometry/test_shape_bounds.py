from math import sqrt

import pytest

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Sphere
from compas.geometry import Torus


def test_rotated_box_aabb_is_exact():
    frame = Frame([1, 2, 3], [1, 1, 0], [-1, 1, 0])
    box = Box(2, 4, 6, frame=frame)

    bounds = box.aabb

    assert bounds.frame == Frame([1, 2, 3], [1, 0, 0], [0, 1, 0])
    assert bounds.xsize == pytest.approx(3 * sqrt(2))
    assert bounds.ysize == pytest.approx(3 * sqrt(2))
    assert bounds.zsize == pytest.approx(6)


def test_box_bounds_support_degenerate_dimensions():
    box = Box(0, 2, 0, frame=Frame([1, 2, 3], [1, 1, 0], [-1, 1, 0]))

    assert box.aabb.xsize == pytest.approx(sqrt(2))
    assert box.aabb.ysize == pytest.approx(sqrt(2))
    assert box.aabb.zsize == pytest.approx(0)
    assert box.obb.dimensions == box.dimensions


@pytest.mark.parametrize(
    ("shape", "dimensions"),
    [
        (Cylinder(2, 6, frame=Frame([1, 2, 3], [0, 1, 0], [0, 0, 1])), (6, 4, 4)),
        (Sphere(2, frame=Frame([1, 2, 3], [0, 1, 0], [0, 0, 1])), (4, 4, 4)),
        (Torus(5, 2, frame=Frame([1, 2, 3], [0, 1, 0], [0, 0, 1])), (4, 14, 14)),
        (Capsule(2, 6, frame=Frame([1, 2, 3], [0, 1, 0], [0, 0, 1])), (10, 4, 4)),
    ],
)
def test_centered_shape_aabb_uses_exact_parameter_extrema(shape, dimensions):
    bounds = shape.aabb

    assert bounds.frame == Frame(shape.frame.point, [1, 0, 0], [0, 1, 0])
    assert bounds.dimensions == pytest.approx(dimensions)


def test_cone_aabb_accounts_for_asymmetric_base_and_apex():
    cone = Cone(2, 6, frame=Frame([1, 2, 3], [0, 1, 0], [0, 0, 1]))

    bounds = cone.aabb

    assert bounds.frame == Frame([4, 2, 3], [1, 0, 0], [0, 1, 0])
    assert bounds.dimensions == pytest.approx((6, 4, 4))


def test_capsule_aabb_supports_degenerate_parameters():
    point = Capsule(0, 0, frame=Frame([1, 2, 3], [1, 1, 0], [-1, 1, 0])).aabb
    segment = Capsule(0, 4, frame=Frame([1, 2, 3], [0, 1, 0], [0, 0, 1])).aabb
    sphere = Capsule(2, 0, frame=Frame([1, 2, 3], [1, 1, 0], [-1, 1, 0])).aabb

    assert point.dimensions == pytest.approx((0, 0, 0))
    assert segment.dimensions == pytest.approx((4, 0, 0))
    assert sphere.dimensions == pytest.approx((4, 4, 4))


def test_sphere_obb_is_exact_and_uses_sphere_frame():
    sphere = Sphere(2, frame=Frame([1, 2, 3], [1, 1, 0], [-1, 1, 0]))

    assert sphere.obb.frame == sphere.frame
    assert sphere.obb.dimensions == pytest.approx((4, 4, 4))


@pytest.mark.parametrize("shape", [Cylinder(1, 2), Cone(1, 2), Torus(2, 1), Capsule(1, 2)])
def test_obb_is_not_approximated_from_samples(shape):
    with pytest.raises(NotImplementedError):
        shape.obb
