from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Plane


__all__ = ['Circle']


class Circle(Primitive):
    """A circle is defined by a plane and a radius.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane` or tuple of point and normal
        The plane of the circle.
    radius : float
        The radius of the circle.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane of the circle.
    radius : float
        The radius.
    center : :class:`compas.geometry.Point`
        The base point of the plane and center of the circle.
    normal : :class:`compas.geometry.Vector`
        The normal vector of the plane.
    diameter : float, read-only
        The diameter of the circle.
    circumference : float, read-only
        The circumference of the circle.
    area : float, read-only
        The area of the circle.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Circle
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    """

    __slots__ = ['_plane', '_radius']

    def __init__(self, plane, radius):
        super(Circle, self).__init__()
        self._plane = None
        self._radius = None
        self.plane = plane
        self.radius = radius

    @property
    def data(self):
        """dict : The data dictionary that represents the circle."""
        return {'plane': [list(self.plane.point), list(self.plane.normal)], 'radius': self.radius}

    @data.setter
    def data(self, data):
        self.plane = data['plane']
        self.radius = data['radius']

    @property
    def plane(self):
        """:class:`compas.geometry.Plane` : The plane of the circle."""
        return self._plane

    @plane.setter
    def plane(self, plane):
        self._plane = Plane(plane[0], plane[1])

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
        return self.plane.normal

    @property
    def diameter(self):
        """float: The diameter of the circle."""
        return self.radius * 2

    @property
    def center(self):
        """:class:`compas.geometry.Point` : The center of the circle."""
        return self.plane.point

    @center.setter
    def center(self, point):
        self.plane.point = point

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
        return 'Circle({0}, {1})'.format(self.plane, self.radius)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.radius])

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
        >>> data = {'plane': [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], 'radius': 5.}
        >>> circle = Circle.from_data(data)
        """
        return cls(data['plane'], data['radius'])

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
        self.plane.transform(T)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
