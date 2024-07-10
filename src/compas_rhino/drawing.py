from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import wraps

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import System  # type: ignore

from compas.geometry import centroid_polygon
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.layers import clear_current_layer
from compas_rhino.layers import clear_layer
from compas_rhino.layers import create_layers_from_path

find_object = sc.doc.Objects.Find
add_point = sc.doc.Objects.AddPoint
add_line = sc.doc.Objects.AddLine
add_dot = sc.doc.Objects.AddTextDot
add_curve = sc.doc.Objects.AddCurve
add_polyline = sc.doc.Objects.AddPolyline
add_brep = sc.doc.Objects.AddBrep
add_sphere = sc.doc.Objects.AddSphere
add_mesh = sc.doc.Objects.AddMesh
add_circle = sc.doc.Objects.AddCircle
add_surface = sc.doc.Objects.AddSurface

TOL = sc.doc.ModelAbsoluteTolerance

try:
    find_layer_by_fullpath = sc.doc.Layers.FindByFullPath
except SystemError:
    find_layer_by_fullpath = None


def wrap_drawfunc(f):
    """Wraps all ``draw_`` functions with support for recurring keyword arguments."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        layer = kwargs.get("layer", None)
        clear = kwargs.get("clear", False)
        redraw = kwargs.get("redraw", False)
        if layer:
            if not rs.IsLayer(layer):
                create_layers_from_path(layer)
            previous = rs.CurrentLayer(layer)
        if clear:
            if not layer:
                clear_current_layer()
            else:
                clear_layer(layer)
        rs.EnableRedraw(False)
        res = f(*args, **kwargs)
        if redraw:
            rs.EnableRedraw(True)
        if layer:
            rs.CurrentLayer(previous)  # type: ignore
        return res

    return wrapper


@wrap_drawfunc
def draw_labels(labels, **kwargs):
    """Draw labels as text dots and optionally set individual font, fontsize, name, layer and color.

    Parameters
    ----------
    labels : list[dict]
        A list of labels dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A label dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "pos": And(list, lambda x: len(x) == 3),
                "text": And(str, len),
                Optional("name", default=""): str,
                Optional("color", default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
                Optional("fontsize", default=10): Or(int, float),
                Optional("font", default="Arial Regular"): str,
            }
        )

    """
    guids = []
    for label in iter(labels):
        pos = label["pos"]
        text = label["text"]
        name = label.get("name", "")
        color = label.get("color", None)
        layer = label.get("layer")
        size = label.get("fontsize", 10)
        font = label.get("font", "Arial Regular")
        dot = Rhino.Geometry.TextDot(str(text), Rhino.Geometry.Point3d(*pos))
        dot.FontHeight = size
        dot.FontFace = font
        guid = add_dot(dot)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_points(points, **kwargs):
    """Draw points and optionally set individual name, layer, and color properties.

    Parameters
    ----------
    labels : list[dict]
        A list of point dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A point dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "pos": And(list, lambda x: len(x) == 3),
                Optional("name", default=""): str,
                Optional("color", default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    for p in iter(points):
        pos = p["pos"]
        name = p.get("name", "")
        color = p.get("color")
        layer = p.get("layer")
        guid = add_point(Rhino.Geometry.Point3d(*pos))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_lines(lines, **kwargs):
    """Draw lines and optionally set individual name, color, arrow, layer, and
    width properties.

    Parameters
    ----------
    labels : list[dict]
        A list of line dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A line dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "start": And(list, lambda x: len(x) == 3),
                "end": And(list, lambda x: len(x) == 3),
                Optional("name", default=""): str,
                Optional("color", default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
                Optional("arrow", default=None): str,
                Optional("width", default=None): Or(int, float),
            }
        )

    """
    guids = []
    for line in iter(lines):
        sp = line["start"]
        ep = line["end"]
        name = line.get("name", "")
        color = line.get("color")
        arrow = line.get("arrow")
        layer = line.get("layer")
        width = line.get("width")
        guid = add_line(Rhino.Geometry.Point3d(*sp), Rhino.Geometry.Point3d(*ep))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if arrow == "end":
            attr.ObjectDecoration = Rhino.DocObjects.ObjectColorSource.EndArrowhead
        if arrow == "start":
            attr.ObjectDecoration = Rhino.DocObjects.ObjectColorSource.StartArrowhead
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        if width:
            attr.PlotWeight = width
            attr.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_geodesics(geodesics, **kwargs):
    """Draw geodesic lines on specified surfaces, and optionally set individual
    name, color, arrow, and layer properties.

    Parameters
    ----------
    labels : list[dict]
        A list of geodesic dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A geodesic dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "start": And(list, lambda x: len(x) == 3),
                "end": And(list, lambda x: len(x) == 3),
                "srf": Or(str, System.Guid),
                Optional("name", default=""): str,
                Optional("color", default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
                Optional("arrow", default=None): str,
            }
        )

    """
    guids = []
    for g in iter(geodesics):
        sp = g["start"]
        ep = g["end"]
        srf = g["srf"]
        name = g.get("name", "")
        color = g.get("color")
        arrow = g.get("arrow")
        layer = g.get("layer")
        # replace this by a proper rhinocommon call
        guid = rs.ShortPath(srf, Rhino.Geometry.Point3d(*sp), Rhino.Geometry.Point3d(*ep))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if arrow == "end":
            attr.ObjectDecoration = Rhino.DocObjects.ObjectColorSource.EndArrowhead
        if arrow == "start":
            attr.ObjectDecoration = Rhino.DocObjects.ObjectColorSource.StartArrowhead
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_polylines(polylines, **kwargs):
    """Draw polylines, and optionally set individual name, color, arrow, and
    layer properties.

    Parameters
    ----------
    labels : list[dict]
        A list of polyline dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A polyline dict has the following schema:

    .. code-block:: python

        Schema({
            'points': And(list, lambda x: all(len(point) == 3 for point in x),
            Optional('name', default=''): str,
            Optional('color', default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
            Optional('layer', default=None): str,
            Optional('arrow', default=None): str
        })

    """
    guids = []
    for p in iter(polylines):
        points = p["points"]
        name = p.get("name", "")
        color = p.get("color")
        arrow = p.get("arrow")
        layer = p.get("layer")
        poly = Rhino.Geometry.Polyline([Rhino.Geometry.Point3d(*xyz) for xyz in points])
        poly.DeleteShortSegments(TOL)
        guid = add_polyline(poly)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if arrow == "end":
            attr.ObjectDecoration = Rhino.DocObjects.ObjectColorSource.EndArrowhead
        if arrow == "start":
            attr.ObjectDecoration = Rhino.DocObjects.ObjectColorSource.StartArrowhead
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_breps(faces, u=10, v=10, join=False, **kwargs):
    """Draw polygonal faces as Rhino.Geometry.Breps, and optionally set individual name, color,
    and layer properties.

    Parameters
    ----------
    faces : list[dict]
        A list of brep dictionaries.
        See Notes, for more information about the structure of the dict.
    u : int, optional
        Number of spans in the U direction.
    v : int, optional
        Number of spans in the V direction.
    join : bool, optional
        If True, join the individual faces as polysurfaces

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A brep dict has the following schema:

    .. code-block:: python

        Schema({
            'points': And(list, lambda x: len(x) > 3 and all(len(point) == 3 for point in x),
            Optional('name', default=''): str,
            Optional('color', default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
            Optional('layer', default=None): str,
        })

    Examples
    --------
    Using a compas Mesh as an example:

    >>> from compas.datastructures import Mesh
    >>> from compas.geometry import Box, Frame
    >>> from compas_rhino.utilities import draw_breps
    >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)
    >>> mesh = Mesh.from_shape(box)

    Draw convert each mesh face to brep dict schema:

    >>> vertices = mesh.vertices_attributes("xyz")
    >>> breps = [{"points": mesh.face_coordinates(face)} for face in mesh.faces()]

    Draw brep faces as one joined brep.

    >>> guids = draw_breps(breps, join=True)

    """
    breps = []
    for f in iter(faces):
        points = f["points"]
        name = f.get("name", "")
        color = f.get("color")
        layer = f.get("layer")
        corners = [Rhino.Geometry.Point3d(*point) for point in points + points[:1]]
        pcurve = Rhino.Geometry.PolylineCurve(corners)
        geo = System.Collections.Generic.List[Rhino.Geometry.GeometryBase](1)
        geo.Add(pcurve)
        p = len(points)
        if p == 3:
            brep = Rhino.Geometry.Brep.CreateFromCornerPoints(
                Rhino.Geometry.Point3d(*points[0]),
                Rhino.Geometry.Point3d(*points[1]),
                Rhino.Geometry.Point3d(*points[2]),
                TOL,
            )
        elif p == 4:
            brep = Rhino.Geometry.Brep.CreateFromCornerPoints(
                Rhino.Geometry.Point3d(*points[0]),
                Rhino.Geometry.Point3d(*points[1]),
                Rhino.Geometry.Point3d(*points[2]),
                Rhino.Geometry.Point3d(*points[3]),
                TOL,
            )
        else:
            brep = Rhino.Geometry.Brep.CreatePatch(geo, u, v, TOL)
        if brep:
            breps.append(brep)

    if join:
        breps = Rhino.Geometry.Brep.JoinRhino.Geometry.Breps(breps, TOL)

    guids = []
    for brep in breps:
        guid = add_brep(brep)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_cylinders(cylinders, cap=False, **kwargs):
    """Draw cylinders and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    cylinders : list[dict]
        A list of cylinder dictionaries.
        See Notes, for more information about the structure of the dict.
    cap : bool, optional
        If True, add caps.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A cylinder dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "start": And(list, lambda x: len(x) == 3),
                "end": And(list, lambda x: len(x) == 3),
                "radius": And(Or(int, float), lambda x: x > 0.0),
                Optional("name", default=""): str,
                Optional("color", default=None): (lambda x: len(x) == 3 and all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    for c in iter(cylinders):
        start = c["start"]
        end = c["end"]
        radius = c["radius"]
        name = c.get("name", "")
        color = c.get("color")
        layer = c.get("layer")
        if radius < TOL:
            continue
        base = Rhino.Geometry.Point3d(*start)
        normal = Rhino.Geometry.Point3d(*end) - base
        height = normal.Length
        if height < TOL:
            continue
        plane = Rhino.Geometry.Plane(base, normal)
        circle = Rhino.Geometry.Circle(plane, radius)
        cylinder = Rhino.Geometry.Cylinder(circle, height)
        brep = cylinder.ToRhino.Geometry.Brep(cap, cap)
        if not brep:
            continue
        guid = add_brep(brep)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_pipes(pipes, cap=2, fit=1.0, **kwargs):
    """Draw pipes and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    pipes : list[dict]
        A list of pipe dictionaries.
        See Notes, for more information about the structure of the dict.

    Other Parameters
    ----------------
    cap : {0, 1, 2}, optional
    fit : float, optional

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A pipe dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "points": And(list, lambda x: all(len(y) == 3 for y in x)),
                "radius": And(Or(int, float), lambda x: x > 0.0),
                Optional("name", default=""): str,
                Optional("color", default=None): And(lambda x: len(x) == 3, all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    abs_tol = TOL
    ang_tol = sc.doc.ModelAngleToleranceRadians
    for p in pipes:
        points = p["points"]
        radius = p["radius"]
        name = p.get("name", "")
        color = p.get("color")
        layer = p.get("layer")
        params = [0.0, 1.0]
        cap = System.Enum.ToObject(Rhino.Geometry.PipeCapMode, cap)
        if type(radius) in (int, float):
            radius = [radius] * 2
        radius = [float(r) for r in radius]
        rail = Rhino.Geometry.Curve.CreateControlPointRhino.Geometry.Curve([Rhino.Geometry.Point3d(*xyz) for xyz in points])
        breps = Rhino.Geometry.Brep.CreatePipe(rail, params, radius, 1, cap, fit, abs_tol, ang_tol)
        temp = [add_brep(brep) for brep in breps]
        for guid in temp:
            if not guid:
                continue
            obj = find_object(guid)
            if not obj:
                continue
            attr = obj.Attributes
            if color:
                attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
                attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            else:
                attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
            if layer and find_layer_by_fullpath:
                index = find_layer_by_fullpath(layer, True)
                if index >= 0:
                    attr.LayerIndex = index
            attr.Name = name
            attr.WireDensity = -1
            obj.CommitChanges()
            guids.append(guid)
    return guids


@wrap_drawfunc
def draw_spheres(spheres, **kwargs):
    """Draw spheres and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    spheres : list[dict]
        A list of sphere dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A sphere dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "pos": And(list, lambda x: len(x) == 3),
                "radius": And(Or(int, float), lambda x: x > 0.0),
                Optional("name", default=""): str,
                Optional("color", default=None): And(lambda x: len(x) == 3, all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    for s in iter(spheres):
        pos = s["pos"]
        radius = s["radius"]
        name = s.get("name", "")
        color = s.get("color")
        layer = s.get("layer")
        sphere = Rhino.Geometry.Sphere(Rhino.Geometry.Point3d(*pos), radius)
        guid = add_sphere(sphere)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_mesh(vertices, faces, name=None, color=None, vertex_color=None, disjoint=False, **kwargs):
    """Draw a mesh and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`compas.geometry.Point`]
        A list of point locations.
    faces : list[list[int]]
        A list of faces as lists of indices into `vertices`.
    name : str, optional
        The name of the mesh object in Rhino.
    color : tuple[[int, int, int]], optional
        The base color of the mesh.
    vertex_color : dict[int, tuple[int, int, int]], optional
        A color per vertex of the mesh.
        Vertices without a color specification in this mapping, will receive the base color.
        For example: ``vertex_color = {vertex: Color.from_i(random.random()).rgb255 for face in faces for vertex in face}``
    disjoint : bool, optional
        If True, draw the mesh with disjoint faces.

    Returns
    -------
    System.Guid

    """

    def average_color(colors):
        c = len(colors)
        r, g, b = zip(*colors)
        r = sum(r) / c
        g = sum(g) / c
        b = sum(b) / c
        return int(r), int(g), int(b)

    vertex_color = vertex_color or {}
    vertexcolors = []

    def populate_vertexcolors(face):
        v_count = len(face)
        facecolors = [vertex_color.get(vertex, color) for vertex in face]
        if v_count > 4:
            facecolors.append(average_color(facecolors))
        vertexcolors.extend(facecolors)

    if not disjoint:
        rhino_mesh = vertices_and_faces_to_rhino(vertices, faces, disjoint)
        vertexcolors = [vertex_color.get(vertex, color) for vertex in vertices]
    else:
        rhino_mesh = vertices_and_faces_to_rhino(vertices, faces, disjoint, face_callback=populate_vertexcolors)

    guid = add_mesh(rhino_mesh)

    if guid != System.Guid.Empty:
        if vertexcolors:
            try:
                rs.MeshVertexColors(guid, vertexcolors)
            except Exception:
                pass

        obj = find_object(guid)
        if obj:
            attr = obj.Attributes
            if color:
                attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
                attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            else:
                attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
            if name:
                attr.Name = name
            obj.CommitChanges()
        return guid


@wrap_drawfunc
def draw_faces(faces, **kwargs):
    """Draw faces as individual meshes and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    faces : list[dict]
        A list of face dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A face dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "points": And(len, lambda x: all(len(y) == 3 for y in x)),
                Optional("name", default=""): str,
                Optional("color", default=None): And(lambda x: len(x) == 3, all(0 <= y <= 255 for y in x)),
                Optional("vertexcolors", default=None): And(len, lambda x: all(0 <= y <= 255 for y in x)),
            }
        )

    """
    guids = []
    for face in iter(faces):
        points = face["points"][:]
        name = face.get("name")
        color = face.get("color")
        vertexcolors = face.get("vertexcolors")

        v = len(points)

        if v < 3:
            continue
        elif v == 3:
            mfaces = [[0, 1, 2, 2]]
        elif v == 4:
            mfaces = [[0, 1, 2, 3]]
        else:
            mfaces = [list(range(v))]

        guid = draw_mesh(
            points,
            mfaces,
            color=color,
            name=name,
            clear=False,
            redraw=False,
            layer=None,
        )

        if vertexcolors:
            try:
                rs.MeshVertexColors(guid, vertexcolors)
            except Exception:
                pass

        guids.append(guid)

    return guids


def _face_to_max_quad(points, face):
    faces = []
    c = len(points)
    points.append(centroid_polygon(points))
    for i in range(-1, len(face) - 1):
        a = face[i]
        b = face[i + 1]
        faces.append([c, a, b, b])
    return faces


@wrap_drawfunc
def draw_circles(circles, **kwargs):
    """Draw circles and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    circles : list[dict]
        A list of circle dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A circle dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "plane": lambda x: len(x[0]) == 3 and len(x[1]) == 3,
                "radius": And(Or(int, float), lambda x: x > 0),
                Optional("name", default=""): str,
                Optional("color", default=None): And(lambda x: len(x) == 3, all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    for data in iter(circles):
        point, normal = data["plane"]
        radius = data["radius"]
        name = data.get("name", "")
        color = data.get("color")
        layer = data.get("layer")
        circle = Rhino.Geometry.Circle(Rhino.Geometry.Plane(Rhino.Geometry.Point3d(*point), Rhino.Geometry.Vector3d(*normal)), radius)
        guid = add_circle(circle)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_curves(curves, **kwargs):
    """Draw curves and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    curves : list[dict]
        A list of curve dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A curve dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "curve": compas.geometry.Rhino.Geometry.Curve,
                Optional("name", default=""): str,
                Optional("color", default=None): And(lambda x: len(x) == 3, all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    for data in iter(curves):
        curve = data["curve"]
        name = data.get("name", "")
        color = data.get("color")
        layer = data.get("layer")
        guid = add_curve(curve.rhino_curve)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_surfaces(surfaces, **kwargs):
    """Draw surfaces and optionally set individual name, color, and layer properties.

    Parameters
    ----------
    surfaces : list[dict]
        A list of surface dictionaries.
        See Notes, for more information about the structure of the dict.

    Returns
    -------
    list[System.Guid]

    Notes
    -----
    A surface dict has the following schema:

    .. code-block:: python

        Schema(
            {
                "surface": compas.geometry.Surface,
                Optional("name", default=""): str,
                Optional("color", default=None): And(lambda x: len(x) == 3, all(0 <= y <= 255 for y in x)),
                Optional("layer", default=None): str,
            }
        )

    """
    guids = []
    for data in iter(surfaces):
        surface = data["surface"]
        name = data.get("name", "")
        color = data.get("color")
        layer = data.get("layer")
        guid = add_surface(surface.rhino_surface)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = System.Drawing.Color.FromArgb(*color)
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        else:
            attr.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_drawfunc
def draw_brep(brep, color=None, **kwargs):
    """Draw a brep to the Rhino document.

    Parameters
    ----------
    brep : :class:`compas_rhino.geometry.RhinoRhino.Geometry.Brep`
        The brep to draw.
    color : tuple[int, int, int] | tuple[float, float, float], optional
        The color to draw the brep with.

    Returns
    -------
    :rhino:`System.Guid`
        The Rhino document GUID of the drawn Rhino.Geometry.Brep.

    """
    native_brep = brep.native_brep
    if color:
        for face in native_brep.Faces:
            face.PerFaceColor = System.Drawing.Color.FromArgb(*color)
    return add_brep(native_brep)
