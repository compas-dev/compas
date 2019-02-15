from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import compas
import compas_rhino

try:
    import System
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find

except ImportError:
    compas.raise_if_ironpython()

else:
    try:
        purge_object = sc.doc.Objects.Purge
    except AttributeError:
        purge_object = None


# get_point_coordinates => get_coordinates_points
# get_line_coordinates => get_coordinates_lines
# get_polyline_coordinates => get_coordinates_polylines
# get_polygon_coordinates => get_coordinates_polygons


__all__ = [
    'get_objects',
    'get_object_layers',
    'get_object_types',
    'get_object_names',
    'get_object_name',
    'get_object_attributes',
    'get_object_attributes_from_name',
    'delete_object',
    'delete_objects',
    'delete_objects_by_name',
    'purge_objects',
    'is_curve_line',
    'is_curve_polyline',
    'is_curve_polygon',
    'get_points',
    'get_curves',
    'get_lines',
    'get_polylines',
    'get_polygons',
    'get_point_coordinates',
    'get_line_coordinates',
    'get_polyline_coordinates',
    'get_polygon_coordinates',
    'get_meshes',
    'get_mesh_face_vertices',
    'get_mesh_vertex_coordinates',
    'get_mesh_vertex_colors',
    'set_mesh_vertex_colors',
    'get_mesh_vertices_and_faces',
    'get_mesh_vertex_index',
    'get_mesh_face_index',
    'get_mesh_edge_index',
    'select_object',
    'select_objects',
    'select_point',
    'select_points',
    'select_curve',
    'select_curves',
    'select_line',
    'select_lines',
    'select_polyline',
    'select_polylines',
    'select_polygon',
    'select_polygons',
    'select_surface',
    'select_surfaces',
    'select_mesh',
    'select_meshes',
]


# ==============================================================================
# Objects
# ==============================================================================


def get_objects(name=None, color=None, layer=None, type=None):
    guids = rs.AllObjects()
    if name:
        guids = list(set(guids) & set(rs.ObjectsByName(name)))
    if color:
        guids = list(set(guids) & set(rs.ObjectsByColor(color)))
    if layer:
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
    if type:
        guids = list(set(guids) & set(rs))
    return guids


def delete_object(guid, purge=None):
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE

    if purge and purge_object:
        purge_objects([guid])
    else:
        delete_objects([guid], purge)


def delete_objects(guids, purge=None):
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE

    if purge and purge_object:
        purge_objects(guids)
    else:
        for guid in guids:
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
        rs.DeleteObjects(guids)


def delete_objects_by_name(name, purge=None):
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE

    guids = get_objects(name)
    delete_objects(guids, purge=purge)


def purge_objects(guids):
    if not purge_object:
        raise RuntimeError('Cannot purge outside Rhino script context')
    for guid in guids:
        if rs.IsObjectHidden(guid):
            rs.ShowObject(guid)
        o = find_object(guid)
        purge_object(o.RuntimeSerialNumber)
    sc.doc.Views.Redraw()


def get_object_layers(guids):
    return [rs.ObjectLayer(guid) for guid in guids]


def get_object_types(guids):
    return [rs.ObjectType(guid) for guid in guids]


def get_object_names(guids):
    return [rs.ObjectName(guid) for guid in guids]


def get_object_name(guid):
    return rs.ObjectName(guid)


def get_object_attributes(guids):
    attrs = []
    for guid in guids:
        o = find_object(guid)
        u = o.Attributes.UserDictionary
        a = {}
        if u.Count:
            for key in u.Keys:
                a[key] = u.Item[key]
        attrs.append(a)
    return attrs


def get_object_attributes_from_name(guids, prefix=None):
    attrs = []
    for name in get_object_names(guids):
        try:
            if prefix:
                name = name.lstrip(prefix)
            attr = literal_eval(name)
        except (ValueError, TypeError):
            attr = {}
        attrs.append(attr)
    return attrs


def select_object(message="Select an object."):
    return rs.GetObject(message)


def select_objects(message='Select objects.'):
    guids = []
    temp = rs.GetObjects(message)
    if temp:
        return temp
    return guids


# ==============================================================================
# Points
# ==============================================================================


def select_point(message='Select a point.'):
    return rs.GetObject(message, filter=rs.filter.point)


def select_points(message='Select points.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.point)
    if temp:
        guids = temp
    return guids


def get_points(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.point)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.point)
    return guids


def get_point_coordinates(guids):
    points = []
    for guid in guids:
        point = rs.PointCoordinates(guid)
        if point:
            points.append(map(float, point))
    return points


# ==============================================================================
# Curves
# ==============================================================================


def is_curve_line(guid):
    return rs.IsCurve(guid) and rs.IsLine(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) == 2


def is_curve_polyline(guid):
    return rs.IsCurve(guid) and rs.IsPolyline(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) > 2


def is_curve_polygon(guid):
    return rs.IsCurve(guid) and rs.IsCurveClosed(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) > 2


def select_curve(message='Select curve.'):
    return rs.GetObject(message, filter=rs.filter.curve)


def select_curves(message='Select curves.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        guids = temp
    return guids


def select_line(message='Select line.'):
    guid = rs.GetObject(message, filter=rs.filter.curve)
    if is_curve_line(guid):
        return guid
    return None


def select_lines(message='Select lines.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_curve_line(guid):
                    guids.append(guid)
    return guids


def select_polyline(message='Select a polyline (curve with degree = 1, and multiple segments).'):
    guid = rs.GetObject(message, filter=rs.filter.curve)
    if is_curve_polyline(guid):
        return guid
    return None


def select_polylines(message='Select polylines (curves with degree = 1, and multiple segments).'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_curve_polyline(guid):
                    guids.append(guid)
    return guids


def select_polygon(message='Select a polygon (closed curve with degree = 1)'):
    guid = rs.GetObject(message, filter=rs.filter.curve)
    if is_curve_polygon(guid):
        return guid
    return None


def select_polygons(message='Select polygons (closed curves with degree = 1)'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_curve_polygon(guid):
                guids.append(guid)
    return guids


def get_curves(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
    return guids


def get_lines(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_line(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_line(guid)]
    return guids


def get_polylines(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polyline(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polyline(guid)]
    return guids


def get_polygons(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polygon(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polygon(guid)]
    return guids


def get_curve_coordinates():
    pass


def get_line_coordinates(guids):
    if isinstance(guids, System.Guid):
        sp = map(float, rs.CurveStartPoint(guids))
        ep = map(float, rs.CurveEndPoint(guids))
        return sp, ep
    lines = []
    for guid in guids:
        sp = map(float, rs.CurveStartPoint(guid))
        ep = map(float, rs.CurveEndPoint(guid))
        lines.append((sp, ep))
    return lines


def get_polycurve_coordinates():
    pass


def get_polyline_coordinates(guids):
    if isinstance(guids, System.Guid):
        points = rs.PolylineVertices(guids)
        coords = []
        if points:
            coords = [map(float, point) for point in points]
        return coords
    polylines = []
    for guid in guids:
        points = rs.PolylineVertices(guid)
        coords = []
        if points:
            coords = [map(float, point) for point in points]
        polylines.append(coords)
    return polylines


def get_polygon_coordinates(guids):
    if isinstance(guids, System.Guid):
        points = rs.CurvePoints(guids)
        coords = []
        if points:
            coords = [list(point) for point in points]
        return coords
    polygons = []
    if guids:
        for guid in guids:
            points = rs.CurvePoints(guid)
            coords = []
            if points:
                coords = map(list, points)
            polygons.append(coords)
    return polygons


# ==============================================================================
# Surfaces
# ==============================================================================


def select_surface(message='Select a surface.'):
    return rs.GetObject(
        message,
        filter=rs.filter.surface | rs.filter.polysurface
    )


def select_surfaces(message='Select surfaces.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.surface | rs.filter.polysurface)
    if temp:
        guids = temp
    return guids


# ==============================================================================
# Meshes
# ==============================================================================


def select_mesh(message='Select a mesh.'):
    return rs.GetObject(
        message,
        filter=rs.filter.mesh
    )


def select_meshes(message='Select meshes.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.mesh)
    if temp:
        guids = temp
    return guids


def get_meshes(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.mesh)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.mesh)
    return guids


def get_mesh_border(guid):
    return rs.DuplicateMeshBorder(guid)


def get_mesh_face_vertices(guid):
    faces = []
    if guid:
        temp = rs.MeshFaceVertices(guid)
        faces = map(list, temp)
    return faces


def get_mesh_vertex_coordinates(guid):
    vertices = []
    if guid:
        vertices = [map(float, vertex) for vertex in rs.MeshVertices(guid)]
    return vertices


def get_mesh_vertex_colors(guid):
    colors = []
    if guid:
        temp = rs.MeshVertexColors(guid)
        if temp:
            colors = map(list, temp)
    return colors


def set_mesh_vertex_colors(guid, colors):
    if not guid:
        return
    return rs.MeshVertexColors(guid, colors)


def get_mesh_vertices_and_faces(guid):
    if not guid:
        return
    vertices = [map(float, vertex) for vertex in rs.MeshVertices(guid)]
    faces = map(list, rs.MeshFaceVertices(guid))
    return vertices, faces


def get_mesh_vertex_index(guid):
    class CustomGetObject(Rhino.Input.Custom.GetObject):
        def CustomGeometryFilter(self, rhino_object, geometry, component_index):
            return guid == rhino_object.Id
    go = CustomGetObject()
    go.SetCommandPrompt('Select a vertex of the mesh.')
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshVertex
    go.AcceptNothing(True)
    if go.Get() != Rhino.Input.GetResult.Object:
        return None
    objref = go.Object(0)
    if not objref:
        return None
    tvindex = objref.GeometryComponentIndex.Index
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    vindex = temp[0]
    go.Dispose()
    return vindex


def get_mesh_face_index(guid):
    class CustomGetObject(Rhino.Input.Custom.GetObject):
        def CustomGeometryFilter(self, rhino_object, geometry, component_index):
            return guid == rhino_object.Id
    go = CustomGetObject()
    go.SetCommandPrompt('Select a face of the mesh.')
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshFace
    go.AcceptNothing(True)
    if go.Get() != Rhino.Input.GetResult.Object:
        return None
    objref = go.Object(0)
    if not objref:
        return None
    findex = objref.GeometryComponentIndex.Index
    go.Dispose()
    return findex


def get_mesh_edge_index(guid):
    class CustomGetObject(Rhino.Input.Custom.GetObject):
        def CustomGeometryFilter(self, rhino_object, geometry, component_index):
            return guid == rhino_object.Id
    go = CustomGetObject()
    go.SetCommandPrompt('Select an edge of the mesh.')
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    go.AcceptNothing(True)
    if go.Get() != Rhino.Input.GetResult.Object:
        return None
    objref = go.Object(0)
    if not objref:
        return None
    eindex = objref.GeometryComponentIndex.Index
    go.Dispose()
    return eindex


def get_mesh_vertex_indices(guid):
    tvindices = rs.GetMeshVertices(guid, 'Select mesh vertices.')
    if not tvindices:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    vindices = []
    for tvindex in tvindices:
        temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
        vindices.append(temp[0])
    return vindices


def get_mesh_face_indices(guid):
    return rs.GetMeshFaces(guid, 'Select mesh faces.')


def get_mesh_vertex_face_indices(guid):
    vindex = get_mesh_vertex_index(guid)
    if vindex is None:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    findices = mgeo.TopologyVertices.ConnectedFaces(vindex)
    return findices


def get_mesh_face_vertex_indices(guid):
    findex = get_mesh_face_index(guid)
    if findex is None:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    tvertices = mgeo.Faces.GetTopologicalVertices(findex)
    vindices = []
    for tvertex in tvertices:
        temp = mgeo.TopologyVertices.MeshVertexIndices(tvertex)
        vindices.append(temp[0])
    return vindices


def get_mesh_edge_vertex_indices(guid):
    eindex = get_mesh_edge_index(guid)
    if eindex is None:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    temp = mgeo.TopologyEdges.GetTopologyVertices(eindex)
    tvindices = temp.I, temp.J
    vindices = []
    for tvindex in tvindices:
        temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
        vindices.append(temp[0])
    return vindices


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
