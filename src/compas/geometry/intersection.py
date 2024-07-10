from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from compas.precision import Precision
from compas.geometry import distance_point_point


class Intersection(object):
    """A class for computing intersections between geometric objects.

    Attributes
    ----------
    number_of_intersections : int
        The number of intersections.
    points : list[:class:`compas.geometry.Point`]
        The intersection points.

    Examples
    --------
    >>> from compas.geometry import Line  # doctest: +SKIP
    >>> from compas.geometry import Intersection  # doctest: +SKIP
    >>> a = Line([0, 0, 0], [2, 0, 0])  # doctest: +SKIP
    >>> b = Line([1, 0, 0], [1, 1, 0])  # doctest: +SKIP
    >>> intersection = Intersection()  # doctest: +SKIP
    >>> intersection.line_line(a, b)  # doctest: +SKIP
    >>> intersection.number_of_intersections  # doctest: +SKIP
    1
    >>> intersection.points[0]  # doctest: +SKIP
    Point(1.0, 0.0, z=0.0)

    """

    def __init__(self):
        self.number_of_intersections = 0
        self.points = []

    def __len__(self):
        return self.number_of_intersections

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def line_line(self, a, b, tol=1e-6):
        """Compute the intersection of two lines.

        Parameters
        ----------
        a : :class:`compas.geometry.Line`
            A line.
        b : :class:`compas.geometry.Line`
            A line.
        tol : float, optional
            The tolerance for numerical fuzz.

        Returns
        -------
        None

        """
        from compas.geometry import intersection_line_line

        x1, x2 = intersection_line_line(a, b)

        if x1 is None or x2 is None:
            self.number_of_intersections = 0
            self.points = []
            return

        if distance_point_point(x1, x2) < tol:
            self.number_of_intersections = 1
            self.points = [x1]
            return

        self.number_of_intersections = 2
        self.points = [x1, x2]

    def line_segment(self, a, b):
        pass

    def line_polyline(self, a, b):
        pass

    def line_plane(self, a, b):
        pass

    def line_circle(self, a, b):
        pass

    def line_ellipse(self, a, b):
        pass

    def line_curve(self, a, b):
        pass

    def line_surface(self, a, b):
        pass

    def line_box(self, a, b):
        pass

    def line_sphere(self, a, b):
        pass

    def line_cylinder(self, a, b):
        pass

    def line_cone(self, a, b):
        pass

    def line_torus(self, a, b):
        pass

    def line_triangle(self, a, b):
        pass

    def line_mesh(self, a, b):
        pass
