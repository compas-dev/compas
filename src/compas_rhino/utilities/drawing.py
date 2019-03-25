from __future__ import print_function

from functools import wraps

import compas

from compas.geometry import centroid_polygon

from compas_rhino.utilities import create_layers_from_path
from compas_rhino.utilities import clear_layer
from compas_rhino.utilities import clear_current_layer

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb
    from System.Enum import ToObject

    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Polyline
    from Rhino.Geometry import PolylineCurve
    from Rhino.Geometry import GeometryBase
    from Rhino.Geometry import Brep
    from Rhino.Geometry import Cylinder
    from Rhino.Geometry import Circle
    from Rhino.Geometry import Plane
    from Rhino.Geometry import PipeCapMode
    from Rhino.Geometry import Curve
    from Rhino.Geometry import Sphere
    from Rhino.Geometry import TextDot
    from Rhino.DocObjects.ObjectColorSource import ColorFromObject
    from Rhino.DocObjects.ObjectColorSource import ColorFromLayer
    from Rhino.DocObjects.ObjectDecoration import EndArrowhead
    from Rhino.DocObjects.ObjectDecoration import StartArrowhead
    from Rhino.DocObjects.ObjectPlotWeightSource import PlotWeightFromObject

    find_object = sc.doc.Objects.Find
    add_point = sc.doc.Objects.AddPoint
    add_line = sc.doc.Objects.AddLine
    add_dot = sc.doc.Objects.AddTextDot
    add_curve = sc.doc.Objects.AddCurve
    add_polyline = sc.doc.Objects.AddPolyline
    add_brep = sc.doc.Objects.AddBrep
    add_sphere = sc.doc.Objects.AddSphere

    TOL = sc.doc.ModelAbsoluteTolerance

except ImportError:
    compas.raise_if_ironpython()

else:
    try:
        find_layer_by_fullpath = sc.doc.Layers.FindByFullPath
    except SystemError:
        find_layer_by_fullpath = None


__all__ = [
    'xdraw_labels',
    'xdraw_points',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_polylines',
    'xdraw_faces',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_spheres',
    'xdraw_mesh',
]


# ==============================================================================
# Extended drawing
#
# these functions are optimized for speed,
# but potential error checking has been removed
# perhaps a good middle ground would be better...
# ==============================================================================


def wrap_xdrawfunc(f):
    """Wraps all ``xdraw_`` functions with support for recurring keyword arguments."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        layer  = kwargs.get('layer', None)
        clear  = kwargs.get('clear', False)
        redraw = kwargs.get('redraw', True)

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
            rs.CurrentLayer(previous)

        return res
    return wrapper


@wrap_xdrawfunc
def xdraw_labels(labels, **kwargs):
    """Draw labels as text dots and optionally set individual name and color."""
    guids = []
    for l in iter(labels):
        pos   = l['pos']
        text  = l['text']
        name  = l.get('name', '')
        color = l.get('color', None)
        guid  = add_dot(TextDot(str(text), Point3d(*pos)))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_points(points, **kwargs):
    """Draw points and optionally set individual name, layer, and color properties.
    """
    guids = []
    for p in iter(points):
        pos   = p['pos']
        name  = p.get('name', '')
        color = p.get('color')
        layer = p.get('layer')
        guid  = add_point(Point3d(*pos))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_lines(lines, **kwargs):
    """Draw lines and optionally set individual name, color, arrow, layer, and
    width properties.
    """
    guids = []
    for l in iter(lines):
        sp    = l['start']
        ep    = l['end']
        name  = l.get('name', '')
        color = l.get('color')
        arrow = l.get('arrow')
        layer = l.get('layer')
        width = l.get('width')
        guid  = add_line(Point3d(*sp), Point3d(*ep))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if arrow == 'end':
            attr.ObjectDecoration = EndArrowhead
        if arrow == 'start':
            attr.ObjectDecoration = StartArrowhead
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        if width:
            attr.PlotWeight = width
            attr.PlotWeightSource = PlotWeightFromObject
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_geodesics(geodesics, **kwargs):
    """Draw geodesic lines on specified surfaces, and optionally set individual
    name, color, arrow, and layer properties.
    """
    guids = []
    for g in iter(geodesics):
        sp    = g['start']
        ep    = g['end']
        srf   = g['srf']
        name  = g.get('name', '')
        color = g.get('color')
        arrow = g.get('arrow')
        layer = g.get('layer')
        # replace this by a proper rhinocommon call
        guid  = rs.ShortPath(srf, Point3d(*sp), Point3d(*ep))
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if arrow == 'end':
            attr.ObjectDecoration = EndArrowhead
        if arrow == 'start':
            attr.ObjectDecoration = StartArrowhead
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_polylines(polylines, **kwargs):
    """Draw polylines, and optionally set individual name, color, arrow, and
    layer properties.
    """
    guids = []
    for p in iter(polylines):
        points = p['points']
        name   = p.get('name', '')
        color  = p.get('color')
        arrow  = p.get('arrow')
        layer  = p.get('layer')
        poly   = Polyline([Point3d(*xyz) for xyz in points])
        poly.DeleteShortSegments(TOL)
        guid   = add_polyline(poly)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if arrow == 'end':
            attr.ObjectDecoration = EndArrowhead
        if arrow == 'start':
            attr.ObjectDecoration = StartArrowhead
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_breps(faces, srf=None, u=10, v=10, trim=True, tangency=True, spacing=0.1, flex=1.0, pull=1.0, **kwargs):
    """Draw polygonal faces as Breps, and optionally set individual name, color,
    and layer properties.
    """
    guids = []
    for f in iter(faces):
        points  = f['points']
        name    = f.get('name', '')
        color   = f.get('color')
        layer   = f.get('layer')
        corners = [Point3d(*point) for point in points]
        pcurve  = PolylineCurve(corners)
        geo     = List[GeometryBase](1)
        geo.Add(pcurve)
        p = len(points)
        if p == 4:
            brep = Brep.CreateFromCornerPoints(Point3d(*points[0]),
                                               Point3d(*points[1]),
                                               Point3d(*points[2]),
                                               TOL)
        elif p == 5:
            brep = Brep.CreateFromCornerPoints(Point3d(*points[0]),
                                               Point3d(*points[1]),
                                               Point3d(*points[2]),
                                               Point3d(*points[3]),
                                               TOL)
        else:
            brep = Brep.CreatePatch(geo, u, v, TOL)
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
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_cylinders(cylinders, cap=False, **kwargs):
    guids = []
    for c in iter(cylinders):
        start  = c['start']
        end    = c['end']
        radius = c['radius']
        name   = c.get('name', '')
        color  = c.get('color')
        layer  = c.get('layer')
        if radius < TOL:
            continue
        base     = Point3d(*start)
        normal   = Point3d(*end) - base
        height   = normal.Length
        if height < TOL:
            continue
        plane    = Plane(base, normal)
        circle   = Circle(plane, radius)
        cylinder = Cylinder(circle, height)
        brep     = cylinder.ToBrep(cap, cap)
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
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_pipes(pipes, cap=2, fit=1.0, **kwargs):
    guids = []
    abs_tol = TOL
    ang_tol = sc.doc.ModelAngleToleranceRadians
    for p in pipes:
        points  = p['points']
        radius  = p['radius']
        name    = p.get('name', '')
        color   = p.get('color')
        layer   = p.get('layer')
        params  = [0.0, 1.0]
        cap     = ToObject(PipeCapMode, cap)
        if type(radius) in (int, float):
            radius = [radius] * 2
        radius = [float(r) for r in radius]
        rail   = Curve.CreateControlPointCurve([Point3d(*xyz) for xyz in points])
        breps  = Brep.CreatePipe(rail, params, radius, 1, cap, fit, abs_tol, ang_tol)
        temp   = [add_brep(brep) for brep in breps]
        for guid in temp:
            if not guid:
                continue
            obj = find_object(guid)
            if not obj:
                continue
            attr = obj.Attributes
            if color:
                attr.ObjectColor = FromArgb(*color)
                attr.ColorSource = ColorFromObject
            else:
                attr.ColorSource = ColorFromLayer
            if layer and find_layer_by_fullpath:
                index = find_layer_by_fullpath(layer, True)
                if index >= 0:
                    attr.LayerIndex = index
            attr.Name = name
            attr.WireDensity = -1
            obj.CommitChanges()
            guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_spheres(spheres, **kwargs):
    guids = []
    for s in iter(spheres):
        pos    = s['pos']
        radius = s['radius']
        name   = s.get('name', '')
        color  = s.get('color')
        layer  = s.get('layer')
        sphere = Sphere(Point3d(*pos), radius)
        guid   = add_sphere(sphere)
        if not guid:
            continue
        obj = find_object(guid)
        if not obj:
            continue
        attr = obj.Attributes
        if color:
            attr.ObjectColor = FromArgb(*color)
            attr.ColorSource = ColorFromObject
        else:
            attr.ColorSource = ColorFromLayer
        if layer and find_layer_by_fullpath:
            index = find_layer_by_fullpath(layer, True)
            if index >= 0:
                attr.LayerIndex = index
        attr.Name = name
        attr.WireDensity = -1
        obj.CommitChanges()
        guids.append(guid)
    return guids


@wrap_xdrawfunc
def xdraw_mesh(vertices, faces, name=None, color=None, **kwargs):
    guid = rs.AddMesh(vertices, faces)
    if color:
        rs.ObjectColor(guid, color)
    if name:
        rs.ObjectName(guid, name)
    return guid


@wrap_xdrawfunc
def xdraw_faces(faces, **kwargs):
    guids = []
    for face in iter(faces):
        points = face['points'][:]
        name   = face.get('name')
        color  = face.get('color')
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

        guid = xdraw_mesh(points, mfaces, color=color, name=name, clear=False, redraw=False, layer=None)

        if vertexcolors:
            try:
                compas_rhino.set_mesh_vertex_colors(guid, vertexcolors)
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from random import randint
    import time

    points = [(randint(0, 100), randint(0, 100), randint(0, 100)) for i in range(10000)]

    faces = []
    faces.append({
        'points' : [[0, 0, 0], [100, 0, 0], [100, 100, 0], [0, 100, 0], [0, 0, 0]],
        'color'  : (255, 0, 0),
    })

    lines = []
    for i in range(10 - 1):
        lines.append({
            'start' : points[i],
            'end'   : points[i + 1],
            'name'  : 'test',
            'color' : (0, 255, 0),
            'arrow' : 'end',
        })

    polylines = []
    polylines.append({
        'points' : points[:10],
        'color'  : (0, 255, 255),
        'arrow'  : 'start',
    })

    cylinders = []
    for i in range(10 - 1):
        cylinders.append({
            'start'  : points[i],
            'end'    : points[i + 1],
            'radius' : 3,
            'name'   : 'test',
            'color'  : (0, 255, 0),
        })

    pipes = []
    pipes.append({
        'points' : points[:10],
        'color'  : (0, 255, 255),
        'radius' : [3, 5],
    })

    spheres = []
    for i in range(10):
        spheres.append({
            'pos'    : points[i],
            'radius' : 3,
            'color'  : (0, 0, 255),
        })

    t0 = time.time()

    xdraw_faces(faces, layer='Default', clear=True)

    t1 = time.time()

    xdraw_lines(lines, layer='Layer 01', clear=True)

    t2 = time.time()

    xdraw_polylines(polylines, layer='Layer 02', clear=True)

    t3 = time.time()

    xdraw_cylinders(cylinders, layer='Layer 03', clear=True)

    t4 = time.time()

    xdraw_pipes(pipes, layer='Layer 04', clear=True)

    t5 = time.time()

    xdraw_spheres(spheres, layer='Layer 05', clear=True)

    t6 = time.time()

    print()
    print('faces', t1 - t0)
    print('lines', t2 - t1)
    print('polylines', t3 - t2)
    print('cylinders', t4 - t3)
    print('pipes', t5 - t4)
    print('spheres', t6 - t5)
