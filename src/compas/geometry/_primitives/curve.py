from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import scale_vector
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import add_vectors
from compas.geometry.basic import subtract_vectors

from compas.geometry._primitives import Point
from compas.geometry._primitives import Vector

from compas.utilities import binomial_coefficient

__all__ = ['Bezier']


def bernstein(n, k, t):
    """k:sup:`th` of `n` + 1 Bernstein basis polynomials of degree `n`. A
    weighted linear combination of these basis polynomials is called a Bernstein
    polynomial [wikipedia2017k]_.

    Notes
    -----
    When constructing Bezier curves, the weights are simply the coordinates
    of the control points of the curve.

    Parameters
    ----------
    n : int
        The degree of the polynomial.
    k : int
        The number of the basis polynomial.
    t : float
        The variable.

    Returns
    -------
    float
        The value of the Bernstein basis polynomial at `t`.

    """
    if k < 0:
        return 0
    if k > n:
        return 0
    return binomial_coefficient(n, k) * t ** k * (1 - t) ** (n - k)


class BezierException(Exception):
    pass


class Bezier(object):
    """A Bezier curve.

    A Bezier curve of degree `n` is a linear combination of `n` + 1 Bernstein
    basis polynomials of degree `n`.

    Parameters
    ----------
    points : sequence
        A sequence of control points, represented by their location in 3D space.

    Attributes
    ----------
    points : list
        The control points.
    degree : int
        The degree of the curve.

    """
    def __init__(self, points):
        self._points = []
        self.points = points

    @property
    def points(self):
        """The control points.

        Parameters
        ----------
        points : sequence
            A sequence of control point locations in 3d space.

        Returns
        -------
        list
            A list of ``Point`` objects.

        """
        return self._points

    @points.setter
    def points(self, points):
        if points:
            self._points = [Point(*point) for point in points]

    @property
    def degree(self):
        """The degree of the curve."""
        return len(self.points) - 1

    def compute_point(self, t):
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
        n = self.degree
        point = Point(0, 0, 0)
        for i, p in enumerate(self.points):
            b = bernstein(n, i, t)
            point += p * b
        return point

    def compute_tangent(self, t):
        n = self.degree
        v = Vector(0, 0, 0)
        for i, p in enumerate(self.points):
            a = bernstein(n - 1, i - 1, t)
            b = bernstein(n - 1, i, t)
            c = n * (a - b)
            v += p * c
        v.unitize()
        return v

    def compute_locus(self, resolution=100):
        """Compute the locus of all points on the curve.

        Parameters
        ----------
        resolution : int
            The number of intervals at which a point on the
            curve should be computed. Defaults to 100.

        Returns
        -------
        list

        """
        locus = []
        divisor = float(resolution - 1)
        for i in range(resolution):
            t = i / divisor
            locus.append(self.compute_point(t))
        return locus

    def draw(self, params=None):
        import matplotlib.pyplot as plt
        locus = self.compute_locus()
        x, y, _ = zip(*locus)
        plt.plot(x, y, '-b')
        x, y, _ = zip(* self.points)
        plt.plot(x, y, 'ro')
        if params is not None:
            for t in params:
                p0 = self.compute_point(t)
                v = self.compute_tangent(t)
                p1 = p0 + v
                plt.plot([p0[0], p1[0]], [p0[1], p1[1]], '-k')
                plt.plot([p0[0]], [p0[1]], 'ok')
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    curve = Bezier([[0, 0, 0], [1, -1, 0], [2, +1, 0], [3, 0, 0]])
    curve.draw(params=[0.1, 0.2, 0.3, 0.4, 0.5])
