from shapely.geometry import Polygon

from compas.plugins import plugin


@plugin(category="booleans", requires=["shapely"])
def boolean_union_polygon_polygon(A, B):
    """Compute the boolean union of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean union.

    See Also
    --------
    boolean_difference_polygon_polygon
    boolean_symmetric_difference_polygon_polygon
    boolean_intersection_polygon_polygon

    """
    a = Polygon([point[:2] for point in A.points])
    b = Polygon([point[:2] for point in B.points])

    c = a.union(b)

    return list(c.exterior.coords)  # type: ignore


@plugin(category="booleans", requires=["shapely"])
def boolean_difference_polygon_polygon(A, B):
    """Compute the boolean differencen of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean difference.

    See Also
    --------
    boolean_union_polygon_polygon
    boolean_symmetric_difference_polygon_polygon
    boolean_intersection_polygon_polygon

    """
    a = Polygon([point[:2] for point in A.points])
    b = Polygon([point[:2] for point in B.points])

    c = a.difference(b)

    return list(c.exterior.coords)  # type: ignore


@plugin(category="booleans", requires=["shapely"])
def boolean_symmetric_difference_polygon_polygon(A, B):
    """Compute the boolean symmetric difference of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[list[point]]
        The lists of vertices of the boolean symmetric difference.

    See Also
    --------
    boolean_union_polygon_polygon
    boolean_difference_polygon_polygon
    boolean_intersection_polygon_polygon

    """
    a = Polygon([point[:2] for point in A.points])
    b = Polygon([point[:2] for point in B.points])

    c = a.symmetric_difference(b)

    return [list(polygon.exterior.coords) for polygon in c.geoms]  # type: ignore


@plugin(category="booleans", requires=["shapely"])
def boolean_intersection_polygon_polygon(A, B):
    """Compute the boolean intersection of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean difference.

    See Also
    --------
    boolean_union_polygon_polygon
    boolean_difference_polygon_polygon
    boolean_symmetric_difference_polygon_polygon

    """
    a = Polygon([point[:2] for point in A.points])
    b = Polygon([point[:2] for point in B.points])

    c = a.intersection(b)

    return list(c.exterior.coords)  # type: ignore
