from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import matrix_from_frame
from compas.geometry import transform_points
from compas.geometry import Frame
from compas.geometry import Plane

from compas.geometry.shapes import Shape

__all__ = ['Torus']


class Torus(Shape):
    """A torus is defined by a plane and two radii.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane` or tuple of point and normal
        The plane of the torus.
    radius_axis: float
        The radius of the axis.
    radius_pipe: float
        The radius of the pipe.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane of the torus.
    radius_axis: float
        The radius of the axis.
    radius_pipe: float
        The radius of the pipe.
    center (read-only): :class:`compas.geometry.Point`
        The center of the torus.
    area (read-only): float
        The surface area of the torus.
    volume (read-only): float
        The volume of the torus.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Torus
    >>> torus = Torus(Plane.worldXY(), 5., 2.)

    """

    __slots__ = ['_plane', '_radius_axis', '_radius_pipe']

    def __init__(self, plane, radius_axis, radius_pipe):
        super(Torus, self).__init__()
        self._plane = None
        self._radius_axis = None
        self._radius_pipe = None
        self.plane = plane
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

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
        return {'plane': Plane.worldXY().to_data(),
                'radius_axis': self.radius_axis,
                'radius_pipe': self.radius_pipe}

    @data.setter
    def data(self, data):
        self.plane = Plane.from_data(data['plane'])
        self.radius_axis = data['radius_axis']
        self.radius_pipe = data['radius_pipe']

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

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return 'Torus({0}, {1}, {2})'.format(self.plane, self.radius_axis, self.radius_pipe)

    def __len__(self):
        return 3

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
    # constructors
    # ==========================================================================

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
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=10, v=10):
        """Returns a list of vertices and faces

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``10``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``10``.

        Returns
        -------
        (vertices, faces)
            A list of vertex locations and a list of faces,
            with each face defined as a list of indices into the list of vertices.
        """
        if u < 3:
            raise ValueError('The value for u should be u > 3.')
        if v < 3:
            raise ValueError('The value for v should be v > 3.')

        theta = pi*2 / u
        phi = pi*2 / v
        vertices = []
        for i in range(u):
            for j in range(v):
                x = cos(i * theta) * (self.radius_axis + self.radius_pipe * cos(j * phi))
                y = sin(i * theta) * (self.radius_axis + self.radius_pipe * cos(j * phi))
                z = self.radius_pipe * sin(j * phi)
                vertices.append([x, y, z])

        # transform vertices to torus' plane
        frame = Frame.from_plane(self.plane)
        M = matrix_from_frame(frame)
        vertices = transform_points(vertices, M)

        faces = []
        for i in range(u):
            ii = (i + 1) % u
            for j in range(v):
                jj = (j + 1) % v
                a = i * v + j
                b = ii * v + j
                c = ii * v + jj
                d = i * v + jj
                faces.append([a, b, c, d])
        return vertices, faces

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    # from compas.geometry import Transformation

    # torus = Torus(Plane.worldXY(), 5, 2)
    # frame = Frame([5, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    # T = Transformation.from_frame(frame)
    # torus.transform(T)
    # print(torus)

    # torus = Torus(Plane.worldXY(), 5, 2)
    # print(torus.data)
    # print(torus)
    # torus = Torus.from_data(torus.data)
    # print(torus)

    import doctest
    doctest.testmod()
