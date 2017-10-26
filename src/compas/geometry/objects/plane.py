from compas.geometry.objects import Point
from compas.geometry.objects import Vector

from compas.geometry import orthonormalise_vectors


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Plane']


class Plane(object):
    """"""

    def __init__(self):
        self.point = None
        self.normal = None

    # ==========================================================================
    # factory
    # ==========================================================================

    @classmethod
    def from_point_and_normal(cls, point, normal):
        plane = cls()
        plane.point = Point(*point)
        plane.normal = Vector(*normal)
        plane.normal.unitize()
        return plane

    @classmethod
    def from_three_points(cls, p1, p2, p3):
        p1 = Point(*p1)
        p2 = Point(*p2)
        p3 = Point(*p3)
        v1 = p2 - p1
        v2 = p3 - p1
        plane = cls()
        plane.point  = p1
        plane.normal = Vector.cross(v1, v2)
        plane.normal.unitize()
        return plane

    @classmethod
    def from_point_and_two_vectors(cls, point, v1, v2):
        v1 = Vector(*v1)
        v2 = Vector(*v2)
        n  = Vector.cross(v1, v2)
        n.unitize()
        plane = cls()
        plane.point = Point(*point)
        plane.normal = n
        return plane

    @classmethod
    def from_points(cls, points):
        pass

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def d(self):
        a, b, c = self.normal
        x, y, z = self.point
        return - a * x - b * y - c * z

    @property
    def basis(self):
        a, b, c = self.normal
        u = 1.0, 0.0, - a / c
        v = 0.0, 1.0, - b / c
        return [Vector(*vector, unitize=True) for vector in orthonormalise_vectors([u, v])]

    # ==========================================================================
    # representation
    # ==========================================================================

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if i == 0:
            return self.point
        if i == 1:
            return self.normal
        raise KeyError

    def __setitem__(self, key, value):
        if i == 0:
            self.point = value
            return
        if i == 1:
            self.normal = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.point, self.normal])

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



# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from compas.visualization.viewers import Viewer
    from compas.visualization.viewers import xdraw_points
    from compas.visualization.viewers import xdraw_lines

    base = Point(1.0, 0.0, 0.0)
    normal = Vector(1.0, 1.0, 1.0)

    plane = Plane.from_point_and_normal(base, normal)

    points = [{
        'pos'  : base,
        'color': (1.0, 0.0, 0.0),
        'size' : 10.0
    }]

    lines = []
    for vector in plane.basis + [plane.normal]:
        lines.append({
            'start' : base,
            'end'   : base + vector,
            'color' : (0.0, 0.0, 0.0),
            'width' : 3.0
        })

    def draw_plane():
        xdraw_points(points)
        xdraw_lines(lines)

    Viewer(
        displayfuncs=[draw_plane, ],
        delay_setup=False
    ).show()
