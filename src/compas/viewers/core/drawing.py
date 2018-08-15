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
    'xdraw_texts',
]


# ==============================================================================
# arrays
# ------
# http://www.songho.ca/opengl/gl_vertexarray.html
# https://gist.github.com/ousttrue/c4ae334fc1505cdf4cd7
# ==============================================================================


def draw_arrays(vertices, arrays):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_colour_ARRAY)

    # vertex coordinates flattened
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    for primitive, indices, colours, flag_on in arrays:
        # primitive => GL_POINTS, GL_LINES, GL_TRIANGLES, GL_QUADS
        # colours => RGB colours flattened
        # indices => element vertex indices flattened
        # flag_on => True or False
        if not flag_on:
            continue

        glcolourPointer(3, GL_FLOAT, 0, colours)
        glDrawElements(primitive, len(indices), GL_UNSIGNED_INT, indices)

    glDisableClientState(GL_colour_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_triangle_array(vertices, indices, colours):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_colour_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glcolourPointer(3, GL_FLOAT, 0, colours)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
    glDisableClientState(GL_colour_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_line_array(vertices, indices, colours):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_colour_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glcolourPointer(3, GL_FLOAT, 0, colours)
    glDrawElements(GL_LINES, len(indices), GL_UNSIGNED_INT, indices)
    glDisableClientState(GL_colour_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


# ==============================================================================
# buffers
# -------
# http://www.songho.ca/opengl/gl_vbo.html
# https://gist.github.com/ousttrue/c4ae334fc1505cdf4cd7
# ==============================================================================


# ==============================================================================
# display lists
# -------------
# http://www.songho.ca/opengl/gl_displaylist.html
# ==============================================================================


# def _make_lists(self):
#     self._clear_lists()
#     key_xyz = {key: self.mesh.vertex_coordinates(key) for key in self.mesh.vertices()}
#     self._make_faces_list(key_xyz)
#     self._make_edges_list(key_xyz)
#     self._make_vertices_list(key_xyz)

# def _make_faces_list(self, key_xyz):
#     faces = []
#     front = hex_to_rgb(self.settings['faces.colour:front'])
#     front = list(front) + [1.0]
#     back  = hex_to_rgb(self.settings['faces.colour:back'])
#     back  = list(back) + [1.0]
#     for fkey in self.mesh.faces():
#         faces.append({'points'      : [key_xyz[key] for key in self.mesh.face_vertices(fkey)],
#                       'colour.front' : front,
#                       'colour.back'  : back})
#     self.view.faces = glGenLists(1)
#     glNewList(self.view.faces, GL_COMPILE)
#     xdraw_polygons(faces)
#     glEndList()

# def _make_edges_list(self, key_xyz):
#     lines = []
#     colour = hex_to_rgb(self.settings['edges.colour'])
#     width = self.settings['edges.width']
#     for u, v in self.mesh.edges():
#         lines.append({'start' : key_xyz[u],
#                       'end'   : key_xyz[v],
#                       'colour' : colour,
#                       'width' : width})
#     self.view.edges = glGenLists(1)
#     glNewList(self.view.edges, GL_COMPILE)
#     xdraw_cylinders(lines)
#     glEndList()

# def _make_vertices_list(self, key_xyz):
#     points = []
#     colour = hex_to_rgb(self.settings['vertices.colour'])
#     size = self.settings['vertices.size']
#     for key in self.mesh.vertices():
#         points.append({'pos'   : key_xyz[key],
#                        'colour' : colour,
#                        'size'  : size})
#     self.view.vertices = glGenLists(1)
#     glNewList(self.view.vertices, GL_COMPILE)
#     xdraw_spheres(points)
#     glEndList()


# ==============================================================================
# draw
# ==============================================================================


def draw_points(points, colour=None, size=1):
    colour = colour if colour else (0.0, 0.0, 0.0)
    glcolour3f(*colour)
    glPointSize(size)
    glBegin(GL_POINTS)
    for x, y, z in iter(points):
        glVertex3f(x, y, z)
    glEnd()


def draw_lines(lines, colour=None, linewidth=1):
    colour = colour if colour else (0.0, 0.0, 0.0)
    glcolour3f(*colour)
    glLineWidth(linewidth)
    glBegin(GL_LINES)
    for a, b in iter(lines):
        glVertex3f(*a)
        glVertex3f(*b)
    glEnd()


def draw_faces(faces, colour=None):
    colour = colour if colour else (1.0, 0.0, 0.0, 0.5)
    glcolour4f(*colour)
    for face in faces:
        glBegin(GL_POLYGON)
        for xyz in face:
            glVertex3f(*xyz)
        glEnd()


def draw_sphere(r=1.0):
    slices = 17
    stacks = 17
    glcolour4f(0.8, 0.8, 0.8, 0.5)
    glLineWidth(0.1)
    glutWireSphere(r, slices, stacks)


def draw_circle(circle, colour=None, n=100):
    (center, normal), radius = circle
    cx, cy, cz = center
    a, b, c = normal

    u = -1.0, 0.0, a
    v = 0.0, -1.0, b
    w = cross_vectors(u, v)

    uvw = [normalize_vector(u), normalize_vector(v), normalize_vector(w)]

    colour = colour if colour else (1.0, 0.0, 0.0, 0.5)
    sector = 2 * pi  / n

    glcolour4f(*colour)

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
        colour = attr['colour']
        size  = attr['size']
        glcolour3f(*colour)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex3f(*pos)
        glEnd()
        pass


def xdraw_lines(lines):
    for attr in lines:
        start = attr['start']
        end   = attr['end']
        colour = attr['colour']
        width = attr['width']
        glcolour3f(*colour)
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex3f(*start)
        glVertex3f(*end)
        glEnd()


def xdraw_polygons(polygons):
    for attr in polygons:
        points      = attr['points']
        colour_front = attr['colour.front']
        colour_back  = attr['colour.back']
        colour_wires = attr.get('colour.wires', (0.0, 0.0, 0.0, 1.0))
        wires_on    = attr.get('wires_on', False)
        # front faces
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glcolour4f(*colour_front)
        glBegin(GL_POLYGON)
        for xyz in points:
            glVertex3f(*xyz)
        glEnd()
        if wires_on:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glcolour4f(*colour_wires)
            glBegin(GL_POLYGON)
            for xyz in points:
                glVertex3f(*xyz)
            glEnd()
        # back faces
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glcolour4f(*colour_back)
        glBegin(GL_POLYGON)
        for xyz in points[::-1]:
            glVertex3f(*xyz)
        glEnd()
        if wires_on:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glcolour4f(*colour_wires)
            glBegin(GL_POLYGON)
            for xyz in points[::-1]:
                glVertex3f(*xyz)
            glEnd()


def xdraw_texts(texts):
    for attr in texts:
        text  = attr['text']
        pos   = attr['pos']
        colour = attr['colour']
        shift = attr['shift']
        glcolour4f(colour[0], colour[1], colour[2], colour[3])
        glRasterPos3f(pos[0] + shift[0], pos[1] + shift[1], pos[2] + shift[2])
        font = GLUT_BITMAP_HELVETICA_18
        for char in text:
            glutBitmapCharacter(font, ord(char))


def xdraw_spheres(spheres):
    for attr in spheres:
        glPushMatrix()
        glTranslatef(* attr['pos'])
        glcolour3f(* attr['colour'])
        glutSolidSphere(attr['size'], 24, 24)
        glPopMatrix()


def xdraw_cylinders(cylinders):
    for attr in cylinders:
        points = [attr['start'], attr['start'], attr['end'], attr['end']]
        colours = [attr['colour'], attr['colour'], attr['colour'], attr['colour']]
        glePolyCylinder(points, colours, attr['width'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
