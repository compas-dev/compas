from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import NurbsCurve
from compas.tolerance import TOL


class StubNurbsCurve(NurbsCurve):
    @property
    def knots(self):
        return [0.0, 0.5, 1.0]

    @property
    def multiplicities(self):
        return [3, 1, 3]


def test_nurbscurve_forwards_interpolation_precision(monkeypatch):
    captured = {}
    sentinel = object()

    def factory(points, precision):
        captured.update(points=points, precision=precision)
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.from_interpolation", factory)
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

    assert NurbsCurve.from_interpolation(points, precision=0.25) is sentinel
    assert captured == {"points": points, "precision": 0.25}


def test_nurbscurve_forwards_periodicity(monkeypatch):
    captured = {}
    native_curve = object()

    def factory(points, weights, knots, multiplicities, degree, is_periodic):
        captured.update(
            points=points,
            weights=weights,
            knots=knots,
            multiplicities=multiplicities,
            degree=degree,
            is_periodic=is_periodic,
        )
        return NurbsCurve(native_curve)

    monkeypatch.setattr("compas.geometry.curves.nurbs.from_parameters", factory)

    result = StubNurbsCurve.from_parameters([[0.0, 0.0, 0.0]], [1.0], [0.0], [1], 1, is_periodic=True)

    assert type(result) is NurbsCurve
    assert result.native_curve is native_curve
    assert captured["is_periodic"] is True


def test_nurbscurve_from_points_forwards_periodicity(monkeypatch):
    captured = {}
    sentinel = object()

    def factory(points, degree, is_periodic):
        captured.update(points=points, degree=degree, is_periodic=is_periodic)
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.from_points", factory)
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

    assert NurbsCurve.from_points(points, degree=1, is_periodic=True) is sentinel
    assert captured == {"points": points, "degree": 1, "is_periodic": True}


def test_nurbscurve_from_ellipse_preserves_frame(monkeypatch):
    captured = {}
    sentinel = object()

    def factory(points, weights, knots, multiplicities, degree, is_periodic):
        captured.update(points=points)
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.from_parameters", factory)
    ellipse = Ellipse(major=2.0, minor=1.0, frame=Frame.worldZX())

    assert NurbsCurve.from_ellipse(ellipse) is sentinel
    assert all(TOL.is_zero(point.y) for point in captured["points"])
    assert TOL.is_allclose(captured["points"][2], ellipse.center - ellipse.frame.xaxis * ellipse.major)


def test_nurbscurve_knotvector_expands_multiplicities():
    curve = StubNurbsCurve()

    assert curve.knotvector == [0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0]


def test_nurbscurve_query_dispatch_uses_core_wrapper(monkeypatch):
    curve = NurbsCurve(object())
    captured = []

    def query(value):
        captured.append(value)
        return [1.0, 2.0]

    monkeypatch.setattr("compas.geometry.curves.nurbs.curve_weights", query)

    assert curve.weights == [1.0, 2.0]
    assert captured == [curve]


def test_nurbscurve_mutation_dispatch_uses_core_wrapper(monkeypatch):
    curve = NurbsCurve(object())
    captured = []

    def reverse(value):
        captured.append(value)

    monkeypatch.setattr("compas.geometry.curves.nurbs.curve_reverse", reverse)

    curve.reverse()

    assert captured == [curve]
