from compas.geometry import orthonormalise_vectors

from compas.geometry.objects.point import Point
from compas.geometry.objects.vector import Vector


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class Plane(object):
    """"""

    def __init__(self):
        self.point = None
        self.normal = None

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

    @property
    def d(self):
        a, b, c = self.normal
        x, y, z = self.point
        return - a * x - b * y - c * z

    def basis(self):
        a, b, c = self.normal
        u = 1.0, 0.0, - a / c
        v = 0.0, 1.0, - b / c
        return [Vector(*vector, unitize=True) for vector in orthonormalise_vectors([u, v])]


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

    basis = plane.basis()

    points = [{
        'pos'  : base,
        'color': (1.0, 0.0, 0.0),
        'size' : 10.0
    }]

    lines = []
    for vector in basis + [plane.normal]:
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
