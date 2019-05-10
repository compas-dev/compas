from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt


__author__     = ['Mark Kilgard (?)']
__link__       = 'http://svn.red-bean.com/pyobjc/other/PyOpenGL-2.0.2.01/OpenGL/trackball.py'
__see__        = ['https://github.com/markkilgard/glut/blob/master/progs/examples/trackball.c']
__doc__        = """A module which implements a trackball class."""


class Trackball(object):
    """A trackball object.  This is deformed trackball which is a hyperbolic
       sheet of rotation away from the center. This particular function was chosen
       after trying out several variations.  The current transformation matrix
       can be retrieved using the "matrix" attribute."""

    def __init__(self, size=0.8, scale=2.0, renorm=97):
        """Create a Trackball object.  "size" is the radius of the inner trackball
           sphere.  "scale" is a multiplier applied to the mouse coordinates before
           mapping into the viewport.  "renorm" is not currently used."""

        self.size = size
        self.scale = scale
        self.renorm = renorm
        self.quat = 1, 0, 0, 0

    def __project_to_sphere(self, px, py):
        """Return projection of px,py on deformed sphere.

        If point x,y is inside the circle where the actual spere and the
        hyperbolic sheet intersect, return the projection onto the sphere:

            z = sqrt(r**2 - (x**2 + y**2)).

        The equation of the circle is:

            x**2 + y**2 = (r * 0.5 * sqrt(2))**2

        If the point is outside the circle, return the projection onto the
        hyperbolic sheet:

            z = (r / sqrt(2))**2 / sqrt(x**2 + y**2)
        """
        d2 = px**2 + py**2
        d  = sqrt(d2)
        if d < self.size * 0.70710678118654752440:
            return sqrt(self.size**2 - d2)
        t = self.size / 1.41421356237309504880
        return t**2 / d

    def update(self, x1, y1, x2, y2, width, height, mat=0):
        """Update the quaterion with a new rotation position derived
        from the first point (x1, y1) and the second point (x2, y2).

        The the mat parameter is not currently used.
        """
        if x1 == x2 and y1 == y2:
            self.quat = 1, 0, 0, 0
        else:
            # unitize x1, y1
            x1_u = self.scale * x1 / width - 1.0
            y1_u = 1.0 - self.scale * y1 / height
            # unitize x2, y2
            x2_u = self.scale * x2 / width - 1.0
            y2_u = 1.0 - self.scale * y2 / height
            # project p1 and p2 to deformed sphere
            P1 = (x1_u, y1_u, self.__project_to_sphere(x1_u, y1_u))
            P2 = (x2_u, y2_u, self.__project_to_sphere(x2_u, y2_u))
            # rotation axis is cross product of P1 and P2
            a = [P2[1] * P1[2] - P2[2] * P1[1],
                 P2[2] * P1[0] - P2[0] * P1[2],
                 P2[0] * P1[1] - P2[1] * P1[0]]
            # rotation angle is ?
            d = P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2]
            t = sqrt(d[0]**2 + d[1]**2 + d[2]**2) / (2.0 * self.size)
            t = max(min(t, 1.0), -1.0)
            w = sqrt(1.0 - t**2)
            # scale vector for the rotation axis
            s = t * sqrt(a[0]**2 + a[1]**2 + a[2]**2)
            # the quaternion
            self.quat = a[0] * s, a[1] * s, a[2] * s, w

    # def __getattr__(self, name):
    #     if name != 'matrix':
    #         raise AttributeError('No attribute named "%s"' % name)
    #     return self.quat.matrix4


glTrackball = Trackball
