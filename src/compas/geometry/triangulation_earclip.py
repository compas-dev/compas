from compas.geometry import is_ccw_xy, is_point_in_triangle_xy


def earclip_polygon(polygon):
    """Triangulate a polygon using the ear clipping method.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon` | list[:class:`compas.geometry.Point`]
        A polygon defined by a sequence of points.

    Returns
    -------
    list[[point, point, point]]
        A list of triangles.

    Raises
    ------
    Exception
        If not all points were consumed by the procedure.

    """

    def find_ear(points, point_index):
        p = len(points)
        if p == 3:
            triangle = [
                point_index[id(points[0])],
                point_index[id(points[1])],
                point_index[id(points[2])],
            ]
            del points[2]
            del points[1]
            del points[0]
            return triangle
        for i in range(-2, p - 2):
            a = points[i]
            b = points[i + 1]
            c = points[i + 2]
            is_valid = True
            if not is_ccw_xy(b, c, a):
                continue
            for j in range(p):
                if j == i or j == i + 1 or j == i + 2:
                    continue
                if is_point_in_triangle_xy(points[j], (a, b, c)):
                    is_valid = False
                    break
            if is_valid:
                del points[i + 1]
                return [point_index[id(a)], point_index[id(b)], point_index[id(c)]]

    points = list(polygon)
    point_index = {id(point): index for index, point in enumerate(points)}

    triangles = []
    while len(points) >= 3:
        ear = find_ear(points, point_index)
        triangles.append(ear)

    if points:
        raise Exception("Not all points were consumed by the clipping procedure.")

    return triangles
