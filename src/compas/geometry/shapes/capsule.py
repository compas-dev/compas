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
from compas.geometry import Line

from ._shape import Shape


class Capsule(Shape):
    """A capsule is defined by a line segment and a radius.

    Parameters
    ----------
    line : [point, point] | :class:`~compas.geometry.Line`
        The axis line of the capsule.
    radius : float
        The radius of the capsule.

    Attributes
    ----------
    line : :class:`~compas.geometry.Line`
        The centre line of the capsule.
    radius : float
        The radius of the capsule.
    start : :class:`~compas.geometry.Point`, read-only
        The start point of the centre line.
    end : :class:`~compas.geometry.Point`, read-only
        The end point of the centre line.
    length : float, read-only
        The length of the centre line of the capsule.
    volume : float, read-only
        The volume of the capsule.
    area : float, read-only
        The area of the capsule surface.

    Examples
    --------
    >>> line = Line((1, 2, 3), (5, 3, 1))
    >>> capsule = Capsule(line, 2.3)

    """

    __slots__ = ["_line", "_radius"]

    def __init__(self, line, radius, **kwargs):
        super(Capsule, self).__init__(**kwargs)
        self._line = None
        self._radius = None
        self.line = line
        self.radius = radius

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema

        return schema.Schema(
            {
                "line": Line.DATASCHEMA.fget(None),
                "radius": schema.And(float, lambda x: x > 0),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "capsule"

    @property
    def data(self):
        """dict : Returns the data dictionary that represents the capsule."""
        return {"line": self.line.data, "radius": self.radius}

    @data.setter
    def data(self, data):
        self.line = Line.from_data(data["line"])
        self.radius = data["radius"]

    @classmethod
    def from_data(cls, data):
        """Construct a capsule from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Capsule`
            The constructed capsule.

        """
        capsule = Capsule(Line.from_data(data["line"]), data["radius"])
        return capsule

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = Line(*line)

    @property
    def start(self):
        return self.line.start

    @property
    def end(self):
        return self.line.end

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(abs(radius))

    @property
    def length(self):
        return self.line.length

    @property
    def volume(self):
        # cylinder plus 2 half spheres
        cylinder = self.radius**2 * pi * self.length
        caps = 4.0 / 3.0 * pi * self.radius**3
        return cylinder + caps

    @property
    def area(self):
        # cylinder minus caps plus 2 half spheres
        cylinder = self.radius * 2 * pi * self.length
        caps = 4 * pi * self.radius**2
        return cylinder + caps

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "Capsule({0!r}, {1!r})".format(self.line, self.radius)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.line
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.line = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.line, self.radius])

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, v=16, triangulated=False):
        """Returns a list of vertices and faces.

        Parameters
        ----------
        u : int, optional
            Number of faces in the 'u' direction.
        v : int, optional
            Number of faces in the 'v' direction.
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
        if v % 2 == 1:
            v += 1

        theta = pi / v
        phi = pi * 2 / u
        hpi = pi * 0.5
        halfheight = self.line.length / 2
        sidemult = -1
        capswitch = 0

        vertices = []
        for i in range(1, v + 1):
            for j in range(u):
                a = i + capswitch
                tx = self.radius * cos(a * theta - hpi) * cos(j * phi)
                ty = self.radius * cos(a * theta - hpi) * sin(j * phi)
                tz = self.radius * sin(a * theta - hpi) + sidemult * halfheight
                vertices.append([tx, ty, tz])
            # switch from lower pole cap to upper pole cap
            if i == v / 2 and sidemult == -1:
                capswitch = -1
                sidemult *= -1

        vertices.append([0, 0, halfheight + self.radius])
        vertices.append([0, 0, -halfheight - self.radius])

        # move points to correct location in space
        plane = Plane(self.line.midpoint, self.line.direction)
        frame = Frame.from_plane(plane)
        M = matrix_from_frame(frame)
        vertices = transform_points(vertices, M)

        faces = []

        # south pole triangle fan
        sp = len(vertices) - 1
        for j in range(u):
            faces.append([sp, (j + 1) % u, j])

        for i in range(v - 1):
            for j in range(u):
                jj = (j + 1) % u
                a = i * u + j
                b = i * u + jj
                c = (i + 1) * u + jj
                d = (i + 1) * u + j
                faces.append([a, b, c, d])

        # north pole triangle fan
        np = len(vertices) - 2
        for j in range(u):
            nc = len(vertices) - 3 - j
            nn = len(vertices) - 3 - (j + 1) % u
            faces.append([np, nn, nc])

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
        """Transform this `Capsule` using a given transformation.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the capsule.

        Returns
        -------
        None

        """
        self.line.transform(transformation)
