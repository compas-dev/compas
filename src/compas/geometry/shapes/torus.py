from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import transform_points

from .shape import Shape


class Torus(Shape):
    """A torus is defined by a plane and two radii.

    Parameters
    ----------
    radius_axis: float, optional
        The radius of the axis.
    radius_pipe: float, optional
        The radius of the pipe.
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the torus.
        Default is ``None``, in which case the torus is constructed in the world XY plane.
    name : str, optional
        The name of the shape.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate system of the torus.
    transformation : :class:`compas.geometry.Transformation`
        The transformation of the sphere to global coordinates.
    radius_axis : float
        The radius of the axis.
    radius_pipe : float
        The radius of the pipe.
    axis : :class:`compas.geometry.Line`, read-only
        The central axis of the torus.
    base : :class:`compas.geometry.Point`, read-only
        The base point of the torus.
        The base point is at the origin of the local coordinate system.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the torus.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    circle : :class:`compas.geometry.Circle`, read-only
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

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "radius_axis": {"type": "number", "minimum": 0},
            "radius_pipe": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["radius_axis", "radius_pipe", "frame"],
    }

    @property
    def __data__(self):
        return {
            "radius_axis": self.radius_axis,
            "radius_pipe": self.radius_pipe,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius_axis=data["radius_axis"],
            radius_pipe=data["radius_pipe"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius_axis, radius_pipe, frame=None, name=None):
        super(Torus, self).__init__(frame=frame, name=name)
        self._radius_axis = None
        self._radius_pipe = None
        self.radius_axis = radius_axis
        self.radius_pipe = radius_pipe

    def __repr__(self):
        return "Torus(frame={0!r}, radius_axis={1!r}, radius_pipe={2!r})".format(
            self.frame,
            self.radius_axis,
            self.radius_pipe,
        )

    # ==========================================================================
    # Properties
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
    # Constructors
    # ==========================================================================

    @classmethod
    def from_plane_and_radii(cls, plane, radius_axis, radius_pipe):
        """Construct a torus from a plane and two radii.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane of the torus.
        radius_axis: float
            The radius of the axis.
        radius_pipe: float
            The radius of the pipe.

        Returns
        -------
        :class:`compas.geometry.Torus`
            The constructed torus.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Torus
        >>> plane = Plane.worldXY()
        >>> torus = Torus.from_plane_and_radii(plane, 5.0, 2.0)

        """
        frame = Frame.from_plane(plane)
        return cls(radius_axis=radius_axis, radius_pipe=radius_pipe, frame=frame)

    # ==========================================================================
    # Discretisation
    # ==========================================================================

    def compute_vertices(self):  # type: () -> list[float]
        """Compute the vertices of the discrete representation of the sphere.

        Returns
        -------
        list[list[float]]

        """
        u = self.resolution_u
        v = self.resolution_v

        theta = pi * 2 / u
        phi = pi * 2 / v

        vertices = []
        for i in range(u):
            for j in range(v):
                x = cos(i * theta) * (self.radius_axis + self.radius_pipe * cos(j * phi))
                y = sin(i * theta) * (self.radius_axis + self.radius_pipe * cos(j * phi))
                z = self.radius_pipe * sin(j * phi)
                vertices.append([x, y, z])

        vertices = transform_points(vertices, self.transformation)
        return vertices

    def compute_faces(self):  # type: () -> list[list[int]]
        """Compute the faces of the discrete representation of the sphere.

        Returns
        -------
        list[list[int]]

        """
        u = self.resolution_u
        v = self.resolution_v

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

        return faces

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_brep(self):
        """Returns a BRep representation of the torus.

        Returns
        -------
        :class:`compas.brep.Brep`

        """
        from compas.geometry import Brep

        return Brep.from_torus(self)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the torus.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation used to transform the Torus.

        Returns
        -------
        None

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Torus
        >>> torus = Torus(5, 2)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> torus.transform(T)

        """
        self.frame.transform(transformation)
