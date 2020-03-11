from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt

from compas.geometry._shapes import Shape

__all__ = ['Polyhedron']


class Polyhedron(Shape):
    """Compute the vertices and faces of one of the Platonic solids.

    Notes
    -----
    A Platonic solid is a regular, convex polyhedron. It is constructed by
    congruent regular polygonal faces with the same number of faces meeting
    at each vertex [1]_.

    References
    ----------
    .. [1] Wikipedia. *Platonic solids*.
           Available at: https://en.wikipedia.org/wiki/Platonic_solid.

    """

    __module__ = "compas.geometry"

    def __init__(self, fcount):
        self.vertices = None
        self.faces = None
        if fcount == 4:
            vertices, faces = tetrahedron()
        elif fcount == 6:
            vertices, faces = hexahedron()
        elif fcount == 8:
            vertices, faces = octahedron()
        elif fcount == 12:
            vertices, faces = dodecahedron()
        elif fcount == 20:
            vertices, faces = icosahedron()
        else:
            raise ValueError('Unsupported solid type. Supported face count values: 4, 6, 8, 12, 20')
        self.vertices = vertices
        self.faces = faces

    @classmethod
    def from_data(cls, data):
        """Construct a polyhedron from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Polyhedron
            The constructed polyhedron.

        Examples
        --------
        >>> from compas.geometry import Polyhedron
        >>> p = Polyhedron(4)
        >>> q = Polyhedron.from_data(p.data)
        """
        p = cls.generate(len(data.get('faces')))
        p.data = data
        return p

    def to_data(self):
        """Returns the data dictionary that represents the polyhedron.

        Returns
        -------
        dict
            The polyhedron data.
        """
        return self.data

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __iter__(self):
        return iter([self.vertices, self.faces])

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def data(self):
        """Returns the data dictionary that represents the polyhedron.

        Returns
        -------
        dict
            The polyhedron data.

        """
        return {'vertices': self.vertices, 'faces': self.faces}

    @data.setter
    def data(self, data):
        self.vertices = data['vertices']
        self.faces = data['faces']

    # ==========================================================================
    # Methods
    # ==========================================================================


# ==============================================================================
# Platonic solids
# ==============================================================================

def tetrahedron():
    faces = [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]
    vertices = []
    L = 2.0
    r = L * sqrt(6) / 4.0
    c = 1.0 / r
    for i in (-1, 1):
        i *= c
        vertices.append([i, 0.0, -c / sqrt(2)])
        vertices.append([0.0, i, +c / sqrt(2)])
    return vertices, faces


def hexahedron():
    faces = [[0, 3, 2, 1],
             [0, 1, 7, 6],
             [0, 6, 5, 3],
             [4, 2, 3, 5],
             [4, 7, 1, 2],
             [4, 5, 6, 7]]
    vertices = []
    L = 1.
    r = L * sqrt(3) / 2.
    c = 1. / r
    for i in -1., +1.:
        i *= c
        vertices.append([+i, +i, +i])
        vertices.append([-i, +i, +i])
        vertices.append([-i, -i, +i])
        vertices.append([+i, -i, +i])
    return vertices, faces


def octahedron():
    faces = [[0, 1, 5],
             [1, 3, 5],
             [3, 4, 5],
             [0, 5, 4],
             [0, 2, 1],
             [1, 2, 3],
             [3, 2, 4],
             [0, 4, 2]]
    vertices = []
    L = sqrt(2)
    r = L * sqrt(2) / 2.
    c = 1. / r
    for i in -1., +1.:
        i *= c
        vertices.append([i, 0., 0.])
        vertices.append([0., i, 0.])
        vertices.append([0., 0., i])
    return vertices, faces


def dodecahedron():
    phi = 0.5 * (1 + sqrt(5))
    vertices = []
    faces = [[0,  13,  11, 1,  3],
             [0,   3,  2,  8, 10],
             [0,  10, 18, 12, 13],
             [1,   4,  7,  2,  3],
             [1,  11, 14,  5,  4],
             [2,   7,  9,  6,  8],
             [5,  15,  9,  7,  4],
             [5,  14, 17, 19, 15],
             [6,  16, 18, 10,  8],
             [6,   9, 15, 19, 16],
             [12, 17, 14, 11, 13],
             [12, 18, 16, 19, 17]]
    L = 2. / phi
    r = L * phi * sqrt(3) / 2.
    c = 1. / r
    for i in -1, +1:
        i *= c
        for j in -1, +1:
            j *= c
            vertices.append([0, i / phi, j * phi])
            vertices.append([i / phi, j * phi, 0])
            vertices.append([i * phi, 0, j / phi])
            for k in -1, +1:
                k *= c
                vertices.append([i * 1., j * 1., k * 1.])
    return vertices, faces


def icosahedron():
    phi = (1 + sqrt(5)) / 2.
    vertices = [
        (-1, phi, 0),
        (1, phi, 0),
        (-1, -phi, 0),
        (1, -phi, 0),

        (0, -1, phi),
        (0, 1, phi),
        (0, -1, -phi),
        (0, 1, -phi),

        (phi, 0, -1),
        (phi, 0, 1),
        (-phi, 0, -1),
        (-phi, 0, 1),
    ]
    faces = [
        # 5 faces around point 0
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        # Adjacent faces
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        # 5 faces around 3
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        # Adjacent faces
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ]
    return vertices, faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
