from compas.geometry.objects.point import Point
from compas.geometry.objects.line import Line


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Polyline']


# def align_polylines(pointsets, tol=0.001):
#     tol = tol**2
#     aligned = [pointsets[0][1:]]
#     found = [0]
#     n = len(pointsets)
#     for i in range(n):
#         ep = aligned[-1][-1]
#         for j in range(n):
#             if j in found:
#                 continue
#             points = pointsets[j]
#             sp = points[0]
#             if (sp[0] - ep[0]) ** 2 < tol and (sp[1] - ep[1]) ** 2 < tol and (sp[2] - ep[2]) ** 2 < tol:
#                 aligned.append(points[1:])
#                 found.append(j)
#                 break
#             sp = points[-1]
#             if (sp[0] - ep[0]) ** 2 < tol and (sp[1] - ep[1]) ** 2 < tol and (sp[2] - ep[2]) ** 2 < tol:
#                 points[:] = points[::-1]
#                 aligned.append(points[1:])
#                 found.append(j)
#                 break
#     if len(aligned) == len(pointsets):
#         return aligned
#     return None


# def join_polylines(pointsets):
#     return [point for points in pointsets for point in points]


class Polyline(object):
    """A polyline object represents a concatenation of lines.

    A polyline is a piecewise linear element. It does not have an interior. It
    can be open or closed. It can be self-intersecting.

    Parameters:
        points (tuple, list): A list of points in three-dimensional space.

    Attributes:
        points (list): A list of ``Point`` objects.
        lines (list): A list of ``Line`` objects.
        p (int): The number of objects in `points`.
        l (int): The number of objects in 'lines'.
        length (float): The length of the polyline.

    Examples:
        >>> polyline = Polyline([[0,0,0], [1,0,0], [2,0,0], [3,0,0]])
        >>> polyline.length
        3.0

        >>> type(polyline.points[0])
        <class 'point.Point'>
        >>> polyline.points[0].x
        0.0

        >>> type(polyline.lines[0])
        <class 'line.Line'>
        >>> polyline.lines[0].length
        1.0

    """
    def __init__(self, points):
        self._points = []
        self._lines = []
        self._p = 0
        self._l = 0
        self.points = points

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def points(self):
        """The points of the polyline.

        Parameters:
            points (sequence): A sequence of xyz coordinates.

        Returns:
            list: A list of ``Point`` objects.
        """
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*xyz) for xyz in points]
        self._p = len(points)
        self._lines = [Line(self._points[i], self._points[i + 1]) for i in range(0, self._p - 1)]
        self._l = len(self._lines)

    @property
    def lines(self):
        """The lines of the polyline.

        Parameters:
            None

        Returns:
            list: A list of ``Line`` objects.
        """
        return self._lines

    @property
    def p(self):
        """The number of points."""
        return self._p

    @property
    def l(self):
        """The number of lines."""
        return self._l

    @property
    def length(self):
        """The length of the polyline."""
        return sum([line.length for line in self.lines])

    def is_selfintersecting(self):
        """Return True if the polyline is `self-intersecting`, False otherwise.
        """
        raise NotImplementedError

    def is_closed(self):
        """Verify if the polyline is closed. The polyline is closed if the first
        and last point are identical.

        Returns:
            bool: True if the polyline is closed, False otherwise.
        """
        return self.points[0] == self.points[-1]

    # ==========================================================================
    # representation
    # ==========================================================================

    # ==========================================================================
    # access
    # ==========================================================================

    # ==========================================================================
    # comparison
    # ==========================================================================

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    # ==========================================================================
    # transformations
    # ==========================================================================


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == '__main__':

    polyline = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]])
    print(polyline.lines)
    print(polyline.length)

    print(type(polyline.points[0]))
    print(polyline.points[0].x)

    print(type(polyline.lines[0]))
    print(polyline.lines[0].length)

    print(polyline.is_closed())
