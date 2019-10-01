from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.geometry.primitives import Plane
from compas.geometry.primitives.shapes import Shape

__all__ = ['Torus']


class Torus(Shape):
    """A torus is defined by a plane and two radii.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane of the torus.
    radius_axis: float
        The radius of the axis.
    radius_pipe: float
        The radius of the pipe.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Torus
    >>> torus = Torus(Plane.worldXY(), 5., 2.)

    """

    __slots__ = ['_plane', '_radius_axis', '_radius_pipe']

    def __init__(self, plane, radius_axis, radius_pipe):
        self._plane = None
        self._radius_axis = None
        self._radius_pipe = None
        self.plane = plane
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    @classmethod
    def from_data(cls, data):
        """Construct a torus from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Torus
            The constructed torus.

        Examples
        --------
        >>> from compas.geometry import Torus
        >>> data = {'plane': Plane.worldXY().data, 'radius_axis': 4., 'radius_pipe': 1.}
        >>> torus = Torus.from_data(data)

        """
        torus = cls(Plane.worldXY(), 1, 1)
        torus.data = data
        return torus

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def plane(self):
        """Plane: The torus' plane."""
        return self._plane

    @plane.setter
    def plane(self, plane):
        self._plane = Plane(plane[0], plane[1])

    @property
    def radius_axis(self):
        """float: The radius of the axis."""
        return self._radius_axis

    @radius_axis.setter
    def radius_axis(self, radius):
        self._radius_axis = float(radius)

    @property
    def radius_pipe(self):
        """float: The radius of the pipe."""
        return self._radius_pipe

    @radius_pipe.setter
    def radius_pipe(self, radius):
        self._radius_pipe = float(radius)

    @property
    def center(self):
        return self.plane.point

    @property
    def area(self):
        """Float: The surface area of the torus."""
        return (2 * pi * self.radius_pipe) * (2 * pi * self.radius_axis)

    @property
    def volume(self):
        """Float: The volume of the torus."""
        return (pi * self.radius_pipe**2) * (2 * pi * self.radius_axis)

    @property
    def data(self):
        """Returns the data dictionary that represents the torus.

        Returns
        -------
        dict
            The torus data.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Torus
        >>> torus = Torus(Plane.worldXY(), 5, 2)
        >>> sdict = {'plane': Plane.worldXY().data, 'radius_axis': 5., 'radius_pipe': 2.}
        >>> sdict == torus.data
        True

        """
        return {'plane': Plane.worldXY(),
                'radius_axis': self.radius_axis,
                'radius_pipe': self.radius_pipe}

    @data.setter
    def data(self, data):
        self.plane = Plane.from_data(data['plane'])
        self.radius_axis = data['radius_axis']
        self.radius_pipe = data['radius_pipe']

    def to_data(self):
        """Returns the data dictionary that represents the torus.

        Returns
        -------
        dict
            The torus data.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Torus
        >>> torus = Torus(Plane.worldXY(), 5, 2)
        >>> sdict = {'plane': Plane.worldXY().data, 'radius_axis': 5., 'radius_pipe': 2.}
        >>> sdict == torus.to_data()
        True

        """
        return self.data

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Torus({0}, {1}, {2})'.format(self.plane, self.radius_axis, self.radius_pipe)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.radius_axis
        elif key == 2:
            return self.radius_pipe
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.radius_axis = value
        elif key == 2:
            self.radius_pipe = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.radius_axis, self.radius_pipe])

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Makes a copy of this ``Torus``.

        Returns
        -------
        Torus
            The copy.

        Examples
        --------
        >>> from compas.geometry import Torus
        >>> torus = Torus(Plane.worldXY(), 5, 2)
        >>> torus_copy = torus.copy()

        """
        cls = type(self)
        return cls(self.plane.copy(), self.radius_axis, self.radius_pipe)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the torus.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Torus.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Torus
        >>> torus = Torus(Plane.worldXY(), 5, 2)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> torus.transform(T)

        """
        self.plane.transform(transformation)

    def transformed(self, transformation):
        """Returns a transformed copy of the current torus.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Torus.

        Returns
        -------
        :class:`Torus`
            The transformed torus.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Torus
        >>> torus = Torus(Plane.worldXY(), 5, 2)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> torus_transformed = torus.transformed(T)

        """
        torus = self.copy()
        torus.transform(transformation)
        return torus


if __name__ == '__main__':
    from compas.geometry import Frame
    from compas.geometry import Plane
    from compas.geometry import Transformation

    torus = Torus(Plane.worldXY(), 5, 2)
    frame = Frame([5, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(frame)
    torus.transform(T)
    print(torus)

    torus = Torus(Plane.worldXY(), 5, 2)
    print(torus.data)
    print(torus)
    torus = Torus.from_data(torus.data)
    print(torus)

    import doctest
    doctest.testmod()
