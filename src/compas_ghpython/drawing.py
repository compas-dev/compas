from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import rhinoscriptsyntax as rs
import scriptcontext as sc
from Rhino.Geometry import Brep
from Rhino.Geometry import Circle
from Rhino.Geometry import Curve
from Rhino.Geometry import Cylinder
from Rhino.Geometry import Line
from Rhino.Geometry import Mesh
from Rhino.Geometry import PipeCapMode
from Rhino.Geometry import Plane
from Rhino.Geometry import Point2f
from Rhino.Geometry import Point3d
from Rhino.Geometry import PolylineCurve
from Rhino.Geometry import Sphere
from Rhino.Geometry import Vector3d
from Rhino.Geometry import Vector3f

from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.itertools import pairwise

try:
    from Rhino.Geometry import MeshNgon
except ImportError:
    MeshNgon = False

TOL = sc.doc.ModelAbsoluteTolerance


def _face_to_max_quad(points, face):
    faces = []
    c = len(points)
    points.append(centroid_polygon(points))
    for i in range(-1, len(face) - 1):
        a = face[i]
        b = face[i + 1]
        faces.append([c, a, b, b])
    return faces


def draw_frame(frame):
    """Draw a frame."""
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
    list[:rhino:`Rhino.Geometry.Point3d`]

    Notes
    -----
    .. code-block:: python

        Schema({
            'pos': lambda x: len(x) == 3)
        })

    """
    rg_points = []
    for p in iter(points):
        pos = p["pos"]
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
    list[:rhino:`Rhino.Geometry.Line`]

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
        sp = line["start"]
        ep = line["end"]
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
    list[:rhino:`Rhino.Geometry.Curve`]

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
        sp = g["start"]
        ep = g["end"]
        srf = g["srf"]
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
    list[:rhino:`Rhino.Geometry.PolylineCurve`]

    Notes
    -----
    .. code-block:: python

        Schema({"points": lambda x: all(len(y) == 3 for y in x)})

    """
    rg_polylines = []
    # We need to use PolylineCurve because of this:
    # https://discourse.mcneel.com/t/polyline-output-wanted-but-got-a-list-of-points/77509
    for p in iter(polylines):
        points = p["points"]
        poly = PolylineCurve([Point3d(*xyz) for xyz in points])
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
    list[:rhino:`Rhino.Geometry.Mesh`]

    Notes
    -----
    .. code-block:: python

        Schema({"points": lambda x: all(len(y) == 3 for y in x), Optional("vertexcolors", default=None): lambda x: all(len(y) == 3 for y in x)})

    """
    meshes = []
    for face in iter(faces):
        points = face["points"][:]
        vertexcolors = face.get("vertexcolors")
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
        Default is False.

    Returns
    -------
    list[:rhino:`Rhino.Geometry.Cylinder`]

    Notes
    -----
    .. code-block:: python

        Schema({"start": lambda x: len(x) == 3, "end": lambda x: len(x) == 3, "radius": And(Or(int, float), lambda x: x > 0)})

    """
    rg_cylinders = []
    for c in iter(cylinders):
        start = c["start"]
        end = c["end"]
        radius = c["radius"]
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
    list[:rhino:`Rhino.Geometry.Brep`]

    Notes
    -----
    .. code-block:: python

        Schema({"points": lambda x: all(len(y) == 3 for y in x), "radius": And(Or(int, float), lambda x: x > 0)})

    """
    abs_tol = TOL
    ang_tol = sc.doc.ModelAngleToleranceRadians
    for p in pipes:
        points = p["points"]
        radius = p["radius"]
        params = [0.0, 1.0]
        cap = PipeCapMode(cap)
        if type(radius) in (int, float):
            radius = [radius] * 2
        radius = [float(r) for r in radius]

        rail = Curve.CreateControlPointCurve([Point3d(*xyz) for xyz in points])
        breps = Brep.CreatePipe(rail, params, radius, 1, cap, fit, abs_tol, ang_tol)
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
    list[:rhino:`Rhino.Geometry.Sphere`]

    Notes
    -----
    .. code-block:: python

        Schema({"pos": lambda x: len(x) == 3, "radius": And(Or(int, float), lambda x: x > 0)})

    """
    rg_sheres = []
    for s in iter(spheres):
        pos = s["pos"]
        radius = s["radius"]
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
    color : tuple, list | :class:`System.Drawing.Color`, optional
    vertex_normals : bool, optional
    texture_coordinates

    Returns
    -------
    list[:rhino:`Rhino.Geometry.Mesh`]

    """
    mesh = Mesh()
    for a, b, c in vertices:
        mesh.Vertices.Add(a, b, c)
    for face in faces:
        f = len(face)
        if f < 3:
            continue
        if f == 3:
            mesh.Faces.AddFace(*face)
        elif f == 4:
            mesh.Faces.AddFace(*face)
        else:
            if MeshNgon:
                centroid = centroid_points([vertices[index] for index in face])
                c = mesh.Vertices.Add(*centroid)
                facets = []
                for i, j in pairwise(face + face[:1]):
                    facets.append(mesh.Faces.AddFace(i, j, c))
                ngon = MeshNgon.Create(face, facets)
                mesh.Ngons.AddNgon(ngon)

    if vertex_normals:
        count = len(vertex_normals)
        normals = [Vector3f(normal[0], normal[1], normal[2]) for normal in vertex_normals]
        mesh.Normals.SetNormals(normals)

    if texture_coordinates:
        count = len(texture_coordinates)
        tcs = [Point2f(tc[0], tc[1]) for tc in texture_coordinates]
        mesh.TextureCoordinates.SetTextureCoordinates(tcs)

    if color:
        count = len(mesh.Vertices)
        color = rs.CreateColor(color)

        for i in range(count):
            mesh.VertexColors.SetColor(i, color.R, color.G, color.B)

    return mesh


def draw_graph(graph):
    """Draw a graph in Grasshopper.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph`

    Returns
    -------
    tuple
        A list[:rhino:`Rhino.Geometry.Point3d`].
        A list[:rhino:`Rhino.Geometry.Line`].

    """
    points = []
    for key in graph.nodes():
        points.append({"pos": graph.node_coordinates(key)})
    lines = []
    for u, v in graph.edges():
        lines.append({"start": graph.node_coordinates(u), "end": graph.node_coordinates(v)})
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
    list[:rhino:`Rhino.Geometry.Circle`]

    Notes
    -----
    .. code-block:: python

        Schema({"plane": lambda x: len(x[0]) == 3 and len(x[1]) == 3, "radius": And(Or(int, float), lambda x: x > 0)})

    """
    rg_circles = []
    for c in iter(circles):
        point, normal = c["plane"]
        radius = c["radius"]
        rg_circles.append(Circle(Plane(Point3d(*point), Vector3d(*normal)), radius))
    return rg_circles


def draw_brep(brep):
    """Draw a RhinoBrep in Grasshopper.

    Parameters
    ----------
    brep : :class:`compas.geometry.RhinoBrep`
        The Brep to draw.

    Returns
    -------
    :rhino:`Rhino.Geometry.Brep`

    """
    return brep.native_brep
