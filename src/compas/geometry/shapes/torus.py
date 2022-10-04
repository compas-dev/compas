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

from ._shape import Shape


class Torus(Shape):
    """A torus is defined by a plane and two radii.

    Parameters
    ----------
    plane : [point, normal] | :class:`~compas.geometry.Plane`
        The plane of the torus.
    radius_axis: float
        The radius of the axis.
    radius_pipe: float
        The radius of the pipe.

    Attributes
    ----------
    plane : :class:`~compas.geometry.Plane`
        The torus' plane.
    radius_axis : float
        The radius of the axis.
    radius_pipe : float
        The radius of the pipe.
    center : :class:`~compas.geometry.Point`, read-only
        The centre of the torus.
    area : float, read-only
        The surface area of the torus.
    volume : float, read-only
        The volume of the torus.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Torus
    >>> torus = Torus(Plane.worldXY(), 5., 2.)

    >>> from compas.geometry import Plane
    >>> from compas.geometry import Torus
    >>> torus = Torus(Plane.worldXY(), 5, 2)
    >>> sdict = {'plane': Plane.worldXY().data, 'radius_axis': 5., 'radius_pipe': 2.}
    >>> sdict == torus.data
    True

    """

    __slots__ = ["_plane", "_radius_axis", "_radius_pipe"]

    def __init__(self, plane, radius_axis, radius_pipe, **kwargs):
        super(Torus, self).__init__(**kwargs)
        self._plane = None
        self._radius_axis = None
        self._radius_pipe = None
        self.plane = plane
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema

        return schema.Schema(
            {
                "plane": Plane.DATASCHEMA.fget(None),
                "radius_axis": schema.And(float, lambda x: x > 0),
                "radius_pipe": schema.And(float, lambda x: x > 0),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "torus"

    @property
    def data(self):
        """dict : Returns the data dictionary that represents the torus."""
        return {
            "plane": self.plane.data,
            "radius_axis": self.radius_axis,
            "radius_pipe": self.radius_pipe,
        }

    @data.setter
    def data(self, data):
        self.plane = Plane.from_data(data["plane"])
        self.radius_axis = data["radius_axis"]
        self.radius_pipe = data["radius_pipe"]

    @classmethod
    def from_data(cls, data):
        """Construct a torus from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Torus`
            The constructed torus.

        Examples
        --------
        >>> from compas.geometry import Torus
        >>> data = {'plane': Plane.worldXY().data, 'radius_axis': 4., 'radius_pipe': 1.}
        >>> torus = Torus.from_data(data)

        """
        torus = cls(Plane.from_data(data["plane"]), data["radius_axis"], data["radius_pipe"])
        return torus

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def plane(self):
        return self._plane

    @plane.setter
    def plane(self, plane):
        self._plane = Plane(*plane)

    @property
    def radius_axis(self):
        return self._radius_axis

    @radius_axis.setter
    def radius_axis(self, radius):
        self._radius_axis = float(radius)

    @property
    def radius_pipe(self):
        return self._radius_pipe

    @radius_pipe.setter
    def radius_pipe(self, radius):
        self._radius_pipe = float(radius)

    @property
    def center(self):
        return self.plane.point

    @property
    def area(self):
        return (2 * pi * self.radius_pipe) * (2 * pi * self.radius_axis)

    @property
    def volume(self):
        return (pi * self.radius_pipe**2) * (2 * pi * self.radius_axis)

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "Torus({0!r}, {1!r}, {2!r})".format(self.plane, self.radius_axis, self.radius_pipe)

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

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, v=16, triangulated=False):
        """Returns a list of vertices and faces

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.
        triangulated: bool, optional
            If True, triangulate the faces.

        Returns
        -------
        list[list[float]]
            A list of vertex locations.
        list[list[int]]
            And a list of faces,
            with each face defined as a list of indices into the list of vertices.

        """
        if u < 3:
            raise ValueError("The value for u should be u > 3.")
        if v < 3:
            raise ValueError("The value for v should be v > 3.")

        theta = pi * 2 / u
        phi = pi * 2 / v
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

        if triangulated:
            triangles = []
            for face in faces:
                if len(face) == 4:
                    triangles.append(face[0:3])
                    triangles.append([face[0], face[2], face[3]])
                else:
                    triangles.append(face)
            faces = triangles

        return vertices, faces

    def transform(self, transformation):
        """Transform the torus.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the Torus.

        Returns
        -------
        None

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
