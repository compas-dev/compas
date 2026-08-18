import pytest

from compas.geometry import NurbsSurface
from compas.geometry import Point


class TestNurbsSurface(NurbsSurface):
    __test__ = False

    def __init__(
        self,
        points,
        weights,
        knots_u,
        knots_v,
        mults_u,
        mults_v,
        degree_u,
        degree_v,
        is_periodic_u=False,
        is_periodic_v=False,
    ):
        super().__init__()
        self._points = [[Point(point[0], point[1], point[2]) for point in row] for row in points]
        self._weights = [list(row) for row in weights]
        self._knots_u = list(knots_u)
        self._knots_v = list(knots_v)
        self._mults_u = list(mults_u)
        self._mults_v = list(mults_v)
        self._degree_u = degree_u
        self._degree_v = degree_v
        self._is_periodic_u = is_periodic_u
        self._is_periodic_v = is_periodic_v

    @classmethod
    def from_parameters(
        cls,
        points,
        weights,
        knots_u,
        knots_v,
        mults_u,
        mults_v,
        degree_u,
        degree_v,
        is_periodic_u=False,
        is_periodic_v=False,
    ):
        return cls(
            points,
            weights,
            knots_u,
            knots_v,
            mults_u,
            mults_v,
            degree_u,
            degree_v,
            is_periodic_u,
            is_periodic_v,
        )

    @classmethod
    def from_points(cls, points, degree_u=3, degree_v=3):
        count_u = len(points[0])
        count_v = len(points)
        degree_u = min(degree_u, count_u - 1)
        degree_v = min(degree_v, count_v - 1)
        return cls.from_parameters(
            points=points,
            weights=[[1.0] * count_u for _ in range(count_v)],
            knots_u=[0.0, 1.0],
            knots_v=[0.0, 1.0],
            mults_u=[degree_u + 1, degree_u + 1],
            mults_v=[degree_v + 1, degree_v + 1],
            degree_u=degree_u,
            degree_v=degree_v,
        )

    @property
    def points(self):
        return self._points

    @property
    def weights(self):
        return self._weights

    @property
    def knots_u(self):
        return self._knots_u

    @property
    def knots_v(self):
        return self._knots_v

    @property
    def mults_u(self):
        return self._mults_u

    @property
    def mults_v(self):
        return self._mults_v

    @property
    def degree_u(self):
        return self._degree_u

    @property
    def degree_v(self):
        return self._degree_v

    @property
    def domain_u(self):
        return self.knots_u[0], self.knots_u[-1]

    @property
    def domain_v(self):
        return self.knots_v[0], self.knots_v[-1]

    @property
    def is_periodic_u(self):
        return self._is_periodic_u

    @property
    def is_periodic_v(self):
        return self._is_periodic_v


@pytest.fixture
def surface():
    return TestNurbsSurface.from_parameters(
        points=[[[0, 0, 0], [1, 0, 0]], [[0, 1, 0], [1, 1, 0]]],
        weights=[[1.0, 0.5], [1.0, 1.0]],
        knots_u=[0.0, 1.0],
        knots_v=[0.0, 1.0],
        mults_u=[2, 2],
        mults_v=[2, 2],
        degree_u=1,
        degree_v=1,
    )


def test_nurbs_surface_derived_properties(surface):
    assert surface.knotvector_u == [0.0, 0.0, 1.0, 1.0]
    assert surface.knotvector_v == [0.0, 0.0, 1.0, 1.0]
    assert surface.order_u == 2
    assert surface.order_v == 2
    assert surface.is_rational


def test_nurbs_surface_data_roundtrip_preserves_concrete_class(surface):
    other = TestNurbsSurface.__from_data__(surface.__data__)

    assert isinstance(other, TestNurbsSurface)
    assert other.__data__ == surface.__data__


def test_nurbs_surface_copy_preserves_concrete_class_and_is_independent(surface):
    other = surface.copy()

    assert isinstance(other, TestNurbsSurface)
    assert other.__data__ == surface.__data__
    assert other.points[0][0] is not surface.points[0][0]


def test_nurbs_surface_meshgrid_uses_requested_interval_counts():
    surface = TestNurbsSurface.from_meshgrid(nu=2, nv=3)

    assert len(surface.points) == 4
    assert len(surface.points[0]) == 3
    assert surface.degree_u == 2
    assert surface.degree_v == 3
    assert surface.points[1][2] == [2.0, 1.0, 0.0]


@pytest.mark.parametrize("nu, nv", [(0, 1), (1, 0), (-1, 1), (1, -1)])
def test_nurbs_surface_meshgrid_requires_positive_interval_counts(nu, nv):
    with pytest.raises(ValueError, match="at least one interval"):
        TestNurbsSurface.from_meshgrid(nu=nu, nv=nv)
