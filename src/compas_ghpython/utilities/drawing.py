from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import wraps

import compas

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    from System.Collections.Generic import List
    from System.Enum import ToObject
    from System.Array import CreateInstance
    from System.Drawing import Color

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
    from Rhino.Geometry import Vector3f, Point2f

    from compas_rhino.utilities.drawing import _face_to_max_quad

    TOL = sc.doc.ModelAbsoluteTolerance

except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'xdraw_labels',
    'xdraw_frame',
    'xdraw_points',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_polylines',
    'xdraw_faces',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_spheres',
    'xdraw_mesh',
    'xdraw_network',
]


def xdraw_labels(labels):
    # This is not yet possible through GhPython. Using Text Tag from ghpythonlib
    # (only Windows) would be an option, but ghpythonlib.components.TextTag does
    # not return anything.
    raise NotImplementedError


def xdraw_frame(frame):
    """Draw frame.
    """
    pt = Point3d(*iter(frame.point))
    xaxis = Vector3d(*iter(frame.xaxis))
    yaxis = Vector3d(*iter(frame.yaxis))
    return Plane(pt, xaxis, yaxis)


def xdraw_points(points):
    """Draw points.
    """
    rg_points = []
    for p in iter(points):
        pos = p['pos']
        rg_points.append(Point3d(*pos))
    return rg_points


def xdraw_lines(lines):
    """Draw lines.
    """
    rg_lines = []
    for l in iter(lines):
        sp = l['start']
        ep = l['end']
        rg_lines.append(Line(Point3d(*sp), Point3d(*ep)))
    return rg_lines


def xdraw_geodesics(geodesics, **kwargs):
    """Draw geodesic lines on specified surfaces.
    """
    rg_geodesics = []
    for g in iter(geodesics):
        sp = g['start']
        ep = g['end']
        srf = g['srf']
        curve = srf.ShortPath(Point3d(*sp), Point3d(*ep), TOL)
        rg_geodesics.append(curve)
    return rg_geodesics


def xdraw_polylines(polylines):
    """Draw polylines.
    """
    rg_polylines = []
    for p in iter(polylines):
        points = p['points']
        poly = Polyline([Point3d(*xyz) for xyz in points])
        poly.DeleteShortSegments(TOL)
        rg_polylines.append(poly)
    return rg_polylines


def xdraw_faces(faces, **kwargs):
    """Draw polygonal faces as Meshes.
    """
    meshes = []
    for face in iter(faces):
        points = face['points'][:]
        name = face.get('name')
        color = face.get('color')
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
            mesh = xdraw_mesh(points, mfaces, color=vertexcolors)
        else:
            mesh = xdraw_mesh(points, mfaces)
        meshes.append(mesh)

    return meshes


def xdraw_cylinders(cylinders, cap=False):
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


def xdraw_pipes(pipes, cap=2, fit=1.0):
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


def xdraw_spheres(spheres):
    rg_sheres = []
    for s in iter(spheres):
        pos = s['pos']
        radius = s['radius']
        rg_sheres.append(Sphere(Point3d(*pos), radius))
    return rg_sheres


def xdraw_mesh(vertices, faces, color=None, vertex_normals=None, texture_coordinates=None):
    """Draw mesh in Grasshopper.
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


def xdraw_network(network):
    """Draw a network in Grasshopper.
    """
    points = []
    for key, attr in network.vertices(True):
        points.append({
            'pos': network.vertex_coordinates(key),
        })

    lines = []
    for u, v, attr in network.edges(True):
        lines.append({
            'start': network.vertex_coordinates(u),
            'end': network.vertex_coordinates(v),
        })

    points_rg = xdraw_points(points)
    lines_rg = xdraw_lines(lines)

    return points_rg, lines_rg


if __name__ == '__main__':
    pass
