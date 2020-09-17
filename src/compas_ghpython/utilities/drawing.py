from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino.utilities.drawing import _face_to_max_quad

from System.Enum import ToObject
from System.Array import CreateInstance
from System.Drawing import Color

import rhinoscriptsyntax as rs
import scriptcontext as sc

from Rhino.Geometry import Point3d
from Rhino.Geometry import Vector3d
from Rhino.Geometry import Line
from Rhino.Geometry import Polyline
from Rhino.Geometry import Brep
from Rhino.Geometry import Cylinder
from Rhino.Geometry import Circle
from Rhino.Geometry import Plane
from Rhino.Geometry import PipeCapMode
from Rhino.Geometry import Curve
from Rhino.Geometry import Sphere
from Rhino.Geometry import Mesh
from Rhino.Geometry import Vector3f
from Rhino.Geometry import Point2f

TOL = sc.doc.ModelAbsoluteTolerance


__all__ = [
    'draw_frame',
    'draw_points',
    'draw_lines',
    'draw_geodesics',
    'draw_polylines',
    'draw_faces',
    'draw_cylinders',
    'draw_pipes',
    'draw_spheres',
    'draw_mesh',
    'draw_network',
    'draw_circles',
]


def draw_frame(frame):
    """Draw a frame.
    """
    pt = Point3d(*iter(frame.point))
    xaxis = Vector3d(*iter(frame.xaxis))
    yaxis = Vector3d(*iter(frame.yaxis))
    return Plane(pt, xaxis, yaxis)


def draw_points(points):
    """Draw points.

    Parameters
    ----------
    points : list of dict
        The point definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Point3d`

    Notes
    -----
    .. code-block:: python

        Schema({
            'pos': lambda x: len(x) == 3)
        })

    """
    rg_points = []
    for p in iter(points):
        pos = p['pos']
        rg_points.append(Point3d(*pos))
    return rg_points


def draw_lines(lines):
    """Draw lines.

    Parameters
    ----------
    lines : list of dict
        The line definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Line`

    Notes
    -----
    .. code-block:: python

        Schema({
            'start': lambda x: len(x) == 3),
            'end': lambda x: len(x) == 3),
        })

    """
    rg_lines = []
    for line in iter(lines):
        sp = line['start']
        ep = line['end']
        rg_lines.append(Line(Point3d(*sp), Point3d(*ep)))
    return rg_lines


def draw_geodesics(geodesics):
    """Draw geodesic lines on specified surfaces.

    Parameters
    ----------
    geodesics : list of dict
        The geodesic definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Curve`

    Notes
    -----
    .. code-block:: python

        Schema({
            'start': lambda x: len(x) == 3),
            'end': lambda x: len(x) == 3),
            'srf': str
        })

    """
    rg_geodesics = []
    for g in iter(geodesics):
        sp = g['start']
        ep = g['end']
        srf = g['srf']
        curve = srf.ShortPath(Point3d(*sp), Point3d(*ep), TOL)
        rg_geodesics.append(curve)
    return rg_geodesics


def draw_polylines(polylines):
    """Draw polylines.

    Parameters
    ----------
    polylines : list of dict
        The polyline definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Polyline`

    Notes
    -----
    .. code-block:: python

        Schema({
            'points': lambda x: all(len(y) == 3 for y in x)
        })

    """
    rg_polylines = []
    for p in iter(polylines):
        points = p['points']
        poly = Polyline([Point3d(*xyz) for xyz in points])
        poly.DeleteShortSegments(TOL)
        rg_polylines.append(poly)
    return rg_polylines


def draw_faces(faces):
    """Draw polygonal faces as Meshes.

    Parameters
    ----------
    faces : list of dict
        The face definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Mesh`

    Notes
    -----
    .. code-block:: python

        Schema({
            'points': lambda x: all(len(y) == 3 for y in x),
            Optional('vertexcolors', default=None): lambda x: all(len(y) == 3 for y in x)
        })

    """
    meshes = []
    for face in iter(faces):
        points = face['points'][:]
        vertexcolors = face.get('vertexcolors')
        v = len(points)
        if v < 3:
            continue
        if v == 3:
            mfaces = [[0, 1, 2, 2]]
        elif v == 4:
            mfaces = [[0, 1, 2, 3]]
        else:
            mfaces = _face_to_max_quad(points, range(v))
            if vertexcolors:
                r, g, b = [sum(component) / v for component in zip(*vertexcolors)]
                r = int(min(max(0, r), 255))
                g = int(min(max(0, g), 255))
                b = int(min(max(0, b), 255))
                vertexcolors.append((r, g, b))
        if vertexcolors:
            mesh = draw_mesh(points, mfaces, color=vertexcolors)
        else:
            mesh = draw_mesh(points, mfaces)
        meshes.append(mesh)
    return meshes


def draw_cylinders(cylinders, cap=False):
    """Draw cylinders.

    Parameters
    ----------
    cylinders : list of dict
        The cylinder definitions.

    Other Parameters
    ----------------
    cap : bool, optional
        Default is ``False``.

    Returns
    -------
    list of :class:`Rhino.Geometry.Cylinder`

    Notes
    -----
    .. code-block:: python

        Schema({
            'start': lambda x: len(x) == 3,
            'end': lambda x: len(x) == 3,
            'radius': And(Or(int, float), lambda x: x > 0)
        })

    """
    rg_cylinders = []
    for c in iter(cylinders):
        start = c['start']
        end = c['end']
        radius = c['radius']
        if radius < TOL:
            continue
        base = Point3d(*start)
        normal = Point3d(*end) - base
        height = normal.Length
        if height < TOL:
            continue
        plane = Plane(base, normal)
        circle = Circle(plane, radius)
        cylinder = Cylinder(circle, height)
        brep = cylinder.ToBrep(cap, cap)
        if not brep:
            continue
        rg_cylinders.append(brep)
    return rg_cylinders


def draw_pipes(pipes, cap=2, fit=1.0):
    """Draw pipes.

    Parameters
    ----------
    pipes : list of dict
        The pipe definitions.

    Other Parameters
    ----------------
    cap : {0, 1, 2}, optional
    fit : float, optional

    Returns
    -------
    list of :class:`Rhino.Geometry.Brep`

    Notes
    -----
    .. code-block:: python

        Schema({
            'points': lambda x: all(len(y) == 3 for y in x),
            'radius': And(Or(int, float), lambda x: x > 0)
        })

    """
    abs_tol = TOL
    ang_tol = sc.doc.ModelAngleToleranceRadians
    for p in pipes:
        points = p['points']
        radius = p['radius']
        params = [0.0, 1.0]
        cap = ToObject(PipeCapMode, cap)
        if type(radius) in (int, float):
            radius = [radius] * 2
        radius = [float(r) for r in radius]

        rail = Curve.CreateControlPointCurve([Point3d(*xyz) for xyz in points])
        breps = Brep.CreatePipe(rail, params, radius, 1, cap, fit, abs_tol,
                                ang_tol)
        for brep in breps:
            yield brep


def draw_spheres(spheres):
    """Draw spheres.

    Parameters
    ----------
    spheres : list of dict
        The sphere definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Sphere`

    Notes
    -----
    .. code-block:: python

        Schema({
            'pos': lambda x: len(x) == 3,
            'radius': And(Or(int, float), lambda x: x > 0)
        })

    """
    rg_sheres = []
    for s in iter(spheres):
        pos = s['pos']
        radius = s['radius']
        rg_sheres.append(Sphere(Point3d(*pos), radius))
    return rg_sheres


def draw_mesh(vertices, faces, color=None, vertex_normals=None, texture_coordinates=None):
    """Draw mesh in Grasshopper.

    Parameters
    ----------
    vertices : list of point
        List of vertex locations.
    faces : list of list of int
        List of faces defined as lists of indices into the list of vertices.

    Other Parameters
    ----------------
    color : tuple, list or :class:`System.Drawing.Color`, optional
    vertex_normals : bool, optional
    texture_coordinates

    Returns
    -------
    list of :class:`Rhino.Geometry.Mesh`

    """
    mesh = Mesh()
    for a, b, c in vertices:
        mesh.Vertices.Add(a, b, c)
    for face in faces:
        if len(face) < 4:
            mesh.Faces.AddFace(face[0], face[1], face[2])
        else:
            mesh.Faces.AddFace(face[0], face[1], face[2], face[3])

    if vertex_normals:
        count = len(vertex_normals)
        normals = CreateInstance(Vector3f, count)
        for i, normal in enumerate(vertex_normals):
            normals[i] = Vector3f(normal[0], normal[1], normal[2])
        mesh.Normals.SetNormals(normals)

    if texture_coordinates:
        count = len(texture_coordinates)
        tcs = CreateInstance(Point2f, count)
        for i, tc in enumerate(texture_coordinates):
            tcs[i] = Point2f(tc[0], tc[1])
        mesh.TextureCoordinates.SetTextureCoordinates(tcs)

    if color:
        count = len(vertices)
        colors = CreateInstance(Color, count)
        for i in range(count):
            colors[i] = rs.coercecolor(color)
        mesh.VertexColors.SetColors(colors)

    return mesh


def draw_network(network):
    """Draw a network in Grasshopper.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`

    Returns
    -------
    tuple
        A list of :class:`Rhino.Geometry.Point3d`.
        A list of :class:`Rhino.Geometry.Line`.

    """
    points = []
    for key in network.nodes():
        points.append({
            'pos': network.node_coordinates(key)})
    lines = []
    for u, v in network.edges():
        lines.append({
            'start': network.node_coordinates(u),
            'end': network.node_coordinates(v)})
    points_rg = draw_points(points)
    lines_rg = draw_lines(lines)

    return points_rg, lines_rg


def draw_circles(circles):
    """Draw circles in Grasshopper.

    Parameters
    ----------
    circles : list of dict
        The circle definitions.

    Returns
    -------
    list of :class:`Rhino.Geometry.Circle`

    Notes
    -----
    .. code-block:: python

        Schema({
            'plane': lambda x: len(x[0]) == 3 and len(x[1]) == 3,
            'radius': And(Or(int, float), lambda x: x > 0)
        })

    """
    rg_circles = []
    for c in iter(circles):
        point, normal = c['plane']
        radius = c['radius']
        rg_circles.append(Circle(Plane(Point3d(*point), Vector3d(*normal)), radius))
    return rg_circles


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
