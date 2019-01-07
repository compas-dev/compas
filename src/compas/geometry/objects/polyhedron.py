from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt


__all__ = ['Polyhedron']


class Polyhedron(object):
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

    def __init__(self):
        self.vertices = None
        self.faces = None

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    # ==========================================================================
    # representation
    # ==========================================================================

    # ==========================================================================
    # access
    # ==========================================================================

    # ==========================================================================
    # comparison
    # ==========================================================================

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    # ==========================================================================
    # transformations
    # ==========================================================================


    @classmethod
    def generate(cls, fcount):
        if fcount == 4:
            return Tetrahedron()
        if fcount == 6:
            return Hexahedron()
        if fcount == 8:
            return Octahedron()
        if fcount == 12:
            return Dodecahedron()
        if fcount == 20:
            return Icosahedron()
        raise Exception


#     1
#   / | \
#  /  |  \
# 0 ----- 2
#  \  |  /
#   \ | /
#     3
#
# (+/-1, 0, -0.5**0.5)
# (0, +/-1, +0.5**0.5)
#
# 13 = 2 * sqrt(2)
# r = sqrt((0.5 * 13)**2 + (1/sqrt(2))**2)
class Tetrahedron(Polyhedron):
    """
    V = 4
    F = 4
    E = 6
    """
    def __init__(self):
        super(Tetrahedron, self).__init__()
        self.compute()

    def compute(self):
        """"""
        self.faces = [[0, 1, 2],
                      [0, 3, 1],
                      [0, 2, 3],
                      [1, 3, 2]]
        self.vertices = []
        l = 2.
        r = l * sqrt(6) / 4.
        c = 1. / r
        for i in -1., +1.:
            i *= c
            self.vertices.append([i, 0., -c / sqrt(2)])
            self.vertices.append([0., i, +c / sqrt(2)])


class Hexahedron(Polyhedron):
    """
    V = 8
    F = 6
    E = 12
    """
    def __init__(self):
        super(Hexahedron, self).__init__()
        self.compute()

    #   5------4
    # 6------7 |
    # | |    | |
    # | 3    | 2
    # 0------1
    #
    # (+-1, +-1, +-1)
    #
    # 04 = 2 * sqrt(3)
    def compute(self):
        """"""
        self.faces = [[0, 3, 2, 1],
                      [0, 1, 7, 6],
                      [0, 6, 5, 3],
                      [4, 2, 3, 5],
                      [4, 7, 1, 2],
                      [4, 5, 6, 7]]
        self.vertices = []
        l = 1.
        r = l * sqrt(3) / 2.
        c = 1. / r
        for i in -1., +1.:
            i *= c
            self.vertices.append([+i, +i, +i])
            self.vertices.append([-i, +i, +i])
            self.vertices.append([-i, -i, +i])
            self.vertices.append([+i, -i, +i])


class Octahedron(Polyhedron):
    """
    V = 6
    F = 8
    E = 12
    """
    def __init__(self):
        super(Octahedron, self).__init__()
        self.compute()

    #      5
    #      |
    #   4--|---3
    # 0----------1
    #      |
    #      2
    #
    #      4
    #    /   \
    #   /     \
    #  0  5/2  3
    #   \     /
    #    \   /
    #      1
    def compute(self):
        """"""
        self.faces = [[0, 1, 5],
                      [1, 3, 5],
                      [3, 4, 5],
                      [0, 5, 4],
                      [0, 2, 1],
                      [1, 2, 3],
                      [3, 2, 4],
                      [0, 4, 2]]
        self.vertices = []
        l = sqrt(2)
        r = l * sqrt(2) / 2.
        c = 1. / r
        for i in -1., +1.:
            i *= c
            self.vertices.append([i, 0., 0.])
            self.vertices.append([0., i, 0.])
            self.vertices.append([0., 0., i])


class Dodecahedron(Polyhedron):
    """
    V = 20
    F = 12
    E = 30
    """
    def __init__(self):
        super(Dodecahedron, self).__init__()
        self.compute()

    # (      0, +-1/phi,   +-phi)
    # (+-1/phi,   +-phi,       0)
    # (  +-phi,       0, +-1/phi)
    # (    +-1,     +-1,     +-1)
    def compute(self):
        """"""
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
        l = 2. / phi
        r = l * phi * sqrt(3) / 2.
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
        self.vertices = vertices
        self.faces = faces


class Icosahedron(Polyhedron):
    """
    V = 12
    F = 20
    E = 30
    """
    def __init__(self):
        super(Icosahedron, self).__init__()
        self.compute()

    # (    0,   +-1, +-phi)
    # (  +-1, +-phi,     0)
    # (+-phi,     0,   +-1)
    def compute(self):
        """"""
        phi = (1 + sqrt(5)) / 2.
        vertices = []
        faces = []
        l = 2.
        r = l * sqrt(phi * sqrt(5)) / 2.
        c = 1. / r
        for i in -1., +1.:
            i *= c
            for j in -1., +1.:
                j *= c
                vertices.append([     0.,       i, j * phi])
                vertices.append([      i, j * phi,      0.])
                vertices.append([j * phi,      0.,       i])
        self.vertices = vertices
        self.faces = faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
