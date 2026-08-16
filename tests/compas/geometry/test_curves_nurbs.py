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

    def factory(cls, points, precision):
        captured.update(cls=cls, points=points, precision=precision)
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.nurbscurve_from_interpolation", factory)
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

    assert NurbsCurve.from_interpolation(points, precision=0.25) is sentinel
    assert captured == {"cls": NurbsCurve, "points": points, "precision": 0.25}


def test_nurbscurve_forwards_periodicity(monkeypatch):
    captured = {}
    sentinel = object()

    def factory(cls, points, weights, knots, multiplicities, degree, is_periodic):
        captured.update(
            cls=cls,
            points=points,
            weights=weights,
            knots=knots,
            multiplicities=multiplicities,
            degree=degree,
            is_periodic=is_periodic,
        )
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.nurbscurve_from_parameters", factory)

    result = NurbsCurve.from_parameters([[0.0, 0.0, 0.0]], [1.0], [0.0], [1], 1, is_periodic=True)

    assert result is sentinel
    assert captured["is_periodic"] is True


def test_nurbscurve_from_points_forwards_periodicity(monkeypatch):
    captured = {}
    sentinel = object()

    def factory(cls, points, degree, is_periodic):
        captured.update(cls=cls, points=points, degree=degree, is_periodic=is_periodic)
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.nurbscurve_from_points", factory)
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]

    assert NurbsCurve.from_points(points, degree=1, is_periodic=True) is sentinel
    assert captured == {"cls": NurbsCurve, "points": points, "degree": 1, "is_periodic": True}


def test_nurbscurve_from_ellipse_preserves_frame(monkeypatch):
    captured = {}
    sentinel = object()

    def factory(cls, points, weights, knots, multiplicities, degree, is_periodic):
        captured.update(points=points)
        return sentinel

    monkeypatch.setattr("compas.geometry.curves.nurbs.nurbscurve_from_parameters", factory)
    ellipse = Ellipse(major=2.0, minor=1.0, frame=Frame.worldZX())

    assert NurbsCurve.from_ellipse(ellipse) is sentinel
    assert all(TOL.is_zero(point.y) for point in captured["points"])
    assert TOL.is_allclose(captured["points"][2], ellipse.center - ellipse.frame.xaxis * ellipse.major)


def test_nurbscurve_knotvector_expands_multiplicities():
    curve = StubNurbsCurve()

    assert curve.knotvector == [0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0]
