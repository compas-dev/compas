from compas.plugins import plugin
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely import is_ccw


# @plugin(category="offset", requires=["shapely"])
# def offset_line(line, distance, **kwargs):
#     """Offset a line by a distance.

#     Parameters
#     ----------
#     line : :class:`~compas.geometry.Line`
#         A line defined by two points.
#     distance : float
#         The offset distance as float.

#     Returns
#     -------
#     list[point]
#         The two points of the offseted line.

#     Notes
#     -----
#     The side is determined by the sign of the distance parameter
#     (negative for right side offset, positive for left side offset).

#     """
#     linestring = LineString((line.start, line.end))
#     offset = linestring.offset_curve(distance)
#     return list(offset.coords)


@plugin(category="offset", requires=["shapely"])
def offset_polyline(polyline, distance, join_style="sharp", sharp_limit=5, **kwargs):
    """Offset a polyline by a distance.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A polyline defined by a sequence of points.
    distance : float
        The offset distance as float.
    join_style : {"sharp", "round", "chamfer"}
        Specifies the shape of offsetted line midpoints. "round" results in rounded shapes.
        "chamfer" results in a chamfered edge that touches the original vertex. "sharp" results in a single vertex
        that is chamfered depending on the sharp_limit parameter. Defaults to "sharp".
    sharp_limit: float, optional
        The sharp limit ratio is used for very sharp corners. The sharp ratio is the ratio of the distance
        from the corner to the end of the chamfered offset corner. When two line segments meet at a sharp angle,
        a sharp join will extend the original geometry. To prevent unreasonable geometry,
        the sharp limit allows controlling the maximum length of the join corner.
        Corners with a ratio which exceed the limit will be chamfered.

    Returns
    -------
    list[point]
        The points of the offseted polyline.

    Notes
    -----
    The side is determined by the sign of the distance parameter
    (negative for right side offset, positive for left side offset).

    """
    join_styles = ("round", "sharp", "chamfer")
    try:
        join_style_int = join_styles.index(join_style.lower()) + 1
    except ValueError:
        print("Join styles supported are round, sharp and chamfer.")
    linestring = LineString(polyline.points)
    offset = linestring.offset_curve(distance, join_style=join_style_int, mitre_limit=sharp_limit)
    return list(offset.coords)


@plugin(category="offset", requires=["shapely"])
def offset_polygon(polygon, distance, join_style="sharp", sharp_limit=5, **kwargs):
    """Offset a polygon by a distance.

    Parameters
    ----------
    polygon : :class:`~compas.geometry.Polygon`
        A polygon defined by a sequence of vertices.
    distance : float
        The offset distance as float.
    join_style : {"sharp", "round", "chamfer"}
        Specifies the shape of offsetted line midpoints. "round" results in rounded shapes.
        "chamfer" results in a chamfered edge that touches the original vertex. "sharp" results in a single vertex
        that is chamfered depending on the sharp_limit parameter. Defaults to "sharp".
    sharp_limit: float, optional
        The sharp limit ratio is used for very sharp corners. The sharp ratio is the ratio of the distance
        from the corner to the end of the chamfered offset corner. When two line segments meet at a sharp angle,
        a sharp join will extend the original geometry. To prevent unreasonable geometry,
        the sharp limit allows controlling the maximum length of the join corner.
        Corners with a ratio which exceed the limit will be chamfered.

    Returns
    -------
    list[point]
        The vertices of the offseted polygon.

    Notes
    -----
    The offset direction is determined by the provided normal vector.
    If the polyline is in the XY plane and the normal is along the positive Z axis,
    positive offset distances will result in counterclockwise offsets,
    and negative values in clockwise direction.

    """
    join_styles_dict = {"round": "round", "sharp": "mitre", "chamfer": "bevel"}
    join_style = join_styles_dict.get(join_style)
    if not join_style:
        raise ValueError("Join styles supported are round, sharp and chamfer.")
    pgon = Polygon(polygon.points)
    offset = pgon.buffer(-distance, join_style=join_style, mitre_limit=sharp_limit, single_sided=True)
    if is_ccw(pgon.exterior):
        return list(offset.reverse().exterior.coords)
    return list(offset.exterior.coords)
