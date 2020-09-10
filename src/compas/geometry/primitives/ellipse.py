from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from math import pi

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Plane


__all__ = ['Ellipse']


class Ellipse(Primitive):
    """A ellipse is defined by a plane and a major.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane` or tuple of point and normal
        The plane of the ellipse.
    major : float
        The major of the ellipse.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane of the ellipse.
    major : float
        The major.
    minor : float
        The minor.
    center : :class:`compas.geometry.Point`
        The base point of the plane and center of the ellipse.
    normal : :class:`compas.geometry.Vector`
        The normal vector of the plane.
    circumference : float, read-only
        The circumference of the ellipse.
    area : float, read-only
        The area of the ellipse.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Ellipse
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> ellipse = Ellipse(plane, 2, 1)
    """

    __slots__ = ['_plane', '_major', '_minor']

    def __init__(self, plane, major, minor):
        super(Ellipse, self).__init__()
        self._plane = None
        self._major = None
        self._minor = None
        self.plane = plane
        self.major = major
        self.minor = minor

    @property
    def data(self):
        """dict : The data dictionary that represents the ellipse."""
        return {'plane': [list(self.plane.point), list(self.plane.normal)], 'major': self.major, 'minor': self.minor}

    @data.setter
    def data(self, data):
        self.plane = data['plane']
        self.major = data['major']
        self.minor = data['minor']

    @property
    def plane(self):
        """:class:`compas.geometry.Plane` : The plane of the ellipse."""
        return self._plane

    @plane.setter
    def plane(self, plane):
        self._plane = Plane(plane[0], plane[1])

    @property
    def major(self):
        """float : The major of the ellipse."""
        return self._major

    @major.setter
    def major(self, major):
        self._major = float(major)

    @property
    def minor(self):
        """float : The minor of the ellipse."""
        return self._minor

    @minor.setter
    def minor(self, minor):
        self._minor = float(minor)

    @property
    def normal(self):
        """:class:`compas.geometry.Vector` : The normal of the ellipse."""
        return self.plane.normal

    @property
    def center(self):
        """:class:`compas.geometry.Point` : The center of the ellipse."""
        return self.plane.point

    @center.setter
    def center(self, point):
        self.plane.point = point

    @property
    def area(self):
        """float  : The area of the ellipse."""
        raise NotImplementedError

    @property
    def circumference(self):
        """float : The circumference of the ellipse."""
        raise NotImplementedError

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return 'Ellipse({0}, {1}, {2})'.format(self.plane, self.major, self.minor)

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.major
        elif key == 2:
            return self.minor
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.major = value
        elif key == 2:
            self.minor = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.major, self.minor])

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a ellipse from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Ellipse`
            The constructed ellipse.

        Examples
        --------
        >>> from compas.geometry import Ellipse
        >>> data = {'plane': [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], 'major': 2.0, 'minor': 1.0}
        >>> ellipse = Ellipse.from_data(data)
        """
        return cls(data['plane'], data['minor'], data['minor'])

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, T):
        """Transform the ellipse.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Ellipse
        >>> ellipse = Ellipse(Plane.worldXY(), 8, 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> ellipse.transform(T)
        """
        self.plane.transform(T)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
