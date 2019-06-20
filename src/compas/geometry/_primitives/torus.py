from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Plane

__all__ = ['Torus']


class Torus(object):
    """A torus is defined by a plane and two radii.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane of the torus.
    radius1: float
        The radius of the axis.
    radius2: float
        The radius of the pipe.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Torus
    >>> torus = Torus(Plane.worldXY(), 5., 2.)

    """

    __slots__ = ['_plane', '_radius1', '_radius2']

    def __init__(self, plane, radius1, radius2):
        self._plane = None
        self._radius1 = None
        self._radius2 = None
        self.plane = plane
        self.radius1 = radius1
        self.radius2 = radius2

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
        >>> data = {'plane': Plane.worldXY().data, 'radius1': 4., 'radius2': 1.}
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
    def radius1(self):
        """float: The radius of the axis."""
        return self._radius1

    @radius1.setter
    def radius1(self, radius):
        self._radius1 = float(radius)
    
    @property
    def radius2(self):
        """float: The radius of the pipe."""
        return self._radius2

    @radius2.setter
    def radius2(self, radius):
        self._radius2 = float(radius)

    @property
    def center(self):
        return self.plane

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
        >>> sdict = {'plane': Plane.worldXY().data, 'radius1': 5., 'radius2': 2.}
        >>> sdict == torus.data
        True

        """
        return {'plane': Plane.worldXY(),
                'radius1': self.radius1,
                'radius2': self.radius2}

    @data.setter
    def data(self, data):
        self.plane = data['plane']
        self.radius1 = data['radius1']
        self.radius2 = data['radius2']

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
        >>> sdict = {'plane': Plane.worldXY().data, 'radius1': 5., 'radius2': 2.}
        >>> sdict == torus.to_data()
        True

        """
        return self.data

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Torus({0}, {1}, {2})'.format(self.plane, self.radius1, self.radius2)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.radius1
        elif key == 2:
            return self.radius2
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.radius1 = value
        elif key == 2:
            self.radius2 = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.radius1, self.radius2])

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
        return cls(self.plane.copy(), self.radius1, self.radius2)

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
