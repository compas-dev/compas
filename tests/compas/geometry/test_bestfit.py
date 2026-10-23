import pytest

from compas.geometry import bestfit_circle
from compas.geometry import bestfit_frame
from compas.geometry import bestfit_line
from compas.geometry import bestfit_plane
from compas.geometry import bestfit_sphere
from compas.linalg import dot_vectors
from compas.linalg import length_vector
from compas.tolerance import TOL


def test_bestfit_line():
    origin, direction = bestfit_line([[-2, 0, 0], [-1, 0, 0], [1, 0, 0], [2, 0, 0]])

    assert TOL.is_allclose(origin, [0, 0, 0])
    assert abs(dot_vectors(direction, [1, 0, 0])) == pytest.approx(1.0)


def test_bestfit_plane():
    point, normal = bestfit_plane([[-1, -1, 2], [1, -1, 2], [1, 1, 2], [-1, 1, 2]])

    assert TOL.is_allclose(point, [0, 0, 2])
    assert abs(dot_vectors(normal, [0, 0, 1])) == pytest.approx(1.0)


def test_bestfit_frame():
    point, xaxis, yaxis = bestfit_frame([[-2, -1, 0], [2, -1, 0], [2, 1, 0], [-2, 1, 0]])

    assert TOL.is_allclose(point, [0, 0, 0])
    assert length_vector(xaxis) == pytest.approx(1.0)
    assert length_vector(yaxis) == pytest.approx(1.0)
    assert dot_vectors(xaxis, yaxis) == pytest.approx(0.0)


def test_bestfit_circle():
    center, normal, radius = bestfit_circle([[3, 2, 3], [1, 4, 3], [-1, 2, 3], [1, 0, 3]])

    assert TOL.is_allclose(center, [1, 2, 3])
    assert abs(dot_vectors(normal, [0, 0, 1])) == pytest.approx(1.0)
    assert radius == pytest.approx(2.0)


def test_bestfit_sphere():
    center, radius = bestfit_sphere([[3, 2, 3], [-1, 2, 3], [1, 4, 3], [1, 0, 3], [1, 2, 5], [1, 2, 1]])

    assert TOL.is_allclose(center, [1, 2, 3])
    assert radius == pytest.approx(2.0)
