from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from compas.geometry import Plane

__all__ = ['Cylinder']


class Cylinder(object):
    """A cylinder is defined by a plane, a radius and a height.

    Attributes
    ----------
    plane: :class:`compas.geometry.Plane`
        The plane of the cylinder.
    radius: float
        The radius of the cylinder.
    height: float
        The height of the cylinder.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cylinder
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> cylinder = Cylinder(plane, 5, 7)

    """

    __slots__ = ['_plane', '_radius', '_height']

    def __init__(self, plane, radius, height):
        self._plane = None
        self._radius = None
        self._height = None
        self.plane = plane
        self.radius = radius
        self.height = height

    @classmethod
    def from_data(cls, data):
        """Construct a cylinder from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Cylinder
            The constructed cylinder.

        Examples
        --------
        >>> from compas.geometry import Cylinder
        >>> from compas.geometry import Plane
        >>> data = {'plane': Plane.worldXY().data, 'radius': 5., 'height': 7.}
        >>> cylinder = Cylinder.from_data(data)

        """
        cylinder = cls(Plane.worldXY(), 1, 1)
        cylinder.data = data
        return cylinder

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def plane(self):
        """Plane: The plane of the cylinder."""
        return self._plane

    @plane.setter
    def plane(self, plane):
        self._plane = Plane(plane[0], plane[1])

    @property
    def radius(self):
        """float: The radius of the cylinder."""
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)
    
    @property
    def height(self):
        """float: The height of the cylinder."""
        return self._height

    @height.setter
    def height(self, height):
        self._height = float(height)

    @property
    def normal(self):
        """Vector: The normal of the cylinder."""
        return self.plane.normal

    @property
    def diameter(self):
        """float: The diameter of the cylinder."""
        return self.radius * 2

    @property
    def data(self):
        """Returns the data dictionary that represents the cylinder.

        Returns
        -------
        dict
            The cylinder data.

        """
        return {'plane': self.plane.data,
                'radius': self.radius}

    @data.setter
    def data(self, data):
        self.plane = Plane.from_data(data['plane'])
        self.radius = data['radius']
        self.height = data['height']

    def to_data(self):
        """Returns the data dictionary that represents the cylinder.

        Returns
        -------
        dict
            The cylinder data.

        """
        return self.data

    @property
    def center(self):
        """Point: The center of the cylinder."""
        return self.plane.point

    @center.setter
    def center(self, point):
        self.plane.point = point

    @property
    def area(self):
        """Float: The area of the cylinder."""
        return (pi * (self.radius**2) * 2) + (2 * pi * self.radius * self.height)

    @property
    def circumference(self):
        """Float: The circumference of the cylinder."""
        return 2 * pi * self.radius
    
    @property
    def volume(self):
        """Float: The volume of the cylinder."""
        return pi * (self.radius**2) * self.height

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Cylinder({0}, {1}, {2})'.format(self.plane, self.radius, self.height)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.radius
        elif key == 2:
            return self.height
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.radius = value
        elif key == 2:
            self.height = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.radius, self.height])

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Makes a copy of this ``Cylinder``.

        Returns
        -------
        Cylinder
            The copy.

        """
        cls = type(self)
        return cls(self.plane.copy(), self.radius, self.height)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the cylinder.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the cylinder.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Cylinder
        >>> cylinder = Cylinder(Plane.worldXY(), 5, 7)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> cylinder.transform(T)

        """
        self.plane.transform(transformation)

    def transformed(self, transformation):
        """Returns a transformed copy of the current cylinder.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the cylinder.

        Returns
        -------
        :class:`cylinder`
            The transformed cylinder.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Cylinder
        >>> cylinder = Cylinder(Plane.worldXY(), 5, 7)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> circle_transformed = cylinder.transformed(T)

        """
        cylinder = self.copy()
        cylinder.transform(transformation)
        return cylinder


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas.geometry import Frame
    from compas.geometry import Transformation
    cylinder = Cylinder(Plane.worldXY(), 5, 7)
    frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    print(frame.normal)
    T = Transformation.from_frame(frame)
    cylinder.transform(T)
    print(cylinder)

    print(Plane.worldXY().data)
    data = {'plane': Plane.worldXY().data, 'radius': 5., 'height': 7.}
    cylinder = Cylinder.from_data(data)
    print(cylinder)

    import doctest
    doctest.testmod()
