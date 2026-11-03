from math import inf
from math import nan

import pytest

from compas.geometry import NurbsSurface
from compas.geometry import Point
from compas.geometry import Translation


class StubNurbsSurface(NurbsSurface):
    def __init__(self):
        super().__init__()
        self._points = [[Point(0, 0, 0), Point(1, 0, 0)], [Point(0, 1, 0), Point(1, 1, 0)]]

    @property
    def control_points(self):
        return self._points

    @property
    def weights(self):
        return [[1.0, 0.5], [1.0, 1.0]]

    @property
    def knots_u(self):
        return [0.0, 1.0]

    @property
    def knots_v(self):
        return [0.0, 1.0]

    @property
    def mults_u(self):
        return [2, 2]

    @property
    def mults_v(self):
        return [2, 2]

    @property
    def degree_u(self):
        return 1

    @property
    def degree_v(self):
        return 1

    @property
    def domain_u(self):
        return 0.0, 1.0

    @property
    def domain_v(self):
        return 0.0, 1.0

    @property
    def is_periodic_u(self):
        return False

    @property
    def is_periodic_v(self):
        return False


class BoundsNurbsSurface(NurbsSurface):
    def __init__(self, points, weights):
        super().__init__()
        self._points = points
        self._weights = weights

    @property
    def control_points(self):
        return self._points

    @property
    def weights(self):
        return self._weights

    def point_at(self, u, v):
        """Evaluate the rational bilinear test surface."""
        basis_u = [1.0 - u, u]
        basis_v = [1.0 - v, v]
        denominator = 0.0
        coordinates = [0.0, 0.0, 0.0]
        for row in range(2):
            for column in range(2):
                coefficient = basis_u[column] * basis_v[row] * self._weights[row][column]
                denominator += coefficient
                for axis in range(3):
                    coordinates[axis] += coefficient * self._points[row][column][axis]
        return Point(*(coordinate / denominator for coordinate in coordinates))


@pytest.fixture
def surface():
    return StubNurbsSurface()


def test_nurbs_surface_derived_properties(surface):
    assert surface.knotvector_u == [0.0, 0.0, 1.0, 1.0]
    assert surface.knotvector_v == [0.0, 0.0, 1.0, 1.0]
    assert surface.order_u == 2
    assert surface.order_v == 2
    assert surface.is_rational


def test_nurbs_surface_data_reconstruction_returns_core_wrapper(surface, monkeypatch):
    captured = {}
    native_surface = object()

    def factory(*args, **kwargs):
        captured.update(points=args[0], is_periodic_u=kwargs["is_periodic_u"], is_periodic_v=kwargs["is_periodic_v"])
        return NurbsSurface(native_surface)

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.from_parameters", factory)

    other = StubNurbsSurface.__from_data__(surface.__data__)

    assert type(other) is NurbsSurface
    assert other.native_surface is native_surface
    assert captured["points"] == surface.__data__["control_points"]
    assert captured["is_periodic_u"] is False
    assert captured["is_periodic_v"] is False


def test_nurbs_surface_copy_returns_independent_core_wrapper(surface, monkeypatch):
    native_surface = object()

    def factory(*args, **kwargs):
        return NurbsSurface(native_surface)

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.from_parameters", factory)

    other = surface.copy()

    assert type(other) is NurbsSurface
    assert other.native_surface is native_surface


def test_nurbs_surface_meshgrid_uses_requested_interval_counts(monkeypatch):
    captured = {}
    result = NurbsSurface(object())

    def factory(points, degree_u, degree_v):
        captured.update(points=points, degree_u=degree_u, degree_v=degree_v)
        return result

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.from_points", factory)

    surface = StubNurbsSurface.from_meshgrid(nu=2, nv=3)

    assert surface is result
    assert len(captured["points"]) == 4
    assert len(captured["points"][0]) == 3
    assert captured["points"][1][2] == [2.0, 1.0, 0.0]


@pytest.mark.parametrize("nu, nv", [(0, 1), (1, 0), (-1, 1), (1, -1)])
def test_nurbs_surface_meshgrid_requires_positive_interval_counts(nu, nv):
    with pytest.raises(ValueError, match="at least one interval"):
        NurbsSurface.from_meshgrid(nu=nu, nv=nv)


def test_nurbs_surface_query_dispatch_uses_core_wrapper(monkeypatch):
    surface = NurbsSurface(object())
    captured = []

    def query(value):
        captured.append(value)
        return [0.0, 1.0]

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.surface_knots_u", query)

    assert surface.knots_u == [0.0, 1.0]
    assert captured == [surface]


def test_nurbs_surface_evaluation_dispatch_uses_core_wrapper(monkeypatch):
    surface = NurbsSurface(object())
    point = Point(1, 2, 3)
    captured = []

    def evaluate(value, u, v):
        captured.append((value, u, v))
        return point

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.surface_point_at", evaluate)

    assert surface.point_at(0.25, 0.75) is point
    assert captured == [(surface, 0.25, 0.75)]


def test_nurbs_surface_aabb_is_control_net_enclosure_without_sampling(monkeypatch):
    surface = BoundsNurbsSurface(
        [
            [Point(-2, 1, 4), Point(3, -1, 4)],
            [Point(0, 5, 4), Point(1, 2, 4)],
        ],
        [[1.0, 0.5], [2.0, 1.0]],
    )

    def fail_if_sampled(*args, **kwargs):
        raise AssertionError("NURBS bounds should not sample the surface.")

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.surface_point_at", fail_if_sampled)

    bounds = surface.aabb

    assert list(bounds.frame.point) == pytest.approx([0.5, 2.0, 4.0])
    assert bounds.dimensions == pytest.approx([5.0, 6.0, 0.0])


def test_nurbs_surface_aabb_encloses_evaluated_positive_weight_surface():
    surface = BoundsNurbsSurface(
        [
            [Point(-2, 1, 0), Point(3, -1, 2)],
            [Point(0, 5, -3), Point(1, 2, 4)],
        ],
        [[1.0, 0.25], [3.0, 1.5]],
    )

    bounds = surface.aabb
    points = [surface.point_at(u / 10.0, v / 10.0) for u in range(11) for v in range(11)]

    assert bounds.contains_points(points)


def test_nurbs_surface_aabb_follows_backend_control_net_transform(monkeypatch):
    surface = BoundsNurbsSurface(
        [
            [Point(-2, 1, 0), Point(3, -1, 2)],
            [Point(0, 5, -3), Point(1, 2, 4)],
        ],
        [[1.0, 0.25], [3.0, 1.5]],
    )
    transformation = Translation.from_vector([7.0, -4.0, 2.0])
    initial = surface.aabb

    def transform_control_net(value, xform):
        value._points = [[point.transformed(xform) for point in row] for row in value._points]

    monkeypatch.setattr("compas.geometry.surfaces.nurbs.surface_transform", transform_control_net)

    surface.transform(transformation)
    transformed = surface.aabb

    assert list(transformed.frame.point) == pytest.approx(list(initial.frame.point.transformed(transformation)))
    assert transformed.dimensions == pytest.approx(initial.dimensions)


@pytest.mark.parametrize(
    "points, weights, message",
    [
        ([], [], "nonempty control-point grid"),
        ([[]], [[]], "nonempty control-point grid"),
        (
            [[Point(0, 0, 0)], [Point(0, 0, 0), Point(1, 0, 0)]],
            [[1.0], [1.0, 1.0]],
            "control-point grid should be rectangular",
        ),
        ([[Point(0, 0, 0)]], [], "weight grid should match"),
        ([[Point(0, 0, 0)]], [[0.0]], "strictly positive weights"),
        ([[Point(0, 0, 0)]], [[-1.0]], "strictly positive weights"),
        ([[Point(0, 0, 0)]], [[inf]], "strictly positive weights"),
        ([[Point(0, 0, 0)]], [[nan]], "strictly positive weights"),
        ([[Point(inf, 0, 0)]], [[1.0]], "finite control-point coordinates"),
    ],
)
def test_nurbs_surface_aabb_rejects_uncertified_control_nets(points, weights, message):
    surface = BoundsNurbsSurface(points, weights)

    with pytest.raises(ValueError, match=message):
        surface.aabb
