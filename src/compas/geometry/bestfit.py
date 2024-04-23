from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points
from compas.geometry import normalize_vector
from compas.geometry import subtract_vectors


def bestfit_plane(points):
    """Fit a plane to a list of (more than three) points.

    Parameters
    ----------
    points : sequence[point]
        A list of points represented by their XYZ coordinates.

    Returns
    -------
    [float, float, float]
        Base point.
    [float, float, float]
        Normal vector (normalized).

    See Also
    --------
    :func:`compas.geometry.bestfit_plane_numpy`

    Notes
    -----
    This method will minimize the squares of the residuals as perpendicular
    to the main axis, not the residuals perpendicular to the plane. If the
    residuals are small (i.e. your points all lie close to the resulting plane),
    then this method will probably suffice. However, if your points are more
    spread then this method may not be the best fit. For more information see
    [ernerfeldt2015]_

    References
    ----------
    .. [ernerfeldt2015] Ernerfeldt, E. *Fitting a plane to many points in 3D*.
                        Available at: http://www.ilikebigbits.com/blog/2015/3/2/plane-from-points

    """
    centroid = centroid_points(points)

    xx, xy, xz = 0.0, 0.0, 0.0
    yy, yz, zz = 0.0, 0.0, 0.0

    for point in points:
        rx, ry, rz = subtract_vectors(point, centroid)
        xx += rx * rx
        xy += rx * ry
        xz += rx * rz
        yy += ry * ry
        yz += ry * rz
        zz += rz * rz

    det_x = yy * zz - yz * yz
    det_y = xx * zz - xz * xz
    det_z = xx * yy - xy * xy

    det_max = max(det_x, det_y, det_z)

    if det_max == det_x:
        a = (xz * yz - xy * zz) / det_x
        b = (xy * yz - xz * yy) / det_x
        normal = (1.0, a, b)
    elif det_max == det_y:
        a = (yz * xz - xy * zz) / det_y
        b = (xy * xz - yz * xx) / det_y
        normal = (a, 1.0, b)
    else:
        a = (yz * xy - xz * yy) / det_z
        b = (xz * xy - yz * xx) / det_z
        normal = (a, b, 1.0)

    return centroid, normalize_vector(normal)
