from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import array
from numpy import asarray
from numpy import argmax
from numpy import argmin
from numpy import amax
from numpy import amin
from numpy import dot
# from numpy import ptp
from numpy import sum

from scipy.spatial import ConvexHull
# from scipy.spatial import QhullError

from compas.geometry import local_axes
from compas.geometry import world_to_local_coordinates_numpy
from compas.geometry import local_to_world_coordinates_numpy
from compas.geometry import transform_points_numpy
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.numerical import pca_numpy

from compas.geometry.bbox.bbox import bounding_box


__all__ = [
    'oriented_bounding_box_numpy',
    'oriented_bounding_box_xy_numpy',
    'oabb_numpy'
]


# make alternative implementation using PCA
# compare results
def oriented_bounding_box_numpy(points):
    r"""Compute the oriented minimum bounding box of a set of points in 3D space.

    Parameters
    ----------
    points : array-like
        XYZ coordinates of the points.

    Returns
    -------
    array
        XYZ coordinates of 8 points defining a box.

    Raises
    ------
    QhullError
        If the data is essentially 2D.

    Notes
    -----
    The *oriented (minimum) bounding box* (OBB) of a given set of points
    is computed using the following procedure:

    1. Compute the convex hull of the points.
    2. For each of the faces on the hull:

       1. Compute face frame.
       2. Compute coordinates of other points in face frame.
       3. Find "peak-to-peak" (PTP) values of point coordinates along local axes.
       4. Compute volume of box formed with PTP values.

    3. Select the box with the smallest volume.

    Examples
    --------
    Generate a random set of points with
    :math:`x \in [0, 10]`, :math:`y \in [0, 1]` and :math:`z \in [0, 3]`.
    Add the corners of the box such that we now the volume is supposed to be :math:`30.0`.

    >>> points = numpy.random.rand(10000, 3)
    >>> bottom = numpy.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])
    >>> top = numpy.array([[0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0]])
    >>> points = numpy.concatenate((points, bottom, top))
    >>> points[:, 0] *= 10
    >>> points[:, 2] *= 3

    Rotate the points around an arbitrary axis by an arbitrary angle.

    >>> from compas.geometry import Rotation
    >>> from compas.geometry import transform_points_numpy
    >>> R = Rotation.from_axis_and_angle([1.0, 1.0, 0.0], 0.3 * 3.14159)
    >>> points = transform_points_numpy(points, R)

    Compute the volume of the oriented bounding box.

    >>> bbox = oriented_bounding_box_numpy(points)
    >>> a = length_vector(subtract_vectors(bbox[1], bbox[0]))
    >>> b = length_vector(subtract_vectors(bbox[3], bbox[0]))
    >>> c = length_vector(subtract_vectors(bbox[4], bbox[0]))
    >>> close(a * b * c, 30.)
    True

    """
    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]

    try:
        hull = ConvexHull(points)
    except Exception:
        return oabb_numpy(points)
        # if 'QH6154' in str(e):
        #     hull = ConvexHull(points, qhull_options='Qb2:0B2:0')
        # else:
        #     raise e

    hull = ConvexHull(points)

    volume = None
    bbox = []

    # this can be vectorised!
    for simplex in hull.simplices:
        a, b, c = points[simplex]
        uvw = local_axes(a, b, c)
        xyz = points[hull.vertices]
        frame = [a, uvw[0], uvw[1]]
        rst = world_to_local_coordinates_numpy(frame, xyz)
        rmin, smin, tmin = amin(rst, axis=0)
        rmax, smax, tmax = amax(rst, axis=0)
        dr = rmax - rmin
        ds = smax - smin
        dt = tmax - tmin
        v = dr * ds * dt

        if volume is None or v < volume:
            bbox = [
                [rmin, smin, tmin],
                [rmax, smin, tmin],
                [rmax, smax, tmin],
                [rmin, smax, tmin],
                [rmin, smin, tmax],
                [rmax, smin, tmax],
                [rmax, smax, tmax],
                [rmin, smax, tmax],
            ]
            bbox = local_to_world_coordinates_numpy(frame, bbox)
            volume = v

    return bbox


def oriented_bounding_box_xy_numpy(points):
    """Compute the oriented minimum bounding box of set of points in the XY plane.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    list
        XYZ coordinates of 8 points defining a box.

    Notes
    -----
    The *oriented (minimum) bounding box* (OBB) is computed using the following
    procedure:

    1. Compute the convex hull of the points.
    2. For each of the edges on the hull:

       1. Compute the s-axis as the unit vector in the direction of the edge
       2. Compute the othorgonal t-axis.
       3. Use the start point of the edge as origin.
       4. Compute the spread of the points along the s-axis. (dot product of the point vecor in local coordinates and the s-axis)
       5. Compute the spread along the t-axis.
       6. Determine the side of s on which the points are.
       7. Compute and store the corners of the bbox and its area.

    3. Select the box with the smallest area.

    Examples
    --------
    >>>

    """
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]

    hull = ConvexHull(points)
    xy_hull = points[hull.vertices].reshape((-1, 2))

    boxes = []
    m = sum(xy_hull, axis=0) / n

    for simplex in hull.simplices:
        p0 = points[simplex[0]]
        p1 = points[simplex[1]]

        # s direction
        s = p1 - p0
        sl = sum(s ** 2) ** 0.5
        su = s / sl
        vn = xy_hull - p0
        sc = (sum(vn * s, axis=1) / sl).reshape((-1, 1))
        scmax = argmax(sc)
        scmin = argmin(sc)

        # box corners
        b0 = p0 + sc[scmin] * su
        b1 = p0 + sc[scmax] * su

        # t direction
        t = array([-s[1], s[0]])
        tl = sum(t ** 2) ** 0.5
        tu = t / tl
        vn = xy_hull - p0
        tc = (sum(vn * t, axis=1) / tl).reshape((-1, 1))
        tcmax = argmax(tc)
        tcmin = argmin(tc)

        # area
        w = sc[scmax] - sc[scmin]
        h = tc[tcmax] - tc[tcmin]
        a = w * h

        # box corners
        if dot(t, m - p0) < 0:
            b3 = b0 - h * tu
            b2 = b1 - h * tu
        else:
            b3 = b0 + h * tu
            b2 = b1 + h * tu

        # box
        boxes.append([[b0, b1, b2, b3], a[0]])

    # return the box with the smallest area
    return [point.tolist() for point in min(boxes, key=lambda b: b[1])[0]]


def oabb_numpy(points):
    origin, (xaxis, yaxis, zaxis), values = pca_numpy(points)
    frame = Frame(origin, xaxis, yaxis)
    world = Frame.worldXY()
    X = Transformation.from_frame_to_frame(frame, world)
    points = transform_points_numpy(points, X)
    bbox = bounding_box(points)
    bbox = transform_points_numpy(bbox, X.inverse())
    return bbox


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    import numpy  # noqa: F401
    import math  # noqa: F401

    from compas.geometry import bounding_box  # noqa: F401 F811
    from compas.geometry import subtract_vectors  # noqa: F401
    from compas.geometry import length_vector  # noqa: F401
    from compas.geometry import Rotation  # noqa: F401
    from compas.geometry import transform_points_numpy  # noqa: F401 F811
    from compas.geometry import allclose  # noqa: F401
    from compas.geometry import close  # noqa: F401

    doctest.testmod(globs=globals())
