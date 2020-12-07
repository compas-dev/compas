from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

import compas_rhino

import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

find_object = sc.doc.Objects.Find

try:
    purge_object = sc.doc.Objects.Purge
except AttributeError:
    purge_object = None


__all__ = [
    'find_object',
    'get_objects',
    'get_object_layers',
    'get_object_types',
    'get_object_names',
    'get_object_name',
    'get_object_attributes',
    'get_object_attributes_from_name',
    'delete_object',
    'delete_objects',
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
    """Get identifiers of Rhino objects, potentially filtered by name, color, layer, or type.

    Parameters
    ----------
    name : str, optional
    color : tuple or list, optional
        RGB color components in integer format (0-255).
    layer : str, optional
    type : Rhino.DocObjects.ObjectType, optional
        The object type.

    Returns
    -------
    list
        The GUIDs of the objects matching the filter parameters.

    Examples
    --------
    .. code-block:: python

        import compas_rhino

        guids_all = compas_rhino.get_objects()
        guids_compas = compas_rhino.get_objects(name='COMPAS.*')
        guids_red = compas_rhino.get_objects(color=(255, 0, 0))
        guids_points = compas_rhino.get_objects(type=compas_rhino.rs.filter.point)
        guids_redpoints = compas_rhino.get_objects(color=(255, 0, 0), type=compas_rhino.rs.filter.point)

    .. code-block:: python

        guids_all = set(compas_rhino.get_objects())
        guids_compas = set(compas_rhino.get_objects(name='COMPAS.*'))
        guids_red = set(compas_rhino.get_objects(color=(255, 0, 0)))
        guids_points = set(compas_rhino.get_objects(type=compas_rhino.rs.filter.point))
        guids_redpoints = set(compas_rhino.get_objects(color=(255, 0, 0), type=compas_rhino.rs.filter.point))

        print guids_compas.issubset(guids_all)
        print guids_all.issubset(guids_compas)

        # True, False

        print guids_red.issubset(guids_all)
        print guids_points.issubset(guids_all)
        print guids_redpoints.issubset(guids_all)

        # True, True, True

        print guids_redpoints.issubset(guids_points)
        print guids_redpoints.issubset(guids_red)
        print guids_points.issubset(guids_red)

        # True, True, False

    """
    guids = rs.AllObjects()
    if name:
        guids = list(set(guids) & set(rs.ObjectsByName(name)))
    if color:
        guids = list(set(guids) & set(rs.ObjectsByColor(color)))
    if layer:
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
    if type:
        guids = list(set(guids) & set(rs.ObjectsByType(type)))
    return guids


def delete_object(guid, purge=None):
    """Delete Rhino object.

    Parameters
    ----------
    guid : GUID
    purge : None or bool, optional
        If None, the value of the global purge setting (:obj:`compas_rhino.PURGE_ON_DELETE`) will be used.
        If True, purge the object from history after deleting.
        If False, delete but don't purge.
        Default is None.
    """
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE
    if purge and purge_object:
        purge_objects([guid])
    else:
        delete_objects([guid], purge)


def delete_objects(guids, purge=None):
    """Delete multiple Rhino objects.

    Parameters
    ----------
    guids : list of GUID
    purge : None or bool, optional
        If None, the value of the global purge setting (:obj:`compas_rhino.PURGE_ON_DELETE`) will be used.
        If True, purge the objects from history after deleting.
        If False, delete but don't purge.
        Default is None.
    """
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE
    if purge and purge_object:
        purge_objects(guids)
    else:
        rs.EnableRedraw(False)
        for guid in guids:
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
        rs.DeleteObjects(guids)
        rs.EnableRedraw(True)
        sc.doc.Views.Redraw()


def purge_objects(guids):
    """Purge objects from memory.

    Parameters
    ----------
    guids : list of GUID
    """
    if not purge_object:
        raise RuntimeError('Cannot purge outside Rhino script context')
    rs.EnableRedraw(False)
    for guid in guids:
        if rs.IsObject(guid):
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
            o = find_object(guid)
            purge_object(o.RuntimeSerialNumber)
    rs.EnableRedraw(True)
    sc.doc.Views.Redraw()


def get_object_layers(guids):
    """Get the layer names of multiple objects.

    Parameters
    ----------
    guids : list of GUID

    Returns
    -------

    """
    return [rs.ObjectLayer(guid) for guid in guids]


def get_object_types(guids):
    return [rs.ObjectType(guid) for guid in guids]


def get_object_names(guids):
    return [rs.ObjectName(guid) for guid in guids]


def get_object_name(guid):
    return rs.ObjectName(guid)


def get_object_attributes(guids):
    """Get attributes from object user dictionaries.

    Parameters
    ----------
    guids : list of GUID

    Returns
    -------
    list of dict
    """
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
    """Get attributes from JSON parsable object names.

    Parameters
    ----------
    guids : list of GUID
    prefix : str, optional
        A prefix that should be removed before the name is JSON parsable.
        For example, in Rhino 6 and above, names can't start with curly braces ("{").
        Therefore, to make the string representation of a dict a valid name it has to be prefixed with something.
        This prefix can be stripped automatically using this parameter.

    Results
    -------
    list of dict
        The attribute dicts of the objects.
    """
    load = json.loads
    attrs = []
    for name in get_object_names(guids):
        try:
            if prefix:
                name = name.lstrip(prefix)
            attr = load(name)
        except (ValueError, TypeError):
            attr = {}
        attrs.append(attr)
    return attrs


def select_object(message="Select an object."):
    """Select one object in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an object.".

    Returns
    -------
    GUID
        The identifer of the selected object.
    """
    return rs.GetObject(message)


def select_objects(message='Select multiple objects.'):
    """Select multiple objects in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select objects.".

    Returns
    -------
    list of GUID
        The identifers of the selected objects.
    """
    guids = []
    temp = rs.GetObjects(message)
    if temp:
        return temp
    return guids


# ==============================================================================
# Points
# ==============================================================================


def select_point(message='Select one point.'):
    """Select one point in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an point.".

    Returns
    -------
    GUID
        The identifer of the selected point.
    """
    return rs.GetObject(message, preselect=True, select=True, filter=rs.filter.point)


def select_points(message='Select multiple points.'):
    """Select multiple points in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select points.".

    Returns
    -------
    list of GUID
        The identifers of the selected points.
    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.point)
    if temp:
        guids = temp
    return guids


def get_points(layer=None):
    if layer:
        rs.EnableRedraw(False)
        # Argument names for LayerVisible command are not the same for Rhino5 and Rhino6
        # that is why we use positional instead of named arguments
        visible = rs.LayerVisible(layer, True, True)
        guids = rs.ObjectsByType(rs.filter.point)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible, True)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.point)
    return guids


def get_point_coordinates(guids):
    """Get the coordintes of the locations of point objects.

    Parameters
    ----------
    guids : list of GUID

    Returns
    -------
    list of point
        The location coordinates of the points.
    """
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


def select_curve(message='Select one curve.'):
    """Select one curve in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an line.".

    Returns
    -------
    GUID
        The identifer of the selected curve.
    """
    return rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)


def select_curves(message='Select multiple curves.'):
    """Select multiple curves in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an line.".

    Returns
    -------
    list of GUID
        The identifers of the selected curves.
    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    if temp:
        guids = temp
    return guids


def select_line(message='Select line.'):
    """Select one line in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an line.".

    Returns
    -------
    GUID
        The identifer of the selected line.
    """
    guid = rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)
    if is_curve_line(guid):
        return guid
    return None


def select_lines(message='Select multiple lines.'):
    """Select multiple lines in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select lines.".

    Returns
    -------
    list of GUID
        The identifers of the selected lines.
    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_curve_line(guid):
                guids.append(guid)
    return guids


def select_polyline(message='Select one polyline (curve with degree = 1, and multiple segments).'):
    """Select one polyline in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an polyline.".

    Returns
    -------
    GUID
        The identifer of the selected polyline.
    """
    guid = rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)
    if is_curve_polyline(guid):
        return guid
    return None


def select_polylines(message='Select multiple polylines (curves with degree = 1, and multiple segments).'):
    """Select multiple polylines in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select polylines.".

    Returns
    -------
    list of GUID
        The identifers of the selected polylines.
    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_curve_polyline(guid):
                guids.append(guid)
    return guids


def select_polygon(message='Select one polygon (closed curve with degree = 1)'):
    """Select one polygon in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an polygon.".

    Returns
    -------
    GUID
        The identifer of the selected polygon.
    """
    guid = rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)
    if is_curve_polygon(guid):
        return guid
    return None


def select_polygons(message='Select multiple polygons (closed curves with degree = 1)'):
    """Select multiple polygons in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select polygons.".

    Returns
    -------
    list of GUID
        The identifers of the selected polygons.
    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_curve_polygon(guid):
                guids.append(guid)
    return guids


def get_curves(layer=None):
    if layer:
        rs.EnableRedraw(False)
        # Argument names for LayerVisible command are not the same for Rhino5 and Rhino6
        # that is why we use positional instead of named arguments
        visible = rs.LayerVisible(layer, True, True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible, True)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
    return guids


def get_lines(layer=None):
    if layer:
        rs.EnableRedraw(False)
        # Argument names for LayerVisible command are not the same for Rhino5 and Rhino6
        # that is why we use positional instead of named arguments
        visible = rs.LayerVisible(layer, True, True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_line(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible, True)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_line(guid)]
    return guids


def get_polylines(layer=None):
    if layer:
        rs.EnableRedraw(False)
        # Argument names for LayerVisible command are not the same for Rhino5 and Rhino6
        # that is why we use positional instead of named arguments
        visible = rs.LayerVisible(layer, True, True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polyline(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible, True)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polyline(guid)]
    return guids


def get_polygons(layer=None):
    if layer:
        rs.EnableRedraw(False)
        # Argument names for LayerVisible command are not the same for Rhino5 and Rhino6
        # that is why we use positional instead of named arguments
        visible = rs.LayerVisible(layer, True, True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_curve_polygon(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible, True)
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


def select_surface(message='Select one surface.'):
    """Select one surface in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an surface.".

    Returns
    -------
    GUID
        The identifer of the selected surface.
    """
    return rs.GetObject(
        message, preselect=True, select=True,
        filter=rs.filter.surface | rs.filter.polysurface)


def select_surfaces(message='Select multiple surfaces.'):
    """Select multiple surfaces in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select surfaces.".

    Returns
    -------
    list of GUID
        The identifers of the selected surfaces.
    """
    guids = []
    temp = rs.GetObjects(
        message, preselect=True, select=True, group=False,
        filter=rs.filter.surface | rs.filter.polysurface)
    if temp:
        guids = temp
    return guids


# ==============================================================================
# Meshes
# ==============================================================================


def select_mesh(message='Select one mesh.'):
    """Select one mesh in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select an mesh.".

    Returns
    -------
    GUID
        The identifer of the selected mesh.
    """
    return rs.GetObject(
        message, preselect=True, select=True,
        filter=rs.filter.mesh
    )


def select_meshes(message='Select multiple meshes.'):
    """Select multiple meshes in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Default is "Select meshs.".

    Returns
    -------
    list of GUID
        The identifers of the selected meshs.
    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.mesh)
    if temp:
        guids = temp
    return guids


def get_meshes(layer=None):
    if layer:
        rs.EnableRedraw(False)
        # Argument names for LayerVisible command are not the same for Rhino5 and Rhino6
        # that is why we use positional instead of named arguments
        visible = rs.LayerVisible(layer, True, True)
        guids = rs.ObjectsByType(rs.filter.mesh)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible, True)
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
    go.SetCommandPrompt('Select one vertex of the mesh.')
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
    go.SetCommandPrompt('Select one face of the mesh.')
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
