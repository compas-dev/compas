from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import warnings

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import System  # type: ignore

import compas_rhino

find_object = sc.doc.Objects.Find

try:
    purge_object = sc.doc.Objects.Purge
except AttributeError:
    purge_object = None


# ==============================================================================
# Deprecated
# ==============================================================================


def get_point_coordinates(guids):
    """Get the coordintes of the locations of point objects.

    Parameters
    ----------
    guids : list[System.Guid]

    Returns
    -------
    list[[float, float, float]]
        The location coordinates of the points.

    Warnings
    --------
    .. deprecated:: 2.3
        Use `compas_rhino.conversions` instead.

    """
    warnings.warn("This function will be removed in v2.3. Please use `compas_rhino.conversions` instead.", DeprecationWarning, stacklevel=2)

    points = []
    for guid in guids:
        point = rs.PointCoordinates(guid)
        if point:
            points.append(point)
    return points


def get_line_coordinates(guids):
    """Get the start and end point coordinates of line curves.

    Parameters
    ----------
    guids : list[System.Guid]
        Line curve identifiers.

    Returns
    -------
    list[tuple[[float, float, float], [float, float, float]]]
        A start and end point per line.

    Warnings
    --------
    .. deprecated:: 2.3
        Use `compas_rhino.conversions` instead.

    """
    warnings.warn("This function will be removed in v2.3. Please use `compas_rhino.conversions` instead.", DeprecationWarning, stacklevel=2)

    if isinstance(guids, System.Guid):
        sp = rs.CurveStartPoint(guids)
        ep = rs.CurveEndPoint(guids)
        return [sp.X, sp.Y, sp.Z], [ep.X, ep.Y, ep.Z]
    lines = []
    for guid in guids:
        sp = rs.CurveStartPoint(guid)
        ep = rs.CurveEndPoint(guid)
        lines.append(([sp.X, sp.Y, sp.Z], [ep.X, ep.Y, ep.Z]))
    return lines


def get_polyline_coordinates(guids):
    """Get the point coordinates of polylines.

    Parameters
    ----------
    guids : list[System.Guid]
        Polyline curve identifiers.

    Returns
    -------
    list[list[[float, float, float]]]
        A list of point coordinates per polyline.

    Warnings
    --------
    .. deprecated:: 2.3
        Use `compas_rhino.conversions` instead.

    """
    warnings.warn("This function will be removed in v2.3. Please use `compas_rhino.conversions` instead.", DeprecationWarning, stacklevel=2)

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
    """Get the point coordinates of polygons.

    Parameters
    ----------
    guids : list[System.Guid]
        Polygon curve identifiers.

    Returns
    -------
    list[list[[float, float, float]]]
        A list of point coordinates per polygon.

    Warnings
    --------
    .. deprecated:: 2.3
        Use `compas_rhino.conversions` instead.

    """
    warnings.warn("This function will be removed in v2.3. Please use `compas_rhino.conversions` instead.", DeprecationWarning, stacklevel=2)

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
# Get objects by filtering
# ==============================================================================


def get_objects(name=None, color=None, layer=None, type=None):
    """Get identifiers of Rhino objects, potentially filtered by name, color, layer, or type.

    Parameters
    ----------
    name : str, optional
        Name of the objects.
    color : tuple or list, optional
        RGB color components in integer format (0-255).
    layer : str, optional
        Layer containing the objects.
    type : Rhino.DocObjects.ObjectType, optional
        The object type.

    Returns
    -------
    list[System.Guid]
        The System.Guids of the objects matching the filter parameters.

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


def get_points(layer=None):
    """Get all points.

    Parameters
    ----------
    layer : str, optional
        Name of a layer containing the points.

    Returns
    -------
    list[System.Guid]
        The identifiers of the points.

    """
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


def get_curves(layer=None):
    """Get all curves.

    Parameters
    ----------
    layer : str, optional
        Name of a layer containing the curves.

    Returns
    -------
    list[System.Guid]
        The identifiers of the curves.

    """
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
    """Get all lines.

    Parameters
    ----------
    layer : str, optional
        Name of a layer containing the lines.

    Returns
    -------
    list[System.Guid]
        The identifiers of the lines.

    """
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
    """Get all polylines.

    Parameters
    ----------
    layer : str, optional
        Name of a layer containing the polylines.

    Returns
    -------
    list[System.Guid]
        The identifiers of the polylines.

    """
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
    """Get all polygons.

    Parameters
    ----------
    layer : str, optional
        Name of a layer containing the polygons.

    Returns
    -------
    list[System.Guid]
        The identifiers of the polygons.

    """
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


def get_meshes(layer=None):
    """Get (all) meshes.

    Parameters
    ----------
    layer : str, optional
        Name of a layer containing the meshes.

    Returns
    -------
    list[System.Guid]
        The identifiers of the meshes.

    """
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


# ==============================================================================
# Object info
# ==============================================================================


def get_object_layers(guids):
    """Get the layer names of multiple objects.

    Parameters
    ----------
    guids : list[System.Guid]
        Object identifiers.

    Returns
    -------
    list[str]

    """
    return [rs.ObjectLayer(guid) for guid in guids]


def get_object_types(guids):
    """Get the type of multiple objects.

    Parameters
    ----------
    guids : list[System.Guid]
        Object identifiers.

    Returns
    -------
    list[str]

    """
    return [rs.ObjectType(guid) for guid in guids]


def get_object_names(guids):
    """Get the names of multiple objects.

    Parameters
    ----------
    guids : list[System.Guid]
        Object identifiers.

    Returns
    -------
    list[str]

    """
    return [rs.ObjectName(guid) for guid in guids]


def get_object_name(guid):
    """Get the name of one object.

    Parameters
    ----------
    guid : System.Guid
        Object identifier.

    Returns
    -------
    str

    """
    return rs.ObjectName(guid)


def get_object_attributes(guid):
    """Get attributes from an object's user dictionary.

    Parameters
    ----------
    guid : System.Guid
        Object identifier.

    Returns
    -------
    dict[str, Any]

    """
    o = find_object(guid)
    u = o.Attributes.UserDictionary
    a = {}
    if u.Count:
        for key in u.Keys:
            a[key] = u.Item[key]
    return a


def set_object_attributes(guid, attr):
    """Set the custom attributes of a Rhino object.

    Parameters
    ----------
    guid : System.Guid
        Object identifier.
    attr : dict[str, Any]
        A dictionary of attributes.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If the operation fails.

    """
    o = find_object(guid)
    u = o.Attributes.UserDictionary
    for name, value in iter(attr.items()):
        try:
            u.Set(name, value)
        except Exception:
            print("The following item cannot be stored in the user dictionary of this object: {0} => {1}".format(name, value))


def get_object_attributes_from_name(guids, prefix=None):
    """Get attributes from JSON parsable object names.

    Parameters
    ----------
    guids : list[System.Guid]
        Object identifiers.
    prefix : str, optional
        A prefix that should be removed before the name is JSON parsable.
        For example, in Rhino 6 and above, names can't start with curly braces ("{").
        Therefore, to make the string representation of a dict a valid name it has to be prefixed with something.
        This prefix can be stripped automatically using this parameter.

    Returns
    -------
    list[dict[str, Any]]
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


def is_curve_line(guid):
    """Verify that a curve is really a line.

    Parameters
    ----------
    guid : System.Guid
        The identifier of the curve.

    Returns
    -------
    bool
        True if the curve is a line.
        False otherwise.

    """
    return rs.IsCurve(guid) and rs.IsLine(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) == 2


def is_curve_polyline(guid):
    """Verify that a curve is really a polyline.

    Parameters
    ----------
    guid : System.Guid
        The identifier of the curve.

    Returns
    -------
    bool
        True if the curve is a polyline.
        False otherwise.

    """
    return rs.IsCurve(guid) and rs.IsPolyline(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) > 2


def is_curve_polygon(guid):
    """Verify that a curve is really a polygon.

    Parameters
    ----------
    guid : System.Guid
        The identifier of the curve.

    Returns
    -------
    bool
        True if the curve is a polygon.
        False otherwise.

    """
    return rs.IsCurve(guid) and rs.IsCurveClosed(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) > 2


# ==============================================================================
# Delete objects
# ==============================================================================


def delete_object(guid, purge=None, redraw=True):
    """Delete Rhino object.

    Parameters
    ----------
    guid : System.Guid
        Object identifier.
    purge : None or bool, optional
        If None, the value of the global purge setting (:obj:`compas_rhino.PURGE_ON_DELETE`) will be used.
        If True, purge the object from history after deleting.
        If False, delete but don't purge.
    redraw : bool, optional
        If True, redrawing will be enabled and enacted.
        If False, redrawing will be disabled.

    Returns
    -------
    None

    """
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE
    if purge and purge_object:
        purge_objects([guid], redraw=redraw)
    else:
        delete_objects([guid], purge, redraw=redraw)


def delete_objects(guids, purge=None, redraw=True):
    """Delete multiple Rhino objects.

    Parameters
    ----------
    guids : list[System.Guid]
        Object identifiers.
    purge : None or bool, optional
        If None, the value of the global purge setting (:obj:`compas_rhino.PURGE_ON_DELETE`) will be used.
        If True, purge the objects from history after deleting.
        If False, delete but don't purge.
    redraw : bool, optional
        If True, redrawing will be enabled and enacted.
        If False, redrawing will be disabled.

    Returns
    -------
    None

    """
    if purge is None:
        purge = compas_rhino.PURGE_ON_DELETE
    if purge and purge_object:
        purge_objects(guids, redraw=redraw)
    else:
        rs.EnableRedraw(False)
        for guid in guids:
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
        rs.DeleteObjects(guids)
        if redraw:
            rs.EnableRedraw(True)
            sc.doc.Views.Redraw()


def purge_objects(guids, redraw=True):
    """Purge objects from memory.

    Parameters
    ----------
    guids : list[System.Guid]
        Object identifiers.
    redraw : bool, optional
        If True, redrawing will be enabled and enacted.
        If False, redrawing will be disabled.

    Returns
    -------
    None

    """
    if not purge_object:
        raise RuntimeError("Cannot purge outside Rhino script context")
    rs.EnableRedraw(False)
    for guid in guids:
        if rs.IsObject(guid):
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
            o = find_object(guid)
            purge_object(o.RuntimeSerialNumber)
    if redraw:
        rs.EnableRedraw(True)
        sc.doc.Views.Redraw()


# ==============================================================================
# Select objects
# ==============================================================================


def select_object(message="Select an object."):
    """Select one object in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected object.

    """
    return rs.GetObject(message)


def select_objects(message="Select multiple objects."):
    """Select multiple objects in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected objects.

    """
    return rs.GetObjects(message)


def select_point(message="Select one point."):
    """Select one point in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected point.

    """
    return rs.GetObject(message, preselect=True, select=True, filter=rs.filter.point)


def select_points(message="Select multiple points."):
    """Select multiple points in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected points.

    """
    return rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.point)


def select_curve(message="Select one curve."):
    """Select one curve in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected curve.

    """
    return rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)


def select_curves(message="Select multiple curves."):
    """Select multiple curves in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected curves.

    """
    return rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)


def select_line(message="Select line."):
    """Select one line in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected line.

    """
    guid = rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)
    if is_curve_line(guid):
        return guid
    return None


def select_lines(message="Select multiple lines."):
    """Select multiple lines in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected lines.

    """
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    return [guid for guid in temp if is_curve_line(guid)]


def select_polyline(
    message="Select one polyline (curve with degree = 1, and multiple segments).",
):
    """Select one polyline in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected polyline.

    """
    guid = rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)
    if is_curve_polyline(guid):
        return guid
    return None


def select_polylines(
    message="Select multiple polylines (curves with degree = 1, and multiple segments).",
):
    """Select multiple polylines in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected polylines.

    """
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    return [guid for guid in temp if is_curve_polyline(guid)]


def select_polygon(message="Select one polygon (closed curve with degree = 1)"):
    """Select one polygon in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected polygon.

    """
    guid = rs.GetObject(message, preselect=True, select=True, filter=rs.filter.curve)
    if is_curve_polygon(guid):
        return guid
    return None


def select_polygons(message="Select multiple polygons (closed curves with degree = 1)"):
    """Select multiple polygons in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected polygons.

    """
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.curve)
    return [guid for guid in temp if is_curve_polygon(guid)]


def select_surface(message="Select one surface."):
    """Select one surface in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected surface.

    """
    return rs.GetObject(
        message,
        preselect=True,
        select=True,
        filter=rs.filter.surface | rs.filter.polysurface,
    )


def select_surfaces(message="Select multiple surfaces."):
    """Select multiple surfaces in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected surfaces.

    """
    return rs.GetObjects(
        message,
        preselect=True,
        select=True,
        group=False,
        filter=rs.filter.surface | rs.filter.polysurface,
    )


def select_mesh(message="Select one mesh."):
    """Select one mesh in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    System.Guid
        The identifer of the selected mesh.

    """
    return rs.GetObject(message, preselect=True, select=True, filter=rs.filter.mesh)


def select_meshes(message="Select multiple meshes."):
    """Select multiple meshes in the Rhino view.

    Parameters
    ----------
    message : str, optional
        Instruction for the user.

    Returns
    -------
    list[System.Guid]
        The identifers of the selected meshs.

    """
    guids = []
    temp = rs.GetObjects(message, preselect=True, select=True, group=False, filter=rs.filter.mesh)
    if temp:
        guids = temp
    return guids
