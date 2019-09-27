from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.geometry.primitives import Plane
from compas.geometry.primitives import Circle

from compas.geometry.primitives.shapes import Shape

__all__ = ['Cylinder']


class Cylinder(Shape):
    """A cylinder is defined by a circle and a height.

    Attributes
    ----------
    circle: :class:`compas.geometry.Circle`
        The circle of the cylinder.
    height: float
        The height of the cylinder.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cylinder
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cylinder = Cylinder(circle, 7)

    """

    __slots__ = ['_circle', '_height']

    def __init__(self, circle, height):
        self._circle = None
        self._height = None
        self.circle = circle
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
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Plane
        >>> data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
        >>> cylinder = Cylinder.from_data(data)

        """
        cylinder = cls(Circle(Plane.worldXY(), 1), 1)
        cylinder.data = data
        return cylinder

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def plane(self):
        """Plane: The plane of the cylinder."""
        return self.circle.plane

    @plane.setter
    def plane(self, plane):
        self.circle.plane = Plane(plane[0], plane[1])

    @property
    def circle(self):
        """float: The circle of the cylinder."""
        return self._circle

    @circle.setter
    def circle(self, circle):
        self._circle = circle

    @property
    def radius(self):
        """float: The radius of the cylinder."""
        return self.circle.radius

    @radius.setter
    def radius(self, radius):
        self.circle.radius = float(radius)

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
        return self.circle.diameter

    @property
    def data(self):
        """Returns the data dictionary that represents the cylinder.

        Returns
        -------
        dict
            The cylinder data.

        """
        return {'circle': self.circle.data,
                'height': self.height}

    @data.setter
    def data(self, data):
        self.circle = Circle.from_data(data['circle'])
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
        return self.circle.center

    @center.setter
    def center(self, point):
        self.circle.center = point

    @property
    def area(self):
        """Float: The surface area of the cylinder."""
        return (self.circle.area * 2) + (self.circle.circumference * self.height)

    @property
    def volume(self):
        """Float: The volume of the cylinder."""
        return self.circle.area * self.height

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Cylinder({0}, {1})'.format(self.circle, self.height)

    def __len__(self):
        return 2

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.circle
        elif key == 1:
            return self.height
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.circle = value
        elif key == 1:
            self.height = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.circle, self.height])

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
        return cls(self.circle.copy(), self.height)

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
        self.circle.transform(transformation)

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
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Cylinder
        >>> cylinder = Cylinder(Circle(Plane.worldXY(), 5), 7)
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
    from compas.geometry import Circle
    from compas.geometry import Cylinder

    cylinder = Cylinder(Circle(Plane.worldXY(), 5), 7)
    frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    print(frame.normal)
    T = Transformation.from_frame(frame)
    cylinder.transform(T)
    print(cylinder)

    print(Plane.worldXY().data)
    data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
    cylinder = Cylinder.from_data(data)
    print(cylinder)

    import doctest
    doctest.testmod()
