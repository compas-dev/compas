from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos
from math import sin
from math import pi

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLE import *
from OpenGL.GL import *

from compas.geometry import normalize_vector
from compas.geometry import cross_vectors

from compas.geometry import global_coords_numpy


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', 'Shajay Bhooshan']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'draw_points',
    'draw_lines',
    'draw_faces',
    'draw_sphere',
    'xdraw_points',
    'xdraw_lines',
    'xdraw_polygons',
    'xdraw_cylinders',
    'xdraw_spheres',
]


# ==============================================================================
# draw
# ==============================================================================


def draw_points(points, color=None, size=1):
    color = color if color else (0.0, 0.0, 0.0)
    glColor3f(*color)
    glPointSize(size)
    glBegin(GL_POINTS)
    for x, y, z in iter(points):
        glVertex3f(x, y, z)
    glEnd()


def draw_lines(lines, color=None, linewidth=1):
    color = color if color else (0.0, 0.0, 0.0)
    glColor3f(*color)
    glLineWidth(linewidth)
    glBegin(GL_LINES)
    for a, b in iter(lines):
        glVertex3f(*a)
        glVertex3f(*b)
    glEnd()


def draw_faces(faces, color=None):
    color = color if color else (1.0, 0.0, 0.0, 0.5)
    glColor4f(*color)
    for face in faces:
        glBegin(GL_POLYGON)
        for xyz in face:
            glVertex3f(*xyz)
        glEnd()


def draw_sphere(r=1.0):
    slices = 17
    stacks = 17
    glColor4f(0.8, 0.8, 0.8, 0.5)
    glLineWidth(0.1)
    glutWireSphere(r, slices, stacks)


def draw_circle(circle, color=None, n=100):
    (center, normal), radius = circle
    cx, cy, cz = center
    a, b, c = normal

    u = -1.0, 0.0, a
    v = 0.0, -1.0, b
    w = cross_vectors(u, v)

    uvw = [normalize_vector(u), normalize_vector(v), normalize_vector(w)]

    color = color if color else (1.0, 0.0, 0.0, 0.5)
    sector = 2 * pi  / n

    glColor4f(*color)

    glBegin(GL_POLYGON)
    for i in range(n):
        a = i * sector
        x = radius * cos(a)
        y = radius * sin(a)
        z = 0
        x, y, z = global_coords_numpy(center, uvw, [[x, y, z]]).tolist()[0]
        glVertex3f(x, y, z)
    glEnd()

    glBegin(GL_POLYGON)
    for i in range(n):
        a = -i * sector
        x = radius * cos(a)
        y = radius * sin(a)
        z = 0
        x, y, z = global_coords_numpy(center, uvw, [[x, y, z]]).tolist()[0]
        glVertex3f(x, y, z)
    glEnd()


# ==============================================================================
# xdraw
# ==============================================================================


def xdraw_points(points):
    for attr in points:
        pos   = attr['pos']
        color = attr['color']
        size  = attr['size']
        glColor3f(*color)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex3f(*pos)
        glEnd()
        pass


def xdraw_lines(lines):
    for attr in lines:
        start = attr['start']
        end   = attr['end']
        color = attr['color']
        width = attr['width']
        glColor3f(*color)
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex3f(*start)
        glVertex3f(*end)
        glEnd()


def xdraw_polygons(polygons):
    for attr in polygons:
        points      = attr['points']
        color_front = attr['color.front']
        color_back  = attr['color.back']
        # front faces
        glColor4f(*color_front)
        glBegin(GL_POLYGON)
        for xyz in points:
            glVertex3f(*xyz)
        glEnd()
        # back faces
        glColor4f(*color_back)
        glBegin(GL_POLYGON)
        for xyz in points[::-1]:
            glVertex3f(*xyz)
        glEnd()


def xdraw_texts(texts):
    for attr in texts:
        text  = attr['text']
        pos   = attr['pos']
        color = attr['color']
        shift = attr['shift']
        glColor4f(color[0], color[1], color[2], color[3])
        glRasterPos3f(pos[0] + shift[0], pos[1] + shift[1], pos[2] + shift[2])
        font = GLUT_BITMAP_HELVETICA_12
        for char in text:
            glutBitmapCharacter(font, ord(char))


def xdraw_spheres(spheres):
    for attr in spheres:
        glPushMatrix()
        glTranslatef(* attr['pos'])
        glColor3f(* attr['color'])
        glutSolidSphere(attr['size'], 24, 24)
        glPopMatrix()


def xdraw_cylinders(cylinders):
    for attr in cylinders:
        points = [attr['start'], attr['start'], attr['end'], attr['end']]
        colors = [attr['color'], attr['color'], attr['color'], attr['color']]
        glePolyCylinder(points, colors, attr['width'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
