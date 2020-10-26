from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from ._primitive import Primitive
from .point import Point
from .vector import Vector


__all__ = ['Circle']


class Circle(Primitive):
    """A circle is defined by a plane and a radius.

    Parameters
    ----------
    point : :class:`compas.geometry.Point` or [float, float, float]
        The center point of the circle.
    radius : float
        The radius of the circle.
    normal : :class:`compas.geometry.Vector` or [float, float, float], optional
        The normal of the plane of the circle.
        Default is ``Vector(0, 0, 1)``.

    Attributes
    ----------
    point : :class:`compas.geometry.Point`
        The center point of the circle.
    radius : float
        The radius.
    normal : :class:`compas.geometry.Vector`
        The normal vector of the plane.
    center : :class:`compas.geometry.Point`
        Alias for ``Circle.point``.
    diameter : float, read-only
        The diameter of the circle.
    circumference : float, read-only
        The circumference of the circle.
    area : float, read-only
        The area of the circle.

    Examples
    --------
    >>> from compas.geometry import Circle
    >>> circle = Circle([0, 0, 0], 5)
    """

    __slots__ = ['_point', '_radius', '_normal']

    def __init__(self, point, radius, normal=None):
        super(Circle, self).__init__()
        self._point = None
        self._radius = None
        self._normal = None
        self.point = point
        self.radius = radius
        self.normal = normal

    @property
    def data(self):
        """dict : The data dictionary that represents the circle."""
        return {'point': self.point, 'radius': self.radius, 'normal': self.normal}

    @data.setter
    def data(self, data):
        self.point = data['point']
        self.radius = data['radius']
        self.normal = data['normal']

    @property
    def point(self):
        """:class:`compas.geometry.Point` : The center point of the circle."""
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def radius(self):
        """float : The radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)

    @property
    def normal(self):
        """:class:`compas.geometry.Vector` : The normal of the circle."""
        return self._normal

    @normal.setter
    def normal(self, normal):
        if not normal:
            normal = [0, 0, 1]
        self._normal = Vector(*normal)

    @property
    def diameter(self):
        """float: The diameter of the circle."""
        return self.radius * 2

    @property
    def center(self):
        """:class:`compas.geometry.Point` : The center of the circle."""
        return self.point

    @center.setter
    def center(self, point):
        self.point = point

    @property
    def area(self):
        """float  : The area of the circle."""
        return pi * (self.radius**2)

    @property
    def circumference(self):
        """float : The circumference of the circle."""
        return 2 * pi * self.radius

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return 'Circle({0}, {1}, {2})'.format(self.point, self.radius, self.normal)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.point
        elif key == 1:
            return self.radius
        elif key == 2:
            return self.normal
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
        elif key == 1:
            self.radius = value
        elif key == 2:
            self.normal = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.point, self.radius, self.normal])

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a circle from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The constructed circle.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> data = {'point': [0.0, 0.0, 0.0], 'radius': 5., 'normal': [0.0, 0.0, 1.0]}
        >>> circle = Circle.from_data(data)
        """
        return cls(data['point'], data['radius'], data['normal'])

    # ==========================================================================
    # methods
    # ==========================================================================

    def transform(self, T):
        """Transform the circle.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> circle = Circle(Plane.worldXY(), 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> circle.transform(T)
        """
        self.point.transform(T)
        self.normal.transform(T)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
