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

from .shape import Shape


class Torus(Shape):
    """A torus is defined by a plane and two radii.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system of the torus.
        Default is ``None``, in which case the torus is constructed in the
    radius_axis: float, optional
        The radius of the axis.
    radius_pipe: float, optional
        The radius of the pipe.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The coordinate system of the torus.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation of the sphere to global coordinates.
    radius_axis : float
        The radius of the axis.
    radius_pipe : float
        The radius of the pipe.
    axis : :class:`~compas.geometry.Line`, read-only
        The central axis of the torus.
    base : :class:`~compas.geometry.Point`, read-only
        The base point of the torus.
        The base point is at the origin of the local coordinate system.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the torus.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    circle : :class:`~compas.geometry.Circle`, read-only
        The base circle of the torus.
        The center of the circle is at the origin of the local coordinate system.
    area : float, read-only
        The surface area of the torus.
    volume : float, read-only
        The volume of the torus.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Torus
    >>> torus = Torus(frame=Frame.worldXY(), radius_axis=5.0, radius_pipe=2.0)
    >>> torus = Torus(radius_axis=5.0, radius_pipe=2.0)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "radius_axis": {"type": "number", "minimum": 0},
            "radius_pipe": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "radius_axis", "radius_pipe"],
    }

    def __init__(self, frame=None, radius_axis=1.0, radius_pipe=0.3, **kwargs):
        super(Torus, self).__init__(frame=frame, **kwargs)
        self._radius_axis = None
        self._radius_pipe = None
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def data(self):
        return {
            "frame": self.frame,
            "radius_axis": self.radius_axis,
            "radius_pipe": self.radius_pipe,
        }

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
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
        >>> data = {"frame": Frame.worldXY(), "radius_axis": 1.0, "radius_pipe": 0.3}
        >>> torus = Torus.from_data(data)

        """
        return cls(**data)

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def radius_axis(self):
        if self._radius_axis is None:
            raise ValueError("The torus has no axis radius.")
        return self._radius_axis

    @radius_axis.setter
    def radius_axis(self, radius):
        if radius < 0:
            raise ValueError("The value for the axis radius should be radius >= 0.")
        self._radius_axis = float(radius)

    @property
    def radius_pipe(self):
        if self._radius_pipe is None:
            raise ValueError("The torus has no pipe radius.")
        return self._radius_pipe

    @radius_pipe.setter
    def radius_pipe(self, radius):
        if radius < 0:
            raise ValueError("The value for the pipe radius should be radius >= 0.")
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
        return "Torus(frame={0!r}, radius_axis={1!r}, radius_pipe={2!r})".format(
            self.frame, self.radius_axis, self.radius_pipe
        )

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.radius_axis
        elif key == 2:
            return self.radius_pipe
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.radius_axis = value
        elif key == 2:
            self.radius_pipe = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius_axis, self.radius_pipe])

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_plane_and_radii(cls, plane, radius_axis, radius_pipe):
        """Construct a torus from a plane and two radii.

        Parameters
        ----------
        plane : :class:`~compas.geometry.Plane`
            The plane of the torus.
        radius_axis: float
            The radius of the axis.
        radius_pipe: float
            The radius of the pipe.

        Returns
        -------
        :class:`~compas.geometry.Torus`
            The constructed torus.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Torus
        >>> plane = Plane.worldXY()
        >>> torus = Torus.from_plane_and_radii(plane, 5.0, 2.0)

        """
        return cls(plane=plane, radius_axis=radius_axis, radius_pipe=radius_pipe)

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, v=16, triangulated=False):
        """Returns a list of vertices and faces.

        The vertices are defined in global coordinates.

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
        list[list[float]], list[list[int]]
            A list of vertex locations, and a list of faces,
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

        vertices = transform_points(vertices, self.transformation)

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
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Torus
        >>> torus = Torus(Frame.worldXY(), 5, 2)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> torus.transform(T)

        """
        self.frame.transform(transformation)
