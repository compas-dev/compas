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
    glEnableClientState(GL_COLOR_ARRAY)

    # vertex coordinates flattened
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    for primitive, indices, colors, flag_on in arrays:
        # primitive => GL_POINTS, GL_LINES, GL_TRIANGLES, GL_QUADS
        # colors => RGB colors flattened
        # indices => element vertex indices flattened
        # flag_on => True or False
        if not flag_on:
            continue

        glColorPointer(3, GL_FLOAT, 0, colors)
        glDrawElements(primitive, len(indices), GL_UNSIGNED_INT, indices)

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_triangle_array(vertices, indices, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, indices)
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_line_array(vertices, indices, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glDrawElements(GL_LINES, len(indices), GL_UNSIGNED_INT, indices)
    glDisableClientState(GL_COLOR_ARRAY)
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
#     front = hex_to_rgb(self.settings['faces.color:front'])
#     front = list(front) + [1.0]
#     back  = hex_to_rgb(self.settings['faces.color:back'])
#     back  = list(back) + [1.0]
#     for fkey in self.mesh.faces():
#         faces.append({'points'      : [key_xyz[key] for key in self.mesh.face_vertices(fkey)],
#                       'color.front' : front,
#                       'color.back'  : back})
#     self.view.faces = glGenLists(1)
#     glNewList(self.view.faces, GL_COMPILE)
#     xdraw_polygons(faces)
#     glEndList()

# def _make_edges_list(self, key_xyz):
#     lines = []
#     color = hex_to_rgb(self.settings['edges.color'])
#     width = self.settings['edges.width']
#     for u, v in self.mesh.edges():
#         lines.append({'start' : key_xyz[u],
#                       'end'   : key_xyz[v],
#                       'color' : color,
#                       'width' : width})
#     self.view.edges = glGenLists(1)
#     glNewList(self.view.edges, GL_COMPILE)
#     xdraw_cylinders(lines)
#     glEndList()

# def _make_vertices_list(self, key_xyz):
#     points = []
#     color = hex_to_rgb(self.settings['vertices.color'])
#     size = self.settings['vertices.size']
#     for key in self.mesh.vertices():
#         points.append({'pos'   : key_xyz[key],
#                        'color' : color,
#                        'size'  : size})
#     self.view.vertices = glGenLists(1)
#     glNewList(self.view.vertices, GL_COMPILE)
#     xdraw_spheres(points)
#     glEndList()


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
        color_wires = attr.get('color.wires', (0.0, 0.0, 0.0, 1.0))
        wires_on    = attr.get('wires_on', False)
        # front faces
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor4f(*color_front)
        glBegin(GL_POLYGON)
        for xyz in points:
            glVertex3f(*xyz)
        glEnd()
        if wires_on:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor4f(*color_wires)
            glBegin(GL_POLYGON)
            for xyz in points:
                glVertex3f(*xyz)
            glEnd()
        # back faces
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor4f(*color_back)
        glBegin(GL_POLYGON)
        for xyz in points[::-1]:
            glVertex3f(*xyz)
        glEnd()
        if wires_on:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor4f(*color_wires)
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
        font = GLUT_BITMAP_HELVETICA_18
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
