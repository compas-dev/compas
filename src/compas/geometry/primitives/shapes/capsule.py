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
from compas.geometry.primitives import Line
from compas.geometry.primitives.shapes import Shape

__all__ = ['Capsule']


class Capsule(Shape):
    """A capsule is defined by a line segment and a radius.

    Attributes
    ----------
    segment: :class:`compas.geometry.Line`
        The axis line of the capsule.
    radius: float
        The radius of the capsule.

    Examples
    --------
    >>> TODO

    """

    __slots__ = ['_segment', '_radius']

    def __init__(self, line, radius):
        self._line = None
        self._radius = None
        self.line = line
        self.radius = radius

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

    @property
    def start(self):
        return self.line.start

    @property
    def end(self):
        return self.line.end

    @property
    def radius(self):
        """float: The radius of the capsule."""
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(abs(radius))

    @property
    def length(self):
        self.line.length

    @property
    def volume(self):
        # cylinder plus 2 half spheres
        cylinder = self.radius**2 * pi * self.length
        caps = 4./3. * pi * self.radius**3
        return cylinder + caps

    @property
    def area(self):
        # cylinder minus caps plus 2 half spheres
        cylinder = self.radius*2 * pi * self.length
        caps = 4 * pi * self.radius**2
        return cylinder + caps

    @property
    def data(self):
        """Returns the data dictionary that represents the capsule.

        Returns
        -------
        dict
            The capsule data.

        """
        return {'line': self.line.data,
                'radius': self.radius}

    @data.setter
    def data(self, data):
        self.line = Line.from_data(data['line'])
        self.radius = data['radius']

    def to_data(self):
        """Returns the data dictionary that represents the capsule.

        Returns
        -------
        dict
            The capsule data.

        """
        return self.data

    @classmethod
    def from_data(cls, data):
        """Construct a capsule from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class: `Capsule`
            The constructed capsule.
        """
        line = Line.from_data(data['line'])
        capsule = Capsule(line, data['radius'])
        return capsule

    def to_vertices_and_faces(self, **kwargs):
        """Returns a list of vertices and faces"""

        u = kwargs.get('u') or 10
        v = kwargs.get('v') or 10
        if u < 3:
            raise ValueError('The value for u should be u > 3.')
        if v < 3:
            raise ValueError('The value for v should be v > 3.')
        if v % 2 == 1:
            v += 1

        theta = pi / v
        phi = pi*2 / u
        hpi = pi * 0.5
        halfheight = self.line.length/2
        sidemult = -1
        capswitch = 0

        vertices = []
        for i in range(1, v+1):
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
            faces.append([sp, (j+1) % u, j])

        for i in range(v-1):
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

        return vertices, faces

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Capsule({0}, {1})'.format(self.line, self.radius)

    def __len__(self):
        return 2

    # ==========================================================================
    # access
    # ==========================================================================

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
    # helpers
    # ==========================================================================

    def copy(self):
        """
        Make a copy of this ``Capsule``.

        Returns
        -------
        Capsule
            The copy.
        """
        cls = type(self)
        return cls(self.line.copy(), self.height)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform this ``Capsule`` using a given transformation.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the capsule.
        """
        self.line.transform(transformation)

    def transformed(self, transformation):
        """Return a transformed copy of the current ``Capsule``.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the capsule.

        Returns
        -------
        :class: `Capsule`
            The transformed copy of the current capsule.
        """
        capsule = self.copy()
        capsule.line.transform(transformation)
        return capsule


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas.geometry import Transformation

    capsule = Capsule(Line((1, 2, 3), (4, 5, 6)), 1.3)
    frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    print(frame.normal)
    T = Transformation.from_frame(frame)
    capsule.transform(T)
    print(capsule)

    print(Plane.worldXY().data)
    data = {'line': Line((1, 2, 3), (5, 4, 2)).data, 'radius': 1.2}
    capsule = Capsule.from_data(data)
    print(capsule)

    import doctest
    doctest.testmod()
