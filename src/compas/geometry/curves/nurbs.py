from compas.geometry import Point
from ._curve import Curve


class NURBSCurve(Curve):

    def __init__(self, dimension, is_rational, order, pointcount):
        self._points = None
        self._knots = None

    @property
    def data(self):
        return {'points': [point.data for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = [Point.from_data(point) for point in data['points']]

    @property
    def degree(self):
        pass

    @property
    def dimension(self):
        pass

    @property
    def domain(self):
        pass

    @property
    def order(self):
        pass

    @property
    def is_closed(self):
        pass

    @property
    def is_periodic(self):
        pass

    @property
    def is_rational(self):
        pass

    @property
    def knots(self):
        pass

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(x, y, z) for x, y, z in points]

    @property
    def start(self):
        pass

    @property
    def end(self):
        pass

    @classmethod
    def from_points(cls, points, degree, is_periodic=False):
        pass

    @classmethod
    def from_arc(cls, arc, degree, pointcount=None):
        pass

    @classmethod
    def from_circle(cls, circle, degree, pointcount=None):
        pass

    @classmethod
    def from_ellipse(cls, ellipse, degree, pointcount=None):
        pass

    @classmethod
    def from_line(cls, line, degree, pointcount=None):
        pass

    @classmethod
    def from_data(cls, data):
        """Construct a Bézier curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.BezierCurve`
            The constructed bezier curve.

        """
        return cls([Point.from_data(point) for point in data['points']])

    def point(self, t):
        """Compute a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Point
            the corresponding point on the curve.
        """
        pass

    def locus(self, resolution=100):
        """Compute the locus of all points on the curve.

        Parameters
        ----------
        resolution : int
            The number of intervals at which a point on the
            curve should be computed. Defaults to 100.

        Returns
        -------
        list
            Points along the curve.

        """
        locus = []
        divisor = float(resolution - 1)
        for i in range(resolution):
            t = i / divisor
            locus.append(self.point(t))
        return locus

    def tangent(self, t):
        """Compute the tangent vector at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Vector
            The corresponding tangent vector.

        """
        pass
