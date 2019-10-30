from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import matrix_from_frame
from compas.geometry import transform_points
from compas.geometry.primitives import Circle
from compas.geometry.primitives import Line
from compas.geometry.primitives.shapes import Sphere
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
        # add check if segment is
        # ((x,y,z),(x,y,z)) or
        # [[x,y,z],[x,y,z]] or
        # [point,point] or ...
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

    def to_vertices_and_faces(self, **kwargs):
        """Returns a list of vertices and faces"""

        u = kwargs.get('u') or 10
        if u < 3:
            raise ValueError('The value for u should be u > 3.')

        vertices = []
        faces = []
        a = 2 * pi / u

        # lateral surface
        halfheight = self.length/2
        for i in range(u):
            x = self.radius * cos(i * a)
            y = self.radius * sin(i * a)
            vertices.append([x, y, halfheight])
            vertices.append([x, y, -halfheight])

        for i in range(0, u * 2, 2):
            faces.append([i, i + 1, (i + 3) % (u * 2), (i + 2) % (u * 2)])

        # cap surfaces (hemi spheres)
        # TODO

        return vertices, faces

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

    def transform(self, matrix):
        """Transform this ``Capsule`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.
        """
        self.line.transform(matrix)
    
    def transformed(self, matrix):
        """Return a transformed copy of this ``Capsule`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        Returns
        -------
        Capsule
            The transformed copy.
        """
        capsule = self.copy()
        capsule.line.transform(matrix)
        return capsule


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
